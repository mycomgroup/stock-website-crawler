---
id: "url-27bb5f99"
type: "api"
title: "Stock Symbol"
url: "https://finnhub.io/docs/api/stock-symbols"
description: "List supported stocks. We use the following symbology to identify stocks on Finnhub Exchange_Ticker.Exchange_Code. A list of supported exchange codes can be found here."
source: ""
tags: []
crawl_time: "2026-03-18T04:45:55.964Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/symbol?exchange=US"
  parameters:
    - {"name":"exchange","in":"query","required":true,"type":"string","description":"Exchange you want to get the list of symbols from. List of exchange codes can be found here."}
    - {"name":"mic","in":"query","required":false,"type":"string","description":"Filter by MIC code."}
    - {"name":"securityType","in":"query","required":false,"type":"string","description":"Filter by security type used by OpenFigi standard."}
    - {"name":"currency","in":"query","required":false,"type":"string","description":"Filter by currency."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.stockSymbols(\"US\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_symbols('US'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.StockSymbols(context.Background()).Exchange(\"US\").Execute()"}
    - {"language":"PHP","code":"print_r($client->stockSymbols(\"US\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.stock_symbols('US'))"}
    - {"language":"Kotlin","code":"println(apiClient.stockSymbols(\"US\", \"\", \"\", \"\"))"}
  sampleResponse: "[\n  {\n    \"currency\": \"USD\",\n    \"description\": \"UAN POWER CORP\",\n    \"displaySymbol\": \"UPOW\",\n    \"figi\": \"BBG000BGHYF2\",\n    \"mic\": \"OTCM\",\n    \"symbol\": \"UPOW\",\n    \"type\": \"Common Stock\"\n  },\n  {\n    \"currency\": \"USD\",\n    \"description\": \"APPLE INC\",\n    \"displaySymbol\": \"AAPL\",\n    \"figi\": \"BBG000B9Y5X2\",\n    \"mic\": \"XNGS\",\n    \"symbol\": \"AAPL\",\n    \"type\": \"Common Stock\"\n  },\n  {\n    \"currency\": \"USD\",\n    \"description\": \"EXCO TECHNOLOGIES LTD\",\n    \"displaySymbol\": \"EXCOF\",\n    \"figi\": \"BBG000JHDDS8\",\n    \"mic\": \"OOTC\",\n    \"symbol\": \"EXCOF\",\n    \"type\": \"Common Stock\"\n  }\n]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"currency\": \"USD\",\n    \"description\": \"UAN POWER CORP\",\n    \"displaySymbol\": \"UPOW\",\n    \"figi\": \"BBG000BGHYF2\",\n    \"mic\": \"OTCM\",\n    \"symbol\": \"UPOW\",\n    \"type\": \"Common Stock\"\n  },\n  {\n    \"currency\": \"USD\",\n    \"description\": \"APPLE INC\",\n    \"displaySymbol\": \"AAPL\",\n    \"figi\": \"BBG000B9Y5X2\",\n    \"mic\": \"XNGS\",\n    \"symbol\": \"AAPL\",\n    \"type\": \"Common Stock\"\n  },\n  {\n    \"currency\": \"USD\",\n    \"description\": \"EXCO TECHNOLOGIES LTD\",\n    \"displaySymbol\": \"EXCOF\",\n    \"figi\": \"BBG000JHDDS8\",\n    \"mic\": \"OOTC\",\n    \"symbol\": \"EXCOF\",\n    \"type\": \"Common Stock\"\n  }\n]"
  rawContent: "Stock Symbol\n\nList supported stocks. We use the following symbology to identify stocks on Finnhub Exchange_Ticker.Exchange_Code. A list of supported exchange codes can be found here.\n\nMethod: GET\n\nExamples:\n\n/stock/symbol?exchange=US\n\n/stock/symbol?exchange=US&mic=XNYS\n\nArguments:\n\nexchangeREQUIRED\n\nExchange you want to get the list of symbols from. List of exchange codes can be found here.\n\nmicoptional\n\nFilter by MIC code.\n\nsecurityTypeoptional\n\nFilter by security type used by OpenFigi standard.\n\ncurrencyoptional\n\nFilter by currency.\n\nResponse Attributes:\n\ncurrency\n\nPrice's currency. This might be different from the reporting currency of fundamental data.\n\ndescription\n\nSymbol description\n\ndisplaySymbol\n\nDisplay symbol name.\n\nfigi\n\nFIGI identifier.\n\nisin\n\nISIN. This field is only available for EU stocks and selected Asian markets. Entitlement from Finnhub is required to access this field.\n\nmic\n\nPrimary exchange's MIC.\n\nshareClassFIGI\n\nGlobal Share Class FIGI.\n\nsymbol\n\nUnique symbol used to identify this symbol used in /stock/candle endpoint.\n\nsymbol2\n\nAlternative ticker for exchanges with multiple tickers for 1 stock such as BSE.\n\ntype\n\nSecurity type.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_symbols('US'))\n\nSample response\n\n[\n  {\n    \"currency\": \"USD\",\n    \"description\": \"UAN POWER CORP\",\n    \"displaySymbol\": \"UPOW\",\n    \"figi\": \"BBG000BGHYF2\",\n    \"mic\": \"OTCM\",\n    \"symbol\": \"UPOW\",\n    \"type\": \"Common Stock\"\n  },\n  {\n    \"currency\": \"USD\",\n    \"description\": \"APPLE INC\",\n    \"displaySymbol\": \"AAPL\",\n    \"figi\": \"BBG000B9Y5X2\",\n    \"mic\": \"XNGS\",\n    \"symbol\": \"AAPL\",\n    \"type\": \"Common Stock\"\n  },\n  {\n    \"currency\": \"USD\",\n    \"description\": \"EXCO TECHNOLOGIES LTD\",\n    \"displaySymbol\": \"EXCOF\",\n    \"figi\": \"BBG000JHDDS8\",\n    \"mic\": \"OOTC\",\n    \"symbol\": \"EXCOF\",\n    \"type\": \"Common Stock\"\n  }\n]"
  suggestedFilename: "stock-symbols"
---

# Stock Symbol

## 源URL

https://finnhub.io/docs/api/stock-symbols

## 描述

List supported stocks. We use the following symbology to identify stocks on Finnhub Exchange_Ticker.Exchange_Code. A list of supported exchange codes can be found here.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/symbol?exchange=US`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `exchange` | string | 是 | - | Exchange you want to get the list of symbols from. List of exchange codes can be found here. |
| `mic` | string | 否 | - | Filter by MIC code. |
| `securityType` | string | 否 | - | Filter by security type used by OpenFigi standard. |
| `currency` | string | 否 | - | Filter by currency. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.stockSymbols("US", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_symbols('US'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.StockSymbols(context.Background()).Exchange("US").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->stockSymbols("US"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.stock_symbols('US'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.stockSymbols("US", "", "", ""))
```

### 示例 7 (json)

```json
[
  {
    "currency": "USD",
    "description": "UAN POWER CORP",
    "displaySymbol": "UPOW",
    "figi": "BBG000BGHYF2",
    "mic": "OTCM",
    "symbol": "UPOW",
    "type": "Common Stock"
  },
  {
    "currency": "USD",
    "description": "APPLE INC",
    "displaySymbol": "AAPL",
    "figi": "BBG000B9Y5X2",
    "mic": "XNGS",
    "symbol": "AAPL",
    "type": "Common Stock"
  },
  {
    "currency": "USD",
    "description": "EXCO TECHNOLOGIES LTD",
    "displaySymbol": "EXCOF",
    "figi": "BBG000JHDDS8",
    "mic": "OOTC",
    "symbol": "EXCOF",
    "type": "Common Stock"
  }
]
```

## 文档正文

List supported stocks. We use the following symbology to identify stocks on Finnhub Exchange_Ticker.Exchange_Code. A list of supported exchange codes can be found here.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/symbol?exchange=US`

Stock Symbol

List supported stocks. We use the following symbology to identify stocks on Finnhub Exchange_Ticker.Exchange_Code. A list of supported exchange codes can be found here.

Method: GET

Examples:

/stock/symbol?exchange=US

/stock/symbol?exchange=US&mic=XNYS

Arguments:

exchangeREQUIRED

Exchange you want to get the list of symbols from. List of exchange codes can be found here.

micoptional

Filter by MIC code.

securityTypeoptional

Filter by security type used by OpenFigi standard.

currencyoptional

Filter by currency.

Response Attributes:

currency

Price's currency. This might be different from the reporting currency of fundamental data.

description

Symbol description

displaySymbol

Display symbol name.

figi

FIGI identifier.

isin

ISIN. This field is only available for EU stocks and selected Asian markets. Entitlement from Finnhub is required to access this field.

mic

Primary exchange's MIC.

shareClassFIGI

Global Share Class FIGI.

symbol

Unique symbol used to identify this symbol used in /stock/candle endpoint.

symbol2

Alternative ticker for exchanges with multiple tickers for 1 stock such as BSE.

type

Security type.

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

print(finnhub_client.stock_symbols('US'))

Sample response

[
  {
    "currency": "USD",
    "description": "UAN POWER CORP",
    "displaySymbol": "UPOW",
    "figi": "BBG000BGHYF2",
    "mic": "OTCM",
    "symbol": "UPOW",
    "type": "Common Stock"
  },
  {
    "currency": "USD",
    "description": "APPLE INC",
    "displaySymbol": "AAPL",
    "figi": "BBG000B9Y5X2",
    "mic": "XNGS",
    "symbol": "AAPL",
    "type": "Common Stock"
  },
  {
    "currency": "USD",
    "description": "EXCO TECHNOLOGIES LTD",
    "displaySymbol": "EXCOF",
    "figi": "BBG000JHDDS8",
    "mic": "OOTC",
    "symbol": "EXCOF",
    "type": "Common Stock"
  }
]
