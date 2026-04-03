---
id: "url-347d6818"
type: "api"
title: "Market Status"
url: "https://finnhub.io/docs/api/market-status"
description: "Get current market status for global exchanges (whether exchanges are open or close)."
source: ""
tags: []
crawl_time: "2026-03-18T04:46:06.913Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/market-status?exchange=US"
  parameters:
    - {"name":"exchange","in":"query","required":true,"type":"string","description":"Exchange code."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.marketStatus({'exchange': 'US'}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.market_status(exchange='US'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.MarketStatus(context.Background()).Exchange(\"US\").Execute()"}
    - {"language":"PHP","code":"print_r($client->marketStatus(\"US\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.market_status({exchange: 'US'}))"}
    - {"language":"Kotlin","code":"println(apiClient.marketStatus(exchange = \"US\"))"}
  sampleResponse: "{\n  \"exchange\": \"US\",\n  \"holiday\": null,\n  \"isOpen\": false,\n  \"session\": \"pre-market\",\n  \"timezone\": \"America/New_York\",\n  \"t\": 1697018041\n}"
  curlExample: ""
  jsonExample: "{\n  \"exchange\": \"US\",\n  \"holiday\": null,\n  \"isOpen\": false,\n  \"session\": \"pre-market\",\n  \"timezone\": \"America/New_York\",\n  \"t\": 1697018041\n}"
  rawContent: "Market Status\n\nGet current market status for global exchanges (whether exchanges are open or close).\n\nMethod: GET\n\nExamples:\n\n/stock/market-status?exchange=US\n\n/stock/market-status?exchange=L\n\nArguments:\n\nexchangeREQUIRED\n\nExchange code.\n\nResponse Attributes:\n\nexchange\n\nExchange.\n\nholiday\n\nHoliday event.\n\nisOpen\n\nWhether the market is open at the moment.\n\nsession\n\nMarket session. Can be 1 of the following values: pre-market,regular,post-market or null if the market is closed.\n\nt\n\nCurrent timestamp.\n\ntimezone\n\nTimezone.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.market_status(exchange='US'))\n\nSample response\n\n{\n  \"exchange\": \"US\",\n  \"holiday\": null,\n  \"isOpen\": false,\n  \"session\": \"pre-market\",\n  \"timezone\": \"America/New_York\",\n  \"t\": 1697018041\n}"
  suggestedFilename: "market-status"
---

# Market Status

## 源URL

https://finnhub.io/docs/api/market-status

## 描述

Get current market status for global exchanges (whether exchanges are open or close).

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/market-status?exchange=US`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `exchange` | string | 是 | - | Exchange code. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.marketStatus({'exchange': 'US'}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.market_status(exchange='US'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.MarketStatus(context.Background()).Exchange("US").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->marketStatus("US"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.market_status({exchange: 'US'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.marketStatus(exchange = "US"))
```

### 示例 7 (json)

```json
{
  "exchange": "US",
  "holiday": null,
  "isOpen": false,
  "session": "pre-market",
  "timezone": "America/New_York",
  "t": 1697018041
}
```

## 文档正文

Get current market status for global exchanges (whether exchanges are open or close).

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/market-status?exchange=US`

Market Status

Get current market status for global exchanges (whether exchanges are open or close).

Method: GET

Examples:

/stock/market-status?exchange=US

/stock/market-status?exchange=L

Arguments:

exchangeREQUIRED

Exchange code.

Response Attributes:

exchange

Exchange.

holiday

Holiday event.

isOpen

Whether the market is open at the moment.

session

Market session. Can be 1 of the following values: pre-market,regular,post-market or null if the market is closed.

t

Current timestamp.

timezone

Timezone.

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

print(finnhub_client.market_status(exchange='US'))

Sample response

{
  "exchange": "US",
  "holiday": null,
  "isOpen": false,
  "session": "pre-market",
  "timezone": "America/New_York",
  "t": 1697018041
}
