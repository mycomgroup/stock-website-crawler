# 2.4.1 Overview of the Tiingo Forex API

## 源URL

https://www.tiingo.com/documentation/forex

## 描述

Tiingo connects directly to tier-1 banks and FX dark pools to provide institutional-grade quality Forex quotes.

Benefits of the Tiingo Forex API

For more details please visit the Forex API product page.

- 140+ Forex Tickers Quoted
- Data includes Top-of-Book (Bid/Ask) data
- Data now includes intraday OHLC bar historical data for all your needs.
- Quotes updated to the latest microsecond.
- Data is served via a REST API & Websocket API.
- Market hours are from 8pm EST Sunday through 5pm EST Friday.

## 2.4.2 Current Top-of-Book

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Ticker | ticker | string | Ticker related to the asset. |
| Timestamp | quoteTimestamp | datetime | The timestamp the data was last refresh on. |
| Mid Price | midPrice | float | The mid price of the current timestamp when both "bidPrice" and "askPrice" are not-null.
In mathematical terms:
        
midPrice = (bidPrice + askPrice)/2.0 |
| Bid Size | bidSize | float | The amount of units at the bid price. |
| Bid Price | bidPrice | float | The current bid price. |
| Ask Size | askSize | float | The amount of units at the ask price. |
| Ask Price | askPrice | float | The current ask price. |

```text
# To request top-of-book/last for mulitple base and quote pairs, use the following REST endpoint
https://api.tiingo.com/tiingo/fx/top?tickers=<ticker>,<ticker>,...<ticker>

# To request top-of-book/last for specific tickers, use the following REST endpoint
https://api.tiingo.com/tiingo/fx/<ticker>/top
```

## 2.4.3 Intraday Prices Endpoint

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Date | date | datetime | The date this data pertains to. |
| Ticker | ticker | string | Ticker related to the asset. |
| Open | open | float | The opening price for the asset on the given date. |
| High | high | float | The high price for the asset on the given date. |
| Low | low | float | The low price for the asset on the given date. |
| Close | close | float | The closing price for the asset on the given date. |

```text
# Current OHLC for the day
https://api.tiingo.com/tiingo/fx/<ticker>/prices?resampleFreq=1day

# Historical Intraday Prices
https://api.tiingo.com/tiingo/fx/<ticker>/prices?startDate=2019-06-30&resampleFreq=5min
```

### 2.4.1 Overview of the Tiingo Forex API - Tab 内容

#### Request

| Field Name | Parameter | JSON Field | Data Type | Required | Description |
| --- | --- | --- | --- | --- | --- |
| Ticker | URL or GET | tickers | string | N | Ticker related to the asset. |
| Response Format | GET | format | string | N | Sets the response format of the returned data. Acceptable values are "csv" and "json". Defaults to JSON. |

#### Examples

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/fx/top?tickers=audusd,eurusd&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

```text
[
    {
        "ticker":"audusd",
        "quoteTimestamp":"2019-07-01T21:00:01.289000+00:00",
        "bidPrice":0.6963,
        "bidSize":100000.0,
        "askPrice":0.69645,
        "askSize":1200000.0,
        "midPrice":0.696375
    },
    {
        "ticker":"eurusd",
        "quoteTimestamp":"2019-07-01T21:00:01.181000+00:00",
        "bidPrice":1.12849,
        "bidSize":250000.0,
        "askPrice":1.12864,
        "askSize":250000.0,
        "midPrice":1.128565
    }
]
```

#### Python

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/fx/top?tickers=audusd,eurusd&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

#### Node

```text
var request = require('request');
var requestOptions = {
    'url': 'https://api.tiingo.com/tiingo/fx/top?tickers=audusd,eurusd&token=Not logged-in or registered. Please login or register to see your API Token',
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
$res = $client->get("https://api.tiingo.com/tiingo/fx/top?tickers=audusd,eurusd&token=Not logged-in or registered. Please login or register to see your API Token", [
'headers' => [
    'Content-type' =>  'application/json'
    ]
]);
```
