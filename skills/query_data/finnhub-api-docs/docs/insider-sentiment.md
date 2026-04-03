---
id: "url-fd40573"
type: "api"
title: "Insider Sentiment"
url: "https://finnhub.io/docs/api/insider-sentiment"
description: "Get insider sentiment data for US companies calculated using method discussed here. The MSPR ranges from -100 for the most negative to 100 for the most positive which can signal price changes in the coming 30-90 days."
source: ""
tags: []
crawl_time: "2026-03-18T08:12:34.832Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/insider-sentiment?symbol=TSLA&from=2015-01-01&to=2022-03-01"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date: 2020-03-15."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date: 2020-03-16."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.insiderSentiment('AAPL', '2015-01-01', '2022-03-01', (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_insider_sentiment('AAPL', '2021-01-01', '2022-03-01'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.InsiderSentiment(context.Background()).Symbol(\"AAPL\").From(\"2021-01-01\").To(\"2022-07-30\").Execute()"}
    - {"language":"PHP","code":"print_r($client->insiderSentiment(\"AAPL\", \"2021-01-01\", \"2022-03-01\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.insider_sentiment('AAPL', '2015-01-01', '2022-03-01'))"}
    - {"language":"Kotlin","code":"println(apiClient.insiderSentiment(\"AAPL\", \"2021-01-01\", \"2022-07-07\"))"}
  sampleResponse: "{\n  \"data\":[\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2021,\n      \"month\":3,\n      \"change\":5540,\n      \"mspr\":12.209097\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":1,\n      \"change\":-1250,\n      \"mspr\":-5.6179776\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":2,\n      \"change\":-1250,\n      \"mspr\":-2.1459227\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":3,\n      \"change\":5870,\n      \"mspr\":8.960191\n    }\n  ],\n  \"symbol\":\"TSLA\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\":[\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2021,\n      \"month\":3,\n      \"change\":5540,\n      \"mspr\":12.209097\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":1,\n      \"change\":-1250,\n      \"mspr\":-5.6179776\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":2,\n      \"change\":-1250,\n      \"mspr\":-2.1459227\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":3,\n      \"change\":5870,\n      \"mspr\":8.960191\n    }\n  ],\n  \"symbol\":\"TSLA\"\n}"
  rawContent: "Insider Sentiment\n\nGet insider sentiment data for US companies calculated using method discussed here. The MSPR ranges from -100 for the most negative to 100 for the most positive which can signal price changes in the coming 30-90 days.\n\nMethod: GET\n\nExamples:\n\n/stock/insider-sentiment?symbol=TSLA&from=2015-01-01&to=2022-03-01\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nfromREQUIRED\n\nFrom date: 2020-03-15.\n\ntoREQUIRED\n\nTo date: 2020-03-16.\n\nResponse Attributes:\n\ndata\n\nArray of sentiment data.\n\nchange\n\nNet buying/selling from all insiders' transactions.\n\nmonth\n\nMonth.\n\nmspr\n\nMonthly share purchase ratio.\n\nsymbol\n\nSymbol.\n\nyear\n\nYear.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_insider_sentiment('AAPL', '2021-01-01', '2022-03-01'))\n\nSample response\n\n{\n  \"data\":[\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2021,\n      \"month\":3,\n      \"change\":5540,\n      \"mspr\":12.209097\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":1,\n      \"change\":-1250,\n      \"mspr\":-5.6179776\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":2,\n      \"change\":-1250,\n      \"mspr\":-2.1459227\n    },\n    {\n      \"symbol\":\"TSLA\",\n      \"year\":2022,\n      \"month\":3,\n      \"change\":5870,\n      \"mspr\":8.960191\n    }\n  ],\n  \"symbol\":\"TSLA\"\n}"
  suggestedFilename: "insider-sentiment"
---

# Insider Sentiment

## 源URL

https://finnhub.io/docs/api/insider-sentiment

## 描述

Get insider sentiment data for US companies calculated using method discussed here. The MSPR ranges from -100 for the most negative to 100 for the most positive which can signal price changes in the coming 30-90 days.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/insider-sentiment?symbol=TSLA&from=2015-01-01&to=2022-03-01`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol of the company: AAPL. |
| `from` | string | 是 | - | From date: 2020-03-15. |
| `to` | string | 是 | - | To date: 2020-03-16. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.insiderSentiment('AAPL', '2015-01-01', '2022-03-01', (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_insider_sentiment('AAPL', '2021-01-01', '2022-03-01'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.InsiderSentiment(context.Background()).Symbol("AAPL").From("2021-01-01").To("2022-07-30").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->insiderSentiment("AAPL", "2021-01-01", "2022-03-01"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.insider_sentiment('AAPL', '2015-01-01', '2022-03-01'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.insiderSentiment("AAPL", "2021-01-01", "2022-07-07"))
```

### 示例 7 (json)

```json
{
  "data":[
    {
      "symbol":"TSLA",
      "year":2021,
      "month":3,
      "change":5540,
      "mspr":12.209097
    },
    {
      "symbol":"TSLA",
      "year":2022,
      "month":1,
      "change":-1250,
      "mspr":-5.6179776
    },
    {
      "symbol":"TSLA",
      "year":2022,
      "month":2,
      "change":-1250,
      "mspr":-2.1459227
    },
    {
      "symbol":"TSLA",
      "year":2022,
      "month":3,
      "change":5870,
      "mspr":8.960191
    }
  ],
  "symbol":"TSLA"
}
```

## 文档正文

Get insider sentiment data for US companies calculated using method discussed here. The MSPR ranges from -100 for the most negative to 100 for the most positive which can signal price changes in the coming 30-90 days.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/insider-sentiment?symbol=TSLA&from=2015-01-01&to=2022-03-01`

Insider Sentiment

Get insider sentiment data for US companies calculated using method discussed here. The MSPR ranges from -100 for the most negative to 100 for the most positive which can signal price changes in the coming 30-90 days.

Method: GET

Examples:

/stock/insider-sentiment?symbol=TSLA&from=2015-01-01&to=2022-03-01

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

fromREQUIRED

From date: 2020-03-15.

toREQUIRED

To date: 2020-03-16.

Response Attributes:

data

Array of sentiment data.

change

Net buying/selling from all insiders' transactions.

month

Month.

mspr

Monthly share purchase ratio.

symbol

Symbol.

year

Year.

symbol

Symbol of the company.

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

print(finnhub_client.stock_insider_sentiment('AAPL', '2021-01-01', '2022-03-01'))

Sample response

{
  "data":[
    {
      "symbol":"TSLA",
      "year":2021,
      "month":3,
      "change":5540,
      "mspr":12.209097
    },
    {
      "symbol":"TSLA",
      "year":2022,
      "month":1,
      "change":-1250,
      "mspr":-5.6179776
    },
    {
      "symbol":"TSLA",
      "year":2022,
      "month":2,
      "change":-1250,
      "mspr":-2.1459227
    },
    {
      "symbol":"TSLA",
      "year":2022,
      "month":3,
      "change":5870,
      "mspr":8.960191
    }
  ],
  "symbol":"TSLA"
}
