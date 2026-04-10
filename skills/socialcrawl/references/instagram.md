# Instagram (12 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| profile/posts | `handle` | standard | List user posts |
| post | `url` | standard | Get post details |
| post/comments | `url` | standard | List post comments |
| basic-profile | `userId` | standard | Get basic profile by user ID |
| profile/reels | `handle` | standard | List user reels |
| highlights | `handle` | standard | List story highlights |
| highlight/detail | `id` | standard | Get highlight detail |
| search/reels | `query` | standard | Search reels |
| media/transcript | `url` | premium | Get media transcript |
| user/embed | `handle` | standard | Get user embed HTML |
| song/reels | `audio_id` | standard | List reels using a song |

## Parameter Details

- `handle`: Instagram username without @ symbol (e.g., `instagram`)
- `url`: Full Instagram post or reel URL (e.g., `https://www.instagram.com/p/CwA1234abcd/`)
- `userId`: Instagram numeric user ID (e.g., `25025320`)
- `query`: Search keyword or phrase (e.g., `workout routine`)
- `id`: Instagram highlight ID (e.g., `17854360229135492`)
- `audio_id`: Instagram audio/song ID (e.g., `243313786724210`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/instagram/profile?handle=instagram"
```
