---
id: "url-7d2832d9"
type: "api"
title: "COT Report API"
url: "https://site.financialmodelingprep.com/developer/docs/report-by-symbol-commitment-of-traders"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T17:58:14.551Z"
metadata:
  markdownContent: "# COT Report API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"KC\",\n\t\t\"date\": \"2024-02-27 00:00:00\",\n\t\t\"name\": \"Coffee (KC)\",\n\t\t\"sector\": \"SOFTS\",\n\t\t\"marketAndExchangeNames\": \"COFFEE C - ICE FUTURES U.S.\",\n\t\t\"cftcContractMarketCode\": \"083731\",\n\t\t\"cftcMarketCode\": \"ICUS\",\n\t\t\"cftcRegionCode\": \"1\",\n\t\t\"cftcCommodityCode\": \"83\",\n\t\t\"openInterestAll\": 209453,\n\t\t\"noncommPositionsLongAll\": 75330,\n\t\t\"noncommPositionsShortAll\": 23630,\n\t\t\"noncommPositionsSpreadAll\": 47072,\n\t\t\"commPositionsLongAll\": 79690,\n\t\t\"commPositionsShortAll\": 132114,\n\t\t\"totReptPositionsLongAll\": 202092,\n\t\t\"totReptPositionsShortAll\": 202816,\n\t\t\"nonreptPositionsLongAll\": 7361,\n\t\t\"nonreptPositionsShortAll\": 6637,\n\t\t\"openInterestOld\": 179986,\n\t\t\"noncommPositionsLongOld\": 75483,\n\t\t\"noncommPositionsShortOld\": 35395,\n\t\t\"noncommPositionsSpreadOld\": 27067,\n\t\t\"commPositionsLongOld\": 70693,\n\t\t\"commPositionsShortOld\": 111666,\n\t\t\"totReptPositionsLongOld\": 173243,\n\t\t\"totReptPositionsShortOld\": 174128,\n\t\t\"nonreptPositionsLongOld\": 6743,\n\t\t\"nonreptPositionsShortOld\": 5858,\n\t\t\"openInterestOther\": 29467,\n\t\t\"noncommPositionsLongOther\": 18754,\n\t\t\"noncommPositionsShortOther\": 7142,\n\t\t\"noncommPositionsSpreadOther\": 1098,\n\t\t\"commPositionsLongOther\": 8997,\n\t\t\"commPositionsShortOther\": 20448,\n\t\t\"totReptPositionsLongOther\": 28849,\n\t\t\"totReptPositionsShortOther\": 28688,\n\t\t\"nonreptPositionsLongOther\": 618,\n\t\t\"nonreptPositionsShortOther\": 779,\n\t\t\"changeInOpenInterestAll\": 2957,\n\t\t\"changeInNoncommLongAll\": -3545,\n\t\t\"changeInNoncommShortAll\": 618,\n\t\t\"changeInNoncommSpeadAll\": 1575,\n\t\t\"changeInCommLongAll\": 4978,\n\t\t\"changeInCommShortAll\": 802,\n\t\t\"changeInTotReptLongAll\": 3008,\n\t\t\"changeInTotReptShortAll\": 2995,\n\t\t\"changeInNonreptLongAll\": -51,\n\t\t\"changeInNonreptShortAll\": -38,\n\t\t\"pctOfOpenInterestAll\": 100,\n\t\t\"pctOfOiNoncommLongAll\": 36,\n\t\t\"pctOfOiNoncommShortAll\": 11.3,\n\t\t\"pctOfOiNoncommSpreadAll\": 22.5,\n\t\t\"pctOfOiCommLongAll\": 38,\n\t\t\"pctOfOiCommShortAll\": 63.1,\n\t\t\"pctOfOiTotReptLongAll\": 96.5,\n\t\t\"pctOfOiTotReptShortAll\": 96.8,\n\t\t\"pctOfOiNonreptLongAll\": 3.5,\n\t\t\"pctOfOiNonreptShortAll\": 3.2,\n\t\t\"pctOfOpenInterestOl\": 100,\n\t\t\"pctOfOiNoncommLongOl\": 41.9,\n\t\t\"pctOfOiNoncommShortOl\": 19.7,\n\t\t\"pctOfOiNoncommSpreadOl\": 15,\n\t\t\"pctOfOiCommLongOl\": 39.3,\n\t\t\"pctOfOiCommShortOl\": 62,\n\t\t\"pctOfOiTotReptLongOl\": 96.3,\n\t\t\"pctOfOiTotReptShortOl\": 96.7,\n\t\t\"pctOfOiNonreptLongOl\": 3.7,\n\t\t\"pctOfOiNonreptShortOl\": 3.3,\n\t\t\"pctOfOpenInterestOther\": 100,\n\t\t\"pctOfOiNoncommLongOther\": 63.6,\n\t\t\"pctOfOiNoncommShortOther\": 24.2,\n\t\t\"pctOfOiNoncommSpreadOther\": 3.7,\n\t\t\"pctOfOiCommLongOther\": 30.5,\n\t\t\"pctOfOiCommShortOther\": 69.4,\n\t\t\"pctOfOiTotReptLongOther\": 97.9,\n\t\t\"pctOfOiTotReptShortOther\": 97.4,\n\t\t\"pctOfOiNonreptLongOther\": 2.1,\n\t\t\"pctOfOiNonreptShortOther\": 2.6,\n\t\t\"tradersTotAll\": 357,\n\t\t\"tradersNoncommLongAll\": 132,\n\t\t\"tradersNoncommShortAll\": 77,\n\t\t\"tradersNoncommSpreadAll\": 94,\n\t\t\"tradersCommLongAll\": 106,\n\t\t\"tradersCommShortAll\": 119,\n\t\t\"tradersTotReptLongAll\": 286,\n\t\t\"tradersTotReptShortAll\": 250,\n\t\t\"tradersTotOl\": 351,\n\t\t\"tradersNoncommLongOl\": 136,\n\t\t\"tradersNoncommShortOl\": 72,\n\t\t\"tradersNoncommSpeadOl\": 88,\n\t\t\"tradersCommLongOl\": 94,\n\t\t\"tradersCommShortOl\": 114,\n\t\t\"tradersTotReptLongOl\": 269,\n\t\t\"tradersTotReptShortOl\": 239,\n\t\t\"tradersTotOther\": 164,\n\t\t\"tradersNoncommLongOther\": 31,\n\t\t\"tradersNoncommShortOther\": 34,\n\t\t\"tradersNoncommSpreadOther\": 16,\n\t\t\"tradersCommLongOther\": 59,\n\t\t\"tradersCommShortOther\": 68,\n\t\t\"tradersTotReptLongOther\": 102,\n\t\t\"tradersTotReptShortOther\": 106,\n\t\t\"concGrossLe4TdrLongAll\": 16,\n\t\t\"concGrossLe4TdrShortAll\": 23.7,\n\t\t\"concGrossLe8TdrLongAll\": 25.8,\n\t\t\"concGrossLe8TdrShortAll\": 38.9,\n\t\t\"concNetLe4TdrLongAll\": 9.8,\n\t\t\"concNetLe4TdrShortAll\": 16.2,\n\t\t\"concNetLe8TdrLongAll\": 17.7,\n\t\t\"concNetLe8TdrShortAll\": 25.4,\n\t\t\"concGrossLe4TdrLongOl\": 13.6,\n\t\t\"concGrossLe4TdrShortOl\": 24.7,\n\t\t\"concGrossLe8TdrLongOl\": 23.2,\n\t\t\"concGrossLe8TdrShortOl\": 40.3,\n\t\t\"concNetLe4TdrLongOl\": 11.3,\n\t\t\"concNetLe4TdrShortOl\": 18.2,\n\t\t\"concNetLe8TdrLongOl\": 20.3,\n\t\t\"concNetLe8TdrShortOl\": 31.9,\n\t\t\"concGrossLe4TdrLongOther\": 68.2,\n\t\t\"concGrossLe4TdrShortOther\": 29.1,\n\t\t\"concGrossLe8TdrLongOther\": 77.8,\n\t\t\"concGrossLe8TdrShortOther\": 47.3,\n\t\t\"concNetLe4TdrLongOther\": 64.7,\n\t\t\"concNetLe4TdrShortOther\": 26.7,\n\t\t\"concNetLe8TdrLongOther\": 73.9,\n\t\t\"concNetLe8TdrShortOther\": 44.2,\n\t\t\"contractUnits\": \"(CONTRACTS OF 37,500 POUNDS)\"\n\t}\n]\n```\n\n\n## About COT Report API\n\nThe FMP COT Report API is designed for traders, analysts, and market observers to evaluate the positions of market participants. This includes:\n\nMarket Sentiment Tracking: Understand how commercial and non-commercial traders are positioned, giving you insights into the current sentiment of a specific market.\nSector-Wide Analysis: Analyze trader positions across different sectors such as soft commodities, energy, and financials, offering a holistic view of market trends.\nLong and Short Positions: Get detailed data on long, short, and spread positions, helping you make informed decisions on market direction.\n\nThis API is perfect for anyone looking to gain a deeper understanding of market dynamics by observing how various market participants are positioned.\nExample Use CaseA commodity trader can use the COT Report API to analyze the open interest and trader positions in the cocoa market, identifying trends in long and short positions to refine their trading strategy.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/commitment-of-traders-report\n```\n\n- Market Sentiment Tracking: Understand how commercial and non-commercial traders are positioned, giving you insights into the current sentiment of a specific market.\n- Sector-Wide Analysis: Analyze trader positions across different sectors such as soft commodities, energy, and financials, offering a holistic view of market trends.\n- Long and Short Positions: Get detailed data on long, short, and spread positions, helping you make informed decisions on market direction.\n\n\n## Related COT Report APIs\n\n\n## COT Report API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "report-by-symbol-commitment-of-traders"
---

# COT Report API

## 源URL

https://site.financialmodelingprep.com/developer/docs/report-by-symbol-commitment-of-traders

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "KC",
		"date": "2024-02-27 00:00:00",
		"name": "Coffee (KC)",
		"sector": "SOFTS",
		"marketAndExchangeNames": "COFFEE C - ICE FUTURES U.S.",
		"cftcContractMarketCode": "083731",
		"cftcMarketCode": "ICUS",
		"cftcRegionCode": "1",
		"cftcCommodityCode": "83",
		"openInterestAll": 209453,
		"noncommPositionsLongAll": 75330,
		"noncommPositionsShortAll": 23630,
		"noncommPositionsSpreadAll": 47072,
		"commPositionsLongAll": 79690,
		"commPositionsShortAll": 132114,
		"totReptPositionsLongAll": 202092,
		"totReptPositionsShortAll": 202816,
		"nonreptPositionsLongAll": 7361,
		"nonreptPositionsShortAll": 6637,
		"openInterestOld": 179986,
		"noncommPositionsLongOld": 75483,
		"noncommPositionsShortOld": 35395,
		"noncommPositionsSpreadOld": 27067,
		"commPositionsLongOld": 70693,
		"commPositionsShortOld": 111666,
		"totReptPositionsLongOld": 173243,
		"totReptPositionsShortOld": 174128,
		"nonreptPositionsLongOld": 6743,
		"nonreptPositionsShortOld": 5858,
		"openInterestOther": 29467,
		"noncommPositionsLongOther": 18754,
		"noncommPositionsShortOther": 7142,
		"noncommPositionsSpreadOther": 1098,
		"commPositionsLongOther": 8997,
		"commPositionsShortOther": 20448,
		"totReptPositionsLongOther": 28849,
		"totReptPositionsShortOther": 28688,
		"nonreptPositionsLongOther": 618,
		"nonreptPositionsShortOther": 779,
		"changeInOpenInterestAll": 2957,
		"changeInNoncommLongAll": -3545,
		"changeInNoncommShortAll": 618,
		"changeInNoncommSpeadAll": 1575,
		"changeInCommLongAll": 4978,
		"changeInCommShortAll": 802,
		"changeInTotReptLongAll": 3008,
		"changeInTotReptShortAll": 2995,
		"changeInNonreptLongAll": -51,
		"changeInNonreptShortAll": -38,
		"pctOfOpenInterestAll": 100,
		"pctOfOiNoncommLongAll": 36,
		"pctOfOiNoncommShortAll": 11.3,
		"pctOfOiNoncommSpreadAll": 22.5,
		"pctOfOiCommLongAll": 38,
		"pctOfOiCommShortAll": 63.1,
		"pctOfOiTotReptLongAll": 96.5,
		"pctOfOiTotReptShortAll": 96.8,
		"pctOfOiNonreptLongAll": 3.5,
		"pctOfOiNonreptShortAll": 3.2,
		"pctOfOpenInterestOl": 100,
		"pctOfOiNoncommLongOl": 41.9,
		"pctOfOiNoncommShortOl": 19.7,
		"pctOfOiNoncommSpreadOl": 15,
		"pctOfOiCommLongOl": 39.3,
		"pctOfOiCommShortOl": 62,
		"pctOfOiTotReptLongOl": 96.3,
		"pctOfOiTotReptShortOl": 96.7,
		"pctOfOiNonreptLongOl": 3.7,
		"pctOfOiNonreptShortOl": 3.3,
		"pctOfOpenInterestOther": 100,
		"pctOfOiNoncommLongOther": 63.6,
		"pctOfOiNoncommShortOther": 24.2,
		"pctOfOiNoncommSpreadOther": 3.7,
		"pctOfOiCommLongOther": 30.5,
		"pctOfOiCommShortOther": 69.4,
		"pctOfOiTotReptLongOther": 97.9,
		"pctOfOiTotReptShortOther": 97.4,
		"pctOfOiNonreptLongOther": 2.1,
		"pctOfOiNonreptShortOther": 2.6,
		"tradersTotAll": 357,
		"tradersNoncommLongAll": 132,
		"tradersNoncommShortAll": 77,
		"tradersNoncommSpreadAll": 94,
		"tradersCommLongAll": 106,
		"tradersCommShortAll": 119,
		"tradersTotReptLongAll": 286,
		"tradersTotReptShortAll": 250,
		"tradersTotOl": 351,
		"tradersNoncommLongOl": 136,
		"tradersNoncommShortOl": 72,
		"tradersNoncommSpeadOl": 88,
		"tradersCommLongOl": 94,
		"tradersCommShortOl": 114,
		"tradersTotReptLongOl": 269,
		"tradersTotReptShortOl": 239,
		"tradersTotOther": 164,
		"tradersNoncommLongOther": 31,
		"tradersNoncommShortOther": 34,
		"tradersNoncommSpreadOther": 16,
		"tradersCommLongOther": 59,
		"tradersCommShortOther": 68,
		"tradersTotReptLongOther": 102,
		"tradersTotReptShortOther": 106,
		"concGrossLe4TdrLongAll": 16,
		"concGrossLe4TdrShortAll": 23.7,
		"concGrossLe8TdrLongAll": 25.8,
		"concGrossLe8TdrShortAll": 38.9,
		"concNetLe4TdrLongAll": 9.8,
		"concNetLe4TdrShortAll": 16.2,
		"concNetLe8TdrLongAll": 17.7,
		"concNetLe8TdrShortAll": 25.4,
		"concGrossLe4TdrLongOl": 13.6,
		"concGrossLe4TdrShortOl": 24.7,
		"concGrossLe8TdrLongOl": 23.2,
		"concGrossLe8TdrShortOl": 40.3,
		"concNetLe4TdrLongOl": 11.3,
		"concNetLe4TdrShortOl": 18.2,
		"concNetLe8TdrLongOl": 20.3,
		"concNetLe8TdrShortOl": 31.9,
		"concGrossLe4TdrLongOther": 68.2,
		"concGrossLe4TdrShortOther": 29.1,
		"concGrossLe8TdrLongOther": 77.8,
		"concGrossLe8TdrShortOther": 47.3,
		"concNetLe4TdrLongOther": 64.7,
		"concNetLe4TdrShortOther": 26.7,
		"concNetLe8TdrLongOther": 73.9,
		"concNetLe8TdrShortOther": 44.2,
		"contractUnits": "(CONTRACTS OF 37,500 POUNDS)"
	}
]
```

## About COT Report API

The FMP COT Report API is designed for traders, analysts, and market observers to evaluate the positions of market participants. This includes:

Market Sentiment Tracking: Understand how commercial and non-commercial traders are positioned, giving you insights into the current sentiment of a specific market.
Sector-Wide Analysis: Analyze trader positions across different sectors such as soft commodities, energy, and financials, offering a holistic view of market trends.
Long and Short Positions: Get detailed data on long, short, and spread positions, helping you make informed decisions on market direction.

This API is perfect for anyone looking to gain a deeper understanding of market dynamics by observing how various market participants are positioned.
Example Use CaseA commodity trader can use the COT Report API to analyze the open interest and trader positions in the cocoa market, identifying trends in long and short positions to refine their trading strategy.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/commitment-of-traders-report
```

- Market Sentiment Tracking: Understand how commercial and non-commercial traders are positioned, giving you insights into the current sentiment of a specific market.
- Sector-Wide Analysis: Analyze trader positions across different sectors such as soft commodities, energy, and financials, offering a holistic view of market trends.
- Long and Short Positions: Get detailed data on long, short, and spread positions, helping you make informed decisions on market direction.

## Related COT Report APIs

## COT Report API FAQs

## Unlock Premium Financial Insights Today!
