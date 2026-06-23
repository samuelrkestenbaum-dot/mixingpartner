"""Logic bridge (build packet sections 41-42).

The execution layer. Per the build-priority rule, the product is the decision
system; the bridge only *proposes, previews, logs, and validates* — it never
blindly alters a Logic session. On this platform it is strictly dry-run:
it exports actions and generates AppleScript / Shortcuts scaffolding, but
executes nothing and writes to no audio.

Execution modes (section 41.1):
- A: direct file/audio processing (analysis, reports, preview renders)
- B: Logic-guided checklist (human / Cowork executes)
- C: UI automation (AppleScript / Shortcuts / accessibility) — scaffolding only
- D: custom Audio Unit helper plugin (see au_helper_plugin_spec.md)
"""

from .exporter import export_actions
from .executor import EXECUTION_MODES, dry_run

__all__ = ["export_actions", "dry_run", "EXECUTION_MODES"]
