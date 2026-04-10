# Kick (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| clip | `url` | standard | Get clip details |

## Parameter Details

- `url`: Full Kick clip URL (e.g., `https://kick.com/xqc/clips/clip_abc123`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/kick/clip?url=https://kick.com/xqc/clips/clip_abc123"
```
