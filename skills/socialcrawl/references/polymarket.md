# Polymarket

1 endpoint. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: single endpoint at 5 credits (advanced) — exact cost listed per endpoint below.

Polymarket prediction-market event data sourced from Polymarket's public Gamma API. Responses come back as `{ data: { items: [...gamma events] } }` — the full Gamma event shape (with `outcomes`, `outcomePrices`, `volume`, `liquidity`, `oneDayPriceChange`, `endDate`, …) sits under each item, with no field-mapping into the unified Author/Post schema since prediction markets don't fit those archetypes.

## GET /v1/polymarket/research — 5 credits (advanced)

Polymarket prediction markets — multi-query research.

- `query` (required) — The research topic — free-text natural language (e.g. 'last 30 days bitcoin halving', 'kanye west tour'). Framing prefixes like 'last N days' and 'what are people saying about' are stripped automatically before expansion.

```bash
curl "https://www.socialcrawl.dev/v1/polymarket/research?query=trump 2028 election" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

### How research works server-side

1. **Strip framing** — prefixes like `last 7/30 days …`, `what are people saying about …`, `tell me about …`, `research …` are dropped.
2. **Expand queries** — generates up to 6 distinct search queries from the core subject, individual informative words, and the original full topic.
3. **Parallel fetch** — fires all expanded queries concurrently.
4. **Merge + dedupe** — by `event.id`, first occurrence wins.
5. **Topic filter** — keeps events whose title contains at least one informative word from the topic.
6. **Score + sort** — descending by text similarity.

If at least one fan-out call succeeds, the merged result is returned; credits refund only when every call fails.
