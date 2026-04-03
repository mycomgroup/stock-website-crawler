---
id: "url-7a24c05c"
type: "api"
title: "Financial Ratios API"
url: "https://site.financialmodelingprep.com/developer/docs/stable/metrics-ratios"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T07:54:16.180Z"
metadata:
  markdownContent: "# Financial Ratios API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"date\": \"2024-09-28\",\n\t\t\"fiscalYear\": \"2024\",\n\t\t\"period\": \"FY\",\n\t\t\"reportedCurrency\": \"USD\",\n\t\t\"grossProfitMargin\": 0.4620634981523393,\n\t\t\"ebitMargin\": 0.31510222870075566,\n\t\t\"ebitdaMargin\": 0.3443707085043538,\n\t\t\"operatingProfitMargin\": 0.31510222870075566,\n\t\t\"pretaxProfitMargin\": 0.3157901466620635,\n\t\t\"continuousOperationsProfitMargin\": 0.23971255769943867,\n\t\t\"netProfitMargin\": 0.23971255769943867,\n\t\t\"bottomLineProfitMargin\": 0.23971255769943867,\n\t\t\"receivablesTurnover\": 5.903038811648023,\n\t\t\"payablesTurnover\": 3.0503480278422272,\n\t\t\"inventoryTurnover\": 28.870710952511665,\n\t\t\"fixedAssetTurnover\": 8.560310858143607,\n\t\t\"assetTurnover\": 1.0713874732862074,\n\t\t\"currentRatio\": 0.8673125765340832,\n\t\t\"quickRatio\": 0.8260068483831466,\n\t\t\"solvencyRatio\": 0.3414634938155374,\n\t\t\"cashRatio\": 0.16975259648963673,\n\t\t\"priceToEarningsRatio\": 37.287278415656736,\n\t\t\"priceToEarningsGrowthRatio\": -45.93792700808932,\n\t\t\"forwardPriceToEarningsGrowthRatio\": -45.93792700808932,\n\t\t\"priceToBookRatio\": 61.37243774486391,\n\t\t\"priceToSalesRatio\": 8.93822887866815,\n\t\t\"priceToFreeCashFlowRatio\": 32.12256867269569,\n\t\t\"priceToOperatingCashFlowRatio\": 29.55638142954995,\n\t\t\"debtToAssetsRatio\": 0.29215025480848267,\n\t\t\"debtToEquityRatio\": 1.872326602282704,\n\t\t\"debtToCapitalRatio\": 0.6518501763673821,\n\t\t\"longTermDebtToCapitalRatio\": 0.6009110021023125,\n\t\t\"financialLeverageRatio\": 6.408779631255487,\n\t\t\"workingCapitalTurnoverRatio\": -31.099932397502684,\n\t\t\"operatingCashFlowRatio\": 0.6704045534944896,\n\t\t\"operatingCashFlowSalesRatio\": 0.3024128274962599,\n\t\t\"freeCashFlowOperatingCashFlowRatio\": 0.9201126388959359,\n\t\t\"debtServiceCoverageRatio\": 5.024761722304708,\n\t\t\"interestCoverageRatio\": 0,\n\t\t\"shortTermOperatingCashFlowCoverageRatio\": 5.663777000814215,\n\t\t\"operatingCashFlowCoverageRatio\": 1.109022873702276,\n\t\t\"capitalExpenditureCoverageRatio\": 12.517624642743728,\n\t\t\"dividendPaidAndCapexCoverageRatio\": 4.7912969490701345,\n\t\t\"dividendPayoutRatio\": 0.16252026969360758,\n\t\t\"dividendYield\": 0.0043585983369965175,\n\t\t\"dividendYieldPercentage\": 0.43585983369965176,\n\t\t\"revenuePerShare\": 25.484914639368924,\n\t\t\"netIncomePerShare\": 6.109054070954992,\n\t\t\"interestDebtPerShare\": 6.949329249507765,\n\t\t\"cashPerShare\": 4.247388013764271,\n\t\t\"bookValuePerShare\": 3.711600978715614,\n\t\t\"tangibleBookValuePerShare\": 3.711600978715614,\n\t\t\"shareholdersEquityPerShare\": 3.711600978715614,\n\t\t\"operatingCashFlowPerShare\": 7.706965094592383,\n\t\t\"capexPerShare\": 0.6156891035281195,\n\t\t\"freeCashFlowPerShare\": 7.091275991064264,\n\t\t\"netIncomePerEBT\": 0.7590881483581001,\n\t\t\"ebtPerEbit\": 1.0021831580314244,\n\t\t\"priceToFairValue\": 61.37243774486391,\n\t\t\"debtToMarketCap\": 0.03050761336980449,\n\t\t\"effectiveTaxRate\": 0.24091185164189982,\n\t\t\"enterpriseValueMultiple\": 26.524727497716487\n\t}\n]\n```\n\n\n## About Financial Ratios API\n\nThe Financial Ratios API delivers key ratios that help investors, analysts, and researchers evaluate a company's performance. These ratios include profitability indicators like gross profit margin and net profit margin, liquidity metrics such as current ratio and quick ratio, and efficiency measurements like asset turnover and inventory turnover. This API offers a comprehensive view of a company's financial health and operational efficiency.\n\nProfitability Ratios: Gain insight into a company's ability to generate profit, with metrics like net profit margin and return on equity.\nLiquidity Ratios: Understand how well a company can meet its short-term obligations using ratios like current ratio and quick ratio.\nEfficiency Ratios: Assess how effectively a company utilizes its assets with metrics such as asset turnover and inventory turnover.\nDebt Ratios: Evaluate a company's leverage and debt management through ratios like debt-to-equity and interest coverage ratios.\n\nThis API is an essential tool for investors and analysts looking to analyze financial ratios and make informed decisions based on a company's financial performance.\nExample Use CaseA portfolio manager can use the Financial Ratios API to compare liquidity ratios between companies in the same industry, helping them identify firms with stronger financial stability and more efficient operations.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ratios?symbol=AAPL\n```\n\n- Profitability Ratios: Gain insight into a company's ability to generate profit, with metrics like net profit margin and return on equity.\n- Liquidity Ratios: Understand how well a company can meet its short-term obligations using ratios like current ratio and quick ratio.\n- Efficiency Ratios: Assess how effectively a company utilizes its assets with metrics such as asset turnover and inventory turnover.\n- Debt Ratios: Evaluate a company's leverage and debt management through ratios like debt-to-equity and interest coverage ratios.\n\n\n## Related Financial Ratios APIs\n\n\n## Financial Ratios API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "stable_metrics-ratios"
---

# Financial Ratios API

## 源URL

https://site.financialmodelingprep.com/developer/docs/stable/metrics-ratios

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"date": "2024-09-28",
		"fiscalYear": "2024",
		"period": "FY",
		"reportedCurrency": "USD",
		"grossProfitMargin": 0.4620634981523393,
		"ebitMargin": 0.31510222870075566,
		"ebitdaMargin": 0.3443707085043538,
		"operatingProfitMargin": 0.31510222870075566,
		"pretaxProfitMargin": 0.3157901466620635,
		"continuousOperationsProfitMargin": 0.23971255769943867,
		"netProfitMargin": 0.23971255769943867,
		"bottomLineProfitMargin": 0.23971255769943867,
		"receivablesTurnover": 5.903038811648023,
		"payablesTurnover": 3.0503480278422272,
		"inventoryTurnover": 28.870710952511665,
		"fixedAssetTurnover": 8.560310858143607,
		"assetTurnover": 1.0713874732862074,
		"currentRatio": 0.8673125765340832,
		"quickRatio": 0.8260068483831466,
		"solvencyRatio": 0.3414634938155374,
		"cashRatio": 0.16975259648963673,
		"priceToEarningsRatio": 37.287278415656736,
		"priceToEarningsGrowthRatio": -45.93792700808932,
		"forwardPriceToEarningsGrowthRatio": -45.93792700808932,
		"priceToBookRatio": 61.37243774486391,
		"priceToSalesRatio": 8.93822887866815,
		"priceToFreeCashFlowRatio": 32.12256867269569,
		"priceToOperatingCashFlowRatio": 29.55638142954995,
		"debtToAssetsRatio": 0.29215025480848267,
		"debtToEquityRatio": 1.872326602282704,
		"debtToCapitalRatio": 0.6518501763673821,
		"longTermDebtToCapitalRatio": 0.6009110021023125,
		"financialLeverageRatio": 6.408779631255487,
		"workingCapitalTurnoverRatio": -31.099932397502684,
		"operatingCashFlowRatio": 0.6704045534944896,
		"operatingCashFlowSalesRatio": 0.3024128274962599,
		"freeCashFlowOperatingCashFlowRatio": 0.9201126388959359,
		"debtServiceCoverageRatio": 5.024761722304708,
		"interestCoverageRatio": 0,
		"shortTermOperatingCashFlowCoverageRatio": 5.663777000814215,
		"operatingCashFlowCoverageRatio": 1.109022873702276,
		"capitalExpenditureCoverageRatio": 12.517624642743728,
		"dividendPaidAndCapexCoverageRatio": 4.7912969490701345,
		"dividendPayoutRatio": 0.16252026969360758,
		"dividendYield": 0.0043585983369965175,
		"dividendYieldPercentage": 0.43585983369965176,
		"revenuePerShare": 25.484914639368924,
		"netIncomePerShare": 6.109054070954992,
		"interestDebtPerShare": 6.949329249507765,
		"cashPerShare": 4.247388013764271,
		"bookValuePerShare": 3.711600978715614,
		"tangibleBookValuePerShare": 3.711600978715614,
		"shareholdersEquityPerShare": 3.711600978715614,
		"operatingCashFlowPerShare": 7.706965094592383,
		"capexPerShare": 0.6156891035281195,
		"freeCashFlowPerShare": 7.091275991064264,
		"netIncomePerEBT": 0.7590881483581001,
		"ebtPerEbit": 1.0021831580314244,
		"priceToFairValue": 61.37243774486391,
		"debtToMarketCap": 0.03050761336980449,
		"effectiveTaxRate": 0.24091185164189982,
		"enterpriseValueMultiple": 26.524727497716487
	}
]
```

## About Financial Ratios API

The Financial Ratios API delivers key ratios that help investors, analysts, and researchers evaluate a company's performance. These ratios include profitability indicators like gross profit margin and net profit margin, liquidity metrics such as current ratio and quick ratio, and efficiency measurements like asset turnover and inventory turnover. This API offers a comprehensive view of a company's financial health and operational efficiency.

Profitability Ratios: Gain insight into a company's ability to generate profit, with metrics like net profit margin and return on equity.
Liquidity Ratios: Understand how well a company can meet its short-term obligations using ratios like current ratio and quick ratio.
Efficiency Ratios: Assess how effectively a company utilizes its assets with metrics such as asset turnover and inventory turnover.
Debt Ratios: Evaluate a company's leverage and debt management through ratios like debt-to-equity and interest coverage ratios.

This API is an essential tool for investors and analysts looking to analyze financial ratios and make informed decisions based on a company's financial performance.
Example Use CaseA portfolio manager can use the Financial Ratios API to compare liquidity ratios between companies in the same industry, helping them identify firms with stronger financial stability and more efficient operations.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ratios?symbol=AAPL
```

- Profitability Ratios: Gain insight into a company's ability to generate profit, with metrics like net profit margin and return on equity.
- Liquidity Ratios: Understand how well a company can meet its short-term obligations using ratios like current ratio and quick ratio.
- Efficiency Ratios: Assess how effectively a company utilizes its assets with metrics such as asset turnover and inventory turnover.
- Debt Ratios: Evaluate a company's leverage and debt management through ratios like debt-to-equity and interest coverage ratios.

## Related Financial Ratios APIs

## Financial Ratios API FAQs

## Unlock Premium Financial Insights Today!
