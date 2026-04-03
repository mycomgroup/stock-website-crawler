---
id: "url-2975c922"
type: "api"
title: "As Reported Balance Statements API"
url: "https://site.financialmodelingprep.com/developer/docs/stable/as-reported-balance-statements"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T16:30:25.334Z"
metadata:
  markdownContent: "# As Reported Balance Statements API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"fiscalYear\": 2024,\n\t\t\"period\": \"FY\",\n\t\t\"reportedCurrency\": null,\n\t\t\"date\": \"2024-09-27\",\n\t\t\"data\": {\n\t\t\t\"cashandcashequivalentsatcarryingvalue\": 29943000000,\n\t\t\t\"marketablesecuritiescurrent\": 35228000000,\n\t\t\t\"accountsreceivablenetcurrent\": 33410000000,\n\t\t\t\"nontradereceivablescurrent\": 32833000000,\n\t\t\t\"inventorynet\": 7286000000,\n\t\t\t\"otherassetscurrent\": 14287000000,\n\t\t\t\"assetscurrent\": 152987000000,\n\t\t\t\"marketablesecuritiesnoncurrent\": 91479000000,\n\t\t\t\"propertyplantandequipmentnet\": 45680000000,\n\t\t\t\"otherassetsnoncurrent\": 74834000000,\n\t\t\t\"assetsnoncurrent\": 211993000000,\n\t\t\t\"assets\": 364980000000,\n\t\t\t\"accountspayablecurrent\": 68960000000,\n\t\t\t\"otherliabilitiescurrent\": 78304000000,\n\t\t\t\"contractwithcustomerliabilitycurrent\": 8249000000,\n\t\t\t\"commercialpaper\": 10000000000,\n\t\t\t\"longtermdebtcurrent\": 10912000000,\n\t\t\t\"liabilitiescurrent\": 176392000000,\n\t\t\t\"longtermdebtnoncurrent\": 85750000000,\n\t\t\t\"otherliabilitiesnoncurrent\": 45888000000,\n\t\t\t\"liabilitiesnoncurrent\": 131638000000,\n\t\t\t\"liabilities\": 308030000000,\n\t\t\t\"commonstocksharesoutstanding\": 15116786000,\n\t\t\t\"commonstocksharesissued\": 15116786000,\n\t\t\t\"commonstocksincludingadditionalpaidincapital\": 83276000000,\n\t\t\t\"retainedearningsaccumulateddeficit\": -19154000000,\n\t\t\t\"accumulatedothercomprehensiveincomelossnetoftax\": -7172000000,\n\t\t\t\"stockholdersequity\": 56950000000,\n\t\t\t\"liabilitiesandstockholdersequity\": 364980000000,\n\t\t\t\"commonstockparorstatedvaluepershare\": 0.00001,\n\t\t\t\"commonstocksharesauthorized\": 50400000000\n\t\t}\n\t}\n]\n```\n\n\n## About As Reported Balance Statements API\n\nThe As Reported Balance Statements API offers unadjusted balance sheet data as reported by companies. It provides insight into a company's financial position, including:\n\nAsset Overview: View cash, receivables, inventory, and long-term assets as reported.\nLiability Breakdown: Access current and non-current liabilities, deferred revenues, and more.\nEquity Insights: Examine stockholders’ equity, including retained earnings and stock details.\n\nThis API is ideal for analysts and investors who want raw, as-reported balance sheet data to perform accurate financial assessments.\nExample Use CaseAn investment analyst can use the As Reported Balance Statements API to evaluate Apple's asset-liability structure for Q1 2010, helping to understand the company's financial position during that period without any adjustments.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/balance-sheet-statement-as-reported?symbol=AAPL\n```\n\n- Asset Overview: View cash, receivables, inventory, and long-term assets as reported.\n- Liability Breakdown: Access current and non-current liabilities, deferred revenues, and more.\n- Equity Insights: Examine stockholders’ equity, including retained earnings and stock details.\n\n\n## Related As Reported Balance Statements APIs\n\n\n## As Reported Balance Statements API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "stable_as-reported-balance-statements"
---

# As Reported Balance Statements API

## 源URL

https://site.financialmodelingprep.com/developer/docs/stable/as-reported-balance-statements

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"fiscalYear": 2024,
		"period": "FY",
		"reportedCurrency": null,
		"date": "2024-09-27",
		"data": {
			"cashandcashequivalentsatcarryingvalue": 29943000000,
			"marketablesecuritiescurrent": 35228000000,
			"accountsreceivablenetcurrent": 33410000000,
			"nontradereceivablescurrent": 32833000000,
			"inventorynet": 7286000000,
			"otherassetscurrent": 14287000000,
			"assetscurrent": 152987000000,
			"marketablesecuritiesnoncurrent": 91479000000,
			"propertyplantandequipmentnet": 45680000000,
			"otherassetsnoncurrent": 74834000000,
			"assetsnoncurrent": 211993000000,
			"assets": 364980000000,
			"accountspayablecurrent": 68960000000,
			"otherliabilitiescurrent": 78304000000,
			"contractwithcustomerliabilitycurrent": 8249000000,
			"commercialpaper": 10000000000,
			"longtermdebtcurrent": 10912000000,
			"liabilitiescurrent": 176392000000,
			"longtermdebtnoncurrent": 85750000000,
			"otherliabilitiesnoncurrent": 45888000000,
			"liabilitiesnoncurrent": 131638000000,
			"liabilities": 308030000000,
			"commonstocksharesoutstanding": 15116786000,
			"commonstocksharesissued": 15116786000,
			"commonstocksincludingadditionalpaidincapital": 83276000000,
			"retainedearningsaccumulateddeficit": -19154000000,
			"accumulatedothercomprehensiveincomelossnetoftax": -7172000000,
			"stockholdersequity": 56950000000,
			"liabilitiesandstockholdersequity": 364980000000,
			"commonstockparorstatedvaluepershare": 0.00001,
			"commonstocksharesauthorized": 50400000000
		}
	}
]
```

## About As Reported Balance Statements API

The As Reported Balance Statements API offers unadjusted balance sheet data as reported by companies. It provides insight into a company's financial position, including:

Asset Overview: View cash, receivables, inventory, and long-term assets as reported.
Liability Breakdown: Access current and non-current liabilities, deferred revenues, and more.
Equity Insights: Examine stockholders’ equity, including retained earnings and stock details.

This API is ideal for analysts and investors who want raw, as-reported balance sheet data to perform accurate financial assessments.
Example Use CaseAn investment analyst can use the As Reported Balance Statements API to evaluate Apple's asset-liability structure for Q1 2010, helping to understand the company's financial position during that period without any adjustments.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/balance-sheet-statement-as-reported?symbol=AAPL
```

- Asset Overview: View cash, receivables, inventory, and long-term assets as reported.
- Liability Breakdown: Access current and non-current liabilities, deferred revenues, and more.
- Equity Insights: Examine stockholders’ equity, including retained earnings and stock details.

## Related As Reported Balance Statements APIs

## As Reported Balance Statements API FAQs

## Unlock Premium Financial Insights Today!
