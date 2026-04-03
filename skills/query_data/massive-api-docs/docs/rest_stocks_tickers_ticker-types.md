# Ticker Types

## 源URL

https://massive.com/docs/rest/stocks/tickers/ticker-types

## 描述

Retrieve a list of all ticker types supported by Massive. This endpoint categorizes tickers across asset classes, markets, and instruments, helping users understand the different classifications and their attributes.

## Endpoint

```
GET /v3/reference/tickers/types
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| asset_class | enum (string) | 否 | Filter by asset class. |
| locale | enum (string) | 否 | Filter by locale. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| count | integer | 否 | The total number of results for this request. |
| request_id | string | 否 | A request ID assigned by the server. |
| results | array (object) | 否 | An array of results containing the requested data. |
| asset_class | enum | 否 | An identifier for a group of similar financial instruments. |
| code | string | 否 | A code used by Massive to refer to this ticker type. |
| description | string | 否 | A short description of this ticker type. |
| locale | enum | 否 | An identifier for a geographical location. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/v3/reference/tickers/types
```

### Request

```bash
curl -X GET "https://api.massive.com/v3/reference/tickers/types?asset_class=stocks&locale=us&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": "31d59dda-80e5-4721-8496-d0d32a654afe",
  "results": {
    "asset_class": "stocks",
    "code": "CS",
    "description": "Common Stock",
    "locale": "us"
  },
  "status": "OK"
}
```
