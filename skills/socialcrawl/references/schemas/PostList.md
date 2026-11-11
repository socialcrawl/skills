# PostList fields

Every field the 113 field-mapped endpoints returning `PostList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `computed.content_category` | string\|null | Keyword-classified content category (e.g. tech, food, gaming). Null when undetectable. |
| `computed.engagement_rate` | number\|null | Computed engagement rate (0..1). Null when the upstream lacks enough signal. |
| `computed.estimated_reach` | number\|null | Estimated reach based on views or follower count. Null when uncomputable. |
| `computed.labels_evidence` | object\|null | When 1, every labelled row also carries computed.labels_evidence.<preset> = { quote, sentence_index }: the sentence in the row that most clearly shows the label, copied verbatim. (with `label_evidence=1`) |
| `computed.labels.ai_style` | object\|null | ai_style: writing patterns common in AI-generated text, judged on the text alone. (with `label=ai_style`) |
| `computed.labels.ai_written` | object\|null | ai_written: how likely the post was written by an AI model, from SocialCrawl's own text classifier, reading the opening of the post (about 1,000 characters): p (0 to 1, calibrated), level (likely (p 0.95 or higher), possible (p 0.71 or higher) or unlikely) and model (the model name; a new name means a new scale). (with `label=ai_written`) |
| `computed.labels.injection` | object\|null | injection flags text that addresses an AI system and tries to direct it (flagged, p); it never drops or rewrites a row. (with `label=injection`) |
| `computed.labels.intent` | object\|null | intent: what the author is mainly doing (label: asking_for_recommendation, comparing_options, switching_away, complaining, promoting, news_or_discussion, other, or null when unsure, with confidence), whether they read as a potential buyer rather than a seller (buyer, seller), how pressing the need is (urgency, 0 to 3), and, when you pass offer=, whether your offer would plausibly help them (fits_offer). |
| `computed.labels.mention` | object\|null | mention (needs brand=): is the post about that brand rather than something that shares its name (about_brand, 0 to 1), how it feels about the brand on five levels (sentiment_level 0 to 4 and sentiment_score 0 to 1, null when the post is not about the brand), is it sarcastic, which aspect it talks about (taste_or_quality, price_or_value, availability_or_delivery, health_or_safety, advertising_or_campaign, customer_service, none), and did the author buy or use it (first_hand). (with `label=mention`) |
| `computed.labels.niche` | object\|null | niche: which of the 33 niches of the published taxonomy sc-niche-v1 the caption belongs to, or personal_no_niche, or other (label, confidence, taxonomy), with label null when the caption is too thin to tell or the pick is unsure. |
| `computed.labels.quality` | object\|null | quality: how much checkable detail the caption carries (fact_density 0 to 3), whether it mainly asks for likes, replies, shares, follows or tags (engagement_bait, 0 to 1), whether it is written to provoke anger as a way to get engagement (rage_bait, 0 to 1; about the writing, never the side taken), whether it only repeats someone else's news or view (secondhand, 0 to 1), and what the post is mainly doing (post_aim: inform, opinion, sell, entertain, provoke, other). (with `label=quality`) |
| `computed.labels.sponsored` | object\|null | sponsored: is the post a paid or gifted promotion (p, 0 to 1), did it carry a disclosure marker such as #ad or 광고 (disclosed), is it likely paid with no marker (undisclosed), and which of the accounts it mentions does it promote (brand, or null). |
| `computed.language` | string\|null | ISO 639-1 language code detected from the post text. Null when undetectable. |
| `computed.relevance` | object\|null | Without this param every row already carries computed.relevance against your query, free ({ p, sense, depth, spam }: is this row about what your query means, or a different thing that shares its words?), and nothing is dropped or reordered. |
| `computed.save_rate` | number\|null | Saves divided by views, rounded to six places. Present only when the post has both a save count and a view count above zero. |
| `computed.vs_creator` | object\|null |  |
| `post.author.avatar_url` | string\|null | URL to author profile picture (with `include=ad`, `include=channel`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.author.display_name` | string\|null | Author display name (with `include=engagement`, `include=creator`, `include=channel`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.author.url` | unknown\|null |  |
| `post.author.username` | string\|null | Author username (with `include=channel` on some endpoints) |
| `post.author.verified` | boolean\|null | Whether the account carries TikTok's verification badge. The source sends a badge label rather than a flag, and the API writes false when no label is present, so false can also mean the source sent no verification signal. (with `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.content.duration_seconds` | number\|null | Video/clip duration in seconds (null for non-video posts) (with `include=engagement`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.content.media_urls` | string\|array\|null | URL(s) of the primary media. Single string for video/photo posts; array of strings for carousels. (on some endpoints only when the fallback source serves) |
| `post.content.text` | string\|null | Post caption, description, or text content (with `include=engagement` on some endpoints) |
| `post.content.thumbnail_url` | string\|null | URL to thumbnail image (with `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.engagement.comments` | number\|null | Comment count. Note: on `GET /v1/instagram/post` this is Instagram's `edge_media_to_parent_comment.count` (top-level comments); the IG list endpoints report the mobile `comment_count` total (includes replies). Both land on this same field. (with `include=engagement`, `include=exact_counts`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.engagement.likes` | number\|null | Like / reaction count (with `include=engagement`, `include=exact_counts`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.engagement.saves` | number\|null | Save / bookmark count. `null` on Instagram: the save count is platform-private and Instagram exposes no numeric save metric on any surface (never fabricated). (with `include=engagement`, `include=exact_counts` on some endpoints) |
| `post.engagement.shares` | number\|null | Share / repost / retweet count. On Instagram this is `reshare_count` (the paper-plane Share / Send count) and it exists only on Instagram's mobile surface, so it is returned by `/v1/instagram/post/stats`, `/v1/instagram/profile/reels/full`, and `/v1/instagram/profile/posts/full`. The web-sourced Instagram list and search endpoints return `null` (never fabricated). (with `include=engagement`, `include=exact_counts`, `include=details` on some endpoints) |
| `post.engagement.views` | number\|null | View count (if available). For Instagram video/reels this is the play count: the headline 'Views' the IG app shows. Instagram removed per-post play counts from its public web pages in August 2026, so `GET /v1/instagram/post` now fills the count automatically from a second source within the same call: videos and reels keep a numeric `views` with no extra endpoint or workaround. Note: since mid-July 2026 Instagram's play count is Instagram-only. It no longer includes Facebook crosspost views (Meta-side change; the app UI changed identically). For combined reach, also fetch the Facebook crosspost via `/v1/facebook/post`. (with `include=engagement`, `include=exact_counts`, `include=details` on some endpoints) |
| `post.ext.ad.ad_format` | unknown\|null | The ad's format. |
| `post.ext.ad.audit_status` | unknown | The library's review status code for the ad. |
| `post.ext.ad.brand_name` | unknown\|null | The advertiser's name. (with `include=ad`) |
| `post.ext.ad.byline` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.caption` | unknown | The ad's caption. |
| `post.ext.ad.categories` | unknown | The ad's content categories. |
| `post.ext.ad.cost_score` | unknown | Relative cost score. |
| `post.ext.ad.country_code` | unknown\|null | The country or countries the ad ran in. (with `include=ad` on some endpoints) |
| `post.ext.ad.cta_text` | unknown | The call-to-action button text. |
| `post.ext.ad.cta_type` | unknown | The call-to-action type, such as `LEARN_MORE`. |
| `post.ext.ad.ctr` | unknown | Click-through rate band, 0 to 1. |
| `post.ext.ad.currency` | unknown | ISO 4217 currency code of the spend figures. |
| `post.ext.ad.display_format` | unknown | The ad's display format, such as `DCO`. |
| `post.ext.ad.end_date_iso` | unknown | When the ad stopped, ISO 8601. |
| `post.ext.ad.estimated_audience` | unknown | Audience size band, such as `10K-100K`. |
| `post.ext.ad.eu_reach_breakdown` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.eu_total_reach` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.image_urls` | unknown | Links to the ad's images. |
| `post.ext.ad.impressions_text` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.industry` | unknown | The industry the ad belongs to. |
| `post.ext.ad.is_active` | unknown | True when the ad is still running. |
| `post.ext.ad.is_partnership_ad` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.is_spark_ad` | unknown\|null | True when the ad boosts an organic post. |
| `post.ext.ad.landing_page` | unknown\|null | Landing page the ad opens. (with `include=ad`) |
| `post.ext.ad.landing_page_url` | unknown\|null | Landing page the ad opens. |
| `post.ext.ad.language` | unknown\|null | The ad's language. |
| `post.ext.ad.last_shown_date` | unknown | When the ad was last shown, Unix milliseconds. |
| `post.ext.ad.like_tier` | unknown\|null | Like-count tier. |
| `post.ext.ad.link_url` | unknown | Where the ad sends people. |
| `post.ext.ad.objective` | unknown | The campaign objective's code. |
| `post.ext.ad.objectives` | unknown\|null | The campaign objectives the advertiser chose. (with `include=ad`) |
| `post.ext.ad.page_categories` | unknown | The advertiser page's categories. |
| `post.ext.ad.page_id` | unknown | Id of the advertiser's page. |
| `post.ext.ad.page_like_count` | unknown | Followers or likes of the advertiser's page. |
| `post.ext.ad.page_profile_uri` | unknown | Link to the advertiser's page. |
| `post.ext.ad.partnership` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.period_days` | unknown | Length of the ranking window in days. |
| `post.ext.ad.profile_web_link` | unknown\|null | Link to the advertiser's profile. (with `include=ad`) |
| `post.ext.ad.publisher_platforms` | unknown | Where the ad ran. |
| `post.ext.ad.rank` | unknown | The ad's rank on the board it was read from. |
| `post.ext.ad.reach_estimate` | unknown | Reach estimate the library reports. The shape differs by library and is null when it hides reach. |
| `post.ext.ad.retention` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.retention_2s` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.retention_6s` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.source` | unknown\|null | The library the ad came from. (with `include=ad`) |
| `post.ext.ad.spend` | unknown | Spend range the library reports. The shape differs by library and is null when it hides spend. |
| `post.ext.ad.spent` | unknown | Spend as the library words it. Empty when not disclosed. |
| `post.ext.ad.sponsor_instagram_username` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.target_ages` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.target_gender` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.target_locations` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.targeted_or_reached_countries` | unknown | Countries the ad targeted or reached. |
| `post.ext.ad.targets_eu` | unknown\|null | (with `include=audience`) |
| `post.ext.ad.title` | unknown | The ad's headline. |
| `post.ext.ad.total_active_time_seconds` | unknown\|null | (only when the fallback source serves) |
| `post.ext.ad.type` | unknown | The library's ad type code. |
| `post.ext.ad.video_hd_url` | unknown\|null | Link to the high-definition video. |
| `post.ext.ad.video_id` | unknown | The video's id. |
| `post.ext.ad.video_sd_url` | unknown\|null | Link to the standard-definition video. |
| `post.ext.ad.video_url_360p` | unknown | Link to the 360p video. |
| `post.ext.ad.video_url_540p` | unknown | Link to the 540p video. |
| `post.ext.all_media_urls` | array\|null | Every media URL on the post in source order. Present only when there is more than one. X only. (seen in a sample response) |
| `post.ext.alt_text` | string\|null | Pinterest's machine caption of the image. Never the creator's own text. |
| `post.ext.apple_music.artist_id` | unknown | The artist's id. |
| `post.ext.apple_music.artist_url` | unknown | Link to the artist's page. |
| `post.ext.apple_music.content_advisory` | unknown\|null | Content advisory label, such as `explicit`. |
| `post.ext.apple_music.genres` | unknown | Genres the item belongs to. |
| `post.ext.apple_music.kind` | unknown | What the item is, such as `album` or `songs`. |
| `post.ext.apple_music.release_date` | unknown | Release date, as YYYY-MM-DD. |
| `post.ext.article` | object\|null | The article a link post shares. |
| `post.ext.article.source` | string | The article's publisher or domain. (seen in a sample response) |
| `post.ext.article.title` | string | Title of the shared article. (seen in a sample response) |
| `post.ext.article.url` | string | Link to the article. (seen in a sample response) |
| `post.ext.aspect_ratio` | number\|null | A video's width divided by its height, so 0.5625 is 9:16. LinkedIn feeds and post search. |
| `post.ext.audio_cluster_id` | string\|null | Instagram's audio cluster for a reel, as an exact digit string: the id Instagram uses to group different uploads of the same sound. Present on `/v1/instagram/audio/reels` rows and on `/v1/instagram/profile/reels` with `include=stats`; absent on a row when it is not available and on every other surface. (seen in a sample response) |
| `post.ext.author_country` | string\|null | The creator's country. On Instagram it is the country the creator declares on the About this account panel, as a country name (for example `Spain`), and it is not where the post was filmed. It is present on `/v1/instagram/search/reels` when the request sends `include=creator`, `include=country` or `country`, and on `/v1/instagram/search/hashtag` and `/v1/instagram/location/posts` when it sends `include=country`, filled by looking the creator up. On YouTube rows joined with `include=channel` it is the channel's own country as an ISO 3166-1 alpha-2 code (for example `ZA`). Null when the platform publishes no country for the creator or the lookup did not resolve, and nothing is guessed; absent on a plain call. (with `include=channel`, `include=creator`, `include=country`) |
| `post.ext.author_followers` | number\|null | The creator's follower count as embedded in the search payload itself, when the search source happens to carry one. On `instagram/search/reels` it is null on a plain call, because Instagram stopped sending follower counts in its search payload in August 2026; send `include=creator` (or `country`) and it is filled from the creator's profile, 2 credits per creator looked up. It stays null when that lookup does not resolve. (with `include=channel`, `include=creator` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.ext.author_following` | number\|null | Accounts the author follows, as of when the list source captured the row. Not live. (with `include=creator` on some endpoints) |
| `post.ext.author_headline` | string\|null | The author's profile headline. LinkedIn only. |
| `post.ext.author_id` | string\|null | The creator's platform-native numeric user id. On TikTok search and list items, pass to `/v1/tiktok/profile?user_id=` for the creator's current follower count (survives username changes). On Instagram `/v1/instagram/search/reels`, `/v1/instagram/search/hashtag` and `/v1/instagram/location/posts` items it is present on every row, accepted by `/v1/instagram/profile/country?user_id=` and `/v1/instagram/basic-profile?userId=`. On Facebook it appears when the upstream exposed a numeric actor id and no real handle. (with `include=details` on some endpoints) |
| `post.ext.author_is_premium` | boolean\|null | True when LinkedIn marks the author as a Premium member. Null otherwise: LinkedIn sends the mark only when it is true, so null does not mean the author is not Premium. LinkedIn post search. |
| `post.ext.author_location` | string\|null | The free text the author wrote in their profile's location field, exactly as written (for example `Johannesburg, South Africa`). It is not a country code and is not checked; discover reads a country from it into `geo.country` (`source: author_location`). Present on X tweet and reply rows; null or absent when the author left it blank. |
| `post.ext.author_posts_count` | number\|null | Posts the author has made, as of when the list source captured the row. Not live. (with `include=creator` on some endpoints) |
| `post.ext.author_public_email` | string\|null | The public contact email on the creator's profile. Present only on `/v1/instagram/search/reels` when the request sends `include=creator`, filled by looking the creator up. Null when the creator lists no public email or the lookup did not resolve; absent on a plain call. (with `include=creator`) |
| `post.ext.author_public_phone` | string\|null | The public contact phone number on the creator's profile. Present only on `/v1/instagram/search/reels` when the request sends `include=creator`, filled by looking the creator up. Null when the creator lists no public phone or the lookup did not resolve; absent on a plain call. (with `include=creator`) |
| `post.ext.author_type` | string\|null | Whether the author is a user or a company. LinkedIn only. |
| `post.ext.author_url` | string\|null | The posting account's profile URL, so a matching post can be followed to its account. Present on `/v1/facebook/search/posts` rows: the vanity or `/people/<name>/<id>/` URL when Facebook sends one, otherwise `https://www.facebook.com/profile.php?id=<numeric id>` built from the account id. Pass it as `url` to `/v1/facebook/profile` (or to `/v1/prism/profiles` with `platform: facebook`). Null when the row names neither an account URL nor a numeric account id. Absent on other endpoints. |
| `post.ext.author_urn` | string\|null | Opaque LinkedIn urn of the author. Joins to the /user endpoints without a lookup step. |
| `post.ext.author_website` | string\|null | The link on the button in the author's profile header, such as their newsletter or website. LinkedIn feeds and post search. |
| `post.ext.author_website_label` | string\|null | The text of that button, for example `View my newsletter`. LinkedIn feeds and post search. |
| `post.ext.board_name` | string\|null | Name of the board the pin was saved to. Pinterest only. |
| `post.ext.caption` | string\|null | Whether the video has captions, as the string true or false. YouTube only. (seen in a sample response) |
| `post.ext.carousel_count` | number\|null | Number of slides in an Instagram carousel. Present only when media_type is carousel. (seen in a sample response) |
| `post.ext.categoryId` | string\|null | YouTube's category id, for example 10. (seen in a sample response) |
| `post.ext.categoryTitle` | string\|null | Name of the YouTube category. |
| `post.ext.celebration` | object\|null | The celebration card a post shows. |
| `post.ext.channel_id` | string\|null | The 24 character YouTube channel id (starts with UC). Used because these rows carry no handle. (with `include=channel`, `include=engagement` on some endpoints) |
| `post.ext.coauthors` | array\|null | Instagram collaborative posts (the native "Collab" feature). The full list of co-author accounts on the post, as `{ id, username, full_name, is_verified, profile_pic_url }`. A collab post has ONE producer and appears in every co-author's grid, so `post.author` is whichever account created it, which is not necessarily the profile you queried. The complete set of accounts on a post is `post.author.username` plus every `username` in this array. An empty array means Instagram reports the post as NOT a collab; the field is absent on surfaces that carry no co-author signal, including `/v1/instagram/post` (its web source ships the field permanently empty, so use `/v1/instagram/post/stats` for a single post). (seen in a sample response) |
| `post.ext.comments_disabled` | boolean\|null | True when the author turned comments off on the post. LinkedIn feeds and post search. |
| `post.ext.content_language` | string\|null | The language the platform itself tags the post with, when it sends one: Reddit's own language tag on Reddit endpoints, and TikTok's caption-language tag (for example `de`) on `/v1/tiktok/trending?feed=local`. Null when the platform could not tell (Reddit `und`, TikTok `un`, common on short or emoji-only captions); absent where the source sends no tag. Never inferred from the text by us: that is `post.computed.language`. (on some endpoints only when the fallback source serves) |
| `post.ext.content_type` | string\|null | YouTube format: video, short, live, channel or playlist. (seen in a sample response) |
| `post.ext.conversation_id` | string\|null | Id of the post that opened the thread. Equals the row's own id on a top level post. X only. |
| `post.ext.default_language` | string\|null | Default language of the video's metadata as a BCP 47 code. (seen in a sample response) |
| `post.ext.defaultAudioLanguage` | string\|null | Language of the video's audio track as a BCP 47 code. (seen in a sample response) |
| `post.ext.description` | string\|null | Description text from the source record. |
| `post.ext.document` | object\|null | The document a document post shares. Its PDF is also in `content.media_urls`. |
| `post.ext.download_count` | number\|null | How many times the video has been saved to a device. TikTok only, and distinct from `engagement.saves`: a save keeps the video in a private collection on the platform, a download takes a copy off it, and TikTok counts the two separately. Present on TikTok post, search and post-list responses; absent everywhere else. |
| `post.ext.dsp_ids.amazon` | string\|null | (seen in a sample response) |
| `post.ext.dsp_ids.apple_music` | string\|null | (seen in a sample response) |
| `post.ext.dsp_ids.spotify` | string\|null | (seen in a sample response) |
| `post.ext.duration` | string\|null | Video length as an ISO 8601 duration, for example PT3M33S. (seen in a sample response) |
| `post.ext.event` | object\|null | Event detail for a post that is an event. |
| `post.ext.event.address` | unknown\|null | Street address. (with `include=details`) |
| `post.ext.event.attendance_count` | unknown\|null | Total attendance figure. (with `include=details`) |
| `post.ext.event.category` | unknown\|null | The event's category. (with `include=details`) |
| `post.ext.event.city` | unknown\|null | City. (with `include=details` on some endpoints) |
| `post.ext.event.description` | unknown\|null | The event's description. (with `include=details`) |
| `post.ext.event.duration_text` | unknown\|null | How long the event lasts, as text. (with `include=details`) |
| `post.ext.event.going_count` | unknown\|null | People who said they are going. (with `include=details` on some endpoints) |
| `post.ext.event.host_context_text` | unknown\|null | The host line, such as `Event by ...`. (with `include=details`) |
| `post.ext.event.hosts` | unknown\|null | The people or pages hosting the event. (with `include=details`) |
| `post.ext.event.interested_count` | unknown\|null | People who marked themselves interested. (with `include=details` on some endpoints) |
| `post.ext.event.is_canceled` | unknown\|null | True when the event is cancelled. (with `include=details` on some endpoints) |
| `post.ext.event.is_online` | unknown | True when the event is online. |
| `post.ext.event.is_past` | unknown | True when the event has already happened. |
| `post.ext.event.latitude` | unknown\|null | Latitude of the venue in degrees. (with `include=details`) |
| `post.ext.event.location_name` | unknown | Name of the venue, or `Online event`. |
| `post.ext.event.longitude` | unknown\|null | Longitude of the venue in degrees. (with `include=details`) |
| `post.ext.event.privacy` | unknown\|null | Who can see the event, such as `public`. (with `include=details`) |
| `post.ext.event.start_timestamp` | unknown | When the event starts, in Unix seconds. |
| `post.ext.event.time_text` | unknown | The event time as the platform words it, with time zone. |
| `post.ext.feedback_id` | string\|null | Join key that /v1/facebook/post/comments takes to read the post's comments. (seen in a sample response) |
| `post.ext.flair` | string\|null | The post's link flair. Reddit only. (on some endpoints only when the fallback source serves) |
| `post.ext.hashtags` | array\|null | Hashtags parsed from the caption, lower cased without the #, each listed once in order. |
| `post.ext.hasPaidProductPlacement` | boolean\|null | Whether the video discloses a paid product placement. YouTube only. (seen in a sample response) |
| `post.ext.ig_play_count` | number\|null | Instagram-only play count (`ig_play_count`). Since mid-July 2026 Instagram's headline play count (`engagement.views`) no longer includes Facebook crosspost views and equals this value; it is surfaced explicitly so you can tell the Instagram-only figure apart and detect any future re-divergence. For combined Instagram + Facebook reach, also fetch the Facebook crosspost via `/v1/facebook/post`. Present on `/v1/instagram/post/stats` and, since the August 2026 views fix, on `/v1/instagram/post` for video posts. (with `include=engagement`) |
| `post.ext.in_reply_to_id` | string\|null | Id of the post this row replies to. Null when it answers nothing. |
| `post.ext.in_reply_to_username` | string\|null | Handle of the account this row replies to. |
| `post.ext.ip_location` | string\|null | Province the note was published from. Xiaohongshu only, not a self declared location. |
| `post.ext.is_edited` | boolean\|null | True when LinkedIn shows the post as edited. LinkedIn feeds and post search. |
| `post.ext.is_repost_quote` | boolean\|null | Whether a reshare added commentary (true) or was a plain repost (false). LinkedIn reposts only. |
| `post.ext.job` | object\|null | The job a job post shares. |
| `post.ext.license` | string\|null | Licence the video is published under, for example youtube or creativeCommon. (seen in a sample response) |
| `post.ext.link_domain` | string\|null | Host a Reddit link post points at. Null on text posts and Reddit hosted media. |
| `post.ext.madeForKids` | boolean\|null | Whether the video is marked as made for kids. YouTube only. (seen in a sample response) |
| `post.ext.media_type` | string\|null | Media kind: image, video or carousel. |
| `post.ext.mentioned_accounts` | array\|null | The accounts LinkedIn links in the post's text, in order. Our parse of `@handles` in the caption stays in `mentions`. |
| `post.ext.mentions` | array\|null | Handles mentioned in the caption, lower cased with the @, each listed once in order. (seen in a sample response) |
| `post.ext.music` | object\|null | The sound or music the post uses. (with `include=audio`) |
| `post.ext.music_id` | string\|null | TikTok music/clip id (exact string): pass to `/v1/tiktok/song/videos?clipId=` to find videos using the same sound (with `include=audio` on some endpoints) |
| `post.ext.music.id` | unknown\|null | The id of the sound or audio track. |
| `post.ext.music.track_title` | unknown\|null | Title of the sound or track. |
| `post.ext.newsletter` | object\|null | The newsletter this post is an edition of. |
| `post.ext.numeric_id` | number\|null | GitHub's numeric REST id, beside the GraphQL node id in post.id. |
| `post.ext.on_screen_texts` | array\|null | Text the creator typed onto the video with TikTok's text tool. (seen in a sample response) |
| `post.ext.outbound_links` | array\|null | The web links in the post's text, in order, each once. LinkedIn feeds and post search. |
| `post.ext.outbound_url` | string\|null | The page a Pinterest pin saves. Absent when it saves none. |
| `post.ext.playlist_item_id` | string\|null | Id of the playlist item itself, distinct from the video id in post.id. (seen in a sample response) |
| `post.ext.playlist_owner_channel_id` | string\|null | Channel id of the playlist's owner, not necessarily the video's channel. (seen in a sample response) |
| `post.ext.playlist_owner_title` | string\|null | Name of the playlist's owner. (seen in a sample response) |
| `post.ext.playlistId` | string\|null | Id of the playlist the item belongs to. (seen in a sample response) |
| `post.ext.poll` | object\|null | The poll a poll post asks. |
| `post.ext.position` | number\|null | Position of the item in the playlist, counting from 0. (seen in a sample response) |
| `post.ext.post_type` | string\|null | The activity type of a LinkedIn post, such as ugc or activity. |
| `post.ext.published_at_epoch` | number\|null | Raw Unix epoch for `published_at` (seconds, or milliseconds when the upstream sent millis). Present only when the upstream sent a numeric epoch that was normalised to the ISO 8601 `published_at` string. Kept for one deprecation cycle for integrations pinned to the numeric form. (seen in a sample response) |
| `post.ext.published_at_precision` | string\|null | How exactly published_at is known: hour or day on LinkedIn feeds, where the source only gives a relative age. Absent means the time is exact. |
| `post.ext.published_label` | string\|null | The relative label the source showed instead of a date, for example 'Streamed 3 weeks ago'. (seen in a sample response) |
| `post.ext.published_precision` | string\|null | How precise published_at is when the source gave only a relative label: minute, hour, day, week, month or year. (seen in a sample response) |
| `post.ext.quote_count` | number\|null | How many times the post was quoted. X and Threads. |
| `post.ext.quoted_post` | object\|null | Threads quote posts: the post this one quotes, as `{ id, url, author: { id, username }, text, media_urls, thumbnail_url }`. A quote post usually carries no caption or media of its own, and the text and video you see on the post's page belong to this attachment, by a different author. It is returned here rather than merged into `post.content`, so `content.*` always stays the outer post's own content and one account's media is never attributed to another. Absent on posts that are not quote posts. On LinkedIn feeds, `/v1/linkedin/search/posts` and `/v1/linkedin/search/hashtag`, the post a quote post quotes, in the same shape with the author's `display_name`, `engagement` and `published_at`; there the leaf is present on every post and null when the post quotes none. |
| `post.ext.reacted_at` | string\|null | When the member reacted, as an ISO 8601 UTC timestamp; published_at stays the post's own time. Profile reactions endpoint only. |
| `post.ext.reaction` | string\|null | The member's reaction to the post as LinkedIn's code: LIKE, PRAISE, EMPATHY, APPRECIATION, INTEREST or ENTERTAINMENT. Null on a reaction to a comment, and where reaction_type holds a sentence that is not one of LinkedIn's English forms for a reaction to the post. Profile reactions endpoint only. |
| `post.ext.reaction_activity_id` | string\|null | The id of the member's reaction itself on LinkedIn, the activity post.url links. Profile reactions endpoint only. |
| `post.ext.reaction_counts` | array\|null | Reaction counts by type. (with `include=details` on some endpoints) |
| `post.ext.reaction_type` | string\|null | How the member reacted, as LinkedIn's own rendered sentence (for example 'Bill Gates likes this'), localised. Profile reactions endpoint only. |
| `post.ext.region` | string\|null | TikTok only: the country TikTok registers the video to, as an ISO 3166-1 alpha-2 code (normally the creator's account country when they posted). It is not the viewer's country, not the `region` you requested, and not a language. On `/v1/tiktok/trending`, `/v1/tiktok/search`, `/v1/tiktok/search/top`, `/v1/tiktok/profile/videos`, `/v1/tiktok/search/hashtag` and `/v1/tiktok/song/videos` it is how you tell which rows are from a given country: filter on it when you need only that country. A row whose source omits the country stays null. The `region` request parameter still only sets the proxy. (on some endpoints only when the fallback source serves) |
| `post.ext.remix_count` | number\|null | How many reels were made from this reel. Instagram only. (seen in a sample response) |
| `post.ext.removed` | boolean\|null |  |
| `post.ext.removed_by` | string\|null |  |
| `post.ext.reposted_at` | string\|null | When the feed's member or page reposted this post, as an ISO 8601 UTC timestamp. LinkedIn feeds. |
| `post.ext.reposted_by` | object\|null | Who reposted this post into the feed you asked for. |
| `post.ext.reshare_count` | number\|null | The boosted reshare figure Threads shows in the app. |
| `post.ext.retweeted_post` | object | The original post behind a retweet. It is a different post by a different author. |
| `post.ext.retweeted_post.author.display_name` | string | The author's display name. (seen in a sample response) |
| `post.ext.retweeted_post.author.id` | string | The author's id on the platform. (seen in a sample response) |
| `post.ext.retweeted_post.author.username` | string | The author's handle. (seen in a sample response) |
| `post.ext.retweeted_post.author.verified` | boolean | Whether the platform marks the author as verified. (seen in a sample response) |
| `post.ext.retweeted_post.engagement.comments` | number | Reply count. (seen in a sample response) |
| `post.ext.retweeted_post.engagement.likes` | number | Like count. (seen in a sample response) |
| `post.ext.retweeted_post.engagement.saves` | number | Save or bookmark count. (seen in a sample response) |
| `post.ext.retweeted_post.engagement.shares` | number | Share or repost count. (seen in a sample response) |
| `post.ext.retweeted_post.engagement.views` | number | View count. (seen in a sample response) |
| `post.ext.retweeted_post.id` | string | The original post's id. (seen in a sample response) |
| `post.ext.retweeted_post.media_urls` | array\|null | Links to the media attached to the original post. (seen in a sample response) |
| `post.ext.retweeted_post.published_at` | string | When the original post was published, as the platform reported it (usually ISO 8601). (seen in a sample response) |
| `post.ext.retweeted_post.quote_count` | number | How many times the original post was quoted. (seen in a sample response) |
| `post.ext.retweeted_post.text` | string\|null | The text of the original post. (seen in a sample response) |
| `post.ext.retweeted_post.url` | string | Link to the original post. (seen in a sample response) |
| `post.ext.selftext` | string\|null | The Reddit post body without the title. Null on link posts. |
| `post.ext.share_urn` | string\|null | LinkedIn's share urn for the post. |
| `post.ext.sponsored_disclosed` | boolean\|null | The platform's own disclosure that the post is paid or promotional: on Instagram the paid-partnership label (`is_paid_partnership`) or a tagged brand partner, on TikTok the label TikTok shows viewers ("Paid partnership", "Commission paid", "Promotional content"), on LinkedIn the brand partnership label LinkedIn shows on the post. `false` when the post carries the flag unset, null when it carries none. Present on `/v1/instagram/post/stats`, `/v1/instagram/profile/posts`, `/v1/instagram/profile/reels`, `/v1/instagram/search/reels`, `/v1/tiktok/profile/videos` and `/v1/tiktok/search`, and on every post of the LinkedIn feeds (`/v1/linkedin/profile/posts`, `/v1/linkedin/company/posts`, `/v1/linkedin/profile/posts/archive`, `/v1/linkedin/profile/reactions`, `/v1/linkedin/post/reposts` and `/v1/linkedin/group/posts`), where it is null unless the source that answered reports the label; absent on every other endpoint. |
| `post.ext.subreddit` | string\|null | Reddit subreddit name (search/list items): pass to `/v1/reddit/subreddit/details?subreddit=` |
| `post.ext.tags` | array\|null | Video tags set by the creator. YouTube only. |
| `post.ext.text_entities` | array\|null | The linked ranges of the post's text. |
| `post.ext.text_truncated` | boolean\|null | True when content.text is a shortened summary and not the full note. Xiaohongshu only. |
| `post.ext.title` | string\|null | The post title on its own. Reddit only. |
| `post.ext.topic_tag` | string\|null | Name of the topic a Threads post is filed under. Not a slug, so join on topic_tag_id. |
| `post.ext.topic_tag_id` | string\|null | Id of the Threads topic. Use it to join, not the topic name. |
| `post.ext.topicCategories` | array\|null | Wikipedia URLs for the video's topics. YouTube only. (seen in a sample response) |
| `post.ext.trend.boards` | unknown | Every board the row ranks on, with its rank there. |
| `post.ext.trend.chart` | unknown | Which chart the row ranks on, such as `songs`. |
| `post.ext.trend.chart_title` | unknown | The chart's title in the board's language. |
| `post.ext.trend.content_tags` | unknown | Tags describing the video's content. |
| `post.ext.trend.country_code` | unknown | The market the board covers, as a country code. |
| `post.ext.trend.engagement_rate` | unknown | Engagement rate for the window, 0 to 1. |
| `post.ext.trend.industry` | unknown\|null | The industry code the board covers. |
| `post.ext.trend.industry_id` | unknown\|null | The industry's id. |
| `post.ext.trend.industry_label` | unknown\|null | The industry's name. |
| `post.ext.trend.order_by` | unknown | The sort the board was read with. |
| `post.ext.trend.organic_views` | unknown | Organic views in the window. |
| `post.ext.trend.period_days` | unknown | Length of the ranking window in days. |
| `post.ext.trend.period_views` | unknown | Views in the window. |
| `post.ext.trend.popularity_curve` | unknown | Daily popularity values for the window. |
| `post.ext.trend.posts` | unknown | How many posts used the item in the window. |
| `post.ext.trend.rank` | unknown | The row's rank on the board. |
| `post.ext.trend.six_second_view_through_rate` | unknown | Share of views that reached six seconds, 0 to 1. |
| `post.ext.trend.top_creators` | unknown | Creators who used the item most in the window. |
| `post.ext.trend.updated_at` | unknown | When the board was last refreshed, ISO 8601. |
| `post.ext.trend.views` | unknown | Views the item earned in the window. |
| `post.ext.type` | string\|null | Item type: pull_request or issue on GitHub lists; on LinkedIn feeds and post search, the kind of post in lower case, such as text, image, video, article, newsletter, document, poll, job, event or celebration. A poll can read text on a feed page whose answering source does not send the poll. |
| `post.ext.updated_at` | string\|null | When the platform last changed the post, as opposed to when it was published. |
| `post.ext.upvote_ratio` | number\|null | Reddit only: the share of a post's votes that are upvotes, as a fraction from 0 to 1 and usually close to 1 (six live rows measured 1, 1, 1, 0.86, 0.75, 1). Fractional despite the integer type this schema emits for every numeric leaf, the same caveat as `author.ext.average_rating`. Populated on `/v1/reddit/search` rows whose source carries it, and null everywhere else on Reddit including `/v1/reddit/post` and `/v1/reddit/subreddit`. |
| `post.ext.usertags` | array\|null | Handles of the accounts tagged in the post, in the order the platform lists them. (with `include=tags`) |
| `post.ext.video_count` | number\|null | Number of videos in the playlist. It is not a view count. |
| `post.ext.videoOwnerChannelId` | string\|null | Channel id of the video's owner. YouTube playlist items only. (seen in a sample response) |
| `post.ext.videoPublishedAt` | string\|null | When the video was published, as an ISO 8601 time. YouTube playlist items only. (seen in a sample response) |
| `post.flags.deleted` | boolean | Whether the post is tombstoned (always present) |
| `post.flags.likes_hidden` | boolean\|null | Present and `true` when the creator has hidden the like count. `engagement.likes` is `null` in that case (never the platform's decoy preview number). Absent on normal posts. (seen in a sample response) |
| `post.flags.nsfw` | boolean\|null | NSFW flag (null when platform does not surface) |
| `post.flags.pinned` | boolean\|null | Pinned-to-profile flag (null when platform does not surface) (with `exclude_pinned=true`, `include=engagement` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.flags.spoiler` | boolean\|null | Spoiler flag (null when platform does not surface) |
| `post.id` | string | Platform-specific post ID (always a string; numeric upstream IDs are stringified) |
| `post.published_at` | string\|number\|null | Post creation timestamp as an ISO 8601 UTC string. When the upstream sent a Unix epoch it is converted here and the raw epoch is preserved under `post.ext.published_at_epoch` for one deprecation cycle. (with `include=engagement`, `include=details` on some endpoints) (on some endpoints only when the fallback source serves) |
| `post.url` | string\|null | Direct URL to the post on the source platform (on some endpoints only when the fallback source serves) |
