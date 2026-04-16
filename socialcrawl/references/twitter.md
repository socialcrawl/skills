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

## Field Maps

The `profile` endpoint returns an `Author` response normalized by the `twitter-author` field map, and `tweet` returns a `Post` normalized by `twitter-post`. Both include computed fields (`engagement_rate`, `language`, `content_category`, `estimated_reach`) under `data.computed`. Twitter responses use GraphQL-style deep nesting upstream — the field map flattens them into the unified schema. Use `?format=raw` to see the original deeply-nested JSON.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/twitter/profile?handle=elonmusk"
```
