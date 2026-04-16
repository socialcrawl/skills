# TikTok (26 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| profile/videos | `handle` | standard | List user's videos |
| post | `url` | standard | Get video details |
| post/comments | `url` | standard | List video comments |
| video/comment/replies | `comment_id`, `url` | standard | List replies to a comment |
| search | `query` | standard | Search videos by keyword |
| trending | `region` | advanced | Get trending feed |
| search/hashtag | `hashtag` | standard | Search by hashtag |
| search/top | `query` | standard | Top search results |
| search/users | `query` | standard | Search users |
| user/audience | `handle` | advanced | User audience demographics |
| user/followers | `handle` / `user_id` | standard | List user followers (one of required) |
| user/showcase | `handle` | standard | List user showcase items |
| user/following | `handle` | standard | List user following |
| user/live | `handle` | standard | Get user live stream |
| post/transcript | `url` | premium | Get video transcript |
| song | `clipId` | standard | Get song details |
| song/videos | `(clipId)` | standard | List videos using a song |
| songs/popular | *(none)* | advanced | Get popular songs |
| creators/popular | *(none)* | advanced | Get popular creators |
| hashtags/popular | *(none)* | advanced | Get popular hashtags |
| videos/popular | *(none)* | advanced | Get popular videos |
| shop/product | `url` | standard | Get Shop product details |
| shop/product/reviews | `url` / `product_id` | standard | List Shop product reviews (one of required) |
| shop/products | `url` | standard | List Shop products |
| shop/search | `query` | standard | Search Shop products |

### Parameter legend

- `a, b` — both params are required.
- `a / b` — a `oneOf` group: at least one member must be provided.
- `(a)` — optional only, no required params.
- *(none)* — endpoint takes no query parameters.

## Parameter Details

- `handle`: TikTok username without @ symbol (e.g., `charlidamelio`)
- `user_id`: Numeric TikTok user ID (e.g., `6755273742928806405`)
- `url`: Full TikTok video or Shop URL (e.g., `https://www.tiktok.com/@charlidamelio/video/7321485815660738859`)
- `comment_id`: TikTok comment ID for fetching replies
- `query`: Search keyword or phrase (e.g., `cooking recipes`)
- `clipId`: TikTok sound/song clip ID (e.g., `7252403792087040774`)
- `region`: ISO 3166-1 alpha-2 country code (e.g., `US`)
- `hashtag`: Hashtag without # symbol (e.g., `fyp`)
- `product_id`: TikTok Shop product ID

## Field Maps

The `profile` endpoint returns an `Author` response normalized by the `tiktok-author` field map, and `post` returns a `Post` normalized by `tiktok-post`. Both include computed fields (`engagement_rate`, `language`, `content_category`, `estimated_reach`) under `data.computed`. Use `?format=raw` to bypass both and get the upstream JSON. Other TikTok endpoints are passthrough.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tiktok/profile?handle=charlidamelio"
```
