# Cohorts

Ask one keyword question of a list of people you already have. Upload up to 10,000 public social identities, submit a keyword query over a date window, and read back which of those accounts talked about it, with per-member coverage telling you how completely each one was read. *"Prism searches the world; cohorts search your list."*

Cohorts are **not** registry endpoints. They live at `/v1/cohorts/*` and `/v1/cohort-queries/*`, use POST/PUT/DELETE as well as GET, and are **not** counted in the endpoint total quoted in `SKILL.md`. Auth is the same `x-api-key` header.

**Use this when the audience is already known.** If the user has a customer list, a creator roster, or a set of handles and wants to know which of THEM mentioned something, this is the surface. If they want to find who in the world is talking about a term, that is `/v1/prism/brand-mentions` or `/v1/search/*`. If they want to watch one thing over time, that is [monitors.md](monitors.md).

**Supported platforms:** bluesky, instagram, kwai, linkedin, threads, tiktok, truth-social, twitch, twitter, youtube. A member can carry an identity on more than one of them.

## Billing

Every management call is **0 credits**: create, upload members, get, delete, check status, cancel, and read results. Only the query bills.

Submitting a query **reserves a worst-case ceiling** and settles down to real work:

```
ceiling = SUM over members, over lanes, of (lane page cap x lane credits per page)
```

- Workers charge **that lane's own per-page price** for every successful upstream page. Failed, timed-out, cancelled-before-call, and skipped pages cost nothing.
- A lane with no cursor can only ever fetch one page, so its page cap in the ceiling is 1 no matter what `max_pages_per_identity` says. The reservation never exceeds what the query can actually spend.

Per member, per platform (lanes come from the registry, so these are the live numbers):

| Platform | Lanes | Credits per member |
|----------|-------|--------------------|
| linkedin | `profile/posts` (5cr, no cursor) | **5, fixed** - a bigger page budget does not deepen it or cost more |
| bluesky, threads, twitch | one 1cr lane, no cursor | **1, fixed** |
| tiktok, twitter, kwai, truth-social | one 1cr lane, cursor-paged | **1 x pages** |
| instagram | `profile/posts` + `profile/reels`, both cursor-paged | **2 x pages** |
| youtube | `channel/videos` + `channel/shorts`, both cursor-paged | **2 x pages** |

Twitter DOES page (its `user/tweets` lane carries a cursor) and LinkedIn does NOT - the opposite of what the per-page price alone suggests. Get those two backwards and you either overquote by 5x or set `max_credits` below the real ceiling and get a 400.
- On a terminal state the query charges the accumulated total and refunds `reserved - actual` exactly once. The invariant is `actual + refunded == reserved`.
- A dead or private handle returns `not_found` at **zero cost**. On a verified 1,000-identity run, 20 credits were charged and 980 refunded.

`max_credits` is **required** and is your safety limit, not permission to spend. Submission is rejected with a `400` if the computed ceiling exceeds it, your key's budget, or your balance, and the rejection happens before any row is created. Quote the ceiling to the user before submitting; the `202` response returns `estimated_credits` and `reserved_credits` so you can report the real reservation afterwards.

## Limits

| Limit | Value |
|-------|-------|
| Members per cohort | 10,000 |
| Members per upload chunk | 1,000 |
| Cohorts per API key | 100 |
| Keywords per query | 20 (100 code points each) |
| Handle length | 256 code points |
| Pages per identity | 20 |
| Items per identity | 1,000 |
| Results page size | 500 rows (1 MB) |
| Retention | 7 to 90 days, default 30 |
| Request body | 4 MB |

## Rules that will bite you

- **`POST` and `PUT` require an `Idempotency-Key` UUID header.** `DELETE` does not. Same key plus the same body replays the original resource and sets `X-Idempotent-Replay: true`; same key plus a different body is a `422 IDEMPOTENCY_KEY_PAYLOAD_MISMATCH`.
- **`date_from` is a full RFC3339 timestamp**, not a calendar date. `2026-08-01` is a `400`; send `2026-08-01T00:00:00.000Z`.
- **A cohort never reads identities back.** `GET /v1/cohorts/{id}` returns metadata and counts only. The handles you uploaded are encrypted at rest and are not retrievable through the API, so keep your own copy.
- **A cross-tenant hit and a genuine miss both return `404`**, never `403`.
- **`succeeded` does not mean exhaustive.** Read `progress.pages_failed` and each member's `coverage` before treating a result set as complete. A member whose page budget ran out has `window_complete: false`.
- Every response carries `Cache-Control: private, no-store`.

## POST /v1/cohorts: create a cohort

0 credits. `Idempotency-Key` required.

Body (JSON):
- `name` (optional, string): label, up to 120 characters.
- `retention_days` (optional, integer, 7 to 90, default 30): how long membership is kept before automatic purge. Uploading members or submitting a query renews the expiry.

```bash
curl -X POST "https://www.socialcrawl.dev/v1/cohorts" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 3f1c9c6e-6a1a-4f8e-9a0f-2b6d4a7c5e11" \
  -d '{ "name": "Q3 buyers", "retention_days": 30 }'
```

## PUT /v1/cohorts/{cohortId}/members: upload members

0 credits. `Idempotency-Key` required. One chunk holds 1 to 1,000 members; a cohort holds 10,000, so a full cohort is at least 10 calls.

Each row is **flat**: `{ external_id?, platform, handle }`. The body schema is `.strict()`, so a nested `identities` array is a `400` - a member with identities on several platforms is several rows that share one `external_id`. Re-sending an `external_id` you already uploaded updates that identity rather than adding a row, so a nightly full re-push is an upsert, not a duplicate. `external_id` is optional but you almost always want it: it is echoed back on every match and coverage row, is how you join results to your own records, and is never sent upstream.

LinkedIn takes the full profile URL, not a bare handle. A leading `@` is stripped everywhere else.

```bash
curl -X PUT "https://www.socialcrawl.dev/v1/cohorts/coh_123/members" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 8c2f0b14-97d1-4a55-9d3e-1f0b7c2a4d90" \
  -d '{
    "members": [
      { "external_id": "buyer_01983", "platform": "instagram", "handle": "natgeo" },
      { "external_id": "buyer_01984", "platform": "tiktok",    "handle": "mrbeast" },
      { "external_id": "buyer_01984", "platform": "youtube",   "handle": "MrBeast" }
    ]
  }'
```

## GET /v1/cohorts/{cohortId}: get a cohort

0 credits. Metadata and counts only, never the stored identities.

```bash
curl "https://www.socialcrawl.dev/v1/cohorts/coh_123" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## DELETE /v1/cohorts/{cohortId}: delete a cohort

0 credits. Returns `204`. Cascades members, queries, shards, and results, and marks active queries cancelled. Credit-ledger receipts are never deleted.

```bash
curl -X DELETE "https://www.socialcrawl.dev/v1/cohorts/coh_123" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## POST /v1/cohorts/{cohortId}/queries: submit a keyword query

**Metered** (see Billing). `Idempotency-Key` required. Returns `202` immediately with `status_url` and `result_url`; the work runs asynchronously.

Body (JSON):
- `keywords` (required, array, 1 to 20): matched literally after Unicode normalization and case folding. Not a search syntax, so no operators, wildcards, or phrases.
- `date_from` (required, string): full RFC3339 start of the observation window.
- `max_credits` (required, integer): your safety limit. Submission fails if the computed ceiling exceeds it.
- `max_items_per_identity` (required, integer, 1 to 1,000).
- `max_pages_per_identity` (required, integer, 1 to 20): page budget per route. Exhausting it leaves `window_complete` false for that member. This is the main lever on the ceiling.
- `date_to` (optional, string): RFC3339 end of the window.
- `platforms` (optional, array): subset of the cohort's platforms to query. Defaults to every platform present in the cohort, so naming a subset is the other way to cut the ceiling.

The `202` body carries `query_id`, `status`, `member_count`, `shard_count`, `estimated_credits`, `reserved_credits`, `progress`, `status_url`, and `result_url`. `replayed: true` means an `Idempotency-Key` replay, and it reports the query's CURRENT state rather than `queued`.

```bash
curl -X POST "https://www.socialcrawl.dev/v1/cohorts/coh_123/queries" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: b7d4a2f0-5c19-4e3a-8f62-0d9e1a3c7b45" \
  -d '{
    "keywords": ["acme", "acme pro"],
    "date_from": "2026-08-01T00:00:00.000Z",
    "max_pages_per_identity": 2,
    "max_items_per_identity": 200,
    "max_credits": 500
  }'
```

## GET /v1/cohort-queries/{queryId}: check status

0 credits. Returns `status` (`queued`, `running`, `succeeded`, `failed`, `cancelled`, `expired`), durable progress counters, and billing. Poll this until the status is terminal.

Read `progress.pages_failed` before trusting the result set: a query can be `succeeded` with partial failures.

```bash
curl "https://www.socialcrawl.dev/v1/cohort-queries/qry_456" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/cohort-queries/{queryId}/results: read results

0 credits. Cursor-paginated matches plus per-member coverage. `limit` is 1 to 500 (default 100), and a page is also capped at 1 MB. Page with the standard `next_cursor`.

Each match carries the member's `external_id`, the platform, the matched item, and which keyword hit. Each coverage row says how completely that member was read, including `window_complete` and any `not_found` verdict for a dead or private handle.

```bash
curl "https://www.socialcrawl.dev/v1/cohort-queries/qry_456/results?limit=500" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## DELETE /v1/cohort-queries/{queryId}: cancel a query

0 credits. Returns `204`. Queued work never starts and running work stops at the next page boundary. Pages already fetched stay billable; the unspent reservation is refunded exactly once.

```bash
curl -X DELETE "https://www.socialcrawl.dev/v1/cohort-queries/qry_456" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## Errors specific to cohorts

| Code | Status | What it means |
|------|--------|---------------|
| COHORT_LIMIT_EXCEEDED | 400 | The account already holds the maximum 100 cohorts |
| COHORT_MEMBER_LIMIT_EXCEEDED | 400 | This upload would push the cohort past 10,000 members |
| COHORT_IDENTITY_PLATFORM_UNSUPPORTED | 400 | A member names a platform outside the supported list |
| COHORT_IDENTITY_CONFLICT | 409 | The normalized identity is already assigned to another `external_id` |
| COHORT_QUERY_NOT_READY | 409 | The query has not completed, so results are not available yet |
| COHORT_QUERY_NOT_CANCELLABLE | 409 | The query is already terminal |
| COHORT_RESULT_TOO_LARGE | 413 | One result exceeds the maximum page size |

Validation `400`s name the failing element (`members[3]: COHORT_...`) and carry `error.details.issues`, so read those before retrying. A rejected submission is unbilled.
