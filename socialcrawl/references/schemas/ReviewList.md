# ReviewList fields

Every field the 26 field-mapped endpoints returning `ReviewList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `computed.labels_evidence` | object\|null | When 1, every labelled row also carries computed.labels_evidence.<preset> = { quote, sentence_index }: the sentence in the row that most clearly shows the label, copied verbatim. (with `label_evidence=1`) |
| `computed.labels.incentivized` | object\|null | incentivized: does the reviewer say they got the product free, discounted or rewarded for the review (p), and did the text carry a disclosure such as 'in exchange for my honest review', Vine or 체험단 (disclosed). (with `label=incentivized`) |
| `computed.labels.injection` | object\|null | injection flags text that addresses an AI system and tries to direct it (flagged, p); it never drops or rewrites a row. (with `label=injection`) |
| `computed.labels.issue` | object\|null | issue: the main problem the review reports (label: product_defect, sizing_or_fit, shipping_or_delivery, customer_service, price_or_value, missing_feature, other, or none, with confidence; label is null when unsure). |
| `computed.labels.reports` | object\|null | reports (needs reports=): does this review say that the thing you describe happened (p, 0 to 1). (with `label=reports`) |
| `computed.labels.sentiment` | object\|null | sentiment and issue are free when asked for too; reports, incentivized and injection add 1 credit per started 25 newly judged reviews. |
| `review.author.avatar_url` | string\|null | URL of the reviewer's avatar. (on some endpoints only when the fallback source serves) |
| `review.author.location` | string\|null | Where the reviewer says they are from. (on some endpoints only when the fallback source serves) |
| `review.author.name` | string\|null | Reviewer name. |
| `review.author.reviews_count` | number\|null | Number of reviews the reviewer has written. (on some endpoints only when the fallback source serves) |
| `review.author.url` | string\|null | URL of the reviewer's profile. |
| `review.entity_id` | string\|null | ID of the reviewed entity (e.g. the Amazon ASIN) |
| `review.ext.appdata.entity_id` | string | Id of the app the review is about. (seen in a sample response) |
| `review.ext.appdata.helpful_count` | unknown\|null | How many people found the review helpful. (seen in a sample response) |
| `review.ext.appdata.id` | string | The review's id in the store. (seen in a sample response) |
| `review.ext.appdata.position` | string | Where the row sits in the source's layout. (seen in a sample response) |
| `review.ext.appdata.rank_absolute` | number | Position among all rows. (seen in a sample response) |
| `review.ext.appdata.rank_group` | number | Position within the group. (seen in a sample response) |
| `review.ext.appdata.rating.rating_max` | number | The top of the scale. (seen in a sample response) |
| `review.ext.appdata.rating.rating_type` | string | The rating scale's label, such as `Max5`. (seen in a sample response) |
| `review.ext.appdata.rating.value` | number | The rating. (seen in a sample response) |
| `review.ext.appdata.rating.votes_count` | unknown\|null | How many ratings it is based on. (seen in a sample response) |
| `review.ext.appdata.responses` | array\|null | Developer replies to the review. (seen in a sample response) |
| `review.ext.appdata.review_text` | string | The review text. (seen in a sample response) |
| `review.ext.appdata.timestamp` | string | When the review was posted, ISO 8601. (seen in a sample response) |
| `review.ext.appdata.title` | unknown\|string\|null | The review's title. (seen in a sample response) |
| `review.ext.appdata.type` | string | The kind of row the source returned. (seen in a sample response) |
| `review.ext.appdata.user_profile.profile_image_url` | string\|unknown\|null | Link to the reviewer's picture. (seen in a sample response) |
| `review.ext.appdata.user_profile.profile_name` | string | The reviewer's name. (seen in a sample response) |
| `review.ext.appdata.version` | string\|null | App version the review was written for. (seen in a sample response) |
| `review.ext.naver` | object\|null | What a Naver visitor review carries beyond the shared fields. |
| `review.ext.room_type` | string\|null |  |
| `review.ext.stay_check_in` | string\|null |  |
| `review.ext.stay_check_out` | string\|null |  |
| `review.ext.stay_nights` | number\|null |  |
| `review.ext.tiktokshop.is_incentivized_review` | unknown | True when the reviewer was given an incentive. |
| `review.ext.tiktokshop.reviewer_id` | unknown | The reviewer's id. |
| `review.ext.tiktokshop.sku_specification` | unknown | The variant the reviewer bought. |
| `review.ext.traveler_type` | string\|null |  |
| `review.helpful_votes` | number\|null | Helpful-vote count (Amazon; null elsewhere) |
| `review.id` | string | Review ID (parsed from the review URL when not first-class) |
| `review.images` | array\|null | URLs of images attached to the review. |
| `review.language` | string\|null | Language code of the review text. |
| `review.original_language` | string\|null | Language the review was written in, when the text shown is a translation. |
| `review.published_at` | string\|number\|null | Review creation timestamp as an ISO 8601 UTC string (REL-07.6). Upstreams that send only a calendar date land on midnight UTC. When the upstream sent a Unix epoch it is converted here and the raw epoch is preserved under `review.ext.published_at_epoch`. |
| `review.rating.max` | number\|null | Highest possible rating value, normally 5. (on some endpoints only when the fallback source serves) |
| `review.rating.value` | number\|null | The rating the reviewer gave. |
| `review.responses` | array\|null | Owner/brand/management replies to the review, each `{id, author, text, published_at}` with `published_at` as an ISO 8601 UTC string (REL-07.6). |
| `review.source` | string\|null | Where the review was originally posted, as a provider name or retailer domain. |
| `review.text` | string\|null | Full review body |
| `review.title` | string\|null | Review headline. |
| `review.translated` | boolean\|null | Whether the text shown is a translation of the original. |
| `review.url` | string\|null | URL of the review. |
| `review.verified` | boolean\|null | Verified-purchase flag (Amazon; null elsewhere) |
