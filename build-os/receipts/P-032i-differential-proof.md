# Receipt — P-032i: the Timbaland-vs-Halee/Ramone DIFFERENTIAL PROOF (the sub-arc's formal close)

- **Packet:** P-032i — the Timbaland-vs-Halee/Ramone DIFFERENTIAL PROOF: a
  permanent, binding 21-test suite (`tests/test_differential_proof.py`)
  formalizing the sub-arc's five obligations. **The sub-arc's formal close.**
- **Date closed:** 2026-07-02
- **Branch:** `claude/logic-mix-os-hardening-12-7hbeh1`; packet base = parent
  `b884a59` (active-packet confirmation), atop `40eb94d` (P-032h close).
  Merge base for landing decisions unchanged: `e79426a` (PR #16 — nothing
  since P-025 has been merged).
- **Verdict:** qa **GREEN**; reviewer **PASS (no must-fix)**. **Codex NOT
  available — single-model review.**

## ★★★ SUB-ARC COMPLETION

**The Timbaland sub-arc is COMPLETE: P-032e ✓ → P-032a ✓ → P-032b ✓ →
P-032d ✓ → P-032c ✓ → P-032g ✓ → P-032f ✓ → P-031 ✓ → P-032h ✓ → P-032i ✓.
Ten packets.**

What was built across the arc:

- **Seven new producer-agnostic measurement axes** (14 doctrine components).
- **Two profile-decided gates** (loop protection, vocal blend) with
  engine-fixed safety rails.
- **The per-area honesty/confidence layer** (the required `confidence_map`).
- **The second live producer profile** (`timbaland.json`).
- **The permanent differential proof** (this packet).

The reference profile stayed **byte-identical throughout**
(73.8 / 70.7 / 74.3 on every surface, every packet). The user's architecture
doctrine held end-to-end: **axes are shared measurable substrate; taste is
the weighting layer; safety/governance is invariant.** The next producer
profile is now: a JSON file + three required declarations + its own
confidence map + a differential test.

## Scope

**In:**

- `tests/test_differential_proof.py` — 21 tests, 772 lines: the permanent,
  BINDING formalization of the five sub-arc obligations (a)–(e): coherent
  differential judgment/plan surfaces, full attributability, safety
  invariance, the binding negative expectations, and per-profile confidence
  rendering.

**Explicitly out:**

- **ZERO product code** — no engine, profile, analyzer, or config change.
  Exactly 1 NEW test file, 772+/0−.
- The two builder observations (verdict-filename producer-independence;
  residue re-confirmations) — reported NOT patched, per the mandated
  stop-and-report behavior.
- Everything in the post-sub-arc backlog (P-030 rename, the
  `_default_creative_mode` wiring packet, the analyzer-extension packet,
  the verdict-filename cosmetic packet, the standing sweeps).

## Commit (single, ≤2-commit contract met)

| Commit | Summary |
| --- | --- |
| `010734d` | P-032i: the Timbaland-vs-Halee/Ramone differential proof — the sub-arc's formal close. 1 NEW file: `tests/test_differential_proof.py` (21 tests), 772 insertions / 0 deletions; ZERO product code. Parent `b884a59`. **HEAD IS Commit-1 → green in isolation.** |

Push state at close: `010734d` local AND pushed to the dev branch. NOT merged
(merge base still `e79426a` = PR #16).

## The proof's headline facts (permanent)

- **THE PLAN REVERSAL (the iconic scenario):** reference winner `loop_A`
  **85.9** (chop / high-pass / narrow / push = DECONSTRUCT the loop) vs
  timbaland winner `loop_B` **86.7** (one-shot accents = KEEP the loop,
  punctuate around it); keep/reject lists are exact mirrors; BOTH plans
  coherent, schema-valid, non-destructive. (Loop-branch scores from each
  profile's own tables: 81.9/85.3 vs 80.7/86.7.)
- **Search modes:** `ramone_vocal_truth` vs `dramatic_contrast` on simple.
- **Attributability:** divergence == exactly **{overall, confidence}**
  (+`loop_context` on the loop fixtures); the overalls reconstruct from
  shared components + authored values.
- **Safety:** the 5 SAFETY switches **verbatim-pinned FILE-LOCALLY**,
  first-in-order under both profiles; masked-lead pressure holds under both;
  **zero class-5 anywhere.**
- **Negative pins with NAMED legitimizing packets:** no vocal-blend delta
  (→ the future analyzer-extension packet); no intimate-mode claim (→ the
  future `_default_creative_mode` wiring packet); next-pass identical (→ a
  future profile-aware planner).
- **Confidence:** the 8-entry vs 11-entry maps render per-profile; the
  deferred tails are verbatim-shared; zero cross-leak.

## QA proof (exact counts)

- **Suite:** 639 → **660 passed** (+21), 0 failed / skipped. **Regression:**
  **68/68** (0 critical / 0 warnings).
- **Commit-1 isolation:** single commit — HEAD IS Commit-1 → green in
  isolation.
- **Obligations (a)–(e) re-derived independently LIVE: 60/60 checks passed.**
- **Proof-liveness verified:** a SAFETY-switch reorder in a throwaway
  worktree → the verbatim pin FAILED — the guard bites.
- **Safety grep:** NONE (1 new test file, 772+/0−, zero product code).
- **UI smoke:** n/a (no UI surface in this packet — tests only).

## Reviewer verdict — PASS (no must-fix)

- **The tests BIND, not describe.** Strongest-form attributability
  re-verified BY HAND in plain Python: the reference components + the
  authored values ALONE reconstruct 68.4 / 52.6 / 49.7 exactly.
- **The anti-drift audit covers the FULL 18-key doctrine surface with exact
  set-equality** — a NEW divergence OR a VANISHED one both fail.
- **The file-local safety pin closes a REAL gap** (proven empirically by
  sabotage): rewording a safety switch FAILED the new pin while P-032h's
  module-referencing test PASSED.
- Legitimizing-change comments fact-checked to line numbers — the
  `dramatic_contrast` fallback KeyError risk confirmed real at
  creative.py:532.
- Pins judged **right-not-brittle**: established differential facts, mostly
  mirroring existing pins.
- **Codex NOT available — single-model review.**

## Builder conduct

Two observations reported NOT patched — the mandated stop-and-report
behavior:

1. The verdict-filename producer-independence (cosmetic).
2. Residue re-confirmations.

## Residue (carried to `build-os/memory/residue.md`)

- **NEW (reviewer note):** P-030's expected-touch list now ALSO includes
  `tests/test_differential_proof.py` (two producer JSONs + this test file).
- **NEW (cosmetic):** two truthiness asserts in the new file
  (`v["risk"] and v["validation"]`; `0 <= len(nxt)`) — tighten
  opportunistically.
- **NEW (cosmetic):** the `tim_analyzed` fixture duplicates
  `test_timbaland_profile`'s module fixture (~3 extra analyses per full run)
  — promote to a session conftest fixture only if a third consumer appears.
- The sub-arc residue block is marked **✓ COMPLETE**; all standing
  carry-forwards move to the **post-sub-arc backlog**.

## Open boundaries

- **★★ THE STANDING DECISION NOW OPEN — the next user-gated boundary:** the
  ENTIRE EPIC (P-025 → P-032i + P-031, everything since `e79426a` = PR #16)
  sits on the dev branch, pushed, **awaiting the USER'S MERGE GO.** Nothing
  merges/deploys without it.
- No deploy/publish surface in play.

## Next (orthogonal backlog — staged-not-active, no order dependency)

- **P-030** — rename the halee/ramone dims (now touches TWO producer JSONs +
  `tests/test_differential_proof.py`).
- **The `_default_creative_mode` wiring packet** (P-016-family;
  byte-identical for the reference; must fix the dramatic_contrast-fallback
  KeyError risk).
- **The analyzer-extension packet** (non-lead vocal-band events → makes
  vocal blend live on real data; also fix creative.py:98 name-matching).
- **The verdict-filename cosmetic packet.**
- **The standing residue sweeps** (liveness-docstrings across ~8 files;
  validation tightening; NaN-floor guard; etc.).
