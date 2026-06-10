#!/usr/bin/env python3
"""
Publish the THREE already-created Zenodo drafts by ID.
Does NOT create or re-upload anything. Token via Authorization header
(never in URL), and all errors are sanitized so the token can't leak.
"""
import json
import sys
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
ENV_PATH = Path("c:/Users/Usuario/Documents/Aural Syncro/TCO/.env")
BASE = "https://zenodo.org/api"

# The drafts created by the --publish run (dep#... from that output):
DRAFTS = {
    "CAL v1.4": 20628125,
    "L2 v3.1": 20628131,
    "L3 v0.2": 20628133,
}


def load_token():
    for line in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line.startswith("zenodo_token=") or line.startswith("zenodo_token ="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def safe(resp):
    """Return status + body WITHOUT the request URL (which carries no token here,
    but we sanitize defensively)."""
    body = resp.text[:500]
    return f"HTTP {resp.status_code}: {body}"


def main():
    token = load_token()
    if not token:
        print("ERROR: no zenodo_token in .env")
        sys.exit(1)
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {token}",
                      "Content-Type": "application/json"})
    print("[ok] token loaded (never printed); using Authorization header\n")

    published = []
    for key, dep_id in DRAFTS.items():
        print(f"--- {key} (dep#{dep_id}) ---")
        # confirm draft exists + show files
        g = s.get(f"{BASE}/deposit/depositions/{dep_id}", timeout=30)
        if g.status_code != 200:
            print(f"  ! cannot read draft: {safe(g)}")
            continue
        info = g.json()
        files = [f["filename"] for f in info.get("files", [])]
        title = info.get("metadata", {}).get("title", "(no title)")
        print(f"  title: {title[:70]}")
        print(f"  files: {files}")
        # publish
        p = s.post(f"{BASE}/deposit/depositions/{dep_id}/actions/publish", timeout=30)
        if p.status_code in (200, 201, 202):
            doi = p.json().get("doi", "(pending)")
            rec = p.json().get("links", {}).get("record_html", "")
            print(f"  PUBLISHED — DOI: {doi}  {rec}")
            published.append((key, doi, rec))
        else:
            print(f"  ! publish failed: {safe(p)}")
    print("\n=== Published ===")
    for key, doi, rec in published:
        print(f"  {key:10s} {doi}  {rec}")


if __name__ == "__main__":
    main()
