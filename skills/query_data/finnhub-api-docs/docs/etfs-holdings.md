---
id: "url-432cac76"
type: "api"
title: "etfs-holdings"
url: "https://finnhub.io/docs/api/etfs-holdings"
description: "Get full ETF holdings/constituents. This endpoint has global coverage. Widget only shows top 10 holdings. A list of supported ETFs can be found here."
source: ""
tags: []
crawl_time: "2026-03-18T06:27:07.615Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/etf/holdings"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"ETF symbol."}
    - {"name":"isin","in":"query","required":false,"type":"string","description":"ETF isin."}
    - {"name":"skip","in":"query","required":false,"type":"integer","description":"Skip the first n results. You can use this parameter to query historical constituents data. The latest result is returned if skip=0 or not set."}
    - {"name":"date","in":"query","required":false,"type":"string","description":"Query holdings by date. You can use either this param or skip param, not both."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.etfsHoldings({'symbol': 'ARKK'}, (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.etfs_holdings('SPY'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.EtfsHoldings(context.Background()).Symbol(\"SPY\").Execute()"}
    - {"language":"PHP","code":"print_r($client->etfsHoldings(\"SPY\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.etfs_holdings({symbol:'SPY'}))"}
    - {"language":"Kotlin","code":"println(apiClient.etfsHoldings(\"SPY\", \"\", 0, \"\"))"}
  sampleResponse: "{\n  \"atDate\": \"2023-03-24\",\n  \"holdings\": [\n    {\n      \"assetType\": \"Equity\",\n      \"cusip\": \"88160R101\",\n      \"isin\": \"US88160R1014\",\n      \"name\": \"TESLA INC\",\n      \"percent\": 10.54,\n      \"share\": 3971395,\n      \"symbol\": \"TSLA\",\n      \"value\": 763381546.9\n    },\n    {\n      \"assetType\": \"Equity\",\n      \"cusip\": \"98980L101\",\n      \"isin\": \"US98980L1017\",\n      \"name\": \"ZOOM VIDEO COMMUNICATIONS-A\",\n      \"percent\": 8.05,\n      \"share\": 8418916,\n      \"symbol\": \"ZM\",\n      \"value\": 582504798.04\n    },\n  ],\n  \"numberOfHoldings\": 28,\n  \"symbol\": \"ARKK\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"atDate\": \"2023-03-24\",\n  \"holdings\": [\n    {\n      \"assetType\": \"Equity\",\n      \"cusip\": \"88160R101\",\n      \"isin\": \"US88160R1014\",\n      \"name\": \"TESLA INC\",\n      \"percent\": 10.54,\n      \"share\": 3971395,\n      \"symbol\": \"TSLA\",\n      \"value\": 763381546.9\n    },\n    {\n      \"assetType\": \"Equity\",\n      \"cusip\": \"98980L101\",\n      \"isin\": \"US98980L1017\",\n      \"name\": \"ZOOM VIDEO COMMUNICATIONS-A\",\n      \"percent\": 8.05,\n      \"share\": 8418916,\n      \"symbol\": \"ZM\",\n      \"value\": 582504798.04\n    },\n  ],\n  \"numberOfHoldings\": 28,\n  \"symbol\": \"ARKK\"\n}"
  rawContent: ""
  suggestedFilename: "etfs-holdings"
---

# etfs-holdings

## 源URL

https://finnhub.io/docs/api/etfs-holdings

## 描述

Get full ETF holdings/constituents. This endpoint has global coverage. Widget only shows top 10 holdings. A list of supported ETFs can be found here.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/etf/holdings`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | ETF symbol. |
| `isin` | string | 否 | - | ETF isin. |
| `skip` | integer | 否 | - | Skip the first n results. You can use this parameter to query historical constituents data. The latest result is returned if skip=0 or not set. |
| `date` | string | 否 | - | Query holdings by date. You can use either this param or skip param, not both. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.etfsHoldings({'symbol': 'ARKK'}, (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.etfs_holdings('SPY'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.EtfsHoldings(context.Background()).Symbol("SPY").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->etfsHoldings("SPY"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.etfs_holdings({symbol:'SPY'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.etfsHoldings("SPY", "", 0, ""))
```

### 示例 7 (json)

```json
{
  "atDate": "2023-03-24",
  "holdings": [
    {
      "assetType": "Equity",
      "cusip": "88160R101",
      "isin": "US88160R1014",
      "name": "TESLA INC",
      "percent": 10.54,
      "share": 3971395,
      "symbol": "TSLA",
      "value": 763381546.9
    },
    {
      "assetType": "Equity",
      "cusip": "98980L101",
      "isin": "US98980L1017",
      "name": "ZOOM VIDEO COMMUNICATIONS-A",
      "percent": 8.05,
      "share": 8418916,
      "symbol": "ZM",
      "value": 582504798.04
    },
  ],
  "numberOfHoldings": 28,
  "symbol": "ARKK"
}
```

## 文档正文

Get full ETF holdings/constituents. This endpoint has global coverage. Widget only shows top 10 holdings. A list of supported ETFs can be found here.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/etf/holdings`
