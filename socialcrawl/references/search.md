# Universal Search (1 endpoint)

`/v1/search/everywhere` is a meta-search endpoint that fans out a single query across **12 platforms in parallel**, fuses the results with weighted RRF + LLM rerank, and returns either a sync JSON envelope or an SSE stream. It collapses what would otherwise be 12 separate `/v1/{platform}/{resource}` calls into one billable request with server-side parallelism, rich social signals (engagement, freshness, source quality), and per-candidate top-comment enrichment.

## Endpoint

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| everywhere | `query` | **flat 20 credits** | Cross-platform meta-search across 12 sources |

> **20 credits flat — confirm with the user before executing.** This is a tier override (`endpoint.cost: 20`), not the standard 1/5/10 ladder. Cache hits are still free; zero-floor (every source fails) auto-refunds.

## 12 sources

`reddit`, `twitter-ai-search`, `youtube`, `tiktok`, `instagram`, `hackernews`, `polymarket`, `github`, `threads`, `pinterest`, `perplexity`, `tavily`.

## Parameters

| Param | Required | Notes |
|-------|----------|-------|
| `query` | yes | Free-text search query — natural language is fine. |
| `sources` | no | CSV allowlist (e.g. `sources=reddit,youtube,hackernews`). Mutually exclusive with `exclude`. |
| `exclude` | no | CSV blocklist of sources to skip. Mutually exclusive with `sources`. |
| `lookback_days` | no | Recency window. Values >90 emit a `warning` chunk but are accepted. |
| `from_date` | no | ISO 8601 date lower bound. |
| `to_date` | no | ISO 8601 date upper bound. |

## Response modes

The `Accept` header decides the response shape.

### Sync mode — `Accept: application/json` (default)

Returns the standard envelope. `data` carries the ranked + clustered candidates plus per-source success/failure metadata. Cache TTL: 120s. Idempotency works as it does for every other endpoint.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/search/everywhere?query=claude+code"
```

### Streaming mode — `Accept: text/event-stream`

Returns typed SSE chunks as the pipeline progresses. **Bypasses cache** (a sync hit can never poison a stream). Idempotency replays cannot replay a stream — replays serve the cached sync envelope or 409.

```bash
curl -N -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Accept: text/event-stream" \
  "https://www.socialcrawl.dev/v1/search/everywhere?query=claude+code"
```

#### Chunk types

| Chunk | When |
|-------|------|
| `meta` | Immediately after parse — carries `request_id`, `query`, deterministic `plan`, `sources_planned`. TTFB <50ms. |
| `source_started` | Synchronously before each adapter starts. |
| `items` | Per source, on success. Carries `items[]` and `duration_ms`. |
| `source_failed` | Per source, on failure. Carries `{code, message}`. |
| `warning` | Advisory notice (e.g. `lookback_days > 90`). |
| `plan_refined` | LLM-refined plan replaces the deterministic plan (only when it differs). |
| `ranked_partial` | Per LLM rerank batch — incremental scores. |
| `ranked_final` | Final ordered candidate list. |
| `comments_enriched` | Top comments for a single candidate (Reddit, TikTok, Instagram, YouTube, HN, GitHub). Keyed by `candidate_id`. |
| `clusters` | When intent is clusterable (breaking_news, opinion, comparison, prediction). |
| `done` | Always last. Carries `summary` including `refunded: true|false`. |
| `error` | Terminal on thrown error — paired with a `done(refunded: true)`. |

## Algorithm pipeline

1. **Plan** — deterministic intent classifier + subquery fan-out (~5ms), races an LLM plan refinement in parallel (8s timeout).
2. **Fan-out** — 12 adapters concurrently, per-source 8s timeout (12s for `twitter-ai-search` and `perplexity`).
3. **Per-stream processing** — raw-map → normalize → annotate (relevance / freshness / engagement / source_quality) → dedupe.
4. **Fusion** — weighted RRF, per-author cap of 3, diversity floor of 2 per source.
5. **Comment enrichment** — top comments fetched in parallel with rerank for the top 40 candidates (rank-tiered: 15 for hero rows, 5 for tail).
6. **Rerank** — LLM (gpt-5.4-nano) with entity-grounding penalty, partial-on-timeout fallback to local scoring.
7. **Clustering** — greedy + MMR, only for clusterable intents.

All numeric tunings are server-locked — clients can't tune them per-request.

## Billing & refunds

- **20 credits per call** — flat override, deducted before dispatch.
- **Cache hits cost 0 credits** (sync only — streaming bypasses cache).
- **Zero-floor refund**: when the pipeline produces zero ranked items (every source either failed or returned empty), credits auto-refund. Sync uses the standard `!ok` router branch; streaming calls `billing.refund()` before the terminal `done(refunded: true)` chunk.
- **Partial results are billable.** If at least one source returned items, the call is charged.

## Known limitations

- **Pinterest is currently broken upstream** (verified live 2026-04-29) — returns empty `pins[]` for every query. Render the Pinterest section conditionally; don't surface as an error.
- **Twitter (twitter-ai-search) frequently times out** at the 12s slow-source budget. Lands in `sources_failed` as a silent partial failure — render conditionally, don't show as an error toast.
- **Truth Social and Bluesky aren't sources** — no `/search` endpoint upstream.
- **Streaming idempotency replay returns the sync envelope** if cached, otherwise 409.

## Examples

Sync, all sources:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/search/everywhere?query=claude+code"
```

Sync, allowlist:

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
