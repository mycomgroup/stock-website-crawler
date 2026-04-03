---
id: "url-4ea1fb64"
type: "api"
title: "Ownership Premium"
url: "https://finnhub.io/docs/api/ownership"
description: "Get a full list of shareholders of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets."
source: ""
tags: []
crawl_time: "2026-03-18T03:13:14.320Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/ownership?symbol=AAPL&limit=20"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL."}
    - {"name":"limit","in":"query","required":false,"type":"integer","description":"Limit number of results. Leave empty to get the full list."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"let optsLimit = {'limit': 10};\nfinnhubClient.ownership(\"AAPL\", optsLimit, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.ownership('AAPL', limit=5))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.Ownership(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->ownership(\"AAPL\", 5));"}
    - {"language":"Ruby","code":"puts(finnhub_client.ownership('AAPL', {limit: 5}))"}
    - {"language":"Kotlin","code":"println(apiClient.ownership(\"AAPL\", limit = 5))"}
  sampleResponse: "{\n  \"ownership\": [\n    {\n      \"name\": \"The Vanguard Group, Inc.\",\n      \"share\": 329323420,\n      \"change\": -1809077,\n      \"filingDate\": \"2019-12-31\"\n    },\n    {\n      \"name\": \"BRK.A | Berkshire Hathaway Inc.\",\n      \"share\": 245155570,\n      \"change\": -3683113,\n      \"filingDate\": \"2019-12-31\"\n    },\n    {\n      \"name\": \"BlackRock Institutional Trust Co NA\",\n      \"share\": 187354850,\n      \"change\": -2500563,\n      \"filingDate\": \"2020-03-31\"\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"ownership\": [\n    {\n      \"name\": \"The Vanguard Group, Inc.\",\n      \"share\": 329323420,\n      \"change\": -1809077,\n      \"filingDate\": \"2019-12-31\"\n    },\n    {\n      \"name\": \"BRK.A | Berkshire Hathaway Inc.\",\n      \"share\": 245155570,\n      \"change\": -3683113,\n      \"filingDate\": \"2019-12-31\"\n    },\n    {\n      \"name\": \"BlackRock Institutional Trust Co NA\",\n      \"share\": 187354850,\n      \"change\": -2500563,\n      \"filingDate\": \"2020-03-31\"\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  rawContent: "Ownership Premium\n\nGet a full list of shareholders of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/ownership?symbol=AAPL&limit=20\n\n/stock/ownership?symbol=IBM\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nlimitoptional\n\nLimit number of results. Leave empty to get the full list.\n\nResponse Attributes:\n\nownership\n\nArray of investors with detailed information about their holdings.\n\nchange\n\nNumber of share changed (net buy or sell) from the last period.\n\nfilingDate\n\nFiling date.\n\nname\n\nInvestor's name.\n\nshare\n\nNumber of shares held by the investor.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.ownership('AAPL', limit=5))\n\nSample response\n\n{\n  \"ownership\": [\n    {\n      \"name\": \"The Vanguard Group, Inc.\",\n      \"share\": 329323420,\n      \"change\": -1809077,\n      \"filingDate\": \"2019-12-31\"\n    },\n    {\n      \"name\": \"BRK.A | Berkshire Hathaway Inc.\",\n      \"share\": 245155570,\n      \"change\": -3683113,\n      \"filingDate\": \"2019-12-31\"\n    },\n    {\n      \"name\": \"BlackRock Institutional Trust Co NA\",\n      \"share\": 187354850,\n      \"change\": -2500563,\n      \"filingDate\": \"2020-03-31\"\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "ownership"
---

# Ownership Premium

## 源URL

https://finnhub.io/docs/api/ownership

## 描述

Get a full list of shareholders of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/ownership?symbol=AAPL&limit=20`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol of the company: AAPL. |
| `limit` | integer | 否 | - | Limit number of results. Leave empty to get the full list. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
let optsLimit = {'limit': 10};
finnhubClient.ownership("AAPL", optsLimit, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.ownership('AAPL', limit=5))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.Ownership(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->ownership("AAPL", 5));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.ownership('AAPL', {limit: 5}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.ownership("AAPL", limit = 5))
```

### 示例 7 (json)

```json
{
  "ownership": [
    {
      "name": "The Vanguard Group, Inc.",
      "share": 329323420,
      "change": -1809077,
      "filingDate": "2019-12-31"
    },
    {
      "name": "BRK.A | Berkshire Hathaway Inc.",
      "share": 245155570,
      "change": -3683113,
      "filingDate": "2019-12-31"
    },
    {
      "name": "BlackRock Institutional Trust Co NA",
      "share": 187354850,
      "change": -2500563,
      "filingDate": "2020-03-31"
    }
  ],
  "symbol": "AAPL"
}
```

## 文档正文

Get a full list of shareholders of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/ownership?symbol=AAPL&limit=20`

Ownership Premium

Get a full list of shareholders of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets.

Method: GET

Premium: Premium Access Required

Examples:

/stock/ownership?symbol=AAPL&limit=20

/stock/ownership?symbol=IBM

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

limitoptional

Limit number of results. Leave empty to get the full list.

Response Attributes:

ownership

Array of investors with detailed information about their holdings.

change

Number of share changed (net buy or sell) from the last period.

filingDate

Filing date.

name

Investor's name.

share

Number of shares held by the investor.

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

print(finnhub_client.ownership('AAPL', limit=5))

Sample response

{
  "ownership": [
    {
      "name": "The Vanguard Group, Inc.",
      "share": 329323420,
      "change": -1809077,
      "filingDate": "2019-12-31"
    },
    {
      "name": "BRK.A | Berkshire Hathaway Inc.",
      "share": 245155570,
      "change": -3683113,
      "filingDate": "2019-12-31"
    },
    {
      "name": "BlackRock Institutional Trust Co NA",
      "share": 187354850,
      "change": -2500563,
      "filingDate": "2020-03-31"
    }
  ],
  "symbol": "AAPL"
}
