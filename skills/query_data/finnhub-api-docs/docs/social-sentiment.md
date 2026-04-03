---
id: "url-3b0390ba"
type: "api"
title: "Social Sentiment Premium"
url: "https://finnhub.io/docs/api/social-sentiment"
description: "Get social sentiment for stocks on Reddit and Twitter."
source: ""
tags: []
crawl_time: "2026-03-18T08:12:03.409Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/social-sentiment?symbol=GME"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Company symbol."}
    - {"name":"from","in":"query","required":false,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.socialSentiment('GME', (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_social_sentiment('GME'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.SocialSentiment(context.Background()).Symbol(\"GME\").Execute()"}
    - {"language":"PHP","code":"print_r($client->socialSentiment(\"GME\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.social_sentiment('GME'))"}
    - {"language":"Kotlin","code":"println(apiClient.socialSentiment(\"GME\", \"\", \"\"))"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"atTime\": \"2021-05-08 14:00:00\",\n      \"mention\": 32,\n      \"positiveScore\": 0.9213675,\n      \"negativeScore\": -0.9864475,\n      \"positiveMention\": 20,\n      \"negativeMention\": 12,\n      \"score\": -0.0341123222115352\n    },\n    {\n      \"atTime\": \"2021-05-08 13:00:00\",\n      \"mention\": 25,\n      \"positiveScore\": 0.92,\n      \"negativeScore\": -0.991266,\n      \"positiveMention\": 8,\n      \"negativeMention\": 17,\n      \"score\": -0.56282\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"atTime\": \"2021-05-08 14:00:00\",\n      \"mention\": 32,\n      \"positiveScore\": 0.9213675,\n      \"negativeScore\": -0.9864475,\n      \"positiveMention\": 20,\n      \"negativeMention\": 12,\n      \"score\": -0.0341123222115352\n    },\n    {\n      \"atTime\": \"2021-05-08 13:00:00\",\n      \"mention\": 25,\n      \"positiveScore\": 0.92,\n      \"negativeScore\": -0.991266,\n      \"positiveMention\": 8,\n      \"negativeMention\": 17,\n      \"score\": -0.56282\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  rawContent: "Social Sentiment Premium\n\nGet social sentiment for stocks on Reddit and Twitter.\n\nMethod: GET\n\nPremium: Premium required.\n\nExamples:\n\n/stock/social-sentiment?symbol=GME\n\nArguments:\n\nsymbolREQUIRED\n\nCompany symbol.\n\nfromoptional\n\nFrom date YYYY-MM-DD.\n\ntooptional\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ndata\n\nSentiment data.\n\natTime\n\nPeriod.\n\nmention\n\nNumber of mentions\n\nnegativeMention\n\nNumber of negative mentions\n\nnegativeScore\n\nNegative score. Range 0-1\n\npositiveMention\n\nNumber of positive mentions\n\npositiveScore\n\nPositive score. Range 0-1\n\nscore\n\nFinal score. Range: -1 to 1 with 1 is very positive and -1 is very negative\n\nsymbol\n\nCompany symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_social_sentiment('GME'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"atTime\": \"2021-05-08 14:00:00\",\n      \"mention\": 32,\n      \"positiveScore\": 0.9213675,\n      \"negativeScore\": -0.9864475,\n      \"positiveMention\": 20,\n      \"negativeMention\": 12,\n      \"score\": -0.0341123222115352\n    },\n    {\n      \"atTime\": \"2021-05-08 13:00:00\",\n      \"mention\": 25,\n      \"positiveScore\": 0.92,\n      \"negativeScore\": -0.991266,\n      \"positiveMention\": 8,\n      \"negativeMention\": 17,\n      \"score\": -0.56282\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "social-sentiment"
---

# Social Sentiment Premium

## 源URL

https://finnhub.io/docs/api/social-sentiment

## 描述

Get social sentiment for stocks on Reddit and Twitter.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/social-sentiment?symbol=GME`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Company symbol. |
| `from` | string | 否 | - | From date YYYY-MM-DD. |
| `to` | string | 否 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.socialSentiment('GME', (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_social_sentiment('GME'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.SocialSentiment(context.Background()).Symbol("GME").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->socialSentiment("GME"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.social_sentiment('GME'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.socialSentiment("GME", "", ""))
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "atTime": "2021-05-08 14:00:00",
      "mention": 32,
      "positiveScore": 0.9213675,
      "negativeScore": -0.9864475,
      "positiveMention": 20,
      "negativeMention": 12,
      "score": -0.0341123222115352
    },
    {
      "atTime": "2021-05-08 13:00:00",
      "mention": 25,
      "positiveScore": 0.92,
      "negativeScore": -0.991266,
      "positiveMention": 8,
      "negativeMention": 17,
      "score": -0.56282
    }
  ],
  "symbol": "AAPL"
}
```

## 文档正文

Get social sentiment for stocks on Reddit and Twitter.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/social-sentiment?symbol=GME`

Social Sentiment Premium

Get social sentiment for stocks on Reddit and Twitter.

Method: GET

Premium: Premium required.

Examples:

/stock/social-sentiment?symbol=GME

Arguments:

symbolREQUIRED

Company symbol.

fromoptional

From date YYYY-MM-DD.

tooptional

To date YYYY-MM-DD.

Response Attributes:

data

Sentiment data.

atTime

Period.

mention

Number of mentions

negativeMention

Number of negative mentions

negativeScore

Negative score. Range 0-1

positiveMention

Number of positive mentions

positiveScore

Positive score. Range 0-1

score

Final score. Range: -1 to 1 with 1 is very positive and -1 is very negative

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

print(finnhub_client.stock_social_sentiment('GME'))

Sample response

{
  "data": [
    {
      "atTime": "2021-05-08 14:00:00",
      "mention": 32,
      "positiveScore": 0.9213675,
      "negativeScore": -0.9864475,
      "positiveMention": 20,
      "negativeMention": 12,
      "score": -0.0341123222115352
    },
    {
      "atTime": "2021-05-08 13:00:00",
      "mention": 25,
      "positiveScore": 0.92,
      "negativeScore": -0.991266,
      "positiveMention": 8,
      "negativeMention": 17,
      "score": -0.56282
    }
  ],
  "symbol": "AAPL"
}
