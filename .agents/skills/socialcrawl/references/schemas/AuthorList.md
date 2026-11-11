# AuthorList fields

Every field the 39 field-mapped endpoints returning `AuthorList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `author.avatar_url` | string\|null | URL to profile picture (with `include=details` on some endpoints) |
| `author.bio` | string\|null | Profile biography or description (with `include=details`, `include=profile` on some endpoints) |
| `author.display_name` | string\|null | Display name or full name (with `include=details` on some endpoints) |
| `author.ext.account_created` | string\|null | When the account was created, as a readable label such as 'August 2013'. (with `include=about`) |
| `author.ext.account_type` | string\|null | Whether the reactor is a member (user) or a page (company). LinkedIn reactor lists only. |
| `author.ext.bannerExternalUrl` | string\|null | URL of the channel banner image. YouTube only. (seen in a sample response) |
| `author.ext.bio_link` | string\|null | The website set in the Threads bio. (with `include=profile` on some endpoints) (on some endpoints only when the fallback source serves) |
| `author.ext.business_category` | string\|null | Professional or page category label, for example 'Live Music Venue'. Instagram and Facebook. (with `include=profile`) |
| `author.ext.business_hours` | array | The page's opening hours as the source reports them. The source's format is not normalised and the field is null on every sampled page. |
| `author.ext.call_to_action_url` | string\|null | Where the page's main button leads. |
| `author.ext.company_id` | string\|null | Numeric company id, which is what the LinkedIn company endpoints take. author.id on these rows is the vanity slug. |
| `author.ext.company_type` | string\|null | Company type from the About tab, for example 'Public Company' or 'Privately Held'. |
| `author.ext.company_type_code` | string\|null | LinkedIn's stable code for the company type, for example PUBLIC_COMPANY. Match on this rather than on the label. |
| `author.ext.country` | string\|null | Account country as an ISO 3166-1 alpha-2 code, or null when the profile does not name a single country. (with `include=profile`, `include=about` on some endpoints) |
| `author.ext.country_name` | string\|null | English name of country, for example 'South Korea' for KR. (seen in a sample response) |
| `author.ext.cover_url` | string\|null | URL of the page banner or cover image. (with `include=profile` on some endpoints) |
| `author.ext.crunchbase_url` | string\|null | The company's Crunchbase profile, when the page links one. |
| `author.ext.domain` | string\|null | The host of the company's website as LinkedIn records it, for example stripe.com. |
| `author.ext.employee_count` | number\|null | Exact headcount shown on the company page. |
| `author.ext.employee_count_range` | object\|null | The size bucket LinkedIn shows, for example 10,001+ employees, as numbers. |
| `author.ext.followers_approximate` | boolean\|null | True when `author.followers` is a published or rounded figure rather than an unrounded census: LinkedIn people-list display buckets, TikTok `stats.followerCount` when the exact sibling is absent, and YouTube subscriber counts at or above 1,000. Null or absent on exact counts. |
| `author.ext.founded_on` | object\|null | The founding date the company page sets. Month and day are null when the page gives the year only, and the whole field is null when it sets no date. |
| `author.ext.founded_year` | number\|null | Year the company was founded. |
| `author.ext.funding` | object\|null | The company's funding. Its inner fields are empty objects when the source sends no figures. |
| `author.ext.gender` | string\|null |  |
| `author.ext.group.activity` | unknown\|null | Recent posting and joining activity. (with `include=details`) |
| `author.ext.group.id` | unknown\|null | (with `include=details`) |
| `author.ext.group.privacy_label` | unknown\|null | Privacy setting, such as `Public`. (with `include=details`) |
| `author.ext.group.visibility_label` | unknown\|null | Visibility setting, such as `Visible`. (with `include=details`) |
| `author.ext.hashtags` | array\|null | Hashtags the company page follows, or on a LinkedIn member the hashtags the member says they talk about. An empty list when a company page follows none; null on a member who lists none. |
| `author.ext.headquarters` | object\|null | The company's headquarters address. |
| `author.ext.hiddenSubscriberCount` | boolean\|null | Whether the channel hides its subscriber count. YouTube only. (seen in a sample response) |
| `author.ext.industries` | array\|null | Industries the company lists. |
| `author.ext.industry_hierarchy` | string\|null | The company's industry with its parent categories, for example 'Manufacturing > Paper and Forest Product Manufacturing'. |
| `author.ext.industry_id` | string\|null | LinkedIn's numeric industry id, as a string. The stable key for the member's or company's industry. |
| `author.ext.is_archived` | boolean\|null | Whether LinkedIn has archived the company page. |
| `author.ext.is_auto_generated` | boolean\|null | Whether LinkedIn created the page itself rather than the company. |
| `author.ext.is_claimable` | boolean\|null | Whether the company page is unclaimed and can still be claimed by the company. |
| `author.ext.is_creator` | boolean\|null | Whether the member is in LinkedIn's creator programme. (with `include=profile`) |
| `author.ext.is_hiring` | boolean\|null | Whether the member shows a hiring badge. (with `include=profile`) |
| `author.ext.is_influencer` | boolean\|null | Whether the member is flagged as a LinkedIn influencer. (with `include=profile`) |
| `author.ext.is_nsfw` | boolean\|null | Whether the community is marked as adult. X communities only. |
| `author.ext.is_open_to_work` | boolean\|null | Whether the member shows the open to work badge. (with `include=profile`) |
| `author.ext.is_premium` | boolean\|null | Whether the member has a LinkedIn Premium subscription, or on a company page whether it is a paid Premium page. (with `include=profile` on some endpoints) |
| `author.ext.is_top_voice` | boolean\|null | Whether the member carries LinkedIn's Top Voice badge. (with `include=profile` on some endpoints) |
| `author.ext.joined_at_precision` | string\|null | month when author.joined_at is the first day of the month the member joined, because the answering source gives the month and year only. Null when author.joined_at is the exact day. LinkedIn only. (with `include=profile`) |
| `author.ext.joined_at_timestamp` | string\|null | Full ISO 8601 creation time of the channel or account. author.joined_at holds its date part. YouTube, and TikTok with include=account. (seen in a sample response) |
| `author.ext.keywords` | string\|null | Channel keywords as one space separated string. YouTube only. (seen in a sample response) |
| `author.ext.language` | string\|null | The community's primary language tag, for example en. Reddit only. (with `include=details`) |
| `author.ext.locations` | array\|null | The company's offices and other locations. |
| `author.ext.madeForKids` | boolean\|null | Whether the channel is marked as made for kids. YouTube only. (seen in a sample response) |
| `author.ext.member_id` | string\|null | Numeric LinkedIn member id. author.id is the vanity slug, and post endpoints publish this id as post.ext.author_id. (with `include=profile`) |
| `author.ext.open_job_count` | number\|null | How many jobs the company has open on LinkedIn. |
| `author.ext.page_active` | boolean\|null | Whether the page is active, as the page reports it. |
| `author.ext.page_type` | string\|null | Which kind of LinkedIn page this is: company, school or showcase. |
| `author.ext.products` | array | The products the company page lists, as the source sends them. Null when it lists none. |
| `author.ext.public_email` | string\|null | The public contact address the account publishes, or null. On instagram/profile/about it is the address on the account's contact panel, and the first address in the bio only when the panel has none. On instagram/profile it is the first address in the bio. (with `include=about` on some endpoints) |
| `author.ext.public_identifier` | string\|null |  |
| `author.ext.public_phone` | string\|null | Business phone number the account publishes, when it exposes one. (with `include=about` on some endpoints) |
| `author.ext.public_phone_extension` | string\|null | The extension of the page's phone number, or null. |
| `author.ext.reaction_type` | string\|null | How this member reacted to the post, on the reactions endpoint: LIKE, PRAISE, EMPATHY, APPRECIATION, INTEREST or ENTERTAINMENT. |
| `author.ext.related_playlists.likes` | string | Id of the liked-videos playlist. Empty when it is private. (seen in a sample response) |
| `author.ext.related_playlists.uploads` | string | Id of the playlist holding every upload. (seen in a sample response) |
| `author.ext.rules_text` | string\|null | The community rules as one newline separated text block. Reddit only. (with `include=details`) |
| `author.ext.search_hit.evidence_url` | string | The exact URL the search hit. |
| `author.ext.search_hit.match` | string | What was hit: group_page, post_in_group, channel_page or post_in_channel. |
| `author.ext.search_hit.matched_urls` | array | Every distinct URL the search matched for this channel, in order. Telegram only. |
| `author.ext.search_hit.snippet` | string\|null | The hit text as the search index showed it. It is not the account's own description. |
| `author.ext.search_hit.title` | string\|null | The hit title as the search index showed it. It is not the account's own name. |
| `author.ext.specialities` | array\|null | Specialities the company lists. |
| `author.ext.tagline` | string\|null | The page tagline. |
| `author.ext.topic_ids` | array\|null | Freebase topic ids for the channel. YouTube only. (seen in a sample response) |
| `author.ext.topicCategories` | array\|null | Wikipedia URLs for the channel's topics. YouTube only. (seen in a sample response) |
| `author.ext.total_views` | number\|null | Lifetime view count of the channel. YouTube only. (seen in a sample response) |
| `author.ext.unsubscribed_trailer` | string\|null | Video id of the channel trailer shown to people who have not subscribed. YouTube only. (seen in a sample response) |
| `author.ext.urn` | string\|null | Opaque LinkedIn urn for the member or company. The /user endpoints take it as their join key. |
| `author.ext.verification_updated_at` | string\|null | When LinkedIn last changed the page's verification record, as an ISO 8601 timestamp. It is not the date the page was verified. |
| `author.ext.verified_reason` | string\|null |  |
| `author.ext.website` | string\|null | The company, page or member's own website, not the profile permalink. (with `include=profile` on some endpoints) |
| `author.ext.weekly_active_users` | number\|null | People active in the community in a week, as Reddit shows it. Not the subscriber count. (with `include=details`) |
| `author.ext.weekly_contributions` | number\|null | Posts and comments made in the community in a week, as Reddit shows it. (with `include=details`) |
| `author.external_url` | string\|null | Bio link / external website URL when surfaced by the platform |
| `author.followers` | number\|null | Follower or subscriber count as an integer. Exact on Instagram and on TikTok when the source exposes an unrounded figure. YouTube above 1,000 subscribers is YouTube's published three-significant-figure figure. When the integer is a published/rounded value, `author.ext.followers_approximate` is true. (with `include=profile`, `include=details` on some endpoints) |
| `author.following` | number\|null | Number of accounts followed (with `include=profile` on some endpoints) |
| `author.id` | string | Platform-specific user ID (always a string; platform-specific prefixes like `did:`, `spotify:artist:`, `t2_` are stripped) |
| `author.joined_at` | string\|null | When the account was created, as an ISO 8601 date (YYYY-MM-DD). (with `include=profile`, `include=details` on some endpoints) |
| `author.likes_count` | number\|null | Total likes received across the author's content (when surfaced) (with `include=details` on some endpoints) |
| `author.location` | string\|null | ISO region code (e.g. `US`) or freeform location string when surfaced (with `include=profile` on some endpoints) (on some endpoints only when the fallback source serves) |
| `author.posts_count` | number\|null | Total number of posts / videos / tracks / episodes (with `include=profile` on some endpoints) |
| `author.private` | boolean\|null | Whether the account is private. (with `include=profile` on some endpoints) |
| `author.url` | string\|null | Direct URL to the profile page |
| `author.username` | string\|null | User handle or username |
| `author.verified` | boolean\|null | Whether the account is verified (with `include=details` on some endpoints) |
| `computed.relevance` | object\|null | Without this param every row already carries computed.relevance against your query, free ({ p, sense, depth, spam }: is this row about what your query means, or a different thing that shares its words?), and nothing is dropped or reordered. |
