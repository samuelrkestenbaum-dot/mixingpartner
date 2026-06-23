"""Command-line interface for Logic Mix OS.

Thin wrapper over :mod:`logic_mix_os.pipeline`. Uses only stdlib argparse so the
tool has no CLI-framework dependency. Local-only, deterministic, non-destructive.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .album import analyze_album
from .analyzers.audio_loader import load_audio
from .analyzers.reference_comparator import compare_to_reference
from .memory import ProjectMemory
from .pipeline import analyze, write_artifacts
from .planners.next_pass_planner import generate_creative_hypotheses
from .project import load_manifest
from .regression import run_regression_suite
from .renderers import checklist_renderer
from .renderers.operator_view import render_status
from .validation.output_validator import validate_output


def _load_manifest(path: Optional[str]) -> dict:
    if not path:
        return {}
    return load_manifest(path)


def _run_analyze(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(
        args.stems,
        manifest,
        bounce_path=args.bounce,
        reference_path=args.reference,
    )
    written = write_artifacts(result, args.out)
    _print_summary(result, args.out, len(written))
    return 0


def _print_summary(result, out_dir, n_written) -> None:
    ds = result.doctrine_score
    print(f"\nLogic Mix OS — {result.project.song_title}")
    print("=" * 48)
    print(f"Tracks analysed: {len(result.track_analysis)} | Sections: {len(result.section_analysis)}")
    if ds.get("overall_mix_readiness_score") is not None:
        print(f"Overall mix readiness: {ds['overall_mix_readiness_score']}/100")
        print(f"  Halee {ds.get('halee_score')} | Ramone {ds.get('ramone_score')} | "
              f"Static {ds.get('static_mix_score')} | Dynamic {ds.get('dynamic_mix_score')}")
    print("\nTop next-pass moves:")
    for item in result.mix_plan.get("next_pass", []):
        print(f"  {item['priority']}. {item['title']}: {item['detail']}")
    print(f"\nWrote {n_written} artifacts to {out_dir}/")


def _run_detect_identities(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest)
    write_artifacts(result, args.out)
    print(f"{'Track':<28} {'Identity':<18} {'Family':<10} Conf")
    print("-" * 64)
    for it in result.track_identity:
        print(f"{it['name'][:27]:<28} {it['instrument_identity']:<18} {it['identity_family']:<10} {it['confidence']:.2f}")
    return 0


def _run_analyze_sections(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest, bounce_path=args.bounce)
    write_artifacts(result, args.out)
    if not result.section_analysis:
        print("No sections found (provide section markers in the manifest or a bounce).")
        return 0
    print(f"{'Section':<18} {'Goal':<14} {'RMS dB':>8} {'Width':>7} {'ΔRMS':>7}")
    print("-" * 58)
    for s in result.section_analysis:
        c = s.get("contrast_vs_previous", {})
        print(f"{s['name'][:17]:<18} {str(s.get('emotional_goal'))[:13]:<14} "
              f"{s['metrics']['rms_dbfs']:>8.1f} {s['metrics']['width']:>7.2f} "
              f"{str(c.get('rms_delta_db', '—')):>7}")
        if "warning" in c:
            print(f"   ⚠️  {c['warning']}")
    return 0


def _run_generate_plan(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest, bounce_path=args.bounce, reference_path=args.reference)
    written = write_artifacts(result, args.out)
    print(f"Mix plan written. {len(written)} artifacts in {args.out}/")
    print(f"Overall diagnosis: {result.mix_plan.get('overall_diagnosis')}")
    return 0


def _run_render_checklist(args) -> int:
    with open(args.plan, "r", encoding="utf-8") as fh:
        mix_plan = json.load(fh)
    md = checklist_renderer.render_logic_checklist(mix_plan)
    if args.out:
        Path(args.out).write_text(md + "\n", encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(md)
    return 0


def _run_validate_output(args) -> int:
    report = validate_output(args.output)
    print(f"Validator: {report['validator']}")
    for f in report["files"]:
        status = f["status"]
        mark = "✓" if status == "ok" else "✗"
        print(f"  {mark} {f['file']} ({status})")
    if report["errors"]:
        print("\nErrors:")
        for e in report["errors"]:
            print(f"  - {e}")
    print(f"\n{'PASS' if report['ok'] else 'FAIL'}")
    return 0 if report["ok"] else 1


def _run_compare_reference(args) -> int:
    bounce = load_audio(args.bounce)
    reference = load_audio(args.reference)
    delta = compare_to_reference(bounce, reference)
    if args.out:
        Path(args.out).write_text(json.dumps(delta, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(json.dumps(delta, indent=2))
    return 0


def _run_suggest_creative(args) -> int:
    with open(args.plan, "r", encoding="utf-8") as fh:
        mix_plan = json.load(fh)
    hyps = generate_creative_hypotheses(mix_plan, records=[])
    print(json.dumps({"creative_hypotheses": hyps}, indent=2))
    return 0


def _run_status(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest, bounce_path=args.bounce)
    print(render_status(result))
    return 0


def _run_creative(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest, bounce_path=args.bounce, creative_mode=args.mode)
    write_artifacts(result, args.out)
    c = result.creative
    print(f"Creative engine (mode: {c['search_mode']})")
    print(f"Static vs dynamic: {c['static_vs_dynamic']['recommendation']}")
    governed = {b["problem_id"]: b for b in result.governance.get("governed_branches", [])}
    for branch in c["branches"]:
        win = branch.get("winning", {})
        gov = governed.get(branch["problem_id"], {})
        print(f"\n• {branch['problem']}")
        for v in branch["variants"]:
            print(f"    {v['name']:<20} overall {v['scores']['overall_score']:<5} ({v['scores']['overall_verdict']})")
        print(f"    → top-scored: {win.get('winning_variant')}  |  governed pick: {gov.get('governed_winner')}")
    return 0


def _run_governance(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest, bounce_path=args.bounce)
    write_artifacts(result, args.out)
    g = result.governance
    truth = g["emotional_truth_lock"]
    print(f"Emotional truth ({truth.get('lean')}): {truth.get('statement') or '—'}")
    print("\nListener panel:")
    for who, note in g["listener_panel"].items():
        print(f"  {who}: {note}")
    print(f"\nStop iterating: {g['stop_conditions']['should_stop']}")
    for r in g["stop_conditions"]["reasons"]:
        print(f"  - {r}")
    return 0


def _run_mixer_feedback(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest, bounce_path=args.bounce)
    fb = result.governance["mixer_feedback"]
    print(fb.get(args.tone, fb["collaborative"]))
    return 0


def _run_regression(args) -> int:
    report = run_regression_suite(args.fixtures, update_golden=args.update_golden)
    if args.update_golden:
        print("Updated golden snapshots for:", ", ".join(report.get("updated", [])))
        return 0
    print(json.dumps(report, indent=2))
    if report["critical_failures"]:
        print(f"\nREGRESSION FAILED: {len(report['critical_failures'])} critical failure(s)")
        return 1
    print(f"\nPASS — {report['passed']}/{report['tests_run']} checks "
          f"({len(report['warnings'])} warning(s))")
    return 0


def _run_audit(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest, bounce_path=args.bounce)
    write_artifacts(result, args.out)
    for a in result.source_audits["audits"]:
        flags = f"  [red flags: {', '.join(a['red_flags'])}]" if a["red_flags"] else ""
        print(f"\n{a['track']} — {a['auditor_type']} ({a['source_kind']}){flags}")
        for r in a["recommendations"]:
            print(f"  • {r}")
    return 0


def _run_memory_record(args) -> int:
    manifest = _load_manifest(args.manifest)
    result = analyze(args.stems, manifest, bounce_path=args.bounce)
    mem = ProjectMemory(args.memory_dir)
    record = mem.record_pass(args.name, result, input_bounce=args.bounce)
    mem.record_plan_decisions(result)
    print(f"Recorded pass '{record['pass_name']}' ({record['date']}).")
    if record["improved"]:
        print("  improved: " + ", ".join(record["improved"]))
    if record["got_worse"]:
        print("  got worse: " + ", ".join(record["got_worse"]))
    if not record["improved"] and not record["got_worse"]:
        print("  (first pass or no change vs previous)")
    return 0


def _run_memory_show(args) -> int:
    mem = ProjectMemory(args.memory_dir)
    history = mem.history()
    print(f"Mix pass history ({len(history)} pass(es)):")
    for p in history:
        overall = p["scores"].get("overall_mix_readiness_score")
        print(f"  - {p['pass_name']} [{p['date']}] overall {overall} "
              f"| improved {len(p['improved'])} | worse {len(p['got_worse'])}")
    taste = mem.taste_profile().get("profile", [])
    if taste:
        print("Taste profile:")
        for t in taste:
            print(f"  - {t}")
    ledger = mem.ledger()
    print(f"Decision ledger: {len(ledger)} entr(ies).")
    return 0


def _run_feedback(args) -> int:
    mem = ProjectMemory(args.memory_dir)
    taste = mem.add_feedback(args.label, context=args.context)
    print(f"Recorded feedback '{args.label}'. Taste profile now:")
    for t in taste["profile"]:
        print(f"  - {t}")
    if not taste["profile"]:
        print("  (need more feedback to form a stable preference)")
    return 0


def _run_album(args) -> int:
    base = Path(args.projects)
    results, names = [], []
    for sub in sorted(base.iterdir()):
        manifest_path = sub / "project_manifest.json"
        if manifest_path.exists():
            manifest = _load_manifest(str(manifest_path))
            results.append(analyze(str(sub / "stems"), manifest))
            names.append(sub.name)
    if not results:
        print(f"No projects (with project_manifest.json) found under {base}")
        return 1
    report = analyze_album(results, names)
    print(f"Album coherence: {report['coherence_score']}/100 — {report['verdict']}")
    print(f"Consistency: {report['consistency']}")
    if report["outliers"]:
        print("Outliers:")
        for o in report["outliers"]:
            print(f"  - {o['name']} stands out on {', '.join(o['stands_out_on'])}")
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="logic-mix-os", description="Local-first Logic Pro mix decision system.")
    p.add_argument("--version", action="version", version=f"logic-mix-os {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    def add_common(sp):
        sp.add_argument("--stems", help="Folder of exported stems")
        sp.add_argument("--manifest", help="project_manifest.json")
        sp.add_argument("--out", default="./output", help="Output directory")

    a = sub.add_parser("analyze", help="Full analysis + mix plan")
    add_common(a)
    a.add_argument("--bounce", help="Optional stereo bounce for section analysis")
    a.add_argument("--reference", help="Optional reference track")
    a.set_defaults(func=_run_analyze)

    di = sub.add_parser("detect-identities", help="Detect source material + instrument identity")
    add_common(di)
    di.set_defaults(func=_run_detect_identities)

    asx = sub.add_parser("analyze-sections", help="Per-section metrics + contrast")
    add_common(asx)
    asx.add_argument("--bounce", help="Optional stereo bounce")
    asx.set_defaults(func=_run_analyze_sections)

    gp = sub.add_parser("generate-plan", help="Generate the mix plan")
    add_common(gp)
    gp.add_argument("--bounce", help="Optional stereo bounce")
    gp.add_argument("--reference", help="Optional reference track")
    gp.add_argument("--analysis", help="(accepted for compatibility; analysis is recomputed)")
    gp.set_defaults(func=_run_generate_plan)

    rc = sub.add_parser("render-checklist", help="Render the Logic checklist from a mix_plan.json")
    rc.add_argument("--plan", required=True, help="Path to mix_plan.json")
    rc.add_argument("--out", help="Optional output .md path (default: stdout)")
    rc.set_defaults(func=_run_render_checklist)

    vo = sub.add_parser("validate-output", help="Validate an output directory against the schemas")
    vo.add_argument("--output", required=True, help="Output directory to validate")
    vo.set_defaults(func=_run_validate_output)

    cr = sub.add_parser("compare-reference", help="Compare a bounce to a reference track")
    cr.add_argument("--bounce", required=True)
    cr.add_argument("--reference", required=True)
    cr.add_argument("--out", help="Optional output .json path (default: stdout)")
    cr.set_defaults(func=_run_compare_reference)

    sc = sub.add_parser("suggest-creative-variants", help="Creative hypotheses stub from a mix_plan.json")
    sc.add_argument("--plan", required=True, help="Path to mix_plan.json")
    sc.set_defaults(func=_run_suggest_creative)

    st = sub.add_parser("status", help="Operator 'control room' status surface (text)")
    add_common(st)
    st.add_argument("--bounce", help="Optional stereo bounce")
    st.set_defaults(func=_run_status)

    rg = sub.add_parser("regression", help="Run the golden-output + doctrine regression suite")
    rg.add_argument("--fixtures", default="./fixtures", help="Fixtures directory")
    rg.add_argument("--update-golden", action="store_true", help="(Re)write golden snapshots instead of comparing")
    rg.set_defaults(func=_run_regression)

    cv = sub.add_parser("creative", help="Creative experimentation engine (variants + governance)")
    add_common(cv)
    cv.add_argument("--bounce", help="Optional stereo bounce")
    cv.add_argument("--mode", help="Search mode (conservative, halee_depth, ramone_vocal_truth, "
                                   "dramatic_contrast, deconstructive, experimental)")
    cv.set_defaults(func=_run_creative)

    gv = sub.add_parser("governance", help="Taste protection: truth lock, listener panel, stop conditions")
    add_common(gv)
    gv.add_argument("--bounce", help="Optional stereo bounce")
    gv.set_defaults(func=_run_governance)

    mf = sub.add_parser("mixer-feedback", help="Render diagnosis as mixer-facing feedback in a chosen tone")
    add_common(mf)
    mf.add_argument("--bounce", help="Optional stereo bounce")
    mf.add_argument("--tone", default="collaborative",
                    choices=["collaborative", "producer", "direct", "technical", "do_not"])
    mf.set_defaults(func=_run_mixer_feedback)

    mr = sub.add_parser("memory-record", help="Analyse and record a mix pass to project memory")
    add_common(mr)
    mr.add_argument("--bounce", help="Optional stereo bounce")
    mr.add_argument("--memory-dir", required=True, help="Project memory directory")
    mr.add_argument("--name", required=True, help="Mix pass name (e.g. mix_pass_03)")
    mr.set_defaults(func=_run_memory_record)

    ms = sub.add_parser("memory-show", help="Show mix pass history, taste profile, and ledger size")
    ms.add_argument("--memory-dir", required=True)
    ms.set_defaults(func=_run_memory_show)

    fb = sub.add_parser("feedback", help="Record taste feedback (e.g. 'too wide', 'too modern')")
    fb.add_argument("--memory-dir", required=True)
    fb.add_argument("--label", required=True)
    fb.add_argument("--context", help="Optional note")
    fb.set_defaults(func=_run_feedback)

    al = sub.add_parser("album", help="Album-level coherence across a folder of projects")
    al.add_argument("--projects", required=True, help="Folder containing project subfolders")
    al.add_argument("--out", help="Optional output .json path")
    al.set_defaults(func=_run_album)

    au = sub.add_parser("audit", help="Source-aware auditors (live / synth / sampler / loop)")
    add_common(au)
    au.add_argument("--bounce", help="Optional stereo bounce")
    au.set_defaults(func=_run_audit)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
