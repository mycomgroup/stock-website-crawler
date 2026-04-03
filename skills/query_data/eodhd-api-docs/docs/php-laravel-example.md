---
id: "url-bd1df9c"
type: "api"
title: "PHP/Laravel Example"
url: "https://eodhd.com/financial-apis/php-laravel-example"
description: "EOD Historical Data API Client Wrapper (Financial and Stock Market API) for Laravel/PHP."
source: ""
tags: []
crawl_time: "2026-03-18T03:04:37.055Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# PHP/Laravel Example\n\nEOD Historical Data API Client Wrapper (Financial and Stock Market API) for Laravel/PHP.\n\n\n## Exchanges API Example\n\nYou can find more on Github page: https://github.com/radicalloop/eodhistoricaldata.\n\nThanks to RadicalLoop for it!\n\n## Code Examples\n\n```text\nuse Eod;\n\n$stock = Eod::stock();\n\n// JSON \n$stock->realTime('AAPL.US')->json();\n$stock->eod('AAPL.US')->json();\n\n// Download CSV \n$stock->realTime('AAPL.US' ['s' => ['VTI','EUR','FX']])->download();\n$stock->eod('AAPL.US')->download();\n\n// Save CSV to specific path\n$stock->realTime('AAPL.US')->save('path/to/save/csv/stock.csv');\n\n// For other parameters, for ex. dividend api with other params\n$stock->dividend('AAPL.US', ['from' => '2017-01-01'])->json();\n```\n\n```text\nuse Eod;\n\n$exchange = Eod::exchange();\n\n// JSON \n$exchange->symbol('US')->json();\n$exchange->multipleTicker('US')->json();\n\n// Download CSV \n$exchange->symbol('US')->download();\n$exchange->multipleTicker('US')->download();\n\n// Save CSV to specific path\n$exchange->symbol('US')->save('path/to/save/csv/stock.csv');\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "php-laravel-example"
---

# PHP/Laravel Example

## 源URL

https://eodhd.com/financial-apis/php-laravel-example

## 描述

EOD Historical Data API Client Wrapper (Financial and Stock Market API) for Laravel/PHP.

## 文档正文

EOD Historical Data API Client Wrapper (Financial and Stock Market API) for Laravel/PHP.

## Exchanges API Example

You can find more on Github page: https://github.com/radicalloop/eodhistoricaldata.

Thanks to RadicalLoop for it!

## Code Examples

```text
use Eod;

$stock = Eod::stock();

// JSON 
$stock->realTime('AAPL.US')->json();
$stock->eod('AAPL.US')->json();

// Download CSV 
$stock->realTime('AAPL.US' ['s' => ['VTI','EUR','FX']])->download();
$stock->eod('AAPL.US')->download();

// Save CSV to specific path
$stock->realTime('AAPL.US')->save('path/to/save/csv/stock.csv');

// For other parameters, for ex. dividend api with other params
$stock->dividend('AAPL.US', ['from' => '2017-01-01'])->json();
```

```text
use Eod;

$exchange = Eod::exchange();

// JSON 
$exchange->symbol('US')->json();
$exchange->multipleTicker('US')->json();

// Download CSV 
$exchange->symbol('US')->download();
$exchange->multipleTicker('US')->download();

// Save CSV to specific path
$exchange->symbol('US')->save('path/to/save/csv/stock.csv');
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
