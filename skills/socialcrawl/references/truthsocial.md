# Truth Social (3 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| user/posts | `handle` | standard | List user posts |
| post | `url` | standard | Get post details |

## Parameter Details

- `handle`: Truth Social username without @ symbol (e.g., `realDonaldTrump`)
- `url`: Full Truth Social post URL (e.g., `https://truthsocial.com/@realDonaldTrump/posts/123456789`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/truthsocial/profile?handle=realDonaldTrump"
```
