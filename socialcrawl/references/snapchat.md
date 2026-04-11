# Snapchat (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |

## Parameter Details

- `handle`: Snapchat username (e.g., `djkhaled305`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/snapchat/profile?handle=djkhaled305"
```
