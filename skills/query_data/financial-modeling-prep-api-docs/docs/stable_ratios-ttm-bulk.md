---
id: "url-4011c24d"
type: "api"
title: "Ratios TTM Bulk API"
url: "https://site.financialmodelingprep.com/developer/docs/stable/ratios-ttm-bulk"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T08:45:08.243Z"
metadata:
  markdownContent: "# Ratios TTM Bulk API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"000001.SZ\",\n\t\t\"grossProfitMarginTTM\": \"1.1622776732779352\",\n\t\t\"ebitMarginTTM\": \"0.22525536322293388\",\n\t\t\"ebitdaMarginTTM\": \"0.2018381390033096\",\n\t\t\"operatingProfitMarginTTM\": \"0.4658682349579752\",\n\t\t\"pretaxProfitMarginTTM\": \"0.3160551441700993\",\n\t\t\"continuousOperationsProfitMarginTTM\": \"0.25995857044215337\",\n\t\t\"netProfitMarginTTM\": \"0.25995857044215337\",\n\t\t\"bottomLineProfitMarginTTM\": \"0.25995857044215337\",\n\t\t\"receivablesTurnoverTTM\": \"0\",\n\t\t\"payablesTurnoverTTM\": \"0\",\n\t\t\"inventoryTurnoverTTM\": \"0\",\n\t\t\"fixedAssetTurnoverTTM\": \"13.114441842310695\",\n\t\t\"assetTurnoverTTM\": \"0.029075827062555015\",\n\t\t\"currentRatioTTM\": \"0\",\n\t\t\"quickRatioTTM\": \"0\",\n\t\t\"solvencyRatioTTM\": \"0.008534174446189174\",\n\t\t\"cashRatioTTM\": \"0\",\n\t\t\"priceToEarningsRatioTTM\": \"6.68445715569793\",\n\t\t\"priceToEarningsGrowthRatioTTM\": \"-3.6096068640768793\",\n\t\t\"forwardPriceToEarningsGrowthRatioTTM\": \"2.4481492401413427\",\n\t\t\"priceToBookRatioTTM\": \"0.576796465809228\",\n\t\t\"priceToSalesRatioTTM\": \"1.483200528584014\",\n\t\t\"priceToFreeCashFlowRatioTTM\": \"1.518395607609901\",\n\t\t\"priceToOperatingCashFlowRatioTTM\": \"1.7523793147342828\",\n\t\t\"debtToAssetsRatioTTM\": \"0\",\n\t\t\"debtToEquityRatioTTM\": \"0\",\n\t\t\"debtToCapitalRatioTTM\": \"0\",\n\t\t\"longTermDebtToCapitalRatioTTM\": \"0\",\n\t\t\"financialLeverageRatioTTM\": \"11.416164801466868\",\n\t\t\"workingCapitalTurnoverRatioTTM\": \"0.23544250931631752\",\n\t\t\"operatingCashFlowRatioTTM\": \"0\",\n\t\t\"operatingCashFlowSalesRatioTTM\": \"0.991612895545132\",\n\t\t\"freeCashFlowOperatingCashFlowRatioTTM\": \"0.9850828696116743\",\n\t\t\"debtServiceCoverageRatioTTM\": \"0.24758322210087771\",\n\t\t\"interestCoverageRatioTTM\": \"0.7914088096104842\",\n\t\t\"shortTermOperatingCashFlowCoverageRatioTTM\": \"0\",\n\t\t\"operatingCashFlowCoverageRatioTTM\": \"0\",\n\t\t\"capitalExpenditureCoverageRatioTTM\": \"67.03702213279678\",\n\t\t\"dividendPaidAndCapexCoverageRatioTTM\": \"6.192364879934577\",\n\t\t\"dividendPayoutRatioTTM\": \"0.5590996519509067\",\n\t\t\"dividendYieldTTM\": \"0.10335\",\n\t\t\"enterpriseValueTTM\": \"-496959244000\",\n\t\t\"revenuePerShareTTM\": \"7.389154370023568\",\n\t\t\"netIncomePerShareTTM\": \"1.9208740068077172\",\n\t\t\"interestDebtPerShareTTM\": \"4.349676503966586\",\n\t\t\"cashPerShareTTM\": \"32.81790720767194\",\n\t\t\"bookValuePerShareTTM\": \"22.260885357516656\",\n\t\t\"tangibleBookValuePerShareTTM\": \"21.662613507347245\",\n\t\t\"shareholdersEquityPerShareTTM\": \"22.260885357516656\",\n\t\t\"operatingCashFlowPerShareTTM\": \"7.327180760489036\",\n\t\t\"capexPerShareTTM\": \"0.10930051078304583\",\n\t\t\"freeCashFlowPerShareTTM\": \"7.21788024970599\",\n\t\t\"netIncomePerEBTTTM\": \"0.8225101702576465\",\n\t\t\"ebtPerEbitTTM\": \"0.6784217520188082\",\n\t\t\"priceToFairValueTTM\": \"0.576796465809228\",\n\t\t\"debtToMarketCapTTM\": \"0\",\n\t\t\"effectiveTaxRateTTM\": \"0.17748982974235347\",\n\t\t\"enterpriseValueMultipleTTM\": \"-14.656106051669223\",\n\t\t\"dividendPerShareTTM\": \"1.327\"\n\t}\n]\n```\n\n\n## About Ratios TTM Bulk API\n\nWith this API, you can access a wide array of financial ratios including:\n\nProfitability Ratios: Gross profit margin, operating profit margin, net profit margin, and more, helping investors assess how well a company is generating profit from its operations.\nLiquidity Ratios: Key liquidity measures such as current ratio, quick ratio, and cash ratio to understand how well a company can meet its short-term liabilities.\nEfficiency Ratios: Metrics such as receivables turnover, inventory turnover, and asset turnover to evaluate how efficiently a company utilizes its assets.\nLeverage Ratios: Debt-to-assets, debt-to-equity, and debt-to-capital ratios, which provide insight into a company’s capital structure and financial leverage.\nValuation Ratios: Ratios such as price-to-earnings (P/E), price-to-book (P/B), and price-to-sales (P/S) to help investors determine whether a stock is overvalued or undervalued.\nCash Flow Ratios: Free cash flow yield, operating cash flow coverage, and capital expenditure coverage ratios to assess how well a company manages its cash flow relative to its operations and investments.\n\nThis API is invaluable for financial analysts, institutional investors, and portfolio managers who need to track and compare TTM ratios across multiple companies for investment decision-making.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ratios-ttm-bulk\n```\n\n- Profitability Ratios: Gross profit margin, operating profit margin, net profit margin, and more, helping investors assess how well a company is generating profit from its operations.\n- Liquidity Ratios: Key liquidity measures such as current ratio, quick ratio, and cash ratio to understand how well a company can meet its short-term liabilities.\n- Efficiency Ratios: Metrics such as receivables turnover, inventory turnover, and asset turnover to evaluate how efficiently a company utilizes its assets.\n- Leverage Ratios: Debt-to-assets, debt-to-equity, and debt-to-capital ratios, which provide insight into a company’s capital structure and financial leverage.\n- Valuation Ratios: Ratios such as price-to-earnings (P/E), price-to-book (P/B), and price-to-sales (P/S) to help investors determine whether a stock is overvalued or undervalued.\n- Cash Flow Ratios: Free cash flow yield, operating cash flow coverage, and capital expenditure coverage ratios to assess how well a company manages its cash flow relative to its operations and investments.\n\n\n## Related Ratios TTM Bulk APIs\n\n\n## Ratios TTM Bulk API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "stable_ratios-ttm-bulk"
---

# Ratios TTM Bulk API

## 源URL

https://site.financialmodelingprep.com/developer/docs/stable/ratios-ttm-bulk

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "000001.SZ",
		"grossProfitMarginTTM": "1.1622776732779352",
		"ebitMarginTTM": "0.22525536322293388",
		"ebitdaMarginTTM": "0.2018381390033096",
		"operatingProfitMarginTTM": "0.4658682349579752",
		"pretaxProfitMarginTTM": "0.3160551441700993",
		"continuousOperationsProfitMarginTTM": "0.25995857044215337",
		"netProfitMarginTTM": "0.25995857044215337",
		"bottomLineProfitMarginTTM": "0.25995857044215337",
		"receivablesTurnoverTTM": "0",
		"payablesTurnoverTTM": "0",
		"inventoryTurnoverTTM": "0",
		"fixedAssetTurnoverTTM": "13.114441842310695",
		"assetTurnoverTTM": "0.029075827062555015",
		"currentRatioTTM": "0",
		"quickRatioTTM": "0",
		"solvencyRatioTTM": "0.008534174446189174",
		"cashRatioTTM": "0",
		"priceToEarningsRatioTTM": "6.68445715569793",
		"priceToEarningsGrowthRatioTTM": "-3.6096068640768793",
		"forwardPriceToEarningsGrowthRatioTTM": "2.4481492401413427",
		"priceToBookRatioTTM": "0.576796465809228",
		"priceToSalesRatioTTM": "1.483200528584014",
		"priceToFreeCashFlowRatioTTM": "1.518395607609901",
		"priceToOperatingCashFlowRatioTTM": "1.7523793147342828",
		"debtToAssetsRatioTTM": "0",
		"debtToEquityRatioTTM": "0",
		"debtToCapitalRatioTTM": "0",
		"longTermDebtToCapitalRatioTTM": "0",
		"financialLeverageRatioTTM": "11.416164801466868",
		"workingCapitalTurnoverRatioTTM": "0.23544250931631752",
		"operatingCashFlowRatioTTM": "0",
		"operatingCashFlowSalesRatioTTM": "0.991612895545132",
		"freeCashFlowOperatingCashFlowRatioTTM": "0.9850828696116743",
		"debtServiceCoverageRatioTTM": "0.24758322210087771",
		"interestCoverageRatioTTM": "0.7914088096104842",
		"shortTermOperatingCashFlowCoverageRatioTTM": "0",
		"operatingCashFlowCoverageRatioTTM": "0",
		"capitalExpenditureCoverageRatioTTM": "67.03702213279678",
		"dividendPaidAndCapexCoverageRatioTTM": "6.192364879934577",
		"dividendPayoutRatioTTM": "0.5590996519509067",
		"dividendYieldTTM": "0.10335",
		"enterpriseValueTTM": "-496959244000",
		"revenuePerShareTTM": "7.389154370023568",
		"netIncomePerShareTTM": "1.9208740068077172",
		"interestDebtPerShareTTM": "4.349676503966586",
		"cashPerShareTTM": "32.81790720767194",
		"bookValuePerShareTTM": "22.260885357516656",
		"tangibleBookValuePerShareTTM": "21.662613507347245",
		"shareholdersEquityPerShareTTM": "22.260885357516656",
		"operatingCashFlowPerShareTTM": "7.327180760489036",
		"capexPerShareTTM": "0.10930051078304583",
		"freeCashFlowPerShareTTM": "7.21788024970599",
		"netIncomePerEBTTTM": "0.8225101702576465",
		"ebtPerEbitTTM": "0.6784217520188082",
		"priceToFairValueTTM": "0.576796465809228",
		"debtToMarketCapTTM": "0",
		"effectiveTaxRateTTM": "0.17748982974235347",
		"enterpriseValueMultipleTTM": "-14.656106051669223",
		"dividendPerShareTTM": "1.327"
	}
]
```

## About Ratios TTM Bulk API

With this API, you can access a wide array of financial ratios including:

Profitability Ratios: Gross profit margin, operating profit margin, net profit margin, and more, helping investors assess how well a company is generating profit from its operations.
Liquidity Ratios: Key liquidity measures such as current ratio, quick ratio, and cash ratio to understand how well a company can meet its short-term liabilities.
Efficiency Ratios: Metrics such as receivables turnover, inventory turnover, and asset turnover to evaluate how efficiently a company utilizes its assets.
Leverage Ratios: Debt-to-assets, debt-to-equity, and debt-to-capital ratios, which provide insight into a company’s capital structure and financial leverage.
Valuation Ratios: Ratios such as price-to-earnings (P/E), price-to-book (P/B), and price-to-sales (P/S) to help investors determine whether a stock is overvalued or undervalued.
Cash Flow Ratios: Free cash flow yield, operating cash flow coverage, and capital expenditure coverage ratios to assess how well a company manages its cash flow relative to its operations and investments.

This API is invaluable for financial analysts, institutional investors, and portfolio managers who need to track and compare TTM ratios across multiple companies for investment decision-making.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ratios-ttm-bulk
```

- Profitability Ratios: Gross profit margin, operating profit margin, net profit margin, and more, helping investors assess how well a company is generating profit from its operations.
- Liquidity Ratios: Key liquidity measures such as current ratio, quick ratio, and cash ratio to understand how well a company can meet its short-term liabilities.
- Efficiency Ratios: Metrics such as receivables turnover, inventory turnover, and asset turnover to evaluate how efficiently a company utilizes its assets.
- Leverage Ratios: Debt-to-assets, debt-to-equity, and debt-to-capital ratios, which provide insight into a company’s capital structure and financial leverage.
- Valuation Ratios: Ratios such as price-to-earnings (P/E), price-to-book (P/B), and price-to-sales (P/S) to help investors determine whether a stock is overvalued or undervalued.
- Cash Flow Ratios: Free cash flow yield, operating cash flow coverage, and capital expenditure coverage ratios to assess how well a company manages its cash flow relative to its operations and investments.

## Related Ratios TTM Bulk APIs

## Ratios TTM Bulk API FAQs

## Unlock Premium Financial Insights Today!
