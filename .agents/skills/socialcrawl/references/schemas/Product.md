# Product fields

Every field the 15 field-mapped endpoints returning `Product` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `product.availability` | string\|null | Stock/availability string when surfaced |
| `product.brand` | string\|null | Brand name (cleaned). Null when the platform exposes a seller instead. |
| `product.description` | string\|null | Product description. |
| `product.ext.aliexpress.category` | string | Top-level category. (seen in a sample response) |
| `product.ext.aliexpress.commission_rate` | string | Affiliate commission rate, such as `7.0%`. (seen in a sample response) |
| `product.ext.aliexpress.discount` | string | Discount, such as `49%`. (seen in a sample response) |
| `product.ext.aliexpress.shop_url` | string | Link to the seller's shop. (seen in a sample response) |
| `product.ext.aliexpress.subcategory` | string | Sub-category. (seen in a sample response) |
| `product.ext.available_quantity` | number\|null | Units the seller currently has listed. eBay only. (seen in a sample response) |
| `product.ext.bought_past_month` | number\|null | Lower bound of the purchase badge, for example 10000 for '10K+ bought in past month'. Null when there is no count. (only when the fallback source serves) |
| `product.ext.catalog_id` | string\|null | Walmart's alphanumeric catalog id. product.id holds the numeric id from the URL. |
| `product.ext.condition` | string\|null | Condition of a marketplace listing, for example Used or Open Box. (seen in a sample response) |
| `product.ext.etsy.favorites` | number | How many people favourited the item. (seen in a sample response) |
| `product.ext.etsy.is_bestseller` | boolean | True when Etsy marks the item a bestseller. (seen in a sample response) |
| `product.ext.etsy.is_top_rated` | boolean | True when Etsy marks the item top rated. (seen in a sample response) |
| `product.ext.etsy.materials` | array | Materials the item is made of. (seen in a sample response) |
| `product.ext.etsy.taxonomy_path` | string | Etsy's category path, dot-separated. (seen in a sample response) |
| `product.ext.etsy.user_id` | string | The seller's user id. (seen in a sample response) |
| `product.ext.etsy.when_made` | string | When the item was made, such as `made_to_order`. (seen in a sample response) |
| `product.ext.g2.ai_verified` | boolean | True when G2 verified the listing with AI. (seen in a sample response) |
| `product.ext.g2.alternatives` | array | Alternatives G2 suggests. (seen in a sample response) |
| `product.ext.g2.categories` | array | G2 categories the product is listed in. (seen in a sample response) |
| `product.ext.g2.comparisons` | array | Head-to-head comparisons G2 offers. (seen in a sample response) |
| `product.ext.g2.cons` | array | What reviewers dislike. (seen in a sample response) |
| `product.ext.g2.cons_details` | array | What reviewers dislike, with evidence. (seen in a sample response) |
| `product.ext.g2.detailed_features` | array | Feature groups with a description per feature. (seen in a sample response) |
| `product.ext.g2.features` | array | Feature groups. (seen in a sample response) |
| `product.ext.g2.g2_reviews_link` | string | Link to the product's reviews on G2. (seen in a sample response) |
| `product.ext.g2.integrations.count` | number | How many integrations G2 lists. (seen in a sample response) |
| `product.ext.g2.integrations.items` | array | The integrations shown. (seen in a sample response) |
| `product.ext.g2.pricing_details.alternatives_pricing` | array | Pricing of alternative products. (seen in a sample response) |
| `product.ext.g2.pricing_details.faqs` | array | Pricing questions and answers. (seen in a sample response) |
| `product.ext.g2.pricing_details.free_trial` | boolean | True when a free trial exists. (seen in a sample response) |
| `product.ext.g2.pricing_details.last_updated` | string | When the pricing was last updated, as text. (seen in a sample response) |
| `product.ext.g2.pricing_details.overview` | string | G2's summary of the pricing. (seen in a sample response) |
| `product.ext.g2.pricing_plans` | array | The product's pricing plans. (seen in a sample response) |
| `product.ext.g2.product_uuid` | string | G2's unique id for the product. (seen in a sample response) |
| `product.ext.g2.pros` | array | What reviewers like. (seen in a sample response) |
| `product.ext.g2.pros_details` | array | What reviewers like, with evidence. (seen in a sample response) |
| `product.ext.g2.solution_type` | string | Kind of solution, such as `All-in-One`. (seen in a sample response) |
| `product.ext.gumtree.account_id` | string | The seller's account id. (seen in a sample response) |
| `product.ext.gumtree.category` | string | The category's name. (seen in a sample response) |
| `product.ext.gumtree.category_id` | string | The category's id. (seen in a sample response) |
| `product.ext.gumtree.location` | string | Where the item is. (seen in a sample response) |
| `product.ext.gumtree.location_id` | string | The location's id. (seen in a sample response) |
| `product.ext.gumtree.public_user_id` | string | The seller's public id. (seen in a sample response) |
| `product.ext.gumtree.seller_type` | string | Kind of seller, such as `trade`. (seen in a sample response) |
| `product.ext.gumtree.user_id` | string | The seller's user id. (seen in a sample response) |
| `product.ext.model_number` | unknown\|null |  |
| `product.ext.rating_distribution.star_1` | number\|null | Reviews that gave 1 star. (seen in a sample response) |
| `product.ext.rating_distribution.star_2` | number\|null | Reviews that gave 2 stars. (seen in a sample response) |
| `product.ext.rating_distribution.star_3` | number\|null | Reviews that gave 3 stars. (seen in a sample response) |
| `product.ext.rating_distribution.star_4` | number\|null | Reviews that gave 4 stars. (seen in a sample response) |
| `product.ext.rating_distribution.star_5` | number\|null | Reviews that gave 5 stars. (seen in a sample response) |
| `product.ext.requested_id` | string\|null | The id you asked for, when the retailer rolled a variant up to its parent. Set only when it differs from product.id. (seen in a sample response) |
| `product.ext.seller_id` | string\|null | The seller's id on the retailer. |
| `product.ext.seller_reputation.detailed_ratings.accurate_description` | number\|null | Score for how accurately listings describe the item, up to 5. (seen in a sample response) |
| `product.ext.seller_reputation.detailed_ratings.communication` | number\|null | Score for the seller's communication, up to 5. (seen in a sample response) |
| `product.ext.seller_reputation.detailed_ratings.reasonable_shipping_cost` | number\|null | Score for how reasonable shipping costs are, up to 5. (seen in a sample response) |
| `product.ext.seller_reputation.detailed_ratings.shipping_speed` | number\|null | Score for shipping speed, up to 5. (seen in a sample response) |
| `product.ext.seller_reputation.feedback_count` | number\|null | Lifetime number of feedback ratings the seller received. (seen in a sample response) |
| `product.ext.seller_reputation.feedback_percentage` | number\|null | Share of the seller's feedback that is positive, as a percentage. (seen in a sample response) |
| `product.ext.seller_reputation.items_sold` | number\|null | Items the seller has sold. (seen in a sample response) |
| `product.ext.seller_reputation.joined` | string\|null | When the seller joined the marketplace, as the marketplace prints it. (seen in a sample response) |
| `product.ext.seller_reputation.top_rated` | boolean\|null | Whether the marketplace gives the seller its top rated status. (seen in a sample response) |
| `product.ext.seller_reputation.url` | string\|null | URL of the seller's page. (seen in a sample response) |
| `product.ext.sephora.ingredients` | string | The ingredient list as printed. (seen in a sample response) |
| `product.ext.sephora.loves_count` | number | How many shoppers loved the product. (seen in a sample response) |
| `product.ext.sephora.size` | string | Size or volume, such as `3.3 oz/100 mL`. (seen in a sample response) |
| `product.ext.sephora.sku` | string | The SKU. (seen in a sample response) |
| `product.ext.sku_id` | string\|null | Colour or size variant id. Shipping quotes need it beside the product id. |
| `product.ext.sold_count` | number\|null | Units sold, as the listing reports it. |
| `product.ext.store_inventory` | array\|null | Stock at individual stores or fulfilment points. (seen in a sample response) |
| `product.ext.tiktokshop` | object\|null | TikTok Shop detail. |
| `product.ext.tiktokshop.delivery_days_max` | unknown\|null | Most days delivery takes. (with `include=details`) |
| `product.ext.tiktokshop.delivery_days_min` | unknown\|null | Fewest days delivery takes. (with `include=details`) |
| `product.ext.tiktokshop.delivery_estimate` | unknown\|null | Estimated delivery window, as text. (with `include=details`) |
| `product.ext.tiktokshop.free_shipping` | unknown\|null | True when shipping is free. (with `include=details`) |
| `product.ext.tiktokshop.shipping_fee` | unknown\|null | Shipping fee. (with `include=details`) |
| `product.ext.tiktokshop.shop_identity` | unknown\|null | Kind of shop, such as `official`. (with `include=details`) |
| `product.ext.upc` | unknown\|null |  |
| `product.features` | array\|null | Feature bullet points from the product page. Detail only. |
| `product.id` | string | Platform product ID (Amazon ASIN / Google Shopping product id) |
| `product.image_urls` | string\|array\|null | Primary image URL, or an array of image URLs for products with a gallery. |
| `product.price.currency` | string\|null | Currency code of the price. |
| `product.price.current` | number\|null | Current price, in the price currency. |
| `product.price.original` | number\|null | Price before any discount, in the price currency. |
| `product.rating.average` | number\|null | Average rating, normally out of 5. |
| `product.rating.count` | number\|null | Number of ratings behind the average. |
| `product.reviews_count` | number\|null | Number of written reviews. |
| `product.seller` | string\|null | Name of the seller. Null where the source names none. |
| `product.specifications` | array\|null | Specification rows from the product page. Detail only. (with `include=details` on some endpoints) |
| `product.title` | string\|null | Product title |
| `product.url` | string\|null | Direct URL to the product page |
| `product.variations` | array\|null | Other variants of the product, such as colour or size. Detail only. |
