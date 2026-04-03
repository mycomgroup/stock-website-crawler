# Trades

## 源URL

https://massive.com/docs/rest/futures/trades-quotes

## 描述

Retrieve comprehensive, tick-level trade data for a specified futures contract ticker over a defined time range. Each record includes the trade price, size, session start date, and precise timestamps, capturing individual trade events throughout the period. This granular data is essential for constructing aggregated bars and performing detailed analyses of intraday price movements, making it a valuable tool for backtesting, algorithmic strategy development, and market research.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | The futures contract identifier, including the base symbol and contract expiration (e.g., GCJ5 for the April 2025 gold contract). |
| timestamp | string | 否 | Query by trade timestamp. Either a date with the format YYYY-MM-DD or a nanosecond timestamp. |
| session_end_date | string | 否 | Also known as the trading date, the date of the end of the trading session, in YYYY-MM-DD format. |
| limit | integer | 否 | The number of results to return per page (default=1000, maximum=50000, minimum=1). |
| sort | enum (string) | 否 | Sort results by field and direction using dotted notation (e.g., 'ticker.asc', 'name.desc'). |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page of data. |
| results | array (object) | 否 | The price of the trade. This is the actual dollar value per whole contract of this trade. A trade of 100 contracts with a price of $2.00 would be worth a total dollar value of $200.00. |
| price | number | 否 | The price of the trade. This is the actual dollar value per whole contract of this trade. A trade of 100 contracts with a price of $2.00 would be worth a total dollar value of $200.00. |
| report_sequence | integer | 否 | The reporting sequence number. |
| sequence_number | integer | 否 | The unique sequence number assigned to this trade. |
| session_end_date | string | 否 | Also known as the trading date, the date of the end of the trading session, in YYYY-MM-DD format. |
| size | number | 否 | The total number of contracts exchanged between buyers and sellers on a given trade. |
| ticker | string | 否 | ticker of the trade |
| timestamp | integer | 否 | The time when the trade was generated at the exchange to nanosecond precision. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/futures/vX/trades/{ticker}
```

### Request

```bash
curl -X GET "https://api.massive.com/futures/vX/trades/GCJ5?limit=1000&sort=timestamp.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "next_url": "https://api.massive.com/futures/vX/trades/ESZ4?cursor=YXA9MTczNDQ3MDk3MDAwODU5OTI2MSZhcz0yNzIzNTI4MyZsaW1pdD0xMDAwJnNlc3Npb25fZW5kX2RhdGU9MjAyNC0xMi0xNyZzb3J0PXRpbWVzdGFtcC5kZXNj",
  "request_id": "a47d1beb8c11b6ae897ab76cdbbf35a3",
  "results": [
    {
      "price": 6052,
      "report_sequence": 12033289,
      "sequence_number": 27317882,
      "session_end_date": "2024-12-17",
      "size": 3,
      "ticker": "ESZ4",
      "timestamp": 1734472799000509200
    },
    {
      "price": 6051.75,
      "report_sequence": 12033276,
      "sequence_number": 27317863,
      "session_end_date": "2024-12-17",
      "size": 1,
      "ticker": "ESZ4",
      "timestamp": 1734472798789679900
    },
    {
      "price": 6052,
      "report_sequence": 12033255,
      "sequence_number": 27317826,
      "session_end_date": "2024-12-17",
      "size": 2,
      "ticker": "ESZ4",
      "timestamp": 1734472797000893000
    }
  ],
  "status": "OK"
}
```
