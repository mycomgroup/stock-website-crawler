---
id: "url-408cd2fc"
type: "website"
title: "New ISINs have been added"
url: "https://eodhd.com/financial-apis-blog/new-isins-have-been-added"
description: "Great news for our Fundamental Data API users. Today we have added more than 24000 new ISINs for symbols from 48 exchanges all around the world, including ISINs for US exchanges, London Stock Exchange, Euronext Exchanges, Brazil Exchange, Chinese exchanges, Singapore Exchange and many other."
source: ""
tags: []
crawl_time: "2026-03-18T04:36:35.319Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# New ISINs have been added\n\n## 正文\n\nGreat news for our Fundamental Data API users. Today we have added more than 24000 new ISINs for symbols from 48 exchanges all around the world, including ISINs for US exchanges, London Stock Exchange, Euronext Exchanges, Brazil Exchange, Chinese exchanges, Singapore Exchange and many other.\n\nRight now, the total number of tickers with ISINs in our database is more than 35000, including ISINs for stocks, ETFs, mutual funds and bonds. For bonds, ISINs are the primary identification.\n\nFor US symbols we also provide CUSIPs. A CUSIP is a 9-character alphanumeric code which identifies a North American financial security. It’s easy to convert ISIN to CUSIP: remove the first two symbols, which are ‘US’ and the last checksum digit. However, it’s a little bit more complicated to convert CUSIP to ISIN. The checksum is calculated with Luhn Algorithm. But we already calculated it for you.\n\nWe also do not recommend to use ISINs as only identification for assets. The reason in that ISINs are not unique ID for symbols. For example, you can have two symbols on different exchanges with the same ISIN: AAPL.US and AAPL.MX. We use TICKER + EXCHANGE as unique ID and like many other data providers.\n\nAnd yes, OpenFIGI support is coming soon!\n\n> Right now, the total number of tickers with ISINs in our database is more than 35000, including ISINs for stocks, ETFs, mutual funds and bonds. For bonds, ISINs are the primary identification.\n\n![](https://eodhd.com/financial-apis-blog/wp-content/uploads/2019/02/james-orr-1346107-unsplash.jpg)\n"
  rawContent: ""
  suggestedFilename: "-blog_new-isins-have-been-added"
  publishDate: ""
  author: ""
  categories: []
---

# New ISINs have been added

## 源URL

https://eodhd.com/financial-apis-blog/new-isins-have-been-added

## 正文

Great news for our Fundamental Data API users. Today we have added more than 24000 new ISINs for symbols from 48 exchanges all around the world, including ISINs for US exchanges, London Stock Exchange, Euronext Exchanges, Brazil Exchange, Chinese exchanges, Singapore Exchange and many other.

Right now, the total number of tickers with ISINs in our database is more than 35000, including ISINs for stocks, ETFs, mutual funds and bonds. For bonds, ISINs are the primary identification.

For US symbols we also provide CUSIPs. A CUSIP is a 9-character alphanumeric code which identifies a North American financial security. It’s easy to convert ISIN to CUSIP: remove the first two symbols, which are ‘US’ and the last checksum digit. However, it’s a little bit more complicated to convert CUSIP to ISIN. The checksum is calculated with Luhn Algorithm. But we already calculated it for you.

We also do not recommend to use ISINs as only identification for assets. The reason in that ISINs are not unique ID for symbols. For example, you can have two symbols on different exchanges with the same ISIN: AAPL.US and AAPL.MX. We use TICKER + EXCHANGE as unique ID and like many other data providers.

And yes, OpenFIGI support is coming soon!

> Right now, the total number of tickers with ISINs in our database is more than 35000, including ISINs for stocks, ETFs, mutual funds and bonds. For bonds, ISINs are the primary identification.

![](https://eodhd.com/financial-apis-blog/wp-content/uploads/2019/02/james-orr-1346107-unsplash.jpg)
