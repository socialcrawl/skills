# YouTube (11 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| channel | `handle` | standard | Get channel info |
| channel/videos | `handle` | standard | List channel videos |
| video | `url` | standard | Get video details |
| video/comments | `url` | standard | List video comments |
| search | `query` | standard | Search videos |
| channel/shorts | `handle` | standard | List channel shorts |
| community-post | `url` | standard | Get community post |
| playlist | `playlist_id` | standard | Get playlist |
| search/hashtag | `hashtag` | standard | Search by hashtag |
| shorts/trending | *(none)* | advanced | Get trending shorts |
| video/transcript | `url` | premium | Get video transcript |

## Parameter Details

- `handle`: YouTube channel handle without @ symbol (e.g., `MrBeast`)
- `url`: Full YouTube video or post URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
- `query`: Search keyword or phrase (e.g., `javascript tutorial`)
- `playlist_id`: YouTube playlist ID (e.g., `PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf`)
- `hashtag`: Hashtag without # symbol (e.g., `shorts`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/youtube/channel?handle=MrBeast"
```
