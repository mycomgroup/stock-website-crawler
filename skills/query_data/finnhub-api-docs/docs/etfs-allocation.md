---
id: "url-525e63a"
type: "api"
title: "etfs-allocation"
url: "https://finnhub.io/docs/api/etfs-allocation"
description: "Get ETF equity allocation based on the characteristics of the holdings."
source: ""
tags: []
crawl_time: "2026-03-18T07:30:10.561Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/etf/allocation"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"ETF symbol."}
    - {"name":"isin","in":"query","required":false,"type":"string","description":"ETF isin."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.etfsAllocation('SPY', (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.etfs_allocation('SPY'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.EtfsAllocation(context.Background()).Symbol(\"SPY\").Execute()"}
    - {"language":"PHP","code":"print_r($client->etfsAllocation(\"SPY\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.etfs_allocation('SPY'))"}
    - {"language":"Kotlin","code":"println(apiClient.etfsAllocation(\"SPY\"))"}
  sampleResponse: "{\n  \"data\": {\n    \"largeBlend\": 38.1,\n    \"largeGrowth\": 20.41,\n    \"largeValue\": 22.03,\n    \"midBlend\": 8.67,\n    \"midGrowth\": 3.88,\n    \"midValue\": 5.94,\n    \"smallBlend\": 0.52,\n    \"smallGrowth\": 0.05,\n    \"smallValue\": 0.4\n  },\n  \"symbol\": \"SPY\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": {\n    \"largeBlend\": 38.1,\n    \"largeGrowth\": 20.41,\n    \"largeValue\": 22.03,\n    \"midBlend\": 8.67,\n    \"midGrowth\": 3.88,\n    \"midValue\": 5.94,\n    \"smallBlend\": 0.52,\n    \"smallGrowth\": 0.05,\n    \"smallValue\": 0.4\n  },\n  \"symbol\": \"SPY\"\n}"
  rawContent: ""
  suggestedFilename: "etfs-allocation"
---

# etfs-allocation

## 源URL

https://finnhub.io/docs/api/etfs-allocation

## 描述

Get ETF equity allocation based on the characteristics of the holdings.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/etf/allocation`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | ETF symbol. |
| `isin` | string | 否 | - | ETF isin. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.etfsAllocation('SPY', (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.etfs_allocation('SPY'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.EtfsAllocation(context.Background()).Symbol("SPY").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->etfsAllocation("SPY"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.etfs_allocation('SPY'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.etfsAllocation("SPY"))
```

### 示例 7 (json)

```json
{
  "data": {
    "largeBlend": 38.1,
    "largeGrowth": 20.41,
    "largeValue": 22.03,
    "midBlend": 8.67,
    "midGrowth": 3.88,
    "midValue": 5.94,
    "smallBlend": 0.52,
    "smallGrowth": 0.05,
    "smallValue": 0.4
  },
  "symbol": "SPY"
}
```

## 文档正文

Get ETF equity allocation based on the characteristics of the holdings.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/etf/allocation`
