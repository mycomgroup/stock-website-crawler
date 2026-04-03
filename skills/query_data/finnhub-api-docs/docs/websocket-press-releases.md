---
id: "url-122435c7"
type: "api"
title: "Press Releases Premium"
url: "https://finnhub.io/docs/api/websocket-press-releases"
description: "Stream real-time press releases data for global companies. This feature is only available for Enterprise users. Method: Websocket Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T09:54:00.780Z"
metadata:
  requestMethod: "GET"
  endpoint: ""
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Press Releases Premium\n\nStream real-time press releases data for global companies. This feature is only available for Enterprise users.\n\nMethod: Websocket\n\nPremium: Premium Access Required\n\nExamples:\n\nwss://ws.finnhub.io\n\nResponse Attributes:\n\ntype\n\nMessage type: news.\n\ndata\n\nList of news.\n\ndatetime\n\nPublished time in UNIX timestamp.\n\nheadline\n\nNews headline.\n\nsymbol\n\nRelated stocks and companies mentioned in the article.\n\nfullText\n\nURL to download the full-text data.\n\nurl\n\nURL to read the article.\n\nSample code\nPython\nJavascript\nGo\n\n#https://pypi.org/project/websocket_client/\nimport websocket\n\ndef on_message(ws, message):\n    print(message)\n\ndef on_error(ws, error):\n    print(error)\n\ndef on_close(ws):\n    print(\"### closed ###\")\n\ndef on_open(ws):\n    ws.send('{\"type\":\"subscribe-pr\",\"symbol\":\"AAPL\"}')\n    ws.send('{\"type\":\"subscribe-pr\",\"symbol\":\"AMZN\"}')\n    ws.send('{\"type\":\"subscribe-pr\",\"symbol\":\"MSFT\"}')\n    ws.send('{\"type\":\"subscribe-pr\",\"symbol\":\"BYND\"}')\n\nif __name__ == \"__main__\":\n    websocket.enableTrace(True)\n    ws = websocket.WebSocketApp(\"wss://ws.finnhub.io?token=\",\n                              on_message = on_message,\n                              on_error = on_error,\n                              on_close = on_close)\n    ws.on_open = on_open\n    ws.run_forever()\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"datetime\": 1637696940,\n      \"fullText\": \"https://static2.finnhub.io/file/publicdatany/pr/0eb7fb4118ec53204755719b4cc4d57e9370d3caa2fa15d5e7a8f3b4d99cc881.html\",\n      \"headline\": \"STOCKHOLDER ALERT: Monteverde &amp; Associates PC Continues to Investigate the Following Merger\",\n      \"symbol\": \"PAE,ZIXI,KRA\",\n      \"url\": \"https://finnhub.io/api/press-releases?id=0eb7fb4118ec53204755719b4cc4d57e9370d3caa2fa15d5e7a8f3b4d99cc881\"\n    }\n  ],\n  \"type\": \"pr\"\n}"
  suggestedFilename: "websocket-press-releases"
---

# Press Releases Premium

## 源URL

https://finnhub.io/docs/api/websocket-press-releases

## 描述

Stream real-time press releases data for global companies. This feature is only available for Enterprise users. Method: Websocket Premium: Premium Access Required

## API 端点

**Method**: `GET`

## 文档正文

Stream real-time press releases data for global companies. This feature is only available for Enterprise users. Method: Websocket Premium: Premium Access Required

## API 端点

**Method:** `GET`

Press Releases Premium

Stream real-time press releases data for global companies. This feature is only available for Enterprise users.

Method: Websocket

Premium: Premium Access Required

Examples:

wss://ws.finnhub.io

Response Attributes:

type

Message type: news.

data

List of news.

datetime

Published time in UNIX timestamp.

headline

News headline.

symbol

Related stocks and companies mentioned in the article.

fullText

URL to download the full-text data.

url

URL to read the article.

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
    ws.send('{"type":"subscribe-pr","symbol":"AAPL"}')
    ws.send('{"type":"subscribe-pr","symbol":"AMZN"}')
    ws.send('{"type":"subscribe-pr","symbol":"MSFT"}')
    ws.send('{"type":"subscribe-pr","symbol":"BYND"}')

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
      "datetime": 1637696940,
      "fullText": "https://static2.finnhub.io/file/publicdatany/pr/0eb7fb4118ec53204755719b4cc4d57e9370d3caa2fa15d5e7a8f3b4d99cc881.html",
      "headline": "STOCKHOLDER ALERT: Monteverde &amp; Associates PC Continues to Investigate the Following Merger",
      "symbol": "PAE,ZIXI,KRA",
      "url": "https://finnhub.io/api/press-releases?id=0eb7fb4118ec53204755719b4cc4d57e9370d3caa2fa15d5e7a8f3b4d99cc881"
    }
  ],
  "type": "pr"
}
