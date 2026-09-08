# SocialCrawl Pricing Reference

Complete per-endpoint credit pricing for all 572 active endpoints across 65 platforms. Auto-derived from the live endpoint registry - the same registry the router uses to charge your balance.

## How billing works

- Every billable API call deducts credits from your balance **before** the upstream call, atomically. The response reports the net charge in `credits_used` and `X-Credits-Used`.
- On billed responses, `credits_remaining` and `X-Credits-Remaining` are authoritative. Free cache hits return `credits_remaining: null` and omit the header because they do not establish an authoritative post-request balance. Idempotent replays return the current balance when their lookup succeeds; otherwise they return `credits_remaining: null` and omit the header. Routes that explicitly model an unavailable balance, including endpoint-parameter validation and best-effort metadata, omit both fields when their balance read fails.
- **Cache hits are free** - a response served from cache costs 0 credits (`X-Cache: HIT`, `cached: true`). Each endpoint's TTL is in the tables below; a repeat call inside the TTL window is free.
- **Automatic refunds** - credits are refunded on upstream errors (502), circuit-breaker rejections (503), internal errors (500), request-deadline timeouts (504), and empty-upstream results (404 `RESOURCE_NOT_FOUND` / an empty `items` list). You only pay for calls that return real data.
- **Free before billing** - invalid params, bad handle/URL formats, and rate-limit rejections (429) are rejected at the boundary and never deduct.
- **Idempotent replays are free** - resending with the same `Idempotency-Key` returns the stored response at 0 credits.
- **Metered endpoints** deduct an upfront ceiling and auto-refund down to the actual work done; the response `credits_used` is the real charge. Every metered endpoint is listed with its full pricing rule under [Metered and custom-priced endpoints](#metered-and-custom-priced-endpoints).
- **Multi-source endpoints charge once** no matter how many upstream providers are tried before one succeeds.
- `GET /v1/credits/balance` and `GET /v1/credits/transactions` are always 0 credits, as is every `/v1/utility/*` endpoint.

## Credit tiers

Most endpoints sit on a simple 1 / 5 / 10 ladder. A set of bundle and fan-out endpoints use a **custom** override that bypasses the ladder, flat or metered per recipe. Those run far past the ladder at the top end, so read the endpoint's own rule rather than assuming a ceiling.

| Tier | Cost per call | Endpoints | Typical endpoints |
|------|--------------|-----------|-------------------|
| standard | 1 credit | 277 | Profiles, posts, comments, search, reference data |
| advanced | 5 credits | 171 | Ad libraries, trending, audience analytics, app/product/business/place reviews, retail catalogs, LinkedIn social graph + jobs |
| premium | 10 credits | 22 | Video transcripts, LinkedIn people/job search + reactions, app-listings search |
| **custom (flat/metered)** | **varies (0-10000)** | 102 | Prism composites, `{platform}/profile/full`, `search/everywhere` (20), `search/forums` (10), `search/news` (2-62 metered), `naver/brief` (10), the free `/v1/utility/*` endpoints, web scrape/crawl/agent/sessions |

Counted by underlying tier (custom endpoints folded into their base tier), the split is **327 standard · 210 advanced · 35 premium = 572**. Exact per-endpoint costs are in the tables below.

## Credit packs

| Plan | Credits | Price |
|------|---------|-------|
| Free (signup bonus) | 100 | £0 |
| Starter | 2,500 | £15 one-time |
| Growth | 20,000 | £49 one-time |
| Pro | 150,000 | £299 one-time |
| Enterprise | Custom | [Contact](https://socialcrawl.dev/contact) |

Current packs and any promotions: https://socialcrawl.dev/pricing

## Estimating a job before you run it

Quote a cost to the user BEFORE spending their credits. The arithmetic:

1. **One call** - look the endpoint up in the tables below. That number is the whole charge for a live successful call.
2. **A paginated pull** - the price is per PAGE, not per item. `pages = ceil(items_wanted / page_size)`, and the cost is `pages x per-call credits`. Each endpoint's page-size param and its maximum are on its `**Pagination**` line in the platform reference.
3. **A repeat pull inside the cache TTL** - free. Re-reading the same profile twice in a minute bills once.
4. **A metered endpoint** - use the ceiling from the range for the quote, then report the real `credits_used` afterwards. It is usually well under the ceiling.
5. **A composite** - a Prism recipe is ONE charge that already covers every leg it fans out to. Running the legs yourself is almost always more expensive, and slower.

Worked example - 1,000 TikTok comments on one video: `prism/comments` is metered at 1 credit per comment page scanned, so roughly 2-20 credits for the whole thread in a single call, versus paginating `tiktok/video/comments` yourself at 1 credit per page plus your own cursor loop.

When a pull would cost more than a user's likely balance, say so and offer the cheaper shape (a smaller `limit`, a web-only `include`, a composite instead of a fan-out) rather than starting it.

## Free endpoints (0 credits)

18 endpoints never bill, plus `GET /v1/credits/balance` and `GET /v1/credits/transactions`. Use them freely to discover the surface, resolve a URL, or manage async jobs.

| Endpoint | What it returns |
|----------|-----------------|
| `GET /v1/prism/lookup` | Universal post/product URL dispatcher: any post, video, product or repo link → the right detail endpoint's unified response. |
| `GET /v1/utility/endpoint` | How to use any endpoint |
| `GET /v1/utility/endpoints` | List every available endpoint |
| `GET /v1/utility/llms` | AI-agent context payload |
| `GET /v1/utility/quickstart` | Get started in one call |
| `GET /v1/web/jobs` | List async web jobs |
| `GET /v1/web/jobs/{job_id}` | Get an async web job |
| `DELETE /v1/web/jobs/{job_id}` | Cancel an async web job |
| `POST /v1/web/monitors` | Create a web monitor |
| `GET /v1/web/monitors` | List web monitors |
| `GET /v1/web/monitors/{monitor_id}` | Get a web monitor |
| `PATCH /v1/web/monitors/{monitor_id}` | Update a web monitor |
| `DELETE /v1/web/monitors/{monitor_id}` | Delete a web monitor |
| `GET /v1/web/monitors/{monitor_id}/checks` | List web monitor checks |
| `GET /v1/web/sessions` | List interactive web sessions |
| `GET /v1/web/sessions/{session_id}` | Get an interactive web session |
| `DELETE /v1/web/sessions/{session_id}` | Close an interactive web session |
| `POST /v1/web/sessions/{session_id}/execute` | Execute an interaction in a web session |

## Metered and custom-priced endpoints

43 endpoints do not charge a flat ladder price. Each one holds an upfront ceiling and refunds the unused portion, so the response `credits_used` is always the real charge. Quote the RANGE to a user before calling, then report the actual charge afterwards.

| Endpoint | Range | How it is charged |
|----------|-------|-------------------|
| `GET /v1/douyin/comment/replies` | 5-250 credits | 5 credits per reply RETURNED. The call holds `limit x 5` up front - the default limit of 10 holds 50 and the 50 maximum holds 250 - and settles down to the replies actually delivered. Only a comment with a non-zero `engagement.replies` has a thread, so check that on the parent row before spending a call here |
| `GET /v1/douyin/post/comments` | 2-100 credits | 1 credit per comment RETURNED, with a floor of 2. The call holds `limit x 1` up front - the default limit of 20 holds 20 and the 100 maximum holds 100 - and settles down to the comments actually delivered, so a video with four comments does not cost a twenty-comment request |
| `GET /v1/douyin/profile/posts` | 5-125 credits | 5 credits per row RETURNED. The call holds `limit x 5` up front - the default limit of 10 holds 50 and the 50 maximum holds 250 - and settles down to the videos actually delivered, so a creator with 4 recent videos costs 20 credits however high `limit` was set. `recent_days` and `exclude_pinned` narrow the result set BEFORE billing settles, so they lower the charge as well as the noise |
| `GET /v1/douyin/search` | 5-125 credits | 5 credits per row RETURNED. The call holds `limit x 5` up front - the default limit of 10 holds 50 and the 50 maximum holds 250 - and settles down to the rows actually delivered, so a narrow query that returns 3 videos costs 15 credits however high `limit` was set |
| `GET /v1/douyin/search/users` | 5-125 credits | 5 credits per creator RETURNED. The call holds `limit x 5` up front - the default limit of 10 holds 50 and the 50 maximum holds 250 - and settles down to the creators actually delivered |
| `GET /v1/facebook/profile/reels/full` | 5-25 credits | 5 credits per page of 10 reels - 1 for the list and 4 for the per-reel enrichment - which is roughly half what running the list-then-post-stats chain yourself costs. With no `limit` that is one page and a flat 5 credits. With `limit` set the endpoint walks `ceil(limit / 10)` pages, up to 5 for the 50 maximum (25 credits), holds that many up front and refunds every page it did not need. A page whose enrichment yields zero coverage refunds the 4-credit premium automatically, leaving the 1-credit list price |
| `GET /v1/instagram/comment` | 5-15 credits | 5 credits for a standard lookup, 15 with `deep_scan=true`, which keeps paging the thread when the comment is not in the first pages. Reach for deep_scan only after a standard lookup comes back not-found |
| `GET /v1/instagram/profile/posts/full` | 5-25 credits | 5 credits per upstream page of about 12 posts. With no `limit` that is one page and a flat 5 credits. With `limit` set the composite walks `ceil(limit / 12)` pages - 3 for limit=30, 5 for the 50 maximum, so 25 credits at the top - holds that many up front and refunds every page it did not need. Two partial refunds sit inside the per-page price: a shares leg that fails outright refunds 4 of the 5 credits for that page, leaving the 1-credit list price, and a `user_id`-only call refunds the same 4 because the shares leg needs a handle. A shares leg that succeeds with low coverage is still the full 5, because the second source was queried either way |
| `GET /v1/instagram/profile/reels/full` | 5-25 credits | 5 credits per upstream page of about 12 reels. With no `limit` that is one page and a flat 5 credits. With `limit` set the composite walks `ceil(limit / 12)` pages - 3 for limit=30, 5 for the 50 maximum, so 25 credits at the top - holds that many up front and refunds every page it did not need. Two partial refunds sit inside the per-page price: a shares leg that fails outright refunds 4 of the 5 credits for that page, leaving the 1-credit list price, and a `user_id`-only call refunds the same 4 because the shares leg needs a handle. A shares leg that succeeds with low coverage is still the full 5, because the second source was queried either way |
| `GET /v1/linkedin/profile/posts/archive` | 5-500 credits | 5 credits per post RETURNED. The call holds `limit x 5` up front - the default limit of 20 holds 100 and the 100 maximum holds 500 - and refunds down to the posts that actually came back, so a member with 12 posts settles at 60 credits however high `limit` was set. This is the most expensive read on the platform per row: check whether /v1/linkedin/profile/posts (5 credits a page) already covers the window you need before walking the archive |
| `GET /v1/prism/ai-visibility` | 2-1605 credits | 2 credits per probe, where a probe is one prompt run once on one engine, so the charge is `2 x prompts x runs x engines`. On the defaults (both engines, 8 runs) a 5-prompt audit is 160 credits. `include=web_baseline` adds a flat 5. The 1,605 ceiling is the 20-prompt, 20-run, two-engine worst case with the baseline on - `preset=quick` holds far less, and the hold settles down to the probes that actually completed |
| `GET /v1/prism/app-reviews` | 10-15 credits | 10 credits for one store, 15 for both. A bare `query` resolves both stores and costs 15; naming a single store in `stores`, or passing only one of `google_play_id` / `app_store_id`, costs 10 |
| `POST /v1/prism/comment-lookup` | 2-100 credits | 2 credits per found TikTok item and 5 per found Instagram item, raised by `deep_scan`. Up to 25 items per call: the whole batch holds at most 100 credits up front and refunds every not_found, errored and deferred item |
| `GET /v1/prism/comments` | 2-200 credits | 1 credit per comment page scanned, except on Instagram, where a post URL is a flat 5 credits whatever `max` and `replies` you pass |
| `GET /v1/prism/creator-card` | 5-8 credits | 5 credits covering any 4 platforms, plus 1 credit per platform beyond 4. The default selection is 4 platforms, so the 7-platform maximum is 8 credits |
| `GET /v1/prism/creator-vet` | 50-75 credits | 50 credits for the standard vet. `include=cross_platform` raises it to 75 for the cross-platform identity check on top |
| `GET /v1/prism/crisis-radar` | 15-45 credits | 15 credits for the baseline breach check. `confirm=true` escalates to the full 45-credit investigation. Run the baseline first and escalate only when it reports a breach: that is the whole point of the two-step shape |
| `GET /v1/prism/handle-audit` | 5-8 credits | 5 credits for any selection of up to 4 supported platforms; +1 credit per selected platform beyond 4 |
| `GET /v1/prism/korea-gap` | 15-40 credits | 15 credits for the web-only read. The default `include` carries the social leg, which makes the call 40; pass an `include` without `social` to stay at 15 |
| `GET /v1/prism/org-radar` | 6-51 credits | 1 credit for the org read plus 5 per repository expanded into a dossier. The default of 5 repos is 26 credits, a single repo is 6, and the 10-repo maximum is 51. Set `repos` to bound it before calling |
| `POST /v1/prism/post-stats` | 1-500 credits | 1 credit per successful URL on most platforms, 5 on Instagram and LinkedIn, charged at each URL's own platform rate. Up to 100 URLs per call: the call holds the summed worst case up front (a 100-URL Instagram batch holds 500) and refunds every dead, errored and unsupported URL, so you pay for exactly the rows that returned counts |
| `POST /v1/prism/profiles` | 1-250 credits | 1 credit per successful row on most platforms and 5 on LinkedIn, charged at each handle's own platform tier. Up to 50 items per call: the call holds the summed worst case up front and refunds every not_found, unsupported, errored and deferred row |
| `GET /v1/prism/share-of-voice` | 20-200 credits | 40 credits per brand with the social leg, which is the default, or 20 per brand for the web-only read. Up to 5 brands per call, so the 200-credit ceiling is 5 brands with social and dropping `social` from `include` halves it. Price the call as `brands x per-brand` before you send it - this is the most expensive composite on the API |
| `GET /v1/prism/video-intel` | 5-15 credits | 5 credits for the video detail, stats and comments. `include=transcript` adds 10, which is exactly what the standalone transcript endpoint charges, so the bundle never costs more than running the two calls yourself |
| `GET /v1/reddit/omni-search` | 5-9 credits | 1 credit for the search page plus 1 per thread SUCCESSFULLY expanded, with a floor of 5. The call holds `1 + threads` up front (the 8-thread maximum holds 9) and refunds every thread that failed to expand, so the floor is what most sweeps cost. Running the same sweep by hand - one reddit/search plus eight reddit/post/comments calls - costs the same 9 at best and gives you no subreddit rollup |
| `GET /v1/reddit/profile/comments` | 2-200 credits | 2 credits per comment returned. A limit of 25 holds 50 credits and settles down to the number of comments that actually came back; an account with no comments costs nothing. |
| `GET /v1/reddit/search` | 1-26 credits | 1 credit for the search page. include_body=true reserves up to 25 extra credits and refunds every one it does not spend. Rows now arrive with their bodies, and a link post has no body to fetch, so a row is only charged for when a body actually comes back: on most pages nothing is spent and the page costs 1 credit. |
| `GET /v1/reddit/subreddit/search` | 1-26 credits | 1 credit for the search page. With include_body=true, 1 extra credit per post that comes back with a body, up to 25 per page, unused credits refunded. Link posts have no body and are not charged for. |
| `GET /v1/search/news` | 2-62 credits | 2 credits + 1 credit per google leg that returns at least one article (upfront hold 2 + min(5 x countries, max_legs, 12), maximum 14 on the default engine). Adding the bing engine adds 1 credit per 5 articles it returns, because that engine is priced per article rather than per call; the absolute ceiling with both engines is 62. The hold always settles down to the actual charge, and empty, skipped or failed legs bill 0. |
| `GET /v1/threads/post/comments` | 1-10 credits | 1 credit for the bundled window of about 20 replies, which is what a call with no `limit`, or `limit` at 25 or below, costs. Above 25 the deeper lane is metered at 1 credit per 5 replies RETURNED: the call holds `ceil(limit / 5)` up front (the 50 maximum holds 10) and refunds down to what came back, so a post with 12 replies settles at 3 credits however high `limit` was set |
| `GET /v1/threads/search` | 1-11 credits | 1 credit per result window. A call with no `limit` is one window and costs exactly 1. With `limit` set the walker consumes `ceil(limit / 15)` windows - 4 for limit=50, 7 for the 100 maximum - holds that many up front and refunds every window it did not need. Query relaxation can add up to 4 more windows on a page-1 request, billed only for the relaxed searches that returned posts and refunded for the ones that did not; send `expand=false` to hold none of them, and note that a request carrying a cursor never relaxes, so a pagination loop's last hop costs nothing extra |
| `GET /v1/tiktok/ads/top` | 10-100 credits | 1 credit per ad returned, minimum 10 credits. A limit of 20 holds 20 credits and settles down to the number of ads that actually came back; a filter combination with no board costs nothing. |
| `GET /v1/tiktok/comment` | 2-6 credits | 2 credits for a standard lookup, 6 with `deep_scan=true`, which keeps paging the thread when the comment is not in the first pages. Reach for deep_scan only after a standard lookup comes back not-found |
| `POST /v1/web/batch-scrape` | 1 credit | 1 credit per URL submitted, held up front and refunded down to the URLs actually scraped when the job settles |
| `POST /v1/web/crawl` | 1-10000 credits | 1 credit per page crawled. Submitting holds `limit` credits up front (default limit 10, max 10,000) and the unused portion is refunded when the job settles |
| `GET /v1/web/extract` | 5 credits | A flat 5 credits. It runs through the metered pricer for consistency with the rest of the web surface, but nothing in your query changes the charge |
| `GET /v1/web/scrape` | 1-5 credits | 1 credit for a standard scrape. It rises to a flat 5 when the fetch needs more than a plain request: `proxy=auto`, `proxy=enhanced`, or `pdf_parse=true`. Nothing else moves the price, so screenshots, tag filters, `wait_for` and a mobile viewport are all included in the 1 credit |
| `GET /v1/web/search` | 2-120 credits | 2 credits per 10 results, so `limit` up to 10 costs 2, 11-20 costs 4, and the 100 maximum costs 20. `include_content=true` adds 1 credit per result, because it scrapes each result page as well as reading the SERP row - that is what takes a 100-result content search to the 120-credit ceiling. The hold settles down to the work actually done |
| `POST /v1/web/sessions` | 5 credits | 20 credits per browser-hour, minimum 5. The hold is taken from `ttl_seconds` when the session is created (60s default = 5, the 3,600s maximum = 20) and settled when it closes |
| `POST /v1/youtube/channels` | 5-100 credits | 5 credits per 50-id chunk, so a 50-id batch is 5 credits and the 1,000-id maximum is 100. Batching is what makes this cheap: the same 1,000 channels fetched one at a time through GET /v1/youtube/channel cost 1,000 credits. A chunk is charged whether or not every id in it resolves, so there is no per-id refund; a call that resolves nothing at all is refunded in full |
| `GET /v1/youtube/search/advanced` | 1-6 credits | 1 credit for the search page. `includeExtras=true` adds a flat 5 credits for the single hydration call that fills view, like and comment counts and `duration_seconds` on the whole page. The increment never repeats: the page caps at 50 results, which one hydration call covers, so a hydrated page of 50 costs 6 credits and so does a hydrated page of 5 |
| `POST /v1/youtube/transcripts` | 3-300 credits | 3 credits per successful transcript. Up to 100 ids per call: the call holds ids × 3 up front (a full batch holds 300) and refunds every not_found, errored and deferred row |
| `POST /v1/youtube/videos` | 5-100 credits | 5 credits per 50-id chunk, so a 50-id batch is 5 credits and the 1,000-id maximum is 100. Batching is what makes this cheap: the same 1,000 videos fetched one at a time through GET /v1/youtube/video cost 1,000 credits. A chunk is charged whether or not every id in it resolves, so there is no per-id refund; a call that resolves nothing at all is refunded in full |

## Per-endpoint pricing

`Credits` is the charge for one live (non-cached) successful call. `Cache` is how long a successful response is reused - a repeat call inside that window costs 0.

### AliExpress (9)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/aliexpress/categories` | GET | List AliExpress categories | 1 | standard | 1800s |
| `/v1/aliexpress/product` | GET | Get an AliExpress product by id or URL | 5 | advanced | 600s |
| `/v1/aliexpress/product/shipping` | GET | Get AliExpress shipping for a product SKU | 5 | advanced | 600s |
| `/v1/aliexpress/product/similar` | GET | Get similar AliExpress products | 5 | advanced | 120s |
| `/v1/aliexpress/promo` | GET | List AliExpress featured promotions | 1 | standard | 1800s |
| `/v1/aliexpress/reviews` | GET | Get AliExpress product reviews | 5 | advanced | 300s |
| `/v1/aliexpress/search` | GET | Search AliExpress products | 5 | advanced | 120s |
| `/v1/aliexpress/search/hot` | GET | List hot AliExpress products | 5 | advanced | 120s |
| `/v1/aliexpress/search/promo` | GET | List AliExpress products in a featured promotion | 5 | advanced | 120s |

### Amazon (8)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/amazon/best-sellers` | GET | Get Amazon Best Sellers in a category | 1 | standard | 120s |
| `/v1/amazon/deals` | GET | Get current Amazon deals | 1 | standard | 120s |
| `/v1/amazon/product` | GET | Get an Amazon product by ASIN | 5 | advanced | 600s |
| `/v1/amazon/product-search` | GET | Search Amazon products by keyword | 1 | standard | 120s |
| `/v1/amazon/reviews` | GET | Get Amazon product reviews | 5 | advanced | 300s |
| `/v1/amazon/seller` | GET | Get an Amazon seller profile | 1 | standard | 900s |
| `/v1/amazon/sellers` | GET | Get Amazon sellers and offers for a product | 1 | standard | 600s |
| `/v1/amazon/shop` | GET | Get Amazon shop page | 1 | standard | 600s |

### Apple App Store (9)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/app_store/app-info` | GET | Get full Apple App Store app details | 5 | advanced | 600s |
| `/v1/app_store/app-list` | GET | Get an Apple App Store chart | 5 | advanced | 120s |
| `/v1/app_store/app-listings-search` | GET | Search the Apple App Store listings database (paginated) | 10 | premium | 120s |
| `/v1/app_store/app-reviews` | GET | Get Apple App Store reviews for an app | 5 | advanced | 300s |
| `/v1/app_store/app-search` | GET | Search Apple App Store apps by keyword | 5 | advanced | 120s |
| `/v1/app_store/categories` | GET | List Apple App Store app categories | 1 | standard | 1800s |
| `/v1/app_store/languages` | GET | List supported Apple App Store languages | 1 | standard | 1800s |
| `/v1/app_store/locations` | GET | List supported Apple App Store storefront locations | 1 | standard | 1800s |
| `/v1/app_store/search-suggestions` | GET | Get Apple App Store search suggestions | 1 | standard | 120s |

### Apple Music (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/apple_music/album` | GET | Get an Apple Music album | 1 | standard | 600s |
| `/v1/apple_music/artist` | GET | Get an Apple Music artist | 1 | standard | 900s |
| `/v1/apple_music/search` | GET | Search Apple Music | 1 | standard | 120s |
| `/v1/apple_music/track` | GET | Get an Apple Music track | 1 | standard | 600s |

### Bluesky (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/bluesky/post` | GET | Get a Bluesky post | 1 | standard | 600s |
| `/v1/bluesky/profile` | GET | Get a Bluesky profile | 1 | standard | 900s |
| `/v1/bluesky/user/posts` | GET | List a Bluesky user's posts | 1 | standard | 600s |

### Content Analysis (10)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/content_analysis/categories` | GET | List the Content Analysis category taxonomy | 1 | standard | 1800s |
| `/v1/content_analysis/category-trends` | GET | Category mention volume + sentiment over time | 20 | custom | 1800s |
| `/v1/content_analysis/filters` | GET | List the filterable fields for Content Analysis | 1 | standard | 1800s |
| `/v1/content_analysis/languages` | GET | List supported Content Analysis languages | 1 | standard | 1800s |
| `/v1/content_analysis/locations` | GET | List supported Content Analysis locations | 1 | standard | 1800s |
| `/v1/content_analysis/phrase-trends` | GET | Keyword mention volume + sentiment over time | 20 | custom | 1800s |
| `/v1/content_analysis/rating-distribution` | GET | Rating histogram for a keyword | 20 | custom | 1800s |
| `/v1/content_analysis/search` | GET | Search web citations of a keyword with per-mention sentiment | 20 | custom | 1800s |
| `/v1/content_analysis/sentiment` | GET | Sentiment breakdown for a keyword | 20 | custom | 1800s |
| `/v1/content_analysis/summary` | GET | Aggregate mention summary for a keyword | 20 | custom | 1800s |

### Douyin (8)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/douyin/comment/replies` | GET | Get replies to a Douyin comment | 5-250 (metered) | advanced | 300s |
| `/v1/douyin/post` | GET | Get a Douyin video | 10 | premium | 600s |
| `/v1/douyin/post/comments` | GET | Get Douyin video comments | 2-100 (metered) | standard | 300s |
| `/v1/douyin/profile` | GET | Get a Douyin creator profile | 6 | custom | 900s |
| `/v1/douyin/profile/posts` | GET | List a Douyin creator's videos | 5-125 (metered) | advanced | 900s |
| `/v1/douyin/search` | GET | Search Douyin videos | 5-125 (metered) | advanced | 120s |
| `/v1/douyin/search/users` | GET | Search Douyin creators | 5-125 (metered) | advanced | 120s |
| `/v1/douyin/trending` | GET | Get the Douyin hot-search board | 25 | custom | 1800s |

### eBay (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/ebay/product` | GET | Get an eBay listing by item id | 5 | advanced | 600s |
| `/v1/ebay/search` | GET | Search eBay listings | 5 | advanced | 120s |

### Etsy (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/etsy/product` | GET | Get an Etsy listing by id or URL | 5 | advanced | 600s |
| `/v1/etsy/product/similar` | GET | Get listings similar to an Etsy product | 5 | advanced | 120s |
| `/v1/etsy/search/suggestions` | GET | Get Etsy search suggestions | 5 | advanced | 120s |
| `/v1/etsy/shop/products` | GET | List products in an Etsy shop | 5 | advanced | 120s |

### Facebook (24)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/facebook/adlibrary/ad` | GET | Get Facebook Ad Library ad details | 5 | advanced | 1800s |
| `/v1/facebook/adlibrary/ad/transcript` | GET | Get a Facebook Ad Library video ad transcript | 10 | premium | 2592000s |
| `/v1/facebook/adlibrary/company/ads` | GET | List Facebook Ad Library company ads | 5 | advanced | 1800s |
| `/v1/facebook/adlibrary/search/ads` | GET | Search Facebook Ad Library | 5 | advanced | 120s |
| `/v1/facebook/adlibrary/search/companies` | GET | Search Facebook Ad Library companies | 5 | advanced | 120s |
| `/v1/facebook/event/details` | GET | Get details for a Facebook event | 1 | standard | 600s |
| `/v1/facebook/events` | GET | List Facebook events for a city | 1 | standard | 600s |
| `/v1/facebook/events/search` | GET | Search Facebook events by keyword | 1 | standard | 120s |
| `/v1/facebook/group` | GET | Get a Facebook group | 1 | standard | 900s |
| `/v1/facebook/group/posts` | GET | List Facebook group posts | 1 | standard | 600s |
| `/v1/facebook/marketplace/item` | GET | Get a Facebook Marketplace item | 1 | standard | 600s |
| `/v1/facebook/marketplace/location/search` | GET | Search Facebook Marketplace locations | 1 | standard | 120s |
| `/v1/facebook/marketplace/search` | GET | Search Facebook Marketplace listings | 1 | standard | 120s |
| `/v1/facebook/post` | GET | Get Facebook post details | 1 | standard | 600s |
| `/v1/facebook/post/comment/replies` | GET | List replies to a Facebook post comment | 1 | standard | 300s |
| `/v1/facebook/post/comments` | GET | List Facebook post comments | 1 | standard | 300s |
| `/v1/facebook/post/transcript` | GET | Get Facebook video transcript | 10 | premium | 2592000s |
| `/v1/facebook/profile` | GET | Get Facebook page profile | 1 | standard | 900s |
| `/v1/facebook/profile/events` | GET | List a Facebook page's events | 1 | standard | 600s |
| `/v1/facebook/profile/full` | GET | Facebook profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/facebook/profile/photos` | GET | List Facebook profile photos | 1 | standard | 600s |
| `/v1/facebook/profile/posts` | GET | List Facebook page posts | 1 | standard | 600s |
| `/v1/facebook/profile/reels` | GET | List Facebook profile reels | 1 | standard | 600s |
| `/v1/facebook/profile/reels/full` | GET | Facebook profile reels with exact views, likes, comments, and shares merged in, in one call. | 5-25 (metered) | advanced | 600s |

### Finance (7)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/finance/history` | GET | Get daily price history for an instrument | 1 | standard | 1800s |
| `/v1/finance/markets` | GET | Get a markets overview (indices + movers) | 1 | standard | 60s |
| `/v1/finance/news` | GET | Get recent news for a financial instrument | 1 | standard | 600s |
| `/v1/finance/options` | GET | Get an options chain for an instrument | 5 | advanced | 1800s |
| `/v1/finance/quote` | GET | Get a financial instrument quote | 5 | advanced | 60s |
| `/v1/finance/statements` | GET | Get financial statements for a company | 5 | advanced | 1800s |
| `/v1/finance/ticker-search` | GET | Search financial instruments by name | 1 | standard | 120s |

### G2 (7)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/g2/categories` | GET | List every G2 category URL | 1 | standard | 1800s |
| `/v1/g2/category` | GET | List products in a G2 category | 5 | advanced | 120s |
| `/v1/g2/product` | GET | Get a G2 product by slug or URL | 5 | advanced | 600s |
| `/v1/g2/product-index` | GET | List G2 product URLs | 5 | advanced | 1800s |
| `/v1/g2/reviews` | GET | Get G2 reviews for a product | 5 | advanced | 300s |
| `/v1/g2/seller` | GET | Get a G2 seller (vendor) profile | 5 | advanced | 900s |
| `/v1/g2/seller/products` | GET | List products for a G2 seller | 5 | advanced | 120s |

### GitHub (12)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/github/issue` | GET | Get a single issue or pull request | 1 | standard | 600s |
| `/v1/github/issue/comments` | GET | Get comments on an issue or pull request | 1 | standard | 300s |
| `/v1/github/profile` | GET | Get a GitHub user profile | 1 | standard | 900s |
| `/v1/github/profile/repos` | GET | List a GitHub user's repositories | 1 | standard | 900s |
| `/v1/github/repo` | GET | Get a GitHub repository | 1 | standard | 900s |
| `/v1/github/repo/dossier` | GET | Full project dossier for a repository | 5 | advanced | 1800s |
| `/v1/github/repo/issues` | GET | List a repository's issues (and PRs) | 1 | standard | 600s |
| `/v1/github/repo/readme` | GET | Get a repository's README | 1 | standard | 900s |
| `/v1/github/repo/releases` | GET | List a repository's releases | 1 | standard | 600s |
| `/v1/github/repo/top-issues` | GET | Top feature request and top complaint for a repository | 5 | advanced | 1800s |
| `/v1/github/search` | GET | Search GitHub issues and pull requests | 1 | standard | 120s |
| `/v1/github/user/profile-velocity` | GET | User contribution velocity dossier | 10 | premium | 1800s |

### Google (10)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google/ad` | GET | Get Google ad details | 5 | advanced | 1800s |
| `/v1/google/adlibrary/advertisers/search` | GET | Search Google Ad Library advertisers | 5 | advanced | 120s |
| `/v1/google/business/extended-reviews` | GET | Get Google extended (multi-source) reviews | 5 | advanced | 600s |
| `/v1/google/business/info` | GET | Get a Google Business Profile | 1 | standard | 900s |
| `/v1/google/business/questions` | GET | Get Google Business Profile questions & answers | 5 | advanced | 300s |
| `/v1/google/business/updates` | GET | Get Google Business Profile posts (updates) | 1 | standard | 600s |
| `/v1/google/company/ads` | GET | List Google ads by company | 5 | advanced | 1800s |
| `/v1/google/hotels/info` | GET | Get Google hotel detail | 5 | advanced | 900s |
| `/v1/google/hotels/search` | GET | Search Google hotels | 1 | standard | 120s |
| `/v1/google/search` | GET | Google web search | 1 | standard | 120s |

### Google News (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google_news/search` | GET | Search Google News | 1 | standard | 300s |

### Google Play (9)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google_play/app-info` | GET | Get full Google Play app details | 5 | advanced | 600s |
| `/v1/google_play/app-list` | GET | Get a Google Play store chart | 5 | advanced | 120s |
| `/v1/google_play/app-listings-search` | GET | Search the Google Play listings database (paginated) | 10 | premium | 120s |
| `/v1/google_play/app-reviews` | GET | Get Google Play reviews for an app | 5 | advanced | 300s |
| `/v1/google_play/app-search` | GET | Search Google Play apps by keyword | 5 | advanced | 120s |
| `/v1/google_play/categories` | GET | List Google Play app categories | 1 | standard | 1800s |
| `/v1/google_play/languages` | GET | List supported Google Play languages | 1 | standard | 1800s |
| `/v1/google_play/locations` | GET | List supported Google Play storefront locations | 1 | standard | 1800s |
| `/v1/google_play/search-suggestions` | GET | Get Google Play search suggestions | 1 | standard | 120s |

### Google Shopping (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google_shopping/price-history` | GET | Get Google Shopping price history for a product | 1 | standard | 1800s |
| `/v1/google_shopping/product` | GET | Get Google Shopping product detail | 1 | standard | 600s |
| `/v1/google_shopping/product-search` | GET | Search Google Shopping products | 5 | advanced | 120s |
| `/v1/google_shopping/reviews` | GET | Get Google Shopping product reviews | 1 | standard | 300s |
| `/v1/google_shopping/sellers` | GET | Get Google Shopping sellers for a product | 1 | standard | 600s |

### Google Trends (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google_trends/explore` | GET | Get Google Trends interest over time | 5 | advanced | 120s |
| `/v1/google_trends/rising` | GET | Get related + rising Google Trends queries | 5 | advanced | 120s |

### Gumtree (11)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/gumtree/categories` | GET | Get the Gumtree category tree | 1 | standard | 1800s |
| `/v1/gumtree/filters` | GET | Get Gumtree filters for a category | 1 | standard | 1800s |
| `/v1/gumtree/locations` | GET | Autocomplete Gumtree locations | 5 | advanced | 120s |
| `/v1/gumtree/locations/nearest` | GET | Find the nearest Gumtree location | 5 | advanced | 120s |
| `/v1/gumtree/product` | GET | Get a Gumtree listing by ad id or URL | 5 | advanced | 600s |
| `/v1/gumtree/product/similar` | GET | Get listings similar to a Gumtree ad | 5 | advanced | 120s |
| `/v1/gumtree/search` | GET | Search Gumtree UK listings | 5 | advanced | 120s |
| `/v1/gumtree/search/suggestions` | GET | Get Gumtree search suggestions | 5 | advanced | 120s |
| `/v1/gumtree/seller` | GET | Get a Gumtree seller profile | 5 | advanced | 900s |
| `/v1/gumtree/seller/listings` | GET | List a Gumtree seller's active ads | 5 | advanced | 120s |
| `/v1/gumtree/trending` | GET | Get trending Gumtree searches | 1 | standard | 1800s |

### H&M (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/hm/categories` | GET | Get the H&M category tree | 1 | standard | 1800s |
| `/v1/hm/countries` | GET | List H&M countries and languages | 1 | standard | 1800s |
| `/v1/hm/product/suppliers` | GET | Get H&M suppliers and factories for a product | 5 | advanced | 1800s |
| `/v1/hm/search` | GET | Search H&M products by keyword | 5 | advanced | 120s |
| `/v1/hm/search/suggestions` | GET | Get H&M search suggestions | 5 | advanced | 120s |
| `/v1/hm/stores` | GET | List H&M stores in a country | 5 | advanced | 1800s |

### Hacker News (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/hackernews/profile` | GET | Get a Hacker News user profile | 1 | standard | 900s |
| `/v1/hackernews/search` | GET | Search Hacker News | 1 | standard | 120s |
| `/v1/hackernews/story` | GET | Get a Hacker News story | 1 | standard | 600s |
| `/v1/hackernews/story/comments` | GET | Get comments on a Hacker News story | 1 | standard | 300s |

### Home Depot (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/home_depot/product` | GET | Get a Home Depot product by item id or URL | 5 | advanced | 600s |
| `/v1/home_depot/reviews` | GET | Get Home Depot product reviews | 5 | advanced | 300s |
| `/v1/home_depot/search` | GET | Search Home Depot products by keyword | 5 | advanced | 120s |
| `/v1/home_depot/stores` | GET | Find Home Depot stores near a ZIP code | 1 | standard | 1800s |

### Instagram (37)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/instagram/audio/reels` | GET | List Instagram reels using an audio track | 1 | standard | 600s |
| `/v1/instagram/basic-profile` | GET | Get Instagram basic profile | 1 | standard | 900s |
| `/v1/instagram/comment` | GET | Look up one Instagram comment by URL or id | 5-15 (metered) | custom | 300s |
| `/v1/instagram/engagement` | GET | Get Instagram engagement statistics | 5 | advanced | 1800s |
| `/v1/instagram/followers` | GET | List Instagram followers | 5 | advanced | 900s |
| `/v1/instagram/following` | GET | List Instagram following | 5 | advanced | 900s |
| `/v1/instagram/highlight/detail` | GET | Get Instagram highlight detail | 1 | standard | 600s |
| `/v1/instagram/highlights` | GET | List Instagram story highlights | 1 | standard | 900s |
| `/v1/instagram/location/posts` | GET | List recent posts at an Instagram location | 5 | advanced | 600s |
| `/v1/instagram/media/transcript` | GET | Get Instagram media transcript | 10 | premium | 2592000s |
| `/v1/instagram/music/trending` | GET | List trending Instagram music | 5 | advanced | 120s |
| `/v1/instagram/post` | GET | Get Instagram post details | 1 | standard | 600s |
| `/v1/instagram/post/comment/replies` | GET | List replies under an Instagram comment | 1 | standard | 300s |
| `/v1/instagram/post/comments` | GET | List Instagram post comments | 5 | advanced | 300s |
| `/v1/instagram/post/likers` | GET | List Instagram post likers | 5 | advanced | 900s |
| `/v1/instagram/post/stats` | GET | Get Instagram post stats including the share count | 5 | advanced | 600s |
| `/v1/instagram/profile` | GET | Get Instagram user profile | 1 | standard | 900s |
| `/v1/instagram/profile/about` | GET | Get Instagram account transparency details | 1 | standard | 900s |
| `/v1/instagram/profile/full` | GET | Instagram profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/instagram/profile/posts` | GET | List Instagram user posts | 1 | standard | 600s |
| `/v1/instagram/profile/posts/full` | GET | Instagram posts with views, likes, comments, and per-post share counts where available, in one call. | 5-25 (metered) | advanced | 600s |
| `/v1/instagram/profile/reels` | GET | List Instagram user reels | 1 | standard | 600s |
| `/v1/instagram/profile/reels/full` | GET | Instagram reels with views, likes, comments, and per-reel share counts where available, in one call. | 5-25 (metered) | advanced | 600s |
| `/v1/instagram/reels/trending` | GET | Get trending Instagram reels | 5 | advanced | 120s |
| `/v1/instagram/search` | GET | Search Instagram accounts, hashtags, and places | 1 | standard | 120s |
| `/v1/instagram/search/hashtag` | GET | Search Instagram posts by hashtag | 5 | advanced | 120s |
| `/v1/instagram/search/location` | GET | Search Instagram locations | 5 | advanced | 120s |
| `/v1/instagram/search/music` | GET | Search Instagram music | 5 | advanced | 21600s |
| `/v1/instagram/search/popular` | GET | Search popular Instagram posts | 1 | standard | 120s |
| `/v1/instagram/search/profiles` | GET | Search Instagram profiles by keyword | 1 | standard | 120s |
| `/v1/instagram/search/reels` | GET | Search Instagram reels | 1 | standard | 120s |
| `/v1/instagram/similar` | GET | List similar Instagram accounts | 5 | advanced | 900s |
| `/v1/instagram/stories` | GET | List an Instagram user's active stories | 5 | advanced | 600s |
| `/v1/instagram/story/download` | GET | Download a single Instagram story | 5 | advanced | 600s |
| `/v1/instagram/tagged` | GET | List posts an Instagram user is tagged in | 5 | advanced | 600s |
| `/v1/instagram/user/embed` | GET | Get Instagram user embed HTML | 1 | standard | 900s |
| `/v1/instagram/username-suggestions` | GET | Get Instagram username suggestions | 5 | advanced | 120s |

### Jobs (11)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/jobs/bing` | GET | Get a Bing job listing by id | 5 | advanced | 600s |
| `/v1/jobs/bing/search` | GET | Search Bing job listings | 10 | premium | 120s |
| `/v1/jobs/indeed` | GET | Get an Indeed job listing by id | 5 | advanced | 600s |
| `/v1/jobs/indeed/search` | GET | Search Indeed job listings | 10 | premium | 120s |
| `/v1/jobs/linkedin` | GET | Get a LinkedIn job listing by id | 5 | advanced | 600s |
| `/v1/jobs/linkedin/organizations` | GET | Resolve LinkedIn organization ids | 1 | standard | 120s |
| `/v1/jobs/linkedin/search` | GET | Search LinkedIn job listings | 10 | premium | 120s |
| `/v1/jobs/salary` | GET | Get salary ranges for a job title and country | 1 | standard | 1800s |
| `/v1/jobs/salary/titles` | GET | Suggest job titles for a salary lookup | 1 | standard | 1800s |
| `/v1/jobs/xing` | GET | Get a Xing job listing by id | 5 | advanced | 600s |
| `/v1/jobs/xing/search` | GET | Search Xing job listings | 10 | premium | 120s |

### Kick (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/kick/clip` | GET | Get Kick clip details | 1 | standard | 600s |

### Klarna (18)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/klarna/categories` | GET | List Klarna root categories | 1 | standard | 1800s |
| `/v1/klarna/categories/children` | GET | Get Klarna sub-categories | 1 | standard | 1800s |
| `/v1/klarna/category` | GET | Browse Klarna products in a category | 5 | advanced | 120s |
| `/v1/klarna/category/filters` | GET | Get Klarna filters for a category | 1 | standard | 1800s |
| `/v1/klarna/category/guide` | GET | Get Klarna buying-guide content for a category | 1 | standard | 1800s |
| `/v1/klarna/category/keywords` | GET | Get popular Klarna search keywords for a category | 1 | standard | 120s |
| `/v1/klarna/product` | GET | Get a Klarna product by id or URL | 5 | advanced | 600s |
| `/v1/klarna/product/compare` | GET | Compare two Klarna products | 5 | advanced | 600s |
| `/v1/klarna/product/offers` | GET | List merchant offers for a Klarna product | 5 | advanced | 600s |
| `/v1/klarna/product/price-history` | GET | Get Klarna price history for a product | 5 | advanced | 1800s |
| `/v1/klarna/reviews` | GET | Get Klarna user reviews for a product | 5 | advanced | 300s |
| `/v1/klarna/reviews/overview` | GET | Get Klarna review totals and score distributions | 5 | advanced | 1800s |
| `/v1/klarna/reviews/pro` | GET | Get Klarna professional reviews for a product | 5 | advanced | 300s |
| `/v1/klarna/search` | GET | Search Klarna products by keyword | 5 | advanced | 120s |
| `/v1/klarna/search/suggestions` | GET | Get Klarna search suggestions | 1 | standard | 120s |
| `/v1/klarna/store/filters` | GET | Get Klarna filters for a store page | 1 | standard | 1800s |
| `/v1/klarna/store/products` | GET | List products from a Klarna store | 5 | advanced | 120s |
| `/v1/klarna/stores` | GET | List Klarna shopping stores | 1 | standard | 1800s |

### Kohl's (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/kohls/categories` | GET | Get the Kohl's category tree | 1 | standard | 1800s |
| `/v1/kohls/questions` | GET | Get Kohl's product questions and answers | 5 | advanced | 300s |
| `/v1/kohls/reviews` | GET | Get Kohl's product reviews | 5 | advanced | 300s |
| `/v1/kohls/search` | GET | Search Kohl's products by keyword | 5 | advanced | 120s |
| `/v1/kohls/stores` | GET | Find Kohl's stores near a coordinate | 5 | advanced | 1800s |

### Komi (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/komi/page` | GET | Get Komi page | 1 | standard | 900s |

### Kwai (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/kwai/post` | GET | Get a Kwai post | 1 | standard | 600s |
| `/v1/kwai/profile` | GET | Get a Kwai user profile | 1 | standard | 900s |
| `/v1/kwai/user/posts` | GET | List a Kwai user's posts | 1 | standard | 600s |

### LinkBio (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/linkbio/page` | GET | Get Linkbio page | 1 | standard | 900s |

### LinkedIn (45)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/linkedin/ad` | GET | Get LinkedIn ad details | 5 | advanced | 1800s |
| `/v1/linkedin/ads/search` | GET | Search LinkedIn ads | 5 | advanced | 120s |
| `/v1/linkedin/company` | GET | Get LinkedIn company page with its full About tab | 5 | advanced | 900s |
| `/v1/linkedin/company/affiliated-pages` | GET | List a company's affiliated/showcase pages | 5 | advanced | 900s |
| `/v1/linkedin/company/insights` | GET | Get aggregate insights about a company's members | 5 | advanced | 1800s |
| `/v1/linkedin/company/job-count` | GET | Get a company's open job count | 5 | advanced | 1800s |
| `/v1/linkedin/company/jobs` | GET | List a company's job postings | 10 | premium | 120s |
| `/v1/linkedin/company/people` | GET | List people at a LinkedIn company | 10 | premium | 900s |
| `/v1/linkedin/company/posts` | GET | List LinkedIn company posts | 5 | advanced | 600s |
| `/v1/linkedin/group` | GET | Get LinkedIn group details | 5 | advanced | 900s |
| `/v1/linkedin/group/posts` | GET | List posts in a LinkedIn group | 5 | advanced | 600s |
| `/v1/linkedin/job` | GET | Get LinkedIn job details | 5 | advanced | 600s |
| `/v1/linkedin/post` | GET | Get LinkedIn post details | 5 | advanced | 600s |
| `/v1/linkedin/post/comments` | GET | Get LinkedIn post comments | 5 | advanced | 600s |
| `/v1/linkedin/post/comments/replies` | GET | List replies to a LinkedIn comment | 5 | advanced | 300s |
| `/v1/linkedin/post/reactions` | GET | List reactors on a LinkedIn post | 10 | premium | 300s |
| `/v1/linkedin/post/reposts` | GET | List reposts of a LinkedIn post | 5 | advanced | 600s |
| `/v1/linkedin/post/transcript` | GET | Get a LinkedIn post video transcript | 10 | premium | 2592000s |
| `/v1/linkedin/profile` | GET | Get LinkedIn user profile | 5 | advanced | 900s |
| `/v1/linkedin/profile/about` | GET | Get a member's account freshness signals (NOT the profile About section) | 5 | advanced | 900s |
| `/v1/linkedin/profile/certifications` | GET | List a member's licenses and certifications | 5 | advanced | 900s |
| `/v1/linkedin/profile/comments` | GET | List a member's comments | 5 | advanced | 300s |
| `/v1/linkedin/profile/contact` | GET | Get a member's public contact info | 5 | advanced | 900s |
| `/v1/linkedin/profile/educations` | GET | List a member's education history | 5 | advanced | 900s |
| `/v1/linkedin/profile/experiences` | GET | List a member's work experiences | 5 | advanced | 900s |
| `/v1/linkedin/profile/full` | GET | LinkedIn company profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/linkedin/profile/honors` | GET | List a member's honors and awards | 5 | advanced | 900s |
| `/v1/linkedin/profile/images` | GET | List a member's image posts | 5 | advanced | 600s |
| `/v1/linkedin/profile/interests/companies` | GET | List companies a member follows | 5 | advanced | 900s |
| `/v1/linkedin/profile/interests/groups` | GET | List groups a member follows | 5 | advanced | 900s |
| `/v1/linkedin/profile/posts` | GET | List a LinkedIn member's posts | 5 | advanced | 600s |
| `/v1/linkedin/profile/posts/archive` | GET | Walk a LinkedIn member's COMPLETE post history, 100 posts a page, with exact publish times and share counts the other lanes cannot return. Metered: 5 credits per post returned, so try the cheaper /v1/linkedin/profile/posts first | 5-500 (metered) | advanced | 600s |
| `/v1/linkedin/profile/publications` | GET | List a member's publications | 5 | advanced | 900s |
| `/v1/linkedin/profile/reactions` | GET | List posts a LinkedIn member reacted to | 5 | advanced | 600s |
| `/v1/linkedin/profile/recommendations` | GET | List recommendations for a member | 5 | advanced | 900s |
| `/v1/linkedin/profile/skills` | GET | List a member's skills | 5 | advanced | 900s |
| `/v1/linkedin/profile/stats` | GET | Get a member's follower + connection counts | 5 | advanced | 900s |
| `/v1/linkedin/profile/videos` | GET | List a member's video posts | 5 | advanced | 600s |
| `/v1/linkedin/profile/volunteers` | GET | List a member's volunteer experiences | 5 | advanced | 900s |
| `/v1/linkedin/search/industry` | GET | Resolve an industry name to a LinkedIn industry id | 1 | standard | 120s |
| `/v1/linkedin/search/jobs` | GET | Search LinkedIn jobs | 10 | premium | 120s |
| `/v1/linkedin/search/location` | GET | Resolve a location to a LinkedIn geocode id | 1 | standard | 120s |
| `/v1/linkedin/search/people` | GET | Search LinkedIn people | 10 | premium | 120s |
| `/v1/linkedin/search/posts` | GET | Search public LinkedIn posts by keyword | 5 | advanced | 120s |
| `/v1/linkedin/search/schools` | GET | Search LinkedIn schools | 1 | standard | 120s |

### LinkMe (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/linkme/page` | GET | Get Linkme profile | 1 | standard | 900s |

### Linktree (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/linktree/page` | GET | Get Linktree page | 1 | standard | 900s |

### Naver (14)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/naver/adult` | GET | Check whether a Korean search term is adult-only (성인 검색어 판별) | 1 | standard | 1800s |
| `/v1/naver/blog/search` | GET | Search Naver Blog | 1 | standard | 120s |
| `/v1/naver/brief` | GET | One query across the Korean internet (5 Naver corpora) + optional digest. | 10 | custom | 120s |
| `/v1/naver/cafearticle/search` | GET | Search Naver Cafe articles | 1 | standard | 120s |
| `/v1/naver/encyc/search` | GET | Search Naver Encyclopedia | 1 | standard | 120s |
| `/v1/naver/errata` | GET | Correct a mistyped Korean search query (오타변환) | 1 | standard | 1800s |
| `/v1/naver/image/search` | GET | Search Naver Image | 1 | standard | 120s |
| `/v1/naver/kin/search` | GET | Search Naver KnowledgeiN (지식iN) | 1 | standard | 120s |
| `/v1/naver/local/search` | GET | Search Naver Local (장소 검색) | 1 | standard | 120s |
| `/v1/naver/news/search` | GET | Search Naver News | 1 | standard | 120s |
| `/v1/naver/search-trend` | GET | Get Naver search-volume trend for Korean keywords (검색어트렌드) | 5 | advanced | 1800s |
| `/v1/naver/shopping-insight/category` | GET | Get Naver Shopping click trend for a category (쇼핑인사이트) | 5 | advanced | 1800s |
| `/v1/naver/shopping-insight/keyword` | GET | Get Naver Shopping click trend for keywords inside a category (쇼핑인사이트) | 5 | advanced | 1800s |
| `/v1/naver/webkr/search` | GET | Search Naver Web (웹문서) | 1 | standard | 120s |

### On-Page (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/on_page/page` | GET | Run an on-page SEO audit for one URL | 1 | standard | 1800s |

### Perplexity (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/perplexity/research` | GET | Web research via Perplexity Sonar | 1 | standard | 120s |

### Pillar (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/pillar/page` | GET | Get Pillar page | 1 | standard | 900s |

### Pinterest (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/pinterest/board` | GET | Get Pinterest board | 1 | standard | 600s |
| `/v1/pinterest/pin` | GET | Get Pinterest pin details | 1 | standard | 600s |
| `/v1/pinterest/search` | GET | Search Pinterest pins | 1 | standard | 120s |
| `/v1/pinterest/url-stats` | GET | Get Pinterest save counts for external URLs | 1 | standard | 1800s |
| `/v1/pinterest/user/boards` | GET | List Pinterest user boards | 1 | standard | 900s |

### Polymarket (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/polymarket/research` | GET | Polymarket prediction markets: multi-query research | 5 | advanced | 120s |

### Prism (33)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/prism/ai-visibility` | GET | AI Share-of-Voice / GEO monitoring: prompt set x reruns to per-brand appearance-% per AI engine plus a cited-domain ranking. | 2-1605 (metered) | custom | 120s |
| `/v1/prism/answers` | GET | Multi-engine AI consensus: one question → Perplexity + Grok + Tavily answers verbatim, merged citations, and an agreement matrix. | 15 | custom | 120s |
| `/v1/prism/app-reviews` | GET | Cross-store app review intelligence (Google Play + App Store): translated, clustered, sentiment-scored. | 10-15 (metered) | custom | 300s |
| `/v1/prism/apps-lookup` | GET | One app across Google Play + the App Store: resolved, title-matched, and compared into a cross-store rating + listing report. | 30 | custom | 1800s |
| `/v1/prism/audience-overlap` | GET | How much two TikTok creators' commenter audiences overlap. Jaccard, shared-fan count, and a confidence label. | 20 | custom | 1800s |
| `/v1/prism/audience-questions` | GET | The real questions a topic's audience asks: harvested from Reddit + YouTube threads and clustered by intent (who/what/why/how/vs). | 30 | custom | 1800s |
| `/v1/prism/brand-mentions` | GET | Brand mention volume time-series, sentiment split, top sources, and recent mentions for one keyword. | 50 | custom | 1800s |
| `/v1/prism/campaign` | GET | Campaign tracker: pre/during/post volume lift, cross-platform engagement, and ranked top amplifiers for a hashtag or phrase. | 35 | custom | 1800s |
| `/v1/prism/comment-lookup` | POST | Re-check up to 25 known comments in one call: per-item results, failed items refunded. | 2-100 (metered) | custom | none |
| `/v1/prism/comments` | GET | Every comment on a post, replies nested, server-paginated to completion. | 2-200 (metered) | standard | 300s |
| `/v1/prism/creator-card` | GET | One handle, unified author cards across TikTok, Instagram, YouTube, X (and more). | 5-8 (metered) | custom | 900s |
| `/v1/prism/creator-vet` | GET | Vet a creator before partnering: engagement quality, commenter authenticity, posting cadence, and controversy signals, optionally across platforms. | 50-75 (metered) | custom | 1800s |
| `/v1/prism/crisis-postmortem` | GET | Crisis post-mortem: a who-said-what-first timeline across web, Reddit, Hacker News, and social, with an origin, peak, propagation sequence, and a grounded narrative. | 35 | custom | 1800s |
| `/v1/prism/crisis-radar` | GET | Stateless crisis breach check: a z-score on daily mention volume and negative share, with on-breach confirmation and a severity grade. | 15-45 (metered) | custom | 1800s |
| `/v1/prism/demand-signals` | GET | Consumer-demand nowcast: app-review velocity, web mention slope, Reddit velocity, and commerce review levels, fused into a published demand index. | 30 | custom | 300s |
| `/v1/prism/devtool-pulse` | GET | Developer-brand health: a devtool's repo dossier + Hacker News reaction + Reddit chatter + dev-blog echo, in one call. | 20 | custom | 1800s |
| `/v1/prism/earned-media` | GET | A brand's earned-media footprint: news + tech-press + fresh-web clips, deduped and ranked, with an outlet-coverage rollup. | 25 | custom | 1800s |
| `/v1/prism/employer-brand` | GET | A company's employer brand: what people say about working there across Reddit, the web, YouTube, Naver, and the company's own LinkedIn voice. | 30 | custom | 1800s |
| `/v1/prism/handle-audit` | GET | Should you pull this handle? One call scores a handle across platforms, ranks the best ones, and projects the data volume + credit cost to pull it. | 5-8 (metered) | custom | 1800s |
| `/v1/prism/korea-gap` | GET | What the world is talking about that Korea isn't (and vice versa): the global vs Korean (Naver) conversation gap for a brand/topic. | 15-40 (metered) | custom | 1800s |
| `/v1/prism/launch-echo` | GET | How a launch landed: the Hacker News reaction (top threads + comments), the dev-blog echo, and an optional repo dossier. | 20 | custom | 1800s |
| `/v1/prism/leads` | GET | Ranked feed of public conversations where people seek alternatives to or are switching from a competitor. | 50 | custom | 1800s |
| `/v1/prism/lookup` | GET | Universal post/product URL dispatcher: any post, video, product or repo link → the right detail endpoint's unified response. | 0 | custom | 600s |
| `/v1/prism/org-radar` | GET | A GitHub org's footprint: its top repos each expanded into a full dossier (releases, issue load, top request/complaint), rolled up. | 6-51 (metered) | custom | 1800s |
| `/v1/prism/post-stats` | POST | Up to 100 mixed-platform post URLs → current engagement per URL, failed URLs refunded. | 1-500 (metered) | custom | none |
| `/v1/prism/product-reviews` | GET | A product's reviews across Amazon + Google Shopping + Trustpilot, folded into a cross-marketplace rating + themed pros/cons report. | 30 | custom | 1800s |
| `/v1/prism/profiles` | POST | Up to 50 (platform, handle) pairs → one canonical Author per row, failed handles refunded. | 1-250 (metered) | custom | none |
| `/v1/prism/reputation` | GET | A brand's cross-source reputation. Trustpilot + app stores + Google Business + web sentiment, blended into one weighted score with themed pros/cons. | 30 | custom | 1800s |
| `/v1/prism/review-integrity` | GET | Cross-source review integrity verdict (statistical, deterministic). | 30 | custom | 1800s |
| `/v1/prism/share-of-voice` | GET | Engagement-weighted Share of Voice across 2-5 brands, with web+social split, emotion overlay, and ESOV. | 20-200 (metered) | custom | 1800s |
| `/v1/prism/truthsocial-pulse` | GET | A Truth Social handle's pulse: profile, recent posts, per-post detail drill, and the news echo, in one call. | 20 | custom | 1800s |
| `/v1/prism/video-intel` | GET | One video URL → detail + stats + transcript + top comments + commenter sample, across YouTube/TikTok/Rumble/Instagram. | 5-15 (metered) | custom | 600s |
| `/v1/prism/voice` | GET | One person's public posts across X, Threads, Bluesky, and Truth Social, time-merged. | 5 | custom | 600s |

### Quora (7)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/quora/answers` | GET | Search Quora answers | 5 | advanced | 120s |
| `/v1/quora/post` | GET | Get a Quora question | 5 | advanced | 600s |
| `/v1/quora/posts` | GET | Search Quora space posts | 5 | advanced | 120s |
| `/v1/quora/profiles` | GET | Search Quora profiles | 5 | advanced | 120s |
| `/v1/quora/search` | GET | Search Quora questions | 5 | advanced | 120s |
| `/v1/quora/spaces` | GET | Search Quora Spaces | 5 | advanced | 120s |
| `/v1/quora/topics` | GET | Search Quora topics | 5 | advanced | 120s |

### Reddit (14)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/reddit/omni-search` | GET | Reddit VoC sweep: one keyword → threads across all of Reddit with subreddit attribution and top comments inline. | 5-9 (metered) | standard | 120s |
| `/v1/reddit/post` | GET | Get a Reddit post | 1 | standard | 600s |
| `/v1/reddit/post/comments` | GET | List Reddit post comments | 5 | advanced | 300s |
| `/v1/reddit/post/transcript` | GET | Get a Reddit video post transcript | 10 | premium | 2592000s |
| `/v1/reddit/profile` | GET | Get a Reddit user profile | 1 | standard | 900s |
| `/v1/reddit/profile/comments` | GET | Read a Reddit account's own comment history, newest first, deeper than any search index reaches. Metered: 2 credits per comment returned, so try /v1/reddit/search/comments?query=author:name first | 2-200 (metered) | standard | 600s |
| `/v1/reddit/profile/posts` | GET | List a Reddit user's posts | 1 | standard | 600s |
| `/v1/reddit/search` | GET | Search Reddit posts | 1-26 (metered) | standard | 120s |
| `/v1/reddit/search/comments` | GET | Search Reddit comments | 1 | standard | 120s |
| `/v1/reddit/search/media` | GET | Search Reddit image and video posts | 1 | standard | 120s |
| `/v1/reddit/subreddit` | GET | List Reddit subreddit posts | 1 | standard | 600s |
| `/v1/reddit/subreddit/details` | GET | Get Reddit subreddit details | 1 | standard | 900s |
| `/v1/reddit/subreddit/search` | GET | Search within a subreddit | 1-26 (metered) | standard | 120s |
| `/v1/reddit/subreddits/search` | GET | Find subreddits by topic | 1 | standard | 120s |

### Rumble (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/rumble/channel/videos` | GET | List videos for a Rumble channel | 1 | standard | 600s |
| `/v1/rumble/search` | GET | Search Rumble videos | 1 | standard | 120s |
| `/v1/rumble/video` | GET | Get a Rumble video | 1 | standard | 600s |
| `/v1/rumble/video/comments` | GET | List top-level comments on a Rumble video | 1 | standard | 300s |
| `/v1/rumble/video/transcript` | GET | Get a Rumble video transcript | 10 | premium | 2592000s |

### Sephora (11)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/sephora/availability` | GET | Get Sephora in-store availability for a sku | 5 | advanced | 600s |
| `/v1/sephora/brand/products` | GET | List Sephora products for a brand | 5 | advanced | 120s |
| `/v1/sephora/brands` | GET | List Sephora brands | 1 | standard | 1800s |
| `/v1/sephora/categories` | GET | List Sephora root categories | 1 | standard | 1800s |
| `/v1/sephora/category` | GET | Browse Sephora products in a category | 5 | advanced | 120s |
| `/v1/sephora/category/data` | GET | Get a Sephora category and its children | 1 | standard | 1800s |
| `/v1/sephora/product` | GET | Get a Sephora product by id or URL | 5 | advanced | 600s |
| `/v1/sephora/reviews` | GET | Get Sephora product reviews | 5 | advanced | 300s |
| `/v1/sephora/search` | GET | Search Sephora products by keyword | 5 | advanced | 120s |
| `/v1/sephora/search/suggestions` | GET | Get Sephora search suggestions | 1 | standard | 120s |
| `/v1/sephora/stores` | GET | Find Sephora stores near a coordinate | 1 | standard | 1800s |

### Snapchat (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/snapchat/profile` | GET | Get Snapchat user profile | 1 | standard | 900s |
| `/v1/snapchat/spotlight/comments` | GET | List comments on a Snapchat Spotlight | 1 | standard | 300s |

### Spotify (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/spotify/album` | GET | Get a Spotify album | 1 | standard | 600s |
| `/v1/spotify/artist` | GET | Get a Spotify artist | 1 | standard | 900s |
| `/v1/spotify/podcast` | GET | Get a Spotify podcast | 1 | standard | 900s |
| `/v1/spotify/podcast/episodes` | GET | List a Spotify podcast's episodes | 1 | standard | 600s |
| `/v1/spotify/search` | GET | Search Spotify | 1 | standard | 120s |
| `/v1/spotify/track` | GET | Get a Spotify track | 1 | standard | 600s |

### Target (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/target/categories` | GET | List the Target category taxonomy | 1 | standard | 1800s |
| `/v1/target/category` | GET | Browse Target products in a category | 5 | advanced | 120s |
| `/v1/target/product` | GET | Get a Target product by TCIN | 5 | advanced | 600s |
| `/v1/target/reviews` | GET | Get Target product reviews | 5 | advanced | 300s |
| `/v1/target/stores` | GET | Find Target stores near a location | 1 | standard | 1800s |

### Tavily (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tavily/crawl` | GET | Crawl a website with LLM-driven path selection | 1 | standard | 1800s |
| `/v1/tavily/extract` | GET | Extract clean content from one or more URLs | 1 | standard | 600s |
| `/v1/tavily/map` | GET | Map a website's sitegraph | 1 | standard | 1800s |
| `/v1/tavily/search` | GET | Tavily web search with optional LLM-generated answer | 1 | standard | 120s |

### Telegram (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/telegram/post` | GET | Get Telegram post | 1 | standard | 600s |
| `/v1/telegram/profile` | GET | Get Telegram channel profile | 1 | standard | 900s |
| `/v1/telegram/profile/posts` | GET | List Telegram channel posts | 1 | standard | 600s |

### Threads (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/threads/post` | GET | Get Threads post details | 1 | standard | 600s |
| `/v1/threads/post/comments` | GET | Get comments on a Threads post | 1-10 (metered) | standard | 300s |
| `/v1/threads/profile` | GET | Get Threads user profile | 1 | standard | 900s |
| `/v1/threads/search` | GET | Search Threads posts | 1-11 (metered) | standard | 120s |
| `/v1/threads/search/users` | GET | Search Threads users | 1 | standard | 120s |
| `/v1/threads/user/posts` | GET | List Threads user posts | 1 | standard | 600s |

### TikTok (34)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tiktok/adlibrary/ad` | GET | Get a TikTok Ad Library ad | 5 | advanced | 1800s |
| `/v1/tiktok/adlibrary/search` | GET | Search the TikTok Ad Library | 5 | advanced | 120s |
| `/v1/tiktok/ads/top` | GET | Read TikTok's Creative Center Top Ads board: the best-performing ads in a market, ranked by CTR, impressions or engagement. Metered: 1 credit per ad returned, minimum 10 | 10-100 (metered) | standard | 1800s |
| `/v1/tiktok/collection/videos` | GET | List videos in a TikTok collection | 1 | standard | 600s |
| `/v1/tiktok/comment` | GET | Look up one TikTok comment by URL or id | 2-6 (metered) | custom | 300s |
| `/v1/tiktok/effect/videos` | GET | List TikTok videos made with an effect | 1 | standard | 600s |
| `/v1/tiktok/effects` | GET | Get TikTok effects by id | 1 | standard | 600s |
| `/v1/tiktok/hashtag` | GET | Get TikTok hashtag details | 1 | standard | 600s |
| `/v1/tiktok/location/posts` | GET | List TikTok videos tagged at a place | 1 | standard | 600s |
| `/v1/tiktok/playlist/videos` | GET | List videos in a TikTok playlist | 1 | standard | 600s |
| `/v1/tiktok/post` | GET | Get TikTok post details | 1 | standard | 600s |
| `/v1/tiktok/post/comments` | GET | List TikTok post comments | 1 | standard | 300s |
| `/v1/tiktok/post/transcript` | GET | Get TikTok video transcript | 10 | premium | 2592000s |
| `/v1/tiktok/profile` | GET | Get TikTok user profile | 1 | standard | 900s |
| `/v1/tiktok/profile/full` | GET | TikTok profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/tiktok/profile/playlists` | GET | List a TikTok account's playlists | 1 | standard | 900s |
| `/v1/tiktok/profile/region` | GET | Get TikTok profile region | 1 | standard | 900s |
| `/v1/tiktok/profile/videos` | GET | List TikTok user videos | 1 | standard | 600s |
| `/v1/tiktok/search` | GET | Search TikTok videos by keyword | 1 | standard | 120s |
| `/v1/tiktok/search/hashtag` | GET | Search TikTok by hashtag | 1 | standard | 120s |
| `/v1/tiktok/search/music` | GET | Search TikTok sounds | 1 | standard | 120s |
| `/v1/tiktok/search/suggestions` | GET | Get TikTok search suggestions | 1 | standard | 120s |
| `/v1/tiktok/search/top` | GET | TikTok top search results | 1 | standard | 120s |
| `/v1/tiktok/search/users` | GET | Search TikTok users | 1 | standard | 120s |
| `/v1/tiktok/song` | GET | Get TikTok song details | 1 | standard | 600s |
| `/v1/tiktok/song/videos` | GET | List TikTok videos using a song | 1 | standard | 600s |
| `/v1/tiktok/trending` | GET | Get TikTok trending feed | 5 | advanced | 120s |
| `/v1/tiktok/user/audience` | GET | Get TikTok user audience demographics | 5 | advanced | 1800s |
| `/v1/tiktok/user/followers` | GET | List TikTok user followers | 1 | standard | 900s |
| `/v1/tiktok/user/following` | GET | List TikTok user following | 1 | standard | 900s |
| `/v1/tiktok/user/liked` | GET | List the videos a TikTok account has liked | 1 | standard | 600s |
| `/v1/tiktok/user/live` | GET | Get TikTok user live stream | 1 | standard | 60s |
| `/v1/tiktok/video/comment/replies` | GET | List TikTok comment replies | 1 | standard | 300s |
| `/v1/tiktok/video/screen-text` | GET | Get TikTok video on-screen text | 5 | advanced | 600s |

### TikTok Shop (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tiktokshop/product` | GET | Get TikTok Shop product details | 1 | standard | 600s |
| `/v1/tiktokshop/product/reviews` | GET | List TikTok Shop product reviews | 1 | standard | 300s |
| `/v1/tiktokshop/products` | GET | List TikTok Shop products | 1 | standard | 600s |
| `/v1/tiktokshop/search` | GET | Search TikTok Shop products | 1 | standard | 120s |
| `/v1/tiktokshop/user/showcase` | GET | List TikTok user showcase products | 1 | standard | 600s |

### Tripadvisor (16)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tripadvisor/attraction` | GET | Get a TripAdvisor attraction | 1 | standard | 900s |
| `/v1/tripadvisor/attraction/reviews` | GET | Get TripAdvisor reviews for an attraction | 1 | standard | 300s |
| `/v1/tripadvisor/attractions` | GET | Search TripAdvisor attractions and things to do | 1 | standard | 120s |
| `/v1/tripadvisor/autocomplete` | GET | Autocomplete TripAdvisor places | 1 | standard | 120s |
| `/v1/tripadvisor/cruise` | GET | Get a TripAdvisor cruise ship | 1 | standard | 900s |
| `/v1/tripadvisor/cruise/reviews` | GET | Get TripAdvisor reviews for a cruise ship | 1 | standard | 300s |
| `/v1/tripadvisor/cruises` | GET | Search TripAdvisor cruises | 1 | standard | 120s |
| `/v1/tripadvisor/experience-types` | GET | List TripAdvisor experience types for a destination | 1 | standard | 1800s |
| `/v1/tripadvisor/hotel` | GET | Get a TripAdvisor hotel | 1 | standard | 900s |
| `/v1/tripadvisor/hotels` | GET | Search TripAdvisor hotels | 1 | standard | 120s |
| `/v1/tripadvisor/place` | GET | Get a TripAdvisor place by URL | 1 | standard | 900s |
| `/v1/tripadvisor/restaurant` | GET | Get a TripAdvisor restaurant | 1 | standard | 900s |
| `/v1/tripadvisor/restaurant/reviews` | GET | Get TripAdvisor reviews for a restaurant | 1 | standard | 300s |
| `/v1/tripadvisor/restaurants` | GET | Search TripAdvisor restaurants | 1 | standard | 120s |
| `/v1/tripadvisor/reviews` | GET | Get TripAdvisor reviews for a place | 1 | standard | 300s |
| `/v1/tripadvisor/search` | GET | Search TripAdvisor businesses & places | 1 | standard | 120s |

### Trustpilot (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/trustpilot/business-search` | GET | Search Trustpilot businesses | 1 | standard | 120s |
| `/v1/trustpilot/reviews` | GET | Get Trustpilot reviews for a business | 5 | advanced | 300s |

### Truth Social (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/truthsocial/post` | GET | Get Truth Social post details | 1 | standard | 600s |
| `/v1/truthsocial/profile` | GET | Get Truth Social user profile | 1 | standard | 900s |
| `/v1/truthsocial/user/posts` | GET | List Truth Social user posts | 1 | standard | 600s |

### Twitch (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/twitch/clip` | GET | Get Twitch clip details | 1 | standard | 600s |
| `/v1/twitch/profile` | GET | Get Twitch streamer profile | 1 | standard | 900s |
| `/v1/twitch/user/schedule` | GET | Get a Twitch user's stream schedule | 1 | standard | 600s |
| `/v1/twitch/user/videos` | GET | List a Twitch user's videos | 1 | standard | 600s |

### Twitter/X (15)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/twitter/ai-search` | GET | AI-powered X (Twitter) search via xAI Grok | 5 | advanced | 120s |
| `/v1/twitter/community` | GET | Get Twitter community details | 1 | standard | 900s |
| `/v1/twitter/community/tweets` | GET | List Twitter community tweets | 1 | standard | 600s |
| `/v1/twitter/profile` | GET | Get Twitter user profile | 1 | standard | 900s |
| `/v1/twitter/profile/full` | GET | X (Twitter) profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/twitter/search/tweets` | GET | Search Twitter tweets | 1 | standard | 120s |
| `/v1/twitter/search/users` | GET | Search Twitter users | 1 | standard | 120s |
| `/v1/twitter/tweet` | GET | Get Twitter tweet details | 1 | standard | 600s |
| `/v1/twitter/tweet/replies` | GET | List Twitter tweet replies | 1 | standard | 300s |
| `/v1/twitter/tweet/retweeters` | GET | List Twitter tweet retweeters | 1 | standard | 900s |
| `/v1/twitter/tweet/transcript` | GET | Get Twitter video transcript | 10 | premium | 2592000s |
| `/v1/twitter/user/followers` | GET | List Twitter user followers | 1 | standard | 900s |
| `/v1/twitter/user/following` | GET | List Twitter user following | 1 | standard | 900s |
| `/v1/twitter/user/media` | GET | List Twitter user media tweets | 1 | standard | 600s |
| `/v1/twitter/user/tweets` | GET | List Twitter user tweets | 1 | standard | 600s |

### Universal Search (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/search/creators` | GET | Fused creator discovery across TikTok, Threads, and Instagram, ranked by relevance, followers, and verification. | 10 | custom | 120s |
| `/v1/search/everywhere` | GET | Universal social search across 14 platforms | 20 | custom | 120s |
| `/v1/search/forums` | GET | Fused forum search across Reddit, Hacker News, and Naver 지식iN/카페, with top comments inline on hero threads by default. | 10 | custom | 120s |
| `/v1/search/news` | GET | Planned multi-country news search: one query, localized and fanned out across two independent news indexes in a single call. | 2-62 (metered) | standard | 300s |

### US Congress Trades (19)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/us_congress_trades/members` | GET | List members of Congress who have disclosed trades | 1 | standard | 120s |
| `/v1/us_congress_trades/politician` | GET | Get a politician's trading summary | 1 | standard | 1800s |
| `/v1/us_congress_trades/politician/trades` | GET | List trades for one politician | 1 | standard | 120s |
| `/v1/us_congress_trades/state/trades` | GET | List trades from a state's congressional delegation | 1 | standard | 120s |
| `/v1/us_congress_trades/stats` | GET | Dataset summary | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/buy-sell` | GET | Congressional buy vs sell ratio | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/issuers` | GET | Most-traded issuers in Congress | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/party` | GET | Compare trade counts by party | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/politicians` | GET | Most-active congressional traders | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/reporting-gaps` | GET | Politicians ranked by late STOCK Act filings | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/sectors` | GET | Trade counts by industry sector | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/tickers` | GET | Most-traded tickers in Congress | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/unusual` | GET | Tickers with unusual congressional activity | 1 | standard | 1800s |
| `/v1/us_congress_trades/stats/volume` | GET | Congressional trade volume over time | 1 | standard | 1800s |
| `/v1/us_congress_trades/ticker` | GET | Get congressional trading stats for a ticker | 1 | standard | 1800s |
| `/v1/us_congress_trades/ticker/trades` | GET | List congressional trades for a ticker | 1 | standard | 120s |
| `/v1/us_congress_trades/trades` | GET | Search US Congress stock trades | 1 | standard | 120s |
| `/v1/us_congress_trades/trades/latest` | GET | Latest US Congress trades (48 hours) | 1 | standard | 120s |
| `/v1/us_congress_trades/trades/recent` | GET | Recent US Congress trades (7 days) | 1 | standard | 120s |

### Utility (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/utility/endpoint` | GET | How to use any endpoint | 0 | custom | 1800s |
| `/v1/utility/endpoints` | GET | List every available endpoint | 0 | custom | 1800s |
| `/v1/utility/llms` | GET | AI-agent context payload | 0 | custom | 1800s |
| `/v1/utility/quickstart` | GET | Get started in one call | 0 | custom | 1800s |

### Walmart (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/walmart/category` | GET | Browse Walmart products in a category | 5 | advanced | 120s |
| `/v1/walmart/offers` | GET | Get every seller offering a Walmart product | 5 | advanced | 600s |
| `/v1/walmart/product` | GET | Get a Walmart product by id | 5 | advanced | 600s |
| `/v1/walmart/reviews` | GET | Get Walmart product reviews | 5 | advanced | 300s |
| `/v1/walmart/search` | GET | Search Walmart products by keyword | 5 | advanced | 120s |

### Wayfair (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/wayfair/product` | GET | Get a Wayfair product by SKU | 5 | advanced | 600s |
| `/v1/wayfair/reviews` | GET | Get Wayfair product reviews | 5 | advanced | 300s |
| `/v1/wayfair/search` | GET | Search Wayfair products | 5 | advanced | 120s |

### Web Scraping (22)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/web/agent` | POST | Start an async web agent job | 25 | custom | none |
| `/v1/web/batch-scrape` | POST | Start an async batch scrape | 1 | custom | none |
| `/v1/web/crawl` | POST | Start an async web crawl | 1-10000 (metered) | custom | none |
| `/v1/web/extract` | GET | Extract structured data from a web page | 5 (metered) | custom | none |
| `/v1/web/jobs` | GET | List async web jobs | 0 | custom | none |
| `/v1/web/jobs/{job_id}` | GET | Get an async web job | 0 | custom | none |
| `/v1/web/jobs/{job_id}` | DELETE | Cancel an async web job | 0 | custom | none |
| `/v1/web/map` | GET | Map URLs on a site | 1 | custom | 120s |
| `/v1/web/monitors` | GET | List web monitors | 0 | custom | none |
| `/v1/web/monitors` | POST | Create a web monitor | 0 | custom | none |
| `/v1/web/monitors/{monitor_id}` | GET | Get a web monitor | 0 | custom | none |
| `/v1/web/monitors/{monitor_id}` | PATCH | Update a web monitor | 0 | custom | none |
| `/v1/web/monitors/{monitor_id}` | DELETE | Delete a web monitor | 0 | custom | none |
| `/v1/web/monitors/{monitor_id}/checks` | GET | List web monitor checks | 0 | custom | none |
| `/v1/web/parse` | POST | Parse an uploaded document | 1 | custom | none |
| `/v1/web/scrape` | GET | Scrape a web page | 1-5 (metered) | custom | none |
| `/v1/web/search` | GET | Search the web | 2-120 (metered) | custom | 120s |
| `/v1/web/sessions` | GET | List interactive web sessions | 0 | custom | none |
| `/v1/web/sessions` | POST | Create an interactive web session | 5 | custom | none |
| `/v1/web/sessions/{session_id}` | GET | Get an interactive web session | 0 | custom | none |
| `/v1/web/sessions/{session_id}` | DELETE | Close an interactive web session | 0 | custom | none |
| `/v1/web/sessions/{session_id}/execute` | POST | Execute an interaction in a web session | 0 | custom | none |

### Yelp (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/yelp/business/info` | GET | Get a Yelp business by encid | 1 | standard | 900s |
| `/v1/yelp/business/reviews` | GET | Get Yelp reviews for a business | 5 | advanced | 300s |
| `/v1/yelp/search` | GET | Search Yelp businesses | 1 | standard | 120s |
| `/v1/yelp/search/full` | GET | Search Yelp businesses with full cards | 1 | standard | 120s |
| `/v1/yelp/search/suggestions` | GET | Get Yelp search suggestions | 1 | standard | 120s |

### YouTube (29)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/youtube/channel` | GET | Get YouTube channel info | 1 | standard | 900s |
| `/v1/youtube/channel/about` | GET | Get a YouTube channel's contact email and country. Try the 1-credit youtube/channel first: it already carries the email for some channels, and you are charged here only when an address is returned | 60 | custom | 900s |
| `/v1/youtube/channel/community-posts` | GET | List a YouTube channel's community posts | 1 | standard | 600s |
| `/v1/youtube/channel/lives` | GET | List a YouTube channel's live streams | 1 | standard | 600s |
| `/v1/youtube/channel/playlists` | GET | List a YouTube channel's playlists | 1 | standard | 600s |
| `/v1/youtube/channel/shorts` | GET | List YouTube channel shorts | 1 | standard | 600s |
| `/v1/youtube/channel/videos` | GET | List YouTube channel videos | 1 | standard | 600s |
| `/v1/youtube/channels` | POST | Batch get YouTube channel details (up to 1000) | 5-100 (metered) | advanced | none |
| `/v1/youtube/community-post` | GET | Get YouTube community post | 1 | standard | 600s |
| `/v1/youtube/playlist` | GET | Get YouTube playlist | 1 | standard | 600s |
| `/v1/youtube/playlist/items` | GET | List the videos in a YouTube playlist | 1 | standard | 600s |
| `/v1/youtube/profile/full` | GET | YouTube profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/youtube/search` | GET | Search YouTube | 1 | standard | 120s |
| `/v1/youtube/search/advanced` | GET | Advanced YouTube video search | 1-6 (metered) | standard | 120s |
| `/v1/youtube/search/hashtag` | GET | Search YouTube by hashtag | 1 | standard | 120s |
| `/v1/youtube/search/suggestions` | GET | Get YouTube search suggestions | 1 | standard | 120s |
| `/v1/youtube/shorts/trending` | GET | Get trending YouTube shorts | 5 | advanced | 120s |
| `/v1/youtube/transcripts` | POST | Up to 100 YouTube video ids → one transcript per row, failed ids refunded. | 3-300 (metered) | custom | none |
| `/v1/youtube/video` | GET | Get YouTube video details | 1 | standard | 600s |
| `/v1/youtube/video/audio` | GET | Get a YouTube video's audio file streams | 5 | advanced | none |
| `/v1/youtube/video/comment/replies` | GET | List YouTube comment replies | 1 | standard | 300s |
| `/v1/youtube/video/comments` | GET | List YouTube video comments | 1 | standard | 300s |
| `/v1/youtube/video/files` | GET | Get a YouTube video's video file streams | 5 | advanced | none |
| `/v1/youtube/video/sponsors` | GET | Detect sponsors of a YouTube video | 10 | premium | 1800s |
| `/v1/youtube/video/subtitles` | GET | Get a YouTube video's subtitle files | 1 | standard | none |
| `/v1/youtube/video/thumbnails` | GET | Get a YouTube video's thumbnail files | 1 | standard | none |
| `/v1/youtube/video/transcript` | GET | Get YouTube video transcript | 3 | custom | 2592000s |
| `/v1/youtube/videos` | POST | Batch get YouTube video details (up to 1000) | 5-100 (metered) | advanced | none |
| `/v1/youtube/videos/trending` | GET | Get trending YouTube videos | 1 | standard | 120s |
