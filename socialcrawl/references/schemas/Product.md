# Product fields

Every field the 15 field-mapped endpoints returning `Product` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `product.availability` | string\|null | Stock/availability string when surfaced |
| `product.brand` | string\|null | Brand name (cleaned). Null when the platform exposes a seller instead. |
| `product.description` | string\|null |  |
| `product.ext.aliexpress.category` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.commission_rate` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.discount` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.shop_url` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.subcategory` | string\|null | (seen in a sample response) |
| `product.ext.available_quantity` | number\|null | (seen in a sample response) |
| `product.ext.bought_past_month` | number\|null |  |
| `product.ext.catalog_id` | string\|null |  |
| `product.ext.condition` | string\|null | (seen in a sample response) |
| `product.ext.etsy.favorites` | number\|null | (seen in a sample response) |
| `product.ext.etsy.is_bestseller` | boolean\|null | (seen in a sample response) |
| `product.ext.etsy.is_top_rated` | boolean\|null | (seen in a sample response) |
| `product.ext.etsy.materials` | array\|null | (seen in a sample response) |
| `product.ext.etsy.taxonomy_path` | string\|null | (seen in a sample response) |
| `product.ext.etsy.user_id` | string\|null | (seen in a sample response) |
| `product.ext.etsy.when_made` | string\|null | (seen in a sample response) |
| `product.ext.g2.ai_verified` | boolean\|null | (seen in a sample response) |
| `product.ext.g2.alternatives` | array\|null | (seen in a sample response) |
| `product.ext.g2.categories` | array\|null | (seen in a sample response) |
| `product.ext.g2.comparisons` | array\|null | (seen in a sample response) |
| `product.ext.g2.cons` | array\|null | (seen in a sample response) |
| `product.ext.g2.cons_details` | array\|null | (seen in a sample response) |
| `product.ext.g2.detailed_features` | array\|null | (seen in a sample response) |
| `product.ext.g2.features` | array\|null | (seen in a sample response) |
| `product.ext.g2.g2_reviews_link` | string\|null | (seen in a sample response) |
| `product.ext.g2.integrations.count` | number\|null | (seen in a sample response) |
| `product.ext.g2.integrations.items` | array\|null | (seen in a sample response) |
| `product.ext.g2.pricing_details.alternatives_pricing` | array\|null | (seen in a sample response) |
| `product.ext.g2.pricing_details.faqs` | array\|null | (seen in a sample response) |
| `product.ext.g2.pricing_details.free_trial` | boolean\|null | (seen in a sample response) |
| `product.ext.g2.pricing_details.last_updated` | string\|null | (seen in a sample response) |
| `product.ext.g2.pricing_details.overview` | string\|null | (seen in a sample response) |
| `product.ext.g2.pricing_plans` | array\|null | (seen in a sample response) |
| `product.ext.g2.product_uuid` | string\|null | (seen in a sample response) |
| `product.ext.g2.pros` | array\|null | (seen in a sample response) |
| `product.ext.g2.pros_details` | array\|null | (seen in a sample response) |
| `product.ext.g2.solution_type` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.account_id` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.category` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.category_id` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.location` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.location_id` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.public_user_id` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.seller_type` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.user_id` | string\|null | (seen in a sample response) |
| `product.ext.model_number` | unknown\|null |  |
| `product.ext.rating_distribution.star_1` | number\|null | (seen in a sample response) |
| `product.ext.rating_distribution.star_2` | number\|null | (seen in a sample response) |
| `product.ext.rating_distribution.star_3` | number\|null | (seen in a sample response) |
| `product.ext.rating_distribution.star_4` | number\|null | (seen in a sample response) |
| `product.ext.rating_distribution.star_5` | number\|null | (seen in a sample response) |
| `product.ext.requested_id` | string\|null | (seen in a sample response) |
| `product.ext.seller_id` | string\|null |  |
| `product.ext.seller_reputation.detailed_ratings.accurate_description` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.detailed_ratings.communication` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.detailed_ratings.reasonable_shipping_cost` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.detailed_ratings.shipping_speed` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.feedback_count` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.feedback_percentage` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.items_sold` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.joined` | string\|null | (seen in a sample response) |
| `product.ext.seller_reputation.top_rated` | boolean\|null | (seen in a sample response) |
| `product.ext.seller_reputation.url` | string\|null | (seen in a sample response) |
| `product.ext.sephora.ingredients` | string\|null | (seen in a sample response) |
| `product.ext.sephora.loves_count` | number\|null | (seen in a sample response) |
| `product.ext.sephora.size` | string\|null | (seen in a sample response) |
| `product.ext.sephora.sku` | string\|null | (seen in a sample response) |
| `product.ext.sku_id` | string\|null |  |
| `product.ext.sold_count` | number\|null |  |
| `product.ext.store_inventory` | array\|null | (seen in a sample response) |
| `product.ext.tiktokshop` | object\|null |  |
| `product.ext.upc` | unknown\|null |  |
| `product.features` | array\|null |  |
| `product.id` | string | Platform product ID (Amazon ASIN / Google Shopping product id) |
| `product.image_urls` | string\|array\|null | Primary image URL, or an array of image URLs for products with a gallery. |
| `product.price.currency` | string\|null |  |
| `product.price.current` | number\|null |  |
| `product.price.original` | number\|null |  |
| `product.rating.average` | number\|null |  |
| `product.rating.count` | number\|null |  |
| `product.reviews_count` | number\|null |  |
| `product.seller` | string\|null |  |
| `product.specifications` | array\|null |  |
| `product.title` | string\|null | Product title |
| `product.url` | string\|null | Direct URL to the product page |
| `product.variations` | array\|null |  |
