---
id: "url-29e82300"
type: "api"
title: "Quarterly Cash Flow Statement API"
url: "https://eulerpool.com/developers/api/equity/cashflow/statement/quarterly"
description: "Returns quarterly cash flow statement data (operating, investing, financing cash flows) for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:16:58.361Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/cashflow-statement-quarterly/{identifier}"
  responses:
    - {"code":"200","description":"Returns quarterly cash flow statement."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/cashflow-statement-quarterly/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "equity_cashflow_statement_quarterly"
---

# Quarterly Cash Flow Statement API

## 源URL

https://eulerpool.com/developers/api/equity/cashflow/statement/quarterly

## 描述

Returns quarterly cash flow statement data (operating, investing, financing cash flows) for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/cashflow-statement-quarterly/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns quarterly cash flow statement. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/cashflow-statement-quarterly/{identifier}' \
  -H 'Accept: application/json'
```

## 文档正文

Returns quarterly cash flow statement data (operating, investing, financing cash flows) for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/cashflow-statement-quarterly/{identifier}`
