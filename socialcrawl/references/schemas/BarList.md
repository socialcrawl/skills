# BarList fields

Every field the 1 field-mapped endpoints returning `BarList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `bar.adj_close` | number\|null | Closing price adjusted for BOTH splits and dividends. Use this for total-return maths; use close for price maths |
| `bar.close` | number\|null | Closing price, split-adjusted, NOT dividend-adjusted |
| `bar.currency` | string\|null | Price currency |
| `bar.date` | string\|number\|null | Session date, absolute UTC ISO-8601 |
| `bar.dividend` | number\|null | Cash dividend per share going ex on this date; null on an ordinary day |
| `bar.high` | number\|null | Session high |
| `bar.id` | string | Stable row id ("<symbol>:<date>") |
| `bar.interval` | string\|null | Bar width ("1d" \| "1wk" \| "1mo" \| "1m" \| "5m" \| ...) |
| `bar.low` | number\|null | Session low |
| `bar.open` | number\|null | Opening price |
| `bar.split_ratio` | string\|null | Split effective on this date (e.g. "10:1"); null on an ordinary day |
| `bar.symbol` | string\|null | Instrument symbol this bar belongs to |
| `bar.volume` | number\|null | Shares traded |
