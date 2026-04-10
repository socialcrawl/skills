# TikTok (24 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| profile/videos | `handle` | standard | List user's videos |
| post | `url` | standard | Get video details |
| post/comments | `url` | standard | List video comments |
| search | `query` | standard | Search videos by keyword |
| trending | `region` | advanced | Get trending feed |
| search/hashtag | `hashtag` | standard | Search by hashtag |
| search/top | `query` | standard | Top search results |
| search/users | `query` | standard | Search users |
| user/audience | `handle` | advanced | User audience demographics |
| user/followers | `handle` | standard | List user followers |
| user/following | `handle` | standard | List user following |
| user/live | `handle` | standard | Get user live stream |
| post/transcript | `url` | premium | Get video transcript |
| song | `clipId` | standard | Get song details |
| song/videos | `clipId` | standard | List videos using a song |
| songs/popular | *(none)* | advanced | Get popular songs |
| creators/popular | *(none)* | advanced | Get popular creators |
| hashtags/popular | *(none)* | advanced | Get popular hashtags |
| videos/popular | *(none)* | advanced | Get popular videos |
| shop/product | `url` | standard | Get Shop product details |
| shop/product/reviews | `url` | standard | List Shop product reviews |
| shop/products | `url` | standard | List Shop products |
| shop/search | `query` | standard | Search Shop products |

## Parameter Details

- `handle`: TikTok username without @ symbol (e.g., `charlidamelio`)
- `url`: Full TikTok video or Shop URL (e.g., `https://www.tiktok.com/@charlidamelio/video/7321485815660738859`)
- `query`: Search keyword or phrase (e.g., `cooking recipes`)
- `clipId`: TikTok sound/song clip ID (e.g., `7252403792087040774`)
- `region`: ISO 3166-1 alpha-2 country code (e.g., `US`)
- `hashtag`: Hashtag without # symbol (e.g., `fyp`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/tiktok/profile?handle=charlidamelio"
```
