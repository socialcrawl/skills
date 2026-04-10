# Amazon (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| shop | `url` | standard | Get shop page |

## Parameter Details

- `url`: Full Amazon shop or storefront URL (e.g., `https://www.amazon.com/shop/influencer123`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/amazon/shop?url=https://www.amazon.com/shop/influencer123"
```
