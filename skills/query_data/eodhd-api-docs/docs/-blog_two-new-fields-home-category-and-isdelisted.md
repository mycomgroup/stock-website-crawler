---
id: "url-1164c5ed"
type: "website"
title: "Two New Fields: Home Category and isDelisted"
url: "https://eodhd.com/financial-apis-blog/two-new-fields-home-category-and-isdelisted"
description: "This week we re-worked again our data and added two new fields to our Fundamental API: “Home Category” and “isDelisted”. You often asked us to add this information to our fundamentals output. And eventually, after some cleaning of the data, we are ready to publish it."
source: ""
tags: []
crawl_time: "2026-03-18T12:06:03.585Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Two New Fields: Home Category and isDelisted\n\n## 正文\n\nThis week we re-worked again our data and added two new fields to our Fundamental API: “Home Category” and “isDelisted”. You often asked us to add this information to our fundamentals output. And eventually, after some cleaning of the data, we are ready to publish it.\n\nIsDelisted flag marks if the ticker is delisted now or not. We have the end of day data for more than 12,000 delisted tickers on the US markets starting from January 2000. It means that if the ticker had been delisted in February 2000 and has a history from 1989, we have the end of day data for this ticker from 1989 till February 2000.\n\nHomeCategory field indicates if the company is Domestic or ADR (American Depositary Receipt). In most cases it’s a foreign company’s stock traded on US markets. For example for AAPL the home category is domestic, but for BABA (Alibaba Group) or YNDX (Yandex) the home category is ADR.\n\nThese fields are available only for US tickers for the moment. More information about the Fundamental API you can read in our documentation.\n\n![Domestic ADR Home Category](https://eodhd.com/financial-apis-blog/wp-content/uploads/2020/07/blue-and-yellow-graph-on-stock-market-monitor-159888.jpg)\n"
  rawContent: ""
  suggestedFilename: "-blog_two-new-fields-home-category-and-isdelisted"
  publishDate: ""
  author: ""
  categories: []
---

# Two New Fields: Home Category and isDelisted

## 源URL

https://eodhd.com/financial-apis-blog/two-new-fields-home-category-and-isdelisted

## 正文

This week we re-worked again our data and added two new fields to our Fundamental API: “Home Category” and “isDelisted”. You often asked us to add this information to our fundamentals output. And eventually, after some cleaning of the data, we are ready to publish it.

IsDelisted flag marks if the ticker is delisted now or not. We have the end of day data for more than 12,000 delisted tickers on the US markets starting from January 2000. It means that if the ticker had been delisted in February 2000 and has a history from 1989, we have the end of day data for this ticker from 1989 till February 2000.

HomeCategory field indicates if the company is Domestic or ADR (American Depositary Receipt). In most cases it’s a foreign company’s stock traded on US markets. For example for AAPL the home category is domestic, but for BABA (Alibaba Group) or YNDX (Yandex) the home category is ADR.

These fields are available only for US tickers for the moment. More information about the Fundamental API you can read in our documentation.

![Domestic ADR Home Category](https://eodhd.com/financial-apis-blog/wp-content/uploads/2020/07/blue-and-yellow-graph-on-stock-market-monitor-159888.jpg)
