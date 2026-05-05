# Twitter/X (7 endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| user/tweets | `handle` | standard | List user tweets |
| tweet | `url` | standard | Get tweet details |
| community | `url` | standard | Get community details |
| community/tweets | `url` | standard | List community tweets |
| ai-search | `query` | standard | **AI-powered freeform Twitter search via Grok 4.20 — returns `{ answer, sources, tool_calls_count }`** |
| tweet/transcript | `url` | premium | Get video transcript |

## Parameter Details

- `handle`: Twitter username without @ symbol (e.g. `elonmusk`)
- `url`: Full tweet or community URL (e.g. `https://x.com/elonmusk/status/1234567890`)
- `query`: Natural-language prompt for `ai-search` (e.g. `What did @elonmusk say about xAI this week?`)

## `ai-search` optional params

| Param | Notes |
|-------|-------|
| `from_handles` | CSV, max 10 — restrict search to these handles. Mutually exclusive with `exclude_handles`. |
| `exclude_handles` | CSV, max 10 — exclude these handles. |
| `from_date` | ISO 8601 `YYYY-MM-DD` lower bound. |
| `to_date` | ISO 8601 `YYYY-MM-DD` upper bound. |

## Field Maps

The `profile` endpoint returns an `Author` response normalized by the `twitter-author` field map, and `tweet` returns a `Post` normalized by `twitter-post`. Both include computed fields (`engagement_rate`, `language`, `content_category`, `estimated_reach`) under `data.computed`. Twitter responses use GraphQL-style deep nesting upstream — the field map flattens them into the unified schema. Use `?format=raw` to see the original deeply-nested JSON.

`ai-search` is passthrough — archetype `Analytics`. Returns `{ answer, sources, tool_calls_count }` directly under `data`. `tool_calls_count` reports how many times Grok invoked its `x_search` tool during reasoning (cost depth signal — client still pays only 1 credit).

## Examples

```bash
# Standard profile
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/twitter/profile?handle=elonmusk"

# AI-powered freeform search scoped to specific handles + date range
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/twitter/ai-search?query=what+is+elon+saying+about+xAI&from_handles=elonmusk,xai&from_date=2026-04-01&to_date=2026-04-30"
```
