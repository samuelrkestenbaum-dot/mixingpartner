# Source Material Report

What kind of Logic object each track is, and what can actually be changed.

## Lead Vocal  `lead_vocal`

- **Source kind:** `comped_audio_track` (confidence 0.95)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** manifest_hint: comped_audio_track

## Acoustic Guitar  `acoustic_guitar`

- **Source kind:** `live_audio_recording` (confidence 0.55)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** filename_clue: live-instrument name

## Electric Guitar 1  `electric_guitar_1`

- **Source kind:** `live_audio_recording` (confidence 0.55)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** filename_clue: live-instrument name

## Electric Guitar 2  `electric_guitar_2`

- **Source kind:** `live_audio_recording` (confidence 0.55)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** filename_clue: live-instrument name

## Synth Pad  `synth_pad`

- **Source kind:** `synth_bounce` (confidence 0.82)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade, stereo_width
- **Not directly editable:** midi_notes, velocity, synth_patch_parameters
- **Evidence:** filename_clue: synth
- ⚠️ Printed instrument bounce: note/patch/envelope changes require re-rendering from the original MIDI, not audio editing.

## Splice Texture Loop  `splice_texture_loop`

- **Source kind:** `splice_sample` (confidence 0.82)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade, stereo_width, pitch_shift, time_stretch, chop, reverse
- **Evidence:** filename_clue: splice
- ⚠️ Imported loop/sample: verify it is not accepted at full width in the foreground by default. Re-contextualise into the song's depth and tone.
- ⚠️ Stereo image is wide; consider narrowing and placing it in the midground/background rather than full-width foreground.
- ⚠️ Low crest factor suggests the loop is pre-compressed/mastered; it may make live tracks feel small next to it.

## Bass  `bass`

- **Source kind:** `live_audio_recording` (confidence 0.55)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** filename_clue: live-instrument name

## Kick  `kick`

- **Source kind:** `live_audio_recording` (confidence 0.55)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** filename_clue: live-instrument name

## Snare  `snare`

- **Source kind:** `live_audio_recording` (confidence 0.55)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** filename_clue: live-instrument name
