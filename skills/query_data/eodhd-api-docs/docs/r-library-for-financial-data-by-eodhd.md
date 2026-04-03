---
id: "url-2e719a4f"
type: "api"
title: "R Library for Financial Data"
url: "https://eodhd.com/financial-apis/r-library-for-financial-data-by-eodhd"
description: "Important! Since we have introduced a new version of the R library for EODHD functions, the current library is no longer supported on CRAN and has been replaced by the new library (eodhdR2). The current library is still available via our GitHub."
source: ""
tags: []
crawl_time: "2026-03-18T04:40:04.234Z"
metadata:
  endpoint: ""
  parameters:
    - {"name":"Live (Delayed) Stock Prices and Macroeconomic Data (doc)","description":"get_live_stock_prices <- function(api_token, ticker, s = NULL)"}
    - {"name":"Bonds Fundamentals (doc)","description":"get_bonds_fundamentals_data( api_token <- \"demo\", isin <- \"DE000CB83CF0\" )"}
    - {"name":"Intraday Historical Data (doc)","description":"get_intraday_historical_data( api_token <- \"YOUR_API_TOKEN\", interval <- \"5m\", from_unix_time <- \"1627896900\", to_unix_time <- \"1630575300\", symbol <- \"AAPL.MX\")"}
    - {"name":"Historical Dividends (doc)","description":"get_historical_dividends_data( api_token <- \"demo\", ticker <- \"AAPL.US\", date_from <- \"2017-09-10\", date_to <- \"2017-09-12\" )"}
    - {"name":"Historical Splits (doc)","description":"get_historical_splits_data( api_token <- \"demo\",  ticker <- \"AAPL.US\",  date_from <- \"2017-09-10\", date_to <- \"2017-09-12\" )"}
    - {"name":"Bulk API for EOD, Splits and Dividends (doc)","description":"get_bulk_eod_splits_dividends_data( api_token = \"demo\", country = 'US', type = 'splits', date = \"2010-09-21\", symbols = \"MSFT\", filter = \"extended\" )"}
    - {"name":"Calendar. Upcoming Earnings, Trends, IPOs and Splits (doc)","description":"get_upcoming_earnings_data( api_token <- \"demo\", from_date <- \"2017-09-10\", to_date <- \"2017-09-12\", symbols <- \"AAPL\" )get_earning_trends_data(  api_token = \"demo\",  symbols = \"AAPL.US\" ) # for Earnings trendsget_upcoming_IPOs_data( api_token <- \"YOUR_API_TOKEN\", from_date <- \"2017-09-10\", to_date <- \"2017-09-12\" ) # for upcoming IPOsget_upcoming_splits_data( api_token <- \"YOUR_API_TOKEN\", from_date <- \"2017-09-10\", to_date <- \"2017-09-12\" ) # for upcoming splits"}
    - {"name":"Economic Events (doc)","description":"get_economic_events_data( api_token <- \"demo\", date_from <- \"2017-09-10\", date_to <- \"2017-09-12\", country <- \"US\", comparison <- \"qoq\", offset <- \"0\", limit <- \"50\" )"}
    - {"name":"Stock Market and Financial News (doc)","description":"financial_news( api_token <- \"demo\", s <- \"balance sheet\", t <- NULL, from_date <- \"2017-09-10\", to_date <- \"2017-09-12\", limit <- \"50\", offset <- \"100\" )"}
    - {"name":"End of the Day Historical Stock Market Data (doc)","description":"get_eod_historical_stock_market_data <- function( api_token, symbol, from_date = NULL,to_date = NULL, period = 'd', order = 'a' )"}
    - {"name":"List of supported Exchanges (doc)","description":"get_list_of_exchanges( api_token <- \"demo\" )"}
    - {"name":"Insider Transactions (doc)","description":"get_insider_transactions_data( api_token <- \"demo\", date_from <- \"2017-09-10\", date_to <- \"2017-09-12\", code <- \"AAPL.US\", limit <- \"150\" )"}
    - {"name":"Macro Indicators (doc)","description":"get_macro_indicators_data( api_token <- \"YOUR_API_TOKEN\", country <- \"USA\", indicator <- \"gdp_current_usd\" )"}
    - {"name":"Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History (doc)","description":"get_details_trading_hours_stock_market_holidays( api_token <- \"YOUR_API_TOKEN\", code <- \"US\", from_date <- \"2017-09-10\", to_date <- \"2017-09-12\") symbol_change_history(api_token <- \"YOUR_API_TOKEN\", from_date <- \"2023-01-01\", to_date <- \"2023-12-31\" )"}
    - {"name":"Stock Market Screener (doc)","description":"stock_market_screener( api_token <- \"YOUR_API_TOKEN\",  sort <- \"market_capitalization.desc\", filters <- NULL, limit <- \"1\", signals <- \"bookvalue_neg\", offset <- \"50\" )"}
    - {"name":"Technical Indicator (doc)","description":"get_technical_indicator_data( api_token <- \"demo\", ticker <- \"AAPL.US\", func <- \"slope\", period <- 100 )"}
    - {"name":"Historical Market Capitalization (doc)","description":"get_historical_market_capitalization_data <- function( api_token, ticker,from_date = NULL,to_date = NULL )"}
    - {"name":"Fundamental Data: Stocks, ETFs, Mutual Funds, Indices and Cryptocurrencies (doc)","description":"get_fundamentals_data( api_token <- \"demo\", ticker <- \"AAPL.US\" )"}
  markdownContent: "# R Library for Financial Data\n\nImportant! Since we have introduced a new version of the R library for EODHD functions, the current library is no longer supported on CRAN and has been replaced by the new library (eodhdR2). The current library is still available via our GitHub.\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| Live (Delayed) Stock Prices and Macroeconomic Data (doc) | get_live_stock_prices <- function(api_token, ticker, s = NULL) |\n| Bonds Fundamentals (doc) | get_bonds_fundamentals_data( api_token <- \"demo\", isin <- \"DE000CB83CF0\" ) |\n| Intraday Historical Data (doc) | get_intraday_historical_data( api_token <- \"YOUR_API_TOKEN\", interval <- \"5m\", from_unix_time <- \"1627896900\", to_unix_time <- \"1630575300\", symbol <- \"AAPL.MX\") |\n| Historical Dividends (doc) | get_historical_dividends_data( api_token <- \"demo\", ticker <- \"AAPL.US\", date_from <- \"2017-09-10\", date_to <- \"2017-09-12\" ) |\n| Historical Splits (doc) | get_historical_splits_data( api_token <- \"demo\",  ticker <- \"AAPL.US\",  date_from <- \"2017-09-10\", date_to <- \"2017-09-12\" ) |\n| Bulk API for EOD, Splits and Dividends (doc) | get_bulk_eod_splits_dividends_data( api_token = \"demo\", country = 'US', type = 'splits', date = \"2010-09-21\", symbols = \"MSFT\", filter = \"extended\" ) |\n| Calendar. Upcoming Earnings, Trends, IPOs and Splits (doc) | get_upcoming_earnings_data( api_token <- \"demo\", from_date <- \"2017-09-10\", to_date <- \"2017-09-12\", symbols <- \"AAPL\" )get_earning_trends_data(  api_token = \"demo\",  symbols = \"AAPL.US\" ) # for Earnings trendsget_upcoming_IPOs_data( api_token <- \"YOUR_API_TOKEN\", from_date <- \"2017-09-10\", to_date <- \"2017-09-12\" ) # for upcoming IPOsget_upcoming_splits_data( api_token <- \"YOUR_API_TOKEN\", from_date <- \"2017-09-10\", to_date <- \"2017-09-12\" ) # for upcoming splits |\n| Economic Events (doc) | get_economic_events_data( api_token <- \"demo\", date_from <- \"2017-09-10\", date_to <- \"2017-09-12\", country <- \"US\", comparison <- \"qoq\", offset <- \"0\", limit <- \"50\" ) |\n| Stock Market and Financial News (doc) | financial_news( api_token <- \"demo\", s <- \"balance sheet\", t <- NULL, from_date <- \"2017-09-10\", to_date <- \"2017-09-12\", limit <- \"50\", offset <- \"100\" ) |\n| End of the Day Historical Stock Market Data (doc) | get_eod_historical_stock_market_data <- function( api_token, symbol, from_date = NULL,to_date = NULL, period = 'd', order = 'a' ) |\n| List of supported Exchanges (doc) | get_list_of_exchanges( api_token <- \"demo\" ) |\n| Insider Transactions (doc) | get_insider_transactions_data( api_token <- \"demo\", date_from <- \"2017-09-10\", date_to <- \"2017-09-12\", code <- \"AAPL.US\", limit <- \"150\" ) |\n| Macro Indicators (doc) | get_macro_indicators_data( api_token <- \"YOUR_API_TOKEN\", country <- \"USA\", indicator <- \"gdp_current_usd\" ) |\n| Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History (doc) | get_details_trading_hours_stock_market_holidays( api_token <- \"YOUR_API_TOKEN\", code <- \"US\", from_date <- \"2017-09-10\", to_date <- \"2017-09-12\") symbol_change_history(api_token <- \"YOUR_API_TOKEN\", from_date <- \"2023-01-01\", to_date <- \"2023-12-31\" ) |\n| Stock Market Screener (doc) | stock_market_screener( api_token <- \"YOUR_API_TOKEN\",  sort <- \"market_capitalization.desc\", filters <- NULL, limit <- \"1\", signals <- \"bookvalue_neg\", offset <- \"50\" ) |\n| Technical Indicator (doc) | get_technical_indicator_data( api_token <- \"demo\", ticker <- \"AAPL.US\", func <- \"slope\", period <- 100 ) |\n| Historical Market Capitalization (doc) | get_historical_market_capitalization_data <- function( api_token, ticker,from_date = NULL,to_date = NULL ) |\n| Fundamental Data: Stocks, ETFs, Mutual Funds, Indices and Cryptocurrencies (doc) | get_fundamentals_data( api_token <- \"demo\", ticker <- \"AAPL.US\" ) |\n\n\n## Installation and examples\n\nFirst things first, ensure you have R and RStudio installed on your machine. RStudio is an integrated development environment (IDE) that makes working with R more convinient. You can download R from CRAN and RStudio from RStudio’s official website. Following guide will be based on RStudio.\n\nRequired Environment:\n\nFeel free to visit our Github page to subscribe to receive notifications about future updates for R library.\n\n## R library installation process\n\n1. Installing the library. Type the following command and hit Enter:\n\nSee the screenshot:\n\n2. Library Import. Next, let’s import EODHD library for accessing EODHD API’s functions:\n\nSee the screenshot:\n\nR Financial Library is installed now. Next, we are going to activate EODHD’s API key to get an access to data.\n\n## API access activation: free and payed options\n\n1. You can start with “DEMO” API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. For these tickers, all of our APIs, including Real-Time Data, are availible without limitations.2. Register for the free plan to receive your API key (limited to 20 API calls per day) with access to End-Of-Day Historical Stock Market Data API for any ticker, but within the past year only. Plus a List of tickers per Exchange is availible.3. We recommend exploring our plans, starting from $19.99, to access the necessary type of API without limitations.\n\nOnce you have EODHD API key, you can set it in an additional file, for example “key.R”:\n\nTo implement the “key.R” file in your code:\n\nOr set the type as an argument for the function:\n\nHaving implemented an active API key, we are ready to call for data.\n\n## Information about a function\n\nTo access all information about a specific function, you can use the help command:\n\nSee the example:\n\nScroll down to the end of this guide to see all availible functions.\n\n## Example: End of the day historical stock market data\n\nLets call for End of the day historical stock market data:\n\nSee the example:\n\nThe function will return the following JSON respond:\n\nAll the parameters for this function are listed and described here.\n\n## List of the available functions\n\nBelow is the list of functions to retrieve various data, including code examples and links to documentation containing descriptions of all parameters:\n\n## Direct EODHD request call in R enviroment\n\nIn the following example, we use direct EODHD API request without pre-installed library and it’s functions. Plus this time, we request result as .csv file.\n\nIf you run the code in RStudio (or any other software for R), you will get the following output:\n\nExperience is similair to Yahoo Finance, only instead of:\n\nDon’t forget to add your API key an additional parameter.\n\nWe recommend to use HTTP instead of HTTPS for R language.\n\n## Code Examples\n\n```text\ninstall.packages(\"eodhd\")\n```\n\n```text\nlibrary(\"eodhd\")\n```\n\n```text\napi_key <- 'demo'\n```\n\n```text\nsource(\"key.R\")\nprint(api_key)\n```\n\n```text\napi_token='demo'\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "r-library-for-financial-data-by-eodhd"
---

# R Library for Financial Data

## 源URL

https://eodhd.com/financial-apis/r-library-for-financial-data-by-eodhd

## 描述

Important! Since we have introduced a new version of the R library for EODHD functions, the current library is no longer supported on CRAN and has been replaced by the new library (eodhdR2). The current library is still available via our GitHub.

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Live (Delayed) Stock Prices and Macroeconomic Data (doc)` | - | 否 | - | get_live_stock_prices <- function(api_token, ticker, s = NULL) |
| `Bonds Fundamentals (doc)` | - | 否 | - | get_bonds_fundamentals_data( api_token <- "demo", isin <- "DE000CB83CF0" ) |
| `Intraday Historical Data (doc)` | - | 否 | - | get_intraday_historical_data( api_token <- "YOUR_API_TOKEN", interval <- "5m", from_unix_time <- "1627896900", to_unix_time <- "1630575300", symbol <- "AAPL.MX") |
| `Historical Dividends (doc)` | - | 否 | - | get_historical_dividends_data( api_token <- "demo", ticker <- "AAPL.US", date_from <- "2017-09-10", date_to <- "2017-09-12" ) |
| `Historical Splits (doc)` | - | 否 | - | get_historical_splits_data( api_token <- "demo",  ticker <- "AAPL.US",  date_from <- "2017-09-10", date_to <- "2017-09-12" ) |
| `Bulk API for EOD, Splits and Dividends (doc)` | - | 否 | - | get_bulk_eod_splits_dividends_data( api_token = "demo", country = 'US', type = 'splits', date = "2010-09-21", symbols = "MSFT", filter = "extended" ) |
| `Calendar. Upcoming Earnings, Trends, IPOs and Splits (doc)` | - | 否 | - | get_upcoming_earnings_data( api_token <- "demo", from_date <- "2017-09-10", to_date <- "2017-09-12", symbols <- "AAPL" )get_earning_trends_data(  api_token = "demo",  symbols = "AAPL.US" ) # for Earnings trendsget_upcoming_IPOs_data( api_token <- "YOUR_API_TOKEN", from_date <- "2017-09-10", to_date <- "2017-09-12" ) # for upcoming IPOsget_upcoming_splits_data( api_token <- "YOUR_API_TOKEN", from_date <- "2017-09-10", to_date <- "2017-09-12" ) # for upcoming splits |
| `Economic Events (doc)` | - | 否 | - | get_economic_events_data( api_token <- "demo", date_from <- "2017-09-10", date_to <- "2017-09-12", country <- "US", comparison <- "qoq", offset <- "0", limit <- "50" ) |
| `Stock Market and Financial News (doc)` | - | 否 | - | financial_news( api_token <- "demo", s <- "balance sheet", t <- NULL, from_date <- "2017-09-10", to_date <- "2017-09-12", limit <- "50", offset <- "100" ) |
| `End of the Day Historical Stock Market Data (doc)` | - | 否 | - | get_eod_historical_stock_market_data <- function( api_token, symbol, from_date = NULL,to_date = NULL, period = 'd', order = 'a' ) |
| `List of supported Exchanges (doc)` | - | 否 | - | get_list_of_exchanges( api_token <- "demo" ) |
| `Insider Transactions (doc)` | - | 否 | - | get_insider_transactions_data( api_token <- "demo", date_from <- "2017-09-10", date_to <- "2017-09-12", code <- "AAPL.US", limit <- "150" ) |
| `Macro Indicators (doc)` | - | 否 | - | get_macro_indicators_data( api_token <- "YOUR_API_TOKEN", country <- "USA", indicator <- "gdp_current_usd" ) |
| `Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History (doc)` | - | 否 | - | get_details_trading_hours_stock_market_holidays( api_token <- "YOUR_API_TOKEN", code <- "US", from_date <- "2017-09-10", to_date <- "2017-09-12") symbol_change_history(api_token <- "YOUR_API_TOKEN", from_date <- "2023-01-01", to_date <- "2023-12-31" ) |
| `Stock Market Screener (doc)` | - | 否 | - | stock_market_screener( api_token <- "YOUR_API_TOKEN",  sort <- "market_capitalization.desc", filters <- NULL, limit <- "1", signals <- "bookvalue_neg", offset <- "50" ) |
| `Technical Indicator (doc)` | - | 否 | - | get_technical_indicator_data( api_token <- "demo", ticker <- "AAPL.US", func <- "slope", period <- 100 ) |
| `Historical Market Capitalization (doc)` | - | 否 | - | get_historical_market_capitalization_data <- function( api_token, ticker,from_date = NULL,to_date = NULL ) |
| `Fundamental Data: Stocks, ETFs, Mutual Funds, Indices and Cryptocurrencies (doc)` | - | 否 | - | get_fundamentals_data( api_token <- "demo", ticker <- "AAPL.US" ) |

## 文档正文

Important! Since we have introduced a new version of the R library for EODHD functions, the current library is no longer supported on CRAN and has been replaced by the new library (eodhdR2). The current library is still available via our GitHub.

## Parameters

| Parameter | Description |
|-----------|-------------|
| Live (Delayed) Stock Prices and Macroeconomic Data (doc) | get_live_stock_prices <- function(api_token, ticker, s = NULL) |
| Bonds Fundamentals (doc) | get_bonds_fundamentals_data( api_token <- "demo", isin <- "DE000CB83CF0" ) |
| Intraday Historical Data (doc) | get_intraday_historical_data( api_token <- "YOUR_API_TOKEN", interval <- "5m", from_unix_time <- "1627896900", to_unix_time <- "1630575300", symbol <- "AAPL.MX") |
| Historical Dividends (doc) | get_historical_dividends_data( api_token <- "demo", ticker <- "AAPL.US", date_from <- "2017-09-10", date_to <- "2017-09-12" ) |
| Historical Splits (doc) | get_historical_splits_data( api_token <- "demo",  ticker <- "AAPL.US",  date_from <- "2017-09-10", date_to <- "2017-09-12" ) |
| Bulk API for EOD, Splits and Dividends (doc) | get_bulk_eod_splits_dividends_data( api_token = "demo", country = 'US', type = 'splits', date = "2010-09-21", symbols = "MSFT", filter = "extended" ) |
| Calendar. Upcoming Earnings, Trends, IPOs and Splits (doc) | get_upcoming_earnings_data( api_token <- "demo", from_date <- "2017-09-10", to_date <- "2017-09-12", symbols <- "AAPL" )get_earning_trends_data(  api_token = "demo",  symbols = "AAPL.US" ) # for Earnings trendsget_upcoming_IPOs_data( api_token <- "YOUR_API_TOKEN", from_date <- "2017-09-10", to_date <- "2017-09-12" ) # for upcoming IPOsget_upcoming_splits_data( api_token <- "YOUR_API_TOKEN", from_date <- "2017-09-10", to_date <- "2017-09-12" ) # for upcoming splits |
| Economic Events (doc) | get_economic_events_data( api_token <- "demo", date_from <- "2017-09-10", date_to <- "2017-09-12", country <- "US", comparison <- "qoq", offset <- "0", limit <- "50" ) |
| Stock Market and Financial News (doc) | financial_news( api_token <- "demo", s <- "balance sheet", t <- NULL, from_date <- "2017-09-10", to_date <- "2017-09-12", limit <- "50", offset <- "100" ) |
| End of the Day Historical Stock Market Data (doc) | get_eod_historical_stock_market_data <- function( api_token, symbol, from_date = NULL,to_date = NULL, period = 'd', order = 'a' ) |
| List of supported Exchanges (doc) | get_list_of_exchanges( api_token <- "demo" ) |
| Insider Transactions (doc) | get_insider_transactions_data( api_token <- "demo", date_from <- "2017-09-10", date_to <- "2017-09-12", code <- "AAPL.US", limit <- "150" ) |
| Macro Indicators (doc) | get_macro_indicators_data( api_token <- "YOUR_API_TOKEN", country <- "USA", indicator <- "gdp_current_usd" ) |
| Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History (doc) | get_details_trading_hours_stock_market_holidays( api_token <- "YOUR_API_TOKEN", code <- "US", from_date <- "2017-09-10", to_date <- "2017-09-12") symbol_change_history(api_token <- "YOUR_API_TOKEN", from_date <- "2023-01-01", to_date <- "2023-12-31" ) |
| Stock Market Screener (doc) | stock_market_screener( api_token <- "YOUR_API_TOKEN",  sort <- "market_capitalization.desc", filters <- NULL, limit <- "1", signals <- "bookvalue_neg", offset <- "50" ) |
| Technical Indicator (doc) | get_technical_indicator_data( api_token <- "demo", ticker <- "AAPL.US", func <- "slope", period <- 100 ) |
| Historical Market Capitalization (doc) | get_historical_market_capitalization_data <- function( api_token, ticker,from_date = NULL,to_date = NULL ) |
| Fundamental Data: Stocks, ETFs, Mutual Funds, Indices and Cryptocurrencies (doc) | get_fundamentals_data( api_token <- "demo", ticker <- "AAPL.US" ) |

## Installation and examples

First things first, ensure you have R and RStudio installed on your machine. RStudio is an integrated development environment (IDE) that makes working with R more convinient. You can download R from CRAN and RStudio from RStudio’s official website. Following guide will be based on RStudio.

Required Environment:

Feel free to visit our Github page to subscribe to receive notifications about future updates for R library.

## R library installation process

1. Installing the library. Type the following command and hit Enter:

See the screenshot:

2. Library Import. Next, let’s import EODHD library for accessing EODHD API’s functions:

See the screenshot:

R Financial Library is installed now. Next, we are going to activate EODHD’s API key to get an access to data.

## API access activation: free and payed options

1. You can start with “DEMO” API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. For these tickers, all of our APIs, including Real-Time Data, are availible without limitations.2. Register for the free plan to receive your API key (limited to 20 API calls per day) with access to End-Of-Day Historical Stock Market Data API for any ticker, but within the past year only. Plus a List of tickers per Exchange is availible.3. We recommend exploring our plans, starting from $19.99, to access the necessary type of API without limitations.

Once you have EODHD API key, you can set it in an additional file, for example “key.R”:

To implement the “key.R” file in your code:

Or set the type as an argument for the function:

Having implemented an active API key, we are ready to call for data.

## Information about a function

To access all information about a specific function, you can use the help command:

See the example:

Scroll down to the end of this guide to see all availible functions.

## Example: End of the day historical stock market data

Lets call for End of the day historical stock market data:

See the example:

The function will return the following JSON respond:

All the parameters for this function are listed and described here.

## List of the available functions

Below is the list of functions to retrieve various data, including code examples and links to documentation containing descriptions of all parameters:

## Direct EODHD request call in R enviroment

In the following example, we use direct EODHD API request without pre-installed library and it’s functions. Plus this time, we request result as .csv file.

If you run the code in RStudio (or any other software for R), you will get the following output:

Experience is similair to Yahoo Finance, only instead of:

Don’t forget to add your API key an additional parameter.

We recommend to use HTTP instead of HTTPS for R language.

## Code Examples

```text
install.packages("eodhd")
```

```text
library("eodhd")
```

```text
api_key <- 'demo'
```

```text
source("key.R")
print(api_key)
```

```text
api_token='demo'
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
