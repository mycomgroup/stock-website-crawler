---
id: "url-3e661498"
type: "api"
title: "Balance Sheet API"
url: "https://eulerpool.com/developers/api/equity/balancesheet"
description: "Returns all Balance Sheet data for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:01:19.992Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/balancesheet/{identifier}"
  responses:
    - {"code":"200","description":"Returns a array of balancsheet data."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/balancesheet/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"liabilities\": 10.624,\n  \"longTermDebt\": 0,\n  \"longTermInvestments\": 0,\n  \"noteReceivableLongTerm\": 0,\n  \"otherCurrentAssets\": 1.926,\n  \"otherCurrentliabilities\": 6.812,\n  \"otherEquity\": 0,\n  \"otherLiabilities\": 0,\n  \"otherLongTermAssets\": 1.808,\n  \"otherReceivables\": 0,\n  \"period\": \"1985-06-30T00:00:00.000Z\",\n  \"propertyPlantEquipment\": 11.19,\n  \"receivables\": 25.273,\n  \"retainedEarnings\": 54.413,\n  \"shortTermDebt\": 0,\n  \"unrealizedProfitLossSecurity\": 1.808\n}\n]"
  suggestedFilename: "equity_balancesheet"
---

# Balance Sheet API

## 源URL

https://eulerpool.com/developers/api/equity/balancesheet

## 描述

Returns all Balance Sheet data for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/balancesheet/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a array of balancsheet data. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/balancesheet/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "liabilities": 10.624,
  "longTermDebt": 0,
  "longTermInvestments": 0,
  "noteReceivableLongTerm": 0,
  "otherCurrentAssets": 1.926,
  "otherCurrentliabilities": 6.812,
  "otherEquity": 0,
  "otherLiabilities": 0,
  "otherLongTermAssets": 1.808,
  "otherReceivables": 0,
  "period": "1985-06-30T00:00:00.000Z",
  "propertyPlantEquipment": 11.19,
  "receivables": 25.273,
  "retainedEarnings": 54.413,
  "shortTermDebt": 0,
  "unrealizedProfitLossSecurity": 1.808
}
]
```

## 文档正文

Returns all Balance Sheet data for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/balancesheet/{identifier}`
