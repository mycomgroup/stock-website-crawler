---
id: "url-248ee94b"
type: "api"
title: "Business Segments API"
url: "https://eulerpool.com/developers/api/equity/segments"
description: "Returns business segments breakdown for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:51:25.404Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/segments/{identifier}"
  responses:
    - {"code":"200","description":"Returns raw business segments data."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/segments/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"period\": \"2024-06-30T00:00:00.000Z\",\n  \"unit\": \"u_usd\",\n  \"axis\": \"srt_ProductOrServiceAxis\",\n  \"label\": \"Devices\",\n  \"value\": 4706000000,\n  \"percentage\": 1.9198603144556587,\n  \"member\": \"msft_DevicesMember\",\n  \"symbol\": \"MSFT\",\n  \"axisIndex\": 1\n}\n]"
  suggestedFilename: "equity_segments"
---

# Business Segments API

## 源URL

https://eulerpool.com/developers/api/equity/segments

## 描述

Returns business segments breakdown for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/segments/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns raw business segments data. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/segments/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "period": "2024-06-30T00:00:00.000Z",
  "unit": "u_usd",
  "axis": "srt_ProductOrServiceAxis",
  "label": "Devices",
  "value": 4706000000,
  "percentage": 1.9198603144556587,
  "member": "msft_DevicesMember",
  "symbol": "MSFT",
  "axisIndex": 1
}
]
```

## 文档正文

Returns business segments breakdown for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/segments/{identifier}`
