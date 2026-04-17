# SocialCrawl API Overview

## Base URL

```
https://www.socialcrawl.dev
```

## Authentication

Pass your API key in the `x-api-key` header with every request:

```bash
curl -s -H "x-api-key: sc_your_api_key_here" \
  "https://www.socialcrawl.dev/v1/tiktok/profile?handle=charlidamelio"
```

## Response Format

All successful responses follow this envelope:

```json
{
  "success": true,
  "platform": "tiktok",
  "endpoint": "/v1/tiktok/profile",
  "data": { ... },
  "credits_used": 1,
  "credits_remaining": 4999,
  "request_id": "req-XXXXX",
  "cached": false
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "type": "INSUFFICIENT_CREDITS",
    "message": "Your account has 0 credits remaining. This endpoint requires 1 credits.",
    "status": 402,
    "doc_url": "https://socialcrawl.dev/docs/errors/insufficient-credits"
  },
  "credits_remaining": 0,
  "request_id": "req-XXXXX"
}
```

## Response Headers

| Header | Value |
|--------|-------|
| X-Request-Id | Unique request identifier (`req-XXXXX`) |
| X-Credits-Used | Credits consumed by this request (`0` on cache hit, idempotent replay, or refunded error) |
| X-Credits-Remaining | Balance after deduction |
| X-Cache | `HIT` or `MISS` |
| X-Idempotent-Replay | `"true"` when the request was served as an idempotent replay. Absent otherwise. |
| Retry-After | `"30"` (seconds) — only on 503 circuit-breaker responses |
| Allow | `"GET"` — only on 405 `METHOD_NOT_ALLOWED` responses |

## Credit Tiers

| Tier | Cost | Count | Typical endpoints |
|------|------|-------|-------------------|
| standard | 1 credit | 84 endpoints | Profiles, posts, search, comments |
| advanced | 5 credits | 18 endpoints | Audience, ad libraries, trending |
| premium | 10 credits | 6 endpoints | Transcripts, AI analysis |

Total: **108 endpoints across 21 platforms.**

## Credit Balance

Check remaining credits via the public, API-key-authed meta endpoint:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/credits/balance"
```

Returns the standard envelope:

```json
{
  "success": true,
  "platform": "meta",
  "endpoint": "/v1/credits/balance",
  "data": {
    "balance": 8432,
    "recent_deductions": { "last_24h": 128, "last_7d": 1043 }
  },
  "credits_used": 0,
  "credits_remaining": 8432,
  "request_id": "req-XXXXX",
  "cached": false
}
```

This call costs **0 credits** and is never cached (`Cache-Control: no-store`). The dashboard UI uses a separate session-authed `/api/credits/balance` route — programmatic callers must use `/v1/credits/balance`.

## Unified Schema & Computed Fields

Author and Post endpoints for 13 platforms go through platform-specific field maps that normalize upstream JSON into a single schema. When a field map applies, four computed fields are added under `data.computed`:

| Field | Type | Author formula | Post formula |
|-------|------|---------------|-------------|
| `engagement_rate` | `number \| null` | `likes_count / followers` (clamped `[0, 1]`) | `(likes + comments + shares) / views` (clamped `[0, 1]`) |
| `language` | `string \| null` | ISO 639-1 detected from `bio` (franc-min trigram) | ISO 639-1 detected from `post.content.text` |
| `content_category` | `string` | Keyword-based (15 categories) | Keyword-based (15 categories) |
| `estimated_reach` | `number \| null` | `round(followers * engagement_rate * 0.1)` when `engagement_rate` non-null, else `null` | `round(views * 1.2)` when `views > 0`, else `null` |

**Null semantics.** `engagement_rate` returns `null` when the divisor or numerator is missing/zero (never `Infinity`, `NaN`, or negatives). Raw ratios >1.0 (possible when upstream `views` under-reports impressions) are clamped to 1.0 with a `_warnings` entry. `estimated_reach` returns `null` whenever `engagement_rate` is null — post variant does **not** fall back to a follower-based estimate.

**Instagram author fallback.** Instagram `Author` responses without upstream `total_likes` fall back to the mean likes+comments across the inline post list, so IG creators get a real `engagement_rate` instead of 0.

**Language detection.** Uses `franc-min` (82 languages, ISO 639-3 → 639-1). Unicode fast-path for Korean, Japanese, Chinese, Arabic, Devanagari, and Thai. Minimum input length 10 chars — shorter text returns `null`. Known limitation: Persian (Farsi) text written in Arabic script detects as `ar`.

Unified **Author** schema: `id`, `username`, `display_name`, `avatar_url`, `bio`, `url`, `verified`, `private`, `followers`, `following`, `posts_count`, `likes_count`, `joined_at`.

Unified **Post** schema: `id`, `content.text`, `content.media_urls`, `content.thumbnail_url`, `content.duration_seconds`, `author.username`, `author.display_name`, `author.avatar_url`, `author.verified`, `engagement.views`, `engagement.likes`, `engagement.comments`, `engagement.shares`, `engagement.saves`, `published_at`.

Endpoints that return lists (PostList, CommentList, SearchResult, Analytics, Audience) are currently passthrough for computed fields — they **do** go through the upstream-envelope stripper, which normalises list responses to `{ items, next_cursor?, total? }` regardless of the upstream key name (`posts | videos | tweets | aweme_list | media_data | data | ...`).

## Response Warnings (`data._warnings`)

Successful responses may include an optional `data._warnings: string[]` aggregating non-fatal notices from the transform pipeline:

- Field-mapper warnings when a declared source path fails to resolve against upstream.
- Computed-field warnings (e.g. `"computed.engagement_rate: value exceeded 1.0 (raw: N.NNN); clamped"`).

The array is **advisory** — do not flip success, gate retries, or treat it as an error signal. Empty arrays are omitted from the response.

## Parameter Validation

Every request is validated before any credit is deducted:

1. **Required params (`params[]`)** — every listed name must be present and non-empty.
2. **`oneOf` groups** — endpoints like `GET /v1/youtube/channel` accept `channelId` or `handle` or `url`; at least one member must be present. The platform reference files list these groups.
3. **Optional params** — forwarded to upstream only when provided, ignored otherwise.
4. **Per-platform format validators** — handle, URL, and subreddit strings are checked against platform-specific regexes before the upstream call. Obvious garbage (SQL-ish strings, 512-char handles, URLs from the wrong platform) is rejected at the boundary in <100ms with no credit deducted.

A failing request returns `400 INVALID_REQUEST` with either `Missing required parameter(s): ...` (for rules 1-3) or a format message (for rule 4).

## Raw Format

Add `?format=raw` to any endpoint to receive the original upstream response without unified schema transformation or computed fields:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tiktok/profile?handle=charlidamelio&format=raw"
```

## Caching

Responses are cached by deterministic key (platform + resource + sorted query params). Cache category TTLs:

| Category | TTL |
|----------|-----|
| profile | 15 min |
| post | 10 min |
| comments | 5 min |
| search | 2 min |
| analytics | 30 min |

**Cache hits are free.** Serving from cache deducts **0 credits** — the balance is unchanged, `X-Credits-Used: 0`, and `X-Cache: HIT` / `cached: true` indicate the hit. Rationale: we already paid upstream for the first call that produced the cached body. If the cached body is empty (resource has since been deleted), the empty-upstream guard fires and returns `404 RESOURCE_NOT_FOUND` (no credit impact).

## Idempotent Retries

Any `/v1/*` call can be made safely retryable by sending an `Idempotency-Key` header (UUIDv4 or any opaque 16+ char string):

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Idempotency-Key: 7a5e1b4c-2d8f-4a3b-9c1e-6e8b4d2a1f3c" \
  "https://www.socialcrawl.dev/v1/tiktok/profile?handle=charlidamelio"
```

Lookup outcomes for `(user_id, key)`:

| Outcome | HTTP | Credits | Notes |
|---------|------|---------|-------|
| First call | (normal) | cost | Response is stored; 24h TTL |
| Replay (same key, same params) | 200 with stored body | 0 | `X-Idempotent-Replay: true` |
| Payload mismatch (same key, different params) | 422 `IDEMPOTENCY_KEY_PAYLOAD_MISMATCH` | 0 | Use a fresh key |
| Conflict (same key, different account) | 409 `IDEMPOTENCY_KEY_CONFLICT` | 0 | Pick a new key |

Requests without an `Idempotency-Key` header skip this subsystem entirely.

## Empty-Upstream Guard

Some upstream endpoints return HTTP 200 with an all-null payload for nonexistent handles/posts (IG, TikTok, Twitter, Snapchat, Reddit, Kick, Twitch). An archetype-aware guard catches this after transform:

- **Author**: `id` AND `username` both missing → empty.
- **Post**: `id` missing AND all engagement counts (`views`, `likes`, `comments`, `shares`) missing → empty.
- **List variants**: `items.length === 0` → empty.

When the guard trips, the credit is **auto-refunded** and the response is `404 RESOURCE_NOT_FOUND`. This also fires on cache hits of previously-empty bodies.

## Circuit Breaker & Refunds

Each platform has a per-instance circuit breaker (5 failures in 60s → open for 30s). When open, requests return `503 SERVICE_UNAVAILABLE` with `Retry-After: 30` and credits are auto-refunded. Upstream 5xx errors (`502 UPSTREAM_ERROR`), empty-upstream bodies (`404 RESOURCE_NOT_FOUND` via the BIL-01 guard), and internal errors (`500 INTERNAL_ERROR`) also auto-refund. Cache hits, `405`, `409`, and `422` never deduct credits so no refund is needed. Check live platform health:

```bash
curl -s "https://www.socialcrawl.dev/v1/status"
```

## Error Codes

| Code | Status | Description | Credits |
|------|--------|-------------|---------|
| MISSING_API_KEY | 401 | No x-api-key header | Not charged |
| INVALID_API_KEY | 401 | Key malformed, not found, or revoked | Not charged |
| INSUFFICIENT_CREDITS | 402 | Balance too low | Not charged |
| INVALID_REQUEST | 400 | Missing required params OR malformed handle/URL (format validator) | Not charged |
| METHOD_NOT_ALLOWED | 405 | Non-GET request on `/v1/*`. Response includes `Allow: GET`. | Not charged |
| ENDPOINT_NOT_FOUND | 404 | Unknown platform or resource | Not charged |
| RESOURCE_NOT_FOUND | 404 | Item not found on platform (includes empty-upstream guard) | Refunded when guard trips |
| IDEMPOTENCY_KEY_CONFLICT | 409 | `Idempotency-Key` owned by a different account | Not charged |
| IDEMPOTENCY_KEY_PAYLOAD_MISMATCH | 422 | `Idempotency-Key` reused by the same account with different params | Not charged |
| CONCURRENCY_LIMIT | 429 | Over 50 concurrent requests per key | Not charged |
| UPSTREAM_ERROR | 502 | Platform returned an error | Refunded |
| SERVICE_UNAVAILABLE | 503 | Circuit breaker open, retry in 30s | Refunded |
| INTERNAL_ERROR | 500 | Unexpected server error | Refunded |

Error envelopes include a `doc_url` pointing at `https://www.socialcrawl.dev/docs/errors/<code>` for the human-readable explainer.
