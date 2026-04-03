---
id: "url-5bd25678"
type: "api"
title: "QUICK START with our Financial Data APIs"
url: "https://eodhd.com/financial-apis/quick-start-with-our-financial-data-apis"
description: "Welcome to EODHD! We specialize in providing extensive financial data through APIs. With our services, you can seamlessly integrate a wide range of financial data into your projects, including 30+ years Historical End-of-Day (EOD) prices, Real-time prices, Intraday data, Fundamental data for stocks, ETFs, funds, indices, bonds, forex pairs, and alternative currencies, across various programming languages or without coding at all (check Excel and Google Sheets add-ons below)."
source: ""
tags: []
crawl_time: "2026-03-18T06:19:08.834Z"
metadata:
  endpoint: "https://eodhd.com/api/exchanges-list/"
  parameters: []
  markdownContent: "# QUICK START with our Financial Data APIs\n\nWelcome to EODHD! We specialize in providing extensive financial data through APIs. With our services, you can seamlessly integrate a wide range of financial data into your projects, including 30+ years Historical End-of-Day (EOD) prices, Real-time prices, Intraday data, Fundamental data for stocks, ETFs, funds, indices, bonds, forex pairs, and alternative currencies, across various programming languages or without coding at all (check Excel and Google Sheets add-ons below).\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/exchanges-list/?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=json\n```\n\n\n## API Key (token)\n\nAn API key or token looks like 15d35814de0491.03453438 (each API key is different) and is necessary to make any API requests for our data. The key will be generated automatically after registration and can be found in the user dashboard or in the email sent right after signing up.\n\nAll API requests include this token as a parameter. This is how our server determines which data is available to which user, as we offer different plans and have an API call quota for each user. Refer to the API request examples further in this article – all of them use the “demo” API key or your API key if you are already a registered user and logged in.\n\nImportant! Do not share this API key publicly, as other users might use your plan quota.\n\nIt is possible to re-generate API key on user dashboard page.\n\n## Demo mode\n\nWithout registration (or without API key) you can test a few stock & forex tickers for getting almost all types of data we offer – Fundamental Data, EOD Historical Data, Live Data, Real-time, Financial News API. For demo API requests simply use “demo” for API key in JSON API requests.\n\nUsers can use “demo” API key in our Excel & Google Sheets as well. It will be set there by default after installation.\n\n## Free plan\n\nIf you are a registered user but haven’t subscribed to any of our extended payed plans, you are probably on our free plan. Free plan is a great way to test our data deeper. It offers access to most of stocks, forex pairs, ETFs and covers EOD Historical (limited 1 year history only) data, Live data, Splits & Dividents and more. Visit our pricing page to see all the data included.\n\n## API call limits\n\nTo maintain the stability of our data servers and provide all users with equal quality service, we have two types of API limits: Minute API Limit and Daily API Limit. Each plan in our pricing mentions the number of API calls included. To learn more about how API call limits work, read the article.\n\nIt is possible to buy extra API calls and keep them as a buffer. Additionally, you can increase your daily API call limits for an extra fee. These options are available on the user dashboard page.\n\n## Generate code with our own ChatGPT assistant\n\nA great option for those who are just starting to use our data and spend a lot of time writing code to retrieve it is our own ChatGPT assistant. It is trained on our data and API documentation and can effortlessly generate working code in any programming language to fetch specific pieces of data.\n\nSimply ask, “Write Python code to retrieve dividends for AAPL for 2024,” and see the magic happen!\n\nWatch a short YouTube video to learn how to use our GPT for code generation.\n\n## Stock Prices and more in Excel and Google Sheets add-ons\n\nIf you are not a developer but still in need of data such as stock prices, end-of-day (with charts), intraday, and fundamental data API, among others, we recommend you try our Excel and Google Sheets add-ins. They can work with “demo” key as well (set there by default) but we recommend to sign up for free to get an API key from free plan. With it, more data will be available.\n\n## Financial Data API examples\n\nLet’s begin testing our API with some of the most common requests, which you can try out directly in your browser.\n\nUsing our Exchanges and Get List of Tickers API, here’s how to request a list of all supported exchanges along with their codes (please note that this specific API returns data only in JSON format):\n\nNow, let’s retrieve the list of tickers per exchange. For the USA, the exchange code will be ‘US’. Please note that this API can return data in both CSV and JSON formats (using the parameter ‘&fmt’), with CSV being the default when no ‘&fmt’ is specified. In our case, we are expecting JSON:\n\nTo get End Of Day (EOD data) please use our End-Of-Day Historical Stock Market Data API:\n\nTo get Live/Delayed (15-minutes delayed data) please use our Live (Delayed) Stock Prices API:\n\nTo get Fundamental Data please use our Fundamental Data: Stocks, ETFs, Mutual Funds, Indices:\n\nTo get Intraday Data please use our Intraday Historical Data API:\n\nTo get Splits please use our Historical Splits and Dividends API:\n\nTo get Dividends please use our Historical Splits and Dividends API:\n\nTo Search stocks and any other assets please use our Search API:\n\nThese are a few examples, but we recommend studying our documentation and exploring additional APIs for various types of data. We offer over 50 API endpoints and continually add new data sources, APIs, and applied libraries.\n\n## Documentation & useful articles\n\nFor detailed documentation, please visit our Documentation section. Feel free to use the Search feature to find information on specific topics.\n\nExplore all the different ways you can make the most of our Financial Data API in our educational Academy section. This collection, gathered over several years from the insights of top traders, programmers, and market enthusiasts, offers articles on diverse trading strategies, analytical methods, and the application of AI in financial data analysis.\n\n## API Marketplace\n\nIn addition to our main data plans, our Marketplace offers unique data packages from both our partners and ourselves. All packages operate via APIs and work seamlessly with the same EODHD accounts and API tokens. Explore tools for technical analysis, ESG data, S&P historical indices, and much more.\n\n## 24/7 live support\n\nOne of our points of pride is our live support, which can not only advise you on any questions related to EODHD features and pricing plans but also resolve most technical issues while you’re online. You can contact support via the live chat in the lower right corner of every page on our site.\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "quick-start-with-our-financial-data-apis"
---

# QUICK START with our Financial Data APIs

## 源URL

https://eodhd.com/financial-apis/quick-start-with-our-financial-data-apis

## 描述

Welcome to EODHD! We specialize in providing extensive financial data through APIs. With our services, you can seamlessly integrate a wide range of financial data into your projects, including 30+ years Historical End-of-Day (EOD) prices, Real-time prices, Intraday data, Fundamental data for stocks, ETFs, funds, indices, bonds, forex pairs, and alternative currencies, across various programming languages or without coding at all (check Excel and Google Sheets add-ons below).

## API 端点

**Endpoint**: `https://eodhd.com/api/exchanges-list/`

## 文档正文

Welcome to EODHD! We specialize in providing extensive financial data through APIs. With our services, you can seamlessly integrate a wide range of financial data into your projects, including 30+ years Historical End-of-Day (EOD) prices, Real-time prices, Intraday data, Fundamental data for stocks, ETFs, funds, indices, bonds, forex pairs, and alternative currencies, across various programming languages or without coding at all (check Excel and Google Sheets add-ons below).

## API Endpoint

```text
https://eodhd.com/api/exchanges-list/?api_token={YOUR_API_TOKEN}&fmt=json
```

```text
https://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}?api_token={YOUR_API_TOKEN}&fmt=json
```

```text
https://eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=json
```

## API Key (token)

An API key or token looks like 15d35814de0491.03453438 (each API key is different) and is necessary to make any API requests for our data. The key will be generated automatically after registration and can be found in the user dashboard or in the email sent right after signing up.

All API requests include this token as a parameter. This is how our server determines which data is available to which user, as we offer different plans and have an API call quota for each user. Refer to the API request examples further in this article – all of them use the “demo” API key or your API key if you are already a registered user and logged in.

Important! Do not share this API key publicly, as other users might use your plan quota.

It is possible to re-generate API key on user dashboard page.

## Demo mode

Without registration (or without API key) you can test a few stock & forex tickers for getting almost all types of data we offer – Fundamental Data, EOD Historical Data, Live Data, Real-time, Financial News API. For demo API requests simply use “demo” for API key in JSON API requests.

Users can use “demo” API key in our Excel & Google Sheets as well. It will be set there by default after installation.

## Free plan

If you are a registered user but haven’t subscribed to any of our extended payed plans, you are probably on our free plan. Free plan is a great way to test our data deeper. It offers access to most of stocks, forex pairs, ETFs and covers EOD Historical (limited 1 year history only) data, Live data, Splits & Dividents and more. Visit our pricing page to see all the data included.

## API call limits

To maintain the stability of our data servers and provide all users with equal quality service, we have two types of API limits: Minute API Limit and Daily API Limit. Each plan in our pricing mentions the number of API calls included. To learn more about how API call limits work, read the article.

It is possible to buy extra API calls and keep them as a buffer. Additionally, you can increase your daily API call limits for an extra fee. These options are available on the user dashboard page.

## Generate code with our own ChatGPT assistant

A great option for those who are just starting to use our data and spend a lot of time writing code to retrieve it is our own ChatGPT assistant. It is trained on our data and API documentation and can effortlessly generate working code in any programming language to fetch specific pieces of data.

Simply ask, “Write Python code to retrieve dividends for AAPL for 2024,” and see the magic happen!

Watch a short YouTube video to learn how to use our GPT for code generation.

## Stock Prices and more in Excel and Google Sheets add-ons

If you are not a developer but still in need of data such as stock prices, end-of-day (with charts), intraday, and fundamental data API, among others, we recommend you try our Excel and Google Sheets add-ins. They can work with “demo” key as well (set there by default) but we recommend to sign up for free to get an API key from free plan. With it, more data will be available.

## Financial Data API examples

Let’s begin testing our API with some of the most common requests, which you can try out directly in your browser.

Using our Exchanges and Get List of Tickers API, here’s how to request a list of all supported exchanges along with their codes (please note that this specific API returns data only in JSON format):

Now, let’s retrieve the list of tickers per exchange. For the USA, the exchange code will be ‘US’. Please note that this API can return data in both CSV and JSON formats (using the parameter ‘&fmt’), with CSV being the default when no ‘&fmt’ is specified. In our case, we are expecting JSON:

To get End Of Day (EOD data) please use our End-Of-Day Historical Stock Market Data API:

To get Live/Delayed (15-minutes delayed data) please use our Live (Delayed) Stock Prices API:

To get Fundamental Data please use our Fundamental Data: Stocks, ETFs, Mutual Funds, Indices:

To get Intraday Data please use our Intraday Historical Data API:

To get Splits please use our Historical Splits and Dividends API:

To get Dividends please use our Historical Splits and Dividends API:

To Search stocks and any other assets please use our Search API:

These are a few examples, but we recommend studying our documentation and exploring additional APIs for various types of data. We offer over 50 API endpoints and continually add new data sources, APIs, and applied libraries.

## Documentation & useful articles

For detailed documentation, please visit our Documentation section. Feel free to use the Search feature to find information on specific topics.

Explore all the different ways you can make the most of our Financial Data API in our educational Academy section. This collection, gathered over several years from the insights of top traders, programmers, and market enthusiasts, offers articles on diverse trading strategies, analytical methods, and the application of AI in financial data analysis.

## API Marketplace

In addition to our main data plans, our Marketplace offers unique data packages from both our partners and ourselves. All packages operate via APIs and work seamlessly with the same EODHD accounts and API tokens. Explore tools for technical analysis, ESG data, S&P historical indices, and much more.

## 24/7 live support

One of our points of pride is our live support, which can not only advise you on any questions related to EODHD features and pricing plans but also resolve most technical issues while you’re online. You can contact support via the live chat in the lower right corner of every page on our site.

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
