"""Output validator.

Confirms a finished output directory contains every required artifact and that
each JSON validates against its schema. Uses ``jsonschema`` if installed,
otherwise a small built-in checker so the tool stays dependency-light.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

try:
    import jsonschema as _jsonschema  # type: ignore

    _HAVE_JSONSCHEMA = True
except Exception:  # pragma: no cover - exercised only without jsonschema
    _jsonschema = None
    _HAVE_JSONSCHEMA = False

_SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"

# output file -> schema file
JSON_OUTPUTS = {
    "source_material.json": "source_material.schema.json",
    "track_identity.json": "track_identity.schema.json",
    "track_analysis.json": "track_analysis.schema.json",
    "section_analysis.json": "section_analysis.schema.json",
    "depth_map.json": "depth_map.schema.json",
    "masking_report.json": "masking_report.schema.json",
    "mix_plan.json": "mix_plan.schema.json",
    "doctrine_score.json": "doctrine_score.schema.json",
}

MD_OUTPUTS = [
    "source_material_report.md",
    "track_identity_report.md",
    "halee_ramone_mix_verdict.md",
    "logic_action_checklist.md",
    "next_pass_recommendations.md",
]


def load_schema(schema_file: str) -> Dict:
    with open(_SCHEMA_DIR / schema_file, "r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_instance(instance, schema: Dict) -> List[str]:
    """Return a list of error strings ([] = valid)."""
    if _HAVE_JSONSCHEMA:
        validator = _jsonschema.Draft7Validator(schema)
        return [f"{list(e.path)}: {e.message}" for e in validator.iter_errors(instance)]
    return _lightweight_validate(instance, schema, path="$")


def validate_output(output_dir: str | Path) -> Dict:
    output_dir = Path(output_dir)
    files: List[Dict] = []
    errors: List[str] = []

    for name, schema_file in JSON_OUTPUTS.items():
        path = output_dir / name
        if not path.exists():
            errors.append(f"Missing required output: {name}")
            files.append({"file": name, "status": "missing"})
            continue
        try:
            with open(path, "r", encoding="utf-8") as fh:
                instance = json.load(fh)
        except Exception as exc:
            errors.append(f"{name}: invalid JSON ({exc})")
            files.append({"file": name, "status": "invalid_json"})
            continue
        schema = load_schema(schema_file)
        file_errors = validate_instance(instance, schema)
        if file_errors:
            errors.extend(f"{name}: {e}" for e in file_errors)
            files.append({"file": name, "status": "schema_error", "errors": file_errors})
        else:
            files.append({"file": name, "status": "ok"})

    for name in MD_OUTPUTS:
        path = output_dir / name
        if not path.exists() or path.stat().st_size == 0:
            errors.append(f"Missing or empty report: {name}")
            files.append({"file": name, "status": "missing"})
        else:
            files.append({"file": name, "status": "ok"})

    return {
        "ok": not errors,
        "validator": "jsonschema" if _HAVE_JSONSCHEMA else "builtin",
        "files": files,
        "errors": errors,
    }


# --------------------------------------------------------------------------- #
def _lightweight_validate(instance, schema: Dict, path: str) -> List[str]:
    errors: List[str] = []
    expected = schema.get("type")

    type_ok = {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "string": lambda v: isinstance(v, str),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "boolean": lambda v: isinstance(v, bool),
        "null": lambda v: v is None,
    }
    if expected:
        types = expected if isinstance(expected, list) else [expected]
        if not any(type_ok.get(t, lambda v: True)(instance) for t in types):
            errors.append(f"{path}: expected {expected}, got {type(instance).__name__}")
            return errors

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required property '{req}'")
        for key, subschema in schema.get("properties", {}).items():
            if key in instance:
                errors.extend(_lightweight_validate(instance[key], subschema, f"{path}.{key}"))
    elif isinstance(instance, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(instance):
                errors.extend(_lightweight_validate(item, item_schema, f"{path}[{i}]"))
    return errors
