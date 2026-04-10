# SocialCrawl Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a distributable Claude Code skill that gives AI agents full access to the SocialCrawl unified social media data API (21 platforms, 105 endpoints).

**Architecture:** Progressive disclosure skill — lean SKILL.md (~200 lines) with platform index and workflow logic, backed by 22 reference files (1 api-overview + 21 per-platform). Content derived from existing `llms-full.txt` and `llms-{platform}.txt` generated docs.

**Tech Stack:** Claude Code skill format (SKILL.md + references/), skill-creator tooling (init_skill.py, package_skill.py)

---

### Task 1: Scaffold the Skill

**Files:**
- Create: `for-agents/socialcrawl/SKILL.md` (via init_skill.py, then overwritten)
- Create: `for-agents/socialcrawl/references/` (via init_skill.py)

- [ ] **Step 1: Run init_skill.py to scaffold**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl"
python "C:/Users/doodd/.claude/skills/skill-creator/scripts/init_skill.py" socialcrawl --path for-agents
```

Expected: Directory `for-agents/socialcrawl/` created with template SKILL.md, scripts/, references/, assets/ directories.

- [ ] **Step 2: Delete unneeded directories and example files**

Delete these files and directories — the skill only uses references/:

```bash
rm -rf "for-agents/socialcrawl/scripts"
rm -rf "for-agents/socialcrawl/assets"
rm "for-agents/socialcrawl/references/api_reference.md"
```

Expected: Only `for-agents/socialcrawl/SKILL.md` and empty `for-agents/socialcrawl/references/` remain.

- [ ] **Step 3: Commit scaffold**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents"
git add socialcrawl/SKILL.md socialcrawl/references/
git commit -m "chore: scaffold socialcrawl skill via init_skill.py"
```

---

### Task 2: Write SKILL.md

**Files:**
- Modify: `for-agents/socialcrawl/SKILL.md`

- [ ] **Step 1: Replace the template SKILL.md with the full skill content**

Write the following exact content to `for-agents/socialcrawl/SKILL.md`:

```markdown
---
name: socialcrawl
description: >
  Interact with the SocialCrawl API — a unified social media data API covering
  21 platforms and 105 endpoints. Fetch profiles, posts, comments, search results,
  and analytics from TikTok, Instagram, YouTube, Facebook, Twitter/X, LinkedIn,
  Reddit, Threads, Pinterest, and 12 more platforms through a single API.
  Use when the user wants to: (1) fetch social media data (profiles, posts,
  comments, search), (2) generate code that calls the SocialCrawl API,
  (3) understand SocialCrawl endpoints, pricing, or capabilities,
  (4) check their SocialCrawl credit balance, or mentions "SocialCrawl",
  "social crawl", or "social media API".
---

# SocialCrawl API

Unified social media data API. One API key, one response format, 21 platforms, 105 endpoints.

## API Key

Resolve the API key before making any call:

1. Check env var `SOCIALCRAWL_API_KEY`
2. If not set, ask the user for their key
3. After receiving a key inline, suggest they set it for future sessions:
   ```bash
   export SOCIALCRAWL_API_KEY="sc_xxxxx"
   ```

## First Use

On the first interaction with this skill in a session:

1. Briefly introduce: "SocialCrawl provides a single API for 21 social media platforms (105 endpoints). Let me verify your API key."
2. Tell the user you'll make a test call that costs 1 credit, then run:
   ```bash
   curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" "https://api.socialcrawl.com/v1/tiktok/profile?handle=tiktok"
   ```
3. If successful, confirm the key works and show credits_remaining. Then respond to whatever the user actually asked.
4. If it fails, report the error and help troubleshoot (see Error Handling below).

## Platforms

| Platform | Endpoints | Reference |
|----------|-----------|-----------|
| TikTok | 24 | [references/tiktok.md](references/tiktok.md) |
| Instagram | 12 | [references/instagram.md](references/instagram.md) |
| YouTube | 11 | [references/youtube.md](references/youtube.md) |
| Facebook | 12 | [references/facebook.md](references/facebook.md) |
| Twitter/X | 6 | [references/twitter.md](references/twitter.md) |
| LinkedIn | 6 | [references/linkedin.md](references/linkedin.md) |
| Reddit | 7 | [references/reddit.md](references/reddit.md) |
| Threads | 5 | [references/threads.md](references/threads.md) |
| Pinterest | 4 | [references/pinterest.md](references/pinterest.md) |
| Google | 4 | [references/google.md](references/google.md) |
| Truth Social | 3 | [references/truthsocial.md](references/truthsocial.md) |
| Twitch | 2 | [references/twitch.md](references/twitch.md) |
| Snapchat | 1 | [references/snapchat.md](references/snapchat.md) |
| Kick | 1 | [references/kick.md](references/kick.md) |
| Amazon | 1 | [references/amazon.md](references/amazon.md) |
| Linktree | 1 | [references/linktree.md](references/linktree.md) |
| Linkbio | 1 | [references/linkbio.md](references/linkbio.md) |
| Linkme | 1 | [references/linkme.md](references/linkme.md) |
| Komi | 1 | [references/komi.md](references/komi.md) |
| Pillar | 1 | [references/pillar.md](references/pillar.md) |
| Utility | 1 | [references/utility.md](references/utility.md) |

## Workflow

Determine what the user wants, then follow the matching workflow:

**User wants data:**
1. Identify the platform and resource from their request
2. Read the platform's reference file from the table above
3. Resolve API key
4. Construct and execute the curl command
5. Return raw JSON response
6. Note `credits_used` and `credits_remaining` from the response

**User wants code:**
1. Identify platform, resource, and target language
2. Read the platform's reference file
3. Generate a working code snippet using `$SOCIALCRAWL_API_KEY` env var for the key
4. Present the code without executing

**User asks about capabilities:**
1. Answer from the platform table above
2. If they need details about auth, response format, errors, or credits, read [references/api-overview.md](references/api-overview.md)

**User asks about credits/balance:**
1. Resolve API key
2. Run: `curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" "https://api.socialcrawl.com/api/credits/balance"`
3. Return the balance

**Ambiguous platform:** If the user says "get profile for @nike" without specifying a platform, ask which platform they mean.

**Multi-platform requests:** Load each platform's reference file and make sequential calls.

## Making API Calls

Base URL: `https://api.socialcrawl.com`

All endpoints are GET requests:

```
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/{platform}/{resource}?{param}={value}"
```

URL-encode parameter values that contain spaces or special characters.

## Credit Tiers

| Tier | Cost | Typical endpoints |
|------|------|-------------------|
| standard | 1 credit | Profiles, posts, search, comments |
| advanced | 5 credits | Audience demographics, ad libraries, trending |
| premium | 10 credits | Video transcripts, AI analysis |

Before executing an advanced or premium call, mention the credit cost to the user. After every call, report `credits_used` and `credits_remaining` from the response.

## Error Handling

| Code | Status | Action |
|------|--------|--------|
| MISSING_API_KEY | 401 | Ask user for their API key |
| INVALID_API_KEY | 401 | "Your API key appears invalid. Check your SocialCrawl dashboard." |
| INSUFFICIENT_CREDITS | 402 | "You're out of credits. Top up at socialcrawl.com/dashboard/billing" |
| INVALID_REQUEST | 400 | Check required params in the platform reference file |
| ENDPOINT_NOT_FOUND | 404 | "That endpoint doesn't exist. Check the platform table above." |
| RESOURCE_NOT_FOUND | 404 | "That profile/post wasn't found on the platform." |
| CONCURRENCY_LIMIT | 429 | "Too many concurrent requests. Wait a moment and retry." |
| UPSTREAM_ERROR | 502 | "Platform temporarily unavailable. Credits were refunded." |
| SERVICE_UNAVAILABLE | 503 | "Platform circuit breaker is open. Try again in 30s. Credits refunded." |
| INTERNAL_ERROR | 500 | "Unexpected error. Credits were refunded." |

## References

- **[references/api-overview.md](references/api-overview.md)** — Read when user asks about authentication, response format, error details, credit system, or the `?format=raw` parameter
- **[references/{platform}.md](references/)** — Read the specific platform file when user asks about or wants to call that platform's endpoints
```

- [ ] **Step 2: Verify line count**

```bash
wc -l "for-agents/socialcrawl/SKILL.md"
```

Expected: approximately 140-160 lines (under the 200 target, well under the 500 skill-creator limit).

- [ ] **Step 3: Commit**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents"
git add socialcrawl/SKILL.md
git commit -m "feat: write SKILL.md with workflows, platform index, and error handling"
```

---

### Task 3: Write references/api-overview.md

**Files:**
- Create: `for-agents/socialcrawl/references/api-overview.md`

- [ ] **Step 1: Write api-overview.md**

Write the following exact content to `for-agents/socialcrawl/references/api-overview.md`:

```markdown
# SocialCrawl API Overview

## Base URL

```
https://api.socialcrawl.com
```

## Authentication

Pass your API key in the `x-api-key` header with every request:

```bash
curl -s -H "x-api-key: sc_your_api_key_here" \
  "https://api.socialcrawl.com/v1/tiktok/profile?handle=charlidamelio"
```

## Response Format

All successful responses follow this envelope:

```json
{
  "success": true,
  "platform": "tiktok",
  "endpoint": "/v1/tiktok/profile",
  "data": { ... },
  "credits_used": 1,
  "credits_remaining": 4999,
  "request_id": "req-XXXXX",
  "cached": false
}
```

Error responses:

```json
{
  "success": false,
  "error": {
    "type": "INSUFFICIENT_CREDITS",
    "message": "Your account has 0 credits remaining. This endpoint requires 1 credits.",
    "status": 402,
    "doc_url": "https://socialcrawl.com/docs/errors/insufficient-credits"
  },
  "credits_remaining": 0,
  "request_id": "req-XXXXX"
}
```

## Response Headers

| Header | Value |
|--------|-------|
| X-Request-Id | Unique request identifier (`req-XXXXX`) |
| X-Credits-Used | Credits consumed by this request |
| X-Credits-Remaining | Balance after deduction |
| X-Cache | `HIT` or `MISS` |

## Credit Tiers

| Tier | Cost | Count | Typical endpoints |
|------|------|-------|-------------------|
| standard | 1 credit | 81 endpoints | Profiles, posts, search, comments |
| advanced | 5 credits | 18 endpoints | Audience, ad libraries, trending |
| premium | 10 credits | 6 endpoints | Transcripts, AI analysis |

## Credit Balance

Check remaining credits:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/api/credits/balance"
```

Returns: `{ "balance": 4999 }`

## Raw Format

Add `?format=raw` to any endpoint to receive the original upstream response without unified schema transformation:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/tiktok/profile?handle=charlidamelio&format=raw"
```

## Error Codes

| Code | Status | Description | Credits |
|------|--------|-------------|---------|
| MISSING_API_KEY | 401 | No x-api-key header | Not charged |
| INVALID_API_KEY | 401 | Key malformed, not found, or revoked | Not charged |
| INSUFFICIENT_CREDITS | 402 | Balance too low | Not charged |
| INVALID_REQUEST | 400 | Missing required parameters | Not charged |
| ENDPOINT_NOT_FOUND | 404 | Unknown platform or resource | Not charged |
| RESOURCE_NOT_FOUND | 404 | Item not found on platform | Not charged |
| CONCURRENCY_LIMIT | 429 | Over 50 concurrent requests per key | Not charged |
| UPSTREAM_ERROR | 502 | Platform returned an error | Refunded |
| SERVICE_UNAVAILABLE | 503 | Circuit breaker open, retry in 30s | Refunded |
| INTERNAL_ERROR | 500 | Unexpected server error | Refunded |
```

- [ ] **Step 2: Commit**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents"
git add socialcrawl/references/api-overview.md
git commit -m "feat: add api-overview reference with auth, response format, errors, credits"
```

---

### Task 4: Write Major Platform References (TikTok, Instagram, YouTube, Facebook)

**Files:**
- Create: `for-agents/socialcrawl/references/tiktok.md`
- Create: `for-agents/socialcrawl/references/instagram.md`
- Create: `for-agents/socialcrawl/references/youtube.md`
- Create: `for-agents/socialcrawl/references/facebook.md`

Content for each file is derived from `codebase/apps/web/public/llms-{platform}.txt`. The format for every platform reference is identical:

```
# {Platform} ({N} endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| ... | ... | ... | ... |

## Parameter Details

- `param`: Description (e.g., `example_value`)

## Example

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/{platform}/{resource}?{param}={value}"
```
```

- [ ] **Step 1: Write references/tiktok.md**

Read `codebase/apps/web/public/llms-tiktok.txt` for exact endpoint details, then write `for-agents/socialcrawl/references/tiktok.md` with all 24 endpoints in the table format above. Include these parameter details:

- `handle`: TikTok username without @ symbol (e.g., `charlidamelio`)
- `url`: Full TikTok video URL (e.g., `https://www.tiktok.com/@charlidamelio/video/7321485815660738859`)
- `query`: Search keyword or phrase (e.g., `cooking recipes`)
- `clipId`: TikTok sound/song clip ID (e.g., `7252403792087040774`)
- `region`: ISO 3166-1 alpha-2 country code (e.g., `US`)
- `hashtag`: Hashtag without # symbol (e.g., `fyp`)

Example curl should use the `profile` endpoint with `handle=charlidamelio`.

- [ ] **Step 2: Write references/instagram.md**

Read `codebase/apps/web/public/llms-instagram.txt` for exact endpoint details, then write `for-agents/socialcrawl/references/instagram.md` with all 12 endpoints. Parameter details:

- `handle`: Instagram username without @ symbol (e.g., `instagram`)
- `url`: Full Instagram post/reel URL (e.g., `https://www.instagram.com/p/CwA1234abcd/`)
- `userId`: Instagram numeric user ID (e.g., `25025320`)
- `query`: Search keyword or phrase (e.g., `workout routine`)
- `id`: Instagram highlight ID (e.g., `17854360229135492`)
- `audio_id`: Instagram audio/song ID (e.g., `243313786724210`)

Example curl should use the `profile` endpoint with `handle=instagram`.

- [ ] **Step 3: Write references/youtube.md**

Read `codebase/apps/web/public/llms-youtube.txt` for exact endpoint details, then write `for-agents/socialcrawl/references/youtube.md` with all 11 endpoints. Parameter details:

- `handle`: YouTube channel handle without @ symbol (e.g., `MrBeast`)
- `url`: Full YouTube video URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
- `query`: Search keyword or phrase (e.g., `javascript tutorial`)
- `playlist_id`: YouTube playlist ID (e.g., `PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf`)
- `hashtag`: Hashtag without # symbol (e.g., `shorts`)

Example curl should use the `channel` endpoint with `handle=MrBeast`.

- [ ] **Step 4: Write references/facebook.md**

Read `codebase/apps/web/public/llms-facebook.txt` for exact endpoint details, then write `for-agents/socialcrawl/references/facebook.md` with all 12 endpoints. Parameter details:

- `url`: Full Facebook page/post/video URL (e.g., `https://www.facebook.com/Meta`)
- `id`: Facebook Ad Library ad ID (e.g., `23851234567890123`)
- `pageId`: Facebook page ID of advertiser (e.g., `20531316728`)
- `query`: Search keyword or phrase (e.g., `artificial intelligence`)

Example curl should use the `profile` endpoint with `url=https://www.facebook.com/Meta`.

- [ ] **Step 5: Commit**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents"
git add socialcrawl/references/tiktok.md socialcrawl/references/instagram.md socialcrawl/references/youtube.md socialcrawl/references/facebook.md
git commit -m "feat: add platform references for TikTok, Instagram, YouTube, Facebook"
```

---

### Task 5: Write Mid-Size Platform References (Twitter, LinkedIn, Reddit, Threads, Pinterest, Google)

**Files:**
- Create: `for-agents/socialcrawl/references/twitter.md`
- Create: `for-agents/socialcrawl/references/linkedin.md`
- Create: `for-agents/socialcrawl/references/reddit.md`
- Create: `for-agents/socialcrawl/references/threads.md`
- Create: `for-agents/socialcrawl/references/pinterest.md`
- Create: `for-agents/socialcrawl/references/google.md`

Same table format as Task 4. Source content from `llms-full.txt` (already read above — all endpoint details are captured there).

- [ ] **Step 1: Write references/twitter.md**

6 endpoints. Parameter details:
- `handle`: Twitter username without @ symbol (e.g., `elonmusk`)
- `url`: Full tweet/community URL (e.g., `https://x.com/elonmusk/status/1234567890`)

Example curl: `profile` endpoint with `handle=elonmusk`.

- [ ] **Step 2: Write references/linkedin.md**

6 endpoints. Parameter details:
- `url`: Full LinkedIn profile/company/post/ad URL (e.g., `https://www.linkedin.com/in/williamhgates/`)
- `company`: Company name or LinkedIn company URL (e.g., `Microsoft`)

Example curl: `profile` endpoint with `url=https://www.linkedin.com/in/williamhgates/`.

- [ ] **Step 3: Write references/reddit.md**

7 endpoints. Parameter details:
- `subreddit`: Subreddit name without r/ prefix (e.g., `technology`)
- `url`: Full Reddit post URL (e.g., `https://www.reddit.com/r/technology/comments/abc123/example_post/`)
- `query`: Search keyword or phrase (e.g., `best programming languages 2024`)
- `id`: Reddit ad ID (e.g., `t3_abc123`)

Example curl: `subreddit` endpoint with `subreddit=technology`.

- [ ] **Step 4: Write references/threads.md**

5 endpoints. Parameter details:
- `handle`: Threads username without @ symbol (e.g., `zuck`)
- `url`: Full Threads post URL (e.g., `https://www.threads.net/@zuck/post/CwABCDEFGHI`)
- `query`: Search keyword or phrase (e.g., `artificial intelligence`)

Example curl: `profile` endpoint with `handle=zuck`.

- [ ] **Step 5: Write references/pinterest.md**

4 endpoints. Parameter details:
- `query`: Search keyword or phrase (e.g., `home decor ideas`)
- `url`: Full Pinterest pin/board URL (e.g., `https://www.pinterest.com/pin/1234567890/`)
- `handle`: Pinterest username (e.g., `pinterest`)

Example curl: `search` endpoint with `query=home decor ideas`.

- [ ] **Step 6: Write references/google.md**

4 endpoints. Parameter details:
- `query`: Search keyword or phrase (e.g., `best restaurants in London`)
- `url`: Full Google ad/Ads Transparency Center URL (e.g., `https://adstransparency.google.com/advertiser/AR12345678901234567`)
- `domain`: Company domain name (e.g., `nike.com`)

Example curl: `search` endpoint with `query=best restaurants in London`.

- [ ] **Step 7: Commit**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents"
git add socialcrawl/references/twitter.md socialcrawl/references/linkedin.md socialcrawl/references/reddit.md socialcrawl/references/threads.md socialcrawl/references/pinterest.md socialcrawl/references/google.md
git commit -m "feat: add platform references for Twitter, LinkedIn, Reddit, Threads, Pinterest, Google"
```

---

### Task 6: Write Small Platform References (Twitch, Truth Social, Snapchat, Kick, Amazon, Linktree, Linkbio, Linkme, Komi, Pillar, Utility)

**Files:**
- Create: `for-agents/socialcrawl/references/twitch.md`
- Create: `for-agents/socialcrawl/references/truthsocial.md`
- Create: `for-agents/socialcrawl/references/snapchat.md`
- Create: `for-agents/socialcrawl/references/kick.md`
- Create: `for-agents/socialcrawl/references/amazon.md`
- Create: `for-agents/socialcrawl/references/linktree.md`
- Create: `for-agents/socialcrawl/references/linkbio.md`
- Create: `for-agents/socialcrawl/references/linkme.md`
- Create: `for-agents/socialcrawl/references/komi.md`
- Create: `for-agents/socialcrawl/references/pillar.md`
- Create: `for-agents/socialcrawl/references/utility.md`

Same table format. Each of these is small (1-3 endpoints, ~15-25 lines). Source from `llms-full.txt`.

- [ ] **Step 1: Write references/twitch.md**

2 endpoints: `profile` (`handle`, e.g., `ninja`) and `clip` (`url`).
Example curl: `profile` endpoint with `handle=ninja`.

- [ ] **Step 2: Write references/truthsocial.md**

3 endpoints: `profile` (`handle`, e.g., `realDonaldTrump`), `user/posts` (`handle`), `post` (`url`).
Example curl: `profile` endpoint with `handle=realDonaldTrump`.

- [ ] **Step 3: Write references/snapchat.md**

1 endpoint: `profile` (`handle`, e.g., `djkhaled305`).
Example curl: `profile` endpoint with `handle=djkhaled305`.

- [ ] **Step 4: Write references/kick.md**

1 endpoint: `clip` (`url`, e.g., `https://kick.com/xqc/clips/clip_abc123`).
Example curl: `clip` endpoint.

- [ ] **Step 5: Write references/amazon.md**

1 endpoint: `shop` (`url`, e.g., `https://www.amazon.com/shop/influencer123`).
Example curl: `shop` endpoint.

- [ ] **Step 6: Write references/linktree.md**

1 endpoint: `page` (`url`, e.g., `https://linktr.ee/charlidamelio`).
Example curl: `page` endpoint.

- [ ] **Step 7: Write references/linkbio.md**

1 endpoint: `page` (`url`, e.g., `https://lnk.bio/example`).
Example curl: `page` endpoint.

- [ ] **Step 8: Write references/linkme.md**

1 endpoint: `page` (`url`, e.g., `https://linkme.bio/example`).
Example curl: `page` endpoint.

- [ ] **Step 9: Write references/komi.md**

1 endpoint: `page` (`url`, e.g., `https://komi.io/example`).
Example curl: `page` endpoint.

- [ ] **Step 10: Write references/pillar.md**

1 endpoint: `page` (`url`, e.g., `https://pillar.io/example`).
Example curl: `page` endpoint.

- [ ] **Step 11: Write references/utility.md**

1 endpoint: `age-gender` (`url` — direct image URL, e.g., `https://example.com/photo.jpg`). Credit cost: 10 (premium).
Example curl: `age-gender` endpoint.

- [ ] **Step 12: Commit**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents"
git add socialcrawl/references/twitch.md socialcrawl/references/truthsocial.md socialcrawl/references/snapchat.md socialcrawl/references/kick.md socialcrawl/references/amazon.md socialcrawl/references/linktree.md socialcrawl/references/linkbio.md socialcrawl/references/linkme.md socialcrawl/references/komi.md socialcrawl/references/pillar.md socialcrawl/references/utility.md
git commit -m "feat: add platform references for remaining 11 platforms"
```

---

### Task 7: Validate and Package the Skill

**Files:**
- Read: `for-agents/socialcrawl/SKILL.md` (verify)
- Read: all `for-agents/socialcrawl/references/*.md` (verify count)
- Create: `for-agents/socialcrawl.skill` (output of package_skill.py)

- [ ] **Step 1: Verify file count and structure**

```bash
find "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents/socialcrawl" -type f -name "*.md" | wc -l
```

Expected: 23 files (1 SKILL.md + 1 api-overview.md + 21 platform files).

```bash
ls "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents/socialcrawl/references/"
```

Expected: 22 .md files listed (api-overview + 21 platforms).

- [ ] **Step 2: Verify SKILL.md frontmatter is valid YAML**

Read `for-agents/socialcrawl/SKILL.md` and confirm:
- Has `---` delimiters
- Has `name: socialcrawl`
- Has `description:` with content
- No other frontmatter fields

- [ ] **Step 3: Verify no TODO placeholders remain**

```bash
grep -r "TODO" "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents/socialcrawl/" || echo "No TODOs found"
```

Expected: "No TODOs found"

- [ ] **Step 4: Package the skill**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl"
python "C:/Users/doodd/.claude/skills/skill-creator/scripts/package_skill.py" "for-agents/socialcrawl" "for-agents"
```

Expected: Validation passes, `for-agents/socialcrawl.skill` file created.

- [ ] **Step 5: Verify the .skill file**

```bash
ls -la "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents/socialcrawl.skill"
```

Expected: File exists, reasonable size (should be under 50KB since it's all text).

- [ ] **Step 6: Commit the packaged skill**

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents"
git add socialcrawl.skill
git commit -m "feat: package socialcrawl.skill for distribution"
```

---

### Task 8: Final Review

- [ ] **Step 1: Review SKILL.md for skill-creator compliance**

Check against skill-creator best practices:
- Frontmatter has only `name` and `description` (no extra fields)
- Description includes what the skill does AND when to use it
- Body is under 500 lines
- References are one level deep from SKILL.md
- No README.md, CHANGELOG.md, or other extraneous files
- No scripts/ or assets/ directories (we only need references/)

- [ ] **Step 2: Spot-check 3 reference files for accuracy**

Read `references/tiktok.md`, `references/linkedin.md`, and `references/utility.md`. Cross-reference against `llms-full.txt` to verify:
- Correct endpoint count
- Correct parameter names and examples
- Correct credit tiers (standard/advanced/premium)
- Curl example uses correct base URL (`https://api.socialcrawl.com`)

- [ ] **Step 3: Verify platform index in SKILL.md matches reference files**

Count the rows in the SKILL.md platform table (should be 21). Count the reference files in references/ (should be 22 including api-overview.md). Every platform in the table should have a matching reference file.

- [ ] **Step 4: Final commit with any fixes**

If any issues were found and fixed:

```bash
cd "c:/Users/doodd/Documents/RidioCompany/Projects/SocialCrawl/for-agents"
git add -A socialcrawl/
git commit -m "fix: address review findings in socialcrawl skill"
```
