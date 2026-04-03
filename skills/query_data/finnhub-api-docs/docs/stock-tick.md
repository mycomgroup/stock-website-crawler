---
id: "url-77bc4761"
type: "api"
title: "Tick Data Premium"
url: "https://finnhub.io/docs/api/stock-tick"
description: "Get historical tick data for global exchanges.For more historical tick data, you can visit our bulk download page in the Dashboard here to speed up the download process.\n  \n    \n      Exchange\n      Segment\n      Delay\n    \n  \n  \n    \n      US CTA/UTP\n      Full SIP\n      End-of-day\n    \n    \n      TSX\n      TSXTSX VentureIndex\n      End-of-day\n    \n    \n      LSE\n      London Stock Exchange (L)LSE International (L)LSE European (L)\n      15 minute\n    \n    \n      Euronext\n       Euronext Paris (PA) Euronext Amsterdam (AS) Euronext Lisbon (LS) Euronext Brussels (BR) Euronext Oslo (OL) Euronext London (LN) Euronext Dublin (IR) Index Warrant\n      End-of-day\n    \n    \n      Deutsche Börse\n       Frankfurt (F) Xetra (DE) Duesseldorf (DU) Hamburg (HM) Berlin (BE) Hanover (HA) Stoxx (SX) TradeGate (TG) Zertifikate (SC) Index Warrant\n      End-of-day"
source: ""
tags: []
crawl_time: "2026-03-18T03:15:12.698Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/tick?symbol=AAPL&date=2021-03-09&limit=500&skip=0&format=json"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol."}
    - {"name":"date","in":"query","required":true,"type":"string","description":"Date: 2020-04-02."}
    - {"name":"limit","in":"query","required":true,"type":"integer","description":"Limit number of ticks returned. Maximum value: 25000"}
    - {"name":"skip","in":"query","required":true,"type":"integer","description":"Number of ticks to skip. Use this parameter to loop through the entire data."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.stockTick(\"AAPL\", \"2020-03-25\", 500, 0, (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_tick('AAPL', '2020-03-25', 500, 0))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.StockTick(context.Background()).Symbol(\"AAPL\").Date(\"2021-07-23\").Limit(50).Skip(0).Execute()"}
    - {"language":"PHP","code":"print_r($client->stockTick(\"AAPL\", \"2020-03-25\", 500, 0));"}
    - {"language":"Ruby","code":"puts(finnhub_client.stock_tick('AAPL', '2020-03-25', 500, 0))"}
    - {"language":"Kotlin","code":"println(apiClient.stockTick(\"AAPL\", \"2020-03-25\", 500, 0))"}
  sampleResponse: "{\n  \"p\": [\n    255,\n    255,\n    255\n  ],\n  \"s\": \"AAPL\",\n  \"skip\": 0,\n  \"t\": [\n    1585108800073,\n    1585108800315,\n    1585108800381\n  ],\n  \"v\": [\n    2513,\n    24,\n    1\n  ],\n  \"x\": [\n    \"P\",\n    \"P\",\n    \"P\"\n  ],\n  \"count\": 3,\n  \"c\":[[\"1\",\"24\"],[\"1\",\"24\",\"12\"],[\"1\",\"24\",\"12\"]]\n}"
  curlExample: ""
  jsonExample: "{\n  \"p\": [\n    255,\n    255,\n    255\n  ],\n  \"s\": \"AAPL\",\n  \"skip\": 0,\n  \"t\": [\n    1585108800073,\n    1585108800315,\n    1585108800381\n  ],\n  \"v\": [\n    2513,\n    24,\n    1\n  ],\n  \"x\": [\n    \"P\",\n    \"P\",\n    \"P\"\n  ],\n  \"count\": 3,\n  \"c\":[[\"1\",\"24\"],[\"1\",\"24\",\"12\"],[\"1\",\"24\",\"12\"]]\n}"
  rawContent: "Tick Data Premium\n\nGet historical tick data for global exchanges.\n\nFor more historical tick data, you can visit our bulk download page in the Dashboard here to speed up the download process.\n\nExchange\tSegment\tDelay\nUS CTA/UTP\tFull SIP\tEnd-of-day\nTSX\t\nTSX\nTSX Venture\nIndex\n\tEnd-of-day\nLSE\t\nLondon Stock Exchange (L)\nLSE International (L)\nLSE European (L)\n\t15 minute\nEuronext\t\nEuronext Paris (PA)\nEuronext Amsterdam (AS)\nEuronext Lisbon (LS)\nEuronext Brussels (BR)\nEuronext Oslo (OL)\nEuronext London (LN)\nEuronext Dublin (IR)\nIndex\nWarrant\n\tEnd-of-day\nDeutsche Börse\t\nFrankfurt (F)\nXetra (DE)\nDuesseldorf (DU)\nHamburg (HM)\nBerlin (BE)\nHanover (HA)\nStoxx (SX)\nTradeGate (TG)\nZertifikate (SC)\nIndex\nWarrant\n\tEnd-of-day\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/tick?symbol=AAPL&date=2021-03-09&limit=500&skip=0&format=json\n\n/stock/tick?symbol=AC.TO&date=2021-03-09&limit=500&skip=0&format=json\n\n/stock/tick?symbol=BARC.L&date=2021-03-09&limit=500&skip=0&format=json\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\ndateREQUIRED\n\nDate: 2020-04-02.\n\nlimitREQUIRED\n\nLimit number of ticks returned. Maximum value: 25000\n\nskipREQUIRED\n\nNumber of ticks to skip. Use this parameter to loop through the entire data.\n\nResponse Attributes:\n\nc\n\nList of trade conditions. A comprehensive list of trade conditions code can be found here\n\ncount\n\nNumber of ticks returned. If count < limit, all data for that date has been returned.\n\np\n\nList of price data.\n\ns\n\nSymbol.\n\nskip\n\nNumber of ticks skipped.\n\nt\n\nList of timestamp in UNIX ms.\n\ntotal\n\nTotal number of ticks for that date.\n\nv\n\nList of volume data.\n\nx\n\nList of venues/exchanges. A list of exchange codes can be found here\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_tick('AAPL', '2020-03-25', 500, 0))\n\nSample response\n\n{\n  \"p\": [\n    255,\n    255,\n  ],\n  \"s\": \"AAPL\",\n  \"skip\": 0,\n  \"t\": [\n    1585108800073,\n    1585108800315,\n  ],\n  \"v\": [\n    2513,\n    24,\n  ],\n  \"x\": [\n    \"P\",\n    \"P\",\n    \"P\"\n  ],\n  \"count\": 3,\n  \"c\":[[\"1\",\"24\"],[\"1\",\"24\",\"12\"],[\"1\",\"24\",\"12\"]]\n}"
  suggestedFilename: "stock-tick"
---

# Tick Data Premium

## 源URL

https://finnhub.io/docs/api/stock-tick

## 描述

Get historical tick data for global exchanges.For more historical tick data, you can visit our bulk download page in the Dashboard here to speed up the download process.
  
    
      Exchange
      Segment
      Delay
    
  
  
    
      US CTA/UTP
      Full SIP
      End-of-day
    
    
      TSX
      TSXTSX VentureIndex
      End-of-day
    
    
      LSE
      London Stock Exchange (L)LSE International (L)LSE European (L)
      15 minute
    
    
      Euronext
       Euronext Paris (PA) Euronext Amsterdam (AS) Euronext Lisbon (LS) Euronext Brussels (BR) Euronext Oslo (OL) Euronext London (LN) Euronext Dublin (IR) Index Warrant
      End-of-day
    
    
      Deutsche Börse
       Frankfurt (F) Xetra (DE) Duesseldorf (DU) Hamburg (HM) Berlin (BE) Hanover (HA) Stoxx (SX) TradeGate (TG) Zertifikate (SC) Index Warrant
      End-of-day

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/tick?symbol=AAPL&date=2021-03-09&limit=500&skip=0&format=json`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol. |
| `date` | string | 是 | - | Date: 2020-04-02. |
| `limit` | integer | 是 | - | Limit number of ticks returned. Maximum value: 25000 |
| `skip` | integer | 是 | - | Number of ticks to skip. Use this parameter to loop through the entire data. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.stockTick("AAPL", "2020-03-25", 500, 0, (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_tick('AAPL', '2020-03-25', 500, 0))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.StockTick(context.Background()).Symbol("AAPL").Date("2021-07-23").Limit(50).Skip(0).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->stockTick("AAPL", "2020-03-25", 500, 0));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.stock_tick('AAPL', '2020-03-25', 500, 0))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.stockTick("AAPL", "2020-03-25", 500, 0))
```

### 示例 7 (json)

```json
{
  "p": [
    255,
    255,
    255
  ],
  "s": "AAPL",
  "skip": 0,
  "t": [
    1585108800073,
    1585108800315,
    1585108800381
  ],
  "v": [
    2513,
    24,
    1
  ],
  "x": [
    "P",
    "P",
    "P"
  ],
  "count": 3,
  "c":[["1","24"],["1","24","12"],["1","24","12"]]
}
```

## 文档正文

Get historical tick data for global exchanges.For more historical tick data, you can visit our bulk download page in the Dashboard here to speed up the download process.
  
    
      Exchange
      Segment
      Delay
    
  
  
    
      US CTA/UTP
      Full SIP
      End-of-day
    
    
      TSX
      TSXTSX VentureIndex
      End-of-day
    
    
      LSE
      London Stock Exchange (L)LSE International (L)LSE European (L)
      15 minute
    
    
      Euronext
       Euronext Paris (PA) Euronext Amsterdam (AS) Euronext Lisbon (LS) Euronext Brussels (BR) Euronext Oslo (OL) Euronext London (LN) Euronext Dublin (IR) Index Warrant
      End-of-day
    
    
      Deutsche Börse
       Frankfurt (F) Xetra (DE) Duesseldorf (DU) Hamburg (HM) Berlin (BE) Hanover (HA) Stoxx (SX) TradeGate (TG) Zertifikate (SC) Index Warrant
      End-of-day

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/tick?symbol=AAPL&date=2021-03-09&limit=500&skip=0&format=json`

Tick Data Premium

Get historical tick data for global exchanges.

For more historical tick data, you can visit our bulk download page in the Dashboard here to speed up the download process.

Exchange	Segment	Delay
US CTA/UTP	Full SIP	End-of-day
TSX	
TSX
TSX Venture
Index
	End-of-day
LSE	
London Stock Exchange (L)
LSE International (L)
LSE European (L)
	15 minute
Euronext	
Euronext Paris (PA)
Euronext Amsterdam (AS)
Euronext Lisbon (LS)
Euronext Brussels (BR)
Euronext Oslo (OL)
Euronext London (LN)
Euronext Dublin (IR)
Index
Warrant
	End-of-day
Deutsche Börse	
Frankfurt (F)
Xetra (DE)
Duesseldorf (DU)
Hamburg (HM)
Berlin (BE)
Hanover (HA)
Stoxx (SX)
TradeGate (TG)
Zertifikate (SC)
Index
Warrant
	End-of-day

Method: GET

Premium: Premium Access Required

Examples:

/stock/tick?symbol=AAPL&date=2021-03-09&limit=500&skip=0&format=json

/stock/tick?symbol=AC.TO&date=2021-03-09&limit=500&skip=0&format=json

/stock/tick?symbol=BARC.L&date=2021-03-09&limit=500&skip=0&format=json

Arguments:

symbolREQUIRED

Symbol.

dateREQUIRED

Date: 2020-04-02.

limitREQUIRED

Limit number of ticks returned. Maximum value: 25000

skipREQUIRED

Number of ticks to skip. Use this parameter to loop through the entire data.

Response Attributes:

c

List of trade conditions. A comprehensive list of trade conditions code can be found here

count

Number of ticks returned. If count < limit, all data for that date has been returned.

p

List of price data.

s

Symbol.

skip

Number of ticks skipped.

t

List of timestamp in UNIX ms.

total

Total number of ticks for that date.

v

List of volume data.

x

List of venues/exchanges. A list of exchange codes can be found here

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

print(finnhub_client.stock_tick('AAPL', '2020-03-25', 500, 0))

Sample response

{
  "p": [
    255,
    255,
  ],
  "s": "AAPL",
  "skip": 0,
  "t": [
    1585108800073,
    1585108800315,
  ],
  "v": [
    2513,
    24,
  ],
  "x": [
    "P",
    "P",
    "P"
  ],
  "count": 3,
  "c":[["1","24"],["1","24","12"],["1","24","12"]]
}
