# Mix Verdict

**Producer profile:** Quincy Jones (quincy_jones)

> **Emotional truth:** A groove built from voices: the lead sings while chopped and stacked vocals lock into the beat.

## Overall Diagnosis

Overall mix readiness 68.2/100. Static balance 80.0/100; dynamic movement 28.2/100. The mix is more balanced than it is alive — invest in section contrast and rides, not more EQ.

## Scores

| Dimension | Score | |
|---|---|---|
| Overall mix readiness | 68.2/100 | `██████████████░░░░░░` |
| Physical space / depth | 81.3/100 | `████████████████░░░░` |
| Emotional hierarchy / vocal belief | 86.0/100 | `█████████████████░░░` |
| Vocal centrality | 90.0/100 | `██████████████████░░` |
| Depth hierarchy | 72.0/100 | `██████████████░░░░░░` |
| Section contrast | 82/100 | `████████████████░░░░` |
| Static mix | 80.0/100 | `████████████████░░░░` |
| Dynamic mix | 28.2/100 | `██████░░░░░░░░░░░░░░` |

**The physical-space test:** Can the listener visualize musicians in a real physical space?  
**The emotional-hierarchy test:** Do I believe every word the singer is saying?

## Confidence

_Per-area trust labels from the producer profile: which parts of this judgment carry what strength, and why._

**High**

- ensemble depth and layering interpretation (depth hierarchy) — hand-curated from documented Quincy Jones technique — big-band and orchestral arranging practice from the Basie/Sinatra-era chairs and his own published writing on arranging: the ensemble sits in named layers around the lead; this axis is live and weighted above both existing profiles as this profile's center of gravity
- sectional architecture and arranged-lift interpretation (section contrast, dynamic movement) — hand-curated from documented Quincy Jones technique — the sectional builds documented across the Off the Wall/Thriller-era production literature: parts enter and exit so each section lifts the record; these axes are live and weighted above both existing profiles
- vocal prominence inside the ensemble (vocal centrality, emotional hierarchy) — hand-curated from documented Quincy Jones technique — the serve-the-song, leave-space-for-the-singer ethos documented in his autobiography Q and in producer interviews: the lead stays prominent inside an arranged ensemble, so these axes sit deliberately between the two existing poles
- groove as support (beat identity, groove coherence, rhythmic surprise, low-end motion as retained measurement) — hand-curated from documented Quincy Jones technique — the rhythm section holds the floor for the song rather than centering the record's identity; these axes stay live at deliberately moderated weights below the groove-first profile: support, never dominance
- space and balance hygiene as retained measurement (physical space, negative space, static balance) — hand-curated from documented Quincy Jones technique — space is kept where it reveals an arrangement role (leave space for the singer), not composed as silence; these axes stay live at moderate weight
- loop context interpretation (static vs iconic) — hand-curated from documented Quincy Jones production philosophy — an arrangement-led practice, not a loop-based one: a static dominant loop reads as arrested arrangement (authored 12.0), and even an iconic-functioning loop reads as material for the arrangement rather than the record's identity (authored 85.0, protect_iconic_loops: false); the status-to-score polarity is authored in this profile while every detection floor stays on the shared basis

**Limited**

- vocal blend interpretation — the opt-in is authored from documented technique — Bruce Swedien's stacked background-vocal ensembles in the documented Jones/Swedien engineering partnership (the Acusonic recording process: a prominent lead atop an arranged vocal ensemble) — and the gate is live and measured on real exported-stem data: a qualified vocal chop and stack under masking read 85.0 on vocal_role_fit against the reference's 65.0 at this profile's authored 0.8 confidence floor; the level stays limited because coverage is bounded: events arise only from the masker-instrument set, info-tier events are emitted but not consumed, and vocal-band events carry no per-track masking risk
- textural coherence as its own measurement — the opt-in is authored from documented Quincy Jones technique — big-band and orchestral arranging keeps the ensemble's texture beds sharing one coherent surface (the section timbres blend into a single arranged voice rather than reading as a pile of unrelated layers), and it ships as a pure cross-bed dispersion statistic over the engine's texture-bed set (band_energy L1 spread + brightness, stereo_width and crest_factor stdev on the exported stems); the level stays limited, NOT high, because this reading is a SECONDARY support-tier concern that runs partly counter to this profile's center of gravity — the distinct, readable ensemble layer (depth_hierarchy weighted 1.4, above this axis's authored 0.6): the arrangement keeps every part in its own readable place first, so the one-woven-surface framing is a support reading, never the arrangement-led practice's engine

**Deferred**

- harmonic and instrumental conversation (voicing, counterlines, call-and-response) — voicing and counterline interplay are central to the documented arranging practice yet not measurable on exported stems at doctrine time — the engine carries no harmonic analysis; the depth and section axes are the closest shipped proxies
- cultural loop recognizability — iconic-ness as cultural recognition needs provenance/manifest signals not measurable on exported stems at doctrine time; the acoustic loop-context proxy is what ships
- true hook recurrence — a proven hook needs a recurrence signal that does not exist at doctrine time; the strongest claim ships as vocal_hook_candidate
- motif provenance — motif lineage across sources is not measurable on exported stems at doctrine time
- onset-timing strong forms (fingerprint typing, fills/unexpected-hit detection, kick/sub temporal interlock) — these need per-onset timing and typing signals not measurable on exported stems at doctrine time; the section-aggregate weak forms are what ship
- per-section true-sub movement — section analysis exposes low_mid_energy (120-500 Hz) only, so the true-sub band (20-120 Hz) is not measurable at section grain on exported stems; the low_mid section grain is what ships

## Biggest Risks

- Chorus 1 may not lift enough relative to the previous section (only +1.4 dB and -0.03 width). Target roughly +3 to +5 dB and +0.05 to +0.10 width via supporting elements and automation, not master level.
- Dynamic movement is weak (28.2/100).

## Best Opportunities

- Create real section contrast with automation (bloom/intimacy) instead of master level.

## Top Recommended Moves

1. **Vocal belief** — Ride the lead vocal phrase-by-phrase before adding compression.
2. **Section contrast** — Chorus 1 do not lift enough. Create lift through supporting elements and automation (bloom on entry, intimacy in verses), not master level.
3. **Depth cleanup** — Too many elements occupy the foreground. Move supporting guitars/keys/pads to the midground instead of EQ-ing everything.

## Production vs. Mix Boundaries

- **Chorus 1 does not lift but is already dense** → `arrangement_problem`. Density increases without an increase in space/width; adding more will not create lift. _Best fix:_ Create contrast by subtraction before the section, then bloom space at entry.

## Negative Constraints (what this must NOT become)

- Do not bury the lead vocal.
- Do not let the chopped vocals lose their rhythmic identity.
