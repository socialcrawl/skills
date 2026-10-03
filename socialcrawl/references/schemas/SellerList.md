# SellerList fields

Every field the 4 field-mapped endpoints returning `SellerList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `seller.annotation` | string\|null |  |
| `seller.availability` | string\|null |  |
| `seller.condition` | string\|null | Item condition (e.g. "New", "Refurbished - Excellent") |
| `seller.domain` | string\|null |  |
| `seller.id` | string\|null |  |
| `seller.name` | string\|null | Seller name |
| `seller.price.base` | number\|null |  |
| `seller.price.currency` | string\|null |  |
| `seller.price.shipping` | number\|null |  |
| `seller.price.tax` | number\|null |  |
| `seller.price.total` | number\|null |  |
| `seller.rating.average` | number\|null |  |
| `seller.rating.count` | number\|null |  |
| `seller.url` | string\|null |  |
