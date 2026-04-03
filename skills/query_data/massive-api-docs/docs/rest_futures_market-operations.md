# Market Status

## 源URL

https://massive.com/docs/rest/futures/market-operations

## 描述

Retrieve the current market status for a specific product or products. This endpoint returns real-time indicators, such as open, pause, close, for futures products, along with the corresponding exchange and product codes and an evaluation timestamp. This information enables users to monitor operational conditions and adjust their trading strategies accordingly.Use Cases: Real-time monitoring, algorithm scheduling, UI updates, operational planning.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| product_code | string | 否 | The product code of the futures contracts for which you want statuses. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| market_event | string | 否 | The current status of the market for the product. |
| name | string | 否 | The name of the futures product. |
| product_code | string | 否 | The product code of the futures contracts for which you want statuses. |
| session_end_date | string | 否 | The trading date for the current session. |
| timestamp | string | 否 | The timestamp for the given market event. |
| trading_venue | string | 否 | The trading venue (MIC) for the exchange on which the corresponding product trades. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/futures/vX/market-status
```

### Request

```bash
curl -X GET "https://api.massive.com/futures/vX/market-status?limit=100&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": "445ebfcfe5bb4b688b7971e1600c952d",
  "results": [
    {
      "market_event": "open",
      "name": "ERCOT North 345 kV Hub Day-Ahead 5 MW Off-Peak Futures",
      "product_code": "ERL",
      "session_end_date": "2025-12-05",
      "timestamp": "2025-12-04T23:00:00+00:00",
      "trading_venue": "XNYM"
    }
  ],
  "status": "OK"
}
```
