# Facebook (12 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `url` | standard | Get page profile |
| profile/posts | `url` | standard | List page posts |
| post | `url` | standard | Get post details |
| post/comments | `url` | standard | List post comments |
| group/posts | `url` | standard | List group posts |
| post/transcript | `url` | premium | Get video transcript |
| profile/photos | `url` | standard | List profile photos |
| profile/reels | `url` | standard | List profile reels |
| adlibrary/ad | `id` | advanced | Get Ad Library ad details |
| adlibrary/company/ads | `pageId` | advanced | List company ads |
| adlibrary/search/ads | `query` | advanced | Search Ad Library |
| adlibrary/search/companies | `query` | advanced | Search Ad Library companies |

## Parameter Details

- `url`: Full Facebook page, post, video, or group URL (e.g., `https://www.facebook.com/Meta`)
- `id`: Facebook Ad Library ad ID (e.g., `23851234567890123`)
- `pageId`: Facebook page ID of the advertiser (e.g., `20531316728`)
- `query`: Search keyword or phrase (e.g., `artificial intelligence`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/facebook/profile?url=https://www.facebook.com/Meta"
```
