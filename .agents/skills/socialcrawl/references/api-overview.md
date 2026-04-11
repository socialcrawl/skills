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
| standard | 1 credit | 81 endpoints | Profiles, posts, search, comments |
| advanced | 5 credits | 18 endpoints | Audience, ad libraries, trending |
| premium | 10 credits | 6 endpoints | Transcripts, AI analysis |

## Credit Balance

Check remaining credits:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/api/credits/balance"
```

Returns: `{ "balance": 4999 }`

## Raw Format

Add `?format=raw` to any endpoint to receive the original upstream response without unified schema transformation:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tiktok/profile?handle=charlidamelio&format=raw"
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
