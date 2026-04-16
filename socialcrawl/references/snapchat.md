# Snapchat (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |

## Parameter Details

- `handle`: Snapchat username (e.g., `djkhaled305`)

## Field Maps

The `profile` endpoint returns an `Author` response normalized by the `snapchat-author` field map. Snapchat profile responses are nested under `userProfile.*` upstream; the field map flattens them. Includes computed fields under `data.computed`.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/snapchat/profile?handle=djkhaled305"
```
