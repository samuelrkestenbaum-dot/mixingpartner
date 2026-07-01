"""P-016 — the FIRST reward/promotion nudge, through the REAL evidence path.

P-012/P-015 shipped a bounded, PENALTY-ONLY evidence-nudge layer (a nudge could
only LOWER a variant's score). P-016 crosses that line deliberately, on the
user's delegation: it adds a bounded, evidence-gated PROMOTION nudge that can
RAISE a variant's score — the first reward nudge — layered on top of the
untouched ``_KIND_SCORES`` base, exactly the way the penalties were.

The doctrine anchor is the system's OWN principle: ``governance.anti_template``
warns when the same move-kind wins >=3 problems ("vary the move per problem"),
and ``subtractive_drop`` currently wins ``chorus_lift`` + ``density`` + ``loop`` =
3 branches. When a loop is GENUINELY foregrounded (the source auditors flag a
"foregrounded loop" red_flag, corroborated by ``provenance`` high_risk), the
loop-specific move ``loop_deconstruct`` is promoted so it wins the ``loop``
problem — dropping ``subtractive_drop`` to 2 branches and honoring
``loops_not_foregrounded`` / "never let a stock loop dominate the song identity."

The variant-scoring path is golden-unguarded (``regression.py`` reads
``doctrine_score``, never ``score_variant``), so THESE unit tests are the binding
guard for the aesthetic change.

The proof is driven through the REAL ``analyze()`` result and the REAL source
auditors / provenance analyzer. The only thing synthesized is genuinely
FOREGROUNDING the loop — we set the loop record's ``depth_default`` (and its
depth_map entry) to ``"foreground"`` on a deep COPY, then re-run the REAL
``audit_all`` / ``analyze_provenance`` so THEY emit the real "foregrounded loop"
red_flag and ``high_risk`` provenance. We do NOT hand-inject the flag string and
we do NOT monkeypatch the nudge — the evidence is produced by the real
analyzers off a genuinely-foregrounded loop.

Fake adapters only: the fixture is the project's own seeded synthetic stems +
manifest run through ``analyze()``. No DAW / Logic / AppleScript / subprocess /
network.
"""

from __future__ import annotations

import copy
import pathlib

import pytest

import logic_mix_os.pipeline as pipeline
from logic_mix_os.analyzers.provenance import analyze_provenance
from logic_mix_os.analyzers.source_auditors import audit_all
from logic_mix_os.constants import LOOP_SAMPLE_KINDS
from logic_mix_os.creative import (
    CREATIVE_NUDGE_CAP,
    CREATIVE_PROMOTION_CAP,
    _KIND_SCORES,
    _RISK_PENALTY,
    _foregrounded_loop,
    run_creative_engine,
)
from logic_mix_os.project import load_manifest

_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Verbatim promotion evidence string (the P-016 contract surface).
PROMOTION_REASON = (
    "loop_promotion +4.0: a foregrounded/dominating loop — deconstruct it "
    "(source material respected), don't just accent it"
)

_NUMERIC = ["technical", "halee", "ramone", "contrast", "vocal_belief", "excitement", "taste"]


def _curated_base_overall(kind: str) -> float:
    """Overall score governance ranks on, BEFORE any nudge — the exact formula
    ``score_variant`` uses for ``base_overall`` (creative.py)."""
    b = _KIND_SCORES[kind]
    return round(sum(b[k] for k in _NUMERIC) / len(_NUMERIC) - _RISK_PENALTY[b["translation"]], 1)


def _with_foregrounded_loop(result):
    """Deep copy of a real analyze() result in which the loop is GENUINELY
    foregrounded, with the REAL auditors/provenance re-run so THEY emit the
    real evidence.

    Copy, never mutate: the ``analyzed`` fixture is session-scoped and shared
    with the collateral tests. This is the exact wire the promotion predicate
    reads (``source_audits`` red_flags + ``provenance`` high_risk), produced by
    the real analyzers off a genuinely-foregrounded loop — not a hand-set flag.
    """
    r = copy.deepcopy(result)
    loop_ids = {rec["track_id"] for rec in r.records if rec["source_kind"] in LOOP_SAMPLE_KINDS}
    assert loop_ids, "fixture must contain at least one imported loop"
    for rec in r.records:
        if rec["track_id"] in loop_ids:
            rec["depth_default"] = "foreground"
    for d in r.depth_map:
        if d["track_id"] in loop_ids:
            d["default_depth"] = "foreground"
    # Re-run the REAL analyzers off the genuinely-foregrounded loop.
    r.source_audits = audit_all(r.records)
    r.provenance = analyze_provenance(r.project, r.source_material, r.depth_map)
    return r


def _loop_branch(creative_out):
    return next(b for b in creative_out["branches"] if b["problem_id"] == "loop")


def _variant_by_id(branch, vid):
    return next(v for v in branch["variants"] if v["variant_id"] == vid)


# --------------------------------------------------------------------------- #
# Sanity: a clean analyze() of this fixture does NOT foreground the loop, so the
# only foregrounded-loop signal in these tests is the one we genuinely produce.
# --------------------------------------------------------------------------- #
def test_fixture_loop_is_not_foregrounded_unmodified(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    assert _foregrounded_loop(res) is False


def test_foregrounding_produces_real_evidence(analyzed):
    """The evidence is REAL: genuinely foregrounding the loop makes the REAL
    source auditor emit a ``"foregrounded loop"`` red_flag AND the REAL
    provenance analyzer report ``high_risk`` — nothing hand-set."""
    res = _with_foregrounded_loop(analyzed["dense_chorus_with_loops"])
    red_flags = {f for a in res.source_audits["audits"] for f in a["red_flags"]}
    assert "foregrounded loop" in red_flags
    assert res.provenance["summary"]["high_risk"] >= 1
    assert _foregrounded_loop(res) is True


# --------------------------------------------------------------------------- #
# THE FLIP — evidence ON: a genuinely foregrounded loop promotes loop_deconstruct
# (loop_A) so it wins the loop branch, carrying the promotion evidence line.
# --------------------------------------------------------------------------- #
def test_foregrounded_loop_flips_loop_winner_to_loop_deconstruct(analyzed):
    res = _with_foregrounded_loop(analyzed["dense_chorus_with_loops"])
    assert _foregrounded_loop(res) is True
    out = run_creative_engine(res, res.creative["search_mode"])
    branch = _loop_branch(out)

    loop_a = _variant_by_id(branch, "loop_A")   # loop_deconstruct
    loop_b = _variant_by_id(branch, "loop_B")   # subtractive_drop
    assert loop_a["kind"] == "loop_deconstruct"
    assert loop_b["kind"] == "subtractive_drop"

    # loop_deconstruct carries the promotion evidence line and lands at base + 4.0.
    assert loop_a["scores"].get("score_nudges") == [PROMOTION_REASON]
    assert loop_a["scores"]["overall_score"] == pytest.approx(85.9, abs=1e-9)
    # subtractive_drop is not promoted: unchanged at its curated base 85.3.
    assert "score_nudges" not in loop_b["scores"]
    assert loop_b["scores"]["overall_score"] == pytest.approx(85.3, abs=1e-9)

    # The decisive flip: loop_deconstruct (loop_A) now wins, by 0.6 (rounded axis).
    assert branch["winning"]["winning_variant"] == "loop_A"
    assert (
        loop_a["scores"]["overall_score"] - loop_b["scores"]["overall_score"]
    ) == pytest.approx(0.6, abs=1e-9)


# --------------------------------------------------------------------------- #
# LOAD-BEARING NEGATIVE CONTROL — evidence OFF: no foregrounded loop -> the loop
# winner stays subtractive_drop (loop_B). Proves the flip is CAUSED by the
# evidence, not a base re-rank.
# --------------------------------------------------------------------------- #
def test_no_foregrounded_loop_keeps_subtractive_drop_winner(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    assert _foregrounded_loop(res) is False  # no foregrounded-loop evidence present
    out = run_creative_engine(res, res.creative["search_mode"])
    branch = _loop_branch(out)

    loop_a = _variant_by_id(branch, "loop_A")   # loop_deconstruct
    loop_b = _variant_by_id(branch, "loop_B")   # subtractive_drop
    # No promotion fires on loop_deconstruct when the loop is not foregrounded.
    assert "score_nudges" not in loop_a["scores"]
    assert "score_nudges" not in loop_b["scores"]
    # Base ranking: subtractive_drop (85.3) outranks loop_deconstruct (81.9).
    assert loop_a["scores"]["overall_score"] == pytest.approx(81.9, abs=1e-9)
    assert loop_b["scores"]["overall_score"] == pytest.approx(85.3, abs=1e-9)
    assert branch["winning"]["winning_variant"] == "loop_B"


# --------------------------------------------------------------------------- #
# CAP BINDS — the promotion clamps at exactly +CREATIVE_PROMOTION_CAP (4.0),
# a SEPARATE constant from the +/-2.0 penalty cap.
# --------------------------------------------------------------------------- #
def test_promotion_cap_binds_at_exactly_four(analyzed):
    assert CREATIVE_PROMOTION_CAP == 4.0
    assert CREATIVE_PROMOTION_CAP != CREATIVE_NUDGE_CAP  # distinct from the penalty cap
    res = _with_foregrounded_loop(analyzed["dense_chorus_with_loops"])
    out = run_creative_engine(res, res.creative["search_mode"])
    branch = _loop_branch(out)
    loop_a = _variant_by_id(branch, "loop_A")   # loop_deconstruct
    base = _curated_base_overall("loop_deconstruct")  # 81.9
    movement = loop_a["scores"]["overall_score"] - base
    # The raw promotion delta exceeds the cap and is clamped to exactly +4.0.
    assert movement == pytest.approx(CREATIVE_PROMOTION_CAP, abs=1e-9)
    assert base == pytest.approx(81.9, abs=1e-9)


# --------------------------------------------------------------------------- #
# PENALTY CAP UNTOUCHED — the promotion cap is separate; the penalty cap is 2.0.
# --------------------------------------------------------------------------- #
def test_penalty_cap_untouched():
    assert CREATIVE_NUDGE_CAP == 2.0


# --------------------------------------------------------------------------- #
# COLLATERAL SAFETY — no OTHER branch's winner changes between evidence OFF and
# ON. Only the loop branch flips; everything else is identical.
# --------------------------------------------------------------------------- #
def test_only_loop_branch_flips_under_foregrounded_loop(analyzed):
    clean = analyzed["dense_chorus_with_loops"]
    foreg = _with_foregrounded_loop(clean)
    out_clean = run_creative_engine(clean, clean.creative["search_mode"])
    out_foreg = run_creative_engine(foreg, foreg.creative["search_mode"])

    win_clean = {b["problem_id"]: b["winning"]["winning_variant"] for b in out_clean["branches"]}
    win_foreg = {b["problem_id"]: b["winning"]["winning_variant"] for b in out_foreg["branches"]}

    # Same set of branches.
    assert set(win_clean) == set(win_foreg)
    # The ONLY winner that changes is loop: loop_B -> loop_A.
    changed = {pid for pid in win_clean if win_clean[pid] != win_foreg[pid]}
    assert changed == {"loop"}
    assert win_clean["loop"] == "loop_B"
    assert win_foreg["loop"] == "loop_A"


# --------------------------------------------------------------------------- #
# COLLATERAL SAFETY — the other subtractive_drop branches (chorus_lift, density)
# still win subtractive_drop even WITH the foregrounded-loop evidence present:
# loop_deconstruct only competes in the loop branch, so nothing else can shift.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("problem_id", ["chorus_lift", "density"])
def test_other_subtractive_drop_branches_do_not_flip(analyzed, problem_id):
    res = _with_foregrounded_loop(analyzed["dense_chorus_with_loops"])
    out = run_creative_engine(res, res.creative["search_mode"])
    branch = next((b for b in out["branches"] if b["problem_id"] == problem_id), None)
    assert branch is not None, problem_id
    winner = _variant_by_id(branch, branch["winning"]["winning_variant"])
    assert winner["kind"] == "subtractive_drop"


# --------------------------------------------------------------------------- #
# PRODUCTION LIVENESS (P-009-style guard) — the promotion must fire through the
# REAL production ``analyze()`` path, reading ``result.creative`` DIRECTLY with
# NO re-run of ``run_creative_engine``. This is the guard that catches the inert-
# in-production failure: ``score_variant``'s ``_foregrounded_loop`` predicate
# reads ``result.provenance`` / ``result.source_audits``, so those must be
# computed BEFORE the creative engine in ``pipeline.analyze()``.
#
# To exercise the production path on a GENUINELY foregrounded loop we patch the
# ONE planner decision that sets a loop's depth (``pipeline.plan_depth``), so the
# loop is really foregrounded — then the ENTIRE real pipeline flows from that
# state: the REAL ``audit_all`` emits the real "foregrounded loop" red_flag, the
# REAL ``analyze_provenance`` reports real ``high_risk``, and the REAL
# ``run_creative_engine`` inside ``analyze()`` fires the promotion. We do NOT
# monkeypatch the nudge, the flag, provenance, or ``run_creative_engine``.
# --------------------------------------------------------------------------- #
def _analyze_with_foregrounded_loops(monkeypatch):
    """Run the REAL production ``analyze()`` with loops genuinely foregrounded at
    the depth-planner seam. Returns the production ``ProjectAnalysis``."""
    real_plan_depth = pipeline.plan_depth

    def _foreground_loop_depth(identity, roles, source_material, sections):
        d = real_plan_depth(identity, roles, source_material, sections)
        if source_material.get("source_kind") in LOOP_SAMPLE_KINDS:
            d["default_depth"] = "foreground"
        return d

    monkeypatch.setattr(pipeline, "plan_depth", _foreground_loop_depth)
    fixture = _ROOT / "fixtures" / "dense_chorus_with_loops"
    manifest = load_manifest(fixture / "project_manifest.json")
    return pipeline.analyze(str(fixture / "stems"), manifest)


def test_promotion_is_live_in_production_analyze(monkeypatch):
    """The production ``result.creative`` (NO re-run) has the loop branch won by
    ``loop_deconstruct`` carrying the promotion line — proving the promotion fires
    in the real pipeline, i.e. provenance/source_audits are computed before
    creative and the evidence is available to ``score_variant``."""
    res = _analyze_with_foregrounded_loops(monkeypatch)

    # The evidence is genuinely produced by the REAL analyzers in the pipeline.
    red_flags = {f for a in res.source_audits["audits"] for f in a["red_flags"]}
    assert "foregrounded loop" in red_flags
    assert res.provenance["summary"]["high_risk"] >= 1

    # Read the PRODUCTION creative value directly — no re-run of the engine.
    branch = next(b for b in res.creative["branches"] if b["problem_id"] == "loop")
    loop_a = _variant_by_id(branch, "loop_A")
    assert loop_a["kind"] == "loop_deconstruct"
    assert branch["winning"]["winning_variant"] == "loop_A"
    assert loop_a["scores"].get("score_nudges") == [PROMOTION_REASON]
    assert loop_a["scores"]["overall_score"] == pytest.approx(85.9, abs=1e-9)


def test_production_governed_winner_is_loop_deconstruct(monkeypatch):
    """The governed winner (the layer that actually ranks) likewise flips to
    ``loop_A`` in production — the promotion reaches the governed surface, no
    veto. Asserted on ``result.governance`` from the real ``analyze()``."""
    res = _analyze_with_foregrounded_loops(monkeypatch)
    gb = next(
        b for b in res.governance["governed_branches"] if b["problem_id"] == "loop"
    )
    assert gb["governed_winner"] == "loop_A"
