# WebPageList fields

Every field the 2 field-mapped endpoints returning `WebPageList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `page.answer` | unknown | The source's answer to a question about the page, when you asked for the `answer` format. Null otherwise. Its shape follows the format, so it has no single fixed shape. |
| `page.change_tracking` | unknown | What changed on the page since the last scrape of it, when you asked for the `changeTracking` format. Null otherwise. Its shape follows the format, so it has no single fixed shape. |
| `page.content.html` | string\|null | HTML body. |
| `page.content.markdown` | string\|null | Markdown body. |
| `page.content.raw_html` | string\|null | Raw HTML body. |
| `page.content.summary` | string\|null | Generated summary. |
| `page.description` | string\|null | The page description or search snippet, or null when there is none. |
| `page.extraction` | unknown\|null | Structured extraction result when requested. The schema you send decides its keys, so it has no fixed shape. On `web/extract` every value is checked against the page text: a placeholder such as 'Not specified', or a value the page does not state, comes back as null and is listed in `extraction_check.removed`. |
| `page.extraction_check.checked` | number | Non-null values examined. |
| `page.extraction_check.confirmed` | number | Values kept because a check found the page states them, for example in another language. |
| `page.extraction_check.found_in_text` | number | Values kept because they appear word for word on the page. |
| `page.extraction_check.removed` | array | Fields set to null, with the value the extractor gave. |
| `page.extraction_check.unverified` | array | Fields returned as extracted without a check. |
| `page.fetch.cache_state` | string\|null | Upstream cache state when reported. |
| `page.fetch.cached_at` | string\|null | Upstream cache timestamp when reported. |
| `page.fetch.proxy_tier` | string\|null | Proxy tier used for the fetch. |
| `page.fetched_at` | string\|null | Fetch timestamp when reported. |
| `page.final_url` | string\|null | Final resolved URL after redirects. |
| `page.highlights` | unknown | The passages the source picked out of the page, when you asked for the `highlights` format. Null otherwise. Its shape follows the format, so it has no single fixed shape. |
| `page.media.audio_url` | string\|null | Audio URL. |
| `page.media.screenshot_url` | string\|null | Screenshot URL when requested. |
| `page.media.video_url` | string\|null | Video URL. |
| `page.native.credits_used` | number | The credits that endpoint charged. |
| `page.native.endpoint` | string | The endpoint that read the page, such as `/v1/linkedin/profile`. |
| `page.page_count` | number\|null | How many pages of a document were read, or null when the source does not report it. |
| `page.published_at` | string\|null | When the page was published: an ISO 8601 instant, or a YYYY-MM-DD date when only the day is printed. From the page's own article:published_time meta tag on a scrape, and from the news date or that tag on a search row. Null when the page states none. |
| `page.scrape_id` | string\|null | Opaque scrape identifier for follow-up interactions. |
| `page.source_type` | string\|null | Which kind of result a search row is: `web`, `news` or `image`. Null when the result is not a search row. |
| `page.status_code` | number\|null | HTTP status code observed while fetching the page. |
| `page.title` | string\|null | The page title, or null when the page has none. Sent on search and map results and on a parsed document. |
| `page.total_page_count` | number\|null | How many pages the document has in all, or null when the source does not report it. |
| `page.url` | string | Requested URL. |
