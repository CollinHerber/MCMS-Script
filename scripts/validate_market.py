#!/usr/bin/env python3
"""Validate marketplace JSON files without third-party dependencies."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MARKET_FILES = (ROOT / "market.json", ROOT / "market-v2.json", ROOT / "templates.json")


def walk(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")
    else:
        yield path, value


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for file_path in MARKET_FILES:
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{file_path.name}: invalid JSON: {error}")
            continue

        for json_path, value in walk(data):
            if not isinstance(value, str):
                continue
            if json_path.endswith(".image") and value.startswith("http://"):
                errors.append(f"{file_path.name}:{json_path}: insecure image URL: {value}")
            if (
                file_path.name == "market-v2.json"
                and json_path.endswith(".image")
                and "mcsmanager.oss-cn-guangzhou.aliyuncs.com" in value
            ):
                errors.append(f"{file_path.name}:{json_path}: inaccessible image host: {value}")
            if "githubyumao/" in value:
                warnings.append(f"{file_path.name}:{json_path}: upstream runtime image: {value}")

    for warning in sorted(set(warnings)):
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    print(
        f"Validated {len(MARKET_FILES)} marketplace files: "
        f"{len(errors)} error(s), {len(set(warnings))} upstream-image reference(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
