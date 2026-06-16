# YouTube

17 endpoints. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: most endpoints cost 1 credit (standard); trending shorts costs 5 (advanced); sponsor detection and video transcript cost 10 (premium); the `profile/full` Prism composite is a flat 5 credits — exact cost listed per endpoint below.

## GET /v1/youtube/channel — 1 credit (standard)

Get YouTube channel info

- `channelId` (optional, string) — YouTube channel ID. Can pass a channelId, handle or url
- `handle` (optional, string) — YouTube channel handle without the @ symbol
- `url` (optional, string) — YouTube channel URL. Can pass a channelId, handle or url

**At least one of `channelId` / `handle` / `url` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/youtube/channel" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/channel/videos — 1 credit (standard)

List YouTube channel videos

- `channelId` (optional, string) — YouTube channel ID
- `handle` (optional, string) — YouTube channel handle without the @ symbol
- `sort` (optional, enum: latest | popular) — Sort by latest or popular
- `continuationToken` (optional, string) — Continuation token to get more videos. Get 'continuationToken' from previous response.
- `includeExtras` (optional, string) — This will get you the like + comment count and the description. To get the full details of the video, use the /v1/youtube/video endpoint. This will slow down the response slightly.
- `is_paid_promotions` (optional, string) — Set to 'true' to search YouTube's public paid product placement / sponsorship / endorsement surface — returns normal videos where the creator disclosed a paid promotion.

**At least one of `channelId` / `handle` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/youtube/channel/videos" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/video — 1 credit (standard)

Get YouTube video details

- `url` (required) — Full URL of the YouTube video
- `language` (optional, string) — Preferred response language (mapped to Accept-Language header; not guaranteed due to YouTube localization behavior). 2 letter language code, ie 'en', 'es', 'fr' etc.

```bash
curl "https://www.socialcrawl.dev/v1/youtube/video?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/video/sponsors — 10 credits (premium)

Detect sponsors of a YouTube video

- `url` (required) — Full URL of the YouTube video or short
- `language` (optional, string) — 2 letter language code used for transcript lookup, ie 'en', 'es', 'fr' etc.

```bash
curl "https://www.socialcrawl.dev/v1/youtube/video/sponsors?url=https://www.youtube.com/watch?v=AVO0ifle-OU" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/video/comments — 1 credit (standard)

List YouTube video comments

- `url` (required) — Full URL of the YouTube video to fetch comments for
- `continuationToken` (optional, string) — Continuation token to get more comments. Get 'continuationToken' from previous response.
- `order` (optional, enum: top | newest) — Order of comments

```bash
curl "https://www.socialcrawl.dev/v1/youtube/video/comments?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/video/comment/replies — 1 credit (standard)

List YouTube comment replies

- `continuationToken` (required) — Continuation token for the comment replies. Use 'repliesContinuationToken' from the Comments endpoint, or 'continuationToken' from a previous replies response to paginate.

```bash
curl "https://www.socialcrawl.dev/v1/youtube/video/comment/replies?continuationToken=Eg0SC2RRdzR3OVdnWGNRGAYygwEaUBIa..." \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/search — 1 credit (standard)

Search YouTube

- `query` (required) — Search keyword or phrase.
- `uploadDate` (optional, enum: today | this_week | this_month | this_year) — Upload date filter.
- `sortBy` (optional, enum: relevance | popular) — Sort order — relevance or popular.
- `type` (optional, enum: videos | shorts | channels | playlists) — Type of content to return.
- `duration` (optional, enum: under_3_min | between_3_and_20_min | over_20_min) — Video duration filter. Only applies to videos (not shorts).
- `region` (optional, string) — 2-letter country code of the country to put the proxy in.
- `continuationToken` (optional, string) — Continuation token to get more results. Get `continuationToken` from a previous response.
- `includeExtras` (optional, string) — Set to `true` to include like + comment count and description. For full per-video details use `/v1/youtube/video`. Slows the response slightly.

```bash
curl "https://www.socialcrawl.dev/v1/youtube/search?query=javascript tutorial" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/channel/shorts — 1 credit (standard)

List YouTube channel shorts

- `handle` (optional, string) — YouTube channel handle without the @ symbol
- `channelId` (optional, string) — Can pass channelId or handle
- `sort` (optional, enum: newest | popular) — Sort by newest or popular
- `continuationToken` (optional, string) — Continuation token to get more videos. Get 'continuationToken' from previous response.

**At least one of `channelId` / `handle` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/youtube/channel/shorts" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/community-post — 1 credit (standard)

Get YouTube community post

- `url` (required) — Full URL of the YouTube community post

```bash
curl "https://www.socialcrawl.dev/v1/youtube/community-post?url=https://www.youtube.com/post/Ugkxvj2KoApYAXoqLWnKVr6zZe5JjeHrQeP8" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/playlist — 1 credit (standard)

Get YouTube playlist

- `playlist_id` (required) — YouTube playlist ID

```bash
curl "https://www.socialcrawl.dev/v1/youtube/playlist?playlist_id=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/search/hashtag — 1 credit (standard)

Search YouTube by hashtag

- `hashtag` (required) — Hashtag to search for without the # symbol
- `continuationToken` (optional, string) — Continuation token to get more videos. Get 'continuationToken' from previous response.
- `type` (optional, enum: all | shorts) — Search for all types of content or only shorts

```bash
curl "https://www.socialcrawl.dev/v1/youtube/search/hashtag?hashtag=shorts" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/shorts/trending — 5 credits (advanced)

Get trending YouTube shorts

No parameters.

```bash
curl "https://www.socialcrawl.dev/v1/youtube/shorts/trending" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/video/transcript — 10 credits (premium)

Get YouTube video transcript

- `url` (required) — Full URL of the YouTube video
- `language` (optional, string) — 2 letter language code, ie 'en', 'es', 'fr' etc. If the transcript is not available in the language you specify, the transcript will be null.

```bash
curl "https://www.socialcrawl.dev/v1/youtube/video/transcript?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/channel/playlists — 1 credit (standard)

List a YouTube channel's playlists

- `channelId` (optional, string) — YouTube channel ID.
- `handle` (optional, string) — YouTube channel handle (with or without @).
- `continuationToken` (optional, string) — Continuation token from a previous response — fetches the next page.

**At least one of `channelId` / `handle` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/youtube/channel/playlists" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/channel/lives — 1 credit (standard)

List a YouTube channel's live streams

- `channelId` (optional, string) — YouTube channel ID.
- `handle` (optional, string) — YouTube channel handle (with or without @).
- `continuationToken` (optional, string) — Continuation token from a previous response — fetches the next page.

**At least one of `channelId` / `handle` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/youtube/channel/lives" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/channel/community-posts — 1 credit (standard)

List a YouTube channel's community posts

- `channelId` (optional, string) — YouTube channel ID.
- `handle` (optional, string) — YouTube channel handle (with or without @).
- `continuationToken` (optional, string) — Continuation token from a previous response — fetches the next page.

**At least one of `channelId` / `handle` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/youtube/channel/community-posts" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/youtube/profile/full — 5 credits (flat override)

Profile-360 composite — channel profile, recent posts, and a computed analytics block (avg engagement rate, posts/week cadence, top post, format mix) folded into one call. Part of the "Prism" composite family.

- `handle` (optional, string) — YouTube channel handle without the @ symbol.
- `channelId` (optional, string) — YouTube channel ID.
- `url` (optional, string) — YouTube channel URL.
- `posts` (optional, integer) — How many recent posts to fetch + average the computed metrics over (1–100, default 25).
- `cursor` (optional, string) — Pass a prior response's `posts_cursor` to deepen the post window.
- `include` (optional, string) — CSV subset of `posts,computed` (default both). `include=computed` drops the raw `posts[]` to save payload.

```bash
curl "https://www.socialcrawl.dev/v1/youtube/profile/full?handle=mkbhd" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
