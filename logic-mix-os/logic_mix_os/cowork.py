"""Claude Cowork command surface (build packet section 43).

A single registry of named commands Cowork can call, each a thin, JSON-returning
view over one shared analysis (or a memory operation). This is the orchestration
layer: Cowork stays the reasoner; these commands are the bounded actions.

Usage::

    from logic_mix_os.cowork import build_context, run_command, list_commands
    ctx = build_context(stems, manifest)
    run_command("detect_masking", ctx)
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .constants import IDENTITY_FAMILY
from .memory import ProjectMemory
from .pipeline import analyze
from .renderers.checklist_renderer import render_logic_checklist


def build_context(stems=None, manifest=None, memory_dir=None, bounce=None,
                  reference=None, result=None) -> Dict:
    """Build the shared context (runs one full analysis unless ``result`` given)."""
    if result is None:
        result = analyze(stems, manifest or {}, bounce_path=bounce, reference_path=reference,
                         memory_dir=memory_dir)
    return {"result": result, "memory": ProjectMemory(memory_dir) if memory_dir else None}


# --------------------------------------------------------------------------- #
# Handlers (ctx, **params) -> JSON-able
# --------------------------------------------------------------------------- #
def _r(ctx):
    return ctx["result"]


def _intake_project(ctx, **k):
    r = _r(ctx)
    return {"song_title": r.project.song_title, "tempo": r.project.tempo, "key": r.project.key,
            "sections": len(r.section_analysis), "tracks": len(r.track_analysis)}


def _manipulation_capabilities(ctx, **k):
    return [{"track": s["name"], "source_kind": s["source_kind"],
             "editable_domains": s["editable_domains"],
             "not_editable_directly": s.get("not_editable_directly", [])}
            for s in _r(ctx).source_material]


def _review_uncertain(ctx, threshold=0.7, **k):
    return [i for i in _r(ctx).track_identity if i["confidence"] < threshold]


def _override_identity(ctx, track_id=None, identity=None, **k):
    for i in _r(ctx).track_identity:
        if i["track_id"] == track_id:
            i["manual_override"] = identity
            i["instrument_identity"] = identity
            i["identity_family"] = IDENTITY_FAMILY.get(identity, "unknown")
            i["confidence"] = 1.0
            return {"updated": i, "note": "Re-run analysis to propagate the override downstream."}
    return {"error": f"track_id '{track_id}' not found"}


def _classify_tracks(ctx, **k):
    sm = {s["track_id"]: s for s in _r(ctx).source_material}
    roles = {x["track_id"]: x for x in _r(ctx).roles}
    out = []
    for i in _r(ctx).track_identity:
        tid = i["track_id"]
        out.append({"track": i["name"], "identity": i["instrument_identity"],
                    "source_kind": sm[tid]["source_kind"], "musical_role": roles[tid]["musical_role"],
                    "perceptual_role": roles[tid]["perceptual_role"], "sacredness": roles[tid]["sacredness"]})
    return out


def _audits_of(ctx, types):
    return [a for a in _r(ctx).source_audits["audits"] if a["auditor_type"] in types]


def _validate_mix_pass(ctx, **k):
    r = _r(ctx)
    return {"scores": r.doctrine_score, "stop_conditions": r.governance.get("stop_conditions"),
            "warnings": r.mix_plan.get("warnings", [])}


def _write_mix_decision(ctx, decision=None, **k):
    mem = ctx.get("memory")
    if not mem:
        return {"error": "no memory_dir configured"}
    return mem.add_decision(decision or {}, event_type="mix_decision")


def _record_mix_pass(ctx, name=None, reverted=False, **k):
    # P-019 — CLOSE the learning loop inside cowork. Records a pass OUTCOME on the
    # LIVE history channel (memory.record_pass, P-008/P-009) against this context's
    # analysis result, passing through the P-018 ``reverted`` ground-truth flag
    # (opt-in, default False). Mirrors ``_write_mix_decision``'s no-memory error
    # path; unlike the DEAD decision ledger, this feeds the live next-pass planner.
    mem = ctx.get("memory")
    if not mem:
        return {"error": "no memory_dir configured"}
    return mem.record_pass(name, _r(ctx), reverted=reverted)


def _update_taste(ctx, label=None, context=None, **k):
    mem = ctx.get("memory")
    if not mem:
        return {"error": "no memory_dir configured"}
    return mem.add_feedback(label, context=context)


def _build_missing_tool(ctx, capability_gap="", **k):
    return {"capability_gap": capability_gap,
            "recommendation": "Spec a Mode-D helper Audio Unit (see bridge/au_helper_plugin_spec.md) "
                              "that emits metrics matching the existing schemas.",
            "candidate_tools": ["Mix Probe", "Room Send Auditor", "Vocal Masking Detector",
                                "Stereo Loop Auditor", "Depth Layer Meter", "Reference Delta Meter"]}


COMMANDS = {
    "intake_project": {"desc": "Project summary", "fn": _intake_project},
    "detect_source_materials": {"desc": "Source material per track", "fn": lambda c, **k: _r(c).source_material},
    "map_manipulation_capabilities": {"desc": "Editable domains per track", "fn": _manipulation_capabilities},
    "detect_track_identities": {"desc": "Instrument identity per track", "fn": lambda c, **k: _r(c).track_identity},
    "review_uncertain_identities": {"desc": "Identities below a confidence threshold", "fn": _review_uncertain},
    "override_track_identity": {"desc": "Override an identity (params: track_id, identity)", "fn": _override_identity},
    "classify_tracks": {"desc": "Identity + source + role per track", "fn": _classify_tracks},
    "classify_musical_roles": {"desc": "Musical role per track", "fn": lambda c, **k: [{"track": x["name"], "musical_role": x["musical_role"]} for x in _r(c).roles]},
    "classify_felt_vs_heard": {"desc": "Perceptual role per track", "fn": lambda c, **k: [{"track": x["name"], "perceptual_role": x["perceptual_role"]} for x in _r(c).roles]},
    "classify_sacred_vs_expendable": {"desc": "Sacredness per track", "fn": lambda c, **k: [{"track": x["name"], "sacredness": x["sacredness"]} for x in _r(c).roles]},
    "detect_sections": {"desc": "Section analysis", "fn": lambda c, **k: _r(c).section_analysis},
    "analyze_section_contrast": {"desc": "Section contrast deltas", "fn": lambda c, **k: [{"section": s["section_id"], **s.get("contrast_vs_previous", {})} for s in _r(c).section_analysis]},
    "map_arrangement_density": {"desc": "Per-section depth occupancy", "fn": lambda c, **k: _r(c).expanded.get("arrangement_density")},
    "assign_depth_layers": {"desc": "Depth map", "fn": lambda c, **k: _r(c).depth_map},
    "detect_masking": {"desc": "Masking report", "fn": lambda c, **k: _r(c).masking_report},
    "detect_bad_masking_by_depth": {"desc": "Critical masking only", "fn": lambda c, **k: [e for e in _r(c).masking_report["events"] if e["classification"] == "bad_masking"]},
    "analyze_live_track": {"desc": "Live-track audits", "fn": lambda c, **k: _audits_of(c, {"live_track"})},
    "analyze_synth_patch": {"desc": "Synth-patch audits", "fn": lambda c, **k: _audits_of(c, {"synth_patch"})},
    "audit_sample_loop": {"desc": "Loop/sample audits", "fn": lambda c, **k: _audits_of(c, {"sample_loop"})},
    "generate_mix_plan": {"desc": "Full mix plan", "fn": lambda c, **k: _r(c).mix_plan},
    "generate_automation_plan": {"desc": "Automation plan", "fn": lambda c, **k: _r(c).mix_plan.get("automation_plan")},
    "compare_to_reference": {"desc": "Reference delta", "fn": lambda c, **k: _r(c).reference_delta or {"note": "no reference supplied"}},
    "render_logic_checklist": {"desc": "Logic checklist (markdown)", "fn": lambda c, **k: render_logic_checklist(_r(c).mix_plan)},
    "score_mix": {"desc": "Doctrine scores", "fn": lambda c, **k: _r(c).doctrine_score},
    "validate_mix_pass": {"desc": "Scores + stop conditions + warnings", "fn": _validate_mix_pass},
    "suggest_next_pass": {"desc": "Prioritised next-pass moves", "fn": lambda c, **k: _r(c).mix_plan.get("next_pass")},
    "identify_mute_candidates": {"desc": "Mute/chop candidates", "fn": lambda c, **k: _r(c).mix_plan.get("mute_candidates")},
    "run_creative_engine": {"desc": "Creative variants + governance", "fn": lambda c, **k: _r(c).creative},
    "run_governance": {"desc": "Taste protection report", "fn": lambda c, **k: _r(c).governance},
    "write_mix_decision": {"desc": "Append a decision to the ledger (params: decision)", "fn": _write_mix_decision},
    "record_mix_pass": {"desc": "Record a pass outcome on the live history channel (params: name, reverted)", "fn": _record_mix_pass},
    "update_taste_calibration": {"desc": "Record taste feedback (params: label)", "fn": _update_taste},
    "build_missing_tool": {"desc": "Spec a helper tool for a capability gap", "fn": _build_missing_tool},
}


def list_commands() -> List[Dict]:
    return [{"command": name, "description": meta["desc"]} for name, meta in sorted(COMMANDS.items())]


def run_command(name: str, ctx: Dict, /, **params):
    # ``name``/``ctx`` are positional-only so a handler param may itself be called
    # ``name`` (e.g. record_mix_pass's pass name) without colliding with this
    # dispatcher's own ``name`` — the cowork ``--params '{...}'`` path unpacks
    # straight into ``**params``.
    if name not in COMMANDS:
        raise KeyError(f"Unknown command '{name}'. Use list_commands() to see the catalog.")
    return COMMANDS[name]["fn"](ctx, **params)
