# 2.9.1 Overview

## 源URL

https://www.tiingo.com/documentation/corporate-actions/splits

## 描述

The Tiingo API Splits API endpoint provides detailed split data, for both historical and future split data. This endpoint remains newly exposed in beta and is included for all customers with the End-of-Day endpoint entitlement.

Splits are available for current and future dates, and data is updated as new corporate communications get processed. The tickers covered are the same found via the End-of-Day price data endpoints. This mean you can get past and future split data for stocks, ETFs, and mutual funds.

You can find out about the full product offering on the Product - Stock, ETF, & Mutual Fund Split API page.

## 2.9.2 Batch Split Data

Use this endpoint to get past, present, and future splits. This endpoint will return detailed split data for a given stock, ETF, or Mutual Fund. You will also notice split status - this can either be active ("a") or cancelled ("c").

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| PermaTicker | permaTicker | string | The Tiingo permaticker. |
| Ticker | ticker | string | Ticker related to the asset. |
| Ex-Date | exDate | datetime | The ex-Date of the split. In the Tiingo EOD Endpoints, this is the date where "splitFactor" will not be 1.0. This is also the date used for split adjustments. |
| Split From | splitFrom | float | The prior split ratio. |
| Split To | splitTo | float | The new split ratio, i.e. how many shares of "splitTo" are given for each share of "splitFrom". |
| Split Factor | splitFactor | float | The ratio of splitTo from splitFrom. In other words:
          splitFactor = splitTo/splitFrom 
          This ratio is helpful in calculating split price adjustments. |
| Split Status | splitStatus | string | A code representing the status of split

  a: Active
  c: Cancelled |

```text
# Latest Split Data with an Ex-Date of the current day
https://api.tiingo.com/tiingo/corporate-actions/splits

# Latest Split Data with an ex-date explicitly specified (future date or historical date)
https://api.tiingo.com/tiingo/corporate-actions/splits?exDate=2023-08-25
```

- a: Active
- c: Cancelled

## 2.9.3 Ticker-specific Split Data

This endpoint is similar to the batch endpoint, but allows you to specify a specific ticker to limit the query and also provide historical split timeseries data for a ticker as well. Stocks, ETFs, and Mutual Funds are supported.

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| PermaTicker | permaTicker | string | The Tiingo permaticker. |
| Ticker | ticker | string | Ticker related to the asset. |
| Ex-Date | exDate | datetime | The ex-Date of the split. In the Tiingo EOD Endpoints, this is the date where "splitFactor" will not be 1.0. This is also the date used for split adjustments. |
| Split From | splitFrom | float | The prior split ratio. |
| Split To | splitTo | float | The new split ratio, i.e. how many shares of "splitTo" are given for each share of "splitFrom". |
| Split Factor | splitFactor | float | The ratio of splitTo from splitFrom. In other words:
          splitFactor = splitTo/splitFrom 
          This ratio is helpful in calculating split price adjustments. |
| Split Status | splitStatus | string | A code representing the status of split

  a: Active
  c: Cancelled |

```text
# Latest Split Data with an Ex-Date of the current day
https://api.tiingo.com/tiingo/corporate-actions/cvs/splits

# Latest Split Data with an ex-date explicitly specified (future date or historical date)
https://api.tiingo.com/tiingo/corporate-actions/cvs/splits?startExDate=2002-08-25
```

- a: Active
- c: Cancelled

### 2.9.1 Overview - Tab 内容

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
requestResponse = requests.get("https://api.tiingo.com/tiingo/corporate-actions/splits?exDate=2023-9-28&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

```text
[
    {
        "permaTicker":"US000000060663",
        "ticker":"dinrf",
        "exDate":"2023-09-28T00:00:00.000Z",
        "splitFrom":1.0,
        "splitTo":2.0,
        "splitFactor":2.0
    }
    ...
]
```

#### Python

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/corporate-actions/splits?exDate=2023-9-28&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

#### Node

```text
var request = require('request');
var requestOptions = {
    'url': 'https://api.tiingo.com/tiingo/corporate-actions/splits?exDate=2023-9-28&token=Not logged-in or registered. Please login or register to see your API Token',
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
$res = $client->get("https://api.tiingo.com/tiingo/corporate-actions/splits?exDate=2023-9-28&token=Not logged-in or registered. Please login or register to see your API Token", [
'headers' => [
    'Content-type' =>  'application/json'
    ]
]);
```
