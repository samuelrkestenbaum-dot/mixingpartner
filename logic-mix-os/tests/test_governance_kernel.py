"""Layer 1 — Gravito governance kernel (Hardening Packet 3)."""

from __future__ import annotations

from logic_mix_os.governance_kernel import (
    AUTHORITY_CLASSES,
    GovernanceKernel,
    classify_action,
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
