# CommentList fields

Every field the 24 field-mapped endpoints returning `CommentList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `comment.author.avatar_url` | string\|null | URL to comment author profile picture |
| `comment.author.display_name` | string\|null | Comment author display name |
| `comment.author.username` | string\|null | Comment author username (null when tombstoned) |
| `comment.author.verified` | boolean\|null | Whether the account carries TikTok's verification badge. The source sends a badge label rather than a flag, and the API writes false when no label is present, so false can also mean the source sent no verification signal. (on some endpoints only when the fallback source serves) |
| `comment.engagement.likes` | number\|null | Like / upvote count |
| `comment.engagement.replies` | number\|null | Reply / child-comment count. `0` when the upstream structurally reports the count and the comment has no replies; `null` only when the upstream does not surface a reply count at all. (on some endpoints only when the fallback source serves) |
| `comment.ext.author_channel_id` | string\|null | (only when the fallback source serves) |
| `comment.ext.author_followers` | number\|null | The commenter's follower count as embedded in this row. Snapshot as of whenever the replies source saw the account, not a live figure. On X this is present on every `tweet/replies` row. |
| `comment.ext.author_following` | number\|null | The commenter's following count as embedded in this row. Same snapshot caveat as `author_followers`. |
| `comment.ext.author_headline` | string\|null |  |
| `comment.ext.author_id` | string\|null | The commenter's platform-native numeric user id, where the upstream exposes one. |
| `comment.ext.author_posts_count` | number\|null | The commenter's post count as embedded in this row. Same snapshot caveat as `author_followers`. |
| `comment.ext.author_url` | string\|null |  |
| `comment.ext.content_language` | string\|null | ISO 639-1 language tag for this comment, when the source reports one. X writes `zxx` / `und` for no linguistic content; those collapse to null. |
| `comment.ext.controversiality` | number\|null |  |
| `comment.ext.depth` | number\|null | Reddit comment nesting depth as the source reports it: 0 on a top-level comment, 1 on a direct reply, and so on. Present when the thread arrived flat and was re-nested into `replies[]`, so you can verify that nesting independently. |
| `comment.ext.expansion_token` | string\|null | Facebook comment expansion/paginator token: feeds `/v1/facebook/post/comment/replies` |
| `comment.ext.feedback_id` | string\|null | Facebook comment feedback id: feeds `/v1/facebook/post/comment/replies` (only when the fallback source serves) |
| `comment.ext.ip_location` | string\|null |  |
| `comment.ext.is_edited` | boolean\|null |  |
| `comment.ext.is_submitter` | boolean\|null |  |
| `comment.ext.post_author` | string\|null |  |
| `comment.ext.post_comment_count` | number\|null |  |
| `comment.ext.post_flair` | string\|null |  |
| `comment.ext.post_published_at` | string\|null |  |
| `comment.ext.post_score` | number\|null |  |
| `comment.ext.post_title` | string\|null |  |
| `comment.ext.post_url` | string\|null |  |
| `comment.ext.preview_replies` | array\|null | (seen in a sample response) |
| `comment.ext.previous_replies_token` | string\|null |  |
| `comment.ext.published_at_epoch` | number\|null | Raw Unix epoch for `published_at` (present only when the upstream sent a numeric epoch that was normalised to the ISO 8601 string). (seen in a sample response) |
| `comment.ext.quote_count` | number\|null | How many quote-posts this comment has, when the source reports it. On X a reply is a tweet, so this is the same figure `post.ext.quote_count` carries on tweet endpoints. |
| `comment.ext.reaction_counts` | array\|null | (seen in a sample response) |
| `comment.ext.replies_token` | string\|null | YouTube reply continuation token: pass to `/v1/youtube/video/comment/replies?continuationToken=` (only when the fallback source serves) |
| `comment.ext.saves` | number\|null | Bookmark / save count for this comment, when the source reports it. On X this is `legacy.bookmark_count`. |
| `comment.ext.subreddit` | string\|null |  |
| `comment.ext.subreddit_subscribers` | number\|null |  |
| `comment.ext.text_original` | string\|null | (seen in a sample response) |
| `comment.ext.updated_at` | string\|null | (seen in a sample response) |
| `comment.ext.urn` | string\|null |  |
| `comment.ext.viewer_rating` | string\|null | (seen in a sample response) |
| `comment.ext.views` | number\|null | View count for this comment, when the source reports it. On X a reply is a tweet and the count is public on posts from ~2022 onward. |
| `comment.flags.deleted` | boolean | Whether the comment is tombstoned (always present, even when false) |
| `comment.flags.pinned` | boolean\|null | Pinned flag (null when platform does not surface) (on some endpoints only when the fallback source serves) |
| `comment.id` | string | Platform-specific comment ID (always a string) |
| `comment.parent_id` | string\|null | Parent comment ID for nested replies, or null for top-level comments |
| `comment.post_id` | string\|null | ID of the post this comment belongs to |
| `comment.published_at` | string\|number\|null | Comment creation timestamp as an ISO 8601 UTC string. When the upstream sent a Unix epoch it is converted here and the raw epoch is preserved under `comment.ext.published_at_epoch` for one deprecation cycle. |
| `comment.replies` | array\|null | Nested reply tree: array of child comments, each itself a full Comment object with its own `replies`. Populated on threaded platforms (Reddit); absent on flat-comment platforms, which thread only via `parent_id`. (seen in a sample response) |
| `comment.text` | string\|null | Comment body. Tombstone sentinels ([deleted] / [removed]) are collapsed to null upstream: customers never see them. |
| `comment.url` | string\|null | Direct URL to the comment on the source platform |
| `computed.labels_evidence` | object\|null | When 1, every labelled row also carries computed.labels_evidence.<preset> = { quote, sentence_index }: the sentence in the row that most clearly shows the label, copied verbatim. (with `label_evidence=1`) |
| `computed.labels.complaint` | object\|null | Each comment gains computed.labels with probabilities (0 to 1), so you choose the cut-off; a comment that could not be judged carries labels: null. |
| `computed.labels.injection` | object\|null | injection flags text that addresses an AI system and tries to direct it (flagged, p); it never drops or rewrites a row. (with `label=injection`) |
| `computed.labels.low_quality` | object\|null | Each comment gains computed.labels with probabilities (0 to 1), so you choose the cut-off; a comment that could not be judged carries labels: null. (with `label=low_quality`) |
| `computed.labels.purchase_intent` | object\|null | Each comment gains computed.labels with probabilities (0 to 1), so you choose the cut-off; a comment that could not be judged carries labels: null. |
| `computed.labels.question` | object\|null | Each comment gains computed.labels with probabilities (0 to 1), so you choose the cut-off; a comment that could not be judged carries labels: null. |
| `computed.labels.sentiment` | object\|null | Each comment gains computed.labels with probabilities (0 to 1), so you choose the cut-off; a comment that could not be judged carries labels: null. |
| `computed.labels.spam` | object\|null | Each comment gains computed.labels with probabilities (0 to 1), so you choose the cut-off; a comment that could not be judged carries labels: null. (with `label=spam`) |
| `computed.labels.toxic` | object\|null | Each comment gains computed.labels with probabilities (0 to 1), so you choose the cut-off; a comment that could not be judged carries labels: null. (with `label=toxic`) |
| `computed.language` | string\|null |  |
