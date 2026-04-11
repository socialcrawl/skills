# Pillar (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| page | `url` | standard | Get Pillar page |

## Parameter Details

- `url`: Full Pillar URL (e.g., `https://pillar.io/example`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/pillar/page?url=https://pillar.io/example"
```
