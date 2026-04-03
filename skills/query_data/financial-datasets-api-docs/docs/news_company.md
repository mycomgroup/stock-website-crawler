# Company News

## 源URL

https://docs.financialdatasets.ai/api/news/company

## 描述

Get recent news articles for a given ticker. Articles are sourced from RSS feeds of publishers like The Motley Fool, Investing.com, Reuters, and more.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/news`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol of the company. |

## 响应字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `ticker` | string | The ticker symbol. |
| `title` | string | The title of the news article. |
| `source` | string | The source of the news article. |
| `date` | string | <date> |
| `url` | string | <uri> |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url 'https://api.financialdatasets.ai/news?limit=5' \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "news": [
    {
      "ticker": "<string>",
      "title": "<string>",
      "source": "<string>",
      "date": "2023-12-25",
      "url": "<string>"
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
limit = 5  # optional, max is 10

# create the URL
url = (
    f'https://api.financialdatasets.ai/news'
    f'?ticker={ticker}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse news from the response
news = response.json().get('news')
```
