"""Regression + doctrine-protection suite (build packet sections 51 & 53).

Two layers of protection against silent changes to musical judgment:

1. **Golden snapshots** — a stable, categorical fingerprint of each fixture's
   output (identities, source kinds, depth layers, masking classifications,
   section lift warnings, score bands). Drift is reported, with categorical
   regressions treated as *critical* and score/confidence drift as *warnings*.

2. **Doctrine invariants** — absolute behaviours that must never regress
   (don't foreground stock loops, don't treat all masking as bad, don't widen
   the lead vocal to lift a chorus, don't recommend destructive edits, etc.).

Scores are deterministic given numpy (they do not depend on the loudness
backend), but the golden comparison still uses tolerances so a numpy point
release can't turn a rounding boundary into a false failure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from .constants import LOOP_SAMPLE_KINDS
from .pipeline import ProjectAnalysis, analyze
from .project import load_manifest

SCORE_KEYS = [
    "halee_score",
    "ramone_score",
    "vocal_centrality_score",
    "depth_hierarchy_score",
    "section_contrast_score",
    "static_mix_score",
    "dynamic_mix_score",
    "overall_mix_readiness_score",
]

# Score-drift tolerances (points).
SCORE_WARN = 3.0
SCORE_FAIL = 9.0
CONF_WARN = 0.1


# --------------------------------------------------------------------------- #
# Snapshots
# --------------------------------------------------------------------------- #
def build_snapshot(result: ProjectAnalysis) -> Dict:
    roles = {r["track_id"]: r for r in result.roles}
    source = {s["track_id"]: s for s in result.source_material}
    depth = {d["track_id"]: d for d in result.depth_map}

    tracks = []
    for ident in sorted(result.track_identity, key=lambda x: x["name"]):
        tid = ident["track_id"]
        tracks.append({
            "name": ident["name"],
            "source_kind": source[tid]["source_kind"],
            "instrument_identity": ident["instrument_identity"],
            "identity_family": ident["identity_family"],
            "confidence": round(ident["confidence"], 2),
            "perceptual_role": roles[tid]["perceptual_role"],
            "sacredness": roles[tid]["sacredness"],
            "default_depth": depth[tid]["default_depth"],
        })

    class_counts: Dict[str, int] = {}
    for e in result.masking_report.get("events", []):
        class_counts[e["classification"]] = class_counts.get(e["classification"], 0) + 1

    sections = [
        {"section_id": s["section_id"], "lift_warning": "warning" in s.get("contrast_vs_previous", {})}
        for s in result.section_analysis
    ]

    return {
        "tracks": tracks,
        "masking_classifications": class_counts,
        "sections": sections,
        "scores": {k: result.doctrine_score.get(k) for k in SCORE_KEYS},
        "next_pass_titles": [i["title"] for i in result.mix_plan.get("next_pass", [])],
    }


def compare_snapshots(fixture: str, golden: Dict, current: Dict):
    """Return (tests, passed, critical, warnings)."""
    tests = 0
    passed = 0
    critical: List[str] = []
    warnings: List[str] = []

    gt = {t["name"]: t for t in golden["tracks"]}
    ct = {t["name"]: t for t in current["tracks"]}
    cat = ["source_kind", "instrument_identity", "identity_family", "perceptual_role", "sacredness", "default_depth"]
    for name, g in gt.items():
        tests += 1
        c = ct.get(name)
        if c is None:
            critical.append(f"{fixture}: track '{name}' disappeared from output")
            continue
        diffs = [f"{f} {g[f]}->{c[f]}" for f in cat if g[f] != c[f]]
        if diffs:
            critical.append(f"{fixture}: '{name}' changed: " + ", ".join(diffs))
        else:
            passed += 1
        if abs(g["confidence"] - c["confidence"]) > CONF_WARN:
            warnings.append(f"{fixture}: '{name}' confidence {g['confidence']} -> {c['confidence']}")

    # masking classifications present in golden must remain present
    tests += 1
    missing = [k for k in golden["masking_classifications"] if k not in current["masking_classifications"]]
    if missing:
        critical.append(f"{fixture}: masking classification(s) no longer produced: {missing}")
    else:
        passed += 1

    # section lift warnings must not silently flip off
    tests += 1
    gw = {s["section_id"] for s in golden["sections"] if s["lift_warning"]}
    cw = {s["section_id"] for s in current["sections"] if s["lift_warning"]}
    if gw - cw:
        critical.append(f"{fixture}: section contrast warning lost for {sorted(gw - cw)}")
    else:
        passed += 1

    # score drift
    for k in SCORE_KEYS:
        tests += 1
        g, c = golden["scores"].get(k), current["scores"].get(k)
        if g is None and c is None:
            passed += 1
            continue
        if g is None or c is None:
            critical.append(f"{fixture}: score '{k}' availability changed ({g} -> {c})")
            continue
        diff = abs(g - c)
        if diff > SCORE_FAIL:
            critical.append(f"{fixture}: score '{k}' drifted {g} -> {c} (>{SCORE_FAIL})")
        else:
            passed += 1
            if diff > SCORE_WARN:
                warnings.append(f"{fixture}: score '{k}' drifted {g} -> {c}")

    return tests, passed, critical, warnings


# --------------------------------------------------------------------------- #
# Doctrine invariants
# --------------------------------------------------------------------------- #
def doctrine_invariants(result: ProjectAnalysis) -> List[Dict]:
    records = result.records
    plan = result.mix_plan
    events = result.masking_report.get("events", [])
    lead = next((r for r in records if r["instrument_identity"] == "lead_vocal"), None)
    lead_actions = (
        next((t for t in plan["per_track_actions"] if t["track"] == lead["name"]), None)
        if lead else None
    )
    loops = [r for r in records if r["source_kind"] in LOOP_SAMPLE_KINDS]
    n = len(records) or 1
    forward_count = sum(1 for r in records if r["depth_default"] in {"intimate", "foreground"})
    fg_frac = forward_count / n

    inv: List[Dict] = []

    def add(name, applicable, ok, critical, detail=""):
        inv.append({"name": name, "applicable": applicable, "ok": ok, "critical": critical, "detail": detail})

    # 1. Never recommend destructive edits.
    dz = [a for t in plan["per_track_actions"] for a in t["actions"] if a["risk_class"] >= 5]
    add("no_destructive_edits", True, not dz, True, f"{len(dz)} class-5 action(s)")

    # 2. Don't treat all masking as bad: a bad_masking event must not include a
    #    midground/background participant.
    bad_low = [e for e in events if e["classification"] == "bad_masking"
               and any(d in {"midground", "background"} for d in e.get("depth_layers", []))]
    add("masking_is_hierarchy", bool(events), not bad_low, True,
        f"{len(bad_low)} bad-masking event(s) include a non-forward element")

    # 3. Don't send unidentified tracks into doctrine scoring.
    unident = [r for r in records if not r.get("instrument_identity")]
    add("no_unidentified_in_doctrine", True, not unident, True, f"{len(unident)} record(s) lack an identity")

    # 4. Don't widen the lead vocal as the default chorus-lift move.
    ok4, det4 = True, ""
    if lead_actions:
        for a in lead_actions["actions"]:
            if "widen" in a["setting"].lower() or "width" in a["setting"].lower():
                ok4, det4 = False, f"lead-vocal action mentions width: {a['plugin']}"
    for item in plan.get("next_pass", []):
        d = (item["title"] + " " + item["detail"]).lower()
        if "widen" in d and "lead vocal" in d and "support" not in d and "backing" not in d:
            ok4, det4 = False, "next-pass widens the lead vocal"
    add("no_default_vocal_widening", lead is not None, ok4, True, det4)

    # 5. Respect source type: loops/samples are felt/back + carry a warning.
    viol5 = [
        r["name"] for r in loops
        if not ((r["perceptual_role"] in {"felt", "candidate_for_mute", "transitional"}
                 or r["depth_default"] in {"midground", "background"}) and r.get("source_warnings"))
    ]
    add("source_material_respected", bool(loops), not viol5, True, f"loops not re-contextualised: {viol5}")

    # 6. Don't solve arrangement density only with EQ.
    arr = [b for b in plan["production_vs_mix_boundaries"] if b["boundary_classification"] == "arrangement_problem"]
    ok6 = all(any(k in b["best_fix"].lower() for k in ("mute", "push", "subtract", "background")) for b in arr)
    add("density_not_only_eq", bool(arr), ok6, False, "arrangement boundary should prefer subtraction")

    # 7. Never ignore section contrast.
    ok7 = len(result.section_analysis) < 2 or result.doctrine_score.get("section_contrast_score") is not None
    add("section_contrast_considered", len(result.section_analysis) >= 2, ok7, True, "section_contrast_score missing")

    # 8. Prefer vocal rides before heavier compression.
    has_ride = bool(lead_actions) and any("ride" in au["move"].lower() for au in lead_actions["automation"])
    add("vocal_rides_before_compression", lead is not None, has_ride, True, "no vocal phrase-ride recommended")

    # 9. Don't foreground full-width stock loops by default.
    viol9 = [r["name"] for r in loops if r["depth_default"] in {"foreground", "intimate"}]
    add("loops_not_foregrounded", bool(loops), not viol9, True, f"loops foregrounded: {viol9}")

    # 10. Don't make everything audible at the expense of hierarchy.
    #     Only meaningful for genuinely dense arrangements (high fraction AND a
    #     real number of forward elements) — a 3-track song is not "crowded".
    crowded = fg_frac > 0.6 and forward_count >= 5
    ok10 = (not crowded) or (result.doctrine_score.get("halee_score", 100) < 80) \
        or any(e["classification"] == "width_crowding" for e in events)
    add("hierarchy_flagged_when_crowded", crowded, ok10, True, "crowded arrangement not penalised")

    return inv


# --------------------------------------------------------------------------- #
# Suite runner
# --------------------------------------------------------------------------- #
def _fixture_dirs(base: Path) -> List[Path]:
    return sorted(p for p in base.iterdir() if (p / "project_manifest.json").exists())


def run_regression_suite(base: Optional[str | Path] = None, update_golden: bool = False) -> Dict:
    base = Path(base or "./fixtures")
    suite = {
        "tests_run": 0,
        "passed": 0,
        "failed": 0,
        "critical_failures": [],
        "warnings": [],
    }
    if update_golden:
        suite["updated"] = []

    for fx_dir in _fixture_dirs(base):
        name = fx_dir.name
        manifest = load_manifest(fx_dir / "project_manifest.json")
        result = analyze(str(fx_dir / "stems"), manifest)
        snapshot = build_snapshot(result)

        golden_path = fx_dir / "golden" / "snapshot.json"
        if update_golden:
            golden_path.parent.mkdir(parents=True, exist_ok=True)
            with open(golden_path, "w", encoding="utf-8") as fh:
                json.dump(snapshot, fh, indent=2)
                fh.write("\n")
            suite["updated"].append(name)
        else:
            if golden_path.exists():
                with open(golden_path, "r", encoding="utf-8") as fh:
                    golden = json.load(fh)
                tests, passed, critical, warnings = compare_snapshots(name, golden, snapshot)
                suite["tests_run"] += tests
                suite["passed"] += passed
                suite["failed"] += len(critical)
                suite["critical_failures"].extend(critical)
                suite["warnings"].extend(warnings)
            else:
                suite["warnings"].append(f"{name}: no golden snapshot (run with --update-golden)")

        # Doctrine invariants always run (independent of golden).
        for item in doctrine_invariants(result):
            if not item["applicable"]:
                continue
            suite["tests_run"] += 1
            if item["ok"]:
                suite["passed"] += 1
            else:
                suite["failed"] += 1
                msg = f"{name}: {item['name']} — {item['detail']}"
                (suite["critical_failures"] if item["critical"] else suite["warnings"]).append(msg)

    return suite
