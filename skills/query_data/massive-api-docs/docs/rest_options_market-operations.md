# Exchanges

## 源URL

https://massive.com/docs/rest/options/market-operations

## 描述

Retrieve a list of known exchanges, including their identifiers, names, market types, and other relevant attributes. This information helps map exchange codes, understand market coverage, and integrate exchange details into applications.

## Endpoint

```
GET /v3/reference/exchanges
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
| acronym | string | 否 | A commonly used abbreviation for this exchange. |
| asset_class | enum | 否 | An identifier for a group of similar financial instruments. |
| id | integer | 否 | A unique identifier used by Massive for this exchange. |
| locale | enum | 否 | An identifier for a geographical location. |
| mic | string | 否 | The Market Identifier Code of this exchange (see ISO 10383). |
| name | string | 否 | Name of this exchange. |
| operating_mic | string | 否 | The MIC of the entity that operates this exchange. |
| participant_id | string | 否 | The ID used by SIP's to represent this exchange. |
| type | enum | 否 | Represents the type of exchange. |
| url | string | 否 | A link to this exchange's website, if one exists. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/v3/reference/exchanges
```

### Request

```bash
curl -X GET "https://api.massive.com/v3/reference/exchanges?asset_class=options&locale=us&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": "31d59dda-80e5-4721-8496-d0d32a654afe",
  "results": {
    "acronym": "AMEX",
    "asset_class": "stocks",
    "id": 1,
    "locale": "us",
    "mic": "XASE",
    "name": "NYSE American, LLC",
    "operating_mic": "XNYS",
    "participant_id": "A",
    "type": "exchange",
    "url": "https://www.nyse.com/markets/nyse-american"
  },
  "status": "OK"
}
```
