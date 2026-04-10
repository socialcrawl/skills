# Twitch (2 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get streamer profile |
| clip | `url` | standard | Get clip details |

## Parameter Details

- `handle`: Twitch username (e.g., `ninja`)
- `url`: Full Twitch clip URL (e.g., `https://www.twitch.tv/ninja/clip/ExampleClipSlug`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/twitch/profile?handle=ninja"
```
