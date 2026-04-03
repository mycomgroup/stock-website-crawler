---
id: "url-281cfbc7"
type: "api"
title: "Positions Summary API"
url: "https://site.financialmodelingprep.com/developer/docs/form-13-f-asset-allocation-diversification-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T19:42:57.336Z"
metadata:
  markdownContent: "# Positions Summary API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"cik\": \"0000320193\",\n\t\t\"date\": \"2023-09-30\",\n\t\t\"investorsHolding\": 4805,\n\t\t\"lastInvestorsHolding\": 4749,\n\t\t\"investorsHoldingChange\": 56,\n\t\t\"numberOf13Fshares\": 9247670386,\n\t\t\"lastNumberOf13Fshares\": 9345671472,\n\t\t\"numberOf13FsharesChange\": -98001086,\n\t\t\"totalInvested\": 1613733330618,\n\t\t\"lastTotalInvested\": 1825154796061,\n\t\t\"totalInvestedChange\": -211421465443,\n\t\t\"ownershipPercent\": 59.2821,\n\t\t\"lastOwnershipPercent\": 59.5356,\n\t\t\"ownershipPercentChange\": -0.2535,\n\t\t\"newPositions\": 158,\n\t\t\"lastNewPositions\": 188,\n\t\t\"newPositionsChange\": -30,\n\t\t\"increasedPositions\": 1921,\n\t\t\"lastIncreasedPositions\": 1775,\n\t\t\"increasedPositionsChange\": 146,\n\t\t\"closedPositions\": 156,\n\t\t\"lastClosedPositions\": 122,\n\t\t\"closedPositionsChange\": 34,\n\t\t\"reducedPositions\": 2375,\n\t\t\"lastReducedPositions\": 2506,\n\t\t\"reducedPositionsChange\": -131,\n\t\t\"totalCalls\": 173528138,\n\t\t\"lastTotalCalls\": 198746782,\n\t\t\"totalCallsChange\": -25218644,\n\t\t\"totalPuts\": 192878290,\n\t\t\"lastTotalPuts\": 177007062,\n\t\t\"totalPutsChange\": 15871228,\n\t\t\"putCallRatio\": 1.1115,\n\t\t\"lastPutCallRatio\": 0.8906,\n\t\t\"putCallRatioChange\": 22.0894\n\t}\n]\n```\n\n\n## About Positions Summary API\n\nThe Positions Summary API enables users to analyze institutional positions in a particular stock by providing data such as the number of investors holding the stock, the number of shares held, the total amount invested, and changes in these metrics over a given time period. It is ideal for:\n\nTracking Institutional Investment Trends: Monitor how institutional investors are changing their positions in a stock over time.\nOwnership Insights: Understand what percentage of a company is owned by institutional investors and how this changes.\nCall & Put Analysis: Get insights into the put/call ratio and track options activity for institutional positions.\n\nThis API is ideal for understanding institutional activity in the market and gaining insights into the behavior of major investors. It is essential for investors, analysts, and portfolio managers who want to keep a close eye on institutional movements in specific stocks.\nExample Use CaseA hedge fund manager can use the Positions Summary API to track institutional ownership trends in Apple (AAPL), monitoring how many institutions are increasing or reducing their positions, and assessing overall market sentiment.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/symbol-positions-summary?symbol=AAPL&year=2023&quarter=3\n```\n\n- Tracking Institutional Investment Trends: Monitor how institutional investors are changing their positions in a stock over time.\n- Ownership Insights: Understand what percentage of a company is owned by institutional investors and how this changes.\n- Call & Put Analysis: Get insights into the put/call ratio and track options activity for institutional positions.\n\n\n## Related Positions Summary APIs\n\n\n## Positions Summary API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "form-13-f-asset-allocation-diversification-api"
---

# Positions Summary API

## 源URL

https://site.financialmodelingprep.com/developer/docs/form-13-f-asset-allocation-diversification-api

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"cik": "0000320193",
		"date": "2023-09-30",
		"investorsHolding": 4805,
		"lastInvestorsHolding": 4749,
		"investorsHoldingChange": 56,
		"numberOf13Fshares": 9247670386,
		"lastNumberOf13Fshares": 9345671472,
		"numberOf13FsharesChange": -98001086,
		"totalInvested": 1613733330618,
		"lastTotalInvested": 1825154796061,
		"totalInvestedChange": -211421465443,
		"ownershipPercent": 59.2821,
		"lastOwnershipPercent": 59.5356,
		"ownershipPercentChange": -0.2535,
		"newPositions": 158,
		"lastNewPositions": 188,
		"newPositionsChange": -30,
		"increasedPositions": 1921,
		"lastIncreasedPositions": 1775,
		"increasedPositionsChange": 146,
		"closedPositions": 156,
		"lastClosedPositions": 122,
		"closedPositionsChange": 34,
		"reducedPositions": 2375,
		"lastReducedPositions": 2506,
		"reducedPositionsChange": -131,
		"totalCalls": 173528138,
		"lastTotalCalls": 198746782,
		"totalCallsChange": -25218644,
		"totalPuts": 192878290,
		"lastTotalPuts": 177007062,
		"totalPutsChange": 15871228,
		"putCallRatio": 1.1115,
		"lastPutCallRatio": 0.8906,
		"putCallRatioChange": 22.0894
	}
]
```

## About Positions Summary API

The Positions Summary API enables users to analyze institutional positions in a particular stock by providing data such as the number of investors holding the stock, the number of shares held, the total amount invested, and changes in these metrics over a given time period. It is ideal for:

Tracking Institutional Investment Trends: Monitor how institutional investors are changing their positions in a stock over time.
Ownership Insights: Understand what percentage of a company is owned by institutional investors and how this changes.
Call & Put Analysis: Get insights into the put/call ratio and track options activity for institutional positions.

This API is ideal for understanding institutional activity in the market and gaining insights into the behavior of major investors. It is essential for investors, analysts, and portfolio managers who want to keep a close eye on institutional movements in specific stocks.
Example Use CaseA hedge fund manager can use the Positions Summary API to track institutional ownership trends in Apple (AAPL), monitoring how many institutions are increasing or reducing their positions, and assessing overall market sentiment.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/symbol-positions-summary?symbol=AAPL&year=2023&quarter=3
```

- Tracking Institutional Investment Trends: Monitor how institutional investors are changing their positions in a stock over time.
- Ownership Insights: Understand what percentage of a company is owned by institutional investors and how this changes.
- Call & Put Analysis: Get insights into the put/call ratio and track options activity for institutional positions.

## Related Positions Summary APIs

## Positions Summary API FAQs

## Unlock Premium Financial Insights Today!
