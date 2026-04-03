---
id: "url-26c30087"
type: "api"
title: "Financial Excel Add-on For Historical, EOD, Intraday & Fundamental data. Video tutorial"
url: "https://eodhd.com/financial-apis/excel-financial-add-on-fundamentals-end-of-day-charts/"
description: "If you are not familiar with programming languages, one of the best ways to retrieve stock price in Excel and Google Sheets (or any other financial data) is our Excel and Google Sheets add-ons. Without any complicated code, you can easily get:• Fundamental data for Stocks, ETF or Funds• End-of-day historical data• Intraday data"
source: ""
tags: []
crawl_time: "2026-03-18T14:48:11.864Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Financial Excel Add-on For Historical, EOD, Intraday & Fundamental data. Video tutorial\n\nIf you are not familiar with programming languages, one of the best ways to retrieve stock price in Excel and Google Sheets (or any other financial data) is our Excel and Google Sheets add-ons. Without any complicated code, you can easily get:• Fundamental data for Stocks, ETF or Funds• End-of-day historical data• Intraday data\n\n\n## What is stock market data, and why do you need it?\n\nUnderstanding stock market data is crucial for making informed investment decisions, eather you are implementing data to your coding project or using it in Excel and Google Sheets analysis. It provides insights into the performance of various assets, including stocks, indices, and currencies. With access to reliable financial data, investors can analyze market trends, identify opportunities, and mitigate risks effectively. Our Financial Data API offers a seamless way to access high quality market data, empowering users to make informed decisions and stay ahead in the competitive financial landscape.\n\n## Different types of stock market data\n\nStock market data, comprising Historical, Real-time, Intraday, and End of Day (EOD) data, is pivotal for investors & data analysts. Fundamental data reveals company financials, and alternative sources offer insights into market sentiment. Intraday data sheds light on price fluctuations during the trading day, while EOD data summarizes market activity at the close. Historical data provides insights into past market trends, while real-time data offers up-to-the-minute information crucial for timely decision-making. Plus to the data our API also offers useful tools such as Screener & Technical Indicators.\n\n## Getting stock market data using a web platform\n\nConsidered to be the least convenient method, obtaining stock market data through a web platform or an application involves navigating to the platform, specifying desired criteria such as date ranges and asset classes, and then accessing the data either through downloadable files or interactive charts and tables. As the market constantly evolves and data changes, it becomes very hard to track data updates.\n\n## Getting stock market data using an API\n\nUtilizing an API straight away makes a developer’s life much easier, as from now on, the API provider is responsible for adapting to any data updates. To access stock market data, it entails integrating the API into your software environment, sending requests to the API specifying the required data parameters, and receiving the requested data in a structured format such as JSON or CSV files.\n\n## Getting stock market data in Excel or Google Sheets\n\nA logical alternative to working with APIs, especially if you lack coding skills, is to implement financial data directly into Excel or Google Sheets. We provide both add-ons that retrieve the data, build charts, and don’t even require the use of formulas – all requests can be done in just a few clicks.\n\n## How to choose the best stock market data provider method\n\nAs there are various data providers in the market offering data via API, pay attention not only to pricing but also to the quality of data, the professionalism of the support team, and the convenience of Excel, Google Sheets, and other add-ons if they are offered. When choosing an Excel add-on, it’s important to understand if the app has a user-friendly interface, requires knowledge of writing Excel formulas, automatically builds charts, and which data can be accessed. The data we offer:\n\nEODHD Excel add-on is formula-free, constantly updates, and has a 24/7 support team behind it. Download the Excel add-on and see the full list of its features here.\n\n## Video tutorial for EODHD Excel add-on: Installation and examples\n\nWatch the video where Jonathon shows you how to use the EODHD Financial Excel add-on. Or scroll down to read more about the add-on.\n\n## Activate your API key\n\nIn order to use EODHD Excel Add-on it’s necessary to register on our site.  Registration is free and provides you API Key which should be used in Excel Add-on in order to get access to data. We offer free financial API for Excel and payed plans which include different types of data.\n\n1. You can start with “DEMO” API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. For these tickers, all of our types of data (APIs), including Real-Time Data, are available without limitations.2. Register for the free plan to receive your API key (limited to 20 API calls per day) with access to End-Of-Day Historical Stock Market Data API for any ticker, but within the past year only. Plus a List of tickers per Exchange is available.3. We recommend to explore our plans, starting from $19.99, to access the necessary type of data without limitations.\n\nOnce you have an API key and Excel add-on is installed, you are ready to use it:\n\n## Examples of Excel add-on features\n\nAll company tickers are connected to our database, so you won’t need to guess; you can easily search for them:\n\nAll possible type of data requests are listed above the spreadsheet. An example for intraday request with chart:\n\nA result of Historical data request with candlestick chart:\n\n## Excel VBA example\n\nWe created an Excel VBA example that works with our API. You can download an example of XLS-file and read our instructions below.\n\nTo access our API, you can use our defined function “=EODSymbolData(Symbol, From_Date, To_Date).” It’s easy like you use other functions “=SUM(…)” or “=AVERAGE(…)”\n\nDont forget to change DEMO key to your own. The current key works only with AAPL.US.\n\nTo see the code, please push ALT+F11 and open VBA Module ‘EODHistoricalData’ to check the VBA function:\n\nDownload our XLS-file example for getting EOD Historical Data via API and check the source to create your spreadsheet\n\n## Excel VBA script for multiple (bulk) downloads\n\nHere you can find an Excel VBA script for multiple (or bulk) downloads: vba-multiple-download-new 2.1.xlsm. It’s easy to test and use. Just follow these two steps:\n\nOctober 2024 update. By clicking the “Get dividends” button, dividends are downloaded for the tickers listed in the ticker column. The “from” and “to” dates also work and are passed in the request. A separate tab is created for each company’s dividends.\n\n## LIVE API Excel Webservice support\n\nIn order to access data via Excel Webservice feature, keep in mind this tip.\n\nIf you need only any one field, use ‘filter=FIELDNAME’ parameter. For example, if you use the following URL:\n\nThen only one number will be returned: 172.5. Which is very useful for Excel WEBSERVICE function like this:\n\nEODHD offers finance API for stock data Excel. In case if you have more questions and need an assistance with Excel add-on contact us through chat or via email support@eodhistoricaldata.com.\n\n## Code Examples\n\n```text\nhttps://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json&filter=close\n```\n\n```text\n=WEBSERVICE(https://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json&filter=close)\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "excel-financial-add-on-fundamentals-end-of-day-charts"
---

# Financial Excel Add-on For Historical, EOD, Intraday & Fundamental data. Video tutorial

## 源URL

https://eodhd.com/financial-apis/excel-financial-add-on-fundamentals-end-of-day-charts/

## 描述

If you are not familiar with programming languages, one of the best ways to retrieve stock price in Excel and Google Sheets (or any other financial data) is our Excel and Google Sheets add-ons. Without any complicated code, you can easily get:• Fundamental data for Stocks, ETF or Funds• End-of-day historical data• Intraday data

## 文档正文

If you are not familiar with programming languages, one of the best ways to retrieve stock price in Excel and Google Sheets (or any other financial data) is our Excel and Google Sheets add-ons. Without any complicated code, you can easily get:• Fundamental data for Stocks, ETF or Funds• End-of-day historical data• Intraday data

## What is stock market data, and why do you need it?

Understanding stock market data is crucial for making informed investment decisions, eather you are implementing data to your coding project or using it in Excel and Google Sheets analysis. It provides insights into the performance of various assets, including stocks, indices, and currencies. With access to reliable financial data, investors can analyze market trends, identify opportunities, and mitigate risks effectively. Our Financial Data API offers a seamless way to access high quality market data, empowering users to make informed decisions and stay ahead in the competitive financial landscape.

## Different types of stock market data

Stock market data, comprising Historical, Real-time, Intraday, and End of Day (EOD) data, is pivotal for investors & data analysts. Fundamental data reveals company financials, and alternative sources offer insights into market sentiment. Intraday data sheds light on price fluctuations during the trading day, while EOD data summarizes market activity at the close. Historical data provides insights into past market trends, while real-time data offers up-to-the-minute information crucial for timely decision-making. Plus to the data our API also offers useful tools such as Screener & Technical Indicators.

## Getting stock market data using a web platform

Considered to be the least convenient method, obtaining stock market data through a web platform or an application involves navigating to the platform, specifying desired criteria such as date ranges and asset classes, and then accessing the data either through downloadable files or interactive charts and tables. As the market constantly evolves and data changes, it becomes very hard to track data updates.

## Getting stock market data using an API

Utilizing an API straight away makes a developer’s life much easier, as from now on, the API provider is responsible for adapting to any data updates. To access stock market data, it entails integrating the API into your software environment, sending requests to the API specifying the required data parameters, and receiving the requested data in a structured format such as JSON or CSV files.

## Getting stock market data in Excel or Google Sheets

A logical alternative to working with APIs, especially if you lack coding skills, is to implement financial data directly into Excel or Google Sheets. We provide both add-ons that retrieve the data, build charts, and don’t even require the use of formulas – all requests can be done in just a few clicks.

## How to choose the best stock market data provider method

As there are various data providers in the market offering data via API, pay attention not only to pricing but also to the quality of data, the professionalism of the support team, and the convenience of Excel, Google Sheets, and other add-ons if they are offered. When choosing an Excel add-on, it’s important to understand if the app has a user-friendly interface, requires knowledge of writing Excel formulas, automatically builds charts, and which data can be accessed. The data we offer:

EODHD Excel add-on is formula-free, constantly updates, and has a 24/7 support team behind it. Download the Excel add-on and see the full list of its features here.

## Video tutorial for EODHD Excel add-on: Installation and examples

Watch the video where Jonathon shows you how to use the EODHD Financial Excel add-on. Or scroll down to read more about the add-on.

## Activate your API key

In order to use EODHD Excel Add-on it’s necessary to register on our site.  Registration is free and provides you API Key which should be used in Excel Add-on in order to get access to data. We offer free financial API for Excel and payed plans which include different types of data.

1. You can start with “DEMO” API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. For these tickers, all of our types of data (APIs), including Real-Time Data, are available without limitations.2. Register for the free plan to receive your API key (limited to 20 API calls per day) with access to End-Of-Day Historical Stock Market Data API for any ticker, but within the past year only. Plus a List of tickers per Exchange is available.3. We recommend to explore our plans, starting from $19.99, to access the necessary type of data without limitations.

Once you have an API key and Excel add-on is installed, you are ready to use it:

## Examples of Excel add-on features

All company tickers are connected to our database, so you won’t need to guess; you can easily search for them:

All possible type of data requests are listed above the spreadsheet. An example for intraday request with chart:

A result of Historical data request with candlestick chart:

## Excel VBA example

We created an Excel VBA example that works with our API. You can download an example of XLS-file and read our instructions below.

To access our API, you can use our defined function “=EODSymbolData(Symbol, From_Date, To_Date).” It’s easy like you use other functions “=SUM(…)” or “=AVERAGE(…)”

Dont forget to change DEMO key to your own. The current key works only with AAPL.US.

To see the code, please push ALT+F11 and open VBA Module ‘EODHistoricalData’ to check the VBA function:

Download our XLS-file example for getting EOD Historical Data via API and check the source to create your spreadsheet

## Excel VBA script for multiple (bulk) downloads

Here you can find an Excel VBA script for multiple (or bulk) downloads: vba-multiple-download-new 2.1.xlsm. It’s easy to test and use. Just follow these two steps:

October 2024 update. By clicking the “Get dividends” button, dividends are downloaded for the tickers listed in the ticker column. The “from” and “to” dates also work and are passed in the request. A separate tab is created for each company’s dividends.

## LIVE API Excel Webservice support

In order to access data via Excel Webservice feature, keep in mind this tip.

If you need only any one field, use ‘filter=FIELDNAME’ parameter. For example, if you use the following URL:

Then only one number will be returned: 172.5. Which is very useful for Excel WEBSERVICE function like this:

EODHD offers finance API for stock data Excel. In case if you have more questions and need an assistance with Excel add-on contact us through chat or via email support@eodhistoricaldata.com.

## Code Examples

```text
https://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json&filter=close
```

```text
=WEBSERVICE(https://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json&filter=close)
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
