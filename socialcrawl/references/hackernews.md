# Hacker News (4 endpoints)

Hacker News is exposed via Algolia's free public HN API — no ScrapeCreators dependency, no separate auth. Customers use their normal `sc_...` SocialCrawl key.

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| search | `query` | standard | Search stories — defaults to `tags=story` and `numericFilters=points>2` |
| story | `id` | standard | Get a single story (item) |
| story/comments | `id` | standard | Get the comment tree for a story |
| profile | `handle` | standard | Get a user profile (karma, about, joined_at) |

`story` and `story/comments` share one upstream call (`/api/v1/items/{id}`) but produce different shapes via the archetype dispatch.

## Parameter Details

- `query`: Search keyword or phrase (e.g. `claude code`, `vector databases`).
- `id`: HN item id — numeric, 1–12 digits (e.g. `8863`).
- `handle`: HN username — 2–15 chars, alphanumeric + underscore + hyphen (e.g. `pg`, `tom-rodgers`).

## Optional params (search)

| Param | Notes |
|-------|-------|
| `tags` | `story` (default) / `comment` / `poll` / `show_hn` / `ask_hn` / `front_page` etc. |
| `numericFilters` | e.g. `points>50,num_comments>10` |
| `hitsPerPage` | 1–1000, default 30 |
| `page` | 0-indexed |

## Field Maps

- `profile` → `Author` via `hackernews-author` (karma → likes_count, no follower/following concept upstream).
- `story` → `Post` via `hackernews-post` (points → engagement.likes, num_comments → engagement.comments, title → content.text).
- `search` and `story/comments` are passthrough.
- HN genuinely lacks several unified fields (avatars, follower counts, video/duration). Those resolve to `null`.

## Search payload cleanup

`/v1/hackernews/search` strips three Algolia-specific fields from each hit before returning:

- `children` (misleading, redundant with `num_comments`)
- `_highlightResult` (search-highlight clone, doubles payload size)
- `_snippetResult` (snippet clone, same noise)

`_tags` is kept — it tells you whether each hit is a story / comment / poll. `story/comments` keeps `children` because it IS the comment tree.

## Examples

```bash
# Search
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/hackernews/search?query=claude+code"

# Single story
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/hackernews/story?id=8863"

# Comment tree
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/hackernews/story/comments?id=8863"

# Profile
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/hackernews/profile?handle=pg"
```
