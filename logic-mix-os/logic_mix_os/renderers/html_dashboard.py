"""Local static HTML dashboard — the section-50 "mix control room".

Renders one self-contained HTML file (inline CSS, no JS framework, no server,
no network) from a ProjectAnalysis. Open it with file://. This is the local-first
realisation of the section-50 screen map; it visualises state, it does not
execute anything.
"""

from __future__ import annotations

import html
from typing import Dict, List

from ..renderers.checklist_renderer import render_logic_checklist

_CSS = """
:root{--bg:#0f1216;--panel:#171c23;--ink:#e6edf3;--muted:#8b98a5;--line:#222a33;
--good:#3fb950;--warn:#d29922;--bad:#f85149;--accent:#58a6ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:14px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
header{padding:24px 28px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}
h1{margin:0 0 4px;font-size:20px}h2{font-size:15px;margin:0 0 12px;color:var(--accent);
text-transform:uppercase;letter-spacing:.05em}.muted{color:var(--muted)}
nav{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}nav a{color:var(--muted);
text-decoration:none;font-size:12px;padding:3px 8px;border:1px solid var(--line);border-radius:12px}
nav a:hover{color:var(--ink);border-color:var(--accent)}
main{padding:24px 28px;max-width:1100px}section.card{background:var(--panel);
border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:20px}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;
padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600}.bar{height:8px;background:#0a0d11;border-radius:6px;overflow:hidden;min-width:120px}
.bar>i{display:block;height:100%;background:linear-gradient(90deg,#1f6feb,#58a6ff)}
.scoregrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.score{background:#0d1117;border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.score b{font-size:20px}.big{font-size:42px;font-weight:700}.flag{color:var(--warn)}
.bad{color:var(--bad)}.good{color:var(--good)}.pill{display:inline-block;padding:1px 7px;border:1px solid var(--line);
border-radius:10px;font-size:11px;color:var(--muted)}pre{white-space:pre-wrap;background:#0d1117;
border:1px solid var(--line);border-radius:8px;padding:14px;font-size:12px;overflow:auto}
ul{margin:6px 0;padding-left:20px}li{margin:2px 0}
"""


def _esc(x) -> str:
    return html.escape(str(x)) if x is not None else ""


def _bar(v) -> str:
    if v is None:
        return '<span class="muted">n/a</span>'
    pct = max(0, min(100, float(v)))
    return f'<div class="bar"><i style="width:{pct}%"></i></div>'


def _table(headers: List[str], rows: List[List[str]]) -> str:
    head = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _card(anchor: str, title: str, inner: str) -> str:
    return f'<section class="card" id="{anchor}"><h2>{_esc(title)}</h2>{inner}</section>'


def render_dashboard(result) -> str:
    ds = result.doctrine_score
    proj = result.project
    cards: List[str] = []

    # --- scores ---
    score_rows = [
        ("Roy Halee (space)", "halee_score"), ("Phil Ramone (vocal)", "ramone_score"),
        ("Vocal centrality", "vocal_centrality_score"), ("Depth hierarchy", "depth_hierarchy_score"),
        ("Section contrast", "section_contrast_score"), ("Static mix", "static_mix_score"),
        ("Dynamic mix", "dynamic_mix_score"), ("Translation", None), ("Mono", None),
    ]
    score_html = '<div class="scoregrid">'
    for label, key in score_rows:
        if key:
            v = ds.get(key)
        else:
            v = result.mix_plan.get("translation_score" if label == "Translation" else "mono_compatibility_score")
        vtxt = "n/a" if v is None else f"{v}"
        score_html += f'<div class="score"><div class="muted">{_esc(label)}</div><b>{vtxt}</b>{_bar(v)}</div>'
    score_html += "</div>"
    cards.append(_card("scores", "Scores", score_html))

    # --- section map ---
    rows = []
    for s in result.section_analysis:
        sid = s["section_id"]
        fwd = sum(1 for r in result.records
                  if r["depth_by_section"].get(sid, r["depth_default"]) in {"intimate", "foreground"})
        note = '<span class="flag">no lift</span>' if "warning" in s.get("contrast_vs_previous", {}) else ""
        crowd = ' <span class="bad">CROWDED</span>' if fwd >= 6 else ""
        m = s["metrics"]
        rows.append([_esc(s["name"]), _esc(s.get("emotional_goal")), f'{m["rms_dbfs"]:.1f}',
                     f'{m["width"]:.2f}', f'{m["brightness"]:.2f}', f'{m["density"]:.2f}', f'{fwd}{crowd}', note])
    if rows:
        cards.append(_card("sections", "Section Map",
                           _table(["Section", "Goal", "RMS", "Width", "Bright", "Density", "Fwd", ""], rows)))

    # --- tracks (identity + source + role + depth) ---
    sm = {x["track_id"]: x for x in result.source_material}
    roles = {x["track_id"]: x for x in result.roles}
    depth = {x["track_id"]: x for x in result.depth_map}
    rows = []
    for i in result.track_identity:
        tid = i["track_id"]
        rows.append([_esc(i["name"]),
                     f'{_esc(i["instrument_identity"])} <span class="pill">{i["confidence"]:.2f}</span>',
                     _esc(sm[tid]["source_kind"]), _esc(roles[tid]["perceptual_role"]),
                     _esc(roles[tid]["sacredness"]), _esc(depth[tid]["default_depth"])])
    cards.append(_card("tracks", "Tracks — Identity / Source / Role / Depth",
                       _table(["Track", "Identity", "Source kind", "Felt/Heard", "Sacredness", "Depth"], rows)))

    # --- masking ---
    mrows = []
    for e in result.masking_report.get("events", []):
        cls = e["classification"]
        cls_html = f'<span class="bad">{cls}</span>' if e["severity"] == "critical" else _esc(cls)
        mrows.append([_esc(", ".join(e["elements"])), _esc(e.get("frequency_range")),
                      _esc(e.get("section")), cls_html, _esc(e.get("recommendation"))])
    if mrows:
        cards.append(_card("masking", "Masking (hierarchy)",
                           _table(["Elements", "Range", "Section", "Type", "Recommendation"], mrows)))

    # --- next pass ---
    np_html = "<ol>" + "".join(
        f'<li><b>{_esc(i["title"])}</b> — {_esc(i["detail"])}</li>' for i in result.mix_plan.get("next_pass", [])
    ) + "</ol>"
    cards.append(_card("nextpass", "Next Pass", np_html))

    # --- automation narrative ---
    arows = []
    for a in result.mix_plan.get("automation_plan", []):
        moves = a.get("moves", [])
        moves_txt = "; ".join(m if isinstance(m, str) else m.get("move", "") for m in moves[:4])
        arows.append([_esc(a.get("name", a.get("section"))), _esc(a.get("gesture")), _esc(moves_txt)])
    cards.append(_card("automation", "Automation Narrative", _table(["Section", "Gesture", "Moves"], arows)))

    # --- expanded: translation + mono + listener ---
    exp = result.expanded
    tr = exp.get("translation", {})
    trows = [[_esc(p["profile"]),
              f'<span class="{"bad" if p["severity"]=="high" else "flag" if p["severity"]=="moderate" else "good"}">{p["severity"]}</span>',
              _esc("; ".join(p["risks"]) or "—")] for p in tr.get("profiles", [])]
    inner = f'<p class="muted">Translation score {tr.get("translation_score")}/100 · ' \
            f'Mono score {exp.get("mono_compatibility", {}).get("mono_score")}/100</p>'
    inner += _table(["Profile", "Severity", "Risks"], trows)
    le = exp.get("listener_experience", {})
    if le.get("journey"):
        inner += f'<p class="muted">{_esc(le.get("summary"))}</p><ul>'
        inner += "".join(f'<li><b>{_esc(j["name"])}</b> ({_esc(j["engagement"])}): {_esc(j["what_a_fan_hears"])}</li>'
                         for j in le["journey"]) + "</ul>"
    cards.append(_card("translation", "Translation · Mono · Listener Experience", inner))

    # --- source audits ---
    aud = "<ul>"
    for a in result.source_audits.get("audits", []):
        flags = f' <span class="bad">[{_esc(", ".join(a["red_flags"]))}]</span>' if a["red_flags"] else ""
        aud += f'<li><b>{_esc(a["track"])}</b> <span class="pill">{_esc(a["auditor_type"])}</span>{flags}<ul>'
        aud += "".join(f"<li>{_esc(r)}</li>" for r in a["recommendations"]) + "</ul></li>"
    aud += "</ul>"
    cards.append(_card("audits", "Source-Aware Audit", aud))

    # --- creative ---
    cr = "<div>"
    for b in result.creative.get("branches", []):
        cr += f'<p><b>{_esc(b["problem"])}</b></p>'
        rows = [[_esc(v["name"]), _esc(v["kind"]), f'{v["scores"]["overall_score"]}',
                 f'{v["scores"]["vocal_belief_score"]}', _esc(v["scores"]["translation_risk"]),
                 _esc(v["scores"]["overall_verdict"])] for v in b["variants"]]
        cr += _table(["Variant", "Kind", "Overall", "Vocal belief", "Translation", "Verdict"], rows)
    cr += "</div>"
    cards.append(_card("creative", "Creative Variants", cr))

    # --- governance ---
    g = result.governance
    truth = g.get("emotional_truth_lock", {})
    gov = f'<p>Emotional truth <span class="pill">{_esc(truth.get("lean"))}</span>: {_esc(truth.get("statement") or "—")}</p>'
    gov += "<p class='muted'>Listener panel</p><ul>"
    gov += "".join(f'<li><b>{_esc(k.replace("_", " "))}</b>: {_esc(v)}</li>' for k, v in g.get("listener_panel", {}).items())
    gov += "</ul>"
    stop = g.get("stop_conditions", {})
    reasons = stop.get("reasons", [])
    if stop.get("should_stop"):
        gov += '<p><b class="good">READY TO STOP</b> — stop conditions met.</p>'
        gov += "<ul>" + "".join(f'<li class="good">{_esc(r)}</li>' for r in reasons) + "</ul>"
        warning = stop.get("warning")
        if warning:
            gov += f'<p class="flag">⚠ {_esc(warning)}</p>'
    else:
        gov += '<p><b class="bad">NOT YET — keep iterating</b></p>'
        gov += "<ul>" + "".join(f'<li>{_esc(r)}</li>' for r in reasons) + "</ul>"
    cards.append(_card("governance", "Governance & Taste", gov))

    # --- logic checklist ---
    cards.append(_card("checklist", "Logic Action Checklist",
                       f"<pre>{_esc(render_logic_checklist(result.mix_plan))}</pre>"))

    # --- nav ---
    anchors = [("scores", "Scores"), ("sections", "Sections"), ("tracks", "Tracks"),
               ("masking", "Masking"), ("nextpass", "Next Pass"), ("automation", "Automation"),
               ("translation", "Translation"), ("audits", "Audits"), ("creative", "Creative"),
               ("governance", "Governance"), ("checklist", "Checklist")]
    nav = "".join(f'<a href="#{a}">{_esc(t)}</a>' for a, t in anchors)

    overall = ds.get("overall_mix_readiness_score")
    header = f"""<header>
      <h1>Logic Mix OS — {_esc(proj.song_title)}</h1>
      <div class="muted">Tempo {_esc(proj.tempo)} · Key {_esc(proj.key)} ·
        {len(result.track_analysis)} tracks · {len(result.section_analysis)} sections</div>
      <div class="muted">{_esc(proj.intent.get("singular_emotional_truth", ""))}</div>
      <div class="big">{_esc(overall) if overall is not None else "—"}<span class="muted" style="font-size:16px">/100 ready</span></div>
      <nav>{nav}</nav>
    </header>"""

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logic Mix OS — {_esc(proj.song_title)}</title><style>{_CSS}</style></head>
<body>{header}<main>{''.join(cards)}</main></body></html>"""
