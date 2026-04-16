# Truth Social (3 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| user/posts | `handle` / `user_id` | standard | List user posts (one of required) |
| post | `url` | standard | Get post details |

### Parameter legend

- `a, b` — both params are required.
- `a / b` — a `oneOf` group: at least one member must be provided.

## Parameter Details

- `handle`: Truth Social username without @ symbol (e.g., `realDonaldTrump`)
- `user_id`: Numeric Truth Social user ID
- `url`: Full Truth Social post URL (e.g., `https://truthsocial.com/@realDonaldTrump/posts/123456789`)

## Field Maps

The `profile` endpoint returns an `Author` response normalized by the `truthsocial-author` field map, and `post` returns a `Post` normalized by `truthsocial-post`. Both include computed fields under `data.computed`. Use `?format=raw` to bypass both.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/truthsocial/profile?handle=realDonaldTrump"
```
