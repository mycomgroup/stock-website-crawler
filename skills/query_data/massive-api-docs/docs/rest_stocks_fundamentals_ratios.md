# Ratios

## 源URL

https://massive.com/docs/rest/stocks/fundamentals/ratios

## 描述

Retrieve comprehensive financial ratios data providing key valuation, profitability, liquidity, and leverage metrics for public companies. This dataset combines data from income statements, balance sheets, and cash flow statements with daily stock prices to calculate ratios for the most recent trading day using trailing twelve months (TTM) financials.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Stock ticker symbol for the company. |
| cik | string | 否 | Central Index Key (CIK) number assigned by the SEC to identify the company. |
| price | number | 否 | Stock price used in ratio calculations, typically the closing price for the given date. Value must be a floating point number. |
| average_volume | number | 否 | Average trading volume over the last 30 trading days, providing context for liquidity. Value must be a floating point number. |
| market_cap | number | 否 | Market capitalization, calculated as stock price multiplied by total shares outstanding. Value must be a floating point number. |
| earnings_per_share | number | 否 | Earnings per share, calculated as net income available to common shareholders divided by weighted shares outstanding. Value must be a floating point number. |
| price_to_earnings | number | 否 | Price-to-earnings ratio, calculated as stock price divided by earnings per share. Only calculated when earnings per share is positive. Value must be a floating point number. |
| price_to_book | number | 否 | Price-to-book ratio, calculated as stock price divided by book value per share, comparing market value to book value. Value must be a floating point number. |
| price_to_sales | number | 否 | Price-to-sales ratio, calculated as stock price divided by revenue per share, measuring valuation relative to sales. Value must be a floating point number. |
| price_to_cash_flow | number | 否 | Price-to-cash-flow ratio, calculated as stock price divided by operating cash flow per share. Only calculated when operating cash flow per share is positive. Value must be a floating point number. |
| price_to_free_cash_flow | number | 否 | Price-to-free-cash-flow ratio, calculated as stock price divided by free cash flow per share. Only calculated when free cash flow per share is positive. Value must be a floating point number. |
| dividend_yield | number | 否 | Dividend yield, calculated as annual dividends per share divided by stock price, measuring the income return on investment. Value must be a floating point number. |
| return_on_assets | number | 否 | Return on assets ratio, calculated as net income divided by total assets, measuring how efficiently a company uses its assets to generate profit. Value must be a floating point number. |
| return_on_equity | number | 否 | Return on equity ratio, calculated as net income divided by total shareholders' equity, measuring profitability relative to shareholders' equity. Value must be a floating point number. |
| debt_to_equity | number | 否 | Debt-to-equity ratio, calculated as total debt (current debt plus long-term debt) divided by total shareholders' equity, measuring financial leverage. Value must be a floating point number. |
| current | number | 否 | Current ratio, calculated as total current assets divided by total current liabilities, measuring short-term liquidity. Value must be a floating point number. |
| quick | number | 否 | Quick ratio (acid-test ratio), calculated as (current assets minus inventories) divided by current liabilities, measuring immediate liquidity. Value must be a floating point number. |
| cash | number | 否 | Cash ratio, calculated as cash and cash equivalents divided by current liabilities, measuring the most liquid form of liquidity coverage. Value must be a floating point number. |
| ev_to_sales | number | 否 | Enterprise value to sales ratio, calculated as enterprise value divided by revenue, measuring company valuation relative to sales. Value must be a floating point number. |
| ev_to_ebitda | number | 否 | Enterprise value to EBITDA ratio, calculated as enterprise value divided by EBITDA, measuring company valuation relative to earnings before interest, taxes, depreciation, and amortization. Value must be a floating point number. |
| enterprise_value | number | 否 | Enterprise value, calculated as market capitalization plus total debt minus cash and cash equivalents, representing total company value. Value must be a floating point number. |
| free_cash_flow | number | 否 | Free cash flow, calculated as operating cash flow minus capital expenditures (purchase of property, plant, and equipment). Value must be a floating point number. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| average_volume | number | 否 | Average trading volume over the last 30 trading days, providing context for liquidity. |
| cash | number | 否 | Cash ratio, calculated as cash and cash equivalents divided by current liabilities, measuring the most liquid form of liquidity coverage. |
| cik | string | 否 | Central Index Key (CIK) number assigned by the SEC to identify the company. |
| current | number | 否 | Current ratio, calculated as total current assets divided by total current liabilities, measuring short-term liquidity. |
| date | string | 否 | Date for which the ratios are calculated, representing the trading date with available price data. |
| debt_to_equity | number | 否 | Debt-to-equity ratio, calculated as total debt (current debt plus long-term debt) divided by total shareholders' equity, measuring financial leverage. |
| dividend_yield | number | 否 | Dividend yield, calculated as annual dividends per share divided by stock price, measuring the income return on investment. |
| earnings_per_share | number | 否 | Earnings per share, calculated as net income available to common shareholders divided by weighted shares outstanding. |
| enterprise_value | number | 否 | Enterprise value, calculated as market capitalization plus total debt minus cash and cash equivalents, representing total company value. |
| ev_to_ebitda | number | 否 | Enterprise value to EBITDA ratio, calculated as enterprise value divided by EBITDA, measuring company valuation relative to earnings before interest, taxes, depreciation, and amortization. |
| ev_to_sales | number | 否 | Enterprise value to sales ratio, calculated as enterprise value divided by revenue, measuring company valuation relative to sales. |
| free_cash_flow | number | 否 | Free cash flow, calculated as operating cash flow minus capital expenditures (purchase of property, plant, and equipment). |
| market_cap | number | 否 | Market capitalization, calculated as stock price multiplied by total shares outstanding. |
| price | number | 否 | Stock price used in ratio calculations, typically the closing price for the given date. |
| price_to_book | number | 否 | Price-to-book ratio, calculated as stock price divided by book value per share, comparing market value to book value. |
| price_to_cash_flow | number | 否 | Price-to-cash-flow ratio, calculated as stock price divided by operating cash flow per share. Only calculated when operating cash flow per share is positive. |
| price_to_earnings | number | 否 | Price-to-earnings ratio, calculated as stock price divided by earnings per share. Only calculated when earnings per share is positive. |
| price_to_free_cash_flow | number | 否 | Price-to-free-cash-flow ratio, calculated as stock price divided by free cash flow per share. Only calculated when free cash flow per share is positive. |
| price_to_sales | number | 否 | Price-to-sales ratio, calculated as stock price divided by revenue per share, measuring valuation relative to sales. |
| quick | number | 否 | Quick ratio (acid-test ratio), calculated as (current assets minus inventories) divided by current liabilities, measuring immediate liquidity. |
| return_on_assets | number | 否 | Return on assets ratio, calculated as net income divided by total assets, measuring how efficiently a company uses its assets to generate profit. |
| return_on_equity | number | 否 | Return on equity ratio, calculated as net income divided by total shareholders' equity, measuring profitability relative to shareholders' equity. |
| ticker | string | 否 | Stock ticker symbol for the company. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/financials/v1/ratios
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/financials/v1/ratios?limit=100&sort=ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": "8f5374516fec4a819070e53609f47fab",
  "results": [
    {
      "average_volume": 47500000,
      "cash": 0.19,
      "cik": "320193",
      "current": 0.68,
      "date": "2024-09-19",
      "debt_to_equity": 1.52,
      "dividend_yield": 0.0044,
      "earnings_per_share": 6.57,
      "enterprise_value": 3555509835190,
      "ev_to_ebitda": 26.98,
      "ev_to_sales": 9.22,
      "free_cash_flow": 104339000000,
      "market_cap": 3479770835190,
      "price": 228.87,
      "price_to_book": 52.16,
      "price_to_cash_flow": 30.78,
      "price_to_earnings": 34.84,
      "price_to_free_cash_flow": 33.35,
      "price_to_sales": 9.02,
      "quick": 0.63,
      "return_on_assets": 0.3075,
      "return_on_equity": 1.5284,
      "ticker": "AAPL"
    }
  ],
  "status": "OK"
}
```
