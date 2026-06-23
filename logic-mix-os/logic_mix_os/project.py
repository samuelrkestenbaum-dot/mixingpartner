"""Project + manifest model.

Ties a folder of exported stems to a ``project_manifest.json`` and exposes the
resolved tracks, parsed sections, and an on-demand summed mixdown used for
section-level analysis when no stereo bounce is supplied.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from .analyzers.audio_loader import LoadedAudio, load_audio

AUDIO_EXTS = {".wav", ".wave", ".aif", ".aiff", ".flac", ".ogg"}


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")
    return slug or "track"


def parse_time(value) -> float:
    """Parse ``"M:SS"`` / ``"H:MM:SS"`` / seconds into float seconds."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if not s:
        return 0.0
    if ":" in s:
        parts = [float(p) for p in s.split(":")]
        seconds = 0.0
        for p in parts:
            seconds = seconds * 60.0 + p
        return seconds
    return float(s)


@dataclass
class Track:
    track_id: str
    name: str
    file: Optional[str]  # absolute path or None if unresolved
    source_kind_hint: Optional[str] = None
    identity_hint: Optional[str] = None
    extra: Dict = field(default_factory=dict)


@dataclass
class Section:
    section_id: str
    name: str
    start: float
    end: Optional[float]
    emotional_goal: Optional[str] = None


@dataclass
class Project:
    song_title: str
    tempo: Optional[float]
    key: Optional[str]
    intent: Dict
    tracks: List[Track]
    sections: List[Section]
    manifest: Dict
    stems_dir: Optional[Path] = None

    # -- construction -------------------------------------------------------
    @classmethod
    def from_inputs(
        cls, stems_dir: Optional[str | Path], manifest: Dict
    ) -> "Project":
        proj = manifest.get("project", {})
        intent = manifest.get("intent", {})
        stems_path = Path(stems_dir) if stems_dir else None

        tracks: List[Track] = []
        seen_files: set = set()
        used_ids: set = set()

        def unique_id(base: str) -> str:
            tid = base
            i = 2
            while tid in used_ids:
                tid = f"{base}_{i}"
                i += 1
            used_ids.add(tid)
            return tid

        for entry in manifest.get("tracks", []):
            name = entry.get("name") or Path(entry.get("file", "track")).stem
            file_path = _resolve_file(entry.get("file"), stems_path)
            if file_path:
                seen_files.add(file_path.name.lower())
            tracks.append(
                Track(
                    track_id=unique_id(slugify(name)),
                    name=name,
                    file=str(file_path) if file_path else None,
                    source_kind_hint=entry.get("source_kind"),
                    identity_hint=entry.get("known_identity"),
                    extra={
                        k: v
                        for k, v in entry.items()
                        if k not in {"name", "file", "source_kind", "known_identity"}
                    },
                )
            )

        # Merge in any stems present on disk but absent from the manifest.
        if stems_path and stems_path.is_dir():
            for f in sorted(stems_path.iterdir()):
                if f.suffix.lower() in AUDIO_EXTS and f.name.lower() not in seen_files:
                    name = f.stem
                    tracks.append(
                        Track(
                            track_id=unique_id(slugify(name)),
                            name=name,
                            file=str(f),
                        )
                    )

        sections: List[Section] = []
        for i, sec in enumerate(manifest.get("sections", [])):
            sid = sec.get("section_id") or slugify(sec.get("name", f"section_{i + 1}"))
            sections.append(
                Section(
                    section_id=sid,
                    name=sec.get("name", sid),
                    start=parse_time(sec.get("start_time")),
                    end=parse_time(sec.get("end_time")) if sec.get("end_time") else None,
                    emotional_goal=sec.get("emotional_goal"),
                )
            )
        sections.sort(key=lambda s: s.start)

        return cls(
            song_title=proj.get("song_title", manifest.get("song_title", "Untitled")),
            tempo=proj.get("tempo"),
            key=proj.get("key"),
            intent=intent,
            tracks=tracks,
            sections=sections,
            manifest=manifest,
            stems_dir=stems_path,
        )

    # -- helpers ------------------------------------------------------------
    def track_by_id(self, track_id: str) -> Optional[Track]:
        for t in self.tracks:
            if t.track_id == track_id:
                return t
        return None

    def resolved_tracks(self) -> List[Track]:
        return [t for t in self.tracks if t.file]

    def build_mixdown(self, bounce_path: Optional[str | Path] = None) -> Optional[LoadedAudio]:
        """Return a stereo mixdown for section analysis.

        Uses ``bounce_path`` if given; otherwise sums all resolved stems
        (each upmixed to stereo) and normalises to avoid clipping.
        """
        if bounce_path:
            return load_audio(bounce_path)

        loaded = []
        sr = None
        for t in self.resolved_tracks():
            try:
                a = load_audio(t.file)
            except Exception:
                continue
            sr = sr or a.sample_rate
            if a.sample_rate != sr:
                continue  # MVP assumes a consistent project sample rate
            loaded.append(a)
        if not loaded or sr is None:
            return None

        max_len = max(a.num_frames for a in loaded)
        acc = np.zeros((max_len, 2), dtype=np.float64)
        for a in loaded:
            s = a.samples
            stereo = np.column_stack([s, s]) if s.ndim == 1 else s[:, :2]
            if stereo.shape[0] < max_len:
                pad = np.zeros((max_len - stereo.shape[0], 2))
                stereo = np.vstack([stereo, pad])
            acc += stereo

        peak = float(np.max(np.abs(acc))) or 1.0
        if peak > 0.9:
            acc *= 0.9 / peak
        return LoadedAudio(samples=acc, sample_rate=sr, path="<mixdown>")


def load_manifest(path: str | Path) -> Dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _resolve_file(file: Optional[str], stems_dir: Optional[Path]) -> Optional[Path]:
    if not file:
        return None
    p = Path(file)
    if p.is_absolute() and p.exists():
        return p
    if stems_dir:
        candidate = stems_dir / file
        if candidate.exists():
            return candidate
        # try basename match within the stems dir
        base = stems_dir / Path(file).name
        if base.exists():
            return base
    return p if p.exists() else None
