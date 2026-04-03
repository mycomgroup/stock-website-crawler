---
id: "url-1b9e0b7"
type: "api"
title: "Revenue Breakdown & KPI Premium"
url: "https://finnhub.io/docs/api/revenue-breakdown-kpi-api"
description: "Get standardized revenue breakdown and KPIs data for 30,000+ global companies. Method: GET Premium: Premium"
source: ""
tags: []
crawl_time: "2026-03-18T10:37:35.257Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/revenue-breakdown2?symbol=AAPL"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Revenue Breakdown & KPI Premium\n\nGet standardized revenue breakdown and KPIs data for 30,000+ global companies.\n\nMethod: GET\n\nPremium: Premium\n\nExamples:\n\n/stock/revenue-breakdown2?symbol=AAPL\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\nResponse Attributes:\n\ncurrency\n\ncurrency\n\ndata\n\nRevenue breakdown data.\n\nsymbol\n\nSymbol\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_revenue_breakdown2('AAPL'))\n\nSample response\n\n{\n  \"currency\": \"USD\",\n  \"data\": {\n    \"annual\": {\n      \"revenue_by_geography\": [\n        [\n          {\n            \"data\": [\n              {\n                \"period\": \"2023-09-30\",\n                \"value\": 162560000000\n              },\n              {\n                \"period\": \"2024-09-28\",\n                \"value\": 167045000000\n              }\n            ],\n            \"label\": \"Americas\"\n          }\n        ]\n      ],\n      \"revenue_by_product\": [\n        [\n          {\n            \"data\": [\n              {\n                \"period\": \"2023-09-30\",\n                \"value\": 200583000000\n              },\n              {\n                \"period\": \"2024-09-28\",\n                \"value\": 201183000000\n              }\n            ],\n            \"label\": \"iPhone\"\n          }\n        ]\n      ]\n    },\n    \"quarterly\": {\n      \"revenue_by_geography\": [\n        [\n          {\n            \"data\": [\n              {\n                \"period\": \"2024-09-28\",\n                \"value\": 41664000000\n              },\n              {\n                \"period\": \"2024-12-28\",\n                \"value\": 52648000000\n              }\n            ],\n            \"label\": \"Americas\"\n          }\n        ]\n      ],\n      \"revenue_by_product\": [\n        [\n          {\n            \"data\": [\n              {\n                \"period\": \"2024-09-28\",\n                \"value\": 46222000000\n              },\n              {\n                \"period\": \"2024-12-28\",\n                \"value\": 69138000000\n              }\n            ],\n            \"label\": \"iPhone\"\n          }\n        ]\n      ]\n    }\n  },\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "revenue-breakdown-kpi-api"
---

# Revenue Breakdown & KPI Premium

## 源URL

https://finnhub.io/docs/api/revenue-breakdown-kpi-api

## 描述

Get standardized revenue breakdown and KPIs data for 30,000+ global companies. Method: GET Premium: Premium

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/revenue-breakdown2?symbol=AAPL`

## 文档正文

Get standardized revenue breakdown and KPIs data for 30,000+ global companies. Method: GET Premium: Premium

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/revenue-breakdown2?symbol=AAPL`

Revenue Breakdown & KPI Premium

Get standardized revenue breakdown and KPIs data for 30,000+ global companies.

Method: GET

Premium: Premium

Examples:

/stock/revenue-breakdown2?symbol=AAPL

Arguments:

symbolREQUIRED

Symbol.

Response Attributes:

currency

currency

data

Revenue breakdown data.

symbol

Symbol

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

print(finnhub_client.stock_revenue_breakdown2('AAPL'))

Sample response

{
  "currency": "USD",
  "data": {
    "annual": {
      "revenue_by_geography": [
        [
          {
            "data": [
              {
                "period": "2023-09-30",
                "value": 162560000000
              },
              {
                "period": "2024-09-28",
                "value": 167045000000
              }
            ],
            "label": "Americas"
          }
        ]
      ],
      "revenue_by_product": [
        [
          {
            "data": [
              {
                "period": "2023-09-30",
                "value": 200583000000
              },
              {
                "period": "2024-09-28",
                "value": 201183000000
              }
            ],
            "label": "iPhone"
          }
        ]
      ]
    },
    "quarterly": {
      "revenue_by_geography": [
        [
          {
            "data": [
              {
                "period": "2024-09-28",
                "value": 41664000000
              },
              {
                "period": "2024-12-28",
                "value": 52648000000
              }
            ],
            "label": "Americas"
          }
        ]
      ],
      "revenue_by_product": [
        [
          {
            "data": [
              {
                "period": "2024-09-28",
                "value": 46222000000
              },
              {
                "period": "2024-12-28",
                "value": 69138000000
              }
            ],
            "label": "iPhone"
          }
        ]
      ]
    }
  },
  "symbol": "AAPL"
}
