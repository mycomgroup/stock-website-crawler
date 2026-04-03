---
id: "url-63d0395e"
type: "api"
title: "Matlab API Connector and Example"
url: "https://eodhd.com/financial-apis/matlab-api-connector-and-example"
description: "It’s easy to use our API with MatLab without API connector also; below you can find a straightforward example with explanations for MatLab users."
source: ""
tags: []
crawl_time: "2026-03-18T04:26:35.629Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Matlab API Connector and Example\n\nIt’s easy to use our API with MatLab without API connector also; below you can find a straightforward example with explanations for MatLab users.\n\n\n## Simple Example\n\nIt’s easy to use our API with MatLab without API connector also; below you can find a straightforward example with explanations for MatLab users.\n\nFor testing purposes, you can use this API Key: api_token=demo. It works with AAPL.US only.\n\nAs you see, it’s easy to use. Usually, if you used before Yahoo Finance, then URL variable should look like this:\n\nand basically, all you need is to change the beginning of the URL to\n\nand then add your API Key as an additional parameter.\n\nPlease note, that it’s better to use HTTP instead of HTTPS for MatLab projects. And since we do automatic redirects, you should use special sub-domain without redirects: nonsecure.eodhd.com\n\n## Matlab Stock API Connector\n\nSimply download and extract the EODML.zip file from the Undocumented Matlab website in a folder on your Matlab path, then run the EODML command with self-explanatory parameters.\n\nThe usage is very user-friendly, as explained on UndocumentedMatlab.com (for example, case-insensitive parameter names with default values, different ways to specify start/end dates, etc.) Some usage examples are below.\n\n## Usage Example IV. Get Historic Earning Reports\n\n…and so on for the entire EODHD offering. You can read more about the EODML connector on https://UndocumentedMatlab.com/EODML\n\n## About the Author\n\nYair Altman is a recognized Matlab expert with 30 years of experience. Yair published two textbooks on Matlab and is a member of the MathWorks advisory board. He is widely known in the Matlab user community from his UndocumentedMatlab website and contributions to public forums. Yair posted numerous free Matlab code and developed multiple commercial Matlab connectors and programs for the finance sector. Read more on http://UndocumentedMatlab.com\n\n## Code Examples\n\n```text\nurl = 'http://nonsecure.eodhd.com/api/table.csv?s=AAPL.US&api_token=YOUR_API_KEY&a=0&b=1&c=2000&d=5&e=16&f=2017&g=d';\n\noptions = weboptions('ContentType','text');\ns=webread(url,options);\n\nC = textscan(s, '%s%f%f%f%f%f%f', 'HeaderLines', 1, 'delimiter', ',', 'CollectOutput', 0);\n\ndisp(C)\n```\n\n```text\nhttp://ichart.finance.yahoo.com/table.csv.....\n```\n\n```text\nhttp://nonsecure.eodhd.com/api/table.csv\n```\n\n```text\n>> data =\nEODML('prices', 'symbol','AAPL', 'datatype','live')\ndata = \n  struct with fields:\n           symbol: 'AAPL.US'\n        timestamp: 1577480400\n        gmtoffset: 0\n             open: 291.12\n             high: 293.97\n              low: 288.12\n            close: 289.8\n           volume: 36566500\n    previousClose: 289.91\n           change: -0.11\n         change_p: -0.038\n      datestr_GMT: '27-Dec-2019 21:00:00'\n      datenum_GMT: 737786.875\n```\n\n```text\n>> data =\nEODML('prices', 'symbols','IBM,AAPL,GOOG', 'FromDate',20191203, 'ToDate','2019/12/13', 'DataType','day')\ndata = \n  9×3 struct array with fields:\n    symbol\n    date\n    datenum\n    open\n    high\n    low\n    close\n    adjusted_close\n    volume\n>> data(1,2)\nans = \n  struct with fields:\n            symbol: 'AAPL.US'\n              date: '2019-12-03'\n           datenum: 737762\n              open: 258.31\n              high: 259.53\n               low: 256.29\n             close: 259.45\n    adjusted_close: 259.45\n            volume: 29377268\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "matlab-api-connector-and-example"
---

# Matlab API Connector and Example

## 源URL

https://eodhd.com/financial-apis/matlab-api-connector-and-example

## 描述

It’s easy to use our API with MatLab without API connector also; below you can find a straightforward example with explanations for MatLab users.

## 文档正文

It’s easy to use our API with MatLab without API connector also; below you can find a straightforward example with explanations for MatLab users.

## Simple Example

It’s easy to use our API with MatLab without API connector also; below you can find a straightforward example with explanations for MatLab users.

For testing purposes, you can use this API Key: api_token=demo. It works with AAPL.US only.

As you see, it’s easy to use. Usually, if you used before Yahoo Finance, then URL variable should look like this:

and basically, all you need is to change the beginning of the URL to

and then add your API Key as an additional parameter.

Please note, that it’s better to use HTTP instead of HTTPS for MatLab projects. And since we do automatic redirects, you should use special sub-domain without redirects: nonsecure.eodhd.com

## Matlab Stock API Connector

Simply download and extract the EODML.zip file from the Undocumented Matlab website in a folder on your Matlab path, then run the EODML command with self-explanatory parameters.

The usage is very user-friendly, as explained on UndocumentedMatlab.com (for example, case-insensitive parameter names with default values, different ways to specify start/end dates, etc.) Some usage examples are below.

## Usage Example IV. Get Historic Earning Reports

…and so on for the entire EODHD offering. You can read more about the EODML connector on https://UndocumentedMatlab.com/EODML

## About the Author

Yair Altman is a recognized Matlab expert with 30 years of experience. Yair published two textbooks on Matlab and is a member of the MathWorks advisory board. He is widely known in the Matlab user community from his UndocumentedMatlab website and contributions to public forums. Yair posted numerous free Matlab code and developed multiple commercial Matlab connectors and programs for the finance sector. Read more on http://UndocumentedMatlab.com

## Code Examples

```text
url = 'http://nonsecure.eodhd.com/api/table.csv?s=AAPL.US&api_token=YOUR_API_KEY&a=0&b=1&c=2000&d=5&e=16&f=2017&g=d';

options = weboptions('ContentType','text');
s=webread(url,options);

C = textscan(s, '%s%f%f%f%f%f%f', 'HeaderLines', 1, 'delimiter', ',', 'CollectOutput', 0);

disp(C)
```

```text
http://ichart.finance.yahoo.com/table.csv.....
```

```text
http://nonsecure.eodhd.com/api/table.csv
```

```text
>> data =
EODML('prices', 'symbol','AAPL', 'datatype','live')
data = 
  struct with fields:
           symbol: 'AAPL.US'
        timestamp: 1577480400
        gmtoffset: 0
             open: 291.12
             high: 293.97
              low: 288.12
            close: 289.8
           volume: 36566500
    previousClose: 289.91
           change: -0.11
         change_p: -0.038
      datestr_GMT: '27-Dec-2019 21:00:00'
      datenum_GMT: 737786.875
```

```text
>> data =
EODML('prices', 'symbols','IBM,AAPL,GOOG', 'FromDate',20191203, 'ToDate','2019/12/13', 'DataType','day')
data = 
  9×3 struct array with fields:
    symbol
    date
    datenum
    open
    high
    low
    close
    adjusted_close
    volume
>> data(1,2)
ans = 
  struct with fields:
            symbol: 'AAPL.US'
              date: '2019-12-03'
           datenum: 737762
              open: 258.31
              high: 259.53
               low: 256.29
             close: 259.45
    adjusted_close: 259.45
            volume: 29377268
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
