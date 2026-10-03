# QuoteList fields

Every field the 2 field-mapped endpoints returning `QuoteList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `quote.currency` | string\|null | Price currency (null for asset pairs) |
| `quote.id` | string | Instrument identifier: re-feed into /v1/finance/quote ("GOOGL:NASDAQ" \| ".INX:INDEXSP" \| "EUR-USD") |
| `quote.name` | string\|null | Display name (e.g. 'Alphabet Inc Class A') |
| `quote.ticker` | string\|null | Ticker symbol (null for forex/crypto asset pairs) |
| `quote.type` | string | Instrument class: stock \| etf \| index \| crypto \| forex \| futures \| fund \| unknown |
| `quote.url` | string\|null |  |
