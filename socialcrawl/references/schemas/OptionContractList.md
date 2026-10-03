# OptionContractList fields

Every field the 1 field-mapped endpoints returning `OptionContractList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `option_contract.ask` | number\|null |  |
| `option_contract.bid` | number\|null |  |
| `option_contract.change` | number\|null |  |
| `option_contract.contract_size` | string\|null |  |
| `option_contract.contract_symbol` | string\|null |  |
| `option_contract.currency` | string\|null |  |
| `option_contract.expiry` | string\|number\|null | Expiry date, absolute UTC |
| `option_contract.id` | string | OCC contract symbol |
| `option_contract.implied_volatility` | number\|null | Implied volatility as a decimal fraction |
| `option_contract.in_the_money` | boolean\|null | Whether the contract is currently in the money |
| `option_contract.last_price` | number\|null |  |
| `option_contract.last_trade_date` | string\|number\|null |  |
| `option_contract.open_interest` | number\|null | Contracts outstanding |
| `option_contract.percent_change` | number\|null |  |
| `option_contract.strike` | number\|null | Strike price |
| `option_contract.symbol` | string\|null | The UNDERLYING instrument, not the contract |
| `option_contract.type` | string\|null | call \| put |
| `option_contract.volume` | number\|null |  |
