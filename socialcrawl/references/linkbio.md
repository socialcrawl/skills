# Linkbio (1 endpoint)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| page | `url` | standard | Get Linkbio page |

## Parameter Details

- `url`: Full Linkbio URL (e.g., `https://lnk.bio/example`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/linkbio/page?url=https://lnk.bio/example"
```
