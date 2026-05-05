# Tavily (4 endpoints)

Real-time web search, page extraction, and crawling via the Tavily API. The public surface is GET — the fetcher translates query params into a Bearer-auth POST + JSON body server-side, so caching, idempotency, and the OpenAPI spec stay consistent with every other endpoint.

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| search | `query` | standard | Web search with ranked results and an optional LLM-synthesized answer |
| extract | `urls` | standard | Pull clean, AI-ready text from up to 20 URLs |
| map | `url` | standard | Lightweight sitegraph — URLs only, no full content |
| crawl | `url` | standard | Multi-page crawl with per-page extraction |

## Parameter Details

- `query`: Free-text search query.
- `urls`: Comma-separated list of up to 20 URLs (e.g. `urls=https://a.com,https://b.com,https://c.com`).
- `url`: Root URL for `map` / `crawl`.

## Optional params

### `search`

| Param | Notes |
|-------|-------|
| `search_depth` | `basic` (default) / `advanced` / `fast` / `ultra-fast` |
| `topic` | `general` (default) / `news` / `finance` |
| `time_range` | `day` / `week` / `month` / `year` (or `d` / `w` / `m` / `y`) |
| `max_results` | 1–20, default 5 |
| `chunks_per_source` | 1–5, only honoured with `search_depth=advanced` |
| `include_answer` | Boolean — **the high-value flag**, returns Tavily's LLM synthesis |
| `include_images` / `include_image_descriptions` | Booleans |
| `include_raw_content` | Boolean |
| `include_domains` / `exclude_domains` | CSV — domain filters |
| `country` | ISO 3166-1 alpha-2 code |
| `start_date` / `end_date` | YYYY-MM-DD bounds |

### `extract`

| Param | Notes |
|-------|-------|
| `extract_depth` | `basic` (default) / `advanced` |
| `format` | `markdown` (default) / `text` |
| `include_images` / `include_favicon` | Booleans |
| `timeout` | Per-URL timeout, 1–60s |

### `map` / `crawl`

| Param | Notes |
|-------|-------|
| `max_depth` | Default 1 |
| `max_breadth` | Default 20 (per-page link cap) |
| `limit` | Default 50 (total pages) |
| `instructions` | Natural-language guidance for the mapper / crawler |
| `select_paths` / `select_domains` | CSV regex whitelist |
| `exclude_paths` / `exclude_domains` | CSV regex blacklist |
| `allow_external` | Boolean, default `true` |
| `categories` | CSV category hints |
| `extract_depth` / `format` | `crawl` only — same as `extract` |

## Field Maps

None. All four endpoints are passthrough. Archetype: `Analytics` — preserves the full Tavily response (`results`, `answer`, `query_analysis`, `suggestions`, `total_results`, `time_taken`). Using `SearchResult` would silently drop the LLM-generated `answer` field, which is the whole point of Tavily.

Empty `results: []` is billed normally as a successful 200 — the user paid for the search, an empty result is a real answer.

## Examples

```bash
# Search with LLM answer
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tavily/search?query=who+founded+anthropic&include_answer=true&max_results=5"

# Extract single URL
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tavily/extract?urls=https://en.wikipedia.org/wiki/Lionel_Messi"

# Extract multi-URL (comma-separated)
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tavily/extract?urls=https://a.com,https://b.com,https://c.com&format=text"

# Sitegraph
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tavily/map?url=https://docs.tavily.com&limit=50"

# Targeted crawl
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tavily/crawl?url=https://docs.tavily.com&instructions=Find+all+pages+about+the+Search+API&limit=20"
```
