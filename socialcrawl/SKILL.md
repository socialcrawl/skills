---
name: socialcrawl
description: >
  Interact with the SocialCrawl API — a unified social media + research data API
  covering 27 platforms and 133 endpoints. Fetch profiles, posts, comments,
  search results, and analytics from TikTok, Instagram, YouTube, Facebook,
  Twitter/X, LinkedIn, Reddit, Threads, Pinterest, and 18 more platforms
  (including GitHub, Hacker News, Polymarket, Perplexity, and Tavily) through
  a single API. Includes a universal cross-platform search that fans out to
  12 sources in parallel with SSE streaming.
  Use when the user wants to: (1) fetch social or research data (profiles,
  posts, comments, search), (2) generate code that calls the SocialCrawl API,
  (3) understand SocialCrawl endpoints, pricing, or capabilities, (4) check
  their SocialCrawl credit balance, (5) run a universal search across 12
  sources with one call, or mentions "SocialCrawl", "social crawl", or
  "social media API".
---

# SocialCrawl API

Unified social + research data API. One API key, one response format, **27 platforms, 133 endpoints**, plus a universal search that fans out to 12 sources in parallel. Author and Post responses are normalized through platform field maps and augmented with deterministic computed fields (`engagement_rate`, `language`, `content_category`, `estimated_reach`) under `data.computed`. List archetypes (PostList, CommentList, SearchResult, Audience, Analytics) pass through as `{ items, next_cursor?, total? }` without computed fields. Add `?format=raw` to bypass the transform pipeline entirely.

## API Key

Resolve the API key before making any call, checking these sources in order:

1. **Env var**: `echo "$SOCIALCRAWL_API_KEY"` — if set and starts with `sc_` (and is not a placeholder like `sc_your_api_key_here`), use it.
2. **Config file**: `cat ~/.config/socialcrawl/api_key 2>/dev/null` — if the file exists and contains a key starting with `sc_`, use it.
3. **Ask the user**: If neither source has a valid key:
   - Tell the user: "I need your SocialCrawl API key to continue. You can find it at https://socialcrawl.dev/dashboard — every account starts with 100 free credits."
   - Ask them to paste their key.
   - After receiving the key, **auto-save it** so they never need to paste it again:
     ```bash
     mkdir -p ~/.config/socialcrawl && echo "sc_xxxxx" > ~/.config/socialcrawl/api_key
     ```
   - Tell the user: "I've saved your key to `~/.config/socialcrawl/api_key` so it will be available in future sessions."

For all subsequent API calls in the session, use the resolved key directly in the curl command (do not rely on the env var being set).

## First Use

On the first interaction with this skill in a session:

1. Briefly introduce: "SocialCrawl provides a single API for 27 platforms (133 endpoints), plus a universal search across 12 sources. Let me verify your API key."
2. Resolve the API key using the steps above. If the key is missing or a placeholder, stop here and ask for it before proceeding.
3. Tell the user you'll make a test call that costs 1 credit, then run:
   ```bash
   curl -s -H "x-api-key: KEY" "https://www.socialcrawl.dev/v1/tiktok/profile?handle=tiktok"
   ```
   (Replace `KEY` with the resolved key value.)
4. If successful, confirm the key works and show credits_remaining. Then respond to whatever the user actually asked.
5. If it fails, report the error and help troubleshoot (see Error Handling below).

## Platforms

| Platform | Endpoints | Reference |
|----------|-----------|-----------|
| TikTok | 26 | [references/tiktok.md](references/tiktok.md) |
| GitHub | 12 | [references/github.md](references/github.md) |
| Instagram | 12 | [references/instagram.md](references/instagram.md) |
| YouTube | 12 | [references/youtube.md](references/youtube.md) |
| Facebook | 12 | [references/facebook.md](references/facebook.md) |
| Reddit | 7 | [references/reddit.md](references/reddit.md) |
| Twitter/X | 7 | [references/twitter.md](references/twitter.md) |
| LinkedIn | 6 | [references/linkedin.md](references/linkedin.md) |
| Threads | 5 | [references/threads.md](references/threads.md) |
| Pinterest | 4 | [references/pinterest.md](references/pinterest.md) |
| Google | 4 | [references/google.md](references/google.md) |
| Hacker News | 4 | [references/hackernews.md](references/hackernews.md) |
| Tavily | 4 | [references/tavily.md](references/tavily.md) |
| Truth Social | 3 | [references/truthsocial.md](references/truthsocial.md) |
| Polymarket | 2 | [references/polymarket.md](references/polymarket.md) |
| Twitch | 2 | [references/twitch.md](references/twitch.md) |
| Search (universal) | 1 | [references/search.md](references/search.md) |
| Perplexity | 1 | [references/perplexity.md](references/perplexity.md) |
| Snapchat | 1 | [references/snapchat.md](references/snapchat.md) |
| Kick | 1 | [references/kick.md](references/kick.md) |
| Amazon | 1 | [references/amazon.md](references/amazon.md) |
| Linktree | 1 | [references/linktree.md](references/linktree.md) |
| Linkbio | 1 | [references/linkbio.md](references/linkbio.md) |
| Linkme | 1 | [references/linkme.md](references/linkme.md) |
| Komi | 1 | [references/komi.md](references/komi.md) |
| Pillar | 1 | [references/pillar.md](references/pillar.md) |
| Utility | 1 | [references/utility.md](references/utility.md) |

## Workflow

Determine what the user wants, then follow the matching workflow:

**User wants data:**
1. Identify the platform and resource from their request
2. Read the platform's reference file from the table above
3. Resolve API key
4. Construct and execute the curl command
5. Return raw JSON response
6. Note `credits_used` and `credits_remaining` from the response

**User wants code:**
1. Identify platform, resource, and target language
2. Read the platform's reference file
3. Generate a working code snippet using `$SOCIALCRAWL_API_KEY` env var for the key
4. Present the code without executing

**User wants a cross-platform search ("what's everyone saying about X", "search across Reddit + Twitter + YouTube + …"):**
1. Read [references/search.md](references/search.md)
2. Confirm the **20-credit cost** with the user before executing
3. Construct the `/v1/search/everywhere?query=…` call (sync JSON or SSE — see search.md)

**User asks about capabilities:**
1. Answer from the platform table above
2. If they need details about auth, response format, errors, or credits, read [references/api-overview.md](references/api-overview.md)

**User asks about credits/balance:**
1. Resolve API key
2. Run: `curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" "https://www.socialcrawl.dev/v1/credits/balance"`
3. Return `data.balance` from the envelope (the call costs 0 credits)

**Ambiguous platform:** If the user says "get profile for @nike" without specifying a platform, ask which platform they mean.

**Multi-platform requests:** Load each platform's reference file and make sequential calls. For "search 12 sources at once", use `/v1/search/everywhere` instead — one billable call beats 12 separate ones.

## Making API Calls

Base URL: `https://www.socialcrawl.dev`

All endpoints are GET requests:

```
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/{platform}/{resource}?{param}={value}"
```

URL-encode parameter values that contain spaces or special characters.

### Parameter rules

- **Required params** — each platform reference file lists the required query parameters for every endpoint. A request missing any of them returns `400 INVALID_REQUEST` with the message `Missing required parameter(s): ...`; no credit is deducted.
- **`oneOf` groups** — some endpoints (notably on YouTube, Facebook, TikTok, Instagram, Reddit, Google, Truth Social) accept mutually-substitutable identifiers such as `channelId / handle / url`. Pass at least one member of the group; the platform reference file lists the valid choices.
- **Optional params** — any non-required param listed in the reference file may be forwarded. Anything unrecognized is rejected upstream.
- **CSV array params** — Tavily, Twitter AI Search, and a few others accept comma-separated values for array-shaped params (e.g. `urls=a,b,c`, `from_handles=elonmusk,xai`). The fetcher splits server-side.
- **`format=raw`** — disables field maps and computed fields so you receive the original upstream JSON. Has no effect on non-ScrapeCreators platforms (Polymarket, Hacker News, Tavily, GitHub, Perplexity, Twitter AI Search, Universal Search) since those don't have field maps.

## Credit Tiers

| Tier | Cost | Typical endpoints |
|------|------|-------------------|
| standard | 1 credit | Profiles, posts, search, comments, GitHub direct calls, HN, Tavily, Perplexity research, Twitter AI Search |
| advanced | 5 credits | Audience demographics, ad libraries, trending, GitHub composites (`repo/top-issues`, `repo/dossier`), Polymarket research |
| premium | 10 credits | Video transcripts, age/gender detection, GitHub `user/profile-velocity` |
| **flat override** | **20 credits** | `/v1/search/everywhere` (universal cross-platform search — see [references/search.md](references/search.md)) |

Before executing an advanced, premium, or flat-override call, mention the credit cost to the user. After every call, report `credits_used` and `credits_remaining` from the response.

**Free calls (0 credits deducted):**
- **Cache hits** — `cached: true` + `X-Cache: HIT`. Same data, no charge.
- **Idempotent replays** — `X-Idempotent-Replay: true`. See "Idempotent Retries" below.
- **Empty-upstream 404s** — when upstream returns a 200 with an empty body (nonexistent profile/post), the credit is auto-refunded and you get `RESOURCE_NOT_FOUND`.
- **Universal search zero-floor** — `/v1/search/everywhere` auto-refunds when every source fails (or all return empty). Partial results are billable.
- **`GET /v1/credits/balance`** — meta endpoint.
- **Pre-flight rejections** — 400/401/402/405/409/422/404-endpoint-not-found never deduct.

## Idempotent Retries

Any `/v1/*` call can be made safe to retry by sending an `Idempotency-Key` header (UUIDv4 or any opaque 16+ char string). Replays of the same key + same params return the original body verbatim with `X-Idempotent-Replay: true` and 0 credits deducted. Keys last 24h. Reusing the key with different params returns 422; a key owned by a different account returns 409.

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Idempotency-Key: 7a5e1b4c-2d8f-4a3b-9c1e-6e8b4d2a1f3c" \
  "https://www.socialcrawl.dev/v1/tiktok/profile?handle=tiktok"
```

> **Streaming exception**: `Idempotency-Key` is meaningful only for sync responses. SSE streaming requests to `/v1/search/everywhere` (`Accept: text/event-stream`) cannot be replayed — replays return the cached sync envelope or 409 if no sync body was ever cached.

## Response Headers

| Header | Value |
|--------|-------|
| X-Request-Id | `req-XXXXX` |
| X-Credits-Used | Credits charged (0 on cache hit, replay, or refund) |
| X-Credits-Remaining | Balance after this call |
| X-Cache | `HIT` or `MISS` |
| X-Idempotent-Replay | `"true"` on replays (absent otherwise) |
| Retry-After | `"30"` — only on 503 circuit-breaker responses |
| Allow | `"GET"` — only on 405 METHOD_NOT_ALLOWED |

## Warnings Channel

Successful responses may include an optional `data._warnings: string[]` with advisory notices from the transform pipeline (e.g. a clamped `engagement_rate > 1.0`, or an unresolved field-map path). Treat as observability-only — do not gate logic on it. Empty arrays are omitted.

## Error Handling

| Code | Status | Action |
|------|--------|--------|
| MISSING_API_KEY | 401 | Ask user for their API key |
| INVALID_API_KEY | 401 | "Your API key appears invalid. Check your SocialCrawl dashboard." |
| INSUFFICIENT_CREDITS | 402 | "You're out of credits. Top up at socialcrawl.dev/dashboard/billing" |
| INVALID_REQUEST | 400 | Missing required param OR malformed handle/URL (format validator). Check required params + formats in the platform reference. |
| METHOD_NOT_ALLOWED | 405 | All `/v1/*` endpoints are GET-only. Response includes `Allow: GET`. |
| ENDPOINT_NOT_FOUND | 404 | "That endpoint doesn't exist. Check the platform table above." |
| RESOURCE_NOT_FOUND | 404 | "That profile/post wasn't found on the platform." Credits were refunded if the upstream returned an empty body. |
| IDEMPOTENCY_KEY_CONFLICT | 409 | "That Idempotency-Key is in use by a different account. Pick a new key." |
| IDEMPOTENCY_KEY_PAYLOAD_MISMATCH | 422 | "You reused an Idempotency-Key with different params. Use a fresh key." |
| CONCURRENCY_LIMIT | 429 | "Too many concurrent requests (limit 50/key). Wait a moment and retry." |
| UPSTREAM_ERROR | 502 | "Platform temporarily unavailable. Credits were refunded." |
| SERVICE_UNAVAILABLE | 503 | "Platform circuit breaker is open. Try again in 30s. Credits refunded." |
| INTERNAL_ERROR | 500 | "Unexpected error. Credits were refunded." |

## References

- **[references/api-overview.md](references/api-overview.md)** — Read when user asks about authentication, response format, error details, credit system, or the `?format=raw` parameter
- **[references/search.md](references/search.md)** — Read for universal cross-platform search (`/v1/search/everywhere`) — sync JSON vs SSE, 12-source fan-out, ranked + clustered results, 20-credit flat cost
- **[references/{platform}.md](references/)** — Read the specific platform file when user asks about or wants to call that platform's endpoints
