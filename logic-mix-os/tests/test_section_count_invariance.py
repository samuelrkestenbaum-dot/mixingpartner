"""P-060 — the section-count-invariance regression.

``analyzers.masking_analyzer.analyze_masking`` emits every masking conflict
ONCE PER SECTION (per-section recommendations are a feature). Six doctrine
scorers historically counted ``len(per-section events)`` RAW, so ONE physical
conflict duplicated across N sections was penalized N times — the verdict of a
real many-section song CRATERED (a lead "masked by 48 forward elements" that was
really masked by 4, across 12 sections). This is the regression that would have
caught it: the masking-driven component scores must be INVARIANT to how many
sections carry the SAME conflict.

The fix (P-060) is scorer-side dedup of DISTINCT masking relationships, applied
AFTER each scorer's existing classification/severity filter (filter first, then
dedup — never dedup before filtering, or a genuinely section-specific conflict
would be dropped). This test pins both halves:

1. **Invariance** — the SAME records + the SAME conflicts, replayed across 1 vs
   6 vs 12 sections (identical placement in every section), score IDENTICALLY on
   every masking-driven component.
2. **Over-correction guard** — a conflict that is real in only 1 of N sections
   (a masker forward in exactly one section) STILL registers once: its score is
   strictly below the no-conflict baseline AND equal to the single-section case.
   Dedup removes duplicates, never distinct section-specific conflicts.
"""

from __future__ import annotations

import pytest

from logic_mix_os.analyzers.masking_analyzer import analyze_masking
from logic_mix_os.doctrine import doctrine_engine

from test_vocal_type import _lead, _rec

# The six components that historically scaled with section count (the fix's
# whole surface). Every other component either ignores masking events entirely
# or already used a boolean ``any(...)`` read (``beat_identity``,
# ``loop_context`` — deliberately untouched).
MASKING_DRIVEN_COMPONENTS = [
    "physical_space_score",
    "emotional_hierarchy_score",
    "vocal_centrality_score",
    "static_mix_score",
    "low_end_motion_score",
    "vocal_role_fit_score",
]

SECTION_COUNTS = [1, 6, 12]


def _low_carrier(name: str, identity: str, family: str) -> dict:
    """A kick/bass record carrying real sub weight: top-level ``band_energy``
    for the analyzer's ``_low_end_conflict`` read, ``metrics.band_energy`` for
    the ``low_end_motion`` presence gate — both above their floors so a
    CRITICAL kick/bass low-end conflict fires and the pocket scorer reaches its
    conflict penalty."""
    r = _rec(name, identity=identity, family=family, depth="foreground",
             role="structural", width=0.2, presence=0.0)
    r["band_energy"] = {"low": 0.5}
    r["metrics"]["band_energy"] = {"low": 0.5}
    return r


def _all_six_records() -> list:
    """One synthetic project that exercises ALL six masking-driven scorers,
    tuned so none of them clamps to the 0/100 rails (so the invariance pin is
    real, not a clamp artefact):

    * a FORWARD lead vocal masked by two forward/heard presence-band elements
      (Piano, Synth) plus the forward backing chop -> three distinct
      ``bad_masking`` relationships (emotional_hierarchy, vocal_centrality, the
      lead half of vocal_role_fit);
    * three WIDE forward/heard elements with NO presence-band energy -> a
      ``width_crowding`` conflict WITHOUT adding vocal maskers (physical_space);
    * a Kick/Bass critical low-end conflict (static_mix, low_end_motion);
    * a non-lead vocal chop forward under the two presence maskers -> two
      distinct ``vocal_band_masking`` relationships (the non-lead half of
      vocal_role_fit).
    """
    lead = _lead(depth="intimate")  # forward in every section, presence 0.3
    piano = _rec("Piano", identity="piano", family="keys", depth="foreground",
                 role="heard", width=0.2, presence=0.2)
    synth = _rec("Synth", identity="synth", family="synth", depth="foreground",
                 role="heard", width=0.2, presence=0.2)
    chop = _rec("BGV Chop", identity="backing_vocal", family="vocal",
                depth="foreground", role="heard", width=0.2, td=0.8,
                crest=16.0, presence=0.18, source="splice_sample")
    # Three WIDE elements carrying the stereo image but NO presence energy
    # (presence 0.0 -> below the 0.05 vocal-overlap floor), so they crowd the
    # width without becoming lead/chop maskers.
    wide = [
        _rec("Wide Gtr L", identity="electric_guitar", family="guitars",
             depth="foreground", role="heard", width=0.6, presence=0.0),
        _rec("Wide Gtr R", identity="electric_guitar", family="guitars",
             depth="foreground", role="heard", width=0.6, presence=0.0),
        _rec("Wide Keys", identity="organ", family="keys",
             depth="foreground", role="heard", width=0.6, presence=0.0),
    ]
    kick = _low_carrier("Kick", "kick", "drums")
    bass = _low_carrier("Bass", "bass_guitar", "bass")
    return [lead, piano, synth, chop, *wide, kick, bass]


def _sections(n: int) -> list:
    """N sections with NO per-section depth variation: every record keeps its
    ``depth_default`` in every section (``depth_by_section`` is empty), so each
    conflict is emitted IDENTICALLY in all N sections."""
    return [{"section_id": f"s{i}"} for i in range(n)]


def _score(records: list, n_sections: int) -> dict:
    """Run the real per-section emission (``analyze_masking``) for ``n_sections``
    then score. ``sections_analysis`` is held constant (empty) across counts —
    only the number of per-section conflict COPIES varies, so any cross-count
    drift is purely the section-count bug this test targets."""
    report = analyze_masking(records, _sections(n_sections))
    return doctrine_engine.score_doctrine(records, [], report, None)


def test_conflict_emission_actually_scales_with_sections():
    """Sanity: the test is meaningful only if ``analyze_masking`` really does
    duplicate the conflict per section — the critical kick/bass low-end conflict
    appears exactly once per section, so 12 sections carry 12 raw copies of ONE
    physical relationship. This is the input the scorers must now dedup."""
    records = _all_six_records()
    for n in SECTION_COUNTS:
        report = analyze_masking(records, _sections(n))
        crit_low = [e for e in report["events"]
                    if e["classification"] == "low_end_conflict"
                    and e["severity"] == "critical"]
        assert len(crit_low) == n, (n, len(crit_low))
        # ...yet they are ONE distinct relationship (the same element pair).
        assert len({frozenset(e["elements"]) for e in crit_low}) == 1, n


@pytest.mark.parametrize("component", MASKING_DRIVEN_COMPONENTS)
def test_masking_driven_scores_are_section_count_invariant(component):
    """THE HEADLINE PIN: the SAME records + the SAME conflicts replayed across
    1 vs 6 vs 12 sections score IDENTICALLY on every masking-driven component.
    Pre-fix these scaled with section count (the '48 forward elements' crater);
    post-fix the deduped distinct-relationship count is section-invariant."""
    records = _all_six_records()
    scores = {n: _score(records, n) for n in SECTION_COUNTS}
    one = scores[1][component]
    for n in SECTION_COUNTS:
        assert scores[n][component] == one, (component, n, scores[n][component], one)


def test_masked_by_count_uses_distinct_maskers_not_sections():
    """The user-facing evidence stops scaling too: 'Vocal masked by N forward
    element(s)' reports the DISTINCT masker count, not maskers x sections."""
    records = _all_six_records()
    for n in SECTION_COUNTS:
        report = analyze_masking(records, _sections(n))
        _, ev = doctrine_engine._emotional_hierarchy(
            records, records[0], report["events"], [],
            doctrine_engine._DOCTRINE)
        masked_line = next(s for s in ev if "masked by" in s)
        # Three distinct forward maskers (Piano, Synth, BGV Chop) — never
        # multiplied by ``n``.
        assert "masked by 3 forward element(s)" in masked_line, (n, masked_line)


# --------------------------------------------------------------------------- #
# Over-correction guard: dedup drops DUPLICATES, never distinct conflicts.
# --------------------------------------------------------------------------- #
def _section_specific_records(forward_sections: set, n: int) -> list:
    """A lead (forward always) + an Organ masker forward in ONLY the given
    sections (midground elsewhere). The lead/Organ conflict is real exactly in
    ``forward_sections`` and controlled-blend (info) everywhere else."""
    lead = _lead(depth="intimate")
    organ = _rec("Organ", identity="organ", family="keys",
                 depth="midground", role="heard", width=0.2, presence=0.2)
    organ["depth_by_section"] = {f"s{i}": "foreground" for i in range(n)
                                 if i in forward_sections}
    return [lead, organ]


def test_section_specific_conflict_still_registers_once():
    """A masker forward in only 1 of 12 sections is a GENUINE, section-specific
    conflict — dedup must keep it (once), not average it away. Its score is
    strictly below the no-conflict baseline AND equal to the single-section
    case (the vocal_chop_groove ordering guardrail: filter by severity FIRST,
    then dedup the survivors)."""
    n = 12
    specific = _section_specific_records({0}, n)   # forward in s0 only
    none = _section_specific_records(set(), n)     # never forward

    specific_score = _score(specific, n)
    baseline_score = _score(none, n)
    single = _score(_section_specific_records({0}, 1), 1)

    for component in ("emotional_hierarchy_score", "vocal_centrality_score"):
        # It registers (strictly below the clean baseline)...
        assert specific_score[component] < baseline_score[component], component
        # ...exactly once (equal to the honest single-section reading).
        assert specific_score[component] == single[component], component
