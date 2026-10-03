# Seller fields

Every field the 2 field-mapped endpoints returning `Seller` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `seller.domain` | string\|null |  |
| `seller.id` | string |  |
| `seller.name` | string\|null | Seller name |
| `seller.rating.average` | number\|null |  |
| `seller.rating.count` | number\|null |  |
| `seller.url` | string\|null |  |
