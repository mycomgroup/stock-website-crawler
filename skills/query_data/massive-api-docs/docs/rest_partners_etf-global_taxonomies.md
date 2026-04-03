# ETF Taxonomies

## 源URL

https://massive.com/docs/rest/partners/etf-global/taxonomies

## 描述

Access standardized taxonomy systems used to categorize and organize global ETFs. Get structured classification frameworks that help define investment strategies, asset types, and fund characteristics.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| processed_date | string | 否 | The date showing when ETF Global received and processed the data. Value must be formatted 'yyyy-mm-dd'. |
| effective_date | string | 否 | The date showing when the information was accurate or valid; some issuers, such as Vanguard, release their data on a delay, so the effective_date can be several weeks earlier than the processed_date. Value must be formatted 'yyyy-mm-dd'. |
| composite_ticker | string | 否 | The stock ticker symbol used to identify this ETF product on exchanges. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '5000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'composite_ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| asset_class | string | 否 | The primary type of assets held by the ETF, such as equities, bonds, commodities, or other securities. |
| category | string | 否 | The broad investment category that describes the ETF's investment focus and strategy. |
| composite_ticker | string | 否 | The stock ticker symbol used to identify this ETF product on exchanges. |
| country | string | 否 | The specific country focus of the ETF, if applicable. |
| credit_quality_rating | string | 否 | Credit quality rating for fixed income ETFs. |
| description | string | 否 | The official name and description of the ETF product. |
| development_class | string | 否 | The economic development classification of the markets the ETF invests in, such as developed, emerging, or frontier markets. |
| duration | string | 否 | The duration characteristics for fixed income ETFs. |
| effective_date | string | 否 | The date showing when the information was accurate or valid; some issuers, such as Vanguard, release their data on a delay, so the effective_date can be several weeks earlier than the processed_date. |
| esg | string | 否 | Environmental, Social, and Governance characteristics. |
| exposure_mechanism | string | 否 | The mechanism used to achieve exposure. |
| factor | string | 否 | Factor exposure characteristics of the ETF. |
| focus | string | 否 | The specific investment focus or exposure that the ETF provides, such as sector, geography, or investment style. |
| hedge_reset | string | 否 | The frequency of hedge reset, if applicable. |
| holdings_disclosure_frequency | string | 否 | How frequently holdings are disclosed. |
| inception_date | string | 否 | The date when this ETF was first launched and became available for trading. |
| isin | string | 否 | The International Securities Identification Number, a global standard code for uniquely identifying this ETF worldwide. |
| issuer | string | 否 | The financial institution or fund company that created and sponsors this ETF. |
| leverage_reset | string | 否 | The frequency of leverage reset, if applicable. |
| leverage_style | string | 否 | Indicates whether the ETF uses leverage to amplify returns ('leveraged'), or does not use leverage ('unleveraged'). |
| levered_amount | number | 否 | The leverage multiplier applied by the ETF, where positive numbers indicate leveraged exposure and negative numbers indicate inverse exposure. |
| management_classification | string | 否 | Defines whether an ETF is considered active under SEC rules, with managers making investment decisions, or passive, tracking an index. |
| management_style | string | 否 | Indicates whether an ETF is managed actively or passively, and the level of transparency or replication method used. |
| maturity | string | 否 | The maturity profile for fixed income ETFs. |
| objective | string | 否 | The primary investment objective of the ETF. |
| primary_benchmark | string | 否 | The main index or benchmark that this ETF is designed to track or replicate. |
| processed_date | string | 否 | The date showing when ETF Global received and processed the data. |
| product_type | string | 否 | Indicates whether the product is an Exchange-Traded Note ('etn') or an Exchange-Traded Fund ('etf'). |
| rebalance_frequency | string | 否 | How frequently the ETF rebalances its holdings. |
| reconstitution_frequency | string | 否 | How frequently the index is reconstituted. |
| region | string | 否 | The geographic region or area of the world where the ETF concentrates its investments. |
| secondary_objective | string | 否 | The secondary investment objective, if applicable. |
| selection_methodology | string | 否 | The methodology used to select securities. |
| selection_universe | string | 否 | The universe from which securities are selected. |
| strategic_focus | string | 否 | The strategic investment focus of the ETF. |
| targeted_focus | string | 否 | The targeted investment focus of the ETF. |
| tax_classification | string | 否 | The tax structure of the ETF, determining whether investors receive 1099 or K1 tax forms (RIC, Partnership, or UIT). |
| us_code | string | 否 | A unique identifier code that identifies this ETF in US markets. |
| weighting_methodology | string | 否 | The methodology used to weight holdings. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/etf-global/v1/taxonomies
```

### Request

```bash
curl -X GET "https://api.massive.com/etf-global/v1/taxonomies?limit=100&sort=composite_ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "asset_class": "Equity",
      "category": "Size and Style",
      "composite_ticker": "SPY",
      "country": "U.S.",
      "description": "SPDR S&P 500 ETF Trust",
      "development_class": "Developed Markets",
      "effective_date": "2025-09-19",
      "exposure_mechanism": "Blended Replication",
      "factor": "Size",
      "focus": "Large Cap",
      "holdings_disclosure_frequency": "Daily",
      "inception_date": "1993-01-22",
      "isin": "US78462F1030",
      "issuer": "SSgA",
      "leverage_style": "unleveraged",
      "levered_amount": 0,
      "management_classification": "passive",
      "management_style": "Passive - Representative Sampling",
      "objective": "Index-Tracking",
      "primary_benchmark": "S&P 500 Index",
      "processed_date": "2025-09-19",
      "product_type": "etf",
      "rebalance_frequency": "Quarterly",
      "reconstitution_frequency": "Quarterly",
      "region": "North America",
      "selection_methodology": "Modified Market Cap, Fundamental Multifactor, Liquidity",
      "selection_universe": "U.S. Large Caps",
      "strategic_focus": "Factor",
      "targeted_focus": "Size",
      "tax_classification": "Regulated Investment Company",
      "us_code": "78462F103",
      "weighting_methodology": "Modified Market Capitalization-Weighted"
    }
  ],
  "status": "OK"
}
```
