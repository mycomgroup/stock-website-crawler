# All Contracts

## 源URL

https://massive.com/docs/rest/options/contracts/all-contracts

## 描述

Retrieve a comprehensive index of options contracts, encompassing both active and expired listings. This endpoint can return a broad selection of contracts or be narrowed down to those tied to a specific underlying ticker. Each contract entry includes details such as contract type (call/put), exercise style, expiration date, and strike price. By exploring this index, users can assess market availability, analyze contract characteristics, and refine their options trading or research strategies.

## Endpoint

```
GET /v3/reference/options/contracts
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| underlying_ticker | string | 否 | Query for contracts relating to an underlying stock ticker. |
| ticker | string | 否 | This parameter has been deprecated. To search by specific options ticker, use the Options Contract endpoint here. |
| contract_type | enum (string) | 否 | Query by the type of contract. |
| expiration_date | string | 否 | Query by contract expiration with date format YYYY-MM-DD. |
| as_of | string | 否 | Specify a point in time for contracts as of this date with format YYYY-MM-DD. Defaults to today's date. |
| strike_price | number | 否 | Query by strike price of a contract. |
| expired | boolean | 否 | Query for expired contracts. Default is false. |
| order | enum (string) | 否 | Order results based on the `sort` field. |
| limit | integer | 否 | Limit the number of results returned, default is 10 and max is 1000. |
| sort | enum (string) | 否 | Sort field used for ordering. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page of data. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | An array of results containing the requested data. |
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
/v3/reference/options/contracts
```

### Request

```bash
curl -X GET "https://api.massive.com/v3/reference/options/contracts?order=asc&limit=10&sort=ticker&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": "603902c0-a5a5-406f-bd08-f030f92418fa",
  "results": [
    {
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
    {
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
      "strike_price": 90,
      "ticker": "O:AAPL211119C00090000",
      "underlying_ticker": "AAPL"
    }
  ],
  "status": "OK"
}
```
