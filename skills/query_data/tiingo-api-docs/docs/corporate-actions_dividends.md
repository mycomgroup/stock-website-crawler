# 2.8.1 Overview

## 源URL

https://www.tiingo.com/documentation/corporate-actions/dividends

## 描述

The Tiingo API Dividends API endpoint help capture and relay both detailed dividend and distribution data, as well as historical metrics that relate to dividends, such as yield. As of August 28th, 2023, this endpoint remains newly exposed in beta and is included for all customers with the End-of-Day endpoint entitlement. This dividend distribution API endpoints fall under our new corporate action endpoints coming soon.

Diviends are available for current and future dates, and yield is available for tickers after their End-of-Day price data have been processed.

You can find out about the full product offering on the Product - Stock, ETF, & Mutual Fund Dividend API page.

## 2.8.2 Batch Distribution Data

Use this endpoint to get past, present, and future dividends and distributions. This endpoint will return detailed dividend and distribution data for a given stock, ETF, or Mutual Fund. You will also notice a distribution frequency, this is the declared frequency of the distribution that you can use to customize your calculations to determine yield.

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| PermaTicker | permaTicker | string | The Tiingo permaticker. |
| Ticker | ticker | string | Ticker related to the asset. |
| Ex-Date | exDate | datetime | The ex-Date of the distribution. In the Tiingo EOD Endpoints, this is the date where "divCash" will be non-zero. This is also the date used for dividend price adjustments. |
| Payment Date | paymentDate | datetime | The payment date of the distribution. |
| Record Date | recordDate | datetime | The record date of the distribution. |
| Declaration Date | declarationDate | datetime | The declaration date of the distribution. |
| Distribution | distribution | float | The total distribution for the given date. |
| Distribution Frequency | distributionFreqency | string | The frequency that's associated with this distribution. For example "q" means quarterly, meaning this is a declared quarterly distribution.
          The full list of codes is available here:

  w: Weekly
  bm: Bimonthly
  m: Monthly
  tm: Trimesterly
  q: Quarterly
  sa: Semiannually
  a: Annually
  ir: Irregular
  f: Final
  u: Unspecified
  c: Cancelled |

```text
# Latest Distribution Data with an Ex-Date of the current day
https://api.tiingo.com/tiingo/corporate-actions/distributions

# Latest Distribution Data with an ex-date explicitly specified (future date or historical date)
https://api.tiingo.com/tiingo/corporate-actions/distributions?exDate=2023-08-25
```

- w: Weekly
- bm: Bimonthly
- m: Monthly
- tm: Trimesterly
- q: Quarterly
- sa: Semiannually
- a: Annually
- ir: Irregular
- f: Final
- u: Unspecified
- c: Cancelled

## 2.8.3 Ticker-specific Distribution Data

This endpoint is similar to the batch endpoint, but allows you to specify a specific ticker to limit the query and also provide historical distribution timeseries data for a ticker as well. Stocks, ETFs, and Mutual Funds are supported.

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| PermaTicker | permaTicker | string | The Tiingo permaticker. |
| Ticker | ticker | string | Ticker related to the asset. |
| Ex-Date | exDate | datetime | The ex-Date of the distribution. In the Tiingo EOD Endpoints, this is the date where "divCash" will be non-zero. This is also the date used for dividend price adjustments. |
| Payment Date | paymentDate | datetime | The payment date of the distribution. |
| Record Date | recordDate | datetime | The record date of the distribution. |
| Declaration Date | declarationDate | datetime | The declaration date of the distribution. |
| Distribution | distribution | float | The total distribution for the given date. |
| Distribution Frequency | distributionFreqency | string | The frequency that's associated with this distribution. For example "q" means quarterly, meaning this is a declared quarterly distribution.
          The full list of codes is available here:

  w: Weekly
  bm: Bimonthly
  m: Monthly
  tm: Trimesterly
  q: Quarterly
  sa: Semiannually
  a: Annually
  ir: Irregular
  f: Final
  u: Unspecified
  c: Cancelled |

```text
# Distribution data endpoint for specific ticker (Full history)
https://api.tiingo.com/tiingo/corporate-actions/<ticker>/distributions

# Distribution data for a ticker limited to a provided date range
https://api.tiingo.com/tiingo/corporate-actions/<ticker>/distributions?startExDate=2023-01-01&endExDate=2024-01-01
```

- w: Weekly
- bm: Bimonthly
- m: Monthly
- tm: Trimesterly
- q: Quarterly
- sa: Semiannually
- a: Annually
- ir: Irregular
- f: Final
- u: Unspecified
- c: Cancelled

## 2.8.4 Historical Yield Endpoint

Use this endpoint to obtain the current and historical information about yield data for the given Stock, ETF, or Mutual Fund. Please note that we will continue to add new daily metrics, so the fields will change throughout time. We recommend you do not make parsing code that requires columns or fields to be in a particular order. If you do require this, please use the columns request parameter to ensure constant output, even if we add columns. For example, columns=trailingDiv1Y will always ensure only that single field is returned in that exact order.

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Date | date | datetime | Date associated with the yield. |
| Trailing 1 Year Dividend | trailingDiv1Y | string | The trailing distribution yield for the asset based on the previous 1 year of distributions. |

```text
# Distribution yield
https://api.tiingo.com/tiingo/corporate-actions/<ticker>/distribution-yield
```

## 2.8.5 Additional Information & FAQ

This endpoint is used to communicate past, present, and future distribtion data.

Data is updated throughout 2-3 times a day as distribution announcements come in.

Yes, future expansions of various yield calculations will be included in future dates - including forward yield. You may also calculate this yourself using our distribution frequency endpoints.

We have different enterprise relationships with various provides who provide various data feeds. We then error check them using a proprietary framework to check for errors. If a date is null, it generally means this data is not available to us. Ex-date and distribution amounts will never be null however.

### 2.8.1 Overview - Tab 内容

#### Request

| Field Name | Parameter | JSON Field | Data Type | Required | Description |
| --- | --- | --- | --- | --- | --- |
| Ex-Date | GET | exDate | date | N | This filter limits           distributions that have an ex-date on the date passed. Parameter must be in YYYY-MM-DD format. |
| Response Format | GET | format | string | N | Sets the response format of the returned data. Acceptable values are "csv" and "json". Defaults to JSON. |
| Columns | GET | columns | string[] | N | Allows you to specify which columns you would like returned from the output. Pass an array of strings of column names to get only this columns back. |

#### Examples

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/corporate-actions/distributions?exDate=2024-01-05&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

```text
[
    {
        "permaTicker":"US000000000045",
        "ticker":"ge",
        "exDate":"2023-09-25T00:00:00.000Z",
        "paymentDate":"2023-10-25T00:00:00.000Z",
        "recordDate":"2023-09-26T00:00:00.000Z",
        "declarationDate":"2023-09-08T04:00:00.000Z",
        "distribution":0.08,
        "distributionFrequency":"q"
    },
    ...
]
```

#### Python

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/corporate-actions/distributions?exDate=2024-01-05&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

#### Node

```text
var request = require('request');
var requestOptions = {
    'url': 'https://api.tiingo.com/tiingo/corporate-actions/distributions?exDate=2024-01-05&token=Not logged-in or registered. Please login or register to see your API Token',
    'headers': {
        'Content-Type': 'application/json'
        }
};

request(requestOptions,
    function(error, response, body) {
        console.log(body);
    }
);
```

#### PHP

```text
<?php
require 'vendor/autoload.php';
use GuzzleHttp\Client;

$client = new Client();
$res = $client->get("https://api.tiingo.com/tiingo/corporate-actions/distributions?exDate=2024-01-05&token=Not logged-in or registered. Please login or register to see your API Token", [
'headers' => [
    'Content-type' =>  'application/json'
    ]
]);
```

### 2.8.2 Batch Distribution Data - Tab 内容

#### Request

| Field Name | Parameter | JSON Field | Data Type | Required | Description |
| --- | --- | --- | --- | --- | --- |
| Ticker | URL | N/A | string | Y | Ticker related to the asset you would like distribution data for. |
| Start Ex-Date | GET | startExDate | date | N | This filter limits         distributions that have an ex-date >= on the date passed. Parameter must be in YYYY-MM-DD format. |
| End Ex-Date | GET | endExDate | date | N | This filter limits         distributions that have an ex-date <= on the date passed. Parameter must be in YYYY-MM-DD format. |
| Response Format | GET | format | string | N | Sets the response format of the returned data. Acceptable values are "csv" and "json". Defaults to JSON. |
| Columns | GET | columns | string[] | N | Allows you to specify which columns you would like returned from the output. Pass an array of strings of column names to get only this columns back. |

#### Examples

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/corporate-actions/aapl/distributions?startExDate=2024-01-05&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

```text
[
    {
        "permaTicker":"US000000000038",
        "ticker":"aapl",
        "exDate":"2024-02-09T05:00:00.000Z",
        "paymentDate":"2024-02-15T05:00:00.000Z",
        "recordDate":"2024-02-12T05:00:00.000Z",
        "declarationDate":"2024-02-01T10:00:00.000Z",
        "distribution":0.24,
        "distributionFrequency":"q"
    },
    ...
]
```
