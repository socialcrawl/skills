#!/usr/bin/env python3
"""Engagement stats for a file of post URLs: chunks of 100 to prism/post-stats, or one prism/jobs job.

usage: batch.py --urls urls.txt|- [--job | --chunks] [--poll-interval S] [--max-credits C]

  python3 scripts/batch.py --urls links.txt > stats.jsonl

One URL per line (blank lines and #comments ignored, duplicates dropped). Up to 500 URLs go as
POST /v1/prism/post-stats in chunks of 100, in input order; more than that (or --job) is submitted
as one POST /v1/prism/jobs job that is polled until it completes and read page by page (free).
Rows come out as JSONL on stdout, one per URL. Each chunk has its own Idempotency-Key. Stops on a
402 (exit 2) keeping what was read. The stderr summary has the platform split (local host map, with
GET /v1/utility/resolve for hosts it does not know; both only label, every URL is still sent) and
`credits_used`. Failed rows are refunded by the API.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse

import sclib

CHUNK = 100
AUTO_JOB_ABOVE = 500
MAX_RESOLVE = 50


def read_urls(path: str) -> list[str]:
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    seen, out = set(), []
    for line in text.splitlines():
        u = line.strip()
        if not u or u.startswith("#") or u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def host_of(url: str) -> str:
    h = (urllib.parse.urlsplit(url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def platform_split(urls: list[str], hosts: dict, key: str) -> dict[str, int]:
    """Count URLs per platform: the local host map first, then the free resolve route, else unknown."""
    cache: dict[str, str] = {}
    resolved = 0
    counts: dict[str, int] = {}
    for u in urls:
        h = host_of(u)
        plat = cache.get(h)
        if plat is None:
            plat = next((p for d, p in hosts.items() if h == d or h.endswith("." + d)), None)
            if plat is None and resolved < MAX_RESOLVE:
                resolved += 1
                r = sclib.request("GET", "utility/resolve", {"input": u}, key=key, retry=False)
                plat = None
                if r.ok and isinstance(r.body, dict):
                    data = r.body.get("data") or {}
                    first = (data.get("results") or [{}])[0] if isinstance(data.get("results"), list) else data
                    plat = (first or {}).get("platform")
            plat = plat or "unknown"
            cache[h] = plat
        counts[plat] = counts.get(plat, 0) + 1
    return counts


def run_chunks(urls: list[str], key: str, max_credits) -> tuple[int, float, int]:
    spent: float = 0
    rows = 0
    for i in range(0, len(urls), CHUNK):
        chunk = urls[i : i + CHUNK]
        if max_credits is not None and spent >= max_credits:
            print(f"stopped: --max-credits {max_credits} reached after {i} URLs", file=sys.stderr)
            return rows, spent, 0
        resp = sclib.request("POST", "prism/post-stats", None, {"urls": chunk}, key=key, idempotency_key=sclib.new_idempotency_key())
        if not resp.ok:
            sclib.report_error(resp)
            return rows, spent, sclib.exit_code_for(resp)
        spent += resp.credits_used
        for row in sclib.rows_of(resp.body):
            print(json.dumps(row, ensure_ascii=False))
            rows += 1
    return rows, spent, 0


def run_job(urls: list[str], key: str, interval: float) -> tuple[int, float, int]:
    body = {"endpoint": "prism/post-stats", "items": [{"url": u} for u in urls]}
    resp = sclib.request("POST", "prism/jobs", None, body, key=key, idempotency_key=sclib.new_idempotency_key())
    if not resp.ok:
        sclib.report_error(resp)
        return 0, 0, sclib.exit_code_for(resp)
    spent = resp.credits_used
    job_id = ((resp.body or {}).get("data") or {}).get("job_id")
    if not job_id:
        print("job submitted but no job_id came back", file=sys.stderr)
        return 0, spent, 1
    rows, cursor = 0, None
    while True:
        r = sclib.request("GET", f"prism/jobs/{urllib.parse.quote(job_id, safe='')}", {"cursor": cursor} if cursor else None, key=key)
        if not r.ok:
            sclib.report_error(r)
            return rows, spent, sclib.exit_code_for(r)
        data = (r.body or {}).get("data") or {}
        if data.get("status") == "failed":
            print(f"job {job_id} failed", file=sys.stderr)
            return rows, spent, 1
        for row in data.get("results") or []:
            print(json.dumps(row, ensure_ascii=False))
            rows += 1
        if data.get("results_complete"):
            return rows, spent, 0
        if data.get("next_cursor"):
            cursor = str(data["next_cursor"])
            continue
        time.sleep(interval)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--urls", required=True, help="file with one URL per line, or - for stdin")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--job", action="store_true", help="always submit one prism/jobs job")
    mode.add_argument("--chunks", action="store_true", help="always send chunks of 100 to prism/post-stats")
    ap.add_argument("--poll-interval", type=float, default=5.0, help="seconds between job polls (default 5)")
    ap.add_argument("--max-credits", type=float, default=None, help="chunk mode: stop once this much is spent")
    args = ap.parse_args(argv)

    urls = read_urls(args.urls)
    if not urls:
        print("no URLs to send", file=sys.stderr)
        return 1
    key = sclib.require_key()
    cat = sclib.load_catalogue() or {}
    split = platform_split(urls, cat.get("hosts") or {}, key)
    print(json.dumps({"urls": len(urls), "platforms": split}), file=sys.stderr)
    use_job = args.job or (not args.chunks and len(urls) > AUTO_JOB_ABOVE)
    rows, spent, code = (run_job(urls, key, args.poll_interval) if use_job else run_chunks(urls, key, args.max_credits))
    sclib.report_credits(spent)
    print(json.dumps({"rows": rows, "urls": len(urls), "mode": "job" if use_job else "chunks"}), file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
