#!/usr/bin/env python3
"""
(a) Clean the CAL v1.4 published record (dep#20628125):
    - upload the freshly generated cal_prepaper_v1.4.pdf
    - remove the inherited cal_prepaper_v1.3.pdf and cal_prepaper.zip

The record is already PUBLISHED, so we open an edit session (actions/edit),
mutate files, then re-publish.

Token via Authorization header (never in URL, never printed). Errors are
sanitized. DRY-RUN by default; pass --commit to actually mutate + re-publish.

Usage:
  python fix_cal_files.py            # dry-run: show current files + plan
  python fix_cal_files.py --commit   # apply + re-publish
"""
import argparse
import sys
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
ENV_PATH = Path("c:/Users/Usuario/Documents/Aural Syncro/TCO/.env")
BASE = "https://zenodo.org/api"

DEP_ID = 20628125
NEW_PDF = HERE / "cal_prepaper_v1.4.pdf"
REMOVE = {"cal_prepaper_v1.3.pdf", "cal_prepaper.zip"}
KEEP_MD = "CAL_PrePaper_v1.4.md"


def load_token():
    if not ENV_PATH.is_file():
        return None
    for line in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line.startswith("zenodo_token=") or line.startswith("zenodo_token ="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def safe(resp):
    return f"HTTP {resp.status_code}: {resp.text[:400]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()

    if not NEW_PDF.is_file():
        print(f"ERROR: missing {NEW_PDF}. Generate it first.")
        sys.exit(1)

    token = load_token()
    if not token:
        print(f"ERROR: no `zenodo_token` in {ENV_PATH}. Put the NEW token there first.")
        sys.exit(1)

    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {token}"})
    print(f"[ok] token loaded from {ENV_PATH} (never printed)\n")

    # Read current record
    g = s.get(f"{BASE}/deposit/depositions/{DEP_ID}", timeout=30)
    if g.status_code != 200:
        print(f"ERROR reading record: {safe(g)}")
        sys.exit(1)
    rec = g.json()
    state = rec.get("state")
    submitted = rec.get("submitted")
    files = rec.get("files", [])
    print(f"record {DEP_ID}: state={state} submitted={submitted}")
    print("current files:")
    for f in files:
        flag = "  -> REMOVE" if f["filename"] in REMOVE else ""
        print(f"  - {f['filename']}{flag}")
    print(f"plan: + upload {NEW_PDF.name}; - remove {sorted(REMOVE)}; keep {KEEP_MD}")

    if not args.commit:
        print("\nDRY-RUN. Re-run with --commit to apply.")
        return

    # Open edit session if published
    if submitted:
        e = s.post(f"{BASE}/deposit/depositions/{DEP_ID}/actions/edit", timeout=30)
        if e.status_code not in (200, 201):
            print(f"ERROR opening edit session: {safe(e)}")
            sys.exit(1)
        rec = s.get(f"{BASE}/deposit/depositions/{DEP_ID}", timeout=30).json()
        files = rec.get("files", [])
        print("\n[ok] edit session opened")

    # Delete unwanted files
    for f in files:
        if f["filename"] in REMOVE:
            fid = f["id"]
            d = s.delete(f"{BASE}/deposit/depositions/{DEP_ID}/files/{fid}", timeout=30)
            if d.status_code in (200, 204):
                print(f"  removed {f['filename']}")
            else:
                print(f"  ! failed to remove {f['filename']}: {safe(d)}")

    # Upload new PDF via bucket
    bucket = rec["links"]["bucket"]
    with open(NEW_PDF, "rb") as fh:
        up = s.put(f"{bucket}/{NEW_PDF.name}", data=fh, timeout=120)
    if up.status_code in (200, 201):
        print(f"  uploaded {NEW_PDF.name}")
    else:
        print(f"  ! upload failed: {safe(up)}")
        sys.exit(1)

    # Re-publish
    p = s.post(f"{BASE}/deposit/depositions/{DEP_ID}/actions/publish", timeout=30)
    if p.status_code in (200, 201, 202):
        doi = p.json().get("doi", "(pending)")
        print(f"\nRE-PUBLISHED — DOI: {doi}")
        finalfiles = [f["filename"] for f in p.json().get("files", [])]
        print(f"final files: {finalfiles}")
    else:
        print(f"  ! re-publish failed: {safe(p)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
