"""Local HTML dashboard tests (build packet section 50)."""

from __future__ import annotations

import copy
import re

from logic_mix_os.renderers.html_dashboard import render_dashboard
from logic_mix_os.renderers.operator_view import render_status

# Stable readiness labels (P-003). Both renderers must surface these exactly.
READY_LABEL = "READY TO STOP"
NOT_YET_LABEL = "NOT YET — keep iterating"


def _with_stop_conditions(result, stop_conditions):
    """Render-only stand-in: a real analyzed result whose governance carries a
    hand-built stop_conditions dict (other fields untouched, deterministic)."""
    clone = copy.copy(result)
    clone.governance = dict(result.governance)
    clone.governance["stop_conditions"] = stop_conditions
    return clone


def test_dashboard_is_self_contained_html(analyzed):
    html = render_dashboard(analyzed["dense_chorus_with_loops"])
    assert html.startswith("<!doctype html>")
    assert "<style>" in html and "Logic Mix OS" in html
    # local-first: no external resource references, no script tags
    assert "http://" not in html.replace("http://json-schema.org", "")
    assert "https://" not in html
    assert "<script" not in html.lower()


def test_dashboard_includes_core_screens(analyzed):
    html = render_dashboard(analyzed["dense_chorus_with_loops"])
    for anchor in ['id="scores"', 'id="sections"', 'id="tracks"', 'id="masking"',
                   'id="nextpass"', 'id="automation"', 'id="creative"',
                   'id="governance"', 'id="checklist"']:
        assert anchor in html


def test_dashboard_shows_song_and_scores(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    html = render_dashboard(res)
    assert res.project.song_title in html
    assert "Roy Halee" in html and "Phil Ramone" in html


def test_dashboard_escapes_content(analyzed):
    # Ensure track names render and there are no obviously broken tags
    html = render_dashboard(analyzed["splice_loop_problem"])
    assert "Splice Loop" in html
    # balanced-ish: every <table opens and closes
    assert html.count("<table>") == html.count("</table>")


# --- P-003: readiness-vs-refusal clarity (both renderers, both states) ---

def test_status_text_not_yet_block_lists_reasons(analyzed):
    # Real fixture: should_stop is False with non-empty "not yet:" reasons.
    res = analyzed["dense_chorus_with_loops"]
    sc = res.governance["stop_conditions"]
    assert sc["should_stop"] is False and sc["reasons"]

    out = render_status(res)
    assert NOT_YET_LABEL in out
    assert READY_LABEL not in out
    for reason in sc["reasons"]:
        assert reason in out


def test_status_text_ready_block_shows_warning(analyzed):
    ready = {
        "should_stop": True,
        "reasons": ["all stop conditions met — validate and move to mastering-readiness checks"],
        "warning": "Overworking risk: stop creative experimentation once gains are marginal.",
    }
    res = _with_stop_conditions(analyzed["dense_chorus_with_loops"], ready)

    out = render_status(res)
    assert READY_LABEL in out
    assert NOT_YET_LABEL not in out
    assert ready["warning"] in out


def test_dashboard_not_yet_block_lists_reasons(analyzed):
    res = analyzed["dense_chorus_with_loops"]
    sc = res.governance["stop_conditions"]
    assert sc["should_stop"] is False and sc["reasons"]

    html = render_dashboard(res)
    # readiness block lives inside the governance card
    gov_card = html.split('id="governance"', 1)[1].split("</section>", 1)[0]
    assert NOT_YET_LABEL in gov_card
    assert READY_LABEL not in gov_card
    for reason in sc["reasons"]:
        assert reason in gov_card


def test_dashboard_ready_block_shows_warning(analyzed):
    ready = {
        "should_stop": True,
        "reasons": ["all stop conditions met — validate and move to mastering-readiness checks"],
        "warning": "Overworking risk: stop creative experimentation once gains are marginal.",
    }
    res = _with_stop_conditions(analyzed["dense_chorus_with_loops"], ready)

    html = render_dashboard(res)
    gov_card = html.split('id="governance"', 1)[1].split("</section>", 1)[0]
    assert READY_LABEL in gov_card
    assert NOT_YET_LABEL not in gov_card
    assert ready["warning"] in gov_card


def test_dashboard_readiness_block_stays_self_contained(analyzed):
    ready = {
        "should_stop": True,
        "reasons": ["all stop conditions met"],
        "warning": "Overworking risk: stop once gains are marginal.",
    }
    res = _with_stop_conditions(analyzed["dense_chorus_with_loops"], ready)
    html = render_dashboard(res)
    # readiness rendering must not introduce scripts or external assets
    assert "http://" not in html.replace("http://json-schema.org", "")
    assert "https://" not in html
    assert "<script" not in html.lower()
