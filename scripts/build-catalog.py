#!/usr/bin/env python3
"""Builds catalog.json from entries/*.json and revoked.json.

Usage: scripts/build-catalog.py [output]    (default: build/catalog.json)

Each entries/<package>.json holds one extension entry (see Portal's docs/CATALOG.md). The file name must be the
entry's package name plus .json, so a package can't be listed twice. The output has no serial, updated or expires:
the maintainer stamps and signs it with Portal's scripts/CatalogSign.java before publishing.
"""
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "build" / "catalog.json"

problems = []
extensions = []
for f in sorted((root / "entries").glob("*.json")):
    try:
        entry = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        problems.append(f"{f.name}: not valid JSON ({e})")
        continue
    if not isinstance(entry, dict):
        problems.append(f"{f.name}: must hold one JSON object")
        continue
    if entry.get("package") is None or f.name != f"{entry['package']}.json":
        problems.append(f"{f.name}: the file name must be <package>.json, and the entry needs a package")
        continue
    extensions.append(entry)

revoked = []
rf = root / "revoked.json"
if rf.exists():
    try:
        revoked = json.loads(rf.read_text(encoding="utf-8"))
        if not isinstance(revoked, list):
            problems.append("revoked.json: must be a JSON list")
            revoked = []
    except ValueError as e:
        problems.append(f"revoked.json: not valid JSON ({e})")

if problems:
    print("\n".join(problems), file=sys.stderr)
    sys.exit(1)

extensions.sort(key=lambda e: e["package"])
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(
    json.dumps({"format": 1, "extensions": extensions, "revoked": revoked}, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(f"Wrote {out}: {len(extensions)} extension(s), {len(revoked)} revoked line(s)")
