# Linktree (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| page | `url` | standard | Get Linktree page |

## Parameter Details

- `url`: Full Linktree URL (e.g., `https://linktr.ee/charlidamelio`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/linktree/page?url=https://linktr.ee/charlidamelio"
```
