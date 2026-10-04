# ProductList fields

Every field the 34 field-mapped endpoints returning `ProductList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `product.availability` | string\|null | Stock/availability string when surfaced (on some endpoints only when the fallback source serves) |
| `product.brand` | string\|null | Brand name (cleaned). Null when the platform exposes a seller instead. (on some endpoints only when the fallback source serves) |
| `product.description` | string\|null | (on some endpoints only when the fallback source serves) |
| `product.ext.aliexpress.category` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.commission_rate` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.discount` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.positive_rate` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.shop_url` | string\|null | (seen in a sample response) |
| `product.ext.aliexpress.subcategory` | string\|null | (seen in a sample response) |
| `product.ext.availability_type` | unknown\|null |  |
| `product.ext.available_quantity` | number\|null | (seen in a sample response) |
| `product.ext.bought_past_month` | number\|null | (only when the fallback source serves) |
| `product.ext.bought_past_month_label` | string\|null |  |
| `product.ext.buying_format` | string\|null | (seen in a sample response) |
| `product.ext.catalog_id` | string\|null |  |
| `product.ext.condition` | string\|null | (seen in a sample response) |
| `product.ext.data_docid` | string\|null | (seen in a sample response) |
| `product.ext.department` | unknown\|null |  |
| `product.ext.etsy.is_handmade` | boolean\|null | (seen in a sample response) |
| `product.ext.gid` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.category` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.category_id` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.location` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.location_id` | string\|null | (seen in a sample response) |
| `product.ext.gumtree.seller_type` | string\|null | (seen in a sample response) |
| `product.ext.hm.category_code` | string\|null | (seen in a sample response) |
| `product.ext.hm.color` | string\|null | (seen in a sample response) |
| `product.ext.hm.new_arrival` | boolean\|null | (seen in a sample response) |
| `product.ext.hm.sizes` | array\|null | (seen in a sample response) |
| `product.ext.kohls.colors` | array\|null | (seen in a sample response) |
| `product.ext.kohls.coupon_eligible` | boolean\|null | (seen in a sample response) |
| `product.ext.kohls.display_color` | string\|null | (seen in a sample response) |
| `product.ext.kohls.ship` | boolean\|null | (seen in a sample response) |
| `product.ext.kohls.sku` | string\|null | (seen in a sample response) |
| `product.ext.model_number` | unknown\|null |  |
| `product.ext.promotion.amount_off` | number\|null | (seen in a sample response) |
| `product.ext.promotion.label` | string\|null | (seen in a sample response) |
| `product.ext.promotion.percent_off` | number\|null | (seen in a sample response) |
| `product.ext.requested_id` | string\|null | (seen in a sample response) |
| `product.ext.seller_id` | string\|null |  |
| `product.ext.seller_reputation.detailed_ratings` | object\|null | (seen in a sample response) |
| `product.ext.seller_reputation.feedback_count` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.feedback_percentage` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.items_sold` | number\|null | (seen in a sample response) |
| `product.ext.seller_reputation.joined` | string\|null | (seen in a sample response) |
| `product.ext.seller_reputation.top_rated` | boolean\|null | (seen in a sample response) |
| `product.ext.seller_reputation.url` | string\|null | (seen in a sample response) |
| `product.ext.sephora.sku` | string\|null | (seen in a sample response) |
| `product.ext.sku_id` | string\|null |  |
| `product.ext.sold_count` | number\|null |  |
| `product.ext.store_inventory` | array\|null | (seen in a sample response) |
| `product.ext.tiktokshop` | object\|null |  |
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
| `product.specifications` | array\|null | (only when the fallback source serves) |
| `product.title` | string\|null | Product title |
| `product.url` | string\|null | Direct URL to the product page |
| `product.variations` | array\|null | (on some endpoints only when the fallback source serves) |
