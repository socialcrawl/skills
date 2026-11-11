# SellerList fields

Every field the 4 field-mapped endpoints returning `SellerList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `seller.annotation` | string\|null | Note shown with the offer, for example a special offer. |
| `seller.availability` | string\|null | Stock status of the offer as the seller words it. |
| `seller.condition` | string\|null | Item condition (e.g. "New", "Refurbished - Excellent") |
| `seller.domain` | string\|null | Domain of the seller's site. |
| `seller.id` | string\|null | The seller's id: its domain or a slug of its name. |
| `seller.name` | string\|null | Seller name |
| `seller.price.base` | number\|null | Item price before tax and shipping, in the price currency. |
| `seller.price.currency` | string\|null | Currency code of the prices. |
| `seller.price.shipping` | number\|null | Shipping cost, in the price currency. |
| `seller.price.tax` | number\|null | Tax, in the price currency. |
| `seller.price.total` | number\|null | Total price including tax and shipping, in the price currency. |
| `seller.rating.average` | number\|null | Average rating of the seller, normally out of 5. |
| `seller.rating.count` | number\|null | Number of ratings behind the average. |
| `seller.url` | string\|null | URL of the seller's offer page. |
