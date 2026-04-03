# Exchanges

## 源URL

https://massive.com/docs/rest/futures/market-operations/exchanges

## 描述

Retrieve a list of supported futures exchanges, including their unique exchange codes, names, and other important details.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '999'. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| acronym | string | 否 | Well-known acronym for the exchange (e.g., 'CME', 'NYMEX', 'CBOT', 'COMEX'). |
| id | string | 否 | Numeric identifier for the futures exchange or trading venue. |
| locale | string | 否 | Geographic location code where the exchange operates. |
| mic | string | 否 | Market Identifier Code (MIC) - ISO 10383 standard four-character code for the futures market. |
| name | string | 否 | Full official name of the futures exchange (e.g., 'Chicago Mercantile Exchange', 'New York Mercantile Exchange'). |
| operating_mic | string | 否 | Operating Market Identifier Code for the futures exchange. |
| type | string | 否 | Type of venue - 'exchange' for futures exchanges and derivatives trading platforms. |
| url | string | 否 | Official website URL of the futures exchange organization. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/futures/vX/exchanges
```

### Request

```bash
curl -X GET "https://api.massive.com/futures/vX/exchanges?limit=100&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "acronym": "CME",
      "id": "4",
      "locale": "US",
      "mic": "XCME",
      "name": "Chicago Mercantile Exchange",
      "operating_mic": "XCME",
      "type": "exchange",
      "url": "https://cmegroup.com"
    }
  ],
  "status": "OK"
}
```
