---
id: "url-513f22f5"
type: "api"
title: "Economic Calendar Premium"
url: "https://finnhub.io/docs/api/economic-calendar"
description: "Get recent and upcoming economic releases.Historical events and surprises are available for Enterprise clients."
source: ""
tags: []
crawl_time: "2026-03-18T08:13:28.156Z"
metadata:
  requestMethod: "GET"
  endpoint: "/calendar/economic"
  parameters:
    - {"name":"from","in":"query","required":false,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.economicCalendar((error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.calendar_economic())"}
    - {"language":"Go","code":"res, _, err := finnhubClient.EconomicCalendar(context.Background()).Execute()"}
    - {"language":"PHP","code":"print_r($client->economicCalendar());"}
    - {"language":"Ruby","code":"puts(finnhub_client.economic_calendar())"}
    - {"language":"Kotlin","code":"println(apiClient.economicCalendar())"}
  sampleResponse: "{\n  \"economicCalendar\": [\n    {\n      \"actual\": 8.4,\n      \"country\": \"AU\",\n      \"estimate\": 6.9,\n      \"event\": \"Australia - Current Account Balance\",\n      \"impact\": \"low\",\n      \"prev\": 1,\n      \"time\": \"2020-06-02 01:30:00\",\n      \"unit\": \"AUD\"\n    },\n    {\n      \"actual\": 0.5,\n      \"country\": \"AU\",\n      \"estimate\": 0.4,\n      \"event\": \"Australia- Net Exports\",\n      \"impact\": \"low\",\n      \"prev\": -0.1,\n      \"time\": \"2020-06-02 01:30:00\",\n      \"unit\": \"%\"\n    }\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"economicCalendar\": [\n    {\n      \"actual\": 8.4,\n      \"country\": \"AU\",\n      \"estimate\": 6.9,\n      \"event\": \"Australia - Current Account Balance\",\n      \"impact\": \"low\",\n      \"prev\": 1,\n      \"time\": \"2020-06-02 01:30:00\",\n      \"unit\": \"AUD\"\n    },\n    {\n      \"actual\": 0.5,\n      \"country\": \"AU\",\n      \"estimate\": 0.4,\n      \"event\": \"Australia- Net Exports\",\n      \"impact\": \"low\",\n      \"prev\": -0.1,\n      \"time\": \"2020-06-02 01:30:00\",\n      \"unit\": \"%\"\n    }\n  ]\n}"
  rawContent: "Economic Calendar Premium\n\nGet recent and upcoming economic releases.\n\nHistorical events and surprises are available for Enterprise clients.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/calendar/economic\n\nArguments:\n\nfromoptional\n\nFrom date YYYY-MM-DD.\n\ntooptional\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\neconomicCalendar\n\nArray of economic events.\n\nactual\n\nActual release\n\ncountry\n\nCountry\n\nestimate\n\nEstimate\n\nevent\n\nEvent\n\nimpact\n\nImpact level\n\nprev\n\nPrevious release\n\ntime\n\nRelease time\n\nunit\n\nUnit\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.calendar_economic())\n\nSample response\n\n{\n  \"economicCalendar\": [\n    {\n      \"actual\": 8.4,\n      \"country\": \"AU\",\n      \"estimate\": 6.9,\n      \"event\": \"Australia - Current Account Balance\",\n      \"impact\": \"low\",\n      \"prev\": 1,\n      \"time\": \"2020-06-02 01:30:00\",\n      \"unit\": \"AUD\"\n    },\n    {\n      \"actual\": 0.5,\n      \"country\": \"AU\",\n      \"estimate\": 0.4,\n      \"event\": \"Australia- Net Exports\",\n      \"impact\": \"low\",\n      \"prev\": -0.1,\n      \"time\": \"2020-06-02 01:30:00\",\n      \"unit\": \"%\"\n    }\n  ]\n}"
  suggestedFilename: "economic-calendar"
---

# Economic Calendar Premium

## 源URL

https://finnhub.io/docs/api/economic-calendar

## 描述

Get recent and upcoming economic releases.Historical events and surprises are available for Enterprise clients.

## API 端点

**Method**: `GET`
**Endpoint**: `/calendar/economic`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `from` | string | 否 | - | From date YYYY-MM-DD. |
| `to` | string | 否 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.economicCalendar((error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.calendar_economic())
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.EconomicCalendar(context.Background()).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->economicCalendar());
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.economic_calendar())
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.economicCalendar())
```

### 示例 7 (json)

```json
{
  "economicCalendar": [
    {
      "actual": 8.4,
      "country": "AU",
      "estimate": 6.9,
      "event": "Australia - Current Account Balance",
      "impact": "low",
      "prev": 1,
      "time": "2020-06-02 01:30:00",
      "unit": "AUD"
    },
    {
      "actual": 0.5,
      "country": "AU",
      "estimate": 0.4,
      "event": "Australia- Net Exports",
      "impact": "low",
      "prev": -0.1,
      "time": "2020-06-02 01:30:00",
      "unit": "%"
    }
  ]
}
```

## 文档正文

Get recent and upcoming economic releases.Historical events and surprises are available for Enterprise clients.

## API 端点

**Method:** `GET`
**Endpoint:** `/calendar/economic`

Economic Calendar Premium

Get recent and upcoming economic releases.

Historical events and surprises are available for Enterprise clients.

Method: GET

Premium: Premium Access Required

Examples:

/calendar/economic

Arguments:

fromoptional

From date YYYY-MM-DD.

tooptional

To date YYYY-MM-DD.

Response Attributes:

economicCalendar

Array of economic events.

actual

Actual release

country

Country

estimate

Estimate

event

Event

impact

Impact level

prev

Previous release

time

Release time

unit

Unit

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

print(finnhub_client.calendar_economic())

Sample response

{
  "economicCalendar": [
    {
      "actual": 8.4,
      "country": "AU",
      "estimate": 6.9,
      "event": "Australia - Current Account Balance",
      "impact": "low",
      "prev": 1,
      "time": "2020-06-02 01:30:00",
      "unit": "AUD"
    },
    {
      "actual": 0.5,
      "country": "AU",
      "estimate": 0.4,
      "event": "Australia- Net Exports",
      "impact": "low",
      "prev": -0.1,
      "time": "2020-06-02 01:30:00",
      "unit": "%"
    }
  ]
}
