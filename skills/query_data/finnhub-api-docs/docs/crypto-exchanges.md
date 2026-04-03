---
id: "url-51dce0f1"
type: "api"
title: "Crypto Exchanges"
url: "https://finnhub.io/docs/api/crypto-exchanges"
description: "List supported crypto exchanges"
source: ""
tags: []
crawl_time: "2026-03-18T07:31:46.453Z"
metadata:
  requestMethod: "GET"
  endpoint: "/crypto/exchange"
  parameters: []
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.cryptoExchanges((error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.crypto_exchanges())"}
    - {"language":"Go","code":"res, _, err := finnhubClient.CryptoExchanges(context.Background()).Execute()"}
    - {"language":"PHP","code":"print_r($client->cryptoExchanges());"}
    - {"language":"Ruby","code":"puts(finnhub_client.crypto_exchanges())"}
    - {"language":"Kotlin","code":"println(apiClient.cryptoExchanges())"}
  sampleResponse: "[\n  \"KRAKEN\",\n  \"HITBTC\",\n  \"COINBASE\",\n  \"GEMINI\",\n  \"POLONIEX\",\n  \"Binance\",\n  \"ZB\",\n  \"BITTREX\",\n  \"KUCOIN\",\n  \"OKEX\",\n  \"BITFINEX\",\n  \"HUOBI\"\n]"
  curlExample: ""
  jsonExample: "[\n  \"KRAKEN\",\n  \"HITBTC\",\n  \"COINBASE\",\n  \"GEMINI\",\n  \"POLONIEX\",\n  \"Binance\",\n  \"ZB\",\n  \"BITTREX\",\n  \"KUCOIN\",\n  \"OKEX\",\n  \"BITFINEX\",\n  \"HUOBI\"\n]"
  rawContent: "Crypto Exchanges\n\nList supported crypto exchanges\n\nMethod: GET\n\nExamples:\n\n/crypto/exchange\n\nArguments:\n\nResponse Attributes:\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.crypto_exchanges())\n\nSample response\n\n[\n  \"KRAKEN\",\n  \"HITBTC\",\n  \"COINBASE\",\n  \"GEMINI\",\n  \"POLONIEX\",\n  \"Binance\",\n  \"ZB\",\n  \"BITTREX\",\n  \"KUCOIN\",\n  \"OKEX\",\n  \"BITFINEX\",\n  \"HUOBI\"\n]"
  suggestedFilename: "crypto-exchanges"
---

# Crypto Exchanges

## 源URL

https://finnhub.io/docs/api/crypto-exchanges

## 描述

List supported crypto exchanges

## API 端点

**Method**: `GET`
**Endpoint**: `/crypto/exchange`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.cryptoExchanges((error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.crypto_exchanges())
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.CryptoExchanges(context.Background()).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->cryptoExchanges());
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.crypto_exchanges())
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.cryptoExchanges())
```

### 示例 7 (json)

```json
[
  "KRAKEN",
  "HITBTC",
  "COINBASE",
  "GEMINI",
  "POLONIEX",
  "Binance",
  "ZB",
  "BITTREX",
  "KUCOIN",
  "OKEX",
  "BITFINEX",
  "HUOBI"
]
```

## 文档正文

List supported crypto exchanges

## API 端点

**Method:** `GET`
**Endpoint:** `/crypto/exchange`

Crypto Exchanges

List supported crypto exchanges

Method: GET

Examples:

/crypto/exchange

Arguments:

Response Attributes:

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

print(finnhub_client.crypto_exchanges())

Sample response

[
  "KRAKEN",
  "HITBTC",
  "COINBASE",
  "GEMINI",
  "POLONIEX",
  "Binance",
  "ZB",
  "BITTREX",
  "KUCOIN",
  "OKEX",
  "BITFINEX",
  "HUOBI"
]
