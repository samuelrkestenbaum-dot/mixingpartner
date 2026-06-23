# Logic Action Checklist

> **Non-destructive only.** Duplicate tracks / save presets before changes. No source audio is overwritten. Approve creative or source-level moves before applying.

**Preferred order of operations:** automation → level and panning → depth placement → subtractive EQ → compression → additive EQ → saturation / excitement → last-resort enhancement.

## Lead Vocal

*heard element in the intimate layer. Low-mid mud is elevated.*

- **Depth:** intimate · **Role:** heard
- **Reverb / send:** Short room or slapback only, very low send (~-24 dB). Keep it close.

1. **Channel EQ** — High-pass ~80 Hz. Cut ~250 Hz by 1-2 dB (mud). Avoid large 12 kHz+ air boosts (keeps the vocal human, not glossy).
   - _Why:_ Clean low-end build-up and keep believable presence without hype.
   - _Risk:_ Class 2 (reversible mix recommendation)
2. **Compressor** — Vintage Opto, target 2-3 dB gain reduction, slow-ish attack.
   - _Why:_ Stabilise the vocal while preserving the performance (invisible compression).
   - _Risk:_ Class 2 (reversible mix recommendation)
3. **Automation**
   - gain (clip gain + fader): Ride phrase endings +0.5 to +1 dB where the lyric drops, before adding compression.
     _Why:_ Ramone-style vocal belief: performance rides before brute-force compression.

## Acoustic Guitar

*heard element in the foreground layer. Low-mid mud is elevated.*

- **Depth:** foreground · **Role:** heard
- **Reverb / send:** Short chamber, low send (~-18 dB).

1. **Channel EQ** — Cut 250-400 Hz by 1-2 dB.
   - _Why:_ Reduce low-mid mud build-up.
   - _Risk:_ Class 2 (reversible mix recommendation)

## Electric Guitar 1

*heard element in the foreground layer. Low-mid mud is elevated.*

- **Depth:** foreground · **Role:** heard
- **Reverb / send:** Short chamber, low send (~-18 dB).

1. **Channel EQ** — Cut 250-400 Hz by 1-2 dB.
   - _Why:_ Reduce low-mid mud build-up.
   - _Risk:_ Class 2 (reversible mix recommendation)

## Electric Guitar 2

*heard element in the foreground layer. Low-mid mud is elevated.*

- **Depth:** foreground · **Role:** heard
- **Reverb / send:** Short chamber, low send (~-18 dB).

1. **Channel EQ** — Cut 250-400 Hz by 1-2 dB.
   - _Why:_ Reduce low-mid mud build-up.
   - _Risk:_ Class 2 (reversible mix recommendation)

## Synth Pad

*felt element in the background layer. Low-mid mud is elevated.*

- **Depth:** background · **Role:** felt
- **Reverb / send:** Hall or long plate, higher send (~-10 dB), filtered and diffuse.

1. **Channel EQ** — High-pass ~250 Hz; low-pass the top if it is purely atmospheric.
   - _Why:_ Filter felt elements so they support without crowding.
   - _Risk:_ Class 2 (reversible mix recommendation)
2. **Automation**
   - filter cutoff / send: Open the filter and lift the reverb send only in chorus sections; pull back in verses.
     _Why:_ Use the element as movement (felt), not a constant heard layer.

## Splice Texture Loop

*felt element in the background layer. Wider than a felt element should be.*

- **Depth:** background · **Role:** felt
- **Reverb / send:** Hall or long plate, higher send (~-10 dB), filtered and diffuse.

1. **Direction Mixer** — Narrow stereo width to ~35-50%.
   - _Why:_ Felt/atmospheric element should not occupy the same width as heard elements.
   - _Risk:_ Class 3 (reversible Logic action requiring approval)
2. **Channel EQ** — High-pass ~250 Hz; low-pass the top if it is purely atmospheric.
   - _Why:_ Filter felt elements so they support without crowding.
   - _Risk:_ Class 2 (reversible mix recommendation)
3. **(arrangement)** — Consider chopping into transition gestures and muting the continuous bed; reserve for pre-chorus/bridge.
   - _Why:_ Re-contextualise the imported loop instead of running it as a finished record inside the record.
   - _Risk:_ Class 4 (source-level creative change requiring explicit approval)
4. **Automation**
   - filter cutoff / send: Open the filter and lift the reverb send only in chorus sections; pull back in verses.
     _Why:_ Use the element as movement (felt), not a constant heard layer.
- ⚠️ Imported loop: do not let it dominate the song identity. Non-destructive duplicate before chopping.

## Bass

*structural element in the foreground layer.*

- **Depth:** foreground · **Role:** structural
- **Reverb / send:** Short chamber, low send (~-18 dB).

1. **Channel EQ** — High-pass ~30 Hz; control 200-350 Hz if boxy.
   - _Why:_ Tighten the low end without thinning the body.
   - _Risk:_ Class 2 (reversible mix recommendation)
2. **Compressor** — Vintage Opto, gentle 2-4 dB GR for consistent sustain.
   - _Why:_ Even out the low-end foundation.
   - _Risk:_ Class 2 (reversible mix recommendation)
3. **Channel EQ** — Carve a small dip where the kick thumps (complementary to kick).
   - _Why:_ Resolve kick/bass low-end conflict by carving, not stacking.
   - _Risk:_ Class 2 (reversible mix recommendation)

## Kick

*structural element in the foreground layer.*

- **Depth:** foreground · **Role:** structural
- **Reverb / send:** Short chamber, low send (~-18 dB).

1. **Channel EQ** — Shape sub (~50-70 Hz) vs beater (~3-5 kHz); leave room for bass.
   - _Why:_ Define the kick without masking the bass.
   - _Risk:_ Class 2 (reversible mix recommendation)

## Snare

*structural element in the foreground layer.*

- **Depth:** foreground · **Role:** structural
- **Reverb / send:** Short chamber, low send (~-18 dB).

1. **Channel EQ** — Light tonal shaping only; preserve transient detail and room realism.
   - _Why:_ Halee naturalism: keep the kit believable.
   - _Risk:_ Class 2 (reversible mix recommendation)

## Mute / Chop Candidates

_Subtraction often helps more than addition. Non-destructive (duplicate first)._

- **Electric Guitar 2** (section `verse_1`) — Width crowding in 'verse_1': reserve the widest placement for one element; push or mute the rest. _Risk: Class 3._

## Source-Material Warnings

- **Synth Pad**: Printed instrument bounce: note/patch/envelope changes require re-rendering from the original MIDI, not audio editing.
- **Splice Texture Loop**: Imported loop/sample: verify it is not accepted at full width in the foreground by default. Re-contextualise into the song's depth and tone.
- **Splice Texture Loop**: Stereo image is wide; consider narrowing and placing it in the midground/background rather than full-width foreground.
- **Splice Texture Loop**: Low crest factor suggests the loop is pre-compressed/mastered; it may make live tracks feel small next to it.
