---
id: "url-2c1f313a"
type: "api"
title: "Ownership Premium"
url: "https://finnhub.io/docs/api/institutional-ownership"
description: "Get a list institutional investors' positions for a particular stock overtime. Data from 13-F filings. Limit to 1 year of data at a time."
source: ""
tags: []
crawl_time: "2026-03-18T09:53:39.825Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/ownership?symbol=AAPL&limit=20"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Filter by symbol."}
    - {"name":"cusip","in":"query","required":true,"type":"string","description":"Filter by CUSIP."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.institutionalOwnership(\"TSLA\", \"\", \"2022-10-01\",\"2022-10-11\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.institutional_ownership(symbol=\"TSLA\", cusip=\"\", _from=\"2022-10-01\", to=\"2022-10-11\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.InstitutionalOwnership(context.Background()).Symbol(\"TSLA\").From(\"2022-10-01\").To(\"2022-10-11\").Execute()"}
    - {"language":"PHP","code":"print_r($client->institutionalOwnership(\"TSLA\", \"\",\"2022-01-01\", \"2022-06-11\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.institutional_ownership(\"TSLA\", \"\", \"2022-10-01\",\"2022-10-11\"))"}
    - {"language":"Kotlin","code":"println( apiClient.institutionalOwnership(\"TSLA\", \"\", from = \"2022-10-01\", to = \"2022-10-11\"))"}
  sampleResponse: "{\n  \"cusip\": \"023135106\",\n  \"data\": [\n    {\n      \"ownership\": [\n        {\n          \"change\": null,\n          \"cik\": \"1000097\",\n          \"name\": \"KINGDON CAPITAL MANAGEMENT, L.L.C.\",\n          \"noVoting\": 0,\n          \"percentage\": 6.23893,\n          \"putCall\": \"\",\n          \"share\": 11250,\n          \"sharedVoting\": 0,\n          \"soleVoting\": 11250,\n          \"value\": 36674000\n        }\n      ],\n      \"reportDate\": \"2022-03-31\"\n    }\n  ],\n  \"symbol\": \"AMZN\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"cusip\": \"023135106\",\n  \"data\": [\n    {\n      \"ownership\": [\n        {\n          \"change\": null,\n          \"cik\": \"1000097\",\n          \"name\": \"KINGDON CAPITAL MANAGEMENT, L.L.C.\",\n          \"noVoting\": 0,\n          \"percentage\": 6.23893,\n          \"putCall\": \"\",\n          \"share\": 11250,\n          \"sharedVoting\": 0,\n          \"soleVoting\": 11250,\n          \"value\": 36674000\n        }\n      ],\n      \"reportDate\": \"2022-03-31\"\n    }\n  ],\n  \"symbol\": \"AMZN\"\n}"
  rawContent: "Ownership Premium\n\nGet a full list of shareholders of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/ownership?symbol=AAPL&limit=20\n\n/stock/ownership?symbol=IBM\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nlimitoptional\n\nLimit number of results. Leave empty to get the full list.\n\nResponse Attributes:\n\nownership\n\nArray of investors with detailed information about their holdings.\n\nchange\n\nNumber of share changed (net buy or sell) from the last period.\n\nfilingDate\n\nFiling date.\n\nname\n\nInvestor's name.\n\nshare\n\nNumber of shares held by the investor.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.ownership('AAPL', limit=5))\n\nSample response\n\n{\n  \"ownership\": [\n    {\n      \"name\": \"The Vanguard Group, Inc.\",\n      \"share\": 329323420,\n      \"change\": -1809077,\n      \"filingDate\": \"2019-12-31\"\n    },\n    {\n      \"name\": \"BRK.A | Berkshire Hathaway Inc.\",\n      \"share\": 245155570,\n      \"change\": -3683113,\n      \"filingDate\": \"2019-12-31\"\n    },\n    {\n      \"name\": \"BlackRock Institutional Trust Co NA\",\n      \"share\": 187354850,\n      \"change\": -2500563,\n      \"filingDate\": \"2020-03-31\"\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "institutional-ownership"
---

# Ownership Premium

## 源URL

https://finnhub.io/docs/api/institutional-ownership

## 描述

Get a list institutional investors' positions for a particular stock overtime. Data from 13-F filings. Limit to 1 year of data at a time.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/ownership?symbol=AAPL&limit=20`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Filter by symbol. |
| `cusip` | string | 是 | - | Filter by CUSIP. |
| `from` | string | 是 | - | From date YYYY-MM-DD. |
| `to` | string | 是 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.institutionalOwnership("TSLA", "", "2022-10-01","2022-10-11", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.institutional_ownership(symbol="TSLA", cusip="", _from="2022-10-01", to="2022-10-11"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.InstitutionalOwnership(context.Background()).Symbol("TSLA").From("2022-10-01").To("2022-10-11").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->institutionalOwnership("TSLA", "","2022-01-01", "2022-06-11"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.institutional_ownership("TSLA", "", "2022-10-01","2022-10-11"))
```

### 示例 6 (Kotlin)

```Kotlin
println( apiClient.institutionalOwnership("TSLA", "", from = "2022-10-01", to = "2022-10-11"))
```

### 示例 7 (json)

```json
{
  "cusip": "023135106",
  "data": [
    {
      "ownership": [
        {
          "change": null,
          "cik": "1000097",
          "name": "KINGDON CAPITAL MANAGEMENT, L.L.C.",
          "noVoting": 0,
          "percentage": 6.23893,
          "putCall": "",
          "share": 11250,
          "sharedVoting": 0,
          "soleVoting": 11250,
          "value": 36674000
        }
      ],
      "reportDate": "2022-03-31"
    }
  ],
  "symbol": "AMZN"
}
```

## 文档正文

Get a list institutional investors' positions for a particular stock overtime. Data from 13-F filings. Limit to 1 year of data at a time.

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
