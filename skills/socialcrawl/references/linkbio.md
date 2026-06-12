# Linkbio

1 endpoint. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: single endpoint at 1 credit (standard) — exact cost listed per endpoint below.

## GET /v1/linkbio/page — 1 credit (standard)

Get Linkbio page.

- `url` (required) — Full URL of the Linkbio page

```bash
curl "https://www.socialcrawl.dev/v1/linkbio/page?url=https://lnk.bio/example" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
