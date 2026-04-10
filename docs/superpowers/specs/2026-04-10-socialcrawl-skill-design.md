# SocialCrawl Skill — Design Spec

> A Claude Code skill that gives AI agents and users full access to the SocialCrawl unified social media data API.

---

## Problem

SocialCrawl provides a unified API for 21 social media platforms (105 endpoints), but using it requires reading docs, knowing endpoint paths, understanding parameters, and handling auth. An AI agent or non-technical user should be able to say "get me the TikTok profile for @charlidamelio" and get results immediately — without reading any documentation.

## Solution

A distributable `.skill` file that teaches Claude how to use the SocialCrawl API. The skill contains all endpoint documentation, authentication handling, and workflow logic needed to make live API calls, generate code, and check credit balances.

## Audience

Both equally:
- **AI-agent builders** — Agents that call SocialCrawl programmatically as part of larger workflows
- **Non-technical users** — People who ask Claude to fetch social media data in natural language

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| API interaction | Live calls + code generation | Differentiates from just reading docs |
| API key config | Env var preferred, inline fallback | Low friction for first use, proper setup for repeat use |
| Endpoint structure | Tiered loading (index + per-platform refs) | Progressive disclosure, context-efficient |
| Scope | SocialCrawl-only | YAGNI — separate skill per product |
| Output format | Raw JSON | Let user/agent decide presentation |
| Billing awareness | Credit balance check only | Useful safeguard without dashboard bloat |
| First-use flow | Lean guided onboarding | Verify key works, then get out of the way |

---

## File Structure

```
for-agents/socialcrawl/
├── SKILL.md                          # Core instructions (~200 lines)
└── references/
    ├── api-overview.md               # Auth, response format, errors, credits (~80 lines)
    ├── tiktok.md                     # 24 endpoints
    ├── instagram.md                  # 12 endpoints
    ├── youtube.md                    # 11 endpoints
    ├── facebook.md                   # 12 endpoints
    ├── twitter.md                    # 6 endpoints
    ├── linkedin.md                   # 6 endpoints
    ├── reddit.md                     # 7 endpoints
    ├── threads.md                    # 5 endpoints
    ├── pinterest.md                  # 4 endpoints
    ├── google.md                     # 4 endpoints
    ├── twitch.md                     # 2 endpoints
    ├── truthsocial.md               # 3 endpoints
    ├── snapchat.md                   # 1 endpoint
    ├── kick.md                       # 1 endpoint
    ├── amazon.md                     # 1 endpoint
    ├── linktree.md                   # 1 endpoint
    ├── linkbio.md                    # 1 endpoint
    ├── linkme.md                     # 1 endpoint
    ├── komi.md                       # 1 endpoint
    ├── pillar.md                     # 1 endpoint
    └── utility.md                    # 1 endpoint (age-gender detection)
```

No `scripts/` or `assets/` directories — Claude uses Bash for API calls, no bundled executables needed.

---

## SKILL.md Content (~200 lines)

### Frontmatter

```yaml
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
```

### Body Sections

1. **API Key Resolution (~15 lines)**
   - Check `SOCIALCRAWL_API_KEY` env var first
   - If not found, ask user for their key
   - Suggest setting env var for future sessions: `export SOCIALCRAWL_API_KEY=sc_xxxxx`

2. **First-Use Onboarding (~10 lines)**
   - Brief intro: "SocialCrawl: one API key, 21 platforms, 105 endpoints"
   - Verify key with a lightweight call: `GET /v1/tiktok/profile?handle=tiktok` (costs 1 credit — mention this to user before executing)
   - Confirm it works, then become purely reactive

3. **Platform Index (~30 lines)**
   - Compact table: platform name, endpoint count, reference file path
   - Always in context — answers "what platforms do you support?" without loading references
   - Example row: `| TikTok | 24 | references/tiktok.md |`

4. **Workflow Routing (~20 lines)**
   - Conditional workflow pattern:
     - **Fetch data** → Load platform reference → execute curl → return JSON
     - **Generate code** → Load platform reference → produce code snippet
     - **Ask about capabilities** → Answer from index + load api-overview.md if needed
     - **Check credits** → Hit balance endpoint

5. **Making API Calls (~25 lines)**
   - Base URL: `https://api.socialcrawl.com`
   - Auth header: `x-api-key: {KEY}`
   - URL pattern: `/v1/{platform}/{resource}?{params}`
   - Curl template:
     ```
     curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
       "https://api.socialcrawl.com/v1/{platform}/{resource}?{param}={value}"
     ```

6. **Credit Awareness (~10 lines)**
   - Before executing: note credit tier from platform reference (standard=1, advanced=5, premium=10)
   - After executing: report `credits_used` and `credits_remaining` from response
   - Balance check: `GET /api/credits/balance` with same auth header

7. **Error Handling (~15 lines)**
   - Compact table of 10 error codes with user-facing message for each:
     - 401 MISSING_API_KEY / INVALID_API_KEY → "Check your API key"
     - 402 INSUFFICIENT_CREDITS → "Top up at socialcrawl.com/dashboard/billing"
     - 404 ENDPOINT_NOT_FOUND → "That endpoint doesn't exist"
     - 404 RESOURCE_NOT_FOUND → "That profile/post wasn't found"
     - 429 CONCURRENCY_LIMIT → "Too many concurrent requests, try again"
     - 502 UPSTREAM_ERROR → "Platform temporarily unavailable, credits refunded"
     - 503 SERVICE_UNAVAILABLE → "Platform circuit breaker open, credits refunded"
     - 500 INTERNAL_ERROR → "Unexpected error, credits refunded"

8. **Reference File Index (~15 lines)**
   - When to read `references/api-overview.md`: user asks about auth, response format, errors, or credits in general
   - When to read `references/{platform}.md`: user asks about or wants to call a specific platform

---

## Reference File Design

### api-overview.md (~80 lines)

- Base URL
- Authentication (x-api-key header)
- Response envelope (success example + error example)
- Response headers (X-Request-Id, X-Credits-Used, X-Credits-Remaining, X-Cache)
- Credit tiers table
- Credit balance endpoint
- Full error codes table
- `?format=raw` parameter

### Per-Platform Reference Files (~15-80 lines each)

Identical structure across all 21 platforms:

```markdown
# {Platform} ({N} endpoints)

## Endpoints

| Resource | Params | Tier | Description |
|----------|--------|------|-------------|
| profile | `handle` | standard | Get user profile |
| ... | ... | ... | ... |

## Parameter Details

- `handle`: Username without @ symbol (e.g., `charlidamelio`)
- `url`: Full post URL (e.g., `https://tiktok.com/@user/video/123`)

## Example

curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://api.socialcrawl.com/v1/{platform}/profile?handle=example"
```

Content derived from existing `llms-{platform}.txt` generated files.

---

## Workflows

### 1. Live Data Fetch (primary)

```
User asks for social media data
  → Identify platform + resource from request
  → Read references/{platform}.md
  → Resolve API key (env var → ask user)
  → Construct curl command from endpoint table
  → Execute via Bash
  → Return raw JSON response
  → Note credits_used and credits_remaining
```

### 2. Code Generation

```
User asks for code to call SocialCrawl
  → Identify platform + resource + target language
  → Read references/{platform}.md
  → Generate code snippet (curl/JS/Python/etc.)
  → Use env var reference for API key
  → Present code without executing
```

### 3. Credit Balance Check

```
User asks about credits/balance
  → Resolve API key
  → Execute: GET /api/credits/balance
  → Return balance
```

### Edge Cases

- **Ambiguous platform** — Ask user which platform they mean
- **Missing API key** — Ask for it, suggest env var setup
- **401 response** — "Your API key appears invalid. Check your SocialCrawl dashboard."
- **402 response** — "You're out of credits. Visit socialcrawl.com/dashboard/billing to top up."
- **Multi-platform requests** — Load multiple reference files, make sequential calls

---

## Context Budget

| Component | Lines | When loaded |
|---|---|---|
| SKILL.md (always) | ~200 | Every trigger |
| api-overview.md | ~80 | When asked about auth/errors/credits |
| One platform reference | ~15-80 | When calling a specific platform |
| **Typical session** | **~250-300** | Much less than the 1,500-line alternative |

---

## Content Source

All reference file content is derived from existing generated artifacts in the SocialCrawl codebase:

| Source | Target |
|---|---|
| `apps/web/public/llms-{platform}.txt` (21 files) | `references/{platform}.md` (21 files) |
| `apps/web/public/llms-full.txt` | `references/api-overview.md` (subset) |
| `codebase/docs/features/SOCIAL-API-BACKEND.md` | SKILL.md platform index, error codes |

No content needs to be written from scratch — it's reformatting and compacting existing documentation.

---

## Distribution

- Packaged via skill-creator's `package_skill.py` into `socialcrawl.skill`
- Hosted in the `for-agents/` public repo
- Users install by adding the skill to their Claude Code configuration
- No external dependencies — everything self-contained in the skill

---

## What This Skill Does NOT Include

- Dashboard endpoints beyond credit balance (usage analytics, activity logs)
- Response formatting or visualization — raw JSON only
- MCP server functionality — potential future complement, not a replacement
- Multi-product support — SocialCrawl only, other Ridio products get separate skills
