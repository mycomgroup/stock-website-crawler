# Contract Overview

## 源URL

https://massive.com/docs/rest/options/contracts/contract-overview

## 描述

Retrieve detailed information about a specific options contract, including its contract type (call or put), exercise style, expiration date, strike price, shares per contract, underlying ticker, and primary exchange. This endpoint provides essential attributes for understanding the contract’s structure and evaluating it within broader options strategies and portfolios.

## Endpoint

```
GET /v3/reference/options/contracts/{options_ticker}
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| options_ticker | string | 否 | Query for a contract by options ticker. You can learn more about the structure of options tickers here. |
| as_of | string | 否 | Specify a point in time for the contract as of this date with format YYYY-MM-DD. Defaults to today's date. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| request_id | string | 否 | A request id assigned by the server. |
| results | object | 否 | Contains the requested data for the specified options contract. |
| additional_underlyings | array (object) | 否 | If an option contract has additional underlyings or deliverables associated with it, they will appear here.<br>See here for some examples of what might cause a contract to have additional underlyings. |
| cfi | string | 否 | The 6 letter CFI code of the contract (defined in ISO 10962) |
| contract_type | string | 否 | The type of contract. Can be "put", "call", or in some rare cases, "other". |
| correction | integer | 否 | The correction number for this option contract. |
| exercise_style | enum | 否 | The exercise style of this contract. See this link for more details on exercise styles. |
| expiration_date | string | 否 | The contract's expiration date in YYYY-MM-DD format. |
| primary_exchange | string | 否 | The MIC code of the primary exchange that this contract is listed on. |
| shares_per_contract | number | 否 | The number of shares per contract for this contract. |
| strike_price | number | 否 | The strike price of the option contract. |
| ticker | string | 否 | The ticker for the option contract. |
| underlying_ticker | string | 否 | The underlying ticker that the option contract relates to. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/v3/reference/options/contracts/{options_ticker}
```

### Request

```bash
curl -X GET "https://api.massive.com/v3/reference/options/contracts/O:SPY251219C00650000?apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": "603902c0-a5a5-406f-bd08-f030f92418fa",
  "results": {
    "additional_underlyings": [
      {
        "amount": 44,
        "type": "equity",
        "underlying": "VMW"
      },
      {
        "amount": 6.53,
        "type": "currency",
        "underlying": "USD"
      }
    ],
    "cfi": "OCASPS",
    "contract_type": "call",
    "exercise_style": "american",
    "expiration_date": "2021-11-19",
    "primary_exchange": "BATO",
    "shares_per_contract": 100,
    "strike_price": 85,
    "ticker": "O:AAPL211119C00085000",
    "underlying_ticker": "AAPL"
  },
  "status": "OK"
}
```
