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
from .analyzers.audio_loader import load_audio
from .analyzers.reference_comparator import compare_to_reference
from .pipeline import analyze, write_artifacts
from .planners.next_pass_planner import generate_creative_hypotheses
from .project import load_manifest
from .renderers import checklist_renderer
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

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
