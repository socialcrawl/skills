# PlaceList fields

Every field the 25 field-mapped endpoints returning `PlaceList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `place.address` | string\|null | Street address as the source prints it. |
| `place.categories` | array\|null | Additional categories beyond the primary one. |
| `place.category` | string\|null | Primary category (e.g. "Coffee shop", "Hotel") |
| `place.description` | string\|null | Description of the place. |
| `place.ext.ad_description` | string\|null | Description text of a paid slot. Naver only. |
| `place.ext.ad_rank` | number\|null | 1-based position among the paid slots. Naver only. |
| `place.ext.address_parts` | object\|null | On GET /v1/apple_maps/places: the address below the street line (street, neighbourhood, districts, areas of interest, county, country). |
| `place.ext.amenities` | array\|null | On GET /v1/apple_maps/places: the amenities the place lists, such as Free Wi-Fi or Wheelchair Accessible. |
| `place.ext.apartments` | object\|null |  |
| `place.ext.blog_reviews_count` | number\|null | Number of blog reviews. Naver only. |
| `place.ext.booking_url` | string\|null | URL to book at the place. |
| `place.ext.category_ids` | array\|null | On GET /v1/apple_maps/places: Apple's own category ids for the place, for example espresso_bar. |
| `place.ext.category_ratings` | array\|null |  |
| `place.ext.city` | string\|null | City part of the address as Google publishes it. |
| `place.ext.country_code` | string\|null | Country as an ISO 3166-1 alpha-2 code. |
| `place.ext.diets` | array\|null | A restaurant's dietary options as Tripadvisor lists them, for example Vegetarian friendly or Gluten free options. |
| `place.ext.distance` | number\|null | Distance from the searched location, in the source's own unit (miles for Target stores, metres for Naver). |
| `place.ext.domain` | string\|null | Domain of the business website, for example www.example.it. (seen in a sample response) |
| `place.ext.guides` | array\|null | On GET /v1/apple_maps/places: the editorial Apple Maps guides the place appears in, with how many places each lists. |
| `place.ext.hours` | array\|null | Opening hours by day. (seen in a sample response) |
| `place.ext.is_ad` | boolean\|null | True for a paid slot: a Naver 플레이스 광고 slot (such a row has no organic rank), or a sponsored Yelp search result (yelp/search and search/full with ads=true). Null or absent on regular rows. |
| `place.ext.listing` | object\|null |  |
| `place.ext.listing_badges` | array\|null |  |
| `place.ext.listing_price_note` | string\|null |  |
| `place.ext.maps_url` | string\|null | Google Maps link for the place, built from its cid. (seen in a sample response) |
| `place.ext.meal_types` | array\|null | The meals a restaurant serves as Tripadvisor lists them, for example Lunch or Dinner. |
| `place.ext.menu_url` | string\|null | URL of the place's menu. |
| `place.ext.order_url` | string\|null | On GET /v1/apple_maps/places: where to order from the place online. |
| `place.ext.photos` | array\|null | On GET /v1/apple_maps/places: each photo with its category (for example Food & Drink) and who supplied it. |
| `place.ext.place_id` | string\|null | Google Maps place id (ChIJ...). place.id holds the cid. (seen in a sample response) |
| `place.ext.postal_code` | string\|null | Postal code part of the address. |
| `place.ext.pro_desk_phone` | string\|null |  |
| `place.ext.rank` | number\|null | 1-based position of the place in the result list. |
| `place.ext.rating_distribution.1` | number\|null | (seen in a sample response) |
| `place.ext.rating_distribution.2` | number\|null | (seen in a sample response) |
| `place.ext.rating_distribution.3` | number\|null | (seen in a sample response) |
| `place.ext.rating_distribution.4` | number\|null | (seen in a sample response) |
| `place.ext.rating_distribution.5` | number\|null | (seen in a sample response) |
| `place.ext.rating_source` | string\|null | On the apple_maps endpoints: who gave place.rating, Apple (0 to 100) or a partner such as Yelp (5 stars); place.rating.max carries the scale. |
| `place.ext.region` | string\|null | Region part of the address as Google publishes it. |
| `place.ext.review_snippets` | array\|null | On GET /v1/apple_maps/search and /v1/apple_maps/places: short review excerpts shown with the place (id, text, rating, date, and who wrote it; on places also the excerpt's link), from the reviews behind its rating. |
| `place.ext.status` | string\|null | Open or closed status as the source words it, for example Open. |
| `place.ext.status_description` | string\|null | The line under status, for example the next opening time. Naver only. |
| `place.ext.subtitle` | string\|null |  |
| `place.ext.timezone` | string\|null | IANA timezone of the place, for example America/New_York. |
| `place.ext.tool_rental_phone` | string\|null |  |
| `place.ext.visitor_reviews_count` | number\|null | Number of visitor reviews. Naver only. |
| `place.ext.website` | string\|null | `/v1/instagram/location` only: the venue's own website (`place.url` is its Instagram page). |
| `place.ext.weekly_hours` | object\|null | On the apple_maps endpoints: opening hours by weekday (monday to sunday), each day a list of ranges such as 07:00 - 19:00 in the place's own time zone. |
| `place.ext.yelp_id` | string\|null | On GET /v1/apple_maps/search: the same place's Yelp id, which GET /v1/yelp/business/info and /v1/yelp/business/reviews take. |
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
| `place.url` | string\|null | Website or canonical URL (on some endpoints only when the fallback source serves) |
| `place.verified` | boolean\|null | Claimed-business flag (Google is_claimed) |
