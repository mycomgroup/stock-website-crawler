---
id: "url-e534e06"
type: "api"
title: "Crypto Symbol"
url: "https://finnhub.io/docs/api/crypto-symbols"
description: "List supported crypto symbols by exchange"
source: ""
tags: []
crawl_time: "2026-03-18T06:58:29.063Z"
metadata:
  requestMethod: "GET"
  endpoint: "/crypto/symbol?exchange=binance"
  parameters:
    - {"name":"exchange","in":"query","required":true,"type":"string","description":"Exchange you want to get the list of symbols from."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.cryptoSymbols(\"BINANCE\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.crypto_symbols('BINANCE'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.CryptoSymbols(context.Background()).Exchange(\"BINANCE\").Execute()"}
    - {"language":"PHP","code":"print_r($client->cryptoSymbols(\"BINANCE\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.crypto_symbols('BINANCE'))"}
    - {"language":"Kotlin","code":"println(apiClient.cryptoSymbols(\"BINANCE\"))"}
  sampleResponse: "[\n  {\n    \"description\": \"Binance ETHBTC\",\n    \"displaySymbol\": \"ETH/BTC\",\n    \"symbol\": \"ETHBTC\"\n  },\n  {\n    \"description\": \"Binance LTCBTC\",\n    \"displaySymbol\": \"LTC/BTC\",\n    \"symbol\": \"BINANCE:LTCBTC\"\n  },\n  {\n    \"description\": \"Binance BNBBTC\",\n    \"displaySymbol\": \"BNB/BTC\",\n    \"symbol\": \"BINANCE:BNBBTC\"\n  }]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"description\": \"Binance ETHBTC\",\n    \"displaySymbol\": \"ETH/BTC\",\n    \"symbol\": \"ETHBTC\"\n  },\n  {\n    \"description\": \"Binance LTCBTC\",\n    \"displaySymbol\": \"LTC/BTC\",\n    \"symbol\": \"BINANCE:LTCBTC\"\n  },\n  {\n    \"description\": \"Binance BNBBTC\",\n    \"displaySymbol\": \"BNB/BTC\",\n    \"symbol\": \"BINANCE:BNBBTC\"\n  }]"
  rawContent: "Crypto Symbol\n\nList supported crypto symbols by exchange\n\nMethod: GET\n\nExamples:\n\n/crypto/symbol?exchange=binance\n\nArguments:\n\nexchangeREQUIRED\n\nExchange you want to get the list of symbols from.\n\nResponse Attributes:\n\ndescription\n\nSymbol description\n\ndisplaySymbol\n\nDisplay symbol name.\n\nsymbol\n\nUnique symbol used to identify this symbol used in /crypto/candle endpoint.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.crypto_symbols('BINANCE'))\n\nSample response\n\n[\n  {\n    \"description\": \"Binance ETHBTC\",\n    \"displaySymbol\": \"ETH/BTC\",\n    \"symbol\": \"ETHBTC\"\n  },\n  {\n    \"description\": \"Binance LTCBTC\",\n    \"displaySymbol\": \"LTC/BTC\",\n    \"symbol\": \"BINANCE:LTCBTC\"\n  },\n  {\n    \"description\": \"Binance BNBBTC\",\n    \"displaySymbol\": \"BNB/BTC\",\n    \"symbol\": \"BINANCE:BNBBTC\"\n  }]"
  suggestedFilename: "crypto-symbols"
---

# Crypto Symbol

## 源URL

https://finnhub.io/docs/api/crypto-symbols

## 描述

List supported crypto symbols by exchange

## API 端点

**Method**: `GET`
**Endpoint**: `/crypto/symbol?exchange=binance`

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
finnhubClient.cryptoSymbols("BINANCE", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.crypto_symbols('BINANCE'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.CryptoSymbols(context.Background()).Exchange("BINANCE").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->cryptoSymbols("BINANCE"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.crypto_symbols('BINANCE'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.cryptoSymbols("BINANCE"))
```

### 示例 7 (json)

```json
[
  {
    "description": "Binance ETHBTC",
    "displaySymbol": "ETH/BTC",
    "symbol": "ETHBTC"
  },
  {
    "description": "Binance LTCBTC",
    "displaySymbol": "LTC/BTC",
    "symbol": "BINANCE:LTCBTC"
  },
  {
    "description": "Binance BNBBTC",
    "displaySymbol": "BNB/BTC",
    "symbol": "BINANCE:BNBBTC"
  }]
```

## 文档正文

List supported crypto symbols by exchange

## API 端点

**Method:** `GET`
**Endpoint:** `/crypto/symbol?exchange=binance`

Crypto Symbol

List supported crypto symbols by exchange

Method: GET

Examples:

/crypto/symbol?exchange=binance

Arguments:

exchangeREQUIRED

Exchange you want to get the list of symbols from.

Response Attributes:

description

Symbol description

displaySymbol

Display symbol name.

symbol

Unique symbol used to identify this symbol used in /crypto/candle endpoint.

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

print(finnhub_client.crypto_symbols('BINANCE'))

Sample response

[
  {
    "description": "Binance ETHBTC",
    "displaySymbol": "ETH/BTC",
    "symbol": "ETHBTC"
  },
  {
    "description": "Binance LTCBTC",
    "displaySymbol": "LTC/BTC",
    "symbol": "BINANCE:LTCBTC"
  },
  {
    "description": "Binance BNBBTC",
    "displaySymbol": "BNB/BTC",
    "symbol": "BINANCE:BNBBTC"
  }]
