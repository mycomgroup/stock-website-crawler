---
id: "url-7c9ed019"
type: "api"
title: "Historical Market Cap Premium"
url: "https://finnhub.io/docs/api/historical-market-cap"
description: "Get historical market cap data for global companies."
source: ""
tags: []
crawl_time: "2026-03-18T09:27:36.178Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Company symbol."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.historicalMarketCap(\"AAPL\", \"2020-01-01\", \"2020-05-01\", (error, data, response) => {\n\tconsole.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.historical_market_cap('AAPL', _from=\"2020-06-01\", to=\"2020-06-10\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.HistoricalMarketCap(context.Background()).Symbol(\"AAPL\").From(\"2020-05-01\").To(\"2020-05-01\").Execute()"}
    - {"language":"PHP","code":"print_r($client->historicalMarketCap(\"AAPL\", \"2020-06-01\", \"2020-06-10\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.historical_market_cap('AAPL', \"2020-06-01\", \"2020-06-10\"))"}
    - {"language":"Kotlin","code":"println(apiClient.historicalMarketCap(\"AAPL\", from = \"2020-06-01\", to = \"2020-06-10\"))"}
  sampleResponse: "{\n  \"currency\": \"USD\",\n  \"data\": [\n    {\n      \"atDate\": \"2024-06-10\",\n      \"marketCapitalization\": 3759.182\n    },\n    {\n      \"atDate\": \"2024-06-09\",\n      \"marketCapitalization\": 21508.447\n    }\n  ],\n  \"symbol\": \"SYM\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"currency\": \"USD\",\n  \"data\": [\n    {\n      \"atDate\": \"2024-06-10\",\n      \"marketCapitalization\": 3759.182\n    },\n    {\n      \"atDate\": \"2024-06-09\",\n      \"marketCapitalization\": 21508.447\n    }\n  ],\n  \"symbol\": \"SYM\"\n}"
  rawContent: "Historical Market Cap Premium\n\nGet historical market cap data for global companies.\n\nMethod: GET\n\nPremium: Accessible with Fundamental 2 or All in One subscription.\n\nExamples:\n\n/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06\n\nArguments:\n\nsymbolREQUIRED\n\nCompany symbol.\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD.\n\ntoREQUIRED\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ncurrency\n\nCurrency\n\ndata\n\nArray of market data.\n\natDate\n\nDate of the reading\n\nmarketCapitalization\n\nValue\n\nsymbol\n\nSymbol\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.historical_market_cap('AAPL', _from=\"2020-06-01\", to=\"2020-06-10\"))\n\nSample response\n\n{\n  \"currency\": \"USD\",\n  \"data\": [\n    {\n      \"atDate\": \"2024-06-10\",\n      \"marketCapitalization\": 3759.182\n    },\n    {\n      \"atDate\": \"2024-06-09\",\n      \"marketCapitalization\": 21508.447\n    }\n  ],\n  \"symbol\": \"SYM\"\n}"
  suggestedFilename: "historical-market-cap"
---

# Historical Market Cap Premium

## 源URL

https://finnhub.io/docs/api/historical-market-cap

## 描述

Get historical market cap data for global companies.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Company symbol. |
| `from` | string | 是 | - | From date YYYY-MM-DD. |
| `to` | string | 是 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.historicalMarketCap("AAPL", "2020-01-01", "2020-05-01", (error, data, response) => {
	console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.historical_market_cap('AAPL', _from="2020-06-01", to="2020-06-10"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.HistoricalMarketCap(context.Background()).Symbol("AAPL").From("2020-05-01").To("2020-05-01").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->historicalMarketCap("AAPL", "2020-06-01", "2020-06-10"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.historical_market_cap('AAPL', "2020-06-01", "2020-06-10"))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.historicalMarketCap("AAPL", from = "2020-06-01", to = "2020-06-10"))
```

### 示例 7 (json)

```json
{
  "currency": "USD",
  "data": [
    {
      "atDate": "2024-06-10",
      "marketCapitalization": 3759.182
    },
    {
      "atDate": "2024-06-09",
      "marketCapitalization": 21508.447
    }
  ],
  "symbol": "SYM"
}
```

## 文档正文

Get historical market cap data for global companies.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06`

Historical Market Cap Premium

Get historical market cap data for global companies.

Method: GET

Premium: Accessible with Fundamental 2 or All in One subscription.

Examples:

/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06

Arguments:

symbolREQUIRED

Company symbol.

fromREQUIRED

From date YYYY-MM-DD.

toREQUIRED

To date YYYY-MM-DD.

Response Attributes:

currency

Currency

data

Array of market data.

atDate

Date of the reading

marketCapitalization

Value

symbol

Symbol

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

print(finnhub_client.historical_market_cap('AAPL', _from="2020-06-01", to="2020-06-10"))

Sample response

{
  "currency": "USD",
  "data": [
    {
      "atDate": "2024-06-10",
      "marketCapitalization": 3759.182
    },
    {
      "atDate": "2024-06-09",
      "marketCapitalization": 21508.447
    }
  ],
  "symbol": "SYM"
}
