#!/usr/bin/env python3
"""Walk a paged endpoint until N items, has_more=false or the credit budget runs out; JSONL out.

usage: paginate.py <platform/resource> --items N [--max-credits C] [--max-pages P] [k=v ...]

  python3 scripts/paginate.py tiktok/post/comments --items 200 --max-credits 12 url=https://www.tiktok.com/@a/video/1

Each row of `data.items` is one JSON line on stdout; a row already seen (same id, else same url,
else same content) is dropped and counted as `duplicates`, so overlapping pages never inflate N. Pages are chained with the response's
`pagination.next_cursor` sent back verbatim as `cursor`. Budget rule: before each page, spent + the next page's hold must be <= --max-credits. The next
page's hold is the endpoint's cost.max from assets/endpoints.json (the flat price for a flat
endpoint, the registry ceiling for a metered one); with no catalogue it is the last page's
credits_used. Stops, and says why in the stderr
summary (`stopped`: items, has_more, budget, 402, repeat_cursor, max_pages, error): the item
target is met, the API reports no more pages, the next page could exceed --max-credits, a
402, a repeated cursor, or any other error. `credits_used` goes to stderr. Exit 2 on 402,
1 on another error, 3 when no key.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys

import sclib


def page_hold(ep: dict | None) -> float | None:
    """What one more page can hold: the catalogue's cost.max (the flat price, or the ceiling of a
    metered endpoint), or None when the endpoint is not in the catalogue."""
    if not ep or not ep.get("cost"):
        return None
    return ep["cost"]["max"]


def row_key(row) -> str:
    """Identity of a row: its id, else its url, else a hash of its content. Rows come wrapped
    (`{"comment": {...}}`), so the wrapper's object is looked into too."""
    candidates = [row]
    if isinstance(row, dict):
        candidates += [v for v in row.values() if isinstance(v, dict)]
    for field in ("id", "url"):
        for c in candidates:
            if isinstance(c, dict) and c.get(field) not in (None, ""):
                return f"{field}:{c[field]}"
    return "hash:" + hashlib.sha1(json.dumps(row, sort_keys=True, default=str).encode()).hexdigest()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("endpoint")
    ap.add_argument("params", nargs="*", help="k=v params for every page")
    ap.add_argument("--items", type=int, required=True, help="stop after this many rows")
    ap.add_argument("--max-credits", type=float, default=None, help="never start a page that could exceed this")
    ap.add_argument("--max-pages", type=int, default=1000, help="hard page cap (default 1000)")
    args = ap.parse_intermixed_args(argv)
    if args.items <= 0:
        ap.error("--items must be positive")

    endpoint_id = sclib.normalize_id(args.endpoint)
    params = sclib.parse_kv(args.params)
    ep = sclib.find_endpoint(sclib.load_catalogue(), endpoint_id, "GET")
    key = sclib.require_key()

    rows = pages = 0
    spent: float = 0
    hold = page_hold(ep)
    next_cost = hold
    seen_rows: set[str] = set()
    duplicates = 0
    seen: set[str] = set()
    cursor = None
    stopped = "has_more"
    code = 0
    while True:
        if rows >= args.items:
            stopped = "items"
            break
        if pages >= args.max_pages:
            stopped = "max_pages"
            break
        if args.max_credits is not None and next_cost is not None and spent + next_cost > args.max_credits:
            stopped = "budget"
            break
        q = dict(params)
        if cursor:
            q["cursor"] = cursor
        resp = sclib.request("GET", endpoint_id, q, key=key, idempotency_key=sclib.new_idempotency_key())
        if not resp.ok:
            sclib.report_error(resp)
            stopped = "402" if resp.status == 402 else "error"
            code = sclib.exit_code_for(resp)
            break
        pages += 1
        spent += resp.credits_used
        next_cost = hold if hold is not None else (max(resp.credits_used, 0) or next_cost)
        for row in sclib.rows_of(resp.body):
            if rows >= args.items:
                break
            k = row_key(row)
            if k in seen_rows:
                duplicates += 1
                continue
            seen_rows.add(k)
            print(json.dumps(row, ensure_ascii=False))
            rows += 1
        page = sclib.pagination_of(resp.body)
        cursor = page.get("next_cursor")
        if rows >= args.items:
            stopped = "items"
            break
        if not page.get("has_more") or not cursor:
            stopped = "has_more"
            break
        if cursor in seen:
            stopped = "repeat_cursor"
            break
        seen.add(cursor)
    sclib.report_credits(spent)
    print(json.dumps({"rows": rows, "pages": pages, "duplicates": duplicates, "credits_used": spent if not float(spent).is_integer() else int(spent), "stopped": stopped}),
          file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
