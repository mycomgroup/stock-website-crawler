# All Tickers

## 源URL

https://massive.com/docs/rest/indices/tickers/all-tickers

## 描述

Retrieve a comprehensive list of ticker symbols supported by Massive across various asset classes (e.g., stocks, indices, forex, crypto). Each ticker entry provides essential details such as symbol, name, market, currency, and active status.

## Endpoint

```
GET /v3/reference/tickers
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a ticker symbol.<br>Defaults to empty string which queries all tickers. |
| type | enum (string) | 否 | Specify the type of the tickers. Find the types that we support via our Ticker Types API.<br>Defaults to empty string which queries all types. |
| market | enum (string) | 否 | Filter by market type. By default all markets are included. |
| exchange | string | 否 | Specify the asset's primary exchange Market Identifier Code (MIC) according to ISO 10383.<br>Defaults to empty string which queries all exchanges. |
| cusip | string | 否 | Specify the CUSIP code of the asset you want to search for. Find more information about CUSIP codes at their website.<br>Defaults to empty string which queries all CUSIPs.Note: Although you can query by CUSIP, due to legal reasons we do not return the CUSIP in the response. |
| cik | string | 否 | Specify the CIK of the asset you want to search for. Find more information about CIK codes at their website.<br>Defaults to empty string which queries all CIKs. |
| date | string | 否 | Specify a point in time to retrieve tickers available on that date.<br>Defaults to the most recent available date. |
| search | string | 否 | Search for terms within the ticker and/or company name. |
| active | boolean | 否 | Specify if the tickers returned should be actively traded on the queried date. Default is true. |
| order | enum (string) | 否 | Order results based on the `sort` field. |
| limit | integer | 否 | Limit the number of results returned, default is 100 and max is 1000. |
| sort | enum (string) | 否 | Sort field used for ordering. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| count | integer | 否 | The total number of results for this request. |
| next_url | string | 否 | If present, this value can be used to fetch the next page of data. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | An array of tickers that match your query.Note: Although you can query by CUSIP, due to legal reasons we do not return the CUSIP in the response. |
| active | boolean | 否 | Whether or not the asset is actively traded. False means the asset has been delisted. |
| base_currency_name | string | 否 | The name of the currency that this asset is priced against. |
| base_currency_symbol | string | 否 | The ISO 4217 code of the currency that this asset is priced against. |
| cik | string | 否 | The CIK number for this ticker. Find more information here. |
| composite_figi | string | 否 | The composite OpenFIGI number for this ticker. Find more information here |
| currency_name | string | 否 | The name of the currency that this asset is traded with. |
| currency_symbol | string | 否 | The ISO 4217 code of the currency that this asset is traded with. |
| delisted_utc | string | 否 | The last date that the asset was traded. |
| last_updated_utc | string | 否 | The information is accurate up to this time. |
| locale | enum | 否 | The locale of the asset. |
| market | enum | 否 | The market type of the asset. |
| name | string | 否 | The name of the asset. For stocks/equities this will be the companies registered name. For crypto/fx this will be the name of the currency or coin pair. |
| primary_exchange | string | 否 | The ISO code of the primary listing exchange for this asset. |
| share_class_figi | string | 否 | The share Class OpenFIGI number for this ticker. Find more information here |
| ticker | string | 否 | The exchange symbol that this item is traded under. |
| type | string | 否 | The type of the asset. Find the types that we support via our Ticker Types API. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/v3/reference/tickers
```

### Request

```bash
curl -X GET "https://api.massive.com/v3/reference/tickers?market=indices&active=true&order=asc&limit=100&sort=ticker&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "next_url": "https://api.massive.com/v3/reference/tickers?cursor=YWN0aXZlPXRydWUmZGF0ZT0yMDIxLTA0LTI1JmxpbWl0PTEmb3JkZXI9YXNjJnBhZ2VfbWFya2VyPUElN0M5YWRjMjY0ZTgyM2E1ZjBiOGUyNDc5YmZiOGE1YmYwNDVkYzU0YjgwMDcyMWE2YmI1ZjBjMjQwMjU4MjFmNGZiJnNvcnQ9dGlja2Vy",
  "request_id": "e70013d92930de90e089dc8fa098888e",
  "results": [
    {
      "active": true,
      "cik": "0001090872",
      "composite_figi": "BBG000BWQYZ5",
      "currency_name": "usd",
      "last_updated_utc": "2021-04-25T00:00:00Z",
      "locale": "us",
      "market": "stocks",
      "name": "Agilent Technologies Inc.",
      "primary_exchange": "XNYS",
      "share_class_figi": "BBG001SCTQY4",
      "ticker": "A",
      "type": "CS"
    }
  ],
  "status": "OK"
}
```
