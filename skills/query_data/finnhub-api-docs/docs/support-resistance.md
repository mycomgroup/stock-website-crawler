---
id: "url-78ceff5e"
type: "api"
title: "Support/Resistance Premium"
url: "https://finnhub.io/docs/api/support-resistance"
description: "Get support and resistance levels for a symbol."
source: ""
tags: []
crawl_time: "2026-03-18T08:34:50.061Z"
metadata:
  requestMethod: "GET"
  endpoint: "/scan/support-resistance?symbol=IBM&resolution=D"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol"}
    - {"name":"resolution","in":"query","required":true,"type":"string","description":"Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.supportResistance(\"AAPL\", \"D\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.support_resistance('AAPL', 'D'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.SupportResistance(context.Background()).Symbol(\"AAPL\").Resolution(\"D\").Execute()"}
    - {"language":"PHP","code":"print_r($client->supportResistance(\"AAPL\", \"D\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.support_resistance('AAPL', 'D'))"}
    - {"language":"Kotlin","code":"println(apiClient.supportResistance(\"AAPL\", \"D\"))"}
  sampleResponse: "{\n  \"levels\": [\n    1.092360019683838,\n    1.1026300191879272,\n    1.113450050354004,\n    1.1233500242233276,\n    1.134719967842102,\n    1.1513700485229492\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"levels\": [\n    1.092360019683838,\n    1.1026300191879272,\n    1.113450050354004,\n    1.1233500242233276,\n    1.134719967842102,\n    1.1513700485229492\n  ]\n}"
  rawContent: "Support/Resistance Premium\n\nGet support and resistance levels for a symbol.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/scan/support-resistance?symbol=IBM&resolution=D\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol\n\nresolutionREQUIRED\n\nSupported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.\n\nResponse Attributes:\n\nlevels\n\nArray of support and resistance levels.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.support_resistance('AAPL', 'D'))\n\nSample response\n\n{\n  \"levels\": [\n    1.092360019683838,\n    1.1026300191879272,\n    1.113450050354004,\n    1.1233500242233276,\n    1.134719967842102,\n    1.1513700485229492\n  ]\n}"
  suggestedFilename: "support-resistance"
---

# Support/Resistance Premium

## 源URL

https://finnhub.io/docs/api/support-resistance

## 描述

Get support and resistance levels for a symbol.

## API 端点

**Method**: `GET`
**Endpoint**: `/scan/support-resistance?symbol=IBM&resolution=D`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol |
| `resolution` | string | 是 | - | Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.supportResistance("AAPL", "D", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.support_resistance('AAPL', 'D'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.SupportResistance(context.Background()).Symbol("AAPL").Resolution("D").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->supportResistance("AAPL", "D"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.support_resistance('AAPL', 'D'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.supportResistance("AAPL", "D"))
```

### 示例 7 (json)

```json
{
  "levels": [
    1.092360019683838,
    1.1026300191879272,
    1.113450050354004,
    1.1233500242233276,
    1.134719967842102,
    1.1513700485229492
  ]
}
```

## 文档正文

Get support and resistance levels for a symbol.

## API 端点

**Method:** `GET`
**Endpoint:** `/scan/support-resistance?symbol=IBM&resolution=D`

Support/Resistance Premium

Get support and resistance levels for a symbol.

Method: GET

Premium: Premium Access Required

Examples:

/scan/support-resistance?symbol=IBM&resolution=D

Arguments:

symbolREQUIRED

Symbol

resolutionREQUIRED

Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.

Response Attributes:

levels

Array of support and resistance levels.

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

print(finnhub_client.support_resistance('AAPL', 'D'))

Sample response

{
  "levels": [
    1.092360019683838,
    1.1026300191879272,
    1.113450050354004,
    1.1233500242233276,
    1.134719967842102,
    1.1513700485229492
  ]
}
