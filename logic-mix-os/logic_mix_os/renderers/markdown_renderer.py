"""Markdown report renderers (human-readable views of the JSON artifacts)."""

from __future__ import annotations

from typing import Dict, List, Optional


def _fmt_score(v) -> str:
    return "n/a" if v is None else f"{v}/100"


def _bar(v, width: int = 20) -> str:
    if v is None:
        return ""
    filled = int(round((v / 100.0) * width))
    return "█" * filled + "░" * (width - filled)


# --------------------------------------------------------------------------- #
def render_source_material_report(items: List[Dict]) -> str:
    out = ["# Source Material Report", ""]
    out.append("What kind of Logic object each track is, and what can actually be changed.")
    out.append("")
    for it in items:
        out.append(f"## {it['name']}  `{it['track_id']}`")
        out.append("")
        out.append(f"- **Source kind:** `{it['source_kind']}` (confidence {it['confidence']:.2f})")
        out.append(f"- **Editable:** {', '.join(it['editable_domains'])}")
        if it.get("not_editable_directly"):
            out.append(f"- **Not directly editable:** {', '.join(it['not_editable_directly'])}")
        ev = ", ".join(f"{k}: {v}" for k, v in it.get("evidence", {}).items())
        if ev:
            out.append(f"- **Evidence:** {ev}")
        for w in it.get("warnings", []):
            out.append(f"- ⚠️ {w}")
        out.append("")
    return "\n".join(out)


def render_track_identity_report(items: List[Dict]) -> str:
    out = ["# Track Identity Report", ""]
    out.append("What each sound *is* (separate from what it is *doing*).")
    out.append("")
    out.append("| Track | Identity | Family | Confidence | Alternates |")
    out.append("|---|---|---|---|---|")
    for it in items:
        alts = ", ".join(
            f"{a['instrument_identity']} ({a['confidence']:.2f})"
            for a in it.get("alternate_candidates", [])
        ) or "—"
        out.append(
            f"| {it['name']} | `{it['instrument_identity']}` | {it['identity_family']} "
            f"| {it['confidence']:.2f} | {alts} |"
        )
    out.append("")
    out.append("### Evidence")
    for it in items:
        ev = it.get("evidence", {})
        clues = ", ".join(ev.get("filename_clues", [])) or "—"
        out.append(
            f"- **{it['name']}**: name clue: {clues}; "
            f"{ev.get('spectral_profile', 'n/a')}; "
            f"{ev.get('transient_profile', 'n/a')}; {ev.get('stereo_profile', 'n/a')}."
        )
    out.append("")
    return "\n".join(out)


def render_halee_ramone_verdict(mix_plan: Dict, doctrine_score: Dict) -> str:
    out = ["# Halee / Ramone Mix Verdict", ""]
    truth = mix_plan.get("singular_emotional_truth")
    if truth:
        out.append(f"> **Emotional truth:** {truth}")
        out.append("")

    out.append("## Overall Diagnosis")
    out.append("")
    out.append(mix_plan.get("overall_diagnosis", "Analysis complete."))
    out.append("")

    out.append("## Scores")
    out.append("")
    rows = [
        ("Overall mix readiness", "overall_mix_readiness_score"),
        ("Roy Halee (physical space)", "halee_score"),
        ("Phil Ramone (vocal centrality)", "ramone_score"),
        ("Vocal centrality", "vocal_centrality_score"),
        ("Depth hierarchy", "depth_hierarchy_score"),
        ("Section contrast", "section_contrast_score"),
        ("Static mix", "static_mix_score"),
        ("Dynamic mix", "dynamic_mix_score"),
    ]
    out.append("| Dimension | Score | |")
    out.append("|---|---|---|")
    for label, key in rows:
        v = mix_plan.get(key)
        out.append(f"| {label} | {_fmt_score(v)} | `{_bar(v)}` |")
    out.append("")

    out.append("**The Halee test:** Can the listener visualize musicians in a real physical space?  ")
    out.append("**The Ramone test:** Do I believe every word the singer is saying?")
    out.append("")

    risks = mix_plan.get("biggest_risks", [])
    if risks:
        out.append("## Biggest Risks")
        out.append("")
        for r in risks:
            out.append(f"- {r}")
        out.append("")

    opps = mix_plan.get("best_opportunities", [])
    if opps:
        out.append("## Best Opportunities")
        out.append("")
        for o in opps:
            out.append(f"- {o}")
        out.append("")

    nxt = mix_plan.get("next_pass", [])
    if nxt:
        out.append("## Top Recommended Moves")
        out.append("")
        for item in nxt:
            out.append(f"{item['priority']}. **{item['title']}** — {item['detail']}")
        out.append("")

    boundaries = mix_plan.get("production_vs_mix_boundaries", [])
    if boundaries:
        out.append("## Production vs. Mix Boundaries")
        out.append("")
        for b in boundaries:
            out.append(f"- **{b['issue']}** → `{b['boundary_classification']}`. {b['reason']} _Best fix:_ {b['best_fix']}")
        out.append("")

    nc = mix_plan.get("negative_constraints", [])
    if nc:
        out.append("## Negative Constraints (what this must NOT become)")
        out.append("")
        for c in nc:
            out.append(f"- {c}")
        out.append("")

    return "\n".join(out)


def render_next_pass(next_pass: List[Dict], creative_hypotheses: List[Dict]) -> str:
    out = ["# Next Pass Recommendations", ""]
    if not next_pass:
        out.append("_No high-priority moves detected; validate and move to mastering-readiness checks._")
        out.append("")
    for item in next_pass:
        out.append(f"## Priority {item['priority']} — {item['title']}")
        out.append("")
        out.append(item["detail"])
        out.append("")

    out.append("## Optional Creative Tests")
    out.append("")
    out.append("_Non-destructive hypotheses to A/B against the static baseline._")
    out.append("")
    for h in creative_hypotheses:
        out.append(f"- **{h['hypothesis_id']}** — {h['problem']}")
        out.append(f"  - Variant: {h['variant']}")
        out.append(f"  - Risk: {h['risk']}")
        out.append(f"  - Validate: {h['validation']}")
    out.append("")

    out.append("## Validation Checklist")
    out.append("")
    out.append("- [ ] Vocal still believable and intelligible after changes")
    out.append("- [ ] Chorus feels earned (contrast vs. verse improved)")
    out.append("- [ ] No new mono-compatibility or low-end problems")
    out.append("- [ ] Emotional truth preserved")
    out.append("- [ ] Changes are reversible (duplicates / saved presets)")
    out.append("")
    return "\n".join(out)


def render_automation_plan(automation_plan: List[Dict]) -> str:
    out = ["# Automation Plan", ""]
    out.append("Automation is planned from the start, not added later. Prefer rides over static settings.")
    out.append("")
    for entry in automation_plan:
        title = entry.get("name", entry.get("section", "section"))
        out.append(f"## {title}  ·  `{entry.get('gesture', '')}`")
        out.append("")
        if entry.get("emotional_goal"):
            out.append(f"_Emotional goal: {entry['emotional_goal']}_")
            out.append("")
        for move in entry.get("moves", []):
            if isinstance(move, dict):
                out.append(f"- **{move.get('track', '')}** — {move.get('parameter', '')}: {move.get('move', '')}")
            else:
                out.append(f"- {move}")
        if entry.get("contrast_warning"):
            out.append("")
            out.append(f"> ⚠️ {entry['contrast_warning']}")
        out.append("")
    return "\n".join(out)


def render_expanded_analysis(expanded: Dict) -> str:
    out = ["# Expanded Analysis", ""]

    tr = expanded.get("translation", {})
    if tr.get("profiles"):
        out.append(f"## Translation  ·  score {tr.get('translation_score')}/100")
        out.append("")
        out.append("| Profile | Severity | Risks |")
        out.append("|---|---|---|")
        for p in tr["profiles"]:
            risks = "; ".join(p["risks"]) or "—"
            out.append(f"| {p['profile']} | {p['severity']} | {risks} |")
        out.append("")

    mono = expanded.get("mono_compatibility", {})
    out.append(f"## Mono Compatibility  ·  score {mono.get('mono_score')}/100")
    out.append("")
    out.append(f"Mix mono-collapse: {mono.get('mix_mono_collapse_loss_db')} dB · "
               f"phase correlation {mono.get('mix_phase_correlation')}")
    for e in mono.get("events", []):
        out.append(f"- ⚠️ **{e['track']}** ({e['severity']}): {e['issue']} _{e['recommendation']}_")
    out.append("")

    dens = expanded.get("arrangement_density", {})
    if dens.get("per_section"):
        out.append("## Arrangement Density")
        out.append("")
        out.append("| Section | Intimate | Foreground | Midground | Background | Forward |")
        out.append("|---|---|---|---|---|---|")
        for p in dens["per_section"]:
            c = p["layer_counts"]
            out.append(f"| {p['section_id']} | {c['intimate']} | {c['foreground']} | {c['midground']} "
                       f"| {c['background']} | {p['forward_count']} |")
        out.append("")
        for p in dens["per_section"]:
            if p["warning"]:
                out.append(f"- ⚠️ {p['warning']}")
        out.append("")

    le = expanded.get("listener_experience", {})
    if le.get("journey"):
        out.append("## Listener Experience (what a fan hears)")
        out.append("")
        out.append(f"_{le.get('summary')}_")
        out.append("")
        for j in le["journey"]:
            out.append(f"- **{j['name']}** ({j['engagement']}): {j['what_a_fan_hears']}")
        for fp in le.get("fatigue_points", []):
            out.append(f"- ⚠️ {fp}")
        out.append("")

    vp = expanded.get("vocal_performance", {})
    if vp.get("available"):
        out.append("## Vocal Performance")
        out.append("")
        out.append(f"Dynamic range ~{vp['dynamic_range_db']} dB; push at {vp['push_moment_sec']}s, "
                   f"pull-back at {vp['pull_back_moment_sec']}s.")
        for r in vp.get("recommendations", []):
            out.append(f"- {r}")
        out.append("")

    tq = expanded.get("transitions", {})
    if tq.get("transitions"):
        out.append("## Transition Quality")
        out.append("")
        for t in tq["transitions"]:
            out.append(f"- **{t['from']} → {t['to']}** ({t['quality']}, {t['rms_jump_db']:+.1f} dB): {t['note']}")
        out.append("")

    groove = expanded.get("groove", {})
    if groove.get("per_track"):
        out.append("## Groove")
        out.append("")
        out.append(f"_{groove.get('summary')}_")
        out.append("")
        for g in groove["per_track"]:
            out.append(f"- **{g['track']}**: {g['feel']} (regularity {g['regularity']})")
        out.append("")

    harm = expanded.get("harmonic", {})
    if harm.get("available"):
        out.append("## Harmonic / Melodic")
        out.append("")
        out.append(harm.get("summary", ""))
        out.append("")

    lyr = expanded.get("lyrics", {})
    if lyr.get("available"):
        out.append("## Lyric Alignment")
        out.append("")
        out.append(f"_{lyr.get('summary')}_")
        out.append("")

    return "\n".join(out)


def render_session_intelligence(provenance: Dict, render_graph: Dict, plugin_scan: Dict) -> str:
    out = ["# Session Intelligence", ""]

    out.append("## Sample Provenance")
    out.append("")
    items = provenance.get("items", [])
    if items:
        out.append("| Track | Origin | License | Recognizable | Foreground | Risk |")
        out.append("|---|---|---|---|---|---|")
        for it in items:
            out.append(f"| {it['track']} | {it['sample_origin']} | {it['license_status']} "
                       f"| {it['recognizable']} | {it['foregrounded']} | {it['risk']} |")
        out.append("")
        for it in items:
            if it["risk"] != "low":
                out.append(f"- ⚠️ **{it['track']}** ({it['risk']}): {it['reason']} _{it['recommendation']}_")
    else:
        out.append("_No imported loops/samples to track._")
    out.append("")

    out.append("## Plugin Availability")
    out.append("")
    out.append(f"- Inventory source: {plugin_scan.get('inventory_source')}")
    used = plugin_scan.get("plugins_used", {})
    if used:
        out.append(f"- Recommended plugins: {', '.join(f'{k} ×{v}' for k, v in used.items())}")
    if plugin_scan.get("missing"):
        for m in plugin_scan["missing"]:
            out.append(f"- ⚠️ Missing **{m['plugin']}** → alternatives: {', '.join(m['alternatives'])}")
    else:
        out.append("- ✓ All recommended plugins are available.")
    out.append("")

    out.append("## Render Dependency Graph")
    out.append("")
    nodes = render_graph.get("nodes", [])
    out.append(f"{len(nodes)} nodes (source → stem → mixdown → reports). "
               f"Changing a stem invalidates the mix bounce and every analysis report.")
    out.append("")
    return "\n".join(out)


def render_section_contrast_report(sections: List[Dict]) -> str:
    out = ["# Section Contrast Report", ""]
    out.append("| Section | Goal | RMS (dB) | Width | Δ RMS | Δ Width | Note |")
    out.append("|---|---|---|---|---|---|---|")
    for s in sections:
        m = s["metrics"]
        c = s.get("contrast_vs_previous", {})
        note = "lift warning" if "warning" in c else c.get("note", "")
        out.append(
            f"| {s['name']} | {s.get('emotional_goal', '—')} | {m['rms_dbfs']:.1f} | {m['width']:.2f} "
            f"| {c.get('rms_delta_db', '—')} | {c.get('width_delta', '—')} | {note} |"
        )
    out.append("")
    for s in sections:
        c = s.get("contrast_vs_previous", {})
        if "warning" in c:
            out.append(f"- ⚠️ {c['warning']}")
    out.append("")
    return "\n".join(out)
