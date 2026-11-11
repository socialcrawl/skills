# ProductList fields

Every field the 34 field-mapped endpoints returning `ProductList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `product.availability` | string\|null | Stock/availability string when surfaced (on some endpoints only when the fallback source serves) |
| `product.brand` | string\|null | Brand name (cleaned). Null when the platform exposes a seller instead. (on some endpoints only when the fallback source serves) |
| `product.description` | string\|null | Product description. (on some endpoints only when the fallback source serves) |
| `product.ext.aliexpress.category` | string | Top-level category. (seen in a sample response) |
| `product.ext.aliexpress.commission_rate` | string | Affiliate commission rate, such as `7.0%`. (seen in a sample response) |
| `product.ext.aliexpress.discount` | string | Discount, such as `49%`. (seen in a sample response) |
| `product.ext.aliexpress.positive_rate` | string\|null | Share of positive feedback, such as `90.8%`. (seen in a sample response) |
| `product.ext.aliexpress.shop_url` | string | Link to the seller's shop. (seen in a sample response) |
| `product.ext.aliexpress.subcategory` | string | Sub-category. (seen in a sample response) |
| `product.ext.availability_type` | unknown\|null |  |
| `product.ext.available_quantity` | number\|null | Units the seller currently has listed. eBay only. (seen in a sample response) |
| `product.ext.bought_past_month` | number\|null | Lower bound of the purchase badge, for example 10000 for '10K+ bought in past month'. Null when there is no count. (only when the fallback source serves) |
| `product.ext.bought_past_month_label` | string\|null | The purchase badge text exactly as Amazon prints it. |
| `product.ext.buying_format` | string\|null | Sale type of the listing: auction, buy_it_now or accepts_offers. (seen in a sample response) |
| `product.ext.catalog_id` | string\|null | Walmart's alphanumeric catalog id. product.id holds the numeric id from the URL. |
| `product.ext.condition` | string\|null | Condition of a marketplace listing, for example Used or Open Box. (seen in a sample response) |
| `product.ext.data_docid` | string\|null | Google Shopping identifier used to look up the product's detail, reviews and sellers. (seen in a sample response) |
| `product.ext.department` | unknown\|null |  |
| `product.ext.etsy.is_handmade` | boolean | True when the seller marks the item handmade. (seen in a sample response) |
| `product.ext.gid` | string\|null | Google Shopping product group id used to chain from search to detail, reviews and sellers. (seen in a sample response) |
| `product.ext.gumtree.category` | string | The category's name. (seen in a sample response) |
| `product.ext.gumtree.category_id` | string | The category's id. (seen in a sample response) |
| `product.ext.gumtree.location` | string | Where the item is. (seen in a sample response) |
| `product.ext.gumtree.location_id` | string | The location's id. (seen in a sample response) |
| `product.ext.gumtree.seller_type` | string | Kind of seller, such as `trade`. (seen in a sample response) |
| `product.ext.hm.category_code` | string | H&M's category code. (seen in a sample response) |
| `product.ext.hm.color` | string | The colour name. (seen in a sample response) |
| `product.ext.hm.new_arrival` | boolean\|null | True when H&M marks the item a new arrival. (seen in a sample response) |
| `product.ext.hm.sizes` | array | Sizes on offer. (seen in a sample response) |
| `product.ext.kohls.colors` | array | Colours on offer. (seen in a sample response) |
| `product.ext.kohls.coupon_eligible` | boolean | True when store coupons apply. (seen in a sample response) |
| `product.ext.kohls.display_color` | string | The colour shown for the item. (seen in a sample response) |
| `product.ext.kohls.ship` | boolean | True when the item ships. (seen in a sample response) |
| `product.ext.kohls.sku` | string | The SKU. (seen in a sample response) |
| `product.ext.model_number` | unknown\|null |  |
| `product.ext.promotion.amount_off` | number\|null | Amount off the original price, in the price currency. (seen in a sample response) |
| `product.ext.promotion.label` | string\|null | The retailer's own label, for example Clearance or Special Buys. (seen in a sample response) |
| `product.ext.promotion.percent_off` | number\|null | Percentage off the original price. (seen in a sample response) |
| `product.ext.requested_id` | string\|null | The id you asked for, when the retailer rolled a variant up to its parent. Set only when it differs from product.id. (seen in a sample response) |
| `product.ext.seller_id` | string\|null | The seller's id on the retailer. |
| `product.ext.seller_reputation.detailed_ratings` | object\|null | The seller's average score on four specific measures. (seen in a sample response) |
| `product.ext.seller_reputation.feedback_count` | number\|null | Lifetime number of feedback ratings the seller received. (seen in a sample response) |
| `product.ext.seller_reputation.feedback_percentage` | number\|null | Share of the seller's feedback that is positive, as a percentage. (seen in a sample response) |
| `product.ext.seller_reputation.items_sold` | number\|null | Items the seller has sold. (seen in a sample response) |
| `product.ext.seller_reputation.joined` | string\|null | When the seller joined the marketplace, as the marketplace prints it. (seen in a sample response) |
| `product.ext.seller_reputation.top_rated` | boolean\|null | Whether the marketplace gives the seller its top rated status. (seen in a sample response) |
| `product.ext.seller_reputation.url` | string\|null | URL of the seller's page. (seen in a sample response) |
| `product.ext.sephora.sku` | string | The SKU. (seen in a sample response) |
| `product.ext.sku_id` | string\|null | Colour or size variant id. Shipping quotes need it beside the product id. |
| `product.ext.sold_count` | number\|null | Units sold, as the listing reports it. |
| `product.ext.store_inventory` | array\|null | Stock at individual stores or fulfilment points. (seen in a sample response) |
| `product.ext.tiktokshop` | object\|null | TikTok Shop detail. |
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
| `product.specifications` | array\|null | Specification rows from the product page. Detail only. (only when the fallback source serves) |
| `product.title` | string\|null | Product title |
| `product.url` | string\|null | Direct URL to the product page |
| `product.variations` | array\|null | Other variants of the product, such as colour or size. Detail only. (on some endpoints only when the fallback source serves) |
