# Receipt — P-032g — `loop_context` + `protect_iconic_loops` — THE HINGE

**Date:** 2026-07-01
**Packet:** P-032g — `loop_context` (static-vs-iconic) + `protect_iconic_loops`:
**THE HINGE** — the SIXTH new producer-agnostic doctrine axis (the 13th doctrine
component) **plus the FIRST profile-decided creative gate**. The doctrine-pin
exemplar realized: **the engine DETECTS agnostically** (static = dominant + no
evolution; iconic = dominant + groove/fingerprint function — an ACOUSTIC PROXY;
cultural recognizability deferred), **the profile DECIDES**
(`protect_iconic_loops`, a REQUIRED profile field; `halee_ramone` = `false` =
current behavior).
**Status:** CLOSED — qa **GREEN**, reviewer **PASS (no must-fix)** — dual-green
including the **USER-MANDATED dual byte-identity surface** (doctrine AND
creative).

---

## ★ Reviewer's doctrine finding (recorded prominently)

The status→score map (**iconic 90 / evolving 60 / neutral 50 / unassessed 45 /
static 15**) lives in `doctrine.scorers.loop_context` **IN THE PROFILE JSON** —
even the axis's POLARITY is profile-authored; the engine's fixed contribution
is status DETECTION only. A future profile could invert the entire mapping
without touching code. **"The strongest possible form of the doctrine, not a
leak."**

---

## Scope

**In:**
- **Commit-1 (pure additive, byte-identical):** new agnostic scorer
  `_loop_context` in `doctrine/doctrine_engine.py` + a shared
  `read_loop_context()` helper (the shared detection basis) — the established
  idiom: `loop_context_score` appended LAST to `component_scores`,
  `halee_ramone.json` weight 0, constants block in
  `doctrine.scorers.loop_context`, `producer_profile.py` `_validate`
  required-scorers, `doctrine_score.schema.json` optional property; new
  `tests/test_loop_context.py`.
- **Commit-2 (the creative gate):** `_protected_iconic_loop()` in
  `creative.py::_apply_promotions`, gating the `loop_deconstruct` promotion
  behind the new **REQUIRED** profile field `protect_iconic_loops`
  (`halee_ramone` declares `false` = current behavior — the promotion fires
  exactly as today); new `tests/test_protect_iconic_loops.py`.
- **Shared basis identity-asserted:**
  `creative.read_loop_context is doctrine_engine.read_loop_context` — the gate
  and the scorer read the SAME detection, no fork.
- **Ordering honored:** the Ramone/masked-lead gate fires FIRST — iconic
  protection structurally cannot override a masked lead.

**Explicitly OUT (honest deferrals — test-guarded out of evidence, NOT
faked):**
- Cultural / recognizability iconic-ness (needs provenance/manifest — the
  acoustic proxy is what ships).
- Per-loop bar-level variation.
- Onset-sequence needs.
- The `_halee` `loop_foregrounded` penalty coefficient is UNTOUCHED
  (`loop_foregrounded` = 6; promotion table verbatim;
  `test_packet_cautions_untouched`).

**Engine language OBSERVATIONAL:** zero judgment words across all 7 reachable
statuses (the one "bad_masking" hit is a data-vocabulary key read, not emitted
language).

**Constants (`doctrine.scorers.loop_context`):** status scores —
`no_loop`/`not_dominant` 50, `dominant_unassessed` 45, `dominant_evolving` 60,
`static` 15, `iconic` 90; floors — width 0.6, transient_lift 0.15,
groove_transient 0.35, crest 12.0, rms 1.0 dB / width 0.05 / brightness 0.05.
Evolution floors are threshold GATES only — spreads appear in ZERO arithmetic
(no `_dynamic_mix` re-derivation).

---

## Commits (branch base + hashes)

- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`
- **Packet base (parent):** `6af00fa` (`build-os: set P-032g (loop
  static-vs-iconic) active — THE HINGE`), atop `211e04c` (P-032c close).
- **`835e907`** — P-032g: loop_context (static-vs-iconic) — sixth
  producer-agnostic doctrine axis [Commit-1 — pure additive `_loop_context`
  scorer + shared `read_loop_context()` helper]. **8 files, 957 insertions /
  3 deletions**: `doctrine_engine.py` (+286), `producer_profile.py`,
  `halee_ramone.json`, `doctrine_score.schema.json`, `test_loop_context.py`
  (new, 640), + pin updates (`test_doctrine_profile_sourced.py`,
  `test_producer_profile.py`, `test_low_end_motion.py`). **GREEN IN ISOLATION:
  499 passed + 68/68 regression in a real worktree check.**
- **`e9e804d`** — P-032g: protect_iconic_loops — the first profile-DECIDED
  creative gate [Commit-2 — `_protected_iconic_loop()` in `_apply_promotions`;
  flag as REQUIRED profile field]. **4 files, 481 insertions / 2 deletions**:
  `creative.py` (+46 net), `producer_profile.py`, `halee_ramone.json`,
  `test_protect_iconic_loops.py` (new, 421).

Parent chain: `e9e804d` → `835e907` → `6af00fa` (active-packet confirmation) →
`211e04c` (P-032c close) → `ab14ac7`.

**Merge base for decisions is still `e79426a` = PR #16** — nothing since P-025
has been merged. P-032g is **local-only**, not pushed/merged.

---

## QA proof (GREEN)

- **Full suite:** 473 → **512 passed** / 0 failed / 0 skipped (+39 = 26 + 13).
- **Regression:** **68/68**, 0 warnings.
- **Commit-1 green in isolation:** `835e907` verified in a real worktree —
  **499 passed + 68/68**.
- **★ DUAL byte-identity — BOTH surfaces, INDEPENDENT (the USER-MANDATED
  requirement):**
  - **(a) Doctrine:** 0 mismatches × 3 fixtures; overalls **73.8 / 70.7 /
    74.3** untouched; `loop_context_score` = **50.0 / 15.0 / 15.0** at weight 0
    (both loop fixtures read STATIC — thematically exact).
  - **(b) Creative:** full `result.creative` sorted-key JSON, base vs HEAD →
    **EMPTY diff**; `cmp` byte-identical.
- **Flag liveness confirmed LIVE:** A/B **85.9/loop_A(False) ↔
  81.9/loop_B(True)**; STATIC + protect → promotion still fires; masked lead +
  iconic + protect → promotion still fires (the Ramone gate fires FIRST).
- **Shared basis:** identity-asserted
  (`creative.read_loop_context is doctrine_engine.read_loop_context`).
- **Cautions untouched:** `loop_foregrounded` = 6; promotion table verbatim;
  `test_packet_cautions_untouched`.
- **Observational language:** zero judgment words across all 7 reachable
  statuses (the one "bad_masking" hit is a data-vocabulary key read, not
  emitted language).
- **Safety grep:** **NONE FOUND.**
- **UI smoke:** N/A (doctrine/creative engine change, no UI surface).

---

## Reviewer verdict — PASS (no must-fix)

- **Default path PROVEN unreachable:** the flag is checked before any input;
  a **5,000-trial randomized search** through the gated promotion path →
  **0 divergences**.
- **Protection structurally cannot beat a masked lead:** ordering flag →
  `_lead_masked` → iconic; no short-circuit path exists.
- **FIVE own sabotages — ALL caught:** drop axis / hardcode / ignore flag /
  drop the Ramone gate / fork the detection.
- **Required-field judgment ENDORSED:** every producer JSON must state its loop
  philosophy explicitly — `timbaland.json` will declare it in writing.
- **Evolution floors are threshold GATES only:** spreads appear in zero
  arithmetic — no `_dynamic_mix` re-derivation.
- **★ Doctrine finding (see the section above):** the status→score map lives in
  the profile JSON — even the polarity is profile-authored; the engine
  contributes DETECTION only. "The strongest possible form of the doctrine,
  not a leak."
- **Codex NOT available — single-model review.**

---

## Residue (deferred / follow-ups / risks)

1. **Liveness-docstring-overclaim family now spans SIX files:** add
   `tests/test_loop_context.py:566-570` to the standing note
   (`test_beat_identity.py`, `test_negative_space.py`,
   `test_rhythmic_surprise.py`, `test_low_end_motion.py`, + CHECK
   `test_groove_coherence.py`). Fold ONE docstring sweep into a future
   doctrine-touching packet.
2. **NEW ride-alongs:** (a) the gate keys on the literal kind
   `"loop_deconstruct"` (`creative.py:232`) — if promotion kinds generalize,
   move the gating into the table row; (b) the `dominant_unassessed` docstring
   is slightly loose (per-metric, not per-section); (c) `read_loop_context`
   shares the defensive None-value edge family.
3. **Retained:** all prior carry-forwards — the shared-mutable-groove-dict note
   (P-032b), the P-032e `spectral_flatness` docstring drift, the
   `_DEFAULT_PROFILE` no-aliasing carry-forward (P-032h loads a second
   profile), the P-032d non-adjacent-swing defensive note, lem's 84-point
   ceiling + `r.get("metrics",{})` edge (P-032c).
4. **Honest deferrals from this packet:** cultural/recognizability iconic-ness
   (provenance/manifest); per-loop bar-level variation; onset-sequence needs —
   test-guarded out of evidence.
5. **★ P-032f staging notes (USER-GATED — do NOT open without explicit user
   go).** The orchestrator must present to the USER, for explicit go BEFORE any
   building:
   - **(a) The aesthetic rule:** masking of a chopped/stuttered/adlib vocal or
     background stack is ACCEPTABLE-BLEND (context-dependent) — this flips
     masking from fault to accepted for a whole vocal class.
   - **(b) The conservative default:** when `vocal_type` is UNCERTAIN,
     protect-as-lead (never "percussion, masking ok").
   - **(c) The blast radius:** new `vocal_type_classifier.py` (NOT in-place
     edits to `role_classifier.py`), additive record field; interacts with 3
     live scorers (`_ramone` / `_vocal_centrality` / `_static_mix`); caps at
     `hook_candidate` (no recurrence signal at doctrine time).
   - The reusable P-032g gate pattern (profile-decided creative gate on a
     shared detection basis) applies.
6. **Resequenced remaining order (recorded in memory):** e ✓ → a ✓ → b ✓ →
   d ✓ → c ✓ → **g ✓** → **P-032f (vocal-role — ★ USER-GATED, next)** →
   [fold P-031 confidence] → P-032h (author `timbaland.json`) → P-032i
   (differential proof). P-030 orthogonal/last.

---

## Open boundaries (pending explicit go)

- **No merge / no push handled here.** P-032g's commits `835e907` + `e9e804d`
  are local on the dev branch; the orchestrator owns the build-os close commit
  + push. **Merge base to default is still `e79426a` = PR #16 — NOT merged.**
  No deploy, no secrets touched.
- **P-032f is ★ USER-GATED** — must NOT open without the user's explicit go on
  the "masked chop/stack = acceptable-blend" aesthetic rule + the
  protect-as-lead-when-uncertain conservative default (see Residue item 5).

---

## ★ Milestone

**The engine now carries 13 component axes** (7 original + `beat_identity` +
`negative_space` + `groove_coherence` + `rhythmic_surprise` + `low_end_motion`
+ `loop_context`). **6 of the 7 Timbaland "weight up" axes have now landed.**
This packet is THE HINGE — the doctrine-pin exemplar realized end-to-end: the
engine detects agnostically, the profile decides, and even the axis's polarity
lives in profile JSON. **The reusable pattern is established: a
profile-decided creative gate on a shared detection basis (P-032f / P-032h
will reuse it).** Dual-green including the USER-MANDATED dual byte-identity
surface — the recommendation engine is proven byte-identical under
Halee/Ramone defaults before `timbaland.json` turns the interpretation on.
