# Track Identity Report

What each sound *is* (separate from what it is *doing*).

| Track | Identity | Family | Confidence | Alternates |
|---|---|---|---|---|
| Lead Vocal | `lead_vocal` | vocal | 0.70 | organ (0.17), pad (0.17) |
| BGV Chop | `backing_vocal` | vocal | 0.70 | lead_vocal (0.20), snare (0.19) |
| Backing Vocals Stack | `backing_vocal` | vocal | 0.70 | pad (0.25), strings (0.19) |
| Electric Guitar | `electric_guitar` | guitars | 0.70 | pad (0.22), backing_vocal (0.19) |
| Kick | `kick` | drums | 0.70 | bass_guitar (0.21), pad (0.13) |
| Snare | `snare` | drums | 0.70 | cymbal (0.27), hi_hat (0.19) |

### Evidence
- **Lead Vocal**: name clue: lead vocal; centroid 1416 Hz; dominant band: low_mid; sharp, percussive transients; centred / near-mono.
- **BGV Chop**: name clue: bgv; centroid 2324 Hz; dominant band: mid; sharp, percussive transients; centred / near-mono.
- **Backing Vocals Stack**: name clue: backing vocal; centroid 1226 Hz; dominant band: low_mid; slow attack / sustained, low transient density; wide stereo image.
- **Electric Guitar**: name clue: electric guitar; centroid 1210 Hz; dominant band: mid; moderate transient articulation; wide stereo image.
- **Kick**: name clue: kick; centroid 184 Hz; dominant band: low; slow attack / sustained, low transient density; centred / near-mono.
- **Snare**: name clue: snare; centroid 7879 Hz; dominant band: high; slow attack / sustained, low transient density; centred / near-mono.
