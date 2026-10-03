"""Shared helpers for the SocialCrawl skill scripts. Python 3 standard library only.

Key resolution follows SKILL.md: SOCIALCRAWL_API_KEY when it looks like a real key,
else the first line of ~/.config/socialcrawl/api_key. The key is only ever placed in
the x-api-key header; it is never printed, logged or put in an error message.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

DEFAULT_BASE = "https://www.socialcrawl.dev"
KEY_FILE = "~/.config/socialcrawl/api_key"
TIMEOUT_S = 60
MAX_RETRY_WAIT_S = 30

EXIT_ERROR = 1
EXIT_PAYMENT = 2
EXIT_NO_KEY = 3


LOCAL_HOSTS = ("localhost", "127.0.0.1", "::1")


def base_url() -> str:
    """The API origin. SOCIALCRAWL_BASE_URL (tests, local dev) may only point at localhost unless
    SC_ALLOW_REMOTE_BASE=1, and plain http:// is refused for any non-local host: the key travels in
    a header, so a stray override must not send it somewhere else or in the clear."""
    override = os.environ.get("SOCIALCRAWL_BASE_URL")
    if not override:
        return DEFAULT_BASE
    parts = urllib.parse.urlsplit(override)
    local = (parts.hostname or "") in LOCAL_HOSTS
    if not local and os.environ.get("SC_ALLOW_REMOTE_BASE") != "1":
        print(
            "SOCIALCRAWL_BASE_URL points at a non-local host; refusing to send the API key there. "
            "Set SC_ALLOW_REMOTE_BASE=1 only if you mean it.",
            file=sys.stderr,
        )
        sys.exit(EXIT_ERROR)
    if not local and parts.scheme != "https":
        print("SOCIALCRAWL_BASE_URL must use https:// for a non-local host.", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    if parts.scheme not in ("http", "https"):
        print("SOCIALCRAWL_BASE_URL must be an http(s) URL.", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    return override.rstrip("/")


def _usable(key: str | None) -> bool:
    if not key:
        return False
    k = key.strip()
    low = k.lower()
    if not k.startswith("sc_"):
        return False
    return not any(p in low for p in ("xxx", "your", "example", "placeholder", "<", "..."))


def resolve_key() -> str | None:
    env = os.environ.get("SOCIALCRAWL_API_KEY")
    if _usable(env):
        return env.strip()
    path = Path(os.path.expanduser(KEY_FILE))
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        if os.name == "posix" and path.stat().st_mode & 0o077:
            print(f"warning: {KEY_FILE} is readable by other users; run chmod 600 on it", file=sys.stderr)
    except OSError:
        pass
    line = (text.splitlines() or [""])[0].strip()
    return line if _usable(line) else None


def require_key() -> str:
    key = resolve_key()
    if key:
        return key
    print(
        "No SocialCrawl API key found. Create one at https://socialcrawl.dev/dashboard and set "
        f"SOCIALCRAWL_API_KEY or save it in {KEY_FILE} (do not paste it into chat).",
        file=sys.stderr,
    )
    sys.exit(EXIT_NO_KEY)


# --------------------------------------------------------------------------- catalogue


def catalogue_path() -> Path:
    override = os.environ.get("SOCIALCRAWL_ENDPOINTS")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent / "assets" / "endpoints.json"


def load_catalogue() -> dict | None:
    try:
        return json.loads(catalogue_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def normalize_id(raw: str) -> str:
    s = raw.strip()
    if s.startswith("/v1/"):
        s = s[4:]
    return s.strip("/")


def find_endpoint(cat: dict | None, endpoint_id: str, method: str | None = None) -> dict | None:
    if not cat:
        return None
    for e in cat.get("endpoints", []):
        if e["id"] == endpoint_id and (method is None or e["method"] == method):
            return e
    return None


# --------------------------------------------------------------------------- params


def parse_kv(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in pairs:
        if "=" not in p:
            raise SystemExit(f"expected key=value, got {p!r}")
        k, v = p.split("=", 1)
        k = k.strip()
        if not k:
            raise SystemExit(f"empty parameter name in {p!r}")
        if v != "":
            out[k] = v
    return out


def jsonish(value: str):
    s = value.strip()
    if s[:1] in "[{":
        try:
            return json.loads(s)
        except ValueError:
            return value
    return value


def encode_query(params: dict) -> str:
    items = []
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            items.extend((k, str(x)) for x in v)
        elif isinstance(v, bool):
            items.append((k, "true" if v else "false"))
        else:
            items.append((k, str(v)))
    return urllib.parse.urlencode(items, quote_via=urllib.parse.quote)


# --------------------------------------------------------------------------- HTTP


class Response:
    def __init__(self, status: int, headers: dict, body, raw: str):
        self.status = status
        self.headers = {k.lower(): v for k, v in headers.items()}
        self.body = body
        self.raw = raw

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

    @property
    def error(self) -> dict:
        e = self.body.get("error") if isinstance(self.body, dict) else None
        return e if isinstance(e, dict) else {}

    @property
    def code(self) -> str | None:
        # The error envelope names the code in `error.type`.
        return self.error.get("type") or self.error.get("code")

    @property
    def retryable(self) -> bool:
        return bool(self.error.get("retryable"))

    @property
    def credits_used(self) -> int | float:
        if isinstance(self.body, dict) and isinstance(self.body.get("credits_used"), (int, float)):
            return self.body["credits_used"]
        try:
            return float(self.headers.get("x-credits-used", 0)) or 0
        except ValueError:
            return 0


def new_idempotency_key() -> str:
    return str(uuid.uuid4())


def _sleep(seconds: float) -> None:
    if os.environ.get("SC_NO_SLEEP"):
        return
    time.sleep(seconds)


class _KeepKeyOnSameHost(urllib.request.HTTPRedirectHandler):
    """Follow redirects, but never carry the API key (or idempotency key) to another host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and urllib.parse.urlsplit(newurl).netloc != urllib.parse.urlsplit(req.full_url).netloc:
            for h in ("x-api-key", "idempotency-key"):
                new.headers.pop(h.capitalize(), None)
                new.headers.pop(h, None)
                new.unredirected_hdrs.pop(h.capitalize(), None)
                new.unredirected_hdrs.pop(h, None)
        return new


_OPENER = urllib.request.build_opener(_KeepKeyOnSameHost)


def _once(method: str, url: str, headers: dict, data: bytes | None) -> Response:
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with _OPENER.open(req, timeout=TIMEOUT_S) as r:
            status, hdrs, raw = r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        status, hdrs, raw = e.code, dict(e.headers), e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        # Never include the request (headers carry the key) in the message.
        reason = getattr(e, "reason", e)
        body = {"success": False, "error": {"type": "NETWORK_ERROR", "message": f"request failed: {reason}", "status": 0, "retryable": True}}
        return Response(0, {}, body, json.dumps(body))
    try:
        body = json.loads(raw) if raw else None
    except ValueError:
        body = None
    return Response(status, hdrs, body, raw)


def _retry_wait(resp: Response) -> float:
    try:
        wait = float(resp.headers.get("retry-after", ""))
    except ValueError:
        wait = 1.0 + random.random()
    return max(0.0, min(wait, MAX_RETRY_WAIT_S))


def request(
    method: str,
    path: str,
    params: dict | None = None,
    body=None,
    key: str | None = None,
    idempotency_key: str | None = None,
    retry: bool = True,
) -> Response:
    """One API call. `path` is relative to /v1. Retries once, and only when the API says
    the error is retryable; never on 402. The same Idempotency-Key is sent on the retry."""
    url = f"{base_url()}/v1/{path.lstrip('/')}"
    q = encode_query(params or {})
    if q:
        url += "?" + q
    headers = {"accept": "application/json", "user-agent": "socialcrawl-skill-scripts/1"}
    if key:
        headers["x-api-key"] = key
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["content-type"] = "application/json"
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    resp = _once(method, url, headers, data)
    if retry and not resp.ok and resp.status != 402 and resp.retryable:
        _sleep(_retry_wait(resp))
        resp = _once(method, url, headers, data)
    return resp


def report_credits(used, remaining=None) -> None:
    n = int(used) if float(used).is_integer() else used
    line = f"credits_used: {n}"
    if remaining is not None:
        line += f" (credits_remaining: {remaining})"
    print(line, file=sys.stderr)


def report_error(resp: Response) -> None:
    e = resp.error
    reason = (e.get("details") or {}).get("reason") if isinstance(e.get("details"), dict) else None
    msg = f"HTTP {resp.status} {resp.code or 'ERROR'}: {e.get('message', 'request failed')}"
    if reason:
        msg += f" ({reason})"
    if resp.status == 402:
        msg += "; not retryable - top up credits or raise the key's spend cap"
    print(msg, file=sys.stderr)


def exit_code_for(resp: Response) -> int:
    return EXIT_PAYMENT if resp.status == 402 else EXIT_ERROR


def rows_of(body) -> list:
    data = body.get("data") if isinstance(body, dict) else None
    if not isinstance(data, dict):
        return []
    # Lists use data.items; the batch endpoints put one row per input under data.results.
    for k in ("items", "results"):
        if isinstance(data.get(k), list):
            return data[k]
    return []


def pagination_of(body) -> dict:
    p = body.get("pagination") if isinstance(body, dict) else None
    return p if isinstance(p, dict) else {}
