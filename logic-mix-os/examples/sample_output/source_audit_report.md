# Source-Aware Audit

_Different Logic objects afford different fixes; recommendations are source-specific._

## Lead Vocal  ·  `live_track` (comped_audio_track)

- Keep the vocal as the emotional centre — phrase rides before heavier compression.

_Preferred moves:_ clip gain before compression, phrase-level rides, light tuning only where it distracts, de-ess surgically, integrate with shared room/depth

## Acoustic Guitar  ·  `live_track` (live_audio_recording)

- Cut 250-400 Hz low-mid build-up.
- Set source tone and depth before processing; preserve pick/strum transients with light leveling, not heavy compression.

_Preferred moves:_ set source tone first, control noise/handling, light leveling (not heavy compression), preserve pick/strum transients, place with depth

## Electric Guitar 1  ·  `live_track` (live_audio_recording)

- Cut 250-400 Hz low-mid build-up.
- Set source tone and depth before processing; preserve pick/strum transients with light leveling, not heavy compression.

_Preferred moves:_ set source tone first, control noise/handling, light leveling (not heavy compression), preserve pick/strum transients, place with depth

## Electric Guitar 2  ·  `live_track` (live_audio_recording)

- Cut 250-400 Hz low-mid build-up.
- Set source tone and depth before processing; preserve pick/strum transients with light leveling, not heavy compression.

_Preferred moves:_ set source tone first, control noise/handling, light leveling (not heavy compression), preserve pick/strum transients, place with depth

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

- Even out low-end sustain with gentle optical compression (consistency, not pumping).
- Carve complementary low-end space against the kick rather than stacking at the same frequency.

_Preferred moves:_ gentle optical leveling for consistent sustain, complementary EQ vs the kick, source-tone shaping, preserve note definition

## Kick  ·  `live_track` (live_audio_recording)

- Define sub vs beater (~50-70 Hz vs 2-5 kHz); check kick/overhead phase; leave headroom for the bass.
- Use bus/parallel compression for punch instead of squashing the transients.

_Preferred moves:_ transient shaping, overhead/room balance, phase & bleed checks, tuning/ring control, bus/parallel compression for punch, preserve transient detail

## Snare  ·  `live_track` (live_audio_recording)

- Control ring/tuning and balance top vs bottom; check the snare's phase in the overheads.
- Use bus/parallel compression for punch instead of squashing the transients.

_Preferred moves:_ transient shaping, overhead/room balance, phase & bleed checks, tuning/ring control, bus/parallel compression for punch, preserve transient detail
