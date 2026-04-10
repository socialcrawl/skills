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

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/threads/profile?handle=zuck"
```
