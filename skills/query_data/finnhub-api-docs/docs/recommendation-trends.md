---
id: "url-5a459c81"
type: "api"
title: "Recommendation Trends"
url: "https://finnhub.io/docs/api/recommendation-trends"
description: "Get latest analyst recommendation trends for a company."
source: ""
tags: []
crawl_time: "2026-03-18T09:27:47.042Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/recommendation?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.recommendationTrends('AAPL', (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.recommendation_trends('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.RecommendationTrends(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->recommendationTrends(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.recommendation_trends('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.recommendationTrends(\"AAPL\"))"}
  sampleResponse: "[\n  {\n    \"buy\": 24,\n    \"hold\": 7,\n    \"period\": \"2025-03-01\",\n    \"sell\": 0,\n    \"strongBuy\": 13,\n    \"strongSell\": 0,\n    \"symbol\": \"AAPL\"\n  },\n  {\n    \"buy\": 17,\n    \"hold\": 13,\n    \"period\": \"2025-02-01\",\n    \"sell\": 5,\n    \"strongBuy\": 13,\n    \"strongSell\": 0,\n    \"symbol\": \"AAPL\"\n  }\n]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"buy\": 24,\n    \"hold\": 7,\n    \"period\": \"2025-03-01\",\n    \"sell\": 0,\n    \"strongBuy\": 13,\n    \"strongSell\": 0,\n    \"symbol\": \"AAPL\"\n  },\n  {\n    \"buy\": 17,\n    \"hold\": 13,\n    \"period\": \"2025-02-01\",\n    \"sell\": 5,\n    \"strongBuy\": 13,\n    \"strongSell\": 0,\n    \"symbol\": \"AAPL\"\n  }\n]"
  rawContent: "Recommendation Trends\n\nGet latest analyst recommendation trends for a company.\n\nMethod: GET\n\nExamples:\n\n/stock/recommendation?symbol=AAPL\n\n/stock/recommendation?symbol=TSLA\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nResponse Attributes:\n\nbuy\n\nNumber of recommendations that fall into the Buy category\n\nhold\n\nNumber of recommendations that fall into the Hold category\n\nperiod\n\nUpdated period\n\nsell\n\nNumber of recommendations that fall into the Sell category\n\nstrongBuy\n\nNumber of recommendations that fall into the Strong Buy category\n\nstrongSell\n\nNumber of recommendations that fall into the Strong Sell category\n\nsymbol\n\nCompany symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.recommendation_trends('AAPL'))\n\nSample response\n\n[\n  {\n    \"buy\": 24,\n    \"hold\": 7,\n    \"period\": \"2025-03-01\",\n    \"sell\": 0,\n    \"strongBuy\": 13,\n    \"strongSell\": 0,\n    \"symbol\": \"AAPL\"\n  },\n  {\n    \"buy\": 17,\n    \"hold\": 13,\n    \"period\": \"2025-02-01\",\n    \"sell\": 5,\n    \"strongBuy\": 13,\n    \"strongSell\": 0,\n    \"symbol\": \"AAPL\"\n  }\n]\n\nWidget:"
  suggestedFilename: "recommendation-trends"
---

# Recommendation Trends

## 源URL

https://finnhub.io/docs/api/recommendation-trends

## 描述

Get latest analyst recommendation trends for a company.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/recommendation?symbol=AAPL`

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
finnhubClient.recommendationTrends('AAPL', (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.recommendation_trends('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.RecommendationTrends(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->recommendationTrends("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.recommendation_trends('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.recommendationTrends("AAPL"))
```

### 示例 7 (json)

```json
[
  {
    "buy": 24,
    "hold": 7,
    "period": "2025-03-01",
    "sell": 0,
    "strongBuy": 13,
    "strongSell": 0,
    "symbol": "AAPL"
  },
  {
    "buy": 17,
    "hold": 13,
    "period": "2025-02-01",
    "sell": 5,
    "strongBuy": 13,
    "strongSell": 0,
    "symbol": "AAPL"
  }
]
```

## 文档正文

Get latest analyst recommendation trends for a company.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/recommendation?symbol=AAPL`

Recommendation Trends

Get latest analyst recommendation trends for a company.

Method: GET

Examples:

/stock/recommendation?symbol=AAPL

/stock/recommendation?symbol=TSLA

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

Response Attributes:

buy

Number of recommendations that fall into the Buy category

hold

Number of recommendations that fall into the Hold category

period

Updated period

sell

Number of recommendations that fall into the Sell category

strongBuy

Number of recommendations that fall into the Strong Buy category

strongSell

Number of recommendations that fall into the Strong Sell category

symbol

Company symbol.

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

print(finnhub_client.recommendation_trends('AAPL'))

Sample response

[
  {
    "buy": 24,
    "hold": 7,
    "period": "2025-03-01",
    "sell": 0,
    "strongBuy": 13,
    "strongSell": 0,
    "symbol": "AAPL"
  },
  {
    "buy": 17,
    "hold": 13,
    "period": "2025-02-01",
    "sell": 5,
    "strongBuy": 13,
    "strongSell": 0,
    "symbol": "AAPL"
  }
]

Widget:
