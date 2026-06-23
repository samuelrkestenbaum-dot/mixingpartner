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

-- ===== Track: Piano =====
-- TODO(System Events): select track "Piano"
-- Set send for "Piano": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Piano"
--   settings: Cut 250-400 Hz by 1-2 dB.
--   reason:   Reduce low-mid mud build-up.  (risk class 2)

-- ===== Track: Bass =====
-- TODO(System Events): select track "Bass"
-- Set send for "Bass": Short chamber, low send (~-18 dB).
-- Insert "Channel EQ" on "Bass"
--   settings: High-pass ~30 Hz; control 200-350 Hz if boxy.
--   reason:   Tighten the low end without thinning the body.  (risk class 2)
-- Insert "Compressor" on "Bass"
--   settings: Vintage Opto, gentle 2-4 dB GR for consistent sustain.
--   reason:   Even out the low-end foundation.  (risk class 2)

-- End of scaffolding. Apply manually or via the Cowork UI bridge.
