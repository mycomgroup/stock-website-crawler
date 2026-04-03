---
id: "url-150a7c6"
type: "api"
title: "Custom DCF Advanced API"
url: "https://site.financialmodelingprep.com/developer/docs/stable/custom-dcf-advanced"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T10:27:53.147Z"
metadata:
  markdownContent: "# Custom DCF Advanced API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"year\": \"2029\",\n\t\t\"symbol\": \"AAPL\",\n\t\t\"revenue\": 657173266965,\n\t\t\"revenuePercentage\": 10.94,\n\t\t\"ebitda\": 205521399637,\n\t\t\"ebitdaPercentage\": 31.27,\n\t\t\"ebit\": 182813984515,\n\t\t\"ebitPercentage\": 27.82,\n\t\t\"depreciation\": 22707415125,\n\t\t\"depreciationPercentage\": 3.46,\n\t\t\"totalCash\": 154056011356,\n\t\t\"totalCashPercentage\": 23.44,\n\t\t\"receivables\": 100795299078,\n\t\t\"receivablesPercentage\": 15.34,\n\t\t\"inventories\": 10202330691,\n\t\t\"inventoriesPercentage\": 1.55,\n\t\t\"payable\": 106124867281,\n\t\t\"payablePercentage\": 16.15,\n\t\t\"capitalExpenditure\": 20111200574,\n\t\t\"capitalExpenditurePercentage\": 3.06,\n\t\t\"price\": 232.8,\n\t\t\"beta\": 1.244,\n\t\t\"dilutedSharesOutstanding\": 15408095000,\n\t\t\"costofDebt\": 3.64,\n\t\t\"taxRate\": 24.09,\n\t\t\"afterTaxCostOfDebt\": 2.76,\n\t\t\"riskFreeRate\": 3.64,\n\t\t\"marketRiskPremium\": 4.72,\n\t\t\"costOfEquity\": 9.51,\n\t\t\"totalDebt\": 106629000000,\n\t\t\"totalEquity\": 3587004516000,\n\t\t\"totalCapital\": 3693633516000,\n\t\t\"debtWeighting\": 2.89,\n\t\t\"equityWeighting\": 97.11,\n\t\t\"wacc\": 9.33,\n\t\t\"taxRateCash\": 14919580,\n\t\t\"ebiat\": 155538906468,\n\t\t\"ufcf\": 197876962552,\n\t\t\"sumPvUfcf\": 616840860880,\n\t\t\"longTermGrowthRate\": 4,\n\t\t\"terminalValue\": 3863553224578,\n\t\t\"presentTerminalValue\": 2473772391290,\n\t\t\"enterpriseValue\": 3090613252170,\n\t\t\"netDebt\": 76686000000,\n\t\t\"equityValue\": 3013927252170,\n\t\t\"equityValuePerShare\": 195.61,\n\t\t\"freeCashFlowT1\": 205792041054\n\t}\n]\n```\n\n\n## About Custom DCF Advanced API\n\nThe Custom DCF Advanced API is designed for financial analysts and investors who want to customize their DCF analysis based on their specific forecasts and assumptions. This API gives users the flexibility to modify key variables such as revenue growth, EBITDA, capital expenditures, and risk factors to achieve a tailored company valuation. Key features include:\n\nCustomizable Inputs: Adjust core financial metrics such as revenue, EBITDA, and capital expenditures to fit your projections and forecasts.\nAdvanced Financial Assumptions: Modify factors like the risk-free rate, market risk premium, tax rate, and WACC to create a more accurate valuation.\nComprehensive Output: Get detailed results including equity value, free cash flow, terminal value, and equity value per share, all based on your custom inputs.\n\nThis API is ideal for professional analysts or advanced users looking to customize DCF models to reflect their investment strategy or valuation assumptions.\nExample Use CaseAn equity analyst might use the Custom DCF Advanced API to adjust Apple’s financial forecasts, input a different market risk premium, or modify the long-term growth rate. These tailored inputs allow the analyst to create a unique valuation model for the company and make more informed investment decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/custom-discounted-cash-flow?symbol=AAPL\n```\n\n- Customizable Inputs: Adjust core financial metrics such as revenue, EBITDA, and capital expenditures to fit your projections and forecasts.\n- Advanced Financial Assumptions: Modify factors like the risk-free rate, market risk premium, tax rate, and WACC to create a more accurate valuation.\n- Comprehensive Output: Get detailed results including equity value, free cash flow, terminal value, and equity value per share, all based on your custom inputs.\n\n\n## Related Custom DCF Advanced APIs\n\n\n## Custom DCF Advanced API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "stable_custom-dcf-advanced"
---

# Custom DCF Advanced API

## 源URL

https://site.financialmodelingprep.com/developer/docs/stable/custom-dcf-advanced

## 文档正文

**Response Example:**

```json
[
	{
		"year": "2029",
		"symbol": "AAPL",
		"revenue": 657173266965,
		"revenuePercentage": 10.94,
		"ebitda": 205521399637,
		"ebitdaPercentage": 31.27,
		"ebit": 182813984515,
		"ebitPercentage": 27.82,
		"depreciation": 22707415125,
		"depreciationPercentage": 3.46,
		"totalCash": 154056011356,
		"totalCashPercentage": 23.44,
		"receivables": 100795299078,
		"receivablesPercentage": 15.34,
		"inventories": 10202330691,
		"inventoriesPercentage": 1.55,
		"payable": 106124867281,
		"payablePercentage": 16.15,
		"capitalExpenditure": 20111200574,
		"capitalExpenditurePercentage": 3.06,
		"price": 232.8,
		"beta": 1.244,
		"dilutedSharesOutstanding": 15408095000,
		"costofDebt": 3.64,
		"taxRate": 24.09,
		"afterTaxCostOfDebt": 2.76,
		"riskFreeRate": 3.64,
		"marketRiskPremium": 4.72,
		"costOfEquity": 9.51,
		"totalDebt": 106629000000,
		"totalEquity": 3587004516000,
		"totalCapital": 3693633516000,
		"debtWeighting": 2.89,
		"equityWeighting": 97.11,
		"wacc": 9.33,
		"taxRateCash": 14919580,
		"ebiat": 155538906468,
		"ufcf": 197876962552,
		"sumPvUfcf": 616840860880,
		"longTermGrowthRate": 4,
		"terminalValue": 3863553224578,
		"presentTerminalValue": 2473772391290,
		"enterpriseValue": 3090613252170,
		"netDebt": 76686000000,
		"equityValue": 3013927252170,
		"equityValuePerShare": 195.61,
		"freeCashFlowT1": 205792041054
	}
]
```

## About Custom DCF Advanced API

The Custom DCF Advanced API is designed for financial analysts and investors who want to customize their DCF analysis based on their specific forecasts and assumptions. This API gives users the flexibility to modify key variables such as revenue growth, EBITDA, capital expenditures, and risk factors to achieve a tailored company valuation. Key features include:

Customizable Inputs: Adjust core financial metrics such as revenue, EBITDA, and capital expenditures to fit your projections and forecasts.
Advanced Financial Assumptions: Modify factors like the risk-free rate, market risk premium, tax rate, and WACC to create a more accurate valuation.
Comprehensive Output: Get detailed results including equity value, free cash flow, terminal value, and equity value per share, all based on your custom inputs.

This API is ideal for professional analysts or advanced users looking to customize DCF models to reflect their investment strategy or valuation assumptions.
Example Use CaseAn equity analyst might use the Custom DCF Advanced API to adjust Apple’s financial forecasts, input a different market risk premium, or modify the long-term growth rate. These tailored inputs allow the analyst to create a unique valuation model for the company and make more informed investment decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/custom-discounted-cash-flow?symbol=AAPL
```

- Customizable Inputs: Adjust core financial metrics such as revenue, EBITDA, and capital expenditures to fit your projections and forecasts.
- Advanced Financial Assumptions: Modify factors like the risk-free rate, market risk premium, tax rate, and WACC to create a more accurate valuation.
- Comprehensive Output: Get detailed results including equity value, free cash flow, terminal value, and equity value per share, all based on your custom inputs.

## Related Custom DCF Advanced APIs

## Custom DCF Advanced API FAQs

## Unlock Premium Financial Insights Today!
