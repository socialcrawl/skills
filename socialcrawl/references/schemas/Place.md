# Place fields

Every field the 9 field-mapped endpoints returning `Place` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `place.address` | string\|null |  |
| `place.categories` | array\|null |  |
| `place.category` | string\|null | Primary category (e.g. "Coffee shop", "Hotel") |
| `place.description` | string\|null |  |
| `place.hotel.amenities` | array\|null |  |
| `place.hotel.check_in_time` | string\|null |  |
| `place.hotel.check_out_time` | string\|null |  |
| `place.hotel.prices` | array\|null |  |
| `place.hotel.review_topics` | array\|null |  |
| `place.hotel.stars` | number\|null |  |
| `place.hotel.stars_description` | string\|null |  |
| `place.id` | string | Place ID (Google cid for a business, hotel_identifier for a hotel) |
| `place.image_urls` | string\|array\|null |  |
| `place.latitude` | number\|null |  |
| `place.longitude` | number\|null |  |
| `place.name` | string\|null | Business / hotel name |
| `place.phone` | string\|null |  |
| `place.price_level` | string\|null | Price band ("inexpensive" / "$$" / null) |
| `place.rating.max` | number\|null |  |
| `place.rating.value` | number\|null |  |
| `place.reviews_count` | number\|null | Number of ratings |
| `place.url` | string\|null | Website or canonical URL |
| `place.verified` | boolean\|null | Claimed-business flag (Google is_claimed) |
