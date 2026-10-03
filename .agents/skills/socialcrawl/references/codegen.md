# Code generation

Read this when the user wants working code against SocialCrawl, or a paging, cost or CSV job done without hand-rolling it. Documentation and code questions need no API key; running a script or a call does (see SKILL.md, API Key).

Pick one: **run a script** when the job is a one-off (collect rows, quote a price, flatten to CSV), **write code from the client below** when the user wants it in their project. Either way pick the endpoint and its price first from the recipe or the platform reference, and put a comment in the code stating the billing unit.

## Rules for generated code

- Read the key from `SOCIALCRAWL_API_KEY`. Never write a key into code, a URL, a log line or an error message.
- Retry only when `error.retryable` is true, once, honouring `Retry-After`. Never retry a 402 (it says `retry_will_succeed: false`). Send an `Idempotency-Key` on POST, PUT, PATCH and DELETE and reuse it on the retry.
- Page with `pagination.next_cursor` sent back verbatim as `cursor`; stop on `pagination.has_more === false`, on the item target, or before a page whose cost (the last page's, or a metered endpoint's cost.max) would push spend past the budget. A page past the source's last page is a free 400 `page_limit`: stop, do not retry.
- Add up `credits_used` from every response and compare it with the quote from `scripts/estimate.py`.
- Do not loop single-item endpoints when a batch endpoint exists (`prism/post-stats`, `prism/profiles`); see recipes.md.

## TypeScript client

Needs Node 18+ or a browser (`fetch`, `crypto.randomUUID`). `sc(path, params, opts)` is what every recipe snippet calls: it URL-encodes params, skips `undefined` and returns the parsed body.

```ts
const BASE = "https://www.socialcrawl.dev/v1/";

/** Any non-2xx response. `code` is the API's error type, e.g. INSUFFICIENT_CREDITS or RATE_LIMITED. */
export class ScError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly status: number,
    readonly retryable: boolean,
    readonly details?: Record<string, unknown>,
    readonly requestId?: string,
  ) {
    super(message);
    this.name = "ScError";
  }
}

export interface ScOptions {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  /** Defaults to a fresh UUID on every non-GET call; pass your own to make a retry across runs safe. */
  idempotencyKey?: string;
}

/** Running total of credits_used across every call made through sc(). */
export const credits = { used: 0 };

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export async function sc<T = any>(path: string, params: Record<string, unknown> = {}, opts: ScOptions = {}): Promise<T> {
  const key = process.env.SOCIALCRAWL_API_KEY;
  if (!key) throw new Error("Set SOCIALCRAWL_API_KEY");
  const query = new URLSearchParams();
  for (const [k, v] of Object.entries(params ?? {})) if (v !== undefined && v !== null) query.append(k, String(v));
  const method = opts.method ?? "GET";
  const headers: Record<string, string> = { "x-api-key": key };
  if (opts.body !== undefined) headers["content-type"] = "application/json";
  if (method !== "GET") headers["Idempotency-Key"] = opts.idempotencyKey ?? crypto.randomUUID();
  const url = `${BASE}${path}${query.size ? `?${query}` : ""}`;
  for (let attempt = 0; ; attempt++) {
    const res = await fetch(url, { method, headers, body: opts.body === undefined ? undefined : JSON.stringify(opts.body) });
    const json = await res.json().catch(() => ({}));
    if (res.ok) {
      credits.used += json.credits_used ?? 0;
      return json as T;
    }
    const e = json.error ?? {};
    const err = new ScError(e.type ?? "UNKNOWN", e.message ?? res.statusText, res.status, e.retryable === true, e.details, json.request_id);
    if (!err.retryable || res.status === 402 || attempt >= 1) throw err;
    await sleep(Math.min(Number(res.headers.get("retry-after")) || 1, 30) * 1000);
  }
}

/**
 * Yields rows page by page. Before each fetch it checks credits spent + the next page's cost against
 * `maxCredits`, so it never overshoots. The next page's cost is `pageCost` when given (a metered
 * endpoint's cost.max in assets/endpoints.json), else what the last page settled at.
 */
export async function* paginate(path: string, params: Record<string, unknown>, o: { items: number; maxCredits?: number; pageCost?: number }) {
  const start = credits.used;
  const max = o.maxCredits ?? Infinity;
  let next = o.pageCost ?? 0;
  let cursor: string | undefined;
  let n = 0;
  do {
    if (credits.used - start + next > max) return;
    const before = credits.used;
    const r: any = await sc(path, { ...params, cursor });
    next = o.pageCost ?? credits.used - before;
    for (const row of r.data.items) {
      if (n++ >= o.items) return;
      yield row;
    }
    cursor = r.pagination?.has_more ? (r.pagination.next_cursor ?? undefined) : undefined;
  } while (cursor && n < o.items);
}
```

Use it:

```ts
// 1 credit per page of comments (quote first: python3 scripts/estimate.py tiktok/post/comments --items 200 url=...)
for await (const row of paginate("tiktok/post/comments", { url, sort: "recent" }, { items: 200, maxCredits: 12, pageCost: 1 })) {
  console.log(row.comment.text);
}
console.error(`credits_used: ${credits.used}`);
```

## Python client

Standard library only (`urllib`); with `requests` installed swap `urlopen` for `requests.request` and keep the rest.

```python
import email.utils, json, os, time, urllib.error, urllib.parse, urllib.request, uuid
from datetime import datetime, timezone

BASE = "https://www.socialcrawl.dev/v1/"
credits_used = 0  # running total across every call


class ScError(Exception):
    """Any failed call. `code` is the API's error type (e.g. INSUFFICIENT_CREDITS), or NETWORK_ERROR."""

    def __init__(self, code, message, status, retryable=False, details=None, request_id=None):
        super().__init__(message)
        self.code, self.status, self.retryable = code, status, retryable
        self.details, self.request_id = details or {}, request_id


def retry_wait(value):
    """Seconds from a Retry-After header (delta-seconds or an HTTP-date), capped at 30; 1 when absent."""
    if not value:
        return 1.0
    try:
        wait = float(value)
    except ValueError:
        try:
            wait = (email.utils.parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds()
        except (TypeError, ValueError):
            wait = 1.0
    return max(0.0, min(wait, 30.0))


def sc(path, params=None, method="GET", body=None, idempotency_key=None):
    """One call: URL-encodes params, skips None, retries once if (and only if) the error is retryable."""
    global credits_used
    key = os.environ["SOCIALCRAWL_API_KEY"]
    query = urllib.parse.urlencode({k: v for k, v in (params or {}).items() if v is not None})
    headers = {"x-api-key": key}
    if body is not None:
        headers["content-type"] = "application/json"
    if method != "GET":
        headers["Idempotency-Key"] = idempotency_key or str(uuid.uuid4())
    url = BASE + path + ("?" + query if query else "")
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(2):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.load(r)
            credits_used += out.get("credits_used", 0)
            return out
        except urllib.error.HTTPError as h:
            out = json.loads(h.read() or b"{}")
            e = out.get("error", {})
            err = ScError(e.get("type", "UNKNOWN"), e.get("message", h.reason), h.code, e.get("retryable") is True, e.get("details"), out.get("request_id"))
            wait = retry_wait(h.headers.get("Retry-After"))
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            err, wait = ScError("NETWORK_ERROR", f"request failed: {getattr(e, 'reason', e)}", 0, True), 1.0
        if not err.retryable or err.status == 402 or attempt == 1:
            raise err from None
        time.sleep(wait)


def paginate(path, params, items, max_credits=float("inf"), page_cost=None):
    """Yield rows. Before each fetch, checks credits spent + the next page's cost against `max_credits`,
    so it never overshoots. The next page's cost is `page_cost` when given (a metered endpoint's
    cost.max in assets/endpoints.json), else what the last page settled at."""
    start, cursor, n, nxt = credits_used, None, 0, page_cost or 0
    while True:
        if credits_used - start + nxt > max_credits:
            return
        before = credits_used
        page = sc(path, {**params, "cursor": cursor})
        nxt = page_cost if page_cost is not None else credits_used - before
        for row in page["data"]["items"]:
            if n >= items:
                return
            n += 1
            yield row
        p = page.get("pagination") or {}
        cursor = p.get("next_cursor") if p.get("has_more") else None
        if not cursor or n >= items:
            return
```

## Types

`assets/socialcrawl-types.ts` (interfaces) and `assets/socialcrawl_types.py` (TypedDicts, Python 3.8+) are generated from the canonical schemas: the envelope (`ApiResponse<T>`, `Pagination`, `ApiErrorBody`), every canonical object (`Comment`, `Post`, `Author`, `Product`, `Review`, ...), and a response type named after the endpoint for each endpoint the recipes use (`TiktokPostCommentsResponse`). Copy the file into the project rather than retyping shapes (the names are deliberate: a file called `types.py` would shadow the standard library):

```ts
import type { TiktokPostCommentsResponse } from "./socialcrawl-types";
const page = await sc<TiktokPostCommentsResponse>("tiktok/post/comments", { url });
const texts = page.data.items.map((i) => i.comment.text);
```

An endpoint with no named response type returns the canonical type of its archetype; `assets/endpoints.json` lists it per endpoint. Fields can be `null` and most are optional: check before you use one. Where a row lives (`data.items[].comment`) is `rows_at` in the catalogue and in the platform reference.

## Scripts

Python 3, standard library only, in `scripts/`. They read the key the way SKILL.md says, never print it, and print `credits_used` to stderr. Rows go to stdout as JSON lines, so they pipe.

| Script | Use |
| --- | --- |
| `python3 scripts/sc.py <platform/resource> k=v ...` | One call: encodes params, sends an idempotency key, retries once when retryable, never on 402. Prints the JSON body. A POST endpoint's body params (`urls='["..."]'`) go in the JSON body automatically |
| `python3 scripts/paginate.py <id> --items N [--max-credits C] k=v ...` | Walks pages until N rows, `has_more=false` or the budget would be exceeded (spent + the next page's `cost.max` from the catalogue must stay within `--max-credits`); drops duplicate rows by id, url or content; stops on 402. JSONL out, a one-line summary (`stopped`: items, has_more, budget, 402, ...) on stderr |
| `python3 scripts/estimate.py <id> [--items N] k=v ...` or `--plan plan.json` | Quote before paying. Uses `GET /v1/utility/estimate` when a key is set and falls back to `assets/endpoints.json` offline (`source: "offline"`, metered prices are the registry's range) |
| `python3 scripts/batch.py --urls links.txt` | Post URLs in chunks of 100 to `prism/post-stats`, or one `prism/jobs` job above 500 (`--job` to force); polls and merges, one JSONL row per URL |
| `python3 scripts/to_csv.py --archetype Comment` | Flattens rows (from a file or stdin) to CSV with the canonical schema's core columns in a stable order (`--all-ext` adds the platform-specific `ext.*` ones); `--columns`, `--extra`, `--out` |

```sh
python3 scripts/estimate.py tiktok/post/comments --items 200 url=https://www.tiktok.com/@a/video/1
python3 scripts/paginate.py tiktok/post/comments --items 200 --max-credits 12 url=https://www.tiktok.com/@a/video/1 \
  | python3 scripts/to_csv.py --archetype Comment > comments.csv
```

Exit codes: 0 done, 1 error, 2 payment required (402), 3 no key. A script that exits 2 or 3 has made no further call; tell the user, do not retry. `SOCIALCRAWL_BASE_URL` is honoured only for localhost (and never over plain http for a remote host); the key is never sent to another host on a redirect.

`assets/endpoints.json` is the offline contract subset: per endpoint its method, params (location, type, enum, bounds, oneOf groups), cost model (`flat` or `metered` with min and max), paging (page size, `per_n_items` formula, price per page) and `rows_at`. The live registry (`GET /v1/utility/endpoints`, free) wins when they differ.
