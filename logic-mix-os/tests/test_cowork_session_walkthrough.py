"""P-021 — verified end-to-end agent walkthrough THROUGH the cowork surface.

The MILESTONE of the P-019 -> P-023 arc. P-019 made the learning loop *closeable*
inside cowork (``record_mix_pass``); P-020 made the flow *discoverable*
(``describe_session``). This module proves, executably, that an agent using ONLY
the cowork command surface (``build_context`` + ``run_command`` — nothing else)
can drive a COMPLETE mixing session start-to-finish AND close the learning loop.
After this, "Cowork-usable end-to-end" is a pinned fact, not a claim.

The four proofs, exactly as the packet contract cuts them:

  1. **Discover-then-drive:** call ``run_command("describe_session", ctx)`` to get
     the canonical ordered phases, then drive the ESSENTIAL happy-path command of
     each phase IN THAT ORDER via ``run_command`` — intake -> classify -> diagnose
     -> plan -> checklist -> validate -> record-outcome -> next-pass. Each driven
     command must return sane, JSON-serializable structured output: the chain runs
     without ever dropping out of the cowork surface. (We drive the CORE path — one
     essential command per phase — not all 34; param-heavy / auxiliary commands are
     honestly noted, not forced into the line.)
  2. **The loop CLOSES (milestone assertion):** at record-outcome, call
     ``record_mix_pass(..., reverted=True)`` (the LIVE channel), then a FRESH
     ``build_context(memory_dir=...)`` -> ``suggest_next_pass`` surfaces the
     confirmed "Revert last pass" — with NO hand re-run of the planner. Proven
     load-bearing: reading a DIFFERENT (un-threaded) store surfaces no revert, so
     the assertion is not vacuous.
  3. **Live-vs-dead pin:** ``write_mix_decision`` (the display-only DEAD ledger)
     does NOT change ``suggest_next_pass``, whereas ``record_mix_pass`` (LIVE
     history) DOES. Pins, executably, that only ``record_mix_pass`` closes the loop.
  4. **Determinism:** real seeded fixtures + the real ``analyze()`` path (fake
     adapters only — no DAW/Logic/AppleScript/subprocess/network/``.logicx``). Same
     inputs -> same plan / next-pass across independent contexts.

TESTS-ONLY: this module drives the ALREADY-BUILT surface; it adds no product
behaviour. Local JSON I/O of the app's own store only. Deterministic.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from logic_mix_os.cowork import build_context, run_command
from logic_mix_os.memory import ProjectMemory

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "fixtures" / "dense_chorus_with_loops"


def _manifest() -> dict:
    return json.loads((FIXTURE / "project_manifest.json").read_text())


def _stems() -> str:
    return str(FIXTURE / "stems")


# The ONE essential happy-path command that carries each canonical phase. This is
# the core end-to-end spine an agent drives; it is NOT all 34 commands. The
# per-phase choice is deliberate:
#   intake          -> intake_project      (load the project)
#   classify        -> classify_tracks     (identity + source + role, in one view)
#   diagnose        -> detect_masking      (the headline mix problem)
#   plan            -> generate_mix_plan   (the full plan)
#   checklist       -> render_logic_checklist (the human-executable export)
#   validate        -> validate_mix_pass   (scores + stop conditions + warnings)
#   record-outcome  -> record_mix_pass     (LIVE channel — closes the loop)
#   next-pass       -> suggest_next_pass   (the history-informed next iteration)
_ESSENTIAL_PER_PHASE = {
    "intake": "intake_project",
    "classify": "classify_tracks",
    "diagnose": "detect_masking",
    "plan": "generate_mix_plan",
    "checklist": "render_logic_checklist",
    "validate": "validate_mix_pass",
    "record-outcome": "record_mix_pass",
    "next-pass": "suggest_next_pass",
}

# Commands honestly SKIPPED from the driven line (documented, not forced). These
# are exercised by their own tests; the walkthrough proves the CORE spine.
#   compare_to_reference    — needs a reference bounce (param-heavy)
#   override_track_identity — mutates identity; needs track_id/identity params
#   build_missing_tool      — meta helper for a capability gap (auxiliary)
#   run_creative_engine     — parallel creative exploration (auxiliary)
#   describe_session        — the navigation command (drives the walkthrough, not a step)
_KNOWINGLY_SKIPPED = {
    "compare_to_reference",
    "override_track_identity",
    "build_missing_tool",
    "run_creative_engine",
    "describe_session",
}


def _record_confirmed_revert_through_cowork(memory_dir) -> None:
    """Drive the OUTCOME half of the loop ENTIRELY through cowork commands.

    Records a baseline pass, then a pass whose ``section_contrast_score`` is 20
    HIGHER (so the score-delta inference alone says the move IMPROVED — it would
    surface NOTHING) but recorded ``reverted=True``. The non-tautological override
    case: any later confirmed-revert item proves the ``reverted`` flag — recorded
    THROUGH cowork's ``record_mix_pass`` — reached the live planner. Mirrors the
    P-019 liveness seed, but here as the record-outcome step of a FULL session.
    """
    s, m = _stems(), _manifest()

    ctx_base = build_context(stems=s, manifest=m, memory_dir=str(memory_dir))
    run_command("record_mix_pass", ctx_base, name="baseline")

    ctx_rev = build_context(stems=s, manifest=m, memory_dir=str(memory_dir))
    baseline_sc = ctx_rev["result"].doctrine_score.get("section_contrast_score") or 60
    ctx_rev["result"].doctrine_score["section_contrast_score"] = baseline_sc + 20
    run_command("record_mix_pass", ctx_rev, name="reverted_pass", reverted=True)


# --------------------------------------------------------------------------- #
# 1. Discover-then-drive: the full happy-path spine, IN describe_session order.
# --------------------------------------------------------------------------- #
def test_full_session_drives_end_to_end_through_cowork(tmp_path):
    """An agent drives every phase's essential command IN ORDER, via cowork only.

    ``describe_session`` supplies the canonical phase order; the agent then calls
    ``run_command`` for the one essential command of each phase, in that order, on
    a single memory-backed context. Every driven command must return
    JSON-serializable structured output — the chain never drops out of the surface.
    """
    s, m = _stems(), _manifest()
    mem_dir = tmp_path / "walkthrough_store"
    ctx = build_context(stems=s, manifest=m, memory_dir=str(mem_dir))

    # DISCOVER: the ordered phases come from the surface itself, not a hardcode.
    session = run_command("describe_session", ctx)
    phase_order = [p["phase"] for p in session["phases"]]
    assert phase_order == [
        "intake", "classify", "diagnose", "plan",
        "checklist", "validate", "record-outcome", "next-pass",
    ], "describe_session must supply the canonical order the agent drives"

    # Every phase in the discovered order maps to an essential command we drive.
    assert set(phase_order) == set(_ESSENTIAL_PER_PHASE), (
        "the driven spine must cover exactly the discovered phases"
    )

    # DRIVE: one essential command per phase, IN the discovered order.
    driven = {}
    for phase in phase_order:
        cmd = _ESSENTIAL_PER_PHASE[phase]
        if cmd == "record_mix_pass":
            out = run_command(cmd, ctx, name=f"{phase}_pass")
        else:
            out = run_command(cmd, ctx)
        driven[phase] = out
        # Sane, structured, JSON-serializable — the surface is not dropped.
        json.dumps(out)
        assert out is not None, f"phase {phase} command {cmd} returned nothing"

    # Phase-specific sanity: each essential command produced its expected shape,
    # proving the chain genuinely ran (not a string of empty passthroughs).
    assert driven["intake"]["song_title"]
    assert driven["intake"]["tracks"] > 0
    assert isinstance(driven["classify"], list) and driven["classify"]
    assert "identity" in driven["classify"][0] and "musical_role" in driven["classify"][0]
    assert "events" in driven["diagnose"] and "summary" in driven["diagnose"]
    assert driven["plan"]["song_title"] and "overall_mix_readiness_score" in driven["plan"]
    assert isinstance(driven["checklist"], str) and "Logic Action Checklist" in driven["checklist"]
    assert set(driven["validate"]) >= {"scores", "stop_conditions", "warnings"}
    assert driven["record-outcome"]["pass_name"] == "record-outcome_pass"
    assert isinstance(driven["next-pass"], list) and driven["next-pass"]
    assert all("title" in it for it in driven["next-pass"])

    # The record-outcome step landed on the LIVE channel (read back independently),
    # so the spine's record step is real — the loop is fed, not merely returned.
    assert ProjectMemory(mem_dir).history()[-1]["pass_name"] == "record-outcome_pass"


def test_walkthrough_covers_the_registry_honestly(tmp_path):
    """The driven spine + knowingly-skipped set account for the surface honestly.

    Guards the honesty clause: the essential commands we DRIVE and the commands we
    consciously SKIP are all real registry keys, disjoint, and together they leave
    no phase silently unaddressed. This makes the walkthrough's coverage claim
    auditable — a green test cannot quietly skip a phase's essential command.
    """
    from logic_mix_os.cowork import COMMANDS

    driven = set(_ESSENTIAL_PER_PHASE.values())
    skipped = set(_KNOWINGLY_SKIPPED)

    # Every named command is a real registry key.
    for name in driven | skipped:
        assert name in COMMANDS, f"{name!r} is not a real cowork command"

    # Driven and skipped are disjoint — no command is both driven and skipped.
    assert driven.isdisjoint(skipped)

    # Each canonical phase has exactly one driven essential command (no phase
    # silently unaddressed).
    session = run_command("describe_session", {"result": None, "memory": None})
    for phase in session["phases"]:
        assert phase["phase"] in _ESSENTIAL_PER_PHASE, (
            f"phase {phase['phase']!r} has no driven essential command"
        )
        assert _ESSENTIAL_PER_PHASE[phase["phase"]] in phase["commands"], (
            f"the essential command for {phase['phase']!r} is not one of its phase commands"
        )


# --------------------------------------------------------------------------- #
# 2. The loop CLOSES — the milestone assertion (no hand re-run).
# --------------------------------------------------------------------------- #
def test_loop_closes_across_the_full_session_no_rerun(tmp_path):
    """Record a confirmed revert via cowork, then a FRESH context's next-pass
    surfaces it — the loop closes inside the cowork surface, no planner re-run.

    This is the milestone: the OUTCOME half (``record_mix_pass``) and the READ half
    (``suggest_next_pass``) are both driven through ``run_command``, and a brand-new
    ``build_context(memory_dir=...)`` — running a fresh ``analyze(memory_dir=...)`` —
    carries the recorded confirmed revert into the next iteration's plan.
    """
    s, m = _stems(), _manifest()
    seeded = tmp_path / "loop_store"

    # OUTCOME half — recorded through cowork's LIVE channel.
    _record_confirmed_revert_through_cowork(seeded)

    # READ half — a FRESH context; no manual planner re-run.
    ctx_no = build_context(stems=s, manifest=m)
    ctx_mem = build_context(stems=s, manifest=m, memory_dir=str(seeded))

    np_no = run_command("suggest_next_pass", ctx_no)
    np_mem = run_command("suggest_next_pass", ctx_mem)

    # Sanity: the memoryless run surfaces no revert.
    assert not any(it["title"] == "Revert last pass" for it in np_no)

    # The confirmed revert — recorded via cowork — reaches the live next-pass.
    revert = next((it for it in np_mem if it["title"] == "Revert last pass"), None)
    assert revert is not None, "confirmed revert recorded via cowork must close the loop"
    assert "confirm" in revert["evidence"].lower()
    assert np_mem != np_no  # the recorded outcome measurably changed the next pass


def test_loop_close_is_load_bearing(tmp_path):
    """The milestone assertion is NOT vacuous: an un-threaded record surfaces no revert.

    We record the confirmed revert to one store but READ a DIFFERENT (empty) store —
    exactly what a broken / misrouted handler would produce. The fresh next-pass then
    sees nothing and surfaces no revert, so the ``assert revert is not None`` gate
    above WOULD fail. Proves the loop closes because the record is genuinely
    persisted and threaded, not because the assertion is empty.
    """
    s, m = _stems(), _manifest()
    recorded_to = tmp_path / "recorded_store"
    read_from = tmp_path / "empty_store"  # a store the record never reached

    _record_confirmed_revert_through_cowork(recorded_to)

    ctx_broken = build_context(stems=s, manifest=m, memory_dir=str(read_from))
    np_broken = run_command("suggest_next_pass", ctx_broken)
    assert not any(it["title"] == "Revert last pass" for it in np_broken), (
        "with no live record threaded, the loop must NOT surface a revert"
    )


# --------------------------------------------------------------------------- #
# 3. Live-vs-dead pin: only record_mix_pass closes the loop.
# --------------------------------------------------------------------------- #
def test_dead_ledger_write_does_not_change_next_pass(tmp_path):
    """``write_mix_decision`` (display-only DEAD ledger) does NOT move next-pass.

    An agent could mistake a decision-ledger write for loop-closing. This pins,
    executably, that it is not: recording a decision via cowork then reading a fresh
    context's ``suggest_next_pass`` yields the SAME next pass as before the write.
    """
    s, m = _stems(), _manifest()
    ledger_dir = tmp_path / "ledger_store"

    ctx_before = build_context(stems=s, manifest=m, memory_dir=str(ledger_dir))
    np_before = run_command("suggest_next_pass", ctx_before)

    # DEAD channel write via cowork.
    decision = {"decision": "widen the chorus", "reason": "felt narrow"}
    written = run_command("write_mix_decision", ctx_before, decision=decision)
    assert written["event_type"] == "mix_decision"  # it DID write the ledger

    # A fresh context reads the same store — next-pass is unchanged.
    ctx_after = build_context(stems=s, manifest=m, memory_dir=str(ledger_dir))
    np_after = run_command("suggest_next_pass", ctx_after)
    assert np_after == np_before, (
        "the DEAD decision ledger must NOT change next-pass — only record_mix_pass closes the loop"
    )


def test_live_record_changes_next_pass_where_dead_write_does_not(tmp_path):
    """Head-to-head: the SAME confirmed-revert intent moves next-pass only via the
    LIVE ``record_mix_pass`` channel, never via the DEAD ``write_mix_decision`` one.

    Two independent stores start from the identical memoryless next-pass. Into one
    we write a decision describing a revert (DEAD); into the other we record a
    confirmed revert (LIVE). Only the LIVE store's fresh next-pass changes — pinning
    that ``record_mix_pass`` is the sole loop-closing channel.
    """
    s, m = _stems(), _manifest()

    baseline = run_command("suggest_next_pass", build_context(stems=s, manifest=m))

    # DEAD path: describe a revert in the decision ledger.
    dead_dir = tmp_path / "dead_store"
    ctx_dead = build_context(stems=s, manifest=m, memory_dir=str(dead_dir))
    run_command("write_mix_decision", ctx_dead,
                decision={"decision": "revert last pass", "reason": "operator reverted it"})
    np_dead = run_command("suggest_next_pass",
                          build_context(stems=s, manifest=m, memory_dir=str(dead_dir)))

    # LIVE path: record the confirmed revert as a pass outcome.
    live_dir = tmp_path / "live_store"
    _record_confirmed_revert_through_cowork(live_dir)
    np_live = run_command("suggest_next_pass",
                          build_context(stems=s, manifest=m, memory_dir=str(live_dir)))

    # DEAD write left next-pass exactly at baseline; LIVE record changed it.
    assert np_dead == baseline, "DEAD ledger write must not change next-pass"
    assert np_live != baseline, "LIVE record_mix_pass must change next-pass"
    assert any(it["title"] == "Revert last pass" for it in np_live)
    assert not any(it["title"] == "Revert last pass" for it in np_dead)


# --------------------------------------------------------------------------- #
# 4. Determinism: same inputs -> same plan / next-pass through the surface.
# --------------------------------------------------------------------------- #
def test_driven_session_is_deterministic(tmp_path):
    """Same fixture -> byte-identical plan and next-pass across independent contexts.

    Two fresh ``build_context`` runs on the SAME fixture drive ``generate_mix_plan``
    and ``suggest_next_pass``; their JSON must be identical. Proves the walkthrough
    is deterministic where it should be (no adapter / clock leakage into the plan).
    """
    s, m = _stems(), _manifest()

    ctx_a = build_context(stems=s, manifest=m)
    ctx_b = build_context(stems=s, manifest=m)

    plan_a = run_command("generate_mix_plan", ctx_a)
    plan_b = run_command("generate_mix_plan", ctx_b)
    assert json.dumps(plan_a, sort_keys=True) == json.dumps(plan_b, sort_keys=True)

    np_a = run_command("suggest_next_pass", ctx_a)
    np_b = run_command("suggest_next_pass", ctx_b)
    assert json.dumps(np_a, sort_keys=True) == json.dumps(np_b, sort_keys=True)


def test_seeded_loop_close_is_deterministic(tmp_path):
    """The loop-closing next-pass is deterministic across two independent seeds.

    Seeding the SAME confirmed-revert sequence into two separate stores (each via
    cowork's ``record_mix_pass``) and reading each through a fresh context yields
    byte-identical next-pass output — the loop closes reproducibly, not by chance.
    """
    s, m = _stems(), _manifest()

    seed_a = tmp_path / "seed_a"
    seed_b = tmp_path / "seed_b"
    _record_confirmed_revert_through_cowork(seed_a)
    _record_confirmed_revert_through_cowork(seed_b)

    np_a = run_command("suggest_next_pass", build_context(stems=s, manifest=m, memory_dir=str(seed_a)))
    np_b = run_command("suggest_next_pass", build_context(stems=s, manifest=m, memory_dir=str(seed_b)))

    assert json.dumps(np_a, sort_keys=True) == json.dumps(np_b, sort_keys=True)
    assert any(it["title"] == "Revert last pass" for it in np_a)
