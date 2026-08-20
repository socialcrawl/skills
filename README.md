<div align="center">

# @socialcrawl

**Give your AI agent access to 48 social, commerce + research platforms through a single API**

[![Platforms](https://img.shields.io/badge/Platforms-48-blue?style=flat-square)](https://socialcrawl.dev)
[![Endpoints](https://img.shields.io/badge/Endpoints-381-green?style=flat-square)](https://socialcrawl.dev/docs)
[![skills.sh](https://img.shields.io/badge/skills.sh-listed-black?style=flat-square)](https://skills.sh)
[![Agents](https://img.shields.io/badge/Agents-40+-blueviolet?style=flat-square)](https://skills.sh)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Overview](#overview) | [Installation](#installation) | [Setup](#setup) | [Usage](#usage) | [Platforms](#supported-platforms) | [Credits](#credit-system)

</div>

---

## Overview

`@socialcrawl` is a skill for AI coding agents (Claude Code, Cursor, Windsurf, Codex, Gemini CLI, and [40+ more](https://skills.sh)) that lets your agent fetch live social, commerce, and research data — profiles, posts, comments, search results, transcripts, ad libraries, product/app/business reviews, places & hotels, prediction markets, news, finance quotes, AI-grounded answers, a universal cross-platform search, cross-platform **Prism** composites, and scheduled **Monitors** — from 48 platforms (381 endpoints) using the [SocialCrawl API](https://socialcrawl.dev).

One API key. One consistent response format. Every platform. Every response is wrapped in a unified envelope with transparent credit accounting. Social archetypes (`Author`, `Post`, `Comment`) go through per-platform **field maps** that normalize dozens of quirky upstream shapes into a single schema — plus four computed fields (`engagement_rate`, `language`, `content_category`, `estimated_reach`) that most data APIs don't give you. Commerce, review, place, and app-store endpoints share first-class canonical `Product` / `Review` / `Seller` / `Place` / `App` schemas.

**What the skill does:**
- Fetches social, commerce + research data on your behalf (profiles, posts, comments, search, trending, retail products across Amazon/Walmart/Target/eBay/Home Depot, reviews, app-store data, places, prediction markets, web research)
- Runs a universal cross-platform search that fans out to 17 sources in parallel (sync JSON or SSE streaming, 20 credits flat)
- Runs cross-platform **Prism** composites (`/v1/prism/*`) — one call that fans out across many platforms into a unified report
- Creates and manages scheduled **Monitors** that re-run any recipe on a cadence and deliver each result to a signed webhook
- Generates working code snippets that call the SocialCrawl API
- Answers questions about endpoints, parameters, and capabilities
- Scrapes, crawls, and monitors arbitrary web pages, and drives interactive browser sessions (`/v1/web/*`)
- Gives exact per-endpoint pricing for all 381 endpoints — cost, tier, cache TTL, and the full rule behind every metered endpoint (bundled pricing reference)
- Quotes the cost before spending your credits, and reports the real charge afterwards
- Checks your credit balance

## Installation

### Via skills.sh (recommended)

Works with Claude Code, Cursor, Windsurf, Codex, Gemini CLI, and 40+ other agents:

```bash
npx skills add socialcrawl/skills
```

Install globally (available in all projects):

```bash
npx skills add socialcrawl/skills -g
```

Update an existing installation to the latest published skill:

```bash
npx skills update socialcrawl --yes
```

Prefer a single downloadable package? [Download the latest `socialcrawl.skill`](https://github.com/socialcrawl/skills/raw/main/socialcrawl.skill). That URL always follows the `main` branch.

### Via ClawHub

```bash
npx clawhub@latest install socialcrawl
```

### Via Git (manual)

```bash
# Clone the repository, then copy the actual skill directory.
git clone --depth 1 https://github.com/socialcrawl/skills socialcrawl-skills

# Project-scoped (shared via version control)
mkdir -p .claude/skills
cp -R socialcrawl-skills/socialcrawl .claude/skills/socialcrawl

# User-wide (available in all projects)
mkdir -p ~/.claude/skills
cp -R socialcrawl-skills/socialcrawl ~/.claude/skills/socialcrawl
```

Pull `socialcrawl-skills`, then repeat the copy step to update a manual installation. Cloning the repository directly to `.claude/skills/socialcrawl` is not supported because the repository root is a distribution workspace, not the skill directory itself.

### Verify installation

Once installed, invoke the skill in Claude Code:

```
/socialcrawl
```

Or simply ask your agent to fetch social media data — the skill activates automatically when it detects relevant requests.

## Setup

### 1. Get your API key

Sign up at [socialcrawl.dev](https://socialcrawl.dev/dashboard) and grab your API key from the dashboard. Every account starts with **100 free credits** — no credit card required.

### 2. Set the environment variable

```bash
export SOCIALCRAWL_API_KEY="sc_your_api_key_here"
```

Add this to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) so it persists across sessions.

> [!TIP]
> If the environment variable is not set, the skill will ask you to configure it or `~/.config/socialcrawl/api_key` outside the chat. It never asks you to paste a secret into the conversation.

## Usage

### Fetch data

Ask your agent in natural language:

```
Get the TikTok profile for @charlidamelio
```

```
Search YouTube for "machine learning" videos
```

```
Get the comments on this Instagram post: https://instagram.com/p/CwA1234abcd
```

The skill identifies the platform and endpoint, makes the API call, and returns structured JSON.

### Generate code

```
Generate JavaScript code to fetch a Reddit user's posts via SocialCrawl
```

The skill outputs a working snippet using the `SOCIALCRAWL_API_KEY` environment variable.

### Check your balance

```
What's my SocialCrawl credit balance?
```

### Example API call

Under the hood, the skill constructs standard HTTP requests:

```bash
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/tiktok/profile?handle=charlidamelio"
```

Every response follows a unified envelope:

```json
{
  "success": true,
  "platform": "tiktok",
  "endpoint": "/v1/tiktok/profile",
  "data": {
    "author": {
      "id": "5831967",
      "username": "charlidamelio",
      "display_name": "charli d'amelio",
      "avatar_url": "https://...",
      "bio": "...",
      "verified": true,
      "followers": 156800000,
      "following": 1300,
      "posts_count": 2800,
      "likes_count": 11600000000
    },
    "computed": {
      "engagement_rate": 0.074,
      "language": "en",
      "content_category": "entertainment",
      "estimated_reach": 1163120000
    }
  },
  "credits_used": 1,
  "credits_remaining": 99,
  "request_id": "req-a1b2c3d4e5f6",
  "cached": false
}
```

> [!NOTE]
> Add `?format=raw` to any endpoint to receive the original upstream response without unified schema transformation or computed fields.

## Supported Platforms

| Platform | Endpoints | Data Available |
|----------|-----------|----------------|
| **LinkedIn** | 44 | Profiles, company pages, posts & reactions, comments & replies, people & job search, company people/jobs/insights, profile sub-resources (experiences, education, skills, certifications, recommendations…), groups, Ad Library, post search, transcripts, profile-360 |
| **Instagram** | 33 | Profiles, basic profiles, posts, reels, comments, single-comment lookup, highlights, followers/following/similar, post likers & reshare stats, paginated posts/reels-360, tagged & location posts, stories + download, engagement analytics, hashtag/profile/location/music/username search, audio & trending reels/music, transcripts, profile-360 |
| **Prism** | 33 | Cross-platform composites — URL lookup, comment harvesting, batch post stats & profile lookups, brand mentions, demand signals, AI visibility, crisis radar/post-mortem, reputation, share-of-voice, creator vetting, handle audit, AI consensus answers, video/app/product intelligence |
| **YouTube** | 28 | Channels, videos, shorts, playlists & items, comments, search (+ advanced & suggestions), trending videos & shorts, sponsors, community posts, live streams, transcripts (single + 100-id batch), batch video/channel lookups, media files, profile-360 |
| **Facebook** | 23 | Pages, posts, comments, reels (incl. paginated reels-360), photos, groups, events, Marketplace, Ad Library, transcripts, profile-360 |
| **Web** | 22 | Scrape (markdown/screenshot), web search, site crawl & map, structured extraction, browser-agent jobs, page-change monitors, and interactive browser sessions — the general-purpose surface for any URL |
| **TikTok** | 21 | Profiles, videos, comments, single-comment lookup, on-screen text OCR, followers, search, trending, hashtags, songs, live, transcripts, audience demographics, profile-360 |
| **Naver** | 14 | Korean search corpora (blog, news, cafe, KnowledgeiN, local, shopping, image, web, book, academic, encyclopedia, adult-check, errata) plus Data Lab search-volume + shopping-insight trends and a brief summary endpoint |
| **GitHub** | 12 | Profiles, repos, READMEs, releases, issues, top issues, PRs, search, composite dossiers, profile-velocity analytics |
| **Content Analysis** | 10 | Cross-web brand mentions with sentiment, phrase & category trends over time, rating histograms, category taxonomy, reference data |
| **Google** | 10 | Web search, Ad Library, Business Profiles, multi-source + extended reviews, updates, Q&A, hotels |
| **Apple App Store** | 9 | App search, search suggestions, full app details, reviews, store charts, paginated listings DB, reference data |
| **Google Play** | 9 | App search, search suggestions, full app details, reviews, store charts, paginated listings DB, reference data |
| **Reddit** | 8 | Subreddits, posts, post detail, comments, search, subreddit search, transcripts, omni-search VoC sweep |
| **Twitter/X** | 8 | Profiles, tweets, communities, transcripts, AI-powered freeform search (Grok + `x_search`), profile-360 |
| **Spotify** | 6 | Artists, tracks, albums, podcasts, episodes, search |
| **Threads** | 6 | Profiles, posts, post comments, post search, user search |
| **Amazon** | 5 | Product search, ASIN details, reviews, sellers & offers, shop pages |
| **Pinterest** | 5 | Pin search, pin details, boards, URL save-counts |
| **Rumble** | 5 | Channels, videos, search, comments, transcripts |
| **Target** | 5 | Product details, reviews, category browse, store lookup, category taxonomy |
| **TikTok Shop** | 5 | Products, product reviews, shop listings, search, creator showcases |
| **Walmart** | 5 | Product search, product details, reviews, marketplace offers, category browse |
| **Google Shopping** | 4 | Product search, product details, cross-retailer reviews, sellers |
| **Hacker News** | 4 | Search, stories, story comments, profiles |
| **Tavily** | 4 | Web search (with LLM answer), URL extraction, sitegraph, multi-page crawl |
| **Twitch** | 4 | Profiles, clips, videos, stream schedules |
| **Utility** | 4 | Free (0-credit) API self-discovery — list every live endpoint, explain one, fetch the whole agent-context corpus, or get a ready-to-run first call |
| **Bluesky** | 3 | Profiles, posts |
| **Google Finance** | 3 | Instrument quotes, markets overview, ticker search |
| **Kwai** | 3 | Profiles, posts |
| **Search (universal)** | 3 | Cross-platform meta-search across 17 sources (sync JSON / SSE streaming, 20cr flat), a forums lane, and a metered multi-country news lane |
| **Truth Social** | 3 | Profiles, posts |
| **Google Trends** | 2 | Interest over time (multi-keyword, normalized), related + rising queries |
| **Home Depot** | 2 | Product details and product reviews |
| **Tripadvisor** | 2 | Place/business search, traveler reviews (with auto-translation metadata) |
| **Trustpilot** | 2 | Business search, company reviews |
| **eBay** | 2 | Listing search and single-item detail |
| **Google News** | 1 | Real-time Google News SERP search |
| **Kick** | 1 | Clips |
| **Komi** | 1 | Link pages |
| **Linkbio** | 1 | Link pages |
| **Linkme** | 1 | Link pages |
| **Linktree** | 1 | Link pages |
| **Perplexity** | 1 | Web-grounded research (LLM answer + cited sources) |
| **Pillar** | 1 | Link pages |
| **Polymarket** | 1 | Prediction-market multi-query research |
| **Snapchat** | 1 | Profiles |

**Total: 381 endpoints across 48 platforms** — plus the stateful **Monitors** family (`/v1/monitors/*`, scheduled recipe runs with webhook delivery), which is not counted in the endpoint total.

## Credit System

Every API call costs credits based on its complexity:

| Tier | Cost | Endpoints | Examples |
|------|------|-----------|----------|
| **Standard** | 1 credit | 175 | Profiles, posts, search, comments, Naver corpora, GitHub, HN, Tavily, Perplexity, reference data |
| **Advanced** | 5 credits | 102 | Audience demographics, ad libraries, trending, app data, retail catalogs, business/place reviews, Google + Naver trends, LinkedIn social graph + jobs, Instagram relationship/discovery data |
| **Premium** | 10 credits | 17 | Video transcripts, LinkedIn people/job search + reactions, app listings search, web agent jobs |
| **Custom (flat / request-shaped)** | varies by request | 87 | Free discovery, fixed composites, per-row batches, per-probe AI visibility, per-page crawl and search, browser sessions, and recurring monitors |

### Pricing

| Plan | Price | Credits | Per 1k Credits |
|------|-------|---------|----------------|
| **Free** | £0 | 100 (one-time) | — |
| **Starter** | £15 | 2,500 | £6.00 |
| **Growth** | £49 | 20,000 | £2.45 |
| **Pro** | £299 | 150,000 | £1.99 |
| **Enterprise** | Contact | Custom | Custom |

Credits never expire. Pay-as-you-go, no monthly commitments. Failed upstream calls, open circuit breakers, and internal errors auto-refund credits.

> [!IMPORTANT]
> The skill shows a request-level cost gate before every paid call. It includes the billing unit, the row/page/probe/runtime arithmetic, the upfront hold or safe maximum, and the refund rule, then reports the real `credits_used` afterwards.

## Skill Contents

The installed skill contains:

```
socialcrawl/
├── LICENSE               # MIT terms included with every installable copy
├── SKILL.md              # Main skill definition
└── references/
    ├── api-overview.md    # Auth, response envelope, unified schemas, pagination, caching, idempotency, errors
    ├── cost-gate.md       # Mandatory request-level pricing formulas and preflight format
    ├── pricing.md         # Exact credit cost for every one of the 381 endpoints + credit packs
    ├── prism.md           # Cross-platform Prism composite recipes (/v1/prism/*)
    ├── monitors.md        # Scheduled recipe runs + webhook delivery (/v1/monitors/*)
    ├── search.md          # Universal cross-platform search (/v1/search/everywhere + /forums)
    ├── tiktok.md          # TikTok endpoints & parameters
    ├── instagram.md       # Instagram endpoints & parameters
    ├── youtube.md         # YouTube endpoints & parameters
    ├── facebook.md        # Facebook endpoints & parameters
    ├── twitter.md         # Twitter/X endpoints (incl. ai-search)
    ├── amazon.md          # Amazon product search, details, reviews, sellers
    ├── google_shopping.md # Google Shopping products, reviews, sellers
    ├── google_play.md     # Google Play app data, reviews, charts
    ├── app_store.md       # Apple App Store app data, reviews, charts
    ├── trustpilot.md      # Trustpilot business search + reviews
    ├── tripadvisor.md     # Tripadvisor places + traveler reviews
    ├── content_analysis.md# Cross-web brand mentions + sentiment
    ├── github.md          # GitHub endpoints & parameters
    ├── naver.md           # Naver Korean search corpora
    ├── google_news.md     # Google News SERP search
    ├── google_finance.md  # Instrument quotes, markets, ticker search
    ├── web.md             # Scrape, search, crawl, map, agent jobs, monitors, sessions
    ├── google_trends.md   # Interest over time + rising queries
    ├── walmart.md         # Walmart products, reviews, offers, categories
    ├── target.md          # Target products, reviews, categories, stores
    ├── ebay.md            # eBay listing search + item detail
    ├── home_depot.md      # Home Depot products + reviews
    ├── utility.md         # Free API self-discovery endpoints (0 credits)
    └── ...                # 22 more platform references
```

The skill reads the appropriate reference file for each platform on demand, keeping context usage minimal.

## Error Handling

The skill handles common API errors automatically:

| Error | What happens |
|-------|-------------|
| Missing/invalid API key | Asks you to configure or rotate it outside chat; never prints or persists a pasted secret |
| Insufficient credits | Tells you your balance and links to billing |
| Resource not found | Reports that the profile/post wasn't found |
| Platform unavailable | Reports the outage; credits are refunded automatically |
| Rate limited (600 req/min or 50 concurrent) | Honors `Retry-After` and backs off; the throttled call is never billed |
| Wrong HTTP method | Every endpoint reference states its real verb, so batch/web/monitor routes are called as POST/PATCH/DELETE |

## Links

- [SocialCrawl Website](https://socialcrawl.dev)
- [API Documentation](https://socialcrawl.dev/docs)
- [Dashboard & API Keys](https://socialcrawl.dev/dashboard)
- [Billing & Credits](https://socialcrawl.dev/dashboard/billing)

## Maintaining the release

Edit `.agents/skills/socialcrawl`, which is the canonical source. Then regenerate the installable directory copies and deterministic `socialcrawl.skill` archive:

```bash
python scripts/build_skill.py
```

Before publishing, run the same checks used in CI:

```bash
python scripts/build_skill.py --check
python -m unittest discover -s tests -v
```

The release check fails when the licence, pricing safeguards, directory copies, or downloadable archive are missing or stale.

## Licence

This repository is available under the [MIT License](LICENSE). You may reuse and adapt the skill, including its key-resolution and error-handling guidance, in public plugins and derivative skills. Retaining the included copyright and permission notice is sufficient attribution; a link back to `github.com/socialcrawl/skills` is appreciated but not required by the licence.
