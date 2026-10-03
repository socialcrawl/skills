# Product fields

Every field the 15 field-mapped endpoints returning `Product` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `product.availability` | string\|null | Stock/availability string when surfaced |
| `product.brand` | string\|null | Brand name (cleaned). Null when the platform exposes a seller instead. |
| `product.description` | string\|null |  |
| `product.ext.catalog_id` | string\|null |  |
| `product.ext.model_number` | unknown\|null |  |
| `product.ext.seller_id` | string\|null |  |
| `product.ext.sku_id` | string\|null |  |
| `product.ext.sold_count` | number\|null |  |
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
