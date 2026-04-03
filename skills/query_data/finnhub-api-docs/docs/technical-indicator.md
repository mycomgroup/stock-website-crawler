---
id: "url-50272154"
type: "api"
title: "aggregate-indicator"
url: "https://finnhub.io/docs/api/technical-indicator"
description: "Get aggregate signal of multiple technical indicators such as MACD, RSI, Moving Average v.v. A full list of indicators can be found here."
source: ""
tags: []
crawl_time: "2026-03-18T08:36:15.337Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/scan/technical-indicator"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"symbol"}
    - {"name":"resolution","in":"query","required":true,"type":"string","description":"Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.aggregateIndicator(\"AAPL\", \"D\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.aggregate_indicator('AAPL', 'D'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.AggregateIndicator(context.Background()).Symbol(\"AAPL\").Resolution(\"D\").Execute()"}
    - {"language":"PHP","code":"print_r($client->aggregateIndicator(\"AAPL\", \"D\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.aggregate_indicator('AAPL', 'D'))"}
    - {"language":"Kotlin","code":"println(apiClient.aggregateIndicator(\"AAPL\", \"D\"))"}
  sampleResponse: "{\n  \"technicalAnalysis\": {\n    \"count\": {\n      \"buy\": 6,\n      \"neutral\": 7,\n      \"sell\": 4\n    },\n    \"signal\": \"neutral\"\n  },\n  \"trend\": {\n    \"adx\": 24.46020733373421,\n    \"trending\": false\n  }\n}"
  curlExample: ""
  jsonExample: "{\n  \"technicalAnalysis\": {\n    \"count\": {\n      \"buy\": 6,\n      \"neutral\": 7,\n      \"sell\": 4\n    },\n    \"signal\": \"neutral\"\n  },\n  \"trend\": {\n    \"adx\": 24.46020733373421,\n    \"trending\": false\n  }\n}"
  rawContent: ""
  suggestedFilename: "technical-indicator"
---

# aggregate-indicator

## 源URL

https://finnhub.io/docs/api/technical-indicator

## 描述

Get aggregate signal of multiple technical indicators such as MACD, RSI, Moving Average v.v. A full list of indicators can be found here.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/scan/technical-indicator`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | symbol |
| `resolution` | string | 是 | - | Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.aggregateIndicator("AAPL", "D", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.aggregate_indicator('AAPL', 'D'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.AggregateIndicator(context.Background()).Symbol("AAPL").Resolution("D").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->aggregateIndicator("AAPL", "D"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.aggregate_indicator('AAPL', 'D'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.aggregateIndicator("AAPL", "D"))
```

### 示例 7 (json)

```json
{
  "technicalAnalysis": {
    "count": {
      "buy": 6,
      "neutral": 7,
      "sell": 4
    },
    "signal": "neutral"
  },
  "trend": {
    "adx": 24.46020733373421,
    "trending": false
  }
}
```

## 文档正文

Get aggregate signal of multiple technical indicators such as MACD, RSI, Moving Average v.v. A full list of indicators can be found here.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/scan/technical-indicator`
