---
id: "url-31c1770f"
type: "api"
title: "Technical Analysis Indicators API"
url: "https://eodhd.com/financial-apis/technical-indicators-api/"
description: "Our Indicator API provides detailed technical data for equities, offering an expert-backed Technical Analysis API. Users gain access to a diverse range of indicators crucial for informed decision-making in the stock, crypto, and forex markets. Explore our extensive list of all stock market indicators to enhance your trading strategies and optimize your investment portfolios. Our API seamlessly integrates with various technologies, enabling users to leverage industry standards and cutting-edge tools for advanced market analysis."
source: ""
tags: []
crawl_time: "2026-03-18T04:22:54.460Z"
metadata:
  endpoint: "https://eodhd.com/api/technical/AAPL.US"
  parameters: []
  markdownContent: "# Technical Analysis Indicators API\n\nOur Indicator API provides detailed technical data for equities, offering an expert-backed Technical Analysis API. Users gain access to a diverse range of indicators crucial for informed decision-making in the stock, crypto, and forex markets. Explore our extensive list of all stock market indicators to enhance your trading strategies and optimize your investment portfolios. Our API seamlessly integrates with various technologies, enabling users to leverage industry standards and cutting-edge tools for advanced market analysis.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/technical/AAPL.US?order=d&from=2017-08-01&to=2020-01-01&function=sma&period=50&api_token=demo&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/technical/AAPL?function=ema&filter=last_ema&api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n\n## Quick Start\n\nTo retrieve technical indicators data for every equity in our dataset, use the following URL:\n\nAn example of output for SMA function for AAPL\n\n## Filter fields\n\nWe also support the ability to retrieve only the last value. Simply add ‘filter=last_ema‘ or ‘filter=last_volume‘ with ‘fmt=json‘, and you will receive only one number. For example, with this request:\n\nYou will get one value – the last EMA value for AAPL (Apple Inc).\n\n## Technical Indicator API Functions\n\nFor all functions, you can use the following parameters as described above: to, from, order, fmt, and function. We have provided the specific usage for each function below.\n\n## Split Adjusted Data\n\nIt’s not a technical indicator itself, but we added this function to our API. By default Open, High, Low and Close values (OHLC) we provide in raw values and adjust neither for splits nor for dividends. While ‘adjusted_close’ values are adjusted both to splits and dividends. However, if you need only split-adjusted closes, you can use this function to get the desired time series.\n\nfunction [required] – splitadjusted.\n\nagg_period [optional] – aggregation period. Default value – ‘d’. Possible values: d – daily, w – weekly, m – monthly.\n\n## Average Volume (avgvol)\n\nThis function returns the Average Trading Volume. The average volume of a security over a longer period of time is the total amount traded in that period, divided by the length of the period.\n\n## Average Volume by Price (avgvolccy)\n\nThis function returns the Average Trading Volume in currency. The average volume in the currency of a security over a longer period of time is the total amount traded in that period multiplied by the price of the security, and divided by the length of the period.\n\n## SMA (Simple Moving Average)\n\nThis function returns the Simple Moving Average indicator. More information on Wikipedia SMA article.\n\n## EMA (Exponential Moving Average)\n\nThis function returns the Exponential Moving Average indicator. More information on Wikipedia EMA article.\n\n## WMA (Weighted Moving Average)\n\nThis function returns the Weighted Moving Average technical indicator. More information on Wikipedia WMA article.\n\n## Volatility\n\nThis function returns the Volatility, a statistical measure of the dispersion of returns for a given security or market index. More information on the Investopedia Volatility article.\n\n## Stochastic Technical Indicator\n\nThis function returns Stochastic values. More information on Wikipedia Stochastic Oscillator article.\n\nThis function returns K values and D Values.\n\n## Relative Strength Index (rsi)\n\nThis function returns the Relative Strength Index (RSI) technical indicator. More information on Wikipedia RSI article.\n\n## Standard Deviation (stddev)\n\nThis function returns the Standard Deviation (stddev) technical indicator. More information on Wikipedia Standard Deviation article.\n\n## Stochastic Relative Strength Index\n\nThis function returns Stochastic Relative Strength Index values. More information on Stochastic RSI Investopedia article.\n\nThis function returns K values and D Values.\n\n## Slope (Linear Regression)\n\nThis function returns the Linear Regression Slope. More information on Wikipedia Linear Regression article.\n\nReturns an array with calculated data or false on failure.\n\n## Directional Movement Index (dmi or dx)\n\nThis function returns the Directional Movement Index. More information on Directional Movement Index article.\n\nReturns an array with calculated data or false on failure.\n\n## Average Directional Movement Index (adx)\n\nThis function returns the Average Directional Movement Index. More information on Average Directional Movement Index article.\n\nReturns an array with calculated data or false on failure.\n\n## Moving Average Convergence/Divergence  (macd)\n\nThis function returns Moving Average Convergence/Divergence values. More information on Wikipedia MACD article.\n\nThis function returns MACD values, Signal values, and Divergence values.\n\n## Average True Range (ATR)\n\nThis function returns the average of true ranges over the specified period. More information on Average True Range Investopedia article.\n\nReturns an array with calculated data or false on failure.\n\n## Commodity Channel Index (CCI)\n\nThis function returns the CCI data. The Commodity Channel Index​ (CCI) is a momentum-based oscillator used to help determine when an investment vehicle is reaching a condition of being overbought or oversold. More information on Commodity Channel Index Investopedia article.\n\nReturns an array with calculated data or false on failure.\n\n## Parabolic SAR\n\nThis function returns the Parabolic SAR values. More information on Parabolic SAR Wikipedia article.\n\nReturns an array with calculated data or false on failure.\n\n## BETA\n\nThis function returns the BETA values of any ticker against any other ticker, for example, any index like S&P 500. More information on Beta (Finance) Wikipedia article.\n\nReturns an array with calculated data or false on failure.\n\n## Bollinger Bands\n\nThis function returns the Bollinger Bands technical indicator. A type of statistical chart characterizing the prices and volatility over time of a financial instrument, using a formulaic method propounded by John Bollinger in the 1980s. More information on Wikipedia Bollinger Bands article.\n\nReturns an array with calculated data or false on failure.\n\nuband – ‘upper’ band.\n\nmband – ‘middle’ band.\n\nlband – ‘lower’ band.\n\n## Amibroker File format\n\nThis file format returns the data in AmiBroker File format to import the data into AmiBroker software.\n\nThe AmiBroker file format to import the data into AmiBroker software. The example of the output can be seen here:\n\nThe OHLC fields are split-adjusted only, not adjusted to dividends.\n\n## Important Notes\n\nExplore our marketlpace for more technical indicators.\n\nPlease note that each API request for Technical API consumes 5 API calls.\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "technical-indicators-api"
---

# Technical Analysis Indicators API

## 源URL

https://eodhd.com/financial-apis/technical-indicators-api/

## 描述

Our Indicator API provides detailed technical data for equities, offering an expert-backed Technical Analysis API. Users gain access to a diverse range of indicators crucial for informed decision-making in the stock, crypto, and forex markets. Explore our extensive list of all stock market indicators to enhance your trading strategies and optimize your investment portfolios. Our API seamlessly integrates with various technologies, enabling users to leverage industry standards and cutting-edge tools for advanced market analysis.

## API 端点

**Endpoint**: `https://eodhd.com/api/technical/AAPL.US`

## 文档正文

Our Indicator API provides detailed technical data for equities, offering an expert-backed Technical Analysis API. Users gain access to a diverse range of indicators crucial for informed decision-making in the stock, crypto, and forex markets. Explore our extensive list of all stock market indicators to enhance your trading strategies and optimize your investment portfolios. Our API seamlessly integrates with various technologies, enabling users to leverage industry standards and cutting-edge tools for advanced market analysis.

## API Endpoint

```text
https://eodhd.com/api/technical/AAPL.US?order=d&from=2017-08-01&to=2020-01-01&function=sma&period=50&api_token=demo&fmt=json
```

```text
https://eodhd.com/api/technical/AAPL?function=ema&filter=last_ema&api_token={YOUR_API_TOKEN}&fmt=json
```

## Quick Start

To retrieve technical indicators data for every equity in our dataset, use the following URL:

An example of output for SMA function for AAPL

## Filter fields

We also support the ability to retrieve only the last value. Simply add ‘filter=last_ema‘ or ‘filter=last_volume‘ with ‘fmt=json‘, and you will receive only one number. For example, with this request:

You will get one value – the last EMA value for AAPL (Apple Inc).

## Technical Indicator API Functions

For all functions, you can use the following parameters as described above: to, from, order, fmt, and function. We have provided the specific usage for each function below.

## Split Adjusted Data

It’s not a technical indicator itself, but we added this function to our API. By default Open, High, Low and Close values (OHLC) we provide in raw values and adjust neither for splits nor for dividends. While ‘adjusted_close’ values are adjusted both to splits and dividends. However, if you need only split-adjusted closes, you can use this function to get the desired time series.

function [required] – splitadjusted.

agg_period [optional] – aggregation period. Default value – ‘d’. Possible values: d – daily, w – weekly, m – monthly.

## Average Volume (avgvol)

This function returns the Average Trading Volume. The average volume of a security over a longer period of time is the total amount traded in that period, divided by the length of the period.

## Average Volume by Price (avgvolccy)

This function returns the Average Trading Volume in currency. The average volume in the currency of a security over a longer period of time is the total amount traded in that period multiplied by the price of the security, and divided by the length of the period.

## SMA (Simple Moving Average)

This function returns the Simple Moving Average indicator. More information on Wikipedia SMA article.

## EMA (Exponential Moving Average)

This function returns the Exponential Moving Average indicator. More information on Wikipedia EMA article.

## WMA (Weighted Moving Average)

This function returns the Weighted Moving Average technical indicator. More information on Wikipedia WMA article.

## Volatility

This function returns the Volatility, a statistical measure of the dispersion of returns for a given security or market index. More information on the Investopedia Volatility article.

## Stochastic Technical Indicator

This function returns Stochastic values. More information on Wikipedia Stochastic Oscillator article.

This function returns K values and D Values.

## Relative Strength Index (rsi)

This function returns the Relative Strength Index (RSI) technical indicator. More information on Wikipedia RSI article.

## Standard Deviation (stddev)

This function returns the Standard Deviation (stddev) technical indicator. More information on Wikipedia Standard Deviation article.

## Stochastic Relative Strength Index

This function returns Stochastic Relative Strength Index values. More information on Stochastic RSI Investopedia article.

This function returns K values and D Values.

## Slope (Linear Regression)

This function returns the Linear Regression Slope. More information on Wikipedia Linear Regression article.

Returns an array with calculated data or false on failure.

## Directional Movement Index (dmi or dx)

This function returns the Directional Movement Index. More information on Directional Movement Index article.

Returns an array with calculated data or false on failure.

## Average Directional Movement Index (adx)

This function returns the Average Directional Movement Index. More information on Average Directional Movement Index article.

Returns an array with calculated data or false on failure.

## Moving Average Convergence/Divergence  (macd)

This function returns Moving Average Convergence/Divergence values. More information on Wikipedia MACD article.

This function returns MACD values, Signal values, and Divergence values.

## Average True Range (ATR)

This function returns the average of true ranges over the specified period. More information on Average True Range Investopedia article.

Returns an array with calculated data or false on failure.

## Commodity Channel Index (CCI)

This function returns the CCI data. The Commodity Channel Index (CCI) is a momentum-based oscillator used to help determine when an investment vehicle is reaching a condition of being overbought or oversold. More information on Commodity Channel Index Investopedia article.

Returns an array with calculated data or false on failure.

## Parabolic SAR

This function returns the Parabolic SAR values. More information on Parabolic SAR Wikipedia article.

Returns an array with calculated data or false on failure.

## BETA

This function returns the BETA values of any ticker against any other ticker, for example, any index like S&P 500. More information on Beta (Finance) Wikipedia article.

Returns an array with calculated data or false on failure.

## Bollinger Bands

This function returns the Bollinger Bands technical indicator. A type of statistical chart characterizing the prices and volatility over time of a financial instrument, using a formulaic method propounded by John Bollinger in the 1980s. More information on Wikipedia Bollinger Bands article.

Returns an array with calculated data or false on failure.

uband – ‘upper’ band.

mband – ‘middle’ band.

lband – ‘lower’ band.

## Amibroker File format

This file format returns the data in AmiBroker File format to import the data into AmiBroker software.

The AmiBroker file format to import the data into AmiBroker software. The example of the output can be seen here:

The OHLC fields are split-adjusted only, not adjusted to dividends.

## Important Notes

Explore our marketlpace for more technical indicators.

Please note that each API request for Technical API consumes 5 API calls.

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
