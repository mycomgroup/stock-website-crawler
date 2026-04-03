---
id: "url-370a8338"
type: "api"
title: "ESG Rating API"
url: "https://eulerpool.com/developers/api/equity/esg/rating"
description: "Returns ESG rating for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:58:41.499Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/esg-rating/{identifier}"
  responses:
    - {"code":"200","description":"Returns ESG rating data."}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/esg-rating/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"symbol\": \"MSFT\",\n  \"totalESGScore\": 82.49834,\n  \"environmentScore\": 74.24722,\n  \"socialScore\": 82.12883,\n  \"governanceScore\": 91.11896,\n  \"adultContent\": false,\n  \"alcoholic\": false,\n  \"animalTesting\": false,\n  \"firearms\": false,\n  \"gambling\": false,\n  \"tobacco\": false,\n  \"nuclear\": false,\n  \"co2EmissionTotal\": 8222363,\n  \"carbonReductionPolicy\": \"True\",\n  \"climateStrategy\": null,\n  \"humanRightsPolicy\": true,\n  \"workplaceHealthSafety\": true,\n  \"totalWomenPercentage\": 33.1,\n  \"environmentalReporting\": true,\n  \"recyclingPolicy\": true\n}"
  suggestedFilename: "equity_esg_rating"
---

# ESG Rating API

## 源URL

https://eulerpool.com/developers/api/equity/esg/rating

## 描述

Returns ESG rating for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/esg-rating/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns ESG rating data. |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/esg-rating/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "symbol": "MSFT",
  "totalESGScore": 82.49834,
  "environmentScore": 74.24722,
  "socialScore": 82.12883,
  "governanceScore": 91.11896,
  "adultContent": false,
  "alcoholic": false,
  "animalTesting": false,
  "firearms": false,
  "gambling": false,
  "tobacco": false,
  "nuclear": false,
  "co2EmissionTotal": 8222363,
  "carbonReductionPolicy": "True",
  "climateStrategy": null,
  "humanRightsPolicy": true,
  "workplaceHealthSafety": true,
  "totalWomenPercentage": 33.1,
  "environmentalReporting": true,
  "recyclingPolicy": true
}
```

## 文档正文

Returns ESG rating for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/esg-rating/{identifier}`
