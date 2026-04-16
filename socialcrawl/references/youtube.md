# YouTube (12 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| channel | `channelId` / `handle` / `url` | standard | Get channel info (one of required) |
| channel/videos | `channelId` / `handle` | standard | List channel videos (one of required) |
| video | `url` | standard | Get video details |
| video/comments | `url` | standard | List video comments |
| video/comment/replies | `continuationToken` | standard | List replies to a comment |
| search | `query` | standard | Search videos |
| channel/shorts | `channelId` / `handle` | standard | List channel shorts (one of required) |
| community-post | `url` | standard | Get community post |
| playlist | `playlist_id` | standard | Get playlist |
| search/hashtag | `hashtag` | standard | Search by hashtag |
| shorts/trending | *(none)* | advanced | Get trending shorts |
| video/transcript | `url` | premium | Get video transcript |

### Parameter legend

- `a, b` — both params are required.
- `a / b` — a `oneOf` group: at least one member must be provided.
- *(none)* — endpoint takes no query parameters.

## Parameter Details

- `channelId`: YouTube channel ID (e.g., `UCX6OQ3DkcsbYNE6H8uQQuVA`)
- `handle`: YouTube channel handle without @ symbol (e.g., `MrBeast`)
- `url`: Full YouTube channel, video, or post URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
- `query`: Search keyword or phrase (e.g., `javascript tutorial`)
- `playlist_id`: YouTube playlist ID (e.g., `PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf`)
- `hashtag`: Hashtag without # symbol (e.g., `shorts`)
- `continuationToken`: Opaque token returned by `video/comments` to fetch replies for a specific comment

## Field Maps

The `channel` endpoint returns an `Author` response normalized by the `youtube-author` field map, and `video` returns a `Post` normalized by `youtube-post`. Both include computed fields (`engagement_rate`, `language`, `content_category`, `estimated_reach`) under `data.computed`. Use `?format=raw` to bypass both and get the upstream JSON. Other YouTube endpoints are passthrough.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/youtube/channel?handle=MrBeast"
```
