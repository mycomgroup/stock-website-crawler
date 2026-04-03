---
id: "url-5cb7864a"
type: "api"
title: "Macro Calendar API"
url: "https://eulerpool.com/developers/api/macro/calendar"
description: "Returns a list of dates relevant for macro da in the given timeframe and countries."
source: ""
tags: []
crawl_time: "2026-03-18T05:50:05.456Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/calendar"
  responses:
    - {"code":"200","description":"Returns a array of ownership data including name, percentage, share count, change since last time, the date where shares had been filed"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/calendar?language=de' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"name\": \"API-Rohölbestandsänderung\",\n  \"country_code\": \"us\",\n  \"timestamp\": 1729110600000,\n  \"actual_currency\": \"usd\",\n  \"actual_value\": 1,\n  \"actual_multiplier\": 1000,\n  \"previous_currency\": \"usd\",\n  \"previous_value\": 0.5,\n  \"previous_multiplier\": 1000,\n  \"consensus_currency\": \"usd\",\n  \"consensus_value\": 0.5,\n  \"consensus_multiplier\": 1000,\n  \"forecast_currency\": \"usd\",\n  \"forecast_value\": 0.8,\n  \"forecast_multiplier\": 1000,\n  \"full_day\": \"usd\",\n  \"reference_date\": \"usd\"\n}\n]"
  suggestedFilename: "macro_calendar"
---

# Macro Calendar API

## 源URL

https://eulerpool.com/developers/api/macro/calendar

## 描述

Returns a list of dates relevant for macro da in the given timeframe and countries.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/calendar`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a array of ownership data including name, percentage, share count, change since last time, the date where shares had been filed |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/calendar?language=de' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "name": "API-Rohölbestandsänderung",
  "country_code": "us",
  "timestamp": 1729110600000,
  "actual_currency": "usd",
  "actual_value": 1,
  "actual_multiplier": 1000,
  "previous_currency": "usd",
  "previous_value": 0.5,
  "previous_multiplier": 1000,
  "consensus_currency": "usd",
  "consensus_value": 0.5,
  "consensus_multiplier": 1000,
  "forecast_currency": "usd",
  "forecast_value": 0.8,
  "forecast_multiplier": 1000,
  "full_day": "usd",
  "reference_date": "usd"
}
]
```

## 文档正文

Returns a list of dates relevant for macro da in the given timeframe and countries.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/calendar`
