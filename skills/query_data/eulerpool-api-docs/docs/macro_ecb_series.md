---
id: "url-2a91a426"
type: "api"
title: "ECB Series List API"
url: "https://eulerpool.com/developers/api/macro/ecb/series"
description: "Returns all available ECB (European Central Bank) data series: interest rates, EURIBOR, bond yields, HICP inflation, exchange rates, money supply, and lending rates"
source: ""
tags: []
crawl_time: "2026-03-18T05:55:22.760Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/ecb/series"
  responses:
    - {"code":"200","description":"Returns ECB series list"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/ecb/series' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"series_key\": \"FM.B.U2.EUR.4F.KR.MRR_FR.LEV\",\n  \"name\": \"ECB Main Refinancing Rate\",\n  \"frequency\": \"B\",\n  \"category\": \"interest_rates\",\n  \"ref_area\": \"U2\"\n}\n]"
  suggestedFilename: "macro_ecb_series"
---

# ECB Series List API

## 源URL

https://eulerpool.com/developers/api/macro/ecb/series

## 描述

Returns all available ECB (European Central Bank) data series: interest rates, EURIBOR, bond yields, HICP inflation, exchange rates, money supply, and lending rates

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/ecb/series`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns ECB series list |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/ecb/series' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "series_key": "FM.B.U2.EUR.4F.KR.MRR_FR.LEV",
  "name": "ECB Main Refinancing Rate",
  "frequency": "B",
  "category": "interest_rates",
  "ref_area": "U2"
}
]
```

## 文档正文

Returns all available ECB (European Central Bank) data series: interest rates, EURIBOR, bond yields, HICP inflation, exchange rates, money supply, and lending rates

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/ecb/series`
