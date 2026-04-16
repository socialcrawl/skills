# Threads (5 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| user/posts | `handle` | standard | List user posts |
| post | `url` | standard | Get post details |
| search | `query` | standard | Search posts |
| search/users | `query` | standard | Search users |

## Parameter Details

- `handle`: Threads username without @ symbol (e.g., `zuck`)
- `url`: Full Threads post URL (e.g., `https://www.threads.net/@zuck/post/CwABCDEFGHI`)
- `query`: Search keyword or phrase (e.g., `artificial intelligence`)

## Field Maps

The `profile` endpoint returns an `Author` response normalized by the `threads-author` field map, and `post` returns a `Post` normalized by `threads-post`. Threads post responses are deeply nested under `post.*` upstream; the field map flattens them. Both include computed fields under `data.computed`. Use `?format=raw` to bypass both.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/threads/profile?handle=zuck"
```
