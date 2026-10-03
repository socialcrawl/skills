<div align="center">

# @socialcrawl

**Give your AI agent access to 67 social, commerce + research platforms through a single API**

[![Platforms](https://img.shields.io/badge/Platforms-68-blue?style=flat-square)](https://socialcrawl.dev)
[![Endpoints](https://img.shields.io/badge/Endpoints-645-green?style=flat-square)](https://socialcrawl.dev/docs)
[![skills.sh](https://img.shields.io/badge/skills.sh-listed-black?style=flat-square)](https://skills.sh)
[![Agents](https://img.shields.io/badge/Agents-40+-blueviolet?style=flat-square)](https://skills.sh)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Overview](#overview) | [Installation](#installation) | [Setup](#setup) | [Usage](#usage) | [Platforms](#supported-platforms) | [Credits](#credit-system)

</div>

---

## Overview

`@socialcrawl` is a skill for AI coding agents (Claude Code, Cursor, Windsurf, Codex, Gemini CLI, and [40+ more](https://skills.sh)) that lets your agent fetch live social, commerce, and research data — profiles, posts, comments, search results, transcripts, ad libraries, product/app/business reviews, places & hotels, prediction markets, news, finance quotes, AI-grounded answers, job listings and salary bands, market quotes and financial statements, congressional trading disclosures, a universal cross-platform search, cross-platform **Prism** composites, scheduled **Monitors**, and audience-filtered **Cohorts** — from 68 platforms (645 endpoints) using the [SocialCrawl API](https://socialcrawl.dev).

One API key. One consistent response format. Every platform. Every response is wrapped in a unified envelope with transparent credit accounting. Social archetypes (`Author`, `Post`, `Comment`) go through per-platform **field maps** that normalize dozens of quirky upstream shapes into a single schema — plus four computed fields (`engagement_rate`, `language`, `content_category`, `estimated_reach`) that most data APIs don't give you. Commerce, review, place, and app-store endpoints share first-class canonical `Product` / `Review` / `Seller` / `Place` / `App` schemas.

**What the skill does:**
- Fetches social, commerce + research data on your behalf (profiles, posts, comments, search, trending, retail and marketplace products across Amazon/Walmart/Target/eBay/Home Depot/Klarna/AliExpress/Etsy/Sephora/H&M/Kohl's/Wayfair/Gumtree, reviews, app-store data, places and local businesses, job listings and salaries, market data, prediction markets, web research)
- Runs a universal cross-platform search that fans out to 17 sources across 14 platforms in parallel (sync JSON or SSE streaming, 20 credits flat)
- Runs cross-platform **Prism** composites (`/v1/prism/*`) — one call that fans out across many platforms into a unified report
- Creates and manages scheduled **Monitors** that re-run any recipe on a cadence and deliver each result to a signed webhook
- Runs **Cohorts** (`/v1/cohorts/*`) — upload a panel of up to 10,000 public identities you already care about and ask which of *them* posted your keywords, with a coverage record for every member
- Generates working code snippets that call the SocialCrawl API
- Answers questions about endpoints, parameters, and capabilities
- Scrapes, crawls, and monitors arbitrary web pages, and drives interactive browser sessions (`/v1/web/*`)
- Gives exact per-endpoint pricing for all 645 endpoints — cost, tier, cache TTL, and the full rule behind every metered endpoint (bundled pricing reference)
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
| **LinkedIn** | 68 | Profiles & company pages (incl. company by domain, also-viewed, employee counts), posts (deep `profile/posts` metered up to 200), reposts, reactions, comments & replies, articles with comments/reactions, profile activity/articles/posted jobs/similar profiles/interests (newsletters, schools, top voices), complete-profile and all-in-one bundles, people search (incl. by search URL), company/hashtag search, profile sub-resources (experience, education, skills, certifications…), the complete post-history archive walk (metered per post), jobs (search, company jobs, details, hiring team), company insights, groups, transcripts, Ad Library, profile-360 |
| **Prism** | 46 | Cross-platform composites — URL lookup, comment harvesting and comment leads, batch comment/profile lookup (plus async bulk `prism/jobs` up to 5,000 items), find-accounts (name → ranked public accounts), mentions, handle-audit, adverse screening, brief check, brand mentions, demand signals, AI visibility, crisis radar/post-mortem, reputation, share-of-voice, trend board, earliness, format lift, audience language, creator vetting & creator cards, org radar, Korea gap, AI consensus answers, video/app/product intelligence |
| **Instagram** | 38 | Profiles, account transparency (profile/about), posts, reels, comments & comment replies, highlights, stories, tagged & location feeds, on-screen text extraction, followers/following, similar accounts, post likers, reshare stats, one-call reels/posts feeds with share counts, engagement analytics, universal + popular-post search, reels/hashtag/profile/location/music search, trending, transcripts, profile-360 |
| **TikTok** | 37 | Profiles, videos, comments & replies, on-screen text extraction, keyword/hashtag/user/music search + suggestions, hashtag details, trending, audience, followers, similar accounts, liked videos, playlists & collections, place feeds, effects, live, songs, transcripts, Ad Library, profile-360 |
| **Facebook** | 29 | Pages, groups & group posts, posts, comments, photos, reels (incl. full reels feed with view counts), events, Marketplace, keyword search over posts/videos/pages/people/groups, transcripts, full Ad Library |
| **YouTube** | 29 | Channels, videos, shorts, comments & replies, sponsors, playlists & items, community posts, search (advanced + autocomplete), trending, live streams, channel contact email lookup, media files (audio/video/subtitles/thumbnails), transcripts, batch videos/channels/transcripts, profile-360 |
| **Web Scraping** | 22 | Scrape, web search, site map, LLM extract, async crawl/batch-scrape/agent jobs with per-page error feeds, change monitors, interactive browser sessions, document parse |
| **US Congress Trades** | 19 | US Congress STOCK Act disclosures — trade feeds (all/48h/7d), members, per-politician and per-ticker stats and trades, state delegations, and the full statistics suite (party, sectors, issuers, volume, unusual activity, buy/sell ratio, late filings) |
| **Klarna** | 18 | Product details and every merchant offer, keyword search + suggestions, user and professional reviews with score overviews, price history, product comparison, category browsing with filters/keywords/buying guides, store listings |
| **Tripadvisor** | 16 | Hotels, restaurants, attractions and cruise ships — search and full detail for each, traveler reviews with owner replies, place lookup by URL, destination autocomplete, experience types |
| **Twitter/X** | 15 | Profiles, tweets and replies, tweet & user search, user media, followers, following, retweeters, communities, video transcripts, AI search via Grok, profile-360 |
| **Naver** | 14 | Korea's #1 portal — blog, news, encyclopedia, cafe, KiN, local, image, web search, errata & adult classifiers, Data Lab search-trend & shopping-insight series, brief |
| **Reddit** | 14 | Subreddits, post detail, comments, user profiles with post and comment history, keyword/comment/media search, subreddit discovery, transcripts, omni-search VoC sweep |
| **GitHub** | 12 | Users, repos, issues, PRs, READMEs, releases, search, repo dossier, user profile-velocity |
| **Gumtree** | 11 | UK classifieds — listing search and details, similar listings, seller profiles and their ads, search suggestions, trending searches, category tree with filters, location lookup |
| **Jobs** | 11 | Job search and listing detail across LinkedIn, Indeed, Bing and Xing, LinkedIn organization-id resolution, and salary ranges by title and country |
| **Sephora** | 11 | Product details, reviews, keyword search + suggestions, category tree browsing, brand listings and per-brand products, store lookup, per-SKU in-store availability |
| **Content Analysis** | 10 | Cross-web brand mentions, sentiment, rating distributions, phrase/category trends |
| **Google** | 10 | Web search, Ads Transparency, Business Profile (info, reviews, updates, Q&A), Travel hotels |
| **AliExpress** | 9 | Product details, keyword search, similar products, reviews, per-SKU shipping, hot products, featured promotions, category tree |
| **Apple App Store** | 9 | App search, search suggestions, app details, reviews, charts, listings database, reference data |
| **Google Play** | 9 | App search, search suggestions, app details, reviews, charts, listings database, reference data |
| **Amazon** | 8 | Product search, ASIN details, reviews, sellers, shop pages, Best Sellers charts, current deals, seller profiles — ~13 marketplaces |
| **Douyin** | 8 | China's TikTok — video search, creator profiles and feeds, video detail, comments and comment replies, creator search, hot-search board (mostly metered per row) |
| **Finance** | 7 | Instrument quotes, ticker search, markets overview, instrument news, daily price history, company financial statements, options chains |
| **G2** | 7 | Software marketplace — product pages, reviews, category listings and the category index, vendor profiles and their catalogue, product URL index |
| **Quora** | 7 | Question search and detail, answer search, Space post search, profile search, Space/topic search |
| **H&M** | 6 | Keyword search + suggestions, store listings by country, countries/languages, category tree, per-product supplier and factory disclosure |
| **Pinterest** | 6 | Pins, boards, search, URL save-counts, Pinterest Trends by market |
| **Spotify** | 6 | Artists, tracks, albums, podcasts, episodes, search |
| **Threads** | 6 | Profiles, posts, post comments, keyword search, user search |
| **Utility** | 6 | Free API self-discovery — quickstart, endpoint catalogue, per-endpoint usage guide, cross-cutting capabilities (which params work where and what they cost), goal-to-call plans, LLM context payload. 0 credits, served from the live registry |
| **Xiaohongshu** | 6 | RED (Little Red Book) — note search, the hot/trending board, single note with full body, top-level note comments, creator profiles and their notes (5 credits per returned row) |
| **Apple Music** | 5 | Catalog search, artist, album, track, Apple Music charts by country |
| **Google Shopping** | 5 | Product search, product details, price history, cross-retailer reviews, per-seller offers |
| **Kohl's** | 5 | Keyword search, reviews, product questions and answers, store lookup, category tree |
| **Rumble** | 5 | Search, channel videos, video details, comments, transcripts |
| **Target** | 5 | Product details by TCIN, reviews, category browsing, full taxonomy, store lookup |
| **TikTok Shop** | 5 | Products, reviews, listings, search, creator showcases |
| **Universal Search** | 5 | One query fanned out across 14 platforms (20cr flat); `search/multi` (each platform's native search in one call, metered as the sum of the pages); forums lane; multi-country news lane (metered); creator-discovery lane across TikTok/Threads/Instagram |
| **Walmart** | 5 | Product details, reviews, keyword search, category browsing, seller offers |
| **Yelp** | 5 | Business profiles by encid, business reviews, business search (compact and full-card), search suggestions |
| **Bluesky** | 4 | Profiles, posts, keyword post search |
| **Etsy** | 4 | Listings by id or URL, a shop's catalogue, similar listings, search suggestions |
| **Hacker News** | 4 | Story search, story, comment tree, profile |
| **Home Depot** | 4 | Keyword search, product details by item id or URL (store/zip-aware pricing), reviews, store lookup by ZIP |
| **Tavily** | 4 | Web search (with LLM answer), URL extraction, sitemap, full crawl |
| **Twitch** | 4 | Profiles, clips, videos, schedules |
| **Google Trends** | 3 | Interest-over-time (explore), rising/breakout related queries, Trending Now by location |
| **Kwai** | 3 | Profiles, posts |
| **Telegram** | 3 | Public channel profiles, channel post feeds, single post lookup |
| **Truth Social** | 3 | Profiles, posts |
| **Wayfair** | 3 | Product search, product details by SKU, reviews |
| **eBay** | 2 | Listing search incl. sold/completed with realised prices, listing details |
| **Snapchat** | 2 | Profiles, Spotlight comments |
| **Trustpilot** | 2 | Business search, company reviews |
| **Google News** | 1 | Real-time Google News SERP search |
| **Kick** | 1 | Clips |
| **Komi** | 1 | Link pages |
| **LinkBio** | 1 | Link pages |
| **LinkMe** | 1 | Link pages |
| **Linktree** | 1 | Link pages |
| **On-Page** | 1 | Single-URL on-page SEO audit — the technical, content and meta checks in one call |
| **Perplexity** | 1 | Sonar web research with cited sources |
| **Pillar** | 1 | Link pages |
| **Polymarket** | 1 | Prediction-market research — multi-query fan-out + ranking |
| **Product Hunt** | 1 | The public launches feed (~50 launches), optionally by topic |

**Total: 645 endpoints across 68 platforms** — plus two stateful families that are not counted in the endpoint total: **Monitors** (`/v1/monitors/*`, scheduled recipe runs with webhook delivery) and **Cohorts** (`/v1/cohorts/*`, audience-filtered mention search over a panel you upload).

## Credit System

Every API call costs credits based on its complexity:

| Tier | Cost | Endpoints | Examples |
|------|------|-----------|----------|
| **Standard** | 1 credit | 239 | Profiles, posts, search, comments, Naver corpora, GitHub, HN, Tavily, Perplexity, reference data |
| **Advanced** | 5 credits | 167 | Audience demographics, ad libraries, trending, app data, retail catalogs, business/place reviews, Google + Naver trends, LinkedIn social graph + jobs, Instagram relationship/discovery data |
| **Premium** | 10 credits | 25 | Video transcripts, LinkedIn people/job search + reactions, app listings search, web agent jobs |
| **Custom (flat / request-shaped)** | varies by request | 200 | Free discovery, fixed composites, per-row batches, per-probe AI visibility, per-page crawl and search, browser sessions, and recurring monitors |

### Pricing

| Plan | Price | Credits | Per 1k Credits |
|------|-------|---------|----------------|
| **Free** | £0 | 100 (one-time) | — |
| **Starter** | £15 | 2,500 | £6.00 |
| **Growth** | £49 | 20,000 | £2.45 |
| **Pro** | £299 | 150,000 | £1.99 |
| **Enterprise** | Contact | Custom | Custom |

Many list endpoints are now **metered**: the ceiling for your request is held up front and refunded down to the work actually done, and the response's `credits_used` is the real charge. The pricing reference gives every metered endpoint its min-max band and the exact rule. The levers that move a bill:

- **Free default judgments.** Post, comment and review pages carry SocialCrawl labels at no extra cost (for example `sponsored`, `intent` and `niche` on posts; `sentiment`, `question`, `purchase_intent` and `complaint` on comments; `sentiment` and `issue` on reviews), and search pages carry `computed.relevance` against your query. `judgments=off` (or `label=none`) returns the plain page.
- **Metered judgments.** Asking for a paid label preset (`label=mention`, `quality`, `injection`, `reports`, `incentivized`, `spam`, `toxic`, `low_quality`, or `intent` with `offer=`) or a caller-written relevance topic (`relevant_to=`) holds a few extra credits and keeps 1 credit per started 25 newly judged rows. Rows already judged, and cached pages, are free.
- **`dry_run=1`** previews the cost of a labelled or relevance-filtered request at 0 credits, without fetching the page.
- **`max_pages`** walks up to 5 pages in one call, each page billed as one call. **`seen=<id>`** drops rows you already received under that id and discounts the page price by the share of repeats, so a page of nothing but repeats is free. **`since`** and **`stop_at_id`** end a feed walk at what you already have.
- **`include=`** row joins fill a list's rows from a sibling endpoint inside the same call, billed per row actually filled.

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
    ├── pricing.md         # Exact credit cost for every one of the 645 endpoints + credit packs
    ├── prism.md           # Cross-platform Prism composite recipes (/v1/prism/*)
    ├── monitors.md        # Scheduled recipe runs + webhook delivery (/v1/monitors/*)
    ├── cohorts.md         # Audience-filtered mention search over a panel you upload (/v1/cohorts/*)
    ├── search.md          # Universal cross-platform search (/v1/search/everywhere, /multi, /forums, /news, /creators)
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

## Publishing to claude.ai

skills.sh, ClawHub and the Git copy update from this repository on their own. The copy installed in **claude.ai** (and in an organisation's Anthropic skill list) does not: it is an uploaded archive and stays at whatever version was last uploaded. It is a manual step after every release.

**Owner:** the release maintainer (Oscar), once per release, after `python scripts/build_skill.py --check` passes. No automation does this today.

1. Download the release archive: [`socialcrawl.skill`](https://github.com/socialcrawl/skills/raw/main/socialcrawl.skill) (a zip holding the `socialcrawl/` skill directory). Rename it to `socialcrawl.zip` if the file picker only accepts `.zip`.
2. In claude.ai, open **Settings > Capabilities > Skills**, remove or replace the existing SocialCrawl skill, and upload the archive. For a Team or Enterprise organisation, an admin uploads it once for everyone.
3. Check it: in a new chat, ask Claude to run the SocialCrawl Freshness Check. The `registry_fingerprint` near the top of the uploaded `SKILL.md` must equal `data.fingerprint` from `GET /v1/utility/endpoints?fingerprint=1` (free). If they differ, the upload and the API are out of sync; rebuild and upload again.
   - Until `?fingerprint=1` is deployed (the reply has no `data.fingerprint`), check instead that `data.stats.platforms` and `data.stats.endpoints` from `GET /v1/utility/endpoints` equal the totals at the top of `references/index.md`, and that the skill's description no longer says "27 platforms and 133 endpoints" (the stale copy's text).
   - The check runs in claude.ai's code execution, which needs network access to the API host (`www.socialcrawl.dev`) allowed in the organisation's settings. Without it the call fails and the skill skips the check silently, so a stale upload goes unnoticed: run the `curl` yourself instead.

## Licence

This repository is available under the [MIT License](LICENSE). You may reuse and adapt the skill, including its key-resolution and error-handling guidance, in public plugins and derivative skills. Retaining the included copyright and permission notice is sufficient attribution; a link back to `github.com/socialcrawl/skills` is appreciated but not required by the licence.
