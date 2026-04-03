---
id: "url-2ced8105"
type: "api"
title: "Free Stock Market API and Financial Statements API"
url: "https://site.financialmodelingprep.com/developer/docs/stable"
description: "FMP is your source for the most reliable and accurate Stock Market API and Financial Data API available. Whether you're looking for real-time stock prices, financial statements, or historical data, we offer a comprehensive solution to meet all your financial data needs."
source: ""
tags: []
crawl_time: "2026-03-18T04:57:20.100Z"
metadata:
  markdownContent: "# Free Stock Market API and Financial Statements API\n\nFMP is your source for the most reliable and accurate Stock Market API and Financial Data API available. Whether you're looking for real-time stock prices, financial statements, or historical data, we offer a comprehensive solution to meet all your financial data needs.\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"name\": \"Apple Inc.\",\n\t\t\"currency\": \"USD\",\n\t\t\"exchangeFullName\": \"NASDAQ Global Select\",\n\t\t\"exchange\": \"NASDAQ\"\n\t}\n]\n```\n\n\n#### Authorization\n\nAll API requests must be authorized using an API key. Authorization can be done using either request headers or URL query parameters.\n\nHeader Authorization\n\nURL Query Authorization\n\nNote: When adding the API key to your requests, ensure to use &apikey= if other query parameters already exist in the endpoint.\n\n\n## Company Search\n\n### Stock Symbol Search API\n\nEasily find the ticker symbol of any stock with the FMP Stock Symbol Search API. Search by symbol across multiple global markets.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/search-symbol?query=AAPL\n```\n\n---\n\n### Company Name Search API\n\nSearch for ticker symbols, company names, and exchange details for equity securities and ETFs listed on various exchanges with the FMP Name Search API. This endpoint is useful for retrieving ticker symbols when you know the full or partial company or asset name but not the symbol identifier.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/search-name?query=AA\n```\n\n---\n\n### CIK API\n\nEasily retrieve the Central Index Key (CIK) for publicly traded companies with the FMP CIK API. Access unique identifiers needed for SEC filings and regulatory documents for a streamlined compliance and financial analysis process.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/search-cik?cik=320193\n```\n\n---\n\n### CUSIP API\n\nEasily search and retrieve financial securities information by CUSIP number using the FMP CUSIP API. Find key details such as company name, stock symbol, and market capitalization associated with the CUSIP.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/search-cusip?cusip=037833100\n```\n\n---\n\n### ISIN API\n\nEasily search and retrieve the International Securities Identification Number (ISIN) for financial securities using the FMP ISIN API. Find key details such as company name, stock symbol, and market capitalization associated with the ISIN.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/search-isin?isin=US0378331005\n```\n\n---\n\n### Stock Screener API\n\nDiscover stocks that align with your investment strategy using the FMP Stock Screener API. Filter stocks based on market cap, price, volume, beta, sector, country, and more to identify the best opportunities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/company-screener\n```\n\n---\n\n### Exchange Variants API\n\nSearch across multiple public exchanges to find where a given stock symbol is listed using the FMP Exchange Variants API. This allows users to quickly identify all the exchanges where a security is actively traded.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/search-exchange-variants?symbol=AAPL\n```\n\n---\n\n\n## Stock Directory\n\n### Company Symbols List API\n\nEasily retrieve a comprehensive list of financial symbols with the FMP Company Symbols List API. Access a broad range of stock symbols and other tradable financial instruments from various global exchanges, helping you explore the full range of available securities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/stock-list\n```\n\n---\n\n### Financial Statement Symbols List API\n\nAccess a comprehensive list of companies with available financial statements through the FMP Financial Statement Symbols List API. Find companies listed on major global exchanges and obtain up-to-date financial data including income statements, balance sheets, and cash flow statements, are provided.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/financial-statement-symbol-list\n```\n\n---\n\n### CIK List API\n\nAccess a comprehensive database of CIK (Central Index Key) numbers for SEC-registered entities with the FMP CIK List API. This endpoint is essential for businesses, financial professionals, and individuals who need quick access to CIK numbers for regulatory compliance, financial transactions, and investment research.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/cik-list?page=0&limit=1000\n```\n\n---\n\n### Symbol Changes List API\n\nStay informed about the latest stock symbol changes with the FMP Stock Symbol Changes API. Track changes due to mergers, acquisitions, stock splits, and name changes to ensure accurate trading and analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/symbol-change\n```\n\n---\n\n### ETF Symbol Search API\n\nQuickly find ticker symbols and company names for Exchange Traded Funds (ETFs) using the FMP ETF Symbol Search API. This tool simplifies identifying specific ETFs by their name or ticker.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/etf-list\n```\n\n---\n\n### Actively Trading List API\n\nList all actively trading companies and financial instruments with the FMP Actively Trading List API. This endpoint allows users to filter and display securities that are currently being traded on public exchanges, ensuring you access real-time market activity.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/actively-trading-list\n```\n\n---\n\n### Earnings Transcript List API\n\nAccess available earnings transcripts for companies with the FMP Earnings Transcript List API. Retrieve a list of companies with earnings transcripts, along with the total number of transcripts available for each company.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/earnings-transcript-list\n```\n\n---\n\n### Available Exchanges API\n\nAccess a complete list of supported stock exchanges using the FMP Available Exchanges API. This API provides a comprehensive overview of global stock exchanges, allowing users to identify where securities are traded and filter data by specific exchanges for further analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/available-exchanges\n```\n\n---\n\n### Available Sectors API\n\nAccess a complete list of industry sectors using the FMP Available Sectors API. This API helps users categorize and filter companies based on their respective sectors, enabling deeper analysis and more focused queries across different industries.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/available-sectors\n```\n\n---\n\n### Available Industries API\n\nAccess a comprehensive list of industries where stock symbols are available using the FMP Available Industries API. This API helps users filter and categorize companies based on their industry for more focused research and analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/available-industries\n```\n\n---\n\n### Available Countries API\n\nAccess a comprehensive list of countries where stock symbols are available with the FMP Available Countries API. This API enables users to filter and analyze stock symbols based on the country of origin or the primary market where the securities are traded.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/available-countries\n```\n\n---\n\n\n## Company Information\n\n### Company Profile Data API\n\nAccess detailed company profile data with the FMP Company Profile Data API. This API provides key financial and operational information for a specific stock symbol, including the company's market capitalization, stock price, industry, and much more.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/profile?symbol=AAPL\n```\n\n---\n\n### Company Profile by CIK API\n\nRetrieve detailed company profile data by CIK (Central Index Key) with the FMP Company Profile by CIK API. This API allows users to search for companies using their unique CIK identifier and access a full range of company data, including stock price, market capitalization, industry, and much more.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/profile-cik?cik=320193\n```\n\n---\n\n### Company Notes API\n\nRetrieve detailed information about company-issued notes with the FMP Company Notes API. Access essential data such as CIK number, stock symbol, note title, and the exchange where the notes are listed.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/company-notes?symbol=AAPL\n```\n\n---\n\n### Stock Peer Comparison API\n\nIdentify and compare companies within the same sector and market capitalization range using the FMP Stock Peer Comparison API. Gain insights into how a company stacks up against its peers on the same exchange.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/stock-peers?symbol=AAPL\n```\n\n---\n\n### Delisted Companies API\n\nStay informed with the FMP Delisted Companies API. Access a comprehensive list of companies that have been delisted from US exchanges to avoid trading in risky stocks and identify potential financial troubles.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/delisted-companies?page=0&limit=100\n```\n\n---\n\n### Company Employee Count API\n\nRetrieve detailed workforce information for companies, including employee count, reporting period, and filing date. The FMP Company Employee Count API also provides direct links to official SEC documents for further verification and in-depth research.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/employee-count?symbol=AAPL\n```\n\n---\n\n### Company Historical Employee Count API\n\nAccess historical employee count data for a company based on specific reporting periods. The FMP Company Historical Employee Count API provides insights into how a company’s workforce has evolved over time, allowing users to analyze growth trends and operational changes.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-employee-count?symbol=AAPL\n```\n\n---\n\n### Company Market Cap API\n\nRetrieve the market capitalization for a specific company on any given date using the FMP Company Market Capitalization API. This API provides essential data to assess the size and value of a company in the stock market, helping users gauge its overall market standing.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/market-capitalization?symbol=AAPL\n```\n\n---\n\n### Batch Market Cap API\n\nRetrieve market capitalization data for multiple companies in a single request with the FMP Batch Market Capitalization API. This API allows users to compare the market size of various companies simultaneously, streamlining the analysis of company valuations.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/market-capitalization-batch?symbols=AAPL,MSFT,GOOG\n```\n\n---\n\n### Historical Market Cap API\n\nAccess historical market capitalization data for a company using the FMP Historical Market Capitalization API. This API helps track the changes in market value over time, enabling long-term assessments of a company's growth or decline.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-market-capitalization?symbol=AAPL\n```\n\n---\n\n### Company Share Float & Liquidity API\n\nUnderstand the liquidity and volatility of a stock with the FMP Company Share Float and Liquidity API. Access the total number of publicly traded shares for any company to make informed investment decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/shares-float?symbol=AAPL\n```\n\n---\n\n### All Shares Float API\n\nAccess comprehensive shares float data for all available companies with the FMP All Shares Float API. Retrieve critical information such as free float, float shares, and outstanding shares to analyze liquidity across a wide range of companies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/shares-float-all?page=0&limit=1000\n```\n\n---\n\n### Latest Mergers & Acquisitions API\n\nAccess real-time data on the latest mergers and acquisitions with the FMP Latest Mergers and Acquisitions API. This API provides key information such as the transaction date, company names, and links to detailed filing information for further analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/mergers-acquisitions-latest?page=0&limit=100\n```\n\n---\n\n### Search Mergers & Acquisitions API\n\nSearch for specific mergers and acquisitions data with the FMP Search Mergers and Acquisitions API. Retrieve detailed information on M&A activity, including acquiring and targeted companies, transaction dates, and links to official SEC filings.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/mergers-acquisitions-search?name=Apple\n```\n\n---\n\n### Company Executives API\n\nRetrieve detailed information on company executives with the FMP Company Executives API. This API provides essential data about key executives, including their name, title, compensation, and other demographic details such as gender and year of birth.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/key-executives?symbol=AAPL\n```\n\n---\n\n### Executive Compensation API\n\nRetrieve comprehensive compensation data for company executives with the FMP Executive Compensation API. This API provides detailed information on salaries, stock awards, total compensation, and other relevant financial data, including filing details and links to official documents.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/governance-executive-compensation?symbol=AAPL\n```\n\n---\n\n### Executive Compensation Benchmark API\n\nGain access to average executive compensation data across various industries with the FMP Executive Compensation Benchmark API. This API provides essential insights for comparing executive pay by industry, helping you understand compensation trends and benchmarks.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/executive-compensation-benchmark\n```\n\n---\n\n\n## Quote\n\n### Stock Quote API\n\nAccess real-time stock quotes with the FMP Stock Quote API. Get up-to-the-minute prices, changes, and volume data for individual stocks.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote?symbol=AAPL\n```\n\n---\n\n### Stock Quote Short API\n\nGet quick snapshots of real-time stock quotes with the FMP Stock Quote Short API. Access key stock data like current price, volume, and price changes for instant market insights.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote-short?symbol=AAPL\n```\n\n---\n\n### Aftermarket Trade API\n\nTrack real-time trading activity occurring after regular market hours with the FMP Aftermarket Trade API. Access key details such as trade prices, sizes, and timestamps for trades executed during the post-market session.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/aftermarket-trade?symbol=AAPL\n```\n\n---\n\n### Aftermarket Quote API\n\nAccess real-time aftermarket quotes for stocks with the FMP Aftermarket Quote API. Track bid and ask prices, volume, and other relevant data outside of regular trading hours.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/aftermarket-quote?symbol=AAPL\n```\n\n---\n\n### Stock Price Change API\n\nTrack stock price fluctuations in real-time with the FMP Stock Price Change API. Monitor percentage and value changes over various time periods, including daily, weekly, monthly, and long-term.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/stock-price-change?symbol=AAPL\n```\n\n---\n\n### Stock Batch Quote API\n\nRetrieve multiple real-time stock quotes in a single request with the FMP Stock Batch Quote API. Access current prices, volume, and detailed data for multiple companies at once, making it easier to track large portfolios or monitor multiple stocks simultaneously.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-quote?symbols=AAPL\n```\n\n---\n\n### Stock Batch Quote Short API\n\nAccess real-time, short-form quotes for multiple stocks with the FMP Stock Batch Quote Short API. Get a quick snapshot of key stock data such as current price, change, and volume for several companies in one streamlined request.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-quote-short?symbols=AAPL\n```\n\n---\n\n### Batch Aftermarket Trade API\n\nRetrieve real-time aftermarket trading data for multiple stocks with the FMP Batch Aftermarket Trade API. Track post-market trade prices, volumes, and timestamps across several companies simultaneously.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-aftermarket-trade?symbols=AAPL\n```\n\n---\n\n### Batch Aftermarket Quote API\n\nRetrieve real-time aftermarket quotes for multiple stocks with the FMP Batch Aftermarket Quote API. Access bid and ask prices, volume, and other relevant data for several companies during post-market trading.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-aftermarket-quote?symbols=AAPL\n```\n\n---\n\n### Exchange Stock Quotes API\n\nRetrieve real-time stock quotes for all listed stocks on a specific exchange with the FMP Exchange Stock Quotes API. Track price changes and trading activity across the entire exchange.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-exchange-quote?exchange=NASDAQ\n```\n\n---\n\n### Mutual Fund Price Quotes API\n\nAccess real-time quotes for mutual funds with the FMP Mutual Fund Price Quotes API. Track current prices, performance changes, and key data for various mutual funds.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-mutualfund-quotes\n```\n\n---\n\n### ETF Price Quotes API\n\nGet real-time price quotes for exchange-traded funds (ETFs) with the FMP ETF Price Quotes API. Track current prices, performance changes, and key data for a wide variety of ETFs.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-etf-quotes\n```\n\n---\n\n### Full Commodities Quotes API\n\nGet up-to-the-minute quotes for commodities with the FMP Real-Time Commodities Quotes API. Track the latest prices, changes, and volumes for a wide range of commodities, including oil, gold, and agricultural products.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-commodity-quotes\n```\n\n---\n\n### Full Cryptocurrency Quotes API\n\nAccess real-time cryptocurrency quotes with the FMP Full Cryptocurrency Quotes API. Track live prices, trading volumes, and price changes for a wide range of digital assets.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-crypto-quotes\n```\n\n---\n\n### Full Forex Quote API\n\nRetrieve real-time quotes for multiple forex currency pairs with the FMP Batch Forex Quote API. Get real-time price changes and updates for a variety of forex pairs in a single request.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-forex-quotes\n```\n\n---\n\n### Full Index Quotes API\n\nTrack real-time movements of major stock market indexes with the FMP Stock Market Index Quotes API. Access live quotes for global indexes and monitor changes in their performance.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-index-quotes\n```\n\n---\n\n\n## Statements\n\n### Income Statement API\n\nAccess detailed income statement data for publicly traded companies with the Income Statements API. Track profitability, compare competitors, and identify business trends with up-to-date financial data.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/income-statement?symbol=AAPL\n```\n\n---\n\n### Balance Sheet Statement API\n\nAccess detailed balance sheet statements for publicly traded companies with the Balance Sheet Data API. Analyze assets, liabilities, and shareholder equity to gain insights into a company's financial health.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/balance-sheet-statement?symbol=AAPL\n```\n\n---\n\n### Cash Flow Statement API\n\nGain insights into a company's cash flow activities with the Cash Flow Statements API. Analyze cash generated and used from operations, investments, and financing activities to evaluate the financial health and sustainability of a business.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/cash-flow-statement?symbol=AAPL\n```\n\n---\n\n### Latest Financial Statements API\n\n---\n\n### Income Statements TTM API\n\n---\n\n### Balance Sheet Statements TTM API\n\n---\n\n### Cashflow Statements TTM API\n\n---\n\n### Key Metrics API\n\nAccess essential financial metrics for a company with the FMP Financial Key Metrics API. Evaluate revenue, net income, P/E ratio, and more to assess performance and compare it to competitors.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/key-metrics?symbol=AAPL\n```\n\n---\n\n### Financial Ratios API\n\nAnalyze a company's financial performance using the Financial Ratios API. This API provides detailed profitability, liquidity, and efficiency ratios, enabling users to assess a company's operational and financial health across various metrics.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ratios?symbol=AAPL\n```\n\n---\n\n### Key Metrics TTM API\n\nRetrieve a comprehensive set of trailing twelve-month (TTM) key performance metrics with the TTM Key Metrics API. Access data related to a company's profitability, capital efficiency, and liquidity, allowing for detailed analysis of its financial health over the past year.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/key-metrics-ttm?symbol=AAPL\n```\n\n---\n\n### Financial Ratios TTM API\n\nGain access to trailing twelve-month (TTM) financial ratios with the TTM Ratios API. This API provides key performance metrics over the past year, including profitability, liquidity, and efficiency ratios.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ratios-ttm?symbol=AAPL\n```\n\n---\n\n### Financial Scores API\n\nAssess a company's financial strength using the Financial Health Scores API. This API provides key metrics such as the Altman Z-Score and Piotroski Score, giving users insights into a company’s overall financial health and stability.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/financial-scores?symbol=AAPL\n```\n\n---\n\n### Owner Earnings API\n\nRetrieve a company's owner earnings with the Owner Earnings API, which provides a more accurate representation of cash available to shareholders by adjusting net income. This metric is crucial for evaluating a company’s profitability from the perspective of investors.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/owner-earnings?symbol=AAPL\n```\n\n---\n\n### Enterprise Values API\n\nAccess a company's enterprise value using the Enterprise Values API. This metric offers a comprehensive view of a company's total market value by combining both its equity (market capitalization) and debt, providing a better understanding of its worth.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/enterprise-values?symbol=AAPL\n```\n\n---\n\n### Income Statement Growth API\n\nTrack key financial growth metrics with the Income Statement Growth API. Analyze how revenue, profits, and expenses have evolved over time, offering insights into a company’s financial health and operational efficiency.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/income-statement-growth?symbol=AAPL\n```\n\n---\n\n### Balance Sheet Statement Growth API\n\nAnalyze the growth of key balance sheet items over time with the Balance Sheet Statement Growth API. Track changes in assets, liabilities, and equity to understand the financial evolution of a company.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/balance-sheet-statement-growth?symbol=AAPL\n```\n\n---\n\n### Cashflow Statement Growth API\n\nMeasure the growth rate of a company’s cash flow with the FMP Cashflow Statement Growth API. Determine how quickly a company’s cash flow is increasing or decreasing over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/cash-flow-statement-growth?symbol=AAPL\n```\n\n---\n\n### Financial Statement Growth API\n\nAnalyze the growth of key financial statement items across income, balance sheet, and cash flow statements with the Financial Statement Growth API. Track changes over time to understand trends in financial performance.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/financial-growth?symbol=AAPL\n```\n\n---\n\n### Financial Reports Dates API\n\n---\n\n### Financial Reports Form 10-K JSON API\n\nAccess comprehensive annual reports with the FMP Annual Reports on Form 10-K API. Obtain detailed information about a company’s financial performance, business operations, and risk factors as reported to the SEC.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/financial-reports-json?symbol=AAPL&year=2022&period=FY\n```\n\n---\n\n### Financial Reports Form 10-K XLSX API\n\nDownload detailed 10-K reports in XLSX format with the Financial Reports Form 10-K XLSX API. Effortlessly access and analyze annual financial data for companies in a spreadsheet-friendly format.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/financial-reports-xlsx?symbol=AAPL&year=2022&period=FY\n```\n\n---\n\n### Revenue Product Segmentation API\n\nAccess detailed revenue breakdowns by product line with the Revenue Product Segmentation API. Understand which products drive a company's earnings and get insights into the performance of individual product segments.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/revenue-product-segmentation?symbol=AAPL\n```\n\n---\n\n### Revenue Geographic Segments API\n\nAccess detailed revenue breakdowns by geographic region with the Revenue Geographic Segments API. Analyze how different regions contribute to a company’s total revenue and identify key markets for growth.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/revenue-geographic-segmentation?symbol=AAPL\n```\n\n---\n\n### As Reported Income Statements API\n\nRetrieve income statements as they were reported by the company with the As Reported Income Statements API. Access raw financial data directly from official company filings, including revenue, expenses, and net income.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/income-statement-as-reported?symbol=AAPL\n```\n\n---\n\n### As Reported Balance Statements API\n\nAccess balance sheets as reported by the company with the As Reported Balance Statements API. View detailed financial data on assets, liabilities, and equity directly from official filings.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/balance-sheet-statement-as-reported?symbol=AAPL\n```\n\n---\n\n### As Reported Cashflow Statements API\n\nView cash flow statements as reported by the company with the As Reported Cash Flow Statements API. Analyze a company's cash flows related to operations, investments, and financing directly from official reports.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/cash-flow-statement-as-reported?symbol=AAPL\n```\n\n---\n\n### As Reported Financial Statements API\n\nRetrieve comprehensive financial statements as reported by companies with FMP As Reported Financial Statements API. Access complete data across income, balance sheet, and cash flow statements in their original form for detailed analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/financial-statement-full-as-reported?symbol=AAPL\n```\n\n---\n\n\n## Charts\n\n### Stock Chart Light API\n\nAccess simplified stock chart data using the FMP Basic Stock Chart API. This API provides essential charting information, including date, price, and trading volume, making it ideal for tracking stock performance with minimal data and creating basic price and volume charts.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/light?symbol=AAPL\n```\n\n---\n\n### Stock Price and Volume Data API\n\nAccess full price and volume data for any stock symbol using the FMP Comprehensive Stock Price and Volume Data API. Get detailed insights, including open, high, low, close prices, trading volume, price changes, percentage changes, and volume-weighted average price (VWAP).\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/full?symbol=AAPL\n```\n\n---\n\n### Unadjusted Stock Price API\n\nAccess stock price and volume data without adjustments for stock splits with the FMP Unadjusted Stock Price Chart API. Get accurate insights into stock performance, including open, high, low, and close prices, along with trading volume, without split-related changes.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/non-split-adjusted?symbol=AAPL\n```\n\n---\n\n### Dividend Adjusted Price Chart API\n\nAnalyze stock performance with dividend adjustments using the FMP Dividend-Adjusted Price Chart API. Access end-of-day price and volume data that accounts for dividend payouts, offering a more comprehensive view of stock trends over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/dividend-adjusted?symbol=AAPL\n```\n\n---\n\n### 1 Min Interval Stock Chart API\n\nAccess precise intraday stock price and volume data with the FMP 1-Minute Interval Stock Chart API. Retrieve real-time or historical stock data in 1-minute intervals, including key information such as open, high, low, and close prices, and trading volume for each minute.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1min?symbol=AAPL\n```\n\n---\n\n### 5 Min Interval Stock Chart API\n\nAccess stock price and volume data with the FMP 5-Minute Interval Stock Chart API. Retrieve detailed stock data in 5-minute intervals, including open, high, low, and close prices, along with trading volume for each 5-minute period. This API is perfect for short-term trading analysis and building intraday charts.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/5min?symbol=AAPL\n```\n\n---\n\n### 15 Min Interval Stock Chart API\n\nAccess stock price and volume data with the FMP 15-Minute Interval Stock Chart API. Retrieve detailed stock data in 15-minute intervals, including open, high, low, close prices, and trading volume. This API is ideal for creating intraday charts and analyzing medium-term price trends during the trading day.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/15min?symbol=AAPL\n```\n\n---\n\n### 30 Min Interval Stock Chart API\n\nAccess stock price and volume data with the FMP 30-Minute Interval Stock Chart API. Retrieve essential stock data in 30-minute intervals, including open, high, low, close prices, and trading volume. This API is perfect for creating intraday charts and tracking medium-term price movements for more strategic trading decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/30min?symbol=AAPL\n```\n\n---\n\n### 1 Hour Interval Stock Chart API\n\nTrack stock price movements over hourly intervals with the FMP 1-Hour Interval Stock Chart API. Access essential stock price and volume data, including open, high, low, and close prices for each hour, to analyze broader intraday trends with precision.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1hour?symbol=AAPL\n```\n\n---\n\n### 4 Hour Interval Stock Chart API\n\nAnalyze stock price movements over extended intraday periods with the FMP 4-Hour Interval Stock Chart API. Access key stock price and volume data in 4-hour intervals, perfect for tracking longer intraday trends and understanding broader market movements.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/4hour?symbol=AAPL\n```\n\n---\n\n\n## Economics\n\n### Treasury Rates API\n\nAccess latest and historical Treasury rates for all maturities with the FMP Treasury Rates API. Track key benchmarks for interest rates across the economy.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/treasury-rates\n```\n\n---\n\n### Economics Indicators API\n\nAccess real-time and historical economic data for key indicators like GDP, unemployment, and inflation with the FMP Economic Indicators API. Use this data to measure economic performance and identify growth trends.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/economic-indicators?name=GDP\n```\n\n---\n\n### Economic Data Releases Calendar API\n\nStay informed with the FMP Economic Data Releases Calendar API. Access a comprehensive calendar of upcoming economic data releases to prepare for market impacts and make informed investment decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/economic-calendar\n```\n\n---\n\n### Market Risk Premium API\n\nAccess the market risk premium for specific dates with the FMP Market Risk Premium API. Use this key financial metric to assess the additional return expected from investing in the stock market over a risk-free investment.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/market-risk-premium\n```\n\n---\n\n\n## Earnings, Dividends, Splits\n\n### Dividends Company API\n\nStay informed about upcoming dividend payments with the FMP Dividends Company API. This API provides essential dividend data for individual stock symbols, including record dates, payment dates, declaration dates, and more.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/dividends?symbol=AAPL\n```\n\n---\n\n### Dividends Calendar API\n\nStay informed on upcoming dividend events with the Dividend Events Calendar API. Access a comprehensive schedule of dividend-related dates for all stocks, including record dates, payment dates, declaration dates, and dividend yields.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/dividends-calendar\n```\n\n---\n\n### Earnings Report API\n\nRetrieve in-depth earnings information with the FMP Earnings Report API. Gain access to key financial data for a specific stock symbol, including earnings report dates, EPS estimates, and revenue projections to help you stay on top of company performance.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/earnings?symbol=AAPL\n```\n\n---\n\n### Earnings Calendar API\n\nStay informed on upcoming and past earnings announcements with the FMP Earnings Calendar API. Access key data, including announcement dates, estimated earnings per share (EPS), and actual EPS for publicly traded companies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/earnings-calendar\n```\n\n---\n\n### IPOs Calendar API\n\nAccess a comprehensive list of all upcoming initial public offerings (IPOs) with the FMP IPO Calendar API. Stay up to date on the latest companies entering the public market, with essential details on IPO dates, company names, expected pricing, and exchange listings.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ipos-calendar\n```\n\n---\n\n### IPOs Disclosure API\n\nAccess a comprehensive list of disclosure filings for upcoming initial public offerings (IPOs) with the FMP IPO Disclosures API. Stay updated on regulatory filings, including filing dates, effectiveness dates, CIK numbers, and form types, with direct links to official SEC documents.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ipos-disclosure\n```\n\n---\n\n### IPOs Prospectus API\n\nAccess comprehensive information on IPO prospectuses with the FMP IPO Prospectus API. Get key financial details, such as public offering prices, discounts, commissions, proceeds before expenses, and more. This API also provides links to official SEC prospectuses, helping investors stay informed on companies entering the public market.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ipos-prospectus\n```\n\n---\n\n### Stock Split Details API\n\nAccess detailed information on stock splits for a specific company using the FMP Stock Split Details API. This API provides essential data, including the split date and the split ratio, helping users understand changes in a company's share structure after a stock split.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/splits?symbol=AAPL\n```\n\n---\n\n### Stock Splits Calendar API\n\nStay informed about upcoming stock splits with the FMP Stock Splits Calendar API. This API provides essential data on upcoming stock splits across multiple companies, including the split date and ratio, helping you track changes in share structures before they occur.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/splits-calendar\n```\n\n---\n\n\n## Earnings Transcript\n\n### Latest Earning Transcripts API\n\nAccess available earnings transcripts for companies with the FMP Latest Earning Transcripts API. Retrieve a list of companies with earnings transcripts, along with the total number of transcripts available for each company.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/earning-call-transcript-latest\n```\n\n---\n\n### Earnings Transcript API\n\nAccess the full transcript of a company’s earnings call with the FMP Earnings Transcript API. Stay informed about a company’s financial performance, future plans, and overall strategy by analyzing management's communication.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/earning-call-transcript?symbol=AAPL&year=2020&quarter=3\n```\n\n---\n\n### Transcripts Dates By Symbol API\n\nAccess earnings call transcript dates for specific companies with the FMP Transcripts Dates By Symbol API. Get a comprehensive overview of earnings call schedules based on fiscal year and quarter.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/earning-call-transcript-dates?symbol=AAPL\n```\n\n---\n\n### Available Transcript Symbols API\n\nAccess a complete list of stock symbols with available earnings call transcripts using the FMP Available Earnings Transcript Symbols API. Retrieve information on which companies have earnings transcripts and how many are accessible for detailed financial analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/earnings-transcript-list\n```\n\n---\n\n\n## News\n\n### FMP Articles API\n\nAccess the latest articles from Financial Modeling Prep with the FMP Articles API. Get comprehensive updates including headlines, snippets, and publication URLs.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/fmp-articles?page=0&limit=20\n```\n\n---\n\n### General News API\n\nAccess the latest general news articles from a variety of sources with the FMP General News API. Obtain headlines, snippets, and publication URLs for comprehensive news coverage.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/general-latest?page=0&limit=20\n```\n\n---\n\n### Press Releases API\n\nAccess official company press releases with the FMP Press Releases API. Get real-time updates on corporate announcements, earnings reports, mergers, and more.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/press-releases-latest?page=0&limit=20\n```\n\n---\n\n### Stock News API\n\nStay informed with the latest stock market news using the FMP Stock News Feed API. Access headlines, snippets, publication URLs, and ticker symbols for the most recent articles from a variety of sources.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/stock-latest?page=0&limit=20\n```\n\n---\n\n### Crypto News API\n\nStay informed with the latest cryptocurrency news using the FMP Crypto News API. Access a curated list of articles from various sources, including headlines, snippets, and publication URLs.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/crypto-latest?page=0&limit=20\n```\n\n---\n\n### Forex News API\n\nStay updated with the latest forex news articles from various sources using the FMP Forex News API. Access headlines, snippets, and publication URLs for comprehensive market insights.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/forex-latest?page=0&limit=20\n```\n\n---\n\n### Search Press Releases API\n\nSearch for company press releases with the FMP Search Press Releases API. Find specific corporate announcements and updates by entering a stock symbol or company name.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/press-releases?symbols=AAPL\n```\n\n---\n\n### Search Stock News API\n\nSearch for stock-related news using the FMP Search Stock News API. Find specific stock news by entering a ticker symbol or company name to track the latest developments.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/stock?symbols=AAPL\n```\n\n---\n\n### Search Crypto News API\n\nSearch for cryptocurrency news using the FMP Search Crypto News API. Retrieve news related to specific coins or tokens by entering their name or symbol.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/crypto?symbols=BTCUSD\n```\n\n---\n\n### Search Forex News API\n\nSearch for foreign exchange news using the FMP Search Forex News API. Find targeted news on specific currency pairs by entering their symbols for focused updates.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/news/forex?symbols=EURUSD\n```\n\n---\n\n\n## Form 13F\n\n### Institutional Ownership Filings API\n\nStay up to date with the most recent SEC filings related to institutional ownership using the Institutional Ownership Filings API. This tool allows you to track the latest reports and disclosures from institutional investors, giving you a real-time view of major holdings and regulatory submissions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/latest?page=0&limit=100\n```\n\n---\n\n### Filings Extract API\n\nThe SEC Filings Extract API allows users to extract detailed data directly from official SEC filings. This API provides access to key information such as company shares, security details, and filing links, making it easier to analyze corporate disclosures.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/extract?cik=0001388838&year=2023&quarter=3\n```\n\n---\n\n### Form 13F Filings Dates API\n\nThe Form 13F Filings Dates API allows you to retrieve dates associated with Form 13F filings by institutional investors. This is crucial for tracking stock holdings of institutional investors at specific points in time, providing valuable insights into their investment strategies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/dates?cik=0001067983\n```\n\n---\n\n### Filings Extract With Analytics By Holder API\n\nThe Filings Extract With Analytics By Holder API provides an analytical breakdown of institutional filings. This API offers insight into stock movements, strategies, and portfolio changes by major institutional holders, helping you understand their investment behavior and track significant changes in stock ownership.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/extract-analytics/holder?symbol=AAPL&year=2023&quarter=3&page=0&limit=10\n```\n\n---\n\n### Holder Performance Summary API\n\nThe Holder Performance Summary API provides insights into the performance of institutional investors based on their stock holdings. This data helps track how well institutional holders are performing, their portfolio changes, and how their performance compares to benchmarks like the S&P 500.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/holder-performance-summary?cik=0001067983&page=0\n```\n\n---\n\n### Holders Industry Breakdown API\n\nThe Holders Industry Breakdown API provides an overview of the sectors and industries that institutional holders are investing in. This API helps analyze how institutional investors distribute their holdings across different industries and track changes in their investment strategies over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/holder-industry-breakdown?cik=0001067983&year=2023&quarter=3\n```\n\n---\n\n### Positions Summary API\n\nThe Positions Summary API provides a comprehensive snapshot of institutional holdings for a specific stock symbol. It tracks key metrics like the number of investors holding the stock, changes in the number of shares, total investment value, and ownership percentages over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/symbol-positions-summary?symbol=AAPL&year=2023&quarter=3\n```\n\n---\n\n### Industry Performance Summary API\n\nThe Industry Performance Summary API provides an overview of how various industries are performing financially. By analyzing the value of industries over a specific period, this API helps investors and analysts understand the health of entire sectors and make informed decisions about sector-based investments.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/industry-summary?year=2023&quarter=3\n```\n\n---\n\n\n## Analyst\n\n### Financial Estimates API\n\nRetrieve analyst financial estimates for stock symbols with the FMP Financial Estimates API. Access projected figures like revenue, earnings per share (EPS), and other key financial metrics as forecasted by industry analysts to inform your investment decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/analyst-estimates?symbol=AAPL&period=annual&page=0&limit=10\n```\n\n---\n\n### Ratings Snapshot API\n\nQuickly assess the financial health and performance of companies with the FMP Ratings Snapshot API. This API provides a comprehensive snapshot of financial ratings for stock symbols in our database, based on various key financial ratios.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ratings-snapshot?symbol=AAPL\n```\n\n---\n\n### Historical Ratings API\n\nTrack changes in financial performance over time with the FMP Historical Ratings API. This API provides access to historical financial ratings for stock symbols in our database, allowing users to view ratings and key financial metric scores for specific dates.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ratings-historical?symbol=AAPL\n```\n\n---\n\n### Price Target Summary API\n\nGain insights into analysts' expectations for stock prices with the FMP Price Target Summary API. This API provides access to average price targets from analysts across various timeframes, helping investors assess future stock performance based on expert opinions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/price-target-summary?symbol=AAPL\n```\n\n---\n\n### Price Target Consensus API\n\nAccess analysts' consensus price targets with the FMP Price Target Consensus API. This API provides high, low, median, and consensus price targets for stocks, offering investors a comprehensive view of market expectations for future stock prices.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/price-target-consensus?symbol=AAPL\n```\n\n---\n\n### Stock Grades API\n\nAccess the latest stock grades from top analysts and financial institutions with the FMP Grades API. Track grading actions, such as upgrades, downgrades, or maintained ratings, for specific stock symbols, providing valuable insight into how experts evaluate companies over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/grades?symbol=AAPL\n```\n\n---\n\n### Historical Stock Grades API\n\nAccess a comprehensive record of analyst grades with the FMP Historical Grades API. This tool allows you to track historical changes in analyst ratings for specific stock symbol\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/grades-historical?symbol=AAPL\n```\n\n---\n\n### Stock Grades Summary API\n\nQuickly access an overall view of analyst ratings with the FMP Grades Summary API. This API provides a consolidated summary of market sentiment for individual stock symbols, including the total number of strong buy, buy, hold, sell, and strong sell ratings. Understand the overall consensus on a stock’s outlook with just a few data points.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/grades-consensus?symbol=AAPL\n```\n\n---\n\n\n## Market Performance\n\n### Market Sector Performance Snapshot API\n\nGet a snapshot of sector performance using the Market Sector Performance Snapshot API. Analyze how different industries are performing in the market based on average changes across sectors.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sector-performance-snapshot?date=2024-02-01\n```\n\n---\n\n### Industry Performance Snapshot API\n\nAccess detailed performance data by industry using the Industry Performance Snapshot API. Analyze trends, movements, and daily performance metrics for specific industries across various stock exchanges.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/industry-performance-snapshot?date=2024-02-01\n```\n\n---\n\n### Historical Market Sector Performance API\n\nAccess historical sector performance data using the Historical Market Sector Performance API. Review how different sectors have performed over time across various stock exchanges.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-sector-performance?sector=Energy\n```\n\n---\n\n### Historical Industry Performance API\n\nAccess historical performance data for industries using the Historical Industry Performance API. Track long-term trends and analyze how different industries have evolved over time across various stock exchanges.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-industry-performance?industry=Biotechnology\n```\n\n---\n\n### Sector PE Snapshot API\n\nRetrieve the price-to-earnings (P/E) ratios for various sectors using the Sector P/E Snapshot API. Compare valuation levels across sectors to better understand market valuations.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sector-pe-snapshot?date=2024-02-01\n```\n\n---\n\n### Industry PE Snapshot API\n\nView price-to-earnings (P/E) ratios for different industries using the Industry P/E Snapshot API. Analyze valuation levels across various industries to understand how each is priced relative to its earnings.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/industry-pe-snapshot?date=2024-02-01\n```\n\n---\n\n### Historical Sector PE API\n\nAccess historical price-to-earnings (P/E) ratios for various sectors using the Historical Sector P/E API. Analyze how sector valuations have evolved over time to understand long-term trends and market shifts.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-sector-pe?sector=Energy\n```\n\n---\n\n### Historical Industry PE API\n\nAccess historical price-to-earnings (P/E) ratios by industry using the Historical Industry P/E API. Track valuation trends across various industries to understand how market sentiment and valuations have evolved over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-industry-pe?industry=Biotechnology\n```\n\n---\n\n### Biggest Stock Gainers API\n\nTrack the stocks with the largest price increases using the Top Stock Gainers API. Identify the companies that are leading the market with significant price surges, offering potential growth opportunities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/biggest-gainers\n```\n\n---\n\n### Biggest Stock Losers API\n\nAccess data on the stocks with the largest price drops using the Biggest Stock Losers API. Identify companies experiencing significant declines and track the stocks that are falling the fastest in the market.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/biggest-losers\n```\n\n---\n\n### Top Traded Stocks API\n\nView the most actively traded stocks using the Top Traded Stocks API. Identify the companies experiencing the highest trading volumes in the market and track where the most trading activity is happening.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/most-actives\n```\n\n---\n\n\n## Technical Indicators\n\n### Simple Moving Average API\n\n---\n\n### Exponential Moving Average API\n\n---\n\n### Weighted Moving Average API\n\n---\n\n### Double Exponential Moving Average API\n\n---\n\n### Triple Exponential Moving Average API\n\n---\n\n### Relative Strength Index API\n\n---\n\n### Standard Deviation API\n\n---\n\n### Williams API\n\n---\n\n### Average Directional Index API\n\n---\n\n\n## Etf And Mutual Funds\n\n### ETF & Fund Holdings API\n\nGet a detailed breakdown of the assets held within ETFs and mutual funds using the FMP ETF & Fund Holdings API. Access real-time data on the specific securities and their weights in the portfolio, providing insights into asset composition and fund strategies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/etf/holdings?symbol=SPY\n```\n\n---\n\n### ETF & Mutual Fund Information API\n\nAccess comprehensive data on ETFs and mutual funds with the FMP ETF & Mutual Fund Information API. Retrieve essential details such as ticker symbol, fund name, expense ratio, assets under management, and more.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/etf/info?symbol=SPY\n```\n\n---\n\n### ETF & Fund Country Allocation API\n\nGain insight into how ETFs and mutual funds distribute assets across different countries with the FMP ETF & Fund Country Allocation API. This tool provides detailed information on the percentage of assets allocated to various regions, helping you make informed investment decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/etf/country-weightings?symbol=SPY\n```\n\n---\n\n### ETF Asset Exposure API\n\nDiscover which ETFs hold specific stocks with the FMP ETF Asset Exposure API. Access detailed information on market value, share numbers, and weight percentages for assets within ETFs.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/etf/asset-exposure?symbol=AAPL\n```\n\n---\n\n### ETF Sector Weighting API\n\nThe FMP ETF Sector Weighting API provides a breakdown of the percentage of an ETF's assets that are invested in each sector. For example, an investor may want to invest in an ETF that has a high exposure to the technology sector if they believe that the technology sector is poised for growth.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/etf/sector-weightings?symbol=SPY\n```\n\n---\n\n### Mutual Fund & ETF Disclosure API\n\nAccess the latest disclosures from mutual funds and ETFs with the FMP Mutual Fund & ETF Disclosure API. This API provides updates on filings, changes in holdings, and other critical disclosure data for mutual funds and ETFs.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/funds/disclosure-holders-latest?symbol=AAPL\n```\n\n---\n\n### Mutual Fund Disclosures API\n\nAccess comprehensive disclosure data for mutual funds with the FMP Mutual Fund Disclosures API. Analyze recent filings, balance sheets, and financial reports to gain insights into mutual fund portfolios.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/funds/disclosure?symbol=VWO&year=2023&quarter=4\n```\n\n---\n\n### Mutual Fund & ETF Disclosure Name Search API\n\nEasily search for mutual fund and ETF disclosures by name using the Mutual Fund & ETF Disclosure Name Search API. This API allows you to find specific reports and filings based on the fund or ETF name, providing essential details like CIK number, entity information, and reporting file number.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/funds/disclosure-holders-search?name=Federated\n```\n\n---\n\n### Fund & ETF Disclosures by Date API\n\nRetrieve detailed disclosures for mutual funds and ETFs based on filing dates with the FMP Fund & ETF Disclosures by Date API. Stay current with the latest filings and track regulatory updates effectively.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/funds/disclosure-dates?symbol=VWO\n```\n\n---\n\n\n## Sec Filings\n\n### Latest 8-K SEC Filings API\n\nStay up-to-date with the most recent 8-K filings from publicly traded companies using the FMP Latest 8-K SEC Filings API. Get real-time access to significant company events such as mergers, acquisitions, leadership changes, and other material events that may impact the market.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-filings-8k?from=2024-01-01&to=2024-03-01&page=0&limit=100\n```\n\n---\n\n### Latest SEC Filings API\n\nStay updated with the most recent SEC filings from publicly traded companies using the FMP Latest SEC Filings API. Access essential regulatory documents, including financial statements, annual reports, 8-K, 10-K, and 10-Q forms.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-filings-financials?from=2024-01-01&to=2024-03-01&page=0&limit=100\n```\n\n---\n\n### SEC Filings By Form Type API\n\nSearch for specific SEC filings by form type with the FMP SEC Filings By Form Type API. Retrieve filings such as 10-K, 10-Q, 8-K, and others, filtered by the exact type of document you're looking for.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-filings-search/form-type?formType=8-K&from=2024-01-01&to=2024-03-01&page=0&limit=100\n```\n\n---\n\n### SEC Filings By Symbol API\n\nSearch and retrieve SEC filings by company symbol using the FMP SEC Filings By Symbol API. Gain direct access to regulatory filings such as 8-K, 10-K, and 10-Q reports for publicly traded companies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-filings-search/symbol?symbol=AAPL&from=2024-01-01&to=2024-03-01&page=0&limit=100\n```\n\n---\n\n### SEC Filings By CIK API\n\nSearch for SEC filings using the FMP SEC Filings By CIK API. Access detailed regulatory filings by Central Index Key (CIK) number, enabling you to track all filings related to a specific company or entity.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-filings-search/cik?cik=0000320193&from=2024-01-01&to=2024-03-01&page=0&limit=100\n```\n\n---\n\n### SEC Filings By Name API\n\nSearch for SEC filings by company or entity name using the FMP SEC Filings By Name API. Quickly retrieve official filings for any organization based on its name.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-filings-company-search/name?company=Berkshire\n```\n\n---\n\n### SEC Filings Company Search By Symbol API\n\nFind company information and regulatory filings using a stock symbol with the FMP SEC Filings Company Search By Symbol API. Quickly access essential company details based on stock ticker symbols.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-filings-company-search/symbol?symbol=AAPL\n```\n\n---\n\n### SEC Filings Company Search By CIK API\n\nEasily find company information using a CIK (Central Index Key) with the FMP SEC Filings Company Search By CIK API. Access essential company details and filings linked to a specific CIK number.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-filings-company-search/cik?cik=0000320193\n```\n\n---\n\n### SEC Company Full Profile API\n\nRetrieve detailed company profiles, including business descriptions, executive details, contact information, and financial data with the FMP SEC Company Full Profile API.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sec-profile?symbol=AAPL\n```\n\n---\n\n### Industry Classification List API\n\nRetrieve a comprehensive list of industry classifications, including Standard Industrial Classification (SIC) codes and industry titles with the FMP Industry Classification List API.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/standard-industrial-classification-list\n```\n\n---\n\n### Industry Classification Search API\n\nSearch and retrieve industry classification details for companies, including SIC codes, industry titles, and business information, with the FMP Industry Classification Search API.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/industry-classification-search\n```\n\n---\n\n### All Industry Classification API\n\nAccess comprehensive industry classification data for companies across all sectors with the FMP All Industry Classification API. Retrieve key details such as SIC codes, industry titles, and business contact information.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/all-industry-classification\n```\n\n---\n\n\n## Insider Trades\n\n### Latest Insider Trading API\n\nAccess the latest insider trading activity using the Latest Insider Trading API. Track which company insiders are buying or selling stocks and analyze their transactions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/insider-trading/latest?page=0&limit=100\n```\n\n---\n\n### Search Insider Trades API\n\nSearch insider trading activity by company or symbol using the Search Insider Trades API. Find specific trades made by corporate insiders, including executives and directors.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/insider-trading/search?page=0&limit=100\n```\n\n---\n\n### Search Insider Trades by Reporting Name API\n\nSearch for insider trading activity by reporting name using the Search Insider Trades by Reporting Name API. Track trading activities of specific individuals or groups involved in corporate insider transactions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/insider-trading/reporting-name?name=Zuckerberg\n```\n\n---\n\n### All Insider Transaction Types API\n\nAccess a comprehensive list of insider transaction types with the All Insider Transaction Types API. This API provides details on various transaction actions, including purchases, sales, and other corporate actions involving insider trading.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/insider-trading-transaction-type\n```\n\n---\n\n### Insider Trade Statistics API\n\nAnalyze insider trading activity with the Insider Trade Statistics API. This API provides key statistics on insider transactions, including total purchases, sales, and trends for specific companies or stock symbols.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/insider-trading/statistics?symbol=AAPL\n```\n\n---\n\n### Acquisition Ownership API\n\nTrack changes in stock ownership during acquisitions using the Acquisition Ownership API. This API provides detailed information on how mergers, takeovers, or beneficial ownership changes impact the stock ownership structure of a company.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/acquisition-of-beneficial-ownership?symbol=AAPL\n```\n\n---\n\n\n## Indexes\n\n### Stock Market Indexes List API\n\nRetrieve a comprehensive list of stock market indexes across global exchanges using the FMP Stock Market Indexes List API. This API provides essential information such as the symbol, name, exchange, and currency for each index, helping analysts and investors keep track of various market benchmarks.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/index-list\n```\n\n---\n\n### Index Quote API\n\nAccess real-time stock index quotes with the Stock Index Quote API. Stay updated with the latest price changes, daily highs and lows, volume, and other key metrics for major stock indices around the world.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote?symbol=^GSPC\n```\n\n---\n\n### Index Short Quote API\n\nAccess concise stock index quotes with the Stock Index Short Quote API. This API provides a snapshot of the current price, change, and volume for stock indexes, making it ideal for users who need a quick overview of market movements.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote-short?symbol=^GSPC\n```\n\n---\n\n### All Index Quotes API\n\nThe All Index Quotes API provides real-time quotes for a wide range of stock indexes, from major market benchmarks to niche indexes. This API allows users to track market performance across multiple indexes in a single request, giving them a broad view of the financial markets.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-index-quotes\n```\n\n---\n\n### Historical Index Light Chart API\n\nRetrieve end-of-day historical prices for stock indexes using the Historical Price Data API. This API provides essential data such as date, price, and volume, enabling detailed analysis of price movements over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/light?symbol=^GSPC\n```\n\n---\n\n### Historical Index Full Chart API\n\nAccess full historical end-of-day prices for stock indexes using the Detailed Historical Price Data API. This API provides comprehensive information, including open, high, low, close prices, volume, and additional metrics for detailed financial analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/full?symbol=^GSPC\n```\n\n---\n\n### 1-Minute Interval Index Price API\n\nRetrieve 1-minute interval intraday data for stock indexes using the Intraday 1-Minute Price Data API. This API provides granular price information, helping users track short-term price movements and trading volume within each minute.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1min?symbol=^GSPC\n```\n\n---\n\n### 5-Minute Interval Index Price API\n\nRetrieve 5-minute interval intraday price data for stock indexes using the Intraday 5-Minute Price Data API. This API provides crucial insights into price movements and trading volume within 5-minute windows, ideal for traders who require short-term data.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/5min?symbol=^GSPC\n```\n\n---\n\n### 1-Hour Interval Index Price API\n\nAccess 1-hour interval intraday data for stock indexes using the Intraday 1-Hour Price Data API. This API provides detailed price movements and volume within hourly intervals, making it ideal for tracking medium-term market trends during the trading day.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1hour?symbol=^GSPC\n```\n\n---\n\n### S&P 500 Index API\n\nAccess detailed data on the S&P 500 index using the S&P 500 Index API. Track the performance and key information of the companies that make up this major stock market index.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/sp500-constituent\n```\n\n---\n\n### Nasdaq Index API\n\nAccess comprehensive data for the Nasdaq index with the Nasdaq Index API. Monitor real-time movements and track the historical performance of companies listed on this prominent stock exchange.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/nasdaq-constituent\n```\n\n---\n\n### Dow Jones API\n\nAccess data on the Dow Jones Industrial Average using the Dow Jones API. Track current values, analyze trends, and get detailed information about the companies that make up this important stock index.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/dowjones-constituent\n```\n\n---\n\n### Historical S&P 500 API\n\nRetrieve historical data for the S&P 500 index using the Historical S&P 500 API. Analyze past changes in the index, including additions and removals of companies, to understand trends and performance over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-sp500-constituent\n```\n\n---\n\n### Historical Nasdaq API\n\nAccess historical data for the Nasdaq index using the Historical Nasdaq API. Analyze changes in the index composition and view how it has evolved over time, including company additions and removals.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-nasdaq-constituent\n```\n\n---\n\n### Historical Dow Jones API\n\nAccess historical data for the Dow Jones Industrial Average using the Historical Dow Jones API. Analyze changes in the index’s composition and study its performance across different periods.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-dowjones-constituent\n```\n\n---\n\n\n## Market Hours\n\n### Global Exchange Market Hours API\n\nRetrieve trading hours for specific stock exchanges using the Global Exchange Market Hours API. Find out the opening and closing times of global exchanges to plan your trading strategies effectively.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/exchange-market-hours?exchange=NASDAQ\n```\n\n---\n\n### Holidays By Exchange API\n\n---\n\n### All Exchange Market Hours API\n\nView the market hours for all exchanges. Check when different markets are active.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/all-exchange-market-hours\n```\n\n---\n\n\n## Commodity\n\n### Commodities List API\n\nAccess an extensive list of tracked commodities across various sectors, including energy, metals, and agricultural products. The FMP Commodities List API provides essential data on tradable commodities, giving investors the ability to explore market options in real-time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/commodities-list\n```\n\n---\n\n### Commodities Quote API\n\nAccess real-time price quotes for all commodities traded worldwide with the FMP Global Commodities Quotes API. Track market movements and identify investment opportunities with comprehensive price data.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote?symbol=GCUSD\n```\n\n---\n\n### Commodities Quote Short API\n\nGet fast and accurate quotes for commodities with the FMP Commodities Quick Quote API. Instantly access the current price, recent changes, and trading volume for various commodities in real-time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote-short?symbol=GCUSD\n```\n\n---\n\n### All Commodities Quotes API\n\nAccess real-time quotes for multiple commodities at once with the FMP Real-Time Batch Commodities Quotes API. Instantly track price changes, volume, and other key metrics for a broad range of commodities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-commodity-quotes\n```\n\n---\n\n### Light Chart API\n\nAccess historical end-of-day prices for various commodities with the FMP Historical Commodities Price API. Analyze past price movements, trading volume, and trends to support informed decision-making.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/light?symbol=GCUSD\n```\n\n---\n\n### Full Chart API\n\nAccess full historical end-of-day price data for commodities with the FMP Comprehensive Commodities Price API. This API enables users to analyze long-term price trends, patterns, and market movements in great detail.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/full?symbol=GCUSD\n```\n\n---\n\n### 1-Minute Interval Commodities Chart API\n\nTrack real-time, short-term price movements for commodities with the FMP 1-Minute Interval Commodities Chart API. This API provides detailed 1-minute interval data, enabling precise monitoring of intraday market changes.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1min?symbol=GCUSD\n```\n\n---\n\n### 5-Minute Interval Commodities Chart API\n\nMonitor short-term price movements with the FMP 5-Minute Interval Commodities Chart API. This API provides detailed 5-minute interval data, enabling users to track near-term price trends for more strategic trading and investment decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/5min?symbol=GCUSD\n```\n\n---\n\n### 1-Hour Interval Commodities Chart API\n\nMonitor hourly price movements and trends with the FMP 1-Hour Interval Commodities Chart API. This API provides hourly data, offering a detailed look at price fluctuations throughout the trading day to support mid-term trading strategies and market analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1hour?symbol=GCUSD\n```\n\n---\n\n\n## Discounted Cash Flow\n\n### DCF Valuation API\n\nEstimate the intrinsic value of a company with the FMP Discounted Cash Flow Valuation API. Calculate the DCF valuation based on expected future cash flows and discount rates.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/discounted-cash-flow?symbol=AAPL\n```\n\n---\n\n### Levered DCF API\n\nAnalyze a company’s value with the FMP Levered Discounted Cash Flow (DCF) API, which incorporates the impact of debt. This API provides post-debt company valuation, offering investors a more accurate measure of a company's true worth by accounting for its debt obligations.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/levered-discounted-cash-flow?symbol=AAPL\n```\n\n---\n\n### Custom DCF Advanced API\n\nRun a tailored Discounted Cash Flow (DCF) analysis using the FMP Custom DCF Advanced API. With detailed inputs, this API allows users to fine-tune their assumptions and variables, offering a more personalized and precise valuation for a company.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/custom-discounted-cash-flow?symbol=AAPL\n```\n\n---\n\n### Custom DCF Levered API\n\nRun a tailored Discounted Cash Flow (DCF) analysis using the FMP Custom DCF Advanced API. With detailed inputs, this API allows users to fine-tune their assumptions and variables, offering a more personalized and precise valuation for a company.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/custom-levered-discounted-cash-flow?symbol=AAPL\n```\n\n---\n\n\n## Forex\n\n### Forex Currency Pairs API\n\nAccess a comprehensive list of all currency pairs traded on the forex market with the FMP Forex Currency Pairs API. Analyze and track the performance of currency pairs to make informed investment decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/forex-list\n```\n\n---\n\n### Forex Quote API\n\nAccess real-time forex quotes for currency pairs with the Forex Quote API. Retrieve up-to-date information on exchange rates and price changes to help monitor market movements.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote?symbol=EURUSD\n```\n\n---\n\n### Forex Short Quote API\n\nQuickly access concise forex pair quotes with the Forex Quote Snapshot API. Get a fast look at live currency exchange rates, price changes, and volume in real time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote-short?symbol=EURUSD\n```\n\n---\n\n### Batch Forex Quotes API\n\nEasily access real-time quotes for multiple forex pairs simultaneously with the Batch Forex Quotes API. Stay updated on global currency exchange rates and monitor price changes across different markets.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-forex-quotes\n```\n\n---\n\n### Historical Forex Light Chart API\n\nAccess historical end-of-day forex prices with the Historical Forex Light Chart API. Track long-term price trends across different currency pairs to enhance your trading and analysis strategies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/light?symbol=EURUSD\n```\n\n---\n\n### Historical Forex Full Chart API\n\nAccess comprehensive historical end-of-day forex price data with the Full Historical Forex Chart API. Gain detailed insights into currency pair movements, including open, high, low, close (OHLC) prices, volume, and percentage changes.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/full?symbol=EURUSD\n```\n\n---\n\n### 1-Minute Interval Forex Chart API\n\nAccess real-time 1-minute intraday forex data with the 1-Minute Forex Interval Chart API. Track short-term price movements for precise, up-to-the-minute insights on currency pair fluctuations.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1min?symbol=EURUSD\n```\n\n---\n\n### 5-Minute Interval Forex Chart API\n\nTrack short-term forex trends with the 5-Minute Forex Interval Chart API. Access detailed 5-minute intraday data to monitor currency pair price movements and market conditions in near real-time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/5min?symbol=EURUSD\n```\n\n---\n\n### 1-Hour Interval Forex Chart API\n\nTrack forex price movements over the trading day with the 1-Hour Forex Interval Chart API. This tool provides hourly intraday data for currency pairs, giving a detailed view of trends and market shifts.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1hour?symbol=EURUSD\n```\n\n---\n\n\n## Crypto\n\n### Cryptocurrency List API\n\nAccess a comprehensive list of all cryptocurrencies traded on exchanges worldwide with the FMP Cryptocurrencies Overview API. Get detailed information on each cryptocurrency to inform your investment strategies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/cryptocurrency-list\n```\n\n---\n\n### Full Cryptocurrency Quote API\n\nAccess real-time quotes for all cryptocurrencies with the FMP Full Cryptocurrency Quote API. Obtain comprehensive price data including current, high, low, and open prices.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote?symbol=BTCUSD\n```\n\n---\n\n### Cryptocurrency Quote Short API\n\nAccess real-time cryptocurrency quotes with the FMP Cryptocurrency Quick Quote API. Get a concise overview of current crypto prices, changes, and trading volume for a wide range of digital assets.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/quote-short?symbol=BTCUSD\n```\n\n---\n\n### All Cryptocurrencies Quotes API\n\nAccess live price data for a wide range of cryptocurrencies with the FMP Real-Time Cryptocurrency Batch Quotes API. Get real-time updates on prices, market changes, and trading volumes for digital assets in a single request.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/batch-crypto-quotes\n```\n\n---\n\n### Historical Cryptocurrency Light Chart API\n\nAccess historical end-of-day prices for a variety of cryptocurrencies with the Historical Cryptocurrency Price Snapshot API. Track trends in price and trading volume over time to better understand market behavior.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/light?symbol=BTCUSD\n```\n\n---\n\n### Historical Cryptocurrency Full Chart API\n\nAccess comprehensive end-of-day (EOD) price data for cryptocurrencies with the Full Historical Cryptocurrency Data API. Analyze long-term price trends, market movements, and trading volumes to inform strategic decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-price-eod/full?symbol=BTCUSD\n```\n\n---\n\n### 1-Minute Interval Cryptocurrency Data API\n\nGet real-time, 1-minute interval price data for cryptocurrencies with the 1-Minute Cryptocurrency Intraday Data API. Monitor short-term price fluctuations and trading volume to stay updated on market movements.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1min?symbol=BTCUSD\n```\n\n---\n\n### 5-Minute Interval Cryptocurrency Data API\n\nAnalyze short-term price trends with the 5-Minute Interval Cryptocurrency Data API. Access real-time, intraday price data for cryptocurrencies to monitor rapid market movements and optimize trading strategies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/5min?symbol=BTCUSD\n```\n\n---\n\n### 1-Hour Interval Cryptocurrency Data API\n\nAccess detailed 1-hour intraday price data for cryptocurrencies with the 1-Hour Interval Cryptocurrency Data API. Track hourly price movements to gain insights into market trends and make informed trading decisions throughout the day.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/historical-chart/1hour?symbol=BTCUSD\n```\n\n---\n\n\n## Senate\n\n### Latest Senate Financial Disclosures API\n\nAccess the latest financial disclosures from U.S. Senate members with the FMP Latest Senate Financial Disclosures API. Track recent trades, asset ownership, and transaction details for enhanced transparency in government financial activities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/senate-latest?page=0&limit=100\n```\n\n---\n\n### Latest House Financial Disclosures API\n\nAccess real-time financial disclosures from U.S. House members with the FMP Latest House Financial Disclosures API. Track recent trades, asset ownership, and financial holdings for enhanced visibility into political figures' financial activities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/house-latest?page=0&limit=100\n```\n\n---\n\n### Senate Trading Activity API\n\nMonitor the trading activity of US Senators with the FMP Senate Trading Activity API. Access detailed information on trades made by Senators, including trade dates, assets, amounts, and potential conflicts of interest.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/senate-trades?symbol=AAPL\n```\n\n---\n\n### Senate Trades By Name API\n\n---\n\n### U.S. House Trades API\n\nTrack the financial trades made by U.S. House members and their families with the FMP U.S. House Trades API. Access real-time information on stock sales, purchases, and other investment activities to gain insight into their financial decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/house-trades?symbol=AAPL\n```\n\n---\n\n### House Trades By Name API\n\n---\n\n\n## ESG\n\n### ESG Investment Search API\n\nAlign your investments with your values using the FMP ESG Investment Search API. Discover companies and funds based on Environmental, Social, and Governance (ESG) scores, performance, controversies, and business involvement criteria.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/esg-disclosures?symbol=AAPL\n```\n\n---\n\n### ESG Ratings API\n\nAccess comprehensive ESG ratings for companies and funds with the FMP ESG Ratings API. Make informed investment decisions based on environmental, social, and governance (ESG) performance data.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/esg-ratings?symbol=AAPL\n```\n\n---\n\n### ESG Benchmark Comparison API\n\nEvaluate the ESG performance of companies and funds with the FMP ESG Benchmark Comparison API. Compare ESG leaders and laggards within industries to make informed and responsible investment decisions.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/esg-benchmark\n```\n\n---\n\n\n## Commitment Of Traders\n\n### COT Report API\n\nAccess comprehensive Commitment of Traders (COT) reports with the FMP COT Report API. This API provides detailed information about long and short positions across various sectors, helping you assess market sentiment and track positions in commodities, indices, and financial instruments.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/commitment-of-traders-report\n```\n\n---\n\n### COT Analysis By Dates API\n\nGain in-depth insights into market sentiment with the FMP COT Report Analysis API. Analyze the Commitment of Traders (COT) reports for a specific date range to evaluate market dynamics, sentiment, and potential reversals across various sectors.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/commitment-of-traders-analysis\n```\n\n---\n\n### COT Report List API\n\nAccess a comprehensive list of available Commitment of Traders (COT) reports by commodity or futures contract using the FMP COT Report List API. This API provides an overview of different market segments, allowing users to retrieve and explore COT reports for a wide variety of commodities and financial instruments.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/commitment-of-traders-list\n```\n\n---\n\n\n## Fundraisers\n\n### Latest Crowdfunding Campaigns API\n\nDiscover the most recent crowdfunding campaigns with the FMP Latest Crowdfunding Campaigns API. Stay informed on which companies and projects are actively raising funds, their financial details, and offering terms.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/crowdfunding-offerings-latest?page=0&limit=100\n```\n\n---\n\n### Crowdfunding Campaign Search API\n\nSearch for crowdfunding campaigns by company name, campaign name, or platform with the FMP Crowdfunding Campaign Search API. Access detailed information to track and analyze crowdfunding activities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/crowdfunding-offerings-search?name=enotap\n```\n\n---\n\n### Crowdfunding By CIK API\n\nAccess detailed information on all crowdfunding campaigns launched by a specific company with the FMP Crowdfunding By CIK API.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/crowdfunding-offerings?cik=0001916078\n```\n\n---\n\n### Equity Offering Updates API\n\nStay informed about the latest equity offerings with the FMP Equity Offering Updates API. Track new shares being issued by companies and get insights into exempt offerings and amendments.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/fundraising-latest?page=0&limit=10\n```\n\n---\n\n### Equity Offering Search API\n\nEasily search for equity offerings by company name or stock symbol with the FMP Equity Offering Search API. Access detailed information about recent share issuances to stay informed on company fundraising activities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/fundraising-search?name=NJOY\n```\n\n---\n\n### Equity Offering By CIK API\n\nAccess detailed information on equity offerings announced by specific companies with the FMP Company Equity Offerings by CIK API. Track offering activity and identify potential investment opportunities.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/fundraising?cik=0001547416\n```\n\n---\n\n\n## Bulk\n\n### Company Profile Bulk API\n\nThe FMP Profile Bulk API allows users to retrieve comprehensive company profile data in bulk. Access essential information, such as company details, stock price, market cap, sector, industry, and more for multiple companies in a single request.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/profile-bulk?part=0\n```\n\n---\n\n### Stock Rating Bulk API\n\nThe FMP Rating Bulk API provides users with comprehensive rating data for multiple stocks in a single request. Retrieve key financial ratings and recommendations such as overall ratings, DCF recommendations, and more for multiple companies at once.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/rating-bulk\n```\n\n---\n\n### DCF Valuations Bulk API\n\nThe FMP DCF Bulk API enables users to quickly retrieve discounted cash flow (DCF) valuations for multiple symbols in one request. Access the implied price movement and percentage differences for all listed companies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/dcf-bulk\n```\n\n---\n\n### Financial Scores Bulk API\n\nThe FMP Scores Bulk API allows users to quickly retrieve a wide range of key financial scores and metrics for multiple symbols. These scores provide valuable insights into company performance, financial health, and operational efficiency.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/scores-bulk\n```\n\n---\n\n### Price Target Summary Bulk API\n\nThe Price Target Summary Bulk API provides a comprehensive overview of price targets for all listed symbols over multiple timeframes. With this API, users can quickly retrieve price target data, helping investors and analysts compare current prices to projected targets across different periods.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/price-target-summary-bulk\n```\n\n---\n\n### ETF Holder Bulk API\n\nThe ETF Holder Bulk API allows users to quickly retrieve detailed information about the assets and shares held by Exchange-Traded Funds (ETFs). This API provides insights into the weight each asset carries within the ETF, along with key financial information related to these holdings.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/etf-holder-bulk?part=1\n```\n\n---\n\n### Upgrades Downgrades Consensus Bulk API\n\nThe Upgrades Downgrades Consensus Bulk API provides a comprehensive view of analyst ratings across all symbols. Retrieve bulk data for analyst upgrades, downgrades, and consensus recommendations to gain insights into the market's outlook on individual stocks.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/upgrades-downgrades-consensus-bulk\n```\n\n---\n\n### Key Metrics TTM Bulk API\n\nThe Key Metrics TTM Bulk API allows users to retrieve trailing twelve months (TTM) data for all companies available in the database. The API provides critical financial ratios and metrics based on each company’s latest financial report, offering insights into company performance and financial health.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/key-metrics-ttm-bulk\n```\n\n---\n\n### Ratios TTM Bulk API\n\nThe Ratios TTM Bulk API offers an efficient way to retrieve trailing twelve months (TTM) financial ratios for stocks. It provides users with detailed insights into a company’s profitability, liquidity, efficiency, leverage, and valuation ratios, all based on the most recent financial report.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/ratios-ttm-bulk\n```\n\n---\n\n### Stock Peers Bulk API\n\nThe Stock Peers Bulk API allows you to quickly retrieve a comprehensive list of peer companies for all stocks in the database. By accessing this data, you can easily compare a stock’s performance with its closest competitors or similar companies within the same industry or sector.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/peers-bulk\n```\n\n---\n\n### Earnings Surprises Bulk API\n\nThe Earnings Surprises Bulk API allows users to retrieve bulk data on annual earnings surprises, enabling quick analysis of which companies have beaten, missed, or met their earnings estimates. This API provides actual versus estimated earnings per share (EPS) for multiple companies at once, offering valuable insights for investors and analysts.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/earnings-surprises-bulk?year=2025\n```\n\n---\n\n### Income Statement Bulk API\n\nThe Bulk Income Statement API allows users to retrieve detailed income statement data in bulk. This API is designed for large-scale data analysis, providing comprehensive insights into a company's financial performance, including revenue, gross profit, expenses, and net income.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/income-statement-bulk?year=2025&period=Q1\n```\n\n---\n\n### Income Statement Growth Bulk API\n\nThe Bulk Income Statement Growth API provides access to growth data for income statements across multiple companies. Track and analyze growth trends over time for key financial metrics such as revenue, net income, and operating income, enabling a better understanding of corporate performance trends.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/income-statement-growth-bulk?year=2025&period=Q1\n```\n\n---\n\n### Balance Sheet Statement Bulk API\n\nThe Bulk Balance Sheet Statement API provides comprehensive access to balance sheet data across multiple companies. It enables users to analyze financial positions by retrieving key figures such as total assets, liabilities, and equity. Ideal for comparing the financial health and stability of different companies on a large scale.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/balance-sheet-statement-bulk?year=2025&period=Q1\n```\n\n---\n\n### Balance Sheet Statement Growth Bulk API\n\nThe Balance Sheet Growth Bulk API allows users to retrieve growth data across multiple companies’ balance sheets, enabling detailed analysis of how financial positions have changed over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/balance-sheet-statement-growth-bulk?year=2025&period=Q1\n```\n\n---\n\n### Cash Flow Statement Bulk API\n\nThe Cash Flow Statement Bulk API provides access to detailed cash flow reports for a wide range of companies. This API enables users to retrieve bulk cash flow statement data, helping to analyze companies’ operating, investing, and financing activities over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/cash-flow-statement-bulk?year=2025&period=Q1\n```\n\n---\n\n### Cash Flow Statement Growth Bulk API\n\nThe Cash Flow Statement Growth Bulk API allows you to retrieve bulk growth data for cash flow statements, enabling you to track changes in cash flows over time. This API is ideal for analyzing the cash flow growth trends of multiple companies simultaneously.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/cash-flow-statement-growth-bulk?year=2025&period=Q1\n```\n\n---\n\n### Eod Bulk API\n\nThe EOD Bulk API allows users to retrieve end-of-day stock price data for multiple symbols in bulk. This API is ideal for financial analysts, traders, and investors who need to assess valuations for a large number of companies.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/eod-bulk?date=2024-10-22\n```\n\n---\n"
  rawContent: ""
  suggestedFilename: "stable"
---

# Free Stock Market API and Financial Statements API

## 源URL

https://site.financialmodelingprep.com/developer/docs/stable

## 描述

FMP is your source for the most reliable and accurate Stock Market API and Financial Data API available. Whether you're looking for real-time stock prices, financial statements, or historical data, we offer a comprehensive solution to meet all your financial data needs.

## 文档正文

FMP is your source for the most reliable and accurate Stock Market API and Financial Data API available. Whether you're looking for real-time stock prices, financial statements, or historical data, we offer a comprehensive solution to meet all your financial data needs.

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"name": "Apple Inc.",
		"currency": "USD",
		"exchangeFullName": "NASDAQ Global Select",
		"exchange": "NASDAQ"
	}
]
```

#### Authorization

All API requests must be authorized using an API key. Authorization can be done using either request headers or URL query parameters.

Header Authorization

URL Query Authorization

Note: When adding the API key to your requests, ensure to use &apikey= if other query parameters already exist in the endpoint.

## Company Search

### Stock Symbol Search API

Easily find the ticker symbol of any stock with the FMP Stock Symbol Search API. Search by symbol across multiple global markets.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/search-symbol?query=AAPL
```

---

### Company Name Search API

Search for ticker symbols, company names, and exchange details for equity securities and ETFs listed on various exchanges with the FMP Name Search API. This endpoint is useful for retrieving ticker symbols when you know the full or partial company or asset name but not the symbol identifier.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/search-name?query=AA
```

---

### CIK API

Easily retrieve the Central Index Key (CIK) for publicly traded companies with the FMP CIK API. Access unique identifiers needed for SEC filings and regulatory documents for a streamlined compliance and financial analysis process.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/search-cik?cik=320193
```

---

### CUSIP API

Easily search and retrieve financial securities information by CUSIP number using the FMP CUSIP API. Find key details such as company name, stock symbol, and market capitalization associated with the CUSIP.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/search-cusip?cusip=037833100
```

---

### ISIN API

Easily search and retrieve the International Securities Identification Number (ISIN) for financial securities using the FMP ISIN API. Find key details such as company name, stock symbol, and market capitalization associated with the ISIN.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/search-isin?isin=US0378331005
```

---

### Stock Screener API

Discover stocks that align with your investment strategy using the FMP Stock Screener API. Filter stocks based on market cap, price, volume, beta, sector, country, and more to identify the best opportunities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/company-screener
```

---

### Exchange Variants API

Search across multiple public exchanges to find where a given stock symbol is listed using the FMP Exchange Variants API. This allows users to quickly identify all the exchanges where a security is actively traded.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/search-exchange-variants?symbol=AAPL
```

---

## Stock Directory

### Company Symbols List API

Easily retrieve a comprehensive list of financial symbols with the FMP Company Symbols List API. Access a broad range of stock symbols and other tradable financial instruments from various global exchanges, helping you explore the full range of available securities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/stock-list
```

---

### Financial Statement Symbols List API

Access a comprehensive list of companies with available financial statements through the FMP Financial Statement Symbols List API. Find companies listed on major global exchanges and obtain up-to-date financial data including income statements, balance sheets, and cash flow statements, are provided.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/financial-statement-symbol-list
```

---

### CIK List API

Access a comprehensive database of CIK (Central Index Key) numbers for SEC-registered entities with the FMP CIK List API. This endpoint is essential for businesses, financial professionals, and individuals who need quick access to CIK numbers for regulatory compliance, financial transactions, and investment research.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/cik-list?page=0&limit=1000
```

---

### Symbol Changes List API

Stay informed about the latest stock symbol changes with the FMP Stock Symbol Changes API. Track changes due to mergers, acquisitions, stock splits, and name changes to ensure accurate trading and analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/symbol-change
```

---

### ETF Symbol Search API

Quickly find ticker symbols and company names for Exchange Traded Funds (ETFs) using the FMP ETF Symbol Search API. This tool simplifies identifying specific ETFs by their name or ticker.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/etf-list
```

---

### Actively Trading List API

List all actively trading companies and financial instruments with the FMP Actively Trading List API. This endpoint allows users to filter and display securities that are currently being traded on public exchanges, ensuring you access real-time market activity.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/actively-trading-list
```

---

### Earnings Transcript List API

Access available earnings transcripts for companies with the FMP Earnings Transcript List API. Retrieve a list of companies with earnings transcripts, along with the total number of transcripts available for each company.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/earnings-transcript-list
```

---

### Available Exchanges API

Access a complete list of supported stock exchanges using the FMP Available Exchanges API. This API provides a comprehensive overview of global stock exchanges, allowing users to identify where securities are traded and filter data by specific exchanges for further analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/available-exchanges
```

---

### Available Sectors API

Access a complete list of industry sectors using the FMP Available Sectors API. This API helps users categorize and filter companies based on their respective sectors, enabling deeper analysis and more focused queries across different industries.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/available-sectors
```

---

### Available Industries API

Access a comprehensive list of industries where stock symbols are available using the FMP Available Industries API. This API helps users filter and categorize companies based on their industry for more focused research and analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/available-industries
```

---

### Available Countries API

Access a comprehensive list of countries where stock symbols are available with the FMP Available Countries API. This API enables users to filter and analyze stock symbols based on the country of origin or the primary market where the securities are traded.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/available-countries
```

---

## Company Information

### Company Profile Data API

Access detailed company profile data with the FMP Company Profile Data API. This API provides key financial and operational information for a specific stock symbol, including the company's market capitalization, stock price, industry, and much more.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/profile?symbol=AAPL
```

---

### Company Profile by CIK API

Retrieve detailed company profile data by CIK (Central Index Key) with the FMP Company Profile by CIK API. This API allows users to search for companies using their unique CIK identifier and access a full range of company data, including stock price, market capitalization, industry, and much more.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/profile-cik?cik=320193
```

---

### Company Notes API

Retrieve detailed information about company-issued notes with the FMP Company Notes API. Access essential data such as CIK number, stock symbol, note title, and the exchange where the notes are listed.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/company-notes?symbol=AAPL
```

---

### Stock Peer Comparison API

Identify and compare companies within the same sector and market capitalization range using the FMP Stock Peer Comparison API. Gain insights into how a company stacks up against its peers on the same exchange.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/stock-peers?symbol=AAPL
```

---

### Delisted Companies API

Stay informed with the FMP Delisted Companies API. Access a comprehensive list of companies that have been delisted from US exchanges to avoid trading in risky stocks and identify potential financial troubles.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/delisted-companies?page=0&limit=100
```

---

### Company Employee Count API

Retrieve detailed workforce information for companies, including employee count, reporting period, and filing date. The FMP Company Employee Count API also provides direct links to official SEC documents for further verification and in-depth research.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/employee-count?symbol=AAPL
```

---

### Company Historical Employee Count API

Access historical employee count data for a company based on specific reporting periods. The FMP Company Historical Employee Count API provides insights into how a company’s workforce has evolved over time, allowing users to analyze growth trends and operational changes.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-employee-count?symbol=AAPL
```

---

### Company Market Cap API

Retrieve the market capitalization for a specific company on any given date using the FMP Company Market Capitalization API. This API provides essential data to assess the size and value of a company in the stock market, helping users gauge its overall market standing.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/market-capitalization?symbol=AAPL
```

---

### Batch Market Cap API

Retrieve market capitalization data for multiple companies in a single request with the FMP Batch Market Capitalization API. This API allows users to compare the market size of various companies simultaneously, streamlining the analysis of company valuations.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/market-capitalization-batch?symbols=AAPL,MSFT,GOOG
```

---

### Historical Market Cap API

Access historical market capitalization data for a company using the FMP Historical Market Capitalization API. This API helps track the changes in market value over time, enabling long-term assessments of a company's growth or decline.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-market-capitalization?symbol=AAPL
```

---

### Company Share Float & Liquidity API

Understand the liquidity and volatility of a stock with the FMP Company Share Float and Liquidity API. Access the total number of publicly traded shares for any company to make informed investment decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/shares-float?symbol=AAPL
```

---

### All Shares Float API

Access comprehensive shares float data for all available companies with the FMP All Shares Float API. Retrieve critical information such as free float, float shares, and outstanding shares to analyze liquidity across a wide range of companies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/shares-float-all?page=0&limit=1000
```

---

### Latest Mergers & Acquisitions API

Access real-time data on the latest mergers and acquisitions with the FMP Latest Mergers and Acquisitions API. This API provides key information such as the transaction date, company names, and links to detailed filing information for further analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/mergers-acquisitions-latest?page=0&limit=100
```

---

### Search Mergers & Acquisitions API

Search for specific mergers and acquisitions data with the FMP Search Mergers and Acquisitions API. Retrieve detailed information on M&A activity, including acquiring and targeted companies, transaction dates, and links to official SEC filings.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/mergers-acquisitions-search?name=Apple
```

---

### Company Executives API

Retrieve detailed information on company executives with the FMP Company Executives API. This API provides essential data about key executives, including their name, title, compensation, and other demographic details such as gender and year of birth.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/key-executives?symbol=AAPL
```

---

### Executive Compensation API

Retrieve comprehensive compensation data for company executives with the FMP Executive Compensation API. This API provides detailed information on salaries, stock awards, total compensation, and other relevant financial data, including filing details and links to official documents.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/governance-executive-compensation?symbol=AAPL
```

---

### Executive Compensation Benchmark API

Gain access to average executive compensation data across various industries with the FMP Executive Compensation Benchmark API. This API provides essential insights for comparing executive pay by industry, helping you understand compensation trends and benchmarks.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/executive-compensation-benchmark
```

---

## Quote

### Stock Quote API

Access real-time stock quotes with the FMP Stock Quote API. Get up-to-the-minute prices, changes, and volume data for individual stocks.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote?symbol=AAPL
```

---

### Stock Quote Short API

Get quick snapshots of real-time stock quotes with the FMP Stock Quote Short API. Access key stock data like current price, volume, and price changes for instant market insights.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote-short?symbol=AAPL
```

---

### Aftermarket Trade API

Track real-time trading activity occurring after regular market hours with the FMP Aftermarket Trade API. Access key details such as trade prices, sizes, and timestamps for trades executed during the post-market session.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/aftermarket-trade?symbol=AAPL
```

---

### Aftermarket Quote API

Access real-time aftermarket quotes for stocks with the FMP Aftermarket Quote API. Track bid and ask prices, volume, and other relevant data outside of regular trading hours.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/aftermarket-quote?symbol=AAPL
```

---

### Stock Price Change API

Track stock price fluctuations in real-time with the FMP Stock Price Change API. Monitor percentage and value changes over various time periods, including daily, weekly, monthly, and long-term.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/stock-price-change?symbol=AAPL
```

---

### Stock Batch Quote API

Retrieve multiple real-time stock quotes in a single request with the FMP Stock Batch Quote API. Access current prices, volume, and detailed data for multiple companies at once, making it easier to track large portfolios or monitor multiple stocks simultaneously.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-quote?symbols=AAPL
```

---

### Stock Batch Quote Short API

Access real-time, short-form quotes for multiple stocks with the FMP Stock Batch Quote Short API. Get a quick snapshot of key stock data such as current price, change, and volume for several companies in one streamlined request.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-quote-short?symbols=AAPL
```

---

### Batch Aftermarket Trade API

Retrieve real-time aftermarket trading data for multiple stocks with the FMP Batch Aftermarket Trade API. Track post-market trade prices, volumes, and timestamps across several companies simultaneously.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-aftermarket-trade?symbols=AAPL
```

---

### Batch Aftermarket Quote API

Retrieve real-time aftermarket quotes for multiple stocks with the FMP Batch Aftermarket Quote API. Access bid and ask prices, volume, and other relevant data for several companies during post-market trading.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-aftermarket-quote?symbols=AAPL
```

---

### Exchange Stock Quotes API

Retrieve real-time stock quotes for all listed stocks on a specific exchange with the FMP Exchange Stock Quotes API. Track price changes and trading activity across the entire exchange.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-exchange-quote?exchange=NASDAQ
```

---

### Mutual Fund Price Quotes API

Access real-time quotes for mutual funds with the FMP Mutual Fund Price Quotes API. Track current prices, performance changes, and key data for various mutual funds.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-mutualfund-quotes
```

---

### ETF Price Quotes API

Get real-time price quotes for exchange-traded funds (ETFs) with the FMP ETF Price Quotes API. Track current prices, performance changes, and key data for a wide variety of ETFs.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-etf-quotes
```

---

### Full Commodities Quotes API

Get up-to-the-minute quotes for commodities with the FMP Real-Time Commodities Quotes API. Track the latest prices, changes, and volumes for a wide range of commodities, including oil, gold, and agricultural products.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-commodity-quotes
```

---

### Full Cryptocurrency Quotes API

Access real-time cryptocurrency quotes with the FMP Full Cryptocurrency Quotes API. Track live prices, trading volumes, and price changes for a wide range of digital assets.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-crypto-quotes
```

---

### Full Forex Quote API

Retrieve real-time quotes for multiple forex currency pairs with the FMP Batch Forex Quote API. Get real-time price changes and updates for a variety of forex pairs in a single request.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-forex-quotes
```

---

### Full Index Quotes API

Track real-time movements of major stock market indexes with the FMP Stock Market Index Quotes API. Access live quotes for global indexes and monitor changes in their performance.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-index-quotes
```

---

## Statements

### Income Statement API

Access detailed income statement data for publicly traded companies with the Income Statements API. Track profitability, compare competitors, and identify business trends with up-to-date financial data.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/income-statement?symbol=AAPL
```

---

### Balance Sheet Statement API

Access detailed balance sheet statements for publicly traded companies with the Balance Sheet Data API. Analyze assets, liabilities, and shareholder equity to gain insights into a company's financial health.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/balance-sheet-statement?symbol=AAPL
```

---

### Cash Flow Statement API

Gain insights into a company's cash flow activities with the Cash Flow Statements API. Analyze cash generated and used from operations, investments, and financing activities to evaluate the financial health and sustainability of a business.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/cash-flow-statement?symbol=AAPL
```

---

### Latest Financial Statements API

---

### Income Statements TTM API

---

### Balance Sheet Statements TTM API

---

### Cashflow Statements TTM API

---

### Key Metrics API

Access essential financial metrics for a company with the FMP Financial Key Metrics API. Evaluate revenue, net income, P/E ratio, and more to assess performance and compare it to competitors.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/key-metrics?symbol=AAPL
```

---

### Financial Ratios API

Analyze a company's financial performance using the Financial Ratios API. This API provides detailed profitability, liquidity, and efficiency ratios, enabling users to assess a company's operational and financial health across various metrics.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ratios?symbol=AAPL
```

---

### Key Metrics TTM API

Retrieve a comprehensive set of trailing twelve-month (TTM) key performance metrics with the TTM Key Metrics API. Access data related to a company's profitability, capital efficiency, and liquidity, allowing for detailed analysis of its financial health over the past year.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/key-metrics-ttm?symbol=AAPL
```

---

### Financial Ratios TTM API

Gain access to trailing twelve-month (TTM) financial ratios with the TTM Ratios API. This API provides key performance metrics over the past year, including profitability, liquidity, and efficiency ratios.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ratios-ttm?symbol=AAPL
```

---

### Financial Scores API

Assess a company's financial strength using the Financial Health Scores API. This API provides key metrics such as the Altman Z-Score and Piotroski Score, giving users insights into a company’s overall financial health and stability.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/financial-scores?symbol=AAPL
```

---

### Owner Earnings API

Retrieve a company's owner earnings with the Owner Earnings API, which provides a more accurate representation of cash available to shareholders by adjusting net income. This metric is crucial for evaluating a company’s profitability from the perspective of investors.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/owner-earnings?symbol=AAPL
```

---

### Enterprise Values API

Access a company's enterprise value using the Enterprise Values API. This metric offers a comprehensive view of a company's total market value by combining both its equity (market capitalization) and debt, providing a better understanding of its worth.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/enterprise-values?symbol=AAPL
```

---

### Income Statement Growth API

Track key financial growth metrics with the Income Statement Growth API. Analyze how revenue, profits, and expenses have evolved over time, offering insights into a company’s financial health and operational efficiency.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/income-statement-growth?symbol=AAPL
```

---

### Balance Sheet Statement Growth API

Analyze the growth of key balance sheet items over time with the Balance Sheet Statement Growth API. Track changes in assets, liabilities, and equity to understand the financial evolution of a company.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/balance-sheet-statement-growth?symbol=AAPL
```

---

### Cashflow Statement Growth API

Measure the growth rate of a company’s cash flow with the FMP Cashflow Statement Growth API. Determine how quickly a company’s cash flow is increasing or decreasing over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/cash-flow-statement-growth?symbol=AAPL
```

---

### Financial Statement Growth API

Analyze the growth of key financial statement items across income, balance sheet, and cash flow statements with the Financial Statement Growth API. Track changes over time to understand trends in financial performance.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/financial-growth?symbol=AAPL
```

---

### Financial Reports Dates API

---

### Financial Reports Form 10-K JSON API

Access comprehensive annual reports with the FMP Annual Reports on Form 10-K API. Obtain detailed information about a company’s financial performance, business operations, and risk factors as reported to the SEC.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/financial-reports-json?symbol=AAPL&year=2022&period=FY
```

---

### Financial Reports Form 10-K XLSX API

Download detailed 10-K reports in XLSX format with the Financial Reports Form 10-K XLSX API. Effortlessly access and analyze annual financial data for companies in a spreadsheet-friendly format.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/financial-reports-xlsx?symbol=AAPL&year=2022&period=FY
```

---

### Revenue Product Segmentation API

Access detailed revenue breakdowns by product line with the Revenue Product Segmentation API. Understand which products drive a company's earnings and get insights into the performance of individual product segments.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/revenue-product-segmentation?symbol=AAPL
```

---

### Revenue Geographic Segments API

Access detailed revenue breakdowns by geographic region with the Revenue Geographic Segments API. Analyze how different regions contribute to a company’s total revenue and identify key markets for growth.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/revenue-geographic-segmentation?symbol=AAPL
```

---

### As Reported Income Statements API

Retrieve income statements as they were reported by the company with the As Reported Income Statements API. Access raw financial data directly from official company filings, including revenue, expenses, and net income.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/income-statement-as-reported?symbol=AAPL
```

---

### As Reported Balance Statements API

Access balance sheets as reported by the company with the As Reported Balance Statements API. View detailed financial data on assets, liabilities, and equity directly from official filings.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/balance-sheet-statement-as-reported?symbol=AAPL
```

---

### As Reported Cashflow Statements API

View cash flow statements as reported by the company with the As Reported Cash Flow Statements API. Analyze a company's cash flows related to operations, investments, and financing directly from official reports.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/cash-flow-statement-as-reported?symbol=AAPL
```

---

### As Reported Financial Statements API

Retrieve comprehensive financial statements as reported by companies with FMP As Reported Financial Statements API. Access complete data across income, balance sheet, and cash flow statements in their original form for detailed analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/financial-statement-full-as-reported?symbol=AAPL
```

---

## Charts

### Stock Chart Light API

Access simplified stock chart data using the FMP Basic Stock Chart API. This API provides essential charting information, including date, price, and trading volume, making it ideal for tracking stock performance with minimal data and creating basic price and volume charts.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/light?symbol=AAPL
```

---

### Stock Price and Volume Data API

Access full price and volume data for any stock symbol using the FMP Comprehensive Stock Price and Volume Data API. Get detailed insights, including open, high, low, close prices, trading volume, price changes, percentage changes, and volume-weighted average price (VWAP).

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/full?symbol=AAPL
```

---

### Unadjusted Stock Price API

Access stock price and volume data without adjustments for stock splits with the FMP Unadjusted Stock Price Chart API. Get accurate insights into stock performance, including open, high, low, and close prices, along with trading volume, without split-related changes.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/non-split-adjusted?symbol=AAPL
```

---

### Dividend Adjusted Price Chart API

Analyze stock performance with dividend adjustments using the FMP Dividend-Adjusted Price Chart API. Access end-of-day price and volume data that accounts for dividend payouts, offering a more comprehensive view of stock trends over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/dividend-adjusted?symbol=AAPL
```

---

### 1 Min Interval Stock Chart API

Access precise intraday stock price and volume data with the FMP 1-Minute Interval Stock Chart API. Retrieve real-time or historical stock data in 1-minute intervals, including key information such as open, high, low, and close prices, and trading volume for each minute.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1min?symbol=AAPL
```

---

### 5 Min Interval Stock Chart API

Access stock price and volume data with the FMP 5-Minute Interval Stock Chart API. Retrieve detailed stock data in 5-minute intervals, including open, high, low, and close prices, along with trading volume for each 5-minute period. This API is perfect for short-term trading analysis and building intraday charts.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/5min?symbol=AAPL
```

---

### 15 Min Interval Stock Chart API

Access stock price and volume data with the FMP 15-Minute Interval Stock Chart API. Retrieve detailed stock data in 15-minute intervals, including open, high, low, close prices, and trading volume. This API is ideal for creating intraday charts and analyzing medium-term price trends during the trading day.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/15min?symbol=AAPL
```

---

### 30 Min Interval Stock Chart API

Access stock price and volume data with the FMP 30-Minute Interval Stock Chart API. Retrieve essential stock data in 30-minute intervals, including open, high, low, close prices, and trading volume. This API is perfect for creating intraday charts and tracking medium-term price movements for more strategic trading decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/30min?symbol=AAPL
```

---

### 1 Hour Interval Stock Chart API

Track stock price movements over hourly intervals with the FMP 1-Hour Interval Stock Chart API. Access essential stock price and volume data, including open, high, low, and close prices for each hour, to analyze broader intraday trends with precision.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1hour?symbol=AAPL
```

---

### 4 Hour Interval Stock Chart API

Analyze stock price movements over extended intraday periods with the FMP 4-Hour Interval Stock Chart API. Access key stock price and volume data in 4-hour intervals, perfect for tracking longer intraday trends and understanding broader market movements.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/4hour?symbol=AAPL
```

---

## Economics

### Treasury Rates API

Access latest and historical Treasury rates for all maturities with the FMP Treasury Rates API. Track key benchmarks for interest rates across the economy.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/treasury-rates
```

---

### Economics Indicators API

Access real-time and historical economic data for key indicators like GDP, unemployment, and inflation with the FMP Economic Indicators API. Use this data to measure economic performance and identify growth trends.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/economic-indicators?name=GDP
```

---

### Economic Data Releases Calendar API

Stay informed with the FMP Economic Data Releases Calendar API. Access a comprehensive calendar of upcoming economic data releases to prepare for market impacts and make informed investment decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/economic-calendar
```

---

### Market Risk Premium API

Access the market risk premium for specific dates with the FMP Market Risk Premium API. Use this key financial metric to assess the additional return expected from investing in the stock market over a risk-free investment.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/market-risk-premium
```

---

## Earnings, Dividends, Splits

### Dividends Company API

Stay informed about upcoming dividend payments with the FMP Dividends Company API. This API provides essential dividend data for individual stock symbols, including record dates, payment dates, declaration dates, and more.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/dividends?symbol=AAPL
```

---

### Dividends Calendar API

Stay informed on upcoming dividend events with the Dividend Events Calendar API. Access a comprehensive schedule of dividend-related dates for all stocks, including record dates, payment dates, declaration dates, and dividend yields.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/dividends-calendar
```

---

### Earnings Report API

Retrieve in-depth earnings information with the FMP Earnings Report API. Gain access to key financial data for a specific stock symbol, including earnings report dates, EPS estimates, and revenue projections to help you stay on top of company performance.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/earnings?symbol=AAPL
```

---

### Earnings Calendar API

Stay informed on upcoming and past earnings announcements with the FMP Earnings Calendar API. Access key data, including announcement dates, estimated earnings per share (EPS), and actual EPS for publicly traded companies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/earnings-calendar
```

---

### IPOs Calendar API

Access a comprehensive list of all upcoming initial public offerings (IPOs) with the FMP IPO Calendar API. Stay up to date on the latest companies entering the public market, with essential details on IPO dates, company names, expected pricing, and exchange listings.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ipos-calendar
```

---

### IPOs Disclosure API

Access a comprehensive list of disclosure filings for upcoming initial public offerings (IPOs) with the FMP IPO Disclosures API. Stay updated on regulatory filings, including filing dates, effectiveness dates, CIK numbers, and form types, with direct links to official SEC documents.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ipos-disclosure
```

---

### IPOs Prospectus API

Access comprehensive information on IPO prospectuses with the FMP IPO Prospectus API. Get key financial details, such as public offering prices, discounts, commissions, proceeds before expenses, and more. This API also provides links to official SEC prospectuses, helping investors stay informed on companies entering the public market.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ipos-prospectus
```

---

### Stock Split Details API

Access detailed information on stock splits for a specific company using the FMP Stock Split Details API. This API provides essential data, including the split date and the split ratio, helping users understand changes in a company's share structure after a stock split.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/splits?symbol=AAPL
```

---

### Stock Splits Calendar API

Stay informed about upcoming stock splits with the FMP Stock Splits Calendar API. This API provides essential data on upcoming stock splits across multiple companies, including the split date and ratio, helping you track changes in share structures before they occur.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/splits-calendar
```

---

## Earnings Transcript

### Latest Earning Transcripts API

Access available earnings transcripts for companies with the FMP Latest Earning Transcripts API. Retrieve a list of companies with earnings transcripts, along with the total number of transcripts available for each company.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/earning-call-transcript-latest
```

---

### Earnings Transcript API

Access the full transcript of a company’s earnings call with the FMP Earnings Transcript API. Stay informed about a company’s financial performance, future plans, and overall strategy by analyzing management's communication.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/earning-call-transcript?symbol=AAPL&year=2020&quarter=3
```

---

### Transcripts Dates By Symbol API

Access earnings call transcript dates for specific companies with the FMP Transcripts Dates By Symbol API. Get a comprehensive overview of earnings call schedules based on fiscal year and quarter.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/earning-call-transcript-dates?symbol=AAPL
```

---

### Available Transcript Symbols API

Access a complete list of stock symbols with available earnings call transcripts using the FMP Available Earnings Transcript Symbols API. Retrieve information on which companies have earnings transcripts and how many are accessible for detailed financial analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/earnings-transcript-list
```

---

## News

### FMP Articles API

Access the latest articles from Financial Modeling Prep with the FMP Articles API. Get comprehensive updates including headlines, snippets, and publication URLs.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/fmp-articles?page=0&limit=20
```

---

### General News API

Access the latest general news articles from a variety of sources with the FMP General News API. Obtain headlines, snippets, and publication URLs for comprehensive news coverage.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/general-latest?page=0&limit=20
```

---

### Press Releases API

Access official company press releases with the FMP Press Releases API. Get real-time updates on corporate announcements, earnings reports, mergers, and more.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/press-releases-latest?page=0&limit=20
```

---

### Stock News API

Stay informed with the latest stock market news using the FMP Stock News Feed API. Access headlines, snippets, publication URLs, and ticker symbols for the most recent articles from a variety of sources.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/stock-latest?page=0&limit=20
```

---

### Crypto News API

Stay informed with the latest cryptocurrency news using the FMP Crypto News API. Access a curated list of articles from various sources, including headlines, snippets, and publication URLs.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/crypto-latest?page=0&limit=20
```

---

### Forex News API

Stay updated with the latest forex news articles from various sources using the FMP Forex News API. Access headlines, snippets, and publication URLs for comprehensive market insights.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/forex-latest?page=0&limit=20
```

---

### Search Press Releases API

Search for company press releases with the FMP Search Press Releases API. Find specific corporate announcements and updates by entering a stock symbol or company name.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/press-releases?symbols=AAPL
```

---

### Search Stock News API

Search for stock-related news using the FMP Search Stock News API. Find specific stock news by entering a ticker symbol or company name to track the latest developments.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/stock?symbols=AAPL
```

---

### Search Crypto News API

Search for cryptocurrency news using the FMP Search Crypto News API. Retrieve news related to specific coins or tokens by entering their name or symbol.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/crypto?symbols=BTCUSD
```

---

### Search Forex News API

Search for foreign exchange news using the FMP Search Forex News API. Find targeted news on specific currency pairs by entering their symbols for focused updates.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/news/forex?symbols=EURUSD
```

---

## Form 13F

### Institutional Ownership Filings API

Stay up to date with the most recent SEC filings related to institutional ownership using the Institutional Ownership Filings API. This tool allows you to track the latest reports and disclosures from institutional investors, giving you a real-time view of major holdings and regulatory submissions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/latest?page=0&limit=100
```

---

### Filings Extract API

The SEC Filings Extract API allows users to extract detailed data directly from official SEC filings. This API provides access to key information such as company shares, security details, and filing links, making it easier to analyze corporate disclosures.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/extract?cik=0001388838&year=2023&quarter=3
```

---

### Form 13F Filings Dates API

The Form 13F Filings Dates API allows you to retrieve dates associated with Form 13F filings by institutional investors. This is crucial for tracking stock holdings of institutional investors at specific points in time, providing valuable insights into their investment strategies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/dates?cik=0001067983
```

---

### Filings Extract With Analytics By Holder API

The Filings Extract With Analytics By Holder API provides an analytical breakdown of institutional filings. This API offers insight into stock movements, strategies, and portfolio changes by major institutional holders, helping you understand their investment behavior and track significant changes in stock ownership.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/extract-analytics/holder?symbol=AAPL&year=2023&quarter=3&page=0&limit=10
```

---

### Holder Performance Summary API

The Holder Performance Summary API provides insights into the performance of institutional investors based on their stock holdings. This data helps track how well institutional holders are performing, their portfolio changes, and how their performance compares to benchmarks like the S&P 500.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/holder-performance-summary?cik=0001067983&page=0
```

---

### Holders Industry Breakdown API

The Holders Industry Breakdown API provides an overview of the sectors and industries that institutional holders are investing in. This API helps analyze how institutional investors distribute their holdings across different industries and track changes in their investment strategies over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/holder-industry-breakdown?cik=0001067983&year=2023&quarter=3
```

---

### Positions Summary API

The Positions Summary API provides a comprehensive snapshot of institutional holdings for a specific stock symbol. It tracks key metrics like the number of investors holding the stock, changes in the number of shares, total investment value, and ownership percentages over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/symbol-positions-summary?symbol=AAPL&year=2023&quarter=3
```

---

### Industry Performance Summary API

The Industry Performance Summary API provides an overview of how various industries are performing financially. By analyzing the value of industries over a specific period, this API helps investors and analysts understand the health of entire sectors and make informed decisions about sector-based investments.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/industry-summary?year=2023&quarter=3
```

---

## Analyst

### Financial Estimates API

Retrieve analyst financial estimates for stock symbols with the FMP Financial Estimates API. Access projected figures like revenue, earnings per share (EPS), and other key financial metrics as forecasted by industry analysts to inform your investment decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/analyst-estimates?symbol=AAPL&period=annual&page=0&limit=10
```

---

### Ratings Snapshot API

Quickly assess the financial health and performance of companies with the FMP Ratings Snapshot API. This API provides a comprehensive snapshot of financial ratings for stock symbols in our database, based on various key financial ratios.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ratings-snapshot?symbol=AAPL
```

---

### Historical Ratings API

Track changes in financial performance over time with the FMP Historical Ratings API. This API provides access to historical financial ratings for stock symbols in our database, allowing users to view ratings and key financial metric scores for specific dates.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ratings-historical?symbol=AAPL
```

---

### Price Target Summary API

Gain insights into analysts' expectations for stock prices with the FMP Price Target Summary API. This API provides access to average price targets from analysts across various timeframes, helping investors assess future stock performance based on expert opinions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/price-target-summary?symbol=AAPL
```

---

### Price Target Consensus API

Access analysts' consensus price targets with the FMP Price Target Consensus API. This API provides high, low, median, and consensus price targets for stocks, offering investors a comprehensive view of market expectations for future stock prices.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/price-target-consensus?symbol=AAPL
```

---

### Stock Grades API

Access the latest stock grades from top analysts and financial institutions with the FMP Grades API. Track grading actions, such as upgrades, downgrades, or maintained ratings, for specific stock symbols, providing valuable insight into how experts evaluate companies over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/grades?symbol=AAPL
```

---

### Historical Stock Grades API

Access a comprehensive record of analyst grades with the FMP Historical Grades API. This tool allows you to track historical changes in analyst ratings for specific stock symbol

**Endpoint:**

```text
https://financialmodelingprep.com/stable/grades-historical?symbol=AAPL
```

---

### Stock Grades Summary API

Quickly access an overall view of analyst ratings with the FMP Grades Summary API. This API provides a consolidated summary of market sentiment for individual stock symbols, including the total number of strong buy, buy, hold, sell, and strong sell ratings. Understand the overall consensus on a stock’s outlook with just a few data points.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/grades-consensus?symbol=AAPL
```

---

## Market Performance

### Market Sector Performance Snapshot API

Get a snapshot of sector performance using the Market Sector Performance Snapshot API. Analyze how different industries are performing in the market based on average changes across sectors.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sector-performance-snapshot?date=2024-02-01
```

---

### Industry Performance Snapshot API

Access detailed performance data by industry using the Industry Performance Snapshot API. Analyze trends, movements, and daily performance metrics for specific industries across various stock exchanges.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/industry-performance-snapshot?date=2024-02-01
```

---

### Historical Market Sector Performance API

Access historical sector performance data using the Historical Market Sector Performance API. Review how different sectors have performed over time across various stock exchanges.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-sector-performance?sector=Energy
```

---

### Historical Industry Performance API

Access historical performance data for industries using the Historical Industry Performance API. Track long-term trends and analyze how different industries have evolved over time across various stock exchanges.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-industry-performance?industry=Biotechnology
```

---

### Sector PE Snapshot API

Retrieve the price-to-earnings (P/E) ratios for various sectors using the Sector P/E Snapshot API. Compare valuation levels across sectors to better understand market valuations.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sector-pe-snapshot?date=2024-02-01
```

---

### Industry PE Snapshot API

View price-to-earnings (P/E) ratios for different industries using the Industry P/E Snapshot API. Analyze valuation levels across various industries to understand how each is priced relative to its earnings.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/industry-pe-snapshot?date=2024-02-01
```

---

### Historical Sector PE API

Access historical price-to-earnings (P/E) ratios for various sectors using the Historical Sector P/E API. Analyze how sector valuations have evolved over time to understand long-term trends and market shifts.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-sector-pe?sector=Energy
```

---

### Historical Industry PE API

Access historical price-to-earnings (P/E) ratios by industry using the Historical Industry P/E API. Track valuation trends across various industries to understand how market sentiment and valuations have evolved over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-industry-pe?industry=Biotechnology
```

---

### Biggest Stock Gainers API

Track the stocks with the largest price increases using the Top Stock Gainers API. Identify the companies that are leading the market with significant price surges, offering potential growth opportunities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/biggest-gainers
```

---

### Biggest Stock Losers API

Access data on the stocks with the largest price drops using the Biggest Stock Losers API. Identify companies experiencing significant declines and track the stocks that are falling the fastest in the market.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/biggest-losers
```

---

### Top Traded Stocks API

View the most actively traded stocks using the Top Traded Stocks API. Identify the companies experiencing the highest trading volumes in the market and track where the most trading activity is happening.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/most-actives
```

---

## Technical Indicators

### Simple Moving Average API

---

### Exponential Moving Average API

---

### Weighted Moving Average API

---

### Double Exponential Moving Average API

---

### Triple Exponential Moving Average API

---

### Relative Strength Index API

---

### Standard Deviation API

---

### Williams API

---

### Average Directional Index API

---

## Etf And Mutual Funds

### ETF & Fund Holdings API

Get a detailed breakdown of the assets held within ETFs and mutual funds using the FMP ETF & Fund Holdings API. Access real-time data on the specific securities and their weights in the portfolio, providing insights into asset composition and fund strategies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/etf/holdings?symbol=SPY
```

---

### ETF & Mutual Fund Information API

Access comprehensive data on ETFs and mutual funds with the FMP ETF & Mutual Fund Information API. Retrieve essential details such as ticker symbol, fund name, expense ratio, assets under management, and more.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/etf/info?symbol=SPY
```

---

### ETF & Fund Country Allocation API

Gain insight into how ETFs and mutual funds distribute assets across different countries with the FMP ETF & Fund Country Allocation API. This tool provides detailed information on the percentage of assets allocated to various regions, helping you make informed investment decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/etf/country-weightings?symbol=SPY
```

---

### ETF Asset Exposure API

Discover which ETFs hold specific stocks with the FMP ETF Asset Exposure API. Access detailed information on market value, share numbers, and weight percentages for assets within ETFs.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/etf/asset-exposure?symbol=AAPL
```

---

### ETF Sector Weighting API

The FMP ETF Sector Weighting API provides a breakdown of the percentage of an ETF's assets that are invested in each sector. For example, an investor may want to invest in an ETF that has a high exposure to the technology sector if they believe that the technology sector is poised for growth.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/etf/sector-weightings?symbol=SPY
```

---

### Mutual Fund & ETF Disclosure API

Access the latest disclosures from mutual funds and ETFs with the FMP Mutual Fund & ETF Disclosure API. This API provides updates on filings, changes in holdings, and other critical disclosure data for mutual funds and ETFs.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/funds/disclosure-holders-latest?symbol=AAPL
```

---

### Mutual Fund Disclosures API

Access comprehensive disclosure data for mutual funds with the FMP Mutual Fund Disclosures API. Analyze recent filings, balance sheets, and financial reports to gain insights into mutual fund portfolios.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/funds/disclosure?symbol=VWO&year=2023&quarter=4
```

---

### Mutual Fund & ETF Disclosure Name Search API

Easily search for mutual fund and ETF disclosures by name using the Mutual Fund & ETF Disclosure Name Search API. This API allows you to find specific reports and filings based on the fund or ETF name, providing essential details like CIK number, entity information, and reporting file number.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/funds/disclosure-holders-search?name=Federated
```

---

### Fund & ETF Disclosures by Date API

Retrieve detailed disclosures for mutual funds and ETFs based on filing dates with the FMP Fund & ETF Disclosures by Date API. Stay current with the latest filings and track regulatory updates effectively.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/funds/disclosure-dates?symbol=VWO
```

---

## Sec Filings

### Latest 8-K SEC Filings API

Stay up-to-date with the most recent 8-K filings from publicly traded companies using the FMP Latest 8-K SEC Filings API. Get real-time access to significant company events such as mergers, acquisitions, leadership changes, and other material events that may impact the market.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-filings-8k?from=2024-01-01&to=2024-03-01&page=0&limit=100
```

---

### Latest SEC Filings API

Stay updated with the most recent SEC filings from publicly traded companies using the FMP Latest SEC Filings API. Access essential regulatory documents, including financial statements, annual reports, 8-K, 10-K, and 10-Q forms.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-filings-financials?from=2024-01-01&to=2024-03-01&page=0&limit=100
```

---

### SEC Filings By Form Type API

Search for specific SEC filings by form type with the FMP SEC Filings By Form Type API. Retrieve filings such as 10-K, 10-Q, 8-K, and others, filtered by the exact type of document you're looking for.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-filings-search/form-type?formType=8-K&from=2024-01-01&to=2024-03-01&page=0&limit=100
```

---

### SEC Filings By Symbol API

Search and retrieve SEC filings by company symbol using the FMP SEC Filings By Symbol API. Gain direct access to regulatory filings such as 8-K, 10-K, and 10-Q reports for publicly traded companies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-filings-search/symbol?symbol=AAPL&from=2024-01-01&to=2024-03-01&page=0&limit=100
```

---

### SEC Filings By CIK API

Search for SEC filings using the FMP SEC Filings By CIK API. Access detailed regulatory filings by Central Index Key (CIK) number, enabling you to track all filings related to a specific company or entity.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-filings-search/cik?cik=0000320193&from=2024-01-01&to=2024-03-01&page=0&limit=100
```

---

### SEC Filings By Name API

Search for SEC filings by company or entity name using the FMP SEC Filings By Name API. Quickly retrieve official filings for any organization based on its name.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-filings-company-search/name?company=Berkshire
```

---

### SEC Filings Company Search By Symbol API

Find company information and regulatory filings using a stock symbol with the FMP SEC Filings Company Search By Symbol API. Quickly access essential company details based on stock ticker symbols.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-filings-company-search/symbol?symbol=AAPL
```

---

### SEC Filings Company Search By CIK API

Easily find company information using a CIK (Central Index Key) with the FMP SEC Filings Company Search By CIK API. Access essential company details and filings linked to a specific CIK number.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-filings-company-search/cik?cik=0000320193
```

---

### SEC Company Full Profile API

Retrieve detailed company profiles, including business descriptions, executive details, contact information, and financial data with the FMP SEC Company Full Profile API.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sec-profile?symbol=AAPL
```

---

### Industry Classification List API

Retrieve a comprehensive list of industry classifications, including Standard Industrial Classification (SIC) codes and industry titles with the FMP Industry Classification List API.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/standard-industrial-classification-list
```

---

### Industry Classification Search API

Search and retrieve industry classification details for companies, including SIC codes, industry titles, and business information, with the FMP Industry Classification Search API.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/industry-classification-search
```

---

### All Industry Classification API

Access comprehensive industry classification data for companies across all sectors with the FMP All Industry Classification API. Retrieve key details such as SIC codes, industry titles, and business contact information.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/all-industry-classification
```

---

## Insider Trades

### Latest Insider Trading API

Access the latest insider trading activity using the Latest Insider Trading API. Track which company insiders are buying or selling stocks and analyze their transactions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/insider-trading/latest?page=0&limit=100
```

---

### Search Insider Trades API

Search insider trading activity by company or symbol using the Search Insider Trades API. Find specific trades made by corporate insiders, including executives and directors.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/insider-trading/search?page=0&limit=100
```

---

### Search Insider Trades by Reporting Name API

Search for insider trading activity by reporting name using the Search Insider Trades by Reporting Name API. Track trading activities of specific individuals or groups involved in corporate insider transactions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/insider-trading/reporting-name?name=Zuckerberg
```

---

### All Insider Transaction Types API

Access a comprehensive list of insider transaction types with the All Insider Transaction Types API. This API provides details on various transaction actions, including purchases, sales, and other corporate actions involving insider trading.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/insider-trading-transaction-type
```

---

### Insider Trade Statistics API

Analyze insider trading activity with the Insider Trade Statistics API. This API provides key statistics on insider transactions, including total purchases, sales, and trends for specific companies or stock symbols.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/insider-trading/statistics?symbol=AAPL
```

---

### Acquisition Ownership API

Track changes in stock ownership during acquisitions using the Acquisition Ownership API. This API provides detailed information on how mergers, takeovers, or beneficial ownership changes impact the stock ownership structure of a company.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/acquisition-of-beneficial-ownership?symbol=AAPL
```

---

## Indexes

### Stock Market Indexes List API

Retrieve a comprehensive list of stock market indexes across global exchanges using the FMP Stock Market Indexes List API. This API provides essential information such as the symbol, name, exchange, and currency for each index, helping analysts and investors keep track of various market benchmarks.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/index-list
```

---

### Index Quote API

Access real-time stock index quotes with the Stock Index Quote API. Stay updated with the latest price changes, daily highs and lows, volume, and other key metrics for major stock indices around the world.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote?symbol=^GSPC
```

---

### Index Short Quote API

Access concise stock index quotes with the Stock Index Short Quote API. This API provides a snapshot of the current price, change, and volume for stock indexes, making it ideal for users who need a quick overview of market movements.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote-short?symbol=^GSPC
```

---

### All Index Quotes API

The All Index Quotes API provides real-time quotes for a wide range of stock indexes, from major market benchmarks to niche indexes. This API allows users to track market performance across multiple indexes in a single request, giving them a broad view of the financial markets.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-index-quotes
```

---

### Historical Index Light Chart API

Retrieve end-of-day historical prices for stock indexes using the Historical Price Data API. This API provides essential data such as date, price, and volume, enabling detailed analysis of price movements over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/light?symbol=^GSPC
```

---

### Historical Index Full Chart API

Access full historical end-of-day prices for stock indexes using the Detailed Historical Price Data API. This API provides comprehensive information, including open, high, low, close prices, volume, and additional metrics for detailed financial analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/full?symbol=^GSPC
```

---

### 1-Minute Interval Index Price API

Retrieve 1-minute interval intraday data for stock indexes using the Intraday 1-Minute Price Data API. This API provides granular price information, helping users track short-term price movements and trading volume within each minute.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1min?symbol=^GSPC
```

---

### 5-Minute Interval Index Price API

Retrieve 5-minute interval intraday price data for stock indexes using the Intraday 5-Minute Price Data API. This API provides crucial insights into price movements and trading volume within 5-minute windows, ideal for traders who require short-term data.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/5min?symbol=^GSPC
```

---

### 1-Hour Interval Index Price API

Access 1-hour interval intraday data for stock indexes using the Intraday 1-Hour Price Data API. This API provides detailed price movements and volume within hourly intervals, making it ideal for tracking medium-term market trends during the trading day.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1hour?symbol=^GSPC
```

---

### S&P 500 Index API

Access detailed data on the S&P 500 index using the S&P 500 Index API. Track the performance and key information of the companies that make up this major stock market index.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/sp500-constituent
```

---

### Nasdaq Index API

Access comprehensive data for the Nasdaq index with the Nasdaq Index API. Monitor real-time movements and track the historical performance of companies listed on this prominent stock exchange.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/nasdaq-constituent
```

---

### Dow Jones API

Access data on the Dow Jones Industrial Average using the Dow Jones API. Track current values, analyze trends, and get detailed information about the companies that make up this important stock index.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/dowjones-constituent
```

---

### Historical S&P 500 API

Retrieve historical data for the S&P 500 index using the Historical S&P 500 API. Analyze past changes in the index, including additions and removals of companies, to understand trends and performance over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-sp500-constituent
```

---

### Historical Nasdaq API

Access historical data for the Nasdaq index using the Historical Nasdaq API. Analyze changes in the index composition and view how it has evolved over time, including company additions and removals.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-nasdaq-constituent
```

---

### Historical Dow Jones API

Access historical data for the Dow Jones Industrial Average using the Historical Dow Jones API. Analyze changes in the index’s composition and study its performance across different periods.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-dowjones-constituent
```

---

## Market Hours

### Global Exchange Market Hours API

Retrieve trading hours for specific stock exchanges using the Global Exchange Market Hours API. Find out the opening and closing times of global exchanges to plan your trading strategies effectively.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/exchange-market-hours?exchange=NASDAQ
```

---

### Holidays By Exchange API

---

### All Exchange Market Hours API

View the market hours for all exchanges. Check when different markets are active.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/all-exchange-market-hours
```

---

## Commodity

### Commodities List API

Access an extensive list of tracked commodities across various sectors, including energy, metals, and agricultural products. The FMP Commodities List API provides essential data on tradable commodities, giving investors the ability to explore market options in real-time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/commodities-list
```

---

### Commodities Quote API

Access real-time price quotes for all commodities traded worldwide with the FMP Global Commodities Quotes API. Track market movements and identify investment opportunities with comprehensive price data.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote?symbol=GCUSD
```

---

### Commodities Quote Short API

Get fast and accurate quotes for commodities with the FMP Commodities Quick Quote API. Instantly access the current price, recent changes, and trading volume for various commodities in real-time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote-short?symbol=GCUSD
```

---

### All Commodities Quotes API

Access real-time quotes for multiple commodities at once with the FMP Real-Time Batch Commodities Quotes API. Instantly track price changes, volume, and other key metrics for a broad range of commodities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-commodity-quotes
```

---

### Light Chart API

Access historical end-of-day prices for various commodities with the FMP Historical Commodities Price API. Analyze past price movements, trading volume, and trends to support informed decision-making.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/light?symbol=GCUSD
```

---

### Full Chart API

Access full historical end-of-day price data for commodities with the FMP Comprehensive Commodities Price API. This API enables users to analyze long-term price trends, patterns, and market movements in great detail.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/full?symbol=GCUSD
```

---

### 1-Minute Interval Commodities Chart API

Track real-time, short-term price movements for commodities with the FMP 1-Minute Interval Commodities Chart API. This API provides detailed 1-minute interval data, enabling precise monitoring of intraday market changes.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1min?symbol=GCUSD
```

---

### 5-Minute Interval Commodities Chart API

Monitor short-term price movements with the FMP 5-Minute Interval Commodities Chart API. This API provides detailed 5-minute interval data, enabling users to track near-term price trends for more strategic trading and investment decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/5min?symbol=GCUSD
```

---

### 1-Hour Interval Commodities Chart API

Monitor hourly price movements and trends with the FMP 1-Hour Interval Commodities Chart API. This API provides hourly data, offering a detailed look at price fluctuations throughout the trading day to support mid-term trading strategies and market analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1hour?symbol=GCUSD
```

---

## Discounted Cash Flow

### DCF Valuation API

Estimate the intrinsic value of a company with the FMP Discounted Cash Flow Valuation API. Calculate the DCF valuation based on expected future cash flows and discount rates.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/discounted-cash-flow?symbol=AAPL
```

---

### Levered DCF API

Analyze a company’s value with the FMP Levered Discounted Cash Flow (DCF) API, which incorporates the impact of debt. This API provides post-debt company valuation, offering investors a more accurate measure of a company's true worth by accounting for its debt obligations.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/levered-discounted-cash-flow?symbol=AAPL
```

---

### Custom DCF Advanced API

Run a tailored Discounted Cash Flow (DCF) analysis using the FMP Custom DCF Advanced API. With detailed inputs, this API allows users to fine-tune their assumptions and variables, offering a more personalized and precise valuation for a company.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/custom-discounted-cash-flow?symbol=AAPL
```

---

### Custom DCF Levered API

Run a tailored Discounted Cash Flow (DCF) analysis using the FMP Custom DCF Advanced API. With detailed inputs, this API allows users to fine-tune their assumptions and variables, offering a more personalized and precise valuation for a company.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/custom-levered-discounted-cash-flow?symbol=AAPL
```

---

## Forex

### Forex Currency Pairs API

Access a comprehensive list of all currency pairs traded on the forex market with the FMP Forex Currency Pairs API. Analyze and track the performance of currency pairs to make informed investment decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/forex-list
```

---

### Forex Quote API

Access real-time forex quotes for currency pairs with the Forex Quote API. Retrieve up-to-date information on exchange rates and price changes to help monitor market movements.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote?symbol=EURUSD
```

---

### Forex Short Quote API

Quickly access concise forex pair quotes with the Forex Quote Snapshot API. Get a fast look at live currency exchange rates, price changes, and volume in real time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote-short?symbol=EURUSD
```

---

### Batch Forex Quotes API

Easily access real-time quotes for multiple forex pairs simultaneously with the Batch Forex Quotes API. Stay updated on global currency exchange rates and monitor price changes across different markets.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-forex-quotes
```

---

### Historical Forex Light Chart API

Access historical end-of-day forex prices with the Historical Forex Light Chart API. Track long-term price trends across different currency pairs to enhance your trading and analysis strategies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/light?symbol=EURUSD
```

---

### Historical Forex Full Chart API

Access comprehensive historical end-of-day forex price data with the Full Historical Forex Chart API. Gain detailed insights into currency pair movements, including open, high, low, close (OHLC) prices, volume, and percentage changes.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/full?symbol=EURUSD
```

---

### 1-Minute Interval Forex Chart API

Access real-time 1-minute intraday forex data with the 1-Minute Forex Interval Chart API. Track short-term price movements for precise, up-to-the-minute insights on currency pair fluctuations.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1min?symbol=EURUSD
```

---

### 5-Minute Interval Forex Chart API

Track short-term forex trends with the 5-Minute Forex Interval Chart API. Access detailed 5-minute intraday data to monitor currency pair price movements and market conditions in near real-time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/5min?symbol=EURUSD
```

---

### 1-Hour Interval Forex Chart API

Track forex price movements over the trading day with the 1-Hour Forex Interval Chart API. This tool provides hourly intraday data for currency pairs, giving a detailed view of trends and market shifts.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1hour?symbol=EURUSD
```

---

## Crypto

### Cryptocurrency List API

Access a comprehensive list of all cryptocurrencies traded on exchanges worldwide with the FMP Cryptocurrencies Overview API. Get detailed information on each cryptocurrency to inform your investment strategies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/cryptocurrency-list
```

---

### Full Cryptocurrency Quote API

Access real-time quotes for all cryptocurrencies with the FMP Full Cryptocurrency Quote API. Obtain comprehensive price data including current, high, low, and open prices.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote?symbol=BTCUSD
```

---

### Cryptocurrency Quote Short API

Access real-time cryptocurrency quotes with the FMP Cryptocurrency Quick Quote API. Get a concise overview of current crypto prices, changes, and trading volume for a wide range of digital assets.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/quote-short?symbol=BTCUSD
```

---

### All Cryptocurrencies Quotes API

Access live price data for a wide range of cryptocurrencies with the FMP Real-Time Cryptocurrency Batch Quotes API. Get real-time updates on prices, market changes, and trading volumes for digital assets in a single request.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/batch-crypto-quotes
```

---

### Historical Cryptocurrency Light Chart API

Access historical end-of-day prices for a variety of cryptocurrencies with the Historical Cryptocurrency Price Snapshot API. Track trends in price and trading volume over time to better understand market behavior.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/light?symbol=BTCUSD
```

---

### Historical Cryptocurrency Full Chart API

Access comprehensive end-of-day (EOD) price data for cryptocurrencies with the Full Historical Cryptocurrency Data API. Analyze long-term price trends, market movements, and trading volumes to inform strategic decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-price-eod/full?symbol=BTCUSD
```

---

### 1-Minute Interval Cryptocurrency Data API

Get real-time, 1-minute interval price data for cryptocurrencies with the 1-Minute Cryptocurrency Intraday Data API. Monitor short-term price fluctuations and trading volume to stay updated on market movements.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1min?symbol=BTCUSD
```

---

### 5-Minute Interval Cryptocurrency Data API

Analyze short-term price trends with the 5-Minute Interval Cryptocurrency Data API. Access real-time, intraday price data for cryptocurrencies to monitor rapid market movements and optimize trading strategies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/5min?symbol=BTCUSD
```

---

### 1-Hour Interval Cryptocurrency Data API

Access detailed 1-hour intraday price data for cryptocurrencies with the 1-Hour Interval Cryptocurrency Data API. Track hourly price movements to gain insights into market trends and make informed trading decisions throughout the day.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/historical-chart/1hour?symbol=BTCUSD
```

---

## Senate

### Latest Senate Financial Disclosures API

Access the latest financial disclosures from U.S. Senate members with the FMP Latest Senate Financial Disclosures API. Track recent trades, asset ownership, and transaction details for enhanced transparency in government financial activities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/senate-latest?page=0&limit=100
```

---

### Latest House Financial Disclosures API

Access real-time financial disclosures from U.S. House members with the FMP Latest House Financial Disclosures API. Track recent trades, asset ownership, and financial holdings for enhanced visibility into political figures' financial activities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/house-latest?page=0&limit=100
```

---

### Senate Trading Activity API

Monitor the trading activity of US Senators with the FMP Senate Trading Activity API. Access detailed information on trades made by Senators, including trade dates, assets, amounts, and potential conflicts of interest.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/senate-trades?symbol=AAPL
```

---

### Senate Trades By Name API

---

### U.S. House Trades API

Track the financial trades made by U.S. House members and their families with the FMP U.S. House Trades API. Access real-time information on stock sales, purchases, and other investment activities to gain insight into their financial decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/house-trades?symbol=AAPL
```

---

### House Trades By Name API

---

## ESG

### ESG Investment Search API

Align your investments with your values using the FMP ESG Investment Search API. Discover companies and funds based on Environmental, Social, and Governance (ESG) scores, performance, controversies, and business involvement criteria.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/esg-disclosures?symbol=AAPL
```

---

### ESG Ratings API

Access comprehensive ESG ratings for companies and funds with the FMP ESG Ratings API. Make informed investment decisions based on environmental, social, and governance (ESG) performance data.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/esg-ratings?symbol=AAPL
```

---

### ESG Benchmark Comparison API

Evaluate the ESG performance of companies and funds with the FMP ESG Benchmark Comparison API. Compare ESG leaders and laggards within industries to make informed and responsible investment decisions.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/esg-benchmark
```

---

## Commitment Of Traders

### COT Report API

Access comprehensive Commitment of Traders (COT) reports with the FMP COT Report API. This API provides detailed information about long and short positions across various sectors, helping you assess market sentiment and track positions in commodities, indices, and financial instruments.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/commitment-of-traders-report
```

---

### COT Analysis By Dates API

Gain in-depth insights into market sentiment with the FMP COT Report Analysis API. Analyze the Commitment of Traders (COT) reports for a specific date range to evaluate market dynamics, sentiment, and potential reversals across various sectors.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/commitment-of-traders-analysis
```

---

### COT Report List API

Access a comprehensive list of available Commitment of Traders (COT) reports by commodity or futures contract using the FMP COT Report List API. This API provides an overview of different market segments, allowing users to retrieve and explore COT reports for a wide variety of commodities and financial instruments.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/commitment-of-traders-list
```

---

## Fundraisers

### Latest Crowdfunding Campaigns API

Discover the most recent crowdfunding campaigns with the FMP Latest Crowdfunding Campaigns API. Stay informed on which companies and projects are actively raising funds, their financial details, and offering terms.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/crowdfunding-offerings-latest?page=0&limit=100
```

---

### Crowdfunding Campaign Search API

Search for crowdfunding campaigns by company name, campaign name, or platform with the FMP Crowdfunding Campaign Search API. Access detailed information to track and analyze crowdfunding activities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/crowdfunding-offerings-search?name=enotap
```

---

### Crowdfunding By CIK API

Access detailed information on all crowdfunding campaigns launched by a specific company with the FMP Crowdfunding By CIK API.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/crowdfunding-offerings?cik=0001916078
```

---

### Equity Offering Updates API

Stay informed about the latest equity offerings with the FMP Equity Offering Updates API. Track new shares being issued by companies and get insights into exempt offerings and amendments.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/fundraising-latest?page=0&limit=10
```

---

### Equity Offering Search API

Easily search for equity offerings by company name or stock symbol with the FMP Equity Offering Search API. Access detailed information about recent share issuances to stay informed on company fundraising activities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/fundraising-search?name=NJOY
```

---

### Equity Offering By CIK API

Access detailed information on equity offerings announced by specific companies with the FMP Company Equity Offerings by CIK API. Track offering activity and identify potential investment opportunities.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/fundraising?cik=0001547416
```

---

## Bulk

### Company Profile Bulk API

The FMP Profile Bulk API allows users to retrieve comprehensive company profile data in bulk. Access essential information, such as company details, stock price, market cap, sector, industry, and more for multiple companies in a single request.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/profile-bulk?part=0
```

---

### Stock Rating Bulk API

The FMP Rating Bulk API provides users with comprehensive rating data for multiple stocks in a single request. Retrieve key financial ratings and recommendations such as overall ratings, DCF recommendations, and more for multiple companies at once.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/rating-bulk
```

---

### DCF Valuations Bulk API

The FMP DCF Bulk API enables users to quickly retrieve discounted cash flow (DCF) valuations for multiple symbols in one request. Access the implied price movement and percentage differences for all listed companies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/dcf-bulk
```

---

### Financial Scores Bulk API

The FMP Scores Bulk API allows users to quickly retrieve a wide range of key financial scores and metrics for multiple symbols. These scores provide valuable insights into company performance, financial health, and operational efficiency.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/scores-bulk
```

---

### Price Target Summary Bulk API

The Price Target Summary Bulk API provides a comprehensive overview of price targets for all listed symbols over multiple timeframes. With this API, users can quickly retrieve price target data, helping investors and analysts compare current prices to projected targets across different periods.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/price-target-summary-bulk
```

---

### ETF Holder Bulk API

The ETF Holder Bulk API allows users to quickly retrieve detailed information about the assets and shares held by Exchange-Traded Funds (ETFs). This API provides insights into the weight each asset carries within the ETF, along with key financial information related to these holdings.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/etf-holder-bulk?part=1
```

---

### Upgrades Downgrades Consensus Bulk API

The Upgrades Downgrades Consensus Bulk API provides a comprehensive view of analyst ratings across all symbols. Retrieve bulk data for analyst upgrades, downgrades, and consensus recommendations to gain insights into the market's outlook on individual stocks.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/upgrades-downgrades-consensus-bulk
```

---

### Key Metrics TTM Bulk API

The Key Metrics TTM Bulk API allows users to retrieve trailing twelve months (TTM) data for all companies available in the database. The API provides critical financial ratios and metrics based on each company’s latest financial report, offering insights into company performance and financial health.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/key-metrics-ttm-bulk
```

---

### Ratios TTM Bulk API

The Ratios TTM Bulk API offers an efficient way to retrieve trailing twelve months (TTM) financial ratios for stocks. It provides users with detailed insights into a company’s profitability, liquidity, efficiency, leverage, and valuation ratios, all based on the most recent financial report.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/ratios-ttm-bulk
```

---

### Stock Peers Bulk API

The Stock Peers Bulk API allows you to quickly retrieve a comprehensive list of peer companies for all stocks in the database. By accessing this data, you can easily compare a stock’s performance with its closest competitors or similar companies within the same industry or sector.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/peers-bulk
```

---

### Earnings Surprises Bulk API

The Earnings Surprises Bulk API allows users to retrieve bulk data on annual earnings surprises, enabling quick analysis of which companies have beaten, missed, or met their earnings estimates. This API provides actual versus estimated earnings per share (EPS) for multiple companies at once, offering valuable insights for investors and analysts.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/earnings-surprises-bulk?year=2025
```

---

### Income Statement Bulk API

The Bulk Income Statement API allows users to retrieve detailed income statement data in bulk. This API is designed for large-scale data analysis, providing comprehensive insights into a company's financial performance, including revenue, gross profit, expenses, and net income.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/income-statement-bulk?year=2025&period=Q1
```

---

### Income Statement Growth Bulk API

The Bulk Income Statement Growth API provides access to growth data for income statements across multiple companies. Track and analyze growth trends over time for key financial metrics such as revenue, net income, and operating income, enabling a better understanding of corporate performance trends.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/income-statement-growth-bulk?year=2025&period=Q1
```

---

### Balance Sheet Statement Bulk API

The Bulk Balance Sheet Statement API provides comprehensive access to balance sheet data across multiple companies. It enables users to analyze financial positions by retrieving key figures such as total assets, liabilities, and equity. Ideal for comparing the financial health and stability of different companies on a large scale.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/balance-sheet-statement-bulk?year=2025&period=Q1
```

---

### Balance Sheet Statement Growth Bulk API

The Balance Sheet Growth Bulk API allows users to retrieve growth data across multiple companies’ balance sheets, enabling detailed analysis of how financial positions have changed over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/balance-sheet-statement-growth-bulk?year=2025&period=Q1
```

---

### Cash Flow Statement Bulk API

The Cash Flow Statement Bulk API provides access to detailed cash flow reports for a wide range of companies. This API enables users to retrieve bulk cash flow statement data, helping to analyze companies’ operating, investing, and financing activities over time.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/cash-flow-statement-bulk?year=2025&period=Q1
```

---

### Cash Flow Statement Growth Bulk API

The Cash Flow Statement Growth Bulk API allows you to retrieve bulk growth data for cash flow statements, enabling you to track changes in cash flows over time. This API is ideal for analyzing the cash flow growth trends of multiple companies simultaneously.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/cash-flow-statement-growth-bulk?year=2025&period=Q1
```

---

### Eod Bulk API

The EOD Bulk API allows users to retrieve end-of-day stock price data for multiple symbols in bulk. This API is ideal for financial analysts, traders, and investors who need to assess valuations for a large number of companies.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/eod-bulk?date=2024-10-22
```

---
