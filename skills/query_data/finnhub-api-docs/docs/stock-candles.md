---
id: "url-4f8daf3c"
type: "api"
title: "Stock Candles Premium"
url: "https://finnhub.io/docs/api/stock-candles"
description: "Get candlestick data (OHLCV) for stocks. Daily data will be adjusted for Splits. Intraday data will remain unadjusted. Only 1 month of intraday will be returned at a time. If you need more historical intraday data, please use the from and to params iteratively to request more data. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T04:46:50.556Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/candle?symbol=AAPL&resolution=1&from=1738655051&to=1738741451"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Stock Candles Premium\n\nGet candlestick data (OHLCV) for stocks.\n\nDaily data will be adjusted for Splits. Intraday data will remain unadjusted. Only 1 month of intraday will be returned at a time. If you need more historical intraday data, please use the from and to params iteratively to request more data.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/candle?symbol=AAPL&resolution=1&from=1738655051&to=1738741451\n\n/stock/candle?symbol=IBM&resolution=D&from=1735976651&to=1738741451\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\nresolutionREQUIRED\n\nSupported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.\n\nfromREQUIRED\n\nUNIX timestamp. Interval initial value.\n\ntoREQUIRED\n\nUNIX timestamp. Interval end value.\n\nResponse Attributes:\n\nc\n\nList of close prices for returned candles.\n\nh\n\nList of high prices for returned candles.\n\nl\n\nList of low prices for returned candles.\n\no\n\nList of open prices for returned candles.\n\ns\n\nStatus of the response. This field can either be ok or no_data.\n\nt\n\nList of timestamp for returned candles.\n\nv\n\nList of volume data for returned candles.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249))\n\nSample response\n\n{\n  \"c\": [\n    217.68,\n    221.03,\n    219.89\n  ],\n  \"h\": [\n    222.49,\n    221.5,\n    220.94\n  ],\n  \"l\": [\n    217.19,\n    217.1402,\n    218.83\n  ],\n  \"o\": [\n    221.03,\n    218.55,\n  ],\n  \"s\": \"ok\",\n  \"t\": [\n    1569297600,\n    1569384000,\n  ],\n  \"v\": [\n    33463820,\n    24018876,\n  ]\n}\n\nWidget:"
  suggestedFilename: "stock-candles"
---

# Stock Candles Premium

## 源URL

https://finnhub.io/docs/api/stock-candles

## 描述

Get candlestick data (OHLCV) for stocks. Daily data will be adjusted for Splits. Intraday data will remain unadjusted. Only 1 month of intraday will be returned at a time. If you need more historical intraday data, please use the from and to params iteratively to request more data. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/candle?symbol=AAPL&resolution=1&from=1738655051&to=1738741451`

## 文档正文

Get candlestick data (OHLCV) for stocks. Daily data will be adjusted for Splits. Intraday data will remain unadjusted. Only 1 month of intraday will be returned at a time. If you need more historical intraday data, please use the from and to params iteratively to request more data. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/candle?symbol=AAPL&resolution=1&from=1738655051&to=1738741451`

Stock Candles Premium

Get candlestick data (OHLCV) for stocks.

Daily data will be adjusted for Splits. Intraday data will remain unadjusted. Only 1 month of intraday will be returned at a time. If you need more historical intraday data, please use the from and to params iteratively to request more data.

Method: GET

Premium: Premium Access Required

Examples:

/stock/candle?symbol=AAPL&resolution=1&from=1738655051&to=1738741451

/stock/candle?symbol=IBM&resolution=D&from=1735976651&to=1738741451

Arguments:

symbolREQUIRED

Symbol.

resolutionREQUIRED

Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.

fromREQUIRED

UNIX timestamp. Interval initial value.

toREQUIRED

UNIX timestamp. Interval end value.

Response Attributes:

c

List of close prices for returned candles.

h

List of high prices for returned candles.

l

List of low prices for returned candles.

o

List of open prices for returned candles.

s

Status of the response. This field can either be ok or no_data.

t

List of timestamp for returned candles.

v

List of volume data for returned candles.

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

print(finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249))

Sample response

{
  "c": [
    217.68,
    221.03,
    219.89
  ],
  "h": [
    222.49,
    221.5,
    220.94
  ],
  "l": [
    217.19,
    217.1402,
    218.83
  ],
  "o": [
    221.03,
    218.55,
  ],
  "s": "ok",
  "t": [
    1569297600,
    1569384000,
  ],
  "v": [
    33463820,
    24018876,
  ]
}

Widget:
