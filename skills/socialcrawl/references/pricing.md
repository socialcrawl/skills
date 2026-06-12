# SocialCrawl Pricing Reference

Complete per-endpoint credit pricing for all 221 active endpoints across 39 platforms. Auto-derived from the live endpoint registry.

## How billing works

- Every API call deducts credits from your balance **before** the upstream call, atomically. The response reports `credits_used` and `credits_remaining` (also in the `X-Credits-Used` / `X-Credits-Remaining` headers).
- **Cache hits are free** — a response served from cache costs 0 credits (`X-Cache: HIT`, `cached: true`).
- **Automatic refunds** — credits are refunded on upstream errors (502), circuit-breaker rejections (503), internal errors (500), and empty-upstream results (404 `RESOURCE_NOT_FOUND`). You only pay for calls that return real data.
- **Idempotent replays are free** — resending with the same `Idempotency-Key` returns the stored response at 0 credits.
- `GET /v1/credits/balance` is always 0 credits.

## Credit tiers

| Tier | Cost per call | Endpoints | Typical endpoints |
|------|--------------|-----------|-------------------|
| standard | 1 credit | 169 | Profiles, posts, comments, search, Naver corpora, GitHub direct calls, reference data |
| advanced | 5 credits | 37 | Ad libraries, trending, audience analytics, app data, business/place reviews, GitHub composites, Polymarket research |
| premium | 10 credits | 14 | Video transcripts, age-gender audience detection, profile-velocity composite, app listings search |
| flat override | 20 credits | 1 | `/v1/search/everywhere` (universal cross-platform search) |

## Credit packs

| Plan | Credits | Price |
|------|---------|-------|
| Free (signup bonus) | 400 | £0 |
| Starter | 2,500 | £15 one-time |
| Growth | 20,000 | £49 one-time |
| Pro | 150,000 | £299 one-time |
| Enterprise | Custom | [Contact](https://socialcrawl.dev/contact) |

Current packs and any promotions: https://socialcrawl.dev/pricing

## Per-endpoint pricing

### Amazon (5)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/amazon/shop` | Get Amazon shop page | 1 (standard) |
| `/v1/amazon/product-search` | Search Amazon products by keyword | 1 (standard) |
| `/v1/amazon/product` | Get an Amazon product by ASIN | 5 (advanced) |
| `/v1/amazon/reviews` | Get Amazon product reviews | 5 (advanced) |
| `/v1/amazon/sellers` | Get Amazon sellers and offers for a product | 1 (standard) |

### Apple App Store (8)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/app_store/app-search` | Search Apple App Store apps by keyword | 5 (advanced) |
| `/v1/app_store/app-info` | Get full Apple App Store app details | 5 (advanced) |
| `/v1/app_store/app-reviews` | Get Apple App Store reviews for an app | 5 (advanced) |
| `/v1/app_store/app-list` | Get an Apple App Store chart | 5 (advanced) |
| `/v1/app_store/app-listings-search` | Search the Apple App Store listings database (paginated) | 10 (premium) |
| `/v1/app_store/categories` | List Apple App Store app categories | 1 (standard) |
| `/v1/app_store/locations` | List supported Apple App Store storefront locations | 1 (standard) |
| `/v1/app_store/languages` | List supported Apple App Store languages | 1 (standard) |

### Bluesky (3)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/bluesky/profile` | Get a Bluesky profile | 1 (standard) |
| `/v1/bluesky/user/posts` | List a Bluesky user's posts | 1 (standard) |
| `/v1/bluesky/post` | Get a Bluesky post | 1 (standard) |

### Content Analysis (10)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/content_analysis/search` | Search web citations of a keyword with per-mention sentiment | 5 (advanced) |
| `/v1/content_analysis/summary` | Aggregate mention summary for a keyword | 5 (advanced) |
| `/v1/content_analysis/sentiment` | Sentiment breakdown for a keyword | 5 (advanced) |
| `/v1/content_analysis/rating-distribution` | Rating histogram for a keyword | 5 (advanced) |
| `/v1/content_analysis/phrase-trends` | Keyword mention volume + sentiment over time | 5 (advanced) |
| `/v1/content_analysis/category-trends` | Category mention volume + sentiment over time | 5 (advanced) |
| `/v1/content_analysis/languages` | List supported Content Analysis languages | 1 (standard) |
| `/v1/content_analysis/locations` | List supported Content Analysis locations | 1 (standard) |
| `/v1/content_analysis/categories` | List the Content Analysis category taxonomy | 1 (standard) |
| `/v1/content_analysis/filters` | List the filterable fields for Content Analysis | 1 (standard) |

### Facebook (21)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/facebook/profile` | Get Facebook page profile | 1 (standard) |
| `/v1/facebook/profile/posts` | List Facebook page posts | 1 (standard) |
| `/v1/facebook/post` | Get Facebook post details | 1 (standard) |
| `/v1/facebook/post/comments` | List Facebook post comments | 1 (standard) |
| `/v1/facebook/group/posts` | List Facebook group posts | 1 (standard) |
| `/v1/facebook/post/transcript` | Get Facebook video transcript | 10 (premium) |
| `/v1/facebook/profile/photos` | List Facebook profile photos | 1 (standard) |
| `/v1/facebook/profile/reels` | List Facebook profile reels | 1 (standard) |
| `/v1/facebook/adlibrary/ad` | Get Facebook Ad Library ad details | 5 (advanced) |
| `/v1/facebook/adlibrary/company/ads` | List Facebook Ad Library company ads | 5 (advanced) |
| `/v1/facebook/adlibrary/search/ads` | Search Facebook Ad Library | 5 (advanced) |
| `/v1/facebook/adlibrary/search/companies` | Search Facebook Ad Library companies | 5 (advanced) |
| `/v1/facebook/profile/events` | List a Facebook page's events | 1 (standard) |
| `/v1/facebook/post/comment/replies` | List replies to a Facebook post comment | 1 (standard) |
| `/v1/facebook/marketplace/location/search` | Search Facebook Marketplace locations | 1 (standard) |
| `/v1/facebook/marketplace/search` | Search Facebook Marketplace listings | 1 (standard) |
| `/v1/facebook/marketplace/item` | Get a Facebook Marketplace item | 1 (standard) |
| `/v1/facebook/events/search` | Search Facebook events by keyword | 1 (standard) |
| `/v1/facebook/events` | List Facebook events for a city | 1 (standard) |
| `/v1/facebook/event/details` | Get details for a Facebook event | 1 (standard) |
| `/v1/facebook/adlibrary/ad/transcript` | Get a Facebook Ad Library video ad transcript | 10 (premium) |

### GitHub (12)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/github/profile` | Get a GitHub user profile | 1 (standard) |
| `/v1/github/repo` | Get a GitHub repository | 1 (standard) |
| `/v1/github/profile/repos` | List a GitHub user's repositories | 1 (standard) |
| `/v1/github/repo/readme` | Get a repository's README | 1 (standard) |
| `/v1/github/repo/releases` | List a repository's releases | 1 (standard) |
| `/v1/github/repo/issues` | List a repository's issues (and PRs) | 1 (standard) |
| `/v1/github/issue` | Get a single issue or pull request | 1 (standard) |
| `/v1/github/issue/comments` | Get comments on an issue or pull request | 1 (standard) |
| `/v1/github/search` | Search GitHub issues and pull requests | 1 (standard) |
| `/v1/github/repo/top-issues` | Top feature request and top complaint for a repository | 5 (advanced) |
| `/v1/github/repo/dossier` | Full project dossier for a repository | 5 (advanced) |
| `/v1/github/user/profile-velocity` | User contribution velocity dossier | 10 (premium) |

### Google (10)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/google/search` | Google web search | 1 (standard) |
| `/v1/google/ad` | Get Google ad details | 5 (advanced) |
| `/v1/google/adlibrary/advertisers/search` | Search Google Ad Library advertisers | 5 (advanced) |
| `/v1/google/company/ads` | List Google ads by company | 5 (advanced) |
| `/v1/google/business/info` | Get a Google Business Profile | 1 (standard) |
| `/v1/google/business/extended-reviews` | Get Google extended (multi-source) reviews | 5 (advanced) |
| `/v1/google/business/updates` | Get Google Business Profile posts (updates) | 1 (standard) |
| `/v1/google/business/questions` | Get Google Business Profile questions & answers | 5 (advanced) |
| `/v1/google/hotels/search` | Search Google hotels | 1 (standard) |
| `/v1/google/hotels/info` | Get Google hotel detail | 5 (advanced) |

### Google Play (8)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/google_play/app-search` | Search Google Play apps by keyword | 5 (advanced) |
| `/v1/google_play/app-info` | Get full Google Play app details | 5 (advanced) |
| `/v1/google_play/app-reviews` | Get Google Play reviews for an app | 5 (advanced) |
| `/v1/google_play/app-list` | Get a Google Play store chart | 5 (advanced) |
| `/v1/google_play/app-listings-search` | Search the Google Play listings database (paginated) | 10 (premium) |
| `/v1/google_play/categories` | List Google Play app categories | 1 (standard) |
| `/v1/google_play/locations` | List supported Google Play storefront locations | 1 (standard) |
| `/v1/google_play/languages` | List supported Google Play languages | 1 (standard) |

### Google Shopping (4)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/google_shopping/product-search` | Search Google Shopping products | 5 (advanced) |
| `/v1/google_shopping/product` | Get Google Shopping product detail | 1 (standard) |
| `/v1/google_shopping/reviews` | Get Google Shopping product reviews | 1 (standard) |
| `/v1/google_shopping/sellers` | Get Google Shopping sellers for a product | 1 (standard) |

### Hacker News (4)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/hackernews/search` | Search Hacker News | 1 (standard) |
| `/v1/hackernews/story` | Get a Hacker News story | 1 (standard) |
| `/v1/hackernews/story/comments` | Get comments on a Hacker News story | 1 (standard) |
| `/v1/hackernews/profile` | Get a Hacker News user profile | 1 (standard) |

### Instagram (15)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/instagram/profile` | Get Instagram user profile | 1 (standard) |
| `/v1/instagram/profile/posts` | List Instagram user posts | 1 (standard) |
| `/v1/instagram/post` | Get Instagram post details | 1 (standard) |
| `/v1/instagram/post/comments` | List Instagram post comments | 1 (standard) |
| `/v1/instagram/basic-profile` | Get Instagram basic profile | 1 (standard) |
| `/v1/instagram/profile/reels` | List Instagram user reels | 1 (standard) |
| `/v1/instagram/highlights` | List Instagram story highlights | 1 (standard) |
| `/v1/instagram/highlight/detail` | Get Instagram highlight detail | 1 (standard) |
| `/v1/instagram/search/reels` | Search Instagram reels | 1 (standard) |
| `/v1/instagram/media/transcript` | Get Instagram media transcript | 10 (premium) |
| `/v1/instagram/user/embed` | Get Instagram user embed HTML | 1 (standard) |
| `/v1/instagram/audio/reels` | List Instagram reels using an audio track | 1 (standard) |
| `/v1/instagram/search/hashtag` | Search Instagram posts by hashtag | 1 (standard) |
| `/v1/instagram/search/profiles` | Search Instagram profiles by keyword | 1 (standard) |
| `/v1/instagram/reels/trending` | Get trending Instagram reels | 5 (advanced) |

### Kick (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/kick/clip` | Get Kick clip details | 1 (standard) |

### Komi (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/komi/page` | Get Komi page | 1 (standard) |

### Kwai (3)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/kwai/profile` | Get a Kwai user profile | 1 (standard) |
| `/v1/kwai/user/posts` | List a Kwai user's posts | 1 (standard) |
| `/v1/kwai/post` | Get a Kwai post | 1 (standard) |

### Linkbio (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/linkbio/page` | Get Linkbio page | 1 (standard) |

### LinkedIn (8)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/linkedin/profile` | Get LinkedIn user profile | 1 (standard) |
| `/v1/linkedin/company` | Get LinkedIn company page | 1 (standard) |
| `/v1/linkedin/post` | Get LinkedIn post details | 1 (standard) |
| `/v1/linkedin/company/posts` | List LinkedIn company posts | 1 (standard) |
| `/v1/linkedin/ad` | Get LinkedIn ad details | 5 (advanced) |
| `/v1/linkedin/ads/search` | Search LinkedIn ads | 5 (advanced) |
| `/v1/linkedin/search/posts` | Search public LinkedIn posts by keyword | 1 (standard) |
| `/v1/linkedin/post/transcript` | Get a LinkedIn post video transcript | 10 (premium) |

### Linkme (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/linkme/page` | Get Linkme profile | 1 (standard) |

### Linktree (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/linktree/page` | Get Linktree page | 1 (standard) |

### Naver (11)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/naver/blog/search` | Search Naver Blog | 1 (standard) |
| `/v1/naver/news/search` | Search Naver News | 1 (standard) |
| `/v1/naver/book/search` | Search Naver Book | 1 (standard) |
| `/v1/naver/encyc/search` | Search Naver Encyclopedia | 1 (standard) |
| `/v1/naver/cafearticle/search` | Search Naver Cafe articles | 1 (standard) |
| `/v1/naver/kin/search` | Search Naver KnowledgeiN (지식iN) | 1 (standard) |
| `/v1/naver/local/search` | Search Naver Local (장소 검색) | 1 (standard) |
| `/v1/naver/shop/search` | Search Naver Shopping | 1 (standard) |
| `/v1/naver/doc/search` | Search Naver Academic Documents (전문자료) | 1 (standard) |
| `/v1/naver/image/search` | Search Naver Image | 1 (standard) |
| `/v1/naver/webkr/search` | Search Naver Web (웹문서) | 1 (standard) |

### Perplexity (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/perplexity/research` | Web research via Perplexity Sonar | 1 (standard) |

### Pillar (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/pillar/page` | Get Pillar page | 1 (standard) |

### Pinterest (5)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/pinterest/search` | Search Pinterest pins | 1 (standard) |
| `/v1/pinterest/pin` | Get Pinterest pin details | 1 (standard) |
| `/v1/pinterest/url-stats` | Get Pinterest save counts for external URLs | 1 (standard) |
| `/v1/pinterest/board` | Get Pinterest board | 1 (standard) |
| `/v1/pinterest/user/boards` | List Pinterest user boards | 1 (standard) |

### Polymarket (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/polymarket/research` | Polymarket prediction markets — multi-query research | 5 (advanced) |

### Reddit (6)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/reddit/subreddit` | List Reddit subreddit posts | 1 (standard) |
| `/v1/reddit/subreddit/details` | Get Reddit subreddit details | 1 (standard) |
| `/v1/reddit/search` | Search Reddit posts | 1 (standard) |
| `/v1/reddit/post/comments` | List Reddit post comments | 1 (standard) |
| `/v1/reddit/subreddit/search` | Search within a subreddit | 1 (standard) |
| `/v1/reddit/post/transcript` | Get a Reddit video post transcript | 10 (premium) |

### Rumble (5)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/rumble/search` | Search Rumble videos | 1 (standard) |
| `/v1/rumble/channel/videos` | List videos for a Rumble channel | 1 (standard) |
| `/v1/rumble/video` | Get a Rumble video | 1 (standard) |
| `/v1/rumble/video/transcript` | Get a Rumble video transcript | 10 (premium) |
| `/v1/rumble/video/comments` | List top-level comments on a Rumble video | 1 (standard) |

### Universal Search (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/search/everywhere` | Universal social search across 12 platforms | 20 (flat) |

### Snapchat (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/snapchat/profile` | Get Snapchat user profile | 1 (standard) |

### Spotify (6)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/spotify/artist` | Get a Spotify artist | 1 (standard) |
| `/v1/spotify/track` | Get a Spotify track | 1 (standard) |
| `/v1/spotify/album` | Get a Spotify album | 1 (standard) |
| `/v1/spotify/search` | Search Spotify | 1 (standard) |
| `/v1/spotify/podcast` | Get a Spotify podcast | 1 (standard) |
| `/v1/spotify/podcast/episodes` | List a Spotify podcast's episodes | 1 (standard) |

### Tavily (4)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/tavily/search` | Tavily web search with optional LLM-generated answer | 1 (standard) |
| `/v1/tavily/extract` | Extract clean content from one or more URLs | 1 (standard) |
| `/v1/tavily/map` | Map a website's sitegraph | 1 (standard) |
| `/v1/tavily/crawl` | Crawl a website with LLM-driven path selection | 1 (standard) |

### Threads (5)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/threads/profile` | Get Threads user profile | 1 (standard) |
| `/v1/threads/user/posts` | List Threads user posts | 1 (standard) |
| `/v1/threads/post` | Get Threads post details | 1 (standard) |
| `/v1/threads/search` | Search Threads posts | 1 (standard) |
| `/v1/threads/search/users` | Search Threads users | 1 (standard) |

### TikTok (18)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/tiktok/profile` | Get TikTok user profile | 1 (standard) |
| `/v1/tiktok/profile/videos` | List TikTok user videos | 1 (standard) |
| `/v1/tiktok/post` | Get TikTok post details | 1 (standard) |
| `/v1/tiktok/post/comments` | List TikTok post comments | 1 (standard) |
| `/v1/tiktok/video/comment/replies` | List TikTok comment replies | 1 (standard) |
| `/v1/tiktok/search` | Search TikTok videos by keyword | 1 (standard) |
| `/v1/tiktok/trending` | Get TikTok trending feed | 5 (advanced) |
| `/v1/tiktok/search/hashtag` | Search TikTok by hashtag | 1 (standard) |
| `/v1/tiktok/search/top` | TikTok top search results | 1 (standard) |
| `/v1/tiktok/search/users` | Search TikTok users | 1 (standard) |
| `/v1/tiktok/user/audience` | Get TikTok user audience demographics | 5 (advanced) |
| `/v1/tiktok/user/followers` | List TikTok user followers | 1 (standard) |
| `/v1/tiktok/user/following` | List TikTok user following | 1 (standard) |
| `/v1/tiktok/user/live` | Get TikTok user live stream | 1 (standard) |
| `/v1/tiktok/post/transcript` | Get TikTok video transcript | 10 (premium) |
| `/v1/tiktok/song` | Get TikTok song details | 1 (standard) |
| `/v1/tiktok/song/videos` | List TikTok videos using a song | 1 (standard) |
| `/v1/tiktok/profile/region` | Get TikTok profile region | 1 (standard) |

### TikTok Shop (5)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/tiktokshop/product` | Get TikTok Shop product details | 1 (standard) |
| `/v1/tiktokshop/product/reviews` | List TikTok Shop product reviews | 1 (standard) |
| `/v1/tiktokshop/products` | List TikTok Shop products | 1 (standard) |
| `/v1/tiktokshop/search` | Search TikTok Shop products | 1 (standard) |
| `/v1/tiktokshop/user/showcase` | List TikTok user showcase products | 1 (standard) |

### Tripadvisor (2)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/tripadvisor/search` | Search TripAdvisor businesses & places | 1 (standard) |
| `/v1/tripadvisor/reviews` | Get TripAdvisor reviews for a place | 1 (standard) |

### Trustpilot (2)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/trustpilot/business-search` | Search Trustpilot businesses | 1 (standard) |
| `/v1/trustpilot/reviews` | Get Trustpilot reviews for a business | 5 (advanced) |

### Truth Social (3)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/truthsocial/profile` | Get Truth Social user profile | 1 (standard) |
| `/v1/truthsocial/user/posts` | List Truth Social user posts | 1 (standard) |
| `/v1/truthsocial/post` | Get Truth Social post details | 1 (standard) |

### Twitch (4)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/twitch/profile` | Get Twitch streamer profile | 1 (standard) |
| `/v1/twitch/clip` | Get Twitch clip details | 1 (standard) |
| `/v1/twitch/user/videos` | List a Twitch user's videos | 1 (standard) |
| `/v1/twitch/user/schedule` | Get a Twitch user's stream schedule | 1 (standard) |

### Twitter/X (7)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/twitter/profile` | Get Twitter user profile | 1 (standard) |
| `/v1/twitter/user/tweets` | List Twitter user tweets | 1 (standard) |
| `/v1/twitter/tweet` | Get Twitter tweet details | 1 (standard) |
| `/v1/twitter/community` | Get Twitter community details | 1 (standard) |
| `/v1/twitter/community/tweets` | List Twitter community tweets | 1 (standard) |
| `/v1/twitter/tweet/transcript` | Get Twitter video transcript | 10 (premium) |
| `/v1/twitter/ai-search` | AI-powered X (Twitter) search via xAI Grok | 1 (standard) |

### Utility (1)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/utility/age-gender` | Detect age and gender | 10 (premium) |

### YouTube (16)

| Endpoint | What it returns | Credits |
|----------|-----------------|---------|
| `/v1/youtube/channel` | Get YouTube channel info | 1 (standard) |
| `/v1/youtube/channel/videos` | List YouTube channel videos | 1 (standard) |
| `/v1/youtube/video` | Get YouTube video details | 1 (standard) |
| `/v1/youtube/video/sponsors` | Detect sponsors of a YouTube video | 10 (premium) |
| `/v1/youtube/video/comments` | List YouTube video comments | 1 (standard) |
| `/v1/youtube/video/comment/replies` | List YouTube comment replies | 1 (standard) |
| `/v1/youtube/search` | Search YouTube | 1 (standard) |
| `/v1/youtube/channel/shorts` | List YouTube channel shorts | 1 (standard) |
| `/v1/youtube/community-post` | Get YouTube community post | 1 (standard) |
| `/v1/youtube/playlist` | Get YouTube playlist | 1 (standard) |
| `/v1/youtube/search/hashtag` | Search YouTube by hashtag | 1 (standard) |
| `/v1/youtube/shorts/trending` | Get trending YouTube shorts | 5 (advanced) |
| `/v1/youtube/video/transcript` | Get YouTube video transcript | 10 (premium) |
| `/v1/youtube/channel/playlists` | List a YouTube channel's playlists | 1 (standard) |
| `/v1/youtube/channel/lives` | List a YouTube channel's live streams | 1 (standard) |
| `/v1/youtube/channel/community-posts` | List a YouTube channel's community posts | 1 (standard) |
