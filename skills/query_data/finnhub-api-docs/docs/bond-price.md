---
id: "url-2f0b1f96"
type: "api"
title: "bond-price"
url: "https://finnhub.io/docs/api/bond-price"
description: "Get bond's price data. The following datasets are supported:\n  \n    \n      Exchange\n      Segment\n      Delay\n    \n  \n  \n  \n      US Government Bonds\n      Government Bonds\n      End-of-day\n    \n    \n      FINRA Trace\n      BTDS: US Corporate Bonds\n      Delayed 4h\n    \n    \n      FINRA Trace\n      144A Bonds\n      Delayed 4h"
source: ""
tags: []
crawl_time: "2026-03-18T04:34:34.364Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/bond/price"
  parameters:
    - {"name":"isin","in":"query","required":true,"type":"string","description":"ISIN."}
    - {"name":"from","in":"query","required":true,"type":"integer","description":"UNIX timestamp. Interval initial value."}
    - {"name":"to","in":"query","required":true,"type":"integer","description":"UNIX timestamp. Interval end value."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.bondPrice(\"US912810TD00\", 1590988249, 1649099548, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.bond_price('US912810TD00', 1590988249, 1649099548))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.BondPrice(context.Background()).Isin(\"US912810TD00\").From(1590988249).To(1649099548).Execute()"}
    - {"language":"PHP","code":"print_r($client->bondPrice(\"US912810TD00\", 1590988249, 1649099548));"}
    - {"language":"Ruby","code":"puts(finnhub_client.bond_price('US912810TD00', 1590988249, 1649099548))"}
    - {"language":"Kotlin","code":"println(apiClient.bondPrice(\"US912810TD00\", 1590988249, 1649099548))"}
  sampleResponse: "{\n  \"c\":[\n    97.5,\n    97.96875,\n    98.78125,\n  ],\n  \"s\":\"ok\",\n  \"t\":[\n    1644883200,\n    1644969600,\n    1645056000,\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"c\":[\n    97.5,\n    97.96875,\n    98.78125,\n  ],\n  \"s\":\"ok\",\n  \"t\":[\n    1644883200,\n    1644969600,\n    1645056000,\n  ]\n}"
  rawContent: ""
  suggestedFilename: "bond-price"
---

# bond-price

## 源URL

https://finnhub.io/docs/api/bond-price

## 描述

Get bond's price data. The following datasets are supported:
  
    
      Exchange
      Segment
      Delay
    
  
  
  
      US Government Bonds
      Government Bonds
      End-of-day
    
    
      FINRA Trace
      BTDS: US Corporate Bonds
      Delayed 4h
    
    
      FINRA Trace
      144A Bonds
      Delayed 4h

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/bond/price`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `isin` | string | 是 | - | ISIN. |
| `from` | integer | 是 | - | UNIX timestamp. Interval initial value. |
| `to` | integer | 是 | - | UNIX timestamp. Interval end value. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.bondPrice("US912810TD00", 1590988249, 1649099548, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.bond_price('US912810TD00', 1590988249, 1649099548))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.BondPrice(context.Background()).Isin("US912810TD00").From(1590988249).To(1649099548).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->bondPrice("US912810TD00", 1590988249, 1649099548));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.bond_price('US912810TD00', 1590988249, 1649099548))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.bondPrice("US912810TD00", 1590988249, 1649099548))
```

### 示例 7 (json)

```json
{
  "c":[
    97.5,
    97.96875,
    98.78125,
  ],
  "s":"ok",
  "t":[
    1644883200,
    1644969600,
    1645056000,
  ]
}
```

## 文档正文

Get bond's price data. The following datasets are supported:
  
    
      Exchange
      Segment
      Delay
    
  
  
  
      US Government Bonds
      Government Bonds
      End-of-day
    
    
      FINRA Trace
      BTDS: US Corporate Bonds
      Delayed 4h
    
    
      FINRA Trace
      144A Bonds
      Delayed 4h

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/bond/price`
