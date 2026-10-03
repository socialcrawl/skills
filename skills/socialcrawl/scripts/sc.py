#!/usr/bin/env python3
"""One SocialCrawl call: URL-encoded params, idempotency key, retry policy; prints JSON.

usage: sc.py <platform/resource> [k=v ...] [--method M] [--body JSON|@file] [--no-idempotency]

  python3 scripts/sc.py tiktok/profile handle=stoolpresidente
  python3 scripts/sc.py prism/post-stats 'urls=["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]'

The response body goes to stdout, `credits_used` to stderr. The key comes from
SOCIALCRAWL_API_KEY or ~/.config/socialcrawl/api_key and is never printed. Retries once, and
only when the error says retryable; never on 402 (exit 2). Exit 1 on any other error, 3 when no key.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

import sclib


def build(endpoint_id: str, kv: dict, method: str | None, body_arg, catalogue):
    ep = sclib.find_endpoint(catalogue, endpoint_id, method)
    if ep is None and method is None and catalogue:
        # Templated ids (web/jobs/{job_id}): match on the literal segments.
        for e in catalogue.get("endpoints", []):
            if "{" in e["id"] and re.fullmatch(re.sub(r"\\\{[^}]+\\\}", "[^/]+", re.escape(e["id"])), endpoint_id):
                ep = e
                break
    verb = method or (ep["method"] if ep else "GET")
    template = ep["id"] if ep else endpoint_id
    query = dict(kv)
    body = body_arg
    path = template
    for name in re.findall(r"\{(\w+)\}", template):
        if name not in query:
            raise SystemExit(f"{template} needs {name}=<value>")
        path = path.replace("{" + name + "}", urllib.parse.quote(query.pop(name), safe=""))
    if body is None and verb != "GET" and ep:
        in_body = {p["name"] for p in ep["params"] if p.get("in") == "body"}
        moved = {k: sclib.jsonish(v) for k, v in query.items() if k in in_body}
        if moved:
            body = moved
            query = {k: v for k, v in query.items() if k not in in_body}
    return verb, path, query, body


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("endpoint", help="platform/resource, e.g. tiktok/profile")
    ap.add_argument("params", nargs="*", help="k=v query/body params")
    ap.add_argument("--method", help="HTTP method (default: the endpoint's own, else GET)")
    ap.add_argument("--body", help="JSON body, or @file")
    ap.add_argument("--no-idempotency", action="store_true", help="do not send an Idempotency-Key (a non-GET is then not retried)")
    args = ap.parse_intermixed_args(argv)

    body_arg = None
    if args.body:
        text = Path(args.body[1:]).read_text(encoding="utf-8") if args.body.startswith("@") else args.body
        body_arg = json.loads(text)
    kv = sclib.parse_kv(args.params)
    endpoint_id = sclib.normalize_id(args.endpoint)
    verb, path, query, body = build(
        endpoint_id, kv, args.method.upper() if args.method else None, body_arg, sclib.load_catalogue()
    )
    key = sclib.require_key()
    idem = None if args.no_idempotency else sclib.new_idempotency_key()
    # Without an Idempotency-Key a repeated non-GET could charge twice, so it is never retried.
    resp = sclib.request(verb, path, query, body, key=key, idempotency_key=idem, retry=(verb == "GET" or idem is not None))
    out = resp.body if resp.body is not None else {"raw": resp.raw}
    print(json.dumps(out, ensure_ascii=False))
    if resp.ok:
        remaining = out.get("credits_remaining") if isinstance(out, dict) else None
        sclib.report_credits(resp.credits_used, remaining)
        return 0
    sclib.report_error(resp)
    return sclib.exit_code_for(resp)


if __name__ == "__main__":
    sys.exit(main())
