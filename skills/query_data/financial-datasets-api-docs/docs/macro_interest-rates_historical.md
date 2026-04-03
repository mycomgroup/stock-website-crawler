# Historical

## 源URL

https://docs.financialdatasets.ai/api/macro/interest-rates/historical

## 描述

Historical interest rates for all major central banks in the world.

## 请求端点

**方法**: `GET`

```text
https://api.financialdatasets.ai/macro/interest-rates
```

## 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `X-API-KEY` | string | ✓ | API key for authentication. (Header参数) |
| `bank` | string | ✓ | The bank whose interest rates to return. Use the /macro/interest-rates/banks endpoint to get a list of available banks. |
| `start_date` | string | - | The start date of the interest rates to return in YYYY-MM-DD format. |
| `end_date` | string | - | The end date of the interest rates to return in YYYY-MM-DD format. |

## cURL 示例

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/macro/interest-rates \
  --header 'X-API-KEY: <api-key>'
```

## Python 示例

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set parameters
bank = 'FED'  # required
start_date = '2000-01-01'  # optional
end_date = '2025-01-01'    # optional

# create the URL with parameters
url = (
    f'https://api.financialdatasets.ai/macro/interest-rates'
    f'?bank={bank}'
    f'&start_date={start_date}'
    f'&end_date={end_date}'
)

# make API request
response = requests.get(url, headers=headers)

# parse snapshot from the response
interest_rates = response.json().get('interest_rates')
```

## 响应示例

```json
{
  "interest_rates": [
    {
      "bank": "<string>",
      "name": "<string>",
      "rate": 123,
      "date": "<string>"
    }
  ]
}
```

---

## 详细文档

```
Interest Rates (Historical)

cURL

curl --request GET \
  --url https://api.financialdatasets.ai/macro/interest-rates \
  --header 'X-API-KEY: <api-key>'

{
  "interest_rates": [
    {
      "bank": "<string>",
      "name": "<string>",
      "rate": 123,
      "date": "<string>"
    }
  ]
}
Interest Rates
Historical

Historical interest rates for all major central banks in the world.

GET
/
macro
/
interest-rates


Overview
The Interest Rates API lets you pull historical published interest rate data for all major central banks in the world.
We source our data directly from global central banks like the Federal Reserve, People’s Bank of China, European Central Bank, Bank of Japan, and other major monetary authorities. The real-time interest rate data comes from official monetary policy announcements.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.

Available Central Banks
You can fetch a list of available central banks with a GET request to: https://api.financialdatasets.ai/macro/interest-rates/banks/

Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add the bank parameter, which is required
Execute the API request.

Example
Interest Rates
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set parameters
bank = 'FED'  # required
start_date = '2000-01-01'  # optional
end_date = '2025-01-01'    # optional

# create the URL with parameters
url = (
    f'https://api.financialdatasets.ai/macro/interest-rates'
    f'?bank={bank}'
    f'&start_date={start_date}'
    f'&end_date={end_date}'
)

# make API request
response = requests.get(url, headers=headers)

# parse snapshot from the response
interest_rates = response.json().get('interest_rates')

Authorizations

X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters

bank
stringrequired

The bank whose interest rates to return. Use the /macro/interest-rates/banks endpoint to get a list of available banks.


start_date
string

The start date of the interest rates to return in YYYY-MM-DD format.


end_date
string

The end date of the interest rates to return in YYYY-MM-DD format.

Response
200
application/json

Interest rates response


interest_rates
object[]

Hide child attributes


interest_rates.bank
string

The symbol of the central bank.


interest_rates.name
string

The name of the central bank.


interest_rates.rate
number

The interest rate of the central bank.


interest_rates.date
string

The date of the interest rate in YYYY-MM-DD format.

Ownership (by ticker)
Snapshot
```
