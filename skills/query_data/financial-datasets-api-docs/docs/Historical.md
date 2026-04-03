---
id: "url-26e765cb"
type: "website"
title: "Historical"
url: "https://docs.financialdatasets.ai/data-provenance"
description: "Get end-of-day (EOD) historical price data for stocks."
source: ""
tags: []
crawl_time: "2026-03-18T03:13:07.124Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Overview"}
    - {"level":5,"text":"APIs"}
    - {"level":1,"text":"Historical"}
    - {"level":3,"text":"[​](https://docs.financialdatasets.ai/api/prices/historical#overview)Overview"}
    - {"level":3,"text":"[​](https://docs.financialdatasets.ai/api/prices/historical#available-tickers)Available Tickers"}
    - {"level":3,"text":"[​](https://docs.financialdatasets.ai/api/prices/historical#getting-started)Getting Started"}
    - {"level":3,"text":"[​](https://docs.financialdatasets.ai/api/prices/historical#example)Example"}
    - {"level":4,"text":"Authorizations"}
    - {"level":4,"text":"Query Parameters"}
    - {"level":4,"text":"Response"}
  mainContent:
    - {"type":"list","listType":"ul","items":["[Dashboard](https://financialdatasets.ai/)","[Pricing](https://financialdatasets.ai/pricing)","[Discord](https://discord.gg/hTtb8wzgSQ)"]}
    - {"type":"heading","level":5,"content":"Overview"}
    - {"type":"list","listType":"ul","items":["[Introduction](https://docs.financialdatasets.ai/introduction)","[Data Provenance](https://docs.financialdatasets.ai/data-provenance)","[Market Coverage](https://docs.financialdatasets.ai/market-coverage)","[MCP Server](https://docs.financialdatasets.ai/mcp-server)","[Support](https://docs.financialdatasets.ai/support)"]}
    - {"type":"heading","level":5,"content":"APIs"}
    - {"type":"list","listType":"ul","items":["Analyst Estimates[GETAnalyst Estimates](https://docs.financialdatasets.ai/api/analyst-estimates/ticker)","[GETAnalyst Estimates](https://docs.financialdatasets.ai/api/analyst-estimates/ticker)","Company","Earnings[GETEarnings](https://docs.financialdatasets.ai/api/earnings/earnings)[GETPress Releases](https://docs.financialdatasets.ai/api/earnings/press-releases)","[GETEarnings](https://docs.financialdatasets.ai/api/earnings/earnings)","[GETPress Releases](https://docs.financialdatasets.ai/api/earnings/press-releases)","Financial Metrics","Financial Statements[GETIncome Statements](https://docs.financialdatasets.ai/api/financials/income-statements)[GETBalance Sheets](https://docs.financialdatasets.ai/api/financials/balance-sheets)[GETCash Flow Statements](https://docs.financialdatasets.ai/api/financials/cash-flow-statements)[GETAll Financial Statements](https://docs.financialdatasets.ai/api/financials/all-financial-statements)","[GETIncome Statements](https://docs.financialdatasets.ai/api/financials/income-statements)","[GETBalance Sheets](https://docs.financialdatasets.ai/api/financials/balance-sheets)","[GETCash Flow Statements](https://docs.financialdatasets.ai/api/financials/cash-flow-statements)","[GETAll Financial Statements](https://docs.financialdatasets.ai/api/financials/all-financial-statements)","Insider Trades","News[GETCompany News](https://docs.financialdatasets.ai/api/news/company)","[GETCompany News](https://docs.financialdatasets.ai/api/news/company)","Institutional Ownership","Interest Rates[GETHistorical](https://docs.financialdatasets.ai/api/macro/interest-rates/historical)[GETSnapshot](https://docs.financialdatasets.ai/api/macro/interest-rates/snapshot)","[GETHistorical](https://docs.financialdatasets.ai/api/macro/interest-rates/historical)","[GETSnapshot](https://docs.financialdatasets.ai/api/macro/interest-rates/snapshot)","Search","SEC Filings[GETFilings](https://docs.financialdatasets.ai/api/filings/ticker)[GETItems](https://docs.financialdatasets.ai/api/filings/items)","[GETFilings](https://docs.financialdatasets.ai/api/filings/ticker)","[GETItems](https://docs.financialdatasets.ai/api/filings/items)","Segmented Financials","Stock Prices[GETHistorical](https://docs.financialdatasets.ai/api/prices/historical)[GETSnapshot](https://docs.financialdatasets.ai/api/prices/snapshot)","[GETHistorical](https://docs.financialdatasets.ai/api/prices/historical)","[GETSnapshot](https://docs.financialdatasets.ai/api/prices/snapshot)"]}
    - {"type":"codeblock","language":"","content":"curl --request GET \\\n  --url https://api.financialdatasets.ai/prices \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"type":"codeblock","language":"","content":"{\n  \"ticker\": \"<string>\",\n  \"prices\": [\n    {\n      \"open\": 123,\n      \"close\": 123,\n      \"high\": 123,\n      \"low\": 123,\n      \"volume\": 123,\n      \"time\": \"<string>\",\n      \"time_milliseconds\": 123\n    }\n  ]\n}"}
    - {"type":"codeblock","language":"","content":"curl --request GET \\\n  --url https://api.financialdatasets.ai/prices \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"type":"codeblock","language":"","content":"{\n  \"ticker\": \"<string>\",\n  \"prices\": [\n    {\n      \"open\": 123,\n      \"close\": 123,\n      \"high\": 123,\n      \"low\": 123,\n      \"volume\": 123,\n      \"time\": \"<string>\",\n      \"time_milliseconds\": 123\n    }\n  ]\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.financialdatasets.ai/api/prices/historical#overview)Overview"}
    - {"type":"heading","level":3,"content":"[​](https://docs.financialdatasets.ai/api/prices/historical#available-tickers)Available Tickers"}
    - {"type":"heading","level":3,"content":"[​](https://docs.financialdatasets.ai/api/prices/historical#getting-started)Getting Started"}
    - {"type":"list","listType":"ol","items":["Add your API key to the header of the request as `X-API-KEY`.","Add query params like `ticker` to filter the data.","Execute the API request."]}
    - {"type":"heading","level":3,"content":"[​](https://docs.financialdatasets.ai/api/prices/historical#example)Example"}
    - {"type":"codeblock","language":"","content":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\ninterval = 'day'         # possible values are {'day', 'week', 'month', 'year'}\nstart_date = '2025-01-02'\nend_date = '2025-01-05'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/prices/'\n    f'?ticker={ticker}'\n    f'&interval={interval}'\n    f'&start_date={start_date}'\n    f'&end_date={end_date}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse prices from the response\nprices = response.json().get('prices')"}
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"API key for authentication."}
    - {"type":"heading","level":4,"content":"Query Parameters"}
    - {"type":"paragraph","content":"The stock ticker symbol (e.g. AAPL, MSFT)."}
    - {"type":"paragraph","content":"The time interval for the price data."}
    - {"type":"paragraph","content":"The start date for the price data (format: YYYY-MM-DD)."}
    - {"type":"paragraph","content":"The end date for the price data (format: YYYY-MM-DD)."}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Price data response"}
    - {"type":"paragraph","content":"The ticker symbol."}
  paragraphs:
    - "cURL"
    - "Get end-of-day (EOD) historical price data for stocks."
    - "cURL"
    - "API key for authentication."
    - "The stock ticker symbol (e.g. AAPL, MSFT)."
    - "The time interval for the price data."
    - "The start date for the price data (format: YYYY-MM-DD)."
    - "The end date for the price data (format: YYYY-MM-DD)."
    - "Price data response"
    - "The ticker symbol."
    - "Show child attributes"
  lists:
    - {"type":"ul","items":["[Support](https://docs.financialdatasets.ai/support)","[Dashboard](https://financialdatasets.ai/)","[Dashboard](https://financialdatasets.ai/)"]}
    - {"type":"ul","items":["[Dashboard](https://financialdatasets.ai/)","[Pricing](https://financialdatasets.ai/pricing)","[Discord](https://discord.gg/hTtb8wzgSQ)"]}
    - {"type":"ul","items":["[Introduction](https://docs.financialdatasets.ai/introduction)","[Data Provenance](https://docs.financialdatasets.ai/data-provenance)","[Market Coverage](https://docs.financialdatasets.ai/market-coverage)","[MCP Server](https://docs.financialdatasets.ai/mcp-server)","[Support](https://docs.financialdatasets.ai/support)"]}
    - {"type":"ul","items":["Analyst Estimates[GETAnalyst Estimates](https://docs.financialdatasets.ai/api/analyst-estimates/ticker)","[GETAnalyst Estimates](https://docs.financialdatasets.ai/api/analyst-estimates/ticker)","Company","Earnings[GETEarnings](https://docs.financialdatasets.ai/api/earnings/earnings)[GETPress Releases](https://docs.financialdatasets.ai/api/earnings/press-releases)","[GETEarnings](https://docs.financialdatasets.ai/api/earnings/earnings)","[GETPress Releases](https://docs.financialdatasets.ai/api/earnings/press-releases)","Financial Metrics","Financial Statements[GETIncome Statements](https://docs.financialdatasets.ai/api/financials/income-statements)[GETBalance Sheets](https://docs.financialdatasets.ai/api/financials/balance-sheets)[GETCash Flow Statements](https://docs.financialdatasets.ai/api/financials/cash-flow-statements)[GETAll Financial Statements](https://docs.financialdatasets.ai/api/financials/all-financial-statements)","[GETIncome Statements](https://docs.financialdatasets.ai/api/financials/income-statements)","[GETBalance Sheets](https://docs.financialdatasets.ai/api/financials/balance-sheets)","[GETCash Flow Statements](https://docs.financialdatasets.ai/api/financials/cash-flow-statements)","[GETAll Financial Statements](https://docs.financialdatasets.ai/api/financials/all-financial-statements)","Insider Trades","News[GETCompany News](https://docs.financialdatasets.ai/api/news/company)","[GETCompany News](https://docs.financialdatasets.ai/api/news/company)","Institutional Ownership","Interest Rates[GETHistorical](https://docs.financialdatasets.ai/api/macro/interest-rates/historical)[GETSnapshot](https://docs.financialdatasets.ai/api/macro/interest-rates/snapshot)","[GETHistorical](https://docs.financialdatasets.ai/api/macro/interest-rates/historical)","[GETSnapshot](https://docs.financialdatasets.ai/api/macro/interest-rates/snapshot)","Search","SEC Filings[GETFilings](https://docs.financialdatasets.ai/api/filings/ticker)[GETItems](https://docs.financialdatasets.ai/api/filings/items)","[GETFilings](https://docs.financialdatasets.ai/api/filings/ticker)","[GETItems](https://docs.financialdatasets.ai/api/filings/items)","Segmented Financials","Stock Prices[GETHistorical](https://docs.financialdatasets.ai/api/prices/historical)[GETSnapshot](https://docs.financialdatasets.ai/api/prices/snapshot)","[GETHistorical](https://docs.financialdatasets.ai/api/prices/historical)","[GETSnapshot](https://docs.financialdatasets.ai/api/prices/snapshot)"]}
    - {"type":"ul","items":["[GETAnalyst Estimates](https://docs.financialdatasets.ai/api/analyst-estimates/ticker)"]}
    - {"type":"ul","items":["[GETEarnings](https://docs.financialdatasets.ai/api/earnings/earnings)","[GETPress Releases](https://docs.financialdatasets.ai/api/earnings/press-releases)"]}
    - {"type":"ul","items":["[GETIncome Statements](https://docs.financialdatasets.ai/api/financials/income-statements)","[GETBalance Sheets](https://docs.financialdatasets.ai/api/financials/balance-sheets)","[GETCash Flow Statements](https://docs.financialdatasets.ai/api/financials/cash-flow-statements)","[GETAll Financial Statements](https://docs.financialdatasets.ai/api/financials/all-financial-statements)"]}
    - {"type":"ul","items":["[GETCompany News](https://docs.financialdatasets.ai/api/news/company)"]}
    - {"type":"ul","items":["[GETHistorical](https://docs.financialdatasets.ai/api/macro/interest-rates/historical)","[GETSnapshot](https://docs.financialdatasets.ai/api/macro/interest-rates/snapshot)"]}
    - {"type":"ul","items":["[GETFilings](https://docs.financialdatasets.ai/api/filings/ticker)","[GETItems](https://docs.financialdatasets.ai/api/filings/items)"]}
    - {"type":"ul","items":["[GETHistorical](https://docs.financialdatasets.ai/api/prices/historical)","[GETSnapshot](https://docs.financialdatasets.ai/api/prices/snapshot)"]}
    - {"type":"ol","items":["Add your API key to the header of the request as X-API-KEY.","Add query params like ticker to filter the data.","Execute the API request."]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/prices \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"text","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/prices \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"json","code":"{\n  \"ticker\": \"<string>\",\n  \"prices\": [\n    {\n      \"open\": 123,\n      \"close\": 123,\n      \"high\": 123,\n      \"low\": 123,\n      \"volume\": 123,\n      \"time\": \"<string>\",\n      \"time_milliseconds\": 123\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"ticker\": \"<string>\",\n  \"prices\": [\n    {\n      \"open\": 123,\n      \"close\": 123,\n      \"high\": 123,\n      \"low\": 123,\n      \"volume\": 123,\n      \"time\": \"<string>\",\n      \"time_milliseconds\": 123\n    }\n  ]\n}"}
    - {"language":"text","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/prices \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"text","code":"curl --request GET \\\n  --url https://api.financialdatasets.ai/prices \\\n  --header 'X-API-KEY: <api-key>'"}
    - {"language":"json","code":"{\n  \"ticker\": \"<string>\",\n  \"prices\": [\n    {\n      \"open\": 123,\n      \"close\": 123,\n      \"high\": 123,\n      \"low\": 123,\n      \"volume\": 123,\n      \"time\": \"<string>\",\n      \"time_milliseconds\": 123\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"ticker\": \"<string>\",\n  \"prices\": [\n    {\n      \"open\": 123,\n      \"close\": 123,\n      \"high\": 123,\n      \"low\": 123,\n      \"volume\": 123,\n      \"time\": \"<string>\",\n      \"time_milliseconds\": 123\n    }\n  ]\n}"}
    - {"language":"text","code":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\ninterval = 'day'         # possible values are {'day', 'week', 'month', 'year'}\nstart_date = '2025-01-02'\nend_date = '2025-01-05'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/prices/'\n    f'?ticker={ticker}'\n    f'&interval={interval}'\n    f'&start_date={start_date}'\n    f'&end_date={end_date}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse prices from the response\nprices = response.json().get('prices')"}
    - {"language":"text","code":"import requests\n\n# add your API key to the headers\nheaders = {\n    \"X-API-KEY\": \"your_api_key_here\"\n}\n\n# set your query params\nticker = 'AAPL'\ninterval = 'day'         # possible values are {'day', 'week', 'month', 'year'}\nstart_date = '2025-01-02'\nend_date = '2025-01-05'\n\n# create the URL\nurl = (\n    f'https://api.financialdatasets.ai/prices/'\n    f'?ticker={ticker}'\n    f'&interval={interval}'\n    f'&start_date={start_date}'\n    f'&end_date={end_date}'\n)\n\n# make API request\nresponse = requests.get(url, headers=headers)\n\n# parse prices from the response\nprices = response.json().get('prices')"}
  images:
    - {"src":"https://mintcdn.com/financialdatasets/3kIYTNCZBSs0PnUp/logo/light.svg?fit=max&auto=format&n=3kIYTNCZBSs0PnUp&q=85&s=4d1772285e38eaeb683f3a7c060b9407","localPath":"Data_Provenance_-_Financial_Datasets/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/financialdatasets/3kIYTNCZBSs0PnUp/logo/dark.svg?fit=max&auto=format&n=3kIYTNCZBSs0PnUp&q=85&s=85554fb59fca23bbcd8e3893beff9b5c","localPath":"Data_Provenance_-_Financial_Datasets/image_2.svg","alt":"dark logo","title":""}
  charts:
    - {"type":"svg","index":1,"filename":"Data_Provenance_-_Financial_Datasets/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":3,"filename":"Data_Provenance_-_Financial_Datasets/svg_3.png","width":16,"height":16}
    - {"type":"svg","index":9,"filename":"Data_Provenance_-_Financial_Datasets/svg_9.png","width":16,"height":16}
    - {"type":"svg","index":10,"filename":"Data_Provenance_-_Financial_Datasets/svg_10.png","width":16,"height":16}
    - {"type":"svg","index":11,"filename":"Data_Provenance_-_Financial_Datasets/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Data_Provenance_-_Financial_Datasets/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Data_Provenance_-_Financial_Datasets/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Data_Provenance_-_Financial_Datasets/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Data_Provenance_-_Financial_Datasets/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Data_Provenance_-_Financial_Datasets/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Data_Provenance_-_Financial_Datasets/svg_17.png","width":16,"height":16}
    - {"type":"svg","index":19,"filename":"Data_Provenance_-_Financial_Datasets/svg_19.png","width":16,"height":16}
    - {"type":"svg","index":21,"filename":"Data_Provenance_-_Financial_Datasets/svg_21.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Data_Provenance_-_Financial_Datasets/svg_23.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Data_Provenance_-_Financial_Datasets/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Data_Provenance_-_Financial_Datasets/svg_27.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Data_Provenance_-_Financial_Datasets/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":31,"filename":"Data_Provenance_-_Financial_Datasets/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"Data_Provenance_-_Financial_Datasets/svg_33.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Data_Provenance_-_Financial_Datasets/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"Data_Provenance_-_Financial_Datasets/svg_37.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"Data_Provenance_-_Financial_Datasets/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"Data_Provenance_-_Financial_Datasets/svg_41.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"Data_Provenance_-_Financial_Datasets/svg_43.png","width":14,"height":14}
    - {"type":"svg","index":44,"filename":"Data_Provenance_-_Financial_Datasets/svg_44.png","width":14,"height":14}
    - {"type":"svg","index":45,"filename":"Data_Provenance_-_Financial_Datasets/svg_45.png","width":16,"height":16}
    - {"type":"svg","index":46,"filename":"Data_Provenance_-_Financial_Datasets/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":48,"filename":"Data_Provenance_-_Financial_Datasets/svg_48.png","width":12,"height":12}
    - {"type":"svg","index":53,"filename":"Data_Provenance_-_Financial_Datasets/svg_53.png","width":14,"height":12}
    - {"type":"svg","index":54,"filename":"Data_Provenance_-_Financial_Datasets/svg_54.png","width":14,"height":12}
    - {"type":"svg","index":55,"filename":"Data_Provenance_-_Financial_Datasets/svg_55.png","width":14,"height":12}
    - {"type":"svg","index":56,"filename":"Data_Provenance_-_Financial_Datasets/svg_56.png","width":14,"height":12}
    - {"type":"svg","index":57,"filename":"Data_Provenance_-_Financial_Datasets/svg_57.png","width":16,"height":16}
    - {"type":"svg","index":58,"filename":"Data_Provenance_-_Financial_Datasets/svg_58.png","width":18,"height":18}
    - {"type":"svg","index":59,"filename":"Data_Provenance_-_Financial_Datasets/svg_59.png","width":18,"height":18}
    - {"type":"svg","index":60,"filename":"Data_Provenance_-_Financial_Datasets/svg_60.png","width":18,"height":18}
    - {"type":"svg","index":61,"filename":"Data_Provenance_-_Financial_Datasets/svg_61.png","width":18,"height":18}
    - {"type":"svg","index":62,"filename":"Data_Provenance_-_Financial_Datasets/svg_62.png","width":18,"height":18}
    - {"type":"svg","index":63,"filename":"Data_Provenance_-_Financial_Datasets/svg_63.png","width":10,"height":10}
    - {"type":"svg","index":64,"filename":"Data_Provenance_-_Financial_Datasets/svg_64.png","width":18,"height":18}
    - {"type":"svg","index":65,"filename":"Data_Provenance_-_Financial_Datasets/svg_65.png","width":18,"height":18}
    - {"type":"svg","index":66,"filename":"Data_Provenance_-_Financial_Datasets/svg_66.png","width":10,"height":10}
    - {"type":"svg","index":70,"filename":"Data_Provenance_-_Financial_Datasets/svg_70.png","width":20,"height":20}
    - {"type":"svg","index":71,"filename":"Data_Provenance_-_Financial_Datasets/svg_71.png","width":20,"height":20}
    - {"type":"svg","index":72,"filename":"Data_Provenance_-_Financial_Datasets/svg_72.png","width":49,"height":14}
  chartData: []
  blockquotes: []
  definitionLists: []
  horizontalRules: 0
  videos: []
  audios: []
  apiData: 0
  pageFeatures:
    suggestedType: "api-doc"
    confidence: 75
    signals:
      - "article-like"
      - "api-doc-like"
      - "api-endpoints"
  tabsAndDropdowns: []
  dateFilters: []
---

# Historical

## 源URL

https://docs.financialdatasets.ai/data-provenance

## 描述

Get end-of-day (EOD) historical price data for stocks.

## 内容

- [Dashboard](https://financialdatasets.ai/)
- [Pricing](https://financialdatasets.ai/pricing)
- [Discord](https://discord.gg/hTtb8wzgSQ)

###### Overview

- [Introduction](https://docs.financialdatasets.ai/introduction)
- [Data Provenance](https://docs.financialdatasets.ai/data-provenance)
- [Market Coverage](https://docs.financialdatasets.ai/market-coverage)
- [MCP Server](https://docs.financialdatasets.ai/mcp-server)
- [Support](https://docs.financialdatasets.ai/support)

###### APIs

- Analyst Estimates[GETAnalyst Estimates](https://docs.financialdatasets.ai/api/analyst-estimates/ticker)
- [GETAnalyst Estimates](https://docs.financialdatasets.ai/api/analyst-estimates/ticker)
- Company
- Earnings[GETEarnings](https://docs.financialdatasets.ai/api/earnings/earnings)[GETPress Releases](https://docs.financialdatasets.ai/api/earnings/press-releases)
- [GETEarnings](https://docs.financialdatasets.ai/api/earnings/earnings)
- [GETPress Releases](https://docs.financialdatasets.ai/api/earnings/press-releases)
- Financial Metrics
- Financial Statements[GETIncome Statements](https://docs.financialdatasets.ai/api/financials/income-statements)[GETBalance Sheets](https://docs.financialdatasets.ai/api/financials/balance-sheets)[GETCash Flow Statements](https://docs.financialdatasets.ai/api/financials/cash-flow-statements)[GETAll Financial Statements](https://docs.financialdatasets.ai/api/financials/all-financial-statements)
- [GETIncome Statements](https://docs.financialdatasets.ai/api/financials/income-statements)
- [GETBalance Sheets](https://docs.financialdatasets.ai/api/financials/balance-sheets)
- [GETCash Flow Statements](https://docs.financialdatasets.ai/api/financials/cash-flow-statements)
- [GETAll Financial Statements](https://docs.financialdatasets.ai/api/financials/all-financial-statements)
- Insider Trades
- News[GETCompany News](https://docs.financialdatasets.ai/api/news/company)
- [GETCompany News](https://docs.financialdatasets.ai/api/news/company)
- Institutional Ownership
- Interest Rates[GETHistorical](https://docs.financialdatasets.ai/api/macro/interest-rates/historical)[GETSnapshot](https://docs.financialdatasets.ai/api/macro/interest-rates/snapshot)
- [GETHistorical](https://docs.financialdatasets.ai/api/macro/interest-rates/historical)
- [GETSnapshot](https://docs.financialdatasets.ai/api/macro/interest-rates/snapshot)
- Search
- SEC Filings[GETFilings](https://docs.financialdatasets.ai/api/filings/ticker)[GETItems](https://docs.financialdatasets.ai/api/filings/items)
- [GETFilings](https://docs.financialdatasets.ai/api/filings/ticker)
- [GETItems](https://docs.financialdatasets.ai/api/filings/items)
- Segmented Financials
- Stock Prices[GETHistorical](https://docs.financialdatasets.ai/api/prices/historical)[GETSnapshot](https://docs.financialdatasets.ai/api/prices/snapshot)
- [GETHistorical](https://docs.financialdatasets.ai/api/prices/historical)
- [GETSnapshot](https://docs.financialdatasets.ai/api/prices/snapshot)

```text
curl --request GET \
  --url https://api.financialdatasets.ai/prices \
  --header 'X-API-KEY: <api-key>'
```

```text
{
  "ticker": "<string>",
  "prices": [
    {
      "open": 123,
      "close": 123,
      "high": 123,
      "low": 123,
      "volume": 123,
      "time": "<string>",
      "time_milliseconds": 123
    }
  ]
}
```

```text
curl --request GET \
  --url https://api.financialdatasets.ai/prices \
  --header 'X-API-KEY: <api-key>'
```

```text
{
  "ticker": "<string>",
  "prices": [
    {
      "open": 123,
      "close": 123,
      "high": 123,
      "low": 123,
      "volume": 123,
      "time": "<string>",
      "time_milliseconds": 123
    }
  ]
}
```

#### Overview

#### Available Tickers

#### Getting Started

1. Add your API key to the header of the request as `X-API-KEY`.
2. Add query params like `ticker` to filter the data.
3. Execute the API request.

#### Example

```text
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'AAPL'
interval = 'day'         # possible values are {'day', 'week', 'month', 'year'}
start_date = '2025-01-02'
end_date = '2025-01-05'

# create the URL
url = (
    f'https://api.financialdatasets.ai/prices/'
    f'?ticker={ticker}'
    f'&interval={interval}'
    f'&start_date={start_date}'
    f'&end_date={end_date}'
)

# make API request
response = requests.get(url, headers=headers)

# parse prices from the response
prices = response.json().get('prices')
```

##### Authorizations

API key for authentication.

##### Query Parameters

The stock ticker symbol (e.g. AAPL, MSFT).

The time interval for the price data.

The start date for the price data (format: YYYY-MM-DD).

The end date for the price data (format: YYYY-MM-DD).

##### Response

Price data response

The ticker symbol.

## 图片

![light logo](Data_Provenance_-_Financial_Datasets/image_1.svg)

![dark logo](Data_Provenance_-_Financial_Datasets/image_2.svg)

## 图表

![SVG图表 1](Data_Provenance_-_Financial_Datasets/svg_1.png)
*尺寸: 16x16px*

![SVG图表 3](Data_Provenance_-_Financial_Datasets/svg_3.png)
*尺寸: 16x16px*

![SVG图表 9](Data_Provenance_-_Financial_Datasets/svg_9.png)
*尺寸: 16x16px*

![SVG图表 10](Data_Provenance_-_Financial_Datasets/svg_10.png)
*尺寸: 16x16px*

![SVG图表 11](Data_Provenance_-_Financial_Datasets/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Data_Provenance_-_Financial_Datasets/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Data_Provenance_-_Financial_Datasets/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Data_Provenance_-_Financial_Datasets/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Data_Provenance_-_Financial_Datasets/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Data_Provenance_-_Financial_Datasets/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Data_Provenance_-_Financial_Datasets/svg_17.png)
*尺寸: 16x16px*

![SVG图表 19](Data_Provenance_-_Financial_Datasets/svg_19.png)
*尺寸: 16x16px*

![SVG图表 21](Data_Provenance_-_Financial_Datasets/svg_21.png)
*尺寸: 16x16px*

![SVG图表 23](Data_Provenance_-_Financial_Datasets/svg_23.png)
*尺寸: 16x16px*

![SVG图表 25](Data_Provenance_-_Financial_Datasets/svg_25.png)
*尺寸: 16x16px*

![SVG图表 27](Data_Provenance_-_Financial_Datasets/svg_27.png)
*尺寸: 16x16px*

![SVG图表 29](Data_Provenance_-_Financial_Datasets/svg_29.png)
*尺寸: 16x16px*

![SVG图表 31](Data_Provenance_-_Financial_Datasets/svg_31.png)
*尺寸: 16x16px*

![SVG图表 33](Data_Provenance_-_Financial_Datasets/svg_33.png)
*尺寸: 16x16px*

![SVG图表 35](Data_Provenance_-_Financial_Datasets/svg_35.png)
*尺寸: 16x16px*

![SVG图表 37](Data_Provenance_-_Financial_Datasets/svg_37.png)
*尺寸: 16x16px*

![SVG图表 39](Data_Provenance_-_Financial_Datasets/svg_39.png)
*尺寸: 16x16px*

![SVG图表 41](Data_Provenance_-_Financial_Datasets/svg_41.png)
*尺寸: 16x16px*

![SVG图表 43](Data_Provenance_-_Financial_Datasets/svg_43.png)
*尺寸: 14x14px*

![SVG图表 44](Data_Provenance_-_Financial_Datasets/svg_44.png)
*尺寸: 14x14px*

![SVG图表 45](Data_Provenance_-_Financial_Datasets/svg_45.png)
*尺寸: 16x16px*

![SVG图表 46](Data_Provenance_-_Financial_Datasets/svg_46.png)
*尺寸: 16x16px*

![SVG图表 48](Data_Provenance_-_Financial_Datasets/svg_48.png)
*尺寸: 12x12px*

![SVG图表 53](Data_Provenance_-_Financial_Datasets/svg_53.png)
*尺寸: 14x12px*

![SVG图表 54](Data_Provenance_-_Financial_Datasets/svg_54.png)
*尺寸: 14x12px*

![SVG图表 55](Data_Provenance_-_Financial_Datasets/svg_55.png)
*尺寸: 14x12px*

![SVG图表 56](Data_Provenance_-_Financial_Datasets/svg_56.png)
*尺寸: 14x12px*

![SVG图表 57](Data_Provenance_-_Financial_Datasets/svg_57.png)
*尺寸: 16x16px*

![SVG图表 58](Data_Provenance_-_Financial_Datasets/svg_58.png)
*尺寸: 18x18px*

![SVG图表 59](Data_Provenance_-_Financial_Datasets/svg_59.png)
*尺寸: 18x18px*

![SVG图表 60](Data_Provenance_-_Financial_Datasets/svg_60.png)
*尺寸: 18x18px*

![SVG图表 61](Data_Provenance_-_Financial_Datasets/svg_61.png)
*尺寸: 18x18px*

![SVG图表 62](Data_Provenance_-_Financial_Datasets/svg_62.png)
*尺寸: 18x18px*

![SVG图表 63](Data_Provenance_-_Financial_Datasets/svg_63.png)
*尺寸: 10x10px*

![SVG图表 64](Data_Provenance_-_Financial_Datasets/svg_64.png)
*尺寸: 18x18px*

![SVG图表 65](Data_Provenance_-_Financial_Datasets/svg_65.png)
*尺寸: 18x18px*

![SVG图表 66](Data_Provenance_-_Financial_Datasets/svg_66.png)
*尺寸: 10x10px*

![SVG图表 70](Data_Provenance_-_Financial_Datasets/svg_70.png)
*尺寸: 20x20px*

![SVG图表 71](Data_Provenance_-_Financial_Datasets/svg_71.png)
*尺寸: 20x20px*

![SVG图表 72](Data_Provenance_-_Financial_Datasets/svg_72.png)
*尺寸: 49x14px*
