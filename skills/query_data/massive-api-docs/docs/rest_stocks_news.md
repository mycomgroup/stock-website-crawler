# News

## 源URL

https://massive.com/docs/rest/stocks/news

## 描述

Retrieve the most recent news articles related to a specified ticker, along with summaries, source details, and sentiment analysis. This endpoint consolidates relevant financial news in one place, extracting associated tickers, assigning sentiment, and providing direct links to the original sources. By incorporating publisher information, article metadata, and sentiment reasoning, users can quickly gauge market sentiment, stay informed on company developments, and integrate news insights into their trading or research workflows.

## Endpoint

```
GET /v2/reference/news
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a case-sensitive ticker symbol. For example, AAPL represents Apple Inc. |
| published_utc | string (date-time, date) | 否 | Return results published on, before, or after this date. |
| order | enum (string) | 否 | Order results based on the `sort` field. |
| limit | integer | 否 | Limit the number of results returned, default is 10 and max is 1000. |
| sort | enum (string) | 否 | Sort field used for ordering. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| count | integer | 否 | The total number of results for this request. |
| next_url | string | 否 | If present, this value can be used to fetch the next page of data. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | An array of results containing the requested data. |
| amp_url | string | 否 | The mobile friendly Accelerated Mobile Page (AMP) URL. |
| article_url | string | 否 | A link to the news article. |
| author | string | 否 | The article's author. |
| description | string | 否 | A description of the article. |
| id | string | 否 | Unique identifier for the article. |
| image_url | string | 否 | The article's image URL. |
| insights | array (object) | 否 | The insights related to the article. |
| keywords | array (string) | 否 | The keywords associated with the article (which will vary depending on<br>the publishing source). |
| published_utc | string | 否 | The UTC date and time when the article was published, formatted in RFC3339 standard (e.g. YYYY-MM-DDTHH:MM:SSZ). |
| publisher | object | 否 | Details the source of the news article, including the publisher's name, logo, and homepage URLs. This information helps users identify and access the original source of news content. |
| tickers | array (string) | 否 | The ticker symbols associated with the article. |
| title | string | 否 | The title of the news article. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/v2/reference/news
```

### Request

```bash
curl -X GET "https://api.massive.com/v2/reference/news?order=asc&limit=10&sort=published_utc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "next_url": "https://api.massive.com:443/v2/reference/news?cursor=eyJsaW1pdCI6MSwic29ydCI6InB1Ymxpc2hlZF91dGMiLCJvcmRlciI6ImFzY2VuZGluZyIsInRpY2tlciI6e30sInB1Ymxpc2hlZF91dGMiOnsiZ3RlIjoiMjAyMS0wNC0yNiJ9LCJzZWFyY2hfYWZ0ZXIiOlsxNjE5NDA0Mzk3MDAwLG51bGxdfQ",
  "request_id": "831afdb0b8078549fed053476984947a",
  "results": [
    {
      "amp_url": "https://m.uk.investing.com/news/stock-market-news/markets-are-underestimating-fed-cuts-ubs-3559968?ampMode=1",
      "article_url": "https://uk.investing.com/news/stock-market-news/markets-are-underestimating-fed-cuts-ubs-3559968",
      "author": "Sam Boughedda",
      "description": "UBS analysts warn that markets are underestimating the extent of future interest rate cuts by the Federal Reserve, as the weakening economy is likely to justify more cuts than currently anticipated.",
      "id": "8ec638777ca03b553ae516761c2a22ba2fdd2f37befae3ab6fdab74e9e5193eb",
      "image_url": "https://i-invdn-com.investing.com/news/LYNXNPEC4I0AL_L.jpg",
      "insights": [
        {
          "sentiment": "positive",
          "sentiment_reasoning": "UBS analysts are providing a bullish outlook on the extent of future Federal Reserve rate cuts, suggesting that markets are underestimating the number of cuts that will occur.",
          "ticker": "UBS"
        }
      ],
      "keywords": [
        "Federal Reserve",
        "interest rates",
        "economic data"
      ],
      "published_utc": "2024-06-24T18:33:53Z",
      "publisher": {
        "favicon_url": "https://s3.massive.com/public/assets/news/favicons/investing.ico",
        "homepage_url": "https://www.investing.com/",
        "logo_url": "https://s3.massive.com/public/assets/news/logos/investing.png",
        "name": "Investing.com"
      },
      "tickers": [
        "UBS"
      ],
      "title": "Markets are underestimating Fed cuts: UBS By Investing.com - Investing.com UK"
    }
  ],
  "status": "OK"
}
```
