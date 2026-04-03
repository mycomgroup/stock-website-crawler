---
id: "url-fbf4951"
type: "api"
title: "Pattern Recognition Premium"
url: "https://finnhub.io/docs/api/pattern-recognition"
description: "Run pattern recognition algorithm on a symbol. Support double top/bottom, triple top/bottom, head and shoulders, triangle, wedge, channel, flag, and candlestick patterns."
source: ""
tags: []
crawl_time: "2026-03-18T08:35:53.645Z"
metadata:
  requestMethod: "GET"
  endpoint: "/scan/pattern?symbol=AAPL&resolution=D"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol"}
    - {"name":"resolution","in":"query","required":true,"type":"string","description":"Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.patternRecognition(\"AAPL\", \"D\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.pattern_recognition('AAPL', 'D'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.PatternRecognition(context.Background()).Symbol(\"AAPL\").Resolution(\"D\").Execute()"}
    - {"language":"PHP","code":"print_r($client->patternRecognition(\"AAPL\", \"D\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.pattern_recognition('AAPL', 'D'))"}
    - {"language":"Kotlin","code":"println(apiClient.patternRecognition(\"AAPL\", \"D\"))"}
  sampleResponse: "\"points\": [\n    {\n      \"aprice\": 1.09236,\n      \"atime\": 1567458000,\n      \"bprice\": 1.1109,\n      \"btime\": 1568322000,\n      \"cprice\": 1.09897,\n      \"ctime\": 1568667600,\n      \"dprice\": 0,\n      \"dtime\": 0,\n      \"end_price\": 1.1109,\n      \"end_time\": 1568926800,\n      \"entry\": 1.1109,\n      \"eprice\": 0,\n      \"etime\": 0,\n      \"mature\": 0,\n      \"patternname\": \"Double Bottom\",\n      \"patterntype\": \"bullish\",\n      \"profit1\": 1.1294,\n      \"profit2\": 0,\n      \"sortTime\": 1568926800,\n      \"start_price\": 1.1109,\n      \"start_time\": 1566853200,\n      \"status\": \"incomplete\",\n      \"stoploss\": 1.0905,\n      \"symbol\": \"EUR_USD\",\n      \"terminal\": 0\n    },\n    {\n      \"aprice\": 1.09236,\n      \"atime\": 1567458000,\n      \"bprice\": 1.1109,\n      \"btime\": 1568322000,\n      \"cprice\": 1.09897,\n      \"ctime\": 1568667600,\n      \"dprice\": 1.13394884,\n      \"dtime\": 1568926800,\n      \"entry\": 1.1339,\n      \"mature\": 0,\n      \"patternname\": \"Bat\",\n      \"patterntype\": \"bearish\",\n      \"profit1\": 1.1181,\n      \"profit2\": 1.1082,\n      \"przmax\": 1.1339,\n      \"przmin\": 1.129,\n      \"rrratio\": 3.34,\n      \"sortTime\": 1568667600,\n      \"status\": \"incomplete\",\n      \"stoploss\": 1.1416,\n      \"symbol\": \"EUR_USD\",\n      \"terminal\": 0,\n      \"xprice\": 1.1393,\n      \"xtime\": 1561669200\n    }\n]"
  curlExample: ""
  jsonExample: "\"points\": [\n    {\n      \"aprice\": 1.09236,\n      \"atime\": 1567458000,\n      \"bprice\": 1.1109,\n      \"btime\": 1568322000,\n      \"cprice\": 1.09897,\n      \"ctime\": 1568667600,\n      \"dprice\": 0,\n      \"dtime\": 0,\n      \"end_price\": 1.1109,\n      \"end_time\": 1568926800,\n      \"entry\": 1.1109,\n      \"eprice\": 0,\n      \"etime\": 0,\n      \"mature\": 0,\n      \"patternname\": \"Double Bottom\",\n      \"patterntype\": \"bullish\",\n      \"profit1\": 1.1294,\n      \"profit2\": 0,\n      \"sortTime\": 1568926800,\n      \"start_price\": 1.1109,\n      \"start_time\": 1566853200,\n      \"status\": \"incomplete\",\n      \"stoploss\": 1.0905,\n      \"symbol\": \"EUR_USD\",\n      \"terminal\": 0\n    },\n    {\n      \"aprice\": 1.09236,\n      \"atime\": 1567458000,\n      \"bprice\": 1.1109,\n      \"btime\": 1568322000,\n      \"cprice\": 1.09897,\n      \"ctime\": 1568667600,\n      \"dprice\": 1.13394884,\n      \"dtime\": 1568926800,\n      \"entry\": 1.1339,\n      \"mature\": 0,\n      \"patternname\": \"Bat\",\n      \"patterntype\": \"bearish\",\n      \"profit1\": 1.1181,\n      \"profit2\": 1.1082,\n      \"przmax\": 1.1339,\n      \"przmin\": 1.129,\n      \"rrratio\": 3.34,\n      \"sortTime\": 1568667600,\n      \"status\": \"incomplete\",\n      \"stoploss\": 1.1416,\n      \"symbol\": \"EUR_USD\",\n      \"terminal\": 0,\n      \"xprice\": 1.1393,\n      \"xtime\": 1561669200\n    }\n]"
  rawContent: "Pattern Recognition Premium\n\nRun pattern recognition algorithm on a symbol. Support double top/bottom, triple top/bottom, head and shoulders, triangle, wedge, channel, flag, and candlestick patterns.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/scan/pattern?symbol=AAPL&resolution=D\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol\n\nresolutionREQUIRED\n\nSupported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.\n\nResponse Attributes:\n\npoints\n\nArray of patterns.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.pattern_recognition('AAPL', 'D'))\n\nSample response\n\n\"points\": [\n    {\n      \"aprice\": 1.09236,\n      \"atime\": 1567458000,\n      \"bprice\": 1.1109,\n      \"btime\": 1568322000,\n      \"cprice\": 1.09897,\n      \"ctime\": 1568667600,\n      \"dprice\": 0,\n      \"dtime\": 0,\n      \"end_price\": 1.1109,\n      \"end_time\": 1568926800,\n      \"entry\": 1.1109,\n      \"eprice\": 0,\n      \"etime\": 0,\n      \"mature\": 0,\n      \"patternname\": \"Double Bottom\",\n      \"patterntype\": \"bullish\",\n      \"profit1\": 1.1294,\n      \"profit2\": 0,\n      \"sortTime\": 1568926800,\n      \"start_price\": 1.1109,\n      \"start_time\": 1566853200,\n      \"status\": \"incomplete\",\n      \"stoploss\": 1.0905,\n      \"symbol\": \"EUR_USD\",\n      \"terminal\": 0\n    },\n    {\n      \"aprice\": 1.09236,\n      \"atime\": 1567458000,\n      \"bprice\": 1.1109,\n      \"btime\": 1568322000,\n      \"cprice\": 1.09897,\n      \"ctime\": 1568667600,\n      \"dprice\": 1.13394884,\n      \"dtime\": 1568926800,\n      \"entry\": 1.1339,\n      \"mature\": 0,\n      \"patternname\": \"Bat\",\n      \"patterntype\": \"bearish\",\n      \"profit1\": 1.1181,\n      \"profit2\": 1.1082,\n      \"przmax\": 1.1339,\n      \"przmin\": 1.129,\n      \"rrratio\": 3.34,\n      \"sortTime\": 1568667600,\n      \"status\": \"incomplete\",\n      \"stoploss\": 1.1416,\n      \"symbol\": \"EUR_USD\",\n      \"terminal\": 0,\n      \"xprice\": 1.1393,\n      \"xtime\": 1561669200\n    }\n]"
  suggestedFilename: "pattern-recognition"
---

# Pattern Recognition Premium

## 源URL

https://finnhub.io/docs/api/pattern-recognition

## 描述

Run pattern recognition algorithm on a symbol. Support double top/bottom, triple top/bottom, head and shoulders, triangle, wedge, channel, flag, and candlestick patterns.

## API 端点

**Method**: `GET`
**Endpoint**: `/scan/pattern?symbol=AAPL&resolution=D`

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
finnhubClient.patternRecognition("AAPL", "D", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.pattern_recognition('AAPL', 'D'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.PatternRecognition(context.Background()).Symbol("AAPL").Resolution("D").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->patternRecognition("AAPL", "D"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.pattern_recognition('AAPL', 'D'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.patternRecognition("AAPL", "D"))
```

### 示例 7 (json)

```json
"points": [
    {
      "aprice": 1.09236,
      "atime": 1567458000,
      "bprice": 1.1109,
      "btime": 1568322000,
      "cprice": 1.09897,
      "ctime": 1568667600,
      "dprice": 0,
      "dtime": 0,
      "end_price": 1.1109,
      "end_time": 1568926800,
      "entry": 1.1109,
      "eprice": 0,
      "etime": 0,
      "mature": 0,
      "patternname": "Double Bottom",
      "patterntype": "bullish",
      "profit1": 1.1294,
      "profit2": 0,
      "sortTime": 1568926800,
      "start_price": 1.1109,
      "start_time": 1566853200,
      "status": "incomplete",
      "stoploss": 1.0905,
      "symbol": "EUR_USD",
      "terminal": 0
    },
    {
      "aprice": 1.09236,
      "atime": 1567458000,
      "bprice": 1.1109,
      "btime": 1568322000,
      "cprice": 1.09897,
      "ctime": 1568667600,
      "dprice": 1.13394884,
      "dtime": 1568926800,
      "entry": 1.1339,
      "mature": 0,
      "patternname": "Bat",
      "patterntype": "bearish",
      "profit1": 1.1181,
      "profit2": 1.1082,
      "przmax": 1.1339,
      "przmin": 1.129,
      "rrratio": 3.34,
      "sortTime": 1568667600,
      "status": "incomplete",
      "stoploss": 1.1416,
      "symbol": "EUR_USD",
      "terminal": 0,
      "xprice": 1.1393,
      "xtime": 1561669200
    }
]
```

## 文档正文

Run pattern recognition algorithm on a symbol. Support double top/bottom, triple top/bottom, head and shoulders, triangle, wedge, channel, flag, and candlestick patterns.

## API 端点

**Method:** `GET`
**Endpoint:** `/scan/pattern?symbol=AAPL&resolution=D`

Pattern Recognition Premium

Run pattern recognition algorithm on a symbol. Support double top/bottom, triple top/bottom, head and shoulders, triangle, wedge, channel, flag, and candlestick patterns.

Method: GET

Premium: Premium Access Required

Examples:

/scan/pattern?symbol=AAPL&resolution=D

Arguments:

symbolREQUIRED

Symbol

resolutionREQUIRED

Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.

Response Attributes:

points

Array of patterns.

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

print(finnhub_client.pattern_recognition('AAPL', 'D'))

Sample response

"points": [
    {
      "aprice": 1.09236,
      "atime": 1567458000,
      "bprice": 1.1109,
      "btime": 1568322000,
      "cprice": 1.09897,
      "ctime": 1568667600,
      "dprice": 0,
      "dtime": 0,
      "end_price": 1.1109,
      "end_time": 1568926800,
      "entry": 1.1109,
      "eprice": 0,
      "etime": 0,
      "mature": 0,
      "patternname": "Double Bottom",
      "patterntype": "bullish",
      "profit1": 1.1294,
      "profit2": 0,
      "sortTime": 1568926800,
      "start_price": 1.1109,
      "start_time": 1566853200,
      "status": "incomplete",
      "stoploss": 1.0905,
      "symbol": "EUR_USD",
      "terminal": 0
    },
    {
      "aprice": 1.09236,
      "atime": 1567458000,
      "bprice": 1.1109,
      "btime": 1568322000,
      "cprice": 1.09897,
      "ctime": 1568667600,
      "dprice": 1.13394884,
      "dtime": 1568926800,
      "entry": 1.1339,
      "mature": 0,
      "patternname": "Bat",
      "patterntype": "bearish",
      "profit1": 1.1181,
      "profit2": 1.1082,
      "przmax": 1.1339,
      "przmin": 1.129,
      "rrratio": 3.34,
      "sortTime": 1568667600,
      "status": "incomplete",
      "stoploss": 1.1416,
      "symbol": "EUR_USD",
      "terminal": 0,
      "xprice": 1.1393,
      "xtime": 1561669200
    }
]
