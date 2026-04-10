# Linkme (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| page | `url` | standard | Get Linkme page |

## Parameter Details

- `url`: Full Linkme URL (e.g., `https://linkme.bio/example`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/linkme/page?url=https://linkme.bio/example"
```
