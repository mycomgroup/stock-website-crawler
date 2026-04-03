---
id: "url-67812ede"
type: "api"
title: "stock-bidask"
url: "https://finnhub.io/docs/api/stock-bidask"
description: "Get last bid/ask data for US stocks."
source: ""
tags: []
crawl_time: "2026-03-18T04:36:02.984Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/stock/bidask"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.stockBidask(\"AAPL\", (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.last_bid_ask('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.StockBidask(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->stockBidask(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.stock_bidask('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.stockBidask(\"AAPL\"))"}
  sampleResponse: "{\n  \"a\": 338.65,\n  \"av\": 2,\n  \"b\": 338.61,\n  \"bv\": 2,\n  \"t\": 1591995678874\n}"
  curlExample: ""
  jsonExample: "{\n  \"a\": 338.65,\n  \"av\": 2,\n  \"b\": 338.61,\n  \"bv\": 2,\n  \"t\": 1591995678874\n}"
  rawContent: ""
  suggestedFilename: "stock-bidask"
---

# stock-bidask

## 源URL

https://finnhub.io/docs/api/stock-bidask

## 描述

Get last bid/ask data for US stocks.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/stock/bidask`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.stockBidask("AAPL", (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.last_bid_ask('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.StockBidask(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->stockBidask("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.stock_bidask('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.stockBidask("AAPL"))
```

### 示例 7 (json)

```json
{
  "a": 338.65,
  "av": 2,
  "b": 338.61,
  "bv": 2,
  "t": 1591995678874
}
```

## 文档正文

Get last bid/ask data for US stocks.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/stock/bidask`
