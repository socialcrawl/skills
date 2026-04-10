# Komi (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| page | `url` | standard | Get Komi page |

## Parameter Details

- `url`: Full Komi URL (e.g., `https://komi.io/example`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/komi/page?url=https://komi.io/example"
```
