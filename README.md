# mixingpartner

This repository contains **Logic Mix OS** — a local-first, CLI-first mix
decision system that turns Logic Pro stems into a Roy Halee / Phil Ramone-inspired,
section-aware, Logic-native mix plan.

➡️ See [`logic-mix-os/`](logic-mix-os/) for the project, docs, and usage.

```bash
cd logic-mix-os
pip install -e ".[full,dev]"
python fixtures/generate_fixtures.py
logic-mix-os analyze \
  --stems fixtures/dense_chorus_with_loops/stems \
  --manifest fixtures/dense_chorus_with_loops/project_manifest.json \
  --out ./output/dense
```
