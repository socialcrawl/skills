<div align="center">

# @socialcrawl

**Give your AI agent access to 27 social + research platforms through a single API**

[![Platforms](https://img.shields.io/badge/Platforms-27-blue?style=flat-square)](https://socialcrawl.dev)
[![Endpoints](https://img.shields.io/badge/Endpoints-133-green?style=flat-square)](https://socialcrawl.dev/docs)
[![skills.sh](https://img.shields.io/badge/skills.sh-listed-black?style=flat-square)](https://skills.sh)
[![Agents](https://img.shields.io/badge/Agents-40+-blueviolet?style=flat-square)](https://skills.sh)

[Overview](#overview) | [Installation](#installation) | [Setup](#setup) | [Usage](#usage) | [Platforms](#supported-platforms) | [Credits](#credit-system)

</div>

---

## Overview

`@socialcrawl` is a skill for AI coding agents (Claude Code, Cursor, Windsurf, Codex, Gemini CLI, and [40+ more](https://skills.sh)) that lets your agent fetch live social and research data — profiles, posts, comments, search results, prediction markets, AI-grounded answers, and a universal cross-platform search — from 27 platforms using the [SocialCrawl API](https://socialcrawl.dev).

One API key. One consistent response format. Every platform. Every response is wrapped in a unified envelope with transparent credit accounting, and the key social archetypes (`Author`, `Post`) go through per-platform **field maps** that normalize 13 platforms' quirky upstream shapes into a single schema — plus four computed fields (`engagement_rate`, `language`, `content_category`, `estimated_reach`) that most data APIs don't give you.

**What the skill does:**
- Fetches social media + research data on your behalf (profiles, posts, comments, search, trending, prediction markets, web research)
- Runs a universal cross-platform search that fans out to 12 sources in parallel (sync JSON or SSE streaming, 20 credits flat)
- Generates working code snippets that call the SocialCrawl API
- Answers questions about endpoints, pricing, and capabilities
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

### Via ClawHub

```bash
npx clawhub@latest install socialcrawl
```

### Via Git (manual)

```bash
# Project-scoped (shared via version control)
git clone https://github.com/socialcrawl/skills .claude/skills/socialcrawl

# User-wide (available in all projects)
git clone https://github.com/socialcrawl/skills ~/.claude/skills/socialcrawl
```

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
> If the environment variable isn't set, the skill will ask you for your API key inline during the first interaction.

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
| **TikTok** | 26 | Profiles, videos, comments, followers, showcase, search, trending, live, Shop |
| **GitHub** | 12 | Profiles, repos, READMEs, releases, issues, PRs, search, composite dossiers, profile-velocity analytics |
| **Instagram** | 12 | Profiles, posts, reels, comments, highlights, search |
| **YouTube** | 12 | Channels, videos, shorts, playlists, comments, comment replies, trending |
| **Facebook** | 12 | Profiles, posts, reels, photos, groups, Ad Library |
| **Reddit** | 7 | Subreddits, posts, comments, search, ads |
| **Twitter/X** | 7 | Profiles, tweets, communities, AI-powered freeform search (Grok 4.20 + `x_search`) |
| **LinkedIn** | 6 | Profiles, company pages, posts, Ad Library |
| **Threads** | 5 | Profiles, posts, search |
| **Pinterest** | 4 | Search, pins, boards |
| **Google** | 4 | Search, Ad Library |
| **Hacker News** | 4 | Search, stories, story comments, profiles |
| **Tavily** | 4 | Web search (with LLM answer), URL extraction, sitegraph, multi-page crawl |
| **Truth Social** | 3 | Profiles, posts |
| **Polymarket** | 2 | Prediction-market search + server-side topic-expansion research |
| **Twitch** | 2 | Profiles, clips |
| **Search (universal)** | 1 | Cross-platform meta-search across 12 sources (sync JSON / SSE streaming, 20cr flat) |
| **Perplexity** | 1 | Web-grounded research (LLM answer + cited sources) |
| **Snapchat** | 1 | Profiles |
| **Kick** | 1 | Clips |
| **Amazon** | 1 | Shop pages |
| **Linktree** | 1 | Link pages |
| **Linkbio** | 1 | Link pages |
| **Linkme** | 1 | Link pages |
| **Komi** | 1 | Link pages |
| **Pillar** | 1 | Link pages |
| **Utility** | 1 | Age & gender detection |

**Total: 133 endpoints across 27 platforms.**

## Credit System

Every API call costs credits based on its complexity:

| Tier | Cost | Endpoints | Examples |
|------|------|-----------|----------|
| **Standard** | 1 credit | 104 | Profiles, posts, search, comments, GitHub, HN, Tavily, Perplexity, Twitter AI Search |
| **Advanced** | 5 credits | 21 | Audience demographics, ad libraries, trending, GitHub composites, Polymarket research |
| **Premium** | 10 credits | 7 | Video transcripts, AI analysis, GitHub `user/profile-velocity` |
| **Flat override** | 20 credits | 1 | `/v1/search/everywhere` — universal cross-platform search across 12 sources |

### Pricing

| Plan | Price | Credits | Per 1k Credits |
|------|-------|---------|----------------|
| **Free** | £0 | 100 (one-time) | — |
| **Starter** | £14 | 5,000 | £2.80 |
| **Growth** | £49 | 20,000 | £2.45 |
| **Pro** | £299 | 150,000 | £1.99 |
| **Enterprise** | Contact | Custom | Custom |

Credits never expire. Pay-as-you-go, no monthly commitments. Failed upstream calls, open circuit breakers, and internal errors auto-refund credits.

> [!IMPORTANT]
> The skill will inform you of the credit cost before executing advanced or premium tier calls.

## Skill Contents

The installed skill contains:

```
socialcrawl/
├── SKILL.md              # Main skill definition
└── references/
    ├── api-overview.md    # Auth, response format, errors, credits
    ├── search.md          # Universal cross-platform search (/v1/search/everywhere)
    ├── tiktok.md          # TikTok endpoints & parameters
    ├── github.md          # GitHub endpoints & parameters
    ├── instagram.md       # Instagram endpoints & parameters
    ├── youtube.md         # YouTube endpoints & parameters
    ├── facebook.md        # Facebook endpoints & parameters
    ├── twitter.md         # Twitter/X endpoints (incl. ai-search)
    ├── linkedin.md        # LinkedIn endpoints & parameters
    ├── reddit.md          # Reddit endpoints & parameters
    ├── threads.md         # Threads endpoints & parameters
    ├── hackernews.md      # Hacker News endpoints & parameters
    ├── tavily.md          # Tavily web search/extract/map/crawl
    ├── polymarket.md      # Polymarket prediction-market search
    ├── perplexity.md      # Perplexity Sonar web research
    └── ...                # 12 more platform references
```

The skill reads the appropriate reference file for each platform on demand, keeping context usage minimal.

## Error Handling

The skill handles common API errors automatically:

| Error | What happens |
|-------|-------------|
| Missing/invalid API key | Prompts you to provide or fix your key |
| Insufficient credits | Tells you your balance and links to billing |
| Resource not found | Reports that the profile/post wasn't found |
| Platform unavailable | Reports the outage; credits are refunded automatically |

## Links

- [SocialCrawl Website](https://socialcrawl.dev)
- [API Documentation](https://socialcrawl.dev/docs)
- [Dashboard & API Keys](https://socialcrawl.dev/dashboard)
- [Billing & Credits](https://socialcrawl.dev/dashboard/billing)
