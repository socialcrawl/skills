# Cohorts

Ask one keyword question of a list of people you already have. Upload up to 10,000 public social identities, submit a keyword query over a date window, and read back which of those accounts talked about it. Each member also gets a coverage record that says how completely it was read. *"Prism searches the world; cohorts search your list."*

Cohorts are **not** registry endpoints. They live at `/v1/cohorts/*` and `/v1/cohort-queries/*`, use POST/PUT/DELETE as well as GET, and are **not** counted in the endpoint total quoted in `SKILL.md`. Auth is the same `x-api-key` header, and the usual rate and concurrency limits apply.

**Use this when the audience is already known.** If the user has a customer list, a creator roster, or a set of handles and wants to know which of THEM mentioned something, this is the surface. If they want to find who in the world is talking about a term, that is `/v1/prism/brand-mentions` or `/v1/search/*`. If they want to watch one thing over time, that is [monitors.md](monitors.md).

## The eight operations

| Method + path | Cost | Success |
|---------------|------|---------|
| `POST /v1/cohorts` | 0 | `201` cohort |
| `PUT /v1/cohorts/{cohortId}/members` | 0 | `200` upload counts |
| `GET /v1/cohorts/{cohortId}` | 0 | `200` cohort |
| `DELETE /v1/cohorts/{cohortId}` | 0 | `204` |
| `POST /v1/cohorts/{cohortId}/queries` | **metered** | `202` query handle |
| `GET /v1/cohort-queries/{queryId}` | 0 | `200` status + billing |
| `GET /v1/cohort-queries/{queryId}/results` | 0 | `200` matches + coverage |
| `DELETE /v1/cohort-queries/{queryId}` | 0 | `204` (cancel) |

That is the whole surface. **There is no list endpoint and no update endpoint.** `GET /v1/cohorts` and `GET /v1/cohorts/{id}/queries` return `405` with an `Allow` header. You cannot rename a cohort, change its `retention_days`, list its queries, or read its members back, so store the `cohortId` and `queryId` yourself. Any other method on these paths is also a `405`.

Ids in paths are 21-character alphanumeric strings (or UUIDs). Anything else is a `400` before lookup. Success bodies use the standard envelope (`success`, `platform: "cohorts"`, `endpoint`, `data`, `credits_used`, `credits_remaining`, `request_id`), and every field below lives under `data`.

## Supported platforms and identity formats

Ten platforms: `bluesky`, `instagram`, `kwai`, `linkedin`, `threads`, `tiktok`, `truth-social`, `twitch`, `twitter`, `youtube`. Use those exact strings. Platform matching is case-insensitive, so `"Instagram"` is accepted. Facebook, Snapchat and every other platform are rejected at upload with `400 COHORT_IDENTITY_PLATFORM_UNSUPPORTED`, so an unsupported identity can never sit in a cohort holding a reservation.

- `handle`: the public username. A leading `@` is stripped and Unicode is NFKC-normalized. 1 to 256 code points after trimming.
- LinkedIn: a profile slug (`satyanadella`) or a `linkedin.com/in/<slug>` URL. Both are rewritten to `https://www.linkedin.com/in/<slug>` before the fetch. Only `/in/` member profiles work. Pick one form and stick to it, because dedupe compares the string you sent, so the slug and the URL would become two members.
- Identity dedupe is per platform on the normalized, case-folded handle. `MrBeast` and `mrbeast` on YouTube are the same member.

## Limits

| Limit | Value |
|-------|-------|
| Members per cohort | 10,000 |
| Members per upload chunk | 1 to 1,000 |
| Cohorts per API key | 100 |
| Members per shard (internal fan-out) | 50, so `shard_count = ceil(members / 50)` |
| Keywords per query | 1 to 20, each 1 to 100 code points |
| Topics per query | 1 to 10 (topic mode only) |
| `max_pages_per_identity` | 1 to 20 |
| `max_items_per_identity` | 1 to 1,000 |
| `max_credits` | 1 to 1,000,000 |
| Handle | 256 code points |
| `external_id` | 1 to 128 code points |
| Cohort `name` | 1 to 120 code points |
| Results page | `limit` 1 to 500 (default 100), body capped at 1 MB |
| Results cursor | 2,048 characters max |
| Retention | 7 to 90 days, default 30 |
| Request body | 4 MB |

## Rules that will bite you

- **Everything is scoped to the API key, not the account.** A cohort or query created with one key is a `404` from any other key on the same account. A cross-tenant hit and a genuine miss both return `404`, never `403`.
- **`POST` and `PUT` require an `Idempotency-Key` header holding a UUID.** `DELETE` does not. Same key plus the same body replays the original response and sets `X-Idempotent-Replay: true` (the envelope also carries `idempotent_replay: true`). Same key plus a different body is a `422 IDEMPOTENCY_KEY_PAYLOAD_MISMATCH`. A missing or non-UUID key is a `400`.
- **`external_id` names exactly ONE identity in a cohort.** It is unique per cohort. Re-sending an existing `external_id` with a different platform or handle **replaces** that member's identity. It does not add a second one. A person with accounts on three platforms needs three different `external_id`s (for example `buyer_01984:tiktok`, `buyer_01984:youtube`). Reusing one `external_id` for two identities is never supported. Depending on the order the rows arrive in, it either fails the chunk or silently keeps only the last identity.
- **`date_from` is a full RFC3339 timestamp with an offset**, not a calendar date. `2026-08-01` is a `400`. Send `2026-08-01T00:00:00.000Z`. The same applies to `date_to`, and `date_to` must not be earlier than `date_from`.
- **A cohort never reads identities back.** `GET /v1/cohorts/{id}` returns metadata and counts only. Handles and external ids are encrypted at rest and cannot be retrieved through the API, so keep your own copy.
- **Results are served only when `status` is `succeeded`.** For `queued`, `running`, `failed`, `cancelled` and `expired` queries, the results route returns `409 COHORT_QUERY_NOT_READY`. If you cancel a running query, you lose access to the matches it already found, and you still pay for the pages it fetched.
- **`succeeded` does not mean exhaustive.** Upstream errors on a member do not fail the query. They show up as coverage `status: "failed"` and in `progress.pages_failed`. Read each member's `coverage` before you treat a result set as complete.
- Every response carries `Cache-Control: private, no-store`.

## POST /v1/cohorts: create a cohort

0 credits. `Idempotency-Key` required. Returns `201`. The body is strict: unknown keys are a `400`.

Body (JSON):
- `name` (optional, string): label, 1 to 120 code points after trimming. An empty string is a `400` (`COHORT_NAME_INVALID`).
- `retention_days` (optional, integer, 7 to 90, default 30): how long the cohort lives. `expires_at = now + retention_days`. Each new member upload and each query submission renews the clock (an idempotent replay does not).

Response `data`: `id`, `name`, `member_count`, `retention_days`, `created_at`, `updated_at`, `expires_at`.

The 101st cohort on one key is a `400 COHORT_LIMIT_EXCEEDED`. Delete an unused cohort to make room.

```bash
curl -X POST "https://www.socialcrawl.dev/v1/cohorts" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 3f1c9c6e-6a1a-4f8e-9a0f-2b6d4a7c5e11" \
  -d '{ "name": "Q3 buyers", "retention_days": 30 }'
```

## PUT /v1/cohorts/{cohortId}/members: upload members

0 credits. `Idempotency-Key` required. One chunk holds 1 to 1,000 members, and a cohort holds 10,000, so a full cohort takes at least 10 calls, each with its own key.

Body: `{ "members": [ { "platform", "handle", "external_id"? }, ... ] }`. Each row is **flat** and the schema is strict, so a nested `identities` array or any extra key is a `400`.

- `platform` (required): one of the ten supported platforms.
- `handle` (required): see identity formats above.
- `external_id` (optional, 1 to 128 code points): your own opaque key. It is echoed on every match and coverage row, it is how you join results back to your records, and it is never sent upstream. You almost always want it.

Upsert rules:
- An identity you already uploaded, sent again with the same (or no) `external_id`, counts as `unchanged`. That makes a nightly full re-push safe.
- An existing `external_id` with a new identity replaces that member's identity (`updated`).
- An identity that already belongs to a different `external_id` is a `409 COHORT_IDENTITY_CONFLICT`, whether the clash is inside one chunk or across chunks.
- Exact duplicate rows inside one chunk are collapsed silently.
- An upload that would take the cohort past 10,000 members is a `400 COHORT_MEMBER_LIMIT_EXCEEDED`, and none of that chunk is applied.

Response `data`: `inserted`, `updated`, `unchanged`, `member_count` (the cohort total after the upload).

```bash
curl -X PUT "https://www.socialcrawl.dev/v1/cohorts/$COHORT_ID/members" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 8c2f0b14-97d1-4a55-9d3e-1f0b7c2a4d90" \
  -d '{
    "members": [
      { "external_id": "buyer_01983",         "platform": "instagram", "handle": "natgeo" },
      { "external_id": "buyer_01984:tiktok",  "platform": "tiktok",    "handle": "mrbeast" },
      { "external_id": "buyer_01984:youtube", "platform": "youtube",   "handle": "MrBeast" },
      { "external_id": "buyer_01985",         "platform": "linkedin",  "handle": "satyanadella" }
    ]
  }'
```

## GET /v1/cohorts/{cohortId}: get a cohort

0 credits. Returns the same `data` as create: `id`, `name`, `member_count`, `retention_days`, `created_at`, `updated_at`, `expires_at`. It never returns stored identities.

```bash
curl "https://www.socialcrawl.dev/v1/cohorts/$COHORT_ID" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## DELETE /v1/cohorts/{cohortId}: delete a cohort

0 credits. Returns `204` with no body. Deletes members, queries, shards and results. Any query still in flight is cancelled and settled first: pages already fetched are charged, and the rest of the reservation is refunded. Credit-ledger receipts are never deleted.

```bash
curl -X DELETE "https://www.socialcrawl.dev/v1/cohorts/$COHORT_ID" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## POST /v1/cohorts/{cohortId}/queries: submit a query

**Metered** (see Pricing). `Idempotency-Key` required. Returns `202` immediately with a `Location` header pointing at the status URL. The work runs asynchronously. The body is strict.

Body (JSON):
- `keywords` (required, array of 1 to 20 strings, each 1 to 100 code points): duplicates are removed after normalization. Matching rules are under "How matching works".
- `date_from` (required, RFC3339 with offset): start of the window, inclusive.
- `date_to` (optional, RFC3339 with offset): end of the window, inclusive. With no `date_to`, the window runs to now.
- `max_pages_per_identity` (required, integer, 1 to 20, no default): the page budget **per endpoint** of each member. This is the main lever on the ceiling. Endpoints with no cursor always read exactly one page whatever you set here.
- `max_items_per_identity` (required, integer, 1 to 1,000, no default): the cap on items **read** per endpoint of each member. It counts every item read, not only matches. Reaching it ends that endpoint as `partial`. It does not change the ceiling.
- `max_credits` (required, integer, 1 to 1,000,000): your safety limit. If it is below the computed ceiling, the submission is rejected (see Pricing).
- `platforms` (optional, array of 1 to 10 platform names): query only members on these platforms. Defaults to every platform present in the cohort. Naming a subset is the other way to cut the ceiling. A subset with no members in the cohort is a `400` ("no members on the requested platforms"). The same is true of an empty cohort.
- `match` (optional, `"keywords"` | `"topics"` | `"both"`) and `topics` (optional): opt-in topic matching, see below. `keywords` stays required in every mode.

`202` response `data`:
- `query_id`, `status` (`queued` on a fresh submit), `member_count`, `shard_count`.
- `estimated_credits`: the computed ceiling.
- `reserved_credits`: what was actually held (equal to the ceiling).
- `progress`: same shape as the status endpoint.
- `status_url` (`/v1/cohort-queries/{id}`) and `result_url` (`/v1/cohort-queries/{id}/results`).
- `replayed`: `true` means an `Idempotency-Key` replay. A replay reports the query's CURRENT state, not necessarily `queued`, and holds nothing new.

On the envelope of a fresh submit, `credits_used` is the reserved amount and `credits_remaining` is your balance after the hold. A replay shows `credits_used: 0`.

```bash
curl -X POST "https://www.socialcrawl.dev/v1/cohorts/$COHORT_ID/queries" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: b7d4a2f0-5c19-4e3a-8f62-0d9e1a3c7b45" \
  -d '{
    "keywords": ["acme", "acme pro"],
    "date_from": "2026-08-01T00:00:00.000Z",
    "date_to": "2026-08-31T23:59:59.999Z",
    "max_pages_per_identity": 2,
    "max_items_per_identity": 200,
    "max_credits": 500
  }'
```

### Opt-in topic matching (`match` + `topics`)

Keyword matching alone catches homonyms ("apple" the fruit) and misses posts that never name the brand. Topic mode adds a model judgment per post.

- `topics`: 1 to 10 objects `{ id, description }`, sent only together with `match: "topics"` or `match: "both"`.
  - `id`: 1 to 64 characters, `[A-Za-z0-9_-]`, unique within the query. It is echoed back.
  - `description`: 1 to 300 characters, any language. Name the sense you mean (`"Apple the technology company and its products"`, not `"apple"`).
- Pairing rules: `topics` without `match` (or with `match: "keywords"`) is a `400 COHORT_TOPICS_REQUIRE_MATCH`. `match: "topics"` or `"both"` without `topics` is a `400 COHORT_MATCH_REQUIRES_TOPICS`.

| `match` | Posts judged | Posts returned |
|---------|--------------|----------------|
| absent or `keywords` | none | keyword hits, exactly as before. No topic fields appear. |
| `topics` | keyword hits only | keyword hits that are about a topic, plus hits that could not be judged |
| `both` | every authored post in the window | every keyword hit, plus posts that are about a topic |

Each result of a topic query gains two fields:
- `matched_topics`: `[{ id, p }]`, the topics with `p >= 0.7`, strongest first. `[]` means the post was judged and is about none of them. `null` means it could not be judged and stands on its keyword match.
- `mention_type`: `first_hand_use_or_purchase`, `opinion_or_review`, `sponsored_or_promotional`, `news_or_share`, `incidental`, `other`, or `uncertain` (no clear winner). It is `null` when the post was not judged or matched no topic.

In `both` mode, `matched_keywords` can be empty, for a post that only a topic matched. Judgment fails open: a chunk that errors or times out keeps its keyword hits with `matched_topics: null` and adds nothing. Topic mode never changes coverage, pages, or the reservation formula. Only your topic descriptions and the public post text go to the judgment. Handles, member ids and `external_id`s never do.

## GET /v1/cohort-queries/{queryId}: check status

0 credits. Poll this until the status is terminal. There is no webhook. A sensible loop starts at 5 s and backs off to 30 s. A verified 1,000-identity run (20 shards) finished in about 2.5 minutes.

Statuses: `queued`, `running`, then one terminal state:
- `succeeded`: every shard finished. Results are readable.
- `failed`: at least one shard failed internally. This is not an upstream error on a member, which still ends `succeeded`.
- `cancelled`: you cancelled it, or deleted its cohort.
- `expired`: the cohort's retention ran out while the query was still queued or running.

Response `data`: `id`, `cohort_id`, `status`, `member_count`, `shard_count`, `completed_shard_count`, `failed_shard_count`, `result_count`, `max_credits`, `reserved_credits`, `actual_credits`, `refunded_credits`, and `progress`:
`{ members_total, members_completed, shards_total, shards_completed, shards_failed, routes_planned, routes_completed, pages_succeeded, pages_failed, matches }`.

`routes_planned` is the sum of endpoints over the queried members, for example 2 per Instagram or YouTube member. `pages_failed` counts endpoints that gave up with an upstream error. Retries that later succeeded are not counted.

```bash
curl "https://www.socialcrawl.dev/v1/cohort-queries/$QUERY_ID" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/cohort-queries/{queryId}/results: read results

0 credits. Only for `succeeded` queries (`409 COHORT_QUERY_NOT_READY` otherwise).

Query params (other params are ignored):
- `limit` (integer, 1 to 500, default 100): applies to `items` AND to `coverage` separately.
- `cursor` (string, at most 2,048 characters): send back `data.next_cursor`. The envelope's `pagination.next_cursor` is also accepted. The cursor is signed and bound to this query and API key. A tampered or foreign cursor is a `400`.

Response `data`: `{ items: [...], coverage: [...], next_cursor }`. Keep paging until `next_cursor` is `null`, and accumulate both arrays, because they drain independently. A 10,000-member query takes at least 20 pages at `limit=500` even with zero matches, and later pages often have empty `items` but still carry coverage. If a page would exceed 1 MB, the server shrinks it, so a short page is not the end.

Each `items[]` row (one per matched post per member, deduplicated on member + platform + `content_id`):
- `query_id`, `member_id`, `external_id` (yours, or `null`), `platform`.
- `route`: the endpoint, e.g. `profile/posts` or `profile/reels`.
- `content_id`, `canonical_url` (or `null`), `published_at`, `retrieved_at`.
- `text_excerpt`: the matched surface. This is the post text, and on YouTube and Twitch the title plus the description.
- `matched_keywords`: the keywords that hit, in normalized form.
- `matched_topics` and `mention_type` on topic queries only.

Each `coverage[]` row covers one cohort member (one platform identity), whether or not it matched:
- `query_id`, `member_id`, `external_id`, `platform`.
- `status`, one of:
  - `complete`: every endpoint reached `date_from` or the end of the feed.
  - `partial`: a page budget, item budget, or fixed-window endpoint stopped short, or undated posts were dropped.
  - `not_found`: the handle is dead, private, or empty on every endpoint. This costs 0.
  - `failed`: an endpoint gave up on an upstream error.
  - `unsupported`.
- `window_complete`: `true` only when every endpoint provably covered the whole window. A dead handle is never `true`.
- `pages`: successful pages read for this member.
- `route_errors`: `[{ code: "COHORT_UPSTREAM_ERROR", route }]` per endpoint that failed.
- `oldest_seen`: an in-window post timestamp from the last page read, or `null`. It is indicative only. Use `status` and `window_complete` to judge depth.

```bash
curl "https://www.socialcrawl.dev/v1/cohort-queries/$QUERY_ID/results?limit=500" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
# next page:
curl "https://www.socialcrawl.dev/v1/cohort-queries/$QUERY_ID/results?limit=500&cursor=$NEXT_CURSOR" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## DELETE /v1/cohort-queries/{queryId}: cancel a query

0 credits. Returns `204`. This cancels the query. It does not delete it, and the query stays readable on the status route as `cancelled`. Queued work never starts, and running work stops at the next page boundary. Pages already fetched stay billable, and the unspent reservation is refunded exactly once. A query that is already terminal (or whose last shard has finished) is a `409 COHORT_QUERY_NOT_CANCELLABLE`. **A cancelled query serves no results.**

```bash
curl -X DELETE "https://www.socialcrawl.dev/v1/cohort-queries/$QUERY_ID" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## How a query runs

Each queried member is read through its platform's **endpoints**: existing registry endpoints, each read page by page:

| Platform | Registry endpoints | Credits per page | Pages per endpoint |
|----------|---------------------------|------------------|----------------|
| bluesky | `bluesky/user/posts` | 1 | always 1 (no cursor) |
| threads | `threads/user/posts` | 1 | always 1 (no cursor) |
| twitch | `twitch/user/videos` | 1 | always 1 (no cursor) |
| linkedin | `linkedin/profile/posts` (identity sent as `url`) | **5** | always 1 (no cursor) |
| twitter | `twitter/user/tweets` | 1 | up to `max_pages_per_identity` |
| tiktok | `tiktok/profile/videos` | 1 | up to `max_pages_per_identity` |
| kwai | `kwai/user/posts` | 1 | up to `max_pages_per_identity` |
| truth-social | `truthsocial/user/posts` | 1 | up to `max_pages_per_identity` |
| instagram | `instagram/profile/posts` + `instagram/profile/reels` | 1 each | up to `max_pages_per_identity` each |
| youtube | `youtube/channel/videos` + `youtube/channel/shorts` | 1 each | up to `max_pages_per_identity` each |

Twitter DOES page (its `user/tweets` endpoint carries a cursor) and LinkedIn does NOT. That is the opposite of what the per-page price suggests. Get those two backwards and you either overquote by 5x or set `max_credits` below the real ceiling and get a `400`.

An endpoint stops at the first of these. The resulting endpoint state feeds coverage:
- A page reaches posts older than `date_from`. The window is covered.
- The feed ends. The window is covered, except on a no-cursor endpoint, which reads `partial` unless its single page already reached `date_from`.
- `max_pages_per_identity` or `max_items_per_identity` is reached. The endpoint reads `partial`.
- The first page is empty, or the upstream returns 404. The endpoint reads `not_found` and costs 0. A member is `not_found` only when every endpoint is, so an Instagram account with posts but no reels is still `complete`.
- Any other 4xx, or 8 consecutive retryable failures (408, 429, 5xx) on one page. The endpoint reads `failed` and costs 0.

Only posts that the source attributes to the supplied identity, and that fall inside `[date_from, date_to]`, are eligible. Twitter retweets (text starting `RT @`) and LinkedIn reshares or third-party feed items are excluded. A post with no date is dropped, and its endpoint cannot claim a complete window.

### How matching works

Keyword matching is deterministic code, not a model. It never stems, fuzzes, expands, or infers aliases.
- Keyword and text are both NFKC-normalized, case-folded, and whitespace-collapsed.
- **Whole word** at Unicode boundaries: letters, digits, marks and `_` count as word characters. `acme` matches `#acme`, `acme!` and `acme-pro`, but not `acmecorp` or `acme_pro`.
- A multi-word keyword matches those words in sequence with any whitespace between them. `"acme pro"` matches `acme  pro`.
- There are no operators, wildcards, or quoting. To catch `AcmeCo` too, pass it as its own keyword.
- CJK: a keyword glued inside surrounding CJK text does not match (`카카오` does not hit `카톡`). Add the surrounding forms as separate keywords.
- YouTube and Twitch match the title plus the description.

## Pricing

**Every call except query submission costs 0 credits.** That covers create, upload members, get, delete cohort, status, results, and cancel.

A query bills in two steps.

**1. Hold at submission.** The ceiling is computed and deducted from your balance up front:

```
ceiling = SUM over queried members, over that platform's endpoints, of
          (endpoint credits per page x (endpoint has a cursor ? max_pages_per_identity : 1))
```

Per queried member, that works out to:

| Platform | Credits per member in the ceiling |
|----------|-----------------------------------|
| bluesky, threads, twitch | **1**, fixed |
| linkedin | **5**, fixed. A bigger page budget neither deepens nor raises it. |
| twitter, tiktok, kwai, truth-social | **1 x `max_pages_per_identity`** |
| instagram, youtube | **2 x `max_pages_per_identity`** |

- Only members on the queried `platforms` count. `max_items_per_identity` does not enter the ceiling.
- The hardest possible ceiling is 10,000 members x 40 (Instagram or YouTube at 20 pages) = 400,000.
- The hold fails before anything is created, and nothing is charged:
  - `max_credits` below the ceiling: `400 INVALID_REQUEST`, with `error.details = { estimated_credits, max_credits }`. Raise `max_credits` to at least `estimated_credits`.
  - `max_credits` above 1,000,000: `400 INVALID_REQUEST`, with `error.details = { max_credits, max_credits_limit }`.
  - Balance below the ceiling, or the hold would breach the API key's own spend cap: `402 INSUFFICIENT_CREDITS`.
- The hold also counts against the key's spend cap. `max_credits` is a safety limit, never permission to spend: the hold is always exactly the ceiling.

**2. Charge as pages succeed, refund at the end.**
- An endpoint charges its own per-page price for every successful upstream page, including the last page of a feed and a page whose items are cut by `max_items_per_identity`.
- These cost nothing: a first page that is empty (dead or private handle), a 404, any other upstream error, a retried failure, a timeout, and pages never fetched because of cancellation.
- On reaching a terminal state (`succeeded`, `failed`, `cancelled`, `expired`), the query charges what it actually used and refunds `reserved - actual` exactly once. The charge is clamped to the reservation, so it can never exceed it. The invariant is `actual_credits + refunded_credits == reserved_credits`, all three shown on the status endpoint.
- Your usage ledger shows the hold as one deduction and the refund as one refund, both on endpoint `/v1/cohort-queries`.

**Worked examples**

| Panel (members queried) | `max_pages` | Ceiling (held) |
|-------------------------|-------------|----------------|
| 400 instagram + 300 tiktok + 200 twitter + 100 linkedin | 3 | 400x2x3 + 300x1x3 + 200x1x3 + 100x5 = 2,400 + 900 + 600 + 500 = **4,400** |
| same panel, `platforms: ["tiktok","twitter"]` | 3 | 900 + 600 = **1,500** |
| same panel | 1 | 800 + 300 + 200 + 500 = **1,800** |
| 10,000 bluesky / threads / twitch | any | **10,000** |
| 10,000 youtube | 20 | **400,000** (the maximum) |

If the first query (4,400 held) ends having used 1,730 credits of successful pages, it charges 1,730 and refunds 2,670. On a verified 1,000-identity production run, 1,000 credits were held: 20 were charged and 980 refunded, because 980 dead handles came back `not_found` at zero cost. Quote the ceiling to the user before submitting. Afterwards, report `reserved_credits` and, once terminal, `actual_credits` / `refunded_credits`.

## Retention

- A cohort expires `retention_days` after creation. The clock restarts on every new member upload and every query submission.
- At expiry, the cohort, its members, queries and results are purged. A query still running at that point turns `expired` and its unspent reservation is refunded.
- Queries and results have no separate expiry. They live exactly as long as their cohort.
- Only matched posts and coverage are stored, never the unmatched feed pages.

## Errors

| Code | Status | When |
|------|--------|------|
| INVALID_REQUEST | 400 | Body or param validation, invalid JSON, a missing or non-UUID `Idempotency-Key`, a malformed path id, an invalid results cursor, `max_credits` below the ceiling or above 1,000,000, or no members on the requested platforms |
| COHORT_IDENTITY_PLATFORM_UNSUPPORTED | 400 | A member (or a `platforms` entry) names a platform outside the ten |
| COHORT_LIMIT_EXCEEDED | 400 | The key already holds 100 cohorts |
| COHORT_MEMBER_LIMIT_EXCEEDED | 400 | This upload would push the cohort past 10,000 members |
| INSUFFICIENT_CREDITS | 402 | The balance or the key spend cap cannot cover the ceiling |
| RESOURCE_NOT_FOUND | 404 | No such cohort or query under this API key (cross-tenant probes look identical) |
| METHOD_NOT_ALLOWED | 405 | Wrong method for the path. Read the `Allow` header. |
| COHORT_IDENTITY_CONFLICT | 409 | The normalized identity already belongs to another `external_id` |
| COHORT_QUERY_NOT_READY | 409 | Results were requested for a query that is not `succeeded` |
| COHORT_QUERY_NOT_CANCELLABLE | 409 | The query is already terminal or finishing |
| PAYLOAD_TOO_LARGE | 413 | The request body is over 4 MB. Split the chunk. |
| COHORT_RESULT_TOO_LARGE | 413 | A single stored result cannot fit in a 1 MB page |
| IDEMPOTENCY_KEY_PAYLOAD_MISMATCH | 422 | An `Idempotency-Key` was reused with a different body |

Validation `400`s name the failing element in the message (`members[3]: COHORT_IDENTITY_HANDLE_INVALID`) and carry up to 10 entries in `error.details.issues` as `{ code, message, path }` (plus `issues_omitted` when there were more). The element codes are:
- `COHORT_IDENTITY_HANDLE_INVALID`, `COHORT_IDENTITY_HANDLE_REQUIRED`
- `COHORT_EXTERNAL_ID_INVALID`, `COHORT_NAME_INVALID`
- `COHORT_KEYWORD_INVALID`, `COHORT_INVALID_DATE_RANGE`
- `COHORT_TOPIC_INVALID`, `COHORT_TOPICS_REQUIRE_MATCH`, `COHORT_MATCH_REQUIRES_TOPICS`

Other issues carry generic codes such as `invalid_type`, `too_big` or `unrecognized_keys`. Read the issues before retrying. A rejected submission holds and charges nothing.
