# Cost Gate

Read this for the full preflight (see the gate levels below). Endpoint headings are useful lookup labels, but a number in a heading can be a unit, floor, or upfront ceiling. Calculate the total from the exact query parameters or JSON body that will be sent.

**Prices changed.** Many endpoints that used to cost one flat price now hold more when an opt-in parameter is set: `label=`, `relevant_to=`, `include=`, `limit=`, `max_pages=`, `scan_pages=`, `country=`, `urls=`. A plain call (none of those) costs what it always did. Never reuse a remembered flat price for a call that carries one of them; recompute it with the recipes below. The full rule for every metered endpoint is in [pricing.md](pricing.md#metered-and-custom-priced-endpoints).

## Gate levels

Scale the gate to the call:

| Call | Gate |
| --- | --- |
| Flat price ≤ 5 credits, user asked for it | One line: `≈ N credits` |
| Metered, multi-page, batch, monitor/cohort, or > 25 credits | Full preflight via `estimate.py` / `utility/estimate` |
| Upfront hold (worst case) > 500 credits or over budget (the user's stated budget) | Ask before calling |

Cohort queries are the exception to the estimator: neither it nor `estimate.py` prices them, so compute the ceiling with the formula in [cohorts.md](cohorts.md#pricing).

Anything in between, or unsure of the price or params: quote first with the free `GET /v1/utility/estimate?id=<platform/resource>&<params>` (it ships with universal dry runs, so it is the capability check). Any reply except a 404 means a current server (a 5xx or network failure is no reply: retry the estimate): use its quote, and `dry_run=1` is then free on any endpoint before the real call (it validates, returns `data.estimate` and fetches nothing).

A 404 or `ENDPOINT_NOT_FOUND` from `/v1/utility/estimate` means an older server: do **not** send `dry_run=1` (an older server ignores it and bills a normal call, except the labelled dry run in [api-overview.md](api-overview.md#labels-relevance-and-quality)). Quote with `scripts/estimate.py`, which falls back offline to `assets/endpoints.json`, or with the endpoint's **Pricing** line and the recipes on this page. Last resort: a dry run (on a server without `/v1/utility/estimate`) that returned rows was billed; report that charge.

At every level, report `credits_used` after the call (see [After the response](#after-the-response)).

## Preflight format

For the full preflight, show this compact gate before execution:

```text
Cost check
Endpoint: METHOD /v1/platform/resource
Billing: unit or formula
Request: the values that drive price
Upfront: exact hold, or a clearly labelled maximum when settlement varies
Settlement: what is charged and what is refunded
Balance: current balance -> worst-case balance after this request
```

Do not call a paid endpoint until you can fill every line. If the exact total cannot be known before execution, quote the upfront hold or safe maximum and say why the settled charge may be lower. If the user already asked to execute that exact request, show the gate and continue; do not add a redundant confirmation, except the Ask level: always ask. Ask before widening the paid scope.

## General rules

- A fixed endpoint heading is the cost of one HTTP request.
- A normal paginated endpoint bills once per page. Estimate `ceil(items wanted / page size) x credits per page`, then stop when the user has enough data or `next_cursor` ends.
- **Hold, then settle.** The upfront hold is deducted before any upstream call. Metered endpoints settle it down to the work done in the same request; `credits_used` in the response is the final charge. The balance must cover the **hold**, not the expected charge.
- A cache hit (`X-Cache: HIT`, `cached: true`) and an idempotent replay (same `Idempotency-Key`) cost 0, but do not promise a hit before the response confirms it.
- Refunded in full: upstream errors (502), circuit-breaker rejections (503), internal errors (500), request-deadline timeouts (504), not-found (404 `RESOURCE_NOT_FOUND`) and an empty list (`200` with `items: []`). Rejected before billing, at 0: invalid params, bad handle or URL formats, typos in enum values, and rate limits (429).
- Prefer the cheapest endpoint that provides the required fields. Optional enrichment, extra pages, replies, transcripts, engines, countries, judgments and recurring schedules all widen cost.
- For a scheduled monitor, show both cost per run and estimated monthly cost. Management calls are free, but runs are not.
- For a `prism/discover` schedule, show `max_credits_per_run` x runs per month at its `every` (1h ≈ 720, 1d = 30, 7d ≈ 4) and suggest a `max_credits_per_month`; where `/v1/utility/estimate` exists, `dry_run: true` with `schedule` shows one run's estimate, free.
- A **walk** is not a request. Paging a list to completion multiplies the page cost by the page count; `coverage=full` on the Instagram follow lists reaches the hundreds. See [Multi-page walks](#multi-page-walks-coveragefull) and [Search walks](#search-walks-max_pages-and-seen).
- **A band is a range, not a quote.** A band that starts at 0 can settle at 0, because its pages bill only when they return rows: the mention and hashtag searches, `tiktokshop/sales`, `search/multi`, `prism/comment-leads` (and `prism/mentions` refunds a page with no verified row). The top of a wide band is a cap, not the expected charge: see `prism/discover`, `prism/profiles`, `prism/profile/comments` and `trustpilot/reviews/history` below.
- An `include=` token on a list endpoint is **row hydration**: it holds credits per row on top of the page and refunds to rows filled. Never quote the heading cost for a call that carries one. See [Row hydration](#row-hydration-include).

## Free calls (0 credits)

Use these freely to plan and check before spending:

- `GET /v1/credits/balance`, `GET /v1/credits/transactions` and `GET /v1/credits/usage` (credits and requests per API key per UTC day, up to 92 days).
- `dry_run=1` on any registry endpoint (GET query or POST body), only on servers where `/v1/utility/estimate` exists (see [Gate levels](#gate-levels)): validates the exact request and returns `data.estimate` without fetching. `dry_run=0` or `false` is a real call. The discover run and schedule routes take no `dry_run`.
- Every `/v1/utility/*` endpoint **except `utility/ai-detection`, which is 1 credit a text** (a text it cannot score is a 503, not charged). That includes `GET /v1/utility/plan?query=...` (the call plan for a job, with each step's credits), `GET /v1/utility/endpoint?id=platform/resource` (parameters, pricing and the measured `quality` block), `resolve`, `capabilities`, `explain-error`, `docs-search` and `recipes`.
- `GET /v1/prism/lookup`, `GET /v1/prism/jobs`, `GET /v1/prism/jobs/{job_id}`, `POST /v1/prism/discover/inputs`, every `prism/discover` run read and cancel (`GET /v1/prism/discover/runs[/{run_id}[/results.jsonl|/legs]]`, `DELETE /v1/prism/discover/runs/{run_id}`), every `/v1/prism/discover/schedules` route, and reading a review-history job (`GET /v1/trustpilot/reviews/history/{job_id}`). `POST .../runs/{run_id}/resume` and `.../more` are free calls, but the searches they start bill within the run's `max_credits`, so gate them like a paid call (`more` refuses free with `suggested_max_credits` when its estimate exceeds the cap).
- `GET /v1/events`, `POST /v1/events/consumers/{name}/ack`, and every `/v1/webhook-endpoints` route.
- Every cohort call except query submission (`POST /v1/cohorts/{cohortId}/queries`).
- `GET|DELETE /v1/web/jobs...`, web session management (`GET /v1/web/sessions`, `GET|DELETE /v1/web/sessions/{session_id}`, `POST /v1/web/sessions/{session_id}/execute`), and every management call on `/v1/monitors` and `/v1/web/monitors` (create, list, read, update, delete, run history). Creating a monitor is free; its runs are not.
- The default judgments on list rows (comment `sentiment`, `question`, `purchase_intent`, `complaint`; post `sponsored`, `intent`, `niche`; review `sentiment`, `issue`), relevance against your own search query, `contact_email=1`, YouTube exact dates, and `region=` on Instagram reel search.

## Unit to total

Every metered price is one of these units. Find the unit in the endpoint's pricing rule, then apply the recipe.

| Unit | Upfront hold | Settled charge |
|---|---|---|
| per page | `pages x page price` | pages actually served; a cached page is 0 |
| per row / post / comment / reply / ad / hashtag returned | `limit x rate` (default `limit` when absent), plus any floor | `max(floor, rows returned x rate)`; 0 rows is 0 unless a floor applies |
| per row filled (`include=` join) | `page + rows joinable x rate` | page + rows filled from a fresh lookup; cached and unfilled rows are free |
| per creator looked up (`include=creator`) | `page + 30 x 2` | page + 2 per distinct creator looked up |
| per started 25 rows judged (`label=`, `relevant_to=`) | `+ceil(endpoint row cap / 25)`, usually +4 | `ceil(fresh rows judged / 25)` |
| per URL / per profile / per item in a POST batch | sum of each item's rate | items that returned `ok` / `found` |
| per 50-id chunk (YouTube batch) | `5 x ceil(ids / 50)` | same; refunded only when nothing resolves |
| per platform (`search/multi`, `find-accounts`, `creator-card`, `handle-audit`) | sum over the platforms requested (see [Other metered formulas](#other-metered-formulas)) | `search/multi`: platforms whose page returned rows; `find-accounts`: searches that ran + platforms judged |
| per brand / repo / profile / prompt-probe (Prism composites) | `count x unit` | `ai-visibility`: probes completed; `adverse-screen`: profiles screened; others as the endpoint's rule says |
| per window (Threads search) / per search leg (news, expansion) | `windows + legs` | windows used + legs that returned posts |
| per browser-hour (web sessions) | `max(5, ceil(ttl_seconds / 3600 x 20))` | settled at close |
| per run (monitors) | the recipe's own price + 1 | failed run refunded, skipped run 0 |
| per answer (`youtube/channel/about`) | 25 | 25 when an email comes back, else 0 |

## Opt-in judgments (`label=`, `relevant_to=`)

The default judgments and relevance against your own query are free. A **paid** judgment holds extra credits and refunds down to what it judged:

- Paid comment labels: `label=spam`, `toxic` or `low_quality`.
- Paid post labels: `label=quality`, `label=ai_style`, `label=ai_written`, `label=injection`, `label=mention` (needs `brand=`), or `label=intent` with `offer=`. A post too short for `ai_written` (under 8 words), or one not scored within the page budget, is not billed.
- Paid review labels: `label=reports`, `incentivized` or `injection` (the first 100 reviews of a page are judged).
- Paid relevance: `relevance=score|filter` **with** `relevant_to=<your own topic>`.

```text
hold   = page price + ceil(row cap / 25) for each paid opt-in present (label, relevance)
settle = page price + ceil(rows newly judged / 25) for each opt-in
```

Each paid opt-in costs 1 credit per started 25 freshly judged rows: held as `ceil(row cap / 25)`, refunded to the rows actually judged. Relevance against the query itself is free. Several paid label presets in one `label=` share one hold. The row cap is 100 on every endpoint except `tiktok/search` (120, so +5), `linkedin/search/posts` (200, so +8) and `search/multi` (200, so +8). Rows already judged earlier are free, a cached page is free, and a page where nothing could be judged refunds the whole extra. `judgments=off` (or `label=none`) turns the free defaults off.

Worked examples:

- `GET /v1/amazon/reviews?asin=...&label=incentivized`: hold `5 + 4 = 9`. A page of 10 fresh reviews settles at `5 + ceil(10/25) = 6`. The same page again from cache: 0.
- `GET /v1/twitter/search/tweets?query=...&relevance=filter&relevant_to=...&label=mention&brand=acme`: hold `1 + 4 + 4 = 9`. A 20-row page, all fresh: `1 + 1 + 1 = 3`.
- `GET /v1/tiktok/search?query=...&limit=120&relevant_to=...&relevance=score`: hold `32 + 5 = 37` (see the `limit=` rule below). Add `label=mention&brand=...` and it is `32 + 5 + 5 = 42`, the endpoint's ceiling.
- `GET /v1/youtube/video/comments?...` with no `label` or `label=sentiment`: 1, unchanged.

## Request-shaped endpoints most likely to surprise

| Endpoint | Preflight calculation | Settlement |
|---|---|---|
| `POST /v1/prism/post-stats` | 1 to 5 credits per successful URL, at each URL's own rate: 2 per Instagram URL, 5 per LinkedIn URL, 1 on most other platforms. Sum the rates for every submitted URL, up to 100 URLs (range 1-500 credits). 100 LinkedIn URLs hold 500 credits; 100 Instagram URLs hold 200. | Only `ok` rows are charged. Failed, not-found, unsupported, and deferred rows cost 0 and are refunded. |
| `POST /v1/prism/profiles` | Sum each submitted platform's profile rate for up to 50 rows (1 credit on most platforms, 5 on LinkedIn): 50 plain rows hold at most 250. `include: "posts"` (up to 25 rows) adds each row's posts page (1, LinkedIn 5); `posts_limit` walks up to 10 pages per handle and holds them all. `include: "comments"` adds each selected post's comment pages at that platform's comment price (1 on most platforms, 5 on Instagram, LinkedIn and Reddit), held as `comments_top_posts` x the pages `comments_per_post` can take. The band's top (1-126,375) is reached only with the widest comment options; quote the hold for the options actually sent. | Only successful rows are charged; a posts or comment page is charged only when it came back with rows; the rest of the hold is refunded. |
| `GET /v1/prism/profile/comments` | Each page actually read at that endpoint's own price: the post list page (1) plus the comment pages of each post with a new comment (5 a page on Instagram, 1 on Facebook, YouTube, TikTok and X). Holds the most `posts` and `per_post` can take (251 for Instagram's defaults; `replies=true` adds up to 100 replies pages, 300 on Instagram). | With `since`, a post whose comments are all older costs 0, so a poll with no new comment costs only the post list page. `posts[].credits` shows each post's charge. |
| `GET` / `POST /v1/prism/discover` | Each platform search at that platform's own search price, billed only when it returns rows; judging against your keywords is free, against a different `context` 1 per started 15 rows, each label 1 per started 25 rows. `max_credits` caps the whole run: **required on POST (unless `schedule` carries `max_credits_per_run`), default 50 on GET**. Quote `max_credits` as the ceiling. | A GET expected to cost more than `max_credits` is refused free before anything is spent; a POST run pauses at `max_credits` and never overspends. A search still running when a GET answers bills after it (`data.run.credits.pending`). |
| `POST /v1/trustpilot/reviews/history` | Holds `depth + 5`: 1 credit per review returned plus 5 to open (band 6-10,005). | Unused hold refunded when the job settles; reading pages at `GET /v1/trustpilot/reviews/history/{job_id}` is free. |
| `POST /v1/prism/jobs` | The batch endpoint's own per-row price, for 1 to 5,000 items. The 202 holds the whole job's worst case (5,000 LinkedIn profiles hold 25,000). | Every row that is not `ok` is refunded when the job completes. Reading the job is free. |
| `POST /v1/prism/comment-lookup` | Per row: TikTok 2 credits or 6 with `deep_scan`; Instagram 5 or 15 with `deep_scan`. Up to 25 rows. Sum rows, then cap the batch hold at 100 credits. | Only `found` rows are charged, never more than the hold; not-found, error, unsupported, and deferred rows are refunded. |
| `POST /v1/youtube/transcripts` | 3 credits x submitted video IDs, up to 100 IDs. The request range is 3 to 300 credits. | Only successful transcript rows are charged; failed rows are refunded. |
| `POST /v1/youtube/videos` and `POST /v1/youtube/channels` | `5 x ceil(ID count / 50)` credits, up to 1,000 IDs and 100 credits. | A successful upstream chunk is billed as a chunk; unresolved IDs inside a successful chunk do not create per-row refunds. |
| `GET /v1/prism/ai-visibility` | `2 x prompts x runs x engines`, plus 5 when `include=web_baseline`. Defaults are 8 runs and 2 engines. One prompt with defaults is `2 x 1 x 8 x 2 = 32 credits`, not 2. `preset=quick` is 5 runs and at most 5 prompts, `standard` 8 and 10, `deep` 10 and 20. Maximum: `2 x 20 x 20 x 2 + 5 = 1,605`. | The upfront ceiling is refunded down to probes actually completed; failed probes do not bill. |
| `GET /v1/prism/comments` | Instagram is a flat 5 credits. Other platforms hold `ceil(max / 50) x 3` (x1 with `replies=false`), clamped to 2..200; the default `max=1000` with replies holds 60. | Settles at 1 credit per comment page scanned, floor 2. |
| `GET /v1/youtube/channel/about` | 25 credits. Try `GET /v1/youtube/channel` (1 credit) first: it already carries `public_email` for some channels. | Charged only when an email comes back. No published address, a missing channel (404), or a `503` with `Retry-After: 300` all cost 0. |
| `GET /v1/linkedin/profile/posts` | 5 credits with no `limit` or `limit` up to 50. Above 50: `limit x 2` (100 holds 200). | Above 50 it settles to `max(5, posts returned x 2)`: 60 posts is 120. |
| `GET /v1/xiaohongshu/search`, `profile/posts`, `post/comments`, `trending` | `limit x 5` (default 10 holds 50; maximum 20 holds 100). | 5 per row returned; 3 rows is 15. |
| `GET /v1/instagram/search/reels` with `include=creator` or `country=` | `1 + 30 x 2 = 61` per page (plus 4 each for paid `label=` / `relevant_to=`). `region=` alone stays 1. | 1 + 2 per distinct creator looked up. A creator looked up in the last 15 minutes is free, a creator not found is refunded. With `country=`, creators are charged whether their reel is kept or dropped; a page emptied only by failed lookups costs 0. Measured: 27 reels by 20 creators = 41. |
| `GET /v1/search/multi` | 0 held for the platforms. Each platform is billed as its own direct call: 1 a page on TikTok, Instagram, YouTube, Reddit, Threads, X and Facebook, 2 on Telegram, 5 on LinkedIn. Default set (TikTok, Instagram, YouTube, Reddit, Threads) is at most 5; all nine is 14, plus up to 4 Threads expansion searches. `expand=context` runs up to 3 more planned searches per platform, each billed as its own page, so multiply by `1 + expand_queries`. Paid judgments hold +8 each. | A platform that found nothing, failed or was served from cache costs 0. `data.sources.<platform>.credits` itemises it. |
| `GET /v1/search/everywhere` | Flat 20. | No results anywhere costs 0. With rows but fewer than half the called sources succeeding, 10 is refunded. |
| `GET /v1/tiktok/search` with `limit=` | Rows rounded up to 30, 60, 90 or 120; hold `ceil(rows / 4) + 2` (30 holds 10, 120 holds 32). Without `limit` the page is 1. | Settles to `ceil(rows returned / 4) + 2`. |
| `GET /v1/tiktok/search/users` with `country=` | `5 x limit` (default 8 holds 40, maximum 20 holds 100). | 5 per in-country row returned; a miss is 0. |
| `GET /v1/linkedin/search/posts` with `limit=` | `ceil(limit / 5)` (200 holds 40). Without `limit` the page is 5. | `ceil(posts returned / 5)`. |
| `GET /v1/linkedin/profile/all` with `urls=` | 5 x distinct profiles, up to 10 (50). | 5 per profile that resolved; duplicates and dead handles are free. |
| `POST /v1/web/batch-scrape` | `N` credits for `N` submitted URLs. There is no registry-side URL-count cap, so count the actual body. | The submit holds N; unused or failed work is refunded when the async job settles. |
| `POST /v1/web/crawl` | 1 credit per requested page. The upfront hold is `limit`, default 10, maximum 10,000. | Settles to pages actually crawled. |
| `POST /v1/web/sessions` | `max(5, ceil(ttl_seconds / 3600 x 20))`. The default 60 seconds holds 5 credits; 3,600 seconds holds 20. | The TTL-shaped hold settles when the session closes. |
| `POST /v1/web/agent` | Holds 25. Does not honour `Idempotency-Key`: a resend starts and bills a second run. | Settles to the credits the agent run reports; when it reports none, the 25 is kept. |
| `GET /v1/search/news` | Base 2 plus up to 1 credit per country/angle leg returning articles. Hold: `2 + min(5 x countries, max_legs, 12)`, so 2 to 14 credits. Adding the `bing` engine adds `ceil(min(depth, 20) / 5)` per leg (2 at the default depth); both engines can reach 62. | Empty or failed legs cost 0; bing settles at 1 per 5 articles. |
| `GET /v1/tiktok/hashtags/popular` | 2 credits per hashtag returned, minimum 6. One board is 6. `industry=all` is sixteen boards and holds **96**. | Settles to hashtags actually returned, typically 88-92. An empty board costs 0. |
| `GET /v1/tiktok/videos/popular` | 25 credits per board plus 1 per video returned. The default `limit=20` holds **45**. | Settles to videos actually returned; an empty board costs 0. |
| `POST /v1/monitors` | Creation and management cost 0. Each run costs the exact underlying recipe estimate plus 1 orchestration credit. Multiply by the cadence for the recurring budget. Exception: on `search/multi`, `tiktokshop/sales` and the hashtag / mention searches, each run's platform calls bill themselves as the key that created the monitor, so `estimated_cost_per_run` shows only the 1; quote the recipe's own per-call price on top ([monitors.md](monitors.md#billing)). | A failed recipe run is refunded; insufficient-balance runs are skipped and cost 0. |
| `POST /v1/cohorts/{cohortId}/queries` | Holds the full ceiling: per queried member, bluesky / threads / twitch 1, linkedin 5 (fixed), twitter / tiktok / kwai / truth-social 1 x `max_pages_per_identity`, instagram / youtube 2 x `max_pages_per_identity`. Refused free (400) when `max_credits` is below it. Neither `/v1/utility/estimate` nor a cohort `dry_run=1` computes it, so work it out with [cohorts.md](cohorts.md#pricing). | Charges successful pages only; dead handles, 404s, upstream errors and cancelled work cost 0; `reserved - actual` is refunded once at the terminal state. |
| `POST /v1/web/monitors` | Creation costs 0. Each finished check bills `max(1, the credits that check used) + 1`, so at least 2, failed checks included (`credits_booked` on the monitor is always 1 and is not a quote). A 5-minute cadence means 288 checks per day. | Billing repeats until paused or deleted. A check that finds too few credits is skipped at 0. |

## Search walks (`max_pages` and `seen`)

Twelve search endpoints walk pages in one call: `tiktok/search`, `tiktok/search/top`, `tiktok/search/hashtag`, `instagram/search/reels`, `instagram/search/hashtag`, `youtube/search`, `youtube/search/advanced`, `youtube/search/hashtag`, `twitter/search/tweets`, `threads/search`, `reddit/search`, `facebook/search/posts`.

- `max_pages=N` (1 to 5) bills each page walked as one ordinary call to that endpoint, with every opt-in on it (`include=`, `label=`, `relevant_to=`). Worst case: `N x one page's hold`. A cached page is 0. The walk can stop early (`data.walk.stopped`: `end`, `max_pages`, `time_budget`, `page_error`), and unwalked pages are never charged.
- Row filters (`min_views`, `max_age_days`, `country`) do not lower a page's own price; they only stop a join from looking up rows that will be dropped.
- `seen=<id>` removes rows already received under that id in the last 24 hours and prices the page at `ceil(page credits x new rows / rows on the page)`. A page of only repeats is 0. Join credits (`include=`) are charged only for new rows and are never discounted.
- On `instagram/search/reels`, a walk looks each creator up once: `max_pages=2&country=ES` measured 2 pages, 45 reels kept, 78 credits.

Example: `GET /v1/instagram/search/hashtag?hashtag=...&max_pages=3&seen=wk1` holds up to `3 x 5 = 15`. A page of 20 rows with 12 already seen costs `ceil(5 x 8 / 20) = 2`.

## Comment scans (`scan_pages`, `sort`)

`instagram/post/comments` and `tiktok/post/comments` can scan up to 3 pages and sort the merged rows.

```text
hold   = page price x scan_pages (+4 for a paid label)
settle = page price x pages that added new comments
```

- Instagram: 5 a page. A call without `scan_pages` is one page at 5; `scan_pages=3` holds 15. A second page that only repeats the first is not billed (measured: 5 credits, not 10).
- TikTok: 1 a page. `sort=` alone scans one page (1 credit); `sort=recent&scan_pages=3` holds 3 (measured: 149 comments, 3 credits).

## Multi-page walks (`coverage=full`)

Every other rule on this page prices ONE request. This one prices a **walk**, and it is the largest spend in the API: a full follower list runs into the **hundreds of credits**.

`GET /v1/instagram/followers` and `GET /v1/instagram/following` plain walks (5 credits a page) usually end within a few rows of the profile's count. On large verified accounts Instagram caps every route at about 50 rows, so the walk ends there whatever you pay. `data.total` carries the profile's own count on every page: compare it with the rows you collected and switch to `coverage=full` only when a plain walk falls short.

`coverage=full` walks a merged list instead, until the rows reach the count or no read has more (it cannot pass the ~50-row cap on large verified accounts either). It holds **10 credits a page instead of 5**, and settles a page down to 5 when one read covered it in full.

**Budget the walk, not the page.** A page carries about 50 accounts. Quote the worst case:

```text
credits <= ceil(data.total / 50) x 10
```

Measured 13/09/2026: a following list of 2,652 took 54 pages = **540 credits**; a follower list of 2,360 took 59 pages = **590 credits** (later pages of a follower walk add fewer new accounts, so round up).

**Quote that total to the user and get agreement before starting a full walk.** The endpoint heading reads `5-10 credits` — that is one page, not the job. Do not start a walk on a large account on the strength of the heading.

Rules that make a walk fail cheaply rather than expensively:

- `handle` is required with `coverage=full`. `user_id` alone is a free 400 (`coverage_full_requires_handle`).
- Keep the mode constant for the whole walk. A cursor from one mode sent to the other is a free 400 (`cursor_coverage_mismatch`).
- Retry a `503` with the **same** cursor; the page it returns is the page that walk would have served.
- A private account is a refunded `404` with `details.reason: account_private`, in about a second.
- A failed page is refunded. Pages take about 8 seconds each, occasionally up to 45, so a full walk is minutes of wall-clock — say so when you quote the credits.

For most lists the plain walk at 5 credits a page is enough (half the full-coverage worst case above); offer `coverage=full` only for the shortfall.

## Row hydration (`include=`)

The largest class of cost surprise. These list endpoints accept an opt-in `include=` token that joins every row to a sibling endpoint in the same call. **The heading cost is the plain-call cost; a hydrated call can be many times it.**

Preflight: `hold = base + (credits per row x rows joinable)`.
Settlement: refunded to rows actually **filled**. Unfilled rows are refunded; rows served from the sibling's own cache are free; `credits_used` is the real charge and `data.hydration` itemises rows, cache hits, credits held and kept.

Bound the spend with the row cap param where the endpoint offers one — on those endpoints `limit` caps rows and credits together.

<!-- BEGIN:GENERATED:HYDRATION_TABLE (auto-generated by generate-skills.ts from registry hydrate blocks) -->
| Endpoint | Token | Plain | Per row | Default hold | Hydrated ceiling | Row cap |
|---|---|---|---|---|---|---|
| `GET /v1/facebook/adlibrary/company/ads` | `include=audience` | 5 | 1 | 35 | **35** | up to 30 rows; `limit` is not a row cap |
| `GET /v1/facebook/events` | `include=details` | 1 | 1 | 13 | **13** | up to 12 rows; `limit` is not a row cap |
| `GET /v1/facebook/profile/events` | `include=details` | 1 | 1 | 9 | **9** | up to 8 rows; `limit` is not a row cap |
| `GET /v1/facebook/profile/photos` | `include=details` | 1 | 1 | 9 | **9** | up to 8 rows; `limit` is not a row cap |
| `GET /v1/facebook/profile/posts` | `include=engagement` | 1 | 1 | 4 | **4** | up to 3 rows; `limit` is not a row cap |
| `GET /v1/facebook/search/groups` | `include=details` | 1 | 1 | 11 | **11** | up to 10 rows; `limit` is not a row cap |
| `GET /v1/facebook/search/pages` | `include=details` | 1 | 1 | 11 | **11** | up to 10 rows; `limit` is not a row cap |
| `GET /v1/facebook/search/videos` | `include=details` | 1 | 1 | 8 | **8** | up to 7 rows; `limit` is not a row cap |
| `GET /v1/instagram/location/posts` | `include=country` | 5 | 1 | 68 | **68** | up to 63 rows; `limit` is not a row cap |
| `GET /v1/instagram/post/stats` | `include=saves` | 5 | 4 | 9 | **9** | up to 1 rows; `limit` is not a row cap |
| `GET /v1/instagram/profile/posts` | `include=audio` | 1 | 1 | 13 | **13** | up to 12 rows; `limit` is not a row cap |
| `GET /v1/instagram/profile/posts` | `include=tags` | 1 | 1 | 13 | **13** | up to 12 rows; `limit` is not a row cap |
| `GET /v1/instagram/profile/reels` | `include=audio` | 1 | 1 | 13 | **13** | up to 12 rows; `limit` is not a row cap |
| `GET /v1/instagram/search/hashtag` | `include=country` | 5 | 1 | 35 | **35** | up to 30 rows; `limit` is not a row cap |
| `GET /v1/instagram/search/popular` | `include=engagement` | 1 | 1 | 13 | **13** | `limit` caps rows + credits (max 12) |
| `GET /v1/instagram/search/profiles` | `include=about` | 1 | 2 | 17 | **25** | `limit` caps rows + credits (max 12); **defaults to top 8** |
| `GET /v1/instagram/search/reels` | `include=creator` | 1 | 2 | 61 | **61** | up to 30 rows; `limit` is not a row cap |
| `GET /v1/instagram/search/reels` | `include=country` | 1 | 1 | 31 | **31** | up to 30 rows; `limit` is not a row cap |
| `GET /v1/instagram/similar` | `include=profile` | 5 | 1 | 25 | **85** | `limit` caps rows + credits (max 80); **defaults to top 20** |
| `GET /v1/linkedin/company/people` | `include=profile` | 10 | 4 | 50 | **50** | `limit` caps rows + credits (max 10) |
| `GET /v1/linkedin/post/reactions` | `include=profile` | 10 | 4 | 50 | **50** | `limit` caps rows + credits (max 10) |
| `GET /v1/linkedin/search/people` | `include=profile` | 10 | 4 | 50 | **50** | `limit` caps rows + credits (max 10) |
| `GET /v1/pinterest/board` | `include=engagement` | 1 | 1 | 16 | **16** | `limit` caps rows + credits (max 15) |
| `GET /v1/pinterest/search` | `include=engagement` | 1 | 1 | 26 | **26** | `limit` caps rows + credits (max 25) |
| `GET /v1/reddit/subreddits/search` | `include=details` | 1 | 1 | 26 | **26** | `limit` caps rows + credits (max 25) |
| `GET /v1/telegram/search` | `include=details` | 2 | 1 | 12 | **12** | `limit` caps rows + credits (max 10) |
| `GET /v1/threads/search` | `include=engagement` | 1 | 1 | 21 | **21** | up to 20 rows; `limit` is not a row cap |
| `GET /v1/threads/search/users` | `include=profile` | 1 | 1 | 13 | **13** | `limit` caps rows + credits (max 12) |
| `GET /v1/threads/user/posts` | `include=engagement` | 1 | 1 | 16 | **16** | up to 15 rows; `limit` is not a row cap |
| `GET /v1/tiktok/adlibrary/search` | `include=ad` | 5 | 1 | 17 | **17** | `limit` caps rows + credits (max 12) |
| `GET /v1/tiktok/search/users` | `include=profile` | 1 | 1 | 31 | **31** | `limit` caps rows + credits (max 30) |
| `GET /v1/tiktokshop/product` | `include=details` | 1 | 3 | 4 | **4** | up to 1 rows; `limit` is not a row cap |
| `GET /v1/youtube/channel/lives` | `include=engagement` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/channel/lives` | `include=channel` | 1 | 1 | 2 | **2** | up to 1 rows; `limit` is not a row cap |
| `GET /v1/youtube/channel/shorts` | `include=channel` | 1 | 1 | 2 | **2** | up to 1 rows; `limit` is not a row cap |
| `GET /v1/youtube/channel/videos` | `include=channel` | 1 | 1 | 2 | **2** | up to 1 rows; `limit` is not a row cap |
| `GET /v1/youtube/playlist` | `include=engagement` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/playlist` | `include=channel` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/playlist/items` | `include=engagement` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/playlist/items` | `include=channel` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/search` | `include=engagement` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/search` | `include=channel` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/search/advanced` | `include=channel` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/search/hashtag` | `include=engagement` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/search/hashtag` | `include=channel` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/shorts/trending` | `include=channel` | 5 | 1 per id, max 5 per 50 ids | 15 | **15** | up to 100 rows; `limit` is not a row cap |
| `GET /v1/youtube/video/related` | `include=engagement` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/video/related` | `include=channel` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |
| `GET /v1/youtube/videos/trending` | `include=channel` | 1 | 1 per id, max 5 per 50 ids | 6 | **6** | up to 50 rows; `limit` is not a row cap |

Several tokens on one call add up: the hold is the plain cost plus each requested token's ceiling. The default hold is what a call with the token and no row cap holds; the ceiling is the whole page joined.
<!-- END:GENERATED:HYDRATION_TABLE -->

Three shapes to watch:

- **`limit` is not a row cap** on `threads/user/posts`, `threads/search`, `instagram/search/reels`, `facebook/search/groups` and the four Facebook feed endpoints — there the endpoint always holds its full window. Budget the ceiling.
- **Default row caps are below the page** on `instagram/similar` (top 20, hold 25; `limit=80` for 85) and `instagram/search/profiles` (top 8, hold 17; `limit=12` for 25).
- **YouTube is batch-priced**, never per row: 1 credit per distinct id capped at 5 per 50 ids. A 50-row page adds 5 per join. `shorts/trending` is the one list over 50 rows, so it is two chunks (10). Exact publish dates on YouTube lists are a free default join.

`include_details=true` on `threads/search/users` is a legacy alias of `include=profile` at the same price. Prefer the token.

## Other metered formulas

The complete current list is in [pricing.md](pricing.md#metered-and-custom-priced-endpoints). Read the endpoint's platform reference as well.

| Family | Rule |
|---|---|
| Per row returned | `douyin/search`, `profile/posts`, `search/users`: `limit x 5` (default 10, max 25). `douyin/post/comments`: `limit x 1`, floor 2 (default 20, max 100). `douyin/comment/replies`: `limit x 5` (default 10, max 50). `linkedin/profile/posts/archive`: `limit x 5` (default 20 holds 100, max 100 holds 500). `reddit/profile/comments`: `limit x 2` (default 25 holds 50, max 100). `tiktok/ads/top`: `limit x 1`, floor 10 (default 20). All settle to rows returned. |
| Threads | `threads/search`: 1 per window, `ceil(limit / 15)` windows (max 100 = 7), plus up to 4 expansion searches on a page-1 multi-word query (billed only when they return posts; `expand=false` or a cursor holds none). `threads/user/posts`: 1 up to `limit=15`, above it `limit x 3` (max 50 = 150), settled per post. `threads/post/comments`: 1 up to `limit=25`, above it `ceil(limit / 5)` (max 50 = 10), settled at 1 per 5 replies returned. |
| Page composites | `instagram/profile/reels/full`, `profile/posts/full`: `5 x ceil(limit / 12)` (max 25). `facebook/profile/reels/full`: `5 x ceil(limit / 10)` (max 25). No `limit` is one page at 5. Unused pages refunded. `reddit/omni-search`: hold `max(5, 1 + threads)` (default 8 threads holds 9), settles `max(5, 1 + threads expanded)`. |
| Single-comment lookups | `tiktok/comment` 2 (`deep_scan=true` 6); `instagram/comment` 5 (`deep_scan=true` 15). Not found is a refunded 404. |
| Hydrated search | `reddit/search` and `reddit/subreddit/search` with `include_body=true`: +25 held, 1 per body actually returned. `youtube/search/advanced` with `includeExtras=true`: flat +5. `search/creators`: 10, `brief=` +2 (refunded if not every creator was judged); `country=` adds the searches it runs at their own price (1 TikTok search page, 1 web search page, 1 per Instagram profile looked up, at most 10), so at most +12 and a 10-24 range; the 10 are refunded when no creator is found. |
| Prism by count | `share-of-voice`: `brands x 40` with the default social leg, `brands x 20` web-only, up to 5 brands. `org-radar`: `1 + 5 x repos` (default 5 = 26, max 10 = 51). `creator-card`: 5 for up to 4 platforms, +1 each beyond (max 8). `handle-audit`: same shape (max 8). `app-reviews`: 10 one store, 15 both (a bare `query` is both). `adverse-screen`: 25 + 10 per further profile (max 75); unscreened profiles refunded, nothing screened keeps 5. `find-accounts`: per platform searched (Instagram, TikTok, X 1, LinkedIn 10) + 1 per platform judged; person default 6, company 17. `mentions`: X 1, Reddit 2 (comments + posts), Instagram 5, web 1; default holds 3, max 9; a leg with no verified row refunded. `audience-language`: `1 + posts x 1` (Instagram `x 5`), TikTok +6, up to 5 posts (Instagram max 26). `comment-leads`: 1 per search page, 1 per comment page, 1 per started 25 comments labelled; default holds 37. |
| Prism flat | `video-intel` 5, `include=transcript` 15. `crisis-radar` 15, `confirm=true` 45. `creator-vet` 50, `include=cross_platform` 75. `korea-gap` 40 by default, 15 with an `include` that omits `social`. `trend-board` 30 (refunded only when the feed, hashtag board and Google Trending Now all fail). `earliness` 25. `brief-check` 15. `format-lift` 4. The last four are provisional prices. |
| Flat with refund rules | `pinterest/trends` 10, whatever the depth; filters that match nothing are a 404 at 0. `instagram/media/screen-text` 5, refunded when nothing could be read. `tiktok/similar` 5, an empty list refunded. `search/forums` 10. `{platform}/profile/full` 5. |
| Web | `web/scrape` 1; 5 with `proxy=auto`, `proxy=enhanced`, `pdf_parse=true`, `json_schema` or `json_prompt`. `web/search`: `max(2, ceil(limit / 10) x 2)`, `include_content=true` + `limit` (max 120). `web/extract` 5. `web/map` 1. |

Do not call `GET /v1/prism/investigate`: it holds `budget` (default 40, max 200) and was blocked in production with an empty trail at the last check.

## Insufficient credits (402)

The hold, not the expected charge, must fit the balance. When it does not, the call returns `402 INSUFFICIENT_CREDITS` before any upstream call and charges 0. The envelope carries `details.credits_required` (the hold), `details.reason: "balance_too_low"`, `details.retry_will_succeed: false` and a `top_up_url`, and the message says retrying will not succeed until the balance changes. A per-key credit limit returns `402 KEY_BUDGET_EXCEEDED` with `reason: "key_budget_reached"` instead. A key limit is a lifetime cap on that one key's net spend (refunds give it back; it never resets on its own), and scheduled monitor runs are not counted against it. That 402's `credits_remaining` is the account balance, so a healthy number there means the key cap, not the balance, stopped the call.

- **Do not retry a 402 unchanged.** It fails the same way, and a 402 carries no `Retry-After`: waiting does not help, only a top-up, a smaller request or a raised key limit does. `key_name`, `key_prefix` and `account_email_masked`, when present, say which key and account ran out.
- Shrink the hold with the recipes above (a smaller `limit`, fewer IDs, URLs or `brands`, no `include=`, no paid `label=`, `max_pages=1`) and offer that cheaper shape, or a top-up, to the user. On every metered endpoint the 402 itself says so: `details.lower_cost_options` gives each param that lowers the hold with the value to send and the hold it gives (on `threads/search?limit=100`: `limit` at 15 holds 5, `expand=false` holds 7), `details.credits_required_cheapest` the hold with all of them, and on a ceiling `details.credits_typical` what a call like it is usually charged.
- An account still in the signup check shows a hint that its 100 welcome credits are waiting behind card verification.

## After the response

Report the values returned by the API rather than the estimate:

```text
Charged: {credits_used} credits
Remaining: {credits_remaining} credits
Cache: hit|miss
```

`credits_used` is already net of every refund in that request. Where present, quote the itemised blocks: `data.hydration` (joins), `data.walk` (pages walked, repeats, why it stopped), `data.scan` (comment scans), `data.sources.<platform>.credits` (`search/multi`). On a free cache hit `credits_remaining` is `null`; read `GET /v1/credits/balance` if the user needs the number.

For async work, the submit response may show the hold. Poll the documented job endpoint and report the settled charge when it becomes available.
