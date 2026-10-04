#!/usr/bin/env python3
"""One SocialCrawl call: URL-encoded params, idempotency key, retry policy; prints JSON.

usage: sc.py <platform/resource> [k=v ...] [--method M] [--body JSON|@file] [--no-idempotency]

  python3 scripts/sc.py tiktok/profile handle=stoolpresidente
  python3 scripts/sc.py "finance/ticker-search keyword=NVIDIA"   (one quoted argument works too)
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


USAGE = "usage: sc.py <platform/resource> [k=v ...] [--method M] [--body JSON|@file] (see --help)"
# Characters a request line may not carry (http.client refuses them); whitespace splits first.
BAD_ID_CHARS = re.compile(r"[\x00-\x20\x7f?#]")


class UsageError(Exception):
    pass


def split_endpoint(endpoint: str, params: list[str]) -> tuple[str, list[str]]:
    """`sc.py "finance/ticker-search keyword=NVIDIA"`: one quoted argument holding the id and
    its params is split on whitespace, the same as passing them separately."""
    parts = endpoint.split()
    if not parts:
        raise UsageError("missing <platform/resource>")
    endpoint_id = sclib.normalize_id(parts[0])
    if not endpoint_id or BAD_ID_CHARS.search(endpoint_id):
        raise UsageError(f"not an endpoint id: {parts[0]!r} (expected platform/resource, e.g. tiktok/profile)")
    return endpoint_id, parts[1:] + list(params)


def read_body(arg: str):
    try:
        text = Path(arg[1:]).read_text(encoding="utf-8") if arg.startswith("@") else arg
    except OSError as e:
        raise UsageError(f"cannot read --body file {arg[1:]!r}: {e.strerror or e}")
    try:
        return json.loads(text)
    except ValueError as e:
        raise UsageError(f"--body is not valid JSON: {e}")


def main(argv=None) -> int:
    try:
        return run(argv)
    except UsageError as e:
        print(f"sc.py: {e}\n{USAGE}", file=sys.stderr)
        return sclib.EXIT_ERROR


def run(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("endpoint", help="platform/resource, e.g. tiktok/profile")
    ap.add_argument("params", nargs="*", help="k=v query/body params")
    ap.add_argument("--method", help="HTTP method (default: the endpoint's own, else GET)")
    ap.add_argument("--body", help="JSON body, or @file")
    ap.add_argument("--no-idempotency", action="store_true", help="do not send an Idempotency-Key (a non-GET is then not retried)")
    args = ap.parse_intermixed_args(argv)

    body_arg = read_body(args.body) if args.body else None
    endpoint_id, params = split_endpoint(args.endpoint, args.params)
    try:
        kv = sclib.parse_kv(params)
        verb, path, query, body = build(
            endpoint_id, kv, args.method.upper() if args.method else None, body_arg, sclib.load_catalogue()
        )
    except SystemExit as e:
        raise UsageError(str(e.code))
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
