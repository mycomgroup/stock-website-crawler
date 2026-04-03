---
id: "url-6eca54ae"
type: "api"
title: "Windows and Linux Downloaders for End Of Day Data"
url: "https://eodhd.com/financial-apis/windows-downloader-end-of-day-data"
description: "This application is designed for downloading End-of-Day and Intraday data from EODHD. It serves as an excellent no-code alternative to accessing data via API or downloading files through FTP. It’s easy to download even the entire US stock market, with more than 47.000 active tickers we track, just with one click. The application supports multi-threading and proxy servers for optimized performance."
source: ""
tags: []
crawl_time: "2026-03-18T04:27:58.346Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Windows and Linux Downloaders for End Of Day Data\n\nThis application is designed for downloading End-of-Day and Intraday data from EODHD. It serves as an excellent no-code alternative to accessing data via API or downloading files through FTP. It’s easy to download even the entire US stock market, with more than 47.000 active tickers we track, just with one click. The application supports multi-threading and proxy servers for optimized performance.\n\n\n## Versions\n\nVersion 2 (updated: Jan, 2025): This article introduces the second version of the app (featuring a dark blue UI). It is open-source and available on our GitHub.\n\nVersion 1: The older version of the app (with a grey UI) is still available for download, but it is no longer supported by our technical team. You can download it here and find the source code on GitHub. For guidance on how to use it, check out our video tutorial.\n\n## Features\n\nThe app operates using an EODHD API key, which is linked to the user’s subscription. It also supports the “demo” key and the key from the “free” subscription plan. Learn more about our API key system here.\n\nInstall Windows Downloader 2.0\n\n## Windows Downloader 2.0: End-of-Day Data\n\nThis section is tailored for working with historical data of selected tickers, commonly used for financial market analysis.\n\nInstall Windows Downloader 2.0\n\n## Windows Downloader 2.0: Intraday Data\n\nThis section enables users to work with intraday data for selected tickers.\n\n## Settings\n\nThis section provides access to the core application settings, including API key management.\n\n## Linux Downloader for EOD data\n\nThe Linux with bash support does not require special software but shell one-liner to download the end of day data and any other financial data with our API. And it’s easy to download the end of day data for as many tickers as you need just in two steps.\n\nStep 1. Create the file with the list of symbols, in our example, we named it ‘tickers.txt’ and added only two tickers line by line.\n\nStep 2. Use the following one-line command, just change the API key to yours:\n\nWe will be happy to get an email to support@eodhistoricaldata.com.\n\n## Code Examples\n\n```text\nfor i in `cat tickers.txt`; do wget \"https://eodhd.com/api/eod/$i?api_token=YOUR_API_KEY&order=d&fmt=csv&from=2017-08-01\" -O $i.csv; done;\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "windows-downloader-end-of-day-data"
---

# Windows and Linux Downloaders for End Of Day Data

## 源URL

https://eodhd.com/financial-apis/windows-downloader-end-of-day-data

## 描述

This application is designed for downloading End-of-Day and Intraday data from EODHD. It serves as an excellent no-code alternative to accessing data via API or downloading files through FTP. It’s easy to download even the entire US stock market, with more than 47.000 active tickers we track, just with one click. The application supports multi-threading and proxy servers for optimized performance.

## 文档正文

This application is designed for downloading End-of-Day and Intraday data from EODHD. It serves as an excellent no-code alternative to accessing data via API or downloading files through FTP. It’s easy to download even the entire US stock market, with more than 47.000 active tickers we track, just with one click. The application supports multi-threading and proxy servers for optimized performance.

## Versions

Version 2 (updated: Jan, 2025): This article introduces the second version of the app (featuring a dark blue UI). It is open-source and available on our GitHub.

Version 1: The older version of the app (with a grey UI) is still available for download, but it is no longer supported by our technical team. You can download it here and find the source code on GitHub. For guidance on how to use it, check out our video tutorial.

## Features

The app operates using an EODHD API key, which is linked to the user’s subscription. It also supports the “demo” key and the key from the “free” subscription plan. Learn more about our API key system here.

Install Windows Downloader 2.0

## Windows Downloader 2.0: End-of-Day Data

This section is tailored for working with historical data of selected tickers, commonly used for financial market analysis.

Install Windows Downloader 2.0

## Windows Downloader 2.0: Intraday Data

This section enables users to work with intraday data for selected tickers.

## Settings

This section provides access to the core application settings, including API key management.

## Linux Downloader for EOD data

The Linux with bash support does not require special software but shell one-liner to download the end of day data and any other financial data with our API. And it’s easy to download the end of day data for as many tickers as you need just in two steps.

Step 1. Create the file with the list of symbols, in our example, we named it ‘tickers.txt’ and added only two tickers line by line.

Step 2. Use the following one-line command, just change the API key to yours:

We will be happy to get an email to support@eodhistoricaldata.com.

## Code Examples

```text
for i in `cat tickers.txt`; do wget "https://eodhd.com/api/eod/$i?api_token=YOUR_API_KEY&order=d&fmt=csv&from=2017-08-01" -O $i.csv; done;
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
