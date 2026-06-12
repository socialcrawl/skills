# Komi

1 endpoint. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: single endpoint at 1 credit (standard) — exact cost listed per endpoint below.

## GET /v1/komi/page — 1 credit (standard)

Get Komi page.

- `url` (required) — Full URL of the Komi page

```bash
curl "https://www.socialcrawl.dev/v1/komi/page?url=https://kimkardashian.komi.io/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
