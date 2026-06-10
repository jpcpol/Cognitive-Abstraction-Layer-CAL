#!/usr/bin/env python3
"""
Zenodo publisher for the CAL ecosystem.

Deposits in this round:
  - CAL  v1.4  -> NEW VERSION of existing concept (concept DOI 10.5281/zenodo.20430343)
  - L2   v3.1  -> NEW deposit
  - L3   v0.2  -> NEW deposit

Security:
  - Reads `zenodo_token` from a .env file. The token is NEVER printed.
  - DRY-RUN by default. No network writes happen unless you pass --publish
    AND --commit. With --publish alone, drafts are created but NOT published
    (you review them in the Zenodo web UI, then hit Publish there or re-run
    with --commit).

Usage:
  # 1. See exactly what would happen, touch nothing:
  python publish_zenodo.py

  # 2. Create the draft deposits + upload files, but DO NOT publish:
  python publish_zenodo.py --publish

  # 3. Create + upload + actually publish (irreversible DOIs):
  python publish_zenodo.py --publish --commit

  # Sandbox testing first (recommended): add --sandbox to any of the above.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CAL_ROOT = HERE.parent  # .../CAL

# .env that holds `zenodo_token` (confirmed location)
ENV_PATH = CAL_ROOT / "TCO" / ".env"
ENV_FALLBACKS = [
    Path("c:/Users/Usuario/Documents/Aural Syncro/TCO/.env"),
    CAL_ROOT / "L2" / ".env",
]

# CAL concept record (existing). New version goes under this.
CAL_CONCEPT_DOI = "10.5281/zenodo.20430343"

# Deposits: (key, metadata_file, file_to_upload, mode)
#   mode = "newversion"  -> new version of CAL_CONCEPT_DOI
#   mode = "new"         -> brand-new deposit
DEPOSITS = [
    {
        "key": "CAL v1.4",
        "metadata": HERE / "cal_v1.4.metadata.json",
        "file": CAL_ROOT / "CAL_PrePaper_v1.4.md",
        "mode": "newversion",
    },
    {
        "key": "L2 v3.1",
        "metadata": HERE / "l2_v3.1.metadata.json",
        "file": CAL_ROOT / "L2" / "Documentacion" / "TCO_Paper_Final_v3.md",
        "mode": "new",
    },
    {
        "key": "L3 v0.2",
        "metadata": HERE / "l3_v0.2.metadata.json",
        "file": CAL_ROOT / "L3" / "paper" / "CAL_L3_Paper_v0.1.md",
        "mode": "new",
    },
]


def load_token():
    candidates = [ENV_PATH] + ENV_FALLBACKS
    for p in candidates:
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


def concept_recid(doi):
    # "10.5281/zenodo.20430343" -> "20430343"
    return doi.rsplit(".", 1)[-1]


def find_latest_record(base, params, concept_id):
    """Find the latest published record under the CAL concept (for newversion)."""
    r = requests.get(f"{base}/records/{concept_id}", params=params, timeout=30)
    if r.status_code == 200:
        return r.json()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true",
                    help="Actually create drafts + upload files (still not published unless --commit).")
    ap.add_argument("--commit", action="store_true",
                    help="Publish the drafts (mints DOIs, irreversible).")
    ap.add_argument("--sandbox", action="store_true",
                    help="Use sandbox.zenodo.org instead of production.")
    args = ap.parse_args()

    token, env_used = load_token()
    if not token:
        print("ERROR: could not find `zenodo_token` in any .env. Looked in:")
        for p in [ENV_PATH] + ENV_FALLBACKS:
            print(f"  - {p}")
        sys.exit(1)
    print(f"[ok] token loaded from {env_used}  (value never printed)")

    base = api_base(args.sandbox)
    params = {"access_token": token}
    headers = {"Content-Type": "application/json"}

    print(f"\n=== Zenodo target: {base} ===")
    print(f"=== Mode: {'PUBLISH+COMMIT' if (args.publish and args.commit) else ('PUBLISH (draft only)' if args.publish else 'DRY-RUN (no writes)')} ===\n")

    # Pre-flight: validate files + metadata exist and parse
    for d in DEPOSITS:
        assert d["metadata"].is_file(), f"missing metadata: {d['metadata']}"
        assert d["file"].is_file(), f"missing paper file: {d['file']}"
        json.loads(d["metadata"].read_text(encoding="utf-8"))  # parse check
        print(f"[ok] {d['key']:10s} mode={d['mode']:11s} file={d['file'].name}")

    if not args.publish:
        print("\nDRY-RUN complete. Nothing was sent to Zenodo.")
        print("Next: review the .metadata.json files, then run with --publish (drafts) "
              "or --publish --commit (publish).")
        return

    # Verify token works (and we hit the right instance)
    r = requests.get(f"{base}/deposit/depositions", params={**params, "size": 1}, timeout=30)
    if r.status_code == 401:
        print("ERROR: 401 Unauthorized — token rejected by this Zenodo instance.")
        print("       (If your token is for production, drop --sandbox; and vice-versa.)")
        sys.exit(1)
    r.raise_for_status()
    print("\n[ok] token authenticated against", base)

    results = []
    for d in DEPOSITS:
        meta = json.loads(d["metadata"].read_text(encoding="utf-8"))
        print(f"\n--- {d['key']} ---")

        if d["mode"] == "newversion" and not args.sandbox:
            cid = concept_recid(CAL_CONCEPT_DOI)
            latest = find_latest_record(base, params, cid)
            if latest is None:
                print(f"  ! could not resolve CAL concept {cid} on {base}; "
                      f"creating as NEW deposit instead. Link it manually in the UI.")
                dep = requests.post(f"{base}/deposit/depositions", params=params,
                                    json={}, headers=headers, timeout=30).json()
            else:
                rec_id = latest["id"]
                nv = requests.post(
                    f"{base}/deposit/depositions/{rec_id}/actions/newversion",
                    params=params, timeout=30)
                nv.raise_for_status()
                draft_url = nv.json()["links"]["latest_draft"]
                dep = requests.get(draft_url, params=params, timeout=30).json()
                print(f"  new version draft of concept {cid}")
        else:
            dep = requests.post(f"{base}/deposit/depositions", params=params,
                                json={}, headers=headers, timeout=30).json()
            print("  new deposit draft created")

        dep_id = dep["id"]

        # Upload file (new bucket API)
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
        print(f"  metadata set")

        html = m.json()["links"].get("html", "(see Zenodo)")
        results.append((d["key"], dep_id, html))

        if args.commit:
            pub = requests.post(f"{base}/deposit/depositions/{dep_id}/actions/publish",
                                params=params, timeout=30)
            pub.raise_for_status()
            doi = pub.json().get("doi", "(pending)")
            print(f"  PUBLISHED — DOI: {doi}")
        else:
            print(f"  draft ready (NOT published). Review: {html}")

    print("\n=== Summary ===")
    for key, dep_id, html in results:
        print(f"  {key:10s} dep#{dep_id}  {html}")
    if not args.commit:
        print("\nDrafts created but NOT published. Review each in the Zenodo UI, then either")
        print("click Publish there, or re-run with --publish --commit.")


if __name__ == "__main__":
    main()
