# AuthorList fields

Every field the 34 field-mapped endpoints returning `AuthorList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `author.avatar_url` | string\|null | URL to profile picture |
| `author.bio` | string\|null | Profile biography or description (with `include=profile`, `include=details` on some endpoints) |
| `author.display_name` | string\|null | Display name or full name (with `include=details` on some endpoints) |
| `author.ext.account_created` | string\|null | (with `include=about`) |
| `author.ext.bio_link` | string\|null | (with `include=profile` on some endpoints) (on some endpoints only when the fallback source serves) |
| `author.ext.business_category` | string\|null | (with `include=profile`) |
| `author.ext.company_id` | string\|null |  |
| `author.ext.country` | string\|null | (with `include=profile`, `include=about`) |
| `author.ext.cover_url` | string\|null | (with `include=profile` on some endpoints) |
| `author.ext.followers_approximate` | boolean\|null | True when `author.followers` is a published or rounded figure rather than an unrounded census: LinkedIn people-list display buckets, TikTok `stats.followerCount` when the exact sibling is absent, and YouTube subscriber counts at or above 1,000. Null or absent on exact counts. |
| `author.ext.group.activity` | unknown\|null | (with `include=details`) |
| `author.ext.group.id` | unknown\|null | (with `include=details`) |
| `author.ext.group.privacy_label` | unknown\|null | (with `include=details`) |
| `author.ext.group.visibility_label` | unknown\|null | (with `include=details`) |
| `author.ext.is_creator` | boolean\|null | (with `include=profile`) |
| `author.ext.is_hiring` | boolean\|null | (with `include=profile`) |
| `author.ext.is_influencer` | boolean\|null | (with `include=profile`) |
| `author.ext.is_nsfw` | boolean\|null |  |
| `author.ext.is_open_to_work` | boolean\|null | (with `include=profile`) |
| `author.ext.is_premium` | boolean\|null | (with `include=profile` on some endpoints) |
| `author.ext.is_top_voice` | boolean\|null | (with `include=profile` on some endpoints) |
| `author.ext.language` | string\|null | (with `include=details`) |
| `author.ext.member_id` | string\|null | (with `include=profile`) |
| `author.ext.public_email` | string\|null | (with `include=about` on some endpoints) |
| `author.ext.public_phone` | string\|null | (with `include=about`) |
| `author.ext.reaction_type` | string\|null |  |
| `author.ext.rules_text` | string\|null | (with `include=details`) |
| `author.ext.search_hit.evidence_url` | string |  |
| `author.ext.search_hit.match` | string |  |
| `author.ext.search_hit.snippet` | string\|null |  |
| `author.ext.search_hit.title` | string\|null |  |
| `author.ext.urn` | string\|null |  |
| `author.ext.website` | string\|null | (with `include=profile`) |
| `author.ext.weekly_active_users` | number\|null | (with `include=details`) |
| `author.ext.weekly_contributions` | number\|null | (with `include=details`) |
| `author.external_url` | string\|null | Bio link / external website URL when surfaced by the platform |
| `author.followers` | number\|null | Follower or subscriber count as an integer. Exact on Instagram and on TikTok when the source exposes an unrounded figure. YouTube above 1,000 subscribers is YouTube's published three-significant-figure figure. When the integer is a published/rounded value, `author.ext.followers_approximate` is true. (with `include=profile`, `include=details` on some endpoints) |
| `author.following` | number\|null | Number of accounts followed (with `include=profile` on some endpoints) |
| `author.id` | string | Platform-specific user ID (always a string; platform-specific prefixes like `did:`, `spotify:artist:`, `t2_` are stripped) |
| `author.joined_at` | string\|null | (with `include=profile`, `include=details` on some endpoints) |
| `author.likes_count` | number\|null | Total likes received across the author's content (when surfaced) |
| `author.location` | string\|null | ISO region code (e.g. `US`) or freeform location string when surfaced (with `include=profile` on some endpoints) (on some endpoints only when the fallback source serves) |
| `author.posts_count` | number\|null | Total number of posts / videos / tracks / episodes (with `include=profile` on some endpoints) |
| `author.private` | boolean\|null | (with `include=profile` on some endpoints) |
| `author.url` | string\|null | Direct URL to the profile page |
| `author.username` | string\|null | User handle or username |
| `author.verified` | boolean\|null | Whether the account is verified |
| `computed.relevance` | object\|null | Without this param every row already carries computed.relevance against your query, free ({ p, sense, depth, spam }: is this row about what your query means, or a different thing that shares its words?), and nothing is dropped or reordered. |
