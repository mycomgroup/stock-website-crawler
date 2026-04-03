---
id: "url-22c0cbe0"
type: "api"
title: "Country Risk API"
url: "https://eulerpool.com/developers/api/macro/country/risk"
description: "Returns equity risk premiums, country risk premiums, default spreads, and credit ratings for 249 countries (Damodaran-style, sourced from Finnhub). Updated weekly."
source: ""
tags: []
crawl_time: "2026-03-18T05:32:25.259Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/country-risk"
  responses:
    - {"code":"200","description":"Returns country risk data"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/country-risk' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"code2\": \"US\",\n  \"code3\": \"USA\",\n  \"country\": \"United States\",\n  \"currency\": \"US Dollar\",\n  \"currency_code\": \"USD\",\n  \"region\": \"Americas\",\n  \"sub_region\": \"Northern America\",\n  \"rating\": \"Aaa\",\n  \"equity_risk_premium\": 4.6,\n  \"country_risk_premium\": 0,\n  \"default_spread\": 0\n}\n]"
  suggestedFilename: "macro_country_risk"
---

# Country Risk API

## 源URL

https://eulerpool.com/developers/api/macro/country/risk

## 描述

Returns equity risk premiums, country risk premiums, default spreads, and credit ratings for 249 countries (Damodaran-style, sourced from Finnhub). Updated weekly.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/country-risk`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns country risk data |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/country-risk' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "code2": "US",
  "code3": "USA",
  "country": "United States",
  "currency": "US Dollar",
  "currency_code": "USD",
  "region": "Americas",
  "sub_region": "Northern America",
  "rating": "Aaa",
  "equity_risk_premium": 4.6,
  "country_risk_premium": 0,
  "default_spread": 0
}
]
```

## 文档正文

Returns equity risk premiums, country risk premiums, default spreads, and credit ratings for 249 countries (Damodaran-style, sourced from Finnhub). Updated weekly.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/country-risk`
