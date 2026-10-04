# Author fields

Every field the 38 field-mapped endpoints returning `Author` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `author.avatar_url` | string\|null | URL to profile picture (on some endpoints only when the fallback source serves) |
| `author.bio` | string\|null | Profile biography or description (on some endpoints only when the fallback source serves) |
| `author.display_name` | string\|null | Display name or full name (on some endpoints only when the fallback source serves) |
| `author.ext.account_created` | string\|null |  |
| `author.ext.ad_library_page_id` | string\|null |  |
| `author.ext.ad_library_status` | string\|null |  |
| `author.ext.address` | string\|null |  |
| `author.ext.average_rating` | number\|null | Spotify podcasts only: mean listener rating from 0 to 5. Fractional (e.g. 4.66) despite the integer type this schema emits for every numeric leaf |
| `author.ext.awardee_karma` | number\|null |  |
| `author.ext.banner_url` | string\|null |  |
| `author.ext.bannerExternalUrl` | string\|null | (only when the fallback source serves) |
| `author.ext.bio_link` | string\|null | (on some endpoints only when the fallback source serves) |
| `author.ext.business_category` | string\|null | (on some endpoints only when the fallback source serves) |
| `author.ext.business_hours` | array\|null |  |
| `author.ext.collects_received` | number\|null |  |
| `author.ext.comment_karma` | number\|null |  |
| `author.ext.contact_email` | string\|null | Opt-in (`contact_email=1` on instagram/profile, youtube/channel and youtube/channel/about). When the bio lists two or more email addresses, the one the creator gives for contacting them personally, copied verbatim. Null when there is one address or none, when every address belongs to a manager, agency or brand, or when the choice was not confident. `author.ext.public_email` (the first address in the bio) is unchanged. (with `contact_email=1`) |
| `author.ext.country` | string\|null |  |
| `author.ext.cover_url` | string\|null | (on some endpoints only when the fallback source serves) |
| `author.ext.creator_username` | string\|null |  |
| `author.ext.employee_count` | number\|null |  |
| `author.ext.employee_count_range` | object\|null |  |
| `author.ext.followers_approximate` | boolean\|null | True when `author.followers` is a published or rounded figure rather than an unrounded census: LinkedIn people-list display buckets, TikTok `stats.followerCount` when the exact sibling is absent, and YouTube subscriber counts at or above 1,000. Null or absent on exact counts. |
| `author.ext.founded_year` | number\|null |  |
| `author.ext.funding` | object\|null |  |
| `author.ext.group.about_info` | unknown\|null |  |
| `author.ext.group.activity` | unknown\|null |  |
| `author.ext.group.administrator_count` | unknown\|null |  |
| `author.ext.group.administrators` | unknown\|null |  |
| `author.ext.group.categories` | unknown\|null |  |
| `author.ext.group.history_summary` | unknown\|null |  |
| `author.ext.group.member_count_text` | unknown\|null |  |
| `author.ext.group.moderator_count` | unknown\|null |  |
| `author.ext.group.moderators` | unknown\|null |  |
| `author.ext.group.privacy_description` | unknown\|null |  |
| `author.ext.group.privacy_label` | unknown\|null |  |
| `author.ext.group.rules` | unknown\|null |  |
| `author.ext.group.visibility_description` | unknown\|null |  |
| `author.ext.group.visibility_label` | unknown\|null |  |
| `author.ext.hashtags` | array\|null |  |
| `author.ext.hd_avatar_url` | string\|null | (on some endpoints only when the fallback source serves) |
| `author.ext.headquarters` | object\|null |  |
| `author.ext.hiddenSubscriberCount` | boolean\|null | (seen in a sample response) |
| `author.ext.industries` | array\|null |  |
| `author.ext.is_creator` | boolean\|null |  |
| `author.ext.is_hiring` | boolean\|null |  |
| `author.ext.is_influencer` | boolean\|null |  |
| `author.ext.is_nsfw` | boolean\|null | (on some endpoints only when the fallback source serves) |
| `author.ext.is_open_to_work` | boolean\|null |  |
| `author.ext.is_premium` | boolean\|null | (only when the fallback source serves) |
| `author.ext.is_top_voice` | boolean\|null | (only when the fallback source serves) |
| `author.ext.join_policy` | string\|null |  |
| `author.ext.joined_at_timestamp` | string\|null | (seen in a sample response) |
| `author.ext.keywords` | string\|null | (on some endpoints only when the fallback source serves) |
| `author.ext.language` | string\|null | (only when the fallback source serves) |
| `author.ext.links` | array\|null | (on some endpoints only when the fallback source serves) |
| `author.ext.locations` | array\|null |  |
| `author.ext.madeForKids` | boolean\|null | (seen in a sample response) |
| `author.ext.member_id` | string\|null |  |
| `author.ext.monthly_listeners` | number\|null |  |
| `author.ext.page_active` | boolean\|null |  |
| `author.ext.post_karma` | number\|null |  |
| `author.ext.price_range` | string\|null |  |
| `author.ext.profile_title` | string\|null |  |
| `author.ext.public_email` | string\|null |  |
| `author.ext.public_phone` | string\|null |  |
| `author.ext.rating` | string\|null |  |
| `author.ext.rating_count` | number\|null |  |
| `author.ext.related_playlists.likes` | string\|null | (seen in a sample response) |
| `author.ext.related_playlists.uploads` | string\|null | (seen in a sample response) |
| `author.ext.rules` | array\|null |  |
| `author.ext.rules_text` | string\|null |  |
| `author.ext.social_links` | array\|null |  |
| `author.ext.specialities` | array\|null |  |
| `author.ext.talking_about_count` | number\|null |  |
| `author.ext.topic_ids` | array\|null | (seen in a sample response) |
| `author.ext.topicCategories` | array\|null | (seen in a sample response) |
| `author.ext.total_ratings` | number\|null | Spotify podcasts only: how many listeners have rated the show. Cumulative over the show's whole run, so it reflects longevity as well as size, and it is NOT an audience count (Spotify publishes no play, download, subscriber or follower count for a podcast) |
| `author.ext.total_views` | number\|null | (seen in a sample response) |
| `author.ext.trophy_count` | number\|null |  |
| `author.ext.unsubscribed_trailer` | string\|null | (seen in a sample response) |
| `author.ext.urn` | string\|null | (only when the fallback source serves) |
| `author.ext.website` | string\|null | (on some endpoints only when the fallback source serves) |
| `author.ext.weekly_active_users` | number\|null |  |
| `author.ext.weekly_contributions` | number\|null |  |
| `author.external_url` | string\|null | Bio link / external website URL when surfaced by the platform |
| `author.followers` | number\|null | Follower or subscriber count as an integer. Exact on Instagram and on TikTok when the source exposes an unrounded figure. YouTube above 1,000 subscribers is YouTube's published three-significant-figure figure. When the integer is a published/rounded value, `author.ext.followers_approximate` is true. (on some endpoints only when the fallback source serves) |
| `author.following` | number\|null | Number of accounts followed (on some endpoints only when the fallback source serves) |
| `author.id` | string | Platform-specific user ID (always a string; platform-specific prefixes like `did:`, `spotify:artist:`, `t2_` are stripped) |
| `author.joined_at` | string\|null | (on some endpoints only when the fallback source serves) |
| `author.last_post_at` | string\|null | (seen in a sample response) |
| `author.likes_count` | number\|null | Total likes received across the author's content (when surfaced) (on some endpoints only when the fallback source serves) |
| `author.location` | string\|null | ISO region code (e.g. `US`) or freeform location string when surfaced (on some endpoints only when the fallback source serves) |
| `author.posts_count` | number\|null | Total number of posts / videos / tracks / episodes (on some endpoints only when the fallback source serves) |
| `author.private` | boolean\|null | (on some endpoints only when the fallback source serves) |
| `author.url` | string\|null | Direct URL to the profile page |
| `author.username` | string\|null | User handle or username |
| `author.verified` | boolean\|null | Whether the account carries TikTok's verification badge. The source sends a badge label rather than a flag, and the API writes false when no label is present, so false can also mean the source sent no verification signal. (on some endpoints only when the fallback source serves) |
| `computed.content_category` | string\|null | Keyword-classified content category (e.g. tech, food, gaming). Null when undetectable. |
| `computed.engagement_rate` | number\|null | Computed engagement rate (0..1). Null when the upstream lacks enough signal. |
| `computed.estimated_reach` | number\|null | Estimated reach based on views or follower count. Null when uncomputable. |
| `computed.language` | string\|null |  |
