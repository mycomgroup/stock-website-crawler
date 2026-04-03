---
id: "url-687a1d8e"
type: "api"
title: "AI Copilot Premium"
url: "https://finnhub.io/docs/api/ai-copilot-llm"
description: "Chat with our AI copilot trained on the extensive Finnhub's global data. You can ask it any finance-related questions just like with other LLM models and receive results in texts and widgets. Method: POST Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T06:59:12.288Z"
metadata:
  requestMethod: "GET"
  endpoint: "/ai-chat"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "AI Copilot Premium\n\nChat with our AI copilot trained on the extensive Finnhub's global data. You can ask it any finance-related questions just like with other LLM models and receive results in texts and widgets.\n\nMethod: POST\n\nPremium: Premium Access Required\n\nExamples:\n\n/ai-chat\n\nPayload:\n\nmessagesREQUIRED\n\nMessages\n\nstreamoptional\n\nStream responses\n\nResponse Attributes:\n\nchatId\n\nChat ID.\n\ncontent\n\nResponse text.\n\nquerySummary\n\nQuery summary\n\nrelatedQueries\n\nRelated queries.\n\nsources\n\nSources.\n\ntickers\n\nList of tickers mentioned.\n\nwidgets\n\nWidgets.\n\nSample code\ncURL\nPython\nJavascript\n\nimport requests\nimport json\n\nurl = \"https://finnhub.io/api/v1/ai-chat?token=\"\n\npayload = json.dumps({\n    \"messages\": [\n            {\n                \"role\": \"system\",\n                \"content\": \"Be precise and concise.\"\n            },\n            {\n                \"role\": \"user\",\n                \"content\": \"What is the current price of NVDA?\"\n            }\n        ]\n})\n\nresponse = requests.request(\"POST\", url, data=payload)\n\nprint(response.json())\n\nSample response\n\n{\n  \"chatId\": \"uQElLdY7vZ\",\n  \"content\": \"The current price of NVIDIA Corp (NVDA) is $124.92. The price has increased by 3.97% in the past 24 hours.\\n\",\n  \"querySummary\": \"NVDA Stock Price\",\n  \"relatedQueries\": [\n    \"What is NVDA's price target?\",\n    \"Is NVDA a good stock to buy?\",\n    \"What factors affect NVDA's price?\"\n  ],\n  \"sources\": [\n    {\n      \"link\": \"https://finnhub.io/docs/api\",\n      \"shortURL\": \"finnhub.io\",\n      \"snippet\": \"Comprehensive stock API for realtime market data, global company fundamentals, economic data, and alternative data...\",\n      \"title\": \"Finnhub API Documentation\",\n      \"websiteName\": \"Finnhub\"\n    }\n  ],\n  \"tickers\": [\n    {\n      \"priceCurrency\": \"USD\",\n      \"reportingCurrency\": \"USD\",\n      \"ticker\": \"NVDA\"\n    }\n  ],\n  \"widgets\": [\n    \"https://finnhub.io/widget?ticker=NVDA&which=historical-price\"\n  ]\n}"
  suggestedFilename: "ai-copilot-llm"
---

# AI Copilot Premium

## 源URL

https://finnhub.io/docs/api/ai-copilot-llm

## 描述

Chat with our AI copilot trained on the extensive Finnhub's global data. You can ask it any finance-related questions just like with other LLM models and receive results in texts and widgets. Method: POST Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/ai-chat`

## 文档正文

Chat with our AI copilot trained on the extensive Finnhub's global data. You can ask it any finance-related questions just like with other LLM models and receive results in texts and widgets. Method: POST Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/ai-chat`

AI Copilot Premium

Chat with our AI copilot trained on the extensive Finnhub's global data. You can ask it any finance-related questions just like with other LLM models and receive results in texts and widgets.

Method: POST

Premium: Premium Access Required

Examples:

/ai-chat

Payload:

messagesREQUIRED

Messages

streamoptional

Stream responses

Response Attributes:

chatId

Chat ID.

content

Response text.

querySummary

Query summary

relatedQueries

Related queries.

sources

Sources.

tickers

List of tickers mentioned.

widgets

Widgets.

Sample code
cURL
Python
Javascript

import requests
import json

url = "https://finnhub.io/api/v1/ai-chat?token="

payload = json.dumps({
    "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": "What is the current price of NVDA?"
            }
        ]
})

response = requests.request("POST", url, data=payload)

print(response.json())

Sample response

{
  "chatId": "uQElLdY7vZ",
  "content": "The current price of NVIDIA Corp (NVDA) is $124.92. The price has increased by 3.97% in the past 24 hours.\n",
  "querySummary": "NVDA Stock Price",
  "relatedQueries": [
    "What is NVDA's price target?",
    "Is NVDA a good stock to buy?",
    "What factors affect NVDA's price?"
  ],
  "sources": [
    {
      "link": "https://finnhub.io/docs/api",
      "shortURL": "finnhub.io",
      "snippet": "Comprehensive stock API for realtime market data, global company fundamentals, economic data, and alternative data...",
      "title": "Finnhub API Documentation",
      "websiteName": "Finnhub"
    }
  ],
  "tickers": [
    {
      "priceCurrency": "USD",
      "reportingCurrency": "USD",
      "ticker": "NVDA"
    }
  ],
  "widgets": [
    "https://finnhub.io/widget?ticker=NVDA&which=historical-price"
  ]
}
