# REST Quickstart

## 源URL

https://massive.com/docs/rest

## 描述

The Massive REST API provides comprehensive access to historical and real-time market data from major U.S. exchanges. With it, you can query endpoints for dividends, trades, quotes, fundamental data, and more. To get started, you will need to sign up for an account and authenticate your requests using an API key.

## Endpoint

```
GET /v3/reference/dividends
```

## 代码示例

```text
https://api.massive.com/v3/reference/dividends?apiKey=YOUR_API_KEY
```

```text
GET /v3/reference/dividends HTTP/1.1
Host: api.massive.com
Authorization: Bearer YOUR_API_KEY
```

### Request

```bash
curl "https://api.massive.com/v3/reference/dividends?apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "results": [
      {
          "cash_amount": 0.25,
          "currency": "USD",
          "declaration_date": "2024-10-31",
          "dividend_type": "CD",
          "ex_dividend_date": "2024-11-08",
          "frequency": 4,
          "id": "E416a068758f85277196150c3eb73a3331d04698856c141e883ad95710dd0b189",
          "pay_date": "2024-11-14",
          "record_date": "2024-11-11",
          "ticker": "AAPL"
      }
  ],
  "status": "OK",
  "request_id": "5a8e1e551dc3a1c2c203744543b40399",
}
```
