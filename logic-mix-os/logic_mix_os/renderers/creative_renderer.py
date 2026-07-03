"""Renderers for the creative engine and governance/taste reports."""

from __future__ import annotations

from typing import Dict


def render_creative(creative: Dict) -> str:
    out = ["# Creative Experimentation", ""]
    out.append(f"**Search mode:** `{creative.get('search_mode')}` — {creative.get('search_mode_bias')}")
    # P-033: the fallback evidence renders where the mode is reported — the
    # key is present only when a requested mode was substituted, so this line
    # emits zero bytes on every run whose mode resolved from the profile's own
    # table.
    fallback = creative.get("search_mode_fallback")
    if fallback:
        out.append("")
        out.append(f"_{fallback['reason']}_")
    # P-042 (requirement 10): the resolved mode's profile-authored reach —
    # the key is present only when the mode actually forks candidate
    # generation, so this emits zero bytes on every neutral/default run.
    decl = creative.get("search_mode_declarations")
    if decl:
        favors = ", ".join(f"`{k}`" for k in decl["favor_kinds"]) or "—"
        suppresses = ", ".join(f"`{k}`" for k in decl["suppress_kinds"]) or "—"
        line = (f"**Mode reach (profile-authored):** favors {favors}; "
                f"suppresses {suppresses}")
        # P-043: the authored EXTENDED-vocabulary reach — the key is present
        # only when the mode reaches, so runs without reach render this line
        # byte-identically to their P-042 form.
        if decl.get("reach_kinds"):
            line += "; reaches for " + ", ".join(f"`{k}`" for k in decl["reach_kinds"])
        line += f" — capped at `{decl['allowed_risk']}` risk"
        out.append("")
        out.append(line)
    out.append("")

    svd = creative.get("static_vs_dynamic", {})
    out.append("## Static vs. Dynamic")
    out.append("")
    out.append(f"- Static mix: {svd.get('static_mix_score')}/100")
    out.append(f"- Dynamic mix: {svd.get('dynamic_mix_score')}/100")
    out.append(f"- {svd.get('recommendation')}")
    out.append("")

    out.append("## Variant Branches")
    out.append("")
    for branch in creative.get("branches", []):
        out.append(f"### {branch['problem']}")
        out.append("")
        out.append("| Variant | Kind | Overall | Vocal belief | Contrast | Translation | Verdict |")
        out.append("|---|---|---|---|---|---|---|")
        for v in branch["variants"]:
            s = v["scores"]
            out.append(f"| {v['name']} | `{v['kind']}` | {s['overall_score']} | {s['vocal_belief_score']} "
                       f"| {s['section_contrast_score']} | {s['translation_risk']} | {s['overall_verdict']} |")
        out.append("")
        # P-042 (requirement 10): what the mode fork ACTUALLY did to this
        # branch's candidate set — present only on forking modes; silent when
        # nothing applied to this branch.
        fork = branch.get("mode_fork")
        if fork:
            notes = []
            if fork["suppressed"]:
                notes.append("suppressed " + ", ".join(f"`{k}`" for k in fork["suppressed"]))
            if fork["favored"]:
                notes.append("favored " + ", ".join(f"`{k}`" for k in fork["favored"]))
            # P-043: what the authored reach ACTUALLY added to this branch —
            # the keys exist only when the mode reaches (evidence-key
            # discipline), so non-reaching runs render zero new bytes.
            if fork.get("reached"):
                notes.append("reached for " + ", ".join(f"`{k}`" for k in fork["reached"]))
            if fork["risk_capped"]:
                notes.append("favor refused by the allowed-risk cap: "
                             + ", ".join(f"`{k}`" for k in fork["risk_capped"]))
            if fork.get("reach_capped"):
                notes.append("reach refused by the allowed-risk cap: "
                             + ", ".join(f"`{k}`" for k in fork["reach_capped"]))
            if fork["suppression_fallback"]:
                notes.append("suppression would have emptied this set — "
                             "the full neutral pool was emitted (fallback)")
            if notes:
                out.append(f"_Mode fork: {'; '.join(notes)}._")
                out.append("")
        win = branch.get("winning")
        if win:
            out.append(f"**Top-scored:** {win['winning_variant']} — {win['reason']}")
            out.append("")
            out.append("Keep moves:")
            for m in win["keep_moves"]:
                out.append(f"- {m}")
            out.append("")

    out.append("## Guardrails")
    out.append("")
    for g in creative.get("guardrails", []):
        out.append(f"- {g}")
    out.append("")
    out.append(f"> {creative.get('philosophy')}")
    out.append("")
    return "\n".join(out)


def render_governance(governance: Dict) -> str:
    out = ["# Governance & Taste Protection", ""]

    truth = governance.get("emotional_truth_lock", {})
    out.append("## Emotional Truth Lock")
    out.append("")
    if truth.get("statement"):
        out.append(f"> {truth['statement']}  _(lean: {truth.get('lean')})_")
        out.append("")
        for imp in truth.get("implications", []):
            out.append(f"- {imp}")
    else:
        out.append("_No emotional truth supplied in the manifest intent._")
    out.append("")

    out.append("## Governed Variant Selection")
    out.append("")
    for b in governance.get("governed_branches", []):
        g = b.get("governance") or {}
        tri = g.get("taste_triangle", {})
        out.append(f"- **{b['problem']}** → winner `{b.get('governed_winner')}` "
                   f"(truth {g.get('emotional_truth_alignment')}, "
                   f"taste emotion/craft/identity {tri.get('emotion')}/{tri.get('craft')}/{tri.get('identity')})")
        if g.get("constraint_violations"):
            out.append(f"  - ⚠️ would violate: {', '.join(g['constraint_violations'])}")
        if g.get("false_progress"):
            out.append(f"  - false-progress watch: {g['false_progress']['note']}")
        if g.get("emotional_overfit"):
            out.append(f"  - overfit watch: {g['emotional_overfit']['note']}")
    out.append("")

    at = governance.get("anti_template")
    if at:
        out.append(f"## Anti-Template\n\n⚠️ {at['pattern']} — {at['risk']}\n")

    ref = governance.get("reference_sanity", {})
    if ref.get("available"):
        out.append("## Reference Sanity")
        out.append("")
        out.append(f"- Use for: {', '.join(ref.get('use_for', [])) or '—'}")
        out.append(f"- Do NOT use for: {', '.join(ref.get('do_not_use_for', [])) or '—'}")
        out.append(f"- {ref.get('rule')}")
        out.append("")

    panel = governance.get("listener_panel", {})
    if panel:
        out.append("## Listener Panel")
        out.append("")
        for who, note in panel.items():
            out.append(f"- **{who.replace('_', ' ')}**: {note}")
        out.append("")

    stop = governance.get("stop_conditions", {})
    out.append("## Stop Conditions")
    out.append("")
    reasons = stop.get("reasons", [])
    if stop.get("should_stop"):
        out.append("**READY TO STOP** — stop conditions met.")
        out.append("")
        for r in reasons:
            out.append(f"- {r}")
        warning = stop.get("warning")
        if warning:
            out.append(f"- ⚠️ {warning}")
    else:
        out.append("**NOT YET — keep iterating**")
        out.append("")
        for r in reasons:
            out.append(f"- {r}")
    out.append("")

    fb = governance.get("mixer_feedback", {})
    if fb:
        out.append("## Mixer Communication (tones)")
        out.append("")
        for tone, text in fb.items():
            out.append(f"- **{tone}**: {text}")
        out.append("")

    out.append("## Kill-Switches (never auto-applied)")
    out.append("")
    for k in governance.get("kill_switches", []):
        out.append(f"- {k}")
    out.append("")
    return "\n".join(out)
