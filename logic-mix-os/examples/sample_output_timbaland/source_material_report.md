# Source Material Report

What kind of Logic object each track is, and what can actually be changed.

## Lead Vocal  `lead_vocal`

- **Source kind:** `comped_audio_track` (confidence 0.95)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** manifest_hint: comped_audio_track

## BGV Chop  `bgv_chop`

- **Source kind:** `one_shot_sample` (confidence 0.95)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade, stereo_width, pitch_shift, time_stretch, chop, reverse
- **Evidence:** manifest_hint: one_shot_sample
- ⚠️ Imported loop/sample: verify it is not accepted at full width in the foreground by default. Re-contextualise into the song's depth and tone.

## Backing Vocals Stack  `backing_vocals_stack`

- **Source kind:** `comped_audio_track` (confidence 0.95)
- **Editable:** gain, eq, dynamics, reverb_send, automation, region_editing, fade
- **Evidence:** manifest_hint: comped_audio_track

## Electric Guitar  `electric_guitar`

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
