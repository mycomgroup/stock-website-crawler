---
id: "url-24720d8e"
type: "api"
title: "R Library v.2 for Financial Data (2024)"
url: "https://eodhd.com/financial-apis/r-library-v-2-for-financial-data-by-eodhd-2024"
description: "In addition to our previous official R library we are proud to present to you second version of a library (eodhdR2) made by independent developer Prof. Marcelo S. Perlin."
source: ""
tags: []
crawl_time: "2026-03-18T09:23:55.800Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# R Library v.2 for Financial Data (2024)\n\nIn addition to our previous official R library we are proud to present to you second version of a library (eodhdR2) made by independent developer Prof. Marcelo S. Perlin.\n\n\n## Installation and examples\n\nFirst things first, ensure you have R and RStudio installed on your machine. RStudio is an integrated development environment (IDE) that makes working with R more convenient. The suggested steps are:\n\nFeel free to visit our Github page to subscribe to receive notifications about future updates for he R library.\n\n## R library installation process\n\nThis command will install all dependencies of the package. This might take a while depending on your internet connection and hardware.\n\nIf you are able to execute the previous code without error, then the package was installed correctly and you’re good to go. The next step is activating the API with a valid token, and executing the code examples.\n\n## Activating the API\n\nIf you haven’t done so, register a new account at https://eodhd.com/. Once you done that, head out to https://eodhd.com/cp/dashboard and search for your unique API Token. This token is attached to your data subscription. If you only subscribed to fundamentals, it will not work for other types of data. We recommend exploring our plans, starting from $19.99, to access the necessary type of API without limitations.\n\nWhile using eodhdR2, all authentications are managed with function eodhdR2::set_token():\n\nAlternatively, EODHD offers a DEMO API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. We recommend you test your access to the API with the demo token:\n\neodhd API token set\n\nAccount name: API Documentation 2 (supportlevel1@eodhistoricaldata.com)\n\nQuota: 88838 | 10000000\n\nSubscription: demo\n\nYou are using a **DEMONSTRATION** token for testing pourposes, with limited access to the data repositories. See <https://eodhd.com/> for registration and, after finding your token, use it with function eodhdR2::set_token(“TOKEN”).\n\n## Getting Help\n\nTo access all information about a specific function, you can use the help command:\n\nExample of help for function get_prices():\n\n## List of the available functions\n\nFor testing all functions, except, get_exchanges() and get_ticker(), you can use the demo token. Make sure to register it in your R session before executing the code. The instruction are available in previous section Activating the API.\n\nget_demo_token: Returns the demo token\n\nget_dividends: Returns dividend history for a given ticker and exchange.\n\nget_exchanges: Returns the list of available exchanges. Be aware you need a non-demo token for this function.\n\nget_fundamentals: imports fundamental data from eodhd.\n\nget_prices: Imports daily adjusted/unadjusted prices trading volumes from eodhd.\n\nget_splits: retrieves split data from eodhd.\n\nget_tickers: retrieves a list of tickers for a particular exchange. Be aware you need a non-demo token for this function.\n\nparse_financials: organizes financial data imported using get_fundamentals(). The output is a dataframe in the long/wide format.\n\nset_token: authenticates R session with eodhd by setting a token in registry\n\n## Testing for AAPL ticker\n\nThese are examples of using eodhdR2 for APPLE INC (AAPL), which trades on the US exchange. These requests are done with “demo” token.\n\n## Retrieving Financial Prices\n\n── retrieving price data for ticker AAPL|US─────────────────────! Quota status: 89475|10000000, refreshing in 3.72 hours cache file ‘/tmp/RtmpyEk3VW/eodhdR2-cache/AAPL_US_eodhd_prices.rds’ saved got 11008 rows of prices got daily data from 1980-12-12 to 2024-08-13\n\nNow, let’s use ggplot2 to make a plot of the price series for the past five years:\n\n## Retrieving Dividends\n\nWe can also import the dividend history of APPLE INC.\n\n── retrieving dividends for ticker AAPL|US──! Quota status: 89478|10000000, refreshing in 3.72 hours cache file ‘/tmp/RtmpyEk3VW/eodhdR2-cache/AAPL_US_eodhd_dividends.rds’ saved got 84 rows of dividend data\n\nAgain, lets plot the dividend history since 2019-08-15:\n\n## Retrieving Fundamentals\n\nWe can use the same interface for fetching fundamental data from the EODHD endpoint.\n\n── retrieving fundamentals for ticker AAPL|US──! Quota status: 89480|10000000, refreshing in 3.72 hours querying API got 13 elements in raw list\n\n[1] “General” “Highlights” “Valuation”\n\n[4] “SharesStats” “Technicals” “SplitsDividends”\n\n[7] “AnalystRatings” “Holders” “InsiderTransactions”\n\n[10] “ESGScores” “outstandingShares” “Earnings”\n\n[13] “Financials”\n\n## Parsing financials\n\nWe can also use package eodhdR2 for parsing (organizing) the financial data from the raw output.\n\n── Parsing financial data for Apple Inc | AAPL ── parsing Balance_Sheet data quarterly yearly parsing Cash_Flow data quarterly yearly parsing Income_Statement data quarterly yearly got 67680 rows of financial data (long format)\n\n## The last quarterly Balance Sheet of AAPL\n\nNow that we have the financial data, let’s build a simple report of the last quarterly balance sheet of AAPL:\n\n## Code Examples\n\n```text\n# stable version available at CRAN\ninstall.package(\"eodhdR2\")\n\n# development version\nif (!require(devtools)) install.packages(\"devtools\")\ndevtools::install_github(\"EodHistoricalData/R-Library-for-financial-data-2024\")\n```\n\n```text\nlibrary(eodhdR2)\n```\n\n```text\n# set your own token\neodhdR2::set_token(\"YOUR_TOKEN\")\n```\n\n```text\ntoken <- eodhdR2::get_demo_token() \neodhdR2::set_token(token)\n```\n\n```text\nhelp(get_prices)\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "r-library-v-2-for-financial-data-by-eodhd-2024"
---

# R Library v.2 for Financial Data (2024)

## 源URL

https://eodhd.com/financial-apis/r-library-v-2-for-financial-data-by-eodhd-2024

## 描述

In addition to our previous official R library we are proud to present to you second version of a library (eodhdR2) made by independent developer Prof. Marcelo S. Perlin.

## 文档正文

In addition to our previous official R library we are proud to present to you second version of a library (eodhdR2) made by independent developer Prof. Marcelo S. Perlin.

## Installation and examples

First things first, ensure you have R and RStudio installed on your machine. RStudio is an integrated development environment (IDE) that makes working with R more convenient. The suggested steps are:

Feel free to visit our Github page to subscribe to receive notifications about future updates for he R library.

## R library installation process

This command will install all dependencies of the package. This might take a while depending on your internet connection and hardware.

If you are able to execute the previous code without error, then the package was installed correctly and you’re good to go. The next step is activating the API with a valid token, and executing the code examples.

## Activating the API

If you haven’t done so, register a new account at https://eodhd.com/. Once you done that, head out to https://eodhd.com/cp/dashboard and search for your unique API Token. This token is attached to your data subscription. If you only subscribed to fundamentals, it will not work for other types of data. We recommend exploring our plans, starting from $19.99, to access the necessary type of API without limitations.

While using eodhdR2, all authentications are managed with function eodhdR2::set_token():

Alternatively, EODHD offers a DEMO API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. We recommend you test your access to the API with the demo token:

eodhd API token set

Account name: API Documentation 2 (supportlevel1@eodhistoricaldata.com)

Quota: 88838 | 10000000

Subscription: demo

You are using a **DEMONSTRATION** token for testing pourposes, with limited access to the data repositories. See <https://eodhd.com/> for registration and, after finding your token, use it with function eodhdR2::set_token(“TOKEN”).

## Getting Help

To access all information about a specific function, you can use the help command:

Example of help for function get_prices():

## List of the available functions

For testing all functions, except, get_exchanges() and get_ticker(), you can use the demo token. Make sure to register it in your R session before executing the code. The instruction are available in previous section Activating the API.

get_demo_token: Returns the demo token

get_dividends: Returns dividend history for a given ticker and exchange.

get_exchanges: Returns the list of available exchanges. Be aware you need a non-demo token for this function.

get_fundamentals: imports fundamental data from eodhd.

get_prices: Imports daily adjusted/unadjusted prices trading volumes from eodhd.

get_splits: retrieves split data from eodhd.

get_tickers: retrieves a list of tickers for a particular exchange. Be aware you need a non-demo token for this function.

parse_financials: organizes financial data imported using get_fundamentals(). The output is a dataframe in the long/wide format.

set_token: authenticates R session with eodhd by setting a token in registry

## Testing for AAPL ticker

These are examples of using eodhdR2 for APPLE INC (AAPL), which trades on the US exchange. These requests are done with “demo” token.

## Retrieving Financial Prices

── retrieving price data for ticker AAPL|US─────────────────────! Quota status: 89475|10000000, refreshing in 3.72 hours cache file ‘/tmp/RtmpyEk3VW/eodhdR2-cache/AAPL_US_eodhd_prices.rds’ saved got 11008 rows of prices got daily data from 1980-12-12 to 2024-08-13

Now, let’s use ggplot2 to make a plot of the price series for the past five years:

## Retrieving Dividends

We can also import the dividend history of APPLE INC.

── retrieving dividends for ticker AAPL|US──! Quota status: 89478|10000000, refreshing in 3.72 hours cache file ‘/tmp/RtmpyEk3VW/eodhdR2-cache/AAPL_US_eodhd_dividends.rds’ saved got 84 rows of dividend data

Again, lets plot the dividend history since 2019-08-15:

## Retrieving Fundamentals

We can use the same interface for fetching fundamental data from the EODHD endpoint.

── retrieving fundamentals for ticker AAPL|US──! Quota status: 89480|10000000, refreshing in 3.72 hours querying API got 13 elements in raw list

[1] “General” “Highlights” “Valuation”

[4] “SharesStats” “Technicals” “SplitsDividends”

[7] “AnalystRatings” “Holders” “InsiderTransactions”

[10] “ESGScores” “outstandingShares” “Earnings”

[13] “Financials”

## Parsing financials

We can also use package eodhdR2 for parsing (organizing) the financial data from the raw output.

── Parsing financial data for Apple Inc | AAPL ── parsing Balance_Sheet data quarterly yearly parsing Cash_Flow data quarterly yearly parsing Income_Statement data quarterly yearly got 67680 rows of financial data (long format)

## The last quarterly Balance Sheet of AAPL

Now that we have the financial data, let’s build a simple report of the last quarterly balance sheet of AAPL:

## Code Examples

```text
# stable version available at CRAN
install.package("eodhdR2")

# development version
if (!require(devtools)) install.packages("devtools")
devtools::install_github("EodHistoricalData/R-Library-for-financial-data-2024")
```

```text
library(eodhdR2)
```

```text
# set your own token
eodhdR2::set_token("YOUR_TOKEN")
```

```text
token <- eodhdR2::get_demo_token() 
eodhdR2::set_token(token)
```

```text
help(get_prices)
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
