#!/usr/bin/env python3
"""Downloads each listed APK and checks its size and SHA-256 against the entry.

Usage: scripts/check-apks.py build/catalog.json

Catches a dead link or a changed file before it reaches a TV. Portal checks the same things at install time, so this
is a courtesy to authors and reviewers. It does not check the signer: use `apksigner verify --print-certs` for that.
"""
import hashlib
import json
import sys
import urllib.request

catalog = json.load(open(sys.argv[1], encoding="utf-8"))
failed = False
for e in catalog.get("extensions", []):
    for v in e.get("versions", []):
        label = f"{e['package']} {v.get('version_name', v.get('version_code'))}"
        try:
            req = urllib.request.Request(v["apk"], headers={"User-Agent": "portaltv-extensions-ci"})
            h, n = hashlib.sha256(), 0
            with urllib.request.urlopen(req, timeout=60) as r:
                while chunk := r.read(1 << 20):
                    h.update(chunk)
                    n += len(chunk)
                    if n > v["size"] + (1 << 20):
                        break
            if n != v["size"]:
                print(f"FAIL {label}: size is {n}, the entry says {v['size']}")
                failed = True
            elif h.hexdigest() != v["sha256"].lower():
                print(f"FAIL {label}: SHA-256 is {h.hexdigest()}, the entry says {v['sha256']}")
                failed = True
            else:
                print(f"ok   {label}")
        except Exception as ex:  # a dead link, a timeout, a bad entry
            print(f"FAIL {label}: {ex}")
            failed = True
sys.exit(1 if failed else 0)
