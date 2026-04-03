# Quotes

## 源URL

https://massive.com/docs/rest/futures/trades-quotes/quotes

## 描述

Retrieve quote data for a specified futures contract ticker. Each record includes the best bid and offer prices, sizes, and timestamps, reflecting the prevailing quote environment at each moment. This endpoint supports detailed analysis of price dynamics and liquidity conditions to inform trading decisions and market research.

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
| results | array (object) | 否 | The ask price is expressed per unit of the underlying asset, and you apply the contract multiplier to get the full contract value. |
| ask_price | number | 否 | The ask price is expressed per unit of the underlying asset, and you apply the contract multiplier to get the full contract value. |
| ask_size | number | 否 | The quote size represents the number of futures contracts available at the given ask price. |
| ask_timestamp | integer | 否 | The time when the ask price was submitted to the exchange. |
| bid_price | number | 否 | The bid price is expressed per unit of the underlying asset, and you apply the contract multiplier to get the full contract value. |
| bid_size | number | 否 | The quote size represents the number of futures contracts available at the given bid price. |
| bid_timestamp | integer | 否 | The time when the bid price was submitted to the exchange. |
| report_sequence | integer | 否 | The reporting sequence number. |
| sequence_number | integer | 否 | The unique sequence number assigned to this quote by the exchange. |
| session_end_date | string | 否 | Also known as the trading date, the date of the end of the trading session, in YYYY-MM-DD format. |
| ticker | string | 否 | The futures contract identifier, including the base symbol and contract expiration (e.g., GCJ5 for the April 2025 gold contract). |
| timestamp | integer | 否 | The time when the quote was generated at the exchange to nanosecond precision. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/futures/vX/quotes/{ticker}
```

### Request

```bash
curl -X GET "https://api.massive.com/futures/vX/quotes/GCJ5?limit=1000&sort=timestamp.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "next_url": "https://api.massive.com/futures/vX/quotes/GCJ5?cursor=YXA9MTczNDQ2MDIzMDcwODEyNjI4MSZhcz0mbGltaXQ9MTAwMCZzZXNzaW9uX2VuZF9kYXRlPTIwMjQtMTItMTcmc29ydD10aW1lc3RhbXAuZGVzYw",
  "request_id": "a47d1beb8c11b6ae897ab76cdbbf35a3",
  "results": [
    {
      "ask_timestamp": "1734472800076125400,",
      "bid_price": "2660,",
      "bid_size": "1,",
      "bid_timestamp": "1734472800076125400,",
      "report_sequence": "2250337,",
      "sequence_number": 15357766,
      "session_end_date": "2024-12-17,",
      "ticker": "GCJ5,",
      "timestamp": "1734472800076125400,"
    },
    {
      "ask_price": "2685.9,",
      "ask_size": "1,",
      "ask_timestamp": "1734472755134391800,",
      "bid_price": "2684.7,",
      "bid_size": "1,",
      "bid_timestamp": "1734472736352455200,",
      "report_sequence": "2249723,",
      "sequence_number": 15354716,
      "session_end_date": "2024-12-17,",
      "ticker": "GCJ5,",
      "timestamp": "1734472755134391800,"
    }
  ],
  "status": "OK"
}
```
