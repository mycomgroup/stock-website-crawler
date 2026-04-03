---
id: "url-7aafea52"
type: "api"
title: "Java Stock API Example"
url: "https://eodhd.com/financial-apis/java-stock-api-example"
description: "Here you can find a Java example on how to use our API."
source: ""
tags: []
crawl_time: "2026-03-18T03:05:32.771Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Java Stock API Example\n\nHere you can find a Java example on how to use our API.\n\n\n## Code Examples\n\n```text\nimport com.google.gson.annotations.Expose;\nimport com.google.gson.annotations.SerializedName;\n\npublic class EodStock {\n\n    @SerializedName(\"General\")\n    @Expose\n    private General general;\n    @SerializedName(\"Highlights\")\n    @Expose\n    private Highlights highlights;\n    @SerializedName(\"Earnings\")\n    @Expose\n    private Earnings earnings;\n    @SerializedName(\"Financials\")\n    @Expose\n    private Financials financials;\n\n    public General getGeneral() {\n        return general;\n    }\n\n    public void setGeneral(General general) {\n        this.general = general;\n    }\n\n    public Highlights getHighlights() {\n        return highlights;\n    }\n\n    public void setHighlights(Highlights highlights) {\n        this.highlights = highlights;\n    }\n\n    public Earnings getEarnings() {\n        return earnings;\n    }\n\n    public void setEarnings(Earnings earnings) {\n        this.earnings = earnings;\n    }\n\n    public Financials getFinancials() {\n        return financials;\n    }\n\n    public void setFinancials(Financials financials) {\n        this.financials = financials;\n    }\n\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "java-stock-api-example"
---

# Java Stock API Example

## 源URL

https://eodhd.com/financial-apis/java-stock-api-example

## 描述

Here you can find a Java example on how to use our API.

## 文档正文

Here you can find a Java example on how to use our API.

## Code Examples

```text
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class EodStock {

    @SerializedName("General")
    @Expose
    private General general;
    @SerializedName("Highlights")
    @Expose
    private Highlights highlights;
    @SerializedName("Earnings")
    @Expose
    private Earnings earnings;
    @SerializedName("Financials")
    @Expose
    private Financials financials;

    public General getGeneral() {
        return general;
    }

    public void setGeneral(General general) {
        this.general = general;
    }

    public Highlights getHighlights() {
        return highlights;
    }

    public void setHighlights(Highlights highlights) {
        this.highlights = highlights;
    }

    public Earnings getEarnings() {
        return earnings;
    }

    public void setEarnings(Earnings earnings) {
        this.earnings = earnings;
    }

    public Financials getFinancials() {
        return financials;
    }

    public void setFinancials(Financials financials) {
        this.financials = financials;
    }

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
