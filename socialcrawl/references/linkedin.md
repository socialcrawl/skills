# LinkedIn (6 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `url` | standard | Get user profile |
| company | `url` | standard | Get company page |
| post | `url` | standard | Get post details |
| company/posts | `url` | standard | List company posts |
| ad | `url` | advanced | Get ad details |
| ads/search | *(none)* | advanced | Search ads |

### Parameter legend

- *(none)* — endpoint takes no required query parameters. Optional filters (e.g., `company`) may be forwarded but are not validated.

## Parameter Details

- `url`: Full LinkedIn profile, company, post, or ad URL (e.g., `https://www.linkedin.com/in/williamhgates/`)

## Field Maps

The `profile` and `company` endpoints both return an `Author` response normalized by the `linkedin-author` field map, and `post` returns a `Post` normalized by `linkedin-post`. Both include computed fields under `data.computed`. Use `?format=raw` to bypass both.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/linkedin/profile?url=https://www.linkedin.com/in/williamhgates/"
```
