---
id: "url-944464c"
type: "api"
title: "Price Metrics Premium"
url: "https://finnhub.io/docs/api/price-metrics"
description: "Get company price performance statistics such as 52-week high/low, YTD return and much more."
source: ""
tags: []
crawl_time: "2026-03-18T04:46:29.248Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/price-metric?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL."}
    - {"name":"date","in":"query","required":false,"type":"string","description":"Get data on a specific date in the past. The data is available weekly so your date will be automatically adjusted to the last day of that week."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.priceMetrics(\"AAPL\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.price_metrics('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.PriceMetrics(context.Background()).Symbol(\"MSFT\").Execute()"}
    - {"language":"PHP","code":"print_r($client->priceMetrics(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.price_metrics('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.priceMetrics(\"AAPL\"))"}
  sampleResponse: "{\n  \"data\": {\n    \"100DayEMA\": 295.7694,\n    \"100DaySMA\": 319.2297,\n    \"10DayAverageTradingVolume\": 53717320,\n    \"10DayEMA\": 247.4641,\n    \"10DaySMA\": 247.372,\n    \"14DayRSI\": 34.0517,\n    \"1MonthHigh\": 314.67,\n    \"1MonthHighDate\": \"2022-08-16\",\n    \"50DayEMA\": 277.482,\n    \"50DaySMA\": 288.313,\n    \"52WeekHigh\": 414.5,\n    \"52WeekHighDate\": \"2021-11-04\",\n    \"52WeekLow\": 206.86,\n    \"52WeekLowDate\": \"2022-05-24\",\n    \"5DayEMA\": 245.8814,\n    \"ytdPriceReturn\": 10.1819\n  },\n  \"symbol\": \"TSLA\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": {\n    \"100DayEMA\": 295.7694,\n    \"100DaySMA\": 319.2297,\n    \"10DayAverageTradingVolume\": 53717320,\n    \"10DayEMA\": 247.4641,\n    \"10DaySMA\": 247.372,\n    \"14DayRSI\": 34.0517,\n    \"1MonthHigh\": 314.67,\n    \"1MonthHighDate\": \"2022-08-16\",\n    \"50DayEMA\": 277.482,\n    \"50DaySMA\": 288.313,\n    \"52WeekHigh\": 414.5,\n    \"52WeekHighDate\": \"2021-11-04\",\n    \"52WeekLow\": 206.86,\n    \"52WeekLowDate\": \"2022-05-24\",\n    \"5DayEMA\": 245.8814,\n    \"ytdPriceReturn\": 10.1819\n  },\n  \"symbol\": \"TSLA\"\n}"
  rawContent: "Price Metrics Premium\n\nGet company price performance statistics such as 52-week high/low, YTD return and much more.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/price-metric?symbol=AAPL\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\ndateoptional\n\nGet data on a specific date in the past. The data is available weekly so your date will be automatically adjusted to the last day of that week.\n\nResponse Attributes:\n\natDate\n\nData date.\n\ndata\n\nMap key-value pair of key ratios and metrics.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.price_metrics('AAPL'))\n\nSample response\n\n{\n  \"data\": {\n    \"100DayEMA\": 295.7694,\n    \"100DaySMA\": 319.2297,\n    \"10DayAverageTradingVolume\": 53717320,\n    \"10DayEMA\": 247.4641,\n    \"10DaySMA\": 247.372,\n    \"14DayRSI\": 34.0517,\n    \"1MonthHigh\": 314.67,\n    \"1MonthHighDate\": \"2022-08-16\",\n    \"50DayEMA\": 277.482,\n    \"50DaySMA\": 288.313,\n    \"52WeekHigh\": 414.5,\n    \"52WeekHighDate\": \"2021-11-04\",\n    \"52WeekLow\": 206.86,\n    \"52WeekLowDate\": \"2022-05-24\",\n    \"5DayEMA\": 245.8814,\n    \"ytdPriceReturn\": 10.1819\n  },\n  \"symbol\": \"TSLA\"\n}"
  suggestedFilename: "price-metrics"
---

# Price Metrics Premium

## 源URL

https://finnhub.io/docs/api/price-metrics

## 描述

Get company price performance statistics such as 52-week high/low, YTD return and much more.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/price-metric?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol of the company: AAPL. |
| `date` | string | 否 | - | Get data on a specific date in the past. The data is available weekly so your date will be automatically adjusted to the last day of that week. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.priceMetrics("AAPL", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.price_metrics('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.PriceMetrics(context.Background()).Symbol("MSFT").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->priceMetrics("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.price_metrics('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.priceMetrics("AAPL"))
```

### 示例 7 (json)

```json
{
  "data": {
    "100DayEMA": 295.7694,
    "100DaySMA": 319.2297,
    "10DayAverageTradingVolume": 53717320,
    "10DayEMA": 247.4641,
    "10DaySMA": 247.372,
    "14DayRSI": 34.0517,
    "1MonthHigh": 314.67,
    "1MonthHighDate": "2022-08-16",
    "50DayEMA": 277.482,
    "50DaySMA": 288.313,
    "52WeekHigh": 414.5,
    "52WeekHighDate": "2021-11-04",
    "52WeekLow": 206.86,
    "52WeekLowDate": "2022-05-24",
    "5DayEMA": 245.8814,
    "ytdPriceReturn": 10.1819
  },
  "symbol": "TSLA"
}
```

## 文档正文

Get company price performance statistics such as 52-week high/low, YTD return and much more.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/price-metric?symbol=AAPL`

Price Metrics Premium

Get company price performance statistics such as 52-week high/low, YTD return and much more.

Method: GET

Premium: Premium Access Required

Examples:

/stock/price-metric?symbol=AAPL

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

dateoptional

Get data on a specific date in the past. The data is available weekly so your date will be automatically adjusted to the last day of that week.

Response Attributes:

atDate

Data date.

data

Map key-value pair of key ratios and metrics.

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

print(finnhub_client.price_metrics('AAPL'))

Sample response

{
  "data": {
    "100DayEMA": 295.7694,
    "100DaySMA": 319.2297,
    "10DayAverageTradingVolume": 53717320,
    "10DayEMA": 247.4641,
    "10DaySMA": 247.372,
    "14DayRSI": 34.0517,
    "1MonthHigh": 314.67,
    "1MonthHighDate": "2022-08-16",
    "50DayEMA": 277.482,
    "50DaySMA": 288.313,
    "52WeekHigh": 414.5,
    "52WeekHighDate": "2021-11-04",
    "52WeekLow": 206.86,
    "52WeekLowDate": "2022-05-24",
    "5DayEMA": 245.8814,
    "ytdPriceReturn": 10.1819
  },
  "symbol": "TSLA"
}
