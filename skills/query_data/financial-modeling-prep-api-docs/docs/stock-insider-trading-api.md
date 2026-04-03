---
id: "url-7606f32a"
type: "api"
title: "Search Insider Trades API"
url: "https://site.financialmodelingprep.com/developer/docs/stock-insider-trading-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T09:57:24.024Z"
metadata:
  markdownContent: "# Search Insider Trades API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"filingDate\": \"2025-02-04\",\n\t\t\"transactionDate\": \"2025-02-03\",\n\t\t\"reportingCik\": \"0001214128\",\n\t\t\"companyCik\": \"0000320193\",\n\t\t\"transactionType\": \"S-Sale\",\n\t\t\"securitiesOwned\": 4159576,\n\t\t\"reportingName\": \"LEVINSON ARTHUR D\",\n\t\t\"typeOfOwner\": \"director\",\n\t\t\"acquisitionOrDisposition\": \"D\",\n\t\t\"directOrIndirect\": \"D\",\n\t\t\"formType\": \"4\",\n\t\t\"securitiesTransacted\": 1516,\n\t\t\"price\": 226.3501,\n\t\t\"securityName\": \"Common Stock\",\n\t\t\"url\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019325000019/0000320193-25-000019-index.htm\"\n\t}\n]\n```\n\n\n## About Search Insider Trades API\n\nThe FMP Search Insider Trades API allows users to search for specific insider trading activities based on a company or stock symbol. This API provides detailed information on stock transactions by corporate insiders, including transaction dates, types, amounts, and roles within the company. Key features include:\n\nCompany-Specific Searches: Search insider trading activity by entering the stock symbol or company name to retrieve relevant transactions.\nDetailed Transaction Information: Access detailed data such as transaction type (purchase or sale), number of securities transacted, and price.\nInsider Roles: Understand the roles of the insiders involved in the transactions, such as directors or executives.\nDirect Links to Filings: Each transaction includes a link to the official SEC filing for deeper analysis and verification.\n\nThis API is perfect for investors, financial researchers, and analysts who need to investigate insider trading activities of specific companies or individuals.\nExample Use CaseAn investment analyst uses the Search Insider Trades API to investigate recent sales of Apple (AAPL) stock by Chris Kondo, the Principal Accounting Officer. By retrieving detailed information about the transaction, including the sale of 8,706 shares at $225, the analyst can better assess the implications for the company’s financial performance and strategy.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/insider-trading/search?page=0&limit=100\n```\n\n- Company-Specific Searches: Search insider trading activity by entering the stock symbol or company name to retrieve relevant transactions.\n- Detailed Transaction Information: Access detailed data such as transaction type (purchase or sale), number of securities transacted, and price.\n- Insider Roles: Understand the roles of the insiders involved in the transactions, such as directors or executives.\n- Direct Links to Filings: Each transaction includes a link to the official SEC filing for deeper analysis and verification.\n\n\n## Related Search Insider Trades APIs\n\n\n## Search Insider Trades API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "stock-insider-trading-api"
---

# Search Insider Trades API

## 源URL

https://site.financialmodelingprep.com/developer/docs/stock-insider-trading-api

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"filingDate": "2025-02-04",
		"transactionDate": "2025-02-03",
		"reportingCik": "0001214128",
		"companyCik": "0000320193",
		"transactionType": "S-Sale",
		"securitiesOwned": 4159576,
		"reportingName": "LEVINSON ARTHUR D",
		"typeOfOwner": "director",
		"acquisitionOrDisposition": "D",
		"directOrIndirect": "D",
		"formType": "4",
		"securitiesTransacted": 1516,
		"price": 226.3501,
		"securityName": "Common Stock",
		"url": "https://www.sec.gov/Archives/edgar/data/320193/000032019325000019/0000320193-25-000019-index.htm"
	}
]
```

## About Search Insider Trades API

The FMP Search Insider Trades API allows users to search for specific insider trading activities based on a company or stock symbol. This API provides detailed information on stock transactions by corporate insiders, including transaction dates, types, amounts, and roles within the company. Key features include:

Company-Specific Searches: Search insider trading activity by entering the stock symbol or company name to retrieve relevant transactions.
Detailed Transaction Information: Access detailed data such as transaction type (purchase or sale), number of securities transacted, and price.
Insider Roles: Understand the roles of the insiders involved in the transactions, such as directors or executives.
Direct Links to Filings: Each transaction includes a link to the official SEC filing for deeper analysis and verification.

This API is perfect for investors, financial researchers, and analysts who need to investigate insider trading activities of specific companies or individuals.
Example Use CaseAn investment analyst uses the Search Insider Trades API to investigate recent sales of Apple (AAPL) stock by Chris Kondo, the Principal Accounting Officer. By retrieving detailed information about the transaction, including the sale of 8,706 shares at $225, the analyst can better assess the implications for the company’s financial performance and strategy.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/insider-trading/search?page=0&limit=100
```

- Company-Specific Searches: Search insider trading activity by entering the stock symbol or company name to retrieve relevant transactions.
- Detailed Transaction Information: Access detailed data such as transaction type (purchase or sale), number of securities transacted, and price.
- Insider Roles: Understand the roles of the insiders involved in the transactions, such as directors or executives.
- Direct Links to Filings: Each transaction includes a link to the official SEC filing for deeper analysis and verification.

## Related Search Insider Trades APIs

## Search Insider Trades API FAQs

## Unlock Premium Financial Insights Today!
