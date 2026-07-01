# Cowork Contract (raw CLI)

This is the human orientation for integrating **Claude Cowork** with Logic Mix
OS through the raw CLI. The **machine-readable source of truth** is the
`describe_contract` command — this document points at it rather than restating
every command by hand.

## Invocation

```
python -m logic_mix_os.cli cowork --name <command> --params '<json>'
python -m logic_mix_os.cli cowork --list          # flat catalog of every command
```

Every command returns a single JSON document on stdout. `--params` is a JSON
object unpacked straight into the command's keyword arguments.

## Stability guarantee

- **Versioned.** `describe_contract` reports an `api_version` (currently `"1.0"`).
  Pin it. MAJOR bumps on any breaking change to a command's params, its
  `side_effect`, or its removal; MINOR bumps on additive commands.
- **Deterministic, JSON out.** Introspection commands are pure: same input, same
  bytes. Every command's output is JSON-serializable.
- **Self-describing — do not reverse-engineer.** Two introspection commands are
  the source of truth:
  - **`describe_contract`** — the full contract: `api_version`, the `invocation`
    pattern, and per command `{purpose, phase, params, side_effect}`. `params`
    is derived from the real handler signature (via `inspect.signature`), so it
    cannot drift from the code. `side_effect` is an honest, declared
    classification (see below).
  - **`describe_session`** — the canonical ordered, phase-grouped view of the
    same registry (the end-to-end session flow).

## side_effect classification (live vs dead)

Every command declares one of a closed vocabulary. This pins the **live-vs-dead**
distinction as a first-class contract fact:

| `side_effect`          | Meaning                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| `none`                 | Read-only projection over one analysis. No writes, no mutation.     |
| `writes:history(live)` | Appends to the **live** mix-pass history that feeds the next-pass planner (`record_mix_pass`). |
| `writes:taste(live)`   | Records **live** taste feedback that shapes governance (`update_taste_calibration`). |
| `writes:ledger(dead)`  | Appends to the **dead** decision ledger — an audit log, not a live planner input (`write_mix_decision`). |
| `mutates:session`      | Mutates in-session state only; no disk write (`override_track_identity`). |

Exactly four commands are non-`none`; everything else is `none`.

## Product guarantees

- **Local.** All persistence is plain JSON under a memory directory. No database,
  no network, no DAW automation.
- **Non-destructive.** Nothing here edits your Logic project. Writes are additive
  (history, ledger, taste); the checklist is a human-executable export.
- **Plan-only (v1).** The system produces analysis, plans, and checklists — a
  human (or a later version) applies them. It recommends; it does not act.
- **Evidence + confidence + risk-class.** Recommendations carry the evidence
  behind them, a confidence, and a risk class.
- **Class-5 is never recommended.** The highest-risk class is surfaced for
  awareness only — the system will not recommend a Class-5 move.

## Canonical session flow

`describe_session` returns these eight phases in order (plus an `auxiliary`
bucket for off-axis commands):

1. **intake** — load the project; learn what each track is and how it can be manipulated.
2. **classify** — fix instrument identity; assign musical / perceptual / sacredness roles.
3. **diagnose** — analyse sections, depth, masking, and per-source audits.
4. **plan** — generate the mix plan, automation, reference delta, scores, mute candidates.
5. **checklist** — export the plan as a Logic-native, human-executable checklist.
6. **validate** — check the pass against stop conditions and taste-protection governance.
7. **record-outcome** — record the decision, the pass outcome (live), and taste feedback.
8. **next-pass** — read the history-informed next pass to start the next iteration.

For the full, current command list with params and side effects, call
`describe_contract` — it is generated from the code and cannot go stale.
