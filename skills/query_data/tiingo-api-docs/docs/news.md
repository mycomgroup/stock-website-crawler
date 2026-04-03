# 2.2.1 Overview

## 源URL

https://www.tiingo.com/documentation/news

## 描述

Tiingo's news feeds are some of the most comprehensive news feeds available. We not only incorporate financial news sites, but also financial blogs - including those of small-time reputable bloggers, and tag them using the latest algos our team has been developing for over a decade. We bring these powerful feeds to you.

On a typical day, Tiingo adds over 8,000-12,000 articles a day.

You can find out about the full product offering on the Product - News page.

## 2.2.2 News Endpoint

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| Article ID | id | int32 | Unique identifier specific to the news article. |
| Title | title | string | Title of the news article. |
| URL | url | string | URL of the news article. |
| Description | description | string | Long-form descripton of the news story. |
| Published Date | publishedDate | datetime | The datetime the news story was published in UTC. This is usually reported by the news source and not by Tiingo.                 If the news source does not declare a published date,                 Tiingo will use the time the news story was discovered by our crawler farm. |
| Crawl Date | crawlDate | datetime | The datetime the news story was added to our database in UTC. This is always recorded by Tiingo and                 the news source has no input on this date. If you note a large gap between crawlDate and publishedDate,                 it means the news article was backfilled, which usually happens when we add a new data source or                 gain access to historical data archives. |
| News Source | source | string | The domain the news source is from. |
| Tickers | tickers | string[] | What tickers are mentioned in the news story using Tiingo's proprietary tagging algo. |
| Tags | tags | string[] | Tags that are mapped and discovered by Tiingo using Tiingo's proprietary tagging algo. |

```text
# For the latest news
https://api.tiingo.com/tiingo/news

# For the latest news for specific tickers
https://api.tiingo.com/tiingo/news?tickers=aapl,googl

# For the latest news for specific tags/countries/topics/tc
https://api.tiingo.com/tiingo/news?tags=election,argentina
```

## 2.2.3 Bulk Download

To download the entire database, use the following REST endpoints. An "incremental" batchType file is added every evening. At 12am EST a batch process runs saving down all news articles for the past 24 hours.

Note: Bulk Download can only be opened up to our institutional clients.

| Field Name | JSON Field | Data Type | Description |
| --- | --- | --- | --- |
| File ID | id | int32 | Unique identifier specific to the bulk download file. Used to select which file to download. |
| URL | url | string | A url you can use to directly download the batch file. NOTE: This url contains your Auth Token and is meant to be a "copy/paste" url for your convenience |
| Filename | filename | string | The filename of the batch file. |
| Batch Type | batchType | string | Describes what kind of batch file this is. The value will either be: "base" or "incremental". base is an entire dump of the data and incremental is a partial dump of the data. This should be used in conjunction with the startDate and endDate parameters to identify the bounds of the data dump. |
| Start Date | startDate | date | The start date that was used to select the News objects to generate the batch file. This is inclusive. publishedDate >= startDate. |
| End Date | startDate | date | The end date that was used to select the News objects to generate the batch file. This is not inclusive. publishedDate < endDate. |
| Compressed file size | fileSizeCompressed | int64 | The size of the file in bytes compressed using gzip. |
| Uncompressed file size | fileSizeUncompressed | int64 | The size of the file in bytes uncompressed. |

```text
# For a list of all the bulk download files
https://api.tiingo.com/tiingo/news/bulk_download

# To download a specific batch file
https://api.tiingo.com/tiingo/news/bulk_download/{id}
```

### 2.2.1 Overview - Tab 内容

#### Request

| Field Name | Parameter | JSON Field | Data Type | Required | Description |
| --- | --- | --- | --- | --- | --- |
| Tickers | GET | tickers | string[] | N | A comma-separated list of the tickers requested. When passing via GET parameter (not in URL), use a JSON array, otherwise use a comma-separated list.

#Use the below format if querying directly in the URL
https://api.tiingo.com/tiingo/news?tickers=aapl,googl

#Otherwise, if passing GET parameters via a request library, use a JSON array like this:
tickers : ['aapl','googl'] |
| Source (domains) | GET | source | string[] | N | A comma-separated list of the tags requested. When passing via GET parameter (not in URL), use a JSON array, otherwise use a comma-separated list.

#Use the below format if querying directly in the URL
https://api.tiingo.com/tiingo/news?source=bloomberg.com,reuters.com

#Otherwise, if passing GET parameters via a request library, use a JSON array like this:
source : ['bloomberg.com','reuters.com'] |
| Start Date | GET | startDate | date | N | If startDate or endDate is not null, historical data will be queried. This filter limits news stories to on or later than the publishedDate (>=). Parameter must be in YYYY-MM-DD format. |
| End Date | GET | endDate | date | N | If startDate or endDate is not null, historical data will be queried. This filter limits news stories to on or less than the publishedDate (<=). Parameter must be in YYYY-MM-DD format. |
| Limit | GET | limit | int32 | N | The maximum number of news objects to return in the array. The default is 100 and the max is 1000. This is maxed to 1,000 as any more than that tends to lead to longer wait times. 
If you would like this adjusted, please contact us at support@tiingo.com. |
| Offset | GET | offset | int32 | N | This is a "pagination" variable that is often used alongside limit. It returns an array with the results shifted by "offset". For example, when limit is 0 you may get the following: 

0. News Story A
1. News Story B
2. News Story C
3. News Story D

When offset is "2" you will receive:

0. News Story C
1. News Story D
2. News Story E
3. News Story F

This, when used alongside "limit" allows for pagination and more efficient queries. |
| Sort By | GET | sortBy | string | N | The field can take either "publishedDate" or "crawlDate". The date field specified will be used to sort the results in descending order. The results can either be sorted by when the news outlet reported the publish time ("datePublished") or when our feeds came across is ("crawlDate"). Defaults to "publishedDate" if no value provided |

```text
#Use the below format if querying directly in the URL
https://api.tiingo.com/tiingo/news?tickers=aapl,googl

#Otherwise, if passing GET parameters via a request library, use a JSON array like this:
tickers : ['aapl','googl']
```

```text
#Use the below format if querying directly in the URL
https://api.tiingo.com/tiingo/news?source=bloomberg.com,reuters.com

#Otherwise, if passing GET parameters via a request library, use a JSON array like this:
source : ['bloomberg.com','reuters.com']
```

```text
0. News Story A
1. News Story B
2. News Story C
3. News Story D
```

```text
0. News Story C
1. News Story D
2. News Story E
3. News Story F
```

#### Examples

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/news?token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

```text
[{
    "source":"cnbc.com",
    "crawlDate":"2019-01-29T22:20:01.696871Z",
    "description":"Apple CEO Tim Cook told CNBC that trade tensions between the U.S. and China have improved since late
    December.",
    "url":"https://www.cnbc.com/2019/01/29/apples-ceo-sees-optimism-as-trade-tension-between-us-and-china-lessens.html",
    "publishedDate":"2019-01-29T22:17:00Z",
    "tags":[
    "China",
    "Economic Measures",
    "Economics",
    "Markets",
    "Stock",
    "Technology",
    "Tiingo Top",
    "Trade"
    ],
    "tickers":[
    "aapl"
    ],
    "id":15063835,
    "title":"Apple CEO Tim Cook on US-China trade negotiations: 'There is a bit more optimism in the air'"
}...]
```

#### Python

```text
import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/news?token=Not logged-in or registered. Please login or register to see your API Token", headers=headers)
print(requestResponse.json())
```

#### Node

```text
var request = require('request');
var requestOptions = {
    'url': 'https://api.tiingo.com/tiingo/news?token=Not logged-in or registered. Please login or register to see your API Token',
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
$res = $client->get("https://api.tiingo.com/tiingo/news?token=Not logged-in or registered. Please login or register to see your API Token", [
'headers' => [
    'Content-type' =>  'application/json'
    ]
]);
```
