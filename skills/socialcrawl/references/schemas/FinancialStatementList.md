# FinancialStatementList fields

Every field the 1 field-mapped endpoints returning `FinancialStatementList` can carry, with paths exactly as returned (relative to the row; each endpoint's **Response** line says where its rows sit). One endpoint fills only some of them: its own section lists its top fields, fill rates, never-filled fields and opt-in fields.

| Field | Type | Meaning |
|---|---|---|
| `financial_statement.cash_and_short_term_investments` | number\|null | Cash and short term investments at period end, in the statement currency. |
| `financial_statement.cash_and_short_term_investments_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.cash_from_financing` | number\|null | Net cash from financing activities, in the statement currency. |
| `financial_statement.cash_from_financing_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.cash_from_investing` | number\|null | Net cash from investing activities, in the statement currency. Negative when more cash went out. |
| `financial_statement.cash_from_investing_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.cash_from_operations` | number\|null | Net cash from operating activities, in the statement currency. |
| `financial_statement.cash_from_operations_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.currency` | string\|null | Reporting currency |
| `financial_statement.earnings_per_share` | number\|null | Earnings per share, in the statement currency. |
| `financial_statement.earnings_per_share_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.ebitda` | number\|null | Earnings before interest, tax, depreciation and amortisation, in the statement currency. |
| `financial_statement.ebitda_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.effective_tax_rate` | number\|null | Tax paid as a percentage of pre tax income. |
| `financial_statement.free_cash_flow` | number\|null | Operating cash flow minus capital spending, in the statement currency. |
| `financial_statement.free_cash_flow_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.id` | string | Stable row id ("<symbol>:<statement>:<period_end>") |
| `financial_statement.net_change_in_cash` | number\|null | Net change in cash over the period, in the statement currency. |
| `financial_statement.net_change_in_cash_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.net_income` | number\|null | Net income for the period, in the statement currency. |
| `financial_statement.net_income_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.net_profit_margin` | number\|null | Net income as a percentage of revenue. |
| `financial_statement.net_profit_margin_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.operating_expense` | number\|null | Operating expenses for the period, in the statement currency. |
| `financial_statement.operating_expense_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.period_end` | string\|number\|null | Fiscal period END, absolute UTC. NOTE: this is not a filing date. Point-in-time reconstruction and restatement detection are NOT supported on this surface |
| `financial_statement.period_type` | string\|null | quarterly \| annual \| ttm |
| `financial_statement.price_to_book` | number\|null | Share price divided by book value per share. (seen in a sample response) |
| `financial_statement.return_on_assets` | number\|null | Net income as a percentage of total assets. (seen in a sample response) |
| `financial_statement.return_on_capital` | number\|null | Return on invested capital, as a percentage. (seen in a sample response) |
| `financial_statement.revenue` | number\|null | Revenue for the period, in the statement currency. |
| `financial_statement.revenue_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.shares_outstanding` | number\|null | Number of shares outstanding. |
| `financial_statement.statement` | string\|null | income \| balance_sheet \| cash_flow \| combined |
| `financial_statement.symbol` | string\|null | Ticker symbol of the company. |
| `financial_statement.total_assets` | number\|null | Total assets at period end, in the statement currency. |
| `financial_statement.total_assets_delta` | number\|null | Change from the previous period, as a percentage. |
| `financial_statement.total_equity` | number\|null | Total shareholder equity at period end, in the statement currency. |
| `financial_statement.total_liabilities` | number\|null | Total liabilities at period end, in the statement currency. |
| `financial_statement.total_liabilities_delta` | number\|null | Change from the previous period, as a percentage. |
