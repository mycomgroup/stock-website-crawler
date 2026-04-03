---
id: "url-7d61c5a4"
type: "api"
title: "Tick Data Premium"
url: "https://finnhub.io/docs/api/bond-tick"
description: "Get trade-level data for bonds. The following datasets are supported:\n  \n    \n      Exchange\n      Segment\n      Delay\n    \n  \n  \n    \n      FINRA Trace\n      BTDS: US Corporate Bonds\n      Delayed 4h\n    \n    \n      FINRA Trace\n      144A Bonds\n      Delayed 4h"
source: ""
tags: []
crawl_time: "2026-03-18T03:13:24.830Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/tick?symbol=AAPL&date=2021-03-09&limit=500&skip=0&format=json"
  parameters:
    - {"name":"isin","in":"query","required":true,"type":"string","description":"ISIN."}
    - {"name":"date","in":"query","required":true,"type":"string","description":"Date: 2020-04-02."}
    - {"name":"limit","in":"query","required":true,"type":"integer","description":"Limit number of ticks returned. Maximum value: 25000"}
    - {"name":"skip","in":"query","required":true,"type":"integer","description":"Number of ticks to skip. Use this parameter to loop through the entire data."}
    - {"name":"exchange","in":"query","required":true,"type":"string","description":"Currently support the following values: trace."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.bondTick(\"US693475BF18\", \"2022-08-19\", 500, 0, 'trace', (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.bond_tick('US693475BF18', '2022-08-19', 500, 0, 'trace'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.BondTick(context.Background()).Isin(\"US693475BF18\").Date(\"2022-08-19\").Limit(50).Skip(0).Exchange(\"trace\").Execute()"}
    - {"language":"PHP","code":"print_r($client->bondTick(\"US693475BF18\", \"2022-08-19\", 500, 0, \"trace\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.bond_tick('US693475BF18', '2022-08-19', 500, 0, 'trace'))"}
    - {"language":"Kotlin","code":"println(apiClient.bondTick(\"US693475BF18\", \"2022-08-19\", 500, 0, 'trace'))"}
  sampleResponse: "{\n   \"c\":[[],[],[]],\n   \"count\":3,\n   \"cp\":[\n      \"3\",\n      \"1\",\n      \"1\"\n   ],\n   \"p\":[\n      100.592,\n      100.492,\n      100.234\n   ],\n   \"si\":[\n      \"2\",\n      \"2\",\n      \"2\"\n   ],\n   \"skip\":6,\n   \"t\":[\n      1660929161000,\n      1660929161000,\n      1660929778000\n   ],\n   \"total\":211,\n   \"v\":[\n      3000,\n      3000,\n      50000\n   ]\n}"
  curlExample: ""
  jsonExample: "{\n   \"c\":[[],[],[]],\n   \"count\":3,\n   \"cp\":[\n      \"3\",\n      \"1\",\n      \"1\"\n   ],\n   \"p\":[\n      100.592,\n      100.492,\n      100.234\n   ],\n   \"si\":[\n      \"2\",\n      \"2\",\n      \"2\"\n   ],\n   \"skip\":6,\n   \"t\":[\n      1660929161000,\n      1660929161000,\n      1660929778000\n   ],\n   \"total\":211,\n   \"v\":[\n      3000,\n      3000,\n      50000\n   ]\n}"
  rawContent: "Tick Data Premium\n\nGet historical tick data for global exchanges.\n\nFor more historical tick data, you can visit our bulk download page in the Dashboard here to speed up the download process.\n\nExchange\tSegment\tDelay\nUS CTA/UTP\tFull SIP\tEnd-of-day\nTSX\t\nTSX\nTSX Venture\nIndex\n\tEnd-of-day\nLSE\t\nLondon Stock Exchange (L)\nLSE International (L)\nLSE European (L)\n\t15 minute\nEuronext\t\nEuronext Paris (PA)\nEuronext Amsterdam (AS)\nEuronext Lisbon (LS)\nEuronext Brussels (BR)\nEuronext Oslo (OL)\nEuronext London (LN)\nEuronext Dublin (IR)\nIndex\nWarrant\n\tEnd-of-day\nDeutsche Börse\t\nFrankfurt (F)\nXetra (DE)\nDuesseldorf (DU)\nHamburg (HM)\nBerlin (BE)\nHanover (HA)\nStoxx (SX)\nTradeGate (TG)\nZertifikate (SC)\nIndex\nWarrant\n\tEnd-of-day\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/tick?symbol=AAPL&date=2021-03-09&limit=500&skip=0&format=json\n\n/stock/tick?symbol=AC.TO&date=2021-03-09&limit=500&skip=0&format=json\n\n/stock/tick?symbol=BARC.L&date=2021-03-09&limit=500&skip=0&format=json\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\ndateREQUIRED\n\nDate: 2020-04-02.\n\nlimitREQUIRED\n\nLimit number of ticks returned. Maximum value: 25000\n\nskipREQUIRED\n\nNumber of ticks to skip. Use this parameter to loop through the entire data.\n\nResponse Attributes:\n\nc\n\nList of trade conditions. A comprehensive list of trade conditions code can be found here\n\ncount\n\nNumber of ticks returned. If count < limit, all data for that date has been returned.\n\np\n\nList of price data.\n\ns\n\nSymbol.\n\nskip\n\nNumber of ticks skipped.\n\nt\n\nList of timestamp in UNIX ms.\n\ntotal\n\nTotal number of ticks for that date.\n\nv\n\nList of volume data.\n\nx\n\nList of venues/exchanges. A list of exchange codes can be found here\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_tick('AAPL', '2020-03-25', 500, 0))\n\nSample response\n\n{\n  \"p\": [\n    255,\n    255,\n  ],\n  \"s\": \"AAPL\",\n  \"skip\": 0,\n  \"t\": [\n    1585108800073,\n    1585108800315,\n  ],\n  \"v\": [\n    2513,\n    24,\n  ],\n  \"x\": [\n    \"P\",\n    \"P\",\n    \"P\"\n  ],\n  \"count\": 3,\n  \"c\":[[\"1\",\"24\"],[\"1\",\"24\",\"12\"],[\"1\",\"24\",\"12\"]]\n}"
  suggestedFilename: "bond-tick"
---

# Tick Data Premium

## 源URL

https://finnhub.io/docs/api/bond-tick

## 描述

Get trade-level data for bonds. The following datasets are supported:
  
    
      Exchange
      Segment
      Delay
    
  
  
    
      FINRA Trace
      BTDS: US Corporate Bonds
      Delayed 4h
    
    
      FINRA Trace
      144A Bonds
      Delayed 4h

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/tick?symbol=AAPL&date=2021-03-09&limit=500&skip=0&format=json`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `isin` | string | 是 | - | ISIN. |
| `date` | string | 是 | - | Date: 2020-04-02. |
| `limit` | integer | 是 | - | Limit number of ticks returned. Maximum value: 25000 |
| `skip` | integer | 是 | - | Number of ticks to skip. Use this parameter to loop through the entire data. |
| `exchange` | string | 是 | - | Currently support the following values: trace. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.bondTick("US693475BF18", "2022-08-19", 500, 0, 'trace', (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.bond_tick('US693475BF18', '2022-08-19', 500, 0, 'trace'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.BondTick(context.Background()).Isin("US693475BF18").Date("2022-08-19").Limit(50).Skip(0).Exchange("trace").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->bondTick("US693475BF18", "2022-08-19", 500, 0, "trace"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.bond_tick('US693475BF18', '2022-08-19', 500, 0, 'trace'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.bondTick("US693475BF18", "2022-08-19", 500, 0, 'trace'))
```

### 示例 7 (json)

```json
{
   "c":[[],[],[]],
   "count":3,
   "cp":[
      "3",
      "1",
      "1"
   ],
   "p":[
      100.592,
      100.492,
      100.234
   ],
   "si":[
      "2",
      "2",
      "2"
   ],
   "skip":6,
   "t":[
      1660929161000,
      1660929161000,
      1660929778000
   ],
   "total":211,
   "v":[
      3000,
      3000,
      50000
   ]
}
```

## 文档正文

Get trade-level data for bonds. The following datasets are supported:
  
    
      Exchange
      Segment
      Delay
    
  
  
    
      FINRA Trace
      BTDS: US Corporate Bonds
      Delayed 4h
    
    
      FINRA Trace
      144A Bonds
      Delayed 4h

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
