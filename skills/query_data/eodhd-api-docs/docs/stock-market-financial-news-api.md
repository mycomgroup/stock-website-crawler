---
id: "url-61ae31b2"
type: "api"
title: "Financial News Feed and Stock News Sentiment data API"
url: "https://eodhd.com/financial-apis/stock-market-financial-news-api/"
description: "Add our financial news aggregation and in-house sentiment analysis to your project with just one line of code. Our system continuously analyzes the most crucial financial news portals, providing you with access to constantly updated news data and generating daily sentiment scores for stocks, ETFs, Forex, and Cryptocurrencies based on positive and negative mentions."
source: ""
tags: []
crawl_time: "2026-03-18T06:17:33.694Z"
metadata:
  endpoint: "https://eodhd.com/api/news"
  parameters:
    - {"name":"s","description":"Yes"}
    - {"name":"filter[date_from]","description":"No"}
    - {"name":"filter[date_to]","description":"No"}
    - {"name":"page[limit]","description":"No"}
    - {"name":"api_token","description":"Yes"}
  markdownContent: "# Financial News Feed and Stock News Sentiment data API\n\nAdd our financial news aggregation and in-house sentiment analysis to your project with just one line of code. Our system continuously analyzes the most crucial financial news portals, providing you with access to constantly updated news data and generating daily sentiment scores for stocks, ETFs, Forex, and Cryptocurrencies based on positive and negative mentions.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/news?s=AAPL.US&offset=0&limit=10&api_token=your_api_token&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/sentiments?s=btc-usd.cc,aapl.us&from=2022-01-01&to=2022-04-22&api_token=your_api_token&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/news-word-weights?s=AAPL&filter[date_from]=2025-04-08&filter[to]=2025-04-16&page[limit]=10&api_token=your_api_token&fmt=json\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| s | Yes |\n| filter[date_from] | No |\n| filter[date_to] | No |\n| page[limit] | No |\n| api_token | Yes |\n\n\n## Description:\n\nThe Financial News API returns the latest financial news headlines and full articles for a given ticker symbol or topic tag. You must provide either a “s “ (ticker) or a “t” (tag) – at least one is required.\n\nThis API supports filtering by date, pagination, and returning results in JSON.\n\n## Output Format (JSON):\n\nEach article includes:\n\n## Tags in Financial News:\n\nIn addition to the standard list of 50 tags, we have introduced AI-powered auto-detected tags. This enhancement makes your search more flexible – now you can use any tags related to your topic of interest.\n\n‘balance sheet’, ‘capital employed’, ‘class action’, ‘company announcement’, ‘consensus eps estimate’, ‘consensus estimate’, ‘credit rating’, ‘discounted cash flow’, ‘dividend payments’, ‘earnings estimate’, ‘earnings growth’, ‘earnings per share’, ‘earnings release’, ‘earnings report’, ‘earnings results’, ‘earnings surprise’, ‘estimate revisions’, ‘european regulatory news’, ‘financial results’, ‘fourth quarter’, ‘free cash flow’, ‘future cash flows’, ‘growth rate’, ‘initial public offering’, ‘insider ownership’, ‘insider transactions’, ‘institutional investors’, ‘institutional ownership’, ‘intrinsic value’, ‘market research reports’, ‘net income’, ‘operating income’, ‘present value’, ‘press releases’, ‘price target’, ‘quarterly earnings’, ‘quarterly results’, ‘ratings’, ‘research analysis and reports’, ‘return on equity’, ‘revenue estimates’, ‘revenue growth’, ‘roce’, ‘roe’, ‘share price’, ‘shareholder rights’, ‘shareholder’, ‘shares outstanding’, ‘split’, ‘strong buy’, ‘total revenue’, ‘zacks investment research’, ‘zacks rank’\n\nExamples of new tags:\n\n‘GROWTH RATE’,’TOBACCO’, ‘MERGERS AND ACQUISITIONS’, ‘CATERING’, ‘ARTIFICIAL INTELLIGENCE’, ‘AGRITECH’, etc.\n\n## Description:\n\nGet sentiment scores for one or more financial instruments (stocks, ETFs, crypto). Sentiment scores are calculated from both news and social media, normalized on a scale from -1 (very negative) to 1 (very positive).\n\nYou can provide one or multiple tickers, separated by commas.\n\n## Output Format (JSON):\n\nSentiment data is grouped by ticker symbol. Each entry includes:\n\n## Description:\n\nThis API provides a weighted list of the most relevant words found in financial news articles about a specific stock ticker over a defined date range.\n\nEach word is scored based on its frequency and significance across the processed news, allowing for trend analysis, NLP input, or thematic clustering.\n\nNote: This endpoint leverages AI to process hundreds or even thousands of articles, which may result in longer response times. If you encounter a timeout, consider adjusting your filters (e.g., narrowing the date range or focusing on specific tickers) to reduce the volume of data being processed.\n\n## Output Description (JSON Format):\n\nThe API returns a list of weighted words (terms) relevant to the ticker during the selected period, along with metadata about the processed news.\n\n## Code Examples\n\n```text\nGET https://eodhd.com/api/news\n```\n\n```text\n\"date\": \"2025-08-18T08:48:00+00:00\",\n\"title\": \"Kenya Healthcare Statistics Databook 2025: Navigate Healthcare Planning with Over 300 KPIs Spanning Patient to Pharmacist Statistics\",\n\"content\": \"Dublin, Aug.  18, 2025  (GLOBE NEWSWIRE) -- The \\\"Kenya Healthcare Statistics Databook Q2 2025: 300+ KPIs Covering Detailed Statistics on Patients, Healthcare Facilities, Public and Private Spending, Medical Staff\\\" report has been added to  ResearchAndMarkets.com's offering.This comprehensive report on Kenya's healthcare sector offers a range of statistics covering the entire value chain an in-depth data-centric analysis of the entire healthcare ecosystem, covering a range of modules from demographic data to healthcare .....\",\n\"link\": \"https://www.globenewswire.com/news-release/2025/08/18/3134815/28124/en/Kenya-Healthcare-Statistics-Databook-2025-Navigate-Healthcare-Planning-with-Over-300-KPIs-Spanning-Patient-to-Pharmacist-Statistics.html\",\n\"symbols\": [\n\"AAPL.US\"\n],\n\"tags\": [\n\"DEMOGRAPHICS\",\n\"GLOBAL\",\n\"GROSS DOMESTIC PRODUCT\",\n\"HEALTH PROFESSIONAL\",\n\"HEALTHCARE ANALYTICS\",\n\"HEALTHCARE INFRASTRUCTURE\",\n\"HEALTHCARE LANDSCAPE\",\n\"HEALTHCARE RESOURCES\",\n\"HEALTHCARE SECTOR\",\n\"HEALTHCARE SPENDING\",\n\"HEALTHCARE STATISTICS\",\n\"KENYA\",\n\"MARKET OPPORTUNITIES\",\n\"MARKET RESEARCH REPORTS\",\n\"MEDICAL STAFF\",\n\"MEDICAL STAFFING\",\n\"PHARMACEUTICAL DISTRIBUTION\",\n\"PHARMACIES\",\n\"POPULATION TRENDS\"\n],\n\"sentiment\": {\n\"polarity\": 0.959,\n\"neg\": 0.008,\n\"neu\": 0.948,\n\"pos\": 0.044\n}\n.......\n```\n\n```text\nGET https://eodhd.com/api/sentiments\n```\n\n```text\n\"BTC-USD.CC\": [\n{\n\"date\": \"2022-04-22\",\n\"count\": 31,\n\"normalized\": 0.1835\n},\n{\n\"date\": \"2022-04-21\",\n\"count\": 41,\n\"normalized\": 0.2555\n},\n{\n\"date\": \"2022-04-20\",\n\"count\": 34,\n\"normalized\": 0.2068\n},\n{\n\"date\": \"2022-04-19\",\n\"count\": 35,\n\"normalized\": 0.4781\n},\n{\n\"date\": \"2022-04-18\",\n\"count\": 29,\n\"normalized\": 0.1618\n},\n{\n\"date\": \"2022-04-17\",\n\"count\": 12,\n\"normalized\": 0.0056\n```\n\n```text\nGET https://eodhd.com/api/news-word-weights\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "stock-market-financial-news-api"
---

# Financial News Feed and Stock News Sentiment data API

## 源URL

https://eodhd.com/financial-apis/stock-market-financial-news-api/

## 描述

Add our financial news aggregation and in-house sentiment analysis to your project with just one line of code. Our system continuously analyzes the most crucial financial news portals, providing you with access to constantly updated news data and generating daily sentiment scores for stocks, ETFs, Forex, and Cryptocurrencies based on positive and negative mentions.

## API 端点

**Endpoint**: `https://eodhd.com/api/news`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `s` | - | 否 | - | Yes |
| `filter[date_from]` | - | 否 | - | No |
| `filter[date_to]` | - | 否 | - | No |
| `page[limit]` | - | 否 | - | No |
| `api_token` | - | 否 | - | Yes |

## 文档正文

Add our financial news aggregation and in-house sentiment analysis to your project with just one line of code. Our system continuously analyzes the most crucial financial news portals, providing you with access to constantly updated news data and generating daily sentiment scores for stocks, ETFs, Forex, and Cryptocurrencies based on positive and negative mentions.

## API Endpoint

```text
https://eodhd.com/api/news?s=AAPL.US&offset=0&limit=10&api_token=your_api_token&fmt=json
```

```text
https://eodhd.com/api/sentiments?s=btc-usd.cc,aapl.us&from=2022-01-01&to=2022-04-22&api_token=your_api_token&fmt=json
```

```text
https://eodhd.com/api/news-word-weights?s=AAPL&filter[date_from]=2025-04-08&filter[to]=2025-04-16&page[limit]=10&api_token=your_api_token&fmt=json
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| s | Yes |
| filter[date_from] | No |
| filter[date_to] | No |
| page[limit] | No |
| api_token | Yes |

## Description:

The Financial News API returns the latest financial news headlines and full articles for a given ticker symbol or topic tag. You must provide either a “s “ (ticker) or a “t” (tag) – at least one is required.

This API supports filtering by date, pagination, and returning results in JSON.

## Output Format (JSON):

Each article includes:

## Tags in Financial News:

In addition to the standard list of 50 tags, we have introduced AI-powered auto-detected tags. This enhancement makes your search more flexible – now you can use any tags related to your topic of interest.

‘balance sheet’, ‘capital employed’, ‘class action’, ‘company announcement’, ‘consensus eps estimate’, ‘consensus estimate’, ‘credit rating’, ‘discounted cash flow’, ‘dividend payments’, ‘earnings estimate’, ‘earnings growth’, ‘earnings per share’, ‘earnings release’, ‘earnings report’, ‘earnings results’, ‘earnings surprise’, ‘estimate revisions’, ‘european regulatory news’, ‘financial results’, ‘fourth quarter’, ‘free cash flow’, ‘future cash flows’, ‘growth rate’, ‘initial public offering’, ‘insider ownership’, ‘insider transactions’, ‘institutional investors’, ‘institutional ownership’, ‘intrinsic value’, ‘market research reports’, ‘net income’, ‘operating income’, ‘present value’, ‘press releases’, ‘price target’, ‘quarterly earnings’, ‘quarterly results’, ‘ratings’, ‘research analysis and reports’, ‘return on equity’, ‘revenue estimates’, ‘revenue growth’, ‘roce’, ‘roe’, ‘share price’, ‘shareholder rights’, ‘shareholder’, ‘shares outstanding’, ‘split’, ‘strong buy’, ‘total revenue’, ‘zacks investment research’, ‘zacks rank’

Examples of new tags:

‘GROWTH RATE’,’TOBACCO’, ‘MERGERS AND ACQUISITIONS’, ‘CATERING’, ‘ARTIFICIAL INTELLIGENCE’, ‘AGRITECH’, etc.

## Description:

Get sentiment scores for one or more financial instruments (stocks, ETFs, crypto). Sentiment scores are calculated from both news and social media, normalized on a scale from -1 (very negative) to 1 (very positive).

You can provide one or multiple tickers, separated by commas.

## Output Format (JSON):

Sentiment data is grouped by ticker symbol. Each entry includes:

## Description:

This API provides a weighted list of the most relevant words found in financial news articles about a specific stock ticker over a defined date range.

Each word is scored based on its frequency and significance across the processed news, allowing for trend analysis, NLP input, or thematic clustering.

Note: This endpoint leverages AI to process hundreds or even thousands of articles, which may result in longer response times. If you encounter a timeout, consider adjusting your filters (e.g., narrowing the date range or focusing on specific tickers) to reduce the volume of data being processed.

## Output Description (JSON Format):

The API returns a list of weighted words (terms) relevant to the ticker during the selected period, along with metadata about the processed news.

## Code Examples

```text
GET https://eodhd.com/api/news
```

```text
"date": "2025-08-18T08:48:00+00:00",
"title": "Kenya Healthcare Statistics Databook 2025: Navigate Healthcare Planning with Over 300 KPIs Spanning Patient to Pharmacist Statistics",
"content": "Dublin, Aug.  18, 2025  (GLOBE NEWSWIRE) -- The \"Kenya Healthcare Statistics Databook Q2 2025: 300+ KPIs Covering Detailed Statistics on Patients, Healthcare Facilities, Public and Private Spending, Medical Staff\" report has been added to  ResearchAndMarkets.com's offering.This comprehensive report on Kenya's healthcare sector offers a range of statistics covering the entire value chain an in-depth data-centric analysis of the entire healthcare ecosystem, covering a range of modules from demographic data to healthcare .....",
"link": "https://www.globenewswire.com/news-release/2025/08/18/3134815/28124/en/Kenya-Healthcare-Statistics-Databook-2025-Navigate-Healthcare-Planning-with-Over-300-KPIs-Spanning-Patient-to-Pharmacist-Statistics.html",
"symbols": [
"AAPL.US"
],
"tags": [
"DEMOGRAPHICS",
"GLOBAL",
"GROSS DOMESTIC PRODUCT",
"HEALTH PROFESSIONAL",
"HEALTHCARE ANALYTICS",
"HEALTHCARE INFRASTRUCTURE",
"HEALTHCARE LANDSCAPE",
"HEALTHCARE RESOURCES",
"HEALTHCARE SECTOR",
"HEALTHCARE SPENDING",
"HEALTHCARE STATISTICS",
"KENYA",
"MARKET OPPORTUNITIES",
"MARKET RESEARCH REPORTS",
"MEDICAL STAFF",
"MEDICAL STAFFING",
"PHARMACEUTICAL DISTRIBUTION",
"PHARMACIES",
"POPULATION TRENDS"
],
"sentiment": {
"polarity": 0.959,
"neg": 0.008,
"neu": 0.948,
"pos": 0.044
}
.......
```

```text
GET https://eodhd.com/api/sentiments
```

```text
"BTC-USD.CC": [
{
"date": "2022-04-22",
"count": 31,
"normalized": 0.1835
},
{
"date": "2022-04-21",
"count": 41,
"normalized": 0.2555
},
{
"date": "2022-04-20",
"count": 34,
"normalized": 0.2068
},
{
"date": "2022-04-19",
"count": 35,
"normalized": 0.4781
},
{
"date": "2022-04-18",
"count": 29,
"normalized": 0.1618
},
{
"date": "2022-04-17",
"count": 12,
"normalized": 0.0056
```

```text
GET https://eodhd.com/api/news-word-weights
```

## Related APIs

- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)
- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)
- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)
- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)
- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)
- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)
- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)
- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)
- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)
- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)
