<div align="center">

# @socialcrawl

**Give your AI agent access to 21 social media platforms through a single API**

[![Platforms](https://img.shields.io/badge/Platforms-21-blue?style=flat-square)](https://socialcrawl.dev)
[![Endpoints](https://img.shields.io/badge/Endpoints-105-green?style=flat-square)](https://socialcrawl.dev/docs)
[![skills.sh](https://img.shields.io/badge/skills.sh-listed-black?style=flat-square)](https://skills.sh)
[![Agents](https://img.shields.io/badge/Agents-40+-blueviolet?style=flat-square)](https://skills.sh)

[Overview](#overview) | [Installation](#installation) | [Setup](#setup) | [Usage](#usage) | [Platforms](#supported-platforms) | [Credits](#credit-system)

</div>

---

## Overview

`@socialcrawl` is a skill for AI coding agents (Claude Code, Cursor, Windsurf, Codex, Gemini CLI, and [40+ more](https://skills.sh)) that lets your agent fetch live social media data — profiles, posts, comments, search results, and analytics — from 21 platforms using the [SocialCrawl API](https://socialcrawl.dev).

One API key. One consistent response format. Every platform.

**What the skill does:**
- Fetches social media data on your behalf (profiles, posts, comments, search, trending)
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
  "https://api.socialcrawl.com/v1/tiktok/profile?handle=charlidamelio"
```

Every response follows a unified envelope:

```json
{
  "success": true,
  "platform": "tiktok",
  "endpoint": "/v1/tiktok/profile",
  "data": {
    "content": { "text": "...", "media_urls": ["..."] },
    "author": { "username": "charlidamelio", "followers": 156000000 },
    "engagement": { "likes": 5200, "engagement_rate": 0.045 },
    "metadata": { "language": "en", "content_category": "entertainment" }
  },
  "credits_used": 1,
  "credits_remaining": 99
}
```

> [!NOTE]
> Add `?format=raw` to any endpoint to receive the original upstream response without schema transformation.

## Supported Platforms

| Platform | Endpoints | Data Available |
|----------|-----------|----------------|
| **TikTok** | 24 | Profiles, videos, comments, followers, search, trending, live, Shop |
| **Instagram** | 12 | Profiles, posts, reels, comments, highlights, search |
| **YouTube** | 11 | Channels, videos, shorts, playlists, comments, trending |
| **Facebook** | 12 | Profiles, posts, reels, photos, groups, Ad Library |
| **Twitter/X** | 6 | Profiles, tweets, communities |
| **LinkedIn** | 6 | Profiles, company pages, posts, Ad Library |
| **Reddit** | 7 | Subreddits, posts, comments, search, ads |
| **Threads** | 5 | Profiles, posts, search |
| **Pinterest** | 4 | Search, pins, boards |
| **Google** | 4 | Search, Ad Library |
| **Truth Social** | 3 | Profiles, posts |
| **Twitch** | 2 | Profiles, clips |
| **Snapchat** | 1 | Profiles |
| **Kick** | 1 | Clips |
| **Amazon** | 1 | Shop pages |
| **Linktree** | 1 | Link pages |
| **Linkbio** | 1 | Link pages |
| **Linkme** | 1 | Link pages |
| **Komi** | 1 | Link pages |
| **Pillar** | 1 | Link pages |
| **Utility** | 1 | Age & gender detection |

**Total: 105 endpoints across 21 platforms.**

## Credit System

Every API call costs credits based on its complexity:

| Tier | Cost | Endpoints | Examples |
|------|------|-----------|----------|
| **Standard** | 1 credit | 81 | Profiles, posts, search, comments |
| **Advanced** | 5 credits | 18 | Audience demographics, ad libraries, trending |
| **Premium** | 10 credits | 6 | Video transcripts, AI analysis |

### Pricing

| Plan | Price | Credits | Per 1k Credits |
|------|-------|---------|----------------|
| **Free** | £0 | 100 (one-time) | — |
| **Starter** | £14 | 5,000 | £2.80 |
| **Growth** | £49 | 25,000 | £1.96 |
| **Pro** | £299 | 180,000 | £1.66 |
| **Enterprise** | Contact | Custom | Custom |

Credits never expire. No rate limits. No monthly commitments.

> [!IMPORTANT]
> The skill will inform you of the credit cost before executing advanced or premium tier calls.

## Skill Contents

The installed skill contains:

```
socialcrawl/
├── SKILL.md              # Main skill definition
└── references/
    ├── api-overview.md    # Auth, response format, errors, credits
    ├── tiktok.md          # TikTok endpoints & parameters
    ├── instagram.md       # Instagram endpoints & parameters
    ├── youtube.md         # YouTube endpoints & parameters
    ├── facebook.md        # Facebook endpoints & parameters
    ├── twitter.md         # Twitter/X endpoints & parameters
    ├── linkedin.md        # LinkedIn endpoints & parameters
    ├── reddit.md          # Reddit endpoints & parameters
    ├── threads.md         # Threads endpoints & parameters
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
