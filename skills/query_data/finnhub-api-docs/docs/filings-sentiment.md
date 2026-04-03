---
id: "url-16bb61f1"
type: "api"
title: "filings-sentiment"
url: "https://finnhub.io/docs/api/filings-sentiment"
description: "Get sentiment analysis of 10-K and 10-Q filings from SEC. An abnormal increase in the number of positive/negative words in filings can signal a significant change in the company's stock price in the upcoming 4 quarters. We make use of Loughran and McDonald Sentiment Word Lists to calculate the sentiment for each filing."
source: ""
tags: []
crawl_time: "2026-03-18T08:12:56.017Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/stock/filings-sentiment"
  parameters:
    - {"name":"accessNumber","in":"query","required":true,"type":"string","description":"Access number of a specific report you want to retrieve data from."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.filingsSentiment('0000320193-20-000052', (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.sec_sentiment_analysis('0000320193-20-000052'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.FilingsSentiment(context.Background()).AccessNumber(\"0000320193-20-000052\").Execute()"}
    - {"language":"PHP","code":"print_r($client->filingsSentiment(\"0000320193-20-000052\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.filings_sentiment('0000320193-20-000052', {}))"}
    - {"language":"Kotlin","code":"println(apiClient.filingsSentiment(\"0000320193-20-000052\"))"}
  sampleResponse: "{\n  \"cik\": \"320193\",\n  \"symbol\": \"AAPL\",\n  \"accessNumber\": \"0000320193-20-000052\",\n  \"sentiment\": {\n    \"negative\": 1.2698412698412698,\n    \"polarity\": -0.1147540479911535,\n    \"positive\": 0.5042016806722689,\n    \"litigious\": 0.2427637721755369,\n    \"modal-weak\": 0.392156862745098,\n    \"uncertainty\": 1.1391223155929038,\n    \"constraining\": 0.5975723622782446,\n    \"modal-strong\": 0.14939309056956115,\n    \"modal-moderate\": 0.11204481792717086\n  }\n}"
  curlExample: ""
  jsonExample: "{\n  \"cik\": \"320193\",\n  \"symbol\": \"AAPL\",\n  \"accessNumber\": \"0000320193-20-000052\",\n  \"sentiment\": {\n    \"negative\": 1.2698412698412698,\n    \"polarity\": -0.1147540479911535,\n    \"positive\": 0.5042016806722689,\n    \"litigious\": 0.2427637721755369,\n    \"modal-weak\": 0.392156862745098,\n    \"uncertainty\": 1.1391223155929038,\n    \"constraining\": 0.5975723622782446,\n    \"modal-strong\": 0.14939309056956115,\n    \"modal-moderate\": 0.11204481792717086\n  }\n}"
  rawContent: ""
  suggestedFilename: "filings-sentiment"
---

# filings-sentiment

## 源URL

https://finnhub.io/docs/api/filings-sentiment

## 描述

Get sentiment analysis of 10-K and 10-Q filings from SEC. An abnormal increase in the number of positive/negative words in filings can signal a significant change in the company's stock price in the upcoming 4 quarters. We make use of Loughran and McDonald Sentiment Word Lists to calculate the sentiment for each filing.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/stock/filings-sentiment`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `accessNumber` | string | 是 | - | Access number of a specific report you want to retrieve data from. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.filingsSentiment('0000320193-20-000052', (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.sec_sentiment_analysis('0000320193-20-000052'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.FilingsSentiment(context.Background()).AccessNumber("0000320193-20-000052").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->filingsSentiment("0000320193-20-000052"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.filings_sentiment('0000320193-20-000052', {}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.filingsSentiment("0000320193-20-000052"))
```

### 示例 7 (json)

```json
{
  "cik": "320193",
  "symbol": "AAPL",
  "accessNumber": "0000320193-20-000052",
  "sentiment": {
    "negative": 1.2698412698412698,
    "polarity": -0.1147540479911535,
    "positive": 0.5042016806722689,
    "litigious": 0.2427637721755369,
    "modal-weak": 0.392156862745098,
    "uncertainty": 1.1391223155929038,
    "constraining": 0.5975723622782446,
    "modal-strong": 0.14939309056956115,
    "modal-moderate": 0.11204481792717086
  }
}
```

## 文档正文

Get sentiment analysis of 10-K and 10-Q filings from SEC. An abnormal increase in the number of positive/negative words in filings can signal a significant change in the company's stock price in the upcoming 4 quarters. We make use of Loughran and McDonald Sentiment Word Lists to calculate the sentiment for each filing.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/stock/filings-sentiment`
