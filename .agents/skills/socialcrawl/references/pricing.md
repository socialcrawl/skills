# SocialCrawl Pricing Reference

Complete per-endpoint credit pricing for all 381 active endpoints across 48 platforms. Auto-derived from the live endpoint registry - the same registry the router uses to charge your balance.

## How billing works

- Every API call deducts credits from your balance **before** the upstream call, atomically. The response reports `credits_used` and `credits_remaining` (also in the `X-Credits-Used` / `X-Credits-Remaining` headers).
- **Cache hits are free** - a response served from cache costs 0 credits (`X-Cache: HIT`, `cached: true`). Each endpoint's TTL is in the tables below; a repeat call inside the TTL window is free.
- **Automatic refunds** - credits are refunded on upstream errors (502), circuit-breaker rejections (503), internal errors (500), request-deadline timeouts (504), and empty-upstream results (404 `RESOURCE_NOT_FOUND` / an empty `items` list). You only pay for calls that return real data.
- **Free before billing** - invalid params, bad handle/URL formats, and rate-limit rejections (429) are rejected at the boundary and never deduct.
- **Idempotent replays are free** - resending with the same `Idempotency-Key` returns the stored response at 0 credits.
- **Metered endpoints** deduct an upfront ceiling and auto-refund down to the actual work done; the response `credits_used` is the real charge. Every metered endpoint is listed with its full pricing rule under [Metered and custom-priced endpoints](#metered-and-custom-priced-endpoints).
- **Multi-source endpoints charge once** no matter how many upstream providers are tried before one succeeds.
- `GET /v1/credits/balance` and `GET /v1/credits/transactions` are always 0 credits, as is every `/v1/utility/*` endpoint.

## Credit tiers

Most endpoints sit on a simple 1 / 5 / 10 ladder. A set of bundle and fan-out endpoints use a **custom** override that bypasses the ladder (flat or metered per recipe).

| Tier | Cost per call | Endpoints | Typical endpoints |
|------|--------------|-----------|-------------------|
| standard | 1 credit | 175 | Profiles, posts, comments, search, reference data |
| advanced | 5 credits | 102 | Ad libraries, trending, audience analytics, app/product/business/place reviews, retail catalogs, LinkedIn social graph + jobs |
| premium | 10 credits | 17 | Video transcripts, LinkedIn people/job search + reactions, app-listings search |
| **custom (flat/metered)** | **varies (0-50)** | 87 | Prism composites, `{platform}/profile/full`, `search/everywhere` (20), `search/forums` (10), `search/news` (2-14 metered), `naver/brief` (10), the free `/v1/utility/*` endpoints, web scrape/crawl/agent/sessions |

Counted by underlying tier (custom endpoints folded into their base tier), the split is **218 standard · 134 advanced · 29 premium = 381**. Exact per-endpoint costs are in the tables below.

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
| `GET /v1/prism/lookup` | Universal URL dispatcher: any social/commerce URL → the right detail endpoint's unified response. |
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

28 endpoints do not charge a flat ladder price. Each one holds an upfront ceiling and refunds the unused portion, so the response `credits_used` is always the real charge. Quote the RANGE to a user before calling, then report the actual charge afterwards.

| Endpoint | Range | How it is charged |
|----------|-------|-------------------|
| `GET /v1/facebook/profile/reels/full` | 5-25 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/instagram/comment` | 5-15 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/instagram/profile/posts/full` | 5-25 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/instagram/profile/reels/full` | 5-25 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/ai-visibility` | 2-1605 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/app-reviews` | 10-15 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/comments` | 2-200 credits | 1 credit per comment page scanned, except on Instagram, where a post URL is a flat 5 credits whatever `max` and `replies` you pass |
| `GET /v1/prism/creator-card` | 5-8 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/creator-vet` | 50-75 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/crisis-radar` | 15-45 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/handle-audit` | 5-8 credits | 5 credits for any selection of up to 4 supported platforms; +1 credit per selected platform beyond 4 |
| `GET /v1/prism/korea-gap` | 15-40 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/org-radar` | 6-51 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/share-of-voice` | 20-200 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/prism/video-intel` | 5-15 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/reddit/omni-search` | 5-9 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/search/news` | 2-14 credits | 2 credits + 1 credit per country/angle leg that returns at least one article. The upfront hold is 2 + min(5 x countries, max_legs, 12) credits (maximum 14) and settles down to the actual charge; empty or failed legs bill 0. |
| `GET /v1/threads/search` | 1-7 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/tiktok/comment` | 2-6 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `POST /v1/web/batch-scrape` | 1 credit | 1 credit per URL submitted, held up front and refunded down to the URLs actually scraped when the job settles |
| `POST /v1/web/crawl` | 1-10000 credits | 1 credit per page crawled. Submitting holds `limit` credits up front (default limit 10, max 10,000) and the unused portion is refunded when the job settles |
| `GET /v1/web/extract` | 5 credits | Priced through the metered pricer, but the charge does not vary with your params. |
| `GET /v1/web/scrape` | 1-5 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/web/search` | 2-120 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `POST /v1/web/sessions` | 5 credits | 20 credits per browser-hour, minimum 5. The hold is taken from `ttl_seconds` when the session is created (60s default = 5, the 3,600s maximum = 20) and settled when it closes |
| `POST /v1/youtube/channels` | 5-100 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `GET /v1/youtube/search/advanced` | 1-6 credits | An upfront ceiling is held and refunded down to the work actually done. |
| `POST /v1/youtube/videos` | 5-100 credits | An upfront ceiling is held and refunded down to the work actually done. |

## Per-endpoint pricing

`Credits` is the charge for one live (non-cached) successful call. `Cache` is how long a successful response is reused - a repeat call inside that window costs 0.

### Amazon (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/amazon/product` | GET | Get an Amazon product by ASIN | 5 | advanced | 600s |
| `/v1/amazon/product-search` | GET | Search Amazon products by keyword | 1 | standard | 120s |
| `/v1/amazon/reviews` | GET | Get Amazon product reviews | 5 | advanced | 300s |
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

### eBay (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/ebay/product` | GET | Get an eBay listing by item id | 5 | advanced | 600s |
| `/v1/ebay/search` | GET | Search eBay listings | 5 | advanced | 120s |

### Facebook (23)

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

### Google Finance (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google_finance/markets` | GET | Get a markets overview (indices + movers) | 1 | standard | 60s |
| `/v1/google_finance/quote` | GET | Get a financial instrument quote | 5 | advanced | 60s |
| `/v1/google_finance/ticker-search` | GET | Search financial instruments by name | 1 | standard | 120s |

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

### Google Shopping (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google_shopping/product` | GET | Get Google Shopping product detail | 1 | standard | 600s |
| `/v1/google_shopping/product-search` | GET | Search Google Shopping products | 5 | advanced | 120s |
| `/v1/google_shopping/reviews` | GET | Get Google Shopping product reviews | 1 | standard | 300s |
| `/v1/google_shopping/sellers` | GET | Get Google Shopping sellers for a product | 1 | standard | 600s |

### Google Trends (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/google_trends/explore` | GET | Get Google Trends interest over time | 5 | advanced | 120s |
| `/v1/google_trends/rising` | GET | Get related + rising Google Trends queries | 5 | advanced | 120s |

### Hacker News (4)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/hackernews/profile` | GET | Get a Hacker News user profile | 1 | standard | 900s |
| `/v1/hackernews/search` | GET | Search Hacker News | 1 | standard | 120s |
| `/v1/hackernews/story` | GET | Get a Hacker News story | 1 | standard | 600s |
| `/v1/hackernews/story/comments` | GET | Get comments on a Hacker News story | 1 | standard | 300s |

### Home Depot (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/home_depot/product` | GET | Get a Home Depot product by item id or URL | 5 | advanced | 600s |
| `/v1/home_depot/reviews` | GET | Get Home Depot product reviews | 5 | advanced | 300s |

### Instagram (33)

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
| `/v1/instagram/post/comments` | GET | List Instagram post comments | 5 | advanced | 300s |
| `/v1/instagram/post/likers` | GET | List Instagram post likers | 5 | advanced | 900s |
| `/v1/instagram/post/stats` | GET | Get Instagram post stats including the share count | 5 | advanced | 600s |
| `/v1/instagram/profile` | GET | Get Instagram user profile | 1 | standard | 900s |
| `/v1/instagram/profile/full` | GET | Instagram profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/instagram/profile/posts` | GET | List Instagram user posts | 1 | standard | 600s |
| `/v1/instagram/profile/posts/full` | GET | Instagram posts with views, likes, comments, and per-post share counts where available, in one call. | 5-25 (metered) | advanced | 600s |
| `/v1/instagram/profile/reels` | GET | List Instagram user reels | 1 | standard | 600s |
| `/v1/instagram/profile/reels/full` | GET | Instagram reels with views, likes, comments, and per-reel share counts where available, in one call. | 5-25 (metered) | advanced | 600s |
| `/v1/instagram/reels/trending` | GET | Get trending Instagram reels | 5 | advanced | 120s |
| `/v1/instagram/search/hashtag` | GET | Search Instagram posts by hashtag | 5 | advanced | 120s |
| `/v1/instagram/search/location` | GET | Search Instagram locations | 5 | advanced | 120s |
| `/v1/instagram/search/music` | GET | Search Instagram music | 5 | advanced | 21600s |
| `/v1/instagram/search/profiles` | GET | Search Instagram profiles by keyword | 1 | standard | 120s |
| `/v1/instagram/search/reels` | GET | Search Instagram reels | 1 | standard | 120s |
| `/v1/instagram/similar` | GET | List similar Instagram accounts | 5 | advanced | 900s |
| `/v1/instagram/stories` | GET | List an Instagram user's active stories | 5 | advanced | 600s |
| `/v1/instagram/story/download` | GET | Download a single Instagram story | 5 | advanced | 600s |
| `/v1/instagram/tagged` | GET | List posts an Instagram user is tagged in | 5 | advanced | 600s |
| `/v1/instagram/user/embed` | GET | Get Instagram user embed HTML | 1 | standard | 900s |
| `/v1/instagram/username-suggestions` | GET | Get Instagram username suggestions | 5 | advanced | 120s |

### Kick (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/kick/clip` | GET | Get Kick clip details | 1 | standard | 600s |

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

### LinkedIn (44)

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
| `/v1/polymarket/research` | GET | Polymarket prediction markets — multi-query research | 5 | advanced | 120s |

### Prism (33)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/prism/ai-visibility` | GET | AI Share-of-Voice / GEO monitoring: prompt set x reruns to per-brand appearance-% per AI engine plus a cited-domain ranking. | 2-1605 (metered) | custom | 120s |
| `/v1/prism/answers` | GET | Multi-engine AI consensus: one question → Perplexity + Grok + Tavily answers verbatim, merged citations, and an agreement matrix. | 15 | custom | 120s |
| `/v1/prism/app-reviews` | GET | Cross-store app review intelligence (Google Play + App Store) — translated, clustered, sentiment-scored. | 10-15 (metered) | custom | 300s |
| `/v1/prism/apps-lookup` | GET | One app across Google Play + the App Store — resolved, title-matched, and compared into a cross-store rating + listing report. | 30 | custom | 1800s |
| `/v1/prism/audience-overlap` | GET | How much two TikTok creators' commenter audiences overlap — Jaccard, shared-fan count, and a confidence label. | 20 | custom | 1800s |
| `/v1/prism/audience-questions` | GET | The real questions a topic's audience asks — harvested from Reddit + YouTube threads and clustered by intent (who/what/why/how/vs). | 30 | custom | 1800s |
| `/v1/prism/brand-mentions` | GET | Brand mention volume time-series, sentiment split, top sources, and recent mentions for one keyword. | 50 | custom | 1800s |
| `/v1/prism/campaign` | GET | Campaign tracker: pre/during/post volume lift, cross-platform engagement, and ranked top amplifiers for a hashtag or phrase. | 35 | custom | 1800s |
| `/v1/prism/comment-lookup` | POST | Re-check up to 25 known comments in one call — per-item results, failed items refunded. | 2 | custom | none |
| `/v1/prism/comments` | GET | Every comment on a post, replies nested, server-paginated to completion. | 2-200 (metered) | standard | 300s |
| `/v1/prism/creator-card` | GET | One handle, unified author cards across TikTok, Instagram, YouTube, X (and more). | 5-8 (metered) | custom | 900s |
| `/v1/prism/creator-vet` | GET | Vet a creator before partnering — engagement quality, commenter authenticity, posting cadence, and controversy signals, optionally across platforms. | 50-75 (metered) | custom | 1800s |
| `/v1/prism/crisis-postmortem` | GET | Crisis post-mortem: a who-said-what-first timeline across web, Reddit, Hacker News, and social, with an origin, peak, propagation sequence, and a grounded narrative. | 35 | custom | 1800s |
| `/v1/prism/crisis-radar` | GET | Stateless crisis breach check: a z-score on daily mention volume and negative share, with on-breach confirmation and a severity grade. | 15-45 (metered) | custom | 1800s |
| `/v1/prism/demand-signals` | GET | Consumer-demand nowcast: app-review velocity, web mention slope, Reddit velocity, and commerce review levels, fused into a published demand index. | 30 | custom | 300s |
| `/v1/prism/devtool-pulse` | GET | Developer-brand health: a devtool's repo dossier + Hacker News reaction + Reddit chatter + dev-blog echo, in one call. | 20 | custom | 1800s |
| `/v1/prism/earned-media` | GET | A brand's earned-media footprint — news + tech-press + fresh-web clips, deduped and ranked, with an outlet-coverage rollup. | 25 | custom | 1800s |
| `/v1/prism/employer-brand` | GET | A company's employer brand — what people say about working there across Reddit, the web, YouTube, Naver, and the company's own LinkedIn voice. | 30 | custom | 1800s |
| `/v1/prism/handle-audit` | GET | Should you pull this handle? One call scores a handle across platforms, ranks the best ones, and projects the data volume + credit cost to pull it. | 5-8 (metered) | custom | 1800s |
| `/v1/prism/korea-gap` | GET | What the world is talking about that Korea isn't (and vice versa) — the global vs Korean (Naver) conversation gap for a brand/topic. | 15-40 (metered) | custom | 1800s |
| `/v1/prism/launch-echo` | GET | How a launch landed — the Hacker News reaction (top threads + comments), the dev-blog echo, and an optional repo dossier. | 20 | custom | 1800s |
| `/v1/prism/leads` | GET | Ranked feed of public conversations where people seek alternatives to or are switching from a competitor. | 50 | custom | 1800s |
| `/v1/prism/lookup` | GET | Universal URL dispatcher: any social/commerce URL → the right detail endpoint's unified response. | 0 | custom | 600s |
| `/v1/prism/org-radar` | GET | A GitHub org's footprint — its top repos each expanded into a full dossier (releases, issue load, top request/complaint), rolled up. | 6-51 (metered) | custom | 1800s |
| `/v1/prism/post-stats` | POST | Up to 100 mixed-platform post URLs → current engagement per URL, failed URLs refunded. | 1 | custom | none |
| `/v1/prism/product-reviews` | GET | A product's reviews across Amazon + Google Shopping + Trustpilot, folded into a cross-marketplace rating + themed pros/cons report. | 30 | custom | 1800s |
| `/v1/prism/profiles` | POST | Up to 50 (platform, handle) pairs → one canonical Author per row, failed handles refunded. | 1 | custom | none |
| `/v1/prism/reputation` | GET | A brand's cross-source reputation — Trustpilot + app stores + Google Business + web sentiment, blended into one weighted score with themed pros/cons. | 30 | custom | 1800s |
| `/v1/prism/review-integrity` | GET | Cross-source review integrity verdict (statistical, deterministic). | 30 | custom | 1800s |
| `/v1/prism/share-of-voice` | GET | Engagement-weighted Share of Voice across 2-5 brands, with web+social split, emotion overlay, and ESOV. | 20-200 (metered) | custom | 1800s |
| `/v1/prism/truthsocial-pulse` | GET | A Truth Social handle's pulse — profile, recent posts, per-post detail drill, and the news echo, in one call. | 20 | custom | 1800s |
| `/v1/prism/video-intel` | GET | One video URL → detail + stats + transcript + top comments + commenter sample, across YouTube/TikTok/Rumble/Instagram. | 5-15 (metered) | custom | 600s |
| `/v1/prism/voice` | GET | One person's public posts across X, Threads, Bluesky, and Truth Social, time-merged. | 5 | custom | 600s |

### Reddit (8)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/reddit/omni-search` | GET | Reddit VoC sweep: one keyword → threads across all of Reddit with subreddit attribution and top comments inline. | 5-9 (metered) | standard | 120s |
| `/v1/reddit/post` | GET | Get a Reddit post | 1 | standard | 600s |
| `/v1/reddit/post/comments` | GET | List Reddit post comments | 5 | advanced | 300s |
| `/v1/reddit/post/transcript` | GET | Get a Reddit video post transcript | 10 | premium | 2592000s |
| `/v1/reddit/search` | GET | Search Reddit posts | 1 | standard | 120s |
| `/v1/reddit/subreddit` | GET | List Reddit subreddit posts | 1 | standard | 600s |
| `/v1/reddit/subreddit/details` | GET | Get Reddit subreddit details | 1 | standard | 900s |
| `/v1/reddit/subreddit/search` | GET | Search within a subreddit | 1 | standard | 120s |

### Rumble (5)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/rumble/channel/videos` | GET | List videos for a Rumble channel | 1 | standard | 600s |
| `/v1/rumble/search` | GET | Search Rumble videos | 1 | standard | 120s |
| `/v1/rumble/video` | GET | Get a Rumble video | 1 | standard | 600s |
| `/v1/rumble/video/comments` | GET | List top-level comments on a Rumble video | 1 | standard | 300s |
| `/v1/rumble/video/transcript` | GET | Get a Rumble video transcript | 10 | premium | 2592000s |

### Snapchat (1)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/snapchat/profile` | GET | Get Snapchat user profile | 1 | standard | 900s |

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

### Threads (6)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/threads/post` | GET | Get Threads post details | 1 | standard | 600s |
| `/v1/threads/post/comments` | GET | Get comments on a Threads post | 1 | standard | 300s |
| `/v1/threads/profile` | GET | Get Threads user profile | 1 | standard | 900s |
| `/v1/threads/search` | GET | Search Threads posts | 1-7 (metered) | standard | 120s |
| `/v1/threads/search/users` | GET | Search Threads users | 1 | standard | 120s |
| `/v1/threads/user/posts` | GET | List Threads user posts | 1 | standard | 600s |

### TikTok (21)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/tiktok/comment` | GET | Look up one TikTok comment by URL or id | 2-6 (metered) | custom | 300s |
| `/v1/tiktok/post` | GET | Get TikTok post details | 1 | standard | 600s |
| `/v1/tiktok/post/comments` | GET | List TikTok post comments | 1 | standard | 300s |
| `/v1/tiktok/post/transcript` | GET | Get TikTok video transcript | 10 | premium | 2592000s |
| `/v1/tiktok/profile` | GET | Get TikTok user profile | 1 | standard | 900s |
| `/v1/tiktok/profile/full` | GET | TikTok profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/tiktok/profile/region` | GET | Get TikTok profile region | 1 | standard | 900s |
| `/v1/tiktok/profile/videos` | GET | List TikTok user videos | 1 | standard | 600s |
| `/v1/tiktok/search` | GET | Search TikTok videos by keyword | 1 | standard | 120s |
| `/v1/tiktok/search/hashtag` | GET | Search TikTok by hashtag | 1 | standard | 120s |
| `/v1/tiktok/search/top` | GET | TikTok top search results | 1 | standard | 120s |
| `/v1/tiktok/search/users` | GET | Search TikTok users | 1 | standard | 120s |
| `/v1/tiktok/song` | GET | Get TikTok song details | 1 | standard | 600s |
| `/v1/tiktok/song/videos` | GET | List TikTok videos using a song | 1 | standard | 600s |
| `/v1/tiktok/trending` | GET | Get TikTok trending feed | 5 | advanced | 120s |
| `/v1/tiktok/user/audience` | GET | Get TikTok user audience demographics | 5 | advanced | 1800s |
| `/v1/tiktok/user/followers` | GET | List TikTok user followers | 1 | standard | 900s |
| `/v1/tiktok/user/following` | GET | List TikTok user following | 1 | standard | 900s |
| `/v1/tiktok/user/live` | GET | Get TikTok user live stream | 1 | standard | 1800s |
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

### Tripadvisor (2)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
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

### Twitter/X (8)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/twitter/ai-search` | GET | AI-powered X (Twitter) search via xAI Grok | 5 | advanced | 120s |
| `/v1/twitter/community` | GET | Get Twitter community details | 1 | standard | 900s |
| `/v1/twitter/community/tweets` | GET | List Twitter community tweets | 1 | standard | 600s |
| `/v1/twitter/profile` | GET | Get Twitter user profile | 1 | standard | 900s |
| `/v1/twitter/profile/full` | GET | X (Twitter) profile, recent posts, and computed analytics in one call. | 5 | custom | 900s |
| `/v1/twitter/tweet` | GET | Get Twitter tweet details | 1 | standard | 600s |
| `/v1/twitter/tweet/transcript` | GET | Get Twitter video transcript | 10 | premium | 2592000s |
| `/v1/twitter/user/tweets` | GET | List Twitter user tweets | 1 | standard | 600s |

### Universal Search (3)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/search/everywhere` | GET | Universal social search across 14 platforms | 20 | custom | 120s |
| `/v1/search/forums` | GET | Fused forum search across Reddit, Hacker News, and Naver 지식iN/카페 — with top comments inline on hero threads by default. | 10 | custom | 120s |
| `/v1/search/news` | GET | Planned multi-country news search: one query, localized and fanned out across Google News editions in a single call. | 2-14 (metered) | standard | 300s |

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

### YouTube (28)

| Endpoint | Method | What it returns | Credits | Tier | Cache |
|----------|--------|-----------------|---------|------|-------|
| `/v1/youtube/channel` | GET | Get YouTube channel info | 1 | standard | 900s |
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
| `/v1/youtube/transcripts` | POST | Up to 100 YouTube video ids → one transcript per row, failed ids refunded. | 3 | custom | none |
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
