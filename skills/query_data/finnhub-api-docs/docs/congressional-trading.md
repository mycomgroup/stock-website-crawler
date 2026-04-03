---
id: "url-161284"
type: "api"
title: "Congressional Trading Premium"
url: "https://finnhub.io/docs/api/congressional-trading"
description: "Get stock trades data disclosed by members of congress."
source: ""
tags: []
crawl_time: "2026-03-18T09:52:37.853Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/congressional-trading?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.congressionalTrading(\"AAPL\", '2020-01-01', '2023-03-31', (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.congressional_trading('AAPL', '2020-01-01', '2023-03-31'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.CongressionalTrading(context.Background()).Symbol(\"MSFT\").From(\"2020-01-01\").To(\"2023-01-02\").Execute()"}
    - {"language":"PHP","code":"print_r($client->congressionalTrading(\"AAPL\", \"2020-01-01\", \"2023-03-31\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.congressional_trading('AAPL', '2020-01-01', '2023-03-31'))"}
    - {"language":"Kotlin","code":"println(apiClient.congressionalTrading(\"AAPL\", \"2020-01-01\", \"2023-03-31\"))"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"amountFrom\": 100001,\n      \"amountTo\": 250000,\n      \"assetName\": \"Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)\",\n      \"filingDate\": \"2015-05-14\",\n      \"name\": \"Lamar Alexander\",\n      \"ownerType\": \"Spouse\",\n      \"position\": \"senator\",\n      \"symbol\": \"MLPTX\",\n      \"transactionDate\": \"2014-04-04\",\n      \"transactionType\": \"Purchase\"\n    },\n    {\n      \"amountFrom\": 1001,\n      \"amountTo\": 15000,\n      \"assetName\": \"Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)\",\n      \"filingDate\": \"2015-05-14\",\n      \"name\": \"Lamar Alexander\",\n      \"ownerType\": \"Spouse\",\n      \"position\": \"senator\",\n      \"symbol\": \"MLPTX\",\n      \"transactionDate\": \"2014-02-07\",\n      \"transactionType\": \"Purchase\"\n    }\n  ],\n  \"symbol\": \"MLPTX\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"amountFrom\": 100001,\n      \"amountTo\": 250000,\n      \"assetName\": \"Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)\",\n      \"filingDate\": \"2015-05-14\",\n      \"name\": \"Lamar Alexander\",\n      \"ownerType\": \"Spouse\",\n      \"position\": \"senator\",\n      \"symbol\": \"MLPTX\",\n      \"transactionDate\": \"2014-04-04\",\n      \"transactionType\": \"Purchase\"\n    },\n    {\n      \"amountFrom\": 1001,\n      \"amountTo\": 15000,\n      \"assetName\": \"Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)\",\n      \"filingDate\": \"2015-05-14\",\n      \"name\": \"Lamar Alexander\",\n      \"ownerType\": \"Spouse\",\n      \"position\": \"senator\",\n      \"symbol\": \"MLPTX\",\n      \"transactionDate\": \"2014-02-07\",\n      \"transactionType\": \"Purchase\"\n    }\n  ],\n  \"symbol\": \"MLPTX\"\n}"
  rawContent: "Congressional Trading Premium\n\nGet stock trades data disclosed by members of congress.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/congressional-trading?symbol=AAPL\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD.\n\ntoREQUIRED\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ndata\n\nArray of stock trades.\n\namountFrom\n\nTransaction amount from.\n\namountTo\n\nTransaction amount to.\n\nassetName\n\nAsset name.\n\nfilingDate\n\nFiling date.\n\nname\n\nName of the representative.\n\nownerType\n\nOwner Type.\n\nposition\n\nPosition.\n\nsymbol\n\nSymbol.\n\ntransactionDate\n\nTransaction date.\n\ntransactionType\n\nTransaction type Sale or Purchase.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.congressional_trading('AAPL', '2020-01-01', '2023-03-31'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"amountFrom\": 100001,\n      \"amountTo\": 250000,\n      \"assetName\": \"Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)\",\n      \"filingDate\": \"2015-05-14\",\n      \"name\": \"Lamar Alexander\",\n      \"ownerType\": \"Spouse\",\n      \"position\": \"senator\",\n      \"symbol\": \"MLPTX\",\n      \"transactionDate\": \"2014-04-04\",\n      \"transactionType\": \"Purchase\"\n    },\n    {\n      \"amountFrom\": 1001,\n      \"amountTo\": 15000,\n      \"assetName\": \"Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)\",\n      \"filingDate\": \"2015-05-14\",\n      \"name\": \"Lamar Alexander\",\n      \"ownerType\": \"Spouse\",\n      \"position\": \"senator\",\n      \"symbol\": \"MLPTX\",\n      \"transactionDate\": \"2014-02-07\",\n      \"transactionType\": \"Purchase\"\n    }\n  ],\n  \"symbol\": \"MLPTX\"\n}"
  suggestedFilename: "congressional-trading"
---

# Congressional Trading Premium

## 源URL

https://finnhub.io/docs/api/congressional-trading

## 描述

Get stock trades data disclosed by members of congress.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/congressional-trading?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol of the company: AAPL. |
| `from` | string | 是 | - | From date YYYY-MM-DD. |
| `to` | string | 是 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.congressionalTrading("AAPL", '2020-01-01', '2023-03-31', (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.congressional_trading('AAPL', '2020-01-01', '2023-03-31'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.CongressionalTrading(context.Background()).Symbol("MSFT").From("2020-01-01").To("2023-01-02").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->congressionalTrading("AAPL", "2020-01-01", "2023-03-31"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.congressional_trading('AAPL', '2020-01-01', '2023-03-31'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.congressionalTrading("AAPL", "2020-01-01", "2023-03-31"))
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "amountFrom": 100001,
      "amountTo": 250000,
      "assetName": "Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)",
      "filingDate": "2015-05-14",
      "name": "Lamar Alexander",
      "ownerType": "Spouse",
      "position": "senator",
      "symbol": "MLPTX",
      "transactionDate": "2014-04-04",
      "transactionType": "Purchase"
    },
    {
      "amountFrom": 1001,
      "amountTo": 15000,
      "assetName": "Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)",
      "filingDate": "2015-05-14",
      "name": "Lamar Alexander",
      "ownerType": "Spouse",
      "position": "senator",
      "symbol": "MLPTX",
      "transactionDate": "2014-02-07",
      "transactionType": "Purchase"
    }
  ],
  "symbol": "MLPTX"
}
```

## 文档正文

Get stock trades data disclosed by members of congress.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/congressional-trading?symbol=AAPL`

Congressional Trading Premium

Get stock trades data disclosed by members of congress.

Method: GET

Premium: Premium Access Required

Examples:

/stock/congressional-trading?symbol=AAPL

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

fromREQUIRED

From date YYYY-MM-DD.

toREQUIRED

To date YYYY-MM-DD.

Response Attributes:

data

Array of stock trades.

amountFrom

Transaction amount from.

amountTo

Transaction amount to.

assetName

Asset name.

filingDate

Filing date.

name

Name of the representative.

ownerType

Owner Type.

position

Position.

symbol

Symbol.

transactionDate

Transaction date.

transactionType

Transaction type Sale or Purchase.

symbol

Symbol of the company.

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

print(finnhub_client.congressional_trading('AAPL', '2020-01-01', '2023-03-31'))

Sample response

{
  "data": [
    {
      "amountFrom": 100001,
      "amountTo": 250000,
      "assetName": "Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)",
      "filingDate": "2015-05-14",
      "name": "Lamar Alexander",
      "ownerType": "Spouse",
      "position": "senator",
      "symbol": "MLPTX",
      "transactionDate": "2014-04-04",
      "transactionType": "Purchase"
    },
    {
      "amountFrom": 1001,
      "amountTo": 15000,
      "assetName": "Oppenheimer SteelPath MLP Select 40 Y (NASDAQ)",
      "filingDate": "2015-05-14",
      "name": "Lamar Alexander",
      "ownerType": "Spouse",
      "position": "senator",
      "symbol": "MLPTX",
      "transactionDate": "2014-02-07",
      "transactionType": "Purchase"
    }
  ],
  "symbol": "MLPTX"
}
