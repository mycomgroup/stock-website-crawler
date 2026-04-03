---
id: "url-1bf01680"
type: "api"
title: "Price Target Premium"
url: "https://finnhub.io/docs/api/price-target"
description: "Get latest price target consensus."
source: ""
tags: []
crawl_time: "2026-03-18T04:35:52.185Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/price-target?symbol=NFLX"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.priceTarget('AAPL', (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.price_target('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.PriceTarget(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->priceTarget(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.price_target('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.priceTarget(\"AAPL\"))"}
  sampleResponse: "{\n  \"lastUpdated\": \"2023-04-06 00:00:00\",\n  \"numberAnalysts\": 39,\n  \"symbol\": \"NFLX\",\n  \"targetHigh\": 462,\n  \"targetLow\": 217.15,\n  \"targetMean\": 364.37,\n  \"targetMedian\": 359.04\n}"
  curlExample: ""
  jsonExample: "{\n  \"lastUpdated\": \"2023-04-06 00:00:00\",\n  \"numberAnalysts\": 39,\n  \"symbol\": \"NFLX\",\n  \"targetHigh\": 462,\n  \"targetLow\": 217.15,\n  \"targetMean\": 364.37,\n  \"targetMedian\": 359.04\n}"
  rawContent: "Price Target Premium\n\nGet latest price target consensus.\n\nMethod: GET\n\nPremium: Premium required.\n\nExamples:\n\n/stock/price-target?symbol=NFLX\n\n/stock/price-target?symbol=DIS\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nResponse Attributes:\n\nlastUpdated\n\nUpdated time of the data\n\nnumberAnalysts\n\nNumber of Analysts.\n\nsymbol\n\nCompany symbol.\n\ntargetHigh\n\nHighes analysts' target.\n\ntargetLow\n\nLowest analysts' target.\n\ntargetMean\n\nMean of all analysts' targets.\n\ntargetMedian\n\nMedian of all analysts' targets.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.price_target('AAPL'))\n\nSample response\n\n{\n  \"lastUpdated\": \"2023-04-06 00:00:00\",\n  \"numberAnalysts\": 39,\n  \"symbol\": \"NFLX\",\n  \"targetHigh\": 462,\n  \"targetLow\": 217.15,\n  \"targetMean\": 364.37,\n  \"targetMedian\": 359.04\n}\n\nWidget:"
  suggestedFilename: "price-target"
---

# Price Target Premium

## 源URL

https://finnhub.io/docs/api/price-target

## 描述

Get latest price target consensus.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/price-target?symbol=NFLX`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol of the company: AAPL. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.priceTarget('AAPL', (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.price_target('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.PriceTarget(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->priceTarget("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.price_target('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.priceTarget("AAPL"))
```

### 示例 7 (json)

```json
{
  "lastUpdated": "2023-04-06 00:00:00",
  "numberAnalysts": 39,
  "symbol": "NFLX",
  "targetHigh": 462,
  "targetLow": 217.15,
  "targetMean": 364.37,
  "targetMedian": 359.04
}
```

## 文档正文

Get latest price target consensus.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/price-target?symbol=NFLX`

Price Target Premium

Get latest price target consensus.

Method: GET

Premium: Premium required.

Examples:

/stock/price-target?symbol=NFLX

/stock/price-target?symbol=DIS

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

Response Attributes:

lastUpdated

Updated time of the data

numberAnalysts

Number of Analysts.

symbol

Company symbol.

targetHigh

Highes analysts' target.

targetLow

Lowest analysts' target.

targetMean

Mean of all analysts' targets.

targetMedian

Median of all analysts' targets.

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

print(finnhub_client.price_target('AAPL'))

Sample response

{
  "lastUpdated": "2023-04-06 00:00:00",
  "numberAnalysts": 39,
  "symbol": "NFLX",
  "targetHigh": 462,
  "targetLow": 217.15,
  "targetMean": 364.37,
  "targetMedian": 359.04
}

Widget:
