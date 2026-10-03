# NewsArticleList fields

Every field the 2 field-mapped endpoints returning `NewsArticleList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `article.domain` | string\|null | Host domain of the article |
| `article.id` | string | Stable article ID (hash of the url) |
| `article.image_url` | string\|null | Thumbnail image URL |
| `article.placement` | string\|null | Source list: "news_search" or "top_stories" |
| `article.published_at` | string\|number\|null | Absolute UTC publish time |
| `article.rank` | number\|null | Result rank (news_search items only; null on top_stories) |
| `article.snippet` | string\|null | Article excerpt (news_search items only; null on top_stories) (only when the fallback source serves) |
| `article.source` | string\|null | Publishing outlet name (falls back to the domain) |
| `article.title` | string\|null | Article headline |
| `article.url` | string\|null | Direct URL to the article |
