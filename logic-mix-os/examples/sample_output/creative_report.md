# Creative Experimentation

**Search mode:** `dramatic_contrast` — push verse/chorus/bridge contrast harder

## Static vs. Dynamic

- Static mix: 72.0/100
- Dynamic mix: 23.4/100
- Stop EQ-ing the static mix. Build dynamic movement: pre-chorus narrowing, chorus bloom, final-chorus width release, vocal phrase rides.

_Scoring evidence for this song: contrast_deficit 0.92, overcrowding 0.64, masking_pressure 0.33, vocal_risk 0.00, loop_pressure 0.50, width_room 0.26 (lean: neutral)._

## Variant Branches

### Chorus does not lift enough emotionally.

| Variant | Kind | Overall | Vocal belief | Contrast | Translation | Why (top signal) | Verdict |
|---|---|---|---|---|---|---|---|
| Width Bloom | `width_bloom` | 77.4 | 63.5 | 99.9 | high | contrast_deficit=0.92 | worth testing — check vocal wash |
| Subtractive Drop | `subtractive_drop` | 96.8 | 88.7 | 96.9 | low | overcrowding=0.64 | promising |
| Vocal-Ride Lift | `vocal_ride` | 92.0 | 92.0 | 70 | low | vocal_risk=0.0 | promising |
| Drum Room Bloom | `drum_room_bloom` | 90.7 | 69.6 | 89.3 | low | contrast_deficit=0.92 | promising — check vocal wash |

**Top-scored:** chorus_lift_B — 'Subtractive Drop' scored 96.8 (promising); best fit for this song's evidence (driven by overcrowding=0.64).

Keep moves:
- Mute decorative texture in the final pre-chorus bar

### Arrangement is crowded; hierarchy is unclear.

| Variant | Kind | Overall | Vocal belief | Contrast | Translation | Why (top signal) | Verdict |
|---|---|---|---|---|---|---|---|
| Depth Cleanup | `depth_cleanup` | 89.9 | 90.6 | 75.9 | low | overcrowding=0.64 | promising |
| Subtractive Simplify | `subtractive_drop` | 94.1 | 88.7 | 96.9 | low | overcrowding=0.64 | promising |

**Top-scored:** density_B — 'Subtractive Simplify' scored 94.1 (promising); best fit for this song's evidence (driven by overcrowding=0.64).

Keep moves:
- Mute/duplicate-then-remove a redundant midrange layer

### An imported loop behaves like a finished record inside the record.

| Variant | Kind | Overall | Vocal belief | Contrast | Translation | Why (top signal) | Verdict |
|---|---|---|---|---|---|---|---|
| Loop Deconstruct | `loop_deconstruct` | 88.1 | 88.0 | 78 | low | loop_pressure=0.5 | promising |
| Loop as Accent | `subtractive_drop` | 92.7 | 88.7 | 96.9 | low | overcrowding=0.64 | promising |

**Top-scored:** loop_B — 'Loop as Accent' scored 92.7 (promising); best fit for this song's evidence (driven by overcrowding=0.64).

Keep moves:
- Turn Splice Texture Loop into one-shot accents
- Use only at section transitions

### Too many elements occupy the foreground.

| Variant | Kind | Overall | Vocal belief | Contrast | Translation | Why (top signal) | Verdict |
|---|---|---|---|---|---|---|---|
| Depth Cleanup | `depth_cleanup` | 89.9 | 90.6 | 75.9 | low | overcrowding=0.64 | promising |

**Top-scored:** depth_A — 'Depth Cleanup' scored 89.9 (promising); best fit for this song's evidence (driven by overcrowding=0.64).

Keep moves:
- Move felt/decorative elements to midground/background
- Keep vocal + hook forward

### Vocal could feel more believable and present.

| Variant | Kind | Overall | Vocal belief | Contrast | Translation | Why (top signal) | Verdict |
|---|---|---|---|---|---|---|---|
| Phrase Rides | `vocal_ride` | 82.9 | 92.0 | 70 | low | vocal_risk=0.0 | promising |
| Verse Intimacy | `intimacy_pass` | 82.1 | 94.0 | 72 | low | static_dynamic_gap=1.0 | promising |

**Top-scored:** vocal_A — 'Phrase Rides' scored 82.9 (promising); best fit for this song's evidence (driven by vocal_risk=0.0).

Keep moves:
- Clip gain + fader rides on phrase ends +0.5 to +1.5 dB

## Guardrails

- Always preserve a static baseline.
- Never destructively alter source tracks.
- Never judge creative variants only by loudness.
- Never let novelty override vocal belief.
- Always compare creative variants to the song's emotional truth.

> A mix is not finished when it is balanced. It is finished when the static balance supports the song and the dynamic movement makes the song feel inevitable. The best mix is the version where the song feels most inevitable, not the most processed.
