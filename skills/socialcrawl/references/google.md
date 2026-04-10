# Google (4 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| search | `query` | standard | Web search |
| ad | `url` | advanced | Get ad details |
| adlibrary/advertisers/search | `query` | advanced | Search Ad Library advertisers |
| company/ads | `domain` | advanced | List ads by company domain |

## Parameter Details

- `query`: Search keyword or phrase (e.g., `best restaurants in London`)
- `url`: Full Google ad or Ads Transparency Center URL (e.g., `https://adstransparency.google.com/advertiser/AR12345678901234567`)
- `domain`: Company domain name (e.g., `nike.com`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/google/search?query=best%20restaurants%20in%20London"
```
