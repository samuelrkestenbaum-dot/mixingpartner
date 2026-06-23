"""Logic Mix OS — a local-first mix decision system for Logic Pro stems.

The package is intentionally CLI-first and deterministic. Given a folder of
exported stems and a ``project_manifest.json`` it produces a Roy Halee /
Phil Ramone-inspired, section-aware mix plan plus Logic-native action lists.

Nothing here touches the network, uploads audio, or writes to the original
audio files. Outputs are deterministic JSON + Markdown artifacts.
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
