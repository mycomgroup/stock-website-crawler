# Ticker Overview

## 源URL

https://massive.com/docs/rest/stocks/tickers/ticker-overview

## 描述

Retrieve comprehensive details for a single ticker supported by Massive. This endpoint offers a deep look into a company’s fundamental attributes, including its primary exchange, standardized identifiers (CIK, composite FIGI, share class FIGI), market capitalization, industry classification, and key dates. Users also gain access to branding assets (e.g., logos, icons), enabling them to enrich applications and analyses with visually consistent, contextually relevant information.

## Endpoint

```
GET /v3/reference/tickers/{ticker}
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a case-sensitive ticker symbol. For example, AAPL represents Apple Inc. |
| date | string | 否 | Specify a point in time to get information about the ticker available on that date.<br>When retrieving information from SEC filings, we compare this date with the period of report date on the SEC filing.For example, consider an SEC filing submitted by AAPL on 2019-07-31, with a period of report date ending on 2019-06-29.<br>That means that the filing was submitted on 2019-07-31, but the filing was created based on information from 2019-06-29.<br>If you were to query for AAPL details on 2019-06-29, the ticker details would include information from the SEC filing.Defaults to the most recent available date. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| count | integer | 否 | The total number of results for this request. |
| request_id | string | 否 | A request id assigned by the server. |
| results | object | 否 | Ticker with details. |
| active | boolean | 否 | Whether or not the asset is actively traded. False means the asset has been delisted. |
| address | object | 否 | Company headquarters address details. |
| branding | object | 否 | Provides URLs aiding in visual identification. |
| cik | string | 否 | The CIK number for this ticker. Find more information here. |
| composite_figi | string | 否 | The composite OpenFIGI number for this ticker. Find more information here |
| currency_name | string | 否 | The name of the currency that this asset is traded with. |
| delisted_utc | string | 否 | The last date that the asset was traded. |
| description | string | 否 | A description of the company and what they do/offer. |
| homepage_url | string | 否 | The URL of the company's website homepage. |
| list_date | string | 否 | The date that the symbol was first publicly listed in the format YYYY-MM-DD. |
| locale | enum | 否 | The locale of the asset. |
| market | enum | 否 | The market type of the asset. |
| market_cap | number | 否 | The most recent close price of the ticker multiplied by weighted outstanding shares. |
| name | string | 否 | The name of the asset. For stocks/equities this will be the companies registered name. For crypto/fx this will be the name of the currency or coin pair. |
| phone_number | string | 否 | The phone number for the company behind this ticker. |
| primary_exchange | string | 否 | The ISO code of the primary listing exchange for this asset. |
| round_lot | number | 否 | Round lot size of this security. |
| share_class_figi | string | 否 | The share Class OpenFIGI number for this ticker. Find more information here |
| share_class_shares_outstanding | number | 否 | The recorded number of outstanding shares for this particular share class. |
| sic_code | string | 否 | The standard industrial classification code for this ticker.  For a list of SIC Codes, see the SEC's SIC Code List. |
| sic_description | string | 否 | A description of this ticker's SIC code. |
| ticker | string | 否 | The exchange symbol that this item is traded under. |
| ticker_root | string | 否 | The root of a specified ticker. For example, the root of BRK.A is BRK. |
| ticker_suffix | string | 否 | The suffix of a specified ticker. For example, the suffix of BRK.A is A. |
| total_employees | number | 否 | The approximate number of employees for the company. |
| type | string | 否 | The type of the asset. Find the types that we support via our Ticker Types API. |
| weighted_shares_outstanding | number | 否 | The shares outstanding calculated assuming all shares of other share classes are converted to this share class. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/v3/reference/tickers/{ticker}
```

### Request

```bash
curl -X GET "https://api.massive.com/v3/reference/tickers/AAPL?apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": "31d59dda-80e5-4721-8496-d0d32a654afe",
  "results": {
    "active": true,
    "address": {
      "address1": "One Apple Park Way",
      "city": "Cupertino",
      "postal_code": "95014",
      "state": "CA"
    },
    "branding": {
      "icon_url": "https://api.massive.com/v1/reference/company-branding/d3d3LmFwcGxlLmNvbQ/images/2022-01-10_icon.png",
      "logo_url": "https://api.massive.com/v1/reference/company-branding/d3d3LmFwcGxlLmNvbQ/images/2022-01-10_logo.svg"
    },
    "cik": "0000320193",
    "composite_figi": "BBG000B9XRY4",
    "currency_name": "usd",
    "description": "Apple designs a wide variety of consumer electronic devices, including smartphones (iPhone), tablets (iPad), PCs (Mac), smartwatches (Apple Watch), AirPods, and TV boxes (Apple TV), among others. The iPhone makes up the majority of Apple's total revenue. In addition, Apple offers its customers a variety of services such as Apple Music, iCloud, Apple Care, Apple TV+, Apple Arcade, Apple Card, and Apple Pay, among others. Apple's products run internally developed software and semiconductors, and the firm is well known for its integration of hardware, software and services. Apple's products are distributed online as well as through company-owned stores and third-party retailers. The company generates roughly 40% of its revenue from the Americas, with the remainder earned internationally.",
    "homepage_url": "https://www.apple.com",
    "list_date": "1980-12-12",
    "locale": "us",
    "market": "stocks",
    "market_cap": 2771126040150,
    "name": "Apple Inc.",
    "phone_number": "(408) 996-1010",
    "primary_exchange": "XNAS",
    "round_lot": 100,
    "share_class_figi": "BBG001S5N8V8",
    "share_class_shares_outstanding": 16406400000,
    "sic_code": "3571",
    "sic_description": "ELECTRONIC COMPUTERS",
    "ticker": "AAPL",
    "ticker_root": "AAPL",
    "total_employees": 154000,
    "type": "CS",
    "weighted_shares_outstanding": 16334371000
  },
  "status": "OK"
}
```
