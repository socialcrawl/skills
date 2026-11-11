# SocialCrawl Pricing Reference

Complete per-endpoint credit pricing for all 733 active endpoints across 75 platforms. Auto-derived from the live endpoint registry - the same registry the router uses to charge your balance.

## How billing works

- Every billable API call deducts credits from your balance **before** the upstream call, atomically. The response reports the net charge in `credits_used` and `X-Credits-Used`.
- On billed responses, `credits_remaining` and `X-Credits-Remaining` are authoritative. Free cache hits return `credits_remaining: null` and omit the header because they do not establish an authoritative post-request balance. Idempotent replays return the current balance when their lookup succeeds; otherwise they return `credits_remaining: null` and omit the header. Routes that explicitly model an unavailable balance, including endpoint-parameter validation and best-effort metadata, omit both fields when their balance read fails.
- **Cache hits are free** - a response served from cache costs 0 credits (`X-Cache: HIT`, `cached: true`). Each endpoint's TTL is in the tables below; a repeat call inside the TTL window is free.
- **Automatic refunds** - credits are refunded on upstream errors (502), circuit-breaker rejections (503), internal errors (500), request-deadline timeouts (504), and empty-upstream results (404 `RESOURCE_NOT_FOUND` / an empty `items` list). You only pay for calls that return real data.
- **Free before billing** - invalid params, bad handle/URL formats, and rate-limit rejections (429) are rejected at the boundary and never deduct.
- **Idempotent replays are free** - resending with the same `Idempotency-Key` returns the stored response at 0 credits.
- **Metered endpoints** deduct an upfront ceiling and auto-refund down to the actual work done; the response `credits_used` is the real charge. Every metered endpoint is listed with its full pricing rule under [Metered and custom-priced endpoints](#metered-and-custom-priced-endpoints).
- **Multi-source endpoints charge once** no matter how many upstream providers are tried before one succeeds.
- `GET /v1/credits/balance`, `GET /v1/credits/transactions`, `GET /v1/credits/usage` (credits and requests by API key, UTC day and endpoint, up to 92 days), `GET /v1/keys/current` (the calling key's credit limit, used, remaining and `spendable`), `GET /v1/notifications` (what needs the account's attention, each item with a `next_step`) and `POST /v1/notifications/read` are always 0 credits (the balance also returns `runway.days_left`, `recommended_pack` and `checkout_url`, so when `days_left` is under 3, show the owner `checkout_url`), as is every `/v1/utility/*` endpoint except `utility/ai-detection` (1 credit a text).
- A key with a credit limit gets `X-Key-Credits-Remaining` on every response: what it may still spend after that call. Stop or switch keys before it reaches 0; a key past its limit gets a 402 that names the limit.
- **A band is a range, not a quote.** A band that starts at 0 can settle at 0: the mention and hashtag searches, `tiktokshop/sales`, `search/multi` and `prism/comment-leads` bill each page only when it returns rows (`prism/mentions` refunds a page with no verified row). The top of a wide band is a cap, not the expected charge: `prism/discover` never spends past its `max_credits` (required on POST, default 50 on GET), `prism/profiles` reaches its ceiling only with the widest `include: "comments"` options, and `trustpilot/reviews/history` holds `depth + 5`.

## Credit tiers

Most endpoints sit on a simple 1 / 5 / 10 ladder. A set of bundle and fan-out endpoints use a **custom** override that bypasses the ladder, flat or metered per recipe. Those run far past the ladder at the top end, so read the endpoint's own rule rather than assuming a ceiling.

| Tier | Cost per call | Endpoints | Typical endpoints |
|------|--------------|-----------|-------------------|
| standard | 1 credit | 267 | Profiles, posts, comments, search, reference data |
| advanced | 5 credits | 182 | Ad libraries, trending, audience analytics, app/product/business/place reviews, retail catalogs, LinkedIn social graph + jobs |
| premium | 10 credits | 25 | Video transcripts, LinkedIn people/job search + reactions, app-listings search |
| **custom (flat/metered)** | **varies (0-126,375)** | 259 | Prism composites, `{platform}/profile/full`, `search/everywhere` (20), `search/forums` (10), `search/news` (2-62 metered), `naver/brief` (10), the free `/v1/utility/*` endpoints (`utility/ai-detection` is a standard 1 credit), web scrape/crawl/agent/sessions; `prism/discover` and `prism/creators` are capped by the caller's `max_credits` |

Two groupings, both totalling 733: the table above counts endpoints **by pricing rule** (a custom override is its own row); counted instead **by base tier** (custom endpoints folded back into the ladder tier they sit on) the split is **418 standard · 269 advanced · 46 premium = 733**. Exact per-endpoint costs are in the tables below.

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
2. **A paginated pull** - the price is per PAGE, not per item. `pages = ceil(items_wanted / page_size)`, and the cost is `pages x per-call credits`. Each endpoint's page-size param and its maximum are on its `**Pagination**` line in the platform reference. Once page 1 is back, re-quote from the response: `pagination.next_page_credits` is what the next page costs (`null` when there is none) and `pagination.typical_page_size` is how many rows a full page holds.
3. **A repeat pull inside the cache TTL** - free. Re-reading the same profile twice in a minute bills once.
4. **A metered endpoint** - use the ceiling from the range for the quote, then report the real `credits_used` afterwards. It is usually well under the ceiling.
5. **A composite** - a Prism recipe is ONE charge that already covers every leg it fans out to. Running the legs yourself is almost always more expensive, and slower.

Worked example - 1,000 TikTok comments on one video: `prism/comments` is metered at 1 credit per comment page scanned and holds a ceiling inside its 2-200 credits band, settling down to the pages actually scanned, in a single call (`/v1/prism/comments`), versus paginating `tiktok/post/comments` yourself at 1 credit per page plus your own cursor loop. Quote the held ceiling, then report the real `credits_used`.

When a pull would cost more than a user's likely balance, say so and offer the cheaper shape (a smaller `limit`, a web-only `include`, a composite instead of a fan-out) rather than starting it.

## Free endpoints (0 credits)

29 endpoints never bill, plus `GET /v1/credits/balance`, `GET /v1/credits/transactions`, `GET /v1/credits/usage`, `GET /v1/keys/current`, `GET /v1/notifications` and `POST /v1/notifications/read`. Use them freely to discover the surface, resolve a URL, check spend, or manage async jobs.

| Endpoint | What it returns |
|----------|-----------------|
| `POST /v1/prism/discover/inputs` | Store a long author list or exclude list once and reuse it by id. |
| `GET /v1/prism/jobs` | List the API key's background jobs, newest first. |
| `GET /v1/prism/jobs/{job_id}` | Status and results of one background job. |
| `GET /v1/prism/lookup` | Universal post/product URL dispatcher: any post, video, product or repo link → the right detail endpoint's unified response. |
| `GET /v1/utility/capabilities` | List the parameters that work across endpoints |
| `GET /v1/utility/docs-search` | Search the docs |
| `GET /v1/utility/endpoint` | How to use any endpoint |
| `GET /v1/utility/endpoints` | List every available endpoint |
| `GET /v1/utility/estimate` | Quote the credit cost of a call or a plan |
| `GET /v1/utility/explain-error` | Explain a failed API response |
| `GET /v1/utility/find` | Find the endpoint for a task |
| `GET /v1/utility/llms` | AI-agent context payload |
| `GET /v1/utility/plan` | Plan the calls for a job |
| `GET /v1/utility/quickstart` | Get started in one call |
| `GET /v1/utility/recipes` | List task recipes with their cost |
| `GET /v1/utility/resolve` | Identify a URL, handle or id |
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

193 endpoints do not charge a flat ladder price. Each one holds an upfront ceiling and refunds the unused portion, so the response `credits_used` is always the real charge. Quote the RANGE to a user before calling, then report the actual charge afterwards.

| Endpoint | Range | How it is charged |
|----------|-------|-------------------|
| `GET /v1/airbnb/listing/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/aliexpress/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/amazon/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/app_store/app-reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/booking/hotel/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/douyin/comment/replies` | 5-250 credits | 5 credits per reply RETURNED. The call holds `limit x 5` up front - the default limit of 10 holds 50 and the 50 maximum holds 250 - and settles down to the replies actually delivered. Only a comment with a non-zero `engagement.replies` has a thread, so check that on the parent row before spending a call here With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/douyin/post/comments` | 2-100 credits | 1 credit per comment RETURNED, with a floor of 2. The call holds `limit x 1` up front - the default limit of 20 holds 20 and the 100 maximum holds 100 - and settles down to the comments actually delivered, so a video with four comments does not cost a twenty-comment request |
| `GET /v1/douyin/profile/posts` | 5-125 credits | 5 credits per row RETURNED. The call holds `limit x 5` up front - the default limit of 10 holds 50 and the 25 maximum holds 125 - and settles down to the videos actually delivered, so a creator with 4 recent videos costs 20 credits however high `limit` was set. `recent_days` and `exclude_pinned` narrow the result set BEFORE billing settles, so they lower the charge as well as the noise |
| `GET /v1/douyin/search` | 5-125 credits | 5 credits per row RETURNED. The call holds `limit x 5` up front - the default limit of 10 holds 50 and the 25 maximum holds 125 - and settles down to the rows actually delivered, so a narrow query that returns 3 videos costs 15 credits however high `limit` was set |
| `GET /v1/douyin/search/users` | 5-125 credits | 5 credits per creator RETURNED. The call holds `limit x 5` up front - the default limit of 10 holds 50 and the 25 maximum holds 125 - and settles down to the creators actually delivered With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/economy/imports` | 20 credits | 20 credits per call, whatever the limit. A company with no US import records returns 404 and costs 0 credits, and a cached repeat within 24 hours costs 0 credits. |
| `GET /v1/facebook/adlibrary/company/ads` | 5-35 credits | 5 credits for the page. include=audience holds 1 credit per ad (30 a page) and keeps only the rows filled from a fresh lookup, so a page is at most 35 credits; rows served from cache are free, ads that never ran in the EU and other unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/events` | 1-13 credits | 1 credit for the page. include=details holds 1 credit per event (at most 12 a page) and keeps only the rows filled from a fresh lookup, so a page is at most 13 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/post` | 1-2 credits | 1 credit for the post. include=group holds 1 more and keeps it only when the group's name comes back, so a call with include=group is at most 2 credits; it is refunded when the post is not in a group, when the lookup fails, and when the group was looked up recently and is served from cache. |
| `GET /v1/facebook/post/comment/replies` | 1-5 credits | 1 credit per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/post/comments` | 1-5 credits | 1 credit per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/profile` | 1 credit | 1 credit per call. A call that fails, or a handle that does not exist, costs nothing. |
| `GET /v1/facebook/profile/events` | 1-9 credits | 1 credit for the page. include=details holds 1 credit per event (8 a page) and keeps only the rows filled from a fresh lookup, so a page is at most 9 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/profile/photos` | 1-9 credits | 1 credit for the page. include=details holds 1 credit per photo (8 a page) and keeps only the rows filled from a fresh lookup, so a page is at most 9 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/profile/posts` | 1-4 credits | 1 credit for the page. include=engagement holds 1 credit per row (3 rows a page) and keeps only the rows filled from a fresh lookup, so a page is at most 4 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/profile/reels/full` | 5-25 credits | 5 credits per page of 10 reels - 1 for the list and 4 for the per-reel enrichment - which is roughly half what running the list-then-post-stats chain yourself costs. With no `limit` that is one page and a flat 5 credits. With `limit` set the endpoint walks `ceil(limit / 10)` pages, up to 5 for the 50 maximum (25 credits), holds that many up front and refunds every page it did not need. A page whose enrichment yields zero coverage refunds the 4-credit premium automatically, leaving the 1-credit list price |
| `GET /v1/facebook/search/groups` | 1-15 credits | 1 credit for the page. include=details holds 1 credit per group (at most 10 a page) and keeps only the groups filled from a fresh lookup, so a page is at most 11 credits; groups served from cache are free, unfilled groups are refunded, and a repeat of the same call within the cache window costs 0. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/search/hashtag` | 0-9 credits | Metered, 0-9 credits: each call reads one page of /v1/facebook/search/videos (1 credit; with `since` or `until`, up to 8, since each video is looked up for its publish date at 1 credit, and a video still undated is left out) and /v1/facebook/search/posts (1 credit), each billed at that endpoint's own price exactly as a direct call is. A page that found nothing or failed costs nothing, and a page served from cache is free. A page is billed when it returned rows, even if none of them carried the hashtag; data.legs shows each page's charge and data.excluded what was left out. |
| `GET /v1/facebook/search/mentions` | 0-1 credits | Metered, 0-1 credits: each call reads one page of /v1/facebook/search/posts (1 credit), each billed at that endpoint's own price exactly as a direct call is. A page that found nothing or failed costs nothing, and a page served from cache is free. A page is billed when it returned rows, even if none of them carried the mention; data.legs shows each page's charge and data.excluded what was left out. |
| `GET /v1/facebook/search/pages` | 1-11 credits | 1 credit for the page. include=details holds 1 credit per page (at most 10) and keeps only the rows filled from a fresh lookup, so a page is at most 11 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/facebook/search/posts` | 1-9 credits | 1 credit per page. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/facebook/search/videos` | 1-8 credits | 1 credit for the page. include=details holds 1 credit per video (7 a page) and keeps only the rows filled from a fresh lookup, so a page is at most 8 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/g2/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/goodreads/book/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/google_play/app-reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/google_shopping/reviews` | 1-5 credits | 1 credit per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/google/business/extended-reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/hackernews/search` | 1-9 credits | 1 credit per page. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/home_depot/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/instagram/comment` | 5-15 credits | 5 credits for a standard lookup, 15 with `deep_scan=true`, which keeps paging the thread when the comment is not in the first pages. Reach for deep_scan only after a standard lookup comes back not-found |
| `GET /v1/instagram/followers` | 5-10 credits | 5 credits a page. Up to three reads are merged into one page, typically about 50 accounts, and a page can carry fewer. With `coverage=full`, up to 10 credits a page, settled down to 5 when the plain walk covered the whole page. A page that fails is refunded. With `query`, 5 credits for its one window, and nothing when no account matches. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/following` | 5-10 credits | 5 credits a page. Up to three reads are merged into one page, typically about 50 accounts, and a page can carry fewer. With `coverage=full`, up to 10 credits a page, settled down to 5 when the plain walk covered the whole page. A page that fails is refunded. With `query`, 5 credits for its one window, and nothing when no account matches. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/location/posts` | 5-68 credits | 5 credits per page. `include=country` holds 63 more credits a page and keeps 1 per creator whose declared country came back, refunding a creator who publishes none or cannot be found, so a page with it costs 5 to 68. A page that fails is refunded in full and looks no creator up. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/media/screen-text` | 5-10 credits | 5 credits a call, the same for a photo, a reel's cover or a carousel page of 10 slides. 10 credits with `frames=all` on a reel; when the post has no video to read, or the video cannot be read and the cover is read instead, the call costs 5 and the response says so in `warnings`. Refunded when the post cannot be found, when nothing on it could be read, or when a parameter does not fit the post (a `slide_offset` past the last slide, a reel over 180 seconds with `frames=all`). |
| `GET /v1/instagram/post/comment/replies` | 1-5 credits | 1 credit per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/post/comments` | 5-19 credits | 5 credits per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/post/stats` | 5-9 credits | 5 credits for the post. include=saves holds 4 more and keeps them only when it fills a save count the plain call lacked, refunding them otherwise, so a hydrated call is at most 9 credits; on a reel whose save count the plain call already carries, and on any photo or carousel, it settles at 5. Post lookups are cached for 10 minutes. |
| `GET /v1/instagram/profile` | 1 credit | 1 credit per call. A call that fails, or a handle that does not exist, costs nothing. |
| `GET /v1/instagram/profile/about` | 1 credit | 1 credit per call, with or without `include=verified_at`. A call that fails, a handle that does not exist and a refused parameter cost nothing. |
| `GET /v1/instagram/profile/country` | 1 credit | 1 credit per call. A refused username or a missing `user_id` costs nothing. |
| `GET /v1/instagram/profile/posts` | 1-29 credits | 1 credit per page. include=audio holds 1 more per row, up to 12, and keeps it only for each video whose sound came back, refunding the rest, so a page costs at most 13 credits and a page with no videos costs 1. include=tags holds 1 more per row, up to 12, and keeps it only for each post whose tagged accounts came back, refunding the rest; with both tokens a page costs at most 25 credits. exclude_pinned and recent_days do not change the price of a page. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/profile/posts/full` | 5-25 credits | 5 credits per upstream page of about 12 posts. With no `limit` that is one page and a flat 5 credits. With `limit` set the composite walks `ceil(limit / 12)` pages - 3 for limit=30, 5 for the 50 maximum, so 25 credits at the top - holds that many up front and refunds every page it did not need. One partial refund sits inside the per-page price: a shares leg that fails outright refunds 4 of the 5 credits for that page, leaving the 1-credit list price. A shares leg that succeeds with low coverage is still the full 5, because the second source was queried either way. A `user_id` call is priced exactly like a `handle` call |
| `GET /v1/instagram/profile/reels` | 1-18 credits | 1 credit per page. include=stats adds 1 credit a page. include=audio holds 1 more per row, up to 12, and keeps it only for each video whose sound came back, refunding the rest; with include=stats every reel already carries its sound, so the audio join costs nothing more. A page costs at most 14 credits. exclude_pinned and recent_days do not change the price of a page. sort=most_viewed costs the same 1 credit a page. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/profile/reels/full` | 5-25 credits | 5 credits per upstream page of about 12 reels. With no `limit` that is one page and a flat 5 credits. With `limit` set the composite walks `ceil(limit / 12)` pages - 3 for limit=30, 5 for the 50 maximum, so 25 credits at the top - holds that many up front and refunds every page it did not need. One partial refund sits inside the per-page price: a shares leg that fails outright refunds 4 of the 5 credits for that page, leaving the 1-credit list price. A shares leg that succeeds with low coverage is still the full 5, because the second source was queried either way. A `user_id` call is priced exactly like a `handle` call |
| `GET /v1/instagram/search/hashtag` | 1-31 credits | 1 credit per page, on every `type`. `max_items` and `max_pages` walk more pages in one call at 1 credit each, and `max_credits` caps the total. A page Instagram returns empty is not charged. `include=country` holds 30 more credits a page and keeps 1 per creator whose declared country came back, refunding a creator who publishes none or cannot be found, so a page with it costs 1 to 31. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/instagram/search/mentions` | 0-6 credits | Metered, 0-6 credits: each call reads one page of /v1/instagram/tagged (5 credits) and /v1/instagram/search/reels (1 credit), each billed at that endpoint's own price exactly as a direct call is. A page that found nothing or failed costs nothing, and a page served from cache is free. A page is billed when it returned rows, even if none of them carried the mention; data.legs shows each page's charge and data.excluded what was left out. |
| `GET /v1/instagram/search/popular` | 1-13 credits | 1 credit for the page. include=engagement holds 1 credit per row, at most 12 (or `limit`), and keeps only the rows filled from a fresh lookup, so a full page is at most 13 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. Search pages are cached for 2 minutes and the per-post lookups for 10 minutes. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/search/profiles` | 1-25 credits | 1 credit for the search page. With `include=about`, 1 plus 2 credits per row filled, held at the top 8 (17) unless you send `limit`, refunded down to the rows that actually received an About-panel leaf. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/instagram/search/reels` | 1-69 credits | 1 credit per page on a plain call or with `region`; `include=creator` or `country` makes it up to 61 (1 plus 2 per creator looked up). `region` costs nothing extra. `include=country` makes it up to 31: 1 extra credit per creator whose declared country came back, refunded for a creator who publishes none or cannot be found. `include=creator` adds 2 credits per creator looked up: it holds 60 extra credits for a full page of 30 and refunds every creator it did not look up or could not find. Two reels by one creator are one lookup, a creator looked up in the last 15 minutes is free, and on a `max_pages` walk each creator is looked up and billed once. `country` runs the same creator lookup, because it needs each creator's declared country, at the same price, charged for every creator looked up, kept or not; `data.hydration.implied_by` says so on the response. `include=creator,country` is priced as `include=creator` alone, because the creator card already carries the country. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/instagram/similar` | 5-85 credits | 5 credits for the list. include=profile holds 1 credit per row and keeps only the rows filled from a fresh lookup; the hydrated list is its top 20 accounts by default (at most 25 credits) and `limit=80` buys the full roster (at most 85). Rows served from cache are free, unfilled rows are refunded, and a repeat within the cache window costs 0. The list and the per-account lookups are cached for 15 minutes. |
| `GET /v1/klarna/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/klarna/reviews/pro` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/kohls/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/linkedin/company` | 5-8 credits | 5 credits for the company page. include=about holds 3 more and keeps them only when it fills the company type or tagline the plain call lacked, refunding them otherwise, so a call with include=about is at most 8 credits; when the plain answer already carries the company type, no lookup runs and it settles at 5. Company lookups are cached. |
| `GET /v1/linkedin/company/bulk` | 5-125 credits | 5 credits for each company returned, the same rate as /v1/linkedin/company. The call holds 5 credits for each distinct company you send and refunds the ones that are not found; a call where every company has no page is a 404 at no charge, and one where none could be fetched just now is a 503 at no charge. |
| `GET /v1/linkedin/company/people` | 10-50 credits | 10 credits for the list. include=profile holds 4 credits per row and keeps only the rows filled from a fresh lookup: at most 50 for the 10-row page, or 10 + 4 x limit when you pass `limit`. Rows served from cache are free, unfilled rows are refunded, and a repeat of a fully joined page within the list's cache window costs 0. The list is cached for 15 minutes and each profile lookup for 15 minutes. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/linkedin/post/reactions` | 10-50 credits | 10 credits for the list. include=profile holds 4 credits per row and keeps only the rows filled from a fresh lookup: at most 50 for the 10-row page, or 10 + 4 x limit when you pass `limit`. Rows served from cache are free, unfilled rows are refunded, and a repeat of a fully joined page within the list's cache window costs 0. The list is cached for 5 minutes and each profile lookup for 15 minutes. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/linkedin/profile/all` | 5-50 credits | 5 credits for one profile with `url`. With `urls`, 5 credits per profile returned, from 5 for one profile up to 50 for the 10-profile maximum. Duplicate URLs are collapsed before the call and profiles that do not resolve are not charged, so a list with repeats or dead handles costs less than its length. A list where nothing resolves is a free 404. |
| `GET /v1/linkedin/profile/posts` | 5-200 credits | 5 credits for a call with no `limit`, or `limit` at 50 or below. Above 50 the call is metered at 2 credits per post RETURNED: it holds `limit x 2` up front (the 100 maximum holds 200) and refunds down to the posts that actually came back, never below 5, so a member with 60 posts settles at 120 credits however high `limit` was set |
| `GET /v1/linkedin/profile/posts/archive` | 5-500 credits | 5 credits per post RETURNED. The call holds `limit x 5` up front - the default limit of 20 holds 100 and the 100 maximum holds 500 - and refunds down to the posts that actually came back, so a member with 12 posts settles at 60 credits however high `limit` was set. This is the most expensive read on the platform per row: check whether /v1/linkedin/profile/posts (5 credits up to 50 posts, 2 a post above that) already covers the window you need before walking the archive With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/linkedin/search/people` | 10-50 credits | 10 credits for the list. include=profile holds 4 credits per row and keeps only the rows filled from a fresh lookup: at most 50 for the 10-row page, or 10 + 4 x limit when you pass `limit`. Rows served from cache are free, unfilled rows are refunded, and a repeat of a fully joined page within the list's cache window costs 0. The list is cached for 2 minutes and each profile lookup for 15 minutes. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/linkedin/search/posts` | 1-56 credits | 5 credits per page. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 8 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 8 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/naver/blog/search` | 1-9 credits | 1 credit per page. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/naver/cafearticle/search` | 1-9 credits | 1 credit per page. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/naver/news/search` | 1-9 credits | 1 credit per page. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/naver/place/rank` | 4-42 credits | 4 credits per keyword, plus 2 credits when lat and lng are left out (the point is read from the place). The whole amount is refunded when the check fails. |
| `GET /v1/naver/place/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/pinterest/board` | 1-16 credits | 1 credit for the page. include=engagement holds 1 credit per row, at most 15 (or `limit`), and keeps only the rows filled from a fresh lookup, so a page is at most 16 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/pinterest/search` | 1-34 credits | 1 credit for the page. include=engagement holds 1 credit per row, at most 25 (or `limit`), and keeps only the rows filled from a fresh lookup, so a page is at most 26 credits; rows served from cache are free, unfilled rows are refunded, and a repeat of the same call within the cache window costs 0. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/prism/adverse-screen` | 25-75 credits | 25 credits for one profile, plus 10 for each further profile (4 profiles cost 55). Profiles that could not be screened are refunded their share, and a call that screened nothing keeps 5 |
| `GET /v1/prism/ai-visibility` | 2-1,605 credits | 2 credits per probe, where a probe is one prompt run once on one engine, so the charge is `2 x prompts x runs x engines`. On the defaults (both engines, 8 runs) a 5-prompt audit is 160 credits. `include=web_baseline` adds a flat 5. The 1,605 ceiling is the 20-prompt, 20-run, two-engine worst case with the baseline on - `preset=quick` holds far less, and the hold settles down to the probes that actually completed |
| `GET /v1/prism/app-reviews` | 10-15 credits | 10 credits for one store, 15 for both. A bare `query` resolves both stores and costs 15; naming a single store in `stores`, or passing only one of `google_play_id` / `app_store_id`, costs 10 |
| `GET /v1/prism/audience-language` | 2-26 credits | Floor 2 credits (one YouTube post: the channel list plus one comment page). Each further comment page is 1 credit, or 5 on Instagram, up to 5 posts. TikTok also opens the audience sample (5) and one follower page (1). Unopened pages are refunded. Five Instagram posts is 26 credits. |
| `GET /v1/prism/brief-check` | 15 credits | 15 credits per post (provisional). Caption and transcript are pulled; each talking point is scored and quoted. A missing transcript is reported, never treated as a pass. |
| `GET /v1/prism/comment-leads` | 0-243 credits | Pay for what is opened: 1 credit a search page, 1 credit a comment page fetched and 1 credit for every started 25 comments labelled. The default request holds 37 and refunds what did not run; judging which posts to open is free |
| `POST /v1/prism/comment-lookup` | 2-100 credits | 2 credits per found TikTok item and 5 per found Instagram item, raised by `deep_scan`. Up to 25 items per call: the whole batch holds at most 100 credits up front and refunds every not_found, errored and deferred item |
| `GET /v1/prism/comments` | 2-200 credits | 1 credit per comment page scanned (5 on LinkedIn) plus 1 per replies call that returned replies. An Instagram post URL is a flat 5 credits whatever `max` you pass, plus 1 per replies call only when you send `replies=true` |
| `GET /v1/prism/creator-card` | 5-8 credits | 5 credits covering any 4 platforms, plus 1 credit per platform beyond 4. The default selection is 4 platforms, so the 7-platform maximum is 8 credits |
| `GET /v1/prism/creator-vet` | 50-75 credits | 50 credits for the standard vet. `include=cross_platform` raises it to 75 for the cross-platform identity check on top |
| `GET /v1/prism/creators` | pay per search and lookup, capped by max_credits (default 200) | Each platform search is billed at that platform's own search price, only when it returns rows; a search that fails, finds nothing or is served from cache costs 0. A creator's profile lookup costs 1 credit (LinkedIn 5), a posts walk the post page's price, and judging 1 credit per started 5 creators per pass. Compiling a prompt, the metrics, the score, the filters and paging are free. max_credits (default 200 on this call) caps the whole run, and a request expected to cost more is refused free before anything is spent. |
| `POST /v1/prism/creators` | pay per search and lookup, capped by the required max_credits | Nothing is held when the run starts. Each platform search is billed at that platform's own search price when it runs, only when it returns rows; a profile lookup costs 1 credit (LinkedIn 5), a posts walk the post page's price, and judging 1 credit per started 5 creators per pass. max_credits is required and caps the whole run: the run pauses at it and never overspends. Reading the run is free. |
| `GET /v1/prism/crisis-radar` | 15-45 credits | 15 credits for the baseline breach check. `confirm=true` escalates to the full 45-credit investigation. Run the baseline first and escalate only when it reports a breach: that is the whole point of the two-step shape |
| `GET /v1/prism/discover` | pay per search, capped by max_credits (default 50) | Each platform search is billed at that platform's own search price, only when it returns rows; a search that fails, finds nothing or is served from cache costs 0. Judging against your keywords is free; judging against a different context costs 1 credit per started 15 rows, and each label costs 1 credit per started 25 rows. max_credits (default 50 on this call) caps the whole run, judging, joins and page bodies included, and a request expected to cost more is refused free before anything is spent. A search still running when the call answers bills when it finishes, after the answer: credits_used leaves it out and data.run.credits.pending shows the most it can add. |
| `POST /v1/prism/discover` | pay per search, capped by the required max_credits | Nothing is held when the run starts. Each platform search is billed at that platform's own search price when it runs, only when it returns rows, and judging against a context costs 1 credit per started 15 rows and each label costs 1 credit per started 25 rows. max_credits is required and caps the whole run: the run pauses at it and never overspends. Reading the run is free. |
| `GET /v1/prism/earliness` | 25 credits | 25 credits (provisional). One date-sorted page per platform, Google Trends over five years, and one page of the TikTok and Meta ad libraries. An endpoint that does not answer is listed and is not a first-seen date. |
| `GET /v1/prism/find-accounts` | 2-29 credits | The searches at their own prices (1 credit each for Instagram, TikTok and X, 10 for LinkedIn) plus 1 credit per platform judged: 6 credits for a person by default, 17 for a company (LinkedIn included). Threads or YouTube, when named, is 1 credit for its search plus 1 for its judging. With profile_check=true each profile lookup is added at its own price (1 credit on Instagram, TikTok and Threads, 5 for a company page on LinkedIn). For a company with `website`, a LinkedIn search that fails is answered by `linkedin/company/by-domain` at its 5 credits instead of the search's 10, and nothing when it fails too. A search that fails, a platform that could not be judged and a lookup that was not made or failed are refunded |
| `GET /v1/prism/format-lift` | 4 credits | 4 credits (provisional). One page of the creator's recent posts is read, and each post is compared with that creator's own median. A bucket with fewer than eight posts lists the count and leaves the median empty. |
| `GET /v1/prism/handle-audit` | 5-8 credits | 5 credits for any selection of up to 4 supported platforms; +1 credit per selected platform beyond 4 |
| `GET /v1/prism/investigate` | 1 credit | Holds `budget` credits (default 40, max 200) up front and refunds what the walk does not spend. Each underlying page is charged at its own price. Deciding the next step is free. |
| `POST /v1/prism/jobs` | per row, at the batch endpoint's own price | The same price per row as the batch endpoint the job runs: prism/profiles (1 credit per profile on most platforms, 5 on LinkedIn, plus its posts pages and comment pages as on prism/profiles) or prism/post-stats (its per-URL price). The call holds the whole job's worst case up front, answered in credits_used on the 202, and refunds every row that is not ok when the job completes. A job of a GET endpoint holds nothing (credits_used 0 on the 202, `billing: per_call`): each item is billed as that GET when it runs, a cached, failed or not-found item costs what the GET would, and `credits_max` on the 202 is the most the job can cost. Reading the job is free. |
| `GET /v1/prism/korea-gap` | 15-40 credits | 15 credits for the web-only read. The default `include` carries the social leg, which makes the call 40; pass an `include` without `social` to stay at 15 |
| `GET /v1/prism/mentions` | 1-9 credits | 1 credit for each X or Reddit page, 5 for an Instagram tag page, 1 for a web page. A default call holds 3. A page with no verified row is refunded. Facebook, Threads and TikTok are not searched. |
| `GET /v1/prism/org-radar` | 6-51 credits | 1 credit for the org read plus 5 per repository expanded into a dossier. The default of 5 repos is 26 credits, a single repo is 6, and the 10-repo maximum is 51. Set `repos` to bound it before calling |
| `POST /v1/prism/post-comments` | 1-2,500 credits | Each post costs what its own comment endpoint charges per page (1 credit on TikTok, YouTube, Facebook, X and Threads; 5 on Instagram, LinkedIn and Reddit), for the pages that came back with comments. The call holds every post at the pages per_post can take and refunds the rest; unsupported, not found, failed and deferred posts cost nothing. With since, a post with no new comment costs nothing |
| `POST /v1/prism/post-stats` | 1-500 credits | 1 credit per successful URL on most platforms, 2 on Instagram and 5 on LinkedIn, charged at each URL's own platform rate. Up to 100 URLs per call: the call holds the summed worst case up front (a 100-URL Instagram batch holds 200) and refunds every dead, errored and unsupported URL, so you pay for exactly the rows that returned counts |
| `GET /v1/prism/profile/comments` | 2-2,428 credits | each page actually read, at that endpoint's own price: the post list page (1 credit) plus the comment pages of each post that returned a new comment (5 credits a page on Instagram, 1 on Facebook, YouTube, TikTok and X). A post whose comments are all older than `since` costs nothing, so a call that finds no new comment costs only the post list page. With `replies=true`, plus 1 credit per replies call that returned replies. The call holds the most that `posts` and `per_post` can take (251 credits for Instagram's defaults, plus up to 100 replies pages, 300 on Instagram, with `replies=true`) and refunds the rest |
| `POST /v1/prism/profiles` | 1-126,375 credits | 1 credit per successful row on most platforms and 5 on LinkedIn, charged at each handle's own platform tier. Up to 50 items per call: the call holds the summed worst case up front and refunds every not_found, unsupported, errored and deferred row. With include: "posts" (up to 25 items) a row also costs its post list page, 1 credit (5 on LinkedIn), charged only when that page came back with posts. With posts_limit the call walks the list and charges each page that came back with posts; it holds the most pages the limit can take (10 at most per handle) and refunds the unused ones, and a dry run shows that hold. With include: "comments" each selected post's comments cost what that platform's comment endpoint charges per page (1 credit on most platforms, 5 on Instagram, LinkedIn and Reddit), charged only for pages that came back with comments; the call holds comments_top_posts times the pages comments_per_post can take and refunds the rest |
| `GET /v1/prism/share-of-voice` | 20-200 credits | 40 credits per brand with the social leg, which is the default, or 20 per brand for the web-only read. Up to 5 brands per call, so the 200-credit ceiling is 5 brands with social and dropping `social` from `include` halves it. Price the call as `brands x per-brand` before you send it - this is the most expensive composite on the API |
| `GET /v1/prism/trend-board` | 30 credits | 30 credits flat (provisional). One call reads TikTok's local feed, TikTok's hashtag board, Google Trending Now, up to 5 author pages and up to 3 sounds. A source that does not answer is listed under unavailable and its section is empty. Only a call where the feed, the hashtag board and Google Trending Now all fail is refunded. |
| `GET /v1/prism/video-intel` | 5-15 credits | 5 credits for the video detail, stats and comments. `include=transcript` adds 10, which is exactly what the standalone transcript endpoint charges, so the bundle never costs more than running the two calls yourself |
| `GET /v1/reddit/omni-search` | 5-9 credits | 1 credit for the search page plus 1 per thread SUCCESSFULLY expanded, with a floor of 5. The call holds `1 + threads` up front (the 8-thread maximum holds 9) and refunds every thread that failed to expand, so the floor is what most sweeps cost. Running the same sweep by hand - one reddit/search plus eight reddit/post/comments calls - costs the same 9 at best and gives you no subreddit rollup |
| `GET /v1/reddit/post/comments` | 5-9 credits | 5 credits per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/reddit/profile/comments` | 2-200 credits | 2 credits per comment returned. A limit of 25 holds 50 credits and settles down to the number of comments that actually came back; an account with no comments costs nothing. |
| `GET /v1/reddit/search` | 1-48 credits | 1 credit for the search page. include_body=true reserves up to 25 extra credits and refunds every one it does not spend. Rows now arrive with their bodies, and a link post has no body to fetch, so a row is only charged for when a body actually comes back: on most pages nothing is spent and the page costs 1 credit. With limit above 25: 1 credit per 25 posts returned, never less than 1. The call holds limit / 25 credits (rounded up, at most 40) and refunds the rest once the posts are counted; posts left out by since or until are not counted. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/reddit/subreddit` | 1-5 credits | 1 credit per page. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/reddit/subreddit/search` | 1-26 credits | 1 credit for the search page. With include_body=true, 1 extra credit per post that comes back with a body, up to 25 per page, unused credits refunded. Link posts have no body and are not charged for. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/reddit/subreddits/search` | 1-26 credits | 1 credit for the page. include=details holds 1 credit per row, at most 25 (or `limit`), and keeps only the rows filled from a fresh lookup, so a page is at most 26 credits; rows served from cache are free, unfilled rows are refunded, and a repeat within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/search/creators` | 10-24 credits | 10 credits flat, with a coverage-based partial refund. A search no source has a creator for answers 200 with an empty `creators` and `empty_reason: no_matches`, at 0 credits. Adding brief= adds 2 credits, refunded when the judging step could not answer for every judged creator. With country=, the searches and lookups it runs are billed on top, each at its own endpoint's price: 1 credit for the TikTok search page, 1 for the Google page and 1 per Instagram profile looked up (at most 10, and free for a profile looked up recently), so at most 12 more. data.legs lists each one with its credits, and the 10 are refunded when no creator is found. A cached page is free. |
| `POST /v1/search/everywhere` | 20 credits | 20 credits per search, each keyword of a group being its own search. Nothing is held when the run starts; each search reserves and bills its own 20 when it runs, and an answer with no row anywhere is free. max_credits is required, except with dry_run or a schedule, whose max_credits_per_run takes its place, and caps the whole run with its quoted extras. A watch fire costs what the same request costs, with no surcharge and no refund for finding nothing new. |
| `GET /v1/search/multi` | 0-30 credits | Metered, usually 1-14 credits: each platform is billed at its own endpoint's price, per platform, exactly as a direct call to that endpoint is billed (TikTok, Instagram, YouTube, Reddit, Threads, X and Facebook 1 credit a page, Telegram 2, LinkedIn 5). A platform whose page found nothing or failed costs nothing, and a platform page served from cache is free. A Threads phrase that Threads does not recognise is expanded into narrower searches, as on /v1/threads/search, and costs 1 credit per search that returned posts. With expand=context every platform runs your phrase plus expand_queries planned searches (3 by default, 3 at most), each billed as its own page, so the range above is multiplied by 1 plus expand_queries and the estimate quotes it that way. The searches inside a platform judge their rows for free; relevant_to= or label= is billed once on the request, for the rows of the merged page. data.sources.<platform>.credits shows each platform's charge and credits_used the total. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 8 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 8 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/search/news` | 2-62 credits | 2 credits + 1 credit per google leg that returns at least one article (upfront hold 2 + min(5 x countries, max_legs, 12), maximum 14 on the default engine). Adding the bing engine adds 1 credit per 5 articles it returns, because that engine is priced per article rather than per call; the absolute ceiling with both engines is 62. The hold always settles down to the actual charge, and empty, skipped or failed legs bill 0. |
| `GET /v1/sephora/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/target/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/telegram/search` | 2-16 credits | 2 credits for the page. include=details holds 1 credit per channel (at most 10 a page, fewer with limit) and keeps only the channels filled from a fresh lookup, so a page is at most 12 credits; channels served from cache are free, unfilled channels are refunded, and a search that finds no public channel costs 0. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/threads/post/comments` | 1-10 credits | 1 credit for the bundled window of about 20 replies, which is what a call with no `limit`, or `limit` at 25 or below, costs. Above 25 the deeper endpoint is metered at 1 credit per 5 replies RETURNED: the call holds `ceil(limit / 5)` up front (the 50 maximum holds 10) and refunds down to what came back, so a post with 12 replies settles at 3 credits however high `limit` was set |
| `GET /v1/threads/search` | 1-34 credits | 1 credit per result window. A call with no `limit` is one window and costs exactly 1. With `limit` set the walker consumes `ceil(limit / 15)` windows - 4 for limit=50, 7 for the 100 maximum - holds that many up front and refunds every window it did not need. Query relaxation can add up to 4 more windows on a page-1 request, billed only for the relaxed searches that returned posts and refunded for the ones that did not; send `expand=false` to hold none of them. When your balance, or the API key's limit, covers the call without them but not with them, it runs as `expand=false` instead of answering 402, and `data._warnings` says so. A request carrying a cursor never relaxes, so a pagination loop's last hop costs nothing extra. With `include=engagement` the call also holds 20 credits and keeps 1 for each of the first 20 posts whose view count or display name it filled from a fresh lookup; posts served from the post lookup's cache (10 minutes) are free, a post Threads has published no view count for is free (it still gets its pinned flag), and the rest is refunded Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/threads/search/users` | 1-13 credits | 1 credit for the identity window, which is what a call with no `include` costs. With `include=profile` the call holds 1 credit per row of the page (12, or `limit`) and keeps 1 for each account it filled from a fresh lookup; accounts served from the profile lookup's cache (15 minutes) are free and the rest is refunded, so a call costs 13 at most |
| `GET /v1/threads/user/posts` | 1-165 credits | 1 credit for the bundled window of about 15 posts, which is what a call with no `limit`, or `limit` at 15 or below, costs. Above 15 the deeper endpoint is metered at 3 credits per post RETURNED: the call holds `limit x 3` up front (the 50 maximum holds 150) and refunds down to what came back. With `include=engagement` the call also holds 1 credit per post of the window (15) and keeps 1 for each post whose view count or display name it filled from a fresh lookup; posts served from the post lookup's cache (10 minutes) are free and the rest is refunded, so the default window costs 16 at most. Beside a `limit` above 15 the deeper rows already carry both fields, so the 15 are refunded in full |
| `GET /v1/tiktok/adlibrary/search` | 5-17 credits | 5 credits for the page. include=ad holds 1 credit per ad, at most 12 (or `limit`), and keeps only the ads filled from a fresh lookup, so a page is at most 17 credits; ads served from cache are free, unfilled ads are refunded, and a repeat within the cache window costs 0. The page is cached for 2 minutes and the per-ad lookups for 30 minutes. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/ads/top` | 10-100 credits | 1 credit per ad returned, minimum 10 credits. A limit of 20 holds 20 credits and settles down to the number of ads that actually came back; a filter combination with no board costs nothing. With include=retention, 2 credits per ad that carries a retention curve (minimum 20), and 1 per ad TikTok serves no curve for. |
| `GET /v1/tiktok/collection/videos` | 1-21 credits | 1 credit per page; include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/comment` | 2-6 credits | 2 credits for a standard lookup, 6 with `deep_scan=true`, which keeps paging the thread when the comment is not in the first pages. Reach for deep_scan only after a standard lookup comes back not-found |
| `GET /v1/tiktok/effect/videos` | 1-21 credits | 1 credit per page; include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/hashtags/popular` | 6-96 credits | 2 credits per hashtag returned, minimum 6. One board is 6 credits. industry=all holds 96 credits (sixteen boards of three) and settles down to the hashtags actually returned, typically 88 to 92. An empty board costs nothing. |
| `GET /v1/tiktok/location/posts` | 1-21 credits | 1 credit per page; include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/playlist/videos` | 1-21 credits | 1 credit per page; include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/post` | 1-3 credits | 1 credit per call; include=exact_counts: +2, kept only when the exact counts come back. |
| `GET /v1/tiktok/post/comments` | 1-7 credits | 1 credit per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/profile` | 1-3 credits | 1 credit per call. `include=account` holds 2 more and keeps them only when the account's creation date or posting region comes back, so a call with it is at most 3 credits; a lookup that fails and an account looked up recently (served from cache) are refunded. A call that fails, or a handle that does not exist, costs nothing. |
| `GET /v1/tiktok/profile/videos` | 1-25 credits | 1 credit per page. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/search` | 1-62 credits | 1 credit for the page, including any limit of 30 or less. A limit above 30 holds ceil(N/4)+2 credits for the N rows the source fills (60 to 120, rounded up to a multiple of 30), 17 at 60 and 32 at 120, and unfilled slots are refunded. Repeated videos are removed after billing. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 5 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 5 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/tiktok/search/hashtag` | 1-25 credits | 1 credit per page. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/tiktok/search/mentions` | 0-2 credits | Metered, 0-2 credits: each call reads one page of /v1/tiktok/search (1 credit) and /v1/tiktok/search (1 credit), each billed at that endpoint's own price exactly as a direct call is. A page that found nothing or failed costs nothing, and a page served from cache is free. A page is billed when it returned rows, even if none of them carried the mention; data.legs shows each page's charge and data.excluded what was left out. |
| `GET /v1/tiktok/search/top` | 1-21 credits | 1 credit per page; include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/tiktok/search/users` | 1-100 credits | 1 credit for the page. include=profile holds 1 credit per row, at most 30 (or `limit`), and keeps only the rows filled from a fresh lookup, so a page is at most 31 credits; rows served from cache are free, unfilled rows are refunded, and a repeat within the cache window costs 0. country= holds 5 credits per requested in-country row (8 by default, at most 20) and keeps only the rows returned, so a miss is 0. The page is cached for 2 minutes and the per-account lookups for 15 minutes. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/similar` | 5 credits | 5 credits a call. An empty list is refunded, an unknown handle is a free 404, and the list is cached for 15 minutes, so a repeat within that window costs 0. |
| `GET /v1/tiktok/song/videos` | 1-21 credits | 1 credit per page; include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/trending` | 5-25 credits | 5 credits per page; include=exact_counts: +2 a row made exact (max 20). |
| `GET /v1/tiktok/user/liked` | 1-21 credits | 1 credit per page; include=exact_counts: +2 a row made exact (max 20). With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/video/comment/replies` | 1-5 credits | 1 credit per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktok/video/screen-text` | 5-10 credits | 5 credits a call, the same for a video's cover or a photo post page of 10 slides. 10 credits with `frames=all` on a video; when the post is a photo post, or the video cannot be read and the cover is read instead, the call costs 5 and the response says so in `warnings`. Refunded when the post cannot be found, when nothing on it could be read, or when a parameter does not fit the post (a `slide_offset` past the last slide or on a video, a video over 180 seconds with `frames=all`). |
| `GET /v1/tiktok/videos/popular` | 26-45 credits | 25 credits per board plus 1 credit per video returned. The default limit of 20 holds 45 credits and settles to the videos actually returned; an empty board costs nothing. |
| `GET /v1/tiktokshop/product` | 1-4 credits | 1 credit for the product. include=details holds 3 more and keeps them only when it fills a description the plain call lacked, refunding them otherwise, so a hydrated call is at most 4 credits; a SEA product, which carries its description already, settles at 1. Product lookups are cached. |
| `GET /v1/tiktokshop/product/reviews` | 1-5 credits | 1 credit per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/tiktokshop/sales` | 0-8 credits | Metered, 0-8 credits: each market is one /v1/tiktokshop/search page billed at that endpoint's own price (1 credit), exactly as a direct call is billed. A market whose page found nothing or failed costs nothing, and a page served from cache is free. data.regions[].credits shows each market's charge and credits_used the total. |
| `GET /v1/tripadvisor/attraction/reviews` | 1-5 credits | 1 credit per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/tripadvisor/cruise/reviews` | 1-5 credits | 1 credit per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/tripadvisor/restaurant/reviews` | 1-5 credits | 1 credit per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/tripadvisor/reviews` | 1-5 credits | 1 credit per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `GET /v1/trustpilot/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. |
| `POST /v1/trustpilot/reviews/history` | 6-10,005 credits | 1 credit per returned review, plus 5 credits to open. Submitting holds depth plus 5 credits and refunds the unused portion when the job settles. |
| `GET /v1/twitter/profile` | 1 credit | 1 credit per call. A call that fails, or a handle that does not exist, costs nothing. |
| `GET /v1/twitter/search/hashtag` | 0-1 credits | Metered, 0-1 credits: each call reads one page of /v1/twitter/search/tweets (1 credit), each billed at that endpoint's own price exactly as a direct call is. A page that found nothing or failed costs nothing, and a page served from cache is free. A page is billed when it returned rows, even if none of them carried the hashtag; data.legs shows each page's charge and data.excluded what was left out. |
| `GET /v1/twitter/search/mentions` | 0-1 credits | Metered, 0-1 credits: each call reads one page of /v1/twitter/search/tweets (1 credit), each billed at that endpoint's own price exactly as a direct call is. A page that found nothing or failed costs nothing, and a page served from cache is free. A page is billed when it returned rows, even if none of them carried the mention; data.legs shows each page's charge and data.excluded what was left out. |
| `GET /v1/twitter/search/tweets` | 1-9 credits | 1 credit per page. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/twitter/tweet/replies` | 1-5 credits | 1 credit per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/twitter/user/tweets` | 1-5 credits | 1 credit per page. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/utility/ai-detection` | 1 credit | 1 credit per text. A call that cannot be scored right now (503) is not charged. |
| `GET /v1/walmart/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/wayfair/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `POST /v1/web/batch-scrape` | N credits for N submitted URLs | 1 credit per URL submitted, held up front and refunded down to the URLs actually scraped when the job settles |
| `POST /v1/web/crawl` | 1-10,000 credits | 1 credit per page crawled. Submitting holds `limit` credits up front (default limit 10, max 10,000) and the unused portion is refunded when the job settles |
| `GET /v1/web/extract` | 5 credits | A flat 5 credits. It runs through the metered pricer for consistency with the rest of the web surface, but nothing in your query changes the charge |
| `GET /v1/web/scrape` | 1-5 credits | 1 credit for a standard scrape. `proxy=auto`, `proxy=enhanced` and `pdf_parse=true` hold 5 credits and settle to what the fetch actually used, so a page a plain request could read still costs 1. Nothing else moves the price: screenshots, tag filters, `wait_for` and a mobile viewport are included. A page that comes back as the site's own block or error page (HTTP 400 or more), a CAPTCHA, a sign-in wall or an empty shell is returned with `page_state` saying so and a `_warnings` line, and is not charged. When the page scrapers cannot open a LinkedIn, Instagram, Facebook, Reddit, TikTok, YouTube, X or Threads profile or post, the page is read through that platform's own endpoint and costs that endpoint's price instead: 5 credits for a LinkedIn profile, company page or post, 1 credit for the others. The scrape's own charge is refunded to 0, so you pay the platform price once, and Activity Logs show the platform call as its own row |
| `GET /v1/web/search` | 2-120 credits | 2 credits per 10 results, so `limit` up to 10 costs 2, 11-20 costs 4, and the 100 maximum costs 20. `include_content=true` adds 1 credit per result, because it scrapes each result page as well as reading the SERP row - that is what takes a 100-result content search to the 120-credit ceiling. The hold settles down to the work actually done |
| `POST /v1/web/sessions` | 5-20 credits | 20 credits per browser-hour, minimum 5. The hold is taken from `ttl_seconds` when the session is created (60s default = 5, the 3,600s maximum = 20) and settled when it closes |
| `GET /v1/xiaohongshu/post/comments` | 5-100 credits | 5 credits per row RETURNED. The call holds `limit x 5` up front and settles down to the rows actually delivered. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/xiaohongshu/profile/posts` | 5-100 credits | 5 credits per row RETURNED. The call holds `limit x 5` up front and settles down to the rows actually delivered. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/xiaohongshu/search` | 5-100 credits | 5 credits per row RETURNED. The call holds `limit x 5` up front and settles down to the rows actually delivered. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/xiaohongshu/trending` | 5-100 credits | 5 credits per row RETURNED. The call holds `limit x 5` up front and settles down to the rows actually delivered. |
| `GET /v1/yelp/business/reviews` | 5-9 credits | 5 credits per page. The default labels (sentiment, issue) are free. label=reports, incentivized or injection holds 4 extra credits and refunds down to 1 credit per started 25 reviews that were newly judged (the first 100 reviews of a page are judged): reviews already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/youtube/channel/lives` | 1-7 credits | 1 credit for the page. include=engagement adds 1 credit per distinct stream filled, at most 5 per page; include=channel adds 1 credit for the single channel lookup the page shares. Anything that could not be filled is refunded, so a page with both is at most 7 credits, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/youtube/channel/shorts` | 1-2 credits | 1 credit for the page. include=channel adds 1 credit for the single channel lookup the page shares, refunded if the channel could not be read and free when it was looked up recently. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/youtube/channel/videos` | 1-2 credits | 1 credit for the page. include=channel adds 1 credit for the single channel lookup the page shares, refunded if the channel could not be read and free when it was looked up recently. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `POST /v1/youtube/channels` | 5-100 credits | 5 credits per 50-id chunk, so a 50-id batch is 5 credits and the 1,000-id maximum is 100. Batching is what makes this cheap: the same 1,000 channels fetched one at a time through GET /v1/youtube/channel cost 1,000 credits. A chunk is charged whether or not every id in it resolves, so there is no per-id refund; a call that resolves nothing at all is refunded in full |
| `GET /v1/youtube/playlist` | 1-11 credits | 1 credit for the page. include=engagement and include=channel each add 1 credit per distinct video or channel filled, at most 5 per join on a page of up to 50 rows, so a page with both is at most 11 credits; ids that could not be filled are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/youtube/playlist/items` | 1-11 credits | 1 credit for the page. include=engagement and include=channel each add 1 credit per distinct video or channel filled, at most 5 per join on a page of up to 50 rows, so a page with both is at most 11 credits; ids that could not be filled are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/youtube/search` | 1-19 credits | 1 credit for the page. include=engagement and include=channel each add 1 credit per distinct video or channel filled, at most 5 per join on a page of up to 50 rows, so a page with both is at most 11 credits; ids that could not be filled are refunded, and a repeat of the same call within the cache window costs 0. Relevance against your query (by default, or with relevance=) is free. Adding relevant_to= holds 4 extra credits and refunds down to 1 credit per started 25 rows that were newly judged: rows already judged for the same topic are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. The default labels (sponsored, intent, niche) are free. label=mention, quality, ai_style, ai_written, injection, or label=intent with offer=, holds 4 extra credits and refunds down to 1 credit per started 25 posts that were newly judged: posts already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/youtube/search/advanced` | 1-11 credits | 1 credit for the search page. `includeExtras=true` adds a flat 5 credits for the single hydration call that fills view, like and comment counts and `duration_seconds` on the whole page. The increment never repeats: the page caps at 50 results, which one hydration call covers, so a hydrated page of 50 costs 6 credits and so does a hydrated page of 5. include=channel adds 1 credit per distinct channel filled, at most 5 per page, with channels that could not be read refunded, so a page with both is at most 11 With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/youtube/search/hashtag` | 1-11 credits | 1 credit for the page. include=engagement and include=channel each add 1 credit per distinct video or channel filled, at most 5 per join on a page of up to 50 rows, so a page with both is at most 11 credits; ids that could not be filled are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. With `seen`, a page's price falls with its share of rows you already received under that id; credits for joined data (`include=`) are never discounted. |
| `GET /v1/youtube/shorts/trending` | 5-15 credits | 5 credits for the feed. include=channel adds 1 credit per distinct channel filled, at most 5 per 50 channels (the feed carries about 70, so at most 10); channels that could not be read are refunded, and a repeat of the same call within the cache window costs 0. |
| `POST /v1/youtube/transcripts` | 3-300 credits | 3 credits per successful transcript. Up to 100 ids per call: the call holds ids × 3 up front (a full batch holds 300) and refunds every not_found, errored and deferred row |
| `GET /v1/youtube/video` | 1-3 credits | 1 credit for the video. include=availability holds 2 more and keeps them only when the availability block comes back, so a call with it is at most 3 credits; a lookup that fails and a video looked up recently (served from cache) are refunded. |
| `GET /v1/youtube/video/comment/replies` | 1-5 credits | 1 credit per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/youtube/video/comments` | 1-5 credits | 1 credit per page, with the default labels (sentiment, question, purchase_intent, complaint) included free. label=spam, toxic or low_quality holds 4 extra credits and refunds down to 1 credit per started 25 comments that were newly judged: comments already labelled are free, a page where nothing could be judged refunds the whole extra, and a cached page is free. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |
| `GET /v1/youtube/video/related` | 1-11 credits | 1 credit for the page. include=engagement and include=channel each add 1 credit per distinct video or channel filled, at most 5 per join on a page of up to 50 rows, so a page with both is at most 11 credits; ids that could not be filled are refunded, and a repeat of the same call within the cache window costs 0. |
| `POST /v1/youtube/videos` | 5-100 credits | 5 credits per 50-id chunk, so a 50-id batch is 5 credits and the 1,000-id maximum is 100. Batching is what makes this cheap: the same 1,000 videos fetched one at a time through GET /v1/youtube/video cost 1,000 credits. A chunk is charged whether or not every id in it resolves, so there is no per-id refund; a call that resolves nothing at all is refunded in full |
| `GET /v1/youtube/videos/trending` | 1-6 credits | 1 credit for the page. include=channel adds 1 credit per distinct channel filled, at most 5 per 50 channels; channels that could not be read are refunded, and a repeat of the same call within the cache window costs 0. With `max_pages`, `max_items` or `max_credits`, each page walked is billed at this price (a cached page is free), and `max_credits` caps the total. |

## Per-endpoint pricing

`Credits` is the charge for one live (non-cached) successful call. `Cache` is how long a successful response is reused - a repeat call inside that window costs 0.

### Airbnb (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/airbnb/listing` | GET | Get an Airbnb listing | 1 | standard | 900s |
| `/v1/airbnb/listing/availability` | GET | Get an Airbnb listing's availability calendar | 5 | advanced | 1800s |
| `/v1/airbnb/listing/reviews` | GET | List the guest reviews of an Airbnb listing | 5-9 (metered) | advanced | 300s |
| `/v1/airbnb/search` | GET | Search Airbnb listings for a place | 1 | standard | 120s |

### AliExpress (9)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/aliexpress/categories` | GET | List AliExpress categories | 1 | standard | 1800s |
| `/v1/aliexpress/product` | GET | Get an AliExpress product by id or URL | 5 | advanced | 600s |
| `/v1/aliexpress/product/shipping` | GET | Get AliExpress shipping for a product SKU | 5 | advanced | 600s |
| `/v1/aliexpress/product/similar` | GET | Get similar AliExpress products | 5 | advanced | 120s |
| `/v1/aliexpress/promo` | GET | List AliExpress featured promotions | 1 | standard | 1800s |
| `/v1/aliexpress/reviews` | GET | Get AliExpress product reviews | 5-9 (metered) | advanced | 300s |
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
| `/v1/amazon/reviews` | GET | Get Amazon product reviews | 5-9 (metered) | advanced | 300s |
| `/v1/amazon/seller` | GET | Get an Amazon seller profile | 1 | standard | 900s |
| `/v1/amazon/sellers` | GET | Get Amazon sellers and offers for a product | 1 | standard | 600s |
| `/v1/amazon/shop` | GET | Get Amazon shop page | 1 | standard | 600s |

### Apple App Store (9)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/app_store/app-info` | GET | Get full Apple App Store app details | 5 | advanced | 600s |
| `/v1/app_store/app-list` | GET | Get an Apple App Store chart | 5 | advanced | 120s |
| `/v1/app_store/app-listings-search` | GET | Search the Apple App Store listings database (paginated) | 10 | premium | 120s |
| `/v1/app_store/app-reviews` | GET | Get Apple App Store reviews for an app | 5-9 (metered) | advanced | 300s |
| `/v1/app_store/app-search` | GET | Search Apple App Store apps by keyword | 5 | advanced | 120s |
| `/v1/app_store/categories` | GET | List Apple App Store app categories | 1 | standard | 1800s |
| `/v1/app_store/languages` | GET | List supported Apple App Store languages | 1 | standard | 1800s |
| `/v1/app_store/locations` | GET | List supported Apple App Store storefront locations | 1 | standard | 1800s |
| `/v1/app_store/search-suggestions` | GET | Get Apple App Store search suggestions | 1 | standard | 120s |

### Apple Music (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/apple_music/album` | GET | Get an Apple Music album | 1 | standard | 600s |
| `/v1/apple_music/artist` | GET | Get an Apple Music artist | 1 | standard | 900s |
| `/v1/apple_music/charts` | GET | Get the Apple Music charts for a country | 1 | standard | 3600s |
| `/v1/apple_music/search` | GET | Search Apple Music | 1 | standard | 120s |
| `/v1/apple_music/track` | GET | Get an Apple Music track | 1 | standard | 600s |

### Bing (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/bing/rank` | GET | Check where a domain ranks on Bing, up to 200 deep | 5 | advanced | 1800s |
| `/v1/bing/search` | GET | Get Bing's first results page for a search | 1 | standard | 120s |
| `/v1/bing/suggestions` | GET | Get Bing's search suggestions for a partial query | 1 | standard | 120s |
| `/v1/bing/videos` | GET | Search Bing Videos | 5 | advanced | 120s |

### Bluesky (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/bluesky/post` | GET | Get a Bluesky post | 1 | standard | 600s |
| `/v1/bluesky/profile` | GET | Get a Bluesky profile | 1 | standard | 900s |
| `/v1/bluesky/search` | GET | Search Bluesky posts | 1 | standard | 120s |
| `/v1/bluesky/user/posts` | GET | List a Bluesky user's posts | 1 | standard | 600s |

### Booking.com (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/booking/hotel` | GET | Get a Booking.com property | 1 | standard | 900s |
| `/v1/booking/hotel/reviews` | GET | List the guest reviews of a Booking.com property | 5-9 (metered) | advanced | 300s |
| `/v1/booking/search` | GET | Search Booking.com properties for a destination and stay | 1 | standard | 120s |

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

### DuckDuckGo (7)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/duckduckgo/images` | GET | Search DuckDuckGo Images | 1 | standard | 120s |
| `/v1/duckduckgo/instant-answer` | GET | Get DuckDuckGo's instant answer for a topic | 1 | standard | 1800s |
| `/v1/duckduckgo/news` | GET | Search DuckDuckGo News | 1 | standard | 120s |
| `/v1/duckduckgo/rank` | GET | Check where a domain ranks on DuckDuckGo, up to 200 deep | 5 | advanced | 1800s |
| `/v1/duckduckgo/search` | GET | Search DuckDuckGo | 1 | standard | 120s |
| `/v1/duckduckgo/suggestions` | GET | Get DuckDuckGo's search suggestions for a partial query | 1 | standard | 120s |
| `/v1/duckduckgo/videos` | GET | Search DuckDuckGo Videos | 1 | standard | 120s |

### eBay (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/ebay/product` | GET | Get an eBay listing by item id | 5 | advanced | 600s |
| `/v1/ebay/search` | GET | Search eBay listings | 5 | advanced | 120s |

### Economy (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/economy/consumer-spend` | GET | Get household spending by country and category | 1 | standard | 86400s |
| `/v1/economy/government-contracts` | GET | Search US federal contract awards | 1 | standard | 120s |
| `/v1/economy/government-spend` | GET | Get US federal spending by state, county or country | 1 | standard | 21600s |
| `/v1/economy/imports` | GET | Get a US importer's suppliers and shipments | 20 | custom | 86400s |
| `/v1/economy/tourism-spend` | GET | Get travel spending by country and category | 1 | standard | 86400s |

### Etsy (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/etsy/product` | GET | Get an Etsy listing by id or URL | 5 | advanced | 600s |
| `/v1/etsy/product/similar` | GET | Get listings similar to an Etsy product | 5 | advanced | 120s |
| `/v1/etsy/search/suggestions` | GET | Get Etsy search suggestions | 5 | advanced | 120s |
| `/v1/etsy/shop/products` | GET | List products in an Etsy shop | 5 | advanced | 120s |

### Facebook (32)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/facebook/adlibrary/ad` | GET | Get Facebook Ad Library ad details | 5 | advanced | 1800s |
| `/v1/facebook/adlibrary/ad/transcript` | GET | Get a Facebook Ad Library video ad transcript | 10 | premium | 2592000s |
| `/v1/facebook/adlibrary/advertiser` | GET | Get a Facebook Ad Library advertiser's profile | 5 | advanced | 900s |
| `/v1/facebook/adlibrary/company/ads` | GET | List Facebook Ad Library company ads | 5-35 (metered) | advanced | 1800s |
| `/v1/facebook/adlibrary/search/ads` | GET | Search Facebook Ad Library | 5 | advanced | 120s |
| `/v1/facebook/adlibrary/search/companies` | GET | Search Facebook Ad Library companies | 5 | advanced | 120s |
| `/v1/facebook/event/details` | GET | Get details for a Facebook event | 1 | standard | 600s |
| `/v1/facebook/events` | GET | List Facebook events for a city | 1-13 (metered) | standard | 600s |
| `/v1/facebook/events/search` | GET | Search Facebook events by keyword | 1 | standard | 120s |
| `/v1/facebook/group` | GET | Get a Facebook group | 1 | standard | 900s |
| `/v1/facebook/group/posts` | GET | List Facebook group posts | 1 | standard | 600s |
| `/v1/facebook/marketplace/item` | GET | Get a Facebook Marketplace item | 1 | standard | 600s |
| `/v1/facebook/marketplace/location/search` | GET | Search Facebook Marketplace locations | 1 | standard | 120s |
| `/v1/facebook/marketplace/search` | GET | Search Facebook Marketplace listings | 1 | standard | 120s |
| `/v1/facebook/post` | GET | Get Facebook post details | 1-2 (metered) | standard | 600s |
| `/v1/facebook/post/comment/replies` | GET | List replies to a Facebook post comment | 1-5 (metered) | standard | 300s |
| `/v1/facebook/post/comments` | GET | List Facebook post comments | 1-5 (metered) | standard | 300s |
| `/v1/facebook/post/transcript` | GET | Get Facebook video transcript | 10 | premium | 2592000s |
| `/v1/facebook/profile` | GET | Get Facebook page profile | 1 | standard | 900s |
| `/v1/facebook/profile/events` | GET | List a Facebook page's events | 1-9 (metered) | standard | 600s |
| `/v1/facebook/profile/full` | GET | Facebook profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/facebook/profile/photos` | GET | List Facebook profile photos | 1-9 (metered) | standard | 600s |
| `/v1/facebook/profile/posts` | GET | List Facebook page posts | 1-4 (metered) | standard | 600s |
| `/v1/facebook/profile/reels` | GET | List Facebook profile reels | 1 | standard | 600s |
| `/v1/facebook/profile/reels/full` | GET | Facebook profile reels with exact views, likes, comments, and shares merged in, in one call. | 5-25 (metered) | advanced | 600s |
| `/v1/facebook/search/groups` | GET | Search Facebook groups by keyword | 1-15 (metered) | standard | 120s |
| `/v1/facebook/search/hashtag` | GET | Search Facebook posts and videos carrying a hashtag | 0-9 (metered) | standard | 120s |
| `/v1/facebook/search/mentions` | GET | Search Facebook posts that mention a page | 0-1 (metered) | standard | 120s |
| `/v1/facebook/search/pages` | GET | Search Facebook pages by keyword | 1-11 (metered) | standard | 120s |
| `/v1/facebook/search/people` | GET | Search Facebook people by keyword | 1 | standard | 120s |
| `/v1/facebook/search/posts` | GET | Search Facebook posts by keyword | 1-9 (metered) | standard | 120s |
| `/v1/facebook/search/videos` | GET | Search Facebook videos by keyword | 1-8 (metered) | standard | 120s |

### Finance (8)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/finance/fundamentals` | GET | Get quarterly or annual fundamentals for a public company | 1 | standard | 21600s |
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
| `/v1/g2/reviews` | GET | Get G2 reviews for a product | 5-9 (metered) | advanced | 300s |
| `/v1/g2/seller` | GET | Get a G2 seller (vendor) profile | 5 | advanced | 900s |
| `/v1/g2/seller/products` | GET | List products for a G2 seller | 5 | advanced | 120s |

### Gab (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/gab/post` | GET | Get a Gab post | 1 | standard | 600s |
| `/v1/gab/post/comments` | GET | List the comments on a Gab post | 1 | standard | 300s |
| `/v1/gab/profile` | GET | Get a Gab profile | 1 | standard | 900s |
| `/v1/gab/search/posts` | GET | Search Gab posts | 1 | standard | 120s |
| `/v1/gab/user/posts` | GET | List a Gab user's posts | 1 | standard | 600s |

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

### Goodreads (10)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/goodreads/author` | GET | Get a Goodreads author | 1 | standard | 900s |
| `/v1/goodreads/author/books` | GET | List a Goodreads author's books | 1 | standard | 1800s |
| `/v1/goodreads/book` | GET | Get a Goodreads book | 1 | standard | 1800s |
| `/v1/goodreads/book/editions` | GET | List every edition of a Goodreads book | 1 | standard | 1800s |
| `/v1/goodreads/book/reviews` | GET | List the reader reviews of a Goodreads book | 5-9 (metered) | advanced | 300s |
| `/v1/goodreads/lists` | GET | Read a Goodreads Listopia list, or the lists for a tag | 1 | standard | 1800s |
| `/v1/goodreads/quotes` | GET | List Goodreads quotes | 1 | standard | 1800s |
| `/v1/goodreads/review/comments` | GET | List the comments under a Goodreads review | 1 | standard | 300s |
| `/v1/goodreads/search` | GET | Search Goodreads books | 1 | standard | 1800s |
| `/v1/goodreads/series` | GET | Get a Goodreads series in reading order | 1 | standard | 1800s |

### Google (13)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google/ad` | GET | Get Google ad details | 5 | advanced | 1800s |
| `/v1/google/adlibrary/advertiser` | GET | Get a Google advertiser's verified identity | 5 | advanced | 900s |
| `/v1/google/adlibrary/advertisers/search` | GET | Search Google Ad Library advertisers | 5 | advanced | 120s |
| `/v1/google/business/extended-reviews` | GET | Get Google extended (multi-source) reviews | 5-9 (metered) | advanced | 600s |
| `/v1/google/business/info` | GET | Get a Google Business Profile | 1 | standard | 900s |
| `/v1/google/business/questions` | GET | Get Google Business Profile questions & answers | 5 | advanced | 300s |
| `/v1/google/business/search` | GET | Search Google Maps businesses | 5 | advanced | 120s |
| `/v1/google/business/updates` | GET | Get Google Business Profile posts (updates) | 1 | standard | 600s |
| `/v1/google/company/ads` | GET | List Google ads by company | 5 | advanced | 1800s |
| `/v1/google/hotels/info` | GET | Get Google hotel detail | 5 | advanced | 900s |
| `/v1/google/hotels/search` | GET | Search Google hotels | 1 | standard | 120s |
| `/v1/google/keyword-volume` | GET | Get Google keyword search volume by country | 16 | custom | 86400s |
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
| `/v1/google_play/app-reviews` | GET | Get Google Play reviews for an app | 5-9 (metered) | advanced | 300s |
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
| `/v1/google_shopping/reviews` | GET | Get Google Shopping product reviews | 1-5 (metered) | standard | 300s |
| `/v1/google_shopping/sellers` | GET | Get Google Shopping sellers for a product | 1 | standard | 600s |

### Google Trends (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google_trends/explore` | GET | Get Google Trends interest over time | 5 | advanced | 120s |
| `/v1/google_trends/rising` | GET | Get related + rising Google Trends queries | 5 | advanced | 120s |
| `/v1/google_trends/trending` | GET | Get Google Trends Trending Now for a location | 5 | advanced | 300s |

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
| `/v1/hackernews/search` | GET | Search Hacker News | 1-9 (metered) | standard | 120s |
| `/v1/hackernews/story` | GET | Get a Hacker News story | 1 | standard | 600s |
| `/v1/hackernews/story/comments` | GET | Get comments on a Hacker News story | 1 | standard | 300s |

### Home Depot (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/home_depot/product` | GET | Get a Home Depot product by item id or URL | 5 | advanced | 600s |
| `/v1/home_depot/reviews` | GET | Get Home Depot product reviews | 5-9 (metered) | advanced | 300s |
| `/v1/home_depot/search` | GET | Search Home Depot products by keyword | 5 | advanced | 120s |
| `/v1/home_depot/stores` | GET | Find Home Depot stores near a ZIP code | 1 | standard | 1800s |

### Instagram (44)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/instagram/audio/reels` | GET | List Instagram reels using an audio track | 1 | standard | 600s |
| `/v1/instagram/basic-profile` | GET | Get Instagram basic profile | 1 | standard | 900s |
| `/v1/instagram/comment` | GET | Look up one Instagram comment by URL or id | 5-15 (metered) | custom | 300s |
| `/v1/instagram/comment/likers` | GET | List the accounts that liked an Instagram comment | 1 | standard | 300s |
| `/v1/instagram/engagement` | GET | Get Instagram engagement statistics | 5 | advanced | 1800s |
| `/v1/instagram/followers` | GET | List Instagram followers | 5-10 (metered) | advanced | 900s |
| `/v1/instagram/following` | GET | List Instagram following | 5-10 (metered) | advanced | 900s |
| `/v1/instagram/hashtag` | GET | Get an Instagram hashtag's size: its exact media count | 1 | standard | 600s |
| `/v1/instagram/highlight/detail` | GET | Get Instagram highlight detail | 1 | standard | 600s |
| `/v1/instagram/highlights` | GET | List Instagram story highlights | 1 | standard | 900s |
| `/v1/instagram/location` | GET | Get an Instagram location's profile | 1 | standard | 900s |
| `/v1/instagram/location/posts` | GET | List recent posts at an Instagram location | 5-68 (metered) | advanced | 600s |
| `/v1/instagram/media/screen-text` | GET | Get Instagram post on-screen text | 5-10 (metered) | advanced | 600s |
| `/v1/instagram/media/transcript` | GET | Get Instagram media transcript | 10 | premium | 2592000s |
| `/v1/instagram/music/trending` | GET | List trending Instagram music | 5 | advanced | 120s |
| `/v1/instagram/post` | GET | Get Instagram post details | 1 | standard | 600s |
| `/v1/instagram/post/comment/replies` | GET | List replies under an Instagram comment | 1-5 (metered) | standard | 300s |
| `/v1/instagram/post/comments` | GET | List Instagram post comments | 5-19 (metered) | advanced | 300s |
| `/v1/instagram/post/likers` | GET | List Instagram post likers | 5 | advanced | 900s |
| `/v1/instagram/post/stats` | GET | Get Instagram post stats including the share count | 5-9 (metered) | advanced | 600s |
| `/v1/instagram/profile` | GET | Get Instagram user profile | 1 | standard | 900s |
| `/v1/instagram/profile/about` | GET | Get Instagram account transparency details | 1 | standard | 900s |
| `/v1/instagram/profile/country` | GET | Get the country an Instagram account declares, by user id | 1 | standard | 2592000s |
| `/v1/instagram/profile/full` | GET | Instagram profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/instagram/profile/posts` | GET | List Instagram user posts | 1-29 (metered) | standard | 600s |
| `/v1/instagram/profile/posts/full` | GET | Instagram posts with views, likes, comments, and per-post share counts where available, in one call. | 5-25 (metered) | advanced | 600s |
| `/v1/instagram/profile/reels` | GET | List Instagram user reels | 1-18 (metered) | standard | 600s |
| `/v1/instagram/profile/reels/full` | GET | Instagram reels with views, likes, comments, and per-reel share counts where available, in one call. | 5-25 (metered) | advanced | 600s |
| `/v1/instagram/reels/trending` | GET | Get trending Instagram reels | 5 | advanced | 120s |
| `/v1/instagram/search` | GET | Search Instagram accounts, hashtags, and places | 1 | standard | 120s |
| `/v1/instagram/search/hashtag` | GET | Feed of a known hashtag, 1 credit a page, every ranking paginates (for keyword or topic discovery use instagram/search/reels) | 1-31 (metered) | standard | 120s |
| `/v1/instagram/search/location` | GET | Search Instagram locations | 5 | advanced | 120s |
| `/v1/instagram/search/mentions` | GET | Search Instagram posts that tag or mention an account | 0-6 (metered) | standard | 120s |
| `/v1/instagram/search/music` | GET | Search Instagram music | 5 | advanced | 21600s |
| `/v1/instagram/search/popular` | GET | Search popular Instagram posts | 1-13 (metered) | standard | 120s |
| `/v1/instagram/search/profiles` | GET | Search Instagram profiles by keyword | 1-25 (metered) | standard | 120s |
| `/v1/instagram/search/reels` | GET | Search Instagram posts by keyword or topic: reels about a brand, phrase or subject, with view counts (1 credit a page) | 1-69 (metered) | standard | 120s |
| `/v1/instagram/similar` | GET | List similar Instagram accounts | 5-85 (metered) | advanced | 900s |
| `/v1/instagram/stories` | GET | List an Instagram user's active stories | 5 | advanced | 600s |
| `/v1/instagram/story/download` | GET | Download a single Instagram story | 5 | advanced | 600s |
| `/v1/instagram/tagged` | GET | List posts an Instagram user is tagged in | 5 | advanced | 600s |
| `/v1/instagram/trending/searches` | GET | List Instagram's trending searches | 5 | advanced | 300s |
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
| `/v1/klarna/reviews` | GET | Get Klarna user reviews for a product | 5-9 (metered) | advanced | 300s |
| `/v1/klarna/reviews/overview` | GET | Get Klarna review totals and score distributions | 5 | advanced | 1800s |
| `/v1/klarna/reviews/pro` | GET | Get Klarna professional reviews for a product | 5-9 (metered) | advanced | 300s |
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
| `/v1/kohls/reviews` | GET | Get Kohl's product reviews | 5-9 (metered) | advanced | 300s |
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

### LinkedIn (77)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/linkedin/ad` | GET | Get LinkedIn ad details | 5 | advanced | 1800s |
| `/v1/linkedin/ads/search` | GET | Search LinkedIn ads | 5 | advanced | 120s |
| `/v1/linkedin/article` | GET | Get a LinkedIn Pulse article | 5 | advanced | 600s |
| `/v1/linkedin/article/comments` | GET | List comments on a LinkedIn Pulse article | 5 | advanced | 300s |
| `/v1/linkedin/article/reactions` | GET | List reactors on a LinkedIn Pulse article | 5 | advanced | 300s |
| `/v1/linkedin/company` | GET | Get LinkedIn company page with its full About tab | 5-8 (metered) | advanced | 900s |
| `/v1/linkedin/company/affiliated-pages` | GET | List a company's affiliated/showcase pages | 5 | advanced | 900s |
| `/v1/linkedin/company/also-viewed` | GET | List company pages people also viewed | 5 | advanced | 120s |
| `/v1/linkedin/company/bulk` | GET | Get up to 25 LinkedIn company pages in one call | 5-125 (metered) | advanced | 900s |
| `/v1/linkedin/company/by-domain` | GET | Look up a LinkedIn company page from its website domain | 5 | advanced | 900s |
| `/v1/linkedin/company/employees-count` | GET | Get a company's employee count, optionally by location | 5 | advanced | 1800s |
| `/v1/linkedin/company/insights` | GET | Get aggregate insights about a company's members | 5 | advanced | 1800s |
| `/v1/linkedin/company/job-count` | GET | Get a company's open job count | 5 | advanced | 1800s |
| `/v1/linkedin/company/jobs` | GET | List a company's job postings | 10 | premium | 120s |
| `/v1/linkedin/company/people` | GET | List people at a LinkedIn company | 10-50 (metered) | premium | 900s |
| `/v1/linkedin/company/posts` | GET | List LinkedIn company posts | 5 | advanced | 600s |
| `/v1/linkedin/group` | GET | Get LinkedIn group details | 5 | advanced | 900s |
| `/v1/linkedin/group/posts` | GET | List posts in a LinkedIn group | 5 | advanced | 600s |
| `/v1/linkedin/job` | GET | Get LinkedIn job details | 5 | advanced | 600s |
| `/v1/linkedin/job/hiring-team` | GET | List the hiring team on a LinkedIn job | 5 | advanced | 120s |
| `/v1/linkedin/post` | GET | Get LinkedIn post details | 5 | advanced | 600s |
| `/v1/linkedin/post/comments` | GET | Get LinkedIn post comments | 5 | advanced | 600s |
| `/v1/linkedin/post/comments/replies` | GET | List replies to a LinkedIn comment | 5 | advanced | 300s |
| `/v1/linkedin/post/reactions` | GET | List reactors on a LinkedIn post | 10-50 (metered) | premium | 300s |
| `/v1/linkedin/post/reposts` | GET | List reposts of a LinkedIn post | 5 | advanced | 600s |
| `/v1/linkedin/post/transcript` | GET | Get a LinkedIn post video transcript | 10 | premium | 2592000s |
| `/v1/linkedin/post/with-comments` | GET | Get a LinkedIn post together with its comments | 5 | advanced | 600s |
| `/v1/linkedin/profile` | GET | Get LinkedIn user profile | 5 | advanced | 900s |
| `/v1/linkedin/profile/about` | GET | Get a member's account freshness signals (NOT the profile About section) | 5 | advanced | 900s |
| `/v1/linkedin/profile/activity` | GET | Get when a LinkedIn member was last active | 5 | advanced | 900s |
| `/v1/linkedin/profile/all` | GET | Get a member's entire profile, counts included, in one call | 5-50 (metered) | advanced | 900s |
| `/v1/linkedin/profile/articles` | GET | List Pulse articles a LinkedIn member published | 5 | advanced | 600s |
| `/v1/linkedin/profile/certifications` | GET | List a member's licenses and certifications | 5 | advanced | 900s |
| `/v1/linkedin/profile/comments` | GET | List a member's comments | 5 | advanced | 300s |
| `/v1/linkedin/profile/complete` | GET | Get a member's profile, experience, education, skills and recommendations | 10 | premium | 900s |
| `/v1/linkedin/profile/contact` | GET | Get a member's public contact info | 5 | advanced | 900s |
| `/v1/linkedin/profile/courses` | GET | List a member's courses | 5 | advanced | 900s |
| `/v1/linkedin/profile/educations` | GET | List a member's education history | 5 | advanced | 900s |
| `/v1/linkedin/profile/experiences` | GET | List a member's work experiences | 5 | advanced | 900s |
| `/v1/linkedin/profile/featured` | GET | List the items a member features on their profile | 5 | advanced | 900s |
| `/v1/linkedin/profile/full` | GET | LinkedIn company profile, recent posts, and computed analytics in one call. Company pages only; a member's profile is `/v1/linkedin/profile/all`. | 5 | custom | 900s |
| `/v1/linkedin/profile/honors` | GET | List a member's honors and awards | 5 | advanced | 900s |
| `/v1/linkedin/profile/images` | GET | List a member's image posts | 5 | advanced | 600s |
| `/v1/linkedin/profile/interests/companies` | GET | List companies a member follows | 5 | advanced | 900s |
| `/v1/linkedin/profile/interests/groups` | GET | List groups a member follows | 5 | advanced | 900s |
| `/v1/linkedin/profile/interests/newsletters` | GET | List newsletters a LinkedIn member follows | 5 | advanced | 900s |
| `/v1/linkedin/profile/interests/schools` | GET | List schools a LinkedIn member follows | 5 | advanced | 900s |
| `/v1/linkedin/profile/interests/top-voices` | GET | List Top Voices a LinkedIn member follows | 5 | advanced | 900s |
| `/v1/linkedin/profile/languages` | GET | List a member's languages | 5 | advanced | 900s |
| `/v1/linkedin/profile/organizations` | GET | List a member's organizations | 5 | advanced | 900s |
| `/v1/linkedin/profile/patents` | GET | List a member's patents | 5 | advanced | 900s |
| `/v1/linkedin/profile/position-skills` | GET | List a member's positions with the skills on each role | 5 | advanced | 900s |
| `/v1/linkedin/profile/posted-jobs` | GET | List jobs a LinkedIn member has posted | 5 | advanced | 120s |
| `/v1/linkedin/profile/posts` | GET | List a LinkedIn member's posts | 5-200 (metered) | advanced | 600s |
| `/v1/linkedin/profile/posts/archive` | GET | Walk a LinkedIn member's COMPLETE post history, 100 posts a page, with exact publish times and share counts the other endpoints cannot return. Metered: 5 credits per post returned, so try the cheaper /v1/linkedin/profile/posts first | 5-500 (metered) | advanced | 600s |
| `/v1/linkedin/profile/projects` | GET | List a member's projects | 5 | advanced | 900s |
| `/v1/linkedin/profile/publications` | GET | List a member's publications | 5 | advanced | 900s |
| `/v1/linkedin/profile/reactions` | GET | List posts a LinkedIn member reacted to | 5 | advanced | 600s |
| `/v1/linkedin/profile/recommendations` | GET | List recommendations for a member | 5 | advanced | 900s |
| `/v1/linkedin/profile/similar` | GET | List LinkedIn members similar to a given profile | 5 | advanced | 120s |
| `/v1/linkedin/profile/skills` | GET | List a member's skills | 5 | advanced | 900s |
| `/v1/linkedin/profile/skills/endorsers` | GET | List who endorsed a member's skill | 5 | advanced | 900s |
| `/v1/linkedin/profile/stats` | GET | Get a member's follower + connection counts | 5 | advanced | 900s |
| `/v1/linkedin/profile/test-scores` | GET | List a member's test scores | 5 | advanced | 900s |
| `/v1/linkedin/profile/top-position` | GET | Get the company page of a member's top position | 5 | advanced | 900s |
| `/v1/linkedin/profile/videos` | GET | List a member's video posts | 5 | advanced | 600s |
| `/v1/linkedin/profile/volunteers` | GET | List a member's volunteer experiences | 5 | advanced | 900s |
| `/v1/linkedin/profile/with-posts` | GET | Get a member profile with follower and connection counts and recent posts | 10 | premium | 900s |
| `/v1/linkedin/search/companies` | GET | Search LinkedIn company pages | 10 | premium | 120s |
| `/v1/linkedin/search/hashtag` | GET | Search LinkedIn posts by hashtag | 10 | premium | 120s |
| `/v1/linkedin/search/industry` | GET | Resolve an industry name to a LinkedIn industry id | 1 | standard | 120s |
| `/v1/linkedin/search/jobs` | GET | Search LinkedIn jobs | 10 | premium | 120s |
| `/v1/linkedin/search/location` | GET | Resolve a location to a LinkedIn geocode id | 1 | standard | 120s |
| `/v1/linkedin/search/people` | GET | Search LinkedIn people | 10-50 (metered) | premium | 120s |
| `/v1/linkedin/search/people/by-url` | GET | Search LinkedIn people from a search-results URL | 10 | premium | 120s |
| `/v1/linkedin/search/posts` | GET | Search public LinkedIn posts by keyword | 1-56 (metered) | advanced | 120s |
| `/v1/linkedin/search/schools` | GET | Search LinkedIn schools | 1 | standard | 120s |

### LinkMe (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/linkme/page` | GET | Get Linkme profile | 1 | standard | 900s |

### Linktree (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/linktree/page` | GET | Get Linktree page | 1 | standard | 900s |

### Naver (20)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/naver/adult` | GET | Check whether a Korean search term is adult-only (성인 검색어 판별) | 1 | standard | 1800s |
| `/v1/naver/blog` | GET | Get a Naver blog's card and visitor counter (블로그 정보) | 1 | standard | 900s |
| `/v1/naver/blog/posts` | GET | List every post of a Naver blog, newest first (블로그 글 목록) | 1 | standard | 600s |
| `/v1/naver/blog/search` | GET | Search Naver Blog | 1-9 (metered) | standard | 120s |
| `/v1/naver/brief` | GET | One query across the Korean internet (5 Naver corpora) + optional digest. | 10 | custom | 120s |
| `/v1/naver/cafearticle/search` | GET | Search Naver Cafe articles | 1-9 (metered) | standard | 120s |
| `/v1/naver/encyc/search` | GET | Search Naver Encyclopedia | 1 | standard | 120s |
| `/v1/naver/errata` | GET | Correct a mistyped Korean search query (오타변환) | 1 | standard | 1800s |
| `/v1/naver/image/search` | GET | Search Naver Image | 1 | standard | 120s |
| `/v1/naver/kin/search` | GET | Search Naver KnowledgeiN (지식iN) | 1 | standard | 120s |
| `/v1/naver/local/search` | GET | Search Naver Local (장소 검색) | 1 | standard | 120s |
| `/v1/naver/news/search` | GET | Search Naver News | 1-9 (metered) | standard | 120s |
| `/v1/naver/place` | GET | Get a Naver Place card (플레이스 정보) | 3 | custom | 900s |
| `/v1/naver/place/rank` | GET | Check where a place ranks on Naver Map for keywords (플레이스 순위) | 4-42 (metered) | custom | 1800s |
| `/v1/naver/place/reviews` | GET | Get the newest visitor reviews of a Naver Place (방문자 리뷰) | 5-9 (metered) | advanced | 300s |
| `/v1/naver/place/search` | GET | Search Naver Map places for a keyword, in Naver's order (플레이스 검색) | 4 | custom | 120s |
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

### Pinterest (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/pinterest/board` | GET | Get Pinterest board | 1-16 (metered) | standard | 600s |
| `/v1/pinterest/pin` | GET | Get Pinterest pin details | 1 | standard | 600s |
| `/v1/pinterest/search` | GET | Search Pinterest pins | 1-34 (metered) | standard | 120s |
| `/v1/pinterest/trends` | GET | Get Pinterest Trends for a country | 10 | premium | 21600s |
| `/v1/pinterest/url-stats` | GET | Get Pinterest save counts for external URLs | 1 | standard | 1800s |
| `/v1/pinterest/user/boards` | GET | List Pinterest user boards | 1 | standard | 900s |

### Polymarket (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/polymarket/research` | GET | Polymarket prediction markets: multi-query research | 5 | advanced | 120s |
| `/v1/polymarket/search` | GET | Search Polymarket prediction markets | 1 | standard | 120s |

### Prism (53)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/prism/adverse-screen` | GET | Screen a person's public social profiles for adverse posts, with every flag citing its post, for human review. | 25-75 (metered) | custom | 1800s |
| `/v1/prism/ai-visibility` | GET | AI Share-of-Voice / GEO monitoring: prompt set x reruns to per-brand appearance-% per AI engine plus a cited-domain ranking. | 2-1,605 (metered) | custom | 120s |
| `/v1/prism/answers` | GET | Multi-engine AI consensus: one question → Perplexity + Grok + Tavily answers verbatim, merged citations, and an agreement matrix. | 15 | custom | 120s |
| `/v1/prism/app-reviews` | GET | Cross-store app review intelligence (Google Play + App Store): translated, clustered, sentiment-scored. | 10-15 (metered) | custom | 300s |
| `/v1/prism/apps-lookup` | GET | One app across Google Play + the App Store: resolved, title-matched, and compared into a cross-store rating + listing report. | 30 | custom | 1800s |
| `/v1/prism/audience-language` | GET | Language mix of the people commenting on a creator's recent posts, beside the follower sample on TikTok. | 2-26 (metered) | custom | 1800s |
| `/v1/prism/audience-overlap` | GET | How much two TikTok creators' commenter audiences overlap. Jaccard, shared-fan count, and a confidence label. | 20 | custom | 1800s |
| `/v1/prism/audience-questions` | GET | The real questions a topic's audience asks: harvested from Reddit + YouTube threads (Naver KnowledgeiN for Korean topics) and clustered by intent (who/what/why/how/vs). | 30 | custom | 1800s |
| `/v1/prism/brand-mentions` | GET | Brand mention volume time-series, sentiment split, top sources, and recent mentions for one keyword. | 50 | custom | 1800s |
| `/v1/prism/brief-check` | GET | Check a creator post against a campaign brief: talking points, forbidden claims, and disclosure. | 15 | custom | 1800s |
| `/v1/prism/campaign` | GET | Campaign tracker: pre/during/post volume lift, cross-platform engagement, and ranked top amplifiers for a hashtag or phrase. | 35 | custom | 1800s |
| `/v1/prism/comment-leads` | GET | Buyer leads from the comments under the posts a keyword search returns, opening only the posts worth opening. | 0-243 (metered) | custom | 1800s |
| `/v1/prism/comment-lookup` | POST | Re-check up to 25 known comments in one call: per-item results, failed items refunded. | 2-100 (metered) | custom | none |
| `/v1/prism/comments` | GET | Every comment on a post, replies nested, server-paginated to completion. | 2-200 (metered) | standard | 300s |
| `/v1/prism/creator-card` | GET | One handle, unified author cards across TikTok, Instagram, YouTube, X (and more). | 5-8 (metered) | custom | 900s |
| `/v1/prism/creator-vet` | GET | Vet a creator before partnering: engagement quality, commenter authenticity, posting cadence, and controversy signals, optionally across platforms. | 50-75 (metered) | custom | 1800s |
| `/v1/prism/creators` | GET | Find creators (influencers) who post about a niche on TikTok, Instagram, YouTube, X and LinkedIn, or measure and rank creators you already have, in one call or as a background run. | pay per search and lookup, capped by max_credits (default 200) (request-shaped) | standard | none |
| `/v1/prism/creators` | POST | Start a creator search from a JSON body, for handle lists and exclusions too long for a URL; it runs in the background and answers 202 with the run. | pay per search and lookup, capped by the required max_credits (request-shaped) | standard | none |
| `/v1/prism/crisis-postmortem` | GET | Crisis post-mortem: a who-said-what-first timeline across web, Reddit, Hacker News, and social, with an origin, peak, propagation sequence, and a grounded narrative. | 35 | custom | 1800s |
| `/v1/prism/crisis-radar` | GET | Stateless crisis breach check: a z-score on daily mention volume and negative share, with on-breach confirmation and a severity grade. | 15-45 (metered) | custom | 1800s |
| `/v1/prism/demand-signals` | GET | Consumer-demand nowcast: app-review velocity, web mention slope, Reddit velocity, and commerce review levels, fused into a published demand index. | 30 | custom | 300s |
| `/v1/prism/devtool-pulse` | GET | Developer-brand health: a devtool's repo dossier + Hacker News reaction + Reddit chatter + dev-blog echo, in one call. | 20 | custom | 1800s |
| `/v1/prism/discover` | GET | Search many platforms for keywords or a description, keep a date window, judge every row and return the posts, in one call or as a background run. | pay per search, capped by max_credits (default 50) (request-shaped) | standard | none |
| `/v1/prism/discover` | POST | Start a discover run from a JSON body, for groups and lists too long for a URL; it runs in the background and answers 202 with the run. | pay per search, capped by the required max_credits (request-shaped) | standard | none |
| `/v1/prism/discover/inputs` | POST | Store a long author list or exclude list once and reuse it by id. | 0 | custom | none |
| `/v1/prism/earliness` | GET | How early a term appeared on each platform, before Trends and before ads. | 25 | custom | 1800s |
| `/v1/prism/earned-media` | GET | A brand's earned-media footprint: news + tech-press + fresh-web clips, deduped and ranked, with an outlet-coverage rollup. | 25 | custom | 1800s |
| `/v1/prism/employer-brand` | GET | A company's employer brand: what people say about working there across Reddit, the web, YouTube, Naver, and the company's own LinkedIn voice. | 30 | custom | 1800s |
| `/v1/prism/find-accounts` | GET | Turn a person's or a company's name into ranked candidate accounts on Instagram, TikTok, X and LinkedIn (Threads and YouTube on request), with a match level and a match confidence per platform, for human review. | 2-29 (metered) | custom | 1800s |
| `/v1/prism/format-lift` | GET | Which hook works for this creator, measured against their own posts. | 4 | custom | 1800s |
| `/v1/prism/handle-audit` | GET | Should you pull this handle? One call scores a handle across platforms, ranks the best ones, and projects the data volume + credit cost to pull it. | 5-8 (metered) | custom | 1800s |
| `/v1/prism/investigate` | GET | A bounded read-only walk over SocialCrawl endpoints that turns a research goal into a trail of searches, profiles and comments. | 1 | custom | none |
| `/v1/prism/jobs` | GET | List the API key's background jobs, newest first. | 0 | custom | none |
| `/v1/prism/jobs` | POST | Run a batch or any GET endpoint as a background job: up to 5,000 profiles or post URLs, or 1,000 calls to one GET. | per row, at the batch endpoint's own price (request-shaped) | custom | none |
| `/v1/prism/jobs/{job_id}` | GET | Status and results of one background job. | 0 | custom | none |
| `/v1/prism/korea-gap` | GET | What the world is talking about that Korea isn't (and vice versa): the global vs Korean (Naver) conversation gap for a brand/topic. | 15-40 (metered) | custom | 1800s |
| `/v1/prism/launch-echo` | GET | How a launch landed: the Hacker News reaction (top threads + comments), the dev-blog echo, and an optional repo dossier. | 20 | custom | 1800s |
| `/v1/prism/leads` | GET | Ranked feed of public conversations where people seek alternatives to or are switching from a competitor. | 50 | custom | 1800s |
| `/v1/prism/lookup` | GET | Universal post/product URL dispatcher: any post, video, product or repo link → the right detail endpoint's unified response. | 0 | custom | 600s |
| `/v1/prism/mentions` | GET | Public posts and comments that mention a handle or contain a link, from the first page of each search that can find them. | 1-9 (metered) | custom | 1800s |
| `/v1/prism/org-radar` | GET | A GitHub org's footprint: its top repos each expanded into a full dossier (releases, issue load, top request/complaint), rolled up. | 6-51 (metered) | custom | 1800s |
| `/v1/prism/post-comments` | POST | Up to 25 post URLs across platforms → each post's comments in one call, priced per page like the comment endpoints. | 1-2,500 (metered) | custom | none |
| `/v1/prism/post-stats` | POST | Up to 100 mixed-platform post URLs → current engagement per URL, failed URLs refunded. | 1-500 (metered) | custom | none |
| `/v1/prism/product-reviews` | GET | A product's reviews across Amazon + Google Shopping + Trustpilot, folded into a cross-marketplace rating + themed pros/cons report. | 30 | custom | 1800s |
| `/v1/prism/profile/comments` | GET | New comments on a profile's recent posts, in one list, newest first. | 2-2,428 (metered) | standard | none |
| `/v1/prism/profiles` | POST | Up to 50 (platform, handle) pairs → one canonical Author per row, failed handles refunded. | 1-126,375 (metered) | custom | none |
| `/v1/prism/reputation` | GET | A brand's cross-source reputation. Trustpilot + app stores + Google Business + web sentiment, blended into one weighted score with themed pros/cons. | 30 | custom | 1800s |
| `/v1/prism/review-integrity` | GET | Cross-source review integrity verdict (statistical, deterministic). | 30 | custom | 1800s |
| `/v1/prism/share-of-voice` | GET | Engagement-weighted Share of Voice across 2-5 brands, with web+social split, emotion overlay, and ESOV. | 20-200 (metered) | custom | 1800s |
| `/v1/prism/trend-board` | GET | What is rising in one country today, with no keyword in: breakout TikTok posts, sounds, hashtags, and Google searches. | 30 | custom | 900s |
| `/v1/prism/truthsocial-pulse` | GET | A Truth Social handle's pulse: profile, recent posts, per-post detail drill, and the news echo, in one call. | 20 | custom | 1800s |
| `/v1/prism/video-intel` | GET | One video URL → detail + stats + transcript + top comments + commenter sample, across YouTube/TikTok/Rumble/Instagram. | 5-15 (metered) | custom | 600s |
| `/v1/prism/voice` | GET | One person's public posts across X, Threads, Bluesky, and Truth Social, time-merged. | 5 | custom | 600s |

### Product Hunt (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/producthunt/launches` | GET | List current Product Hunt launches | 1 | standard | 120s |
| `/v1/producthunt/leaderboard` | GET | Get a Product Hunt leaderboard for any day, week, month or year since 2013 | 1 | standard | 1800s |
| `/v1/producthunt/product` | GET | Get a Product Hunt product and its launch | 1 | standard | 900s |
| `/v1/producthunt/product/comments` | GET | List the comments on a Product Hunt launch | 1 | standard | 300s |
| `/v1/producthunt/topic` | GET | List the products in a Product Hunt topic | 1 | standard | 1800s |

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
| `/v1/reddit/post/comments` | GET | List Reddit post comments | 5-9 (metered) | advanced | 300s |
| `/v1/reddit/post/transcript` | GET | Get a Reddit video post transcript | 10 | premium | 2592000s |
| `/v1/reddit/profile` | GET | Get a Reddit user profile | 1 | standard | 900s |
| `/v1/reddit/profile/comments` | GET | Read a Reddit account's own comment history, newest first, deeper than any search index reaches. Metered: 2 credits per comment returned, so try /v1/reddit/search/comments?query=author:name first | 2-200 (metered) | standard | 600s |
| `/v1/reddit/profile/posts` | GET | List a Reddit user's posts | 1 | standard | 600s |
| `/v1/reddit/search` | GET | Search Reddit posts | 1-48 (metered) | standard | 120s |
| `/v1/reddit/search/comments` | GET | Search Reddit comments | 1 | standard | 120s |
| `/v1/reddit/search/media` | GET | Search Reddit image and video posts | 1 | standard | 120s |
| `/v1/reddit/subreddit` | GET | List Reddit subreddit posts | 1-5 (metered) | standard | 600s |
| `/v1/reddit/subreddit/details` | GET | Get Reddit subreddit details | 1 | standard | 900s |
| `/v1/reddit/subreddit/search` | GET | Search within a subreddit | 1-26 (metered) | standard | 120s |
| `/v1/reddit/subreddits/search` | GET | Find subreddits by topic | 1-26 (metered) | standard | 120s |

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
| `/v1/sephora/reviews` | GET | Get Sephora product reviews | 5-9 (metered) | advanced | 300s |
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
| `/v1/target/reviews` | GET | Get Target product reviews | 5-9 (metered) | advanced | 300s |
| `/v1/target/stores` | GET | Find Target stores near a location | 1 | standard | 1800s |

### Tavily (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tavily/crawl` | GET | Crawl a website with LLM-driven path selection | 1 | standard | 1800s |
| `/v1/tavily/extract` | GET | Extract clean content from one or more URLs | 1 | standard | 600s |
| `/v1/tavily/map` | GET | Map a website's sitegraph | 1 | standard | 1800s |
| `/v1/tavily/search` | GET | Tavily web search with optional LLM-generated answer | 1 | standard | 120s |

### Telegram (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/telegram/post` | GET | Get Telegram post | 1 | standard | 600s |
| `/v1/telegram/profile` | GET | Get Telegram channel profile | 1 | standard | 900s |
| `/v1/telegram/profile/posts` | GET | List Telegram channel posts | 1 | standard | 600s |
| `/v1/telegram/search` | GET | Search Telegram channels by keyword | 2-16 (metered) | custom | 120s |

### Threads (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/threads/post` | GET | Get Threads post details | 1 | standard | 600s |
| `/v1/threads/post/comments` | GET | Get comments on a Threads post | 1-10 (metered) | standard | 300s |
| `/v1/threads/profile` | GET | Get Threads user profile | 1 | standard | 900s |
| `/v1/threads/search` | GET | Search Threads posts | 1-34 (metered) | standard | 120s |
| `/v1/threads/search/users` | GET | Search Threads users | 1-13 (metered) | standard | 120s |
| `/v1/threads/user/posts` | GET | List Threads user posts | 1-165 (metered) | standard | 600s |

### TikTok (38)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tiktok/adlibrary/ad` | GET | Get a TikTok Ad Library ad | 5 | advanced | 1800s |
| `/v1/tiktok/adlibrary/search` | GET | Search the TikTok Ad Library | 5-17 (metered) | advanced | 120s |
| `/v1/tiktok/ads/top` | GET | Read TikTok's Creative Center Top Ads board: the best-performing ads in a market, ranked by CTR, impressions or engagement. Metered: 1 credit per ad returned, minimum 10 | 10-100 (metered) | standard | 1800s |
| `/v1/tiktok/collection/videos` | GET | List videos in a TikTok collection | 1-21 (metered) | standard | 600s |
| `/v1/tiktok/comment` | GET | Look up one TikTok comment by URL or id | 2-6 (metered) | custom | 300s |
| `/v1/tiktok/effect/videos` | GET | List TikTok videos made with an effect | 1-21 (metered) | standard | 600s |
| `/v1/tiktok/effects` | GET | Get TikTok effects by id | 1 | standard | 600s |
| `/v1/tiktok/hashtag` | GET | Get TikTok hashtag details | 1 | standard | 600s |
| `/v1/tiktok/hashtags/popular` | GET | Read TikTok's own trending-hashtag board for a market and time window: the overall board plus 15 industry boards. Metered: 2 credits per hashtag returned, minimum 6 | 6-96 (metered) | standard | 1800s |
| `/v1/tiktok/location/posts` | GET | List TikTok videos tagged at a place | 1-21 (metered) | standard | 600s |
| `/v1/tiktok/playlist/videos` | GET | List videos in a TikTok playlist | 1-21 (metered) | standard | 600s |
| `/v1/tiktok/post` | GET | Get TikTok post details | 1-3 (metered) | standard | 600s |
| `/v1/tiktok/post/comments` | GET | List TikTok post comments | 1-7 (metered) | standard | 300s |
| `/v1/tiktok/post/transcript` | GET | Get TikTok video transcript | 10 | premium | 2592000s |
| `/v1/tiktok/profile` | GET | Get TikTok user profile | 1-3 (metered) | standard | 900s |
| `/v1/tiktok/profile/full` | GET | TikTok profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/tiktok/profile/playlists` | GET | List a TikTok account's playlists | 1 | standard | 900s |
| `/v1/tiktok/profile/region` | GET | Get TikTok profile region | 1 | standard | 900s |
| `/v1/tiktok/profile/videos` | GET | List TikTok user videos | 1-25 (metered) | standard | 600s |
| `/v1/tiktok/search` | GET | Search TikTok videos by keyword | 1-62 (metered) | standard | 120s |
| `/v1/tiktok/search/hashtag` | GET | Search TikTok by hashtag | 1-25 (metered) | standard | 120s |
| `/v1/tiktok/search/mentions` | GET | Search TikTok videos that mention an account | 0-2 (metered) | standard | 120s |
| `/v1/tiktok/search/music` | GET | Search TikTok sounds | 1 | standard | 120s |
| `/v1/tiktok/search/suggestions` | GET | Get TikTok search suggestions | 1 | standard | 120s |
| `/v1/tiktok/search/top` | GET | TikTok top search results | 1-21 (metered) | standard | 120s |
| `/v1/tiktok/search/users` | GET | Search TikTok users | 1-100 (metered) | standard | 120s |
| `/v1/tiktok/similar` | GET | List similar TikTok accounts | 5 | advanced | 900s |
| `/v1/tiktok/song` | GET | Get TikTok song details | 1 | standard | 600s |
| `/v1/tiktok/song/videos` | GET | List TikTok videos using a song | 1-21 (metered) | standard | 600s |
| `/v1/tiktok/trending` | GET | Get TikTok trending feed | 5-25 (metered) | advanced | 120s |
| `/v1/tiktok/user/audience` | GET | Get TikTok user audience demographics | 5 | advanced | 1800s |
| `/v1/tiktok/user/followers` | GET | List TikTok user followers | 1 | standard | 900s |
| `/v1/tiktok/user/following` | GET | List TikTok user following | 1 | standard | 900s |
| `/v1/tiktok/user/liked` | GET | List the videos a TikTok account has liked | 1-21 (metered) | standard | 600s |
| `/v1/tiktok/user/live` | GET | Get TikTok user live stream | 1 | standard | 60s |
| `/v1/tiktok/video/comment/replies` | GET | List TikTok comment replies | 1-5 (metered) | standard | 300s |
| `/v1/tiktok/video/screen-text` | GET | Get TikTok video on-screen text | 5-10 (metered) | advanced | 600s |
| `/v1/tiktok/videos/popular` | GET | Read TikTok's own Top Videos board for the US, Japan, Vietnam, Thailand or Indonesia. Metered: 25 credits per board plus 1 per video returned | 26-45 (metered) | standard | 1800s |

### TikTok Shop (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tiktokshop/product` | GET | Get TikTok Shop product details | 1-4 (metered) | standard | 600s |
| `/v1/tiktokshop/product/reviews` | GET | List TikTok Shop product reviews | 1-5 (metered) | standard | 300s |
| `/v1/tiktokshop/products` | GET | List TikTok Shop products | 1 | standard | 600s |
| `/v1/tiktokshop/sales` | GET | TikTok Shop units sold and estimated sales per market | 0-8 (metered) | standard | 900s |
| `/v1/tiktokshop/search` | GET | Search TikTok Shop products | 1 | standard | 120s |
| `/v1/tiktokshop/user/showcase` | GET | List TikTok user showcase products | 1 | standard | 600s |

### Tripadvisor (16)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tripadvisor/attraction` | GET | Get a TripAdvisor attraction | 1 | standard | 900s |
| `/v1/tripadvisor/attraction/reviews` | GET | Get TripAdvisor reviews for an attraction | 1-5 (metered) | standard | 300s |
| `/v1/tripadvisor/attractions` | GET | Search TripAdvisor attractions and things to do | 1 | standard | 120s |
| `/v1/tripadvisor/autocomplete` | GET | Autocomplete TripAdvisor places | 1 | standard | 120s |
| `/v1/tripadvisor/cruise` | GET | Get a TripAdvisor cruise ship | 1 | standard | 900s |
| `/v1/tripadvisor/cruise/reviews` | GET | Get TripAdvisor reviews for a cruise ship | 1-5 (metered) | standard | 300s |
| `/v1/tripadvisor/cruises` | GET | Search TripAdvisor cruises | 1 | standard | 120s |
| `/v1/tripadvisor/experience-types` | GET | List TripAdvisor experience types for a destination | 1 | standard | 1800s |
| `/v1/tripadvisor/hotel` | GET | Get a TripAdvisor hotel | 1 | standard | 900s |
| `/v1/tripadvisor/hotels` | GET | Search TripAdvisor hotels | 1 | standard | 120s |
| `/v1/tripadvisor/place` | GET | Get a TripAdvisor place by URL | 1 | standard | 900s |
| `/v1/tripadvisor/restaurant` | GET | Get a TripAdvisor restaurant | 1 | standard | 900s |
| `/v1/tripadvisor/restaurant/reviews` | GET | Get TripAdvisor reviews for a restaurant | 1-5 (metered) | standard | 300s |
| `/v1/tripadvisor/restaurants` | GET | Search TripAdvisor restaurants | 1 | standard | 120s |
| `/v1/tripadvisor/reviews` | GET | Get TripAdvisor reviews for a place | 1-5 (metered) | standard | 300s |
| `/v1/tripadvisor/search` | GET | Search TripAdvisor businesses & places | 1 | standard | 120s |

### Trustpilot (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/trustpilot/business-search` | GET | Search Trustpilot businesses | 1 | standard | 120s |
| `/v1/trustpilot/reviews` | GET | Get Trustpilot reviews for a business | 5-9 (metered) | advanced | 300s |
| `/v1/trustpilot/reviews/history` | POST | Start a Trustpilot review history job | 6-10,005 (metered) | custom | none |

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

### Twitter/X (18)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/twitter/ai-search` | GET | AI-powered X (Twitter) search via xAI Grok | 5 | advanced | 1800s |
| `/v1/twitter/community` | GET | Get Twitter community details | 1 | standard | 900s |
| `/v1/twitter/community/tweets` | GET | List Twitter community tweets | 1 | standard | 600s |
| `/v1/twitter/profile` | GET | Get Twitter user profile | 1 | standard | 900s |
| `/v1/twitter/profile/about` | GET | Get a Twitter account's About details | 2 | custom | 900s |
| `/v1/twitter/profile/full` | GET | X (Twitter) profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/twitter/search/hashtag` | GET | Search X (Twitter) posts carrying a hashtag | 0-1 (metered) | standard | 120s |
| `/v1/twitter/search/mentions` | GET | Search X (Twitter) posts that mention an account | 0-1 (metered) | standard | 120s |
| `/v1/twitter/search/tweets` | GET | Search Twitter tweets | 1-9 (metered) | standard | 120s |
| `/v1/twitter/search/users` | GET | Search Twitter users | 1 | standard | 120s |
| `/v1/twitter/tweet` | GET | Get Twitter tweet details | 1 | standard | 600s |
| `/v1/twitter/tweet/replies` | GET | List Twitter tweet replies | 1-5 (metered) | standard | 300s |
| `/v1/twitter/tweet/retweeters` | GET | List Twitter tweet retweeters | 1 | standard | 900s |
| `/v1/twitter/tweet/transcript` | GET | Get Twitter video transcript | 10 | premium | 2592000s |
| `/v1/twitter/user/followers` | GET | List Twitter user followers | 1 | standard | 900s |
| `/v1/twitter/user/following` | GET | List Twitter user following | 1 | standard | 900s |
| `/v1/twitter/user/media` | GET | List Twitter user media tweets | 1 | standard | 600s |
| `/v1/twitter/user/tweets` | GET | List Twitter user tweets | 1-5 (metered) | standard | 600s |

### Universal Search (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/search/creators` | GET | Fused creator discovery across TikTok, Threads, and Instagram, ranked by relevance, followers, and verification. YouTube, X, and Facebook people are opt-in via sources=. | 10-24 (metered) | custom | 120s |
| `/v1/search/everywhere` | GET | Universal social search across 18 platforms | 20 | custom | 120s |
| `/v1/search/everywhere` | POST | Run a list of universal searches as one background run, or turn a search into a watch that repeats on a schedule and delivers only new rows. | 20 | custom | none |
| `/v1/search/forums` | GET | Fused forum search across Reddit, Hacker News, and Naver 지식iN/카페, with top comments inline on hero threads by default. | 10 | custom | 120s |
| `/v1/search/multi` | GET | One query, each platform's own search results, in one call at each platform's own price. | 0-30 (metered) | standard | 300s |
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

### Utility (13)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/utility/ai-detection` | GET | Check how likely a text was written by AI | 1 | standard | none |
| `/v1/utility/capabilities` | GET | List the parameters that work across endpoints | 0 | custom | 1800s |
| `/v1/utility/docs-search` | GET | Search the docs | 0 | custom | 1800s |
| `/v1/utility/endpoint` | GET | How to use any endpoint | 0 | custom | 1800s |
| `/v1/utility/endpoints` | GET | List every available endpoint | 0 | custom | 1800s |
| `/v1/utility/estimate` | GET | Quote the credit cost of a call or a plan | 0 | custom | none |
| `/v1/utility/explain-error` | GET | Explain a failed API response | 0 | custom | none |
| `/v1/utility/find` | GET | Find the endpoint for a task | 0 | custom | none |
| `/v1/utility/llms` | GET | AI-agent context payload | 0 | custom | 1800s |
| `/v1/utility/plan` | GET | Plan the calls for a job | 0 | custom | none |
| `/v1/utility/quickstart` | GET | Get started in one call | 0 | custom | 1800s |
| `/v1/utility/recipes` | GET | List task recipes with their cost | 0 | custom | 1800s |
| `/v1/utility/resolve` | GET | Identify a URL, handle or id | 0 | custom | 1800s |

### Walmart (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/walmart/category` | GET | Browse Walmart products in a category | 5 | advanced | 120s |
| `/v1/walmart/offers` | GET | Get every seller offering a Walmart product | 5 | advanced | 600s |
| `/v1/walmart/product` | GET | Get a Walmart product by id | 5 | advanced | 600s |
| `/v1/walmart/reviews` | GET | Get Walmart product reviews | 5-9 (metered) | advanced | 300s |
| `/v1/walmart/search` | GET | Search Walmart products by keyword | 5 | advanced | 120s |

### Wayfair (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/wayfair/product` | GET | Get a Wayfair product by SKU | 5 | advanced | 600s |
| `/v1/wayfair/reviews` | GET | Get Wayfair product reviews | 5-9 (metered) | advanced | 300s |
| `/v1/wayfair/search` | GET | Search Wayfair products | 5 | advanced | 120s |

### Web Scraping (22)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/web/agent` | POST | Start an async web agent job | 25 | custom | none |
| `/v1/web/batch-scrape` | POST | Start an async batch scrape | N credits for N submitted URLs (request-shaped) | custom | none |
| `/v1/web/crawl` | POST | Start an async web crawl | 1-10,000 (metered) | custom | none |
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
| `/v1/web/sessions` | POST | Create an interactive web session | 5-20 credits (request-shaped) | custom | none |
| `/v1/web/sessions/{session_id}` | GET | Get an interactive web session | 0 | custom | none |
| `/v1/web/sessions/{session_id}` | DELETE | Close an interactive web session | 0 | custom | none |
| `/v1/web/sessions/{session_id}/execute` | POST | Execute an interaction in a web session | 0 | custom | none |

### Weibo (8)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/weibo/comment/replies` | GET | List the replies to a Weibo comment | 5 | advanced | 300s |
| `/v1/weibo/post` | GET | Get a Weibo post | 1 | standard | 600s |
| `/v1/weibo/post/comments` | GET | List the comments on a Weibo post | 5 | advanced | 300s |
| `/v1/weibo/profile` | GET | Get a Weibo account | 1 | standard | 900s |
| `/v1/weibo/profile/posts` | GET | List a Weibo account's posts | 5 | advanced | 600s |
| `/v1/weibo/search` | GET | Search Weibo posts, back through time | 5 | advanced | 120s |
| `/v1/weibo/search/users` | GET | Search Weibo accounts | 5 | advanced | 120s |
| `/v1/weibo/trending` | GET | Get the Weibo hot-search list | 5 | advanced | 120s |

### Xiaohongshu (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/xiaohongshu/post` | GET | Get a Xiaohongshu note | 5 | advanced | 600s |
| `/v1/xiaohongshu/post/comments` | GET | Get Xiaohongshu note comments | 5-100 (metered) | advanced | 300s |
| `/v1/xiaohongshu/profile` | GET | Get a Xiaohongshu creator | 5 | advanced | 900s |
| `/v1/xiaohongshu/profile/posts` | GET | List a Xiaohongshu creator's notes | 5-100 (metered) | advanced | 900s |
| `/v1/xiaohongshu/search` | GET | Search Xiaohongshu notes | 5-100 (metered) | advanced | 120s |
| `/v1/xiaohongshu/trending` | GET | Get the Xiaohongshu hot search board | 5-100 (metered) | advanced | 120s |

### Yelp (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/yelp/business/info` | GET | Get a Yelp business by encid | 1 | standard | 900s |
| `/v1/yelp/business/reviews` | GET | Get Yelp reviews for a business | 5-9 (metered) | advanced | 300s |
| `/v1/yelp/search` | GET | Search Yelp businesses | 1 | standard | 120s |
| `/v1/yelp/search/full` | GET | Search Yelp businesses with full cards | 1 | standard | 120s |
| `/v1/yelp/search/suggestions` | GET | Get Yelp search suggestions | 1 | standard | 120s |

### YouTube (30)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/youtube/channel` | GET | Get YouTube channel info | 1 | standard | 900s |
| `/v1/youtube/channel/about` | GET | Get a YouTube channel's contact email and country. Try the 1-credit youtube/channel first: it already carries the email for some channels, and you are charged here only when an address is returned. A first read of an address behind the View email address button can take up to 5 minutes, so set your HTTP timeout to at least 300s; on a 503, retry after the Retry-After seconds | 25 | custom | 900s |
| `/v1/youtube/channel/community-posts` | GET | List a YouTube channel's community posts | 1 | standard | 600s |
| `/v1/youtube/channel/lives` | GET | List a YouTube channel's live streams | 1-7 (metered) | standard | 600s |
| `/v1/youtube/channel/playlists` | GET | List a YouTube channel's playlists | 1 | standard | 600s |
| `/v1/youtube/channel/shorts` | GET | List YouTube channel shorts | 1-2 (metered) | standard | 600s |
| `/v1/youtube/channel/videos` | GET | List YouTube channel videos | 1-2 (metered) | standard | 600s |
| `/v1/youtube/channels` | POST | Batch get YouTube channel details (up to 1000) | 5-100 (metered) | advanced | none |
| `/v1/youtube/community-post` | GET | Get YouTube community post | 1 | standard | 600s |
| `/v1/youtube/playlist` | GET | Get YouTube playlist | 1-11 (metered) | standard | 600s |
| `/v1/youtube/playlist/items` | GET | List the videos in a YouTube playlist | 1-11 (metered) | standard | 600s |
| `/v1/youtube/profile/full` | GET | YouTube profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/youtube/search` | GET | Search YouTube | 1-19 (metered) | standard | 120s |
| `/v1/youtube/search/advanced` | GET | Advanced YouTube video search | 1-11 (metered) | standard | 120s |
| `/v1/youtube/search/hashtag` | GET | Search YouTube by hashtag | 1-11 (metered) | standard | 120s |
| `/v1/youtube/search/suggestions` | GET | Get YouTube search suggestions | 1 | standard | 120s |
| `/v1/youtube/shorts/trending` | GET | Get trending YouTube shorts | 5-15 (metered) | advanced | 120s |
| `/v1/youtube/transcripts` | POST | Up to 100 YouTube video ids → one transcript per row, failed ids refunded. | 3-300 (metered) | custom | none |
| `/v1/youtube/video` | GET | Get YouTube video details | 1-3 (metered) | standard | 600s |
| `/v1/youtube/video/audio` | GET | Get a YouTube video's audio file streams | 5 | advanced | none |
| `/v1/youtube/video/comment/replies` | GET | List YouTube comment replies | 1-5 (metered) | standard | 300s |
| `/v1/youtube/video/comments` | GET | List YouTube video comments | 1-5 (metered) | standard | 300s |
| `/v1/youtube/video/files` | GET | Get a YouTube video's video file streams | 5 | advanced | none |
| `/v1/youtube/video/related` | GET | Get videos related to a YouTube video | 1-11 (metered) | standard | 600s |
| `/v1/youtube/video/sponsors` | GET | Detect sponsors of a YouTube video | 10 | premium | 1800s |
| `/v1/youtube/video/subtitles` | GET | Get a YouTube video's subtitle files | 1 | standard | none |
| `/v1/youtube/video/thumbnails` | GET | Get a YouTube video's thumbnail files | 1 | standard | none |
| `/v1/youtube/video/transcript` | GET | Get YouTube video transcript | 3 | custom | 2592000s |
| `/v1/youtube/videos` | POST | Batch get YouTube video details (up to 1000) | 5-100 (metered) | advanced | none |
| `/v1/youtube/videos/trending` | GET | Get trending YouTube videos | 1-6 (metered) | standard | 120s |
