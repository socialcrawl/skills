# Universal Search

2 endpoints. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: both endpoints use flat overrides (not the standard 1/5/10 ladder) — `/v1/search/everywhere` is a FLAT 20 credits and `/v1/search/forums` is a FLAT 10 credits — exact cost listed per endpoint below.

Universal Search offers two fan-out lanes:

- **`/v1/search/everywhere`** — the wide lane. Fans out a single query across **up to 15 sources in parallel** — `reddit`, `twitter-ai-search`, `youtube`, `tiktok`, `instagram`, `hackernews`, `polymarket`, `github`, `threads`, `pinterest`, `perplexity`, `tavily`, plus tiktok/instagram/youtube hashtag siblings in hashtag mode — then fuses, reranks, and clusters the results server-side. It collapses what would otherwise be a dozen separate `/v1/{platform}/{resource}` calls into one billable request.
- **`/v1/search/forums`** — the discussion lane. A fused forum search across Reddit, Hacker News, and Naver 지식iN/카페, with top comments inline on hero threads by default — for voice-of-customer and Q&A research without the wide-lane breadth or price.

## GET /v1/search/everywhere — 20 credits (flat override)

Universal social search across 12 platforms

- `query` (required) — Search query (1–512 chars)
- `lookback_days` (optional, integer) — Days to look back (1–365+, default 30); mutually exclusive with from_date/to_date.
- `from_date` (optional, string) — ISO YYYY-MM-DD lower bound; mutually exclusive with lookback_days.
- `to_date` (optional, string) — ISO YYYY-MM-DD upper bound; defaults to today when from_date is set alone.
- `sources` (optional, string) — Optional CSV allowlist of source names (mutually exclusive with exclude).
- `exclude` (optional, string) — Optional CSV blocklist of source names (mutually exclusive with sources).

```bash
curl "https://www.socialcrawl.dev/v1/search/everywhere?query=kanye west" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## Response modes

The `Accept` header decides the response shape — two modes:

### Sync mode — `Accept: application/json` (default)

Returns the standard envelope. `data` carries the ranked + clustered candidates plus per-source success/failure metadata.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/search/everywhere?query=claude+code"
```

### Streaming mode — `Accept: text/event-stream`

Returns a typed SSE stream as the pipeline progresses — plan, per-source, rerank, enrichment, and done chunks:

| Chunk | When |
|-------|------|
| `meta` | Immediately after parse — carries `request_id`, `query`, deterministic `plan`, `sources_planned`. |
| `source_started` | Before each source adapter starts. |
| `items` | Per source, on success. Carries `items[]` and `duration_ms`. |
| `source_failed` | Per source, on failure. Carries `{code, message}`. |
| `warning` | Advisory notice (e.g. `lookback_days > 90`). |
| `plan_refined` | LLM-refined plan replaces the deterministic plan (only when it differs). |
| `ranked_partial` | Per rerank batch — incremental scores. |
| `ranked_final` | Final ordered candidate list. |
| `comments_enriched` | Top comments for a single candidate, keyed by `candidate_id`. |
| `clusters` | When the query intent is clusterable. |
| `done` | Always last. Carries `summary` including `refunded: true\|false`. |
| `error` | Terminal on thrown error — paired with a `done(refunded: true)`. |

```bash
curl -N -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Accept: text/event-stream" \
  "https://www.socialcrawl.dev/v1/search/everywhere?query=claude+code"
```

## Billing & refunds

- **20 credits flat per call** — deducted before dispatch. Confirm with the user before executing.
- **Fully refunded when every source fails or returns empty** — partial results (at least one source returned items) are billable.

## More examples

Allowlist of sources:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/search/everywhere?query=AI+agents&sources=reddit,hackernews,github"
```

Streaming with date window:

```bash
curl -N -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Accept: text/event-stream" \
  "https://www.socialcrawl.dev/v1/search/everywhere?query=anthropic&from_date=2026-01-01&to_date=2026-04-30"
```

Excluding sources:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/search/everywhere?query=elections+2026&exclude=pinterest,polymarket"
```

## GET /v1/search/forums — 10 credits (flat override)

Fused forum search across Reddit, Hacker News, and Naver 지식iN/카페 — with top comments inline on hero threads by default.

- `query` (required) — Search query (2–256 chars), forwarded to every forum search.
- `sources` (optional, string) — Optional CSV allowlist of forum sources (`reddit`, `hackernews`, `naver_kin`, `naver_cafe`). Mutually exclusive with `exclude`.
- `exclude` (optional, string) — Optional CSV blocklist of forum sources. Mutually exclusive with `sources`.
- `comments` (optional, string) — Comment enrichment toggle (`on`|`off`, default `on`). `off` returns thread-only.
- `timeframe` (optional, string) — Recency window passed to Reddit; HN filtered client-side (`all`|`day`|`week`|`month`|`year`, default `all`).
- `lookback_days` (optional, integer) — Alt recency window in days (1–365); HN filtered client-side.

```bash
curl "https://www.socialcrawl.dev/v1/search/forums?query=airpods pro 3 battery" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
