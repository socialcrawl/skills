#!/usr/bin/env python3
"""One SocialCrawl call: URL-encoded params, idempotency key, retry policy; prints JSON.

usage: sc.py <platform/resource> [k=v ...] [--method M] [--body JSON|@file] [--no-idempotency]
             [--follow [--poll-interval S] [--follow-timeout S]]

  python3 scripts/sc.py tiktok/profile handle=stoolpresidente
  python3 scripts/sc.py "finance/ticker-search keyword=NVIDIA"   (one quoted argument works too)
  python3 scripts/sc.py prism/post-stats 'urls=["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]'

The response body goes to stdout, `credits_used` to stderr. The key comes from
SOCIALCRAWL_API_KEY or ~/.config/socialcrawl/api_key and is never printed. Retries once, and
only when the error says retryable; never on 402 (exit 2). Exit 1 on any other error, 3 when no key.

A 202 answer is a background run: its `credits_used` is the hold (the most it can cost), not the
charge. --follow waits for it (free reads): a discover run is polled at `data.next.status_url`
(path and query only, always sent to the configured API origin), a web job at
GET /v1/web/jobs/{job_id} and a prism job at GET /v1/prism/jobs/{job_id}, until the status is no
longer queued/running/polling. The final body goes to stdout and the settled charge
(`data.run.credits.spent`, else `data.credits_charged`) to stderr as `credits_used`. Exit 1 when
the run ends failed, cancelled or expired, or --follow-timeout (default 1800 s) passes. For every
row of a large prism job, use batch.py.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
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


RUNNING = ("queued", "running", "polling")
FAILED = ("failed", "cancelled", "expired")


def follow_target(path: str, body):
    """(path, params) to poll for a 202 body, or None when there is nothing to follow."""
    data = body.get("data") if isinstance(body, dict) else None
    if not isinstance(data, dict):
        return None
    nxt = data.get("next")
    status_url = nxt.get("status_url") if isinstance(nxt, dict) else None
    if isinstance(status_url, str) and status_url:
        # Only the path and query are used: the key never goes to a host named in a response.
        parts = urllib.parse.urlsplit(status_url)
        if parts.path.startswith("/v1/"):
            return parts.path[4:], dict(urllib.parse.parse_qsl(parts.query))
    job_id = data.get("job_id")
    if isinstance(job_id, str) and job_id:
        family = path.split("/", 1)[0]
        if family in ("web", "prism"):
            return f"{family}/jobs/{urllib.parse.quote(job_id, safe='')}", {}
    return None


def _data(body) -> dict:
    data = body.get("data") if isinstance(body, dict) else None
    return data if isinstance(data, dict) else {}


def run_status(body) -> str | None:
    data = _data(body)
    run = data.get("run")
    status = run.get("status") if isinstance(run, dict) else data.get("status")
    return status if isinstance(status, str) else None


def settled_credits(body):
    """The settled charge: a discover run's credits.spent, else a job's credits_charged."""
    data = _data(body)
    run = data.get("run")
    if isinstance(run, dict) and isinstance(run.get("credits"), dict):
        spent = run["credits"].get("spent")
        if isinstance(spent, (int, float)):
            return spent
    charged = data.get("credits_charged")
    return charged if isinstance(charged, (int, float)) else None


def follow(resp, path: str, key: str, interval: float, timeout: float) -> int:
    target = follow_target(path, resp.body)
    if target is None:
        print(json.dumps(resp.body, ensure_ascii=False))
        print("--follow: this 202 names no status_url or job_id to poll", file=sys.stderr)
        sclib.report_credits(resp.credits_used)
        return 0
    poll_path, params = target
    deadline = time.monotonic() + timeout
    print(f"following {poll_path}; credits_used {resp.credits_used:g} on the 202 is the hold", file=sys.stderr)
    while True:
        r = sclib.request("GET", poll_path, params, key=key)
        if not r.ok:
            print(json.dumps(r.body if r.body is not None else {"raw": r.raw}, ensure_ascii=False))
            sclib.report_error(r)
            return sclib.exit_code_for(r)
        status = run_status(r.body)
        if status not in RUNNING:
            print(json.dumps(r.body, ensure_ascii=False))
            settled = settled_credits(r.body)
            print(f"status: {status}", file=sys.stderr)
            sclib.report_credits(settled if settled is not None else resp.credits_used)
            return sclib.EXIT_ERROR if status in FAILED else 0
        if time.monotonic() >= deadline:
            print(json.dumps(r.body, ensure_ascii=False))
            print(f"--follow-timeout {timeout:g} s passed with status {status}; poll {poll_path} later (free)", file=sys.stderr)
            return sclib.EXIT_ERROR
        # A status_url with wait_s long-polls on the server; the job routes answer at once.
        if not params.get("wait_s"):
            run = _data(r.body).get("run")
            wait = run.get("poll_after_s") if isinstance(run, dict) else None
            sclib._sleep(wait if isinstance(wait, (int, float)) and wait > 0 else interval)


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
    ap.add_argument("--follow", action="store_true", help="on a 202, poll the run or job until it ends; print the final body and settled credits")
    ap.add_argument("--poll-interval", type=float, default=5.0, help="--follow: seconds between job polls (default 5)")
    ap.add_argument("--follow-timeout", type=float, default=1800.0, help="--follow: give up after this many seconds (default 1800)")
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
    if resp.status == 202 and args.follow:
        return follow(resp, path, key, args.poll_interval, args.follow_timeout)
    out = resp.body if resp.body is not None else {"raw": resp.raw}
    print(json.dumps(out, ensure_ascii=False))
    if resp.ok:
        remaining = out.get("credits_remaining") if isinstance(out, dict) else None
        sclib.report_credits(resp.credits_used, remaining)
        if resp.status == 202:
            print("202: a background run; credits_used is the hold, not the charge. Rerun with --follow, or poll "
                  "data.next.status_url / GET /v1/web/jobs/{job_id} / GET /v1/prism/jobs/{job_id} (free)", file=sys.stderr)
        return 0
    sclib.report_error(resp)
    return sclib.exit_code_for(resp)


if __name__ == "__main__":
    sys.exit(main())
