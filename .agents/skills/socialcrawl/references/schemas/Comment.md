# Comment fields

Every field the 2 field-mapped endpoints returning `Comment` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `comment.author.avatar_url` | string\|null | URL to comment author profile picture |
| `comment.author.display_name` | string\|null | Comment author display name |
| `comment.author.username` | string\|null | Comment author username (null when tombstoned) |
| `comment.author.verified` | boolean\|null | Whether the account carries TikTok's verification badge. The source sends a badge label rather than a flag, and the API writes false when no label is present, so false can also mean the source sent no verification signal. |
| `comment.engagement.likes` | number\|null | Like / upvote count |
| `comment.engagement.replies` | number\|null | Reply / child-comment count. `0` when the upstream structurally reports the count and the comment has no replies; `null` only when the upstream does not surface a reply count at all. |
| `comment.ext.published_at_epoch` | number\|null | Raw Unix epoch for `published_at` (present only when the upstream sent a numeric epoch that was normalised to the ISO 8601 string). |
| `comment.flags.deleted` | boolean | Whether the comment is tombstoned (always present, even when false) |
| `comment.flags.pinned` | boolean\|null | Pinned flag (null when platform does not surface) |
| `comment.id` | string | Platform-specific comment ID (always a string) |
| `comment.parent_id` | string\|null | Parent comment ID for nested replies, or null for top-level comments |
| `comment.post_id` | string\|null | ID of the post this comment belongs to |
| `comment.published_at` | string\|number\|null | Comment creation timestamp as an ISO 8601 UTC string. When the upstream sent a Unix epoch it is converted here and the raw epoch is preserved under `comment.ext.published_at_epoch` for one deprecation cycle. |
| `comment.text` | string\|null | Comment body. Tombstone sentinels ([deleted] / [removed]) are collapsed to null upstream: customers never see them. |
| `comment.url` | string\|null | Direct URL to the comment on the source platform |
| `computed.language` | string\|null |  |
