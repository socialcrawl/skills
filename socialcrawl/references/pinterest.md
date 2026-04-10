# Pinterest (4 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| search | `query` | standard | Search pins |
| pin | `url` | standard | Get pin details |
| board | `url` | standard | Get board |
| user/boards | `handle` | standard | List user boards |

## Parameter Details

- `query`: Search keyword or phrase (e.g., `home decor ideas`)
- `url`: Full Pinterest pin or board URL (e.g., `https://www.pinterest.com/pin/1234567890/`)
- `handle`: Pinterest username (e.g., `pinterest`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/pinterest/search?query=home%20decor%20ideas"
```
