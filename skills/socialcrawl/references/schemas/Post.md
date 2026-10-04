# Post fields

Every field the 38 field-mapped endpoints returning `Post` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `computed.content_category` | string\|null | Keyword-classified content category (e.g. tech, food, gaming). Null when undetectable. |
| `computed.engagement_rate` | number\|null | Computed engagement rate (0..1). Null when the upstream lacks enough signal. |
| `computed.estimated_reach` | number\|null | Estimated reach based on views or follower count. Null when uncomputable. |
| `computed.language` | string\|null | ISO 639-1 language code detected from the post text. Null when undetectable. |
| `post.author.avatar_url` | string\|null | URL to author profile picture (on some endpoints only when the fallback source serves) |
| `post.author.display_name` | string\|null | Author display name |
| `post.author.username` | string\|null | Author username (on some endpoints only when the fallback source serves) |
| `post.author.verified` | boolean\|null | Whether the account carries TikTok's verification badge. The source sends a badge label rather than a flag, and the API writes false when no label is present, so false can also mean the source sent no verification signal. (on some endpoints only when the fallback source serves) |
| `post.content.duration_seconds` | number\|null | Video/clip duration in seconds (null for non-video posts) |
| `post.content.media_urls` | string\|array\|null | URL(s) of the primary media. Single string for video/photo posts; array of strings for carousels. |
| `post.content.text` | string\|null | Post caption, description, or text content |
| `post.content.thumbnail_url` | string\|null | URL to thumbnail image (on some endpoints only when the fallback source serves) |
| `post.engagement.comments` | number\|null | Comment count. Note: on `GET /v1/instagram/post` this is Instagram's `edge_media_to_parent_comment.count` (top-level comments); the IG list endpoints report the mobile `comment_count` total (includes replies). Both land on this same field. |
| `post.engagement.likes` | number\|null | Like / reaction count |
| `post.engagement.saves` | number\|null | Save / bookmark count. `null` on Instagram: the save count is platform-private and Instagram exposes no numeric save metric on any surface (never fabricated). (on some endpoints only when the fallback source serves) |
| `post.engagement.shares` | number\|null | Share / repost / retweet count. On Instagram this is `reshare_count` (the paper-plane Share / Send count) and it exists only on Instagram's mobile surface, so it is returned by `/v1/instagram/post/stats`, `/v1/instagram/profile/reels/full`, and `/v1/instagram/profile/posts/full`. The web-sourced Instagram list and search endpoints return `null` (never fabricated). (on some endpoints only when the fallback source serves) |
| `post.engagement.views` | number\|null | View count (if available). For Instagram video/reels this is the play count: the headline 'Views' the IG app shows. Instagram removed per-post play counts from its public web pages in August 2026, so `GET /v1/instagram/post` now fills the count automatically from a second source within the same call: videos and reels keep a numeric `views` with no extra endpoint or workaround. Note: since mid-July 2026 Instagram's play count is Instagram-only. It no longer includes Facebook crosspost views (Meta-side change; the app UI changed identically). For combined reach, also fetch the Facebook crosspost via `/v1/facebook/post`. (on some endpoints only when the fallback source serves) |
| `post.ext.ad.audit_status` | unknown\|null |  |
| `post.ext.ad.brand_name` | unknown\|null |  |
| `post.ext.ad.caption` | unknown\|null |  |
| `post.ext.ad.categories` | unknown\|null |  |
| `post.ext.ad.country_code` | unknown\|null |  |
| `post.ext.ad.cta_text` | unknown\|null |  |
| `post.ext.ad.cta_type` | unknown\|null |  |
| `post.ext.ad.currency` | unknown\|null |  |
| `post.ext.ad.display_format` | unknown\|null |  |
| `post.ext.ad.end_date_iso` | unknown\|null |  |
| `post.ext.ad.eu_reach_breakdown` | unknown\|null |  |
| `post.ext.ad.eu_total_reach` | unknown\|null |  |
| `post.ext.ad.image_urls` | unknown\|null |  |
| `post.ext.ad.is_active` | unknown\|null |  |
| `post.ext.ad.landing_page` | unknown\|null |  |
| `post.ext.ad.last_shown_date` | unknown\|null |  |
| `post.ext.ad.link_url` | unknown\|null |  |
| `post.ext.ad.objectives` | unknown\|null |  |
| `post.ext.ad.page_categories` | unknown\|null |  |
| `post.ext.ad.page_id` | unknown\|null |  |
| `post.ext.ad.page_like_count` | unknown\|null |  |
| `post.ext.ad.page_profile_uri` | unknown\|null |  |
| `post.ext.ad.profile_web_link` | unknown\|null |  |
| `post.ext.ad.publisher_platforms` | unknown\|null |  |
| `post.ext.ad.reach_estimate` | unknown\|null |  |
| `post.ext.ad.source` | unknown\|null |  |
| `post.ext.ad.spend` | unknown\|null |  |
| `post.ext.ad.target_ages` | unknown\|null |  |
| `post.ext.ad.target_gender` | unknown\|null |  |
| `post.ext.ad.target_locations` | unknown\|null |  |
| `post.ext.ad.targets_eu` | unknown\|null |  |
| `post.ext.ad.title` | unknown\|null |  |
| `post.ext.ad.video_hd_url` | unknown\|null |  |
| `post.ext.ad.video_sd_url` | unknown\|null |  |
| `post.ext.all_media_urls` | array\|null | (seen in a sample response) |
| `post.ext.amazon_shop_curations` | array\|null |  |
| `post.ext.amazon_shop_lists` | array\|null |  |
| `post.ext.amazon_shop_socials` | array\|null |  |
| `post.ext.amazon_shop_trending_picks` | array\|null |  |
| `post.ext.apple_music.artist_url` | unknown\|null |  |
| `post.ext.apple_music.explicit` | unknown\|null |  |
| `post.ext.apple_music.kind` | unknown\|null |  |
| `post.ext.apple_music.release_info` | unknown\|null |  |
| `post.ext.apple_music.track_count` | unknown\|null |  |
| `post.ext.apple_music.track_number` | unknown\|null |  |
| `post.ext.article.source` | string\|null | (seen in a sample response) |
| `post.ext.article.title` | string\|null | (seen in a sample response) |
| `post.ext.article.url` | string\|null | (seen in a sample response) |
| `post.ext.author_followers` | number\|null | The creator's follower count as embedded in the search payload itself, when the search source happens to carry one. On `instagram/search/reels` it is null on a plain call, because Instagram stopped sending follower counts in its search payload in August 2026; send `include=creator` (or `country`) and it is filled from the creator's profile, 2 credits per creator looked up. It stays null when that lookup does not resolve. |
| `post.ext.author_following` | number\|null |  |
| `post.ext.author_headline` | string\|null | (seen in a sample response) |
| `post.ext.author_id` | string\|null | The creator's platform-native numeric user id. On TikTok search and list items, pass to `/v1/tiktok/profile?user_id=` for the creator's current follower count (survives username changes). On `instagram/search/reels` items it is present on every row from every serving source, accepted by `/v1/instagram/basic-profile?userId=`. On Facebook it appears when the upstream exposed a numeric actor id and no real handle. (on some endpoints only when the fallback source serves) |
| `post.ext.author_posts_count` | number\|null |  |
| `post.ext.author_type` | string\|null | (seen in a sample response) |
| `post.ext.author_urn` | string\|null | (seen in a sample response) |
| `post.ext.categoryTitle` | string\|null | (only when the fallback source serves) |
| `post.ext.channel_id` | string\|null |  |
| `post.ext.coauthors` | array\|null | Instagram collaborative posts (the native "Collab" feature). The full list of co-author accounts on the post, as `{ id, username, full_name, is_verified, profile_pic_url }`. A collab post has ONE producer and appears in every co-author's grid, so `post.author` is whichever account created it, which is not necessarily the profile you queried. The complete set of accounts on a post is `post.author.username` plus every `username` in this array. An empty array means Instagram reports the post as NOT a collab; the field is absent on surfaces that carry no co-author signal, including `/v1/instagram/post` (its web source ships the field permanently empty, so use `/v1/instagram/post/stats` for a single post). (seen in a sample response) |
| `post.ext.commerce.attributes` | unknown\|null |  |
| `post.ext.commerce.availability_text` | unknown\|null |  |
| `post.ext.commerce.category_id` | unknown\|null |  |
| `post.ext.commerce.currency` | unknown\|null |  |
| `post.ext.commerce.delivery_types` | unknown\|null |  |
| `post.ext.commerce.description` | unknown\|null |  |
| `post.ext.commerce.is_buy_now_enabled` | unknown\|null |  |
| `post.ext.commerce.is_hidden` | unknown\|null |  |
| `post.ext.commerce.is_live` | unknown\|null |  |
| `post.ext.commerce.is_pending` | unknown\|null |  |
| `post.ext.commerce.is_shipping_offered` | unknown\|null |  |
| `post.ext.commerce.is_sold` | unknown\|null |  |
| `post.ext.commerce.latitude` | unknown\|null |  |
| `post.ext.commerce.listing_date_text` | unknown\|null |  |
| `post.ext.commerce.location_text` | unknown\|null |  |
| `post.ext.commerce.longitude` | unknown\|null |  |
| `post.ext.commerce.messaging_enabled` | unknown\|null |  |
| `post.ext.commerce.mileage` | unknown\|null |  |
| `post.ext.commerce.price` | unknown\|null |  |
| `post.ext.commerce.price_formatted` | unknown\|null |  |
| `post.ext.commerce.seller_id` | unknown\|null |  |
| `post.ext.commerce.seller_name` | unknown\|null |  |
| `post.ext.commerce.strikethrough_price_formatted` | unknown\|null |  |
| `post.ext.content_language` | string\|null | The language the platform itself tags the post with, when it sends one: Reddit's own language tag on Reddit endpoints, and TikTok's caption-language tag (for example `de`) on `/v1/tiktok/trending?feed=local`. Null when the platform could not tell (Reddit `und`, TikTok `un`, common on short or emoji-only captions); absent where the source sends no tag. Never inferred from the text by us: that is `post.computed.language`. |
| `post.ext.description` | string\|null | (on some endpoints only when the fallback source serves) |
| `post.ext.download_count` | number\|null | How many times the video has been saved to a device. TikTok only, and distinct from `engagement.saves`: a save keeps the video in a private collection on the platform, a download takes a copy off it, and TikTok counts the two separately. Present on TikTok post, search and post-list responses; absent everywhere else. (on some endpoints only when the fallback source serves) |
| `post.ext.event.address` | unknown\|null |  |
| `post.ext.event.attendance_count` | unknown\|null |  |
| `post.ext.event.category` | unknown\|null |  |
| `post.ext.event.city` | unknown\|null |  |
| `post.ext.event.description` | unknown\|null |  |
| `post.ext.event.duration_text` | unknown\|null |  |
| `post.ext.event.end_timestamp` | unknown\|null |  |
| `post.ext.event.going_count` | unknown\|null |  |
| `post.ext.event.host_context_text` | unknown\|null |  |
| `post.ext.event.hosts` | unknown\|null |  |
| `post.ext.event.interested_count` | unknown\|null |  |
| `post.ext.event.is_canceled` | unknown\|null |  |
| `post.ext.event.is_online` | unknown\|null |  |
| `post.ext.event.is_past` | unknown\|null |  |
| `post.ext.event.latitude` | unknown\|null |  |
| `post.ext.event.location_name` | unknown\|null |  |
| `post.ext.event.longitude` | unknown\|null |  |
| `post.ext.event.privacy` | unknown\|null |  |
| `post.ext.event.start_timestamp` | unknown\|null |  |
| `post.ext.event.ticket_url` | unknown\|null |  |
| `post.ext.event.time_text` | unknown\|null |  |
| `post.ext.flair` | string\|null |  |
| `post.ext.hasPaidProductPlacement` | boolean\|null | (only when the fallback source serves) |
| `post.ext.ig_play_count` | number\|null | Instagram-only play count (`ig_play_count`). Since mid-July 2026 Instagram's headline play count (`engagement.views`) no longer includes Facebook crosspost views and equals this value; it is surfaced explicitly so you can tell the Instagram-only figure apart and detect any future re-divergence. For combined Instagram + Facebook reach, also fetch the Facebook crosspost via `/v1/facebook/post`. Present on `/v1/instagram/post/stats` and, since the August 2026 views fix, on `/v1/instagram/post` for video posts. (on some endpoints only when the fallback source serves) |
| `post.ext.ip_location` | string\|null |  |
| `post.ext.media_type` | string\|null | (seen in a sample response) |
| `post.ext.music_id` | string\|null | TikTok music/clip id (exact string): pass to `/v1/tiktok/song/videos?clipId=` to find videos using the same sound |
| `post.ext.music.artist` | string\|null | (seen in a sample response) |
| `post.ext.music.id` | string\|null | (seen in a sample response) |
| `post.ext.music.is_original` | boolean\|null | (seen in a sample response) |
| `post.ext.music.track_title` | string\|null | (seen in a sample response) |
| `post.ext.post_type` | string\|null | (seen in a sample response) |
| `post.ext.published_at_epoch` | number\|null | Raw Unix epoch for `published_at` (seconds, or milliseconds when the upstream sent millis). Present only when the upstream sent a numeric epoch that was normalised to the ISO 8601 `published_at` string. Kept for one deprecation cycle for integrations pinned to the numeric form. (seen in a sample response) |
| `post.ext.published_at_precision` | string\|null |  |
| `post.ext.quote_count` | number\|null |  |
| `post.ext.reaction_counts` | array\|null |  |
| `post.ext.remix_count` | number\|null | (seen in a sample response) |
| `post.ext.repost_count` | number\|null | (on some endpoints only when the fallback source serves) |
| `post.ext.reshare_count` | number\|null |  |
| `post.ext.selftext` | string\|null |  |
| `post.ext.subreddit` | string\|null | Reddit subreddit name (search/list items): pass to `/v1/reddit/subreddit/details?subreddit=` |
| `post.ext.tags` | array\|null | (only when the fallback source serves) |
| `post.ext.title` | string\|null |  |
| `post.ext.topic_tag` | string\|null |  |
| `post.ext.topic_tag_id` | string\|null |  |
| `post.ext.upvote_ratio` | number\|null | Reddit only: the share of a post's votes that are upvotes, as a fraction from 0 to 1 and usually close to 1 (six live rows measured 1, 1, 1, 0.86, 0.75, 1). Fractional despite the integer type this schema emits for every numeric leaf, the same caveat as `author.ext.average_rating`. Populated on `/v1/reddit/search` rows whose source carries it, and null everywhere else on Reddit including `/v1/reddit/post` and `/v1/reddit/subreddit`. |
| `post.ext.video_count` | number\|null |  |
| `post.flags.deleted` | boolean | Whether the post is tombstoned (always present) |
| `post.flags.nsfw` | boolean\|null | NSFW flag (null when platform does not surface) (seen in a sample response) |
| `post.flags.pinned` | boolean\|null | Pinned-to-profile flag (null when platform does not surface) |
| `post.flags.spoiler` | boolean\|null | Spoiler flag (null when platform does not surface) (seen in a sample response) |
| `post.id` | string | Platform-specific post ID (always a string; numeric upstream IDs are stringified) |
| `post.published_at` | string\|number\|null | Post creation timestamp as an ISO 8601 UTC string. When the upstream sent a Unix epoch it is converted here and the raw epoch is preserved under `post.ext.published_at_epoch` for one deprecation cycle. (on some endpoints only when the fallback source serves) |
| `post.url` | string\|null | Direct URL to the post on the source platform (on some endpoints only when the fallback source serves) |
