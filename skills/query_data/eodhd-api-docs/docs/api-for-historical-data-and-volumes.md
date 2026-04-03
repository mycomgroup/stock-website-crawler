---
id: "url-65bfeb4f"
type: "api"
title: "End-Of-Day Historical Stock Market Data API"
url: "https://eodhd.com/financial-apis/api-for-historical-data-and-volumes"
description: "With End-of-Day data API, we have data for more than 150 000 tickers all around the world. We cover all US stocks, ETFs, and Mutual Funds (more than 51 000 in total) from the beginning, for example, the Ford Motors data is from Jun 1972 and so on. And non-US stock exchanges we cover mostly from Jan 3, 2000. We do provide daily, weekly and monthly data raw and adjusted to splits and dividends."
source: ""
tags: []
crawl_time: "2026-03-18T04:38:17.166Z"
metadata:
  endpoint: "https://eodhd.com/api/eod/MCD.US"
  parameters: []
  markdownContent: "# End-Of-Day Historical Stock Market Data API\n\nWith End-of-Day data API, we have data for more than 150 000 tickers all around the world. We cover all US stocks, ETFs, and Mutual Funds (more than 51 000 in total) from the beginning, for example, the Ford Motors data is from Jun 1972 and so on. And non-US stock exchanges we cover mostly from Jan 3, 2000. We do provide daily, weekly and monthly data raw and adjusted to splits and dividends.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/eod/MCD.US?api_token=demo&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/eod/MCD.US?period=d&api_token=demo&fmt=csv\n```\n\n```text\nhttps://eodhd.com/api/eod/MCD.US?from=2020-01-05&to=2020-02-10&period=d&api_token=demo&fmt=json\n```\n\n\n## Quick Start\n\nTo get historical stock price data use the following URL:\n\nFor testing purposes, you can try the following API Key (works only for MCD.US ticker):  demo\n\nAs a result, you will get the following data in CSV format:\n\n## Daily Updates API\n\nFor daily updates on your end-of-day data, we recommend a special Bulk API for EOD, Splits and Dividends. With this API you will be able to download the data for a particular day for the entire exchange in seconds. Even to download the entire US exchange with more than 45,000 active tickers, you will need 1 API request and 5-10 seconds.\n\n## Stock Prices Data API with Dates Support\n\nWe support two formats for historical data dates.\n\n## EOD Historical Data\n\nHere you can use ‘from’ and ‘to’ parameters with the format ‘YYYY-MM-DD’. For example, if you need to get data only from Jan 5, 2017, to Feb 10, 2017, you need to use from=2017-01-05 and to=2017-02-10. Then the final URL will be:\n\n## Filter fields. WEBSERVICE and YAHOO Support\n\nWe also support ‘=WEBSERVICE’ Excel function, to get only the last value, just add ‘filter=last_close’ or ‘filter=last_volume’ with ‘fmt=json’ and you will get only one number which perfectly works with WEBSERVICE function. For example, with this URL:\n\nYou will get one value – the last price for MCD.\n\n## Yahoo Finance API Support\n\nTo support clients who used Yahoo Finance service non-official API which doesn’t work now (URL: ichart.finance.yahoo.com), we also support yahoo-style for dates. Here there will be 6 parameters.\n\nBE CAREFUL, date used here in American notation: MONTH, DAY, YEAR.\n\nAnd the final URL will be:\n\nWe hope it will be very useful for you.\n\n## JSON Output Support\n\nWe support JSON output as well if you need it for your PHP, Python, Java, or Perl applications. All you need is to add a special parameter: “fmt=json” to your query, then the final query will be:\n\nJSON output doesn’t work for Yahoo-like style.\n\nWe have API limits 100 000 requests per day. Each symbol request costs 1 API call.\n\n## End Of Day Historical Prices Update Time\n\nWe update each stock exchange 2-3 hours after the market closes. But except for major US exchanges (NYSE, NASDAQ), these exchanges are updated next 15 minutes after the market closes. However US mutual funds, PINK, OTCBB, and some indices do update only the next morning, the update starts at 3-4 am EST and usually ends at 5-6 am EST. For these types of symbols, we always get ‘updated price’ up to 3-4 am.\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "api-for-historical-data-and-volumes"
---

# End-Of-Day Historical Stock Market Data API

## 源URL

https://eodhd.com/financial-apis/api-for-historical-data-and-volumes

## 描述

With End-of-Day data API, we have data for more than 150 000 tickers all around the world. We cover all US stocks, ETFs, and Mutual Funds (more than 51 000 in total) from the beginning, for example, the Ford Motors data is from Jun 1972 and so on. And non-US stock exchanges we cover mostly from Jan 3, 2000. We do provide daily, weekly and monthly data raw and adjusted to splits and dividends.

## API 端点

**Endpoint**: `https://eodhd.com/api/eod/MCD.US`

## 文档正文

With End-of-Day data API, we have data for more than 150 000 tickers all around the world. We cover all US stocks, ETFs, and Mutual Funds (more than 51 000 in total) from the beginning, for example, the Ford Motors data is from Jun 1972 and so on. And non-US stock exchanges we cover mostly from Jan 3, 2000. We do provide daily, weekly and monthly data raw and adjusted to splits and dividends.

## API Endpoint

```text
https://eodhd.com/api/eod/MCD.US?api_token=demo&fmt=json
```

```text
https://eodhd.com/api/eod/MCD.US?period=d&api_token=demo&fmt=csv
```

```text
https://eodhd.com/api/eod/MCD.US?from=2020-01-05&to=2020-02-10&period=d&api_token=demo&fmt=json
```

## Quick Start

To get historical stock price data use the following URL:

For testing purposes, you can try the following API Key (works only for MCD.US ticker):  demo

As a result, you will get the following data in CSV format:

## Daily Updates API

For daily updates on your end-of-day data, we recommend a special Bulk API for EOD, Splits and Dividends. With this API you will be able to download the data for a particular day for the entire exchange in seconds. Even to download the entire US exchange with more than 45,000 active tickers, you will need 1 API request and 5-10 seconds.

## Stock Prices Data API with Dates Support

We support two formats for historical data dates.

## EOD Historical Data

Here you can use ‘from’ and ‘to’ parameters with the format ‘YYYY-MM-DD’. For example, if you need to get data only from Jan 5, 2017, to Feb 10, 2017, you need to use from=2017-01-05 and to=2017-02-10. Then the final URL will be:

## Filter fields. WEBSERVICE and YAHOO Support

We also support ‘=WEBSERVICE’ Excel function, to get only the last value, just add ‘filter=last_close’ or ‘filter=last_volume’ with ‘fmt=json’ and you will get only one number which perfectly works with WEBSERVICE function. For example, with this URL:

You will get one value – the last price for MCD.

## Yahoo Finance API Support

To support clients who used Yahoo Finance service non-official API which doesn’t work now (URL: ichart.finance.yahoo.com), we also support yahoo-style for dates. Here there will be 6 parameters.

BE CAREFUL, date used here in American notation: MONTH, DAY, YEAR.

And the final URL will be:

We hope it will be very useful for you.

## JSON Output Support

We support JSON output as well if you need it for your PHP, Python, Java, or Perl applications. All you need is to add a special parameter: “fmt=json” to your query, then the final query will be:

JSON output doesn’t work for Yahoo-like style.

We have API limits 100 000 requests per day. Each symbol request costs 1 API call.

## End Of Day Historical Prices Update Time

We update each stock exchange 2-3 hours after the market closes. But except for major US exchanges (NYSE, NASDAQ), these exchanges are updated next 15 minutes after the market closes. However US mutual funds, PINK, OTCBB, and some indices do update only the next morning, the update starts at 3-4 am EST and usually ends at 5-6 am EST. For these types of symbols, we always get ‘updated price’ up to 3-4 am.

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
