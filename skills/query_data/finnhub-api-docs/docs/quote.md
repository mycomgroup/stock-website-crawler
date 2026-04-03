---
id: "url-4329bf0f"
type: "api"
title: "Quote"
url: "https://finnhub.io/docs/api/quote"
description: "Get real-time quote data for US stocks. Constant polling is not recommended. Use websocket if you need real-time updates.Real-time stock prices for international markets are supported for Enterprise clients via our partner's feed. Contact Us to learn more."
source: ""
tags: []
crawl_time: "2026-03-18T03:12:22.130Z"
metadata:
  requestMethod: "GET"
  endpoint: "/quote?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.quote(\"AAPL\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.quote('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.Quote(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->quote(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.quote('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.quote(\"AAPL\"))"}
  sampleResponse: "{\n  \"c\": 261.74,\n  \"h\": 263.31,\n  \"l\": 260.68,\n  \"o\": 261.07,\n  \"pc\": 259.45,\n  \"t\": 1582641000 \n}"
  curlExample: ""
  jsonExample: "{\n  \"c\": 261.74,\n  \"h\": 263.31,\n  \"l\": 260.68,\n  \"o\": 261.07,\n  \"pc\": 259.45,\n  \"t\": 1582641000 \n}"
  rawContent: "Quote\n\nGet real-time quote data for US stocks. Constant polling is not recommended. Use websocket if you need real-time updates.\n\nReal-time stock prices for international markets are supported for Enterprise clients via our partner's feed. Contact Us to learn more.\n\nMethod: GET\n\nExamples:\n\n/quote?symbol=AAPL\n\n/quote?symbol=MSFT\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol\n\nResponse Attributes:\n\nc\n\nCurrent price\n\nd\n\nChange\n\ndp\n\nPercent change\n\nh\n\nHigh price of the day\n\nl\n\nLow price of the day\n\no\n\nOpen price of the day\n\npc\n\nPrevious close price\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.quote('AAPL'))\n\nSample response\n\n{\n  \"c\": 261.74,\n  \"h\": 263.31,\n  \"l\": 260.68,\n  \"o\": 261.07,\n  \"pc\": 259.45,\n  \"t\": 1582641000 \n}"
  suggestedFilename: "quote"
---

# Quote

## 源URL

https://finnhub.io/docs/api/quote

## 描述

Get real-time quote data for US stocks. Constant polling is not recommended. Use websocket if you need real-time updates.Real-time stock prices for international markets are supported for Enterprise clients via our partner's feed. Contact Us to learn more.

## API 端点

**Method**: `GET`
**Endpoint**: `/quote?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.quote("AAPL", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.quote('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.Quote(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->quote("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.quote('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.quote("AAPL"))
```

### 示例 7 (json)

```json
{
  "c": 261.74,
  "h": 263.31,
  "l": 260.68,
  "o": 261.07,
  "pc": 259.45,
  "t": 1582641000 
}
```

## 文档正文

Get real-time quote data for US stocks. Constant polling is not recommended. Use websocket if you need real-time updates.Real-time stock prices for international markets are supported for Enterprise clients via our partner's feed. Contact Us to learn more.

## API 端点

**Method:** `GET`
**Endpoint:** `/quote?symbol=AAPL`

Quote

Get real-time quote data for US stocks. Constant polling is not recommended. Use websocket if you need real-time updates.

Real-time stock prices for international markets are supported for Enterprise clients via our partner's feed. Contact Us to learn more.

Method: GET

Examples:

/quote?symbol=AAPL

/quote?symbol=MSFT

Arguments:

symbolREQUIRED

Symbol

Response Attributes:

c

Current price

d

Change

dp

Percent change

h

High price of the day

l

Low price of the day

o

Open price of the day

pc

Previous close price

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

print(finnhub_client.quote('AAPL'))

Sample response

{
  "c": 261.74,
  "h": 263.31,
  "l": 260.68,
  "o": 261.07,
  "pc": 259.45,
  "t": 1582641000 
}
