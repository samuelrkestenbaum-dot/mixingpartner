"""Creative governance + taste protection (build packet sections 68-84).

Decides when a creative idea is genuinely good versus merely interesting, louder,
wider, more modern, or closer to a reference. Protects the song from false
progress: reference sanity, negative constraints, the taste triangle, false-
progress / emotional-overfit / anti-template detectors, listener-panel
simulation, the emotional-truth lock, stop conditions, and kill-switches.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .constants import LOOP_SAMPLE_KINDS, RISK_CLASSES

# Section 76: decision review modes.
REVIEW_MODES = [
    "observe_only", "recommend_only", "checklist_only",
    "approve_before_apply", "safe_auto_apply", "manual_only",
]
DEFAULT_REVIEW_MODE = "approve_before_apply"

# Section 78: kill-switch rules (never auto-applied / blocked).
KILL_SWITCHES = [
    "Never overwrite original audio.",
    "Never destructively tune or time-stretch source recordings.",
    "Never delete tracks without backup.",
    "Never flatten comped vocals without a duplicate.",
    "Never apply creative source edits without a versioned duplicate.",
    "Never chase reference loudness at the mix stage.",
    "Never widen the full mix to solve chorus lift.",
    "Never make the lead vocal less intelligible unless explicitly approved.",
    "Never allow a stock loop to dominate the song identity by accident.",
]
_DESTRUCTIVE_PATTERNS = ["overwrite", "delete", "destructive", "flatten", "bounce in place", "render in place"]

_INTIMATE_WORDS = {"intimate", "intimacy", "vulnerable", "vulnerability", "conflicted", "ache",
                   "fragile", "quiet", "restrained", "restraint", "falling apart", "personal",
                   "tender", "grief", "broken", "composed"}
_BIG_WORDS = {"triumphant", "anthemic", "huge", "massive", "stadium", "euphoric", "explosive"}

# Section 38 (taste calibration) feeding governance: the recorded operator taste
# profile (the statements ``memory._TASTE_MAP`` emits) may *bias* a matching-kind
# variant's identity, opt-in and bounded. This is the first read of the learning
# loop. A taste profile can nudge identity but NEVER override doctrine: the
# truth-lock veto, the align<50 veto, and the kill-switch path all fire
# independently of taste (see govern_variant / validate_action_safety).
#
# Hard bound: total identity adjustment is clamped to ±TASTE_MAX_DELTA, strictly
# below the existing intimate-truth -30 nudge, so taste can never out-pull
# doctrine. Re-clamped to [0, 100] afterward.
TASTE_MAX_DELTA = 15

# profile statement (verbatim from memory._TASTE_MAP) -> {variant kind: signed
# identity delta}. Statements not listed here map to no governance kind in this
# pass (creative/EQ surfaces, out of scope). Applied in a fixed order; pure.
_TASTE_KIND_BIAS = {
    "tends to prefer narrower stereo images": {"width_bloom": -TASTE_MAX_DELTA,
                                               "drum_room_bloom": -TASTE_MAX_DELTA},
    "prefers wider images": {"width_bloom": TASTE_MAX_DELTA},
}


def _apply_taste(kind: str, identity: int, statements: Optional[List[str]]):
    """Pure, deterministic taste bias on a variant's identity.

    Returns ``(new_identity, evidence_lines)``. Sums the signed deltas for every
    statement that maps to ``kind`` (fixed iteration order over ``statements``),
    clamps the *total* adjustment to ±TASTE_MAX_DELTA, then re-clamps the result
    to [0, 100]. No time / I/O / randomness. ``evidence_lines`` is empty when no
    statement applies — callers omit the ``taste_adjustments`` key entirely then.
    """
    if not statements:
        return identity, []
    delta = 0
    matched: List[str] = []
    for statement in statements:
        bias = _TASTE_KIND_BIAS.get(statement)
        if not bias or kind not in bias:
            continue
        delta += bias[kind]
        matched.append(statement)
    if not matched:
        return identity, []
    delta = max(-TASTE_MAX_DELTA, min(TASTE_MAX_DELTA, delta))
    new_identity = max(0, min(100, identity + delta))
    if new_identity == identity:
        return identity, []
    direction = "down-weighted" if new_identity < identity else "up-weighted"
    reason = "; ".join(matched)
    line = (f"adjusted for operator taste: {direction} {kind} "
            f"({reason}), identity {identity}->{new_identity}")
    return new_identity, [line]

# emotional-truth alignment (0-100) by variant kind, per truth lean.
_TRUTH_ALIGNMENT = {
    "intimate": {"vocal_ride": 88, "intimacy_pass": 90, "subtractive_drop": 84, "depth_cleanup": 82,
                 "loop_deconstruct": 83, "drum_room_bloom": 58, "width_bloom": 45},
    "big": {"width_bloom": 86, "drum_room_bloom": 86, "vocal_ride": 78, "subtractive_drop": 76,
            "depth_cleanup": 76, "loop_deconstruct": 78, "intimacy_pass": 70},
    "neutral": {"width_bloom": 72, "drum_room_bloom": 78, "vocal_ride": 84, "subtractive_drop": 82,
                "depth_cleanup": 82, "loop_deconstruct": 80, "intimacy_pass": 82},
}


# --------------------------------------------------------------------------- #
def _truth_lean(truth: str) -> str:
    t = (truth or "").lower()
    if any(w in t for w in _INTIMATE_WORDS):
        return "intimate"
    if any(w in t for w in _BIG_WORDS):
        return "big"
    return "neutral"


def emotional_truth_lock(intent: Dict) -> Dict:
    statement = intent.get("singular_emotional_truth", "")
    lean = _truth_lean(statement)
    implications = []
    if lean == "intimate":
        implications = [
            "vocal should remain close and human",
            "arrangement can bloom but should not become triumphant too early",
            "the bridge can narrow rather than explode",
            "the final chorus should release but still carry ache",
        ]
    elif lean == "big":
        implications = ["the chorus should feel large and released", "supporting elements can widen"]
    return {"statement": statement, "lean": lean, "locked": bool(statement), "implications": implications}


def reference_sanity(reference_delta: Optional[Dict], intent: Dict) -> Dict:
    if not reference_delta:
        return {"available": False, "note": "No reference supplied."}
    use_for, avoid = [], []
    if reference_delta.get("stereo_width_delta", 0) < -0.08:
        use_for.append("chorus width / spatial openness")
    if reference_delta.get("brightness_delta", 0) > 0.1:
        avoid.append("brightness / top-end (reference is brighter — don't chase glare)")
    if reference_delta.get("overall_lufs_delta", 0) < -2:
        avoid.append("mastering loudness (don't chase at mix stage)")
    if not use_for:
        use_for.append("overall tonal direction (use selectively)")
    return {
        "available": True,
        "use_for": use_for,
        "do_not_use_for": avoid,
        "rule": "Never chase the whole reference blindly. Extract the relevant trait and reject the irrelevant traits.",
    }


def negative_constraints(intent: Dict) -> List[Dict]:
    out = []
    for c in intent.get("negative_constraints", []):
        severity = "high" if any(k in c.lower() for k in ["vocal", "lyric", "glossy", "dominate"]) else "medium"
        out.append({"constraint": c, "severity": severity})
    return out


def _violates_constraints(variant: Dict, constraints: List[Dict]) -> List[Dict]:
    text = (variant["name"] + " " + " ".join(variant["changes"])).lower()
    violations = []
    for c in constraints:
        cl = c["constraint"].lower()
        if "wall of sound" in cl and variant["kind"] in {"width_bloom"} and "wide" in text:
            violations.append(c)
        if "glossy" in cl and "air" in text:
            violations.append(c)
        if "dominate" in cl and variant["kind"] == "width_bloom" and any(k in text for k in ["loop", "stock"]):
            violations.append(c)
    return violations


def taste_triangle(variant: Dict, truth_lean: str) -> Dict:
    s = variant["scores"]
    emotion = round((s["ramone_score"] + s["listener_excitement_score"] + s["vocal_belief_score"]) / 3)
    craft = s["technical_score"]
    identity = s["taste_alignment_score"]
    if variant["kind"] == "width_bloom" and truth_lean == "intimate":
        identity -= 30
    identity = max(0, identity)
    verdict = "reject" if (identity < 45 or emotion < 45) else "keep"
    return {"emotion": emotion, "craft": craft, "identity": identity, "verdict": verdict}


def false_progress(variant: Dict) -> Optional[Dict]:
    text = " ".join(variant["changes"]).lower()
    if variant["kind"] == "width_bloom" or "widen" in text:
        return {"type": "wider_mistaken_for_better",
                "note": "Width can read as 'bigger' while reducing focus and mono compatibility. Verify vocal focus + a mono check."}
    if "+ db" in text or "louder" in text:
        return {"type": "louder_mistaken_for_better",
                "note": "Level is not lift. Verify perceived openness, not just loudness."}
    return None


def emotional_overfit(variant: Dict, truth_lean: str) -> Optional[Dict]:
    if truth_lean == "intimate" and variant["kind"] in {"width_bloom", "drum_room_bloom"} \
            and variant["scores"]["listener_excitement_score"] >= 83:
        return {"note": "Risk of making a conflicted/intimate song feel triumphant too early. "
                        "Keep some restraint; release without losing the ache."}
    return None


def govern_variant(variant: Dict, constraints: List[Dict], truth_lean: str,
                   taste_profile: Optional[List[str]] = None) -> Dict:
    align = _TRUTH_ALIGNMENT.get(truth_lean, _TRUTH_ALIGNMENT["neutral"]).get(variant["kind"], 75)
    triangle = taste_triangle(variant, truth_lean)
    taste_adjustments: List[str] = []
    if taste_profile:
        new_identity, taste_adjustments = _apply_taste(
            variant["kind"], triangle["identity"], taste_profile)
        if taste_adjustments:
            triangle["identity"] = new_identity
            # Recompute the keep/reject verdict the same way taste_triangle does.
            triangle["verdict"] = (
                "reject" if (triangle["identity"] < 45 or triangle["emotion"] < 45)
                else "keep")
    violations = _violates_constraints(variant, constraints)
    fp = false_progress(variant)
    overfit = emotional_overfit(variant, truth_lean)
    high_violation = any(v["severity"] == "high" for v in violations)
    vetoed = high_violation or align < 50 or triangle["verdict"] == "reject"
    out = {
        "emotional_truth_alignment": align,
        "taste_triangle": triangle,
        "constraint_violations": [v["constraint"] for v in violations],
        "false_progress": fp,
        "emotional_overfit": overfit,
        "vetoed": vetoed,
        "verdict": "reject" if vetoed else "keep",
    }
    if taste_adjustments:
        out["taste_adjustments"] = taste_adjustments
    return out


def govern_branches(branches: List[Dict], intent: Dict, truth_lean: str,
                    taste_profile: Optional[List[str]] = None) -> List[Dict]:
    constraints = negative_constraints(intent)
    out = []
    for branch in branches:
        ranked = sorted(branch["variants"], key=lambda v: v["scores"]["overall_score"], reverse=True)
        chosen, gov = None, None
        for v in ranked:
            g = govern_variant(v, constraints, truth_lean, taste_profile=taste_profile)
            v["governance"] = g
            if chosen is None and not g["vetoed"]:
                chosen, gov = v, g
        if chosen is None and ranked:
            chosen = ranked[0]
            gov = chosen.get("governance")
        out.append({
            "problem_id": branch["problem_id"],
            "problem": branch["problem"],
            "governed_winner": chosen["variant_id"] if chosen else None,
            "governance": gov,
            "reason": (f"'{chosen['name']}' survives governance "
                       f"(truth alignment {gov['emotional_truth_alignment']}, taste {gov['taste_triangle']['verdict']})."
                       if chosen else "All variants vetoed; revisit the problem."),
        })
    return out


def anti_template(branches: List[Dict]) -> Optional[Dict]:
    kinds: Dict[str, int] = {}
    for b in branches:
        win = b.get("winning", {})
        wid = win.get("winning_variant") if win else None
        for v in b["variants"]:
            if v["variant_id"] == wid:
                kinds[v["kind"]] = kinds.get(v["kind"], 0) + 1
    repeated = [k for k, c in kinds.items() if c >= 3]
    if repeated:
        return {"pattern": f"same move kind ({', '.join(repeated)}) winning across problems",
                "risk": "The mix may start to feel formulaic. Repeat doctrine, not presets — vary the move per problem."}
    return None


def listener_panel(result) -> Dict:
    le = result.expanded.get("listener_experience", {})
    masking = result.masking_report.get("summary", {})
    loops = [r["name"] for r in result.records if r["source_kind"] in LOOP_SAMPLE_KINDS]
    truth = result.project.intent.get("singular_emotional_truth", "")
    return {
        "first_time_fan": le.get("summary", "Follows the song but may lose focus where density is high."),
        "producer": (f"The {loops[0]} is exciting but too identifiable as a loop." if loops
                     else "Arrangement reads clearly; watch foreground crowding."),
        "mixer": (f"{masking.get('critical_count', 0)} critical masking conflict(s); low-mid/foreground sharing to resolve."),
        "artist": (f"Make sure the bridge/chorus still serves: '{truth}'." if truth
                   else "Confirm the emotional intent so the mix can protect it."),
        "playlist_listener": "Hook/chorus should land within the first 30s and feel distinct from the verse.",
    }


def stop_conditions(result) -> Dict:
    ds = result.doctrine_score
    reasons = []
    stop = True
    checks = {
        "static mix stable": (ds.get("static_mix_score") or 0) >= 70,
        "dynamic movement working": (ds.get("dynamic_mix_score") or 0) >= 60,
        "vocal belief high": (ds.get("vocal_centrality_score") or 0) >= 75,
        "section contrast sufficient": (ds.get("section_contrast_score") or 100) >= 70,
        "translation safe": (result.mix_plan.get("translation_score") or 0) >= 65,
    }
    for label, ok in checks.items():
        if not ok:
            stop = False
            reasons.append(f"not yet: {label}")
    return {
        "should_stop": stop,
        "reasons": reasons or ["all stop conditions met — validate and move to mastering-readiness checks"],
        "warning": ("Overworking risk: stop creative experimentation once gains are marginal."
                    if stop else None),
    }


def validate_action_safety(action: Dict) -> Dict:
    """Kill-switch check for a single Logic action. Returns blocked + reason."""
    rc = action.get("risk_class", 2)
    setting = (action.get("setting", "") + " " + action.get("plugin", "")).lower()
    if rc >= 5:
        return {"blocked": True, "reason": f"Risk class {rc}: {RISK_CLASSES[5]}"}
    for pat in _DESTRUCTIVE_PATTERNS:
        if pat in setting:
            return {"blocked": True, "reason": f"Matches destructive pattern '{pat}'."}
    return {"blocked": False, "reason": ""}


def mixer_communication(result, tone: str = "collaborative") -> str:
    nxt = result.mix_plan.get("next_pass", [])
    top = nxt[0] if nxt else {"title": "Refinement", "detail": "Validate the current bounce."}
    contrast_weak = any("warning" in s.get("contrast_vs_previous", {}) for s in result.section_analysis)
    if tone == "technical":
        s = next((s for s in result.section_analysis if "warning" in s.get("contrast_vs_previous", {})), None)
        if s:
            c = s["contrast_vs_previous"]
            return (f"Verse-to-chorus RMS delta is only {c.get('rms_delta_db')} dB and width barely changes. "
                    f"Target +3 to +5 dB perceived lift via support-stack automation, not master level.")
        return f"{top['title']}: {top['detail']}"
    if tone == "direct":
        return (f"The chorus needs more section lift — it gets denser, not more open. "
                f"Try widening the supporting elements and BGVs slightly while keeping the lead centered."
                if contrast_weak else f"{top['title']}: {top['detail']}")
    if tone == "do_not":
        return ("Please don't fix this with master level or by widening the lead vocal — "
                "use supporting-element automation and depth.")
    if tone == "producer":
        return (f"Balance is close. The main thing I'm still missing is the chorus opening up emotionally vs the verse — "
                f"maybe a little more bloom around the supporting elements without washing the vocal?")
    # soft / collaborative (default)
    return (f"I think we're getting close. The one thing I'd love to chase next is: {top['detail'].lower()}")


def run_governance(result, creative: Dict, taste_profile: Optional[List[str]] = None) -> Dict:
    intent = result.project.intent
    truth = emotional_truth_lock(intent)
    governed = govern_branches(creative.get("branches", []), intent, truth["lean"],
                               taste_profile=taste_profile)
    return {
        "emotional_truth_lock": truth,
        "reference_sanity": reference_sanity(result.reference_delta, intent),
        "negative_constraints": negative_constraints(intent),
        "governed_branches": governed,
        "anti_template": anti_template(creative.get("branches", [])),
        "listener_panel": listener_panel(result),
        "stop_conditions": stop_conditions(result),
        "kill_switches": KILL_SWITCHES,
        "review_modes": REVIEW_MODES,
        "default_review_mode": DEFAULT_REVIEW_MODE,
        "mixer_feedback": {
            tone: mixer_communication(result, tone)
            for tone in ["collaborative", "producer", "direct", "technical", "do_not"]
        },
    }
