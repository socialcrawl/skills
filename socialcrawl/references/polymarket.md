# Polymarket (2 endpoints)

Polymarket prediction-market data via the public Gamma API (`gamma-api.polymarket.com/public-search`). No upstream auth required. Returns full Gamma event shapes (markets, outcomes, prices, volume, end dates) — no field-mapping into the unified Author/Post schema since prediction markets don't fit those archetypes.

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| search | `query` | standard | Thin proxy — one upstream call per request |
| research | `query` | **advanced** (5cr) | Server-side topic expansion, fan-out, dedup, rank, filter |

## Parameter Details

- `query`: Free-text search query. Natural-language framing prefixes are stripped on `/research` (e.g. `last 30 days bitcoin halving` → `bitcoin halving`).

## How `/research` works

1. **Strip framing** — `last 7/30 days …`, `what are people saying about …`, `what is going on with …`, `how is …`, `tell me about …`, `research …` all drop their prefix.
2. **Expand queries** — generates up to 6 distinct search queries from the core subject, individual informative words (filtering noise like `the`, `vs`, `west`, `league`, `city`, `ai`, `mcp`), and the original full topic.
3. **Parallel fetch** — fires all expanded queries concurrently with `Promise.allSettled`.
4. **Merge + dedupe** — by `event.id`, first occurrence wins.
5. **Topic filter** — keeps events where the title contains at least one informative word from the topic.
6. **Score + sort** — descending by text similarity (exact substring → 1.0; otherwise informative-word ratio).

If at least one fan-out call succeeds, the merged result is returned. Only when every call fails do credits refund.

## Field Maps

None. Both endpoints are passthrough. Archetype: `SearchResult`. Responses come back as `{ data: { items: [...gamma events] } }` — the full Gamma event shape (with `outcomes`, `outcomePrices`, `volume`, `liquidity`, `oneDayPriceChange`, `endDate`, …) sits under each item.

## Examples

```bash
# Thin search
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/polymarket/search?query=bitcoin+halving"

# Server-side research (5 credits)
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/polymarket/research?query=last+30+days+US+election"
```
