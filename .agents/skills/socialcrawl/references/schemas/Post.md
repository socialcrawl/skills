# Post fields

Every field the 41 field-mapped endpoints returning `Post` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `computed.content_category` | string\|null | Keyword-classified content category (e.g. tech, food, gaming). Null when undetectable. |
| `computed.engagement_rate` | number\|null | Computed engagement rate (0..1). Null when the upstream lacks enough signal. |
| `computed.estimated_reach` | number\|null | Estimated reach based on views or follower count. Null when uncomputable. |
| `computed.language` | string\|null | ISO 639-1 language code detected from the post text. Null when undetectable. |
| `computed.save_rate` | number\|null | Saves divided by views, rounded to six places. Present only when the post has both a save count and a view count above zero. |
| `post.author.avatar_url` | string\|null | URL to author profile picture (on some endpoints only when the fallback source serves) |
| `post.author.display_name` | string\|null | Author display name |
| `post.author.username` | string\|null | Author username (on some endpoints only when the fallback source serves) |
| `post.author.verified` | boolean\|null | Whether the account carries TikTok's verification badge. The source sends a badge label rather than a flag, and the API writes false when no label is present, so false can also mean the source sent no verification signal. (on some endpoints only when the fallback source serves) |
| `post.content.duration_seconds` | number\|null | Video/clip duration in seconds (null for non-video posts) |
| `post.content.media_urls` | string\|array\|null | URL(s) of the primary media. Single string for video/photo posts; array of strings for carousels. |
| `post.content.text` | string\|null | Post caption, description, or text content |
| `post.content.thumbnail_url` | string\|null | URL to thumbnail image (on some endpoints only when the fallback source serves) |
| `post.engagement.comments` | number\|null | Comment count. Note: on `GET /v1/instagram/post` this is Instagram's `edge_media_to_parent_comment.count` (top-level comments); the IG list endpoints report the mobile `comment_count` total (includes replies). Both land on this same field. (with `include=exact_counts` on some endpoints) |
| `post.engagement.likes` | number\|null | Like / reaction count (with `include=exact_counts` on some endpoints) |
| `post.engagement.saves` | number\|null | Save / bookmark count. `null` on Instagram: the save count is platform-private and Instagram exposes no numeric save metric on any surface (never fabricated). (with `include=exact_counts` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.engagement.shares` | number\|null | Share / repost / retweet count. On Instagram this is `reshare_count` (the paper-plane Share / Send count) and it exists only on Instagram's mobile surface, so it is returned by `/v1/instagram/post/stats`, `/v1/instagram/profile/reels/full`, and `/v1/instagram/profile/posts/full`. The web-sourced Instagram list and search endpoints return `null` (never fabricated). (with `include=exact_counts` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.engagement.views` | number\|null | View count (if available). For Instagram video/reels this is the play count: the headline 'Views' the IG app shows. Instagram removed per-post play counts from its public web pages in August 2026, so `GET /v1/instagram/post` now fills the count automatically from a second source within the same call: videos and reels keep a numeric `views` with no extra endpoint or workaround. Note: since mid-July 2026 Instagram's play count is Instagram-only. It no longer includes Facebook crosspost views (Meta-side change; the app UI changed identically). For combined reach, also fetch the Facebook crosspost via `/v1/facebook/post`. (with `include=exact_counts` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.ext.activity_id` | string\|null | On a LinkedIn article, the id of the post that shares it. post/comments takes this id. (seen in a sample response) |
| `post.ext.ad.advertiser_account_type` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.advertiser_follower_count_text` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.advertiser_id` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.advertiser_profile_id` | unknown\|null |  |
| `post.ext.ad.advertiser_profile_url` | unknown\|null |  |
| `post.ext.ad.advertiser_registered_location` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.advertiser_sponsor` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.audit_status` | unknown | The library's review status code for the ad. |
| `post.ext.ad.brand_name` | unknown | The advertiser's name. |
| `post.ext.ad.call_to_action` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.caption` | unknown | The ad's caption. |
| `post.ext.ad.categories` | unknown | The ad's content categories. |
| `post.ext.ad.country_code` | unknown | The country or countries the ad ran in. |
| `post.ext.ad.cta_text` | unknown | The call-to-action button text. |
| `post.ext.ad.cta_texts` | unknown\|null |  |
| `post.ext.ad.cta_type` | unknown | The call-to-action type, such as `LEARN_MORE`. |
| `post.ext.ad.currency` | unknown | ISO 4217 currency code of the spend figures. |
| `post.ext.ad.display_format` | unknown | The ad's display format, such as `DCO`. |
| `post.ext.ad.end_date` | unknown\|null |  |
| `post.ext.ad.end_date_iso` | unknown | When the ad stopped, ISO 8601. |
| `post.ext.ad.estimated_audience` | unknown\|null | Audience size band, such as `10K-100K`. (only when the fallback source serves) |
| `post.ext.ad.eu_reach_breakdown` | unknown\|null |  |
| `post.ext.ad.eu_total_reach` | unknown\|null |  |
| `post.ext.ad.format` | unknown\|null |  |
| `post.ext.ad.format_label` | unknown\|null |  |
| `post.ext.ad.headline` | unknown\|null |  |
| `post.ext.ad.image_urls` | unknown | Links to the ad's images. |
| `post.ext.ad.is_active` | unknown\|null | True when the ad is still running. (on some endpoints only when the fallback source serves) |
| `post.ext.ad.landing_page` | unknown | Landing page the ad opens. |
| `post.ext.ad.last_shown_at` | unknown\|null |  |
| `post.ext.ad.last_shown_date` | unknown | When the ad was last shown, Unix milliseconds. |
| `post.ext.ad.link_url` | unknown | Where the ad sends people. |
| `post.ext.ad.media_type` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.objectives` | unknown | The campaign objectives the advertiser chose. |
| `post.ext.ad.page_categories` | unknown | The advertiser page's categories. |
| `post.ext.ad.page_id` | unknown | Id of the advertiser's page. |
| `post.ext.ad.page_like_count` | unknown | Followers or likes of the advertiser's page. |
| `post.ext.ad.page_profile_uri` | unknown | Link to the advertiser's page. |
| `post.ext.ad.payer` | unknown\|null |  |
| `post.ext.ad.profile_web_link` | unknown | Link to the advertiser's profile. |
| `post.ext.ad.promoted_by` | unknown\|null |  |
| `post.ext.ad.publisher_platforms` | unknown | Where the ad ran. |
| `post.ext.ad.reach_estimate` | unknown | Reach estimate the library reports. The shape differs by library and is null when it hides reach. |
| `post.ext.ad.source` | unknown | The library the ad came from. |
| `post.ext.ad.spend` | unknown | Spend range the library reports. The shape differs by library and is null when it hides spend. |
| `post.ext.ad.target_ages` | unknown\|null |  |
| `post.ext.ad.target_gender` | unknown\|null |  |
| `post.ext.ad.target_locations` | unknown\|null |  |
| `post.ext.ad.targeting` | unknown\|null | (on some endpoints only when the fallback source serves) |
| `post.ext.ad.targets_eu` | unknown\|null |  |
| `post.ext.ad.title` | unknown | The ad's headline. |
| `post.ext.ad.video_hd_url` | unknown\|null | Link to the high-definition video. |
| `post.ext.ad.video_renditions` | unknown\|null |  |
| `post.ext.ad.video_sd_url` | unknown\|null | Link to the standard-definition video. |
| `post.ext.ad.video_url` | unknown\|null |  |
| `post.ext.all_media_urls` | array\|null | Every media URL on the post in source order. Present only when there is more than one. X only. (seen in a sample response) |
| `post.ext.amazon_shop_curations` | array\|null | Shoppable post sets the creator curated. |
| `post.ext.amazon_shop_lists` | array\|null | The creator's curated idea lists. |
| `post.ext.amazon_shop_socials` | array\|null | The creator's profile URLs outside Amazon. Amazon Influencer Shop only. |
| `post.ext.amazon_shop_trending_picks` | array\|null | Products the creator features as trending picks. |
| `post.ext.apple_music.artist_url` | unknown | Link to the artist's page. |
| `post.ext.apple_music.explicit` | unknown | True when the track is marked explicit. |
| `post.ext.apple_music.kind` | unknown | What the item is, such as `album` or `songs`. |
| `post.ext.apple_music.release_info` | unknown | Release date, track count, duration and copyright as one text block. |
| `post.ext.apple_music.track_count` | unknown | How many tracks an album has. |
| `post.ext.apple_music.track_number` | unknown | Position of the track on its album. |
| `post.ext.article.source` | string | The article's publisher or domain. (seen in a sample response) |
| `post.ext.article.title` | string | Title of the shared article. (seen in a sample response) |
| `post.ext.article.url` | string | Link to the article. (seen in a sample response) |
| `post.ext.author_followers` | number\|null | The creator's follower count as embedded in the search payload itself, when the search source happens to carry one. On `instagram/search/reels` it is null on a plain call, because Instagram stopped sending follower counts in its search payload in August 2026; send `include=creator` (or `country`) and it is filled from the creator's profile, 2 credits per creator looked up. It stays null when that lookup does not resolve. |
| `post.ext.author_following` | number\|null | Accounts the author follows, as of when the list source captured the row. Not live. |
| `post.ext.author_headline` | string\|null | The author's profile headline. LinkedIn only. (seen in a sample response) |
| `post.ext.author_id` | string\|null | The creator's platform-native numeric user id. On TikTok search and list items, pass to `/v1/tiktok/profile?user_id=` for the creator's current follower count (survives username changes). On Instagram `/v1/instagram/search/reels`, `/v1/instagram/search/hashtag` and `/v1/instagram/location/posts` items it is present on every row, accepted by `/v1/instagram/profile/country?user_id=` and `/v1/instagram/basic-profile?userId=`. On Facebook it appears when the upstream exposed a numeric actor id and no real handle. (on some endpoints only when the fallback source serves) |
| `post.ext.author_location` | string\|null | The free text the author wrote in their profile's location field, exactly as written (for example `Johannesburg, South Africa`). It is not a country code and is not checked; discover reads a country from it into `geo.country` (`source: author_location`). Present on X tweet and reply rows; null or absent when the author left it blank. |
| `post.ext.author_posts_count` | number\|null | Posts the author has made, as of when the list source captured the row. Not live. |
| `post.ext.author_type` | string\|null | Whether the author is a user or a company. LinkedIn only. (seen in a sample response) |
| `post.ext.author_url` | string\|null | The posting account's profile URL, so a matching post can be followed to its account. Present on `/v1/facebook/search/posts` rows: the vanity or `/people/<name>/<id>/` URL when Facebook sends one, otherwise `https://www.facebook.com/profile.php?id=<numeric id>` built from the account id. Pass it as `url` to `/v1/facebook/profile` (or to `/v1/prism/profiles` with `platform: facebook`). Null when the row names neither an account URL nor a numeric account id. Absent on other endpoints. (seen in a sample response) |
| `post.ext.author_urn` | string\|null | Opaque LinkedIn urn of the author. Joins to the /user endpoints without a lookup step. (seen in a sample response) |
| `post.ext.caption` | string\|null | Whether the video has captions, as the string true or false. YouTube only. (seen in a sample response) |
| `post.ext.categoryId` | string\|null | YouTube's category id, for example 10. (seen in a sample response) |
| `post.ext.categoryTitle` | string\|null | Name of the YouTube category. (only when the fallback source serves) |
| `post.ext.channel_id` | string\|null | The 24 character YouTube channel id (starts with UC). Used because these rows carry no handle. |
| `post.ext.coauthors` | array\|null | Instagram collaborative posts (the native "Collab" feature). The full list of co-author accounts on the post, as `{ id, username, full_name, is_verified, profile_pic_url }`. A collab post has ONE producer and appears in every co-author's grid, so `post.author` is whichever account created it, which is not necessarily the profile you queried. The complete set of accounts on a post is `post.author.username` plus every `username` in this array. An empty array means Instagram reports the post as NOT a collab; the field is absent on surfaces that carry no co-author signal, including `/v1/instagram/post` (its web source ships the field permanently empty, so use `/v1/instagram/post/stats` for a single post). (seen in a sample response) |
| `post.ext.commerce.attributes` | unknown | Listing attributes. |
| `post.ext.commerce.availability_text` | unknown\|null | Availability, as text. |
| `post.ext.commerce.category_id` | unknown | The listing category's id. |
| `post.ext.commerce.currency` | unknown | ISO 4217 currency code of the price. |
| `post.ext.commerce.delivery_types` | unknown | How the item can be handed over. |
| `post.ext.commerce.description` | unknown | The listing's description. |
| `post.ext.commerce.is_buy_now_enabled` | unknown | True when the buyer can buy without messaging first. |
| `post.ext.commerce.is_hidden` | unknown | True when the listing is hidden. |
| `post.ext.commerce.is_live` | unknown | True when the listing is live. |
| `post.ext.commerce.is_pending` | unknown | True when a sale is pending. |
| `post.ext.commerce.is_shipping_offered` | unknown | True when the seller ships the item. |
| `post.ext.commerce.is_sold` | unknown | True when the item has sold. |
| `post.ext.commerce.latitude` | unknown | Latitude of the item in degrees. |
| `post.ext.commerce.listing_date_text` | unknown | When the item was listed, as the platform words it. |
| `post.ext.commerce.location_text` | unknown | Where the item is, as text. |
| `post.ext.commerce.longitude` | unknown | Longitude of the item in degrees. |
| `post.ext.commerce.messaging_enabled` | unknown | True when buyers can message the seller. |
| `post.ext.commerce.mileage` | unknown\|null | Mileage, for vehicles. |
| `post.ext.commerce.price` | unknown | The item's price: a number on a marketplace listing, an object on a shop product. |
| `post.ext.commerce.price_formatted` | unknown | Price formatted for display. |
| `post.ext.commerce.seller_id` | unknown\|null | The seller's id on the platform. |
| `post.ext.commerce.seller_name` | unknown\|null | The seller's name. |
| `post.ext.commerce.strikethrough_price_formatted` | unknown | The crossed-out previous price, formatted for display. |
| `post.ext.content_language` | string\|null | The language the platform itself tags the post with, when it sends one: Reddit's own language tag on Reddit endpoints, and TikTok's caption-language tag (for example `de`) on `/v1/tiktok/trending?feed=local`. Null when the platform could not tell (Reddit `und`, TikTok `un`, common on short or emoji-only captions); absent where the source sends no tag. Never inferred from the text by us: that is `post.computed.language`. |
| `post.ext.content_type` | string\|null | YouTube format: video, short, live, channel or playlist. (seen in a sample response) |
| `post.ext.conversation_id` | string\|null | Id of the post that opened the thread. Equals the row's own id on a top level post. X only. |
| `post.ext.counts_approximate` | boolean\|null | (only when the fallback source serves) |
| `post.ext.default_language` | string\|null | Default language of the video's metadata as a BCP 47 code. (seen in a sample response) |
| `post.ext.defaultAudioLanguage` | string\|null | Language of the video's audio track as a BCP 47 code. (seen in a sample response) |
| `post.ext.description` | string\|null | Description text from the source record. (on some endpoints only when the fallback source serves) |
| `post.ext.download_count` | number\|null | How many times the video has been saved to a device. TikTok only, and distinct from `engagement.saves`: a save keeps the video in a private collection on the platform, a download takes a copy off it, and TikTok counts the two separately. Present on TikTok post, search and post-list responses; absent everywhere else. (on some endpoints only when the fallback source serves) |
| `post.ext.duration` | string\|null | Video length as an ISO 8601 duration, for example PT3M33S. (seen in a sample response) |
| `post.ext.event.address` | unknown\|null | Street address. |
| `post.ext.event.attendance_count` | unknown | Total attendance figure. |
| `post.ext.event.category` | unknown | The event's category. |
| `post.ext.event.city` | unknown\|null | City. |
| `post.ext.event.description` | unknown | The event's description. |
| `post.ext.event.duration_text` | unknown | How long the event lasts, as text. |
| `post.ext.event.end_timestamp` | unknown\|null | When the event ends, in Unix seconds. |
| `post.ext.event.going_count` | unknown | People who said they are going. |
| `post.ext.event.host_context_text` | unknown | The host line, such as `Event by ...`. |
| `post.ext.event.hosts` | unknown | The people or pages hosting the event. |
| `post.ext.event.interested_count` | unknown | People who marked themselves interested. |
| `post.ext.event.is_canceled` | unknown | True when the event is cancelled. |
| `post.ext.event.is_online` | unknown | True when the event is online. |
| `post.ext.event.is_past` | unknown | True when the event has already happened. |
| `post.ext.event.latitude` | unknown\|null | Latitude of the venue in degrees. |
| `post.ext.event.location_name` | unknown | Name of the venue, or `Online event`. |
| `post.ext.event.longitude` | unknown\|null | Longitude of the venue in degrees. |
| `post.ext.event.privacy` | unknown | Who can see the event, such as `public`. |
| `post.ext.event.start_timestamp` | unknown | When the event starts, in Unix seconds. |
| `post.ext.event.ticket_url` | unknown\|null | Link to buy tickets. |
| `post.ext.event.time_text` | unknown | The event time as the platform words it, with time zone. |
| `post.ext.feedback_id` | string\|null | Join key that /v1/facebook/post/comments takes to read the post's comments. (seen in a sample response) |
| `post.ext.flair` | string\|null | The post's link flair. Reddit only. |
| `post.ext.group.members` | unknown\|null | The group's member count. (with `include=group`) |
| `post.ext.group.name` | unknown\|null | The group's name. (with `include=group`) |
| `post.ext.hashtags` | array\|null | Hashtags parsed from the caption, lower cased without the #, each listed once in order. |
| `post.ext.hasPaidProductPlacement` | boolean\|null | Whether the video discloses a paid product placement. YouTube only. (only when the fallback source serves) |
| `post.ext.ig_play_count` | number\|null | Instagram-only play count (`ig_play_count`). Since mid-July 2026 Instagram's headline play count (`engagement.views`) no longer includes Facebook crosspost views and equals this value; it is surfaced explicitly so you can tell the Instagram-only figure apart and detect any future re-divergence. For combined Instagram + Facebook reach, also fetch the Facebook crosspost via `/v1/facebook/post`. Present on `/v1/instagram/post/stats` and, since the August 2026 views fix, on `/v1/instagram/post` for video posts. (on some endpoints only when the fallback source serves) |
| `post.ext.in_reply_to_id` | string\|null | Id of the post this row replies to. Null when it answers nothing. |
| `post.ext.in_reply_to_username` | string\|null | Handle of the account this row replies to. |
| `post.ext.ip_location` | string\|null | Province the note was published from. Xiaohongshu only, not a self declared location. |
| `post.ext.license` | string\|null | Licence the video is published under, for example youtube or creativeCommon. (seen in a sample response) |
| `post.ext.madeForKids` | boolean\|null | Whether the video is marked as made for kids. YouTube only. (seen in a sample response) |
| `post.ext.media_type` | string\|null | Media kind: image, video or carousel. (seen in a sample response) |
| `post.ext.mentions` | array\|null | Handles mentioned in the caption, lower cased with the @, each listed once in order. (seen in a sample response) |
| `post.ext.music_artist` | string\|null | TikTok only. The artist TikTok shows for the video's own sound. On an original sound this is the uploader's display name, not the song's artist; use `matched_song_artist` for that. (seen in a sample response) |
| `post.ext.music_id` | string\|null | TikTok music/clip id (exact string): pass to `/v1/tiktok/song/videos?clipId=` to find videos using the same sound |
| `post.ext.music_is_original` | boolean\|null | TikTok only. `true` when the video's sound is an original sound a creator uploaded, `false` when it is a catalogue track. Absent when the source does not say. (seen in a sample response) |
| `post.ext.music_title` | string\|null | TikTok only. The title of the video's own sound (`music_id`). An uploaded sound is titled like `original sound - <handle>`; the song it plays, when TikTok recognised one, is `matched_song_title`. (seen in a sample response) |
| `post.ext.music.artist` | string\|null | The artist or account that made the sound. (seen in a sample response) |
| `post.ext.music.id` | string | The id of the sound or audio track. (seen in a sample response) |
| `post.ext.music.is_original` | boolean | True when the sound is the creator's own original audio. (seen in a sample response) |
| `post.ext.music.track_title` | string\|null | Title of the sound or track. (seen in a sample response) |
| `post.ext.playback_availability` | object\|null | Where and to whom the video plays, and its live state. Present with include=availability. (with `include=availability`) |
| `post.ext.post_type` | string\|null | The activity type of a LinkedIn post, such as ugc or activity. (seen in a sample response) |
| `post.ext.posts_count` | number | `/v1/instagram/hashtag` only: the exact number of public posts Instagram counts under the hashtag. Live: it moves between calls minutes apart. |
| `post.ext.published_at_epoch` | number\|null | Raw Unix epoch for `published_at` (seconds, or milliseconds when the upstream sent millis). Present only when the upstream sent a numeric epoch that was normalised to the ISO 8601 `published_at` string. Kept for one deprecation cycle for integrations pinned to the numeric form. (seen in a sample response) |
| `post.ext.published_at_precision` | string\|null | How exactly published_at is known: hour or day on LinkedIn feeds, where the source only gives a relative age. Absent means the time is exact. |
| `post.ext.published_label` | string\|null | The relative label the source showed instead of a date, for example 'Streamed 3 weeks ago'. (seen in a sample response) |
| `post.ext.published_precision` | string\|null | How precise published_at is when the source gave only a relative label: minute, hour, day, week, month or year. (seen in a sample response) |
| `post.ext.quote_count` | number\|null | How many times the post was quoted. X and Threads. |
| `post.ext.quoted_post` | object | Threads quote posts: the post this one quotes, as `{ id, url, author: { id, username }, text, media_urls, thumbnail_url }`. A quote post usually carries no caption or media of its own, and the text and video you see on the post's page belong to this attachment, by a different author. It is returned here rather than merged into `post.content`, so `content.*` always stays the outer post's own content and one account's media is never attributed to another. Absent on posts that are not quote posts. On LinkedIn feeds, `/v1/linkedin/search/posts` and `/v1/linkedin/search/hashtag`, the post a quote post quotes, in the same shape with the author's `display_name`, `engagement` and `published_at`; there the leaf is present on every post and null when the post quotes none. |
| `post.ext.ran_as_ad` | boolean\|null | (only when the fallback source serves) |
| `post.ext.reaction_counts` | array\|null | Reaction counts by type. |
| `post.ext.region` | string\|null | TikTok only: the country TikTok registers the video to, as an ISO 3166-1 alpha-2 code (normally the creator's account country when they posted). It is not the viewer's country, not the `region` you requested, and not a language. On `/v1/tiktok/trending`, `/v1/tiktok/search`, `/v1/tiktok/search/top`, `/v1/tiktok/profile/videos`, `/v1/tiktok/search/hashtag` and `/v1/tiktok/song/videos` it is how you tell which rows are from a given country: filter on it when you need only that country. A row whose source omits the country stays null. The `region` request parameter still only sets the proxy. (only when the fallback source serves) |
| `post.ext.remix_count` | number\|null | How many reels were made from this reel. Instagram only. (seen in a sample response) |
| `post.ext.repost_count` | number\|null | Reposts of the post. Instagram's two arrow repost count when include=saves is used. (on some endpoints only when the fallback source serves) |
| `post.ext.reshare_count` | number\|null | The boosted reshare figure Threads shows in the app. |
| `post.ext.retweeted_post` | object | The original post behind a retweet. It is a different post by a different author. |
| `post.ext.selftext` | string\|null | The Reddit post body without the title. Null on link posts. |
| `post.ext.sponsored_disclosed` | boolean\|null | The platform's own disclosure that the post is paid or promotional: on Instagram the paid-partnership label (`is_paid_partnership`) or a tagged brand partner, on TikTok the label TikTok shows viewers ("Paid partnership", "Commission paid", "Promotional content"), on LinkedIn the brand partnership label LinkedIn shows on the post. `false` when the post carries the flag unset, null when it carries none. Present on `/v1/instagram/post/stats`, `/v1/instagram/profile/posts`, `/v1/instagram/profile/reels`, `/v1/instagram/search/reels`, `/v1/tiktok/profile/videos` and `/v1/tiktok/search`, and on every post of the LinkedIn feeds (`/v1/linkedin/profile/posts`, `/v1/linkedin/company/posts`, `/v1/linkedin/profile/posts/archive`, `/v1/linkedin/profile/reactions`, `/v1/linkedin/post/reposts` and `/v1/linkedin/group/posts`), where it is null unless the source that answered reports the label; absent on every other endpoint. (only when the fallback source serves) |
| `post.ext.subreddit` | string\|null | Reddit subreddit name (search/list items): pass to `/v1/reddit/subreddit/details?subreddit=` |
| `post.ext.tagged_products` | array\|null | The TikTok Shop products tagged on the video. Empty when it tags none. (only when the fallback source serves) |
| `post.ext.tags` | array\|null | Video tags set by the creator. YouTube only. (only when the fallback source serves) |
| `post.ext.text_truncated` | boolean\|null | True when content.text is a shortened summary and not the full note. Xiaohongshu only. |
| `post.ext.title` | string\|null | The post title on its own. Reddit only. |
| `post.ext.topic_tag` | string\|null | Name of the topic a Threads post is filed under. Not a slug, so join on topic_tag_id. |
| `post.ext.topic_tag_id` | string\|null | Id of the Threads topic. Use it to join, not the topic name. |
| `post.ext.topicCategories` | array\|null | Wikipedia URLs for the video's topics. YouTube only. (seen in a sample response) |
| `post.ext.type` | string\|null | Item type: pull_request or issue on GitHub lists; on LinkedIn feeds and post search, the kind of post in lower case, such as text, image, video, article, newsletter, document, poll, job, event or celebration. A poll can read text on a feed page whose answering source does not send the poll. (seen in a sample response) |
| `post.ext.upvote_ratio` | number\|null | Reddit only: the share of a post's votes that are upvotes, as a fraction from 0 to 1 and usually close to 1 (six live rows measured 1, 1, 1, 0.86, 0.75, 1). Fractional despite the integer type this schema emits for every numeric leaf, the same caveat as `author.ext.average_rating`. Populated on `/v1/reddit/search` rows whose source carries it, and null everywhere else on Reddit including `/v1/reddit/post` and `/v1/reddit/subreddit`. |
| `post.ext.use_count` | number\|null | TikTok sounds only: how many videos use this sound. It is the same number as `post.engagement.views` on this endpoint, labelled correctly, and it is not a play count. (seen in a sample response) |
| `post.ext.use_count_unit` | string\|null | What `use_count` counts. Always `videos`. (seen in a sample response) |
| `post.ext.video_count` | number\|null | Number of videos in the playlist. It is not a view count. |
| `post.flags.deleted` | boolean | Whether the post is tombstoned (always present) |
| `post.flags.nsfw` | boolean\|null | NSFW flag (null when platform does not surface) (seen in a sample response) |
| `post.flags.pinned` | boolean\|null | Pinned-to-profile flag (null when platform does not surface) |
| `post.flags.spoiler` | boolean\|null | Spoiler flag (null when platform does not surface) (seen in a sample response) |
| `post.id` | string | Platform-specific post ID (always a string; numeric upstream IDs are stringified) |
| `post.published_at` | string\|number\|null | Post creation timestamp as an ISO 8601 UTC string. When the upstream sent a Unix epoch it is converted here and the raw epoch is preserved under `post.ext.published_at_epoch` for one deprecation cycle. (on some endpoints only when the fallback source serves) |
| `post.url` | string\|null | Direct URL to the post on the source platform (on some endpoints only when the fallback source serves) |
