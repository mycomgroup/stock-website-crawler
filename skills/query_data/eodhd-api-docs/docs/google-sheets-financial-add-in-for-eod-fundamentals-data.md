---
id: "url-44e7cf5c"
type: "api"
title: "Google Sheets Finance Data Add-on"
url: "https://eodhd.com/financial-apis/google-sheets-financial-add-in-for-eod-fundamentals-data"
description: "Install Financial Data Free Add-on  for Google Sheets"
source: ""
tags: []
crawl_time: "2026-03-18T13:14:46.754Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Google Sheets Finance Data Add-on\n\nInstall Financial Data Free Add-on  for Google Sheets\n\n\n## Activate your API key\n\nThough there is a demo mode in the add-on which gives an opportunity to get Fundamental & Live data for a few tickers, in order to use the add-on fully we recommend to sign up on our site. Registration is free and provides you with API Key which should be used in Google Sheets Add-on in order to get access to more data.\n\n1. You can start with “DEMO” API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. For these tickers, all of our types of data (APIs), including Real-Time Data, are available without limitations.2. Register for the free plan to receive your API key (limited to 20 API calls per day) with access to End-Of-Day Historical Stock Market Data API for any ticker, but within the past year only. Plus a List of tickers per Exchange is available.3. We recommend to explore our plans, starting from $19.99, to access the necessary type of data without limitations.\n\n## Google Sheets Financial Data Add-on installation\n\nThe add-on is free and can be installed in a few clicks from Google Marketplace.\n\n2. The add-on requeres minimum of permissions in order to be able to take financial data via API from our server and export it to your Google Sheets document:\n\n3. After a successful installation, refresh the Google Sheets tab. You can find the add-on in the right sidebar menu or in the main Google Sheets menu under Extensions:\n\n4. If the right sidebar is not visible, click the arrow in the bottom-right corner:\n\n4. By default, the demo key is applied, which only works with a few tickers. After signing up on eodhd.com, you will receive an API key that should be used instead of the ‘demo’ key:\n\n## How to get stock data in Google Sheets\n\nOur add-on provides a formula-free workflow, meaning you don’t have to write formulas yourself. Simply choose the desired options, fill in the fields, and insert the data into a new sheet.\n\nFor example, here we retrieve EOD historical data with chart using add-on for AAPL.US:\n\nEach request will import data by creating a new sheet in your project, ensuring that no existing data is lost or replaced.\n\nVarious types of data are available only under certain subscription plans. As you can see, the ‘demo’ plan has the most limitations and basically works with only a few tickers for each type of data:\n\nFor example, the free plan provides access to all tickers for EOD data but is limited in historical depth. Compare plans to see which one best fits your needs.\n\nIf you believe that you have limitations that do not apply properly to your plan, please contact our support team (chat icon in the lower right corner).\n\n## EOD Historical Data (IMPORTDATA function)\n\nWe support the ‘IMPORTDATA’ Google Sheet function. Just add ‘filter=last_close’ or ‘filter=last_volume’ with ‘fmt=json’, and you will get only one number which perfectly works with IMPORT functions for Google Sheets. This feature works for any End of Day or Fundamentals API request with the ‘filter’ parameter. For example, with this URL:\n\nYou will get one value – the last price for MCD.\n\nThe ‘WEBSERVICE’ function for Excel is also supported.\n\n## Apipheny\n\nAnother option is integrating with the Apipheny Google Sheets service. It’s a fast, flexible, and reasonably priced API used to import financial data into Google Sheets, allowing you to automate your data pulls without overspending. While an Apipheny subscription is required for this integration, their prices are relatively low.\n\nYou can find complete documentation on integrating our Financial APIs with Google Sheets and Apipheny here: https://apipheny.io/eod-historical-data-api/.\n\n## Cryptosheets\n\nWe also offer integration with Cryptosheets, a versatile service offering dozens of integrations with various APIs for both Google Sheets and Excel. All our APIs are seamlessly integrated there, and the service is flexible and user-friendly. A Cryptosheets subscription is required for this integration.\n\nYou can find comprehensive documentation on integrating our Financial APIs with Google Sheets and Cryptosheets here: https://docs.cryptosheets.com/providers/eod-historical-data/.\n\n## 24/7 EODHD Support\n\nIf you found a bug or would like to suggest what other data could be integrated into our Google Sheets add-on, please contact our support team via chat on our main site or via email at support@eodhistoricaldata.com.\n\n## Code Examples\n\n```text\nhttps://eodhd.com/api/eod/MCD.US?api_token=demo&fmt=json&filter=last_close\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "google-sheets-financial-add-in-for-eod-fundamentals-data"
---

# Google Sheets Finance Data Add-on

## 源URL

https://eodhd.com/financial-apis/google-sheets-financial-add-in-for-eod-fundamentals-data

## 描述

Install Financial Data Free Add-on  for Google Sheets

## 文档正文

Install Financial Data Free Add-on  for Google Sheets

## Activate your API key

Though there is a demo mode in the add-on which gives an opportunity to get Fundamental & Live data for a few tickers, in order to use the add-on fully we recommend to sign up on our site. Registration is free and provides you with API Key which should be used in Google Sheets Add-on in order to get access to more data.

1. You can start with “DEMO” API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. For these tickers, all of our types of data (APIs), including Real-Time Data, are available without limitations.2. Register for the free plan to receive your API key (limited to 20 API calls per day) with access to End-Of-Day Historical Stock Market Data API for any ticker, but within the past year only. Plus a List of tickers per Exchange is available.3. We recommend to explore our plans, starting from $19.99, to access the necessary type of data without limitations.

## Google Sheets Financial Data Add-on installation

The add-on is free and can be installed in a few clicks from Google Marketplace.

2. The add-on requeres minimum of permissions in order to be able to take financial data via API from our server and export it to your Google Sheets document:

3. After a successful installation, refresh the Google Sheets tab. You can find the add-on in the right sidebar menu or in the main Google Sheets menu under Extensions:

4. If the right sidebar is not visible, click the arrow in the bottom-right corner:

4. By default, the demo key is applied, which only works with a few tickers. After signing up on eodhd.com, you will receive an API key that should be used instead of the ‘demo’ key:

## How to get stock data in Google Sheets

Our add-on provides a formula-free workflow, meaning you don’t have to write formulas yourself. Simply choose the desired options, fill in the fields, and insert the data into a new sheet.

For example, here we retrieve EOD historical data with chart using add-on for AAPL.US:

Each request will import data by creating a new sheet in your project, ensuring that no existing data is lost or replaced.

Various types of data are available only under certain subscription plans. As you can see, the ‘demo’ plan has the most limitations and basically works with only a few tickers for each type of data:

For example, the free plan provides access to all tickers for EOD data but is limited in historical depth. Compare plans to see which one best fits your needs.

If you believe that you have limitations that do not apply properly to your plan, please contact our support team (chat icon in the lower right corner).

## EOD Historical Data (IMPORTDATA function)

We support the ‘IMPORTDATA’ Google Sheet function. Just add ‘filter=last_close’ or ‘filter=last_volume’ with ‘fmt=json’, and you will get only one number which perfectly works with IMPORT functions for Google Sheets. This feature works for any End of Day or Fundamentals API request with the ‘filter’ parameter. For example, with this URL:

You will get one value – the last price for MCD.

The ‘WEBSERVICE’ function for Excel is also supported.

## Apipheny

Another option is integrating with the Apipheny Google Sheets service. It’s a fast, flexible, and reasonably priced API used to import financial data into Google Sheets, allowing you to automate your data pulls without overspending. While an Apipheny subscription is required for this integration, their prices are relatively low.

You can find complete documentation on integrating our Financial APIs with Google Sheets and Apipheny here: https://apipheny.io/eod-historical-data-api/.

## Cryptosheets

We also offer integration with Cryptosheets, a versatile service offering dozens of integrations with various APIs for both Google Sheets and Excel. All our APIs are seamlessly integrated there, and the service is flexible and user-friendly. A Cryptosheets subscription is required for this integration.

You can find comprehensive documentation on integrating our Financial APIs with Google Sheets and Cryptosheets here: https://docs.cryptosheets.com/providers/eod-historical-data/.

## 24/7 EODHD Support

If you found a bug or would like to suggest what other data could be integrated into our Google Sheets add-on, please contact our support team via chat on our main site or via email at support@eodhistoricaldata.com.

## Code Examples

```text
https://eodhd.com/api/eod/MCD.US?api_token=demo&fmt=json&filter=last_close
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
