# Helper Audio Unit Spec (build packet section 42)

Mode D of the Logic bridge. Where Logic cannot expose enough data to the
decision system, a small Audio Unit (AUv3) helper sits on a track or bus and
reports measurements back to Logic Mix OS. These are **measurement / metering**
tools — they do not alter audio.

This document is a build spec, not an implementation (an AU must be compiled on
macOS with the AudioToolbox / CoreAudio SDKs).

## Tools

### Mix Probe
Per-insert metering, reports: LUFS, true peak, RMS, crest factor, spectral
balance (5 bands), stereo width, phase correlation, transient density,
sibilance, masking estimate, reverb energy.

### Room Send Auditor
Reports the wet/dry ratio and decay character feeding each shared reverb bus, so
the depth field can be validated against the depth-layer plan.

### Vocal Masking Detector
Sidechains the lead vocal against a bus and reports presence-band (1.5-4 kHz)
overlap in real time, distinguishing bad masking from acceptable blend by the
depth/role model.

### Stereo Loop Auditor
Flags full-width foreground loops, side-heavy low end (<250 Hz), mastered/
compressed sample tone, conflicting reverb space, and repetition fatigue.

### Depth Layer Meter
Shows how many elements occupy intimate / foreground / midground / background
per section, surfacing overcrowding.

### Reference Delta Meter
Continuously compares the bus against a loaded reference profile: loudness,
width, brightness, low-end shape, vocal-to-band ratio.

## Data contract

Each tool emits JSON frames matching the existing schemas (e.g. the Mix Probe
emits the `track_analysis` metric block) so the deterministic decision system
can consume them with no new parsing.

## Safety

Helper AUs are read-only metering. They never write audio, never alter the
session, and never auto-apply changes. All execution remains gated by the review
modes and kill-switches in the bridge.
