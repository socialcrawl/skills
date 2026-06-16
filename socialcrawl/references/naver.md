# Naver

12 endpoints. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: every per-corpus endpoint is 1 credit (standard); the `brief` Prism composite is a flat 10 credits — exact cost listed per endpoint below.

Naver is Korea's dominant search portal. This platform exposes 11 Korean search corpora (blog, news, book, encyclopedia, cafe articles, KnowledgeiN, local places, shopping, academic documents, images, web documents), plus the `brief` composite that folds 6 of them into one Korean-internet brief. Notes that apply across all corpora:

- `query` is required everywhere — free-text UTF-8 (Korean or English).
- The `local` corpus caps `display` at 5 and `start` at 1; all other corpora allow `display` up to 100 and `start` up to 1000.
- Item text fields contain Naver `<b>` highlight markup around matched terms — strip or render it as needed.

## GET /v1/naver/blog/search — 1 credit (standard)

Search Naver Blog

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: sim|date. Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/blog/search?query=소셜크롤" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/news/search — 1 credit (standard)

Search Naver News

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: sim|date. Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/news/search?query=삼성전자" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/book/search — 1 credit (standard)

Search Naver Book

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: sim|date|asc|dsc (asc/dsc = price asc/desc). Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/book/search?query=데미안" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/encyc/search — 1 credit (standard)

Search Naver Encyclopedia

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: (sort ignored). Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/encyc/search?query=양자역학" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/cafearticle/search — 1 credit (standard)

Search Naver Cafe articles

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: sim|date. Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/cafearticle/search?query=주식" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/kin/search — 1 credit (standard)

Search Naver KnowledgeiN (지식iN)

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: sim|date|point. Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/kin/search?query=코로나 증상" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/local/search — 1 credit (standard)

Search Naver Local (장소 검색)

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: random|comment (display max 5, start max 1). Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/local/search?query=강남역 카페" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/shop/search — 1 credit (standard)

Search Naver Shopping

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: sim|date|asc|dsc (asc/dsc = price asc/desc). Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/shop/search?query=노트북" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/doc/search — 1 credit (standard)

Search Naver Academic Documents (전문자료)

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: (sort ignored). Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/doc/search?query=딥러닝" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/image/search — 1 credit (standard)

Search Naver Image

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: sim|date. Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/image/search?query=한라산" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/webkr/search — 1 credit (standard)

Search Naver Web (웹문서)

- `query` (required) — Free-text search term (UTF-8). Required.
- `display` (optional, integer) — Number of items to return per page. Defaults to 10. Standard cap 100 (local corpus caps at 5).
- `start` (optional, integer) — 1-indexed offset for pagination. Defaults to 1. Standard cap 1000 (local corpus caps at 1).
- `sort` (optional, string) — Sort order. Accepted values: (sort ignored). Defaults to `sim` (relevance) when the corpus supports sort.

```bash
curl "https://www.socialcrawl.dev/v1/naver/webkr/search?query=기후변화" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/naver/brief — 10 credits (flat override)

One query across 6 Naver corpora (news, blog, cafearticle, kin, shop, webkr) folded into a single Korean-internet brief, with an optional English `digest`. Part of the "Prism" composite family.

- `query` (required) — Search query (Korean or any language).
- `corpora` (optional, string) — CSV subset of `news,blog,cafearticle,kin,shop,webkr` (default all six).
- `display` (optional, integer) — Items per corpus (1–100, default 20).
- `start` (optional, integer) — 1-indexed offset per corpus (1–1000, default 1). Prefer `cursor` for paging.
- `sort` (optional, string) — `sim` (relevance, default) or `date`; shop also `asc`/`dsc` (price); kin also `point`.
- `include` (optional, string) — Set to `digest` for an LLM English digest with translated quotes.
- `cursor` (optional, string) — Opaque pagination token from a prior response's `next_cursor`.

```bash
curl "https://www.socialcrawl.dev/v1/naver/brief?query=삼성전자" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
