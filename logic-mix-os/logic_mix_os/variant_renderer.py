"""Offline variant renderer + before/after compare loop (Hardening Packet 2).

The first real *try -> hear -> compare* loop: apply a bounded, reversible set of
mix moves to the stems, re-bounce to an actual WAV, and compare the render to the
base — including a mandatory **loudness-matched** comparison so the system can't
mistake "louder" for "better".

This is a deliberate OFFLINE APPROXIMATION of Logic's processing (zero-phase FFT
EQ, a simple synthetic reverb, mid/side width). It is good enough to make the
loop real and testable here; ground-truth Logic renders come via the (later)
ingest path. Nothing here touches a Logic session or any source file — it reads
stems and writes new bounces only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from . import dsp
from .analyzers.audio_loader import LoadedAudio, load_audio, write_wav
from .analyzers.audio_metrics import compute_metrics
from .analyzers.section_analyzer import analyze_sections, resolve_section_bounds
from .analyzers.translation_analyzer import analyze_translation
from .constants import LOOP_SAMPLE_KINDS, VOCAL_PRESENCE_BAND

# Moves the offline renderer can approximate. Anything else is reported as
# unmapped rather than silently dropped (guardrail 3).
SUPPORTED_OPS = {"gain", "pan", "width", "eq", "reverb_send", "mute", "fade"}

# Phrases in a variant's change list that the offline renderer cannot do.
_UNSUPPORTED_MARKERS = [
    "delay throw", "sidechain", "chop", "reverse", "re-pitch", "repitch",
    "formant", "one-shot", "one shot", "tuning", "modulation", "envelope",
]


# --------------------------------------------------------------------------- #
# Render result
# --------------------------------------------------------------------------- #
@dataclass
class RenderResult:
    mixdown: LoadedAudio
    stems: Dict[str, LoadedAudio]  # track_id -> processed stereo stem
    applied_ops: List[Dict] = field(default_factory=list)
    unmapped_changes: List[str] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# Per-track DSP (operate on stereo (n, 2) float arrays)
# --------------------------------------------------------------------------- #
def _stereo(samples: np.ndarray) -> np.ndarray:
    s = np.asarray(samples, dtype=np.float64)
    if s.ndim == 1:
        return np.column_stack([s, s])
    return s[:, :2]


def _apply_gain(stereo: np.ndarray, db: float) -> np.ndarray:
    return stereo * (10.0 ** (db / 20.0))


def _apply_width(stereo: np.ndarray, factor: float) -> np.ndarray:
    left, right = stereo[:, 0], stereo[:, 1]
    mid = (left + right) * 0.5
    side = (left - right) * 0.5 * factor
    return np.column_stack([mid + side, mid - side])


def _apply_pan(stereo: np.ndarray, pos: float) -> np.ndarray:
    pos = max(-1.0, min(1.0, pos))
    angle = (pos + 1.0) / 2.0 * (np.pi / 2.0)
    gl, gr = np.cos(angle) * 1.41421356, np.sin(angle) * 1.41421356
    return np.column_stack([stereo[:, 0] * gl, stereo[:, 1] * gr])


def _eq_curve(freqs: np.ndarray, typ: str, f0: float, gain_db: float, q: float) -> np.ndarray:
    g = 10.0 ** (gain_db / 20.0)
    r = freqs / max(f0, 1e-6)
    if typ == "low_shelf":
        return 1.0 + (g - 1.0) * (1.0 / (1.0 + r ** 2))
    if typ == "high_shelf":
        return 1.0 + (g - 1.0) * (r ** 2 / (1.0 + r ** 2))
    if typ == "high_pass":
        return np.sqrt(r ** 2 / (1.0 + r ** 2))  # ~1st-order HP magnitude
    if typ == "low_pass":
        return np.sqrt(1.0 / (1.0 + r ** 2))
    if typ == "bell":
        bw = max(f0 / max(q, 0.1), 1.0)
        return 1.0 + (g - 1.0) * np.exp(-0.5 * ((freqs - f0) / (bw / 2.0)) ** 2)
    return np.ones_like(freqs)


def _apply_eq(stereo: np.ndarray, sr: int, bands: List[Tuple]) -> np.ndarray:
    n = stereo.shape[0]
    if n < 4:
        return stereo
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    gain = np.ones_like(freqs)
    for (typ, f0, g_db, q) in bands:
        gain = gain * _eq_curve(freqs, typ, f0, g_db, q)
    out = np.zeros_like(stereo)
    for ch in range(2):
        out[:, ch] = np.fft.irfft(np.fft.rfft(stereo[:, ch]) * gain, n=n)
    return out


def _reverb_ir(sr: int, decay: float = 0.4, length: float = 0.5, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = max(1, int(length * sr))
    t = np.arange(n) / sr
    return rng.standard_normal(n) * np.exp(-t / max(decay, 1e-3))


def _reverb_wet(stereo: np.ndarray, level_db: float, ir: np.ndarray) -> np.ndarray:
    mono = stereo.mean(axis=1)
    n = mono.shape[0]
    wet_l = np.convolve(mono, ir)[:n]
    wet_r = np.convolve(mono, ir[::-1])[:n]
    return np.column_stack([wet_l, wet_r]) * (10.0 ** (level_db / 20.0))


def _apply_mute(stereo: np.ndarray, sr: int, ranges: List[Tuple[float, float]]) -> np.ndarray:
    if not ranges:
        return np.zeros_like(stereo)
    out = stereo.copy()
    for (start, end) in ranges:
        a = max(0, int(start * sr))
        b = min(out.shape[0], int(end * sr))
        if b > a:
            out[a:b] = 0.0
    return out


def _pad(stereo: np.ndarray, length: int) -> np.ndarray:
    if stereo.shape[0] >= length:
        return stereo[:length]
    pad = np.zeros((length - stereo.shape[0], 2))
    return np.vstack([stereo, pad])


# --------------------------------------------------------------------------- #
# Op planning (variant -> concrete render ops) + unmapped detection
# --------------------------------------------------------------------------- #
def _targets(records: List[Dict], group: str) -> List[str]:
    if group == "supporting":
        return [r["track_id"] for r in records if r["instrument_identity"] in
                {"acoustic_guitar", "electric_guitar", "backing_vocal", "piano", "electric_piano", "strings"}]
    if group == "loops":
        return [r["track_id"] for r in records if r["source_kind"] in LOOP_SAMPLE_KINDS]
    if group == "lead_vocal":
        return [r["track_id"] for r in records if r["instrument_identity"] == "lead_vocal"]
    if group == "drum_room":
        return [r["track_id"] for r in records if r["instrument_identity"] in {"overhead", "drum_room"}]
    if group == "decorative":
        return [r["track_id"] for r in records if r["sacredness"] in {"decorative", "expendable"}]
    return []


def plan_ops(variant: Dict, records: List[Dict], sections: List) -> Tuple[List[Dict], List[str]]:
    """Map a creative variant to concrete render ops; report unmapped changes."""
    kind = variant["kind"]
    ops: List[Dict] = []
    # Resolve a "last pre-chorus / pre-lift" window for subtractive drops.
    bounds = {s.section_id: (s.start, s.end) for s in sections}

    if kind == "width_bloom":
        for tid in _targets(records, "supporting"):
            ops.append({"track_id": tid, "op": "width", "params": {"factor": 1.25}})
            ops.append({"track_id": tid, "op": "reverb_send", "params": {"level_db": -14}})
    elif kind == "subtractive_drop":
        targets = _targets(records, "loops") or _targets(records, "decorative") or _targets(records, "supporting")[-1:]
        for tid in targets:
            ops.append({"track_id": tid, "op": "mute", "params": {"sections": "all"}})
    elif kind == "vocal_ride":
        for tid in _targets(records, "lead_vocal"):
            ops.append({"track_id": tid, "op": "gain", "params": {"db": 1.0}})
    elif kind == "drum_room_bloom":
        for tid in _targets(records, "drum_room"):
            ops.append({"track_id": tid, "op": "gain", "params": {"db": 2.0}})
            ops.append({"track_id": tid, "op": "reverb_send", "params": {"level_db": -12}})
    elif kind == "depth_cleanup":
        for tid in _targets(records, "supporting"):
            ops.append({"track_id": tid, "op": "width", "params": {"factor": 0.6}})
            ops.append({"track_id": tid, "op": "gain", "params": {"db": -2.0}})
    elif kind == "loop_deconstruct":
        for tid in _targets(records, "loops"):
            ops.append({"track_id": tid, "op": "width", "params": {"factor": 0.4}})
            ops.append({"track_id": tid, "op": "eq", "params": {"bands": [("high_pass", 250.0, 0.0, 1.0)]}})
            ops.append({"track_id": tid, "op": "gain", "params": {"db": -3.0}})
    elif kind == "intimacy_pass":
        # closer vocal = less ambience; approximate by trimming a touch of air
        for tid in _targets(records, "lead_vocal"):
            ops.append({"track_id": tid, "op": "eq", "params": {"bands": [("high_shelf", 9000.0, -1.5, 1.0)]}})

    # Unmapped detection: any change the renderer can't approximate.
    unmapped: List[str] = []
    for change in variant.get("changes", []):
        low = change.lower()
        if any(mark in low for mark in _UNSUPPORTED_MARKERS):
            unmapped.append(change)
    # If the variant produced no ops at all, the whole thing is unmapped.
    if not ops:
        unmapped = unmapped or list(variant.get("changes", []))

    return ops, unmapped


# --------------------------------------------------------------------------- #
# Render
# --------------------------------------------------------------------------- #
def render(stems_raw: Dict[str, LoadedAudio], ops: List[Dict], sr: int,
           section_bounds: Dict[str, Tuple[float, float]]) -> RenderResult:
    if not stems_raw:
        raise ValueError("no stems to render")
    max_len = max(_stereo(a.samples).shape[0] for a in stems_raw.values())
    ir = _reverb_ir(sr)
    ops_by_track: Dict[str, List[Dict]] = {}
    for op in ops:
        ops_by_track.setdefault(op["track_id"], []).append(op)

    acc = np.zeros((max_len, 2))
    wet = np.zeros((max_len, 2))
    processed: Dict[str, LoadedAudio] = {}
    applied: List[Dict] = []

    for tid, loaded in stems_raw.items():
        s = _stereo(loaded.samples)
        for op in ops_by_track.get(tid, []):
            kind, p = op["op"], op.get("params", {})
            if kind == "gain":
                s = _apply_gain(s, p.get("db", 0.0))
            elif kind == "width":
                s = _apply_width(s, p.get("factor", 1.0))
            elif kind == "pan":
                s = _apply_pan(s, p.get("pos", 0.0))
            elif kind == "eq":
                s = _apply_eq(s, sr, p.get("bands", []))
            elif kind == "mute":
                ranges = list(section_bounds.values()) if p.get("sections") == "all" else p.get("ranges", [])
                s = _apply_mute(s, sr, ranges)
            elif kind == "reverb_send":
                wet += _pad(_reverb_wet(s, p.get("level_db", -14.0), ir), max_len)
            elif kind == "fade":
                pass  # reserved
            applied.append({"track_id": tid, **op})
        processed[tid] = LoadedAudio(samples=s, sample_rate=sr, path=f"<render:{tid}>")
        acc += _pad(s, max_len)

    acc += wet
    peak = float(np.max(np.abs(acc))) or 1.0
    if peak > 0.95:
        acc *= 0.95 / peak
    return RenderResult(mixdown=LoadedAudio(acc, sr, "<render:mix>"), stems=processed, applied_ops=applied)


# --------------------------------------------------------------------------- #
# Loudness match + compare
# --------------------------------------------------------------------------- #
def loudness_match(samples: np.ndarray, sr: int, target_lufs: float) -> np.ndarray:
    """Scale ``samples`` to ``target_lufs``. No peak protection on purpose: this
    signal is only *measured* (level-invariant qualities), never written, so the
    match must not be undone by a clamp. This is what prevents 'louder = better'.
    """
    cur = dsp.integrated_loudness(samples, sr)
    gain = 10.0 ** ((target_lufs - cur) / 20.0)
    return np.asarray(samples, dtype=np.float64) * gain


def _presence_ratio(vocal: Optional[LoadedAudio], mix: LoadedAudio) -> Optional[float]:
    if vocal is None:
        return None
    vf, vp = dsp.average_power(dsp.to_mono(vocal.samples), vocal.sample_rate)
    mf, mp = dsp.average_power(dsp.to_mono(mix.samples), mix.sample_rate)
    v = dsp.band_fraction(vf, vp, *VOCAL_PRESENCE_BAND)
    m = dsp.band_fraction(mf, mp, *VOCAL_PRESENCE_BAND)
    return round(v - m, 4)


def compare(base: RenderResult, variant: RenderResult, sections: List,
            sr: int, lead_vocal_tid: Optional[str]) -> Dict:
    bm = compute_metrics(base.mixdown.samples, sr)
    vm = compute_metrics(variant.mixdown.samples, sr)

    def delta(a, b, key):
        return round(b[key] - a[key], 4)

    raw_delta = {
        "rms_dbfs": delta(bm, vm, "rms_dbfs"),
        "lufs": delta(bm, vm, "estimated_lufs"),
        "stereo_width": delta(bm, vm, "stereo_width"),
        "brightness": delta(bm, vm, "brightness"),
        "density": delta(bm, vm, "density"),
        "mono_collapse_loss_db": delta(bm, vm, "mono_collapse_loss_db"),
    }

    # Mandatory loudness-matched comparison (guardrail 1).
    matched = loudness_match(variant.mixdown.samples, sr, bm["estimated_lufs"])
    vmm = compute_metrics(matched, sr)
    loudness_matched_delta = {
        "lufs": delta(bm, vmm, "estimated_lufs"),  # ~0 by construction
        "stereo_width": delta(bm, vmm, "stereo_width"),
        "brightness": delta(bm, vmm, "brightness"),
        "density": delta(bm, vmm, "density"),
        "presence_energy": round(vmm["band_energy"]["presence"] - bm["band_energy"]["presence"], 4),
    }

    # Section contrast: lift warnings before/after.
    lead_base = base.stems.get(lead_vocal_tid) if lead_vocal_tid else None
    lead_var = variant.stems.get(lead_vocal_tid) if lead_vocal_tid else None
    base_secs = analyze_sections(sections, base.mixdown, lead_base)
    var_secs = analyze_sections(sections, variant.mixdown, lead_var)
    base_warn = sum(1 for s in base_secs if "warning" in s.get("contrast_vs_previous", {}))
    var_warn = sum(1 for s in var_secs if "warning" in s.get("contrast_vs_previous", {}))

    vocal_intel = {
        "base": _presence_ratio(lead_base, base.mixdown),
        "variant": _presence_ratio(lead_var, variant.mixdown),
    }
    tr_base = analyze_translation(bm, [])["translation_score"]
    tr_var = analyze_translation(vm, [])["translation_score"]

    notes: List[str] = []
    improved = True
    if var_warn < base_warn:
        notes.append(f"Section-contrast warnings {base_warn} -> {var_warn} (improved).")
    elif var_warn > base_warn:
        notes.append(f"Section-contrast warnings {base_warn} -> {var_warn} (worse).")
        improved = False
    if vocal_intel["base"] is not None and vocal_intel["variant"] is not None:
        if vocal_intel["variant"] + 1e-6 < vocal_intel["base"] - 0.01:
            notes.append("Vocal presence dropped (loudness-independent) — wash risk.")
            improved = False
        else:
            notes.append("Vocal presence preserved.")
    if (tr_var or 0) + 1e-6 < (tr_base or 0) - 5:
        notes.append(f"Translation score dropped {tr_base} -> {tr_var}.")
        improved = False
    if raw_delta["rms_dbfs"] > 0.5 and loudness_matched_delta["density"] <= 0 and var_warn >= base_warn:
        notes.append("Louder but not more open once loudness-matched — do not mistake level for improvement.")
        improved = False

    return {
        "raw_delta": raw_delta,
        "loudness_matched_delta": loudness_matched_delta,
        "section_contrast": {"base_warnings": base_warn, "variant_warnings": var_warn},
        "vocal_intelligibility": vocal_intel,
        "translation_score": {"base": tr_base, "variant": tr_var},
        "perceptual_improvement": improved,
        "notes": notes,
    }


# --------------------------------------------------------------------------- #
# Trial orchestration
# --------------------------------------------------------------------------- #
def _find_variant(result, variant_id: Optional[str]) -> Optional[Dict]:
    branches = result.creative.get("branches", [])
    if variant_id:
        for b in branches:
            for v in b["variants"]:
                if v["variant_id"] == variant_id:
                    return v
        return None
    # default: the first branch's governed/top winner
    for b in branches:
        win = b.get("winning", {})
        wid = win.get("winning_variant")
        for v in b["variants"]:
            if v["variant_id"] == wid:
                return v
    return None


def run_variant_trial(result, variant_id: Optional[str] = None,
                      out_dir: Optional[str] = None) -> Dict:
    """Render base + a variant, write WAVs, and compare (with loudness match)."""
    variant = _find_variant(result, variant_id)
    if variant is None:
        return {"error": f"variant '{variant_id}' not found"}

    project = result.project
    stems_raw: Dict[str, LoadedAudio] = {}
    for t in project.resolved_tracks():
        try:
            stems_raw[t.track_id] = load_audio(t.file)
        except Exception:
            continue
    if not stems_raw:
        return {"error": "no stems available to render"}

    sr = next(iter(stems_raw.values())).sample_rate
    duration = max(_stereo(a.samples).shape[0] for a in stems_raw.values()) / sr
    bounds = {s.section_id: b for s, b in zip(project.sections, resolve_section_bounds(project.sections, duration))}

    ops, unmapped = plan_ops(variant, result.records, project.sections)
    lead_tid = next((r["track_id"] for r in result.records if r["instrument_identity"] == "lead_vocal"), None)

    base = render(stems_raw, [], sr, bounds)
    var = render(stems_raw, ops, sr, bounds)
    var.unmapped_changes = unmapped

    out = {
        "variant_id": variant["variant_id"],
        "variant_name": variant["name"],
        "kind": variant["kind"],
        "applied_ops": ops,
        "unmapped_changes": unmapped,
        "compare": compare(base, var, project.sections, sr, lead_tid),
    }
    if out_dir:
        out_path = Path(out_dir)
        out["base_render"] = write_wav(out_path / "base.wav", base.mixdown.samples, sr)
        out["variant_render"] = write_wav(out_path / f"{variant['variant_id']}.wav", var.mixdown.samples, sr)
    return out
