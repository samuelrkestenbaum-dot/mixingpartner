"""Local HTML dashboard tests (build packet section 50)."""

from __future__ import annotations

import re

from logic_mix_os.renderers.html_dashboard import render_dashboard


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
