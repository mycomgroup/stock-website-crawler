---
id: "url-13566dbf"
type: "api"
title: "Forex Symbol"
url: "https://finnhub.io/docs/api/forex-symbols"
description: "List supported forex symbols."
source: ""
tags: []
crawl_time: "2026-03-18T06:27:24.377Z"
metadata:
  requestMethod: "GET"
  endpoint: "/forex/symbol?exchange=oanda"
  parameters:
    - {"name":"exchange","in":"query","required":true,"type":"string","description":"Exchange you want to get the list of symbols from."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.forexSymbols(\"OANDA\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.forex_symbols('OANDA'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.ForexSymbols(context.Background()).Exchange(\"OANDA\").Execute()"}
    - {"language":"PHP","code":"print_r($client->forexSymbols(\"OANDA\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.forex_symbols('OANDA'))"}
    - {"language":"Kotlin","code":"println(apiClient.forexSymbols(\"OANDA\"))"}
  sampleResponse: "[\n  {\n    \"description\": \"IC MARKETS Euro vs US Dollar EURUSD\",\n    \"displaySymbol\": \"EUR/USD\",\n    \"symbol\": \"IC MARKETS:1\"\n  },\n  {\n    \"description\": \"IC MARKETS Australian vs US Dollar AUDUSD\",\n    \"displaySymbol\": \"AUD/USD\",\n    \"symbol\": \"IC MARKETS:5\"\n  },\n  {\n    \"description\": \"IC MARKETS British Pound vs US Dollar GBPUSD\",\n    \"displaySymbol\": \"GBP/USD\",\n    \"symbol\": \"IC MARKETS:2\"\n  }]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"description\": \"IC MARKETS Euro vs US Dollar EURUSD\",\n    \"displaySymbol\": \"EUR/USD\",\n    \"symbol\": \"IC MARKETS:1\"\n  },\n  {\n    \"description\": \"IC MARKETS Australian vs US Dollar AUDUSD\",\n    \"displaySymbol\": \"AUD/USD\",\n    \"symbol\": \"IC MARKETS:5\"\n  },\n  {\n    \"description\": \"IC MARKETS British Pound vs US Dollar GBPUSD\",\n    \"displaySymbol\": \"GBP/USD\",\n    \"symbol\": \"IC MARKETS:2\"\n  }]"
  rawContent: "Forex Symbol\n\nList supported forex symbols.\n\nMethod: GET\n\nExamples:\n\n/forex/symbol?exchange=oanda\n\nArguments:\n\nexchangeREQUIRED\n\nExchange you want to get the list of symbols from.\n\nResponse Attributes:\n\ndescription\n\nSymbol description\n\ndisplaySymbol\n\nDisplay symbol name.\n\nsymbol\n\nUnique symbol used to identify this symbol used in /forex/candle endpoint.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.forex_symbols('OANDA'))\n\nSample response\n\n[\n  {\n    \"description\": \"IC MARKETS Euro vs US Dollar EURUSD\",\n    \"displaySymbol\": \"EUR/USD\",\n    \"symbol\": \"IC MARKETS:1\"\n  },\n  {\n    \"description\": \"IC MARKETS Australian vs US Dollar AUDUSD\",\n    \"displaySymbol\": \"AUD/USD\",\n    \"symbol\": \"IC MARKETS:5\"\n  },\n  {\n    \"description\": \"IC MARKETS British Pound vs US Dollar GBPUSD\",\n    \"displaySymbol\": \"GBP/USD\",\n    \"symbol\": \"IC MARKETS:2\"\n  }]"
  suggestedFilename: "forex-symbols"
---

# Forex Symbol

## 源URL

https://finnhub.io/docs/api/forex-symbols

## 描述

List supported forex symbols.

## API 端点

**Method**: `GET`
**Endpoint**: `/forex/symbol?exchange=oanda`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `exchange` | string | 是 | - | Exchange you want to get the list of symbols from. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.forexSymbols("OANDA", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.forex_symbols('OANDA'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.ForexSymbols(context.Background()).Exchange("OANDA").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->forexSymbols("OANDA"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.forex_symbols('OANDA'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.forexSymbols("OANDA"))
```

### 示例 7 (json)

```json
[
  {
    "description": "IC MARKETS Euro vs US Dollar EURUSD",
    "displaySymbol": "EUR/USD",
    "symbol": "IC MARKETS:1"
  },
  {
    "description": "IC MARKETS Australian vs US Dollar AUDUSD",
    "displaySymbol": "AUD/USD",
    "symbol": "IC MARKETS:5"
  },
  {
    "description": "IC MARKETS British Pound vs US Dollar GBPUSD",
    "displaySymbol": "GBP/USD",
    "symbol": "IC MARKETS:2"
  }]
```

## 文档正文

List supported forex symbols.

## API 端点

**Method:** `GET`
**Endpoint:** `/forex/symbol?exchange=oanda`

Forex Symbol

List supported forex symbols.

Method: GET

Examples:

/forex/symbol?exchange=oanda

Arguments:

exchangeREQUIRED

Exchange you want to get the list of symbols from.

Response Attributes:

description

Symbol description

displaySymbol

Display symbol name.

symbol

Unique symbol used to identify this symbol used in /forex/candle endpoint.

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

print(finnhub_client.forex_symbols('OANDA'))

Sample response

[
  {
    "description": "IC MARKETS Euro vs US Dollar EURUSD",
    "displaySymbol": "EUR/USD",
    "symbol": "IC MARKETS:1"
  },
  {
    "description": "IC MARKETS Australian vs US Dollar AUDUSD",
    "displaySymbol": "AUD/USD",
    "symbol": "IC MARKETS:5"
  },
  {
    "description": "IC MARKETS British Pound vs US Dollar GBPUSD",
    "displaySymbol": "GBP/USD",
    "symbol": "IC MARKETS:2"
  }]
