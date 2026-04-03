# Related Tickers

## 源URL

https://massive.com/docs/rest/stocks/tickers/related-tickers

## 描述

Retrieve a list of tickers related to a specified ticker, identified through an analysis of news coverage and returns data. This endpoint helps users discover peers, competitors, or thematically similar companies, aiding in comparative analysis, portfolio diversification, and market research.

## Endpoint

```
GET /v1/related-companies/{ticker}
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | The ticker symbol to search. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | An array of results containing the requested data. |
| ticker | string | 否 | A ticker related to the requested ticker. |
| status | string | 否 | The status of this request's response. |
| ticker | string | 否 | The ticker being queried. |

## 代码示例

```text
/v1/related-companies/{ticker}
```

### Request

```bash
curl -X GET "https://api.massive.com/v1/related-companies/AAPL?apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": "31d59dda-80e5-4721-8496-d0d32a654afe",
  "results": [
    {
      "ticker": "MSFT"
    },
    {
      "ticker": "GOOGL"
    },
    {
      "ticker": "AMZN"
    },
    {
      "ticker": "FB"
    },
    {
      "ticker": "TSLA"
    },
    {
      "ticker": "NVDA"
    },
    {
      "ticker": "INTC"
    },
    {
      "ticker": "ADBE"
    },
    {
      "ticker": "NFLX"
    },
    {
      "ticker": "PYPL"
    }
  ],
  "status": "OK",
  "stock_symbol": "AAPL"
}
```
