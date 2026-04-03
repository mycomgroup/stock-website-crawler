---
id: "url-7a64ad03"
type: "api"
title: "Investment Themes (Thematic Investing) Premium"
url: "https://finnhub.io/docs/api/investment-themes-thematic-investing"
description: "Thematic investing involves creating a portfolio (or portion of a portfolio) by gathering together a collection of companies involved in certain areas that you predict will generate above-market returns over the long term. Themes can be based on a concept such as ageing populations or a sub-sector such as robotics, and drones. Thematic investing focuses on predicted long-term trends rather than specific companies or sectors, enabling investors to access structural, one-off shifts that can change an entire industry. This endpoint will help you get portfolios of different investment themes that are changing our life and are the way of the future. A full list of themes supported can be found here. The theme coverage and portfolios are updated bi-weekly by our analysts. Our approach excludes penny, super-small cap and illiquid stocks. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T11:22:11.547Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/investment-theme?theme=financialExchangesData"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Investment Themes (Thematic Investing) Premium\n\nThematic investing involves creating a portfolio (or portion of a portfolio) by gathering together a collection of companies involved in certain areas that you predict will generate above-market returns over the long term. Themes can be based on a concept such as ageing populations or a sub-sector such as robotics, and drones. Thematic investing focuses on predicted long-term trends rather than specific companies or sectors, enabling investors to access structural, one-off shifts that can change an entire industry.\n\nThis endpoint will help you get portfolios of different investment themes that are changing our life and are the way of the future.\n\nA full list of themes supported can be found here. The theme coverage and portfolios are updated bi-weekly by our analysts. Our approach excludes penny, super-small cap and illiquid stocks.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/investment-theme?theme=financialExchangesData\n\n/stock/investment-theme?theme=futureFood\n\nArguments:\n\nthemeREQUIRED\n\nInvestment theme. A full list of themes supported can be found here.\n\nResponse Attributes:\n\ndata\n\nInvestment theme portfolio.\n\nsymbol\n\nSymbol\n\ntheme\n\nInvestment theme\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_investment_theme('financialExchangesData'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"symbol\": \"ICE\"\n    },\n    {\n      \"symbol\": \"NDAQ\"\n    },\n    {\n      \"symbol\": \"CBOE\"\n    },\n    {\n      \"symbol\": \"FDS\"\n    },\n    {\n      \"symbol\": \"SPGI\"\n    },\n    {\n      \"symbol\": \"TW\"\n    }\n  ],\n  \"theme\": \"financialExchangesData\"\n}"
  suggestedFilename: "investment-themes-thematic-investing"
---

# Investment Themes (Thematic Investing) Premium

## 源URL

https://finnhub.io/docs/api/investment-themes-thematic-investing

## 描述

Thematic investing involves creating a portfolio (or portion of a portfolio) by gathering together a collection of companies involved in certain areas that you predict will generate above-market returns over the long term. Themes can be based on a concept such as ageing populations or a sub-sector such as robotics, and drones. Thematic investing focuses on predicted long-term trends rather than specific companies or sectors, enabling investors to access structural, one-off shifts that can change an entire industry. This endpoint will help you get portfolios of different investment themes that are changing our life and are the way of the future. A full list of themes supported can be found here. The theme coverage and portfolios are updated bi-weekly by our analysts. Our approach excludes penny, super-small cap and illiquid stocks. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/investment-theme?theme=financialExchangesData`

## 文档正文

Thematic investing involves creating a portfolio (or portion of a portfolio) by gathering together a collection of companies involved in certain areas that you predict will generate above-market returns over the long term. Themes can be based on a concept such as ageing populations or a sub-sector such as robotics, and drones. Thematic investing focuses on predicted long-term trends rather than specific companies or sectors, enabling investors to access structural, one-off shifts that can change an entire industry. This endpoint will help you get portfolios of different investment themes that are changing our life and are the way of the future. A full list of themes supported can be found here. The theme coverage and portfolios are updated bi-weekly by our analysts. Our approach excludes penny, super-small cap and illiquid stocks. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/investment-theme?theme=financialExchangesData`

Investment Themes (Thematic Investing) Premium

Thematic investing involves creating a portfolio (or portion of a portfolio) by gathering together a collection of companies involved in certain areas that you predict will generate above-market returns over the long term. Themes can be based on a concept such as ageing populations or a sub-sector such as robotics, and drones. Thematic investing focuses on predicted long-term trends rather than specific companies or sectors, enabling investors to access structural, one-off shifts that can change an entire industry.

This endpoint will help you get portfolios of different investment themes that are changing our life and are the way of the future.

A full list of themes supported can be found here. The theme coverage and portfolios are updated bi-weekly by our analysts. Our approach excludes penny, super-small cap and illiquid stocks.

Method: GET

Premium: Premium Access Required

Examples:

/stock/investment-theme?theme=financialExchangesData

/stock/investment-theme?theme=futureFood

Arguments:

themeREQUIRED

Investment theme. A full list of themes supported can be found here.

Response Attributes:

data

Investment theme portfolio.

symbol

Symbol

theme

Investment theme

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

print(finnhub_client.stock_investment_theme('financialExchangesData'))

Sample response

{
  "data": [
    {
      "symbol": "ICE"
    },
    {
      "symbol": "NDAQ"
    },
    {
      "symbol": "CBOE"
    },
    {
      "symbol": "FDS"
    },
    {
      "symbol": "SPGI"
    },
    {
      "symbol": "TW"
    }
  ],
  "theme": "financialExchangesData"
}
