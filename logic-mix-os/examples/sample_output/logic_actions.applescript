-- Logic Mix OS — generated AppleScript SCAFFOLDING (does not run automatically).
-- Logic Pro exposes limited AppleScript; UI steps go via System Events / a
-- control surface. Review every step. No source audio is modified.
tell application "Logic Pro" to activate


-- ===== Track: Lead Vocal =====
-- TODO(System Events): select track "Lead Vocal"
-- Set send for "Lead Vocal": Short room or slapback only, very low send (~-24 dB). Keep it close.
-- Insert "Channel EQ" on "Lead Vocal"
--   settings: High-pass ~80 Hz. Cut ~250 Hz by 1-2 dB (mud). Avoid large 12 kHz+ air boosts (keeps the vocal human, not glossy).
--   reason:   Clean low-end build-up and keep believable presence without hype.  (risk class 2)
-- Insert "Compressor" on "Lead Vocal"
--   settings: Vintage Opto, target 2-3 dB gain reduction, slow-ish attack.
--   reason:   Stabilise the vocal while preserving the performance (invisible compression).  (risk class 2)
-- Automate gain (clip gain + fader) on "Lead Vocal": Ride phrase endings +0.5 to +1 dB where the lyric drops, before adding compression.

-- ===== Track: Acoustic Guitar =====
-- TODO(System Events): select track "Acoustic Guitar"
-- Set send for "Acoustic Guitar": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Acoustic Guitar"
--   settings: Cut 250-400 Hz by 1-2 dB.
--   reason:   Reduce low-mid mud build-up.  (risk class 2)

-- ===== Track: Electric Guitar 1 =====
-- TODO(System Events): select track "Electric Guitar 1"
-- Set send for "Electric Guitar 1": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Electric Guitar 1"
--   settings: Cut 250-400 Hz by 1-2 dB.
--   reason:   Reduce low-mid mud build-up.  (risk class 2)

-- ===== Track: Electric Guitar 2 =====
-- TODO(System Events): select track "Electric Guitar 2"
-- Set send for "Electric Guitar 2": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Electric Guitar 2"
--   settings: Cut 250-400 Hz by 1-2 dB.
--   reason:   Reduce low-mid mud build-up.  (risk class 2)

-- ===== Track: Synth Pad =====
-- TODO(System Events): select track "Synth Pad"
-- Set send for "Synth Pad": Hall or long plate, higher send (~-10 dB), filtered and diffuse.
-- Insert "Channel EQ" on "Synth Pad"
--   settings: High-pass ~250 Hz; low-pass the top if it is purely atmospheric.
--   reason:   Filter felt elements so they support without crowding.  (risk class 2)
-- Automate filter cutoff / send on "Synth Pad": Open the filter and lift the reverb send only in chorus sections; pull back in verses.

-- ===== Track: Splice Texture Loop =====
-- TODO(System Events): select track "Splice Texture Loop"
-- Set send for "Splice Texture Loop": Hall or long plate, higher send (~-10 dB), filtered and diffuse.
-- Insert "Direction Mixer" on "Splice Texture Loop"
--   settings: Narrow stereo width to ~35-50%.
--   reason:   Felt/atmospheric element should not occupy the same width as heard elements.  (risk class 3)
-- Insert "Channel EQ" on "Splice Texture Loop"
--   settings: High-pass ~250 Hz; low-pass the top if it is purely atmospheric.
--   reason:   Filter felt elements so they support without crowding.  (risk class 2)
-- Arrangement (manual): Consider chopping into transition gestures and muting the continuous bed; reserve for pre-chorus/bridge.
-- Automate filter cutoff / send on "Splice Texture Loop": Open the filter and lift the reverb send only in chorus sections; pull back in verses.

-- ===== Track: Bass =====
-- TODO(System Events): select track "Bass"
-- Set send for "Bass": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Bass"
--   settings: High-pass ~30 Hz; control 200-350 Hz if boxy.
--   reason:   Tighten the low end without thinning the body.  (risk class 2)
-- Insert "Compressor" on "Bass"
--   settings: Vintage Opto, gentle 2-4 dB GR for consistent sustain.
--   reason:   Even out the low-end foundation.  (risk class 2)
-- Insert "Channel EQ" on "Bass"
--   settings: Carve a small dip where the kick thumps (complementary to kick).
--   reason:   Resolve kick/bass low-end conflict by carving, not stacking.  (risk class 2)

-- ===== Track: Kick =====
-- TODO(System Events): select track "Kick"
-- Set send for "Kick": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Kick"
--   settings: Shape sub (~50-70 Hz) vs beater (~3-5 kHz); leave room for bass.
--   reason:   Define the kick without masking the bass.  (risk class 2)

-- ===== Track: Snare =====
-- TODO(System Events): select track "Snare"
-- Set send for "Snare": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Snare"
--   settings: Light tonal shaping only; preserve transient detail and room realism.
--   reason:   Halee naturalism: keep the kit believable.  (risk class 2)

-- End of scaffolding. Apply manually or via the Cowork UI bridge.
