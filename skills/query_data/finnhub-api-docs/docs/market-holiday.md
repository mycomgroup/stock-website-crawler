---
id: "url-d5894f2"
type: "api"
title: "Market Holiday"
url: "https://finnhub.io/docs/api/market-holiday"
description: "Get a list of holidays for global exchanges."
source: ""
tags: []
crawl_time: "2026-03-18T06:28:56.589Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/market-holiday?exchange=US"
  parameters:
    - {"name":"exchange","in":"query","required":true,"type":"string","description":"Exchange code."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.marketHoliday({'exchange': 'US'}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.market_holiday(exchange='US'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.MarketHoliday(context.Background()).Exchange(\"US\").Execute()"}
    - {"language":"PHP","code":"print_r($client->marketHoliday(\"US\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.market_holiday({exchange: 'US'}))"}
    - {"language":"Kotlin","code":"println(apiClient.marketHoliday(exchange = \"US\"))"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"eventName\": \"Christmas\",\n      \"atDate\": \"2023-12-25\",\n      \"tradingHour\": \"\"\n    },\n    {\n      \"eventName\": \"Independence Day\",\n      \"atDate\": \"2023-07-03\",\n      \"tradingHour\": \"09:30-13:00\"\n    }\n  ],\n  \"exchange\": \"US\",\n  \"timezone\": \"America/New_York\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"eventName\": \"Christmas\",\n      \"atDate\": \"2023-12-25\",\n      \"tradingHour\": \"\"\n    },\n    {\n      \"eventName\": \"Independence Day\",\n      \"atDate\": \"2023-07-03\",\n      \"tradingHour\": \"09:30-13:00\"\n    }\n  ],\n  \"exchange\": \"US\",\n  \"timezone\": \"America/New_York\"\n}"
  rawContent: "Market Holiday\n\nGet a list of holidays for global exchanges.\n\nMethod: GET\n\nExamples:\n\n/stock/market-holiday?exchange=US\n\n/stock/market-holiday?exchange=L\n\nArguments:\n\nexchangeREQUIRED\n\nExchange code.\n\nResponse Attributes:\n\ndata\n\nArray of holidays.\n\natDate\n\nDate.\n\neventName\n\nHoliday's name.\n\ntradingHour\n\nTrading hours for this day if the market is partially closed only.\n\nexchange\n\nExchange.\n\ntimezone\n\nTimezone.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.market_holiday(exchange='US'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"eventName\": \"Christmas\",\n      \"atDate\": \"2023-12-25\",\n      \"tradingHour\": \"\"\n    },\n    {\n      \"eventName\": \"Independence Day\",\n      \"atDate\": \"2023-07-03\",\n      \"tradingHour\": \"09:30-13:00\"\n    }\n  ],\n  \"exchange\": \"US\",\n  \"timezone\": \"America/New_York\"\n}"
  suggestedFilename: "market-holiday"
---

# Market Holiday

## 源URL

https://finnhub.io/docs/api/market-holiday

## 描述

Get a list of holidays for global exchanges.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/market-holiday?exchange=US`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `exchange` | string | 是 | - | Exchange code. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.marketHoliday({'exchange': 'US'}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.market_holiday(exchange='US'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.MarketHoliday(context.Background()).Exchange("US").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->marketHoliday("US"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.market_holiday({exchange: 'US'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.marketHoliday(exchange = "US"))
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "eventName": "Christmas",
      "atDate": "2023-12-25",
      "tradingHour": ""
    },
    {
      "eventName": "Independence Day",
      "atDate": "2023-07-03",
      "tradingHour": "09:30-13:00"
    }
  ],
  "exchange": "US",
  "timezone": "America/New_York"
}
```

## 文档正文

Get a list of holidays for global exchanges.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/market-holiday?exchange=US`

Market Holiday

Get a list of holidays for global exchanges.

Method: GET

Examples:

/stock/market-holiday?exchange=US

/stock/market-holiday?exchange=L

Arguments:

exchangeREQUIRED

Exchange code.

Response Attributes:

data

Array of holidays.

atDate

Date.

eventName

Holiday's name.

tradingHour

Trading hours for this day if the market is partially closed only.

exchange

Exchange.

timezone

Timezone.

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

print(finnhub_client.market_holiday(exchange='US'))

Sample response

{
  "data": [
    {
      "eventName": "Christmas",
      "atDate": "2023-12-25",
      "tradingHour": ""
    },
    {
      "eventName": "Independence Day",
      "atDate": "2023-07-03",
      "tradingHour": "09:30-13:00"
    }
  ],
  "exchange": "US",
  "timezone": "America/New_York"
}
