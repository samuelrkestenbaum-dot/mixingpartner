"""End-to-end analysis pipeline.

Runs every deterministic stage in order and assembles the full set of JSON +
Markdown artifacts. This is the single place that knows how the stages connect;
the CLI is a thin wrapper around it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .analyzers.arrangement_density_mapper import map_density
from .analyzers.audio_loader import LoadedAudio, load_audio
from .analyzers.audio_metrics import compute_metrics
from .analyzers.groove_analyzer import RHYTHM_IDENTITIES, analyze_groove
from .analyzers.harmonic_melodic_analyzer import analyze_harmony
from .analyzers.listener_experience_mapper import map_experience
from .analyzers.lyric_alignment_analyzer import analyze_lyrics
from .analyzers.masking_analyzer import analyze_masking
from .analyzers.mono_compatibility_analyzer import analyze_mono
from .analyzers.plugin_scanner import scan_plugins
from .analyzers.provenance import analyze_provenance
from .analyzers.reference_comparator import compare_to_reference
from .analyzers.render_graph import build_render_graph
from .analyzers.section_analyzer import analyze_sections
from .analyzers.source_auditors import audit_all
from .analyzers.source_material_detector import detect_source_material
from .analyzers.track_identity_detector import detect_track_identity
from .analyzers.transition_quality_analyzer import analyze_transitions
from .analyzers.translation_analyzer import analyze_translation
from .analyzers.vocal_performance_analyzer import analyze_vocal
from .bridge.applescript_bridge import generate_applescript
from .bridge.exporter import export_actions
from .creative import run_creative_engine
from .doctrine.doctrine_engine import score_doctrine
from .governance import run_governance
from .planners.depth_planner import plan_depth
from .planners.logic_action_generator import generate_logic_actions
from .planners.mix_planner import build_plan
from .planners.next_pass_planner import generate_creative_hypotheses, plan_next_pass
from .planners.role_classifier import classify_roles
from .project import Project
from .renderers import checklist_renderer, creative_renderer, markdown_renderer


@dataclass
class ProjectAnalysis:
    project: Project
    source_material: List[Dict] = field(default_factory=list)
    track_identity: List[Dict] = field(default_factory=list)
    track_analysis: List[Dict] = field(default_factory=list)
    roles: List[Dict] = field(default_factory=list)
    depth_map: List[Dict] = field(default_factory=list)
    section_analysis: List[Dict] = field(default_factory=list)
    masking_report: Dict = field(default_factory=dict)
    mix_metrics: Optional[Dict] = None
    doctrine_score: Dict = field(default_factory=dict)
    mix_plan: Dict = field(default_factory=dict)
    reference_delta: Optional[Dict] = None
    creative_hypotheses: List[Dict] = field(default_factory=list)
    expanded: Dict = field(default_factory=dict)
    creative: Dict = field(default_factory=dict)
    governance: Dict = field(default_factory=dict)
    provenance: Dict = field(default_factory=dict)
    render_graph: Dict = field(default_factory=dict)
    plugin_scan: Dict = field(default_factory=dict)
    source_audits: Dict = field(default_factory=dict)
    records: List[Dict] = field(default_factory=list)


def analyze(
    stems_dir: Optional[str | Path],
    manifest: Dict,
    bounce_path: Optional[str | Path] = None,
    reference_path: Optional[str | Path] = None,
    creative_mode: Optional[str] = None,
) -> ProjectAnalysis:
    project = Project.from_inputs(stems_dir, manifest)
    result = ProjectAnalysis(project=project)

    loaded_by_id: Dict[str, LoadedAudio] = {}
    records: List[Dict] = []

    for track in project.tracks:
        metrics: Optional[Dict] = None
        if track.file:
            try:
                loaded = load_audio(track.file)
                loaded_by_id[track.track_id] = loaded
                metrics = compute_metrics(loaded.samples, loaded.sample_rate)
                metrics["path"] = loaded.path
            except Exception as exc:  # corrupt/unsupported file: keep going
                metrics = None
                track.extra["load_error"] = str(exc)

        sm = detect_source_material(track, metrics)
        ident = detect_track_identity(track, metrics)
        roles = classify_roles(ident, sm, metrics)
        depth = plan_depth(ident, roles, sm, project.sections)

        result.source_material.append(sm)
        result.track_identity.append(ident)
        result.roles.append(roles)
        result.depth_map.append(depth)
        if metrics is not None:
            result.track_analysis.append({"track_id": track.track_id, "name": track.name, "metrics": metrics})
            records.append({
                "track_id": track.track_id,
                "name": track.name,
                "instrument_identity": ident["instrument_identity"],
                "identity_family": ident["identity_family"],
                "perceptual_role": roles["perceptual_role"],
                "sacredness": roles["sacredness"],
                "source_kind": sm["source_kind"],
                "depth_default": depth["default_depth"],
                "depth_by_section": depth["depth_by_section"],
                "stereo_width": metrics["stereo_width"],
                "band_energy": metrics["band_energy"],
                "vocal_presence_energy": metrics["vocal_presence_energy"],
                "brightness": metrics["brightness"],
                "metrics": metrics,
                "source_warnings": sm.get("warnings", []),
            })

    result.records = records

    # Lead vocal (loaded) for section vocal-presence analysis.
    lead_vocal_loaded = None
    for ident in result.track_identity:
        if ident["instrument_identity"] == "lead_vocal" and ident["track_id"] in loaded_by_id:
            lead_vocal_loaded = loaded_by_id[ident["track_id"]]
            break

    # Mixdown + sections.
    mixdown = project.build_mixdown(bounce_path)
    if mixdown is not None:
        result.mix_metrics = compute_metrics(mixdown.samples, mixdown.sample_rate)
        result.section_analysis = analyze_sections(project.sections, mixdown, lead_vocal_loaded)

    # Masking, then fold per-track masking risk back into track_analysis.
    result.masking_report = analyze_masking(records, result.section_analysis)
    risk = result.masking_report.get("per_track_masking_risk", {})
    for entry in result.track_analysis:
        entry["metrics"]["masking_risk"] = risk.get(entry["track_id"])

    # Doctrine scoring.
    result.doctrine_score = score_doctrine(
        records, result.section_analysis, result.masking_report, result.mix_metrics, project.intent
    )

    # Reference delta.
    if reference_path and mixdown is not None:
        try:
            ref = load_audio(reference_path)
            result.reference_delta = compare_to_reference(mixdown, ref)
        except Exception:
            result.reference_delta = None

    # Expanded analysis suite (translation, mono, density, narrative, etc.).
    lead_record = next((r for r in records if r["instrument_identity"] == "lead_vocal"), None)
    lead_present = lead_record is not None
    rhythm_tracks = [
        {"name": ident["name"], "identity": ident["instrument_identity"], "loaded": loaded_by_id[ident["track_id"]]}
        for ident in result.track_identity
        if ident["instrument_identity"] in RHYTHM_IDENTITIES and ident["track_id"] in loaded_by_id
    ]
    result.expanded = {
        "translation": analyze_translation(result.mix_metrics, records),
        "mono_compatibility": analyze_mono(records, result.mix_metrics),
        "arrangement_density": map_density(records, result.section_analysis),
        "listener_experience": map_experience(result.section_analysis, lead_present),
        "transitions": analyze_transitions(mixdown, project.sections),
        "groove": analyze_groove(rhythm_tracks),
        "harmonic": analyze_harmony(mixdown, project.key),
        "vocal_performance": analyze_vocal(lead_vocal_loaded, lead_record["metrics"] if lead_record else None),
        "lyrics": analyze_lyrics(manifest, result.section_analysis, lead_present),
    }

    # Logic actions + mix plan + next pass + creative hypotheses.
    logic_actions = generate_logic_actions(records, result.masking_report)
    result.mix_plan = build_plan(
        song_title=project.song_title,
        intent=project.intent,
        records=records,
        sections_analysis=result.section_analysis,
        masking_report=result.masking_report,
        doctrine_score=result.doctrine_score,
        logic_actions=logic_actions,
        mix_metrics=result.mix_metrics,
        reference_delta=result.reference_delta,
    )
    result.mix_plan["next_pass"] = plan_next_pass(
        records, result.doctrine_score, result.masking_report, result.section_analysis
    )
    result.mix_plan["translation_score"] = result.expanded["translation"]["translation_score"]
    result.mix_plan["mono_compatibility_score"] = result.expanded["mono_compatibility"]["mono_score"]
    result.creative_hypotheses = generate_creative_hypotheses(result.mix_plan, records)

    # Creative experimentation engine + governance / taste protection.
    mode = creative_mode or _default_creative_mode(project.intent)
    result.creative = run_creative_engine(result, mode)
    result.governance = run_governance(result, result.creative)

    # Session intelligence: provenance, render graph, plugin availability.
    result.provenance = analyze_provenance(project, result.source_material, result.depth_map)
    result.render_graph = build_render_graph(project)
    result.plugin_scan = scan_plugins(result.mix_plan, manifest.get("plugins"))
    result.source_audits = audit_all(records)

    return result


def _default_creative_mode(intent: Dict) -> str:
    """Pick a sensible search mode from the song's emotional truth."""
    truth = (intent.get("singular_emotional_truth", "") or "").lower()
    if any(w in truth for w in ["intimate", "vulnerable", "conflicted", "ache", "quiet", "restrained", "composed"]):
        return "ramone_vocal_truth"
    return "dramatic_contrast"


# --------------------------------------------------------------------------- #
def _dump_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def _write_text(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text.rstrip() + "\n")


def write_artifacts(result: ProjectAnalysis, out_dir: str | Path) -> List[str]:
    """Write every JSON + Markdown artifact. Returns the list of paths written."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: List[str] = []

    json_files = {
        "source_material.json": result.source_material,
        "track_identity.json": result.track_identity,
        "track_analysis.json": result.track_analysis,
        "section_analysis.json": result.section_analysis,
        "depth_map.json": result.depth_map,
        "masking_report.json": result.masking_report,
        "mix_plan.json": result.mix_plan,
        "doctrine_score.json": result.doctrine_score,
    }
    if result.reference_delta is not None:
        json_files["reference_delta.json"] = result.reference_delta
    if result.expanded:
        json_files["expanded_analysis.json"] = result.expanded
    if result.creative:
        json_files["creative.json"] = result.creative
    if result.governance:
        json_files["governance.json"] = result.governance
    if result.provenance:
        json_files["provenance.json"] = result.provenance
    if result.render_graph:
        json_files["render_graph.json"] = result.render_graph
    if result.plugin_scan:
        json_files["plugin_scan.json"] = result.plugin_scan
    if result.source_audits:
        json_files["source_audits.json"] = result.source_audits
    logic_actions = export_actions(result.mix_plan)
    json_files["logic_actions.json"] = logic_actions

    for name, data in json_files.items():
        _dump_json(out / name, data)
        written.append(str(out / name))

    md_files = {
        "source_material_report.md": markdown_renderer.render_source_material_report(result.source_material),
        "track_identity_report.md": markdown_renderer.render_track_identity_report(result.track_identity),
        "halee_ramone_mix_verdict.md": markdown_renderer.render_halee_ramone_verdict(result.mix_plan, result.doctrine_score),
        "logic_action_checklist.md": checklist_renderer.render_logic_checklist(result.mix_plan),
        "next_pass_recommendations.md": markdown_renderer.render_next_pass(result.mix_plan["next_pass"], result.creative_hypotheses),
        # Bonus reports (not part of the required MVP set, but cheap and useful):
        "automation_plan.md": markdown_renderer.render_automation_plan(result.mix_plan["automation_plan"]),
        "section_contrast_report.md": markdown_renderer.render_section_contrast_report(result.section_analysis),
    }
    if result.expanded:
        md_files["expanded_analysis.md"] = markdown_renderer.render_expanded_analysis(result.expanded)
    if result.creative:
        md_files["creative_report.md"] = creative_renderer.render_creative(result.creative)
    if result.governance:
        md_files["governance_report.md"] = creative_renderer.render_governance(result.governance)
    if result.provenance or result.plugin_scan:
        md_files["session_intelligence.md"] = markdown_renderer.render_session_intelligence(
            result.provenance, result.render_graph, result.plugin_scan
        )
    if result.source_audits:
        md_files["source_audit_report.md"] = markdown_renderer.render_source_audits(result.source_audits)
    for name, text in md_files.items():
        _write_text(out / name, text)
        written.append(str(out / name))

    # AppleScript scaffolding (mode C of the bridge — does not run automatically).
    _write_text(out / "logic_actions.applescript", generate_applescript(logic_actions))
    written.append(str(out / "logic_actions.applescript"))

    return written
