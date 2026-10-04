# FinancialStatementList fields

Every field the 1 field-mapped endpoints returning `FinancialStatementList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `financial_statement.cash_and_short_term_investments` | number\|null |  |
| `financial_statement.cash_and_short_term_investments_delta` | number\|null |  |
| `financial_statement.cash_from_financing` | number\|null |  |
| `financial_statement.cash_from_financing_delta` | number\|null |  |
| `financial_statement.cash_from_investing` | number\|null |  |
| `financial_statement.cash_from_investing_delta` | number\|null |  |
| `financial_statement.cash_from_operations` | number\|null |  |
| `financial_statement.cash_from_operations_delta` | number\|null |  |
| `financial_statement.currency` | string\|null | Reporting currency |
| `financial_statement.earnings_per_share` | number\|null |  |
| `financial_statement.earnings_per_share_delta` | number\|null |  |
| `financial_statement.ebitda` | number\|null |  |
| `financial_statement.ebitda_delta` | number\|null |  |
| `financial_statement.effective_tax_rate` | number\|null |  |
| `financial_statement.free_cash_flow` | number\|null |  |
| `financial_statement.free_cash_flow_delta` | number\|null |  |
| `financial_statement.id` | string | Stable row id ("<symbol>:<statement>:<period_end>") |
| `financial_statement.net_change_in_cash` | number\|null |  |
| `financial_statement.net_change_in_cash_delta` | number\|null |  |
| `financial_statement.net_income` | number\|null |  |
| `financial_statement.net_income_delta` | number\|null |  |
| `financial_statement.net_profit_margin` | number\|null |  |
| `financial_statement.net_profit_margin_delta` | number\|null |  |
| `financial_statement.operating_expense` | number\|null |  |
| `financial_statement.operating_expense_delta` | number\|null |  |
| `financial_statement.period_end` | string\|number\|null | Fiscal period END, absolute UTC. NOTE: this is not a filing date. Point-in-time reconstruction and restatement detection are NOT supported on this surface |
| `financial_statement.period_type` | string\|null | quarterly \| annual \| ttm |
| `financial_statement.price_to_book` | number\|null | (seen in a sample response) |
| `financial_statement.return_on_assets` | number\|null | (seen in a sample response) |
| `financial_statement.return_on_capital` | number\|null | (seen in a sample response) |
| `financial_statement.revenue` | number\|null |  |
| `financial_statement.revenue_delta` | number\|null |  |
| `financial_statement.shares_outstanding` | number\|null |  |
| `financial_statement.statement` | string\|null | income \| balance_sheet \| cash_flow \| combined |
| `financial_statement.symbol` | string\|null |  |
| `financial_statement.total_assets` | number\|null |  |
| `financial_statement.total_assets_delta` | number\|null |  |
| `financial_statement.total_equity` | number\|null |  |
| `financial_statement.total_liabilities` | number\|null |  |
| `financial_statement.total_liabilities_delta` | number\|null |  |
