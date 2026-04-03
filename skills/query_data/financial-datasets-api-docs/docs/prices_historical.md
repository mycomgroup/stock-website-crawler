# Historical

## 源URL

https://docs.financialdatasets.ai/api/prices/historical

## 描述

Get end-of-day (EOD) historical price data for stocks.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/prices`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The stock ticker symbol (e.g. AAPL, MSFT). |
| `interval` | enum | 是 | - | The time interval for the price data. |
| `start_date` | string | 是 | - | The start date for the price data (format: YYYY-MM-DD). |
| `end_date` | string | 是 | - | The end date for the price data (format: YYYY-MM-DD). |

## 响应字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `open` | number | The open price of the ticker in the given time period. |
| `close` | number | The close price of the ticker in the given time period. |
| `high` | number | The high price of the ticker in the given time period. |
| `low` | number | The low price of the ticker in the given time period. |
| `volume` | integer | <number> |
| `time` | string | The human-readable time format of the price in UTC. |
| `time_milliseconds` | number | The timestamp of the price in milliseconds since epoch. |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/prices \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "ticker": "<string>",
  "prices": [
    {
      "open": 123,
      "close": 123,
      "high": 123,
      "low": 123,
      "volume": 123,
      "time": "<string>",
      "time_milliseconds": 123
    }
  ]
}
```

### 示例 3 (python)

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'AAPL'
interval = 'day'         # possible values are {'day', 'week', 'month', 'year'}
start_date = '2025-01-02'
end_date = '2025-01-05'

# create the URL
url = (
    f'https://api.financialdatasets.ai/prices/'
    f'?ticker={ticker}'
    f'&interval={interval}'
    f'&start_date={start_date}'
    f'&end_date={end_date}'
)

# make API request
response = requests.get(url, headers=headers)

# parse prices from the response
prices = response.json().get('prices')
```
