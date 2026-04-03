---
id: "url-6548c4c1"
type: "api"
title: "Press Releases Premium"
url: "https://finnhub.io/docs/api/press-releases"
description: "Get latest major press releases of a company. This data can be used to highlight the most significant events comprised of mostly press releases sourced from the exchanges, BusinessWire, AccessWire, GlobeNewswire, Newsfile, and PRNewswire.Full-text press releases data is available for Enterprise clients. Contact Us to learn more."
source: ""
tags: []
crawl_time: "2026-03-18T06:29:08.273Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/press-releases"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Company symbol."}
    - {"name":"from","in":"query","required":false,"type":"string","description":"From time: 2020-01-01."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To time: 2020-01-05."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.pressReleases(\"AAPL\", {}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.press_releases('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.PressReleases(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->pressReleases(\"AAPL\", \"2020-01-01\", \"2020-12-31\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.press_releases('AAPL', {from: \"2020-01-01\", to: \"2020-12-31\"}))"}
    - {"language":"Kotlin","code":"println(apiClient.pressReleases(\"AAPL\", from = \"2020-01-01\", to = \"2020-12-31\"))"}
  sampleResponse: "{\n  \"majorDevelopment\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"datetime\": \"2020-08-04 17:06:32\",\n      \"headline\": \"27-inch iMac Gets a Major Update\",\n      \"description\": \"CUPERTINO, Calif.--(BUSINESS WIRE)-- Apple today announced a major update to its 27-inch iMac®. By far the most powerful and capable iMac ever, it features faster Intel processors up to 10 cores, double the memory capacity, next-generation AMD graphics, superfast SSDs across the line with four times the storage capacity, a new nano-texture glass option for an even more stunning Retina® 5K display, a 1080p FaceTime® HD camera, higher fidelity speakers, and studio-quality mics. For the consumer using their iMac all day, every day, to the aspiring creative looking for inspiration, to the serious pro pushing the limits of their creativity, the new 27-inch iMac delivers the ultimate desktop experience that is now better in every way.\"\n    },\n    {\n      \"symbol\": \"AAPL\",\n      \"datetime\": \"2020-03-28 09:41:23\",\n      \"headline\": \"Apple Central World Opens Friday in Thailand\",\n      \"description\": \"BANGKOK--(BUSINESS WIRE)-- Apple® today previewed Apple Central World, its second and largest retail location in Thailand. Nestled in the heart of Ratchaprasong, Bangkok’s iconic intersection, the store provides a completely new and accessible destination within the lively city. Apple Central World’s distinctive architecture is brought to life with the first-ever all-glass design, housed under a cantilevered Tree Canopy roof. Once inside, customers can travel between two levels via a spiral staircase that wraps around a timber core, or riding a unique cylindrical elevator clad in mirror-polished stainless steel. Guests can enter from the ground or upper level, which provides a direct connection to the Skytrain and the city’s largest shopping center. The outdoor plaza offers a place for the community to gather, with benches and large Terminalia trees surrounding the space.\"\n    }\n  ],\n   \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"majorDevelopment\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"datetime\": \"2020-08-04 17:06:32\",\n      \"headline\": \"27-inch iMac Gets a Major Update\",\n      \"description\": \"CUPERTINO, Calif.--(BUSINESS WIRE)-- Apple today announced a major update to its 27-inch iMac®. By far the most powerful and capable iMac ever, it features faster Intel processors up to 10 cores, double the memory capacity, next-generation AMD graphics, superfast SSDs across the line with four times the storage capacity, a new nano-texture glass option for an even more stunning Retina® 5K display, a 1080p FaceTime® HD camera, higher fidelity speakers, and studio-quality mics. For the consumer using their iMac all day, every day, to the aspiring creative looking for inspiration, to the serious pro pushing the limits of their creativity, the new 27-inch iMac delivers the ultimate desktop experience that is now better in every way.\"\n    },\n    {\n      \"symbol\": \"AAPL\",\n      \"datetime\": \"2020-03-28 09:41:23\",\n      \"headline\": \"Apple Central World Opens Friday in Thailand\",\n      \"description\": \"BANGKOK--(BUSINESS WIRE)-- Apple® today previewed Apple Central World, its second and largest retail location in Thailand. Nestled in the heart of Ratchaprasong, Bangkok’s iconic intersection, the store provides a completely new and accessible destination within the lively city. Apple Central World’s distinctive architecture is brought to life with the first-ever all-glass design, housed under a cantilevered Tree Canopy roof. Once inside, customers can travel between two levels via a spiral staircase that wraps around a timber core, or riding a unique cylindrical elevator clad in mirror-polished stainless steel. Guests can enter from the ground or upper level, which provides a direct connection to the Skytrain and the city’s largest shopping center. The outdoor plaza offers a place for the community to gather, with benches and large Terminalia trees surrounding the space.\"\n    }\n  ],\n   \"symbol\": \"AAPL\"\n}"
  rawContent: "Press Releases Premium\n\nStream real-time press releases data for global companies. This feature is only available for Enterprise users.\n\nMethod: Websocket\n\nPremium: Premium Access Required\n\nExamples:\n\nwss://ws.finnhub.io\n\nResponse Attributes:\n\ntype\n\nMessage type: news.\n\ndata\n\nList of news.\n\ndatetime\n\nPublished time in UNIX timestamp.\n\nheadline\n\nNews headline.\n\nsymbol\n\nRelated stocks and companies mentioned in the article.\n\nfullText\n\nURL to download the full-text data.\n\nurl\n\nURL to read the article.\n\nSample code\nPython\nJavascript\nGo\n\n#https://pypi.org/project/websocket_client/\nimport websocket\n\ndef on_message(ws, message):\n    print(message)\n\ndef on_error(ws, error):\n    print(error)\n\ndef on_close(ws):\n    print(\"### closed ###\")\n\ndef on_open(ws):\n    ws.send('{\"type\":\"subscribe-pr\",\"symbol\":\"AAPL\"}')\n    ws.send('{\"type\":\"subscribe-pr\",\"symbol\":\"AMZN\"}')\n    ws.send('{\"type\":\"subscribe-pr\",\"symbol\":\"MSFT\"}')\n    ws.send('{\"type\":\"subscribe-pr\",\"symbol\":\"BYND\"}')\n\nif __name__ == \"__main__\":\n    websocket.enableTrace(True)\n    ws = websocket.WebSocketApp(\"wss://ws.finnhub.io?token=\",\n                              on_message = on_message,\n                              on_error = on_error,\n                              on_close = on_close)\n    ws.on_open = on_open\n    ws.run_forever()\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"datetime\": 1637696940,\n      \"fullText\": \"https://static2.finnhub.io/file/publicdatany/pr/0eb7fb4118ec53204755719b4cc4d57e9370d3caa2fa15d5e7a8f3b4d99cc881.html\",\n      \"headline\": \"STOCKHOLDER ALERT: Monteverde &amp; Associates PC Continues to Investigate the Following Merger\",\n      \"symbol\": \"PAE,ZIXI,KRA\",\n      \"url\": \"https://finnhub.io/api/press-releases?id=0eb7fb4118ec53204755719b4cc4d57e9370d3caa2fa15d5e7a8f3b4d99cc881\"\n    }\n  ],\n  \"type\": \"pr\"\n}"
  suggestedFilename: "press-releases"
---

# Press Releases Premium

## 源URL

https://finnhub.io/docs/api/press-releases

## 描述

Get latest major press releases of a company. This data can be used to highlight the most significant events comprised of mostly press releases sourced from the exchanges, BusinessWire, AccessWire, GlobeNewswire, Newsfile, and PRNewswire.Full-text press releases data is available for Enterprise clients. Contact Us to learn more.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/press-releases`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Company symbol. |
| `from` | string | 否 | - | From time: 2020-01-01. |
| `to` | string | 否 | - | To time: 2020-01-05. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.pressReleases("AAPL", {}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.press_releases('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.PressReleases(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->pressReleases("AAPL", "2020-01-01", "2020-12-31"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.press_releases('AAPL', {from: "2020-01-01", to: "2020-12-31"}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.pressReleases("AAPL", from = "2020-01-01", to = "2020-12-31"))
```

### 示例 7 (json)

```json
{
  "majorDevelopment": [
    {
      "symbol": "AAPL",
      "datetime": "2020-08-04 17:06:32",
      "headline": "27-inch iMac Gets a Major Update",
      "description": "CUPERTINO, Calif.--(BUSINESS WIRE)-- Apple today announced a major update to its 27-inch iMac®. By far the most powerful and capable iMac ever, it features faster Intel processors up to 10 cores, double the memory capacity, next-generation AMD graphics, superfast SSDs across the line with four times the storage capacity, a new nano-texture glass option for an even more stunning Retina® 5K display, a 1080p FaceTime® HD camera, higher fidelity speakers, and studio-quality mics. For the consumer using their iMac all day, every day, to the aspiring creative looking for inspiration, to the serious pro pushing the limits of their creativity, the new 27-inch iMac delivers the ultimate desktop experience that is now better in every way."
    },
    {
      "symbol": "AAPL",
      "datetime": "2020-03-28 09:41:23",
      "headline": "Apple Central World Opens Friday in Thailand",
      "description": "BANGKOK--(BUSINESS WIRE)-- Apple® today previewed Apple Central World, its second and largest retail location in Thailand. Nestled in the heart of Ratchaprasong, Bangkok’s iconic intersection, the store provides a completely new and accessible destination within the lively city. Apple Central World’s distinctive architecture is brought to life with the first-ever all-glass design, housed under a cantilevered Tree Canopy roof. Once inside, customers can travel between two levels via a spiral staircase that wraps around a timber core, or riding a unique cylindrical elevator clad in mirror-polished stainless steel. Guests can enter from the ground or upper level, which provides a direct connection to the Skytrain and the city’s largest shopping center. The outdoor plaza offers a place for the community to gather, with benches and large Terminalia trees surrounding the space."
    }
  ],
   "symbol": "AAPL"
}
```

## 文档正文

Get latest major press releases of a company. This data can be used to highlight the most significant events comprised of mostly press releases sourced from the exchanges, BusinessWire, AccessWire, GlobeNewswire, Newsfile, and PRNewswire.Full-text press releases data is available for Enterprise clients. Contact Us to learn more.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/press-releases`

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
