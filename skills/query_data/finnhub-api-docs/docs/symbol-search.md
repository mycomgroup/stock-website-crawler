---
id: "url-7005e30e"
type: "api"
title: "Symbol Lookup"
url: "https://finnhub.io/docs/api/symbol-search"
description: "Search for best-matching symbols based on your query. You can input anything from symbol, security's name to ISIN and Cusip."
source: ""
tags: []
crawl_time: "2026-03-18T04:45:45.316Z"
metadata:
  requestMethod: "GET"
  endpoint: "/search?q=apple&exchange=US"
  parameters:
    - {"name":"q","in":"query","required":true,"type":"string","description":"Query text can be symbol, name, isin, or cusip."}
    - {"name":"exchange","in":"query","required":false,"type":"string","description":"Exchange limit."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.symbolSearch('AAPL', (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.symbol_lookup('apple'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.SymbolSearch(context.Background()).Q(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->symbolSearch(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.symbol_search('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.symbolSearch(\"AAPL\"))"}
  sampleResponse: "{\n  \"count\": 4,\n  \"result\": [\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"AAPL\",\n      \"symbol\": \"AAPL\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"AAPL.SW\",\n      \"symbol\": \"AAPL.SW\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"APC.BE\",\n      \"symbol\": \"APC.BE\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"APC.DE\",\n      \"symbol\": \"APC.DE\",\n      \"type\": \"Common Stock\"\n    }\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"count\": 4,\n  \"result\": [\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"AAPL\",\n      \"symbol\": \"AAPL\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"AAPL.SW\",\n      \"symbol\": \"AAPL.SW\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"APC.BE\",\n      \"symbol\": \"APC.BE\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"APC.DE\",\n      \"symbol\": \"APC.DE\",\n      \"type\": \"Common Stock\"\n    }\n  ]\n}"
  rawContent: "Symbol Lookup\n\nSearch for best-matching symbols based on your query. You can input anything from symbol, security's name to ISIN and Cusip.\n\nMethod: GET\n\nExamples:\n\n/search?q=apple&exchange=US\n\n/search?q=US5949181045\n\nArguments:\n\nqREQUIRED\n\nQuery text can be symbol, name, isin, or cusip.\n\nexchangeoptional\n\nExchange limit.\n\nResponse Attributes:\n\ncount\n\nNumber of results.\n\nresult\n\nArray of search results.\n\ndescription\n\nSymbol description\n\ndisplaySymbol\n\nDisplay symbol name.\n\nsymbol\n\nUnique symbol used to identify this symbol used in /stock/candle endpoint.\n\ntype\n\nSecurity type.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.symbol_lookup('apple'))\n\nSample response\n\n{\n  \"count\": 4,\n  \"result\": [\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"AAPL\",\n      \"symbol\": \"AAPL\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"AAPL.SW\",\n      \"symbol\": \"AAPL.SW\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"APC.BE\",\n      \"symbol\": \"APC.BE\",\n      \"type\": \"Common Stock\"\n    },\n    {\n      \"description\": \"APPLE INC\",\n      \"displaySymbol\": \"APC.DE\",\n      \"symbol\": \"APC.DE\",\n      \"type\": \"Common Stock\"\n    }\n  ]\n}"
  suggestedFilename: "symbol-search"
---

# Symbol Lookup

## 源URL

https://finnhub.io/docs/api/symbol-search

## 描述

Search for best-matching symbols based on your query. You can input anything from symbol, security's name to ISIN and Cusip.

## API 端点

**Method**: `GET`
**Endpoint**: `/search?q=apple&exchange=US`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `q` | string | 是 | - | Query text can be symbol, name, isin, or cusip. |
| `exchange` | string | 否 | - | Exchange limit. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.symbolSearch('AAPL', (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.symbol_lookup('apple'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.SymbolSearch(context.Background()).Q("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->symbolSearch("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.symbol_search('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.symbolSearch("AAPL"))
```

### 示例 7 (json)

```json
{
  "count": 4,
  "result": [
    {
      "description": "APPLE INC",
      "displaySymbol": "AAPL",
      "symbol": "AAPL",
      "type": "Common Stock"
    },
    {
      "description": "APPLE INC",
      "displaySymbol": "AAPL.SW",
      "symbol": "AAPL.SW",
      "type": "Common Stock"
    },
    {
      "description": "APPLE INC",
      "displaySymbol": "APC.BE",
      "symbol": "APC.BE",
      "type": "Common Stock"
    },
    {
      "description": "APPLE INC",
      "displaySymbol": "APC.DE",
      "symbol": "APC.DE",
      "type": "Common Stock"
    }
  ]
}
```

## 文档正文

Search for best-matching symbols based on your query. You can input anything from symbol, security's name to ISIN and Cusip.

## API 端点

**Method:** `GET`
**Endpoint:** `/search?q=apple&exchange=US`

Symbol Lookup

Search for best-matching symbols based on your query. You can input anything from symbol, security's name to ISIN and Cusip.

Method: GET

Examples:

/search?q=apple&exchange=US

/search?q=US5949181045

Arguments:

qREQUIRED

Query text can be symbol, name, isin, or cusip.

exchangeoptional

Exchange limit.

Response Attributes:

count

Number of results.

result

Array of search results.

description

Symbol description

displaySymbol

Display symbol name.

symbol

Unique symbol used to identify this symbol used in /stock/candle endpoint.

type

Security type.

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

print(finnhub_client.symbol_lookup('apple'))

Sample response

{
  "count": 4,
  "result": [
    {
      "description": "APPLE INC",
      "displaySymbol": "AAPL",
      "symbol": "AAPL",
      "type": "Common Stock"
    },
    {
      "description": "APPLE INC",
      "displaySymbol": "AAPL.SW",
      "symbol": "AAPL.SW",
      "type": "Common Stock"
    },
    {
      "description": "APPLE INC",
      "displaySymbol": "APC.BE",
      "symbol": "APC.BE",
      "type": "Common Stock"
    },
    {
      "description": "APPLE INC",
      "displaySymbol": "APC.DE",
      "symbol": "APC.DE",
      "type": "Common Stock"
    }
  ]
}
