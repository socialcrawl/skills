# GitHub (12 endpoints)

GitHub is exposed via the official GitHub REST API (no ScrapeCreators dependency). All endpoints use a single shared service-level token internally — customers authenticate with their normal `sc_...` SocialCrawl key and never touch GitHub credentials.

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| profile/repos | `handle` | standard | List a user's repositories |
| repo | `url` | standard | Get repository details |
| repo/readme | `url` | standard | Get raw README markdown |
| repo/releases | `url` | standard | List repository releases |
| repo/issues | `url` | standard | List repository issues (also includes PRs — every PR is also an issue upstream) |
| issue | `url` | standard | Get a single issue or PR |
| issue/comments | `url` | standard | List comments on an issue or PR |
| search | `query` | standard | Search issues and PRs (uses GitHub's `/search/issues`) |
| repo/top-issues | `url` | **advanced** (5cr) | Composite — top feature request + top complaint |
| repo/dossier | `url` | **advanced** (5cr) | Composite — info + readme + releases + top-issues, 5 calls in parallel |
| user/profile-velocity | `handle` | **premium** (10cr) | Composite — PR velocity, own repos, contributed external repos, 5–15 sub-calls |

## Parameter Details

- `handle`: GitHub username (e.g. `octocat`, `torvalds`). 1–39 chars, alphanumeric + non-consecutive hyphens.
- `url`: Full GitHub URL — repo (`https://github.com/octocat/Hello-World`), issue (`https://github.com/octocat/Hello-World/issues/42`), or PR (`https://github.com/facebook/react/pull/12345`). Tolerates trailing slashes, `.git` suffixes, and query strings.
- `query`: GitHub search query — see [GitHub Search syntax](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests). Example: `repo:facebook/react label:bug is:open`.

## Field Maps

- `profile` → `Author` via the `github-author` field map (followers, following, public_repos → likes_count, etc.). Includes computed fields under `data.computed`.
- `repo` → `Author` via the `github-repo` field map (stargazers_count → followers, forks_count → following, subscribers_count → likes_count). Includes computed fields.
- `issue` → `Post` via the `github-post` field map (title → content.text, reactions.total_count → engagement.likes, comments → engagement.comments).
- All other endpoints are passthrough — `repo/readme` returns the raw markdown string, the rest pass GitHub's native JSON.
- Use `?format=raw` to bypass field-mapping on the three field-mapped endpoints.

## Composite endpoints

The 3 composite endpoints fan out multiple GitHub calls server-side and fold the results into a single dossier:

- **`repo/top-issues`** (~3 calls) — `{ top_feature_request, top_complaint }`. Either can be `null`. If both are null, returns 404 with credit refunded.
- **`repo/dossier`** (~5 calls in parallel) — `{ info, readme, releases, top_issues }`. The `info` call is critical (404 → refund); other enrichments degrade gracefully.
- **`user/profile-velocity`** (~5–15 calls) — `{ velocity, contributed_repos, own_repos }`. Three depth modes via the `depth` optional param: `quick` (3 own + 5 external), `default` (5 + 10), `deep` (5 + 15). `deep` can take 2–3 seconds wall-clock.

## Rate limits

The shared service token caps at 5,000 req/hr for general endpoints and 30 req/min for search. Cache TTLs (profile 15min, post 10min, comments 5min, search 2min, analytics 30min) absorb most of it. Cache hits and 4xx/5xx refunds keep customers off the hook when the bucket is squeezed.

## Examples

```bash
# Profile
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/github/profile?handle=octocat"

# Repo
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/github/repo?url=https://github.com/facebook/react"

# Search issues
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/github/search?query=repo:facebook/react+label:bug+is:open"

# Composite dossier (5 credits)
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/github/repo/dossier?url=https://github.com/anthropics/claude-code"
```
