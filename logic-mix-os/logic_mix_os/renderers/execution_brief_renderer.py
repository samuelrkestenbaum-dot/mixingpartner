"""P-062 — the Multi-Lens Execution Brief renderer.

The "from every angle" planning surface as ONE deterministic markdown artifact:
the Manus-pattern multi-angle read encoded as harness-ours / measurements-ground-
truth / LLM-narrates-but-never-scores. The renderer is a PURE function of the
already-parsed artifact payloads — no timestamps, no randomness, no environment
reads, no recomputation: every number is quoted VERBATIM from the JSON (via the
same ``json.dumps`` scalar form the artifacts were written with).

Structure of the brief:

1. **Six lenses** — arrangement/section, masking/spectral, dynamics/energy,
   vocal, space/depth, translation/texture. Each lens reports what the
   measurements say (the key evidence lines from the artifacts) and what the
   doctrine scorer concluded (score + its evidence entry).
2. **Cross-lens contradictions** — a deterministic, data-driven rule table
   (``CONTRADICTION_RULES``): each rule reads two-plus lens facts (collected by
   :func:`collect_facts`) and emits a contradiction line when its predicate
   holds. No LLM. When nothing fires the section says so explicitly.
3. **Execution order** — the mix plan's actions re-cut into five ordered
   phases, cross-referenced to the ``render_logic_checklist`` artifact.

   Phase-classification rules (deterministic; first match wins):

   a. ORIGIN rules — ``per_track_automation`` / ``automation_plan`` /
      ``per_section_action`` items are section-and-automation work
      (phase 4); ``send_reverb`` settings are space/depth (phase 3);
      ``mute_candidates`` are subtraction, i.e. static-balance decisions
      (phase 1).
   b. RISK rule — ``risk_class >= 4`` (source-level creative change or worse,
      per ``constants.RISK_CLASSES``) is a creative variant (phase 5).
   c. KEYWORD rules — the item's combined text (plugin + setting + reason /
      title + detail), lowercased, scanned against the phase keyword tables
      in this order: masking carves (phase 2) → space/depth (phase 3) →
      section/automation (phase 4) → creative (phase 5) → gain/static
      balance (phase 1).
   d. PLUGIN-FIELD fallback — a ``per_track_action`` whose plugin name
      contains "eq" is a carve (phase 2); one containing "compress" is
      static balance (phase 1).
   e. Anything else lands in the explicit **unphased (review manually)**
      bucket — NEVER silently dropped (count conservation is a tested
      invariant).

4. **Host-synthesis prompt block** — a fenced, DRAFT-ONLY final section
   instructing any hosting LLM how to synthesize the narrative multi-angle
   read ON TOP of the brief (the standing P-025/P-031 confidence policy:
   LLM output is draft-only, NEVER high-confidence, and never re-scores).

Missing/partial artifact dirs are tolerated: an absent payload renders an
honest ``(artifact missing: <file>)`` line; the renderer never crashes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from .checklist_renderer import PREFERRED_ORDER

# The artifact files the brief reads, keyed by payload name. All are produced
# by ``pipeline.write_artifacts`` — the brief is strictly downstream (opt-in;
# it never joins the pinned artifact set).
BRIEF_ARTIFACTS = {
    "section_analysis": "section_analysis.json",
    "masking_report": "masking_report.json",
    "doctrine_score": "doctrine_score.json",
    "expanded_analysis": "expanded_analysis.json",
    "depth_map": "depth_map.json",
    "mix_plan": "mix_plan.json",
}

LENS_HEADINGS = [
    "## Lens 1 — Arrangement & Section",
    "## Lens 2 — Masking & Spectral",
    "## Lens 3 — Dynamics & Energy",
    "## Lens 4 — Vocal",
    "## Lens 5 — Space & Depth",
    "## Lens 6 — Translation & Texture",
]


def load_brief_payloads(artifact_dir: str | Path) -> Dict[str, Any]:
    """Load the brief's payloads from an analysis output directory.

    Missing files load as ``None`` (real out-dirs may be partial); the
    renderer degrades honestly instead of crashing.
    """
    root = Path(artifact_dir)
    payloads: Dict[str, Any] = {}
    for key, filename in BRIEF_ARTIFACTS.items():
        path = root / filename
        if path.is_file():
            with open(path, "r", encoding="utf-8") as fh:
                payloads[key] = json.load(fh)
        else:
            payloads[key] = None
    return payloads


# --------------------------------------------------------------------------- #
# Verbatim formatting — the one scalar form, shared by every section.
# --------------------------------------------------------------------------- #
def _fmt(value: Any) -> str:
    """Quote a scalar VERBATIM in its JSON form (81.3 -> "81.3", 82 -> "82",
    0.2191 -> "0.2191", True -> "true"). Strings pass through unchanged."""
    if isinstance(value, str):
        return value
    return json.dumps(value)


def _missing(key: str) -> str:
    return f"_(artifact missing: {BRIEF_ARTIFACTS[key]})_"


def _doctrine_axis(doctrine: Optional[Dict], label: str, score_key: str,
                   evidence_key: str) -> List[str]:
    """One doctrine axis: score /100 plus its verbatim evidence entry."""
    if not doctrine:
        return [f"- **{label}:** {_missing('doctrine_score')}"]
    lines = [f"- **{label}:** {_fmt(doctrine.get(score_key))}/100"]
    for entry in (doctrine.get("evidence") or {}).get(evidence_key, []):
        lines.append(f"  - {entry}")
    return lines


# --------------------------------------------------------------------------- #
# Cross-lens contradictions — the deterministic rule table.
# --------------------------------------------------------------------------- #
_HIGH_CONTRAST = 70
_LOW_SPACE = 50
_HIGH_CENTRALITY = 80
_LOW_LOW_END_MOTION = 50
_LOW_MONO = 70
_HIGH_STATIC = 70
_LOW_DYNAMIC = 40

# Width-recommendation keywords for the mono-vs-widening rule (deliberately
# narrow: only unambiguous widening language; "stereo" alone is excluded
# because "narrow stereo image" is the OPPOSITE move).
_WIDTH_KEYWORDS = ("widen", "wider", "widest", "width", "mid-side", "mid/side")


@dataclass(frozen=True)
class ContradictionRule:
    rule_id: str
    lenses: Tuple[str, str]
    requires: Tuple[str, ...]
    predicate: Callable[[Dict[str, Any]], bool]
    message: Callable[[Dict[str, Any]], str]


CONTRADICTION_RULES: Tuple[ContradictionRule, ...] = (
    ContradictionRule(
        rule_id="contrast_without_space",
        lenses=("dynamics/energy", "space/depth"),
        requires=("section_contrast_score", "physical_space_score"),
        predicate=lambda f: (f["section_contrast_score"] >= _HIGH_CONTRAST
                             and f["physical_space_score"] < _LOW_SPACE),
        message=lambda f: (
            f"Section contrast reads {_fmt(f['section_contrast_score'])}/100 while physical "
            f"space reads {_fmt(f['physical_space_score'])}/100 — the energy moves between "
            f"sections but the space does not open with it; the lift will feel loud, not big."),
    ),
    ContradictionRule(
        rule_id="central_vocal_masked",
        lenses=("vocal", "masking/spectral"),
        requires=("vocal_centrality_score", "vocal_band_masking_count"),
        predicate=lambda f: (f["vocal_centrality_score"] >= _HIGH_CENTRALITY
                             and f["vocal_band_masking_count"] > 0),
        message=lambda f: (
            f"Vocal centrality reads {_fmt(f['vocal_centrality_score'])}/100 yet the masking "
            f"lens counts {_fmt(f['vocal_band_masking_count'])} vocal-band masking event(s) — "
            f"the mix treats the vocal as central while other elements contest its band."),
    ),
    ContradictionRule(
        rule_id="static_low_end_critical_masking",
        lenses=("translation/texture", "masking/spectral"),
        requires=("low_end_motion_score", "critical_low_end_masking_count"),
        predicate=lambda f: (f["low_end_motion_score"] < _LOW_LOW_END_MOTION
                             and f["critical_low_end_masking_count"] > 0),
        message=lambda f: (
            f"Low-end motion reads {_fmt(f['low_end_motion_score'])}/100 while the masking "
            f"lens carries {_fmt(f['critical_low_end_masking_count'])} critical low-end "
            f"event(s) — the low end is both static and contested; carve before you ride."),
    ),
    ContradictionRule(
        rule_id="mono_risk_while_widening",
        lenses=("translation/texture", "space/depth"),
        requires=("mono_compatibility_score", "plan_recommends_width"),
        predicate=lambda f: (f["mono_compatibility_score"] < _LOW_MONO
                             and f["plan_recommends_width"]),
        message=lambda f: (
            f"Mono compatibility reads {_fmt(f['mono_compatibility_score'])}/100 while the "
            f"plan recommends widening moves — widening a mix that already folds down badly "
            f"trades mono translation for spread; fix correlation first."),
    ),
    ContradictionRule(
        rule_id="balanced_but_static",
        lenses=("dynamics/energy", "arrangement/section"),
        requires=("static_mix_score", "dynamic_mix_score"),
        predicate=lambda f: (f["static_mix_score"] >= _HIGH_STATIC
                             and f["dynamic_mix_score"] < _LOW_DYNAMIC),
        message=lambda f: (
            f"Static balance reads {_fmt(f['static_mix_score'])}/100 against dynamic movement "
            f"{_fmt(f['dynamic_mix_score'])}/100 — the mix is more polished than it is alive; "
            f"the next hour belongs to rides and section contrast, not more EQ."),
    ),
)


def _is_low_end(frequency_range: Any) -> bool:
    """True when a masking event's range STARTS below 250 Hz (e.g. "40Hz-150Hz").
    Unparseable ranges (e.g. "full-band (stereo image)") are not low-end."""
    if not isinstance(frequency_range, str) or "-" not in frequency_range:
        return False
    start = frequency_range.split("-", 1)[0].strip().lower()
    try:
        if start.endswith("khz"):
            return float(start[:-3]) * 1000.0 < 250.0
        if start.endswith("hz"):
            return float(start[:-2]) < 250.0
    except ValueError:
        return False
    return False


def _iter_plan_texts(mix_plan: Dict) -> List[str]:
    """Every human-readable recommendation string in the plan (for keyword
    facts like the widening scan). Deterministic order."""
    texts: List[str] = []
    for track in mix_plan.get("per_track_actions") or []:
        for action in track.get("actions") or []:
            texts.append(f"{action.get('setting', '')} {action.get('reason', '')}")
        for auto in track.get("automation") or []:
            texts.append(f"{auto.get('move', '')} {auto.get('reason', '')}")
    for entry in mix_plan.get("automation_plan") or []:
        for move in entry.get("moves") or []:
            if isinstance(move, dict):
                texts.append(str(move.get("move", "")))
            else:
                texts.append(str(move))
    for item in mix_plan.get("next_pass") or []:
        texts.append(f"{item.get('title', '')} {item.get('detail', '')}")
    return texts


def collect_facts(payloads: Dict[str, Any]) -> Dict[str, Any]:
    """The cross-lens fact sheet the contradiction rules read. Missing
    payloads yield ``None`` facts; a rule whose required facts are ``None``
    never fires."""
    doctrine = payloads.get("doctrine_score") or {}
    masking = payloads.get("masking_report") or {}
    expanded = payloads.get("expanded_analysis") or {}
    mix_plan = payloads.get("mix_plan") or {}
    summary = masking.get("summary") or {}
    mono = expanded.get("mono_compatibility") or {}
    events = masking.get("events") or []

    mono_score = mono.get("mono_score")
    if mono_score is None:
        mono_score = mix_plan.get("mono_compatibility_score")

    plan_texts = " ".join(_iter_plan_texts(mix_plan)).lower()
    return {
        "section_contrast_score": doctrine.get("section_contrast_score"),
        "physical_space_score": doctrine.get("physical_space_score"),
        "vocal_centrality_score": doctrine.get("vocal_centrality_score"),
        "vocal_band_masking_count": summary.get("vocal_band_masking_count"),
        "low_end_motion_score": doctrine.get("low_end_motion_score"),
        "critical_low_end_masking_count": sum(
            1 for e in events
            if e.get("severity") == "critical" and _is_low_end(e.get("frequency_range"))
        ),
        "mono_compatibility_score": mono_score,
        "plan_recommends_width": any(k in plan_texts for k in _WIDTH_KEYWORDS),
        "static_mix_score": doctrine.get("static_mix_score"),
        "dynamic_mix_score": doctrine.get("dynamic_mix_score"),
    }


def detect_contradictions(facts: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Run the rule table over a fact sheet -> ``[(rule_id, message), ...]``.
    Deterministic: rules evaluate in table order; a rule with any missing
    required fact stays silent."""
    fired: List[Tuple[str, str]] = []
    for rule in CONTRADICTION_RULES:
        if any(facts.get(key) is None for key in rule.requires):
            continue
        if rule.predicate(facts):
            fired.append((rule.rule_id, rule.message(facts)))
    return fired


# --------------------------------------------------------------------------- #
# Execution order — the five phases (classification rules in the module
# docstring; keep the two in sync).
# --------------------------------------------------------------------------- #
PHASE_GAIN = "Phase 1 — Gain / static balance"
PHASE_CARVE = "Phase 2 — Masking carves"
PHASE_SPACE = "Phase 3 — Space / depth"
PHASE_SECTION = "Phase 4 — Section & automation"
PHASE_CREATIVE = "Phase 5 — Creative variants"
UNPHASED = "Unphased (review manually)"

PHASE_ORDER = [PHASE_GAIN, PHASE_CARVE, PHASE_SPACE, PHASE_SECTION, PHASE_CREATIVE]

_ORIGIN_PHASES = {
    "per_track_automation": PHASE_SECTION,
    "automation_plan": PHASE_SECTION,
    "per_section_action": PHASE_SECTION,
    "send_reverb": PHASE_SPACE,
    "mute_candidate": PHASE_GAIN,
}

_CREATIVE_RISK_FLOOR = 4  # constants.RISK_CLASSES: 4 = source-level creative change

# Keyword tables, scanned in this order (first hit wins).
_PHASE_KEYWORDS: List[Tuple[str, Tuple[str, ...]]] = [
    (PHASE_CARVE, ("high-pass", "hi-pass", "low-pass", "cut ", "notch", "carve",
                   "mask", "mud", "subtractive", "make room", "leave room",
                   "de-ess")),
    (PHASE_SPACE, ("reverb", "delay", "depth", "midground", "background",
                   "foreground", "widen", "wider", "widest", "width",
                   "chamber", "plate", "slapback")),
    (PHASE_SECTION, ("automation", "ride", "section", "chorus", "verse",
                     "bloom", "intimacy", "contrast", "lift", "arrangement")),
    (PHASE_CREATIVE, ("saturat", "excite", "creative", "variant", "experiment",
                      "parallel")),
    (PHASE_GAIN, ("gain", "fader", "level", "balance", "compress", "opto",
                  "panning", "pan ", "mute", "volume", "trim")),
]


def extract_plan_items(mix_plan: Optional[Dict]) -> List[Dict[str, Any]]:
    """Flatten the plan into classifiable items, each carrying its origin,
    a human summary, and (when present) risk class. Deterministic order:
    exactly the artifact's own list order."""
    items: List[Dict[str, Any]] = []
    if not mix_plan:
        return items

    for track in mix_plan.get("per_track_actions") or []:
        name = track.get("track", "?")
        for action in track.get("actions") or []:
            items.append({
                "origin": "per_track_action", "track": name,
                "plugin": action.get("plugin", ""),
                "risk_class": action.get("risk_class"),
                "summary": f"{action.get('plugin', '')} — {action.get('setting', '')}",
                "text": f"{action.get('plugin', '')} {action.get('setting', '')} "
                        f"{action.get('reason', '')}",
            })
        for auto in track.get("automation") or []:
            items.append({
                "origin": "per_track_automation", "track": name,
                "risk_class": auto.get("risk_class"),
                "summary": f"{auto.get('parameter', '')}: {auto.get('move', '')}",
                "text": f"{auto.get('parameter', '')} {auto.get('move', '')} "
                        f"{auto.get('reason', '')}",
            })
        send = track.get("send_reverb")
        if send:
            items.append({
                "origin": "send_reverb", "track": name,
                "risk_class": None,
                "summary": f"send/reverb: {send}",
                "text": str(send),
            })

    for section in mix_plan.get("per_section_actions") or []:
        summary = (f"{section.get('name', section.get('section', '?'))} "
                   f"({section.get('emotional_goal', '')}): "
                   f"rms_dbfs {_fmt(section.get('rms_dbfs'))}, "
                   f"width {_fmt(section.get('width'))}")
        warning = section.get("contrast_warning")
        if warning:
            summary += f" — ⚠ {warning}"
        items.append({
            "origin": "per_section_action", "section": section.get("section"),
            "risk_class": None, "summary": summary, "text": summary,
        })

    for entry in mix_plan.get("automation_plan") or []:
        moves = []
        for move in entry.get("moves") or []:
            if isinstance(move, dict):
                moves.append(f"{move.get('track', '')} {move.get('parameter', '')}: "
                             f"{move.get('move', '')}".strip())
            else:
                moves.append(str(move))
        items.append({
            "origin": "automation_plan", "section": entry.get("section"),
            "risk_class": None,
            "summary": f"{entry.get('name', entry.get('section', '?'))} — "
                       f"{entry.get('gesture', '')}: " + "; ".join(moves),
            "text": " ".join(moves),
        })

    for mute in mix_plan.get("mute_candidates") or []:
        loc = f" (section {mute.get('section')})" if mute.get("section") else ""
        items.append({
            "origin": "mute_candidate",
            "risk_class": mute.get("risk_class"),
            "summary": f"mute/chop candidate: {mute.get('element', '?')}{loc} — "
                       f"{mute.get('reason', '')}",
            "text": f"{mute.get('element', '')} {mute.get('reason', '')}",
        })

    for item in mix_plan.get("next_pass") or []:
        items.append({
            "origin": "next_pass",
            "risk_class": None,
            "summary": f"[next-pass priority {_fmt(item.get('priority'))}] "
                       f"{item.get('title', '')} — {item.get('detail', '')}",
            "text": f"{item.get('title', '')} {item.get('detail', '')}",
        })

    return items


def classify_plan_item(item: Dict[str, Any]) -> str:
    """Deterministic phase classification — the rule ladder from the module
    docstring: origin -> risk -> keywords -> plugin-field -> unphased."""
    origin = item.get("origin")
    if origin in _ORIGIN_PHASES:
        return _ORIGIN_PHASES[origin]

    risk = item.get("risk_class")
    if isinstance(risk, int) and risk >= _CREATIVE_RISK_FLOOR:
        return PHASE_CREATIVE

    text = str(item.get("text", "")).lower()
    for phase, keywords in _PHASE_KEYWORDS:
        if any(k in text for k in keywords):
            return phase

    if origin == "per_track_action":
        plugin = str(item.get("plugin", "")).lower()
        if "eq" in plugin:
            return PHASE_CARVE
        if "compress" in plugin:
            return PHASE_GAIN

    return UNPHASED


def phase_plan(mix_plan: Optional[Dict]) -> Dict[str, List[Dict[str, Any]]]:
    """The plan re-cut into ordered phases. Every extracted item lands in
    exactly one bucket (phases + unphased) — count conservation is a tested
    invariant; nothing is silently dropped."""
    buckets: Dict[str, List[Dict[str, Any]]] = {phase: [] for phase in PHASE_ORDER}
    buckets[UNPHASED] = []
    for item in extract_plan_items(mix_plan):
        buckets[classify_plan_item(item)].append(item)
    return buckets


# --------------------------------------------------------------------------- #
# Lens renderers.
# --------------------------------------------------------------------------- #
def _lens_arrangement(payloads) -> List[str]:
    out = [LENS_HEADINGS[0], ""]
    sections = payloads.get("section_analysis")
    expanded = payloads.get("expanded_analysis") or {}
    doctrine = payloads.get("doctrine_score")

    out.append("**What the measurements say:**")
    if sections is None:
        out.append(_missing("section_analysis"))
    else:
        for s in sections:
            m = s.get("metrics") or {}
            out.append(
                f"- **{s.get('name', s.get('section_id', '?'))}** "
                f"(`{s.get('section_id')}`, {_fmt(s.get('start_time'))}–"
                f"{_fmt(s.get('end_time'))}s, goal: {s.get('emotional_goal')}): "
                f"rms_dbfs {_fmt(m.get('rms_dbfs'))}, lufs {_fmt(m.get('lufs'))}, "
                f"width {_fmt(m.get('width'))}, brightness {_fmt(m.get('brightness'))}, "
                f"density {_fmt(m.get('density'))}, "
                f"transient_density {_fmt(m.get('transient_density'))}, "
                f"vocal_presence_db {_fmt(m.get('vocal_presence_db'))}"
            )
            if s.get("energy_tag"):
                out.append(f"  - energy tag: {s['energy_tag']}")
            contrast = s.get("contrast_vs_previous") or {}
            if "rms_delta_db" in contrast:
                out.append(
                    f"  - vs previous: rms_delta_db {_fmt(contrast.get('rms_delta_db'))}, "
                    f"width_delta {_fmt(contrast.get('width_delta'))}, "
                    f"brightness_delta {_fmt(contrast.get('brightness_delta'))}, "
                    f"density_delta {_fmt(contrast.get('density_delta'))}"
                )
            if contrast.get("warning"):
                out.append(f"  - ⚠ {contrast['warning']}")
            elif contrast.get("note"):
                out.append(f"  - {contrast['note']}")

    density = expanded.get("arrangement_density") if expanded else None
    if payloads.get("expanded_analysis") is None:
        out.append(_missing("expanded_analysis"))
    elif density:
        for row in density.get("per_section") or []:
            counts = row.get("layer_counts") or {}
            out.append(
                f"- Density `{row.get('section_id')}`: forward_count "
                f"{_fmt(row.get('forward_count'))}, density_metric "
                f"{_fmt(row.get('density_metric'))} (layers: "
                + ", ".join(f"{k} {_fmt(v)}" for k, v in counts.items()) + ")"
            )
        summary = density.get("summary") or {}
        out.append(
            f"- Density summary: {_fmt(summary.get('total_sections'))} section(s), "
            f"{_fmt(summary.get('crowded'))} crowded."
        )

    out.append("")
    out.append("**What the doctrine scorer concluded:**")
    out.extend(_doctrine_axis(doctrine, "Negative space", "negative_space_score",
                              "negative_space"))
    out.extend(_doctrine_axis(doctrine, "Loop context", "loop_context_score",
                              "loop_context"))
    out.append("")
    return out


def _lens_masking(payloads) -> List[str]:
    out = [LENS_HEADINGS[1], ""]
    masking = payloads.get("masking_report")
    doctrine = payloads.get("doctrine_score")

    out.append("**What the measurements say:**")
    if masking is None:
        out.append(_missing("masking_report"))
    else:
        if masking.get("doctrine_rule"):
            out.append(f"- Doctrine rule: {masking['doctrine_rule']}")
        summary = masking.get("summary") or {}
        out.append(
            f"- Summary: critical {_fmt(summary.get('critical_count'))} · "
            f"moderate {_fmt(summary.get('moderate_count'))} · "
            f"blend {_fmt(summary.get('blend_count'))} · "
            f"total {_fmt(summary.get('total_events'))} · "
            f"vocal-band {_fmt(summary.get('vocal_band_masking_count'))}"
        )
        for event in masking.get("events") or []:
            elements = " × ".join(event.get("elements") or [])
            out.append(
                f"- [{event.get('severity')}] {elements} @ "
                f"{event.get('frequency_range')} (`{event.get('section')}`), "
                f"overlap {_fmt(event.get('overlap'))}: {event.get('reason')}"
            )
            if event.get("recommendation"):
                out.append(f"  - recommendation: {event['recommendation']}")
        risk = masking.get("per_track_masking_risk") or {}
        if risk:
            out.append("- Per-track masking risk: "
                       + ", ".join(f"{k} {_fmt(v)}" for k, v in risk.items()))

    out.append("")
    out.append("**What the doctrine scorer concluded:**")
    out.extend(_doctrine_axis(doctrine, "Emotional hierarchy",
                              "emotional_hierarchy_score", "emotional_hierarchy"))
    out.append("")
    return out


def _lens_dynamics(payloads) -> List[str]:
    out = [LENS_HEADINGS[2], ""]
    expanded = payloads.get("expanded_analysis")
    doctrine = payloads.get("doctrine_score")

    out.append("**What the measurements say:**")
    if expanded is None:
        out.append(_missing("expanded_analysis"))
    else:
        listener = expanded.get("listener_experience") or {}
        for stop in listener.get("journey") or []:
            out.append(
                f"- {stop.get('name', stop.get('section_id', '?'))} "
                f"({stop.get('emotional_goal')}): \"{stop.get('what_a_fan_hears')}\" "
                f"— engagement: {stop.get('engagement')}"
            )
        for point in listener.get("fatigue_points") or []:
            out.append(f"- Fatigue point: {point}")
        if "chorus_feels_earned" in listener:
            out.append(f"- chorus_feels_earned: {_fmt(listener['chorus_feels_earned'])}")
        if listener.get("summary"):
            out.append(f"- {listener['summary']}")

    out.append("")
    out.append("**What the doctrine scorer concluded:**")
    out.extend(_doctrine_axis(doctrine, "Dynamic mix", "dynamic_mix_score",
                              "dynamic_mix"))
    out.extend(_doctrine_axis(doctrine, "Section contrast", "section_contrast_score",
                              "section_contrast"))
    out.extend(_doctrine_axis(doctrine, "Static mix", "static_mix_score",
                              "static_mix"))
    out.append("")
    return out


def _lens_vocal(payloads) -> List[str]:
    out = [LENS_HEADINGS[3], ""]
    expanded = payloads.get("expanded_analysis")
    masking = payloads.get("masking_report")
    doctrine = payloads.get("doctrine_score")

    out.append("**What the measurements say:**")
    if masking is None:
        out.append(_missing("masking_report"))
    else:
        summary = masking.get("summary") or {}
        out.append(f"- Vocal-band masking events: "
                   f"{_fmt(summary.get('vocal_band_masking_count'))}")
    if expanded is None:
        out.append(_missing("expanded_analysis"))
    else:
        vp = expanded.get("vocal_performance") or {}
        if vp.get("available"):
            out.append(
                f"- Performance: dynamic range {_fmt(vp.get('dynamic_range_db'))} dB, "
                f"phrase energy variation {_fmt(vp.get('phrase_energy_variation_db'))} dB, "
                f"push moment {_fmt(vp.get('push_moment_sec'))}s, "
                f"pull-back moment {_fmt(vp.get('pull_back_moment_sec'))}s, "
                f"sibilance {_fmt(vp.get('sibilance_indicator'))}"
            )
            for rec in vp.get("recommendations") or []:
                out.append(f"  - {rec}")
            if vp.get("summary"):
                out.append(f"- {vp['summary']}")
        elif vp:
            out.append(f"- Vocal performance: {vp.get('summary', 'not available')}")

    out.append("")
    out.append("**What the doctrine scorer concluded:**")
    out.extend(_doctrine_axis(doctrine, "Vocal centrality", "vocal_centrality_score",
                              "vocal_centrality"))
    out.extend(_doctrine_axis(doctrine, "Vocal role fit", "vocal_role_fit_score",
                              "vocal_role_fit"))
    out.append("")
    return out


def _lens_space(payloads) -> List[str]:
    out = [LENS_HEADINGS[4], ""]
    depth_map = payloads.get("depth_map")
    doctrine = payloads.get("doctrine_score")

    out.append("**What the measurements say:**")
    if depth_map is None:
        out.append(_missing("depth_map"))
    else:
        for row in depth_map:
            by_section = row.get("depth_by_section") or {}
            placement = ", ".join(f"{k}→{v}" for k, v in by_section.items())
            out.append(
                f"- {row.get('name', row.get('track_id', '?'))} "
                f"({row.get('instrument_identity')}): default "
                f"{row.get('default_depth')}; {placement} — {row.get('reason')}"
            )

    out.append("")
    out.append("**What the doctrine scorer concluded:**")
    out.extend(_doctrine_axis(doctrine, "Physical space", "physical_space_score",
                              "physical_space"))
    out.extend(_doctrine_axis(doctrine, "Depth hierarchy", "depth_hierarchy_score",
                              "depth_hierarchy"))
    out.append("")
    return out


def _lens_translation(payloads) -> List[str]:
    out = [LENS_HEADINGS[5], ""]
    expanded = payloads.get("expanded_analysis")
    doctrine = payloads.get("doctrine_score")
    mix_plan = payloads.get("mix_plan") or {}

    out.append("**What the measurements say:**")
    if expanded is None:
        out.append(_missing("expanded_analysis"))
    else:
        translation = expanded.get("translation") or {}
        out.append(f"- Translation score: {_fmt(translation.get('translation_score'))}/100"
                   f" (mirrored on mix_plan.json: "
                   f"{_fmt(mix_plan.get('translation_score'))})")
        checks = translation.get("checks") or {}
        out.append("- Checks: "
                   + ", ".join(f"{k} {_fmt(v)}" for k, v in checks.items()))
        for profile in translation.get("profiles") or []:
            risks = profile.get("risks") or []
            if risks:
                out.append(f"- [{profile.get('severity')}] {profile.get('profile')}: "
                           + " ".join(risks))
        for warning in translation.get("warnings") or []:
            out.append(f"- ⚠ {warning}")

        mono = expanded.get("mono_compatibility") or {}
        out.append(
            f"- Mono score: {_fmt(mono.get('mono_score'))}/100 "
            f"(mirrored on mix_plan.json: {_fmt(mix_plan.get('mono_compatibility_score'))}); "
            f"phase correlation {_fmt(mono.get('mix_phase_correlation'))}, "
            f"mono collapse loss {_fmt(mono.get('mix_mono_collapse_loss_db'))} dB"
        )
        for event in mono.get("events") or []:
            out.append(f"- [{event.get('severity')}] {event.get('track')}: "
                       f"{event.get('issue')} ({event.get('recommendation')})")
        mono_summary = mono.get("summary") or {}
        if mono_summary:
            out.append(f"- Mono summary: tracks_at_risk "
                       f"{_fmt(mono_summary.get('tracks_at_risk'))}, high_severity "
                       f"{_fmt(mono_summary.get('high_severity'))}")

    out.append("")
    out.append("**What the doctrine scorer concluded:**")
    out.extend(_doctrine_axis(doctrine, "Textural coherence",
                              "textural_coherence_score", "textural_coherence"))
    out.extend(_doctrine_axis(doctrine, "Low-end motion", "low_end_motion_score",
                              "low_end_motion"))
    out.append("")
    return out


# --------------------------------------------------------------------------- #
# Header / contradictions / execution order / copilot block.
# --------------------------------------------------------------------------- #
def _header(payloads) -> List[str]:
    doctrine = payloads.get("doctrine_score")
    mix_plan = payloads.get("mix_plan")
    out = ["# Multi-Lens Execution Brief", ""]
    out.append("> Deterministic artifact: every number below is quoted verbatim "
               "from the analysis artifacts. Nothing here is recomputed, and "
               "nothing here is LLM output.")
    out.append("")

    if mix_plan is None:
        out.append(_missing("mix_plan"))
    else:
        if mix_plan.get("song_title"):
            out.append(f"**Song:** {mix_plan['song_title']}")
        if mix_plan.get("singular_emotional_truth"):
            out.append(f"**Emotional truth:** {mix_plan['singular_emotional_truth']}")
        if mix_plan.get("overall_diagnosis"):
            out.append(f"**Overall diagnosis:** {mix_plan['overall_diagnosis']}")

    if doctrine is None:
        out.append(_missing("doctrine_score"))
    else:
        producer = doctrine.get("producer") or {}
        out.append(
            f"**Producer lens:** {producer.get('display_name', '?')} "
            f"(`{producer.get('name', '?')}`) — provenance "
            f"{producer.get('provenance', '?')}, confidence "
            f"{producer.get('confidence', '?')}."
        )
        confidence = doctrine.get("confidence") or []
        if confidence:
            out.append("")
            out.append("**Confidence ledger (from the profile, verbatim):**")
            for entry in confidence:
                out.append(f"- {entry.get('area')}: **{entry.get('level')}** — "
                           f"{entry.get('reason')}")
    out.append("")
    return out


def _contradictions_section(payloads) -> List[str]:
    out = ["## Cross-Lens Contradictions", ""]
    out.append("_Deterministic rule table — each line is two lenses disagreeing, "
               "detected from the measurements alone (no LLM)._")
    out.append("")
    fired = detect_contradictions(collect_facts(payloads))
    if not fired:
        out.append("(no cross-lens contradictions detected)")
    else:
        for rule_id, message in fired:
            rule = next(r for r in CONTRADICTION_RULES if r.rule_id == rule_id)
            out.append(f"- **{rule_id}** ({rule.lenses[0]} × {rule.lenses[1]}): "
                       f"{message}")
    out.append("")
    return out


def _execution_section(payloads) -> List[str]:
    out = ["## Execution Order", ""]
    mix_plan = payloads.get("mix_plan")
    out.append(
        "_The mix plan re-cut into execution phases. Cross-reference: "
        "`logic_action_checklist.md` (the `render-checklist` output) carries "
        "the same per-track actions grouped by track in the preferred order "
        + " → ".join(PREFERRED_ORDER) + "; here they are ordered by phase "
        "across tracks. Non-destructive only — duplicate tracks / save "
        "presets before changes._"
    )
    out.append("")
    if mix_plan is None:
        out.append(_missing("mix_plan"))
        out.append("")
        return out

    buckets = phase_plan(mix_plan)
    for phase in PHASE_ORDER + [UNPHASED]:
        out.append(f"### {phase}")
        out.append("")
        items = buckets[phase]
        if not items:
            out.append("- (no actions in this phase)")
        for item in items:
            tag = item.get("track") or item.get("section") or item.get("origin")
            line = f"- **{tag}** — {item['summary']}"
            if isinstance(item.get("risk_class"), int):
                line += f" _(risk class {_fmt(item['risk_class'])})_"
            if item.get("origin") in ("per_track_action", "per_track_automation",
                                      "send_reverb"):
                line += f" _(checklist → '{item.get('track')}')_"
            out.append(line)
        out.append("")
    return out


def _copilot_block(payloads) -> List[str]:
    doctrine = payloads.get("doctrine_score") or {}
    producer = doctrine.get("producer") or {}
    voice = producer.get("display_name") or "the producer named in the header"
    return [
        "## For an AI mixing copilot (draft-only)",
        "",
        "> **DRAFT-ONLY.** Everything ABOVE this block is deterministic ground "
        "truth: measured by the engine and quoted verbatim. This block is an "
        "instruction to a hosting LLM (Claude Cowork, or wherever this brief is "
        "pasted). Anything such a host writes is a draft, never a measurement, "
        "and is NEVER high-confidence — the standing LLM confidence policy.",
        "",
        "```text",
        "You are a mixing copilot reading this execution brief. Synthesize the",
        "multi-angle narrative ON TOP of the brief, under these rules:",
        "",
        f"1. Adopt the producer's voice: {voice}. Speak the way the confidence",
        "   ledger and evidence lines above speak — specific, grounded, no hype.",
        "2. Cross-reference the six lenses: where two lenses point at the same",
        "   underlying cause, say so and name both. Start from the Cross-Lens",
        "   Contradictions section; extend it with narrative, not new findings.",
        "3. Propose the session narrative: walk the five execution phases in",
        "   order and describe the session as a story — what the first hour is",
        "   for, what proves the phase worked, when to stop.",
        "4. NEVER contradict or re-score the measurements. Every number above",
        "   is ground truth; you may interpret it, you may not adjust it,",
        "   average it, or invent a replacement score.",
        "5. Mark ALL of your output as draft-only. It is a reading of the",
        "   evidence, not evidence.",
        "```",
        "",
    ]


# --------------------------------------------------------------------------- #
# The renderer.
# --------------------------------------------------------------------------- #
def render_execution_brief(payloads: Dict[str, Any]) -> str:
    """Render the multi-lens execution brief from already-parsed payload dicts.

    ``payloads`` carries the keys in :data:`BRIEF_ARTIFACTS` (missing keys and
    ``None`` values are tolerated — each renders an honest missing line).
    Pure function of its inputs: same dicts in -> byte-identical string out.
    """
    out: List[str] = []
    out.extend(_header(payloads))
    out.extend(_lens_arrangement(payloads))
    out.extend(_lens_masking(payloads))
    out.extend(_lens_dynamics(payloads))
    out.extend(_lens_vocal(payloads))
    out.extend(_lens_space(payloads))
    out.extend(_lens_translation(payloads))
    out.extend(_contradictions_section(payloads))
    out.extend(_execution_section(payloads))
    out.extend(_copilot_block(payloads))
    return "\n".join(out).rstrip()
