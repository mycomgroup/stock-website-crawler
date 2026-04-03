# Real-time Benzinga News

## 源URL

https://massive.com/docs/rest/partners/benzinga/news

## 描述

Retrieve real-time structured, timestamped news articles from Benzinga, including headlines, full-text content, tickers, categories, and more. Each article entry contains metadata such as author, publication time, and topic channels, as well as optional elements like teaser summaries, article body text, and images. Some headline-only articles are included for faster delivery of time-sensitive market news. Articles can be filtered by ticker and time, and are returned in a consistent format for easy parsing and integration. This endpoint is ideal for building alerting systems, autonomous risk analysis, and sentiment-driven trading strategies.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| published | string | 否 | The timestamp (formatted as an ISO 8601 timestamp) when the news article was originally published. Value must be an integer timestamp in seconds, formatted 'yyyy-mm-dd', or ISO 8601/RFC 3339 (e.g. '2024-05-28T20:27:41Z'). |
| channels | string | 否 | Filter for arrays that contain the value. |
| tags | string | 否 | Filter for arrays that contain the value. |
| author | string | 否 | The name of the journalist or entity that authored the news article. |
| stocks | string | 否 | Filter for arrays that contain the value. |
| tickers | string | 否 | Filter for arrays that contain the value. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'published' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| author | string | 否 | The name of the journalist or entity that authored the news article. |
| benzinga_id | integer | 否 | The identifer used by Benzinga for this record. |
| body | string | 否 | The full text content of the news article. |
| channels | array (string) | 否 | A list of categories or topics that the article belongs to (e.g., 'News', 'Price Target'). |
| images | array (string) | 否 | A list of images associated with the article. |
| last_updated | string | 否 | The timestamp (formatted as an ISO 8601 timestamp) when the news article was last updated in the system. |
| published | string | 否 | The timestamp (formatted as an ISO 8601 timestamp) when the news article was originally published. |
| tags | array (string) | 否 | A list of tags that describe the themes or content of the article. |
| teaser | string | 否 | A short summary or lead-in to the news article's content. |
| tickers | array (string) | 否 | A list of stock or crypto tickers mentioned in the article. |
| title | string | 否 | The headline of the news article. |
| url | string | 否 | The direct link to the source of the news article. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/benzinga/v2/news
```

### Request

```bash
curl -X GET "https://api.massive.com/benzinga/v2/news?limit=100&sort=published.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "author": "Adam Eckert",
      "benzinga_id": 39046904,
      "body": "<p><strong>CAVA Group Inc</strong> (NYSE:<a class=\"ticker\" href=\"https://www.benzinga.com/stock/CAVA#NYSE\">CAVA</a>) reported financial results for the first quarter of fiscal 2024 after market close on Tuesday. Here&#8217;s a look at the <a href=\"https://www.benzinga.com/pressreleases/24/05/b39046606/cava-group-reports-first-quarter-2024-results\">key metrics from the quarter</a>.</p>",
      "channels": [
        "earnings",
        "news",
        "restaurants",
        "after-hours center",
        "movers"
      ],
      "images": [
        "https://cdn.benzinga.com/files/imagecache/250x187xUP/images/story/2024/05/28/CAVA-group.jpeg",
        "https://cdn.benzinga.com/files/imagecache/1024x768xUP/images/story/2024/05/28/CAVA-group.jpeg",
        "https://cdn.benzinga.com/files/imagecache/2048x1536xUP/images/story/2024/05/28/CAVA-group.jpeg"
      ],
      "last_updated": "2024-05-28T20:27:42Z",
      "published": "2024-05-28T20:27:41Z",
      "tags": [
        "why it's moving"
      ],
      "teaser": "Cava&#39;s first-quarter revenue increased 30.3% year-over-year to $256.3 million, which beat the consensus estimate of $245.935 million, according to Benzinga Pro.",
      "tickers": [
        "CAVA"
      ],
      "title": "Cava Group Q1 Earnings: Revenue Beat, EPS Beat, Guidance Raise, Continued Investments In Scalable Infrastructure And More",
      "url": "https://www.benzinga.com/news/earnings/24/05/39046904/cava-group-q1-earnings-revenue-beat-eps-beat-guidance-raise-continued-investments-in-scalable-infra"
    }
  ],
  "status": "OK"
}
```
