# AppList fields

Every field the 6 field-mapped endpoints returning `AppList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `app.advisories` | array\|null | Apple age/content advisories (null on Google) (seen in a sample response) |
| `app.categories` | array\|null | Extra categories the app is listed under. App Store only. (seen in a sample response) |
| `app.category` | string\|null | The app's main store category. |
| `app.description` | string\|null | Full store description. Present on app detail, null on search and chart rows. |
| `app.developer.address` | string\|null | Postal address the developer published. Google Play only. |
| `app.developer.email` | string\|null | Contact email the developer published. Google Play only. |
| `app.developer.id` | string\|null | The store's id for the developer. |
| `app.developer.name` | string\|null | Developer or publisher name. |
| `app.developer.url` | string\|null | URL of the developer's page in the store. |
| `app.developer.website` | string\|null | The developer's own website. Google Play only. |
| `app.ext.appdata.advisories` | array | Content advisories, such as age ratings. (seen in a sample response) |
| `app.ext.appdata.app_id` | string | The app's id in the store. (seen in a sample response) |
| `app.ext.appdata.categories` | array\|unknown\|null | All categories the app is in. (seen in a sample response) |
| `app.ext.appdata.category_drift_probe` | boolean | An internal consistency marker the source row can carry. It has no meaning for callers and can be ignored. (seen in a sample response) |
| `app.ext.appdata.description` | string | The app's description. (seen in a sample response) |
| `app.ext.appdata.developer` | string | The developer's name. (seen in a sample response) |
| `app.ext.appdata.developer_address` | string | The developer's postal address, as the store lists it. (seen in a sample response) |
| `app.ext.appdata.developer_email` | string | The developer's contact email, as the store lists it. (seen in a sample response) |
| `app.ext.appdata.developer_id` | string | The developer's id in the store. (seen in a sample response) |
| `app.ext.appdata.developer_url` | unknown\|string\|null | Link to the developer's store page. (seen in a sample response) |
| `app.ext.appdata.developer_website` | string | The developer's own website. (seen in a sample response) |
| `app.ext.appdata.genres` | array | Genres the app is listed under. (seen in a sample response) |
| `app.ext.appdata.icon` | string | Link to the app's icon. (seen in a sample response) |
| `app.ext.appdata.images` | array | Links to the app's screenshots. (seen in a sample response) |
| `app.ext.appdata.installs` | string | Install band, such as `1,000,000,000+`. (seen in a sample response) |
| `app.ext.appdata.installs_count` | number | Install count as a number. (seen in a sample response) |
| `app.ext.appdata.is_free` | boolean | True when the app is free. (seen in a sample response) |
| `app.ext.appdata.languages` | array | Languages the app supports. (seen in a sample response) |
| `app.ext.appdata.last_update_date` | string | Last update date, ISO 8601. (seen in a sample response) |
| `app.ext.appdata.main_category` | string\|unknown\|null | The app's main category. (seen in a sample response) |
| `app.ext.appdata.minimum_os_version` | string\|null | Minimum OS version required. (seen in a sample response) |
| `app.ext.appdata.more_apps_by_developer` | array\|null | Other apps by the same developer. (seen in a sample response) |
| `app.ext.appdata.position` | string | Where the row sits in the source's layout. (seen in a sample response) |
| `app.ext.appdata.price.currency` | string | ISO 4217 currency code. (seen in a sample response) |
| `app.ext.appdata.price.current` | number | Current price. (seen in a sample response) |
| `app.ext.appdata.price.displayed_price` | unknown\|null | Price as displayed. (seen in a sample response) |
| `app.ext.appdata.price.is_price_range` | boolean | True when the price is a range. (seen in a sample response) |
| `app.ext.appdata.price.max_value` | unknown\|null | Top of the price range. (seen in a sample response) |
| `app.ext.appdata.price.regular` | unknown\|null | Regular price. (seen in a sample response) |
| `app.ext.appdata.rank_absolute` | number | Position among all rows. (seen in a sample response) |
| `app.ext.appdata.rank_group` | number | Position within the group. (seen in a sample response) |
| `app.ext.appdata.rating.rating_max` | number | The top of the scale. (seen in a sample response) |
| `app.ext.appdata.rating.rating_type` | string | The rating scale's label, such as `Max5`. (seen in a sample response) |
| `app.ext.appdata.rating.value` | number | The rating. (seen in a sample response) |
| `app.ext.appdata.rating.votes_count` | unknown\|number\|null | How many ratings it is based on. (seen in a sample response) |
| `app.ext.appdata.released_date` | string\|unknown\|null | First release date, ISO 8601. (seen in a sample response) |
| `app.ext.appdata.reviews_count` | unknown\|number\|null | How many reviews the app has. (seen in a sample response) |
| `app.ext.appdata.similar_apps` | array | Apps the store suggests as similar. (seen in a sample response) |
| `app.ext.appdata.size` | unknown\|string\|null | Download size, such as `287.4 MB`. (seen in a sample response) |
| `app.ext.appdata.tags` | array | Tags and chart badges the store shows. (seen in a sample response) |
| `app.ext.appdata.title` | string | The app's name. (seen in a sample response) |
| `app.ext.appdata.type` | string | The kind of row the source returned. (seen in a sample response) |
| `app.ext.appdata.update_notes` | string\|null | Release notes of the latest version. (seen in a sample response) |
| `app.ext.appdata.url` | string | Link to the app's store page. (seen in a sample response) |
| `app.ext.appdata.version` | string\|null | Current version. (seen in a sample response) |
| `app.ext.appdata.videos` | array\|null | Links to the app's preview videos. (seen in a sample response) |
| `app.genres` | array\|null | Google Play genres (null on Apple) (seen in a sample response) |
| `app.icon` | string\|null | URL of the app icon. |
| `app.id` | string | Store app ID (Google Play package name / App Store numeric id) |
| `app.image_urls` | array\|null | Screenshot URLs (seen in a sample response) |
| `app.installs` | object\|null | Install signal (Google only): { display "1,000,000,000+", count }; null on Apple (seen in a sample response) |
| `app.installs.count` | number\|null | Install count as a number. Google Play only, null on the App Store. (seen in a sample response) |
| `app.installs.display` | string\|null | Install count as the store prints it, for example '1,000,000,000+'. Google Play only. (seen in a sample response) |
| `app.languages` | array\|null | Languages the app supports. App Store only. (seen in a sample response) |
| `app.minimum_os_version` | string\|null | Lowest operating system version the app runs on. |
| `app.more_by_developer` | array\|null | Other apps from the same developer. (seen in a sample response) |
| `app.price.currency` | string\|null | Currency code of the price. Often null on the App Store. |
| `app.price.current` | number\|null | Current price in the price currency. 0 for a free app. |
| `app.price.displayed` | string\|null | Price exactly as the store shows it, for example '$4.99' or 'Free'. |
| `app.price.is_free` | boolean\|null | Whether the app is free to download. |
| `app.price.original` | number\|null | Regular price before any discount, in the price currency. |
| `app.rating.count` | number\|null | How many ratings the average is based on. |
| `app.rating.max` | number\|null | Highest possible rating value, normally 5. |
| `app.rating.value` | number\|null | Average rating from 0 to the rating max. |
| `app.released_at` | string\|number\|null | When the app was first released. A date string or an epoch number as the store gives it, and null when the store does not say, which is always the case on the App Store. |
| `app.reviews_count` | number\|null | Number of written reviews. |
| `app.similar_apps` | array\|null | Apps the store lists as similar. (seen in a sample response) |
| `app.size` | string\|null | Download size as the store prints it. |
| `app.store` | string | App marketplace ("google_play" or "app_store") |
| `app.subtitle` | string\|null | App Store marketing subtitle under the app name. Absent on Google Play. |
| `app.tags` | array\|null | Chart tags the store attaches to the app. Google Play only. (seen in a sample response) |
| `app.title` | string\|null | App title |
| `app.update_notes` | string\|null | The 'what's new' text of the latest release. |
| `app.updated_at` | string\|number\|null | When the latest version was published. A date string or an epoch number as the store gives it, and null when the store does not say. |
| `app.url` | string\|null | URL of the app's store page. |
| `app.version` | string\|null | Latest version string. |
| `app.video_urls` | array\|null | Preview video URLs from the store page. Google Play only. (seen in a sample response) |
