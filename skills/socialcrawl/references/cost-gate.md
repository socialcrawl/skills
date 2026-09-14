# Cost Gate

Read this before every paid request. Endpoint headings are useful lookup labels, but a number in a heading can be a unit, floor, or upfront ceiling. Calculate the total from the exact query parameters or JSON body that will be sent.

## Preflight format

Show this compact gate before execution:

```text
Cost check
Endpoint: METHOD /v1/platform/resource
Billing: unit or formula
Request: the values that drive price
Upfront: exact hold, or a clearly labelled maximum when settlement varies
Settlement: what is charged and what is refunded
Balance: current balance -> worst-case balance after this request
```

Do not call a paid endpoint until you can fill every line. If the exact total cannot be known before execution, quote the upfront hold or safe maximum and say why the settled charge may be lower. If the user already asked to execute that exact request, show the gate and continue; do not add a redundant confirmation. Ask before widening the paid scope.

## General rules

- A fixed endpoint heading is the cost of one HTTP request.
- A normal paginated endpoint bills once per page. Estimate `ceil(items wanted / page size) x credits per page`, then stop when the user has enough data or `next_cursor` ends.
- A cache hit and an idempotent replay cost 0, but do not promise a hit before the response confirms it.
- Metered and async endpoints may hold the maximum first and refund unused work. `credits_used` after settlement is the final charge.
- Prefer the cheapest endpoint that provides the required fields. Optional enrichment, extra pages, replies, transcripts, engines, countries, and recurring schedules all widen cost.
- For a scheduled monitor, show both cost per run and estimated monthly cost. Management calls are free, but runs are not.
- A **walk** is not a request. Paging a list to completion multiplies the page cost by the page count; `coverage=full` on the Instagram follow lists reaches the hundreds. See [Multi-page walks](#multi-page-walks-coveragefull).
- An `include=` token on a list endpoint is **row hydration**: it holds credits per row on top of the page and refunds to rows filled. Never quote the heading cost for a call that carries one. See [Row hydration](#row-hydration-include).

## Request-shaped endpoints most likely to surprise

| Endpoint | Preflight calculation | Settlement |
|---|---|---|
| `POST /v1/prism/post-stats` | 1 to 5 credits per successful URL. Most supported platforms reserve 1; Instagram and LinkedIn reserve 5. Sum the routed rate for every submitted URL. A batch of 100 Instagram or LinkedIn URLs can hold 500 credits, not 1. | Only `ok` rows are charged. Failed, not-found, unsupported, and deferred rows cost 0 and are refunded. |
| `POST /v1/prism/profiles` | Sum each submitted platform's profile rate for up to 50 rows. Most are 1 credit; LinkedIn is 5. The request range is 1 to 250 credits. | Only successful rows are charged; all other row statuses are refunded. |
| `POST /v1/prism/comment-lookup` | Per row: TikTok 2 credits or 6 with `deep_scan`; Instagram 5 or 15 with `deep_scan`. Sum rows, then cap the batch hold at 100 credits. | Only `found` rows are charged; not-found, error, unsupported, and deferred rows are refunded. |
| `POST /v1/youtube/transcripts` | 3 credits x submitted video IDs, up to 100 IDs. The request range is 3 to 300 credits. | Only successful transcript rows are charged; failed rows are refunded. |
| `POST /v1/youtube/videos` and `POST /v1/youtube/channels` | `5 x ceil(ID count / 50)` credits, up to 1,000 IDs and 100 credits. | A successful upstream chunk is billed as a chunk; unresolved IDs inside a successful chunk do not create per-row refunds. |
| `GET /v1/prism/ai-visibility` | `2 x prompts x runs x engines`, plus 5 when `include=web_baseline`. Defaults are 8 runs and 2 engines. One prompt with defaults is `2 x 1 x 8 x 2 = 32 credits`, not 2. Maximum: `2 x 20 x 20 x 2 + 5 = 1,605`. | The upfront ceiling is refunded down to probes actually completed; failed probes do not bill. |
| `GET /v1/prism/comments` | Instagram is a flat 5 credits. Other supported platforms meter successful comment pages at 1 credit per page, with a 2-credit floor and a 200-credit cap; `max` and `replies` determine the upfront ceiling. | Unused page budget is refunded. |
| `POST /v1/web/batch-scrape` | `N` credits for `N` submitted URLs. There is no registry-side URL-count cap, so count the actual body. | The submit holds N; unused or failed work is refunded when the async job settles. |
| `POST /v1/web/crawl` | 1 credit per requested page. The upfront hold is `limit`, default 10, maximum 10,000. | Settles to pages actually crawled. |
| `POST /v1/web/sessions` | `max(5, ceil(ttl_seconds / 3600 x 20))`. The default 60 seconds holds 5 credits; 3,600 seconds holds 20. | The TTL-shaped hold settles when the session closes. |
| `GET /v1/search/news` | Base 2 plus up to 1 credit per country/angle leg returning articles. Hold: `2 + min(5 x countries, max_legs, 12)`, so 2 to 14 credits. | Empty or failed legs cost 0. |
| `GET /v1/tiktok/hashtags/popular` | 2 credits per hashtag returned, minimum 6. One board is 6. `industry=all` is sixteen boards and holds **96**. | Settles to hashtags actually returned, typically 88-92. An empty board costs 0. |
| `GET /v1/tiktok/videos/popular` | 25 credits per board plus 1 per video returned. The default `limit=20` holds **45**. | Settles to videos actually returned; an empty board costs 0. |
| `POST /v1/monitors` | Creation and management cost 0. Each run costs the exact underlying recipe estimate plus 1 orchestration credit. Multiply by the cadence for the recurring budget. | A failed recipe run is refunded; insufficient-balance runs are skipped. |
| `POST /v1/web/monitors` | Creation costs 0. Each check bills its booked upstream cost plus 1 orchestration credit. A 5-minute cadence means 288 checks per day. | Billing repeats until paused or deleted. |

## Multi-page walks (`coverage=full`)

Every other rule on this page prices ONE request. This one prices a **walk**, and it is the largest spend in the API: a full follower list runs into the **hundreds of credits**.

`GET /v1/instagram/followers` and `GET /v1/instagram/following` serve each plain walk as a partial sample — the walk ends with `has_more: false` at roughly two thirds of the profile's real count. `data.total` carries the true count on every page, so the shortfall is visible from page one.

`coverage=full` walks a merged list instead and reaches the count. It costs **10 credits a page instead of 5**.

**Budget the walk, not the page.** A page carries about 50 accounts:

```text
credits ≈ ceil(data.total / 50) x 10
```

Measured 13/09/2026: a following list of 2,652 took 54 pages = **540 credits**; a follower list of 2,360 took 59 pages = **590 credits** (later pages of a follower walk add fewer new accounts, so round up).

**Quote that total to the user and get agreement before starting a full walk.** The endpoint heading reads `5-10 credits` — that is one page, not the job. Do not start a walk on a large account on the strength of the heading.

Rules that make a walk fail cheaply rather than expensively:

- `handle` is required with `coverage=full`. `user_id` alone is a free 400 (`coverage_full_requires_handle`).
- Keep the mode constant for the whole walk. A cursor from one mode sent to the other is a free 400 (`cursor_coverage_mismatch`).
- Retry a `503` with the **same** cursor; the page it returns is the page that walk would have served.
- A private account is a refunded `404` with `details.reason: account_private`, in about a second.
- A failed page is refunded. Pages take about 8 seconds each, occasionally up to 45, so a full walk is minutes of wall-clock — say so when you quote the credits.

If the user only needs a sample, the plain walk at 5 credits a page is unchanged and its response is byte-identical.

## Row hydration (`include=`)

The largest class of cost surprise. 28 list endpoints across 8 platforms accept an opt-in `include=` token that joins every row to a sibling endpoint in the same call. **The heading cost is the plain-call cost; a hydrated call can be many times it.**

Preflight: `hold = base + (credits per row x rows joinable)`.
Settlement: refunded to rows actually **filled**. Unfilled rows are refunded; rows served from the sibling's own cache are free; `credits_used` is the real charge and `data.hydration` itemises rows, cache hits, credits held and kept.

Bound the spend with the row cap param where the lane offers one — on those lanes `limit` caps rows and credits together.

| Endpoint | Token | Plain | Hydrated ceiling | Row cap |
|---|---|---|---|---|
| `GET /v1/facebook/events` | `details` | 1 | **13** | fixed 12-row window; `limit` is not a row cap |
| `GET /v1/facebook/profile/events` | `details` | 1 | **9** | fixed 8-row window; `limit` is not a row cap |
| `GET /v1/facebook/profile/photos` | `details` | 1 | **9** | fixed 8-row window; `limit` is not a row cap |
| `GET /v1/facebook/profile/posts` | `engagement` | 1 | **4** | fixed 3-row window; `limit` is not a row cap |
| `GET /v1/instagram/post/stats` | `saves` | 5 | **9** | single-object join |
| `GET /v1/instagram/search/popular` | `engagement` | 1 | **13** | `limit` caps rows + credits (max 12) |
| `GET /v1/instagram/similar` | `profile` | 5 | **25 default, 85 max** | `limit` caps rows + credits (max 80); **defaults to top 20** |
| `GET /v1/linkedin/company/people` | `profile` | 10 | **50** | `limit` caps rows + credits (max 10) |
| `GET /v1/linkedin/post/reactions` | `profile` | 10 | **50** | `limit` caps rows + credits (max 10) |
| `GET /v1/linkedin/search/people` | `profile` | 10 | **50** | `limit` caps rows + credits (max 10) |
| `GET /v1/pinterest/board` | `engagement` | 1 | **16** | `limit` caps rows + credits (max 15) |
| `GET /v1/pinterest/search` | `engagement` | 1 | **26** | `limit` caps rows + credits (max 25) |
| `GET /v1/reddit/subreddits/search` | `details` | 1 | **26** | `limit` caps rows + credits (max 25) |
| `GET /v1/threads/search` | `engagement` | 1 | **21** | fixed 20-row window; `limit` is not a row cap |
| `GET /v1/threads/search/users` | `profile` | 1 | **13** | `limit` caps rows + credits (max 12) |
| `GET /v1/threads/user/posts` | `engagement` | 1 | **16** | fixed 15-row window; `limit` is not a row cap |
| `GET /v1/tiktok/adlibrary/search` | `ad` | 5 | **17** | `limit` caps rows + credits (max 12) |
| `GET /v1/tiktok/search/users` | `profile` | 1 | **31** | `limit` caps rows + credits (max 30) |
| `GET /v1/youtube/channel/lives` | `engagement` | 1 | **6** | batch: 5 credits per 50 ids (50-row page) |
| `GET /v1/youtube/channel/shorts` | `channel` | 1 | **2** | one shared channel lookup for the whole page |
| `GET /v1/youtube/channel/videos` | `channel` | 1 | **2** | one shared channel lookup for the whole page |
| `GET /v1/youtube/playlist` | `engagement` | 1 | **6** | batch: 5 credits per 50 ids (50-row page) |
| `GET /v1/youtube/playlist/items` | `engagement` | 1 | **6** | batch: 5 credits per 50 ids (50-row page) |
| `GET /v1/youtube/search` | `engagement` | 1 | **6** | batch: 5 credits per 50 ids (50-row page) |
| `GET /v1/youtube/search/advanced` | `channel` | 1 | **6** | batch: 5 credits per 50 ids (50-row page) |
| `GET /v1/youtube/search/hashtag` | `engagement` | 1 | **6** | batch: 5 credits per 50 ids (50-row page) |
| `GET /v1/youtube/shorts/trending` | `channel` | 5 | **15** | batch: 5 credits per 50 ids (100-row page) |
| `GET /v1/youtube/videos/trending` | `channel` | 1 | **6** | batch: 5 credits per 50 ids (50-row page) |

Three shapes to watch:

- **`limit` is not a row cap** on `threads/user/posts`, `threads/search`, and the four Facebook lanes — there it selects the source or the walker target, so those lanes always hold their full window. Budget the ceiling.
- **`instagram/similar` defaults to its top 20 rows** with `include=profile` (hold 25). The full 80-row roster costs up to 85 and needs `limit=80` explicitly.
- **YouTube is batch-priced**, never per row: 1 credit per distinct id capped at 5 per 50 ids. A 50-row page adds 5. `shorts/trending` is the one list over 50 rows, so it is two chunks (10).

`include_details=true` on `threads/search/users` is a legacy alias of `include=profile` at the same price. Prefer the token.

## Other metered formulas

The complete current list is in [pricing.md](pricing.md#metered-and-custom-priced-endpoints). Read the endpoint's platform reference as well. Important parameter-driven families include `prism/share-of-voice` (brand count and included sources), `prism/org-radar` (repository count), `prism/creator-card` and `prism/handle-audit` (platform count), `prism/video-intel` (optional transcript), app-review store count, full-profile page walks, Threads search windows, web search result count/content hydration, and deep single-comment scans.

## After the response

Report the values returned by the API rather than the estimate:

```text
Charged: {credits_used} credits
Remaining: {credits_remaining} credits
Cache: hit|miss
```

For async work, the submit response may show the hold. Poll the documented job endpoint and report the settled charge when it becomes available.
