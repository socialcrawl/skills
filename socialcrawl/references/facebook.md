# Facebook (12 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `url` | standard | Get page profile |
| profile/posts | `url` / `pageId` | standard | List page posts (one of required) |
| post | `url` | standard | Get post details |
| post/comments | `url` / `feedback_id` | standard | List post comments (one of required) |
| group/posts | `url` / `group_id` | standard | List group posts (one of required) |
| post/transcript | `url` | premium | Get video transcript |
| profile/photos | `url` | standard | List profile photos |
| profile/reels | `url` | standard | List profile reels |
| adlibrary/ad | `id` / `url` | advanced | Get Ad Library ad details (one of required) |
| adlibrary/company/ads | `pageId` / `companyName` | advanced | List company ads (one of required) |
| adlibrary/search/ads | `query` | advanced | Search Ad Library |
| adlibrary/search/companies | `query` | advanced | Search Ad Library companies |

### Parameter legend

- `a, b` — both params are required.
- `a / b` — a `oneOf` group: at least one member must be provided.

## Parameter Details

- `url`: Full Facebook page, post, video, or group URL (e.g., `https://www.facebook.com/Meta`)
- `pageId`: Facebook page ID of the advertiser or creator (e.g., `20531316728`)
- `group_id`: Facebook group ID
- `feedback_id`: Facebook post feedback ID (used by `post/comments` as an alternative to `url`)
- `id`: Facebook Ad Library ad ID (e.g., `23851234567890123`)
- `companyName`: Facebook advertiser page name
- `query`: Search keyword or phrase (e.g., `artificial intelligence`)

## Field Maps

The `profile` endpoint returns an `Author` response normalized by the `facebook-author` field map, and `post` returns a `Post` normalized by `facebook-post`. Both include computed fields under `data.computed`. Use `?format=raw` to bypass both. Other Facebook endpoints are passthrough.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/facebook/profile?url=https://www.facebook.com/Meta"
```
