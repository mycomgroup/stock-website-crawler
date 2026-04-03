---
id: "url-3cd72195"
type: "api"
title: "Live OHLCV Stock Prices API: US & Global Stocks, Currencies"
url: "https://eodhd.com/financial-apis/live-ohlcv-stocks-api"
description: "EODHD APIs offer one of the best ways for trading enthusiasts, developers, and data analysts to incorporate live financial data into their decision-making projects, with a delay of 15-20 min covering almost all stocks on the market and 1 min delay for 1100+ Forex pairs."
source: ""
tags: []
crawl_time: "2026-03-18T03:04:58.925Z"
metadata:
  endpoint: "https://eodhd.com/api/real-time/AAPL.US"
  parameters: []
  markdownContent: "# Live OHLCV Stock Prices API: US & Global Stocks, Currencies\n\nEODHD APIs offer one of the best ways for trading enthusiasts, developers, and data analysts to incorporate live financial data into their decision-making projects, with a delay of 15-20 min covering almost all stocks on the market and 1 min delay for 1100+ Forex pairs.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/real-time/AAPL.US?s=VTI,EUR.FOREX&api_token=demo&fmt=json\n```\n\n\n## Request Example for Live OHLCV Data\n\nHere is an example of live (delayed) stock prices API for AAPL (Apple Inc). Please note that the API token ‘demo’ only works for AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD tickers:\n\nJSON response is:\n\n## Multiple Tickers with One Request\n\nAdd the ‘s=’ parameter to your URL, and you will be able to retrieve data for multiple tickers in a single request. All tickers should be separated by a comma. For example, you can request data for AAPL.US, VTI, and EUR.FOREX with the following URL:\n\nPlease note that ‘AAPL.US’ is used here at the beginning, and additional tickers are added with the ‘s=’ parameter.\n\n## JSON and CSV formats\n\nWe support live (delayed) stock price data in both JSON and CSV formats. If you prefer CSV output, simply change ‘fmt=json’ to ‘fmt=csv’ or remove this parameter altogether.\n\n## Daily limits\n\nOur API has a limit of 100,000 requests per day, with each symbol request counting as 1 API call. For instance, a request for multiple tickers with 10 symbols will consume 10 API calls.\n\n## Live data via Excel and Google Sheets\n\nAccess live data through our free Excel and Google Sheets add-ons. Learn more about them and download them here. With these add-ons, financial data for stocks, ETFs, mutual funds, and FOREX markets is now available on any device without coding. Additionally, we provide Excel support for Webservice.\n\n## Conclusion\n\nEODHD provides one of the best solutions for integrating live finance data into decision-making projects, offering stock market data with real-time streaming and historical data API capabilities across global markets. Explore our pricing plans to explore all avalible features for your financial projects. We recommend checking out our Live (Delayed) Data API, which complements our offerings with free real-time and historical stock market data, empowering users with insights for their trading strategies.\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "live-ohlcv-stocks-api"
---

# Live OHLCV Stock Prices API: US & Global Stocks, Currencies

## 源URL

https://eodhd.com/financial-apis/live-ohlcv-stocks-api

## 描述

EODHD APIs offer one of the best ways for trading enthusiasts, developers, and data analysts to incorporate live financial data into their decision-making projects, with a delay of 15-20 min covering almost all stocks on the market and 1 min delay for 1100+ Forex pairs.

## API 端点

**Endpoint**: `https://eodhd.com/api/real-time/AAPL.US`

## 文档正文

EODHD APIs offer one of the best ways for trading enthusiasts, developers, and data analysts to incorporate live financial data into their decision-making projects, with a delay of 15-20 min covering almost all stocks on the market and 1 min delay for 1100+ Forex pairs.

## API Endpoint

```text
https://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json
```

```text
https://eodhd.com/api/real-time/AAPL.US?s=VTI,EUR.FOREX&api_token=demo&fmt=json
```

## Request Example for Live OHLCV Data

Here is an example of live (delayed) stock prices API for AAPL (Apple Inc). Please note that the API token ‘demo’ only works for AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD tickers:

JSON response is:

## Multiple Tickers with One Request

Add the ‘s=’ parameter to your URL, and you will be able to retrieve data for multiple tickers in a single request. All tickers should be separated by a comma. For example, you can request data for AAPL.US, VTI, and EUR.FOREX with the following URL:

Please note that ‘AAPL.US’ is used here at the beginning, and additional tickers are added with the ‘s=’ parameter.

## JSON and CSV formats

We support live (delayed) stock price data in both JSON and CSV formats. If you prefer CSV output, simply change ‘fmt=json’ to ‘fmt=csv’ or remove this parameter altogether.

## Daily limits

Our API has a limit of 100,000 requests per day, with each symbol request counting as 1 API call. For instance, a request for multiple tickers with 10 symbols will consume 10 API calls.

## Live data via Excel and Google Sheets

Access live data through our free Excel and Google Sheets add-ons. Learn more about them and download them here. With these add-ons, financial data for stocks, ETFs, mutual funds, and FOREX markets is now available on any device without coding. Additionally, we provide Excel support for Webservice.

## Conclusion

EODHD provides one of the best solutions for integrating live finance data into decision-making projects, offering stock market data with real-time streaming and historical data API capabilities across global markets. Explore our pricing plans to explore all avalible features for your financial projects. We recommend checking out our Live (Delayed) Data API, which complements our offerings with free real-time and historical stock market data, empowering users with insights for their trading strategies.

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
