# Instagram

15 endpoints. All are GET requests against `https://www.socialcrawl.dev` with header `x-api-key: $SOCIALCRAWL_API_KEY`.

Credit costs on this platform: most endpoints cost 1 credit (standard); trending reels costs 5 (advanced) and media transcript costs 10 (premium) — exact cost listed per endpoint below.

## GET /v1/instagram/profile — 1 credit (standard)

Get Instagram user profile

- `handle` (required) — Instagram username without the @ symbol
- `trim` (optional, boolean) — Set to true to get a trimmed response

```bash
curl "https://www.socialcrawl.dev/v1/instagram/profile?handle=instagram" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/profile/posts — 1 credit (standard)

List Instagram user posts

- `handle` (required) — Instagram username without the @ symbol
- `next_max_id` (optional, string) — Cursor to get next page of results.
- `trim` (optional, boolean) — Set to true to get a trimmed response

```bash
curl "https://www.socialcrawl.dev/v1/instagram/profile/posts?handle=instagram" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/post — 1 credit (standard)

Get Instagram post details

- `url` (required) — Full URL of the Instagram post
- `region` (optional, string) — 2 letter country code to set the proxy in
- `trim` (optional, boolean) — Set to true to get a trimmed response
- `download_media` (optional, boolean) — Set to true to download the video/images and get back permanent Supabase URLs. Costs 10 credits if media is found, 1 credit otherwise.

```bash
curl "https://www.socialcrawl.dev/v1/instagram/post?url=https://www.instagram.com/p/CwA1234abcd/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/post/comments — 1 credit (standard)

List Instagram post comments

- `url` (required) — Full URL of the Instagram post to fetch comments for
- `cursor` (optional, string) — The cursor to get more comments. Get 'cursor' from previous response.

```bash
curl "https://www.socialcrawl.dev/v1/instagram/post/comments?url=https://www.instagram.com/p/CwA1234abcd/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/basic-profile — 1 credit (standard)

Get Instagram basic profile

- `userId` (optional, string) — Instagram numeric user ID

```bash
curl "https://www.socialcrawl.dev/v1/instagram/basic-profile" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/profile/reels — 1 credit (standard)

List Instagram user reels

- `user_id` (optional, string) — Instagram user id. Use this for faster response times.
- `handle` (optional, string) — Instagram username without the @ symbol
- `max_id` (optional, string) — Max id to get more reels. Get 'max_id' from previous response.
- `trim` (optional, boolean) — Set to true for a trimmed down version of the response

**At least one of `user_id` / `handle` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/instagram/profile/reels" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/highlights — 1 credit (standard)

List Instagram story highlights

- `user_id` (optional, string) — Instagram user id. Use for faster response times.
- `handle` (optional, string) — Instagram username without the @ symbol

**At least one of `user_id` / `handle` is required.**

```bash
curl "https://www.socialcrawl.dev/v1/instagram/highlights" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/highlight/detail — 1 credit (standard)

Get Instagram highlight detail

- `id` (optional, string) — Instagram highlight ID — the numeric id, with or without the `highlight:` prefix. Get it from `/v1/instagram/user/highlights`.

```bash
curl "https://www.socialcrawl.dev/v1/instagram/highlight/detail" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/search/reels — 1 credit (standard)

Search Instagram reels

- `query` (required) — Search keyword or phrase to find Instagram reels
- `date_posted` (optional, enum: last-hour | last-day | last-week | last-month | last-year) — Date posted
- `page` (optional, integer) — The page number to return.

```bash
curl "https://www.socialcrawl.dev/v1/instagram/search/reels?query=workout routine" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/media/transcript — 10 credits (premium)

Get Instagram media transcript

- `url` (required) — Full URL of the Instagram video or reel

```bash
curl "https://www.socialcrawl.dev/v1/instagram/media/transcript?url=https://www.instagram.com/reel/DHsD6HGqJhp/" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/user/embed — 1 credit (standard)

Get Instagram user embed HTML

- `handle` (required) — Instagram username without the @ symbol

```bash
curl "https://www.socialcrawl.dev/v1/instagram/user/embed?handle=instagram" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/audio/reels — 1 credit (standard)

List Instagram reels using an audio track

- `audio_id` (required) — Instagram audio ID — the numeric id from an instagram.com/reels/audio/{audio_id}/ URL
- `cursor` (optional, string) — Pagination cursor from the previous response

```bash
curl "https://www.socialcrawl.dev/v1/instagram/audio/reels?audio_id=1392969992841787" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/search/hashtag — 1 credit (standard)

Search Instagram posts by hashtag

- `hashtag` (required) — The hashtag to search for. The leading # is optional.
- `date_posted` (optional, enum: last-hour | last-day | last-week | last-month | last-year) — Only return Google-indexed posts within this relative window.
- `media_type` (optional, enum: all | reels) — `all` returns posts and reels; `reels` returns reels only. Defaults to `all`.
- `cursor` (optional, string) — The cursor returned by the previous response. In this version it is the next Google results page number.

```bash
curl "https://www.socialcrawl.dev/v1/instagram/search/hashtag?hashtag=makeup" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/search/profiles — 1 credit (standard)

Search Instagram profiles by keyword

- `query` (required) — Bio or caption keyword/phrase to search for.
- `cursor` (optional, string) — The cursor returned by the previous response. In this version it is the next Google results page number.

```bash
curl "https://www.socialcrawl.dev/v1/instagram/search/profiles?query=yoga" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```

## GET /v1/instagram/reels/trending — 5 credits (advanced)

Get trending Instagram reels

No parameters.

```bash
curl "https://www.socialcrawl.dev/v1/instagram/reels/trending" \
  -H "x-api-key: $SOCIALCRAWL_API_KEY"
```
