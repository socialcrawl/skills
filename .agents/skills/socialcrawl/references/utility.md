# Utility (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| age-gender | `url` | premium | Detect age and gender from image |

## Parameter Details

- `url`: Direct URL of the image to analyze (e.g., `https://example.com/photo.jpg`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/utility/age-gender?url=https://example.com/photo.jpg"
```
