---
id: "url-6abcb4de"
type: "api"
title: "SWOT Analysis API"
url: "https://eulerpool.com/developers/api/equity/swot"
description: "Returns AI-generated SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:42:02.665Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/swot/{identifier}"
  responses:
    - {"code":"200","description":"Returns SWOT analysis."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/swot/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"strengths\": [],\n  \"weaknesses\": [],\n  \"opportunities\": [],\n  \"threats\": []\n}"
  suggestedFilename: "equity_swot"
---

# SWOT Analysis API

## 源URL

https://eulerpool.com/developers/api/equity/swot

## 描述

Returns AI-generated SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/swot/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns SWOT analysis. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/swot/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "strengths": [],
  "weaknesses": [],
  "opportunities": [],
  "threats": []
}
```

## 文档正文

Returns AI-generated SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/swot/{identifier}`
