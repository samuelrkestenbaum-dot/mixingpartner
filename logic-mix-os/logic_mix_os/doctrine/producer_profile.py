"""ProducerProfile — the swappable producer-specific judgment (P-025 foundation).

The producer-agnostic *physics* (analyzers, safety kill-switches, the
bounded-nudge mechanism, determinism/evidence contract, the move-kind vocabulary)
stays fixed in the pipeline. The producer-specific *judgment* — today 100%
hardcoded across ``creative.py`` / ``governance.py`` / ``doctrine_engine.py`` /
``pipeline.py`` — becomes a swappable ``ProducerProfile`` loaded from JSON.

**P-025 is data + loader + tests ONLY.** Nothing in the runtime path imports
``load_profile`` yet — the modules above keep using their hardcoded dicts. The
byte-identical round-trip test (``tests/test_producer_profile.py``) is the guard
that the extracted ``halee_ramone.json`` reconstructs today's judgment exactly;
P-026→P-029 will wire consumers against that guard.

The loader is pure, deterministic, and reads a local JSON file only. The returned
``ProducerProfile`` is a frozen dataclass; its collection fields are freshly
parsed from JSON on every load, so a caller can never mutate the live module
dicts (or a previous load) through it.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from ..constants import (
    CREATIVE_EXTENDED_KINDS,
    CREATIVE_VARIANT_KINDS,
    TRANSLATION_RISK_LEVELS,
)

_DIR = Path(__file__).parent
_PRODUCERS_DIR = _DIR / "producers"

# P-031: the closed per-area honesty vocabulary. Exactly three levels — a
# profile labels each interpretation AREA of its judgment ``high`` (live,
# weighted, curated), ``limited`` (mechanically live but constrained on
# today's data — the constraint stated in the reason), or ``deferred`` (not
# measurable at doctrine time — the boundary stated in the reason).
CONFIDENCE_LEVELS = ("high", "limited", "deferred")

# The producer-specific structures a profile must carry (extraction-completeness
# is asserted against this in the tests). Metadata is validated separately.
_REQUIRED_DATA_FIELDS = (
    "kind_scores",
    "nudge_table",
    "promotion_table",
    "creative_nudge_cap",
    "creative_promotion_cap",
    "risk_penalty",
    "search_modes",
    "philosophy",
    "truth_alignment",
    "taste_kind_bias",
    "taste_max_delta",
    "aesthetic_kill_switches",
    "taste_triangle",
    "veto_thresholds",
    "doctrine",
    "default_creative_mode",
    "protect_iconic_loops",
    "vocal_blend_policy",
    "confidence_map",
)

_REQUIRED_METADATA_FIELDS = (
    "name",
    "display_name",
    "provenance",
    "confidence",
    "risk_class",
)


@dataclass(frozen=True)
class ProducerProfile:
    """An immutable view of one producer's judgment, loaded from JSON.

    Field names mirror the source structures verbatim so the round-trip guard is
    a direct ``==`` against the still-hardcoded module dicts (or, for the values
    computed inline in functions, an indirect drive-the-function comparison).
    """

    # metadata (honesty scaffolding — set up now, enforced in P-031)
    metadata: Dict[str, Any]

    # creative.py
    kind_scores: Dict[str, Dict[str, Any]]
    nudge_table: List[Dict[str, Any]]
    promotion_table: List[Dict[str, Any]]
    creative_nudge_cap: float
    creative_promotion_cap: float
    risk_penalty: Dict[str, int]
    # P-042: a mode entry carries ``allowed_risk`` + ``bias`` (str) and MAY
    # author the OPTIONAL declaration fields ``favor_kinds`` /
    # ``suppress_kinds`` (lists of engine-vocabulary kind names) that fork
    # candidate generation per mode. Absent fields = neutral = the engine's
    # un-forked emission, so pre-P-042 profiles stay valid unchanged.
    # P-043: a mode MAY additionally author ``reach_kinds`` — names from the
    # engine's EXTENDED vocabulary (``CREATIVE_EXTENDED_KINDS``) whose
    # curated variants the mode ADMITS into emission. Reach is the only
    # admission path for extended kinds; ``favor_kinds`` stays order-only.
    search_modes: Dict[str, Dict[str, Any]]
    philosophy: str

    # governance.py
    truth_alignment: Dict[str, Dict[str, int]]
    taste_kind_bias: Dict[str, Dict[str, int]]
    taste_max_delta: int
    aesthetic_kill_switches: List[str]
    # governance.py — secondary constants (P-027 Finding A): the taste-triangle
    # rules (intimate-width penalty + the emotion-blend dims) and the veto
    # thresholds, previously inline literals in taste_triangle/govern_variant.
    taste_triangle: Dict[str, Any]
    veto_thresholds: Dict[str, int]

    # doctrine_engine.py — weights / baselines / the _physical_space +
    # _emotional_hierarchy penalty coeffs
    # (P-025), plus (P-028 Finding A) the widened ``scorers`` group holding the
    # per-function aesthetic constants for the five remaining scorers
    # (vocal_centrality / depth_hierarchy / section_contrast / static_mix /
    # dynamic_mix): baselines, bonuses, penalties, coefficients and thresholds.
    doctrine: Dict[str, Any]

    # pipeline.py (_default_creative_mode truth -> mode map)
    default_creative_mode: Dict[str, Any]

    # creative.py — P-032g: the first profile-DECIDED creative gate. The
    # engine's ``loop_context`` axis DETECTS static-vs-iconic observationally;
    # this flag is the profile DECIDING what to do with an iconic reading:
    # True => the ``loop_deconstruct`` promotion does not fire on an
    # iconic-functioning loop (the profile protects the loop as the record's
    # identity); False (halee_ramone) => current behavior, byte-identical —
    # the reference profile deconstructs. A masked lead vocal always overrides
    # protection (the Ramone gate lives in creative.py).
    protect_iconic_loops: bool

    # doctrine_engine.py — P-032f: the profile-AUTHORED masking philosophy for
    # non-lead vocal roles (the P-032g pattern: a REQUIRED top-level field so
    # every producer's decision is explicit in its JSON, never defaulted).
    # Shape: {"acceptable_blend": bool, "confidence_floor": float in [0, 1]}.
    # ``acceptable_blend: true`` lets masking of a QUALIFIED vocal_percussive /
    # vocal_stack stem (classifier confidence >= confidence_floor, never the
    # lead, never on an event that includes the lead) read as accepted blend
    # in the ``vocal_role_fit`` axis. ``false`` (halee_ramone) => the gated
    # path is unreachable and every vocal keeps full lead-grade clarity
    # protection. Uncertain and hook_candidate vocals and the masked-lead
    # pathway are NEVER blend-eligible whatever this field says (the
    # fail-closed gates live in ``accepted_blend_under_policy``).
    vocal_blend_policy: Dict[str, Any]

    # P-031: the per-interpretation-AREA honesty map — a REQUIRED top-level
    # field (the P-032g/P-032f required-field discipline: every producer's
    # honesty labeling is explicit in its JSON, never defaulted). Shape: an
    # ordered, non-empty list of ``{"area": str, "level": one of
    # CONFIDENCE_LEVELS, "reason": str}`` entries; authoring order is
    # preserved and IS the rendering order. This is LABELING, never judgment:
    # no scorer reads it — the pipeline copies it verbatim onto the report
    # surface so a human or Cowork reads which parts of the judgment to
    # trust, at what strength, and WHY. It complements (never replaces) the
    # profile-level ``metadata`` stamp from P-025: metadata carries the
    # GLOBAL provenance/confidence/risk_class; this map carries per-area
    # trust.
    confidence_map: List[Dict[str, Any]]


def _normalize_kinds_sets(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """JSON has no set type: the nudge/promotion rows store ``kinds`` as a list.
    Rehydrate it to a ``set`` so the round-trip ``==`` against the source rows
    (which use sets) is honest rather than loosened to compare lists."""
    out: List[Dict[str, Any]] = []
    for row in rows:
        row = dict(row)
        if "kinds" in row and not isinstance(row["kinds"], set):
            row["kinds"] = set(row["kinds"])
        out.append(row)
    return out


def _validate(raw: Dict[str, Any], name: str) -> None:
    if "metadata" not in raw:
        raise ValueError(f"profile {name!r}: missing 'metadata'")
    meta = raw["metadata"]
    for f in _REQUIRED_METADATA_FIELDS:
        if f not in meta:
            raise ValueError(f"profile {name!r}: metadata missing {f!r}")
    if not isinstance(meta["risk_class"], int) or isinstance(meta["risk_class"], bool):
        raise ValueError(f"profile {name!r}: metadata.risk_class must be an int")
    for key in ("name", "display_name", "provenance", "confidence"):
        if not isinstance(meta[key], str):
            raise ValueError(f"profile {name!r}: metadata.{key} must be a str")
    for f in _REQUIRED_DATA_FIELDS:
        if f not in raw:
            raise ValueError(f"profile {name!r}: missing data field {f!r}")
    doctrine = raw["doctrine"]
    for key in ("weights", "baselines", "penalty_coeffs", "scorers"):
        if key not in doctrine:
            raise ValueError(f"profile {name!r}: doctrine missing {key!r}")
    for fn in ("vocal_centrality", "depth_hierarchy", "section_contrast",
               "static_mix", "dynamic_mix", "beat_identity", "negative_space",
               "groove_coherence", "rhythmic_surprise", "low_end_motion",
               "loop_context", "vocal_role_fit"):
        if fn not in doctrine["scorers"]:
            raise ValueError(f"profile {name!r}: doctrine.scorers missing {fn!r}")
    # P-037: search_modes must be a non-empty object — a zero-mode profile
    # would leave ``creative._profile_default_mode`` with no authored mode to
    # fall back to (its first-authored-mode branch StopIterations on an empty
    # table). Rejected at load, never at judgment time.
    modes = raw["search_modes"]
    if not isinstance(modes, dict) or not modes:
        raise ValueError(f"profile {name!r}: search_modes must be a non-empty object")
    # P-042: profile-authored mode-forking declarations — OPTIONAL per mode
    # (absent fields = neutral = the engine's un-forked emission, so
    # third-party profiles without them stay valid). When a mode authors
    # them, the declaration must be sound at LOAD time, never at judgment
    # time: kind names come from the ENGINE's move vocabulary (the engine
    # owns the vocabulary; the profile only decides what each mode reaches
    # for), a kind cannot be favored and suppressed at once, and a declaring
    # mode must carry a real ``allowed_risk`` whose posture its own favored
    # kinds respect — favoring a kind whose curated translation risk ranks
    # beyond the mode's ``allowed_risk`` is a LOUD error (governance owns
    # the safety cap; it cannot be out-authored).
    kind_scores = raw["kind_scores"] if isinstance(raw["kind_scores"], dict) else {}
    for mode_name, entry in modes.items():
        if not isinstance(entry, dict):
            raise ValueError(
                f"profile {name!r}: search_modes[{mode_name!r}] must be an object"
            )
        declared = [f for f in ("favor_kinds", "suppress_kinds", "reach_kinds")
                    if f in entry]
        for field_name in declared:
            kinds = entry[field_name]
            if not isinstance(kinds, list) or not all(isinstance(k, str) for k in kinds):
                raise ValueError(
                    f"profile {name!r}: search_modes[{mode_name!r}].{field_name} "
                    f"must be a list of strings"
                )
            # P-043: ``reach_kinds`` admits ONLY the engine's EXTENDED
            # vocabulary — the neutral pool needs no reach (favor/suppress
            # shape it), so naming a neutral kind here is authoring
            # confusion, rejected loudly with its own message.
            if field_name == "reach_kinds":
                outside = [k for k in kinds if k not in CREATIVE_EXTENDED_KINDS]
                if outside:
                    raise ValueError(
                        f"profile {name!r}: search_modes[{mode_name!r}].reach_kinds "
                        f"names non-extended kind(s) {outside} — reach admits ONLY "
                        f"the engine's EXTENDED vocabulary "
                        f"{list(CREATIVE_EXTENDED_KINDS)} (the neutral pool needs "
                        f"no reach; favor/suppress shape it)"
                    )
            else:
                unknown = [k for k in kinds if k not in CREATIVE_VARIANT_KINDS]
                if unknown:
                    raise ValueError(
                        f"profile {name!r}: search_modes[{mode_name!r}].{field_name} "
                        f"names unknown variant kind(s) {unknown} — kinds must come "
                        f"from the engine's move vocabulary {list(CREATIVE_VARIANT_KINDS)}"
                    )
            if len(set(kinds)) != len(kinds):
                raise ValueError(
                    f"profile {name!r}: search_modes[{mode_name!r}].{field_name} "
                    f"has duplicate kind(s)"
                )
        if not declared:
            continue
        favor = entry.get("favor_kinds", [])
        suppress = entry.get("suppress_kinds", [])
        reach = entry.get("reach_kinds", [])
        contradiction = [k for k in favor if k in set(suppress)]
        if contradiction:
            raise ValueError(
                f"profile {name!r}: search_modes[{mode_name!r}] both favors and "
                f"suppresses {contradiction} — a kind cannot be reached for and "
                f"removed at once"
            )
        reach_contradiction = [k for k in reach if k in set(suppress)]
        if reach_contradiction:
            raise ValueError(
                f"profile {name!r}: search_modes[{mode_name!r}] both reaches for "
                f"and suppresses {reach_contradiction} — a kind cannot be "
                f"admitted and removed at once"
            )
        allowed = entry.get("allowed_risk")
        if allowed not in TRANSLATION_RISK_LEVELS:
            raise ValueError(
                f"profile {name!r}: search_modes[{mode_name!r}] authors mode "
                f"declarations but its allowed_risk is not one of "
                f"{list(TRANSLATION_RISK_LEVELS)} (got {allowed!r})"
            )
        cap = TRANSLATION_RISK_LEVELS.index(allowed)
        for k in favor:
            row = kind_scores.get(k, kind_scores.get("depth_cleanup", {}))
            risk = row.get("translation") if isinstance(row, dict) else None
            rank = (
                TRANSLATION_RISK_LEVELS.index(risk)
                if risk in TRANSLATION_RISK_LEVELS
                else len(TRANSLATION_RISK_LEVELS) - 1  # unknown risk reads as highest
            )
            if rank > cap:
                raise ValueError(
                    f"profile {name!r}: search_modes[{mode_name!r}] favors {k!r} "
                    f"(curated translation risk {risk!r}) beyond its allowed_risk "
                    f"{allowed!r} — the cap is governance and cannot be out-authored"
                )
        # P-043: the SAME governance cap binds an authored reach — admitting
        # an extended kind whose curated translation risk ranks beyond the
        # mode's posture is rejected at load exactly like an over-cap favor
        # (and refused fail-closed at emission for loader-bypassing profiles).
        for k in reach:
            row = kind_scores.get(k, kind_scores.get("depth_cleanup", {}))
            risk = row.get("translation") if isinstance(row, dict) else None
            rank = (
                TRANSLATION_RISK_LEVELS.index(risk)
                if risk in TRANSLATION_RISK_LEVELS
                else len(TRANSLATION_RISK_LEVELS) - 1  # unknown risk reads as highest
            )
            if rank > cap:
                raise ValueError(
                    f"profile {name!r}: search_modes[{mode_name!r}] reaches for {k!r} "
                    f"(curated translation risk {risk!r}) beyond its allowed_risk "
                    f"{allowed!r} — the cap is governance and cannot be out-authored"
                )
    # P-037: default_creative_mode structural check — the three keys
    # ``pipeline._default_creative_mode`` hard-dereferences must be present
    # with sane types, so a malformed table is a load-time ValueError rather
    # than a KeyError/TypeError mid-analyze.
    dcm = raw["default_creative_mode"]
    if not isinstance(dcm, dict):
        raise ValueError(f"profile {name!r}: default_creative_mode must be an object")
    for key in ("intimate_truth_words", "intimate_mode", "default_mode"):
        if key not in dcm:
            raise ValueError(f"profile {name!r}: default_creative_mode missing {key!r}")
    words = dcm["intimate_truth_words"]
    if not isinstance(words, list) or not all(isinstance(w, str) for w in words):
        raise ValueError(
            f"profile {name!r}: default_creative_mode.intimate_truth_words "
            f"must be a list of strings"
        )
    for key in ("intimate_mode", "default_mode"):
        if not isinstance(dcm[key], str):
            raise ValueError(f"profile {name!r}: default_creative_mode.{key} must be a str")
    # P-032f: the vocal blend policy must be structurally sound — an explicit
    # bool opt-in plus a real confidence floor in [0, 1]. No silent defaults.
    policy = raw["vocal_blend_policy"]
    if not isinstance(policy, dict):
        raise ValueError(f"profile {name!r}: vocal_blend_policy must be an object")
    for key in ("acceptable_blend", "confidence_floor"):
        if key not in policy:
            raise ValueError(f"profile {name!r}: vocal_blend_policy missing {key!r}")
    if not isinstance(policy["acceptable_blend"], bool):
        raise ValueError(f"profile {name!r}: vocal_blend_policy.acceptable_blend must be a bool")
    floor = policy["confidence_floor"]
    if isinstance(floor, bool) or not isinstance(floor, (int, float)):
        raise ValueError(
            f"profile {name!r}: vocal_blend_policy.confidence_floor must be a number in [0, 1]"
        )
    # P-037: reject NaN/±inf EXPLICITLY (the belt to the range check below —
    # NaN comparison semantics happened to fail the range check too, but only
    # as a side effect; the error should name finiteness).
    if not math.isfinite(floor):
        raise ValueError(
            f"profile {name!r}: vocal_blend_policy.confidence_floor must be finite"
        )
    if not 0.0 <= floor <= 1.0:
        raise ValueError(
            f"profile {name!r}: vocal_blend_policy.confidence_floor must be a number in [0, 1]"
        )
    # P-031: the per-area honesty map must be structurally sound — a NON-EMPTY
    # list of {area, level, reason} entries, level from the closed vocabulary,
    # area/reason non-empty strings. No silent defaults (the P-032f attack-4
    # discipline), and an EMPTY map is rejected too: an honesty layer with
    # zero entries is not honest.
    cmap = raw["confidence_map"]
    if not isinstance(cmap, list):
        raise ValueError(f"profile {name!r}: confidence_map must be a list")
    if not cmap:
        raise ValueError(f"profile {name!r}: confidence_map must not be empty")
    for i, entry in enumerate(cmap):
        if not isinstance(entry, dict):
            raise ValueError(f"profile {name!r}: confidence_map[{i}] must be an object")
        for key in ("area", "level", "reason"):
            if key not in entry:
                raise ValueError(f"profile {name!r}: confidence_map[{i}] missing {key!r}")
        # P-037 (the P-031 reviewer judgment note, now conscious): an entry's
        # key set is EXACTLY {area, level, reason} — an unknown extra key (a
        # typo, a smuggled weight, a stray annotation) is rejected, never
        # silently carried onto the report surface.
        extra = set(entry) - {"area", "level", "reason"}
        if extra:
            raise ValueError(
                f"profile {name!r}: confidence_map[{i}] has unknown key(s) "
                f"{sorted(extra)}"
            )
        for key in ("area", "reason"):
            if not isinstance(entry[key], str) or not entry[key].strip():
                raise ValueError(
                    f"profile {name!r}: confidence_map[{i}].{key} must be a non-empty string"
                )
        if entry["level"] not in CONFIDENCE_LEVELS:
            raise ValueError(
                f"profile {name!r}: confidence_map[{i}].level must be one of "
                f"{CONFIDENCE_LEVELS}, got {entry['level']!r}"
            )
    # P-037 (the same P-031 note): duplicate ``area`` strings are ambiguous
    # honesty — which level does the reader trust? — so uniqueness is
    # structural. Every entry is a validated dict with a string area by here.
    areas = [entry["area"] for entry in cmap]
    duplicates = sorted({a for a in areas if areas.count(a) > 1})
    if duplicates:
        raise ValueError(
            f"profile {name!r}: confidence_map has duplicate area(s) {duplicates}"
        )


def load_profile(name: str = "halee_ramone") -> ProducerProfile:
    """Read ``producers/<name>.json``, validate it, and return a frozen profile.

    Pure and deterministic: a local JSON read plus structural validation, no I/O
    beyond the file, no time/randomness/network. Every collection is freshly
    parsed, so the returned profile never aliases the live module dicts.
    """
    path = _PRODUCERS_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"no producer profile named {name!r} at {path}")
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    _validate(raw, name)
    return ProducerProfile(
        metadata=raw["metadata"],
        kind_scores=raw["kind_scores"],
        nudge_table=_normalize_kinds_sets(raw["nudge_table"]),
        promotion_table=_normalize_kinds_sets(raw["promotion_table"]),
        creative_nudge_cap=raw["creative_nudge_cap"],
        creative_promotion_cap=raw["creative_promotion_cap"],
        risk_penalty=raw["risk_penalty"],
        search_modes=raw["search_modes"],
        philosophy=raw["philosophy"],
        truth_alignment=raw["truth_alignment"],
        taste_kind_bias=raw["taste_kind_bias"],
        taste_max_delta=raw["taste_max_delta"],
        aesthetic_kill_switches=raw["aesthetic_kill_switches"],
        taste_triangle=raw["taste_triangle"],
        veto_thresholds=raw["veto_thresholds"],
        doctrine=raw["doctrine"],
        default_creative_mode=raw["default_creative_mode"],
        protect_iconic_loops=raw["protect_iconic_loops"],
        vocal_blend_policy=raw["vocal_blend_policy"],
        confidence_map=raw["confidence_map"],
    )


__all__ = ["CONFIDENCE_LEVELS", "ProducerProfile", "load_profile"]
