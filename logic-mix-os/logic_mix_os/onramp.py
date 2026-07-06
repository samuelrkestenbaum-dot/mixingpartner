"""Real-session on-ramp: manifest scaffolder + field-session capture (P-058).

Two dev-tools that bridge "the engine runs on synthetic fixtures" and "a real
Cowork session can be driven through it and read back":

* ``scaffold_manifest`` / ``write_manifest_draft`` — turn a folder of exported
  stems into a VALID *draft* ``project_manifest.json`` the pipeline accepts. It
  reuses the shipped name->kind heuristic
  (``source_material_detector.guess_source_kind``) so the guessed ``source_kind``
  vocabulary can never drift from the detector's, writes low-confidence guesses
  into a ``_needs_review`` list for a human to confirm, and probes only the WAV
  *header* (read-only) for the project sample rate / bit depth. It never analyses
  audio to invent section timecodes, so it stays deterministic and in-scope.

* ``bundle_field_session`` — copy a session's three memory JSONs plus its
  plan/verdict artifacts into a commit-back bundle and write a deterministic
  ``session_summary.json``. READ/COPY only; raw audio is NEVER bundled.

Boundary: this module writes ONLY a draft manifest and a capture bundle (dev-tool
writes to caller-specified paths). It never drives a DAW, never writes a Logic
session, and never generates or copies an audio file. Imports are stdlib plus the
first-party shared heuristic / vocabulary.
"""

from __future__ import annotations

import json
import shutil
import wave
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .analyzers.source_material_detector import guess_source_kind
from .constants import SOURCE_KINDS

# --------------------------------------------------------------------------- #
# Extension tables.
# --------------------------------------------------------------------------- #
# Audio files the scaffolder turns into one manifest track each.
_SCAFFOLD_AUDIO_EXTS = (".wav", ".wave", ".aif", ".aiff", ".flac", ".ogg", ".caf")
# Header-probe formats (stdlib ``wave`` reads PCM WAV headers read-only).
_WAV_EXTS = (".wav", ".wave")
# Audio extensions that must NEVER enter a captured bundle (belt + suspenders on
# top of the artifact allow-list below).
_EXCLUDED_AUDIO_EXTS = (
    ".wav", ".wave", ".aif", ".aiff", ".flac", ".caf",
    ".ogg", ".mp3", ".m4a", ".aac", ".wma", ".opus",
)
# Text artifacts (plan / verdict / checklist) copied from an analysis output dir.
_ARTIFACT_EXTS = (".json", ".md", ".html")

# A guess at or above this confidence is trusted; anything below is surfaced in
# ``_needs_review``. Keyword-rule hits score 0.82; the coarse vocal / live
# fallbacks (0.6 / 0.55) and ``unknown`` (0.4) fall below the line and are
# flagged for a human to confirm.
_REVIEW_CONFIDENCE = 0.82

# Folder names that are containers, not the song — when the stems folder is one
# of these the song title is taken from its parent instead.
_CONTAINER_DIR_NAMES = {"stems", "audio", "bounces", "wav", "wavs", "exports", "export"}

# The three live memory stores a field session writes (spec 32/37/38/39).
_MEMORY_JSONS = ("mix_pass_history.json", "decision_ledger.json", "taste_profile.json")


# --------------------------------------------------------------------------- #
# D1 — manifest scaffolder.
# --------------------------------------------------------------------------- #
def scaffold_manifest(stems_dir: str | Path, *, force: bool = False) -> Dict:
    """Build a VALID draft ``project_manifest.json`` dict from a stems folder.

    One track per audio file (sorted by filename) carrying the shared name->kind
    guess; a title derived from the folder; a WAV-header-probed sample rate /
    bit depth; blank tempo/key; a single fillable ``0:00`` section stub; an empty
    intent stub; and the annotations ``_draft: true`` + ``_needs_review`` (the
    names whose kind guess was below the confidence line).

    Deterministic: sorted file order + no timestamps => byte-identical on re-run.

    ``force`` is accepted for parity with :func:`write_manifest_draft`; this
    builder performs no filesystem write, so it has no effect here.
    """
    stems_path = Path(stems_dir)
    if not stems_path.is_dir():
        raise NotADirectoryError(f"Stems directory not found: {stems_path}")

    audio_files = sorted(
        (f for f in stems_path.iterdir()
         if f.is_file() and f.suffix.lower() in _SCAFFOLD_AUDIO_EXTS),
        key=lambda p: p.name,
    )

    sample_rate, bit_depth = _probe_wav_format(audio_files)

    tracks: List[Dict] = []
    needs_review: List[str] = []
    for f in audio_files:
        name = f.stem
        kind, confidence, _evidence = guess_source_kind(name)
        if kind not in SOURCE_KINDS:  # defensive: the heuristic is grounded
            kind = "unknown"
        tracks.append({"file": f.name, "name": name, "source_kind": kind})
        if confidence < _REVIEW_CONFIDENCE:
            needs_review.append(name)

    return {
        "project": {
            "song_title": _title_from_dir(stems_path),
            "tempo": None,
            "key": None,
            "sample_rate": sample_rate,
            "bit_depth": bit_depth,
        },
        "intent": {
            "singular_emotional_truth": "",
            "references": [],
            "negative_constraints": [],
        },
        "sections": [
            {
                "section_id": "section_1",
                "name": "Section 1",
                "start_time": "0:00",
                "end_time": "",
                "emotional_goal": "",
            }
        ],
        "tracks": tracks,
        "_draft": True,
        "_needs_review": needs_review,
    }


def write_manifest_draft(
    stems_dir: str | Path, out_path: str | Path, *, force: bool = False
) -> Path:
    """Scaffold a draft manifest and write it to ``out_path`` (pretty JSON).

    Refuses to overwrite an existing file unless ``force`` is set, raising
    :class:`FileExistsError`. Returns the written path.
    """
    out = Path(out_path)
    if out.exists() and not force:
        raise FileExistsError(
            f"Refusing to overwrite existing manifest: {out}. "
            f"Pass force=True (or --force) to overwrite."
        )
    manifest = scaffold_manifest(stems_dir, force=force)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return out


def _probe_wav_format(audio_files: List[Path]) -> Tuple[Optional[int], Optional[int]]:
    """Read (sample_rate, bit_depth) from the first WAV header, read-only.

    Returns ``(None, None)`` when there is no readable WAV (e.g. AIFF-only
    exports) — the draft leaves those fields null for the user to fill.
    """
    for f in audio_files:
        if f.suffix.lower() in _WAV_EXTS:
            try:
                with wave.open(str(f), "rb") as wf:
                    return int(wf.getframerate()), int(wf.getsampwidth()) * 8
            except (wave.Error, EOFError, OSError):
                continue
    return None, None


def _title_from_dir(stems_path: Path) -> str:
    """Humanise a song title from the stems folder (or its parent container)."""
    name = stems_path.name
    if name.lower() in _CONTAINER_DIR_NAMES:
        name = stems_path.parent.name or name
    words = name.replace("_", " ").replace("-", " ").split()
    return " ".join(w[:1].upper() + w[1:] for w in words) or "Untitled"


# --------------------------------------------------------------------------- #
# D2 — field-session capture.
# --------------------------------------------------------------------------- #
def bundle_field_session(
    memory_dir: str | Path,
    out_bundle_dir: str | Path,
    *,
    artifacts_dir: Optional[str | Path] = None,
) -> Dict:
    """Copy a session's memory + artifacts into a commit-back bundle.

    Copies the three memory JSONs from ``memory_dir`` (skipping any that are
    missing), then — if ``artifacts_dir`` is given — every plan/verdict text
    artifact (``.json`` / ``.md`` / ``.html``) from it, and writes a
    deterministic ``session_summary.json``. READ/COPY only; raw audio is NEVER
    bundled. Idempotent: re-running overwrites the bundle with the same content.
    """
    mem_path = Path(memory_dir)
    bundle = Path(out_bundle_dir)
    bundle.mkdir(parents=True, exist_ok=True)

    # 1) the three memory stores (explicit allow-list — audio can't sneak in).
    copied_memory: List[str] = []
    for fname in _MEMORY_JSONS:
        src = mem_path / fname
        if src.is_file():
            shutil.copy2(src, bundle / fname)
            copied_memory.append(fname)

    # 2) plan/verdict text artifacts (audio filtered out twice over).
    copied_artifacts: List[str] = []
    if artifacts_dir is not None:
        art_path = Path(artifacts_dir)
        if art_path.is_dir():
            for f in sorted(art_path.iterdir(), key=lambda p: p.name):
                suffix = f.suffix.lower()
                if not f.is_file() or suffix in _EXCLUDED_AUDIO_EXTS:
                    continue  # raw audio is NEVER bundled
                if suffix not in _ARTIFACT_EXTS:
                    continue
                shutil.copy2(f, bundle / f.name)
                copied_artifacts.append(f.name)

    # 3) a deterministic summary of what was captured.
    summary = _session_summary(mem_path, copied_memory, copied_artifacts)
    (bundle / "session_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    return {
        "bundle_dir": str(bundle),
        "memory_files": copied_memory,
        "artifacts": copied_artifacts,
        "summary": summary,
    }


def _session_summary(
    mem_path: Path, memory_files: List[str], artifacts: List[str]
) -> Dict:
    """A deterministic 'what was captured' summary (no wall-clock — idempotent)."""
    history = _read_json(mem_path / "mix_pass_history.json", [])
    ledger = _read_json(mem_path / "decision_ledger.json", [])
    taste = _read_json(mem_path / "taste_profile.json", {})

    history = history if isinstance(history, list) else []
    ledger = ledger if isinstance(ledger, list) else []
    feedback = taste.get("feedback", []) if isinstance(taste, dict) else []
    profile = taste.get("profile", []) if isinstance(taste, dict) else []
    latest = history[-1].get("pass_name") if history else None

    return {
        "memory_dir": str(mem_path),
        "captured": {
            "memory_files": sorted(memory_files),
            "artifacts": sorted(artifacts),
        },
        "counts": {
            "mix_passes": len(history),
            "decisions": len(ledger),
            "taste_feedback": len(feedback),
        },
        "latest_pass": latest,
        "taste_profile": profile,
    }


def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default
