# Reddit (7 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| subreddit | `subreddit` | standard | List subreddit posts |
| subreddit/details | `subreddit` / `url` | standard | Get subreddit details (one of required) |
| search | `query` | standard | Search posts |
| post/comments | `url` | standard | List post comments |
| ad | `id` | advanced | Get ad details |
| ads/search | `query` | advanced | Search ads |
| subreddit/search | `subreddit` | standard | Search within a subreddit |

### Parameter legend

- `a, b` — both params are required.
- `a / b` — a `oneOf` group: at least one member must be provided.

## Parameter Details

- `subreddit`: Subreddit name without r/ prefix (e.g., `technology`)
- `url`: Full Reddit subreddit or post URL (e.g., `https://www.reddit.com/r/technology/comments/abc123/example_post/`)
- `query`: Search keyword or phrase (e.g., `best programming languages 2024`)
- `id`: Reddit ad ID (e.g., `t3_abc123`)

## Field Maps

The `subreddit/details` endpoint returns an `Author` response normalized by the `reddit-author` field map and includes computed fields under `data.computed`. Other Reddit endpoints are passthrough. Use `?format=raw` on `subreddit/details` to get the upstream JSON.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/reddit/subreddit?subreddit=technology"
```
