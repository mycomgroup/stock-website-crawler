---
id: "url-2c96f6b4"
type: "api"
title: "Stock Market Screener API"
url: "https://eodhd.com/financial-apis/stock-market-screener-api/"
description: "The Screener API empowers users to quickly filter the stock market based on defined criteria / parameters with a single request, encompassing market capitalization, exchange, industry, dividend yield, and more metrics. Use Stock screener for financial visualizations of a higher complexity: realtime stock scanner and screener integrated together, could provide for investors robust trading insights and actionable data for informed decision-making."
source: ""
tags: []
crawl_time: "2026-03-18T06:15:06.161Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Stock Market Screener API\n\nThe Screener API empowers users to quickly filter the stock market based on defined criteria / parameters with a single request, encompassing market capitalization, exchange, industry, dividend yield, and more metrics. Use Stock screener for financial visualizations of a higher complexity: realtime stock scanner and screener integrated together, could provide for investors robust trading insights and actionable data for informed decision-making.\n\n\n## Usage Example & parameters\n\nScreener API request example:\n\n## Output\n\nThe output for the API request above:\n\n## Filtering data by fields\n\nVarious filter fields come in two types: Strings and Numbers. String Operations should be applied to strings, while Numeric Operations are suitable for numbers (see further). List of supported filter fields:\n\nExample: Filter all companies with a market capitalization above 1 billion, positive EPS within the ‘Personal Products’ industry, and names starting with the letter ‘B’:\n\n## List of Operations\n\nString operations are supported for all fields with the type ‘String’. Numeric Operations are supported for all fields with type ‘NUMBER’:\n\n## Filtering Data with Signals\n\nYou can use signals to filter tickers by different calculated fields. All signals are pre-calculated on our side.\n\nFor example, if you need only tickers that have new lows for the past 200 days and the Book Value is negative, you can use the parameter ‘signal’ with the following value, to get all tickers with the criteria:\n\n## Consumption\n\nEach Screener API request consumes 5 API calls. Best to be used together with our other APIs.\n\nScreener and Technical Indicators are integrated into our Google Sheets & Excel add-ons and in Python library already.\n\n## Code Examples\n\n```text\nhttps://eodhd.com/api/screener?api_token=YOUR_API_TOKEN&sort=market_capitalization.desc&filters=[[\"market_capitalization\",\">\",1000],[\"name\",\"match\",\"apple\"],[\"code\",\"=\",\"AAPL\"],[\"exchange\",\"=\",\"us\"],[\"sector\",\"=\",\"Technology\"]]&limit=10&offset=0\n```\n\n```text\nhttps://eodhd.com/api/screener?api_token=YOUR_API_TOKEN&sort=market_capitalization.desc&filters=[[“market_capitalization”,”>”,1000000000],[“earnings_share”,”>”,0],[“industry”,”match”,”Personal Products”],[“name”,”match”,”B*”]]&limit=10&offset=0\n```\n\n```text\nsignals=bookvalue_neg,200d_new_lo\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "stock-market-screener-api"
---

# Stock Market Screener API

## 源URL

https://eodhd.com/financial-apis/stock-market-screener-api/

## 描述

The Screener API empowers users to quickly filter the stock market based on defined criteria / parameters with a single request, encompassing market capitalization, exchange, industry, dividend yield, and more metrics. Use Stock screener for financial visualizations of a higher complexity: realtime stock scanner and screener integrated together, could provide for investors robust trading insights and actionable data for informed decision-making.

## 文档正文

The Screener API empowers users to quickly filter the stock market based on defined criteria / parameters with a single request, encompassing market capitalization, exchange, industry, dividend yield, and more metrics. Use Stock screener for financial visualizations of a higher complexity: realtime stock scanner and screener integrated together, could provide for investors robust trading insights and actionable data for informed decision-making.

## Usage Example & parameters

Screener API request example:

## Output

The output for the API request above:

## Filtering data by fields

Various filter fields come in two types: Strings and Numbers. String Operations should be applied to strings, while Numeric Operations are suitable for numbers (see further). List of supported filter fields:

Example: Filter all companies with a market capitalization above 1 billion, positive EPS within the ‘Personal Products’ industry, and names starting with the letter ‘B’:

## List of Operations

String operations are supported for all fields with the type ‘String’. Numeric Operations are supported for all fields with type ‘NUMBER’:

## Filtering Data with Signals

You can use signals to filter tickers by different calculated fields. All signals are pre-calculated on our side.

For example, if you need only tickers that have new lows for the past 200 days and the Book Value is negative, you can use the parameter ‘signal’ with the following value, to get all tickers with the criteria:

## Consumption

Each Screener API request consumes 5 API calls. Best to be used together with our other APIs.

Screener and Technical Indicators are integrated into our Google Sheets & Excel add-ons and in Python library already.

## Code Examples

```text
https://eodhd.com/api/screener?api_token=YOUR_API_TOKEN&sort=market_capitalization.desc&filters=[["market_capitalization",">",1000],["name","match","apple"],["code","=","AAPL"],["exchange","=","us"],["sector","=","Technology"]]&limit=10&offset=0
```

```text
https://eodhd.com/api/screener?api_token=YOUR_API_TOKEN&sort=market_capitalization.desc&filters=[[“market_capitalization”,”>”,1000000000],[“earnings_share”,”>”,0],[“industry”,”match”,”Personal Products”],[“name”,”match”,”B*”]]&limit=10&offset=0
```

```text
signals=bookvalue_neg,200d_new_lo
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
