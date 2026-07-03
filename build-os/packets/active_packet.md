# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** NONE ACTIVE — **P-042 CLOSED** (2026-07-03). qa GREEN +
  reviewer PASS (no must-fix; all EIGHT user-mandated adversarial attacks
  defeated). Receipt: `build-os/receipts/P-042-mode-forking.md`.

## Last closed — P-042: Profile-Authored Mode Forking (Shape B)

- **The user's go (verbatim, 2026-07-03):** "My call: B — Profile-authored
  mode forking. That is the right next skate." A rejected as the final
  shape; C rejected for that packet and STAGED (below).
- **What landed:** `generate_variants` READS the active mode and forks
  candidate generation via profile-authored `search_modes` declarations —
  `suppress_kinds` = candidate-SET fork, `favor_kinds` = order-only reach,
  absent = byte-identical neutral; loader validation (incl. the over-cap
  "cannot be out-authored" ValueError) + runtime fail-closed cap; non-empty
  `suppression_fallback` surfaced honestly; every mode of all three
  producers explicitly authored (all DEFAULT/intimate modes
  authored-neutral → defaults byte-identical); the requirement-10 artifact
  surface. Doctrine: **engine owns move vocabulary / profile owns mode
  reach / governance owns safety cap.** The P-033 "thin lever" calibration
  note is ✓ RESOLVED.
- **Commits:** `9acecfd` (Commit-1 — the seam; GREEN IN ISOLATION at 894)
  + `9d746e3` (Commit-2 — timbaland + quincy declarations, the three-way
  mode differential, the requirement-10 surface) on parent `ab4914a`
  (active-packet confirmation), atop merge base `dadda12` (= the PR #20
  merge — P-041 landed first). Exactly 9 files, +1069/−27.
- **Proof:** suite 873 → **907** / regression **93/93** / Commit-1 iso
  **894** / 12 default-flow runs byte-identical / the 90-cell attribution
  reconstruction 0 mismatches / sabotage 4/4 bites / safety grep 0 real
  hits. Reviewer PASS, single-model (Codex unavailable), own executed
  probes.
- **Push state:** PUSHED to the dev branch
  `claude/logic-mix-os-hardening-12-7hbeh1` BEFORE qa/reviewer under the
  orchestrator's standing go (both gates validated the final SHAs).
  **NOT merged.**

## ★★ OPEN USER GATE

- **The merge of P-042** — `ab4914a` + `9acecfd` + `9d746e3` (+ the close
  commit) atop `dadda12` (= PR #20) — awaits the user's explicit word.
  Never merge/deploy/publish without go.

## STAGED next (per the USER — not active until the user opens it)

- **Shape C — new mode-specific move families:** extend
  `CREATIVE_VARIANT_KINDS` + the curated variant builders through a
  conscious packet (e.g. the true arrangement-lift / ensemble-rebalance
  families the quincy-experimental approximation motivates); profiles then
  author reach over the widened vocabulary with **zero loader/fork
  changes** (B proved the seam). ★ USER-GATED: do NOT open blind — the
  orchestrator presents scope first (which families, their curated
  score/risk rows, drift discipline for the sample trees, the differential
  proof shape).

---
_Cleared by the archivist at P-042 close (2026-07-03). One packet at a
time: builder → qa + reviewer → archivist → receipt._
