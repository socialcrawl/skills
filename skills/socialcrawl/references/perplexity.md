# Perplexity

1 endpoint. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: the single endpoint is 1 credit (standard) — exact cost listed per endpoint below.

Web research via Perplexity Sonar. Sonar is grounded in the open web — it returns an LLM-synthesized answer plus the URLs it cited, all under the standard SocialCrawl envelope. `data` carries `{ answer, sources }`; `sources` is always an array (empty is legal — Sonar may answer one-line factual questions without citing), each entry has `url` and an optional `title`. Cache TTL is 120s — repeated identical calls within that window return the cached answer for 0 credits. Upstream failures (gateway down, Sonar rate limit, malformed response) are refunded.

## GET /v1/perplexity/research — 1 credit (standard)

Web research via Perplexity Sonar

- `query` (required) — Natural-language research prompt. Sonar autonomously searches the live web and grounds the response in real sources. No prompt-engineering required — phrase it as you would to a search engine or research assistant.

```bash
curl "https://www.socialcrawl.dev/v1/perplexity/research?query=What is the capital of France?" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
