---
id: "url-7a63a325"
type: "api"
title: "Crypto Candles Premium"
url: "https://finnhub.io/docs/api/crypto-candles"
description: "Get candlestick data for crypto symbols."
source: ""
tags: []
crawl_time: "2026-03-18T06:58:50.605Z"
metadata:
  requestMethod: "GET"
  endpoint: "/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=D&from=1572651390&to=1575243390"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Use symbol returned in /crypto/symbol endpoint for this field."}
    - {"name":"resolution","in":"query","required":true,"type":"string","description":"Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange."}
    - {"name":"from","in":"query","required":true,"type":"integer","description":"UNIX timestamp. Interval initial value."}
    - {"name":"to","in":"query","required":true,"type":"integer","description":"UNIX timestamp. Interval end value."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.cryptoCandles(\"BINANCE:BTCUSDT\", \"D\", 1590988249, 1591852249, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', 1590988249, 1591852249))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.CryptoCandles(context.Background()).Symbol(\"BINANCE:BTCUSDT\").Resolution(\"D\").From(1590988249).To(1591852249).Execute()"}
    - {"language":"PHP","code":"print_r($client->cryptoCandles(\"BINANCE:BTCUSDT\", \"D\", 1590988249, 1591852249));"}
    - {"language":"Ruby","code":"puts(finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', 1590988249, 1591852249))"}
    - {"language":"Kotlin","code":"println(apiClient.cryptoCandles(\"BINANCE:BTCUSDT\", \"D\", 1590988249, 1591852249))"}
  sampleResponse: "{\n  \"c\": [\n    1.10713,\n    1.10288,\n    1.10397,\n    1.10182\n  ],\n  \"h\": [\n    1.1074,\n    1.10751,\n    1.10729,\n    1.10595\n  ],\n  \"l\": [\n    1.09897,\n    1.1013,\n    1.10223,\n    1.10101\n  ],\n  \"o\": [\n    1.0996,\n    1.107,\n    1.10269,\n    1.10398\n  ],\n  \"s\": \"ok\",\n  \"t\": [\n    1568667600,\n    1568754000,\n    1568840400,\n    1568926800\n  ],\n  \"v\": [\n    75789,\n    75883,\n    73485,\n    5138\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"c\": [\n    1.10713,\n    1.10288,\n    1.10397,\n    1.10182\n  ],\n  \"h\": [\n    1.1074,\n    1.10751,\n    1.10729,\n    1.10595\n  ],\n  \"l\": [\n    1.09897,\n    1.1013,\n    1.10223,\n    1.10101\n  ],\n  \"o\": [\n    1.0996,\n    1.107,\n    1.10269,\n    1.10398\n  ],\n  \"s\": \"ok\",\n  \"t\": [\n    1568667600,\n    1568754000,\n    1568840400,\n    1568926800\n  ],\n  \"v\": [\n    75789,\n    75883,\n    73485,\n    5138\n  ]\n}"
  rawContent: "Crypto Candles Premium\n\nGet candlestick data for crypto symbols.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=D&from=1572651390&to=1575243390\n\nArguments:\n\nsymbolREQUIRED\n\nUse symbol returned in /crypto/symbol endpoint for this field.\n\nresolutionREQUIRED\n\nSupported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.\n\nfromREQUIRED\n\nUNIX timestamp. Interval initial value.\n\ntoREQUIRED\n\nUNIX timestamp. Interval end value.\n\nResponse Attributes:\n\nc\n\nList of close prices for returned candles.\n\nh\n\nList of high prices for returned candles.\n\nl\n\nList of low prices for returned candles.\n\no\n\nList of open prices for returned candles.\n\ns\n\nStatus of the response. This field can either be ok or no_data.\n\nt\n\nList of timestamp for returned candles.\n\nv\n\nList of volume data for returned candles.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', 1590988249, 1591852249))\n\nSample response\n\n{\n  \"c\": [\n    1.10713,\n    1.10288,\n    1.10397,\n    1.10182\n  ],\n  \"h\": [\n    1.1074,\n    1.10751,\n    1.10729,\n    1.10595\n  ],\n  \"l\": [\n    1.09897,\n    1.1013,\n    1.10223,\n    1.10101\n  ],\n  \"o\": [\n    1.0996,\n    1.107,\n    1.10269,\n    1.10398\n  ],\n  \"s\": \"ok\",\n  \"t\": [\n    1568667600,\n    1568754000,\n    1568840400,\n  ],\n  \"v\": [\n    75789,\n    75883,\n    73485,\n  ]\n}\n\nWidget:"
  suggestedFilename: "crypto-candles"
---

# Crypto Candles Premium

## 源URL

https://finnhub.io/docs/api/crypto-candles

## 描述

Get candlestick data for crypto symbols.

## API 端点

**Method**: `GET`
**Endpoint**: `/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=D&from=1572651390&to=1575243390`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Use symbol returned in /crypto/symbol endpoint for this field. |
| `resolution` | string | 是 | - | Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange. |
| `from` | integer | 是 | - | UNIX timestamp. Interval initial value. |
| `to` | integer | 是 | - | UNIX timestamp. Interval end value. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.cryptoCandles("BINANCE:BTCUSDT", "D", 1590988249, 1591852249, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', 1590988249, 1591852249))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.CryptoCandles(context.Background()).Symbol("BINANCE:BTCUSDT").Resolution("D").From(1590988249).To(1591852249).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->cryptoCandles("BINANCE:BTCUSDT", "D", 1590988249, 1591852249));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', 1590988249, 1591852249))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.cryptoCandles("BINANCE:BTCUSDT", "D", 1590988249, 1591852249))
```

### 示例 7 (json)

```json
{
  "c": [
    1.10713,
    1.10288,
    1.10397,
    1.10182
  ],
  "h": [
    1.1074,
    1.10751,
    1.10729,
    1.10595
  ],
  "l": [
    1.09897,
    1.1013,
    1.10223,
    1.10101
  ],
  "o": [
    1.0996,
    1.107,
    1.10269,
    1.10398
  ],
  "s": "ok",
  "t": [
    1568667600,
    1568754000,
    1568840400,
    1568926800
  ],
  "v": [
    75789,
    75883,
    73485,
    5138
  ]
}
```

## 文档正文

Get candlestick data for crypto symbols.

## API 端点

**Method:** `GET`
**Endpoint:** `/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=D&from=1572651390&to=1575243390`

Crypto Candles Premium

Get candlestick data for crypto symbols.

Method: GET

Premium: Premium Access Required

Examples:

/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=D&from=1572651390&to=1575243390

Arguments:

symbolREQUIRED

Use symbol returned in /crypto/symbol endpoint for this field.

resolutionREQUIRED

Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.

fromREQUIRED

UNIX timestamp. Interval initial value.

toREQUIRED

UNIX timestamp. Interval end value.

Response Attributes:

c

List of close prices for returned candles.

h

List of high prices for returned candles.

l

List of low prices for returned candles.

o

List of open prices for returned candles.

s

Status of the response. This field can either be ok or no_data.

t

List of timestamp for returned candles.

v

List of volume data for returned candles.

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

print(finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', 1590988249, 1591852249))

Sample response

{
  "c": [
    1.10713,
    1.10288,
    1.10397,
    1.10182
  ],
  "h": [
    1.1074,
    1.10751,
    1.10729,
    1.10595
  ],
  "l": [
    1.09897,
    1.1013,
    1.10223,
    1.10101
  ],
  "o": [
    1.0996,
    1.107,
    1.10269,
    1.10398
  ],
  "s": "ok",
  "t": [
    1568667600,
    1568754000,
    1568840400,
  ],
  "v": [
    75789,
    75883,
    73485,
  ]
}

Widget:
