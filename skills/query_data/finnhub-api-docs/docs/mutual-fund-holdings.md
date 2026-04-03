---
id: "url-6ddd14f6"
type: "api"
title: "mutual-fund-holdings"
url: "https://finnhub.io/docs/api/mutual-fund-holdings"
description: "Get full Mutual Funds holdings/constituents. This endpoint covers both US and global mutual funds. For international funds, you must query the data using ISIN. A list of supported funds can be found here."
source: ""
tags: []
crawl_time: "2026-03-18T09:27:15.368Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/mutual-fund/holdings"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Fund's symbol."}
    - {"name":"isin","in":"query","required":false,"type":"string","description":"Fund's isin."}
    - {"name":"skip","in":"query","required":false,"type":"integer","description":"Skip the first n results. You can use this parameter to query historical constituents data. The latest result is returned if skip=0 or not set."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.mutualFundHoldings({'symbol': 'VTSAX'}, (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.mutual_fund_holdings(\"VTSAX\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.MutualFundHoldings(context.Background()).Symbol(\"VTSAX\").Execute()"}
    - {"language":"PHP","code":"print_r($client->mutualFundHoldings(\"VTSAX\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.mutual_fund_holdings({symbol:'VTSAX'}))"}
    - {"language":"Kotlin","code":"println(apiClient.mutualFundHoldings(\"VTSAX\", \"\", 0))"}
  sampleResponse: "{\n  \"atDate\": \"2023-01-31\",\n  \"holdings\": [\n    {\n      \"assetType\": \"Equity\",\n      \"cusip\": \"037833100\",\n      \"isin\": \"US0378331005\",\n      \"name\": \"Apple Inc\",\n      \"percent\": 5.36984,\n      \"share\": 463159883,\n      \"symbol\": \"AAPL\",\n      \"value\": 66829339518\n    },\n    {\n      \"assetType\": \"Equity\",\n      \"cusip\": \"594918104\",\n      \"isin\": \"US5949181045\",\n      \"name\": \"Microsoft Corp\",\n      \"percent\": 4.54903,\n      \"share\": 228457719,\n      \"symbol\": \"MSFT\",\n      \"value\": 56614107345\n    }\n  ],\n  \"numberOfHoldings\": 3972,\n  \"symbol\": \"VTSAX\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"atDate\": \"2023-01-31\",\n  \"holdings\": [\n    {\n      \"assetType\": \"Equity\",\n      \"cusip\": \"037833100\",\n      \"isin\": \"US0378331005\",\n      \"name\": \"Apple Inc\",\n      \"percent\": 5.36984,\n      \"share\": 463159883,\n      \"symbol\": \"AAPL\",\n      \"value\": 66829339518\n    },\n    {\n      \"assetType\": \"Equity\",\n      \"cusip\": \"594918104\",\n      \"isin\": \"US5949181045\",\n      \"name\": \"Microsoft Corp\",\n      \"percent\": 4.54903,\n      \"share\": 228457719,\n      \"symbol\": \"MSFT\",\n      \"value\": 56614107345\n    }\n  ],\n  \"numberOfHoldings\": 3972,\n  \"symbol\": \"VTSAX\"\n}"
  rawContent: ""
  suggestedFilename: "mutual-fund-holdings"
---

# mutual-fund-holdings

## 源URL

https://finnhub.io/docs/api/mutual-fund-holdings

## 描述

Get full Mutual Funds holdings/constituents. This endpoint covers both US and global mutual funds. For international funds, you must query the data using ISIN. A list of supported funds can be found here.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/mutual-fund/holdings`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Fund's symbol. |
| `isin` | string | 否 | - | Fund's isin. |
| `skip` | integer | 否 | - | Skip the first n results. You can use this parameter to query historical constituents data. The latest result is returned if skip=0 or not set. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.mutualFundHoldings({'symbol': 'VTSAX'}, (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.mutual_fund_holdings("VTSAX"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.MutualFundHoldings(context.Background()).Symbol("VTSAX").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->mutualFundHoldings("VTSAX"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.mutual_fund_holdings({symbol:'VTSAX'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.mutualFundHoldings("VTSAX", "", 0))
```

### 示例 7 (json)

```json
{
  "atDate": "2023-01-31",
  "holdings": [
    {
      "assetType": "Equity",
      "cusip": "037833100",
      "isin": "US0378331005",
      "name": "Apple Inc",
      "percent": 5.36984,
      "share": 463159883,
      "symbol": "AAPL",
      "value": 66829339518
    },
    {
      "assetType": "Equity",
      "cusip": "594918104",
      "isin": "US5949181045",
      "name": "Microsoft Corp",
      "percent": 4.54903,
      "share": 228457719,
      "symbol": "MSFT",
      "value": 56614107345
    }
  ],
  "numberOfHoldings": 3972,
  "symbol": "VTSAX"
}
```

## 文档正文

Get full Mutual Funds holdings/constituents. This endpoint covers both US and global mutual funds. For international funds, you must query the data using ISIN. A list of supported funds can be found here.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/mutual-fund/holdings`
