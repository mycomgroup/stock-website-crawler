---
id: "url-3eabcac5"
type: "api"
title: "Bulk API for EOD, Splits and Dividends"
url: "https://eodhd.com/financial-apis/bulk-api-eod-splits-dividends/"
description: "This API allows to easily download the data for the entire exchange for a particular day. It works for end-of-day historical data feed as well as for splits and dividends data. For US tickers you can also use NYSE, NASDAQ, BATS, or AMEX as exchange symbols to get data only for NYSE or only for NASDAQ exchange."
source: ""
tags: []
crawl_time: "2026-03-18T06:17:00.087Z"
metadata:
  endpoint: "https://eodhd.com/api/eod-bulk-last-day/US"
  parameters: []
  markdownContent: "# Bulk API for EOD, Splits and Dividends\n\nThis API allows to easily download the data for the entire exchange for a particular day. It works for end-of-day historical data feed as well as for splits and dividends data. For US tickers you can also use NYSE, NASDAQ, BATS, or AMEX as exchange symbols to get data only for NYSE or only for NASDAQ exchange.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/eod-bulk-last-day/US?api_token={YOUR_API_TOKEN}\n```\n\n```text\nhttps://eodhd.com/api/eod-bulk-last-day/US?api_token={YOUR_API_TOKEN}&type=splits\n```\n\n```text\nhttps://eodhd.com/api/eod-bulk-last-day/US?api_token={YOUR_API_TOKEN}&type=dividends\n```\n\n\n## General bulk (batch) API for EOD, Splits, and Dividends\n\nThe following example returns end-of-day data for US stocks in bulk for a particular day:\n\nThe following example returns all splits for US stocks in bulk for a particular day:\n\nThe following example returns all dividends for US stocks in bulk for a particular day:\n\nPlease note: similar to the historical dividends API, the extended format of output is available in JSON format (&fmt=json), while CSV format (&fmt=csv, default one) supports fewer fields.\n\nThe “symbols” parameter does not work for splits and dividends.\n\n## Additional parameters\n\nBy default, the data for last trading day will be downloaded, but if you need any specific date, add ‘date’ parameter to the URL, in the following example we used September 21, 2017:\n\nTo download last day data for several symbols, for example, for MSFT and AAPL, you can add the ‘symbols’ parameter. For non-US tickers, you should use the exchange code, for example, BMW.XETRA or SAP.F:\n\nAnd, of course, we support JSON output for this API endpoint, to get it, add: “fmt=json”:\n\nIf you need more data, like company name, you can use ‘&filter=extended’ and get an extended dataset, which includes the company name, EMA 50 and EMA 200, and average volumes for 14, 50, and 200 days. The data is available only for the past 30 days, if you need deeper, you should use our Technical API. The data is accessible in both CSV and JSON formats:\n\nWe have API limits 100 000 requests per day. Each symbol request costs 1 API call. For example, multiple tickers request with ten symbols costs 110 API calls; however entire exchange request costs 100 API calls.\n\nThanks! And please connect with us via support@eodhistoricaldata.com if you have further questions.\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "bulk-api-eod-splits-dividends"
---

# Bulk API for EOD, Splits and Dividends

## 源URL

https://eodhd.com/financial-apis/bulk-api-eod-splits-dividends/

## 描述

This API allows to easily download the data for the entire exchange for a particular day. It works for end-of-day historical data feed as well as for splits and dividends data. For US tickers you can also use NYSE, NASDAQ, BATS, or AMEX as exchange symbols to get data only for NYSE or only for NASDAQ exchange.

## API 端点

**Endpoint**: `https://eodhd.com/api/eod-bulk-last-day/US`

## 文档正文

This API allows to easily download the data for the entire exchange for a particular day. It works for end-of-day historical data feed as well as for splits and dividends data. For US tickers you can also use NYSE, NASDAQ, BATS, or AMEX as exchange symbols to get data only for NYSE or only for NASDAQ exchange.

## API Endpoint

```text
https://eodhd.com/api/eod-bulk-last-day/US?api_token={YOUR_API_TOKEN}
```

```text
https://eodhd.com/api/eod-bulk-last-day/US?api_token={YOUR_API_TOKEN}&type=splits
```

```text
https://eodhd.com/api/eod-bulk-last-day/US?api_token={YOUR_API_TOKEN}&type=dividends
```

## General bulk (batch) API for EOD, Splits, and Dividends

The following example returns end-of-day data for US stocks in bulk for a particular day:

The following example returns all splits for US stocks in bulk for a particular day:

The following example returns all dividends for US stocks in bulk for a particular day:

Please note: similar to the historical dividends API, the extended format of output is available in JSON format (&fmt=json), while CSV format (&fmt=csv, default one) supports fewer fields.

The “symbols” parameter does not work for splits and dividends.

## Additional parameters

By default, the data for last trading day will be downloaded, but if you need any specific date, add ‘date’ parameter to the URL, in the following example we used September 21, 2017:

To download last day data for several symbols, for example, for MSFT and AAPL, you can add the ‘symbols’ parameter. For non-US tickers, you should use the exchange code, for example, BMW.XETRA or SAP.F:

And, of course, we support JSON output for this API endpoint, to get it, add: “fmt=json”:

If you need more data, like company name, you can use ‘&filter=extended’ and get an extended dataset, which includes the company name, EMA 50 and EMA 200, and average volumes for 14, 50, and 200 days. The data is available only for the past 30 days, if you need deeper, you should use our Technical API. The data is accessible in both CSV and JSON formats:

We have API limits 100 000 requests per day. Each symbol request costs 1 API call. For example, multiple tickers request with ten symbols costs 110 API calls; however entire exchange request costs 100 API calls.

Thanks! And please connect with us via support@eodhistoricaldata.com if you have further questions.

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
