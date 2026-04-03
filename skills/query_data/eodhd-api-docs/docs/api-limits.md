---
id: "url-30add5c7"
type: "api"
title: "API Limits: calls, requests, consumption"
url: "https://eodhd.com/financial-apis/api-limits/"
description: "To ensure the stability of our data servers and provide all users with equal service quality, we have implemented an “API calls system,” which functions as a currency for each API request. This system includes two types of limits: the Minute Request Limit and the Daily Call Limit."
source: ""
tags: []
crawl_time: "2026-03-18T04:17:23.870Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# API Limits: calls, requests, consumption\n\nTo ensure the stability of our data servers and provide all users with equal service quality, we have implemented an “API calls system,” which functions as a currency for each API request. This system includes two types of limits: the Minute Request Limit and the Daily Call Limit.\n\n\n## Daily API Limit (calls)\n\nAn API request is not the same as an API call; API calls are a form of “currency” used to make requests. Requests for different data consume a different number of API calls. For example, Fundamental data request costs 10 API calls, while Live data request for 1 ticker costs 1 API call.\n\nCurrent API call consumption could be checked in user dashboard.\n\n## Daily Limit Increase\n\nTo increase the API call daily limit (100,000 by default) for a subscription plan, navigate to the “Daily Usage” section in the dashboard and select the “Increase Daily Limit” option. Here, you can view the price of the upgrade and submit a request to our support team with your order:\n\nCurrently, we don’t offer an option to increase the daily limit for marketplace products. If you have a specific case, please contact our support team.\n\nFeel free to chat with our support, if you have any questions.\n\n## Minute Limit (requests)\n\nMinute request limit (not API calls) means that API is restricted to no more than 1000 requests per minute. It’s easy to check this limit with headers you get with every request:\n\nIt is advisable to spread out the requests more or less evenly throughout the minute, without making them go off all at once, to avoid getting a “Too Many Requests” error.\n\n## Extra API Calls\n\nYou can purchase additional API calls, which will only be used once your daily API limit is exhausted, functioning as a buffer. These additional API calls do not expire and can be accumulated by purchasing more as needed. To buy extra calls, find the form titled ‘Buy Extra API Calls’ on your dashboard page.\n\n## API Usage Statistics\n\nTo check your account’s usage statistics go to https://eodhd.com/cp/api\n\nTo adjust the view of your API usage chart, you can select the period and type of API requests. The number displayed on the chart indicates how many times you have called the API.\n\nTo calculate how this has impacted your API limit, you need to multiply the number of calls by the cost per API request. For example, each intraday API call consumes 5 limit units (you can check the cost of each call on the documentation page for that particular API).\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "api-limits"
---

# API Limits: calls, requests, consumption

## 源URL

https://eodhd.com/financial-apis/api-limits/

## 描述

To ensure the stability of our data servers and provide all users with equal service quality, we have implemented an “API calls system,” which functions as a currency for each API request. This system includes two types of limits: the Minute Request Limit and the Daily Call Limit.

## 文档正文

To ensure the stability of our data servers and provide all users with equal service quality, we have implemented an “API calls system,” which functions as a currency for each API request. This system includes two types of limits: the Minute Request Limit and the Daily Call Limit.

## Daily API Limit (calls)

An API request is not the same as an API call; API calls are a form of “currency” used to make requests. Requests for different data consume a different number of API calls. For example, Fundamental data request costs 10 API calls, while Live data request for 1 ticker costs 1 API call.

Current API call consumption could be checked in user dashboard.

## Daily Limit Increase

To increase the API call daily limit (100,000 by default) for a subscription plan, navigate to the “Daily Usage” section in the dashboard and select the “Increase Daily Limit” option. Here, you can view the price of the upgrade and submit a request to our support team with your order:

Currently, we don’t offer an option to increase the daily limit for marketplace products. If you have a specific case, please contact our support team.

Feel free to chat with our support, if you have any questions.

## Minute Limit (requests)

Minute request limit (not API calls) means that API is restricted to no more than 1000 requests per minute. It’s easy to check this limit with headers you get with every request:

It is advisable to spread out the requests more or less evenly throughout the minute, without making them go off all at once, to avoid getting a “Too Many Requests” error.

## Extra API Calls

You can purchase additional API calls, which will only be used once your daily API limit is exhausted, functioning as a buffer. These additional API calls do not expire and can be accumulated by purchasing more as needed. To buy extra calls, find the form titled ‘Buy Extra API Calls’ on your dashboard page.

## API Usage Statistics

To check your account’s usage statistics go to https://eodhd.com/cp/api

To adjust the view of your API usage chart, you can select the period and type of API requests. The number displayed on the chart indicates how many times you have called the API.

To calculate how this has impacted your API limit, you need to multiply the number of calls by the cost per API request. For example, each intraday API call consumes 5 limit units (you can check the cost of each call on the documentation page for that particular API).

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
