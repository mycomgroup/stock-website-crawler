---
id: "url-74d6cafa"
type: "api"
title: "Symbol Change Premium"
url: "https://finnhub.io/docs/api/symbol-change"
description: "Get a list of symbol changes for US-listed, EU-listed, NSE and ASX securities. Limit to 2000 events at a time."
source: ""
tags: []
crawl_time: "2026-03-18T04:46:39.852Z"
metadata:
  requestMethod: "GET"
  endpoint: "/ca/symbol-change?from=2022-09-01&to=2022-10-30"
  parameters:
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.symbolChange({\"from\": \"2022-10-01\", \"to\": \"2022-10-11\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.symbol_change(_from=\"2022-10-01\", to=\"2022-10-11\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.SymbolChange(context.Background()).From(\"2022-10-01\").To(\"2022-10-11\").Execute()"}
    - {"language":"PHP","code":"print_r($client->symbolChange(\"2020-01-01\", \"2020-06-11\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.symbol_change({from: \"2020-01-01\", to: \"2020-06-11\"}))"}
    - {"language":"Kotlin","code":"println(\n            apiClient.symbolChange(\n                from = \"2022-10-01\",\n                to = \"2020-10-11\")\n        )"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"atDate\": \"2022-10-05\",\n      \"newSymbol\": \"MEN.L\",\n      \"oldSymbol\": \"PPC.L\"\n    }\n  ],\n  \"fromDate\": \"2022-10-01\",\n  \"toDate\": \"2022-10-30\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"atDate\": \"2022-10-05\",\n      \"newSymbol\": \"MEN.L\",\n      \"oldSymbol\": \"PPC.L\"\n    }\n  ],\n  \"fromDate\": \"2022-10-01\",\n  \"toDate\": \"2022-10-30\"\n}"
  rawContent: "Symbol Change Premium\n\nGet a list of symbol changes for US-listed, EU-listed, NSE and ASX securities. Limit to 2000 events at a time.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/ca/symbol-change?from=2022-09-01&to=2022-10-30\n\nArguments:\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD.\n\ntoREQUIRED\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ndata\n\nArray of symbol change events.\n\natDate\n\nEvent's date.\n\nnewSymbol\n\nNew symbol.\n\noldSymbol\n\nOld symbol.\n\nfromDate\n\nFrom date.\n\ntoDate\n\nTo date.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.symbol_change(_from=\"2022-10-01\", to=\"2022-10-11\"))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"atDate\": \"2022-10-05\",\n      \"newSymbol\": \"MEN.L\",\n      \"oldSymbol\": \"PPC.L\"\n    }\n  ],\n  \"fromDate\": \"2022-10-01\",\n  \"toDate\": \"2022-10-30\"\n}"
  suggestedFilename: "symbol-change"
---

# Symbol Change Premium

## 源URL

https://finnhub.io/docs/api/symbol-change

## 描述

Get a list of symbol changes for US-listed, EU-listed, NSE and ASX securities. Limit to 2000 events at a time.

## API 端点

**Method**: `GET`
**Endpoint**: `/ca/symbol-change?from=2022-09-01&to=2022-10-30`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `from` | string | 是 | - | From date YYYY-MM-DD. |
| `to` | string | 是 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.symbolChange({"from": "2022-10-01", "to": "2022-10-11"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.symbol_change(_from="2022-10-01", to="2022-10-11"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.SymbolChange(context.Background()).From("2022-10-01").To("2022-10-11").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->symbolChange("2020-01-01", "2020-06-11"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.symbol_change({from: "2020-01-01", to: "2020-06-11"}))
```

### 示例 6 (Kotlin)

```Kotlin
println(
            apiClient.symbolChange(
                from = "2022-10-01",
                to = "2020-10-11")
        )
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "atDate": "2022-10-05",
      "newSymbol": "MEN.L",
      "oldSymbol": "PPC.L"
    }
  ],
  "fromDate": "2022-10-01",
  "toDate": "2022-10-30"
}
```

## 文档正文

Get a list of symbol changes for US-listed, EU-listed, NSE and ASX securities. Limit to 2000 events at a time.

## API 端点

**Method:** `GET`
**Endpoint:** `/ca/symbol-change?from=2022-09-01&to=2022-10-30`

Symbol Change Premium

Get a list of symbol changes for US-listed, EU-listed, NSE and ASX securities. Limit to 2000 events at a time.

Method: GET

Premium: Premium Access Required

Examples:

/ca/symbol-change?from=2022-09-01&to=2022-10-30

Arguments:

fromREQUIRED

From date YYYY-MM-DD.

toREQUIRED

To date YYYY-MM-DD.

Response Attributes:

data

Array of symbol change events.

atDate

Event's date.

newSymbol

New symbol.

oldSymbol

Old symbol.

fromDate

From date.

toDate

To date.

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

print(finnhub_client.symbol_change(_from="2022-10-01", to="2022-10-11"))

Sample response

{
  "data": [
    {
      "atDate": "2022-10-05",
      "newSymbol": "MEN.L",
      "oldSymbol": "PPC.L"
    }
  ],
  "fromDate": "2022-10-01",
  "toDate": "2022-10-30"
}
