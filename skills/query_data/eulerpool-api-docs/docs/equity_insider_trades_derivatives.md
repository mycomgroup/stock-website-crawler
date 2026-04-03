---
id: "url-69c9f826"
type: "api"
title: "SEC Derivative Insider Trades API"
url: "https://eulerpool.com/developers/api/equity/insider/trades/derivatives"
description: "Returns options/derivatives-based insider trades from SEC filings (Form 4). Includes stock option exercises, conversions, and other derivative transactions."
source: ""
tags: []
crawl_time: "2026-03-18T06:16:13.499Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/insider-trades-derivatives/{identifier}"
  responses:
    - {"code":"200","description":"Returns derivative insider trades"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/insider-trades-derivatives/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "equity_insider_trades_derivatives"
---

# SEC Derivative Insider Trades API

## 源URL

https://eulerpool.com/developers/api/equity/insider/trades/derivatives

## 描述

Returns options/derivatives-based insider trades from SEC filings (Form 4). Includes stock option exercises, conversions, and other derivative transactions.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/insider-trades-derivatives/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns derivative insider trades |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/insider-trades-derivatives/{identifier}' \
  -H 'Accept: application/json'
```

## 文档正文

Returns options/derivatives-based insider trades from SEC filings (Form 4). Includes stock option exercises, conversions, and other derivative transactions.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/insider-trades-derivatives/{identifier}`
