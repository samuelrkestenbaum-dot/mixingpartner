"""Vocal-type classifier — *what FUNCTION is this vocal serving?* (P-032f)

The LAST of the seven producer-agnostic axes' detection layers: the engine
DETECTS vocal function OBSERVATIONALLY from per-stem physics already on the
pipeline record; a producer PROFILE decides what the reading is worth (the
masking philosophy lives in profile JSON, never here). This module is pure,
deterministic and producer-agnostic: same record in, same reading out — no
profile, no I/O, no randomness.

It classifies VOCAL stems only (``instrument_identity`` of ``lead_vocal`` /
``backing_vocal``, i.e. the ``vocal`` identity family) into exactly one of
``VOCAL_TYPES``:

  * ``vocal_lead`` — the lead vocal. IDENTITY WINS: a stem the identity
    detector called ``lead_vocal`` is ALWAYS ``vocal_lead``, whatever its
    physics look like. A lead whose physics read percussive (a chopped comp,
    a stuttered ad-lib print on the lead track) is still the lead — the
    classifier never demotes it, so a misread can never strip lead
    protection (misclassification fails CLOSED toward vocal protection).
  * ``vocal_percussive`` — a chop/stutter/ad-lib read: transient-DENSE
    (chops and stutters punch), with a defined non-smeared envelope
    (``crest_factor_db``), corroborated by a chop/loop ``source_kind``.
  * ``vocal_stack`` — a background-stack read: WIDE (a multi-part stack
    occupies the stereo field), SUSTAINED (low transient density — stacks
    sing, they do not punch), corroborated by the ``backing_vocal``
    identity. Identity is one corroborating signal, never the gate.
  * ``vocal_hook_candidate`` — a non-lead vocal PLACED to be heard: forward
    layer, heard/structural role, real presence-band energy, and NOT
    transient-dense (a hook sings; a stutter chops). THE HONESTY CAP: this
    is the STRONGEST hook claim the classifier can ever make. A PROVEN hook
    needs a recurrence/provenance signal (the same phrase returning across
    sections) and NO recurrence signal exists at doctrine time — so a
    proven-hook type is deliberately absent from ``VOCAL_TYPES``, deferred,
    never faked.
  * ``vocal_uncertain`` — the FAIL-CLOSED reading: signals too weak (no
    candidate clears ``MIN_STRENGTH``) or genuinely conflicting (two
    candidate readings tie). Uncertain is protected AS THE LEAD downstream
    and is categorically ineligible for any blend treatment, whatever
    confidence number rides along with it.

Every reading carries a ``confidence`` in [0, 1]: the supporting-signal
fraction of the winning candidate, capped at ``CONFIDENCE_CAP`` (never
certain — these are exported-stem heuristics, and saying 1.0 would be a
lie). For ``vocal_uncertain`` the number is the strength of the STRONGEST
competing reading, reported for transparency only — uncertain stays
categorically protected regardless of it.

NON-VOCAL STEMS: the classifier returns ``None`` and the pipeline writes
EXPLICIT ``None`` into both record fields (``vocal_type`` /
``vocal_type_confidence``) — the keys are always present, so a consumer can
distinguish "not a vocal" (None) from "field missing" (an assembly error).

DEFERRED, NOT FAKED — real signals that are NOT measurable at doctrine time
and are never claimed:
  1. Hook RECURRENCE / provenance (does the phrase return?) — needs a
     cross-section phrase/onset sequence; hence the ``vocal_hook_candidate``
     cap above.
  2. LYRIC MEANING (is this line the title? the emotional payload?) — needs
     lyric alignment at the phrase level, not stem physics.
  3. PER-ONSET STUTTER RATE (the actual chop grid) — needs onset timing,
     which is post-doctrine groove-analyzer territory; transient DENSITY is
     the honest section-grain proxy used instead.
"""

from __future__ import annotations

from typing import Dict, Optional

from ..constants import LOOP_SAMPLE_KINDS

# The complete vocal-function vocabulary. NOTE the honesty cap: there is no
# proven-hook type — ``vocal_hook_candidate`` is the ceiling (see module doc).
VOCAL_TYPES = (
    "vocal_lead",
    "vocal_hook_candidate",
    "vocal_percussive",
    "vocal_stack",
    "vocal_uncertain",
)

_VOCAL_IDENTITIES = {"lead_vocal", "backing_vocal"}
_FORWARD = {"intimate", "foreground"}
_HEARD = {"heard", "structural"}

# Producer-AGNOSTIC physics thresholds. These are MODULE constants, not
# profile JSON, deliberately: the vocal_type record fields are computed once
# per record in the pipeline BEFORE any producer profile applies, so every
# profile reads the SAME detection basis (the P-032g shared-basis rule) —
# profiles author what to DO with the reading, never the reading itself.
LEAD_CONFIDENCE = 0.95        # identity-backed lead read (identity wins)
CONFIDENCE_CAP = 0.95         # never certain on exported-stem heuristics
MIN_STRENGTH = 0.6            # below this the reading fails closed to uncertain
PERC_TRANSIENT_FLOOR = 0.55   # chops/stutters are transient-dense
PERC_CREST_DB = 12.0          # defined, non-smeared hits
STACK_WIDTH_FLOOR = 0.5       # a multi-part stack occupies the stereo field
STACK_TRANSIENT_CEILING = 0.35  # stacks sustain; they do not punch
HOOK_PRESENCE_FLOOR = 0.15    # a hook candidate carries real presence energy


def is_vocal_record(record: Dict) -> bool:
    """True when the record is vocal material: the ``vocal`` identity family
    (today: ``lead_vocal`` / ``backing_vocal``)."""
    return (
        record.get("identity_family") == "vocal"
        or record.get("instrument_identity") in _VOCAL_IDENTITIES
    )


def classify_vocal_type(record: Dict) -> Optional[Dict]:
    """Read one pipeline record's vocal FUNCTION. Pure and deterministic.

    Returns ``{"vocal_type": <one of VOCAL_TYPES>, "confidence": float}`` for
    a vocal stem, ``None`` for a non-vocal stem (the pipeline then writes
    explicit ``None`` fields — see the module doc). Never mutates ``record``.
    """
    if not is_vocal_record(record):
        return None

    # IDENTITY WINS for the lead: percussive-looking physics can never demote
    # the lead vocal (fail-closed toward vocal protection).
    if record.get("instrument_identity") == "lead_vocal":
        return {"vocal_type": "vocal_lead", "confidence": LEAD_CONFIDENCE}

    metrics = record.get("metrics", {}) or {}
    td = float(metrics.get("transient_density", 0.0) or 0.0)
    crest = float(metrics.get("crest_factor_db", 0.0) or 0.0)
    width = float(record.get("stereo_width", 0.0) or 0.0)
    presence = float(record.get("vocal_presence_energy", 0.0) or 0.0)
    chop_source = record.get("source_kind") in LOOP_SAMPLE_KINDS
    forward = record.get("depth_default") in _FORWARD
    heard = record.get("perceptual_role") in _HEARD

    # Candidate readings, each a tuple of independent supporting signals.
    # The hook candidate carries an explicit anti-chop signal (a hook sings;
    # a stutter chops), so a transient-dense forward chop cannot tie the
    # percussive read into uncertainty.
    signals = {
        "vocal_percussive": (
            td >= PERC_TRANSIENT_FLOOR,
            crest >= PERC_CREST_DB,
            chop_source,
        ),
        "vocal_stack": (
            width >= STACK_WIDTH_FLOOR,
            td <= STACK_TRANSIENT_CEILING,
            record.get("instrument_identity") == "backing_vocal",
        ),
        "vocal_hook_candidate": (
            forward,
            heard,
            presence >= HOOK_PRESENCE_FLOOR,
            td < PERC_TRANSIENT_FLOOR,
        ),
    }
    strengths = {t: sum(s) / len(s) for t, s in signals.items()}
    ordered = sorted(strengths.items(), key=lambda kv: kv[1], reverse=True)
    best_type, best = ordered[0]
    runner_up = ordered[1][1]

    # FAIL CLOSED: weak evidence (under MIN_STRENGTH) or a genuine conflict
    # (the top two readings tie) is UNCERTAIN — never a guessed chop/stack.
    if best < MIN_STRENGTH or best == runner_up:
        return {
            "vocal_type": "vocal_uncertain",
            "confidence": round(min(best, CONFIDENCE_CAP), 3),
        }
    return {
        "vocal_type": best_type,
        "confidence": round(min(best, CONFIDENCE_CAP), 3),
    }


__all__ = [
    "VOCAL_TYPES",
    "classify_vocal_type",
    "is_vocal_record",
]
