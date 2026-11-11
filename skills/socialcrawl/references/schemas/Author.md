# Author fields

Every field the 46 field-mapped endpoints returning `Author` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `author.avatar_url` | string\|null | URL to profile picture (on some endpoints only when the fallback source serves) |
| `author.bio` | string\|null | Profile biography or description (on some endpoints only when the fallback source serves) |
| `author.display_name` | string\|null | Display name or full name (on some endpoints only when the fallback source serves) |
| `author.ext.about` | string\|null | The member's About text, as written on the profile. LinkedIn members only. |
| `author.ext.about_localized` | object\|null | The About text in the member's other profile languages, keyed by locale (for example de_DE). The primary locale is left out because it repeats author.ext.about. Null when the profile has one language. |
| `author.ext.account_based_in` | string\|null |  |
| `author.ext.account_created` | string\|null | When the account was created, as a readable label such as 'August 2013'. |
| `author.ext.activity_summary` | string\|null |  |
| `author.ext.ad_library_page_id` | string\|null | The page's id in the Facebook Ad Library, which differs from the profile id. Pass it as the company id to the Ad Library ads endpoint. |
| `author.ext.ad_library_status` | string\|null | Whether the page is running ads, as the Ad Library reports it. |
| `author.ext.address` | string\|null | Street address the business page lists. Facebook only. |
| `author.ext.affiliate_username` | string\|null |  |
| `author.ext.average_rating` | number\|null | Spotify podcasts only: mean listener rating from 0 to 5. Fractional (e.g. 4.66) despite the integer type this schema emits for every numeric leaf |
| `author.ext.awardee_karma` | number\|null | Karma earned from awards received. Reddit accounts only. |
| `author.ext.banner_url` | string\|null | URL of the profile banner image. Reddit only. |
| `author.ext.bannerExternalUrl` | string\|null | URL of the channel banner image. YouTube only. (only when the fallback source serves) |
| `author.ext.bio_link` | string\|null | The website set in the Threads bio. (on some endpoints only when the fallback source serves) |
| `author.ext.bio_links` | array\|null | Every link the account lists on its profile, in order. On Instagram these are the bio links and author.external_url holds the first; on LinkedIn they are the contact links the member lists, with LinkedIn's category for each (the creator website is author.ext.website). |
| `author.ext.birthday` | string\|null |  |
| `author.ext.blog_name` | string\|null | The blog's own name. The display name is the owner's nickname. Naver only. |
| `author.ext.blog_no` | string\|null | Naver's blog number for the blog. |
| `author.ext.business_category` | string\|null | Professional or page category label, for example 'Live Music Venue'. Instagram and Facebook. (on some endpoints only when the fallback source serves) |
| `author.ext.business_hours` | array\|null | The page's opening hours as the source reports them. The source's format is not normalised and the field is null on every sampled page. |
| `author.ext.call_to_action_url` | string\|null | Where the page's main button leads. |
| `author.ext.collects_received` | number\|null | How many times the account's notes were collected. Xiaohongshu only, separate from likes_count. |
| `author.ext.comment_karma` | number\|null | Karma earned from comments. Reddit accounts only. |
| `author.ext.company_type` | string\|null | Company type from the About tab, for example 'Public Company' or 'Privately Held'. |
| `author.ext.company_type_code` | string\|null | LinkedIn's stable code for the company type, for example PUBLIC_COMPANY. Match on this rather than on the label. |
| `author.ext.contact_email` | string\|null | Opt-in (`contact_email=1` on instagram/profile, youtube/channel and youtube/channel/about). When the bio lists two or more email addresses, the one the creator gives for contacting them personally, copied verbatim. Null when there is one address or none, when every address belongs to a manager, agency or brand, or when the choice was not confident. `author.ext.public_email` (the first address in the bio) is unchanged. (with `contact_email=1`) |
| `author.ext.country` | string\|null | Account country as an ISO 3166-1 alpha-2 code, or null when the profile does not name a single country. |
| `author.ext.country_name` | string\|null | English name of country, for example 'South Korea' for KR. (seen in a sample response) |
| `author.ext.cover_url` | string\|null | URL of the page banner or cover image. (on some endpoints only when the fallback source serves) |
| `author.ext.created_country_accurate` | boolean\|null |  |
| `author.ext.creator_subscriptions_count` | number\|null |  |
| `author.ext.creator_username` | string\|null | Handle of the person who created the community. X communities only. |
| `author.ext.credit_level` | string\|null |  |
| `author.ext.crunchbase_url` | string\|null | The company's Crunchbase profile, when the page links one. |
| `author.ext.current_position` | object\|null | The member's current role as LinkedIn shows it in the profile header, or null when they show none. |
| `author.ext.current_school` | object\|null | The school LinkedIn shows in the profile header, or null when the member shows none. |
| `author.ext.domain` | string\|null | The host of the company's website as LinkedIn records it, for example stripe.com. |
| `author.ext.embed_html` | string\|null | Instagram's embed snippet for the profile, ready to paste into a page. |
| `author.ext.embed_url` | string\|null | The iframe source the embed snippet loads. |
| `author.ext.employee_count` | number\|null | Exact headcount shown on the company page. |
| `author.ext.employee_count_range` | object\|null | The size bucket LinkedIn shows, for example 10,001+ employees, as numbers. |
| `author.ext.employer` | string\|null |  |
| `author.ext.entity_type` | string\|null |  |
| `author.ext.first_name` | string\|null | The member's first name. LinkedIn members only. |
| `author.ext.followers_approximate` | boolean\|null | True when `author.followers` is a published or rounded figure rather than an unrounded census: LinkedIn people-list display buckets, TikTok `stats.followerCount` when the exact sibling is absent, and YouTube subscriber counts at or above 1,000. Null or absent on exact counts. |
| `author.ext.founded_on` | object\|null | The founding date the company page sets. Month and day are null when the page gives the year only, and the whole field is null when it sets no date. |
| `author.ext.founded_year` | number\|null | Year the company was founded. |
| `author.ext.funding` | object\|null | The company's funding. Its inner fields are empty objects when the source sends no figures. |
| `author.ext.gender` | string\|null |  |
| `author.ext.geo_id` | string\|null | LinkedIn's id for the member's location, the id /v1/linkedin/search/location returns. |
| `author.ext.group.about_info` | unknown | The entries of the group's About section. |
| `author.ext.group.activity` | unknown | Recent posting and joining activity. |
| `author.ext.group.administrator_count` | unknown | How many administrators the group has. |
| `author.ext.group.administrators` | unknown | The group's administrators. |
| `author.ext.group.categories` | unknown\|null | Categories the group lists. |
| `author.ext.group.history_summary` | unknown | When the group was created, as text. |
| `author.ext.group.member_count_text` | unknown | The member count as the platform words it. |
| `author.ext.group.moderator_count` | unknown | How many moderators the group has. |
| `author.ext.group.moderators` | unknown | The group's moderators. |
| `author.ext.group.privacy_description` | unknown | What the privacy setting means. |
| `author.ext.group.privacy_label` | unknown | Privacy setting, such as `Public`. |
| `author.ext.group.rules` | unknown\|null | The group's rules. |
| `author.ext.group.visibility_description` | unknown | What the visibility setting means. |
| `author.ext.group.visibility_label` | unknown | Visibility setting, such as `Visible`. |
| `author.ext.hashtags` | array\|null | Hashtags the company page follows, or on a LinkedIn member the hashtags the member says they talk about. An empty list when a company page follows none; null on a member who lists none. |
| `author.ext.hd_avatar_url` | string\|null | URL of the full resolution avatar. |
| `author.ext.headline_localized` | object\|null | The headline in the member's other profile languages, keyed by locale. The primary locale is left out because it repeats author.bio. Null when the profile has one language. |
| `author.ext.headquarters` | object\|null | The company's headquarters address. |
| `author.ext.hiddenSubscriberCount` | boolean\|null | Whether the channel hides its subscriber count. YouTube only. (seen in a sample response) |
| `author.ext.hometown` | string\|null |  |
| `author.ext.identity_verified` | boolean\|null |  |
| `author.ext.industries` | array\|null | Industries the company lists. |
| `author.ext.industry` | string\|null | The member's industry label. The wording can vary between answers for the same industry, so match on author.ext.industry_id. |
| `author.ext.industry_hierarchy` | string\|null | The company's industry with its parent categories, for example 'Manufacturing > Paper and Forest Product Manufacturing'. |
| `author.ext.industry_id` | string\|null | LinkedIn's numeric industry id, as a string. The stable key for the member's or company's industry. |
| `author.ext.instagram_followers` | number\|null |  |
| `author.ext.instagram_username` | string\|null | The Instagram account this suggestion was matched from, on TikTok similar accounts. |
| `author.ext.instagram_verified` | boolean\|null |  |
| `author.ext.ip_location` | string\|null |  |
| `author.ext.is_archived` | boolean\|null | Whether LinkedIn has archived the company page. |
| `author.ext.is_auto_generated` | boolean\|null | Whether LinkedIn created the page itself rather than the company. |
| `author.ext.is_claimable` | boolean\|null | Whether the company page is unclaimed and can still be claimed by the company. |
| `author.ext.is_creator` | boolean\|null | Whether the member is in LinkedIn's creator programme. |
| `author.ext.is_hiring` | boolean\|null | Whether the member shows a hiring badge. |
| `author.ext.is_influencer` | boolean\|null | Whether the member is flagged as a LinkedIn influencer. |
| `author.ext.is_memorialized` | unknown\|null | LinkedIn members only: whether LinkedIn has memorialised this member's account. |
| `author.ext.is_nsfw` | boolean\|null | Whether the community is marked as adult. X communities only. (on some endpoints only when the fallback source serves) |
| `author.ext.is_open_profile` | boolean\|null | Whether the member accepts messages from anyone (LinkedIn's Open Profile). |
| `author.ext.is_open_to_work` | boolean\|null | Whether the member shows the open to work badge. |
| `author.ext.is_political_page` | boolean\|null |  |
| `author.ext.is_premium` | boolean\|null | Whether the member has a LinkedIn Premium subscription, or on a company page whether it is a paid Premium page. (on some endpoints only when the fallback source serves) |
| `author.ext.is_top_voice` | boolean\|null | Whether the member carries LinkedIn's Top Voice badge. (only when the fallback source serves) |
| `author.ext.join_policy` | string\|null | How people join the community, as the platform labels it. X communities only. |
| `author.ext.joined_at_precision` | string\|null | month when author.joined_at is the first day of the month the member joined, because the answering source gives the month and year only. Null when author.joined_at is the exact day. LinkedIn only. |
| `author.ext.joined_at_timestamp` | string\|null | Full ISO 8601 creation time of the channel or account. author.joined_at holds its date part. YouTube, and TikTok with include=account. (with `include=account` on some endpoints) |
| `author.ext.keywords` | string\|null | Channel keywords as one space separated string. YouTube only. (on some endpoints only when the fallback source serves) |
| `author.ext.language` | string\|null | The community's primary language tag, for example en. Reddit only. (only when the fallback source serves) |
| `author.ext.last_name` | string\|null | The member's last name, or its initial when LinkedIn shows only that. LinkedIn members only. |
| `author.ext.last_name_is_initial` | boolean\|null | True when LinkedIn shows only the initial of the member's last name. Null otherwise. |
| `author.ext.likes_given` | number\|null |  |
| `author.ext.links` | array\|null | Links the profile lists. On linktree/page each is `{ id, type, title, url }`. On X profiles each is one of the destination URLs written in the bio, in order. On facebook/profile they are the outbound links the page lists in its About tab. (on some endpoints only when the fallback source serves) |
| `author.ext.location_accurate` | boolean\|null |  |
| `author.ext.locations` | array\|null | The company's offices and other locations. |
| `author.ext.madeForKids` | boolean\|null | Whether the channel is marked as made for kids. YouTube only. (seen in a sample response) |
| `author.ext.media_count` | number\|null |  |
| `author.ext.member_id` | string\|null | Numeric LinkedIn member id. author.id is the vanity slug, and post endpoints publish this id as post.ext.author_id. |
| `author.ext.monthly_listeners` | number\|null | Monthly listeners, a reach figure and not a post count. Spotify artists only. |
| `author.ext.official_blog` | boolean\|null | Whether the blog carries Naver's official blog flag. |
| `author.ext.open_job_count` | number\|null | How many jobs the company has open on LinkedIn. |
| `author.ext.page_active` | boolean\|null | Whether the page is active, as the page reports it. |
| `author.ext.page_category` | string\|null |  |
| `author.ext.page_is_restricted` | boolean\|null |  |
| `author.ext.page_type` | string\|null | Which kind of LinkedIn page this is: company, school or showcase. |
| `author.ext.page_verification` | string\|null |  |
| `author.ext.post_karma` | number\|null | Karma earned from posts. Reddit accounts only. |
| `author.ext.posting_region` | string\|null | (with `include=account`) |
| `author.ext.power_blog` | boolean\|null | Whether the blog carries Naver's power blog flag. |
| `author.ext.price_range` | string\|null | Price range the business page lists, for example '$$'. Facebook only. |
| `author.ext.primary_locale` | string\|null | The member's main profile language and region as a locale tag, for example en_US. |
| `author.ext.products` | array\|null | The products the company page lists, as the source sends them. Null when it lists none. |
| `author.ext.profile_actions` | array\|null | The buttons in the member's profile header, such as 'Visit my website'. Not the contact links, which are author.ext.bio_links. Null when the answer gives none. |
| `author.ext.profile_title` | string\|null | Profile title the account set, independent of its username. Reddit only. |
| `author.ext.pronoun` | string\|null | The pronouns the member shows, for example she/her. Null when none. |
| `author.ext.public_email` | string\|null | The public contact address the account publishes, or null. On instagram/profile/about it is the address on the account's contact panel, and the first address in the bio only when the panel has none. On instagram/profile it is the first address in the bio. |
| `author.ext.public_phone` | string\|null | Business phone number the account publishes, when it exposes one. |
| `author.ext.public_phone_extension` | string\|null | The extension of the page's phone number, or null. |
| `author.ext.rating` | string\|null | Recommendation text the page shows, for example '80% recommend (794 Reviews)'. A display string, not a number. |
| `author.ext.rating_count` | number\|null | Number of reviews behind the rating text. Facebook only. |
| `author.ext.related_playlists.likes` | string | Id of the liked-videos playlist. Empty when it is private. (seen in a sample response) |
| `author.ext.related_playlists.uploads` | string | Id of the playlist holding every upload. (seen in a sample response) |
| `author.ext.rules` | array\|null | The community's rules. (on some endpoints only when the fallback source serves) |
| `author.ext.rules_text` | string\|null | The community rules as one newline separated text block. Reddit only. |
| `author.ext.section_totals` | object\|null | The source's own count for each profile section. It can exceed the length of a section list, so trust this for a count. |
| `author.ext.signup_source` | string\|null |  |
| `author.ext.social_links` | array\|null | Social profiles linked from the account. |
| `author.ext.specialities` | array\|null | Specialities the company lists. |
| `author.ext.supported_locales` | array\|null | Every language the member's profile is written in, as locale tags. |
| `author.ext.tagline` | string\|null | The page tagline. (with `include=about` on some endpoints) |
| `author.ext.talking_about_count` | number\|null | Number of people Facebook counts as talking about the page. |
| `author.ext.top_skills` | array\|null | The skills LinkedIn shows first on the profile. |
| `author.ext.topic` | string\|null | The topic the blog is filed under. Naver only. |
| `author.ext.topic_ids` | array\|null | Freebase topic ids for the channel. YouTube only. (seen in a sample response) |
| `author.ext.topicCategories` | array\|null | Wikipedia URLs for the channel's topics. YouTube only. (seen in a sample response) |
| `author.ext.total_ratings` | number\|null | Spotify podcasts only: how many listeners have rated the show. Cumulative over the show's whole run, so it reflects longevity as well as size, and it is NOT an audience count (Spotify publishes no play, download, subscriber or follower count for a podcast) |
| `author.ext.total_views` | number\|null | Lifetime view count of the channel. YouTube only. (seen in a sample response) |
| `author.ext.trophy_count` | number\|null | Number of trophies on the Reddit profile. |
| `author.ext.unsubscribed_trailer` | string\|null | Video id of the channel trailer shown to people who have not subscribed. YouTube only. (seen in a sample response) |
| `author.ext.urn` | string\|null | Opaque LinkedIn urn for the member or company. The /user endpoints take it as their join key. (only when the fallback source serves) |
| `author.ext.username_changes` | number\|null |  |
| `author.ext.username_last_changed_at` | string\|null |  |
| `author.ext.verification_reason` | string\|null |  |
| `author.ext.verification_updated_at` | string\|null | When LinkedIn last changed the page's verification record, as an ISO 8601 timestamp. It is not the date the page was verified. |
| `author.ext.verifications` | array\|null | The verifications LinkedIn lists on the profile, such as an identity check or a work email. Null when the answer did not include the list. |
| `author.ext.verified_blue` | boolean\|null |  |
| `author.ext.verified_country_code` | string\|null |  |
| `author.ext.verified_legacy` | boolean\|null |  |
| `author.ext.verified_name` | string\|null |  |
| `author.ext.verified_reason` | string\|null |  |
| `author.ext.verified_type` | number\|null |  |
| `author.ext.visitors_today` | number\|null | Visitors the blog counted today. Naver only. |
| `author.ext.visitors_total` | number\|null | Visitors the blog counted in total. Naver only. |
| `author.ext.volunteer_causes` | array\|null | The causes the member says they care about, as LinkedIn labels them. |
| `author.ext.website` | string\|null | The company, page or member's own website, not the profile permalink. (on some endpoints only when the fallback source serves) |
| `author.ext.weekly_active_users` | number\|null | People active in the community in a week, as Reddit shows it. Not the subscriber count. |
| `author.ext.weekly_contributions` | number\|null | Posts and comments made in the community in a week, as Reddit shows it. |
| `author.external_url` | string\|null | Bio link / external website URL when surfaced by the platform |
| `author.followers` | number\|null | Follower or subscriber count as an integer. Exact on Instagram and on TikTok when the source exposes an unrounded figure. YouTube above 1,000 subscribers is YouTube's published three-significant-figure figure. When the integer is a published/rounded value, `author.ext.followers_approximate` is true. (on some endpoints only when the fallback source serves) |
| `author.following` | number\|null | Number of accounts followed (on some endpoints only when the fallback source serves) |
| `author.id` | string | Platform-specific user ID (always a string; platform-specific prefixes like `did:`, `spotify:artist:`, `t2_` are stripped) |
| `author.joined_at` | string\|null | When the account was created, as an ISO 8601 date (YYYY-MM-DD). (with `include=account` on some endpoints) (on some endpoints only when the fallback source serves) |
| `author.last_post_at` | string\|null | Publish time of the newest post returned with the profile, as an ISO 8601 instant. Null when the source returned no posts. (seen in a sample response) |
| `author.likes_count` | number\|null | Total likes received across the author's content (when surfaced) (on some endpoints only when the fallback source serves) |
| `author.location` | string\|null | ISO region code (e.g. `US`) or freeform location string when surfaced (on some endpoints only when the fallback source serves) |
| `author.posts_count` | number\|null | Total number of posts / videos / tracks / episodes (on some endpoints only when the fallback source serves) |
| `author.private` | boolean\|null | Whether the account is private. (on some endpoints only when the fallback source serves) |
| `author.url` | string\|null | Direct URL to the profile page |
| `author.username` | string\|null | User handle or username |
| `author.verified` | boolean\|null | Whether the account carries TikTok's verification badge. The source sends a badge label rather than a flag, and the API writes false when no label is present, so false can also mean the source sent no verification signal. (on some endpoints only when the fallback source serves) |
| `computed.content_category` | string\|null | Keyword-classified content category (e.g. tech, food, gaming). Null when undetectable. |
| `computed.engagement_rate` | number\|null | Computed engagement rate (0..1). Null when the upstream lacks enough signal. |
| `computed.estimated_reach` | number\|null | Estimated reach based on views or follower count. Null when uncomputable. |
| `computed.language` | string\|null |  |
| `computed.save_rate` | number\|null |  |
