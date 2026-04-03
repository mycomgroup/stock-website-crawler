---
id: "url-7a38c1f0"
type: "api"
title: "Bridge Volumes API"
url: "https://eulerpool.com/developers/api/crypto/extended/bridge/volumes"
description: "Returns cross-chain bridge daily volumes. Standalone access to bridge flow data for cross-chain analytics."
source: ""
tags: []
crawl_time: "2026-03-18T06:15:11.067Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/bridge-volumes"
  responses:
    - {"code":"200","description":"Returns bridge volume data"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/bridge-volumes' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"bridge_name\": \"Stargate\",\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"volume_24h\": 50000000\n}\n]"
  suggestedFilename: "crypto_extended_bridge_volumes"
---

# Bridge Volumes API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/bridge/volumes

## 描述

Returns cross-chain bridge daily volumes. Standalone access to bridge flow data for cross-chain analytics.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/bridge-volumes`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns bridge volume data |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/bridge-volumes' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "bridge_name": "Stargate",
  "date": "2024-01-15T00:00:00.000Z",
  "volume_24h": 50000000
}
]
```

## 文档正文

Returns cross-chain bridge daily volumes. Standalone access to bridge flow data for cross-chain analytics.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/bridge-volumes`
