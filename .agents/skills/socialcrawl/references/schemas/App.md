# App fields

Every field the 2 field-mapped endpoints returning `App` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `app.category` | string\|null |  |
| `app.description` | string\|null |  |
| `app.developer.address` | string\|null |  |
| `app.developer.email` | string\|null |  |
| `app.developer.id` | string\|null |  |
| `app.developer.name` | string\|null |  |
| `app.developer.url` | string\|null |  |
| `app.developer.website` | string\|null |  |
| `app.icon` | string\|null |  |
| `app.id` | string | Store app ID (Google Play package name / App Store numeric id) |
| `app.minimum_os_version` | string\|null |  |
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
| `app.size` | string\|null |  |
| `app.store` | string | App marketplace ("google_play" or "app_store") |
| `app.subtitle` | string\|null |  |
| `app.title` | string\|null | App title |
| `app.update_notes` | string\|null |  |
| `app.updated_at` | string\|number\|null |  |
| `app.url` | string\|null |  |
| `app.version` | string\|null |  |
