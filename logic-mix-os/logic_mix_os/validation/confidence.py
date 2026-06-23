"""Confidence + evidence tagging (build packet section 37).

Keeps the system honest: every claim can declare whether it is measured,
inferred, subjective, comparative, doctrine-based, or user-intent-based.
"""

from __future__ import annotations

from typing import Dict, List

from ..constants import EVIDENCE_TYPES


def tag_claim(claim: str, confidence: float, evidence_type: List[str], evidence: List[str]) -> Dict:
    bad = [e for e in evidence_type if e not in EVIDENCE_TYPES]
    if bad:
        raise ValueError(f"Unknown evidence types: {bad}. Allowed: {EVIDENCE_TYPES}")
    return {
        "claim": claim,
        "confidence": round(float(max(0.0, min(1.0, confidence))), 2),
        "evidence_type": evidence_type,
        "evidence": evidence,
    }
