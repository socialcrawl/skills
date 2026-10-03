# ReviewList fields

Every field the 22 field-mapped endpoints returning `ReviewList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `computed.labels_evidence` | object\|null | When 1, every labelled row also carries computed.labels_evidence.<preset> = { quote, sentence_index }: the sentence in the row that most clearly shows the label, copied verbatim. (with `label_evidence=1`) |
| `computed.labels.incentivized` | object\|null | incentivized: does the reviewer say they got the product free, discounted or rewarded for the review (p), and did the text carry a disclosure such as 'in exchange for my honest review', Vine or 체험단 (disclosed). (with `label=incentivized`) |
| `computed.labels.injection` | object\|null | injection flags text that addresses an AI system and tries to direct it (flagged, p); it never drops or rewrites a row. (with `label=injection`) |
| `computed.labels.issue` | object\|null | issue: the main problem the review reports (label: product_defect, sizing_or_fit, shipping_or_delivery, customer_service, price_or_value, missing_feature, other, or none, with confidence; label is null when unsure). |
| `computed.labels.reports` | object\|null | reports (needs reports=): does this review say that the thing you describe happened (p, 0 to 1). (with `label=reports`) |
| `computed.labels.sentiment` | object\|null | sentiment and issue are free when asked for too; reports, incentivized and injection add 1 credit per started 25 newly judged reviews. |
| `review.author.avatar_url` | string\|null |  |
| `review.author.location` | string\|null | (on some endpoints only when the fallback source serves) |
| `review.author.name` | string\|null |  |
| `review.author.reviews_count` | number\|null | (on some endpoints only when the fallback source serves) |
| `review.author.url` | string\|null |  |
| `review.entity_id` | string\|null | ID of the reviewed entity (e.g. the Amazon ASIN) |
| `review.ext.tiktokshop.is_incentivized_review` | unknown\|null |  |
| `review.ext.tiktokshop.reviewer_id` | unknown\|null |  |
| `review.ext.tiktokshop.sku_specification` | unknown\|null |  |
| `review.helpful_votes` | number\|null | Helpful-vote count (Amazon; null elsewhere) |
| `review.id` | string | Review ID (parsed from the review URL when not first-class) |
| `review.images` | array\|null |  |
| `review.language` | string\|null |  |
| `review.original_language` | string\|null |  |
| `review.published_at` | string\|number\|null | Review creation timestamp as an ISO 8601 UTC string (REL-07.6). Upstreams that send only a calendar date land on midnight UTC. When the upstream sent a Unix epoch it is converted here and the raw epoch is preserved under `review.ext.published_at_epoch`. |
| `review.rating.max` | number\|null | (on some endpoints only when the fallback source serves) |
| `review.rating.value` | number\|null |  |
| `review.responses` | array\|null | Owner/brand/management replies to the review, each `{id, author, text, published_at}` with `published_at` as an ISO 8601 UTC string (REL-07.6). |
| `review.source` | string\|null |  |
| `review.text` | string\|null | Full review body |
| `review.title` | string\|null |  |
| `review.translated` | boolean\|null |  |
| `review.url` | string\|null |  |
| `review.verified` | boolean\|null | Verified-purchase flag (Amazon; null elsewhere) |
