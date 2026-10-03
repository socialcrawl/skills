# PostList fields

Every field the 106 field-mapped endpoints returning `PostList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `computed.content_category` | string\|null | Keyword-classified content category (e.g. tech, food, gaming). Null when undetectable. |
| `computed.engagement_rate` | number\|null | Computed engagement rate (0..1). Null when the upstream lacks enough signal. |
| `computed.estimated_reach` | number\|null | Estimated reach based on views or follower count. Null when uncomputable. |
| `computed.labels_evidence` | object\|null | When 1, every labelled row also carries computed.labels_evidence.<preset> = { quote, sentence_index }: the sentence in the row that most clearly shows the label, copied verbatim. (with `label_evidence=1`) |
| `computed.labels.injection` | object\|null | injection flags text that addresses an AI system and tries to direct it (flagged, p); it never drops or rewrites a row. (with `label=injection`) |
| `computed.labels.intent` | object\|null | intent: what the author is mainly doing (label: asking_for_recommendation, comparing_options, switching_away, complaining, promoting, news_or_discussion, other, or null when unsure, with confidence), whether they read as a potential buyer rather than a seller (buyer, seller), how pressing the need is (urgency, 0 to 3), and, when you pass offer=, whether your offer would plausibly help them (fits_offer). |
| `computed.labels.mention` | object\|null | mention (needs brand=): is the post about that brand rather than something that shares its name (about_brand, 0 to 1), how it feels about the brand on five levels (sentiment_level 0 to 4 and sentiment_score 0 to 1, null when the post is not about the brand), is it sarcastic, which aspect it talks about (taste_or_quality, price_or_value, availability_or_delivery, health_or_safety, advertising_or_campaign, customer_service, none), and did the author buy or use it (first_hand). (with `label=mention`) |
| `computed.labels.niche` | object\|null | niche: which of the 33 niches of the published taxonomy sc-niche-v1 the caption belongs to, or personal_no_niche, or other (label, confidence, taxonomy), with label null when the caption is too thin to tell or the pick is unsure. |
| `computed.labels.quality` | object\|null | quality: how much checkable detail the caption carries (fact_density 0 to 3), whether it mainly asks for likes, replies, shares, follows or tags (engagement_bait, 0 to 1), whether it is written to provoke anger as a way to get engagement (rage_bait, 0 to 1; about the writing, never the side taken), whether it only repeats someone else's news or view (secondhand, 0 to 1), and what the post is mainly doing (post_aim: inform, opinion, sell, entertain, provoke, other). (with `label=quality`) |
| `computed.labels.sponsored` | object\|null | sponsored: is the post a paid or gifted promotion (p, 0 to 1), did it carry a disclosure marker such as #ad or 광고 (disclosed), is it likely paid with no marker (undisclosed), and which of the accounts it mentions does it promote (brand, or null). |
| `computed.language` | string\|null | ISO 639-1 language code detected from the post text. Null when undetectable. |
| `computed.relevance` | object\|null | Without this param every row already carries computed.relevance against your query, free ({ p, sense, depth, spam }: is this row about what your query means, or a different thing that shares its words?), and nothing is dropped or reordered. |
| `computed.vs_creator` | object\|null |  |
| `post.author.avatar_url` | string\|null | URL to author profile picture (with `include=ad`, `include=channel`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.author.display_name` | string\|null | Author display name (with `include=engagement`, `include=creator`, `include=channel`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.author.url` | unknown\|null |  |
| `post.author.username` | string\|null | Author username (with `include=channel` on some endpoints) |
| `post.author.verified` | boolean\|null | Whether the account carries TikTok's verification badge. The source sends a badge label rather than a flag, and the API writes false when no label is present, so false can also mean the source sent no verification signal. (on some endpoints only when the fallback source serves) |
| `post.content.duration_seconds` | number\|null | Video/clip duration in seconds (null for non-video posts) (with `include=engagement` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.content.media_urls` | string\|array\|null | URL(s) of the primary media. Single string for video/photo posts; array of strings for carousels. (on some endpoints only when the fallback source serves) |
| `post.content.text` | string\|null | Post caption, description, or text content |
| `post.content.thumbnail_url` | string\|null | URL to thumbnail image (with `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.engagement.comments` | number\|null | Comment count. Note: on `GET /v1/instagram/post` this is Instagram's `edge_media_to_parent_comment.count` (top-level comments); the IG list endpoints report the mobile `comment_count` total (includes replies). Both land on this same field. (with `include=engagement`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.engagement.likes` | number\|null | Like / reaction count (with `include=engagement`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.engagement.saves` | number\|null | Save / bookmark count. `null` on Instagram: the save count is platform-private and Instagram exposes no numeric save metric on any surface (never fabricated). (with `include=engagement` on some endpoints) |
| `post.engagement.shares` | number\|null | Share / repost / retweet count. On Instagram this is `reshare_count` (the paper-plane Share / Send count) and it exists only on Instagram's mobile surface, so it is returned by `/v1/instagram/post/stats`, `/v1/instagram/profile/reels/full`, and `/v1/instagram/profile/posts/full`. The web-sourced Instagram list and search endpoints return `null` (never fabricated). (with `include=engagement`, `include=details` on some endpoints) |
| `post.engagement.views` | number\|null | View count (if available). For Instagram video/reels this is the play count: the headline 'Views' the IG app shows. Instagram removed per-post play counts from its public web pages in August 2026, so `GET /v1/instagram/post` now fills the count automatically from a second source within the same call: videos and reels keep a numeric `views` with no extra endpoint or workaround. Note: since mid-July 2026 Instagram's play count is Instagram-only. It no longer includes Facebook crosspost views (Meta-side change; the app UI changed identically). For combined reach, also fetch the Facebook crosspost via `/v1/facebook/post`. (with `include=engagement`, `include=details` on some endpoints) |
| `post.ext.ad.ad_format` | unknown\|null |  |
| `post.ext.ad.audit_status` | unknown\|null |  |
| `post.ext.ad.brand_name` | unknown\|null | (with `include=ad`) |
| `post.ext.ad.caption` | unknown\|null |  |
| `post.ext.ad.categories` | unknown\|null |  |
| `post.ext.ad.cost_score` | unknown\|null |  |
| `post.ext.ad.country_code` | unknown\|null | (with `include=ad` on some endpoints) |
| `post.ext.ad.cta_text` | unknown\|null |  |
| `post.ext.ad.cta_type` | unknown\|null |  |
| `post.ext.ad.ctr` | unknown\|null |  |
| `post.ext.ad.currency` | unknown\|null |  |
| `post.ext.ad.display_format` | unknown\|null |  |
| `post.ext.ad.end_date_iso` | unknown\|null |  |
| `post.ext.ad.estimated_audience` | unknown\|null |  |
| `post.ext.ad.eu_reach_breakdown` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.eu_total_reach` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.image_urls` | unknown\|null |  |
| `post.ext.ad.industry` | unknown\|null |  |
| `post.ext.ad.is_active` | unknown\|null |  |
| `post.ext.ad.is_spark_ad` | unknown\|null |  |
| `post.ext.ad.landing_page` | unknown\|null | (with `include=ad`) |
| `post.ext.ad.landing_page_url` | unknown\|null |  |
| `post.ext.ad.language` | unknown\|null |  |
| `post.ext.ad.last_shown_date` | unknown\|null |  |
| `post.ext.ad.like_tier` | unknown\|null |  |
| `post.ext.ad.link_url` | unknown\|null |  |
| `post.ext.ad.objective` | unknown\|null |  |
| `post.ext.ad.objectives` | unknown\|null | (with `include=ad`) |
| `post.ext.ad.page_categories` | unknown\|null |  |
| `post.ext.ad.page_id` | unknown\|null |  |
| `post.ext.ad.page_like_count` | unknown\|null |  |
| `post.ext.ad.page_profile_uri` | unknown\|null |  |
| `post.ext.ad.period_days` | unknown\|null |  |
| `post.ext.ad.profile_web_link` | unknown\|null | (with `include=ad`) |
| `post.ext.ad.publisher_platforms` | unknown\|null |  |
| `post.ext.ad.rank` | unknown\|null |  |
| `post.ext.ad.reach_estimate` | unknown\|null |  |
| `post.ext.ad.source` | unknown\|null | (with `include=ad`) |
| `post.ext.ad.spend` | unknown\|null |  |
| `post.ext.ad.spent` | unknown\|null |  |
| `post.ext.ad.target_ages` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.target_gender` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.target_locations` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.targeted_or_reached_countries` | unknown\|null |  |
| `post.ext.ad.targets_eu` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.title` | unknown\|null |  |
| `post.ext.ad.type` | unknown\|null |  |
| `post.ext.ad.video_hd_url` | unknown\|null |  |
| `post.ext.ad.video_id` | unknown\|null |  |
| `post.ext.ad.video_sd_url` | unknown\|null |  |
| `post.ext.ad.video_url_360p` | unknown\|null |  |
| `post.ext.ad.video_url_540p` | unknown\|null |  |
| `post.ext.apple_music.artist_id` | unknown\|null |  |
| `post.ext.apple_music.artist_url` | unknown\|null |  |
| `post.ext.apple_music.content_advisory` | unknown\|null |  |
| `post.ext.apple_music.genres` | unknown\|null |  |
| `post.ext.apple_music.kind` | unknown\|null |  |
| `post.ext.apple_music.release_date` | unknown\|null |  |
| `post.ext.author_country` | string\|null | The creator's country as they declare it on Instagram's About this account panel, as a country name (for example `Spain`). It is not where the reel was filmed. Present only on `/v1/instagram/search/reels` when the request sends `include=creator` (or `country`), filled by looking the creator up. Null when Instagram does not publish a country for the creator or the lookup did not resolve, and nothing is guessed; absent on a plain call. (with `include=creator`) |
| `post.ext.author_followers` | number\|null | The creator's follower count as embedded in the search payload itself, when the search source happens to carry one. On `instagram/search/reels` it is null on a plain call, because Instagram stopped sending follower counts in its search payload in August 2026; send `include=creator` (or `country`) and it is filled from the creator's profile, 2 credits per creator looked up. It stays null when that lookup does not resolve. (with `include=channel`, `include=creator` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.ext.author_following` | number\|null | (with `include=creator` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.ext.author_id` | string\|null | The creator's platform-native numeric user id. On TikTok search and list items, pass to `/v1/tiktok/profile?user_id=` for the creator's current follower count (survives username changes). On `instagram/search/reels` items it is present on every row from every serving source, accepted by `/v1/instagram/basic-profile?userId=`. On Facebook it appears when the upstream exposed a numeric actor id and no real handle. (with `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.ext.author_posts_count` | number\|null | (with `include=creator` on some endpoints) |
| `post.ext.author_public_email` | string\|null | The public contact email on the creator's profile. Present only on `/v1/instagram/search/reels` when the request sends `include=creator`, filled by looking the creator up. Null when the creator lists no public email or the lookup did not resolve; absent on a plain call. (with `include=creator`) |
| `post.ext.author_public_phone` | string\|null | The public contact phone number on the creator's profile. Present only on `/v1/instagram/search/reels` when the request sends `include=creator`, filled by looking the creator up. Null when the creator lists no public phone or the lookup did not resolve; absent on a plain call. (with `include=creator`) |
| `post.ext.categoryTitle` | string\|null |  |
| `post.ext.channel_id` | string\|null | (with `include=channel`, `include=engagement` on some endpoints) |
| `post.ext.content_language` | string\|null | The language the platform itself tags the post with, when it sends one: Reddit's own language tag on Reddit endpoints, and TikTok's caption-language tag (for example `de`) on `/v1/tiktok/trending?feed=local`. Null when the platform could not tell (Reddit `und`, TikTok `un`, common on short or emoji-only captions); absent where the source sends no tag. Never inferred from the text by us: that is `post.computed.language`. (on some endpoints only when the fallback source serves) |
| `post.ext.description` | string\|null |  |
| `post.ext.download_count` | number\|null | How many times the video has been saved to a device. TikTok only, and distinct from `engagement.saves`: a save keeps the video in a private collection on the platform, a download takes a copy off it, and TikTok counts the two separately. Present on TikTok post, search and post-list responses; absent everywhere else. |
| `post.ext.event.address` | unknown\|null | (with `include=details`) |
| `post.ext.event.attendance_count` | unknown\|null | (with `include=details`) |
| `post.ext.event.category` | unknown\|null | (with `include=details`) |
| `post.ext.event.city` | unknown\|null | (with `include=details` on some endpoints) |
| `post.ext.event.description` | unknown\|null | (with `include=details`) |
| `post.ext.event.duration_text` | unknown\|null | (with `include=details`) |
| `post.ext.event.going_count` | unknown\|null | (with `include=details` on some endpoints) |
| `post.ext.event.host_context_text` | unknown\|null | (with `include=details`) |
| `post.ext.event.hosts` | unknown\|null | (with `include=details`) |
| `post.ext.event.interested_count` | unknown\|null | (with `include=details` on some endpoints) |
| `post.ext.event.is_canceled` | unknown\|null | (with `include=details` on some endpoints) |
| `post.ext.event.is_online` | unknown\|null |  |
| `post.ext.event.is_past` | unknown\|null |  |
| `post.ext.event.latitude` | unknown\|null | (with `include=details`) |
| `post.ext.event.location_name` | unknown\|null |  |
| `post.ext.event.longitude` | unknown\|null | (with `include=details`) |
| `post.ext.event.privacy` | unknown\|null | (with `include=details`) |
| `post.ext.event.start_timestamp` | unknown\|null |  |
| `post.ext.event.time_text` | unknown\|null |  |
| `post.ext.flair` | string\|null | (on some endpoints only when the fallback source serves) |
| `post.ext.ig_play_count` | number\|null | Instagram-only play count (`ig_play_count`). Since mid-July 2026 Instagram's headline play count (`engagement.views`) no longer includes Facebook crosspost views and equals this value; it is surfaced explicitly so you can tell the Instagram-only figure apart and detect any future re-divergence. For combined Instagram + Facebook reach, also fetch the Facebook crosspost via `/v1/facebook/post`. Present on `/v1/instagram/post/stats` and, since the August 2026 views fix, on `/v1/instagram/post` for video posts. (with `include=engagement`) |
| `post.ext.is_repost_quote` | boolean\|null |  |
| `post.ext.music` | object\|null | (with `include=audio`) |
| `post.ext.music_id` | string\|null | TikTok music/clip id (exact string): pass to `/v1/tiktok/song/videos?clipId=` to find videos using the same sound (with `include=audio` on some endpoints) |
| `post.ext.music.id` | unknown\|null |  |
| `post.ext.music.track_title` | unknown\|null |  |
| `post.ext.published_at_precision` | string\|null |  |
| `post.ext.quote_count` | number\|null |  |
| `post.ext.reaction_counts` | array\|null |  |
| `post.ext.reaction_type` | string\|null |  |
| `post.ext.region` | string\|null | TikTok only: the country TikTok registers the video to, as an ISO 3166-1 alpha-2 code (normally the creator's account country when they posted). It is not the viewer's country, not the `region` you requested, and not a language. On `/v1/tiktok/trending`, `/v1/tiktok/search` and `/v1/tiktok/search/top` it is how you tell which rows are from a given country: filter on it when you need only that country. The `region` request parameter still only sets the proxy. |
| `post.ext.reshare_count` | number\|null |  |
| `post.ext.selftext` | string\|null |  |
| `post.ext.subreddit` | string\|null | Reddit subreddit name (search/list items): pass to `/v1/reddit/subreddit/details?subreddit=` |
| `post.ext.tags` | array\|null |  |
| `post.ext.title` | string\|null |  |
| `post.ext.topic_tag` | string\|null |  |
| `post.ext.topic_tag_id` | string\|null |  |
| `post.ext.trend.boards` | unknown\|null |  |
| `post.ext.trend.chart` | unknown |  |
| `post.ext.trend.chart_title` | unknown\|null |  |
| `post.ext.trend.content_tags` | unknown\|null |  |
| `post.ext.trend.country_code` | unknown\|null |  |
| `post.ext.trend.engagement_rate` | unknown\|null |  |
| `post.ext.trend.industry` | unknown\|null |  |
| `post.ext.trend.industry_id` | unknown\|null |  |
| `post.ext.trend.industry_label` | unknown\|null |  |
| `post.ext.trend.order_by` | unknown\|null |  |
| `post.ext.trend.organic_views` | unknown\|null |  |
| `post.ext.trend.period_days` | unknown\|null |  |
| `post.ext.trend.period_views` | unknown\|null |  |
| `post.ext.trend.popularity_curve` | unknown\|null |  |
| `post.ext.trend.posts` | unknown\|null |  |
| `post.ext.trend.rank` | unknown\|null |  |
| `post.ext.trend.six_second_view_through_rate` | unknown\|null |  |
| `post.ext.trend.top_creators` | unknown\|null |  |
| `post.ext.trend.updated_at` | unknown\|null |  |
| `post.ext.trend.views` | unknown\|null |  |
| `post.ext.updated_at` | string\|null |  |
| `post.ext.upvote_ratio` | number\|null | Reddit only: the share of a post's votes that are upvotes, as a fraction from 0 to 1 and usually close to 1 (six live rows measured 1, 1, 1, 0.86, 0.75, 1). Fractional despite the integer type this schema emits for every numeric leaf, the same caveat as `author.ext.average_rating`. Populated on `/v1/reddit/search` rows whose source carries it, and null everywhere else on Reddit including `/v1/reddit/post` and `/v1/reddit/subreddit`. |
| `post.ext.video_count` | number\|null |  |
| `post.flags.deleted` | boolean | Whether the post is tombstoned (always present) |
| `post.flags.nsfw` | boolean\|null | NSFW flag (null when platform does not surface) |
| `post.flags.pinned` | boolean\|null | Pinned-to-profile flag (null when platform does not surface) (with `include=engagement` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.flags.spoiler` | boolean\|null | Spoiler flag (null when platform does not surface) |
| `post.id` | string | Platform-specific post ID (always a string; numeric upstream IDs are stringified) |
| `post.published_at` | string\|number\|null | Post creation timestamp as an ISO 8601 UTC string. When the upstream sent a Unix epoch it is converted here and the raw epoch is preserved under `post.ext.published_at_epoch` for one deprecation cycle. (with `include=engagement`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.url` | string\|null | Direct URL to the post on the source platform (on some endpoints only when the fallback source serves) |
