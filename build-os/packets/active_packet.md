# Active Packet

> The one packet currently in flight. The orchestrator reads this every session;
> the builder implements exactly this and nothing else; the archivist clears it
> on close. One packet at a time.

- **Status:** ACTIVE — P-030 confirmed by the orchestrator-in-chief on the
  USER'S EXPLICIT GO (2026-07-02): **Option A + memory.py dual-read + verdict
  filename fold-in.** Handed to builder.
- **Packet id:** P-030
- **Title:** the artifact-contract migration — rename the halee/ramone
  dimensions to producer-agnostic names; clean break for public artifacts;
  read-only compatibility for local persisted memory; neutral verdict filename.

## THE USER'S DECISION (verbatim, binding)

```
Clean break for public artifacts.
Compatibility only for local persisted memory.
No old-key aliases in emitted doctrine artifacts.
Fold the verdict filename rename into the same migration.
```

**The rename:**

```
halee_score  → physical_space_score
ramone_score → emotional_hierarchy_score
```

Also rename related internal/evidence keys so the artifact contract no longer
encodes the producer names (`baselines.halee` / `penalty_coeffs.ramone` /
evidence keys `"halee"`/`"ramone"` / the reference taste-triangle dims / etc.).
README-defined meaning: `physical_space_score` = the physical-space / depth /
spatial-realism model; `emotional_hierarchy_score` = the emotional hierarchy /
vocal-belief / narrative-priority model.

**Compatibility rule:** do NOT emit old aliases in new artifacts — no
`halee_score`/`ramone_score` compatibility keys in doctrine_score JSON,
renderers, schemas, Cowork responses, samples, or goldens. The ONLY carve-out:
**`memory.py` dual-reads old + new keys from persisted local mix-pass history**
(read-only compatibility for historical local data; memory.py never WRITES old
keys).

**Filename fold-in:** `halee_ramone_mix_verdict.md` → **`mix_verdict.md`**
(neutral; NOT per-producer filenames — the clean default is producer-agnostic).

## Required scope (every surface from the pin-site survey)

doctrine engine · creative scoring · mix_planner · memory.py · cli.py · all
renderers (markdown/operator_view/html_dashboard) · JSON schemas
(doctrine_score + mix_plan) · regression SCORE_KEYS allow-list · golden
snapshots (×3, consciously regenerated) · BOTH producer JSONs · evidence keys ·
internal profile keys (baselines/penalty_coeffs/taste-triangle dims) · tests
(~20 files) · committed samples (examples/sample_output) · the Cowork
doctrine_score dict surface · verdict filename references.

## Commit shape (user-specified, max 2)

- **Commit-1:** engine/profile/schema/renderer rename — product modules, both
  producer JSONs, schemas, renderers, Cowork response shape, the filename
  change, the memory.py dual-read.
- **Commit-2:** test pins, samples, and the CONSCIOUS golden regeneration —
  updated SCORE_KEYS, regenerated goldens (×3), updated sample outputs,
  updated tests, the explicit migration proof.
(Note: Commit-1 in isolation will NOT be fully green against unmodified tests —
that is inherent to a contract migration and must be stated honestly: report
what IS green at Commit-1 (product imports, the pipeline runs, new-key
artifacts emitted) and what necessarily waits for Commit-2 (test pins,
goldens). qa verifies the FINAL tree green and the Commit-1 boundary honestly.)

## Required tests (user-specified — all 17)

1. new doctrine_score artifacts use `physical_space_score`;
2. new doctrine_score artifacts use `emotional_hierarchy_score`;
3. new artifacts do NOT emit `halee_score`;
4. new artifacts do NOT emit `ramone_score`;
5. schemas require the new keys; 6. schemas do not require old keys;
7. Cowork surface returns new keys only;
8. renderers display producer-agnostic labels;
9. committed samples use new keys only;
10. goldens are consciously regenerated (and match live output);
11. regression SCORE_KEYS uses new keys;
12. memory.py reads new-key history; 13. memory.py reads old-key history;
14. memory.py prefers new keys when both present;
15. memory.py does not WRITE old keys;
16. verdict filename is `mix_verdict.md`;
17. no new `halee_ramone_mix_verdict.md` is written.

## Required grep proof (post-build)

Old strings (`halee_score`/`ramone_score`, plus `halee`/`ramone` as CONTRACT
keys) may remain ONLY in: migration/compat tests · memory.py dual-read code ·
explicit comments/docstrings explaining historical compatibility ·
changelog/receipt text. They must NOT remain in: new JSON artifacts · schemas
as active keys · renderers as active keys · the Cowork active response shape ·
samples · goldens · the active producer JSON contract · default artifact
filenames. (Display names like "Roy Halee / Phil Ramone" in the reference
profile's metadata/display_name and prose ARE fine — the PROFILE is named for
the producers; the CONTRACT keys are not.)

## Non-scope (user-specified)

No scoring-math changes. No weight changes. No Timbaland behavior changes. No
Halee/Ramone behavior changes beyond key names. No safety/governance changes.
No emitted-artifact aliases. No analyzer extension. No residue sweeps.

## The health bar (user-specified)

```
same math · same scores · same differential behavior ·
new producer-agnostic contract · old persisted memory still readable ·
new emitted artifacts clean
```

Scores must be NUMERICALLY IDENTICAL under both producers (73.8/70.7/74.3 ref;
68.4/52.6/49.7 tim) — only the KEY NAMES carrying them change. Regression must
be 68/68 against the REGENERATED goldens, and the regeneration must be proven
conscious (report the exact snapshot diff: key renames only, values identical).

## Required verification (before close)

test count · 68/68 vs regenerated goldens · conscious-regeneration proof
(values identical, keys renamed) · old-key grep summary · memory dual-read
proof · Cowork response-shape proof · filename proof · working tree status.

## Last-closed

- **P-033 ✓ CLOSED** — the creative-mode wire; producer lever complete
  end-to-end. Suite 678 / 68/68. Pushed, not merged (merge base `58d21dd` =
  PR #17).

## Epic arc (post-merge backlog)

**P-033 ✓ → P-030 (artifact-contract migration — ACTIVE) →** analyzer
extension (non-lead vocal-band events + creative.py:98 fix) → residue sweeps.
(The verdict-filename cosmetic is FOLDED INTO this packet.)

---
_Set active by the orchestrator-in-chief on the user's go (2026-07-02). One
packet at a time. Builder implements exactly this; qa proves; reviewer judges;
archivist closes with a receipt._
