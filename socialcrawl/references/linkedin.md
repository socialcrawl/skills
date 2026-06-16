# LinkedIn

9 endpoints. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: most endpoints are 1 credit (standard); ad endpoints are 5 credits (advanced); video transcript is 10 credits (premium); the `profile/full` Prism composite is a flat 5 credits — exact cost listed per endpoint below.

## GET /v1/linkedin/profile — 1 credit (standard)

Get LinkedIn user profile

- `url` (required) — Full URL of the LinkedIn profile page

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/profile?url=https://www.linkedin.com/in/williamhgates/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/linkedin/company — 1 credit (standard)

Get LinkedIn company page

- `url` (required) — Full URL of the LinkedIn company page

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/company?url=https://www.linkedin.com/company/microsoft/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/linkedin/post — 1 credit (standard)

Get LinkedIn post details

- `url` (required) — Full URL of the LinkedIn post

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/post?url=https://www.linkedin.com/posts/williamhgates_example-activity-1234567890" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/linkedin/company/posts — 1 credit (standard)

List LinkedIn company posts

- `url` (required) — Full URL of the LinkedIn company page
- `page` (optional, integer) — The page number to get

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/company/posts?url=https://www.linkedin.com/company/microsoft/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/linkedin/ad — 5 credits (advanced)

Get LinkedIn ad details

- `url` (required) — Full URL of the LinkedIn ad

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/ad?url=https://www.linkedin.com/ad-library/detail/666281156" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/linkedin/ads/search — 5 credits (advanced)

Search LinkedIn ads

- `company` (optional, string) — The company name to search for. 'Microsoft' for example
- `keyword` (optional, string) — The keyword to search for
- `companyId` (optional, string) — The company id to search for
- `countries` (optional, string) — Comma separated list of countries. Example: US,CA,MX
- `startDate` (optional, string) — Start date to search for. Format: YYYY-MM-DD
- `endDate` (optional, string) — End date to search for. Format: YYYY-MM-DD
- `paginationToken` (optional, string) — Pagination token to paginate through results

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/ads/search" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/linkedin/search/posts — 1 credit (standard)

Search public LinkedIn posts by keyword

- `query` (required) — Keyword or phrase to search for in public LinkedIn posts.
- `date_posted` (optional, enum: last-hour | last-day | last-week | last-month | last-year) — Date filter based on Google-indexed results.
- `cursor` (optional, string) — The cursor returned by the previous response — Google results page number.

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/search/posts?query=ai agents" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/linkedin/post/transcript — 10 credits (premium)

Get a LinkedIn post video transcript

- `url` (required) — Full URL of the LinkedIn post to transcribe.

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/post/transcript?url=https://www.linkedin.com/posts/gemini-35-flash-is-a-step-forward-for-google-ugcPost-7465082215316525056-MHBd/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/linkedin/profile/full — 5 credits (flat override)

Profile-360 composite for a LinkedIn **company** page — company profile, recent posts, and a computed analytics block (avg engagement rate, posts/week cadence, top post, format mix) folded into one call. Part of the "Prism" composite family.

- `url` (optional, string) — Full URL of the LinkedIn company page.
- `posts` (optional, integer) — How many recent posts to fetch + average the computed metrics over (1–100, default 25).
- `cursor` (optional, string) — Pass a prior response's `posts_cursor` to deepen the post window.
- `include` (optional, string) — CSV subset of `posts,computed` (default both). `include=computed` drops the raw `posts[]` to save payload.

```bash
curl "https://www.socialcrawl.dev/v1/linkedin/profile/full?url=https://www.linkedin.com/company/microsoft/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
