---
id: "url-420296f0"
type: "api"
title: "Bond Yield Curve Premium"
url: "https://finnhub.io/docs/api/bond-yield-curve"
description: "Get yield curve data for Treasury bonds."
source: ""
tags: []
crawl_time: "2026-03-18T07:31:34.732Z"
metadata:
  requestMethod: "GET"
  endpoint: "/bond/yield-curve?code=10y"
  parameters:
    - {"name":"code","in":"query","required":true,"type":"string","description":"Bond's code. You can find the list of supported code here."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.bondYieldCurve(\"10y\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.bond_yield_curve('10y'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.BondYieldCurve(context.Background()).Code(\"10y\").Execute()"}
    - {"language":"PHP","code":"print_r($client->bondYieldCurve(\"10y\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.bond_yield_curve('10y'))"}
    - {"language":"Kotlin","code":"println(apiClient.bondYieldCurve(\"10y\"))"}
  sampleResponse: "{\n  \"code\": \"10y\",\n  \"data\": [\n    {\n      \"d\": \"2022-10-31\",\n      \"v\": 4.1\n    },\n    {\n      \"d\": \"2022-11-01\",\n      \"v\": 4.07\n    }\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"code\": \"10y\",\n  \"data\": [\n    {\n      \"d\": \"2022-10-31\",\n      \"v\": 4.1\n    },\n    {\n      \"d\": \"2022-11-01\",\n      \"v\": 4.07\n    }\n  ]\n}"
  rawContent: "Bond Yield Curve Premium\n\nGet yield curve data for Treasury bonds.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/bond/yield-curve?code=10y\n\nArguments:\n\ncodeREQUIRED\n\nBond's code. You can find the list of supported code here.\n\nResponse Attributes:\n\ncode\n\nBond's code\n\ndata\n\nArray of data.\n\nd\n\nDate of the reading\n\nv\n\nValue\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.bond_yield_curve('10y'))\n\nSample response\n\n{\n  \"code\": \"10y\",\n  \"data\": [\n    {\n      \"d\": \"2022-10-31\",\n      \"v\": 4.1\n    },\n    {\n      \"d\": \"2022-11-01\",\n      \"v\": 4.07\n    }\n  ]\n}"
  suggestedFilename: "bond-yield-curve"
---

# Bond Yield Curve Premium

## 源URL

https://finnhub.io/docs/api/bond-yield-curve

## 描述

Get yield curve data for Treasury bonds.

## API 端点

**Method**: `GET`
**Endpoint**: `/bond/yield-curve?code=10y`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `code` | string | 是 | - | Bond's code. You can find the list of supported code here. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.bondYieldCurve("10y", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.bond_yield_curve('10y'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.BondYieldCurve(context.Background()).Code("10y").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->bondYieldCurve("10y"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.bond_yield_curve('10y'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.bondYieldCurve("10y"))
```

### 示例 7 (json)

```json
{
  "code": "10y",
  "data": [
    {
      "d": "2022-10-31",
      "v": 4.1
    },
    {
      "d": "2022-11-01",
      "v": 4.07
    }
  ]
}
```

## 文档正文

Get yield curve data for Treasury bonds.

## API 端点

**Method:** `GET`
**Endpoint:** `/bond/yield-curve?code=10y`

Bond Yield Curve Premium

Get yield curve data for Treasury bonds.

Method: GET

Premium: Premium Access Required

Examples:

/bond/yield-curve?code=10y

Arguments:

codeREQUIRED

Bond's code. You can find the list of supported code here.

Response Attributes:

code

Bond's code

data

Array of data.

d

Date of the reading

v

Value

Sample code
cURL
Python
Javascript
Go
Ruby
Kotlin
PHP

import finnhub
finnhub_client = finnhub.Client(api_key="")

print(finnhub_client.bond_yield_curve('10y'))

Sample response

{
  "code": "10y",
  "data": [
    {
      "d": "2022-10-31",
      "v": 4.1
    },
    {
      "d": "2022-11-01",
      "v": 4.07
    }
  ]
}
