# 4.1.1 Overview

## 源URL

https://www.tiingo.com/documentation/utilities/search

## 描述

Tiingo's search feature lets you find specific assets in our database by the ticker or the name of the asset. This endpoint lets you segment by active, delisted, tickers across asset classes. The endpoint first searches for ticker matches and then expands to matches in the name of the asset.

This endpoint is useful for looking up existing assets

## 4.1.2 Search Endpoint

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Ticker | ticker | string | Ticker of the given asset. |
| Name | name | string | The name of the asset. |
| Asset Type | assetType | string | The asset type of the asset (Stock, ETF, & Mutual Fund). |
| Is Active | isActive | boolean | True if the ticker is still actively quoted, and false if the ticker is no longer actively quoted (delisted). |
| Tiingo PermaTicker | permaTicker | string | Placeholder for an upcoming change to the Tiingo API that allows querying by permaticker. |
| OpenFIGI Ticker | openFIGI | string | Placeholder for an upcoming change to the Tiingo API that allows querying by the openFIGI ticker. |

```text
# Search Tiingo database for specific assets
https://api.tiingo.com/tiingo/utilities/search/apple
# or
https://api.tiingo.com/tiingo/utilities/search?query=apple
```

### 4.1.1 Overview - Tab 内容

#### Request

| Field Name | Parameter | JSON Field | Data Type | Required | Description |
| --- | --- | --- | --- | --- | --- |
| Search Query | GET | query | string | Y | The search query to use to look up assets. |
| Exact Ticker Match | GET | exactTickerMatch | boolean | N | True to only include exact ticker matches based on the search query. 
            If set to true, no partial matches will be included and asset names will not be searched. |
| Include Delisted | GET | includeDelisted | boolean | N | True to include delisted tickers and false (default) to exclude delisted tickers. |
| Limit | GET | limit | int32 | N | The maximum number of assets to return. Defaults to 10 and can be set to a maximum of 100. |
| Response Format | GET | format | string | N | Sets the response format of the returned data. Acceptable values are "csv" and "json". Defaults to JSON. |
| Columns | GET | columns | string[] | N | Allows you to specify which columns you would like returned from the output. Pass an array of strings of column names to get only this columns back. |

#### Examples

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/utilities/search?query=apple&token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

```text
[
    {
    "ticker":"AAPL",
    "assetType":"Stock",
    "countryCode":"US",
    "isActive":true,
    "name":"Apple Inc",
    "openFIGI":"BBG000B9XRY4",
    "permaTicker":"US000000000038"
    },
    {
    "ticker":"PNPL",
    "assetType":"Stock",
    "countryCode":"US",
    "isActive":true,
    "name":"Pineapple Exprss",
    "openFIGI":null,
    "permaTicker":"US000000047877"
    },
..]
```
