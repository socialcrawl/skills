# Universal Search

1 endpoint. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: the single endpoint costs a FLAT 20 credits (override — not the standard 1/5/10 ladder) — exact cost listed per endpoint below.

`/v1/search/everywhere` is a meta-search endpoint that fans out a single query across **up to 15 sources in parallel** — `reddit`, `twitter-ai-search`, `youtube`, `tiktok`, `instagram`, `hackernews`, `polymarket`, `github`, `threads`, `pinterest`, `perplexity`, `tavily`, plus tiktok/instagram/youtube hashtag siblings in hashtag mode — then fuses, reranks, and clusters the results server-side. It collapses what would otherwise be a dozen separate `/v1/{platform}/{resource}` calls into one billable request.

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
