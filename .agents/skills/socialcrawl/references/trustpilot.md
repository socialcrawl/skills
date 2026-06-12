# Trustpilot

2 endpoints. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: business-search is 1 credit (standard); reviews is 5 credits (advanced) — exact cost listed per endpoint below.

Notes:
- Trustpilot is COMPANY-reputation data keyed by `domain` — not product reviews (use amazon/reviews or google_shopping/reviews for products).
- Task-polled upstream — calls can take ~15–45s.
- Reviews batch in 20s, max depth 200.
- The total platform-wide review count for a business is the `posts_count` field on the matching `business-search` row.

## GET /v1/trustpilot/business-search — 1 credit (standard)

Search Trustpilot businesses

- `query` (required) — Business name or keyword (e.g. 'nike'). Matches companies, not products; do not pass a bare domain.
- `depth` (optional, integer) — Number of business results to retrieve (default 20, multiples of 10, max 140). More results = longer task time.

```bash
curl "https://www.socialcrawl.dev/v1/trustpilot/business-search?query=nike" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/trustpilot/reviews — 5 credits (advanced)

Get Trustpilot reviews for a business

- `domain` (required) — The business's domain on Trustpilot (e.g. 'www.nike.com' or 'booking.com'), from business-search.
- `depth` (optional, integer) — Number of reviews to retrieve (default 20, multiples of 20, max 200). There is no pagination beyond 200.
- `sort` (optional, enum: recency | relevance) — Review ordering: `recency` (newest first, default) or `relevance`.

```bash
curl "https://www.socialcrawl.dev/v1/trustpilot/reviews?domain=www.nike.com" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
