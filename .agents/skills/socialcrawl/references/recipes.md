# SocialCrawl Recipes

Task to cheapest call chain. Each recipe lists the calls in order (with the value each takes from the previous one), what it costs for a stated size, cheaper and deeper options, pitfalls, and a code example. Costs are computed by the estimator from the live registry; quote your real request free with `GET /v1/utility/estimate` or `scripts/estimate.py` before a paid call. The hold is the most a call can cost, and the unused part is refunded. "≥" marks a floor (a page count or fan-out is unknown) and "about" a guide.

## Contents

- [Watch what the web says about a brand](#watch-what-the-web-says-about-a-brand)
- [This week's posts about a brand on the platforms you name](#this-weeks-posts-about-a-brand-on-the-platforms-you-name)
- [Who mentions or replies to an account](#who-mentions-or-replies-to-an-account)
- [Share of voice between competing brands](#share-of-voice-between-competing-brands)
- [Search a topic on several platforms at once](#search-a-topic-on-several-platforms-at-once)
- [Collect thousands of tweets for a keyword](#collect-thousands-of-tweets-for-a-keyword)
- [Find posts from people ready to buy](#find-posts-from-people-ready-to-buy)
- [Forum threads about a topic, with top replies](#forum-threads-about-a-topic-with-top-replies)
- [News coverage of a topic](#news-coverage-of-a-topic)
- [Find creators in a niche](#find-creators-in-a-niche)
- [Instagram creators from one country about a topic](#instagram-creators-from-one-country-about-a-topic)
- [Instagram creators from one country on a small budget](#instagram-creators-from-one-country-on-a-small-budget)
- [Vet a creator before a partnership](#vet-a-creator-before-a-partnership)
- [One creator on every platform](#one-creator-on-every-platform)
- [A creator's profile, recent posts and the comments on them](#a-creators-profile-recent-posts-and-the-comments-on-them)
- [Find the social accounts of a person or company](#find-the-social-accounts-of-a-person-or-company)
- [A LinkedIn member's profile and recent posts](#a-linkedin-members-profile-and-recent-posts)
- [Find LinkedIn members by role and company](#find-linkedin-members-by-role-and-company)
- [Look up a list of handles in one call](#look-up-a-list-of-handles-in-one-call)
- [Export the latest N comments on a TikTok video](#export-the-latest-n-comments-on-a-tiktok-video)
- [Every comment on any post, in one call](#every-comment-on-any-post-in-one-call)
- [Which comments are questions, complaints or buyers](#which-comments-are-questions-complaints-or-buyers)
- [Transcribe a video](#transcribe-a-video)
- [Compare one product's reviews across retailers](#compare-one-products-reviews-across-retailers)
- [A Home Depot product's price and reviews](#a-home-depot-products-price-and-reviews)
- [One report on a product's reviews across marketplaces](#one-report-on-a-products-reviews-across-marketplaces)
- [Reviews of a mobile app](#reviews-of-a-mobile-app)
- [Reviews of a local business](#reviews-of-a-local-business)
- [See the ads a competitor is running](#see-the-ads-a-competitor-is-running)
- [Track a creator's new posts every day](#track-a-creators-new-posts-every-day)
- [Weekly alert on a competitor's new YouTube videos](#weekly-alert-on-a-competitors-new-youtube-videos)
- [Alert when a web page changes](#alert-when-a-web-page-changes)
- [Engagement stats for a list of post URLs](#engagement-stats-for-a-list-of-post-urls)
- [Which of my accounts posted about a keyword](#which-of-my-accounts-posted-about-a-keyword)
- [Pay for a role in a country, and the open jobs](#pay-for-a-role-in-a-country-and-the-open-jobs)
- [A stock's current price and latest headlines](#a-stocks-current-price-and-latest-headlines)
- [Crawl a site and get each page as markdown](#crawl-a-site-and-get-each-page-as-markdown)
- [Pull structured fields from a web page](#pull-structured-fields-from-a-web-page)
- [What Korean consumers say about a product, and search interest](#what-korean-consumers-say-about-a-product-and-search-interest)

## Watch what the web says about a brand

**When** "brand mentions", "what are people saying about our brand", "brand health or sentiment over time", "monitor mentions of a company or product"

**Inputs**

- `brand`: The brand or product name (e.g. `notion`)
- `start_date`: First day of the window, YYYY-MM-DD (e.g. `2026-09-01`)

**Chain**

1. `GET /v1/prism/brand-mentions?keyword=<brand>&date_from=<start_date>&include=digest` - One call returns the mention volume trend, the sentiment split, top sources and recent mentions; include=digest adds a written summary.

**Cost** for one brand, one window: 50 credits held up front (exact; the unused hold is refunded).

**Cheaper** `search/multi` - Native search results from the platforms you name, priced per platform page, when you need this week's social posts rather than a trend.

**Deeper** `prism/share-of-voice` - The same read for two to five competing brands at once, as a share of voice.

**Pitfalls**

- prism/brand-mentions reads a web citation index (news, blogs, forums, shops) that lags the live web by days; it is not a live social search.
- date_from is required, as YYYY-MM-DD.
- A brand name that is also a common word (Notion, Apple) collides with other meanings: pass brand_description, and read each recent mention's about_brand probability.
- Mentions of one account (replies, tags, retweets) are a different job: use prism/mentions with the handle.

**Which one**

| Option | Endpoint | Best for | Cost shape |
|--------|----------|----------|------------|
| Trend, sentiment and recent mentions of one brand on the web | `prism/brand-mentions` | A brand-health read over a date window, with a written digest | flat per call |
| Posts and replies that mention one account or link one URL | `prism/mentions` | Who is talking to or about a handle on X and Reddit (Instagram tags opt-in) | per search page read; a page with no verified row is refunded |
| Share of voice across competing brands | `prism/share-of-voice` | Comparing two to five brands on web and social reach | per brand; dropping the social leg halves it |
| Raw web citations with per-mention sentiment | `content_analysis/search` | Exporting the individual web mentions behind a trend, paginated | flat per call |
| Each platform's own search, in one call | `search/multi` | Recent social posts from the platforms you name, with since= for a window | per page, per platform, at each platform's own price |
| Ranked and clustered research answer across many sources | `search/everywhere` | A one-off overview with real comments attached, when you do not know which platforms matter | flat per call |
| One platform's native search | `reddit/search` | Depth on one platform with its own filters and paging (also twitter/search/tweets, tiktok/search) | per page |

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const mentions = await sc("prism/brand-mentions", { keyword: "notion", date_from: "2026-09-01", include: "digest" });
```

## This week's posts about a brand on the platforms you name

**When** "Reddit and X chatter about a brand this week", "what are people posting about us on TikTok and Instagram", "recent social posts mentioning a product"

**Inputs**

- `brand`: The brand or product name (e.g. `Notion`)
- `start_date`: Keep only posts on or after this day, YYYY-MM-DD (e.g. `2026-09-25`)

**Chain**

1. `GET /v1/search/multi?query=<brand>&platforms=reddit,twitter&since=<start_date>` - Each platform runs its own search and is billed as a direct call; data.sources reports each platform's rows, charge and next_cursor.

**Cost** for one page from each of two platforms: 2 credits held up front (settles 0-2; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| posts | `search/multi` | 1 | 0 | 0 |
| posts (reddit leg) | `reddit/search` | 1 | 1 | 1 |
| posts (twitter leg) | `twitter/search/tweets` | 1 | 1 | 1 |

**Cheaper** `reddit/search` - One platform only, one page, when the user named a single platform.

**Deeper** `search/everywhere` - A ranked, clustered answer across many more sources, at a much higher flat price.

**Pitfalls**

- Name the platforms: the default set is TikTok, Instagram, YouTube, Reddit and Threads, so X is missing unless you ask for twitter.
- X has no date parameter. search/multi turns since= into the since: operator for you; calling twitter/search/tweets directly, put since:YYYY-MM-DD inside query.
- search/multi does not page itself: continue one platform on its own endpoint with data.sources.<platform>.next_cursor as cursor.
- prism/brand-mentions and search/everywhere are not this job: they cost far more and do not limit the results to the platforms you named.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const posts = await sc("search/multi", { query: "Notion", platforms: "reddit,twitter", since: "2026-09-25" });
```

## Who mentions or replies to an account

**When** "who is talking about @handle", "find replies and tags of our account", "posts that link to our website"

**Inputs**

- `handle`: The account handle, with or without @ (e.g. `nasa`)
- `start_date`: Keep only rows on or after this day, YYYY-MM-DD (e.g. `2026-09-01`)

**Chain**

1. `GET /v1/prism/mentions?handle=<handle>&since=<start_date>` - Searches X and Reddit by default; each kept row says whether it is a reply, retweet, mention or tag.

**Cost** for first page of each default search: 3 credits held up front (settles 1-3; the unused hold is refunded).

**Deeper** `prism/brand-mentions` - Mentions of the brand name across the web index, with a trend and sentiment, rather than of the handle.

**Pitfalls**

- Facebook, Threads and TikTok are accepted in platforms but not searched; add instagram to platforms for posts that tag the handle.
- Pass url= instead of handle to find posts that link to a page, and add web to platforms for web pages that contain the link.
- The account's own posts are dropped unless include_self=true.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const mentions = await sc("prism/mentions", { handle: "nasa", since: "2026-09-01" });
```

## Share of voice between competing brands

**When** "share of voice for us vs competitors", "which brand gets talked about most", "compare mention volume across brands"

**Inputs**

- `brands`: Two to five brand names, comma-separated (e.g. `notion,coda,airtable`)
- `start_date`: First day of the window, YYYY-MM-DD (e.g. `2026-07-01`)

**Chain**

1. `GET /v1/prism/share-of-voice?brands=<brands>&date_from=<start_date>`

**Cost** for three brands with the social leg: 120 credits held up front (settles 20-120; the unused hold is refunded).

**Cheaper** `prism/brand-mentions` - One brand's web trend and sentiment, when you do not need the comparison.

**Pitfalls**

- This is the most expensive composite: price it as number of brands times the per-brand price before you send it.
- Drop social from include for the web-only read at half the per-brand price.
- The emotion overlay is third-party sentiment that is not scoped to your date window; methodology.sentiment_provenance says so.
- Pass brand_descriptions when a brand name is also a common word.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const sov = await sc("prism/share-of-voice", { brands: "notion,coda,airtable", date_from: "2026-07-01" });
```

## Search a topic on several platforms at once

**When** "find TikTok, Instagram and YouTube posts about a topic", "search a hashtag or keyword everywhere", "what content exists about a trend"

**Inputs**

- `topic`: The topic or keyword (e.g. `matcha latte`)

**Chain**

1. `GET /v1/search/multi?query=<topic>&platforms=tiktok,instagram,youtube&relevance=filter` - relevance=filter drops posts that share the words but are about something else.

**Cost** for one page from each of three platforms: 3 credits held up front (settles 0-3; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| search | `search/multi` | 1 | 0 | 0 |
| search (tiktok leg) | `tiktok/search` | 1 | 1 | 1 |
| search (instagram leg) | `instagram/search/reels` | 1 | 1 | 1 |
| search (youtube leg) | `youtube/search` | 1 | 1 | 1 |

**Deeper** `search/everywhere` - Ranked and clustered across many sources, with top comments, for a research overview.

**Pitfalls**

- A filtered page can hold fewer rows than an unfiltered one; the dropped ids are listed in data.relevance.dropped_ids.
- Platform filters pass through with a prefix, for example tiktok.region=US or youtube.uploadDate=this_week.
- Rows keep each platform's own order; there is no cross-platform ranking here.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const search = await sc("search/multi", { query: "matcha latte", platforms: "tiktok,instagram,youtube", relevance: "filter" });
```

## Collect thousands of tweets for a keyword

**When** "cost of 10k tweets for a keyword", "download all tweets mentioning a term", "export tweets about a topic to CSV"

**Inputs**

- `keyword`: Keyword or phrase; X operators allowed (e.g. `nvidia`)

**Chain**

1. `GET /v1/twitter/search/tweets?query=<keyword>&sort=latest&max_pages=5` - repeat with `cursor=<pagination.next_cursor>` until 10000 rows or `has_more=false`. max_pages=5 makes each call walk up to five pages and return them together; the cursor it returns continues from the last page read.

**Cost** for ten thousand tweets: 1 credit per page (page size not yet measured; quote the whole job with GET /v1/utility/estimate or scripts/estimate.py).

**Pitfalls**

- Billing is per page of about twenty tweets, not per call: quote pages (N / 20) before you start, and expect short pages to raise the count.
- max_pages caps at five per call, so a large job is many calls; it does not change the price per page.
- There is no date parameter: put since:YYYY-MM-DD and until:YYYY-MM-DD inside query.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const tweets: unknown[] = [];
let cursor: string | undefined;
do {
  const r = await sc("twitter/search/tweets", { query: "nvidia", sort: "latest", max_pages: "5", cursor });
  tweets.push(...r.data.items);
  cursor = r.pagination.has_more ? r.pagination.next_cursor : undefined;
} while (cursor && tweets.length < 10000);
```

```sh
python3 scripts/paginate.py twitter/search/tweets --items 10000 query=nvidia sort=latest max_pages=5
```

The quote is not exact yet, so set --max-credits from your quote.

## Find posts from people ready to buy

**When** "find people looking for a product like ours", "purchase intent posts on Reddit", "leads from social conversations"

**Inputs**

- `category`: The product category, as a buyer would phrase it (e.g. `best crm for startups`)

**Chain**

1. `GET /v1/reddit/search?query=<category>&label=intent&relevance=filter` - Each post carries computed.labels.intent; relevance=filter drops posts that are not about the category.

**Cost** for one page of posts: 1 credit held up front (exact; the unused hold is refunded).

**Deeper** `prism/comment-leads` - Buyer leads from the comments under the posts a search returns, opening only the posts worth opening.

**Pitfalls**

- The default intent label is free; adding offer= (what you sell) makes it a paid, sharper judgment.
- relevance=filter can return a shorter page; the dropped ids are listed in data.relevance.dropped_ids, and pagination is unchanged.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const posts = await sc("reddit/search", { query: "best crm for startups", label: "intent", relevance: "filter" });
```

## Forum threads about a topic, with top replies

**When** "what do Reddit and Hacker News say about X", "forum discussions about a product", "community opinions with the best replies"

**Inputs**

- `topic`: The topic to look up (e.g. `vector databases`)

**Chain**

1. `GET /v1/search/forums?query=<topic>` - Fuses Reddit, Hacker News and Korean forums, and attaches top comments to the leading threads.

**Cost** for one fused page of threads: 10 credits held up front (exact; the unused hold is refunded).

**Cheaper** `reddit/search` - Reddit only, one page, no comment enrichment.

**Deeper** `search/everywhere` - Adds video, social and web sources to the forum threads.

**Pitfalls**

- Each items[].top_comments[] row has its body in excerpt, not text, clipped on a word boundary (truncated: true when cut).
- Korean forum threads come back without comments; they have no comment endpoint.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const threads = await sc("search/forums", { query: "vector databases" });
```

## News coverage of a topic

**When** "latest news about a company", "press coverage this week", "headlines mentioning a topic"

**Inputs**

- `topic`: The topic or company (e.g. `OpenAI`)

**Chain**

1. `GET /v1/google_news/search?keyword=<topic>&time_range=week`

**Cost** for one call at the default depth: 1 credit held up front (exact; the unused hold is refunded).

**Deeper** `search/news` - One query localised and fanned out across several countries and two news indexes.; `prism/earned-media` - Earned media coverage of a brand against a competitor, with domain authority.

**Pitfalls**

- google_news/search takes keyword, not query, and has no next page: depth (multiples of ten) sets how many articles one call returns.
- For a listed company's headlines, finance/news takes the ticker directly and is more precise.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const news = await sc("google_news/search", { keyword: "OpenAI", time_range: "week" });
```

## Find creators in a niche

**When** "find influencers who post about skincare", "creators in a niche with over 50k followers", "influencer discovery for a campaign"

**Inputs**

- `niche`: The niche, in the words creators use (e.g. `skincare routine`)
- `min_followers`: Follower floor (e.g. `50000`)

**Chain**

1. `GET /v1/search/creators?query=<niche>&sources=tiktok,instagram&min_followers=<min_followers>` - One ranked list across the platforms in sources; YouTube, X and Facebook are opt-in.

**Cost** for one fused list: 10 credits held up front (exact; the unused hold is refunded).

**Deeper** `prism/creator-vet` - Vet each shortlisted creator before you reach out.

**Pitfalls**

- search/creators has no country filter: for creators from one market use instagram/search/reels with country= or tiktok/search/users with country=.
- Pass brief= (what you are looking for) to re-rank creators who post about it above brands, shops and repost pages; it adds a small refundable charge.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const creators = await sc("search/creators", { query: "skincare routine", sources: "tiktok,instagram", min_followers: "50000" });
```

## Instagram creators from one country about a topic

**When** "German Instagram creators about matcha", "Instagram influencers in Spain over 50k followers", "local creators in one market"

**Inputs**

- `topic`: The topic, ideally as locals phrase it (e.g. `matcha`)
- `country`: Market code: ES, MX, DE, BR, KR or FR (e.g. `DE`)

**Chain**

1. `GET /v1/instagram/search/reels?query=<topic>&country=<country>` - Keeps only reels whose creator declares that market, and fills post.ext.author_country and post.ext.author_followers; filter on author_followers yourself for a follower floor.

**Cost** for one page of reels with each creator looked up: 61 credits held up front (settles 1-61; the unused hold is refunded).

**Cheaper** `instagram/profile/about` - On a small budget, the instagram-creators-by-country-budget recipe: search with region= at the plain page price, then one instagram/profile/about call per candidate you keep, which returns both the follower count and the declared country.; `search/creators` - Cross-platform creator search with min_followers, when the country does not matter.

**Pitfalls**

- country= supports ES, MX, DE, BR, KR and FR only; any other code is a free 400.
- Without country= or include=creator, post.ext.author_followers is null, so a follower floor cannot be applied.
- Each creator looked up is billed whether it is kept or dropped; quote the creator lookups, not the plain page price.
- author_country is the country the creator declares, not where the reel was filmed; topics about a place (travel, eSIMs) are often made by visitors.

**Which one**

| Option | Endpoint | Best for | Cost shape |
|--------|----------|----------|------------|
| Reels from creators who declare one market | `instagram/search/reels` | country= keeps only that market's creators (ES, MX, DE, BR, KR, FR) and fills followers | per page, plus per creator looked up |
| Localised reel search without a guarantee | `instagram/search/reels` | region= adds the market to the query at the plain page price; creators may be from anywhere | per page |
| Budget: region= reels, then check each candidate | `instagram/profile/about` | one call per shortlisted creator returns followers and declared country together (recipe instagram-creators-by-country-budget) | per page, plus flat per candidate checked |
| Instagram profile search with declared country | `instagram/search/profiles` | include=about fills author.ext.country on up to twelve rows of a profile search | per page, plus per row filled |
| TikTok creators by account region | `tiktok/search/users` | country= with a wide list of markets, when TikTok fits the brief | per in-country row returned |
| Cross-platform creator discovery | `search/creators` | Ranked creators with min_followers, but no country filter | flat per call |

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const reels = await sc("instagram/search/reels", { query: "matcha", country: "DE" });
```

## Instagram creators from one country on a small budget

**When** "cheapest way to find German Instagram creators about matcha", "Instagram creators in one market on a small budget", "check each creator's country and followers myself"

**Inputs**

- `topic`: The topic, ideally as locals phrase it (e.g. `matcha`)
- `country`: Market code for region=: ES, MX, DE, BR, KR or FR (e.g. `DE`)

**Chain**

1. `GET /v1/instagram/search/reels?query=<topic>&region=<country>` - region= localises the query at the plain page price and looks no creator up; it favours the market's creators but does not promise them, so the next step checks each one.
2. `GET /v1/instagram/profile/about?handle=<reels.items[].post.author.username>` - once per row of `reels`. One call per distinct candidate returns both author.followers and author.ext.country; keep the creators whose country matches and whose followers clear your floor. Do not also call instagram/profile: this call already carries the follower count.

**Cost** for one page of reels with each creator checked: 31 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| reels | `instagram/search/reels` | 1 | 1 | 1 |
| about | `instagram/profile/about` | 30 | 1 | 30 |

**Deeper** `instagram/search/reels` - country= (the instagram-creators-by-country recipe) drops other markets for you and fills followers in the same call, at a higher price per creator.

**Pitfalls**

- region= supports ES, MX, DE, BR, KR and FR only; any other code is a free 400.
- Two reels by one creator are one candidate: deduplicate post.author.username before the lookups, and look up only the creators you would keep.
- author.ext.country is the country the creator declares, and is null when Instagram publishes none; treat a null as unknown, not as a match.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const reels = await sc("instagram/search/reels", { query: "matcha", region: "DE" });
const about = [];
for (const row of reels.data.items.slice(0, 30)) {
  about.push(await sc("instagram/profile/about", { handle: row.post.author.username }));
}
```

## Vet a creator before a partnership

**When** "is this influencer legit", "check a creator's engagement and brand safety", "fake followers or controversy check"

**Inputs**

- `handle`: The creator's handle (e.g. `mkbhd`)
- `platform`: tiktok, youtube or instagram (e.g. `youtube`)

**Chain**

1. `GET /v1/prism/creator-vet?handle=<handle>&platform=<platform>` - Engagement rate, commenter quality, posting cadence and a judged brand-safety read with every flagged item linked to its source.

**Cost** for one creator: 50 credits held up front (exact; the unused hold is refunded).

**Cheaper** `prism/creator-card` - Just the profile cards and follower totals across platforms, without the vetting.

**Pitfalls**

- include=cross_platform adds the cross-platform identity check at a higher price; leave it off unless you need it.
- Namesakes found in the news are excluded and counted in namesakes_excluded, not blamed on the creator.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const vet = await sc("prism/creator-vet", { handle: "mkbhd", platform: "youtube" });
```

## One creator on every platform

**When** "find this creator's TikTok, Instagram, YouTube and X", "total followers across platforms", "is this the same person on each platform"

**Inputs**

- `handle`: The handle to look up (e.g. `mrbeast`)

**Chain**

1. `GET /v1/prism/creator-card?handle=<handle>&platforms=tiktok,instagram,youtube,twitter&verify=true` - verify=true adds an identity verdict per platform (same, possible, different) at the same price.

**Cost** for one handle on four platforms: 5 credits held up front (exact; the unused hold is refunded).

**Deeper** `prism/find-accounts` - When the handle differs by platform: turn a name into ranked candidate accounts.

**Pitfalls**

- A handle existing on a platform does not mean it is the same creator; without verify=true you only learn that the handle exists.
- A null card means the handle was not found there; only a miss on every platform is refunded.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const cards = await sc("prism/creator-card", { handle: "mrbeast", platforms: "tiktok,instagram,youtube,twitter", verify: "true" });
```

## A creator's profile, recent posts and the comments on them

**When** "get a creator's profile, latest videos and their comments", "analyse a TikTok creator's recent content", "comments on a creator's last videos"

**Inputs**

- `handle`: The TikTok handle (e.g. `charlidamelio`)

**Chain**

1. `GET /v1/tiktok/profile?handle=<handle>`
2. `GET /v1/tiktok/profile/videos?handle=<handle>` - Each row's post.url feeds the comments call.
3. `GET /v1/tiktok/post/comments?url=<videos.items[].post.url>` - once per row of `videos`. One call per video you want comments for; pick the videos first rather than fanning out over the whole page.

**Cost** for profile, one page of videos, first comment page on five videos: 7 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| profile | `tiktok/profile` | 1 | 1 | 1 |
| videos | `tiktok/profile/videos` | 1 | 1 | 1 |
| comments | `tiktok/post/comments` | 5 | 1 | 5 |

**Cheaper** `tiktok/profile/full` - Profile, recent posts and computed engagement metrics in one call, without comments.

**Deeper** `prism/comments` - Every comment on one video, replies nested, in one call.

**Pitfalls**

- The comments step is billed per video and per page; the fan-out, not the profile, is what grows the bill.
- The same chain exists per platform: instagram/profile/posts then instagram/post/comments, youtube/channel/videos then youtube/video/comments.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const profile = await sc("tiktok/profile", { handle: "charlidamelio" });
const videos = await sc("tiktok/profile/videos", { handle: "charlidamelio" });
const comments = [];
for (const row of videos.data.items.slice(0, 5)) {
  comments.push(await sc("tiktok/post/comments", { url: row.post.url }));
}
```

## Find the social accounts of a person or company

**When** "what are this company's social accounts", "find a person's Instagram, TikTok, X and LinkedIn", "I only have a name"

**Inputs**

- `name`: The person's or company's name (e.g. `Ogilvy`)
- `type`: person or company (e.g. `company`)

**Chain**

1. `GET /v1/prism/find-accounts?name=<name>&type=<type>` - Ranked candidates per platform, each with a match level, for a person to review.

**Cost** for one name: 17 credits held up front (settles 2-17; the unused hold is refunded).

**Deeper** `prism/creator-card` - Once you know the handle, cards and an identity verdict across platforms.

**Pitfalls**

- The match level is a ranking for human review, not proof of identity.
- Pass website= when you know the official domain: a verified account linking to it is taken as the match without judging.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const accounts = await sc("prism/find-accounts", { name: "Ogilvy", type: "company" });
```

## A LinkedIn member's profile and recent posts

**When** "LinkedIn profile and posts for a person", "everything on someone's LinkedIn"

**Inputs**

- `profile_url`: The member's /in/ profile URL (e.g. `https://www.linkedin.com/in/williamhgates/`)

**Chain**

1. `GET /v1/linkedin/profile?url=<profile_url>` - The canonical Author: name, headline (bio), location, exact followers and connections.
2. `GET /v1/linkedin/profile/posts?url=<profile_url>` - Recent posts as a canonical PostList, one fixed window; limit (up to 100) sets how many.

**Cost** for one member, default post window: 10 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| profile | `linkedin/profile` | 1 | 5 | 5 |
| posts | `linkedin/profile/posts` | 1 | 5 | 5 |

**Cheaper** `linkedin/profile/with-posts` - Profile, counts, recent posts and background in one premium call instead of two.

**Deeper** `linkedin/profile/posts/archive` - The member's complete post history with exact times, billed per post returned.

**Pitfalls**

- linkedin/profile/full is a COMPANY page composite; for a member /in/ URL it is the wrong endpoint.
- linkedin/profile/posts has no next page: a cursor or page= is rejected. Above fifty posts the price is per post returned.
- Experience, education and skills are not on linkedin/profile; use linkedin/profile/complete or linkedin/profile/all.

**Which one**

| Option | Endpoint | Best for | Cost shape |
|--------|----------|----------|------------|
| Identity and counts only | `linkedin/profile` | Name, headline, location, followers, connections; the urn for sub-resources | flat per call |
| Recent posts only | `linkedin/profile/posts` | Up to a hundred recent posts in one fixed window | flat up to fifty posts, then per post returned |
| Profile, counts and recent posts together | `linkedin/profile/with-posts` | One call for a person card plus their latest posts and background | flat per call |
| Background without counts | `linkedin/profile/complete` | Experience, education, skills and recommendations; followers are null | flat per call |
| Every section in one call | `linkedin/profile/all` | A full audit: all background sections, interests, similar profiles, verified flag | per profile returned, up to ten profiles per call |
| Company page with posts and engagement metrics | `linkedin/profile/full` | A /company/ URL only; never a member | flat per call |

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const profile = await sc("linkedin/profile", { url: "https://www.linkedin.com/in/williamhgates/" });
const posts = await sc("linkedin/profile/posts", { url: "https://www.linkedin.com/in/williamhgates/" });
```

## Find LinkedIn members by role and company

**When** "find marketing directors at a company on LinkedIn", "LinkedIn people search with filters", "build a list of prospects"

**Inputs**

- `keywords`: Search keywords (e.g. `head of marketing`)

**Chain**

1. `GET /v1/linkedin/search/people?query=<keywords>` - Ten members a page with handle, headline, location and the profile URL. Add include=profile (with limit for the top rows) to join exact follower and connection counts in the same call.
2. `GET /v1/linkedin/profile/complete?url=<people.items[].author.url>` - once per row of `people`. Only for the members you shortlist.

**Cost** for one page of ten members, three backgrounds: 40 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| people | `linkedin/search/people` | 1 | 10 | 10 |
| background | `linkedin/profile/complete` | 3 | 10 | 30 |

**Pitfalls**

- On a plain search, author.followers is LinkedIn's rounded display bucket (author.ext.followers_approximate is true); include=profile makes it exact.
- current_company and past_company take the numeric company id (author.id on linkedin/company), not a name.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const people = await sc("linkedin/search/people", { query: "head of marketing" });
const background = [];
for (const row of people.data.items.slice(0, 3)) {
  background.push(await sc("linkedin/profile/complete", { url: row.author.url }));
}
```

## Look up a list of handles in one call

**When** "vet a spreadsheet of creator handles", "follower counts for 50 accounts", "bulk profile lookup across platforms"

**Inputs**

- `items`: JSON array of up to 50 {platform, handle, custom_id?}

**Chain**

1. `POST /v1/prism/profiles` body `{"items":"<items>"}` - One canonical Author per row in input order, with a status and the caller's custom_id echoed.

**Cost** for fifty handles: about 50 credits held up front (settles 1-50; the unused hold is refunded); a batch is priced at a cycled example body, so quote your real list first.

**Deeper** `prism/jobs` - Up to five thousand handles as one background job at the same per-row price.

**Pitfalls**

- At most fifty items per call (twenty-five with include=posts); split larger lists or use prism/jobs.
- Each row is priced at its platform's own rate (LinkedIn rows cost more); not_found, unsupported and errored rows are refunded.
- Do not loop the single profile endpoints for a list: one batch call is cheaper to run and to retry.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const profiles = await sc("prism/profiles", undefined, { method: "POST", body: {"items":[{"platform":"tiktok","handle":"@scout2015"},{"platform":"instagram","handle":"nasa"}]} });
```

## Export the latest N comments on a TikTok video

**When** "get/export/download comments on this TikTok", "last 200 comments", "TikTok comments to CSV"

**Inputs**

- `url`: The TikTok video URL

**Chain**

1. `GET /v1/tiktok/post/comments?url=<url>&sort=recent&scan_pages=3` - repeat with `cursor=<pagination.next_cursor>` until 200 rows or `has_more=false`. Reads up to three pages per call and returns them newest first.

**Cost** for two hundred comments: ≥ 15 credits held up front (settles 5-15; the unused hold is refunded); a count or fan-out is unknown, so this is a floor: quote the whole job with GET /v1/utility/estimate or scripts/estimate.py.

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| comments | `tiktok/post/comments` | 5 | 3 | 15 |

**Cheaper** `prism/comments` - One call with max=N that pages to N for you, metered per comment page scanned.

**Pitfalls**

- sort=recent sorts only what was read; TikTok has no native newest-first order, so raise scan_pages to read more of the thread.
- The endpoint is tiktok/post/comments; tiktok/video/comments does not exist.
- On prism/comments set max (the default is a thousand) and replies=false unless you want replies, or the hold is far larger than the job.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const comments: unknown[] = [];
let cursor: string | undefined;
do {
  const r = await sc("tiktok/post/comments", { url: "https://www.tiktok.com/@stoolpresidente/video/7623818255903329566", sort: "recent", scan_pages: "3", cursor });
  comments.push(...r.data.items);
  cursor = r.pagination.has_more ? r.pagination.next_cursor : undefined;
} while (cursor && comments.length < 200);
```

```sh
python3 scripts/paginate.py tiktok/post/comments --items 200 url=https://www.tiktok.com/@stoolpresidente/video/7623818255903329566 sort=recent scan_pages=3
```

The quote is not exact yet, so set --max-credits from your quote.

## Every comment on any post, in one call

**When** "all comments on this YouTube video", "scrape every comment on a Reddit thread", "comments with replies on a post"

**Inputs**

- `url`: A TikTok, YouTube, Facebook, Reddit, Hacker News or Instagram post URL (e.g. `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
- `max_comments`: Stop after about this many top-level comments (e.g. `500`)

**Chain**

1. `GET /v1/prism/comments?url=<url>&max=<max_comments>&replies=false` - Pages the thread server-side to max; replies=true nests replies where the platform has them.

**Cost** for five hundred top-level comments: 10 credits held up front (settles 2-10; the unused hold is refunded).

**Cheaper** `youtube/video/comments` - One page of a single platform's comments, when you only need the first page.

**Pitfalls**

- max drives the price: leave it at its default and a long thread is read to a thousand comments.
- Whole pages are returned, so the count can slightly exceed max.
- Instagram returns top-level comments only at a flat price; replies come from instagram/post/comment/replies, one call per parent with engagement.replies above zero.
- sort=top on Instagram is the platform's own finite ranked head; use the default order to harvest the whole thread.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const comments = await sc("prism/comments", { url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", max: "500", replies: "false" });
```

## Which comments are questions, complaints or buyers

**When** "what are people saying under this post", "find purchase intent in comments", "complaints in the comments"

**Inputs**

- `url`: The TikTok video URL

**Chain**

1. `GET /v1/tiktok/post/comments?url=<url>&label=question,complaint,purchase_intent` - Each comment carries computed.labels for the presets named.

**Cost** for one page of comments: 1 credit held up front (exact; the unused hold is refunded).

**Deeper** `prism/comment-leads` - Buyer leads from the comments of every post a keyword search returns.

**Pitfalls**

- sentiment, question, purchase_intent and complaint are free default labels; spam, toxic and low_quality are paid.
- prism/comments takes no label= (an undeclared param is ignored); it judges the free presets on the first comments of each call by default.
- SocialCrawl reads public data only: there is no endpoint that replies, posts or acts as the user.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const comments = await sc("tiktok/post/comments", { url: "https://www.tiktok.com/@stoolpresidente/video/7623818255903329566", label: "question,complaint,purchase_intent" });
```

## Transcribe a video

**When** "transcript of this YouTube video", "what is said in this TikTok", "get captions to summarise a video"

**Inputs**

- `url`: The YouTube video URL (e.g. `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)

**Chain**

1. `GET /v1/youtube/video/transcript?url=<url>`

**Cost** for one video: 3 credits held up front (exact; the unused hold is refunded).

**Deeper** `youtube/transcripts` - Up to a hundred YouTube transcripts in one POST, by bare video id.; `prism/video-intel` - Video detail, stats, top comments and (with include=transcript) the transcript for one video in one call.

**Pitfalls**

- Each platform has its own transcript endpoint: tiktok/post/transcript, instagram/media/transcript, twitter/tweet/transcript, facebook/post/transcript.
- youtube/transcripts takes bare eleven-character ids, not watch URLs.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const transcript = await sc("youtube/video/transcript", { url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ" });
```

## Compare one product's reviews across retailers

**When** "Amazon vs Walmart reviews for one product", "compare ratings and complaints across stores", "what buyers say about a product on different retailers"

**Inputs**

- `product`: The product name, as a shopper would search it (e.g. `Anker Soundcore Life Q30`)

**Chain**

1. `GET /v1/amazon/product-search?query=<product>&country=US` - Pick the row that is the product itself; its product.id is the ASIN.
2. `GET /v1/amazon/reviews?country=US&asin=<amazon_search.items[].product.id>`
3. `GET /v1/walmart/search?query=<product>` - product.id is the Walmart item id the reviews call takes.
4. `GET /v1/walmart/reviews?product_id=<walmart_search.items[].product.id>`

**Cost** for first review page at two retailers: 16 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| amazon_search | `amazon/product-search` | 1 | 1 | 1 |
| amazon_reviews | `amazon/reviews` | 1 | 5 | 5 |
| walmart_search | `walmart/search` | 1 | 5 | 5 |
| walmart_reviews | `walmart/reviews` | 1 | 5 | 5 |

**Deeper** `prism/product-reviews` - A themed pros-and-cons report across Amazon, Google Shopping and Trustpilot only.

**Pitfalls**

- Never call a reviews endpoint with a guessed id: resolve the ASIN, item id, TCIN or SKU through that retailer's search first.
- prism/product-reviews covers Amazon, Google Shopping and Trustpilot only; it has no Walmart, Target, Home Depot or Wayfair leg.
- amazon/reviews returns one fixed page of on-page reviews (about eight) and does not page.
- A Walmart id from one marketplace (US or CA) does not resolve in the other.

**Which one**

| Option | Endpoint | Best for | Cost shape |
|--------|----------|----------|------------|
| Report across Amazon, Google Shopping and Trustpilot | `prism/product-reviews` | One themed pros-and-cons report over those three sources only | flat per call |
| Amazon | `amazon/reviews` | On-page reviews by ASIN from amazon/product-search | per page |
| Walmart | `walmart/reviews` | Reviews by item id from walmart/search, sortable and paged | per page |
| Target | `target/reviews` | Reviews by TCIN from target/category or a product URL | per page |
| Home Depot | `home_depot/reviews` | Reviews by item id from home_depot/search | per page |
| Wayfair | `wayfair/reviews` | Reviews by SKU from wayfair/search | per page |
| Google Shopping | `google_shopping/reviews` | Aggregated reviews by gid (product.ext.gid on google_shopping/product-search) | per page |
| TikTok Shop | `tiktokshop/product/reviews` | Reviews of a TikTok Shop product by URL or product id | per page |
| Trustpilot (the business, not one product) | `trustpilot/reviews` | Company reviews by domain | per page |

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const amazon_search = await sc("amazon/product-search", { query: "Anker Soundcore Life Q30", country: "US" });
const amazon_reviews = await sc("amazon/reviews", { country: "US", asin: amazon_search.data.items[0].product.id });
const walmart_search = await sc("walmart/search", { query: "Anker Soundcore Life Q30" });
const walmart_reviews = await sc("walmart/reviews", { product_id: walmart_search.data.items[0].product.id });
```

## A Home Depot product's price and reviews

**When** "price and reviews for a drill at Home Depot", "Home Depot product reviews", "is this tool in stock and what do buyers say"

**Inputs**

- `product`: Product name or model number (e.g. `DEWALT 20V MAX cordless drill DCD771C2`)

**Chain**

1. `GET /v1/home_depot/search?query=<product>` - Each row has the item id, price, rating and stock; pick the matching model.
2. `GET /v1/home_depot/reviews?item_id=<search.items[].product.id>`

**Cost** for one search page and the first review page: 10 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| search | `home_depot/search` | 1 | 5 | 5 |
| reviews | `home_depot/reviews` | 1 | 5 | 5 |

**Pitfalls**

- home_depot/search is the keyword-to-item-id resolver; never call home_depot/reviews with a guessed item_id.
- A null price.current comes with product.ext.price_note (for example see final price in cart); prices are the online price.
- prism/product-reviews and the amazon endpoints do not cover Home Depot.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const search = await sc("home_depot/search", { query: "DEWALT 20V MAX cordless drill DCD771C2" });
const reviews = await sc("home_depot/reviews", { item_id: search.data.items[0].product.id });
```

## One report on a product's reviews across marketplaces

**When** "pros and cons of a product from its reviews", "summarise reviews across Amazon and Google Shopping", "review themes for a product"

**Inputs**

- `product`: The product name (e.g. `AirPods Pro 3`)

**Chain**

1. `GET /v1/prism/product-reviews?query=<product>` - Resolves the product on Amazon, Google Shopping and Trustpilot, then returns per-source ratings, a retailer matrix and themed pros and cons.

**Cost** for one product: 30 credits held up front (exact; the unused hold is refunded).

**Cheaper** `amazon/reviews` - One retailer's reviews when you already have the ASIN.

**Pitfalls**

- Three sources only: Amazon, Google Shopping and Trustpilot. For Walmart, Target, Home Depot or Wayfair, chain that retailer's search and reviews.
- Anchor with asin= or gid= for precision; the gid is product.ext.gid, not the catalog id.
- Commerce sources are slow: allow tens of seconds per call.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const report = await sc("prism/product-reviews", { query: "AirPods Pro 3" });
```

## Reviews of a mobile app

**When** "App Store reviews for an app", "what users complain about in our app", "Google Play and App Store ratings"

**Inputs**

- `app`: The app name (e.g. `Spotify`)

**Chain**

1. `GET /v1/app_store/app-search?query=<app>` - app.id is the numeric App Store id the reviews call takes.
2. `GET /v1/app_store/app-reviews?sort_by=most_recent&app_id=<search.items[].app.id>`

**Cost** for one app, first review page: 10 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| search | `app_store/app-search` | 1 | 5 | 5 |
| reviews | `app_store/app-reviews` | 1 | 5 | 5 |

**Deeper** `prism/app-reviews` - Both stores at once, translated, clustered and sentiment-scored.

**Pitfalls**

- The two stores use different ids: a numeric id on the App Store, a package name (com.spotify.music) on Google Play; resolve each through its own app-search.
- The same chain on Google Play is google_play/app-search then google_play/app-reviews.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const search = await sc("app_store/app-search", { query: "Spotify" });
const reviews = await sc("app_store/app-reviews", { sort_by: "most_recent", app_id: search.data.items[0].app.id });
```

## Reviews of a local business

**When** "Yelp reviews for a restaurant", "what customers say about a shop", "reviews of businesses near a location"

**Inputs**

- `business`: Business name or category (e.g. `pizza`)
- `location`: City or neighbourhood (e.g. `New York, NY`)

**Chain**

1. `GET /v1/yelp/search?query=<business>&location=<location>` - place.id is the business encid the reviews call takes.
2. `GET /v1/yelp/business/reviews?id=<search.items[].place.id>`

**Cost** for one search page, one business's first review page: 6 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| search | `yelp/search` | 1 | 1 | 1 |
| reviews | `yelp/business/reviews` | 1 | 5 | 5 |

**Cheaper** `google/business/extended-reviews` - Google's reviews for one business by name, with no search step.

**Pitfalls**

- Yelp alias slugs (prince-street-pizza-new-york-2) are not accepted; use the encid from yelp/search.
- For hotels and attractions use the tripadvisor endpoints.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const search = await sc("yelp/search", { query: "pizza", location: "New York, NY" });
const reviews = await sc("yelp/business/reviews", { id: search.data.items[0].place.id });
```

## See the ads a competitor is running

**When** "what ads is a competitor running", "Facebook ads of a brand", "ad library search"

**Inputs**

- `company`: The advertiser's name (e.g. `Lululemon`)

**Chain**

1. `GET /v1/facebook/adlibrary/company/ads?companyName=<company>&status=ACTIVE` - Active ads in the public Facebook ad library for that advertiser.

**Cost** for one page of ads: 5 credits held up front (exact; the unused hold is refunded).

**Cheaper** `facebook/adlibrary/search/ads` - Keyword search of the ad library when you do not know the advertiser.

**Pitfalls**

- Pass pageId instead of companyName when several pages share the name.
- Each network has its own library; see the decision table.

**Which one**

| Option | Endpoint | Best for | Cost shape |
|--------|----------|----------|------------|
| Facebook and Instagram | `facebook/adlibrary/company/ads` | One advertiser's ads by name or page id, with status and media filters | per page |
| Google (Search, YouTube, Maps, Play, Shopping) | `google/company/ads` | One advertiser's ads by domain or advertiser id | per page |
| LinkedIn | `linkedin/ads/search` | A company's or a keyword's LinkedIn ads | per page |
| TikTok | `tiktok/adlibrary/search` | Ads by keyword or advertiser name | per page |

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const ads = await sc("facebook/adlibrary/company/ads", { companyName: "Lululemon", status: "ACTIVE" });
```

## Track a creator's new posts every day

**When** "poll a creator's new posts daily", "alert me when this account posts", "only fetch posts I do not have yet"

**Inputs**

- `handle`: The Instagram handle (e.g. `instagram`)
- `webhook_url`: HTTPS URL that receives each run (e.g. `https://example.com/hooks/socialcrawl`)
- `last_run_date`: Date of your previous run, YYYY-MM-DD; leave since out on the first run (e.g. `2026-09-30`)

**Chain**

1. `GET /v1/instagram/profile/posts?handle=<handle>&since=<last_run_date>` - Run by hand with the date of your last run; the page that reaches since ends the walk, so you stop paying for posts you already hold. Do not copy a fixed last_run_date into the monitor: its setup uses since=now-1d.

**Schedule it**

1. `POST /v1/monitors` body `{"recipe":"instagram/profile/posts","params":{"handle":"<handle>","since":"now-1d"},"cadence":"daily","webhook_url":"<webhook_url>","track":{"metrics":["items[].post.engagement.likes"]},"alert_rules":[{"metric":"rows_new","op":"gt","value":0}],"suppress_webhook_unless_alert":true}` - Runs the read every day with since set to yesterday and posts to your webhook only when a run has a post the previous run did not. Create is free and returns estimated_cost_per_run and next_run_at; there is no immediate first run.

**Cost** Creating is free. Each scheduled run bills 2 credits (`instagram/profile/posts` read plus 1 scheduling credit; `estimated_cost_per_run` on create); 1 run per day ≈ 2 credits/day. Running the read by hand once holds 1 credit.

**Pitfalls**

- since stops the walk; it does not make the page that reaches it free.
- Pinned posts sit out of date order and never end the walk.
- A scheduled run bills the read's own price plus a small scheduling premium; /v1/monitors returns estimated_cost_per_run and estimated_monthly_cost on create.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const posts = await sc("instagram/profile/posts", { handle: "instagram", since: "2026-09-30" });
const s1 = await sc("monitors", undefined, { method: "POST", body: {"recipe":"instagram/profile/posts","params":{"handle":"instagram","since":"now-1d"},"cadence":"daily","webhook_url":"https://example.com/hooks/socialcrawl","track":{"metrics":["items[].post.engagement.likes"]},"alert_rules":[{"metric":"rows_new","op":"gt","value":0}],"suppress_webhook_unless_alert":true} });
```

## Weekly alert on a competitor's new YouTube videos

**When** "weekly YouTube competitor monitor", "alert on new videos from a channel", "watch a competitor's uploads"

**Inputs**

- `handle`: The channel handle (e.g. `mkbhd`)
- `webhook_url`: HTTPS URL that receives each run (e.g. `https://example.com/hooks/socialcrawl`)
- `last_run_date`: Date of the previous run, YYYY-MM-DD (e.g. `2026-09-25`)

**Chain**

1. `GET /v1/youtube/channel/videos?handle=<handle>&since=<last_run_date>` - The read the monitor replays; run it by hand to see what one run returns. Do not copy a fixed last_run_date into the monitor: its setup uses since=now-7d.

**Schedule it**

1. `POST /v1/monitors` body `{"recipe":"youtube/channel/videos","params":{"handle":"<handle>","since":"now-7d"},"cadence":"weekly","webhook_url":"<webhook_url>","track":{"metrics":["items[].post.engagement.views"]},"alert_rules":[{"metric":"rows_new","op":"gt","value":0}],"suppress_webhook_unless_alert":true}` - Each weekly run reads the uploads of the last seven days and posts to your webhook only when it holds a video the previous run did not; the first run has nothing to compare and stays quiet.

**Cost** Creating is free. Each scheduled run bills 2 credits (`youtube/channel/videos` read plus 1 scheduling credit; `estimated_cost_per_run` on create); 1 run per week ≈ 2 credits per week. Running the read by hand once holds 1 credit.

**Pitfalls**

- Do not build your own cron or polling loop: /v1/monitors schedules any registered GET read and delivers to a signed webhook.
- /v1/web/monitors is a different family that watches one web page; it is not for a channel's uploads.
- since requires sort=latest on this endpoint (filled in when sort is absent).
- Alert on new videos with the rows_new alert (gt 0) on a track monitor, not on a numeric threshold; deltas.rows_new lists the new ids.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const videos = await sc("youtube/channel/videos", { handle: "mkbhd", since: "2026-09-25" });
const s1 = await sc("monitors", undefined, { method: "POST", body: {"recipe":"youtube/channel/videos","params":{"handle":"mkbhd","since":"now-7d"},"cadence":"weekly","webhook_url":"https://example.com/hooks/socialcrawl","track":{"metrics":["items[].post.engagement.views"]},"alert_rules":[{"metric":"rows_new","op":"gt","value":0}],"suppress_webhook_unless_alert":true} });
```

## Alert when a web page changes

**When** "alert me when a pricing page changes", "watch a URL for changes every 15 minutes", "monitor a competitor's web page"

**Inputs**

- `page_url`: The page to watch (e.g. `https://example.com/pricing`)
- `cadence_minutes`: Minutes between checks: 5 to 60, or whole hours (e.g. `15`)
- `webhook_url`: HTTPS URL that receives a signed callback on each check (e.g. `https://example.com/hooks/socialcrawl`)

**Chain**

1. `POST /v1/web/monitors` body `{"url":"<page_url>","cadence_minutes":"<cadence_minutes>","webhook_url":"<webhook_url>"}` - Creating the monitor is free; data.monitor_id names it.
2. `GET /v1/web/monitors/<monitor.monitor_id>/checks` - Reading the checks is free; the webhook means you rarely need to.

**Cost** Creating and reading are free. Each check bills at least 2 credits (the page read, at least 1 credit, plus 1 for orchestration; the page read can bill more); 96 checks per day at least 192 credits/day.

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| monitor | `web/monitors` | 1 | 0 | 0 |
| checks | `web/monitors/{monitor_id}/checks` | 1 | 0 | 0 |

**Pitfalls**

- Creating is free but every check bills the page read plus an orchestration premium: quote checks per day (1440 / cadence_minutes) times the per-check price.
- /v1/monitors (recipe monitors, one-hour floor) is the wrong family for one page; /v1/web/monitors checks as often as every five minutes.
- The change judge is on by default, so you are notified on meaningful changes rather than every byte-level diff; pass goal= to say what matters.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const monitor = await sc("web/monitors", undefined, { method: "POST", body: {"url":"https://example.com/pricing","cadence_minutes":"15","webhook_url":"https://example.com/hooks/socialcrawl"} });
const checks = await sc(`web/monitors/${monitor.data.monitor_id}/checks`);
```

## Engagement stats for a list of post URLs

**When** "views, likes and comments for 500 URLs", "refresh stats for a spreadsheet of post links", "verify clipper payouts"

**Inputs**

- `urls`: JSON array of up to 100 post URLs, any mix of platforms

**Chain**

1. `POST /v1/prism/post-stats` body `{"urls":"<urls>"}` - One row per URL in input order: platform, status, views, likes, comments, shares, saves and fetched_at. Send larger lists in chunks of a hundred.

**Cost** for five hundred URLs in chunks of a hundred: about 500 credits held up front (settles 5-500; the unused hold is refunded); a batch is priced at a cycled example body, so quote your real list first.

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| stats | `prism/post-stats` | 5 | 100 | 500 |

**Deeper** `prism/jobs` - Up to five thousand URLs as one background job at the same per-URL price, with a webhook when it completes.

**Pitfalls**

- At most a hundred URLs per call: five hundred URLs is five calls, or one prism/jobs job.
- Each URL is priced at its platform's own rate (Instagram and LinkedIn cost more than TikTok and YouTube); quote per platform, not one flat rate per URL.
- Dead, errored and unsupported URLs are refunded; one bad link never fails the batch.
- Do not loop the single-post endpoints: it is slower and no cheaper.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const stats = await sc("prism/post-stats", undefined, { method: "POST", body: {"urls":["https://www.youtube.com/watch?v=dQw4w9WgXcQ","https://www.tiktok.com/@stoolpresidente/video/7623818255903329566"]} });
```

## Which of my accounts posted about a keyword

**When** "which of our customers' accounts posted about our brand", "search only the handles in my CSV for a keyword", "did any of these creators mention us last month"

**Inputs**

- `cohort_name`: A label for the list (e.g. `Q3 customers`)
- `members`: JSON array of {platform, handle, external_id}, up to a thousand per upload
- `keywords`: JSON array of one to twenty keywords (e.g. `["acme"]`)
- `date_from`: Window start as a full RFC3339 timestamp (e.g. `2026-09-01T00:00:00.000Z`)
- `date_to`: Window end as a full RFC3339 timestamp (e.g. `2026-09-30T23:59:59.999Z`)
- `max_pages`: Page budget for each feed a member is read from, one to twenty; a feed with no next page reads one page whatever you set (e.g. `2`)
- `max_credits`: Safety limit: the query is rejected when its computed ceiling is above it (e.g. `400`)

**Chain**

1. `POST /v1/cohorts` body `{"name":"<cohort_name>"}` - Free. Send an Idempotency-Key header holding a UUID; data.id is the cohortId.
2. `PUT /v1/cohorts/{cohortId}/members` body `{"members":"<members>"}` - Free. One chunk per call with its own Idempotency-Key; external_id comes back on every match so you can join results to your records.
3. `POST /v1/cohorts/{cohortId}/queries` body `{"keywords":"<keywords>","date_from":"<date_from>","date_to":"<date_to>","max_pages_per_identity":"<max_pages>","max_items_per_identity":200,"max_credits":"<max_credits>"}` - Holds the full computed ceiling (estimated_credits) up front and runs in the background; data.query_id is the queryId.
4. `GET /v1/cohort-queries/{queryId}` - Free. Poll until status is terminal: succeeded, failed, cancelled or expired.
5. `GET /v1/cohort-queries/{queryId}/results` - Free, and only once status is succeeded (any other status is a 409). One row per matching member with its external_id and matched keywords, plus coverage per member.

**Cost** for two hundred accounts, two pages each: a cohort query holds its full computed ceiling (`estimated_credits`), which depends on the members, platforms and page budget; see references/cohorts.md. Creating the cohort, uploading members, polling and reading results are free.

**Pitfalls**

- Do not search the whole platform (prism/brand-mentions, search/everywhere) or loop each handle's posts endpoint: a cohort query reads only your accounts and caps the spend.
- date_from and date_to are full RFC3339 timestamps with an offset; a bare YYYY-MM-DD is a 400.
- The hold is always the full computed ceiling (estimated_credits). max_credits is only a guard: a ceiling above it rejects the query before anything is held. The unused hold is refunded when the query ends, and a 402 means your balance (or the key's spend cap) is below the ceiling.
- The ceiling counts each member at its platform's price: X, TikTok, Kwai and Truth Social cost a page price times max_pages, Instagram and YouTube twice that; LinkedIn, Bluesky, Threads and Twitch ignore the page budget and cost a fixed amount per member, and LinkedIn is the most expensive.
- A feed with no next page reads exactly one page whatever max_pages says; naming platforms in the query is the other way to cut the ceiling.
- POST and PUT need an Idempotency-Key UUID header; everything is scoped to the API key, not the account.
- Results are served only when status is succeeded, and succeeded is not exhaustive: read each member's coverage.
- Facebook and Snapchat accounts are rejected at upload; ten platforms are supported.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const s1 = await sc("cohorts", undefined, { method: "POST", body: {"name":"Q3 customers"}, idempotencyKey: crypto.randomUUID() });
const cohortId = s1.data.id;
const s2 = await sc(`cohorts/${cohortId}/members`, undefined, { method: "PUT", body: {"members":[{"platform":"tiktok","handle":"mrbeast","external_id":"cust_001"},{"platform":"twitter","handle":"nasa","external_id":"cust_002"}]}, idempotencyKey: crypto.randomUUID() });
const s3 = await sc(`cohorts/${cohortId}/queries`, undefined, { method: "POST", body: {"keywords":["acme"],"date_from":"2026-09-01T00:00:00.000Z","date_to":"2026-09-30T23:59:59.999Z","max_pages_per_identity":2,"max_items_per_identity":200,"max_credits":400}, idempotencyKey: crypto.randomUUID() });
const queryId = s3.data.query_id;
const s4 = await sc(`cohort-queries/${queryId}`, undefined, { method: "GET" });
const s5 = await sc(`cohort-queries/${queryId}/results`, undefined, { method: "GET" });
```

## Pay for a role in a country, and the open jobs

**When** "what do senior data engineers earn in Germany", "salary range and open remote jobs", "job listings for a title"

**Inputs**

- `title`: The job title (e.g. `senior data engineer`)
- `country_code`: ISO 3166-1 alpha-2 country code (e.g. `de`)
- `location`: City or country for the listings (e.g. `Germany`)

**Chain**

1. `GET /v1/jobs/salary?query=<title>&country_code=<country_code>` - The pay band for the title in that country.
2. `GET /v1/jobs/linkedin/search?query=<title>&location=<location>&workplace_types=remote` - One page of listings; follow cursor for more.

**Cost** for one salary lookup and one page of listings: 11 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| salary | `jobs/salary` | 1 | 1 | 1 |
| listings | `jobs/linkedin/search` | 1 | 10 | 10 |

**Cheaper** `jobs/salary/titles` - Find the job title the salary data knows before you look it up.

**Pitfalls**

- Listing rows carry a salary only when the board publishes one; the pay band comes from jobs/salary.
- The listing searches are premium endpoints, priced well above the salary lookup.
- jobs/bing/search needs location on its first page; jobs/indeed/search takes country_code.
- workplace_types, employment_types and experience_levels are semicolon-separated.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const salary = await sc("jobs/salary", { query: "senior data engineer", country_code: "de" });
const listings = await sc("jobs/linkedin/search", { query: "senior data engineer", location: "Germany", workplace_types: "remote" });
```

## A stock's current price and latest headlines

**When** "current price of NVIDIA stock and its news", "stock quote and headlines", "how is a company's share price doing"

**Inputs**

- `company`: Company or instrument name (e.g. `NVIDIA`)

**Chain**

1. `GET /v1/finance/ticker-search?keyword=<company>` - quote.id is the TICKER:EXCHANGE form (NVDA:NASDAQ) the quote call takes.
2. `GET /v1/finance/quote?keyword=<ticker.items[].quote.id>`
3. `GET /v1/finance/news?keyword=<ticker.items[].quote.id>` - Recent articles for the instrument, as a NewsArticleList.

**Cost** for one instrument: 7 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| ticker | `finance/ticker-search` | 1 | 1 | 1 |
| quote | `finance/quote` | 1 | 5 | 5 |
| news | `finance/news` | 1 | 1 | 1 |

**Pitfalls**

- Every finance endpoint takes keyword, not ticker= or symbol=.
- Pass finance/quote the TICKER:EXCHANGE id from finance/ticker-search, not the company name.
- finance/news takes the instrument directly; google_news/search and search/news are for topics, not tickers.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const ticker = await sc("finance/ticker-search", { keyword: "NVIDIA" });
const quote = await sc("finance/quote", { keyword: ticker.data.items[0].quote.id });
const news = await sc("finance/news", { keyword: ticker.data.items[0].quote.id });
```

## Crawl a site and get each page as markdown

**When** "crawl the first 50 pages of a docs site", "download a website as markdown", "scrape every page under a path"

**Inputs**

- `site_url`: Root URL to crawl (e.g. `https://docs.example.com/`)
- `max_pages`: Most pages to crawl (e.g. `50`)

**Chain**

1. `POST /v1/web/crawl` body `{"url":"<site_url>","limit":"<max_pages>","formats":"markdown"}` - An async job: the response carries job_id and the credits held for limit pages.
2. `GET /v1/web/jobs/<crawl.job_id>` - Poll until status is completed (or pass webhook_url on the crawl); reading the job is free.

**Cost** for fifty pages: 50 credits held up front (settles 1-50; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| crawl | `web/crawl` | 1 | 50 | 50 |
| result | `web/jobs/{job_id}` | 1 | 0 | 0 |

**Cheaper** `web/map` - List the site's URLs first, then crawl only the paths you need.

**Pitfalls**

- Always set limit: the crawl holds limit pages up front (ten by default) and refunds the pages it did not crawl.
- include_paths is the cheapest way to narrow a crawl; allow_external_links makes limit the only bound.
- Do not loop web/scrape over every page; one crawl job is the same per-page price with one call to manage.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const crawl = await sc("web/crawl", undefined, { method: "POST", body: {"url":"https://docs.example.com/","limit":"50","formats":"markdown"} });
const result = await sc(`web/jobs/${crawl.data.job_id}`);
```

## Pull structured fields from a web page

**When** "extract the prices from this page", "get the plan names and features from a pricing page", "turn a web page into JSON"

**Inputs**

- `page_url`: The page to read (e.g. `https://example.com/pricing`)
- `prompt`: What to extract, in plain words (e.g. `Each plan's name, monthly price and included seats`)

**Chain**

1. `GET /v1/web/extract?url=<page_url>&prompt=<prompt>`

**Cost** for one page: 5 credits held up front (exact; the unused hold is refunded).

**Cheaper** `web/scrape` - The page as markdown, when you will read it yourself.

**Pitfalls**

- Pass schema= (a JSON schema) instead of prompt= when you need fixed field names.
- For changes to the same page over time, use the web-page-change-alert recipe instead of re-extracting.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const extract = await sc("web/extract", { url: "https://example.com/pricing", prompt: "Each plan's name, monthly price and included seats" });
```

## What Korean consumers say about a product, and search interest

**When** "what are Korean consumers saying about a product", "Korean news, blogs and cafe posts about a brand", "Korean search interest over the last year"

**Inputs**

- `keyword`: The keyword, in Korean (e.g. `불닭볶음면`)

**Chain**

1. `GET /v1/naver/brief?query=<keyword>&corpora=news,blog,cafearticle` - One query across the Naver corpora you name; include=digest adds an English digest with translated quotes.
2. `GET /v1/naver/search-trend?keywords=<keyword>&time_unit=month` - Twelve months by default; the series is relative search volume.

**Cost** for one brief and one trend series: 15 credits held up front (exact; the unused hold is refunded).

| Step | Endpoint | Runs | Hold each | Hold total |
|------|----------|------|-----------|------------|
| posts | `naver/brief` | 1 | 10 | 10 |
| trend | `naver/search-trend` | 1 | 5 | 5 |

**Cheaper** `naver/blog/search` - One Naver corpus only (also naver/news/search, naver/cafearticle/search).

**Deeper** `prism/korea-gap` - What Korea says about a topic against what the rest of the web says.

**Pitfalls**

- Search in Korean: translating the keyword to English misses most Korean posts.
- naver/search-trend takes keywords, not query, and sums several keywords into ONE series; call it once per term to compare.
- Western indexes (google_trends, tiktok/search) miss most Korean search; use the Naver endpoints.

**Code**

```ts
// sc(path, params?, { method?, body?, idempotencyKey? }?) -> parsed JSON body; URL-encodes params and skips undefined; canonical client: references/codegen.md
const posts = await sc("naver/brief", { query: "불닭볶음면", corpora: "news,blog,cafearticle" });
const trend = await sc("naver/search-trend", { keywords: "불닭볶음면", time_unit: "month" });
```
