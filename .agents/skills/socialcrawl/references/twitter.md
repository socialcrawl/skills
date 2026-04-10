# Twitter/X (6 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| user/tweets | `handle` | standard | List user tweets |
| tweet | `url` | standard | Get tweet details |
| community | `url` | standard | Get community details |
| community/tweets | `url` | standard | List community tweets |
| tweet/transcript | `url` | premium | Get video transcript |

## Parameter Details

- `handle`: Twitter username without @ symbol (e.g., `elonmusk`)
- `url`: Full tweet or community URL (e.g., `https://x.com/elonmusk/status/1234567890`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/twitter/profile?handle=elonmusk"
```
