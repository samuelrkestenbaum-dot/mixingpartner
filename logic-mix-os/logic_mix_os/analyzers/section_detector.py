"""Audio-driven section detector (P-059).

Deterministic. numpy + first-party :mod:`dsp` only — **no new dependency**.

Infers arrangement sections from *what enters and exits over time*: each stem's
active region across a common frame grid is an arrangement event, and the frames
where the *set of active stems* changes are section boundaries. This is the
honest reading of the user's directive — "based on what's added at various
points". It is used ONLY when the manifest supplies fewer than two sections (see
``pipeline.analyze``); a manifest with >=2 sections is never touched, which is
the whole byte-stability guarantee for the pinned corpus.

Labels are HONEST: a structural ``Section N`` plus a relative ``energy_tag``
(high/med/low from the section's mean active-stem-count). There is deliberately
**no verse/chorus/bridge naming** — musical function is not inferable from audio
alone; the user renames in the manifest if they want function names.

The mixdown RMS/density novelty is a *corroborating tie-breaker only* — it never
creates a boundary on its own (energy alone reacts to WITHIN-section dynamics,
exactly the artifact this packet exists to avoid). Arrangement activity stays
primary.
"""

from __future__ import annotations

from typing import Dict, List

import numpy as np

from .. import dsp
from ..project import Section
from .audio_loader import LoadedAudio

# --------------------------------------------------------------------------- #
# Constants — the whole detector is a fixed grid + fixed thresholds, no
# randomness, so the same stems always yield the same sections.
# --------------------------------------------------------------------------- #
H = 0.25  # frame-grid hop, seconds

# Two-part silence gate: a stem is active in a frame when its RMS is above BOTH
# an absolute floor AND a level relative to that stem's own loudest frame.
ABS_FLOOR_DB = -50.0
REL_RANGE_DB = 40.0

# Debounce / hysteresis, expressed in seconds then resolved to frame counts so
# the intent (~5.0s persistence, ~0.5s gap-fill, ~2.0s boundary cluster) is
# legible and tracks H if H ever changes.
#
# P-061 — the persistence floor is the ORNAMENT/ARRANGEMENT line. At 0.5s a 3-4s
# guitar stab or percussion fill read as an entrance AND an exit, carving
# ornament-sized sections out of the middle of a real block; on a real 49-track
# song that shredded the arrangement into 12 micro-sections and, via the
# per-section dispersion the doctrine engine reads, pinned contrast/dynamics at
# a fake 100/100. A stem presence too short to ever be its own section is not an
# arrangement event — it is an ornament INSIDE one.
_MIN_RUN_SEC = 5.0
_GAP_SEC = 0.5
_CLUSTER_SEC = 2.0
MIN_RUN = max(1, round(_MIN_RUN_SEC / H))       # a state change must persist >= this
GAP = max(1, round(_GAP_SEC / H))               # inactive gaps <= this are filled
CLUSTER_WIN = max(1, round(_CLUSTER_SEC / H))   # boundaries within this collapse to one

# Guardrails.
#
# P-061 — MIN_SECTION_SEC is the section floor; MAX_SECTIONS is a pathological-
# input safety valve, NOT a routine shaper. Whenever the cap binds it drops
# boundaries by novelty alone, with no regard for spacing, which manufactures a
# super-block next to short sections — the very artifact this constant set
# exists to remove. So the floor does the work and the cap stays loose enough
# that an honest arrangement passes through it untouched.
MIN_SECTION_SEC = 7.0   # sections shorter than this merge into a neighbour
MAX_SECTIONS = 12       # cap; keep the highest arrangement-novelty boundaries

_TAG_LOW = 1.0 / 3.0
_TAG_HIGH = 2.0 / 3.0


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def detect_sections(
    loaded_by_id: Dict[str, LoadedAudio],
    mixdown: LoadedAudio,
    duration: float,
) -> List[Section]:
    """Infer arrangement sections from per-stem entry/exit events.

    ``loaded_by_id`` maps ``track_id`` -> decoded stem; ``mixdown`` supplies the
    secondary energy-novelty tie-breaker; ``duration`` (seconds) sets the grid.
    Returns a list of :class:`~logic_mix_os.project.Section`, each carrying
    ``inferred=True`` and a relative ``energy_tag`` — ready to feed the SAME
    ``analyze_sections`` a supplied section list would.
    """
    n_frames = max(1, int(duration / H))

    # Determinism: always iterate stems in a fixed (track_id) order.
    stems = [loaded_by_id[tid] for tid in sorted(loaded_by_id)]
    activity = _activity_matrix(stems, n_frames)          # (n_stems, n_frames) bool
    novelty = _novelty(activity)                          # (n_frames,) int
    energy_novelty = _frame_novelty(mixdown, n_frames)    # (n_frames,) float, tie-break only

    boundaries = _boundaries(novelty, energy_novelty, n_frames)
    boundaries = _merge_short_sections(boundaries, n_frames)
    boundaries = _cap_sections(boundaries)
    return _build_sections(boundaries, activity, n_frames, duration)


def annotate_inferred(
    section_analysis: List[Dict], sections: List[Section]
) -> List[Dict]:
    """Stamp analyzed-section dicts from detected sections (detected path only).

    Adds ``inferred: True`` + the section's ``energy_tag`` to each analyzed
    entry, in order. Called ONLY on the auto-detect branch in ``pipeline.analyze``
    — the supplied-section output shape is never touched.
    """
    for entry, sec in zip(section_analysis, sections):
        entry["inferred"] = True
        entry["energy_tag"] = sec.energy_tag
    return section_analysis


# --------------------------------------------------------------------------- #
# Per-frame RMS on the common grid
# --------------------------------------------------------------------------- #
def _frame_rms_db(mono: np.ndarray, sample_rate: int, n_frames: int) -> np.ndarray:
    """Per-frame RMS in dBFS over ``n_frames`` non-overlapping H-second frames.

    Mirrors ``dsp.rms`` + ``dsp.db_from_amplitude`` (EPS inside the sqrt, a
    -120 dB floor) vectorised across the grid. A stem shorter than the grid is
    zero-padded past its end — so it reads as silent there, i.e. an EXIT.
    """
    hop_n = max(1, int(round(H * sample_rate)))
    need = n_frames * hop_n
    m = np.asarray(mono, dtype=np.float64)[:need]
    if m.size < need:
        m = np.concatenate([m, np.zeros(need - m.size, dtype=np.float64)])
    frames = m.reshape(n_frames, hop_n)
    rms = np.sqrt(np.mean(frames * frames, axis=1) + dsp.EPS)
    floor = 10 ** (-120 / 20)
    return 20.0 * np.log10(np.maximum(rms, floor))


def _activity_matrix(stems: List[LoadedAudio], n_frames: int) -> np.ndarray:
    if not stems:
        return np.zeros((0, n_frames), dtype=bool)
    rows = []
    for stem in stems:
        db = _frame_rms_db(dsp.to_mono(stem.samples), stem.sample_rate, n_frames)
        peak_db = float(np.max(db))
        thresh = max(ABS_FLOOR_DB, peak_db - REL_RANGE_DB)
        rows.append(_debounce(db > thresh))
    return np.vstack(rows)


# --------------------------------------------------------------------------- #
# Debounce / hysteresis
# --------------------------------------------------------------------------- #
def _runs(mask: np.ndarray):
    """Maximal constant runs as ``(start, end_exclusive, value)`` tuples."""
    out = []
    n = len(mask)
    i = 0
    while i < n:
        j = i + 1
        while j < n and bool(mask[j]) == bool(mask[i]):
            j += 1
        out.append((i, j, bool(mask[i])))
        i = j
    return out


def _debounce(active: np.ndarray) -> np.ndarray:
    a = np.asarray(active, dtype=bool).copy()
    # 1) fill short INACTIVE gaps bounded by activity on both sides (a breath /
    #    rest must not toggle a stem off).
    runs = _runs(a)
    for k, (s, e, val) in enumerate(runs):
        if not val and (e - s) <= GAP and 0 < k < len(runs) - 1:
            a[s:e] = True
    # 2) drop ACTIVE blips shorter than the persistence floor.
    for s, e, val in _runs(a):
        if val and (e - s) < MIN_RUN:
            a[s:e] = False
    return a


# --------------------------------------------------------------------------- #
# Novelty
# --------------------------------------------------------------------------- #
def _novelty(activity: np.ndarray) -> np.ndarray:
    """Per-frame count of stems whose active-state changed vs the prior frame."""
    n_frames = activity.shape[1]
    nov = np.zeros(n_frames, dtype=int)
    if activity.shape[0] == 0:
        return nov
    changed = activity[:, 1:] != activity[:, :-1]
    nov[1:] = np.sum(changed, axis=0)
    return nov


def _frame_novelty(mixdown: LoadedAudio, n_frames: int) -> np.ndarray:
    """Mixdown RMS-density novelty on the grid — the corroborating tie-breaker."""
    db = _frame_rms_db(dsp.to_mono(mixdown.samples), mixdown.sample_rate, n_frames)
    en = np.zeros(n_frames, dtype=np.float64)
    if n_frames > 1:
        en[1:] = np.abs(np.diff(db))
    return en


# --------------------------------------------------------------------------- #
# Boundary picking + guardrails
# --------------------------------------------------------------------------- #
def _boundaries(novelty: np.ndarray, energy_novelty: np.ndarray, n_frames: int):
    """Cluster novel frames into boundaries. Returns ``[(frame, magnitude), ...]``
    with ``frame 0`` always first. Arrangement novelty is the sole boundary
    maker; the mixdown energy novelty only breaks ties on the cluster's
    representative frame."""
    candidates = [f for f in range(1, n_frames) if novelty[f] >= 1]
    clusters: List[List[int]] = []
    for f in candidates:
        if clusters and f - clusters[-1][-1] <= CLUSTER_WIN:
            clusters[-1].append(f)
        else:
            clusters.append([f])

    boundaries = [(0, 0.0)]  # t=0 is always the first boundary
    for cl in clusters:
        # representative = strongest arrangement novelty; ties -> stronger
        # mixdown energy novelty (secondary signal); then earliest frame.
        rep = max(cl, key=lambda f: (novelty[f], energy_novelty[f], -f))
        magnitude = float(sum(int(novelty[f]) for f in cl))
        boundaries.append((rep, magnitude))
    return boundaries


def _merge_short_sections(boundaries, n_frames: int):
    """Merge any section shorter than ``MIN_SECTION_SEC`` into a neighbour by
    dropping one boundary. The first section (which owns t=0) merges rightward;
    every other short section merges leftward."""
    b = sorted(boundaries, key=lambda x: x[0])
    min_frames = MIN_SECTION_SEC / H
    while len(b) > 1:
        edges = [x[0] for x in b] + [n_frames]
        lengths = [edges[i + 1] - edges[i] for i in range(len(b))]
        i = min(range(len(b)), key=lambda k: (lengths[k], k))
        if lengths[i] >= min_frames:
            break
        del b[1 if i == 0 else i]
    return b


def _cap_sections(boundaries):
    """Keep at most ``MAX_SECTIONS`` boundaries: t=0 plus the highest-novelty
    survivors (ties -> earliest)."""
    if len(boundaries) <= MAX_SECTIONS:
        return boundaries
    head = boundaries[0]  # frame 0 is always kept
    rest = sorted(boundaries[1:], key=lambda x: (-x[1], x[0]))[: MAX_SECTIONS - 1]
    return sorted([head] + rest, key=lambda x: x[0])


# --------------------------------------------------------------------------- #
# Section assembly + energy tags
# --------------------------------------------------------------------------- #
def _energy_tags(frames: List[int], activity: np.ndarray, n_frames: int) -> List[str]:
    """A relative high/med/low tag per section from its mean active-stem-count."""
    if activity.shape[0] == 0 or len(frames) == 1:
        return ["med"] * len(frames)
    edges = frames + [n_frames]
    means = []
    for i in range(len(frames)):
        s, e = edges[i], edges[i + 1]
        means.append(float(np.mean(np.sum(activity[:, s:e], axis=0))) if e > s else 0.0)
    arr = np.array(means)
    lo, hi = float(arr.min()), float(arr.max())
    if hi - lo < 1e-9:
        return ["med"] * len(frames)
    tags = []
    for v in (arr - lo) / (hi - lo):
        tags.append("low" if v < _TAG_LOW else "high" if v > _TAG_HIGH else "med")
    return tags


def _build_sections(boundaries, activity: np.ndarray, n_frames: int, duration: float):
    frames = [x[0] for x in boundaries]
    tags = _energy_tags(frames, activity, n_frames)
    sections: List[Section] = []
    for i, f in enumerate(frames):
        start = round(f * H, 3)
        end = round(frames[i + 1] * H if i + 1 < len(frames) else duration, 3)
        sections.append(
            Section(
                section_id=f"section_{i + 1}",
                name=f"Section {i + 1}",
                start=start,
                end=end,
                emotional_goal=None,
                energy_tag=tags[i],
                inferred=True,
            )
        )
    return sections
