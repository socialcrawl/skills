# Seller fields

Every field the 2 field-mapped endpoints returning `Seller` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `seller.domain` | string\|null | Domain of the seller's site. |
| `seller.id` | string | The seller's id: its domain or a slug of its name. |
| `seller.name` | string\|null | Seller name |
| `seller.rating.average` | number\|null | Average rating of the seller, normally out of 5. |
| `seller.rating.count` | number\|null | Number of ratings behind the average. |
| `seller.url` | string\|null | URL of the seller's offer page. |
