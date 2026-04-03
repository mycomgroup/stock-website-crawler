# Schedules

## 源URL

https://massive.com/docs/rest/futures/schedules

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| product_code | string | 否 | The product code of the futures contract. |
| session_end_date | string | 否 | The session end date for the schedules (also known as the trading date). This field is optional and can be used to filter results by a specific session end date. If left blank, schedules for all dates will be returned. Note that trading sessions end at 5 PM Central Time, so a session ending at 5 PM CT on January 1st would have a session_end_date of 2025-01-01. |
| trading_venue | string | 否 | The trading venue (MIC) for the exchange on which this schedule's product trades. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '10' if not specified. The maximum allowed limit is '1000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'product_code' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| event | string | 否 | The type of session on the given trading date. |
| product_code | string | 否 | The product code of the futures contract. |
| product_name | string | 否 | The name of the futures product to which this schedule applies. |
| session_end_date | string | 否 | The session end date for the schedules (also known as the trading date). This field is optional and can be used to filter results by a specific session end date. If left blank, schedules for all dates will be returned. Note that trading sessions end at 5 PM Central Time, so a session ending at 5 PM CT on January 1st would have a session_end_date of 2025-01-01. |
| timestamp | string | 否 | The timestamp for the given market event. |
| trading_venue | string | 否 | The trading venue (MIC) for the exchange on which this schedule's product trades. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/futures/vX/schedules
```

### Request

```bash
curl -X GET "https://api.massive.com/futures/vX/schedules?limit=10&sort=product_code.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "next_url": "https://api.staging.massive.com/futures/vX/schedules?cursor=AQANA0VSTAIAAAEFAAEBAwACAQ0DRVJMAQ0ZMjAyNC0wNi0xMFQyMTowMDowMCswMDowMA==",
  "request_id": "a83620d1ec6a4cd5b84ea669e377fd47",
  "results": [
    {
      "event": "pre_open",
      "product_code": "ERL",
      "product_name": "ERCOT North 345 kV Hub Day-Ahead 5 MW Off-Peak Futures",
      "session_end_date": "2024-06-10",
      "timestamp": "2024-06-09T21:00:00+00:00",
      "trading_venue": "XNYM"
    },
    {
      "event": "open",
      "product_code": "ERL",
      "product_name": "ERCOT North 345 kV Hub Day-Ahead 5 MW Off-Peak Futures",
      "session_end_date": "2024-06-10",
      "timestamp": "2024-06-09T22:00:00+00:00",
      "trading_venue": "XNYM"
    },
    {
      "event": "close",
      "product_code": "ERL",
      "product_name": "ERCOT North 345 kV Hub Day-Ahead 5 MW Off-Peak Futures",
      "session_end_date": "2024-06-10",
      "timestamp": "2024-06-10T21:00:00+00:00",
      "trading_venue": "XNYM"
    }
  ],
  "status": "OK"
}
```
