# Quote fields

Every field the 1 field-mapped endpoints returning `Quote` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `quote.currency` | string\|null | Price currency (null for asset pairs) |
| `quote.exchange` | string\|null | Primary exchange / market identifier (seen in a sample response) |
| `quote.financials.annual` | array\|null | Annual results, newest first. (seen in a sample response) |
| `quote.financials.quarterly` | array\|null | Quarterly results, newest first. (seen in a sample response) |
| `quote.graph` | array\|null | Intraday price series ({ timestamp, value, volume }) (seen in a sample response) |
| `quote.id` | string | Instrument identifier: re-feed into /v1/finance/quote ("GOOGL:NASDAQ" \| ".INX:INDEXSP" \| "EUR-USD") |
| `quote.metrics` | object\|null | Fundamentals (market_cap, pe_ratio, dividend_yield, expense_ratio, …); null on thin rows (seen in a sample response) |
| `quote.name` | string\|null | Display name (e.g. 'Alphabet Inc Class A') |
| `quote.pair` | object\|null | Forex/crypto base+quote symbols (null for stocks/indices) (seen in a sample response) |
| `quote.peers` | array\|null | Related instruments (compare_to) (seen in a sample response) |
| `quote.price.current` | number\|null | Latest price, or the index level for an index, in the quote currency. (seen in a sample response) |
| `quote.price.day_high` | number\|null | Highest price of the current trading day. (seen in a sample response) |
| `quote.price.day_low` | number\|null | Lowest price of the current trading day. (seen in a sample response) |
| `quote.price.delta` | number\|null | Absolute change from the previous close, in the quote currency. (seen in a sample response) |
| `quote.price.percentage_delta` | number\|null | Change from the previous close as a percentage (1.5 means 1.5%). (seen in a sample response) |
| `quote.price.previous_close` | number\|null | Closing price of the previous trading session. (seen in a sample response) |
| `quote.price.timestamp` | string\|null | When the price was quoted, as a UTC timestamp string. (seen in a sample response) |
| `quote.price.trend` | string\|null | Direction of the change from the previous close: up, down or stable. (seen in a sample response) |
| `quote.price.year_high` | number\|null | Highest price of the last 52 weeks. (seen in a sample response) |
| `quote.price.year_low` | number\|null | Lowest price of the last 52 weeks. (seen in a sample response) |
| `quote.ticker` | string\|null | Ticker symbol (null for forex/crypto asset pairs) |
| `quote.type` | string | Instrument class: stock \| etf \| index \| crypto \| forex \| futures \| fund \| unknown |
| `quote.url` | string\|null | URL of the quote page on the source. |
