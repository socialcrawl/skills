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
| `POST /v1/monitors` | Creation and management cost 0. Each run costs the exact underlying recipe estimate plus 1 orchestration credit. Multiply by the cadence for the recurring budget. | A failed recipe run is refunded; insufficient-balance runs are skipped. |
| `POST /v1/web/monitors` | Creation costs 0. Each check bills its booked upstream cost plus 1 orchestration credit. A 5-minute cadence means 288 checks per day. | Billing repeats until paused or deleted. |

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
