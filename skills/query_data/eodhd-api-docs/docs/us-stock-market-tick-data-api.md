---
id: "url-7feccb5f"
type: "api"
title: "Tick Data API: US Stock Market"
url: "https://eodhd.com/financial-apis/us-stock-market-tick-data-api"
description: "The US Stock Market Ticks Data API provides granular tick data for all US equities spanning across all exchanges."
source: ""
tags: []
crawl_time: "2026-03-18T03:09:08.679Z"
metadata:
  endpoint: "https://eodhd.com/api/ticks/"
  parameters: []
  markdownContent: "# Tick Data API: US Stock Market\n\nThe US Stock Market Ticks Data API provides granular tick data for all US equities spanning across all exchanges.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/ticks/?s=AAPL&from=1694455200&to=1694541600&limit=1&api_token=demo&fmt=json\n```\n\n\n## Quick Start\n\nTo get historical stock tick data, use the following URL:\n\nFor testing purposes, you can try the following API Key (works only for AAPL.US ticker): demo\n\n## Output\n\nJSON response example:\n\nWhere the fields are:\n\n## Trading codes (sl field)\n\n@  – Regular SaleA – AcquisitionB – Bunched TradeC  – Cash SaleD  – DistributionE  – PlaceholderF – Intermarket SweepG – Bunched Sold TradeH – Price Variation TradeI – Odd Lot TradeK – Rule 155 Trade (AMEX)L – Sold LastM – Market Center Official CloseN – Next DayO – Opening PrintsP – Prior Reference PriceQ – Market Center Official OpenR – SellerS – Split TradeT – Form TU – Extended trading hours (Sold Out of Sequence)V – Contingent TradeW – Average Price TradeX – Cross/Periodic Auction TradeY – Yellow Flag Regular TradeZ – Sold (out of sequence)\n\nYou can also check our Intraday Data API and Real-Time Data API via WebSockets.\n\n## Code Examples\n\n```json\n{\n\"mkt\":[\"V\"],\n\"price\":[179.25],\n\"seq\":[376150475],\n\"shares\":[100],\n\"sl\":[\"@   \"],\n\"sub_mkt\":[\"\"],\n\"ts\":[1694455200017]\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "us-stock-market-tick-data-api"
---

# Tick Data API: US Stock Market

## 源URL

https://eodhd.com/financial-apis/us-stock-market-tick-data-api

## 描述

The US Stock Market Ticks Data API provides granular tick data for all US equities spanning across all exchanges.

## API 端点

**Endpoint**: `https://eodhd.com/api/ticks/`

## 文档正文

The US Stock Market Ticks Data API provides granular tick data for all US equities spanning across all exchanges.

## API Endpoint

```text
https://eodhd.com/api/ticks/?s=AAPL&from=1694455200&to=1694541600&limit=1&api_token=demo&fmt=json
```

## Quick Start

To get historical stock tick data, use the following URL:

For testing purposes, you can try the following API Key (works only for AAPL.US ticker): demo

## Output

JSON response example:

Where the fields are:

## Trading codes (sl field)

@  – Regular SaleA – AcquisitionB – Bunched TradeC  – Cash SaleD  – DistributionE  – PlaceholderF – Intermarket SweepG – Bunched Sold TradeH – Price Variation TradeI – Odd Lot TradeK – Rule 155 Trade (AMEX)L – Sold LastM – Market Center Official CloseN – Next DayO – Opening PrintsP – Prior Reference PriceQ – Market Center Official OpenR – SellerS – Split TradeT – Form TU – Extended trading hours (Sold Out of Sequence)V – Contingent TradeW – Average Price TradeX – Cross/Periodic Auction TradeY – Yellow Flag Regular TradeZ – Sold (out of sequence)

You can also check our Intraday Data API and Real-Time Data API via WebSockets.

## Code Examples

```json
{
"mkt":["V"],
"price":[179.25],
"seq":[376150475],
"shares":[100],
"sl":["@   "],
"sub_mkt":[""],
"ts":[1694455200017]
}
```

## Related APIs

- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)
- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)
- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)
- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)
- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)
- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)
- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)
- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)
- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)
- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)
