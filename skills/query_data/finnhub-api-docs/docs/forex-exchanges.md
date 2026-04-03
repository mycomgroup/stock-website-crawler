---
id: "url-c4cfd94"
type: "api"
title: "Forex Exchanges"
url: "https://finnhub.io/docs/api/forex-exchanges"
description: "List supported forex exchanges"
source: ""
tags: []
crawl_time: "2026-03-18T07:30:31.486Z"
metadata:
  requestMethod: "GET"
  endpoint: "/forex/exchange"
  parameters: []
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.forexExchanges((error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.forex_exchanges())"}
    - {"language":"Go","code":"res, _, err := finnhubClient.ForexExchanges(context.Background()).Execute()"}
    - {"language":"PHP","code":"print_r($client->forexExchanges());"}
    - {"language":"Ruby","code":"puts(finnhub_client.forex_exchanges())"}
    - {"language":"Kotlin","code":"println(apiClient.forexExchanges())"}
  sampleResponse: "[\n  \"oanda\",\n  \"fxcm\",\n  \"forex.com\",\n  \"ic markets\",\n  \"fxpro\"\n]"
  curlExample: ""
  jsonExample: "[\n  \"oanda\",\n  \"fxcm\",\n  \"forex.com\",\n  \"ic markets\",\n  \"fxpro\"\n]"
  rawContent: "Forex Exchanges\n\nList supported forex exchanges\n\nMethod: GET\n\nExamples:\n\n/forex/exchange\n\nArguments:\n\nResponse Attributes:\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.forex_exchanges())\n\nSample response\n\n[\n  \"oanda\",\n  \"fxcm\",\n  \"forex.com\",\n  \"ic markets\",\n  \"fxpro\"\n]"
  suggestedFilename: "forex-exchanges"
---

# Forex Exchanges

## 源URL

https://finnhub.io/docs/api/forex-exchanges

## 描述

List supported forex exchanges

## API 端点

**Method**: `GET`
**Endpoint**: `/forex/exchange`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.forexExchanges((error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.forex_exchanges())
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.ForexExchanges(context.Background()).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->forexExchanges());
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.forex_exchanges())
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.forexExchanges())
```

### 示例 7 (json)

```json
[
  "oanda",
  "fxcm",
  "forex.com",
  "ic markets",
  "fxpro"
]
```

## 文档正文

List supported forex exchanges

## API 端点

**Method:** `GET`
**Endpoint:** `/forex/exchange`

Forex Exchanges

List supported forex exchanges

Method: GET

Examples:

/forex/exchange

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

print(finnhub_client.forex_exchanges())

Sample response

[
  "oanda",
  "fxcm",
  "forex.com",
  "ic markets",
  "fxpro"
]
