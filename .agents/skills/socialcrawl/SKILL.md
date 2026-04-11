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

Resolve the API key before making any call, checking these sources in order:

1. **Env var**: `echo "$SOCIALCRAWL_API_KEY"` — if set and starts with `sc_` (and is not a placeholder like `sc_your_api_key_here`), use it.
2. **Config file**: `cat ~/.config/socialcrawl/api_key 2>/dev/null` — if the file exists and contains a key starting with `sc_`, use it.
3. **Ask the user**: If neither source has a valid key:
   - Tell the user: "I need your SocialCrawl API key to continue. You can find it at https://socialcrawl.dev/dashboard — every account starts with 100 free credits."
   - Ask them to paste their key.
   - After receiving the key, **auto-save it** so they never need to paste it again:
     ```bash
     mkdir -p ~/.config/socialcrawl && echo "sc_xxxxx" > ~/.config/socialcrawl/api_key
     ```
   - Tell the user: "I've saved your key to `~/.config/socialcrawl/api_key` so it will be available in future sessions."

For all subsequent API calls in the session, use the resolved key directly in the curl command (do not rely on the env var being set).

## First Use

On the first interaction with this skill in a session:

1. Briefly introduce: "SocialCrawl provides a single API for 21 social media platforms (105 endpoints). Let me verify your API key."
2. Resolve the API key using the steps above. If the key is missing or a placeholder, stop here and ask for it before proceeding.
3. Tell the user you'll make a test call that costs 1 credit, then run:
   ```bash
   curl -s -H "x-api-key: KEY" "https://www.socialcrawl.dev/v1/tiktok/profile?handle=tiktok"
   ```
   (Replace `KEY` with the resolved key value.)
4. If successful, confirm the key works and show credits_remaining. Then respond to whatever the user actually asked.
5. If it fails, report the error and help troubleshoot (see Error Handling below).

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
2. Run: `curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" "https://www.socialcrawl.dev/api/credits/balance"`
3. Return the balance

**Ambiguous platform:** If the user says "get profile for @nike" without specifying a platform, ask which platform they mean.

**Multi-platform requests:** Load each platform's reference file and make sequential calls.

## Making API Calls

Base URL: `https://www.socialcrawl.dev`

All endpoints are GET requests:

```
curl -s -H "x-api-key: $SOCIALCRAWL_API_KEY" \
  "https://www.socialcrawl.dev/v1/{platform}/{resource}?{param}={value}"
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
| INSUFFICIENT_CREDITS | 402 | "You're out of credits. Top up at socialcrawl.dev/dashboard/billing" |
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
