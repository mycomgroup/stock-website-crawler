---
id: "url-2747109d"
type: "website"
title: "Search by ISIN New Feature"
url: "https://eodhd.com/financial-apis-blog/search-by-isins-new-feature"
description: "Today we introduce a new feature to our Search API – search by ISINs. International Securities Identification Numbers (or ISINs) are very important for investors and traders. And we keep the deep attention on our ISINs database. We keep to add more and more numbers and for the moment we have already 45000+ ISINs."
source: ""
tags: []
crawl_time: "2026-03-18T04:26:53.413Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Search by ISIN New Feature\n\n## 正文\n\nToday we introduce a new feature to our Search API – search by ISINs. International Securities Identification Numbers (or ISINs) are very important for investors and traders. And we keep the deep attention on our ISINs database. We keep to add more and more numbers and for the moment we have already 45000+ ISINs.\n\nIt’s easy to use the search, just use ISIN in the query string. Either complete or incomplete ISINs are accepted. Below you can see an example of query and output with incomplete ISIN:\n\nhttps://eodhistoricaldata.com/api/search/AAPL?api_token=YOUR_API_TOKEN\n\nIf you have CUSIPs only in your database, it’s easy to calculate ISIN from CUSIP.  You should add ‘US’ characters to the beginning of the CUSIP and the checksum to the end. The checksum is calculated with the Luhn Algorithm. If it’s hard to calculate the checksum, you can search for incomplete ISIN, if we have this ISIN in our database, we find it.\n\nMore information and examples you can find on our documentation page for Search API.\n\n> https://eodhistoricaldata.com/api/search/AAPL?api_token=YOUR_API_TOKEN\n\n![Search By ISIN](https://eodhd.com/financial-apis-blog/wp-content/uploads/2019/12/search_by_isin.jpg)\n\n![Search By ISIN. ISIN Lookup](https://eodhistoricaldata.com/financial-apis-blog/wp-content/uploads/2019/12/image.png)\n"
  rawContent: ""
  suggestedFilename: "-blog_search-by-isins-new-feature"
  publishDate: ""
  author: ""
  categories: []
---

# Search by ISIN New Feature

## 源URL

https://eodhd.com/financial-apis-blog/search-by-isins-new-feature

## 正文

Today we introduce a new feature to our Search API – search by ISINs. International Securities Identification Numbers (or ISINs) are very important for investors and traders. And we keep the deep attention on our ISINs database. We keep to add more and more numbers and for the moment we have already 45000+ ISINs.

It’s easy to use the search, just use ISIN in the query string. Either complete or incomplete ISINs are accepted. Below you can see an example of query and output with incomplete ISIN:

https://eodhistoricaldata.com/api/search/AAPL?api_token=YOUR_API_TOKEN

If you have CUSIPs only in your database, it’s easy to calculate ISIN from CUSIP.  You should add ‘US’ characters to the beginning of the CUSIP and the checksum to the end. The checksum is calculated with the Luhn Algorithm. If it’s hard to calculate the checksum, you can search for incomplete ISIN, if we have this ISIN in our database, we find it.

More information and examples you can find on our documentation page for Search API.

> https://eodhistoricaldata.com/api/search/AAPL?api_token=YOUR_API_TOKEN

![Search By ISIN](https://eodhd.com/financial-apis-blog/wp-content/uploads/2019/12/search_by_isin.jpg)

![Search By ISIN. ISIN Lookup](https://eodhistoricaldata.com/financial-apis-blog/wp-content/uploads/2019/12/image.png)
