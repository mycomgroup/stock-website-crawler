# 2.7.1 Overview

## 源URL

https://www.tiingo.com/documentation/mutual-fund-and-etf-fees

## 描述

Tiingo tracks and processes official Mutual Fund & ETF Fee data from over 36,000 Mutual Funds and ETFs. The data includes a detailed breakdown data of fees, even including custom fees (like check processing fee if withdrawing money via check).

Benefits of Mutual Fund & ETF Fee Data

- 36,000+ Mutual Funds and ETFs covered.
- Data includes historical as well as current data.
- Fee data is detailed and broken down (e.g. management fee, 12b-1 fees, and more).
- Fee data is updated intraday as new data comes online from Fund Companies.
- Multiple share classes are mapped allowing you to easily compare fees across share classes.

## 2.7.2 Fund Overview

To see what fields are returned in the "otherShareClasses" field, please see the table below.

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Ticker | ticker | string | Ticker related to the fund. |
| Name | name | string | Full-length name of the fund. |
| Description | description | string | Long-form descripton of the fund. |
| Share Class | shareClass | string | Share class of the fund as described by the parent fund company. |
| Net Expense Ratio | netExpense | float | The top-level net expense ratio for the fund. |
| Other Share Classes | otherShareClasses | object[] | An array of objects representing related share classes of the given fund. See below for the object defintion table. |

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Ticker | ticker | string | Ticker related to the fund. |
| Name | name | string | Full-length name of the fund. |
| Share Class | shareClass | string | Share class of the fund as described by the parent fund company. |
| Net Expense Ratio | netExpense | float | The top-level net expense ratio for the fund. |

```text
# To obtain top-level fund data, including description and share classes, use the following REST endpoint
https://api.tiingo.com/tiingo/funds/<ticker>
```

## 2.7.3 Historical and Current Mutual Fund & ETF Fee Data

To see what fields are returned in the "customFees" field, please see the table below.

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Prospectus Date | prospectusDate | date | The prospectus date when the corresponding fund expense data was published. |
| Net Expense Ratio | netExpense | float | Fund's net expense ratio, or the net expenses related to the fund. |
| Gross Expense Ratio | grossExpense | float | Fund's gross expense ratio, or the expenses related to running the fund. |
| Management Fee | managementFee | float | Fund's management fee, or the fees paid to the manager and/or advisors. |
| 12b-1 Fee | 12b1 | float | Fund's fee related to marketing expenses. |
| Non-12b-1 Fee | non12b1 | float | Fund's fee related to distribution and smilar non 12b-1 fees. |
| Other Fund Expenses | otherExpenses | float | Fund's other expenses, or expenses related to legal, adminstrative, custodial, etc. |
| Acquired Fund Fees | acquiredFundFees | float | Fund's acquired fund fees, or expenses related to underlying businesses or funds. |
| Fee Waiver | feeWaiver | float | Fund's fee waiver, or discount on fees. |
| Exchange Fee (USD) | exchangeFeeUSD | float | Fund's exchange fee if charged in USD, or expenses related to exchanging or transferring funds to another fund in the fund's family. |
| Exchange Fee (%) | exchangeFeePercent | float | Fund's exchange fee if charged as a percentage, or expenses related to exchanging or transferring funds to another fund in the fund's family. |
| Front Load Fee | frontLoad | float | Fund's front load fee, or the upfront fee charged when investing in the fund. |
| Back Load Fee | backLoad | float | Fund's back load fee, or the back-end fee charged when redeeming from the fund. |
| Dividend Load Fee | dividendLoad | float | Dividend load fee, or charges on reinvested dividends. |
| Shareholder Fee | shareholderFee | float | Fund's shareholder fees, or the potential fees when buying/selling a fund. |
| Account Fee (USD) | accountFeeUSD | float | Fund's account fees if charged in USD, or the fee required to maintain your account in USD. |
| Account Fee (%) | accountFeePercent | float | Fund's account fees if charged as a percentage, or the fee required to maintain your account in percentage terms. |
| Redemption Fee (USD) | redemptionFeeUSD | float | Fund's redemption fees if charged in USD, or the fee charged if funds are redeemed early (as defined by the fund company). |
| Redemption Fee (%) | redemptionFeePercent | float | Fund's redemption fees as a percentage, or the fee charged if funds are redeemed early (as defined by the fund company). |
| Portfolio Turnover | portfolioTurnover | float | Portfolio turnover. |
| Miscellaneous Fees | miscFees | float | Fund's miscellaneous fees. |
| Custom Fees | customFees | object[] | Fund's custom fees. For a full breakdown, see the table below. |

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Label | label | string | Label related to the custom fee. |
| Value | value | float | Value of the custom fee field. |
| Units | units | char | "$" if the value is in dollars or "%" if the value is in percentage terms. |
| Parent Fee | parentFee | string | The parent fee the custom fee's belongs under. |

```text
# To obtain detailed current and historical fee data, use the following REST endpoint
https://api.tiingo.com/tiingo/funds/<ticker>/metrics
```

### 2.7.1 Overview - Tab 内容

#### Request

| Field Name | Parameter | JSON Field | Data Type | Required | Description |
| --- | --- | --- | --- | --- | --- |
| Ticker | URL or GET | tickers | string | Y | Ticker related to the fund. |

#### Examples

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/funds/vfinx?token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

```text
{
    "ticker":"vfinx"
    "name":"VANGUARD 500 INDEX FUND INVESTOR SHARES",
    "shareClass":"INVESTOR SHARES",
    "description":"The Fund employs an indexing investment approach designed to track the performance of the Standard & Poor's 500 Index, a widely recognized benchmark of U.S. stock market performance that is dominated by the stocks of large U.S. companies. The Fund attempts to replicate the target index by investing all, or substantially all, of its assets in the stocks that make up the Index, holding each stock in approximately the same proportion as its weighting in the Index.",
    "netExpense":0.0014,
    "otherShareClasses":[
    {
        "ticker":"VFIAX",
        "name":"VANGUARD 500 INDEX FUND ADMIRAL SHARES",
        "shareClass":"ADMIRAL SHARES",
        "netExpense":0.0004
    },
    {
        "ticker":"VFFSX",
        "name":"VANGUARD 500 INDEX FUND INSTITUTIONAL SELECT SHARES",
        "shareClass":"INSTITUTIONAL SELECT SHARES",
        "netExpense":0.0001
    },
    {
        "ticker":"VOO",
        "name":"Vanguard S&P 500 ETF",
        "shareClass":"ETF SHARES",
        "netExpense":0.0003
    }
]
```

#### Python

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/funds/vfinx?token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

#### Node

```text
var request = require('request');
var requestOptions = {
    'url': 'https://api.tiingo.com/tiingo/funds/vfinx?token=Not logged-in or registered. Please login or register to see your API Token',
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
$res = $client->get("https://api.tiingo.com/tiingo/funds/vfinx?token=Not logged-in or registered. Please login or register to see your API Token", [
'headers' => [
    'Content-type' =>  'application/json'
    ]
]);
```
