"""Layer 1 — Gravito governance kernel (Hardening Packet 3)."""

from __future__ import annotations

from logic_mix_os.governance_kernel import (
    AUTHORITY_CLASSES,
    REVIEW_DEFAULT_CLASS,
    GovernanceKernel,
    classify_action,
    classify_action_detailed,
    demo_actions,
    govern_actions,
)


def test_classification_across_the_ladder():
    assert classify_action({"kind": "analyze"}) == 0
    assert classify_action({"kind": "write_report"}) == 1
    assert classify_action({"kind": "offline_render"}) == 2
    assert classify_action({"kind": "insert_plugin"}) == 3
    assert classify_action({"type": "automation"}) == 3
    assert classify_action({"kind": "export_master"}) == 4
    assert classify_action({"kind": "x", "reason": "delete source audio in place"}) == 5
    assert classify_action({"kind": "overwrite_source"}) == 5


def test_class_0_1_allowed_automatically():
    k = GovernanceKernel()
    for kind in ("analyze", "write_report"):
        r = k.propose({"kind": kind})
        assert r["decision"] == "allow" and r["allowed_now"] and not r["approval_required"]


def test_class_2_offline_render_gated_on_source_immutability():
    k = GovernanceKernel()
    ok = k.propose({"kind": "offline_render", "source_immutable": True, "generated_output_only": True})
    assert ok["decision"] == "allow"
    bad = k.propose({"kind": "offline_render", "source_immutable": False})
    assert bad["decision"] == "review_required" and not bad["allowed_now"]


def test_class_3_logic_mutation_is_review_required_not_applied():
    k = GovernanceKernel()
    r = k.propose({"kind": "insert_plugin", "reason": "Channel EQ on vocal"})
    assert r["decision"] == "review_required" and r["must_not_execute_here"] is True
    k.approve(r["action_id"])
    applied = k.mark_applied(r["action_id"])
    assert applied["ok"] is False and "dry-run" in applied["reason"].lower()


def test_class_4_external_cannot_execute():
    k = GovernanceKernel()
    r = k.propose({"kind": "export_master", "reason": "export + upload"})
    assert r["authority_class"] == 4 and r["decision"] == "review_required"
    k.approve(r["action_id"])
    assert k.mark_applied(r["action_id"])["ok"] is False


def test_class_5_blocked_and_unapprovable():
    k = GovernanceKernel()
    r = k.propose({"kind": "overwrite_source"})
    assert r["decision"] == "blocked"
    assert k.approve(r["action_id"])["ok"] is False
    assert k.mark_applied(r["action_id"])["ok"] is False


def test_every_receipt_has_required_fields_and_rollback():
    k = GovernanceKernel()
    required = {"action_id", "receipt_id", "authority_class", "risk_level", "allowed_now",
                "approval_required", "evidence", "reason", "reversibility", "rollback_plan",
                "source_artifacts", "target_artifacts", "decision"}
    for a in demo_actions():
        r = k.propose(a)
        assert required <= set(r)
        assert r["rollback_plan"]


def test_no_unapproved_action_can_be_applied():
    k = GovernanceKernel()
    # Class 2 that needs review (source not immutable) cannot apply without approval...
    r = k.propose({"kind": "offline_render", "source_immutable": False})
    assert k.mark_applied(r["action_id"])["ok"] is False
    k.approve(r["action_id"])
    assert k.mark_applied(r["action_id"])["ok"] is True  # class 2, now approved -> applies locally


def test_auto_allowed_local_artifact_applies():
    k = GovernanceKernel()
    r = k.propose({"kind": "write_report", "target_artifacts": ["reports/x.md"]})
    assert k.mark_applied(r["action_id"])["ok"] is True


def test_govern_actions_summary_and_ledger():
    res = govern_actions(demo_actions())
    assert res["ledger_size"] == len(demo_actions())
    assert "blocked" in res["summary"]  # the destructive demo action
    assert len(AUTHORITY_CLASSES) == 6


# --- Packet 4, Layer 1: fail-safe-high classification ----------------------

def test_unknown_kind_is_review_required_not_allowed():
    """An unrecognised action kind must fail safe (review) — never fail open to Class 0."""
    k = GovernanceKernel()
    r = k.propose({"kind": "frobnicate_the_widget", "reason": "do something the kernel has never heard of"})
    assert r["authority_class"] == REVIEW_DEFAULT_CLASS
    assert r["authority_class"] >= 3
    assert r["decision"] == "review_required"
    assert r["allowed_now"] is False
    assert r["approval_required"] is True


def test_unknown_kind_sets_unknown_kind_flag():
    detail = classify_action_detailed({"kind": "totally_made_up_action"})
    assert detail["unknown_kind"] is True
    assert detail["ambiguous"] is True
    r = GovernanceKernel().propose({"kind": "totally_made_up_action"})
    assert r["unknown_kind"] is True


def test_ambiguous_action_sets_ambiguous_flag():
    """A benign known kind dragging a higher-risk marker is ambiguous and escalates."""
    detail = classify_action_detailed({"kind": "write_report", "reason": "insert plugin on the lead vocal"})
    assert detail["ambiguous"] is True
    assert detail["matched_markers"]


def test_benign_kind_with_daw_marker_escalates_to_class_3():
    k = GovernanceKernel()
    r = k.propose({"kind": "write_report",
                   "reason": "write Logic automation for the chorus send level"})
    assert r["authority_class"] == 3
    assert r["escalated_from"] == 1 and r["escalated_to"] == 3
    assert r["decision"] == "review_required"
    assert "daw_session" in r["matched_markers"]


def test_benign_kind_with_destructive_marker_escalates_to_class_5_blocked():
    k = GovernanceKernel()
    r = k.propose({"kind": "write_report", "reason": "overwrite source stem in place"})
    assert r["authority_class"] == 5
    assert r["decision"] == "blocked"
    assert k.approve(r["action_id"])["ok"] is False
    assert k.mark_applied(r["action_id"])["ok"] is False


def test_known_safe_allowlist_is_not_escalated():
    """Known-safe kinds with no risky markers keep their low class and stay non-ambiguous."""
    for kind, expected in (("analyze", 0), ("write_report", 1), ("offline_render", 2)):
        detail = classify_action_detailed({"kind": kind})
        assert detail["authority_class"] == expected
        assert detail["unknown_kind"] is False
        assert detail["ambiguous"] is False
        assert detail["escalated_from"] == detail["escalated_to"] == expected


def test_ingest_external_render_stays_class_1():
    """The ingest path's known kind must not be swept up by fail-safe-high."""
    detail = classify_action_detailed({"kind": "ingest_external_render",
                                       "reason": "Ingest an externally produced render and write a comparison report."})
    assert detail["authority_class"] == 1
    assert detail["unknown_kind"] is False
    assert detail["ambiguous"] is False
