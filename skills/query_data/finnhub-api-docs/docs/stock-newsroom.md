---
id: "url-47b07fd0"
type: "api"
title: "Newsroom Premium"
url: "https://finnhub.io/docs/api/stock-newsroom"
description: "Get latest articles posted directly on the companies' newsroom and investor relations page. Newsroom API along with the Press Releases API provide a comprehensive text-based dataset directly from the company. We currently cover 1,250 US Companies with this dataset."
source: ""
tags: []
crawl_time: "2026-03-18T06:59:22.867Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/newsroom?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Company symbol."}
    - {"name":"from","in":"query","required":false,"type":"string","description":"From time: 2025-01-01."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To time: 2026-01-05."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.newsroom(\"AAPL\", {}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.newsroom('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.Newsroom(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->newsroom(\"AAPL\", \"2025-01-01\", \"2025-12-31\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.newsroom('AAPL', {from: \"2025-01-01\", to: \"2025-12-31\"}))"}
    - {"language":"Kotlin","code":"println(apiClient.newsroom(\"AAPL\", from = \"2025-01-01\", to = \"2025-12-31\"))"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"atDate\": \"2025-11-25 14:47:50\",\n      \"fullText\": \"https://static2.finnhub.io/file/publicdatany/newsroom_new/5def2b7215a5cae2334ad221236da9978f9eb20e737bcccc9080307f7df068ad.html.gz\",\n      \"title\": \"AI at Work: Which future of jobs are we building toward?\",\n      \"url\": \"https://www.microsoft.com/en-us/worklab/ai-at-work-which-future-of-jobs-are-we-building-towards\"\n    },\n    {\n      \"atDate\": \"2025-11-20 05:50:57\",\n      \"fullText\": \"https://static2.finnhub.io/file/publicdatany/newsroom_new/36de40a2fc8c24227dd6fca77f7acc842bf4550ab7b51ab01a2fbecff250d2f2.html.gz\",\n      \"title\": \"Why becoming an AI Frontier Firm is hard – Raffaella Sadun\",\n      \"url\": \"https://www.microsoft.com/en-us/worklab/podcast/harvard-raffaella-sadun-on-why-its-so-hard-to-become-a-frontier-firm\"\n    }\n  ],\n  \"symbol\": \"MSFT\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"atDate\": \"2025-11-25 14:47:50\",\n      \"fullText\": \"https://static2.finnhub.io/file/publicdatany/newsroom_new/5def2b7215a5cae2334ad221236da9978f9eb20e737bcccc9080307f7df068ad.html.gz\",\n      \"title\": \"AI at Work: Which future of jobs are we building toward?\",\n      \"url\": \"https://www.microsoft.com/en-us/worklab/ai-at-work-which-future-of-jobs-are-we-building-towards\"\n    },\n    {\n      \"atDate\": \"2025-11-20 05:50:57\",\n      \"fullText\": \"https://static2.finnhub.io/file/publicdatany/newsroom_new/36de40a2fc8c24227dd6fca77f7acc842bf4550ab7b51ab01a2fbecff250d2f2.html.gz\",\n      \"title\": \"Why becoming an AI Frontier Firm is hard – Raffaella Sadun\",\n      \"url\": \"https://www.microsoft.com/en-us/worklab/podcast/harvard-raffaella-sadun-on-why-its-so-hard-to-become-a-frontier-firm\"\n    }\n  ],\n  \"symbol\": \"MSFT\"\n}"
  rawContent: "Newsroom Premium\n\nGet latest articles posted directly on the companies' newsroom and investor relations page. Newsroom API along with the Press Releases API provide a comprehensive text-based dataset directly from the company. We currently cover 1,250 US Companies with this dataset.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/newsroom?symbol=AAPL\n\n/stock/newsroom?symbol=NVDA&from=2025-01-01&to=2025-12-15\n\nArguments:\n\nsymbolREQUIRED\n\nCompany symbol.\n\nfromoptional\n\nFrom time: 2025-01-01.\n\ntooptional\n\nTo time: 2026-01-05.\n\nResponse Attributes:\n\ndata\n\nArray of articles.\n\natDate\n\nPublished time in YYYY-MM-DD HH:MM:SS format (EST timezone).\n\nfullText\n\nURL to download the full text data.\n\ntitle\n\nTitle.\n\nurl\n\nOriginal URL.\n\nsymbol\n\nCompany symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.newsroom('AAPL'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"atDate\": \"2025-11-25 14:47:50\",\n      \"fullText\": \"https://static2.finnhub.io/file/publicdatany/newsroom_new/5def2b7215a5cae2334ad221236da9978f9eb20e737bcccc9080307f7df068ad.html.gz\",\n      \"title\": \"AI at Work: Which future of jobs are we building toward?\",\n      \"url\": \"https://www.microsoft.com/en-us/worklab/ai-at-work-which-future-of-jobs-are-we-building-towards\"\n    },\n    {\n      \"atDate\": \"2025-11-20 05:50:57\",\n      \"fullText\": \"https://static2.finnhub.io/file/publicdatany/newsroom_new/36de40a2fc8c24227dd6fca77f7acc842bf4550ab7b51ab01a2fbecff250d2f2.html.gz\",\n      \"title\": \"Why becoming an AI Frontier Firm is hard – Raffaella Sadun\",\n      \"url\": \"https://www.microsoft.com/en-us/worklab/podcast/harvard-raffaella-sadun-on-why-its-so-hard-to-become-a-frontier-firm\"\n    }\n  ],\n  \"symbol\": \"MSFT\"\n}"
  suggestedFilename: "stock-newsroom"
---

# Newsroom Premium

## 源URL

https://finnhub.io/docs/api/stock-newsroom

## 描述

Get latest articles posted directly on the companies' newsroom and investor relations page. Newsroom API along with the Press Releases API provide a comprehensive text-based dataset directly from the company. We currently cover 1,250 US Companies with this dataset.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/newsroom?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Company symbol. |
| `from` | string | 否 | - | From time: 2025-01-01. |
| `to` | string | 否 | - | To time: 2026-01-05. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.newsroom("AAPL", {}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.newsroom('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.Newsroom(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->newsroom("AAPL", "2025-01-01", "2025-12-31"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.newsroom('AAPL', {from: "2025-01-01", to: "2025-12-31"}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.newsroom("AAPL", from = "2025-01-01", to = "2025-12-31"))
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "atDate": "2025-11-25 14:47:50",
      "fullText": "https://static2.finnhub.io/file/publicdatany/newsroom_new/5def2b7215a5cae2334ad221236da9978f9eb20e737bcccc9080307f7df068ad.html.gz",
      "title": "AI at Work: Which future of jobs are we building toward?",
      "url": "https://www.microsoft.com/en-us/worklab/ai-at-work-which-future-of-jobs-are-we-building-towards"
    },
    {
      "atDate": "2025-11-20 05:50:57",
      "fullText": "https://static2.finnhub.io/file/publicdatany/newsroom_new/36de40a2fc8c24227dd6fca77f7acc842bf4550ab7b51ab01a2fbecff250d2f2.html.gz",
      "title": "Why becoming an AI Frontier Firm is hard – Raffaella Sadun",
      "url": "https://www.microsoft.com/en-us/worklab/podcast/harvard-raffaella-sadun-on-why-its-so-hard-to-become-a-frontier-firm"
    }
  ],
  "symbol": "MSFT"
}
```

## 文档正文

Get latest articles posted directly on the companies' newsroom and investor relations page. Newsroom API along with the Press Releases API provide a comprehensive text-based dataset directly from the company. We currently cover 1,250 US Companies with this dataset.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/newsroom?symbol=AAPL`

Newsroom Premium

Get latest articles posted directly on the companies' newsroom and investor relations page. Newsroom API along with the Press Releases API provide a comprehensive text-based dataset directly from the company. We currently cover 1,250 US Companies with this dataset.

Method: GET

Premium: Premium Access Required

Examples:

/stock/newsroom?symbol=AAPL

/stock/newsroom?symbol=NVDA&from=2025-01-01&to=2025-12-15

Arguments:

symbolREQUIRED

Company symbol.

fromoptional

From time: 2025-01-01.

tooptional

To time: 2026-01-05.

Response Attributes:

data

Array of articles.

atDate

Published time in YYYY-MM-DD HH:MM:SS format (EST timezone).

fullText

URL to download the full text data.

title

Title.

url

Original URL.

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

print(finnhub_client.newsroom('AAPL'))

Sample response

{
  "data": [
    {
      "atDate": "2025-11-25 14:47:50",
      "fullText": "https://static2.finnhub.io/file/publicdatany/newsroom_new/5def2b7215a5cae2334ad221236da9978f9eb20e737bcccc9080307f7df068ad.html.gz",
      "title": "AI at Work: Which future of jobs are we building toward?",
      "url": "https://www.microsoft.com/en-us/worklab/ai-at-work-which-future-of-jobs-are-we-building-towards"
    },
    {
      "atDate": "2025-11-20 05:50:57",
      "fullText": "https://static2.finnhub.io/file/publicdatany/newsroom_new/36de40a2fc8c24227dd6fca77f7acc842bf4550ab7b51ab01a2fbecff250d2f2.html.gz",
      "title": "Why becoming an AI Frontier Firm is hard – Raffaella Sadun",
      "url": "https://www.microsoft.com/en-us/worklab/podcast/harvard-raffaella-sadun-on-why-its-so-hard-to-become-a-frontier-firm"
    }
  ],
  "symbol": "MSFT"
}
