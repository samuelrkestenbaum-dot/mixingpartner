"""Mono compatibility + phase analyzer (build packet section 31)."""

from __future__ import annotations

from typing import Dict, List, Optional


def analyze_mono(records: List[Dict], mix_metrics: Optional[Dict]) -> Dict:
    events: List[Dict] = []

    for r in records:
        m = r.get("metrics", {})
        loss = m.get("mono_collapse_loss_db", 0.0)
        corr = m.get("phase_correlation", 1.0)
        width = r.get("stereo_width", 0.0)

        if loss < -4 and width > 0.4:
            events.append({
                "track": r["name"],
                "issue": f"Side-heavy content collapses in mono ({loss:.1f} dB level change).",
                "phase_correlation": corr,
                "severity": "high" if loss < -8 else "moderate",
                "recommendation": "Narrow to ~50%, reduce side energy below 500 Hz, and check a mono bounce.",
            })
        elif corr < 0.2 and width > 0.3:
            events.append({
                "track": r["name"],
                "issue": f"Low L/R correlation ({corr:.2f}) risks partial cancellation in mono.",
                "phase_correlation": corr,
                "severity": "moderate",
                "recommendation": "Check polarity/timing between channels; consider mid-side control.",
            })

    mix_loss = mix_metrics.get("mono_collapse_loss_db", 0.0) if mix_metrics else 0.0
    mix_corr = mix_metrics.get("phase_correlation", 1.0) if mix_metrics else 1.0

    score = 100.0
    score -= sum(8 if e["severity"] == "high" else 4 for e in events)
    if mix_loss < -3:
        score -= min(20, abs(mix_loss) * 2)
    score = max(0.0, round(score, 1))

    return {
        "mix_mono_collapse_loss_db": mix_loss,
        "mix_phase_correlation": mix_corr,
        "events": events,
        "mono_score": score,
        "summary": {
            "tracks_at_risk": len(events),
            "high_severity": sum(1 for e in events if e["severity"] == "high"),
        },
    }
