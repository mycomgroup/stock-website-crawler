---
id: "url-1516f479"
type: "api"
title: "Market News"
url: "https://finnhub.io/docs/api/market-news"
description: "Get latest market news."
source: ""
tags: []
crawl_time: "2026-03-18T04:34:45.188Z"
metadata:
  requestMethod: "GET"
  endpoint: "/news?category=general"
  parameters:
    - {"name":"category","in":"query","required":true,"type":"string","description":"This parameter can be 1 of the following values general, forex, crypto, merger."}
    - {"name":"minId","in":"query","required":false,"type":"integer","description":"Use this field to get only news after this ID. Default to 0"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.marketNews(\"general\", {}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.general_news('general', min_id=0))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.MarketNews(context.Background()).Category(\"general\").Execute()"}
    - {"language":"PHP","code":"print_r($client->marketNews(\"forex\", 0));"}
    - {"language":"Ruby","code":"puts(finnhub_client.market_news('general', {min_id: 0}))"}
    - {"language":"Kotlin","code":"println(apiClient.marketNews(\"general\", minId = 0))"}
  sampleResponse: "[\n  {\n    \"category\": \"technology\",\n    \"datetime\": 1596589501,\n    \"headline\": \"Square surges after reporting 64% jump in revenue, more customers using Cash App\",\n    \"id\": 5085164,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/105569283-1542050972462rts25mct.jpg?v=1542051069\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"Shares of Square soared on Tuesday evening after posting better-than-expected quarterly results and strong growth in its consumer payments app.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/square-sq-earnings-q2-2020.html\"\n  },\n  {\n    \"category\": \"business\",\n    \"datetime\": 1596588232,\n    \"headline\": \"B&G Foods CEO expects pantry demand to hold up post-pandemic\",\n    \"id\": 5085113,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/106629991-1595532157669-gettyimages-1221952946-362857076_1-5.jpeg?v=1595532242\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"\\\"I think post-Covid, people will be working more at home, which means people will be eating more breakfast\\\" and other meals at home, B&G CEO Ken Romanzi said.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/bg-foods-ceo-expects-pantry-demand-to-hold-up-post-pandemic.html\"\n  },\n  {\n    \"category\": \"top news\",\n    \"datetime\": 1596584406,\n    \"headline\": \"Anthony Levandowski gets 18 months in prison for stealing Google self-driving car files\",\n    \"id\": 5084850,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/106648265-1596584130509-UBER-LEVANDOWSKI.JPG?v=1596584247\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"A U.S. judge on Tuesday sentenced former Google engineer Anthony Levandowski to 18 months in prison for stealing a trade secret from Google related to self-driving cars months before becoming the head of Uber Technologies Inc's rival unit.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/anthony-levandowski-gets-18-months-in-prison-for-stealing-google-self-driving-car-files.html\"\n  }\n  }]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"category\": \"technology\",\n    \"datetime\": 1596589501,\n    \"headline\": \"Square surges after reporting 64% jump in revenue, more customers using Cash App\",\n    \"id\": 5085164,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/105569283-1542050972462rts25mct.jpg?v=1542051069\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"Shares of Square soared on Tuesday evening after posting better-than-expected quarterly results and strong growth in its consumer payments app.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/square-sq-earnings-q2-2020.html\"\n  },\n  {\n    \"category\": \"business\",\n    \"datetime\": 1596588232,\n    \"headline\": \"B&G Foods CEO expects pantry demand to hold up post-pandemic\",\n    \"id\": 5085113,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/106629991-1595532157669-gettyimages-1221952946-362857076_1-5.jpeg?v=1595532242\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"\\\"I think post-Covid, people will be working more at home, which means people will be eating more breakfast\\\" and other meals at home, B&G CEO Ken Romanzi said.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/bg-foods-ceo-expects-pantry-demand-to-hold-up-post-pandemic.html\"\n  },\n  {\n    \"category\": \"top news\",\n    \"datetime\": 1596584406,\n    \"headline\": \"Anthony Levandowski gets 18 months in prison for stealing Google self-driving car files\",\n    \"id\": 5084850,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/106648265-1596584130509-UBER-LEVANDOWSKI.JPG?v=1596584247\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"A U.S. judge on Tuesday sentenced former Google engineer Anthony Levandowski to 18 months in prison for stealing a trade secret from Google related to self-driving cars months before becoming the head of Uber Technologies Inc's rival unit.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/anthony-levandowski-gets-18-months-in-prison-for-stealing-google-self-driving-car-files.html\"\n  }\n  }]"
  rawContent: "Market News\n\nGet latest market news.\n\nMethod: GET\n\nExamples:\n\n/news?category=general\n\n/news?category=forex&minId=10\n\nArguments:\n\ncategoryREQUIRED\n\nThis parameter can be 1 of the following values general, forex, crypto, merger.\n\nminIdoptional\n\nUse this field to get only news after this ID. Default to 0\n\nResponse Attributes:\n\ncategory\n\nNews category.\n\ndatetime\n\nPublished time in UNIX timestamp.\n\nheadline\n\nNews headline.\n\nid\n\nNews ID. This value can be used for minId params to get the latest news only.\n\nimage\n\nThumbnail image URL.\n\nrelated\n\nRelated stocks and companies mentioned in the article.\n\nsource\n\nNews source.\n\nsummary\n\nNews summary.\n\nurl\n\nURL of the original article.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.general_news('general', min_id=0))\n\nSample response\n\n[\n  {\n    \"category\": \"technology\",\n    \"datetime\": 1596589501,\n    \"headline\": \"Square surges after reporting 64% jump in revenue, more customers using Cash App\",\n    \"id\": 5085164,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/105569283-1542050972462rts25mct.jpg?v=1542051069\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"Shares of Square soared on Tuesday evening after posting better-than-expected quarterly results and strong growth in its consumer payments app.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/square-sq-earnings-q2-2020.html\"\n  },\n  {\n    \"category\": \"business\",\n    \"datetime\": 1596588232,\n    \"headline\": \"B&G Foods CEO expects pantry demand to hold up post-pandemic\",\n    \"id\": 5085113,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/106629991-1595532157669-gettyimages-1221952946-362857076_1-5.jpeg?v=1595532242\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"\\\"I think post-Covid, people will be working more at home, which means people will be eating more breakfast\\\" and other meals at home, B&G CEO Ken Romanzi said.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/bg-foods-ceo-expects-pantry-demand-to-hold-up-post-pandemic.html\"\n  },\n  {\n    \"category\": \"top news\",\n    \"datetime\": 1596584406,\n    \"headline\": \"Anthony Levandowski gets 18 months in prison for stealing Google self-driving car files\",\n    \"id\": 5084850,\n    \"image\": \"https://image.cnbcfm.com/api/v1/image/106648265-1596584130509-UBER-LEVANDOWSKI.JPG?v=1596584247\",\n    \"related\": \"\",\n    \"source\": \"CNBC\",\n    \"summary\": \"A U.S. judge on Tuesday sentenced former Google engineer Anthony Levandowski to 18 months in prison for stealing a trade secret from Google related to self-driving cars months before becoming the head of Uber Technologies Inc's rival unit.\",\n    \"url\": \"https://www.cnbc.com/2020/08/04/anthony-levandowski-gets-18-months-in-prison-for-stealing-google-self-driving-car-files.html\"\n  }\n  }]"
  suggestedFilename: "market-news"
---

# Market News

## 源URL

https://finnhub.io/docs/api/market-news

## 描述

Get latest market news.

## API 端点

**Method**: `GET`
**Endpoint**: `/news?category=general`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `category` | string | 是 | - | This parameter can be 1 of the following values general, forex, crypto, merger. |
| `minId` | integer | 否 | - | Use this field to get only news after this ID. Default to 0 |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.marketNews("general", {}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.general_news('general', min_id=0))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.MarketNews(context.Background()).Category("general").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->marketNews("forex", 0));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.market_news('general', {min_id: 0}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.marketNews("general", minId = 0))
```

### 示例 7 (json)

```json
[
  {
    "category": "technology",
    "datetime": 1596589501,
    "headline": "Square surges after reporting 64% jump in revenue, more customers using Cash App",
    "id": 5085164,
    "image": "https://image.cnbcfm.com/api/v1/image/105569283-1542050972462rts25mct.jpg?v=1542051069",
    "related": "",
    "source": "CNBC",
    "summary": "Shares of Square soared on Tuesday evening after posting better-than-expected quarterly results and strong growth in its consumer payments app.",
    "url": "https://www.cnbc.com/2020/08/04/square-sq-earnings-q2-2020.html"
  },
  {
    "category": "business",
    "datetime": 1596588232,
    "headline": "B&G Foods CEO expects pantry demand to hold up post-pandemic",
    "id": 5085113,
    "image": "https://image.cnbcfm.com/api/v1/image/106629991-1595532157669-gettyimages-1221952946-362857076_1-5.jpeg?v=1595532242",
    "related": "",
    "source": "CNBC",
    "summary": "\"I think post-Covid, people will be working more at home, which means people will be eating more breakfast\" and other meals at home, B&G CEO Ken Romanzi said.",
    "url": "https://www.cnbc.com/2020/08/04/bg-foods-ceo-expects-pantry-demand-to-hold-up-post-pandemic.html"
  },
  {
    "category": "top news",
    "datetime": 1596584406,
    "headline": "Anthony Levandowski gets 18 months in prison for stealing Google self-driving car files",
    "id": 5084850,
    "image": "https://image.cnbcfm.com/api/v1/image/106648265-1596584130509-UBER-LEVANDOWSKI.JPG?v=1596584247",
    "related": "",
    "source": "CNBC",
    "summary": "A U.S. judge on Tuesday sentenced former Google engineer Anthony Levandowski to 18 months in prison for stealing a trade secret from Google related to self-driving cars months before becoming the head of Uber Technologies Inc's rival unit.",
    "url": "https://www.cnbc.com/2020/08/04/anthony-levandowski-gets-18-months-in-prison-for-stealing-google-self-driving-car-files.html"
  }
  }]
```

## 文档正文

Get latest market news.

## API 端点

**Method:** `GET`
**Endpoint:** `/news?category=general`

Market News

Get latest market news.

Method: GET

Examples:

/news?category=general

/news?category=forex&minId=10

Arguments:

categoryREQUIRED

This parameter can be 1 of the following values general, forex, crypto, merger.

minIdoptional

Use this field to get only news after this ID. Default to 0

Response Attributes:

category

News category.

datetime

Published time in UNIX timestamp.

headline

News headline.

id

News ID. This value can be used for minId params to get the latest news only.

image

Thumbnail image URL.

related

Related stocks and companies mentioned in the article.

source

News source.

summary

News summary.

url

URL of the original article.

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

print(finnhub_client.general_news('general', min_id=0))

Sample response

[
  {
    "category": "technology",
    "datetime": 1596589501,
    "headline": "Square surges after reporting 64% jump in revenue, more customers using Cash App",
    "id": 5085164,
    "image": "https://image.cnbcfm.com/api/v1/image/105569283-1542050972462rts25mct.jpg?v=1542051069",
    "related": "",
    "source": "CNBC",
    "summary": "Shares of Square soared on Tuesday evening after posting better-than-expected quarterly results and strong growth in its consumer payments app.",
    "url": "https://www.cnbc.com/2020/08/04/square-sq-earnings-q2-2020.html"
  },
  {
    "category": "business",
    "datetime": 1596588232,
    "headline": "B&G Foods CEO expects pantry demand to hold up post-pandemic",
    "id": 5085113,
    "image": "https://image.cnbcfm.com/api/v1/image/106629991-1595532157669-gettyimages-1221952946-362857076_1-5.jpeg?v=1595532242",
    "related": "",
    "source": "CNBC",
    "summary": "\"I think post-Covid, people will be working more at home, which means people will be eating more breakfast\" and other meals at home, B&G CEO Ken Romanzi said.",
    "url": "https://www.cnbc.com/2020/08/04/bg-foods-ceo-expects-pantry-demand-to-hold-up-post-pandemic.html"
  },
  {
    "category": "top news",
    "datetime": 1596584406,
    "headline": "Anthony Levandowski gets 18 months in prison for stealing Google self-driving car files",
    "id": 5084850,
    "image": "https://image.cnbcfm.com/api/v1/image/106648265-1596584130509-UBER-LEVANDOWSKI.JPG?v=1596584247",
    "related": "",
    "source": "CNBC",
    "summary": "A U.S. judge on Tuesday sentenced former Google engineer Anthony Levandowski to 18 months in prison for stealing a trade secret from Google related to self-driving cars months before becoming the head of Uber Technologies Inc's rival unit.",
    "url": "https://www.cnbc.com/2020/08/04/anthony-levandowski-gets-18-months-in-prison-for-stealing-google-self-driving-car-files.html"
  }
  }]
