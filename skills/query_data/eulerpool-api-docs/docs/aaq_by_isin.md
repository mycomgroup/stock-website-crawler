# AAQS Score

## 源URL

https://eulerpool.com/developers/api/aaq/by/isin

## 描述

Returns the AlleAktien Quality Score (AAQS) for a stock by ISIN

## 请求端点

**方法**: GET

```text
/api/1/aaq/by-isin/{isin}
```

## Responses

### 200
AAQS data

### 401
Invalid or missing API key

### 404
Resource not found

## 请求示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/aaq/by-isin/US5949181045' \
  -H 'Accept: application/json'
```

## 响应示例

```json
{
  "isin": "US0378331005",
  "score": 8
}
```
