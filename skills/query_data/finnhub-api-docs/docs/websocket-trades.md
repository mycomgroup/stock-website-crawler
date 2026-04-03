---
id: "url-6c18a140"
type: "api"
title: "Trades - Last Price Updates"
url: "https://finnhub.io/docs/api/websocket-trades"
description: "Stream real-time trades for US stocks, forex and crypto. Trades might not be available for some forex and crypto exchanges. In that case, a price update will be sent with volume = 0. A message can contain multiple trades. 1 API key can only open 1 connection at a time. The following FX brokers do not support streaming: FXCM, Forex.com, FHFX. To get latest price for FX, please use the Forex Candles or All Rates endpoint. Method: Websocket"
source: ""
tags: []
crawl_time: "2026-03-18T07:30:52.383Z"
metadata:
  requestMethod: "GET"
  endpoint: ""
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Trades - Last Price Updates\n\nStream real-time trades for US stocks, forex and crypto. Trades might not be available for some forex and crypto exchanges. In that case, a price update will be sent with volume = 0. A message can contain multiple trades. 1 API key can only open 1 connection at a time.\n\nThe following FX brokers do not support streaming: FXCM, Forex.com, FHFX. To get latest price for FX, please use the Forex Candles or All Rates endpoint.\n\nMethod: Websocket\n\nExamples:\n\nwss://ws.finnhub.io\n\nResponse Attributes:\n\ntype\n\nMessage type.\n\ndata\n\nList of trades or price updates.\n\ns\n\nSymbol.\n\np\n\nLast price.\n\nt\n\nUNIX milliseconds timestamp.\n\nv\n\nVolume.\n\nc\n\nList of trade conditions. A comprehensive list of trade conditions code can be found here\n\nSample code\nPython\nJavascript\nGo\n\n#https://pypi.org/project/websocket_client/\nimport websocket\n\ndef on_message(ws, message):\n    print(message)\n\ndef on_error(ws, error):\n    print(error)\n\ndef on_close(ws):\n    print(\"### closed ###\")\n\ndef on_open(ws):\n    ws.send('{\"type\":\"subscribe\",\"symbol\":\"AAPL\"}')\n    ws.send('{\"type\":\"subscribe\",\"symbol\":\"AMZN\"}')\n    ws.send('{\"type\":\"subscribe\",\"symbol\":\"BINANCE:BTCUSDT\"}')\n    ws.send('{\"type\":\"subscribe\",\"symbol\":\"IC MARKETS:1\"}')\n\nif __name__ == \"__main__\":\n    websocket.enableTrace(True)\n    ws = websocket.WebSocketApp(\"wss://ws.finnhub.io?token=\",\n                              on_message = on_message,\n                              on_error = on_error,\n                              on_close = on_close)\n    ws.on_open = on_open\n    ws.run_forever()\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"p\": 7296.89,\n      \"s\": \"BINANCE:BTCUSDT\",\n      \"t\": 1575526691134,\n      \"v\": 0.011467\n    }\n  ],\n  \"type\": \"trade\"\n}"
  suggestedFilename: "websocket-trades"
---

# Trades - Last Price Updates

## 源URL

https://finnhub.io/docs/api/websocket-trades

## 描述

Stream real-time trades for US stocks, forex and crypto. Trades might not be available for some forex and crypto exchanges. In that case, a price update will be sent with volume = 0. A message can contain multiple trades. 1 API key can only open 1 connection at a time. The following FX brokers do not support streaming: FXCM, Forex.com, FHFX. To get latest price for FX, please use the Forex Candles or All Rates endpoint. Method: Websocket

## API 端点

**Method**: `GET`

## 文档正文

Stream real-time trades for US stocks, forex and crypto. Trades might not be available for some forex and crypto exchanges. In that case, a price update will be sent with volume = 0. A message can contain multiple trades. 1 API key can only open 1 connection at a time. The following FX brokers do not support streaming: FXCM, Forex.com, FHFX. To get latest price for FX, please use the Forex Candles or All Rates endpoint. Method: Websocket

## API 端点

**Method:** `GET`

Trades - Last Price Updates

Stream real-time trades for US stocks, forex and crypto. Trades might not be available for some forex and crypto exchanges. In that case, a price update will be sent with volume = 0. A message can contain multiple trades. 1 API key can only open 1 connection at a time.

The following FX brokers do not support streaming: FXCM, Forex.com, FHFX. To get latest price for FX, please use the Forex Candles or All Rates endpoint.

Method: Websocket

Examples:

wss://ws.finnhub.io

Response Attributes:

type

Message type.

data

List of trades or price updates.

s

Symbol.

p

Last price.

t

UNIX milliseconds timestamp.

v

Volume.

c

List of trade conditions. A comprehensive list of trade conditions code can be found here

Sample code
Python
Javascript
Go

#https://pypi.org/project/websocket_client/
import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

Sample response

{
  "data": [
    {
      "p": 7296.89,
      "s": "BINANCE:BTCUSDT",
      "t": 1575526691134,
      "v": 0.011467
    }
  ],
  "type": "trade"
}
