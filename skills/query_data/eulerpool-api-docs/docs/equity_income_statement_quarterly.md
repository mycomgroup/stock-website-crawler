---
id: "url-340778f8"
type: "api"
title: "Quarterly Income Statement API"
url: "https://eulerpool.com/developers/api/equity/income/statement/quarterly"
description: "Returns quarterly income statement data (revenue, EBIT, net income, EPS) for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:16:07.069Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/income-statement-quarterly/{identifier}"
  responses:
    - {"code":"200","description":"Returns quarterly income statement."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/income-statement-quarterly/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "equity_income_statement_quarterly"
---

# Quarterly Income Statement API

## 源URL

https://eulerpool.com/developers/api/equity/income/statement/quarterly

## 描述

Returns quarterly income statement data (revenue, EBIT, net income, EPS) for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/income-statement-quarterly/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns quarterly income statement. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/income-statement-quarterly/{identifier}' \
  -H 'Accept: application/json'
```

## 文档正文

Returns quarterly income statement data (revenue, EBIT, net income, EPS) for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/income-statement-quarterly/{identifier}`
