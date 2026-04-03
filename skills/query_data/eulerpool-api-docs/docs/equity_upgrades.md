---
id: "url-ea38714"
type: "api"
title: "Analyst Upgrade/Downgrade History API"
url: "https://eulerpool.com/developers/api/equity/upgrades"
description: "Returns analyst upgrade/downgrade events for the given ISIN: analyst firm, action (upgrade/downgrade/init/reiterate), from-grade, to-grade, and date"
source: ""
tags: []
crawl_time: "2026-03-18T05:52:05.339Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/upgrades/{identifier}"
  responses:
    - {"code":"200","description":"Returns upgrade/downgrade events."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/upgrades/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"gradeTime\": \"2024-03-15T10:00:00.000Z\",\n  \"company\": \"Morgan Stanley\",\n  \"action\": \"upgrade\",\n  \"fromGrade\": \"Equal-Weight\",\n  \"toGrade\": \"Overweight\"\n}\n]"
  suggestedFilename: "equity_upgrades"
---

# Analyst Upgrade/Downgrade History API

## 源URL

https://eulerpool.com/developers/api/equity/upgrades

## 描述

Returns analyst upgrade/downgrade events for the given ISIN: analyst firm, action (upgrade/downgrade/init/reiterate), from-grade, to-grade, and date

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/upgrades/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns upgrade/downgrade events. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/upgrades/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "gradeTime": "2024-03-15T10:00:00.000Z",
  "company": "Morgan Stanley",
  "action": "upgrade",
  "fromGrade": "Equal-Weight",
  "toGrade": "Overweight"
}
]
```

## 文档正文

Returns analyst upgrade/downgrade events for the given ISIN: analyst firm, action (upgrade/downgrade/init/reiterate), from-grade, to-grade, and date

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/upgrades/{identifier}`
