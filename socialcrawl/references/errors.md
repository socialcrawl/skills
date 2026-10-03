# Errors

Read this when a call fails. The full code table (status, retryable, what to do) is generated in [api-overview.md](api-overview.md#error-codes); the `error.details` reasons are in [api-overview.md](api-overview.md#error-details-errordetails).

## Classify before retrying

- **Fix before retrying:** `MISSING_API_KEY`, `INVALID_API_KEY`, `INSUFFICIENT_CREDITS`, `KEY_BUDGET_EXCEEDED`, `INVALID_REQUEST`, `METHOD_NOT_ALLOWED`, `ENDPOINT_NOT_FOUND`, `PAYLOAD_TOO_LARGE`, and idempotency conflicts. Explain the corrective action and do not automatically repeat the same request.
- **Wait before retrying:** `RATE_LIMITED`, `CONCURRENCY_LIMIT`, and `SERVICE_UNAVAILABLE`. Honour `Retry-After`, then use exponential backoff with jitter.
- **Transient upstream failure:** `UPSTREAM_ERROR` and `INTERNAL_ERROR`. Retry at most once, then report the outage with the endpoint and request ID, never the credential.
- **Not found:** `RESOURCE_NOT_FOUND` is a valid empty outcome, not a retry loop.

## Act on `error.details`

Every error carries `error.retryable`, and many carry `error.details.reason`; act on it rather than on the status alone:

- **402** (`balance_too_low`, `key_budget_reached`) says `retry_will_succeed: false`: never retry, point the user at `top_up_url` or `key_settings_url`. On a metered call `pricing: "ceiling"` means the quoted credits are the maximum hold, and `lower_cost_with` names the params that hold less.
- **400 `page_limit`** (`max_page`, `narrow_with`): the source has no further pages for this query; stop paging and narrow the query instead. A 400 that says `Did you mean ...?` names the parameter or value to fix.
- **404 `account_gone` / `account_private` / `handle_unresolved`**: follow `error.details.suggestion` once (for a YouTube handle, retry with the stored `channelId` to tell a rename from a removal), then report. `site_not_supported` on `web/scrape` is final; its `suggestion` names the SocialCrawl endpoint for a social link.
- **404 `ENDPOINT_NOT_FOUND`** may suggest the right path; check the live registry (`GET /v1/utility/endpoints?search=`, free) before saying something is unsupported.

## Retrying paid calls

For a retryable paid non-streaming request, send an `Idempotency-Key` before the first attempt and reuse it only for the identical payload. Do not automatically retry streaming requests. Never exceed one automatic retry unless the user explicitly asks for continued retries.

Failed calls are refunded (upstream errors, circuit-breaker rejections, timeouts, not-found, empty results); a request rejected for bad params, a page past the source's last page, or a rate limit never deducts at all.
