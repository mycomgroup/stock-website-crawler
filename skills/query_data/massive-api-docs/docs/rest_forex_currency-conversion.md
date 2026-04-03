# Currency Conversion

## 源URL

https://massive.com/docs/rest/forex/currency-conversion

## 描述

Retrieve real-time currency conversion rates between any two supported currencies. This endpoint provides the most recent bid/ask quotes and calculates the converted amount based on the current market rate, enabling users to quickly and accurately convert values in both directions (e.g., USD to CAD or CAD to USD).

## Endpoint

```
GET /v1/conversion/{from}/{to}
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| from | string | 否 | The "from" symbol of the pair. |
| to | string | 否 | The "to" symbol of the pair. |
| amount | number | 否 | The amount to convert, with a decimal. |
| precision | enum (integer) | 否 | The decimal precision of the conversion. Defaults to 2 which is 2 decimal places accuracy. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| converted | number | 否 | The result of the conversion. |
| from | string | 否 | The "from" currency symbol. |
| initialAmount | number | 否 | The amount to convert. |
| last | object | 否 | Contains the requested quote data for the specified forex currency pair. |
| ask | number | 否 | The ask price. |
| bid | number | 否 | The bid price. |
| exchange | integer | 否 | The exchange ID. See Exchanges for Massive's mapping of exchange IDs. |
| timestamp | integer | 否 | The Unix millisecond timestamp. |
| request_id | string | 否 | A request id assigned by the server. |
| status | string | 否 | The status of this request's response. |
| symbol | string | 否 | The symbol pair that was evaluated from the request. |
| to | string | 否 | The "to" currency symbol. |

## 代码示例

```text
/v1/conversion/{from}/{to}
```

### Request

```bash
curl -X GET "https://api.massive.com/v1/conversion/AUD/USD?amount=100&precision=2&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "converted": 73.14,
  "from": "AUD",
  "initialAmount": 100,
  "last": {
    "ask": 1.3673344,
    "bid": 1.3672596,
    "exchange": 48,
    "timestamp": 1605555313000
  },
  "request_id": "a73a29dbcab4613eeaf48583d3baacf0",
  "status": "success",
  "symbol": "AUD/USD",
  "to": "USD"
}
```
