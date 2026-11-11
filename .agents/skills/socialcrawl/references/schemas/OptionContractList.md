# OptionContractList fields

Every field the 1 field-mapped endpoints returning `OptionContractList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `option_contract.ask` | number\|null | Lowest price a seller is asking for the contract. |
| `option_contract.bid` | number\|null | Highest price a buyer is offering for the contract. |
| `option_contract.change` | number\|null | Absolute change in the last price since the previous close. |
| `option_contract.contract_size` | string\|null | Number of underlying shares one contract covers, as a string. |
| `option_contract.contract_symbol` | string\|null | The contract's own OCC symbol. |
| `option_contract.currency` | string\|null | Currency the prices are quoted in. |
| `option_contract.expiry` | string\|number\|null | Expiry date, absolute UTC |
| `option_contract.id` | string | OCC contract symbol |
| `option_contract.implied_volatility` | number\|null | Implied volatility as a decimal fraction |
| `option_contract.in_the_money` | boolean\|null | Whether the contract is currently in the money |
| `option_contract.last_price` | number\|null | Price of the last trade. |
| `option_contract.last_trade_date` | string\|number\|null | When the contract last traded. A date string or an epoch number as the source gives it. |
| `option_contract.open_interest` | number\|null | Contracts outstanding |
| `option_contract.percent_change` | number\|null | Change in the last price since the previous close, as a percentage. |
| `option_contract.strike` | number\|null | Strike price |
| `option_contract.symbol` | string\|null | The UNDERLYING instrument, not the contract |
| `option_contract.type` | string\|null | call \| put |
| `option_contract.volume` | number\|null | Contracts traded in the current session. |
