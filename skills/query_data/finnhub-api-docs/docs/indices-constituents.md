---
id: "url-833f120"
type: "api"
title: "Indices Constituents Premium"
url: "https://finnhub.io/docs/api/indices-constituents"
description: "Get a list of index's constituents. A list of supported indices for this endpoint can be found here."
source: ""
tags: []
crawl_time: "2026-03-18T09:26:53.536Z"
metadata:
  requestMethod: "GET"
  endpoint: "/index/constituents?symbol=^GSPC"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"symbol"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.indicesConstituents(\"^GSPC\", (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.indices_const(symbol = \"^GSPC\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.IndicesConstituents(context.Background()).Symbol(\"^GSPC\").Execute()"}
    - {"language":"PHP","code":"print_r($client->indicesConstituents(\"^GSPC\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.indices_constituents(\"^GSPC\"))"}
    - {"language":"Kotlin","code":"println(apiClient.indicesConstituents(\"^GSPC\"))"}
  sampleResponse: "{\n  \"constituents\": [\n    \"AAPL\",\n    \"MSFT\"\n  ],\n  \"constituentsBreakdown\": [\n    {\n      \"cusip\": \"037833100\",\n      \"isin\": \"US0378331005\",\n      \"name\": \"Apple Inc\",\n      \"shareClassFIGI\": \"BBG001S5N8V8\",\n      \"symbol\": \"AAPL\",\n      \"weight\": 7.03049\n    },\n    {\n      \"cusip\": \"594918104\",\n      \"isin\": \"US5949181045\",\n      \"name\": \"Microsoft Corp\",\n      \"shareClassFIGI\": \"BBG001S5TD05\",\n      \"symbol\": \"MSFT\",\n      \"weight\": 6.3839\n    }\n  ],\n  \"symbol\": \"^GSPC\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"constituents\": [\n    \"AAPL\",\n    \"MSFT\"\n  ],\n  \"constituentsBreakdown\": [\n    {\n      \"cusip\": \"037833100\",\n      \"isin\": \"US0378331005\",\n      \"name\": \"Apple Inc\",\n      \"shareClassFIGI\": \"BBG001S5N8V8\",\n      \"symbol\": \"AAPL\",\n      \"weight\": 7.03049\n    },\n    {\n      \"cusip\": \"594918104\",\n      \"isin\": \"US5949181045\",\n      \"name\": \"Microsoft Corp\",\n      \"shareClassFIGI\": \"BBG001S5TD05\",\n      \"symbol\": \"MSFT\",\n      \"weight\": 6.3839\n    }\n  ],\n  \"symbol\": \"^GSPC\"\n}"
  rawContent: "Indices Constituents Premium\n\nGet a list of index's constituents. A list of supported indices for this endpoint can be found here.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/index/constituents?symbol=^GSPC\n\nArguments:\n\nsymbolREQUIRED\n\nsymbol\n\nResponse Attributes:\n\nconstituents\n\nArray of constituents.\n\nconstituentsBreakdown\n\nArray of constituents' details.\n\ncusip\n\nCusip.\n\nisin\n\nISIN.\n\nname\n\nName.\n\nshareClassFIGI\n\nGlobal Share Class FIGI.\n\nsymbol\n\nSymbol.\n\nweight\n\nWeight.\n\nsymbol\n\nIndex's symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.indices_const(symbol = \"^GSPC\"))\n\nSample response\n\n{\n  \"constituents\": [\n    \"AAPL\",\n    \"MSFT\"\n  ],\n  \"constituentsBreakdown\": [\n    {\n      \"cusip\": \"037833100\",\n      \"isin\": \"US0378331005\",\n      \"name\": \"Apple Inc\",\n      \"shareClassFIGI\": \"BBG001S5N8V8\",\n      \"symbol\": \"AAPL\",\n      \"weight\": 7.03049\n    },\n    {\n      \"cusip\": \"594918104\",\n      \"isin\": \"US5949181045\",\n      \"name\": \"Microsoft Corp\",\n      \"shareClassFIGI\": \"BBG001S5TD05\",\n      \"symbol\": \"MSFT\",\n      \"weight\": 6.3839\n    }\n  ],\n  \"symbol\": \"^GSPC\"\n}"
  suggestedFilename: "indices-constituents"
---

# Indices Constituents Premium

## 源URL

https://finnhub.io/docs/api/indices-constituents

## 描述

Get a list of index's constituents. A list of supported indices for this endpoint can be found here.

## API 端点

**Method**: `GET`
**Endpoint**: `/index/constituents?symbol=^GSPC`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | symbol |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.indicesConstituents("^GSPC", (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.indices_const(symbol = "^GSPC"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.IndicesConstituents(context.Background()).Symbol("^GSPC").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->indicesConstituents("^GSPC"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.indices_constituents("^GSPC"))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.indicesConstituents("^GSPC"))
```

### 示例 7 (json)

```json
{
  "constituents": [
    "AAPL",
    "MSFT"
  ],
  "constituentsBreakdown": [
    {
      "cusip": "037833100",
      "isin": "US0378331005",
      "name": "Apple Inc",
      "shareClassFIGI": "BBG001S5N8V8",
      "symbol": "AAPL",
      "weight": 7.03049
    },
    {
      "cusip": "594918104",
      "isin": "US5949181045",
      "name": "Microsoft Corp",
      "shareClassFIGI": "BBG001S5TD05",
      "symbol": "MSFT",
      "weight": 6.3839
    }
  ],
  "symbol": "^GSPC"
}
```

## 文档正文

Get a list of index's constituents. A list of supported indices for this endpoint can be found here.

## API 端点

**Method:** `GET`
**Endpoint:** `/index/constituents?symbol=^GSPC`

Indices Constituents Premium

Get a list of index's constituents. A list of supported indices for this endpoint can be found here.

Method: GET

Premium: Premium Access Required

Examples:

/index/constituents?symbol=^GSPC

Arguments:

symbolREQUIRED

symbol

Response Attributes:

constituents

Array of constituents.

constituentsBreakdown

Array of constituents' details.

cusip

Cusip.

isin

ISIN.

name

Name.

shareClassFIGI

Global Share Class FIGI.

symbol

Symbol.

weight

Weight.

symbol

Index's symbol.

Sample code
cURL
Python
Javascript
Go
Ruby
Kotlin
PHP

import finnhub
finnhub_client = finnhub.Client(api_key="")

print(finnhub_client.indices_const(symbol = "^GSPC"))

Sample response

{
  "constituents": [
    "AAPL",
    "MSFT"
  ],
  "constituentsBreakdown": [
    {
      "cusip": "037833100",
      "isin": "US0378331005",
      "name": "Apple Inc",
      "shareClassFIGI": "BBG001S5N8V8",
      "symbol": "AAPL",
      "weight": 7.03049
    },
    {
      "cusip": "594918104",
      "isin": "US5949181045",
      "name": "Microsoft Corp",
      "shareClassFIGI": "BBG001S5TD05",
      "symbol": "MSFT",
      "weight": 6.3839
    }
  ],
  "symbol": "^GSPC"
}
