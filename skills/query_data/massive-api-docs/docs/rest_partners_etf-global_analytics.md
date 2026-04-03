# ETF Analytics

## 源URL

https://massive.com/docs/rest/partners/etf-global/analytics

## 描述

Retrieve analytical metrics and calculated insights for global ETFs including performance data, risk measures, and derived analytics.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| composite_ticker | string | 否 | The stock ticker symbol used to identify this ETF product on exchanges. |
| processed_date | string | 否 | The date showing when ETF Global received and processed the data. Value must be formatted 'yyyy-mm-dd'. |
| effective_date | string | 否 | The date showing when the information was accurate or valid; some issuers, such as Vanguard, release their data on a delay, so the effective_date can be several weeks earlier than the processed_date. Value must be formatted 'yyyy-mm-dd'. |
| risk_total_score | number | 否 | ETF Global's proprietary Red Diamond overall risk assessment score for the ETF. Value must be a floating point number. |
| reward_score | number | 否 | ETF Global's proprietary Green Diamond score measuring the potential reward and return prospects of the ETF. Value must be a floating point number. |
| quant_total_score | number | 否 | ETF Global's comprehensive quantitative analysis score combining all quantitative factors. Value must be a floating point number. |
| quant_grade | string | 否 | Letter grade summarizing the ETF's overall quantitative assessment, where A = 71-100, B = 56-70, etc. |
| quant_composite_technical | number | 否 | Combined technical analysis score aggregating short, intermediate, and long-term technical factors. Value must be a floating point number. |
| quant_composite_sentiment | number | 否 | Overall market sentiment score combining put/call ratios, short interest, and implied volatility. Value must be a floating point number. |
| quant_composite_behavioral | number | 否 | Behavioral analysis score measuring investor psychology and market behavior patterns. Value must be a floating point number. |
| quant_composite_fundamental | number | 否 | Overall fundamental analysis score combining P/E, P/CF, P/B, and dividend yield metrics. Value must be a floating point number. |
| quant_composite_global | number | 否 | Overall global theme score combining sector and country analysis for macro investment views. Value must be a floating point number. |
| quant_composite_quality | number | 否 | Overall quality assessment score combining liquidity, diversification, and issuing firm factors. Value must be a floating point number. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '5000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'composite_ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| composite_ticker | string | 否 | The stock ticker symbol used to identify this ETF product on exchanges. |
| effective_date | string | 否 | The date showing when the information was accurate or valid; some issuers, such as Vanguard, release their data on a delay, so the effective_date can be several weeks earlier than the processed_date. |
| processed_date | string | 否 | The date showing when ETF Global received and processed the data. |
| quant_composite_behavioral | number | 否 | Behavioral analysis score measuring investor psychology and market behavior patterns. |
| quant_composite_fundamental | number | 否 | Overall fundamental analysis score combining P/E, P/CF, P/B, and dividend yield metrics. |
| quant_composite_global | number | 否 | Overall global theme score combining sector and country analysis for macro investment views. |
| quant_composite_quality | number | 否 | Overall quality assessment score combining liquidity, diversification, and issuing firm factors. |
| quant_composite_sentiment | number | 否 | Overall market sentiment score combining put/call ratios, short interest, and implied volatility. |
| quant_composite_technical | number | 否 | Combined technical analysis score aggregating short, intermediate, and long-term technical factors. |
| quant_fundamental_div | number | 否 | Fundamental analysis score based on dividend yields of the ETF's underlying securities. |
| quant_fundamental_pb | number | 否 | Fundamental analysis score based on price-to-book value ratios of the ETF's holdings. |
| quant_fundamental_pcf | number | 否 | Fundamental analysis score based on price-to-cash-flow ratios of the ETF's underlying assets. |
| quant_fundamental_pe | number | 否 | Fundamental analysis score based on price-to-earnings ratios of the ETF's underlying holdings. |
| quant_global_country | number | 否 | Quantitative score analyzing global country themes and country-specific market factors. |
| quant_global_sector | number | 否 | Quantitative score analyzing global sector themes and sector-specific performance factors. |
| quant_grade | string | 否 | Letter grade summarizing the ETF's overall quantitative assessment, where A = 71-100, B = 56-70, etc. |
| quant_quality_diversification | number | 否 | Quality assessment score evaluating the diversification benefits and risk distribution of the ETF. |
| quant_quality_firm | number | 否 | Quality assessment score evaluating the reputation and capabilities of the ETF's issuing firm. |
| quant_quality_liquidity | number | 否 | Quality assessment score measuring the liquidity characteristics and trading ease of the ETF. |
| quant_sentiment_iv | number | 否 | Market sentiment score derived from implied volatility levels in options markets. |
| quant_sentiment_pc | number | 否 | Market sentiment score derived from put/call option ratios and options activity. |
| quant_sentiment_si | number | 否 | Market sentiment score based on short interest levels and short selling activity. |
| quant_technical_it | number | 否 | Intermediate-term technical analysis score evaluating medium-term price trends. |
| quant_technical_lt | number | 否 | Long-term technical analysis score assessing extended price trend patterns. |
| quant_technical_st | number | 否 | Short-term technical analysis score based on recent price movements and trading patterns. |
| quant_total_score | number | 否 | ETF Global's comprehensive quantitative analysis score combining all quantitative factors. |
| reward_score | number | 否 | ETF Global's proprietary Green Diamond score measuring the potential reward and return prospects of the ETF. |
| risk_country | number | 否 | A component score assessing country-specific risks based on the ETF's geographic exposure. |
| risk_deviation | number | 否 | A component score measuring how much the ETF deviates from expected performance. |
| risk_efficiency | number | 否 | A component score assessing the operational efficiency and cost-effectiveness of the ETF. |
| risk_liquidity | number | 否 | A component score measuring the liquidity risk and ease of trading the ETF. |
| risk_structure | number | 否 | A component score evaluating risks related to the ETF's structural design and mechanics. |
| risk_total_score | number | 否 | ETF Global's proprietary Red Diamond overall risk assessment score for the ETF. |
| risk_volatility | number | 否 | A component score measuring the volatility risk of the ETF's price movements. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/etf-global/v1/analytics
```

### Request

```bash
curl -X GET "https://api.massive.com/etf-global/v1/analytics?limit=100&sort=composite_ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "composite_ticker": "SPY",
      "effective_date": "2025-09-19",
      "processed_date": "2025-09-19",
      "quant_composite_behavioral": 67.1535,
      "quant_composite_fundamental": 1.2,
      "quant_composite_global": 52.9,
      "quant_composite_quality": 75.9,
      "quant_composite_sentiment": 54.6,
      "quant_composite_technical": 79.7,
      "quant_fundamental_div": 4.7,
      "quant_fundamental_pb": 0,
      "quant_fundamental_pcf": 0,
      "quant_fundamental_pe": 0,
      "quant_global_country": 85.4,
      "quant_global_sector": 20.4,
      "quant_grade": "D",
      "quant_quality_diversification": 29.3,
      "quant_quality_firm": 98.3,
      "quant_quality_liquidity": 100,
      "quant_sentiment_iv": 23,
      "quant_sentiment_pc": 88.9,
      "quant_sentiment_si": 51.6,
      "quant_technical_it": 79,
      "quant_technical_lt": 78.7,
      "quant_technical_st": 83.1,
      "quant_total_score": 40.2,
      "reward_score": 3.12,
      "risk_country": 1.46,
      "risk_deviation": 7.68,
      "risk_efficiency": 1.85,
      "risk_liquidity": 2.5,
      "risk_structure": 2.37,
      "risk_total_score": 9.22,
      "risk_volatility": 4.66
    }
  ],
  "status": "OK"
}
```
