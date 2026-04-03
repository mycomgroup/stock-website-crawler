---
id: "url-5eeb68fc"
type: "api"
title: "Financial Ratios TTM API"
url: "https://site.financialmodelingprep.com/developer/docs/stable/metrics-ratios-ttm"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T10:02:19.027Z"
metadata:
  markdownContent: "# Financial Ratios TTM API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"grossProfitMarginTTM\": 0.46518849807964424,\n\t\t\"ebitMarginTTM\": 0.3175535678188801,\n\t\t\"ebitdaMarginTTM\": 0.34705882352941175,\n\t\t\"operatingProfitMarginTTM\": 0.3175535678188801,\n\t\t\"pretaxProfitMarginTTM\": 0.31773296947645036,\n\t\t\"continuousOperationsProfitMarginTTM\": 0.24295027289266222,\n\t\t\"netProfitMarginTTM\": 0.24295027289266222,\n\t\t\"bottomLineProfitMarginTTM\": 0.24295027289266222,\n\t\t\"receivablesTurnoverTTM\": 6.673186524129093,\n\t\t\"payablesTurnoverTTM\": 3.4187853335486995,\n\t\t\"inventoryTurnoverTTM\": 30.626103313558097,\n\t\t\"fixedAssetTurnoverTTM\": 8.590592372311098,\n\t\t\"assetTurnoverTTM\": 1.1501809145995903,\n\t\t\"currentRatioTTM\": 0.9229383853427077,\n\t\t\"quickRatioTTM\": 0.8750666712845911,\n\t\t\"solvencyRatioTTM\": 0.3888081578786054,\n\t\t\"cashRatioTTM\": 0.20987774044955496,\n\t\t\"priceToEarningsRatioTTM\": 32.889608822880916,\n\t\t\"priceToEarningsGrowthRatioTTM\": 9.104441715061135,\n\t\t\"forwardPriceToEarningsGrowthRatioTTM\": 9.104441715061135,\n\t\t\"priceToBookRatioTTM\": 47.370141231313106,\n\t\t\"priceToSalesRatioTTM\": 7.958949686678795,\n\t\t\"priceToFreeCashFlowRatioTTM\": 32.04339747098139,\n\t\t\"priceToOperatingCashFlowRatioTTM\": 29.201395167968677,\n\t\t\"debtToAssetsRatioTTM\": 0.28132292892744526,\n\t\t\"debtToEquityRatioTTM\": 1.4499985020521886,\n\t\t\"debtToCapitalRatioTTM\": 0.5918364851397372,\n\t\t\"longTermDebtToCapitalRatioTTM\": 0.557055084464615,\n\t\t\"financialLeverageRatioTTM\": 5.154213727193745,\n\t\t\"workingCapitalTurnoverRatioTTM\": -22.92267593397046,\n\t\t\"operatingCashFlowRatioTTM\": 0.7501402694558931,\n\t\t\"operatingCashFlowSalesRatioTTM\": 0.2736355366889024,\n\t\t\"freeCashFlowOperatingCashFlowRatioTTM\": 0.9077049513361775,\n\t\t\"debtServiceCoverageRatioTTM\": 8.390251498870981,\n\t\t\"interestCoverageRatioTTM\": 0,\n\t\t\"shortTermOperatingCashFlowCoverageRatioTTM\": 8.432142022891847,\n\t\t\"operatingCashFlowCoverageRatioTTM\": 1.1187512267688715,\n\t\t\"capitalExpenditureCoverageRatioTTM\": 10.834817408704351,\n\t\t\"dividendPaidAndCapexCoverageRatioTTM\": 4.287173396674584,\n\t\t\"dividendPayoutRatioTTM\": 0.15876235049401977,\n\t\t\"dividendYieldTTM\": 0.0047691720717283476,\n\t\t\"enterpriseValueTTM\": 3216333928000,\n\t\t\"revenuePerShareTTM\": 26.24103186081379,\n\t\t\"netIncomePerShareTTM\": 6.375265851569754,\n\t\t\"interestDebtPerShareTTM\": 6.418298067250137,\n\t\t\"cashPerShareTTM\": 3.565573803101025,\n\t\t\"bookValuePerShareTTM\": 4.426417032959892,\n\t\t\"tangibleBookValuePerShareTTM\": 4.426417032959892,\n\t\t\"shareholdersEquityPerShareTTM\": 4.426417032959892,\n\t\t\"operatingCashFlowPerShareTTM\": 7.180478836504368,\n\t\t\"capexPerShareTTM\": 0.6627226436447186,\n\t\t\"freeCashFlowPerShareTTM\": 6.5177561928596495,\n\t\t\"netIncomePerEBTTTM\": 0.7646366484818603,\n\t\t\"ebtPerEbitTTM\": 1.0005649492739208,\n\t\t\"priceToFairValueTTM\": 47.370141231313106,\n\t\t\"debtToMarketCapTTM\": 0.030731461471514124,\n\t\t\"effectiveTaxRateTTM\": 0.23536335151813975,\n\t\t\"enterpriseValueMultipleTTM\": 23.41672438697653\n\t}\n]\n```\n\n\n## About Financial Ratios TTM API\n\nThe TTM Ratios API offers a comprehensive view of a company's financial performance, making it an essential tool for investors, analysts, and decision-makers. This API is ideal for:\n\nProfitability Analysis: Understand how efficiently a company generates profit using metrics like gross profit margin, net profit margin, and EBITDA margin.\nLiquidity Assessment: Evaluate a company’s ability to meet short-term obligations with ratios such as the current ratio and quick ratio.\nEfficiency Insight: Examine how well a company manages its assets and liabilities with key efficiency ratios like asset turnover and inventory turnover.\nLeverage Evaluation: Assess a company’s debt levels and leverage through metrics like the debt-to-equity ratio and financial leverage ratio.\n\nThis API provides insights into a company's performance across key areas, helping users make more informed decisions by analyzing trends over the past twelve months.\nExample Use CaseAn investor uses the TTM Ratios API to analyze Apple’s liquidity and profitability ratios, helping them decide whether to invest in the company based on its trailing twelve-month financial performance.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ratios-ttm?symbol=AAPL\n```\n\n- Profitability Analysis: Understand how efficiently a company generates profit using metrics like gross profit margin, net profit margin, and EBITDA margin.\n- Liquidity Assessment: Evaluate a company’s ability to meet short-term obligations with ratios such as the current ratio and quick ratio.\n- Efficiency Insight: Examine how well a company manages its assets and liabilities with key efficiency ratios like asset turnover and inventory turnover.\n- Leverage Evaluation: Assess a company’s debt levels and leverage through metrics like the debt-to-equity ratio and financial leverage ratio.\n\n\n## Related Financial Ratios TTM APIs\n\n\n## Financial Ratios TTM API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "stable_metrics-ratios-ttm"
---

# Financial Ratios TTM API

## 源URL

https://site.financialmodelingprep.com/developer/docs/stable/metrics-ratios-ttm

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"grossProfitMarginTTM": 0.46518849807964424,
		"ebitMarginTTM": 0.3175535678188801,
		"ebitdaMarginTTM": 0.34705882352941175,
		"operatingProfitMarginTTM": 0.3175535678188801,
		"pretaxProfitMarginTTM": 0.31773296947645036,
		"continuousOperationsProfitMarginTTM": 0.24295027289266222,
		"netProfitMarginTTM": 0.24295027289266222,
		"bottomLineProfitMarginTTM": 0.24295027289266222,
		"receivablesTurnoverTTM": 6.673186524129093,
		"payablesTurnoverTTM": 3.4187853335486995,
		"inventoryTurnoverTTM": 30.626103313558097,
		"fixedAssetTurnoverTTM": 8.590592372311098,
		"assetTurnoverTTM": 1.1501809145995903,
		"currentRatioTTM": 0.9229383853427077,
		"quickRatioTTM": 0.8750666712845911,
		"solvencyRatioTTM": 0.3888081578786054,
		"cashRatioTTM": 0.20987774044955496,
		"priceToEarningsRatioTTM": 32.889608822880916,
		"priceToEarningsGrowthRatioTTM": 9.104441715061135,
		"forwardPriceToEarningsGrowthRatioTTM": 9.104441715061135,
		"priceToBookRatioTTM": 47.370141231313106,
		"priceToSalesRatioTTM": 7.958949686678795,
		"priceToFreeCashFlowRatioTTM": 32.04339747098139,
		"priceToOperatingCashFlowRatioTTM": 29.201395167968677,
		"debtToAssetsRatioTTM": 0.28132292892744526,
		"debtToEquityRatioTTM": 1.4499985020521886,
		"debtToCapitalRatioTTM": 0.5918364851397372,
		"longTermDebtToCapitalRatioTTM": 0.557055084464615,
		"financialLeverageRatioTTM": 5.154213727193745,
		"workingCapitalTurnoverRatioTTM": -22.92267593397046,
		"operatingCashFlowRatioTTM": 0.7501402694558931,
		"operatingCashFlowSalesRatioTTM": 0.2736355366889024,
		"freeCashFlowOperatingCashFlowRatioTTM": 0.9077049513361775,
		"debtServiceCoverageRatioTTM": 8.390251498870981,
		"interestCoverageRatioTTM": 0,
		"shortTermOperatingCashFlowCoverageRatioTTM": 8.432142022891847,
		"operatingCashFlowCoverageRatioTTM": 1.1187512267688715,
		"capitalExpenditureCoverageRatioTTM": 10.834817408704351,
		"dividendPaidAndCapexCoverageRatioTTM": 4.287173396674584,
		"dividendPayoutRatioTTM": 0.15876235049401977,
		"dividendYieldTTM": 0.0047691720717283476,
		"enterpriseValueTTM": 3216333928000,
		"revenuePerShareTTM": 26.24103186081379,
		"netIncomePerShareTTM": 6.375265851569754,
		"interestDebtPerShareTTM": 6.418298067250137,
		"cashPerShareTTM": 3.565573803101025,
		"bookValuePerShareTTM": 4.426417032959892,
		"tangibleBookValuePerShareTTM": 4.426417032959892,
		"shareholdersEquityPerShareTTM": 4.426417032959892,
		"operatingCashFlowPerShareTTM": 7.180478836504368,
		"capexPerShareTTM": 0.6627226436447186,
		"freeCashFlowPerShareTTM": 6.5177561928596495,
		"netIncomePerEBTTTM": 0.7646366484818603,
		"ebtPerEbitTTM": 1.0005649492739208,
		"priceToFairValueTTM": 47.370141231313106,
		"debtToMarketCapTTM": 0.030731461471514124,
		"effectiveTaxRateTTM": 0.23536335151813975,
		"enterpriseValueMultipleTTM": 23.41672438697653
	}
]
```

## About Financial Ratios TTM API

The TTM Ratios API offers a comprehensive view of a company's financial performance, making it an essential tool for investors, analysts, and decision-makers. This API is ideal for:

Profitability Analysis: Understand how efficiently a company generates profit using metrics like gross profit margin, net profit margin, and EBITDA margin.
Liquidity Assessment: Evaluate a company’s ability to meet short-term obligations with ratios such as the current ratio and quick ratio.
Efficiency Insight: Examine how well a company manages its assets and liabilities with key efficiency ratios like asset turnover and inventory turnover.
Leverage Evaluation: Assess a company’s debt levels and leverage through metrics like the debt-to-equity ratio and financial leverage ratio.

This API provides insights into a company's performance across key areas, helping users make more informed decisions by analyzing trends over the past twelve months.
Example Use CaseAn investor uses the TTM Ratios API to analyze Apple’s liquidity and profitability ratios, helping them decide whether to invest in the company based on its trailing twelve-month financial performance.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ratios-ttm?symbol=AAPL
```

- Profitability Analysis: Understand how efficiently a company generates profit using metrics like gross profit margin, net profit margin, and EBITDA margin.
- Liquidity Assessment: Evaluate a company’s ability to meet short-term obligations with ratios such as the current ratio and quick ratio.
- Efficiency Insight: Examine how well a company manages its assets and liabilities with key efficiency ratios like asset turnover and inventory turnover.
- Leverage Evaluation: Assess a company’s debt levels and leverage through metrics like the debt-to-equity ratio and financial leverage ratio.

## Related Financial Ratios TTM APIs

## Financial Ratios TTM API FAQs

## Unlock Premium Financial Insights Today!
