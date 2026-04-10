# LinkedIn (6 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `url` | standard | Get user profile |
| company | `url` | standard | Get company page |
| post | `url` | standard | Get post details |
| company/posts | `url` | standard | List company posts |
| ad | `url` | advanced | Get ad details |
| ads/search | `company` | advanced | Search ads by company |

## Parameter Details

- `url`: Full LinkedIn profile, company, post, or ad URL (e.g., `https://www.linkedin.com/in/williamhgates/`)
- `company`: Company name or LinkedIn company URL (e.g., `Microsoft`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/linkedin/profile?url=https://www.linkedin.com/in/williamhgates/"
```
