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

-- ===== Track: BGV Chop =====
-- TODO(System Events): select track "BGV Chop"
-- Set send for "BGV Chop": Shared plate/chamber, moderate send (~-14 dB).
-- Insert "Channel EQ" on "BGV Chop"
--   settings: Cut 250-400 Hz by 1-2 dB.
--   reason:   Reduce low-mid mud build-up.  (risk class 2)

-- ===== Track: Backing Vocals Stack =====
-- TODO(System Events): select track "Backing Vocals Stack"
-- Set send for "Backing Vocals Stack": Shared plate/chamber, moderate send (~-14 dB).
-- Insert "Channel EQ" on "Backing Vocals Stack"
--   settings: Cut 250-400 Hz by 1-2 dB.
--   reason:   Reduce low-mid mud build-up.  (risk class 2)

-- ===== Track: Electric Guitar =====
-- TODO(System Events): select track "Electric Guitar"
-- Set send for "Electric Guitar": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Electric Guitar"
--   settings: Light shaping; high-pass below the instrument's body.
--   reason:   Make room without thinning.  (risk class 2)

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
--   reason:   Naturalistic space: keep the kit believable.  (risk class 2)

-- End of scaffolding. Apply manually or via the Cowork UI bridge.
