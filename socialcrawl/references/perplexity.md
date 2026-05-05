# Perplexity (1 endpoint)

Web research via Perplexity Sonar through the Vercel AI Gateway. Sonar is grounded in the open web — it returns an LLM-synthesized answer plus the URLs it cited, all under the standard SocialCrawl envelope.

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| research | `query` | standard | Web-grounded research — returns `{ answer, sources }` |

## Parameter Details

- `query`: Natural-language research prompt — full sentences are fine (e.g. `What is the capital of France?`, `Who founded Anthropic and when?`).

## Response shape

```json
{
  "success": true,
  "platform": "perplexity",
  "endpoint": "/v1/perplexity/research",
  "data": {
    "answer": "Paris is the capital of France.",
    "sources": [
      { "url": "https://en.wikipedia.org/wiki/Paris", "title": "Paris - Wikipedia" }
    ]
  },
  "credits_used": 1,
  "credits_remaining": 99,
  "request_id": "req-...",
  "cached": false
}
```

`data.sources` is always an array. Empty is legal — Sonar may answer one-line factual questions without citing. Each entry has `url` (required) and an optional `title`.

## Notes

- Field map: none. Archetype: `Analytics` (preserves the full payload).
- Cache TTL: 120s (search category). Repeated calls within 120s return identical cached answers for 0 credits. Bust with a unique param if you need absolute freshness.
- `?format=raw` has no effect — there's no transform pipeline to bypass.
- Refunds on upstream failure (gateway down, Sonar rate limit, malformed response) — customer never charged on a transient blip.

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/perplexity/research?query=Who+founded+Anthropic"
```
