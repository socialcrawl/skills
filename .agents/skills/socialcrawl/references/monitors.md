# Monitors

The stateful, scheduled wrapper around any SocialCrawl recipe. A monitor re-runs a registered GET endpoint or a Prism composite on a cadence, evaluates alert rules, optionally delivers each run to a signed webhook, and accumulates a per-run time-series you can read back or export. *"Prism answers once; monitors watch it for you."*

Monitors are **not** registry endpoints. They live at `/v1/monitors/*`, use methods beyond GET (POST/PATCH/DELETE), and are **not** counted in the endpoint total quoted in `SKILL.md`. Auth is the same `x-api-key` header. Monitors belong to the **account**, not the key: every key on the account sees and manages all of them, and revoking the key that created a monitor does **not** stop it (it keeps running and billing on the account balance).

**Do not confuse these with `/v1/web/monitors/*`.** That is a different, narrower family: it watches ONE web page for changes on a minute-level cadence and lives in [web.md](web.md). `/v1/monitors/*` (this file) schedules ANY registered GET endpoint or Prism composite, with a one-hour floor. If the user wants "watch this URL for changes", use the web one; if they want "track this brand / creator / product / sound over time", use this one.

## Two kinds of monitor

| | Legacy monitor (no `track`) | Numbers-only monitor (`track` set) |
| --- | --- | --- |
| `webhook_url` | required | optional (omit = download-only) |
| What each run fetches | the recipe's **primary source only**; for a single-platform endpoint that is the **supplier's raw body, before mapping to the unified shape** (Prism / `search/everywhere` return their own unified body) | the **unified canonical page** (same shape as a `/v1` call), via the endpoint's full source chain with fallback |
| What a run stores | the whole body in `result` | only the tracked numbers (`numbers`) + `deltas`; `result` is always `null` |
| Alert / delta paths | dot paths into the stored body (supplier field names for single-platform endpoints) | must be one of `track.metrics` |
| `webhook_format: "rows"` | not allowed | allowed |
| `legs` on a run | the recipe's own `legs[]` (Prism composites), else `[]` | one entry naming the step that answered, `primary` or `fallback` |

**Prefer `track`** whenever the goal is a number over time (followers, views, a sound's reel count). It reads unified paths (`author.followers`, `items[].post.engagement.views`, `total`), validates them at create for free, and never bills a run that recorded nothing.

## Billing

- **Free:** create, list, get, runs, timeseries, export, pause/resume (PATCH), delete. None of these touch the balance.
- **Each executed run:** the recipe's price for the monitor's frozen params **+ 1 credit** scheduling premium. The recipe price comes from the same pricer `/v1` uses (static tier, flat `cost`, or the metered price computed from the params), with `now-<N>d` tokens resolved first. Look the recipe price up in that endpoint's reference / [cost-gate.md](cost-gate.md). Examples: `instagram/audio/reels` (1) = **2 per run**; `search/everywhere` (20) = **21 per run**; `prism/reputation` (30) = **31 per run**.
- **`estimated_cost_per_run`** (create and GET responses) = that price + 1. **`estimated_monthly_cost`** = cost per run x runs/month: `hourly` 730, `daily` 30, `weekly` 4, cron = round(30 days / its shortest interval between firings, floored at 1 hour).
- The run is charged upfront (cost + 1), then reconciled:

| Run outcome | `status` | Charged |
| --- | --- | --- |
| Balance below cost + 1 when the slot runs | `skipped`, `skip_reason: "insufficient_credits"` | 0 (never deducted). The slot is not retried. |
| Recipe returned an error (any non-OK status) or threw | `failed` | 0 (full refund of cost + 1) |
| `track` monitor: the page came back with no rows | `failed`, `skip_reason`: "The source returned no results on this run, so nothing was recorded and it was not charged." | 0 (full refund) |
| `track` monitor: none of the tracked metrics had a finite number | `failed`, `skip_reason`: "None of the tracked metrics had a value on this run, so it was not charged." | 0 (full refund) |
| Run crashed after the deduct | `failed` | 0 (refunded) |
| Prism composite reported partial coverage | `partial` | cost + 1 minus the recipe's partial refund |
| Success | `ok` | cost + 1 |

- A `track` run that comes back empty or with no tracked number is **re-fetched once, free**, before being refunded, if time remains in the run's 60-second budget. You are charged at most once per slot.
- `failed` and `skipped` runs fire no alert, send no webhook, and are never the comparison point for the next run's deltas.
- Monitor counters on GET: `runs_total`, `credits_spent` (net credits actually kept).

## Plan caps (active monitors per account)

Set by the **highest credit pack the account has ever bought**; if the plan lookup fails, the Free cap applies. Only `active` monitors count; paused ones do not. The cap is checked at create.

| Free | Starter | Growth | Pro | Enterprise |
| --- | --- | --- | --- | --- |
| 3 | 10 | 25 | 100 | 500 |

Over the cap: `403 MONITOR_LIMIT_REACHED`, e.g. "Active-monitor limit reached (10 on the Starter plan). Pause or delete a monitor to free a slot."

## Cadence and timing

- `"hourly"`: next top of the hour, UTC.
- `"daily"`: every 24 h from the creation instant (not midnight). First run = create time + 24 h.
- `"weekly"`: every 7 days from the creation instant. First run = create time + 7 days.
- `{ "cron": "<5 fields>" }`: UTC. Fields minute hour day-of-month month day-of-week (0 = Sunday). Supports `*`, numbers, lists `a,b`, ranges `a-b`, steps `*/n` / `a-b/n`. **No names** (`MON`, `JAN`), no `@daily`, no seconds field. If both day fields are restricted, either matching fires (standard cron). Must fire at least once in the next 366 days. 1 to 120 chars.
- **One-hour floor.** A cron that fires more often is accepted with a `warnings[]` entry ("cadence fires more often than the 60-minute minimum interval; runs will be throttled to the floor.") and each next slot is pushed to at least 1 h after the previous slot (or after create).
- **There is no immediate first run on create.** The first run is at `next_run_at`, returned by create. There is no "run now" endpoint.
- The scheduler sweeps due monitors **every 15 minutes**, so a run executes up to ~15 min after its slot. `scheduled_for` on a run is the slot, not the execution time.
- Missed slots are not replayed: after a pause (or outage) the monitor runs once on the next sweep and the following slot is rolled forward past the current time.

## POST /v1/monitors: create a monitor

Body (JSON). Unknown top-level keys are ignored; unknown keys inside `track` are a 400.

**Validate and price without creating:** add `?dry_run=1` (or `"dry_run": 1` in the body) to create, PATCH or DELETE. It runs the same checks (same 400s), writes nothing and returns `{ valid, normalized_body, estimate }` with `estimated_monthly_cost`. Only where `GET /v1/utility/estimate?id=monitors` answers (a 404 there means an older server that ignores `dry_run` here and **creates the monitor**).

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `recipe` | string, 1-200 | yes | Endpoint path without `/v1/`, e.g. `tiktok/profile`, `instagram/audio/reels`, `prism/brand-mentions`, `search/everywhere`. Must be registered, not disabled, and **GET**. The POST batch endpoints (`prism/post-stats`, `prism/comment-lookup`, `prism/profiles`, `youtube/transcripts`, `youtube/videos`, `youtube/channels`) are refused. |
| `params` | object | no (default `{}`) | The recipe's query params, frozen and replayed every run (values sent as strings). Required params and `oneOf` groups must be present. Validated at create with the **same checks `/v1/{recipe}` runs**: a value `/v1` would 400 is a free 400 here, nothing created. Pass a bare handle (`nasa`, not a profile URL). A value `now-<N>d` is resolved each run to the UTC date N days ago (`YYYY-MM-DD`), for rolling windows. |
| `cadence` | `"hourly"` \| `"daily"` \| `"weekly"` \| `{ "cron": string }` | yes | See above. |
| `webhook_url` | string, ≤2048 | yes, **unless `track` is set** | `https` only, public host (loopback, `localhost`, private 10/8, 172.16/12, 192.168/16, 169.254/16, 0/8, IPv6 `::1`/`fe80:`/`fc`/`fd` refused). |
| `track` | object | no | Makes a numbers-only monitor. See [track](#track-numbers-only-monitors). |
| `webhook_format` | `"full"` \| `"rows"` | no (default `"full"`) | `"rows"` requires `track`. Not allowed without `webhook_url`. |
| `webhook_secret` | string, 8-200 | no | Your own signing secret. Otherwise a `whsec_` + 48-hex secret is generated. Not allowed without `webhook_url`. |
| `name` | string, 1-200 | no | Default `"<recipe> monitor"`. |
| `alert_rules` | array | no (default `[]`) | `[{ "metric", "op", "value", "window"? }]`. See [Alert rules](#alert-rules). |
| `suppress_webhook_unless_alert` | boolean | no (default `false`) | Deliver only runs where at least one rule fired. |
| `output_schema` | object | no | **Stored and echoed back on GET only. It does not shape the payload or the stored result.** |

Response `201`:

```json
{
  "monitor": {
    "id": "Xk3v9QmT2bLr8NwPz5Hc1",
    "name": "instagram/audio/reels monitor",
    "recipe": "instagram/audio/reels",
    "params": { "audio_id": "1581178662912126" },
    "cadence": "daily",
    "status": "active",
    "alert_rules": [],
    "estimated_cost_per_run": 2,
    "estimated_monthly_cost": 60,
    "next_run_at": "2026-10-03T09:12:44.000Z",
    "warnings": [],
    "track": { "metrics": ["total"], "row_key": null, "max_rows": 100 },
    "webhook_format": "full"
  },
  "webhook_secret": null
}
```

- IDs are 21-char alphanumeric strings with no prefix.
- `webhook_secret` is returned **once**, here; it is `null` for a download-only monitor. It cannot be read again (GET shows `signing_secret_hint: "whsec_…"`). Lost it: delete and recreate, passing your own `webhook_secret`.
- `warnings[]` carries cron-floor and `track` "could not be checked" notices. Always surface them.
- `track` is `null` on a legacy monitor.

```bash
# Numbers-only, download-only: a sound's reel count once a day (2 credits/run)
curl -X POST "https://www.socialcrawl.dev/v1/monitors" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipe": "instagram/audio/reels",
    "params": { "audio_id": "1581178662912126" },
    "cadence": "daily",
    "track": { "metrics": ["total"] },
    "alert_rules": [{ "metric": "total", "op": "pct_change_gt", "value": 10 }]
  }'

# Numbers-only per video, delivered as spreadsheet rows
curl -X POST "https://www.socialcrawl.dev/v1/monitors" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipe": "tiktok/profile/videos",
    "params": { "handle": "khaby.lame" },
    "cadence": "daily",
    "track": { "metrics": ["items[].post.engagement.views", "items[].post.engagement.likes"] },
    "webhook_url": "https://example.com/hooks/socialcrawl",
    "webhook_format": "rows"
  }'

# Legacy: full Prism body every week to a webhook (31 credits/run)
curl -X POST "https://www.socialcrawl.dev/v1/monitors" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "recipe": "prism/reputation",
    "params": { "brand": "acme" },
    "cadence": { "cron": "0 9 * * 1" },
    "webhook_url": "https://example.com/hooks/socialcrawl"
  }'
```

## `track`: numbers-only monitors

```json
"track": { "metrics": ["items[].post.engagement.views"], "row_key": "post.id", "max_rows": 100 }
```

| Field | Type | Notes |
| --- | --- | --- |
| `metrics` | string[], 1-20, each ≤200 chars | Paths to numbers on the unified page. Duplicates are dropped. |
| `row_key` | string | Dot path inside a row to its stable id (no `items[]` prefix). Defaults to `post.id` (PostList), `comment.id` (CommentList), `author.id` (AuthorList). **Required** for any other list (e.g. `product.id` on a ProductList) and for `items[]` paths on Prism/meta composites. Must sit under the row's wrapper (`post.` on a PostList). |
| `max_rows` | integer 1-200 | Rows kept per run, in page order. Default 100. |

**Path syntax.** Segments are `[A-Za-z0-9_]`, at most 8, joined by `.`. No array indexes, no nested `[]`.
- `items[].<path>`: one number per row of a list page; `<path>` is relative to the row, which is wrapped (`items[].post.engagement.views`, not `items[].engagement.views`). Rows are keyed by `row_key`; rows whose id does not resolve are dropped; a repeated id keeps its first occurrence.
- `<path>`: one number off the page itself (`total`, `author.followers`), stored under the row id `_`.

**Validated at create, free, never calls an upstream.** Each path must land on a **numeric leaf** of the recipe's unified schema:
- Unknown path: 400 with the closest real one, e.g. `track.metrics: 'totl' is not a field of the instagram/audio/reels page (PostList). Did you mean 'total'?` or `... 'items[].post.engagement.veiws' is not a field of a row of instagram/audio/reels (PostList). Did you mean 'items[].post.engagement.views'?`
- Missing row wrapper: 400 `rows of <recipe> (PostList) are shaped { post, computed }, so 'items[].engagement.views' does not resolve. Did you mean 'items[].post.engagement.views'?`
- A string / boolean leaf: 400 "... is a boolean on <recipe> (...), not a number, so it cannot be tracked." (lists numeric siblings). An object: 400 naming a number inside it.
- `items[]` on a single-object recipe (e.g. `tiktok/profile`): 400, use a dot path like `author.followers`.
- `computed.relevance`, `computed.labels`, `computed.labels_evidence`: 400 (only filled by a live request's judge; a monitor would store null forever).
- **Cannot be checked** (Prism / meta composites, pages with no canonical schema, or a path inside an object whose keys vary by source such as `ext.*`): accepted with a `warnings[]` entry. Such a path stores `null` on any run where it does not resolve, so verify the first run.

**Stored per run** (`GET /runs?include=numbers`):

```json
"numbers": { "7412233": { "items[].post.engagement.views": 184000 }, "_": { "total": 1733 } },
"deltas": {
  "rows": { "7412233": { "items[].post.engagement.views": { "prev": 171500, "cur": 184000, "abs": 12500, "pct": 7.29 } } },
  "rows_new": ["7419981"],
  "rows_gone": []
}
```

A leaf that is missing or not a finite number is stored as `null`, never guessed. `deltas` is `null` on the first run (no prior comparable run); `pct` is `null` when `prev` is 0; `abs`/`pct` are `null` if either side is null. Deltas compare against the newest earlier `ok`/`partial` run that has numbers.

## Alert rules

`{ "metric": string (1-200), "op": enum, "value": number, "window"?: "1d" | "1w" }`

- `op`: `gt`, `lt`, `gte`, `lte` (absolute threshold on this run's value); `abs_change_gt` (|cur - prev| > value), `pct_change_gt`, `pct_change_lt` (percent change vs prev, in percent, e.g. `10` = +10%; `-20` with `pct_change_lt` = dropped more than 20%).
- `rows_new` (a special metric, `track` monitors only): `{ "metric": "rows_new", "op": "gt", "value": 0 }` fires when this run has at least one list row the previous comparable run did not (the count is in `to`). Only `gt` and `gte` are accepted (400 otherwise, free). It needs an `items[].` metric in `track.metrics` (to have rows to count) but is not itself listed there. The first run has no baseline, so it never fires then. "New" means absent from the previous successful run's stored rows (capped at `max_rows`, default 100), so a row that drops off and later returns counts as new again. On a sparse feed an empty-page run is refunded and is not a baseline, so the first run that holds rows has no baseline and stays silent: the first new post after a quiet period may not alert. Use a daily cadence or leave `max_rows` headroom. A legacy monitor (no `track`) cannot use it: 400.
- Change ops compare against the **previous comparable run** (newest earlier `ok`/`partial` run with data). `window` is accepted and stored but **not used** by the evaluator today; it does not change which run is compared.
- No prior run, a path that does not resolve to a finite number, or a 0 baseline for a `pct_*` op: the rule is skipped silently for that run (it never fires on a guess).
- **Legacy monitor:** `metric` is a dot path into the stored body (`coverage`, not `result.coverage`). For a single-platform endpoint that body is the supplier's raw response, so field names are NOT the unified ones. Read `GET /timeseries` after the first run to see the exact keys, and copy one. With `suppress_webhook_unless_alert: true`, a typo makes the monitor silent forever.
- **`track` monitor:** `metric` must be one of `track.metrics`, or `rows_new` (400 otherwise, free). An `items[].` rule is evaluated per row against that row's previous number and each fired alert carries `row_id`; new rows are skipped for change ops.

### Recipe: alert me on new posts or videos

```json
{
  "recipe": "youtube/channel/videos",
  "params": { "handle": "mkbhd", "since": "now-7d" },
  "cadence": "weekly",
  "webhook_url": "https://example.com/hooks/socialcrawl",
  "track": { "metrics": ["items[].post.engagement.views"] },
  "alert_rules": [{ "metric": "rows_new", "op": "gt", "value": 0 }],
  "suppress_webhook_unless_alert": true
}
```

The webhook is called only on a run that holds a row the previous run did not; the fired alert is `{ "metric": "rows_new", "op": "gt", "from": null, "to": 1, "delta": null, "pct_change": null }`, and `deltas.rows_new` lists the new row ids. A misspelling such as `new_rows` is rejected with a "Did you mean 'rows_new'" message.

Fired alert object (in `alerts_fired` on the run and the webhook):

```json
{ "metric": "total", "op": "pct_change_gt", "from": 1500, "to": 1733, "delta": 233, "pct_change": 15.53, "row_id": "7412233" }
```

`from`, `delta`, `pct_change` are `null` for absolute ops. `row_id` only on a per-row `items[].` rule.

## GET /v1/monitors: list your monitors

Account-scoped, newest first, cursor-paginated.
- `status` (optional, enum: `active` | `paused` | `all`). **Omitted = `active` only**; paused monitors need `status=paused` or `all`.
- `cursor` (optional, string): the `next_cursor` from the previous page.
- `limit` (optional, integer, 1 to 100, default 20).

Response `{ "monitors": [Monitor...], "next_cursor": string | null }`. In the list, `webhook` is always `null`; GET one monitor to see its webhook state.

```bash
curl "https://www.socialcrawl.dev/v1/monitors?status=all&limit=50" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/monitors/{id}: get one monitor

404 `RESOURCE_NOT_FOUND` if it does not exist or belongs to another account (existence is never leaked). The signing secret is never returned.

Monitor fields: `id`, `name`, `recipe`, `params`, `cadence`, `status` (`active` | `paused`), `output_schema`, `alert_rules`, `suppress_webhook_unless_alert`, `track` (`{metrics, row_key, max_rows}` or `null`), `webhook_format`, `webhook` (`{ url, status: "active" | "paused", failure_count, last_delivery_at, signing_secret_hint: "whsec_…" }` or `null` when download-only), `estimated_cost_per_run`, `estimated_monthly_cost` (recomputed at read time from current pricing), `runs_total`, `credits_spent`, `next_run_at`, `created_at`, `updated_at`.

```bash
curl "https://www.socialcrawl.dev/v1/monitors/$MONITOR_ID" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/monitors/{id}/runs: run history

Newest first, cursor-paginated.
- `status` (optional, enum: `ok` | `partial` | `failed` | `skipped`)
- `from` / `to` (optional, ISO 8601; filter on `scheduled_for`, inclusive)
- `cursor` (optional, string), `limit` (optional, integer, 1 to 100, default 20)
- `include` (optional, comma-separated `result`, `numbers`): `result` adds the stored body (legacy; always `null` on a `track` monitor), `numbers` adds `numbers` + `deltas` (`track` monitors). Anything else is a 400.

Response `{ "runs": [Run...], "next_cursor": string | null }`. Run fields:

| Field | Notes |
| --- | --- |
| `id`, `monitor_id` | |
| `status` | `ok` \| `partial` \| `failed` \| `skipped` |
| `scheduled_for`, `started_at`, `finished_at` | ISO 8601 |
| `credits_used` | Net credits kept for this run (0 for failed/skipped) |
| `legs` | `track` monitor: `[{ "rung": "primary" \| "fallback", "rung_index": 0, "status": 200, "warnings": [] }]`; `rung_index` 0 is the primary source, a fallback can leave a number empty that the primary fills. Supplier names never appear. Legacy: the recipe's own `legs[]` or `[]`. |
| `alerts_fired` | Array of fired alert objects |
| `webhook_delivery` | `null` until the delivery settles, then `{ attempts, lastStatus, deliveredAt, failedAt }` (the HTTP status your endpoint returned) |
| `skip_reason` | `"insufficient_credits"` on `skipped`; the empty-page / no-tracked-value sentences above on refunded `track` runs; on a recipe error, a sentence such as "Run failed with HTTP 404 RESOURCE_NOT_FOUND. The source found no account or item for the Monitor's params. Nothing was recorded and the run was not charged." (codes: 400/422 `INVALID_REQUEST`, 404 `RESOURCE_NOT_FOUND`, 429/503 `SERVICE_UNAVAILABLE`, 408/504/other `UPSTREAM_ERROR`, crash `INTERNAL_ERROR`). The recipe-error sentence is newer than the rest; older failed runs have `skip_reason: null`. Treat it as human-readable text, do not parse it. `null` on `ok`/`partial`. |
| `result` / `numbers`, `deltas` | Only with `include=` |

```bash
curl "https://www.socialcrawl.dev/v1/monitors/$MONITOR_ID/runs?include=numbers&limit=50" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/monitors/{id}/timeseries: the headline read

Reads stored runs only (no live call, 0 credits). Reads at most the **newest 1,000 runs** in the window, returned oldest first; narrow with `from`/`to` for older history.
- `metric` (optional, comma-separated keys to keep)
- `from` / `to` (optional, ISO 8601)
- `row` (optional, `track` only: comma-separated row ids to keep in `series`)

Response `{ "monitor_id", "metric_keys", "points": [{ "t", "metrics": { key: number } }], "next_cursor": null }`, plus on a `track` monitor `"series": [{ "row_id", "metric", "points": [{ "t", "value" }] }]` and `"series_truncated"` (true when the 100,000-point cap cut it; narrow with `row`, `metric`, `from`/`to`).
- **Legacy:** reads `ok` runs only. `metric_keys` defaults to the numeric leaves auto-discovered in the newest stored body (nested objects only, never arrays, first 50).
- **`track`:** reads `ok`/`partial` runs with numbers. `metric_keys` defaults to `track.metrics`. `points` carries only page-level numbers (row `_`); per-row numbers are in `series`.

```bash
curl "https://www.socialcrawl.dev/v1/monitors/$MONITOR_ID/timeseries?metric=total&from=2026-09-01T00:00:00Z" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/monitors/{id}/export: download the numbers

Streams the stored numbers as a file, 0 credits. One line per run x row x metric, oldest run first, same 1,000-run bound.
- `format` (optional, `csv` | `ndjson`, default `csv`)
- `from` / `to` (optional, ISO 8601; an unparseable date is a 400)

CSV header `t,row_id,metric,value,abs_change,pct_change` (empty cell = null); NDJSON has the same keys. `Content-Disposition: attachment; filename="monitor-<id>.<format>"`. A legacy monitor exports the same numeric leaves `/timeseries` finds, under row `_`; if its stored bodies have no numeric leaf, 400 "The stored results of this monitor have no numeric fields to export. Create a monitor with track to store and export per-row numbers."

```bash
curl "https://www.socialcrawl.dev/v1/monitors/$MONITOR_ID/export?format=csv" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" -o monitor.csv
```

## PATCH /v1/monitors/{id}: pause / resume

Body: exactly `{ "status": "paused" }` or `{ "status": "active" }` (anything else: 400 "status must be active or paused."). Nothing else about a monitor can be edited; to change recipe, params, cadence, track, rules or webhook, delete and recreate. Response `{ "id", "status" }`. A paused monitor does not run or bill and does not count toward the cap. On resume it runs at the next sweep (missed slots are not replayed).

```bash
curl -X PATCH "https://www.socialcrawl.dev/v1/monitors/$MONITOR_ID" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "status": "paused" }'
```

## DELETE /v1/monitors/{id}: delete

Hard delete: unschedules and cascade-deletes the monitor's runs (all stored history) and webhook. Export first if the history matters. Returns `204 No Content`; 404 if not found / not yours.

```bash
curl -X DELETE "https://www.socialcrawl.dev/v1/monitors/$MONITOR_ID" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## Webhook delivery

Sent only for `ok` and `partial` runs, only while the webhook is `active`, and not when `suppress_webhook_unless_alert` is true and no rule fired. `failed` and `skipped` runs never deliver. There is no test-fire endpoint.

**Legacy payload** (`full`):

```json
{
  "monitor_id": "Xk3v9QmT2bLr8NwPz5Hc1",
  "run_id": "q7Lw2Nc9Rt4Yb8Zp1Hd6K",
  "recipe": "search/everywhere",
  "status": "ok",
  "scheduled_for": "2026-10-03T09:00:00.000Z",
  "alerts_fired": [],
  "result": { "...": "the stored recipe body" },
  "deltas": { "coverage": -0.18 }
}
```

`deltas` = current minus previous comparable run for each auto-discovered numeric leaf; `{}` on the first run.

**`track` monitor, `webhook_format: "full"`:** same keys, but `result` is the unified canonical page (delivered, **never stored**), `deltas` is the per-row delta object (or `null` on the first run), plus `numbers` (what was stored).

**`track` monitor, `webhook_format: "rows"`:** flat rows for a spreadsheet:

```json
{
  "monitor_id": "...", "run_id": "...", "recipe": "tiktok/profile/videos", "status": "ok",
  "scheduled_for": "2026-10-03T09:00:00.000Z", "alerts_fired": [],
  "rows": [
    { "t": "2026-10-03T09:00:00.000Z", "row_id": "7412233", "metric": "items[].post.engagement.views",
      "value": 184000, "prev": 171500, "abs_change": 12500, "pct_change": 7.29 }
  ]
}
```

**Signature.** Header `x-socialcrawl-signature: t=<unix seconds>,v1=<hex>`, where `v1 = HMAC-SHA256(secret, "<t>.<rawBody>")`. Verify against the **raw** body bytes (re-serialized JSON breaks it), compare in constant time (check lengths first), and enforce a replay window on `t` (e.g. 300 s). Same scheme as billing webhooks.

```js
import crypto from "node:crypto";
function verify(rawBody, header, secret, toleranceSec = 300) {
  const p = Object.fromEntries(header.split(",").map((kv) => { const i = kv.indexOf("="); return [kv.slice(0, i), kv.slice(i + 1)]; }));
  const t = Number(p.t);
  if (!Number.isFinite(t) || Math.abs(Date.now() / 1000 - t) > toleranceSec) return false;
  const expected = crypto.createHmac("sha256", secret).update(`${t}.${rawBody}`).digest("hex");
  const a = Buffer.from(p.v1 ?? "", "hex"), b = Buffer.from(expected, "hex");
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
```

```python
import hashlib, hmac, time
def verify(raw_body: bytes, header: str, secret: str, tolerance=300) -> bool:
    p = dict(kv.split("=", 1) for kv in header.split(","))
    try: t = int(p["t"])
    except (KeyError, ValueError): return False
    if abs(int(time.time()) - t) > tolerance: return False
    expected = hmac.new(secret.encode(), f"{t}.".encode() + raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(p.get("v1", ""), expected)
```

**Retries and auto-pause.** Up to 6 attempts per run (initial + 5 retries, exponential backoff). Any non-2xx or timeout is a failed attempt. A run whose attempts are all exhausted counts as one failed delivery; a successful delivery resets the count to 0. After **10 consecutive failed deliveries the webhook (not the monitor) is paused**: the monitor keeps running and billing every slot, but delivers nothing. `GET /v1/monitors/{id}` shows `webhook.status: "paused"` and `failure_count`. There is no API to re-activate a paused webhook: pause the monitor to stop billing, then delete and recreate it with a working URL. Deliveries are at-least-once; de-duplicate on `run_id`.

## Errors

Monitors routes answer errors as `{ "error": { "type", "message" } }` (a body-validation 400 also carries `issues[]`).

| Status | `type` | When |
| --- | --- | --- |
| 400 | `INVALID_REQUEST` | Invalid JSON; schema violation; unknown / disabled / non-GET recipe; missing required params ("Missing required parameter(s) for '<recipe>': handle."); a param `/v1` would refuse ("params for '<recipe>': ... The monitor was not created ..."); bad `track` path / `row_key`; alert metric not in `track.metrics`; `webhook_url` missing without `track`; `webhook_secret`/`webhook_format` without `webhook_url`; `rows` without `track`; webhook URL not https / not public / >2048; bad cadence (`INVALID_CRON: ...`, `INVALID_CADENCE: ...`); bad `include` / `status` / `limit` query ("Invalid query."); bad PATCH body; export date or format; legacy export with no numbers. All free. |
| 403 | `MONITOR_LIMIT_REACHED` | Active-monitor cap reached for the plan. |
| 404 | `RESOURCE_NOT_FOUND` | "Monitor not found." (missing or another account's). |
| 401 / 429 / 503 | `MISSING_API_KEY`, `INVALID_API_KEY` / `CONCURRENCY_LIMIT` / `SERVICE_UNAVAILABLE` | Same `x-api-key` and concurrency middleware as `/v1` (standard `/v1` error envelope; honor `Retry-After` on 429). |

## Agent checklist

1. Pick the recipe and confirm its params with a normal `/v1` call first (that call costs credits; monitor create is free and also rejects bad params).
2. Want numbers over time? Use `track`. Create returns 400 with "Did you mean" for a wrong path; fix and retry. Read `warnings[]`.
3. Tell the user `estimated_cost_per_run` and `estimated_monthly_cost`, and that the first run is at `next_run_at` (daily = 24 h after create), not now.
4. After the first slot, check `GET /runs?include=numbers` (or `include=result`): a `failed` run's `skip_reason` says why, and `legs` shows which step answered.
5. Webhook users: store `webhook_secret` from the create response immediately; verify every delivery; de-dupe on `run_id`.
6. To stop spending: `PATCH {"status":"paused"}` or `DELETE` (DELETE erases history; export first).
