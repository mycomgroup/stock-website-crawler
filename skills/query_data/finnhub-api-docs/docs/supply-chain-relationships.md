---
id: "url-126dba04"
type: "api"
title: "Supply Chain Relationships Premium"
url: "https://finnhub.io/docs/api/supply-chain-relationships"
description: "This endpoint provides an overall map of public companies' key customers and suppliers. The data offers a deeper look into a company's supply chain and how products are created. The data will help investors manage risk, limit exposure or generate alpha-generating ideas and trading insights. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T10:37:49.510Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/supply-chain?symbol=AAPL"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Supply Chain Relationships Premium\n\nThis endpoint provides an overall map of public companies' key customers and suppliers. The data offers a deeper look into a company's supply chain and how products are created. The data will help investors manage risk, limit exposure or generate alpha-generating ideas and trading insights.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/supply-chain?symbol=AAPL\n\n/stock/supply-chain?symbol=WMT\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\nResponse Attributes:\n\ndata\n\nKey customers and suppliers.\n\ncountry\n\nCountry\n\ncustomer\n\nWhether the company is a customer.\n\nindustry\n\nIndustry\n\nname\n\nName\n\noneMonthCorrelation\n\n1-month price correlation\n\noneYearCorrelation\n\n1-year price correlation\n\nsixMonthCorrelation\n\n6-month price correlation\n\nsupplier\n\nWhether the company is a supplier\n\nsymbol\n\nSymbol\n\nthreeMonthCorrelation\n\n3-month price correlation\n\ntwoWeekCorrelation\n\n2-week price correlation\n\ntwoYearCorrelation\n\n2-year price correlation\n\nsymbol\n\nsymbol\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_supply_chain('AAPL'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"customer\": true,\n      \"name\": \"Costco Wholesale Corporation\",\n      \"oneMonthCorrelation\": 0.26,\n      \"oneYearCorrelation\": 0.63,\n      \"sixMonthCorrelation\": 0.87,\n      \"supplier\": false,\n      \"symbol\": \"COST\",\n      \"threeMonthCorrelation\": 0.89,\n      \"twoWeekCorrelation\": 0.35,\n      \"twoYearCorrelation\": 0.91\n    },\n    {\n      \"customer\": true,\n      \"name\": \"Qualcomm\",\n      \"oneMonthCorrelation\": 0.06,\n      \"oneYearCorrelation\": 0.58,\n      \"sixMonthCorrelation\": 0.87,\n      \"supplier\": true,\n      \"symbol\": \"QCOM\",\n      \"threeMonthCorrelation\": 0.88,\n      \"twoWeekCorrelation\": 0.71,\n      \"twoYearCorrelation\": 0.94\n    },\n    {\n      \"customer\": false,\n      \"name\": \"Foxconn Industrial Internet Co., Ltd.\",\n      \"oneMonthCorrelation\": 0.25,\n      \"oneYearCorrelation\": -0.48,\n      \"sixMonthCorrelation\": -0.65,\n      \"supplier\": true,\n      \"symbol\": \"601138.SS\",\n      \"threeMonthCorrelation\": -0.79,\n      \"twoWeekCorrelation\": -0.55,\n      \"twoYearCorrelation\": -0.6\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "supply-chain-relationships"
---

# Supply Chain Relationships Premium

## 源URL

https://finnhub.io/docs/api/supply-chain-relationships

## 描述

This endpoint provides an overall map of public companies' key customers and suppliers. The data offers a deeper look into a company's supply chain and how products are created. The data will help investors manage risk, limit exposure or generate alpha-generating ideas and trading insights. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/supply-chain?symbol=AAPL`

## 文档正文

This endpoint provides an overall map of public companies' key customers and suppliers. The data offers a deeper look into a company's supply chain and how products are created. The data will help investors manage risk, limit exposure or generate alpha-generating ideas and trading insights. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/supply-chain?symbol=AAPL`

Supply Chain Relationships Premium

This endpoint provides an overall map of public companies' key customers and suppliers. The data offers a deeper look into a company's supply chain and how products are created. The data will help investors manage risk, limit exposure or generate alpha-generating ideas and trading insights.

Method: GET

Premium: Premium Access Required

Examples:

/stock/supply-chain?symbol=AAPL

/stock/supply-chain?symbol=WMT

Arguments:

symbolREQUIRED

Symbol.

Response Attributes:

data

Key customers and suppliers.

country

Country

customer

Whether the company is a customer.

industry

Industry

name

Name

oneMonthCorrelation

1-month price correlation

oneYearCorrelation

1-year price correlation

sixMonthCorrelation

6-month price correlation

supplier

Whether the company is a supplier

symbol

Symbol

threeMonthCorrelation

3-month price correlation

twoWeekCorrelation

2-week price correlation

twoYearCorrelation

2-year price correlation

symbol

symbol

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

print(finnhub_client.stock_supply_chain('AAPL'))

Sample response

{
  "data": [
    {
      "customer": true,
      "name": "Costco Wholesale Corporation",
      "oneMonthCorrelation": 0.26,
      "oneYearCorrelation": 0.63,
      "sixMonthCorrelation": 0.87,
      "supplier": false,
      "symbol": "COST",
      "threeMonthCorrelation": 0.89,
      "twoWeekCorrelation": 0.35,
      "twoYearCorrelation": 0.91
    },
    {
      "customer": true,
      "name": "Qualcomm",
      "oneMonthCorrelation": 0.06,
      "oneYearCorrelation": 0.58,
      "sixMonthCorrelation": 0.87,
      "supplier": true,
      "symbol": "QCOM",
      "threeMonthCorrelation": 0.88,
      "twoWeekCorrelation": 0.71,
      "twoYearCorrelation": 0.94
    },
    {
      "customer": false,
      "name": "Foxconn Industrial Internet Co., Ltd.",
      "oneMonthCorrelation": 0.25,
      "oneYearCorrelation": -0.48,
      "sixMonthCorrelation": -0.65,
      "supplier": true,
      "symbol": "601138.SS",
      "threeMonthCorrelation": -0.79,
      "twoWeekCorrelation": -0.55,
      "twoYearCorrelation": -0.6
    }
  ],
  "symbol": "AAPL"
}
