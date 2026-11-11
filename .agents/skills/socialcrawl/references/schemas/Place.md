# Place fields

Every field the 13 field-mapped endpoints returning `Place` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `place.address` | string\|null | Street address as the source prints it. |
| `place.categories` | array\|null | Additional categories beyond the primary one. |
| `place.category` | string\|null | Primary category (e.g. "Coffee shop", "Hotel") |
| `place.description` | string\|null | Description of the place. |
| `place.ext.blog_reviews_count` | number\|null | Number of blog reviews. Naver only. |
| `place.ext.booking_url` | string\|null | URL to book at the place. |
| `place.ext.business_username` | string\|null | `/v1/instagram/location` only: the username of the Instagram business account linked to the place, or null when none is linked. |
| `place.ext.capacity` | number\|null |  |
| `place.ext.category_ratings` | array\|null |  |
| `place.ext.city` | string\|null | City part of the address as Google publishes it. |
| `place.ext.country_code` | string\|null | Country as an ISO 3166-1 alpha-2 code. |
| `place.ext.exact_location` | boolean\|null |  |
| `place.ext.facebook_places_id` | string\|null | `/v1/instagram/location` only: the Facebook Places id of the same place. |
| `place.ext.host_profile` | object\|null |  |
| `place.ext.hours` | array\|null | Opening hours by day. |
| `place.ext.keywords` | array\|null | Keywords the place is tagged with. Naver only. |
| `place.ext.languages_spoken` | array\|null |  |
| `place.ext.listing_price_note` | string\|null |  |
| `place.ext.place_id` | string\|null | Google Maps place id (ChIJ...). place.id holds the cid. (seen in a sample response) |
| `place.ext.postal_code` | string\|null | Postal code part of the address. |
| `place.ext.posts_count` | number\|null | `/v1/instagram/location` only: the number of public posts Instagram counts at the place. |
| `place.ext.rating_distribution.1` | number\|null | (seen in a sample response) |
| `place.ext.rating_distribution.2` | number\|null | (seen in a sample response) |
| `place.ext.rating_distribution.3` | number\|null | (seen in a sample response) |
| `place.ext.rating_distribution.4` | number\|null | (seen in a sample response) |
| `place.ext.rating_distribution.5` | number\|null | (seen in a sample response) |
| `place.ext.room_type` | string\|null |  |
| `place.ext.rooms` | array\|null |  |
| `place.ext.status` | string\|null | Open or closed status as the source words it, for example Open. |
| `place.ext.status_description` | string\|null | The line under status, for example the next opening time. Naver only. |
| `place.ext.timezone` | string\|null | IANA timezone of the place, for example America/New_York. (seen in a sample response) |
| `place.ext.visitor_reviews_count` | number\|null | Number of visitor reviews. Naver only. |
| `place.ext.website` | string\|null | `/v1/instagram/location` only: the venue's own website (`place.url` is its Instagram page). |
| `place.hotel.amenities` | array\|null | Amenities the hotel lists. |
| `place.hotel.check_in_time` | string\|null | Check in time as the hotel prints it. |
| `place.hotel.check_out_time` | string\|null | Check out time as the hotel prints it. |
| `place.hotel.prices` | array\|null | Prices offered by booking sites for the hotel. |
| `place.hotel.review_topics` | array\|null | Topics guests mention most in reviews. |
| `place.hotel.stars` | number\|null | Hotel star classification, from 1 to 5. |
| `place.hotel.stars_description` | string\|null | The star classification as text, for example '4-star hotel'. |
| `place.id` | string | Place ID (Google cid for a business, hotel_identifier for a hotel) |
| `place.image_urls` | string\|array\|null | Image URL, or a list of image URLs, for the place. |
| `place.latitude` | number\|null | Latitude in decimal degrees. |
| `place.longitude` | number\|null | Longitude in decimal degrees. |
| `place.name` | string\|null | Business / hotel name |
| `place.phone` | string\|null | Phone number as the source prints it. |
| `place.price_level` | string\|null | Price band ("inexpensive" / "$$" / null) |
| `place.rating.max` | number\|null | Highest possible rating value, normally 5. |
| `place.rating.value` | number\|null | Average rating from 0 to the rating max. |
| `place.reviews_count` | number\|null | Number of ratings |
| `place.url` | string\|null | Website or canonical URL |
| `place.verified` | boolean\|null | Claimed-business flag (Google is_claimed) |
