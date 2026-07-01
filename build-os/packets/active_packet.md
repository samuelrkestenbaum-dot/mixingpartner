# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — P-032g closed by the archivist (2026-07-01).
  **P-032f is STAGED below but is ★ USER-GATED — it must NOT be confirmed
  active until the user's explicit go on the aesthetic rule + the conservative
  default (see the staged spec).**

## Last-closed

- **P-032g — `loop_context` + `protect_iconic_loops` — THE HINGE. ✓ CLOSED** —
  qa **GREEN**, reviewer **PASS (no must-fix)** — **dual-green including the
  USER-MANDATED dual byte-identity surface** (doctrine: 0 mismatches × 3
  fixtures, overalls 73.8 / 70.7 / 74.3; creative: full `result.creative`
  sorted-key JSON base vs HEAD → EMPTY diff, `cmp` byte-identical). The SIXTH
  new producer-agnostic doctrine axis (the 13th component) + the FIRST
  profile-decided creative gate. The doctrine-pin exemplar realized: the
  engine DETECTS agnostically (static = dominant + no evolution; iconic =
  dominant + groove/fingerprint function — an acoustic proxy; cultural
  recognizability deferred), the profile DECIDES (`protect_iconic_loops`, a
  REQUIRED field; halee_ramone=false = current behavior). ★ Reviewer's
  doctrine finding: the status→score map (iconic 90 / evolving 60 / neutral
  50 / unassessed 45 / static 15) lives IN THE PROFILE JSON — even the axis's
  POLARITY is profile-authored; "the strongest possible form of the doctrine,
  not a leak." **13 component axes; 6 of the 7 Timbaland weight-up axes
  landed; the reusable profile-decided-gate pattern established
  (P-032f/P-032h will reuse it).** Two commits `835e907` (Commit-1 green in
  isolation: 499 + 68/68 in a real worktree check) + `e9e804d`; suite
  473 → 512 (+39); regression 68/68, 0 warnings. Local-only, NOT merged
  (merge base still `e79426a` = PR #16). Receipt:
  `build-os/receipts/P-032g-loop-context-hinge.md`.

## Staged next packet (★ USER-GATED — NOT active)

- **Packet id:** P-032f
- **Title:** vocal-role refinement (`vocal_type`) — HIGH risk, the LAST of the
  seven Timbaland weight-up axes.
- **★★ USER GATE (BINDING — must clear BEFORE any building):** the
  orchestrator must present to the USER for explicit go:
  1. **The aesthetic rule** — masking of a chopped/stuttered/adlib vocal or
     background stack is ACCEPTABLE-BLEND (context-dependent); this flips
     masking from fault to accepted for a whole vocal class.
  2. **The conservative default** — when `vocal_type` is UNCERTAIN,
     protect-as-lead (never "percussion, masking ok").
  3. **The blast radius** — new `vocal_type_classifier.py` (NOT in-place edits
     to `role_classifier.py`), an additive record field; interacts with 3 live
     scorers (`_ramone` / `_vocal_centrality` / `_static_mix`); caps at
     `hook_candidate` (no recurrence signal at doctrine time).
  **Do NOT confirm this packet active until the user's explicit go on the
  aesthetic rule (1) and the default (2).**
- **Scoping cautions (from the read-only scoping workflow + P-032g):** the
  reusable P-032g pattern applies — a profile-decided gate on a shared
  detection basis. Established proof idiom: byte-identical (independent
  capture) + distinctness + liveness/sabotage + no-aliasing + honest-scope;
  run `fixtures/generate_fixtures.py` first; ≤2 commits, Commit-1 green in
  isolation; full suite green from the **512** baseline; regression 68/68.

## Epic arc (Timbaland sub-arc P-032.x — RESEQUENCED)

**P-032e ✓ → P-032a ✓ → P-032b ✓ → P-032d ✓ → P-032c ✓ → P-032g ✓ (THE HINGE,
closed) → P-032f (vocal-role — ★ USER-GATED, staged) →** **[fold P-031
confidence here]** → P-032h (author `timbaland.json`) → P-032i (differential
proof). P-030 (rename dims) orthogonal/last.

---
_Cleared by the archivist on P-032g close (2026-07-01). One packet at a time.
The orchestrator confirms the staged packet (P-032f only after the user's
explicit go on the aesthetic rule + the conservative default); the builder
implements exactly it; qa proves; reviewer judges; archivist closes with a
receipt._
