---
id: "url-7b637529"
type: "api"
title: "Earnings Calendar"
url: "https://finnhub.io/docs/api/earnings-calendar"
description: "Get historical and coming earnings release. EPS and Revenue in this endpoint are non-GAAP, which means they are adjusted to exclude some one-time or unusual items. This is the same data investors usually react to and talked about on the media. Estimates are sourced from both sell-side and buy-side analysts."
source: ""
tags: []
crawl_time: "2026-03-18T08:13:17.405Z"
metadata:
  requestMethod: "GET"
  endpoint: "/calendar/earnings?from=2025-08-01&to=2025-08-10"
  parameters:
    - {"name":"from","in":"query","required":false,"type":"string","description":"From date: 2020-03-15."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To date: 2020-03-16."}
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Filter by symbol: AAPL."}
    - {"name":"international","in":"query","required":false,"type":"boolean","description":"Set to true to include international markets. Default value is false"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.earningsCalendar({\"from\": \"2021-06-01\", \"to\": \"2021-06-30\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.earnings_calendar(_from=\"2021-06-10\", to=\"2021-06-30\", symbol=\"\", international=False))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.EarningsCalendar(context.Background()).From(\"2021-07-01\").To(\"2021-07-30\").Execute()"}
    - {"language":"PHP","code":"print_r($client->earningsCalendar(\"2020-06-10\", \"2020-06-30\", null, false));"}
    - {"language":"Ruby","code":"puts(finnhub_client.earnings_calendar({from: \"2021-06-10\", to: \"2021-06-30\", symbol: \"\", international: false}))"}
    - {"language":"Kotlin","code":"println(apiClient.earningsCalendar(from = \"2020-06-10\", to = \"2020-06-30\", symbol = \"\", international = false))"}
  sampleResponse: "{\n  \"earningsCalendar\": [\n    {\n      \"date\": \"2020-01-28\",\n      \"epsActual\": 4.99,\n      \"epsEstimate\": 4.5474,\n      \"hour\": \"amc\",\n      \"quarter\": 1,\n      \"revenueActual\": 91819000000,\n      \"revenueEstimate\": 88496400810,\n      \"symbol\": \"AAPL\",\n      \"year\": 2020\n    },\n    {\n      \"date\": \"2019-10-30\",\n      \"epsActual\": 3.03,\n      \"epsEstimate\": 2.8393,\n      \"hour\": \"amc\",\n      \"quarter\": 4,\n      \"revenueActual\": 64040000000,\n      \"revenueEstimate\": 62985161760,\n      \"symbol\": \"AAPL\",\n      \"year\": 2019\n    }\n   ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"earningsCalendar\": [\n    {\n      \"date\": \"2020-01-28\",\n      \"epsActual\": 4.99,\n      \"epsEstimate\": 4.5474,\n      \"hour\": \"amc\",\n      \"quarter\": 1,\n      \"revenueActual\": 91819000000,\n      \"revenueEstimate\": 88496400810,\n      \"symbol\": \"AAPL\",\n      \"year\": 2020\n    },\n    {\n      \"date\": \"2019-10-30\",\n      \"epsActual\": 3.03,\n      \"epsEstimate\": 2.8393,\n      \"hour\": \"amc\",\n      \"quarter\": 4,\n      \"revenueActual\": 64040000000,\n      \"revenueEstimate\": 62985161760,\n      \"symbol\": \"AAPL\",\n      \"year\": 2019\n    }\n   ]\n}"
  rawContent: "Earnings Calendar\n\nGet historical and coming earnings release. EPS and Revenue in this endpoint are non-GAAP, which means they are adjusted to exclude some one-time or unusual items. This is the same data investors usually react to and talked about on the media. Estimates are sourced from both sell-side and buy-side analysts.\n\nMethod: GET\n\nFree Tier: 1 month of historical earnings and new updates\n\nExamples:\n\n/calendar/earnings?from=2025-08-01&to=2025-08-10\n\n/calendar/earnings?from=2024-03-01&to=2025-08-09&symbol=AAPL\n\nArguments:\n\nfromoptional\n\nFrom date: 2020-03-15.\n\ntooptional\n\nTo date: 2020-03-16.\n\nsymboloptional\n\nFilter by symbol: AAPL.\n\ninternationaloptional\n\nSet to true to include international markets. Default value is false\n\nResponse Attributes:\n\nearningsCalendar\n\nArray of earnings release.\n\ndate\n\nDate.\n\nepsActual\n\nEPS actual.\n\nepsEstimate\n\nEPS estimate.\n\nhour\n\nIndicates whether the earnings is announced before market open(bmo), after market close(amc), or during market hour(dmh).\n\nquarter\n\nEarnings quarter.\n\nrevenueActual\n\nRevenue actual.\n\nrevenueEstimate\n\nRevenue estimate including Finnhub's proprietary estimates.\n\nsymbol\n\nSymbol.\n\nyear\n\nEarnings year.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.earnings_calendar(_from=\"2021-06-10\", to=\"2021-06-30\", symbol=\"\", international=False))\n\nSample response\n\n{\n  \"earningsCalendar\": [\n    {\n      \"date\": \"2020-01-28\",\n      \"epsActual\": 4.99,\n      \"epsEstimate\": 4.5474,\n      \"hour\": \"amc\",\n      \"quarter\": 1,\n      \"revenueActual\": 91819000000,\n      \"revenueEstimate\": 88496400810,\n      \"symbol\": \"AAPL\",\n      \"year\": 2020\n    },\n    {\n      \"date\": \"2019-10-30\",\n      \"epsActual\": 3.03,\n      \"epsEstimate\": 2.8393,\n      \"hour\": \"amc\",\n      \"quarter\": 4,\n      \"revenueActual\": 64040000000,\n      \"revenueEstimate\": 62985161760,\n      \"symbol\": \"AAPL\",\n      \"year\": 2019\n    }\n   ]\n}"
  suggestedFilename: "earnings-calendar"
---

# Earnings Calendar

## 源URL

https://finnhub.io/docs/api/earnings-calendar

## 描述

Get historical and coming earnings release. EPS and Revenue in this endpoint are non-GAAP, which means they are adjusted to exclude some one-time or unusual items. This is the same data investors usually react to and talked about on the media. Estimates are sourced from both sell-side and buy-side analysts.

## API 端点

**Method**: `GET`
**Endpoint**: `/calendar/earnings?from=2025-08-01&to=2025-08-10`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `from` | string | 否 | - | From date: 2020-03-15. |
| `to` | string | 否 | - | To date: 2020-03-16. |
| `symbol` | string | 否 | - | Filter by symbol: AAPL. |
| `international` | boolean | 否 | - | Set to true to include international markets. Default value is false |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.earningsCalendar({"from": "2021-06-01", "to": "2021-06-30"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.earnings_calendar(_from="2021-06-10", to="2021-06-30", symbol="", international=False))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.EarningsCalendar(context.Background()).From("2021-07-01").To("2021-07-30").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->earningsCalendar("2020-06-10", "2020-06-30", null, false));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.earnings_calendar({from: "2021-06-10", to: "2021-06-30", symbol: "", international: false}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.earningsCalendar(from = "2020-06-10", to = "2020-06-30", symbol = "", international = false))
```

### 示例 7 (json)

```json
{
  "earningsCalendar": [
    {
      "date": "2020-01-28",
      "epsActual": 4.99,
      "epsEstimate": 4.5474,
      "hour": "amc",
      "quarter": 1,
      "revenueActual": 91819000000,
      "revenueEstimate": 88496400810,
      "symbol": "AAPL",
      "year": 2020
    },
    {
      "date": "2019-10-30",
      "epsActual": 3.03,
      "epsEstimate": 2.8393,
      "hour": "amc",
      "quarter": 4,
      "revenueActual": 64040000000,
      "revenueEstimate": 62985161760,
      "symbol": "AAPL",
      "year": 2019
    }
   ]
}
```

## 文档正文

Get historical and coming earnings release. EPS and Revenue in this endpoint are non-GAAP, which means they are adjusted to exclude some one-time or unusual items. This is the same data investors usually react to and talked about on the media. Estimates are sourced from both sell-side and buy-side analysts.

## API 端点

**Method:** `GET`
**Endpoint:** `/calendar/earnings?from=2025-08-01&to=2025-08-10`

Earnings Calendar

Get historical and coming earnings release. EPS and Revenue in this endpoint are non-GAAP, which means they are adjusted to exclude some one-time or unusual items. This is the same data investors usually react to and talked about on the media. Estimates are sourced from both sell-side and buy-side analysts.

Method: GET

Free Tier: 1 month of historical earnings and new updates

Examples:

/calendar/earnings?from=2025-08-01&to=2025-08-10

/calendar/earnings?from=2024-03-01&to=2025-08-09&symbol=AAPL

Arguments:

fromoptional

From date: 2020-03-15.

tooptional

To date: 2020-03-16.

symboloptional

Filter by symbol: AAPL.

internationaloptional

Set to true to include international markets. Default value is false

Response Attributes:

earningsCalendar

Array of earnings release.

date

Date.

epsActual

EPS actual.

epsEstimate

EPS estimate.

hour

Indicates whether the earnings is announced before market open(bmo), after market close(amc), or during market hour(dmh).

quarter

Earnings quarter.

revenueActual

Revenue actual.

revenueEstimate

Revenue estimate including Finnhub's proprietary estimates.

symbol

Symbol.

year

Earnings year.

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

print(finnhub_client.earnings_calendar(_from="2021-06-10", to="2021-06-30", symbol="", international=False))

Sample response

{
  "earningsCalendar": [
    {
      "date": "2020-01-28",
      "epsActual": 4.99,
      "epsEstimate": 4.5474,
      "hour": "amc",
      "quarter": 1,
      "revenueActual": 91819000000,
      "revenueEstimate": 88496400810,
      "symbol": "AAPL",
      "year": 2020
    },
    {
      "date": "2019-10-30",
      "epsActual": 3.03,
      "epsEstimate": 2.8393,
      "hour": "amc",
      "quarter": 4,
      "revenueActual": 64040000000,
      "revenueEstimate": 62985161760,
      "symbol": "AAPL",
      "year": 2019
    }
   ]
}
