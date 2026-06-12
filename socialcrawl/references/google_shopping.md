# Google Shopping

4 endpoints. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: product-search is 5 credits (advanced); product, reviews, and sellers are 1 credit (standard) — exact cost listed per endpoint below.

Notes:
- ALL Google Shopping calls are task-polled upstream — expect roughly 10–28 seconds of latency.
- Two-step workflow: `product`, `reviews`, and `sellers` all require opaque ids (`product_id` / `gid` / `data_docid`) that only `product-search` returns (surfaced as `product.id` + `product.ext.{gid,data_docid}` on each search result).
- `reviews` aggregates across retailers; each review carries `review.source` (the hosting retailer domain).
- A product with no reviews returns 404 with automatic credit refund.

## GET /v1/google_shopping/product-search — 5 credits (advanced)

Search Google Shopping products

- `query` (required) — Product search keyword (e.g. 'wireless earbuds').
- `country` (optional, string) — DataForSEO location name (e.g. 'United States', 'United Kingdom'). Defaults to United States.
- `language` (optional, string) — Language code (e.g. 'en'). Defaults to en.
- `depth` (optional, integer) — Number of product results to retrieve (default 40, max 120). More results = longer task time.
- `price_min` (optional, string) — Minimum product price filter.
- `price_max` (optional, string) — Maximum product price filter.
- `sort_by` (optional, enum: review_score | price_low_to_high | price_high_to_low) — Result ordering: review_score, price_low_to_high, or price_high_to_low.

```bash
curl "https://www.socialcrawl.dev/v1/google_shopping/product-search?query=wireless earbuds" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/google_shopping/product — 1 credit (standard)

Get Google Shopping product detail

- `product_id` (optional, string) — Google Shopping product_id (from product-search).
- `gid` (optional, string) — Google Shopping gid (from product-search).
- `data_docid` (optional, string) — Google Shopping data_docid (from product-search).
- `country` (optional, string) — DataForSEO location name. Defaults to United States.
- `language` (optional, string) — Language code. Defaults to en.

**At least one of `product_id` / `gid` / `data_docid` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/google_shopping/product" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/google_shopping/reviews — 1 credit (standard)

Get Google Shopping product reviews

- `gid` (required) — Google Shopping gid of the product (from product-search). Required.
- `product_id` (optional, string) — Google Shopping product_id (recommended for accuracy).
- `data_docid` (optional, string) — Google Shopping data_docid (recommended for accuracy).
- `depth` (optional, integer) — Number of reviews to retrieve (default 10, multiples of 10, max 8000).
- `country` (optional, string) — DataForSEO location name. Defaults to United States.
- `language` (optional, string) — Language code. Defaults to en.

```bash
curl "https://www.socialcrawl.dev/v1/google_shopping/reviews?gid=3591805395819257241" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/google_shopping/sellers — 1 credit (standard)

Get Google Shopping sellers for a product

- `product_id` (optional, string) — Google Shopping product_id (from product-search).
- `gid` (optional, string) — Google Shopping gid (from product-search).
- `data_docid` (optional, string) — Google Shopping data_docid (from product-search).
- `country` (optional, string) — DataForSEO location name. Defaults to United States.
- `language` (optional, string) — Language code. Defaults to en.

**At least one of `product_id` / `gid` / `data_docid` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/google_shopping/sellers" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
