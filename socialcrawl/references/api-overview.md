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
| X-Credits-Used | Credits consumed by this request |
| X-Credits-Remaining | Balance after deduction |
| X-Cache | `HIT` or `MISS` |

## Credit Tiers

| Tier | Cost | Count | Typical endpoints |
|------|------|-------|-------------------|
| standard | 1 credit | 84 endpoints | Profiles, posts, search, comments |
| advanced | 5 credits | 18 endpoints | Audience, ad libraries, trending |
| premium | 10 credits | 6 endpoints | Transcripts, AI analysis |

Total: **108 endpoints across 21 platforms.**

## Credit Balance

Check remaining credits:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/api/credits/balance"
```

Returns: `{ "balance": 4999 }`

## Unified Schema & Computed Fields

Author and Post endpoints for 13 platforms go through platform-specific field maps that normalize upstream JSON into a single schema. When a field map applies, four computed fields are added under `data.computed`:

| Field | Author formula | Post formula |
|-------|---------------|-------------|
| `engagement_rate` | `likes_count / followers` | `(likes + comments + shares) / views` |
| `language` | ISO 639-1 detected from `bio` | ISO 639-1 detected from `post.content.text` |
| `content_category` | Keyword-based (15 categories) | Keyword-based (15 categories) |
| `estimated_reach` | `followers * engagement_rate * 0.1` | `views * 1.2` (fallback: `followers * engagement_rate * 0.15`) |

Unified **Author** schema: `id`, `username`, `display_name`, `avatar_url`, `bio`, `url`, `verified`, `private`, `followers`, `following`, `posts_count`, `likes_count`, `joined_at`.

Unified **Post** schema: `id`, `content.text`, `content.media_urls`, `content.thumbnail_url`, `content.duration_seconds`, `author.username`, `author.display_name`, `author.avatar_url`, `author.verified`, `engagement.views`, `engagement.likes`, `engagement.comments`, `engagement.shares`, `engagement.saves`, `published_at`.

Endpoints that return lists (PostList, CommentList, SearchResult, Analytics, Audience) are currently passthrough — they return the upstream shape and do not get computed fields.

## Parameter Validation

Every request is validated before any credit is deducted:

1. **Required params (`params[]`)** — every listed name must be present and non-empty.
2. **`oneOf` groups** — endpoints like `GET /v1/youtube/channel` accept `channelId` or `handle` or `url`; at least one member must be present. The platform reference files list these groups.
3. **Optional params** — forwarded to upstream only when provided, ignored otherwise.

A failing request returns `400 INVALID_REQUEST` with `Missing required parameter(s): ...` — either the missing names or `one of a, b, c`.

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

Cache hits are indicated via `cached: true` and the `X-Cache: HIT` header and still count as a normal-priced response (cached responses do not refund credits, but they do return instantly).

## Circuit Breaker & Refunds

Each platform has a per-instance circuit breaker (5 failures in 60s → open for 30s). When open, requests return `503 SERVICE_UNAVAILABLE` with `Retry-After: 30` and credits are auto-refunded. Upstream 5xx errors (`502 UPSTREAM_ERROR`) and internal errors (`500 INTERNAL_ERROR`) also auto-refund. Check live platform health:

```bash
curl -s "https://www.socialcrawl.dev/v1/status"
```

## Error Codes

| Code | Status | Description | Credits |
|------|--------|-------------|---------|
| MISSING_API_KEY | 401 | No x-api-key header | Not charged |
| INVALID_API_KEY | 401 | Key malformed, not found, or revoked | Not charged |
| INSUFFICIENT_CREDITS | 402 | Balance too low | Not charged |
| INVALID_REQUEST | 400 | Missing required parameters | Not charged |
| ENDPOINT_NOT_FOUND | 404 | Unknown platform or resource | Not charged |
| RESOURCE_NOT_FOUND | 404 | Item not found on platform | Not charged |
| CONCURRENCY_LIMIT | 429 | Over 50 concurrent requests per key | Not charged |
| UPSTREAM_ERROR | 502 | Platform returned an error | Refunded |
| SERVICE_UNAVAILABLE | 503 | Circuit breaker open, retry in 30s | Refunded |
| INTERNAL_ERROR | 500 | Unexpected server error | Refunded |
