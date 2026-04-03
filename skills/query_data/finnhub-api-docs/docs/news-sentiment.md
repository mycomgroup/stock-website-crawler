---
id: "url-71921b60"
type: "api"
title: "News Sentiment Premium"
url: "https://finnhub.io/docs/api/news-sentiment"
description: "Get company's news sentiment and statistics. This endpoint is only available for US companies."
source: ""
tags: []
crawl_time: "2026-03-18T06:29:25.099Z"
metadata:
  requestMethod: "GET"
  endpoint: "/news-sentiment?symbol=V"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Company symbol."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.newsSentiment('AAPL', (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.news_sentiment('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.NewsSentiment(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->newsSentiment(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.news_sentiment('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.newsSentiment(\"AAPL\"))"}
  sampleResponse: "{\n  \"buzz\": {\n    \"articlesInLastWeek\": 20,\n    \"buzz\": 0.8888,\n    \"weeklyAverage\": 22.5\n  },\n  \"companyNewsScore\": 0.9166,\n  \"sectorAverageBullishPercent\": 0.6482,\n  \"sectorAverageNewsScore\": 0.5191,\n  \"sentiment\": {\n    \"bearishPercent\": 0,\n    \"bullishPercent\": 1\n  },\n  \"symbol\": \"V\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"buzz\": {\n    \"articlesInLastWeek\": 20,\n    \"buzz\": 0.8888,\n    \"weeklyAverage\": 22.5\n  },\n  \"companyNewsScore\": 0.9166,\n  \"sectorAverageBullishPercent\": 0.6482,\n  \"sectorAverageNewsScore\": 0.5191,\n  \"sentiment\": {\n    \"bearishPercent\": 0,\n    \"bullishPercent\": 1\n  },\n  \"symbol\": \"V\"\n}"
  rawContent: "News Sentiment Premium\n\nGet company's news sentiment and statistics. This endpoint is only available for US companies.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/news-sentiment?symbol=V\n\n/news-sentiment?symbol=AAPL\n\nArguments:\n\nsymbolREQUIRED\n\nCompany symbol.\n\nResponse Attributes:\n\nbuzz\n\nStatistics of company news in the past week.\n\narticlesInLastWeek\n\nbuzz\n\nweeklyAverage\n\ncompanyNewsScore\n\nNews score.\n\nsectorAverageBullishPercent\n\nSector average bullish percent.\n\nsectorAverageNewsScore\n\nSectore average score.\n\nsentiment\n\nNews sentiment.\n\nbearishPercent\n\nbullishPercent\n\nsymbol\n\nRequested symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.news_sentiment('AAPL'))\n\nSample response\n\n{\n  \"buzz\": {\n    \"articlesInLastWeek\": 20,\n    \"buzz\": 0.8888,\n    \"weeklyAverage\": 22.5\n  },\n  \"companyNewsScore\": 0.9166,\n  \"sectorAverageBullishPercent\": 0.6482,\n  \"sectorAverageNewsScore\": 0.5191,\n  \"sentiment\": {\n    \"bearishPercent\": 0,\n    \"bullishPercent\": 1\n  },\n  \"symbol\": \"V\"\n}"
  suggestedFilename: "news-sentiment"
---

# News Sentiment Premium

## 源URL

https://finnhub.io/docs/api/news-sentiment

## 描述

Get company's news sentiment and statistics. This endpoint is only available for US companies.

## API 端点

**Method**: `GET`
**Endpoint**: `/news-sentiment?symbol=V`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Company symbol. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.newsSentiment('AAPL', (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.news_sentiment('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.NewsSentiment(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->newsSentiment("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.news_sentiment('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.newsSentiment("AAPL"))
```

### 示例 7 (json)

```json
{
  "buzz": {
    "articlesInLastWeek": 20,
    "buzz": 0.8888,
    "weeklyAverage": 22.5
  },
  "companyNewsScore": 0.9166,
  "sectorAverageBullishPercent": 0.6482,
  "sectorAverageNewsScore": 0.5191,
  "sentiment": {
    "bearishPercent": 0,
    "bullishPercent": 1
  },
  "symbol": "V"
}
```

## 文档正文

Get company's news sentiment and statistics. This endpoint is only available for US companies.

## API 端点

**Method:** `GET`
**Endpoint:** `/news-sentiment?symbol=V`

News Sentiment Premium

Get company's news sentiment and statistics. This endpoint is only available for US companies.

Method: GET

Premium: Premium Access Required

Examples:

/news-sentiment?symbol=V

/news-sentiment?symbol=AAPL

Arguments:

symbolREQUIRED

Company symbol.

Response Attributes:

buzz

Statistics of company news in the past week.

articlesInLastWeek

buzz

weeklyAverage

companyNewsScore

News score.

sectorAverageBullishPercent

Sector average bullish percent.

sectorAverageNewsScore

Sectore average score.

sentiment

News sentiment.

bearishPercent

bullishPercent

symbol

Requested symbol.

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

print(finnhub_client.news_sentiment('AAPL'))

Sample response

{
  "buzz": {
    "articlesInLastWeek": 20,
    "buzz": 0.8888,
    "weeklyAverage": 22.5
  },
  "companyNewsScore": 0.9166,
  "sectorAverageBullishPercent": 0.6482,
  "sectorAverageNewsScore": 0.5191,
  "sentiment": {
    "bearishPercent": 0,
    "bullishPercent": 1
  },
  "symbol": "V"
}
