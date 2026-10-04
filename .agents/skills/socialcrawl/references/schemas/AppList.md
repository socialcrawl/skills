# AppList fields

Every field the 6 field-mapped endpoints returning `AppList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `app.advisories` | array\|null | Apple age/content advisories (null on Google) (seen in a sample response) |
| `app.categories` | array\|null | (seen in a sample response) |
| `app.category` | string\|null |  |
| `app.description` | string\|null |  |
| `app.developer.address` | string\|null |  |
| `app.developer.email` | string\|null |  |
| `app.developer.id` | string\|null |  |
| `app.developer.name` | string\|null |  |
| `app.developer.url` | string\|null |  |
| `app.developer.website` | string\|null |  |
| `app.ext.appdata.advisories` | array\|null | (seen in a sample response) |
| `app.ext.appdata.app_id` | string\|null | (seen in a sample response) |
| `app.ext.appdata.categories` | array\|unknown\|null | (seen in a sample response) |
| `app.ext.appdata.category_drift_probe` | boolean\|null | (seen in a sample response) |
| `app.ext.appdata.description` | string\|null | (seen in a sample response) |
| `app.ext.appdata.developer` | string\|null | (seen in a sample response) |
| `app.ext.appdata.developer_address` | string\|null | (seen in a sample response) |
| `app.ext.appdata.developer_email` | string\|null | (seen in a sample response) |
| `app.ext.appdata.developer_id` | string\|null | (seen in a sample response) |
| `app.ext.appdata.developer_url` | unknown\|string\|null | (seen in a sample response) |
| `app.ext.appdata.developer_website` | string\|null | (seen in a sample response) |
| `app.ext.appdata.genres` | array\|null | (seen in a sample response) |
| `app.ext.appdata.icon` | string\|null | (seen in a sample response) |
| `app.ext.appdata.images` | array\|null | (seen in a sample response) |
| `app.ext.appdata.installs` | string\|null | (seen in a sample response) |
| `app.ext.appdata.installs_count` | number\|null | (seen in a sample response) |
| `app.ext.appdata.is_free` | boolean\|null | (seen in a sample response) |
| `app.ext.appdata.languages` | array\|null | (seen in a sample response) |
| `app.ext.appdata.last_update_date` | string\|null | (seen in a sample response) |
| `app.ext.appdata.main_category` | string\|unknown\|null | (seen in a sample response) |
| `app.ext.appdata.minimum_os_version` | string\|null | (seen in a sample response) |
| `app.ext.appdata.more_apps_by_developer` | array\|null | (seen in a sample response) |
| `app.ext.appdata.position` | string\|null | (seen in a sample response) |
| `app.ext.appdata.price.currency` | string\|null | (seen in a sample response) |
| `app.ext.appdata.price.current` | number\|null | (seen in a sample response) |
| `app.ext.appdata.price.displayed_price` | unknown\|null | (seen in a sample response) |
| `app.ext.appdata.price.is_price_range` | boolean\|null | (seen in a sample response) |
| `app.ext.appdata.price.max_value` | unknown\|null | (seen in a sample response) |
| `app.ext.appdata.price.regular` | unknown\|null | (seen in a sample response) |
| `app.ext.appdata.rank_absolute` | number\|null | (seen in a sample response) |
| `app.ext.appdata.rank_group` | number\|null | (seen in a sample response) |
| `app.ext.appdata.rating.rating_max` | number\|null | (seen in a sample response) |
| `app.ext.appdata.rating.rating_type` | string\|null | (seen in a sample response) |
| `app.ext.appdata.rating.value` | number\|null | (seen in a sample response) |
| `app.ext.appdata.rating.votes_count` | unknown\|number\|null | (seen in a sample response) |
| `app.ext.appdata.released_date` | string\|unknown\|null | (seen in a sample response) |
| `app.ext.appdata.reviews_count` | unknown\|number\|null | (seen in a sample response) |
| `app.ext.appdata.similar_apps` | array\|null | (seen in a sample response) |
| `app.ext.appdata.size` | unknown\|string\|null | (seen in a sample response) |
| `app.ext.appdata.tags` | array\|null | (seen in a sample response) |
| `app.ext.appdata.title` | string\|null | (seen in a sample response) |
| `app.ext.appdata.type` | string\|null | (seen in a sample response) |
| `app.ext.appdata.update_notes` | string\|null | (seen in a sample response) |
| `app.ext.appdata.url` | string\|null | (seen in a sample response) |
| `app.ext.appdata.version` | string\|null | (seen in a sample response) |
| `app.ext.appdata.videos` | array\|null | (seen in a sample response) |
| `app.genres` | array\|null | Google Play genres (null on Apple) (seen in a sample response) |
| `app.icon` | string\|null |  |
| `app.id` | string | Store app ID (Google Play package name / App Store numeric id) |
| `app.image_urls` | array\|null | Screenshot URLs (seen in a sample response) |
| `app.installs` | object\|null | Install signal (Google only): { display "1,000,000,000+", count }; null on Apple (seen in a sample response) |
| `app.installs.count` | number\|null | (seen in a sample response) |
| `app.installs.display` | string\|null | (seen in a sample response) |
| `app.languages` | array\|null | (seen in a sample response) |
| `app.minimum_os_version` | string\|null |  |
| `app.more_by_developer` | array\|null | (seen in a sample response) |
| `app.price.currency` | string\|null |  |
| `app.price.current` | number\|null |  |
| `app.price.displayed` | string\|null |  |
| `app.price.is_free` | boolean\|null |  |
| `app.price.original` | number\|null |  |
| `app.rating.count` | number\|null |  |
| `app.rating.max` | number\|null |  |
| `app.rating.value` | number\|null |  |
| `app.released_at` | string\|number\|null |  |
| `app.reviews_count` | number\|null |  |
| `app.similar_apps` | array\|null | (seen in a sample response) |
| `app.size` | string\|null |  |
| `app.store` | string | App marketplace ("google_play" or "app_store") |
| `app.subtitle` | string\|null |  |
| `app.tags` | array\|null | (seen in a sample response) |
| `app.title` | string\|null | App title |
| `app.update_notes` | string\|null |  |
| `app.updated_at` | string\|number\|null |  |
| `app.url` | string\|null |  |
| `app.version` | string\|null |  |
| `app.video_urls` | array\|null | (seen in a sample response) |
