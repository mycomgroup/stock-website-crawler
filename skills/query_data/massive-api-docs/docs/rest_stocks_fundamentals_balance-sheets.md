# Balance Sheets

## 源URL

https://massive.com/docs/rest/stocks/fundamentals/balance-sheets

## 描述

This endpoint replaces Financials.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| cik | string | 否 | The company's Central Index Key (CIK), a unique identifier assigned by the U.S. Securities and Exchange Commission (SEC). You can look up a company's CIK using the SEC CIK Lookup tool. |
| tickers | string | 否 | Filter for arrays that contain the value. |
| period_end | string | 否 | The last date of the reporting period, representing the specific point in time when the balance sheet snapshot was taken. Value must be formatted 'yyyy-mm-dd'. |
| filing_date | string | 否 | The date when the financial statement was filed with the SEC. Value must be formatted 'yyyy-mm-dd'. |
| fiscal_year | number | 否 | The fiscal year for the reporting period. Value must be a floating point number. |
| fiscal_quarter | number | 否 | The fiscal quarter number (1, 2, 3, or 4) for the reporting period. Value must be a floating point number. |
| timeframe | string | 否 | The reporting period type. Possible values include: quarterly, annual. |
| max_ticker | string | 否 | Filter equal to the value. |
| min_ticker | string | 否 | Filter equal to the value. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'period_end' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| accounts_payable | number | 否 | Amounts owed to suppliers and vendors for goods and services purchased on credit. |
| accrued_and_other_current_liabilities | number | 否 | Current liabilities not classified elsewhere, including accrued expenses, taxes payable, and other obligations due within one year. |
| accumulated_other_comprehensive_income | number | 否 | Cumulative gains and losses that bypass the income statement, including foreign currency translation adjustments and unrealized gains/losses on securities. |
| additional_paid_in_capital | number | 否 | Amount received from shareholders in excess of the par or stated value of shares issued. |
| cash_and_equivalents | number | 否 | Cash on hand and short-term, highly liquid investments that are readily convertible to known amounts of cash. |
| cik | string | 否 | The company's Central Index Key (CIK), a unique identifier assigned by the U.S. Securities and Exchange Commission (SEC). You can look up a company's CIK using the SEC CIK Lookup tool. |
| commitments_and_contingencies | number | 否 | Disclosed amount related to contractual commitments and potential liabilities that may arise from uncertain future events. |
| common_stock | number | 否 | Par or stated value of common shares outstanding representing basic ownership in the company. |
| debt_current | number | 否 | Short-term borrowings and the current portion of long-term debt due within one year. |
| deferred_revenue_current | number | 否 | Customer payments received in advance for goods or services to be delivered within one year. |
| filing_date | string | 否 | The date when the financial statement was filed with the SEC. |
| fiscal_quarter | number | 否 | The fiscal quarter number (1, 2, 3, or 4) for the reporting period. |
| fiscal_year | number | 否 | The fiscal year for the reporting period. |
| goodwill | number | 否 | Intangible asset representing the excess of purchase price over fair value of net assets acquired in business combinations. |
| intangible_assets_net | number | 否 | Intangible assets other than goodwill, including patents, trademarks, and customer relationships, net of accumulated amortization. |
| inventories | number | 否 | Raw materials, work-in-process, and finished goods held for sale in the ordinary course of business. |
| long_term_debt_and_capital_lease_obligations | number | 否 | Long-term borrowings and capital lease obligations with maturities greater than one year. |
| noncontrolling_interest | number | 否 | Equity in consolidated subsidiaries not owned by the parent company, representing minority shareholders' ownership. |
| other_assets | number | 否 | Non-current assets not classified elsewhere, including long-term investments, deferred tax assets, and other long-term assets. |
| other_current_assets | number | 否 | Current assets not classified elsewhere, including prepaid expenses, taxes receivable, and other assets expected to be converted to cash within one year. |
| other_equity | number | 否 | Equity components not classified elsewhere in shareholders' equity. |
| other_noncurrent_liabilities | number | 否 | Non-current liabilities not classified elsewhere, including deferred tax liabilities, pension obligations, and other long-term liabilities. |
| period_end | string | 否 | The last date of the reporting period, representing the specific point in time when the balance sheet snapshot was taken. |
| preferred_stock | number | 否 | Par or stated value of preferred shares outstanding with preferential rights over common stock. |
| property_plant_equipment_net | number | 否 | Tangible fixed assets used in operations, reported net of accumulated depreciation. |
| receivables | number | 否 | Amounts owed to the company by customers and other parties, primarily accounts receivable, net of allowances for doubtful accounts. |
| retained_earnings_deficit | number | 否 | Cumulative net income earned by the company less dividends paid to shareholders since inception. |
| short_term_investments | number | 否 | Marketable securities and other investments with maturities of one year or less that are not classified as cash equivalents. |
| tickers | array (string) | 否 | A list of ticker symbols under which the company is listed. Multiple symbols may indicate different share classes for the same company. |
| timeframe | string | 否 | The reporting period type. Possible values include: quarterly, annual. |
| total_assets | number | 否 | Sum of all current and non-current assets representing everything the company owns or controls. |
| total_current_assets | number | 否 | Sum of all current assets expected to be converted to cash, sold, or consumed within one year. |
| total_current_liabilities | number | 否 | Sum of all liabilities expected to be settled within one year. |
| total_equity | number | 否 | Sum of all equity components representing shareholders' total ownership interest in the company. |
| total_equity_attributable_to_parent | number | 否 | Total shareholders' equity attributable to the parent company, excluding noncontrolling interests. |
| total_liabilities | number | 否 | Sum of all current and non-current liabilities representing everything the company owes. |
| total_liabilities_and_equity | number | 否 | Sum of total liabilities and total equity, which should equal total assets per the fundamental accounting equation. |
| treasury_stock | number | 否 | Cost of the company's own shares that have been repurchased and are held in treasury, typically reported as a negative value. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/financials/v1/balance-sheets
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/financials/v1/balance-sheets?limit=100&sort=period_end.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": "d9f86384d43845a4a3d7b79098fb08dd",
  "results": [
    {
      "accounts_payable": 50374000000,
      "accrued_and_other_current_liabilities": 62499000000,
      "accumulated_other_comprehensive_income": -6369000000,
      "cash_and_equivalents": 36269000000,
      "cik": "0000320193",
      "common_stock": 89806000000,
      "debt_current": 19268000000,
      "deferred_revenue_current": 8979000000,
      "filing_date": "2025-08-01",
      "fiscal_quarter": 3,
      "fiscal_year": 2025,
      "inventories": 5925000000,
      "long_term_debt_and_capital_lease_obligations": 82430000000,
      "other_assets": 160496000000,
      "other_current_assets": 14359000000,
      "other_equity": 0,
      "other_noncurrent_liabilities": 42115000000,
      "period_end": "2025-06-28",
      "property_plant_equipment_net": 48508000000,
      "receivables": 46835000000,
      "retained_earnings_deficit": -17607000000,
      "tickers": [
        "AAPL"
      ],
      "timeframe": "quarterly",
      "total_assets": 331495000000,
      "total_current_assets": 103388000000,
      "total_current_liabilities": 141120000000,
      "total_equity": 65830000000,
      "total_equity_attributable_to_parent": 65830000000,
      "total_liabilities": 265665000000,
      "total_liabilities_and_equity": 331495000000
    }
  ],
  "status": "OK"
}
```
