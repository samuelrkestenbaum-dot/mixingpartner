# Source-Aware Audit

_Different Logic objects afford different fixes; recommendations are source-specific._

## Lead Vocal  ·  `live_track` (comped_audio_track)

- Preserve the human feel; integrate with shared room/depth rather than flattening dynamics.

_Preferred moves:_ clip gain before compression, phrase-level rides, light tuning only where distraction occurs, preserve transient character, use room/depth to integrate the performance

## Acoustic Guitar  ·  `live_track` (live_audio_recording)

- Inconsistent phrase energy: use clip gain + phrase rides before compression (do not compress harder).
- Preserve the human feel; integrate with shared room/depth rather than flattening dynamics.

_Preferred moves:_ clip gain before compression, phrase-level rides, light tuning only where distraction occurs, preserve transient character, use room/depth to integrate the performance

## Electric Guitar 1  ·  `live_track` (live_audio_recording)

- Inconsistent phrase energy: use clip gain + phrase rides before compression (do not compress harder).
- Preserve the human feel; integrate with shared room/depth rather than flattening dynamics.

_Preferred moves:_ clip gain before compression, phrase-level rides, light tuning only where distraction occurs, preserve transient character, use room/depth to integrate the performance

## Electric Guitar 2  ·  `live_track` (live_audio_recording)

- Inconsistent phrase energy: use clip gain + phrase rides before compression (do not compress harder).
- Preserve the human feel; integrate with shared room/depth rather than flattening dynamics.

_Preferred moves:_ clip gain before compression, phrase-level rides, light tuning only where distraction occurs, preserve transient character, use room/depth to integrate the performance

## Synth Pad  ·  `synth_patch` (synth_bounce)

**Red flags:** printed bounce — MIDI-level changes need a re-render

- High-pass the pad (~150-250 Hz); it is a felt element and is clouding the low-mids.
- This is a software-instrument bounce: note/patch/envelope changes require re-rendering from the MIDI, then print to audio for validation.

_Preferred moves:_ automate filter cutoff by section, shorten release if it clouds transitions, narrow width if it competes with guitars/vocals, high-pass pads when they are felt elements, move pads to background, use modulation for motion instead of adding parts

## Splice Texture Loop  ·  `sample_loop` (splice_sample)

**Red flags:** full-width loop, loop is brighter than the vocal, mastered/compressed loop tone

- Narrow to ~35%, high-pass ~250 Hz, push to background except at transitions.
- This loop is acting like a finished record inside your record. Chop into transition gestures and re-contextualise into the song's depth, tone, and groove.

_Preferred moves:_ narrow stereo width, filter lows or highs, chop into smaller gestures, use only at transitions, push into background depth layer, sidechain subtly to vocal or kick if needed, re-pitch or formant-shift if key/tone mismatches, replace with simpler one-shot if loop dominates

## Bass  ·  `live_track` (live_audio_recording)

- Preserve the human feel; integrate with shared room/depth rather than flattening dynamics.

_Preferred moves:_ clip gain before compression, phrase-level rides, light tuning only where distraction occurs, preserve transient character, use room/depth to integrate the performance

## Kick  ·  `live_track` (live_audio_recording)

- Inconsistent phrase energy: use clip gain + phrase rides before compression (do not compress harder).
- Preserve the human feel; integrate with shared room/depth rather than flattening dynamics.

_Preferred moves:_ clip gain before compression, phrase-level rides, light tuning only where distraction occurs, preserve transient character, use room/depth to integrate the performance

## Snare  ·  `live_track` (live_audio_recording)

- Inconsistent phrase energy: use clip gain + phrase rides before compression (do not compress harder).
- Preserve the human feel; integrate with shared room/depth rather than flattening dynamics.

_Preferred moves:_ clip gain before compression, phrase-level rides, light tuning only where distraction occurs, preserve transient character, use room/depth to integrate the performance
