#!/usr/bin/env python3
"""
Zenodo publisher for CAL-L4 (v0.4) — a single NEW deposit.

Mirrors publish_zenodo.py (used for CAL/L2/L3) but deposits ONLY L4, so re-running
this never touches the already-published CAL/L2/L3 records.

Security:
  - Reads `zenodo_token` from a .env file. The token is NEVER printed.
  - DRY-RUN by default. With --publish a draft is created + file uploaded but NOT
    published. With --publish --commit the DOI is minted (irreversible).

Usage:
  python publish_l4.py                    # dry-run, no network writes
  python publish_l4.py --publish          # create draft + upload, do NOT publish
  python publish_l4.py --publish --commit # publish (mints DOI, irreversible)
  # add --sandbox to test against sandbox.zenodo.org first
"""

import argparse
import json
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CAL_ROOT = HERE.parent  # .../CAL

# .env holding `zenodo_token`. CAL/.env is the durable home (gitignored); the legacy
# TCO/.env is kept as a fallback only while that checkout still exists. Checked in order.
ENV_CANDIDATES = [
    CAL_ROOT / ".env",
    Path("c:/Users/Usuario/Documents/Aural Syncro/TCO/.env"),
    CAL_ROOT / "L2" / ".env",
]

CAL_CONCEPT_DOI = "10.5281/zenodo.20430343"  # for reference only; L4 is a NEW deposit

DEPOSIT = {
    "key": "L4 v0.4",
    "metadata": HERE / "l4_v0.4.metadata.json",
    "file": CAL_ROOT / "L4" / "paper" / "CAL_L4_Paper_v0.1.md",
    "mode": "new",
}


def load_token():
    for p in ENV_CANDIDATES:
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() == "zenodo_token":
                tok = v.strip().strip('"').strip("'")
                if tok:
                    return tok, p
    return None, None


def api_base(sandbox):
    return "https://sandbox.zenodo.org/api" if sandbox else "https://zenodo.org/api"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true",
                    help="Create the draft + upload the file (still not published unless --commit).")
    ap.add_argument("--commit", action="store_true",
                    help="Publish the draft (mints the DOI, irreversible).")
    ap.add_argument("--sandbox", action="store_true",
                    help="Use sandbox.zenodo.org instead of production.")
    args = ap.parse_args()

    token, env_used = load_token()
    if not token:
        print("ERROR: could not find `zenodo_token` in any .env. Looked in:")
        for p in ENV_CANDIDATES:
            print(f"  - {p}")
        sys.exit(1)
    print(f"[ok] token loaded from {env_used}  (value never printed)")

    base = api_base(args.sandbox)
    params = {"access_token": token}
    headers = {"Content-Type": "application/json"}

    mode = "PUBLISH+COMMIT" if (args.publish and args.commit) else (
        "PUBLISH (draft only)" if args.publish else "DRY-RUN (no writes)")
    print(f"\n=== Zenodo target: {base} ===")
    print(f"=== Mode: {mode} ===\n")

    d = DEPOSIT
    assert d["metadata"].is_file(), f"missing metadata: {d['metadata']}"
    assert d["file"].is_file(), f"missing paper file: {d['file']}"
    meta = json.loads(d["metadata"].read_text(encoding="utf-8"))  # parse check
    print(f"[ok] {d['key']:8s} mode={d['mode']:4s} file={d['file'].name}")
    print(f"     title: {meta['metadata']['title'][:80]}")

    if not args.publish:
        print("\nDRY-RUN complete. Nothing was sent to Zenodo.")
        print("Next: review l4_v0.4.metadata.json, then run with --publish (draft) "
              "or --publish --commit (publish).")
        return

    # Verify token works against the chosen instance
    r = requests.get(f"{base}/deposit/depositions", params={**params, "size": 1}, timeout=30)
    if r.status_code == 401:
        print("ERROR: 401 Unauthorized — token rejected by this Zenodo instance.")
        print("       (production token? drop --sandbox; sandbox token? add it.)")
        sys.exit(1)
    r.raise_for_status()
    print("[ok] token authenticated against", base)

    # Create new deposit draft
    dep = requests.post(f"{base}/deposit/depositions", params=params,
                        json={}, headers=headers, timeout=30).json()
    dep_id = dep["id"]
    print(f"\n--- {d['key']} ---")
    print("  new deposit draft created")

    # Upload file (bucket API)
    bucket = dep["links"]["bucket"]
    fname = d["file"].name
    with open(d["file"], "rb") as fh:
        up = requests.put(f"{bucket}/{fname}", data=fh, params=params, timeout=120)
    up.raise_for_status()
    print(f"  uploaded {fname}")

    # Set metadata
    m = requests.put(f"{base}/deposit/depositions/{dep_id}",
                     params=params, json=meta, headers=headers, timeout=30)
    m.raise_for_status()
    print("  metadata set")
    html = m.json()["links"].get("html", "(see Zenodo)")

    if args.commit:
        pub = requests.post(f"{base}/deposit/depositions/{dep_id}/actions/publish",
                            params=params, timeout=30)
        pub.raise_for_status()
        doi = pub.json().get("doi", "(pending)")
        print(f"  PUBLISHED — DOI: {doi}")
        print(f"\n=== Done. L4 v0.4 DOI: {doi}  ({html}) ===")
    else:
        print(f"  draft ready (NOT published). Review: {html}")
        print(f"\n=== Draft created (dep#{dep_id}). Review in the Zenodo UI, then "
              f"re-run with --publish --commit. ===")


if __name__ == "__main__":
    main()
