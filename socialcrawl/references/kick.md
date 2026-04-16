# Kick (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| clip | `url` | standard | Get clip details |

## Parameter Details

- `url`: Full Kick clip URL (e.g., `https://kick.com/xqc/clips/clip_abc123`)

## Field Maps

The `clip` endpoint returns a `Post` response normalized by the `kick-post` field map. Kick clip responses are nested under `clip.*` upstream; the field map flattens them. Includes computed fields under `data.computed`.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/kick/clip?url=https://kick.com/xqc/clips/clip_abc123"
```
