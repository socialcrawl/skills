# Reddit

7 endpoints. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: every endpoint costs 1 credit (standard) except video post transcript at 10 (premium) — exact cost listed per endpoint below.

## GET /v1/reddit/subreddit — 1 credit (standard)

List Reddit subreddit posts

- `subreddit` (required) — Subreddit name without the r/ prefix
- `timeframe` (optional, enum: all | day | week | month | year) — Timeframe to get posts from
- `sort` (optional, enum: best | hot | new | top | rising) — Sort order
- `after` (optional, string) — After to get more posts. Get 'after' from previous response.
- `trim` (optional, boolean) — Set to true for a trimmed down version of the response

```bash
curl "https://www.socialcrawl.dev/v1/reddit/subreddit?subreddit=technology" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/reddit/subreddit/details — 1 credit (standard)

Get Reddit subreddit details

- `subreddit` (optional, string) — Subreddit name without the r/ prefix
- `url` (optional, string) — Subreddit URL

**At least one of `subreddit` / `url` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/reddit/subreddit/details" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/reddit/search — 1 credit (standard)

Search Reddit posts

- `query` (required) — Search keyword or phrase to find Reddit posts
- `sort` (optional, enum: relevance | new | top | comment_count) — Sort by
- `timeframe` (optional, enum: all | day | week | month | year) — Timeframe
- `after` (optional, string) — Used to paginate to next page
- `trim` (optional, boolean) — Set to true for a trimmed down version of the response

```bash
curl "https://www.socialcrawl.dev/v1/reddit/search?query=best programming languages 2024" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/reddit/post/comments — 1 credit (standard)

List Reddit post comments

- `url` (required) — Full URL of the Reddit post to fetch comments for
- `cursor` (optional, string) — Cursor to get more comments, or replies.
- `trim` (optional, boolean) — Set to true for a trimmed down version of the response

```bash
curl "https://www.socialcrawl.dev/v1/reddit/post/comments?url=https://www.reddit.com/r/technology/comments/abc123/example_post/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/reddit/subreddit/search — 1 credit (standard)

Search within a subreddit

- `subreddit` (required) — Subreddit name (e.g. 'Fitness', not 'r/Fitness' or a full URL)
- `query` (optional, string) — Search query to find matching content
- `sort` (optional, enum: relevance | hot | top | new | comments) — Sort order. For posts/media: relevance, hot, top, new, comments. For comments: relevance, top, new
- `timeframe` (optional, enum: all | year | month | week | day | hour) — Timeframe to filter results
- `cursor` (optional, string) — Cursor to get more results. Get 'cursor' from previous response.

```bash
curl "https://www.socialcrawl.dev/v1/reddit/subreddit/search?subreddit=technology" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/reddit/post/transcript — 10 credits (premium)

Get a Reddit video post transcript

- `url` (required) — Reddit post URL or direct v.redd.it video URL.
- `language` (optional, string) — 2-letter language code. Defaults to `en`.

```bash
curl "https://www.socialcrawl.dev/v1/reddit/post/transcript?url=https://www.reddit.com/r/youseeingthisshit/comments/1oiu9xm/football_nostalgiasaints_punter_head_coach_cant/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
