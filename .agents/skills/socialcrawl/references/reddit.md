# Reddit (7 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| subreddit | `subreddit` | standard | List subreddit posts |
| subreddit/details | `subreddit` | standard | Get subreddit details |
| search | `query` | standard | Search posts |
| post/comments | `url` | standard | List post comments |
| ad | `id` | advanced | Get ad details |
| ads/search | `query` | advanced | Search ads |
| subreddit/search | `subreddit` | standard | Search within a subreddit |

## Parameter Details

- `subreddit`: Subreddit name without r/ prefix (e.g., `technology`)
- `url`: Full Reddit post URL (e.g., `https://www.reddit.com/r/technology/comments/abc123/example_post/`)
- `query`: Search keyword or phrase (e.g., `best programming languages 2024`)
- `id`: Reddit ad ID (e.g., `t3_abc123`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/reddit/subreddit?subreddit=technology"
```
