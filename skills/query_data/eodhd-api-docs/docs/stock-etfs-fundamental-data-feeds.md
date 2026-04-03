---
id: "url-438d088a"
type: "api"
title: "Fundamental Data: Stocks, ETFs, Mutual Funds, Indices"
url: "https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds/?preview=true"
description: "Simple access to fundamental data API for stocks, ETFs, Mutual Funds, and Indices from different exchanges and countries. Almost all major US, UK, EU and Asia exchanges.Since we provide extensive fundamental data, especially for stocks, the response can be large and include many data sections (see the full list of fields below). To manage this, you have the option to retrieve a specific section or a single field using filters. Read more about this feature below."
source: ""
tags: []
crawl_time: "2026-03-18T12:05:43.291Z"
metadata:
  endpoint: "https://eodhd.com/api/fundamentals/AAPL.US"
  parameters: []
  markdownContent: "# Fundamental Data: Stocks, ETFs, Mutual Funds, Indices\n\nSimple access to fundamental data API for stocks, ETFs, Mutual Funds, and Indices from different exchanges and countries. Almost all major US, UK, EU and Asia exchanges.Since we provide extensive fundamental data, especially for stocks, the response can be large and include many data sections (see the full list of fields below). To manage this, you have the option to retrieve a specific section or a single field using filters. Read more about this feature below.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/fundamentals/AAPL.US?filter=General::Code&api_token=demo&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/fundamentals/AAPL.US?filter=Financials::Balance_Sheet::yearly&api_token=demo&fmt=json\n```\n\n\n## Quick Start\n\nRequest example:\n\n## Stocks Fundamentals Data API\n\nFor stocks, we provide the following data fields:\n\nGeneral Company Details:\n\nFinancial Highlights and Key Metrics:\n\nMarket Valuation Metrics:\n\nShareholder & Ownership Data:\n\nTechnical Performance Metrics:\n\nSplits and Dividends:\n\nInstitutional Holders:\n\nInsider Transactions (Form 4):\n\n* all listed fields are available in the standalone Insider Transactions APIOutstanding Shares:\n\nFinancial Reports:\n\nThis is a JSON response example for the AAPL ticker. Only a portion of the data is shown in this code section. To retrieve the full data for AAPL, even with the “demo” key, perform the request in your browser manually or click here to open the full request in a new tab.\n\n## Partial Data Retrieval using filters: Web-service support\n\nSince we provide extensive fundamental data, especially for stocks, the response can be large and, as you saw above, include many data sections. To manage this, you have the option to retrieve a specific section or a single field using the parameter ‘filter=’. Section names and field names can be referenced from the AAPL response example. Multi-layer filtering is also supported. For example, if you want to retrieve only the ‘General’ block, use the following request:\n\nDifferent filter layers are separated by “::” and can have any number of layers as needed. For example:\n\nIt’s also possible to use multiple comma-separated filters. For example:\n\n## Equities Fundamentals Data API\n\nWe support the following data for Equity symbols:\n\nGeneral Data and Fundamental Highlights:\n\nIncludes sector, industry, company description, market capitalization, EBITDA, book value, dividend share, dividend yield, earnings per share (EPS), estimated EPS for the current and next year/quarter, and price-to-earnings (P/E) ratio.\n\nFinancial Reports (We support both US and non-US companies):\n\nPlease note that not all companies report complete financial data, so some data points may be unavailable for certain companies.\n\n## ETFs Fundamentals Data API\n\nWe also support details for more than 10,000 ETFs from different exchanges and countries. Here you can find the ETF Information and details we support at the moment.\n\n## Funds Fundamentals Data API\n\nWe support more than 20.000 US Mutual Funds. Our database has equity funds as well as balanced and bond-based mutual funds. We support all major information about almost all mutual funds on the market, including:\n\nIt’s also possible to get data from Mutual Fund by ticker. For example, for “Schwab S&P 500 Index” both identifications are correct: SWPPX.US and US8085098551.\n\nHere is an example of the structure for Charles Schwab fund “Schwab S&P 500 Index” provided by our fundamentals API. And do not forget that we also have End-Of-Day with our Stock Price Data API (End-Of-Day Historical Data) and Live data with our Live/Real-time Stock Prices API for SWPPX and other funds.\n\n## Current and Historical Index Constituents API\n\nAvailable data for each Component:\n\n2. Historical data. A list of all components that have ever been in an index is available for the following indices. To view this section in JSON response, purchase the Indices Historical Constituents Data API (this data is part of that dataset).Available indices:\n\nThe response includes not only the current list of active constituents but non-active constituents (those previously included in an index) as well, along with the dates of their addition and exclusion. Non-active constituents are available under the “HistoricalTickerComponents” section of the response. Plus there is an additional data field “Weight” (based on “free float market cap” for S&P and “price-weighted” for DJ).\n\nThe query example:\n\nResponse example for S&P 500 (GSPC.INDX):\n\n## Historical Constituents for the S&P 500 (GSPC)\n\nThrough the Fundamentals API package, Historical data for the S&P 500 (also known as GSPC or simply S&P) is available in the form of snapshots for each date, providing the list of all 500 components for a specific date. We track the data from the 1960s, though the most complete data starts from 2016.\n\nRequest example:\n\nResponse example (“HistoricalComponents” section):\n\n## Bulk Fundamentals API\n\nLearn how to get Fundamental Data for multiple tickers or entire exchanges here.\n\n## Code Examples\n\n```text\n\"General\": {\n    \"Code\": \"AAPL\",\n    \"Type\": \"Common Stock\",\n    \"Name\": \"Apple Inc\",\n    \"Exchange\": \"NASDAQ\",\n    \"CurrencyCode\": \"USD\",\n    \"CurrencyName\": \"US Dollar\",\n    \"CurrencySymbol\": \"$\",\n    \"CountryName\": \"USA\",\n    \"CountryISO\": \"US\",\n    \"OpenFigi\": \"BBG000B9XRY4\",\n    \"ISIN\": \"US0378331005\",\n    \"LEI\": \"HWUPKR0MPOU8FGXBT394\",\n    \"PrimaryTicker\": \"AAPL.US\",\n    \"CUSIP\": \"037833100\",\n    \"CIK\": \"320193\",\n    \"EmployerIdNumber\": \"94-2404110\",\n    \"FiscalYearEnd\": \"September\",\n    \"IPODate\": \"1980-12-12\",\n    \"InternationalDomestic\": \"International/Domestic\",\n    \"Sector\": \"Technology\",\n    \"Industry\": \"Consumer Electronics\",\n    \"GicSector\": \"Information Technology\",\n    \"GicGroup\": \"Technology Hardware & Equipment\",\n    \"GicIndustry\": \"Technology Hardware, Storage & Peripherals\",\n    \"GicSubIndustry\": \"Technology Hardware, Storage & Peripherals\",\n    \"HomeCategory\": \"Domestic\",\n    \"IsDelisted\": false,\n    \"Description\": \"Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts, as well as advertising services include third-party licensing arrangements and its own advertising platforms. In addition, the company offers various subscription-based services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was founded in 1976 and is headquartered in Cupertino, California.\",\n    \"Address\": \"One Apple Park Way, Cupertino, CA, United States, 95014\",\n    \"AddressData\": {\n      \"Street\": \"One Apple Park Way\",\n      \"City\": \"Cupertino\",\n      \"State\": \"CA\",\n      \"Country\": \"United States\",\n      \"ZIP\": \"95014\"\n    },\n    \"Listings\": {\n      \"0\": {\n        \"Code\": \"0R2V\",\n        \"Exchange\": \"LSE\",\n        \"Name\": \"Apple Inc.\"\n      },\n      \"1\": {\n        \"Code\": \"AAPL\",\n        \"Exchange\": \"BA\",\n        \"Name\": \"Apple Inc DRC\"\n      },\n      \"2\": {\n        \"Code\": \"AAPL34\",\n        \"Exchange\": \"SA\",\n        \"Name\": \"Apple Inc\"\n      }\n    },\n    \"Officers\": {\n      \"0\": {\n        \"Name\": \"Mr. Timothy D. Cook\",\n        \"Title\": \"CEO & Director\",\n        \"YearBorn\": \"1961\"\n      },\n      \"1\": {\n        \"Name\": \"Mr. Jeffrey E. Williams\",\n        \"Title\": \"Chief Operating Officer\",\n        \"YearBorn\": \"1964\"\n      },\n      \"2\": {\n        \"Name\": \"Ms. Katherine L. Adams\",\n        \"Title\": \"Senior VP, General Counsel & Secretary\",\n        \"YearBorn\": \"1964\"\n      },\n      \"3\": {\n        \"Name\": \"Ms. Deirdre  O'Brien\",\n        \"Title\": \"Chief People Officer & Senior VP of Retail\",\n        \"YearBorn\": \"1967\"\n      },\n      \"4\": {\n        \"Name\": \"Mr. Kevan  Parekh\",\n        \"Title\": \"Senior VP & CFO\",\n        \"YearBorn\": \"1972\"\n      },\n      \"5\": {\n        \"Name\": \"Mr. Chris  Kondo\",\n        \"Title\": \"Senior Director of Corporate Accounting\",\n        \"YearBorn\": \"NA\"\n      },\n      \"6\": {\n        \"Name\": \"Suhasini  Chandramouli\",\n        \"Title\": \"Director of Investor Relations\",\n        \"YearBorn\": \"NA\"\n      },\n      \"7\": {\n        \"Name\": \"Mr. Greg  Joswiak\",\n        \"Title\": \"Senior Vice President of Worldwide Marketing\",\n        \"YearBorn\": \"NA\"\n      },\n      \"8\": {\n        \"Name\": \"Mr. Adrian  Perica\",\n        \"Title\": \"Head of Corporate Development\",\n        \"YearBorn\": \"1974\"\n      },\n      \"9\": {\n        \"Name\": \"Mr. Michael  Fenger\",\n        \"Title\": \"VP of Worldwide Sales\",\n        \"YearBorn\": \"NA\"\n      }\n    },\n    \"Phone\": \"(408) 996-1010\",\n    \"WebURL\": \"https://www.apple.com\",\n    \"LogoURL\": \"/img/logos/US/aapl.png\",\n    \"FullTimeEmployees\": 164000,\n    \"UpdatedAt\": \"2025-01-21\"\n  },\n  \"Highlights\": {\n    \"MarketCapitalization\": 3458400518144,\n    \"MarketCapitalizationMln\": 3458400.5181,\n    \"EBITDA\": 134660997120,\n    \"PERatio\": 37.8639,\n    \"PEGRatio\": 2.0958,\n    \"WallStreetTargetPrice\": 246.1405,\n    \"BookValue\": 3.767,\n    \"DividendShare\": 0.98,\n    \"DividendYield\": 0.0043,\n    \"EarningsShare\": 5.88,\n    \"EPSEstimateCurrentYear\": 7.368,\n    \"EPSEstimateNextYear\": 8.2441,\n    \"EPSEstimateNextQuarter\": 2.38,\n    \"EPSEstimateCurrentQuarter\": 1.6,\n    \"MostRecentQuarter\": \"2024-09-30\",\n    \"ProfitMargin\": 0.2397,\n    \"OperatingMarginTTM\": 0.3117,\n    \"ReturnOnAssetsTTM\": 0.2146,\n    \"ReturnOnEquityTTM\": 1.5741,\n    \"RevenueTTM\": 391034994688,\n    \"RevenuePerShareTTM\": 25.485,\n    \"QuarterlyRevenueGrowthYOY\": 0.061,\n    \"GrossProfitTTM\": 180682997760,\n    \"DilutedEpsTTM\": 5.88,\n    \"QuarterlyEarningsGrowthYOY\": -0.341\n  },\n  \"Valuation\": {\n    \"TrailingPE\": 37.8639,\n    \"ForwardPE\": 30.7692,\n    \"PriceSalesTTM\": 8.8442,\n    \"PriceBookMRQ\": 60.7271,\n    \"EnterpriseValue\": 3499868262520,\n    \"EnterpriseValueRevenue\": 8.9503,\n    \"EnterpriseValueEbitda\": 25.9902\n  },\n  \"SharesStats\": {\n    \"SharesOutstanding\": 15037899776,\n    \"SharesFloat\": 15091184209,\n    \"PercentInsiders\": 2.0660000000000003,\n    \"PercentInstitutions\": 62.25000000000001,\n    \"SharesShort\": null,\n    \"SharesShortPriorMonth\": null,\n    \"ShortRatio\": null,\n    \"ShortPercentOutstanding\": null,\n    \"ShortPercentFloat\": 0.0104\n  },\n  \"Technicals\": {\n    \"Beta\": 1.24,\n    \"52WeekHigh\": 260.1,\n    \"52WeekLow\": 163.4884,\n    \"50DayMA\": 239.2966,\n    \"200DayMA\": 217.0157,\n    \"SharesShort\": 157008120,\n    \"SharesShortPriorMonth\": 156458273,\n    \"ShortRatio\": 3.37,\n    \"ShortPercent\": 0.0104\n  },\n  \"SplitsDividends\": {\n    \"ForwardAnnualDividendRate\": 1,\n    \"ForwardAnnualDividendYield\": 0.0043,\n    \"PayoutRatio\": 0.1467,\n    \"DividendDate\": \"2024-11-14\",\n    \"ExDividendDate\": \"2024-11-08\",\n    \"LastSplitFactor\": \"4:1\",\n    \"LastSplitDate\": \"2020-08-31\",\n    \"NumberDividendsByYear\": {\n      \"0\": {\n        \"Year\": 1987,\n        \"Count\": 3\n      },\n      \"1\": {\n        \"Year\": 1988,\n        \"Count\": 4\n      },\n      \"2\": {\n        \"Year\": 1989,\n        \"Count\": 4\n      },\n      \"3\": {\n        \"Year\": 1990,\n        \"Count\": 4\n      },\n      \"4\": {\n        \"Year\": 1991,\n        \"Count\": 4\n      },\n      \"5\": {\n        \"Year\": 1992,\n        \"Count\": 4\n      },\n      \"6\": {\n        \"Year\": 1993,\n        \"Count\": 4\n      },\n      \"7\": {\n        \"Year\": 1994,\n        \"Count\": 4\n      },\n      \"8\": {\n        \"Year\": 1995,\n        \"Count\": 4\n      },\n      \"9\": {\n        \"Year\": 2012,\n        \"Count\": 2\n      },\n      \"10\": {\n        \"Year\": 2013,\n        \"Count\": 4\n      },\n      \"11\": {\n        \"Year\": 2014,\n        \"Count\": 4\n      },\n      \"12\": {\n        \"Year\": 2015,\n        \"Count\": 4\n      },\n      \"13\": {\n        \"Year\": 2016,\n        \"Count\": 4\n      },\n      \"14\": {\n        \"Year\": 2017,\n        \"Count\": 4\n      },\n      \"15\": {\n        \"Year\": 2018,\n        \"Count\": 4\n      },\n      \"16\": {\n        \"Year\": 2019,\n        \"Count\": 4\n      },\n      \"17\": {\n        \"Year\": 2020,\n        \"Count\": 4\n      },\n      \"18\": {\n        \"Year\": 2021,\n        \"Count\": 4\n      },\n      \"19\": {\n        \"Year\": 2022,\n        \"Count\": 4\n      },\n      \"20\": {\n        \"Year\": 2023,\n        \"Count\": 4\n      },\n      \"21\": {\n        \"Year\": 2024,\n        \"Count\": 4\n      }\n    }\n  },\n  \"AnalystRatings\": {\n    \"Rating\": 4.1064,\n    \"TargetPrice\": 247.925,\n    \"StrongBuy\": 24,\n    \"Buy\": 8,\n    \"Hold\": 12,\n    \"Sell\": 2,\n    \"StrongSell\": 1\n  },\n  \"Holders\": {\n    \"Institutions\": {\n      \"0\": {\n        \"name\": \"Vanguard Group Inc\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 8.9087,\n        \"totalAssets\": 5.6185,\n        \"currentShares\": 1346616669,\n        \"change\": 21646442,\n        \"change_p\": 1.6337\n      },\n      \"1\": {\n        \"name\": \"BlackRock Inc\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 7.2349,\n        \"totalAssets\": 5.349,\n        \"currentShares\": 1093618174,\n        \"change\": 43402422,\n        \"change_p\": 4.1327\n      },\n      \"2\": {\n        \"name\": \"State Street Corp\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 3.8636,\n        \"totalAssets\": 5.5369,\n        \"currentShares\": 584010284,\n        \"change\": 55935105,\n        \"change_p\": 10.5923\n      },\n      \"3\": {\n        \"name\": \"FMR Inc\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 2.4071,\n        \"totalAssets\": 5.1587,\n        \"currentShares\": 363859362,\n        \"change\": 18224005,\n        \"change_p\": 5.2726\n      },\n      \"4\": {\n        \"name\": \"Geode Capital Management, LLC\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 2.2087,\n        \"totalAssets\": 6.279,\n        \"currentShares\": 333857500,\n        \"change\": 20483787,\n        \"change_p\": 6.5365\n      },\n      \"5\": {\n        \"name\": \"Berkshire Hathaway Inc\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 1.9847,\n        \"totalAssets\": 26.2408,\n        \"currentShares\": 300000000,\n        \"change\": -100000000,\n        \"change_p\": -25\n      },\n      \"6\": {\n        \"name\": \"T. Rowe Price Associates, Inc.\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 1.5585,\n        \"totalAssets\": 6.3197,\n        \"currentShares\": 235581369,\n        \"change\": 7092591,\n        \"change_p\": 3.1041\n      },\n      \"7\": {\n        \"name\": \"Morgan Stanley - Brokerage Accounts\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 1.5312,\n        \"totalAssets\": 3.9098,\n        \"currentShares\": 231460925,\n        \"change\": -230605955,\n        \"change_p\": -49.9075\n      },\n      \"8\": {\n        \"name\": \"JPMorgan Chase & Co\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 1.1829,\n        \"totalAssets\": 3.1757,\n        \"currentShares\": 178809389,\n        \"change\": -1977742,\n        \"change_p\": -1.094\n      },\n      \"9\": {\n        \"name\": \"NORGES BANK\",\n        \"date\": \"2024-06-30\",\n        \"totalShares\": 1.1745,\n        \"totalAssets\": 5.5863,\n        \"currentShares\": 177534454,\n        \"change\": 1393251,\n        \"change_p\": 0.791\n      },\n      \"10\": {\n        \"name\": \"Legal & General Group PLC\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 1.0255,\n        \"totalAssets\": 7.5272,\n        \"currentShares\": 155016460,\n        \"change\": 9426269,\n        \"change_p\": 6.4745\n },\n      \"11\": {\n        \"name\": \"Northern Trust Corp\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 1.001,\n        \"totalAssets\": 5.7712,\n        \"currentShares\": 151306059,\n        \"change\": -1653534,\n        \"change_p\": -1.081\n      },\n      \"12\": {\n        \"name\": \"Bank of New York Mellon Corp\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.7255,\n        \"totalAssets\": 4.7522,\n        \"currentShares\": 109672738,\n        \"change\": -2720923,\n        \"change_p\": -2.4209\n      },\n      \"13\": {\n        \"name\": \"Wellington Management Company LLP\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.6377,\n        \"totalAssets\": 3.9336,\n        \"currentShares\": 96394516,\n        \"change\": -7523962,\n        \"change_p\": -7.2403\n      },\n      \"14\": {\n        \"name\": \"Charles Schwab Investment Management Inc\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.6281,\n        \"totalAssets\": 4.2221,\n        \"currentShares\": 94942731,\n        \"change\": 5893741,\n        \"change_p\": 6.6185\n      },\n      \"15\": {\n        \"name\": \"International Assets Investment Management, LLC\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.6242,\n        \"totalAssets\": 1.602,\n        \"currentShares\": 94347510,\n        \"change\": 93886664,\n        \"change_p\": 20372.6763\n      },\n      \"16\": {\n        \"name\": \"UBS Asset Mgmt Americas Inc\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.6058,\n        \"totalAssets\": 5.4811,\n        \"currentShares\": 91568390,\n        \"change\": 1742087,\n        \"change_p\": 1.9394\n      },\n      \"17\": {\n        \"name\": \"Goldman Sachs Group Inc\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.5723,\n        \"totalAssets\": 3.2457,\n        \"currentShares\": 86514737,\n        \"change\": -4060063,\n        \"change_p\": -4.4826\n      },\n      \"18\": {\n        \"name\": \"Nuveen Asset Management, LLC\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.5461,\n        \"totalAssets\": 5.3998,\n        \"currentShares\": 82544919,\n        \"change\": 114810,\n        \"change_p\": 0.1393\n      },\n      \"19\": {\n        \"name\": \"Bank of America Corp\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.5352,\n        \"totalAssets\": 1.5647,\n        \"currentShares\": 80893112,\n        \"change\": -41754942,\n        \"change_p\": -34.0445\n      }\n    },\n    \"Funds\": {\n      \"0\": {\n        \"name\": \"Vanguard Total Stock Mkt Idx Inv\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 3.1349,\n        \"totalAssets\": 6.6656,\n        \"currentShares\": 473862940,\n        \"change\": 19839097,\n        \"change_p\": 4.3696\n      },\n      \"1\": {\n        \"name\": \"Vanguard Institutional 500 Index Trust\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 2.7081,\n        \"totalAssets\": 7.5955,\n        \"currentShares\": 409358272,\n        \"change\": 564051,\n        \"change_p\": 0.138\n      },\n      \"2\": {\n        \"name\": \"SPDR® S&P 500® ETF Trust\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 1.2573,\n        \"totalAssets\": 7.577,\n        \"currentShares\": 190052772,\n        \"change\": 2195583,\n        \"change_p\": 1.1688\n      },\n      \"3\": {\n        \"name\": \"Fidelity 500 Index\",\n        \"date\": \"2024-11-30\",\n        \"totalShares\": 1.2429,\n        \"totalAssets\": 7.0594,\n        \"currentShares\": 187875400,\n        \"change\": 1276562,\n        \"change_p\": 0.6841\n      },\n      \"4\": {\n        \"name\": \"iShares Core S&P 500 ETF\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 1.1742,\n        \"totalAssets\": 7.5829,\n        \"currentShares\": 177489633,\n        \"change\": 124754,\n        \"change_p\": 0.0703\n      },\n      \"5\": {\n        \"name\": \"Vanguard Growth Index Investor\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 1.0081,\n        \"totalAssets\": 13.3816,\n        \"currentShares\": 152389527,\n        \"change\": 15492874,\n        \"change_p\": 11.3172\n      },\n      \"6\": {\n        \"name\": \"Invesco QQQ Trust\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.8242,\n        \"totalAssets\": 9.7861,\n        \"currentShares\": 124587040,\n        \"change\": 1318284,\n        \"change_p\": 1.0694\n      },\n      \"7\": {\n        \"name\": \"Vanguard Institutional Index I\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.6311,\n        \"totalAssets\": 7.5888,\n        \"currentShares\": 95397328,\n        \"change\": -843973,\n        \"change_p\": -0.8769\n      },\n      \"8\": {\n        \"name\": \"State St S&P 500® Indx SL Cl III\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.4803,\n        \"totalAssets\": 7.5299,\n        \"currentShares\": 72601766,\n        \"change\": -1068251,\n        \"change_p\": -1.45\n      },\n      \"9\": {\n        \"name\": \"Vanguard Information Technology ETF\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.4498,\n        \"totalAssets\": 17.0521,\n        \"currentShares\": 67990581,\n        \"change\": 984400,\n        \"change_p\": 1.4691\n      },\n      \"10\": {\n        \"name\": \"Blackrock Eq Idx Fund CF\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.3756,\n        \"totalAssets\": 7.5672,\n        \"currentShares\": 56769608,\n        \"change\": -776204,\n        \"change_p\": -1.3488\n      },\n      \"11\": {\n        \"name\": \"iShares Russell 1000 Growth ETF\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.3424,\n        \"totalAssets\": 12.1741,\n        \"currentShares\": 51756198,\n        \"change\": 29274,\n        \"change_p\": 0.0566\n      },\n      \"12\": {\n        \"name\": \"Blackrock Russ 1000 Eq Idx Composite\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.2988,\n        \"totalAssets\": 6.417,\n        \"currentShares\": 45164357,\n        \"change\": 951090,\n        \"change_p\": 2.1511\n      },\n      \"13\": {\n        \"name\": \"The Technology Select Sector SPDR® ETF\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.2963,\n        \"totalAssets\": 15.4199,\n        \"currentShares\": 44794398,\n        \"change\": -71720,\n        \"change_p\": -0.1599\n      },\n      \"14\": {\n        \"name\": \"Russell 1000 Index Fund\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.2912,\n        \"totalAssets\": 6.5995,\n        \"currentShares\": 44017897,\n        \"change\": -572224,\n        \"change_p\": -1.2833\n      },\n      \"15\": {\n        \"name\": \"Fidelity Growth Compy Commingled Pl S\",\n        \"date\": \"2024-11-30\",\n        \"totalShares\": 0.2344,\n        \"totalAssets\": 8.9357,\n        \"currentShares\": 35427666,\n        \"change\": -1414616,\n        \"change_p\": -3.8397\n      },\n      \"16\": {\n        \"name\": \"iShares Core S&P 500 ETF USD Acc\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.2219,\n        \"totalAssets\": 7.592,\n        \"currentShares\": 33539284,\n        \"change\": 16640,\n        \"change_p\": 0.0496\n      },\n      \"17\": {\n        \"name\": \"Fidelity Blue Chip Growth\",\n        \"date\": \"2024-11-30\",\n        \"totalShares\": 0.2187,\n        \"totalAssets\": 10.7883,\n        \"currentShares\": 33053745,\n        \"change\": -586300,\n        \"change_p\": -1.7429\n      },\n      \"18\": {\n        \"name\": \"Schwab® S&P 500 Index\",\n        \"date\": \"2024-12-31\",\n        \"totalShares\": 0.218,\n        \"totalAssets\": 7.5465,\n        \"currentShares\": 32947697,\n        \"change\": -28502,\n        \"change_p\": -0.0864\n      },\n      \"19\": {\n        \"name\": \"Capital Group Growth Fnd of Amer Comp\",\n        \"date\": \"2024-09-30\",\n        \"totalShares\": 0.1977,\n        \"totalAssets\": 2.385,\n        \"currentShares\": 29887753,\n        \"change\": 1726645,\n        \"change_p\": 6.1313\n      }\n    }\n  },\n  \"InsiderTransactions\": {\n    \"0\": {\n      \"date\": \"2025-01-02\",\n      \"ownerCik\": null,\n      \"ownerName\": \"James Comer\",\n      \"transactionDate\": \"2025-01-02\",\n      \"transactionCode\": \"P\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 243.85,\n      \"transactionAcquiredDisposed\": \"A\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"1\": {\n      \"date\": \"2024-12-31\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Nancy Pelosi\",\n      \"transactionDate\": \"2024-12-31\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 250.42,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"2\": {\n      \"date\": \"2024-12-19\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Josh Gottheimer\",\n      \"transactionDate\": \"2024-12-19\",\n      \"transactionCode\": \"P\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 249.79,\n      \"transactionAcquiredDisposed\": \"A\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"3\": {\n      \"date\": \"2024-12-19\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Sheldon Whitehouse\",\n      \"transactionDate\": \"2024-12-19\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 249.79,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"4\": {\n      \"date\": \"2024-12-16\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Jeffrey E Williams\",\n      \"transactionDate\": \"2024-12-16\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 100000,\n      \"transactionPrice\": 249.97,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": \"http://www.sec.gov/Archives/edgar/data/320193/000032019324000132/xslF345X05/wk-form4_1734564614.xml\"\n    },\n    \"5\": {\n      \"date\": \"2024-11-18\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Chris Kondo\",\n      \"transactionDate\": \"2024-11-18\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 4130,\n      \"transactionPrice\": 228.87,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": \"http://www.sec.gov/Archives/edgar/data/320193/000032019324000129/xslF345X05/wk-form4_1732059042.xml\"\n    },\n    \"6\": {\n      \"date\": \"2024-11-01\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Marjorie Taylor Greene\",\n      \"transactionDate\": \"2024-11-01\",\n      \"transactionCode\": \"P\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 222.91,\n      \"transactionAcquiredDisposed\": \"A\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"7\": {\n      \"date\": \"2024-10-29\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Tommy Tuberville\",\n      \"transactionDate\": \"2024-10-29\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 233.67,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"8\": {\n      \"date\": \"2024-10-07\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Laurel M. Lee\",\n      \"transactionDate\": \"2024-10-07\",\n      \"transactionCode\": \"P\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 221.69,\n      \"transactionAcquiredDisposed\": \"A\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"9\": {\n      \"date\": \"2024-10-07\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Thomas R. Suozzi\",\n      \"transactionDate\": \"2024-10-07\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 221.69,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"10\": {\n      \"date\": \"2024-10-04\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Luca Maestri\",\n      \"transactionDate\": \"2024-10-04\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 59305,\n      \"transactionPrice\": 226.52,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": \"http://www.sec.gov/Archives/edgar/data/320193/000032019324000114/xslF345X05/wk-form4_1728426607.xml\"\n    },\n    \"11\": {\n      \"date\": \"2024-10-02\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Josh Gottheimer\",\n      \"transactionDate\": \"2024-10-02\",\n      \"transactionCode\": \"P\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 226.78,\n      \"transactionAcquiredDisposed\": \"A\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n    },\n    \"12\": {\n      \"date\": \"2024-10-02\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Timothy D Cook\",\n      \"transactionDate\": \"2024-10-02\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 223986,\n      \"transactionPrice\": 224.46,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": \"http://www.sec.gov/Archives/edgar/data/320193/000032019324000109/xslF345X05/wk-form4_1727994624.xml\"\n    },\n    \"13\": {\n      \"date\": \"2024-10-02\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Jeffrey E Williams\",\n      \"transactionDate\": \"2024-10-02\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 59730,\n      \"transactionPrice\": 226.86,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": \"http://www.sec.gov/Archives/edgar/data/320193/000032019324000112/xslF345X05/wk-form4_1727994654.xml\"\n    },\n    \"14\": {\n      \"date\": \"2024-10-02\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Katherine L Adams\",\n      \"transactionDate\": \"2024-10-02\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 61019,\n      \"transactionPrice\": 226.2,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": \"http://www.sec.gov/Archives/edgar/data/320193/000032019324000108/xslF345X05/wk-form4_1727994612.xml\"\n    },\n    \"15\": {\n      \"date\": \"2024-09-20\",\n      \"ownerCik\": null,\n      \"ownerName\": \"Shelley Moore Capito\",\n      \"transactionDate\": \"2024-09-20\",\n      \"transactionCode\": \"S\",\n      \"transactionAmount\": 0,\n      \"transactionPrice\": 228.2,\n      \"transactionAcquiredDisposed\": \"D\",\n      \"postTransactionAmount\": null,\n      \"secLink\": null\n.....\n```\n\n```text\n...\n\"HistoricalComponents\": {\n    \"2020-01-28\": {\n      \"0\": {\n        \"Date\": \"2020-01-28\",\n        \"Code\": \"AIZ\",\n        \"Exchange\": \"US\",\n        \"Name\": \"Assurant Inc\",\n        \"Sector\": \"Financial Services\",\n        \"Industry\": \"Insurance - Property & Casualty\"\n      },\n      \"1\": {\n        \"Date\": \"2020-01-28\",\n        \"Code\": \"MNST\",\n        \"Exchange\": \"US\",\n        \"Name\": \"Monster Beverage Corp\",\n        \"Sector\": \"Consumer Defensive\",\n        \"Industry\": \"Beverages - Non-Alcoholic\"\n      },\n      \"2\": {\n        \"Date\": \"2020-01-28\",\n        \"Code\": \"GPS\",\n        \"Exchange\": \"US\",\n        \"Name\": \"Gap Inc\",\n        \"Sector\": \"Consumer Cyclical\",\n        \"Industry\": \"Apparel Retail\"\n      },\n      \"3\": {\n        \"Date\": \"2020-01-28\",\n        \"Code\": \"UNM\",\n        \"Exchange\": \"US\",\n        \"Name\": \"Unum Group\",\n        \"Sector\": \"Financial Services\",\n        \"Industry\": \"Insurance - Life\"\n      },\n      \"4\": {\n        \"Date\": \"2020-01-28\",\n        \"Code\": \"PGR\",\n        \"Exchange\": \"US\",\n        \"Name\": \"Progressive Corp\",\n        \"Sector\": \"Financial Services\",\n        \"Industry\": \"Insurance - Property & Casualty\"\n      },\n      \"5\": {\n        \"Date\": \"2020-01-28\",\n        \"Code\": \"CSX\",\n        \"Exchange\": \"US\",\n        \"Name\": \"CSX Corporation\",\n        \"Sector\": \"Industrials\",\n        \"Industry\": \"Railroads\"\n      },\n      \"6\": {\n        \"Date\": \"2020-01-28\",\n        \"Code\": \"ADP\",\n        \"Exchange\": \"US\",\n        \"Name\": \"Automatic Data Processing Inc\",\n        \"Sector\": \"Technology\",\n        \"Industry\": \"Software - Application\"\n      },\n      \"7\": {\n        \"Date\": \"2020-01-28\",\n        \"Code\": \"ANSS\",\n        \"Exchange\": \"US\",\n        \"Name\": \"ANSYS Inc\",\n        \"Sector\": \"Technology\",\n        \"Industry\": \"Software - Application\"\n...\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "stock-etfs-fundamental-data-feeds"
---

# Fundamental Data: Stocks, ETFs, Mutual Funds, Indices

## 源URL

https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds/?preview=true

## 描述

Simple access to fundamental data API for stocks, ETFs, Mutual Funds, and Indices from different exchanges and countries. Almost all major US, UK, EU and Asia exchanges.Since we provide extensive fundamental data, especially for stocks, the response can be large and include many data sections (see the full list of fields below). To manage this, you have the option to retrieve a specific section or a single field using filters. Read more about this feature below.

## API 端点

**Endpoint**: `https://eodhd.com/api/fundamentals/AAPL.US`

## 文档正文

Simple access to fundamental data API for stocks, ETFs, Mutual Funds, and Indices from different exchanges and countries. Almost all major US, UK, EU and Asia exchanges.Since we provide extensive fundamental data, especially for stocks, the response can be large and include many data sections (see the full list of fields below). To manage this, you have the option to retrieve a specific section or a single field using filters. Read more about this feature below.

## API Endpoint

```text
https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json
```

```text
https://eodhd.com/api/fundamentals/AAPL.US?filter=General::Code&api_token=demo&fmt=json
```

```text
https://eodhd.com/api/fundamentals/AAPL.US?filter=Financials::Balance_Sheet::yearly&api_token=demo&fmt=json
```

## Quick Start

Request example:

## Stocks Fundamentals Data API

For stocks, we provide the following data fields:

General Company Details:

Financial Highlights and Key Metrics:

Market Valuation Metrics:

Shareholder & Ownership Data:

Technical Performance Metrics:

Splits and Dividends:

Institutional Holders:

Insider Transactions (Form 4):

* all listed fields are available in the standalone Insider Transactions APIOutstanding Shares:

Financial Reports:

This is a JSON response example for the AAPL ticker. Only a portion of the data is shown in this code section. To retrieve the full data for AAPL, even with the “demo” key, perform the request in your browser manually or click here to open the full request in a new tab.

## Partial Data Retrieval using filters: Web-service support

Since we provide extensive fundamental data, especially for stocks, the response can be large and, as you saw above, include many data sections. To manage this, you have the option to retrieve a specific section or a single field using the parameter ‘filter=’. Section names and field names can be referenced from the AAPL response example. Multi-layer filtering is also supported. For example, if you want to retrieve only the ‘General’ block, use the following request:

Different filter layers are separated by “::” and can have any number of layers as needed. For example:

It’s also possible to use multiple comma-separated filters. For example:

## Equities Fundamentals Data API

We support the following data for Equity symbols:

General Data and Fundamental Highlights:

Includes sector, industry, company description, market capitalization, EBITDA, book value, dividend share, dividend yield, earnings per share (EPS), estimated EPS for the current and next year/quarter, and price-to-earnings (P/E) ratio.

Financial Reports (We support both US and non-US companies):

Please note that not all companies report complete financial data, so some data points may be unavailable for certain companies.

## ETFs Fundamentals Data API

We also support details for more than 10,000 ETFs from different exchanges and countries. Here you can find the ETF Information and details we support at the moment.

## Funds Fundamentals Data API

We support more than 20.000 US Mutual Funds. Our database has equity funds as well as balanced and bond-based mutual funds. We support all major information about almost all mutual funds on the market, including:

It’s also possible to get data from Mutual Fund by ticker. For example, for “Schwab S&P 500 Index” both identifications are correct: SWPPX.US and US8085098551.

Here is an example of the structure for Charles Schwab fund “Schwab S&P 500 Index” provided by our fundamentals API. And do not forget that we also have End-Of-Day with our Stock Price Data API (End-Of-Day Historical Data) and Live data with our Live/Real-time Stock Prices API for SWPPX and other funds.

## Current and Historical Index Constituents API

Available data for each Component:

2. Historical data. A list of all components that have ever been in an index is available for the following indices. To view this section in JSON response, purchase the Indices Historical Constituents Data API (this data is part of that dataset).Available indices:

The response includes not only the current list of active constituents but non-active constituents (those previously included in an index) as well, along with the dates of their addition and exclusion. Non-active constituents are available under the “HistoricalTickerComponents” section of the response. Plus there is an additional data field “Weight” (based on “free float market cap” for S&P and “price-weighted” for DJ).

The query example:

Response example for S&P 500 (GSPC.INDX):

## Historical Constituents for the S&P 500 (GSPC)

Through the Fundamentals API package, Historical data for the S&P 500 (also known as GSPC or simply S&P) is available in the form of snapshots for each date, providing the list of all 500 components for a specific date. We track the data from the 1960s, though the most complete data starts from 2016.

Request example:

Response example (“HistoricalComponents” section):

## Bulk Fundamentals API

Learn how to get Fundamental Data for multiple tickers or entire exchanges here.

## Code Examples

```text
"General": {
    "Code": "AAPL",
    "Type": "Common Stock",
    "Name": "Apple Inc",
    "Exchange": "NASDAQ",
    "CurrencyCode": "USD",
    "CurrencyName": "US Dollar",
    "CurrencySymbol": "$",
    "CountryName": "USA",
    "CountryISO": "US",
    "OpenFigi": "BBG000B9XRY4",
    "ISIN": "US0378331005",
    "LEI": "HWUPKR0MPOU8FGXBT394",
    "PrimaryTicker": "AAPL.US",
    "CUSIP": "037833100",
    "CIK": "320193",
    "EmployerIdNumber": "94-2404110",
    "FiscalYearEnd": "September",
    "IPODate": "1980-12-12",
    "InternationalDomestic": "International/Domestic",
    "Sector": "Technology",
    "Industry": "Consumer Electronics",
    "GicSector": "Information Technology",
    "GicGroup": "Technology Hardware & Equipment",
    "GicIndustry": "Technology Hardware, Storage & Peripherals",
    "GicSubIndustry": "Technology Hardware, Storage & Peripherals",
    "HomeCategory": "Domestic",
    "IsDelisted": false,
    "Description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts, as well as advertising services include third-party licensing arrangements and its own advertising platforms. In addition, the company offers various subscription-based services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was founded in 1976 and is headquartered in Cupertino, California.",
    "Address": "One Apple Park Way, Cupertino, CA, United States, 95014",
    "AddressData": {
      "Street": "One Apple Park Way",
      "City": "Cupertino",
      "State": "CA",
      "Country": "United States",
      "ZIP": "95014"
    },
    "Listings": {
      "0": {
        "Code": "0R2V",
        "Exchange": "LSE",
        "Name": "Apple Inc."
      },
      "1": {
        "Code": "AAPL",
        "Exchange": "BA",
        "Name": "Apple Inc DRC"
      },
      "2": {
        "Code": "AAPL34",
        "Exchange": "SA",
        "Name": "Apple Inc"
      }
    },
    "Officers": {
      "0": {
        "Name": "Mr. Timothy D. Cook",
        "Title": "CEO & Director",
        "YearBorn": "1961"
      },
      "1": {
        "Name": "Mr. Jeffrey E. Williams",
        "Title": "Chief Operating Officer",
        "YearBorn": "1964"
      },
      "2": {
        "Name": "Ms. Katherine L. Adams",
        "Title": "Senior VP, General Counsel & Secretary",
        "YearBorn": "1964"
      },
      "3": {
        "Name": "Ms. Deirdre  O'Brien",
        "Title": "Chief People Officer & Senior VP of Retail",
        "YearBorn": "1967"
      },
      "4": {
        "Name": "Mr. Kevan  Parekh",
        "Title": "Senior VP & CFO",
        "YearBorn": "1972"
      },
      "5": {
        "Name": "Mr. Chris  Kondo",
        "Title": "Senior Director of Corporate Accounting",
        "YearBorn": "NA"
      },
      "6": {
        "Name": "Suhasini  Chandramouli",
        "Title": "Director of Investor Relations",
        "YearBorn": "NA"
      },
      "7": {
        "Name": "Mr. Greg  Joswiak",
        "Title": "Senior Vice President of Worldwide Marketing",
        "YearBorn": "NA"
      },
      "8": {
        "Name": "Mr. Adrian  Perica",
        "Title": "Head of Corporate Development",
        "YearBorn": "1974"
      },
      "9": {
        "Name": "Mr. Michael  Fenger",
        "Title": "VP of Worldwide Sales",
        "YearBorn": "NA"
      }
    },
    "Phone": "(408) 996-1010",
    "WebURL": "https://www.apple.com",
    "LogoURL": "/img/logos/US/aapl.png",
    "FullTimeEmployees": 164000,
    "UpdatedAt": "2025-01-21"
  },
  "Highlights": {
    "MarketCapitalization": 3458400518144,
    "MarketCapitalizationMln": 3458400.5181,
    "EBITDA": 134660997120,
    "PERatio": 37.8639,
    "PEGRatio": 2.0958,
    "WallStreetTargetPrice": 246.1405,
    "BookValue": 3.767,
    "DividendShare": 0.98,
    "DividendYield": 0.0043,
    "EarningsShare": 5.88,
    "EPSEstimateCurrentYear": 7.368,
    "EPSEstimateNextYear": 8.2441,
    "EPSEstimateNextQuarter": 2.38,
    "EPSEstimateCurrentQuarter": 1.6,
    "MostRecentQuarter": "2024-09-30",
    "ProfitMargin": 0.2397,
    "OperatingMarginTTM": 0.3117,
    "ReturnOnAssetsTTM": 0.2146,
    "ReturnOnEquityTTM": 1.5741,
    "RevenueTTM": 391034994688,
    "RevenuePerShareTTM": 25.485,
    "QuarterlyRevenueGrowthYOY": 0.061,
    "GrossProfitTTM": 180682997760,
    "DilutedEpsTTM": 5.88,
    "QuarterlyEarningsGrowthYOY": -0.341
  },
  "Valuation": {
    "TrailingPE": 37.8639,
    "ForwardPE": 30.7692,
    "PriceSalesTTM": 8.8442,
    "PriceBookMRQ": 60.7271,
    "EnterpriseValue": 3499868262520,
    "EnterpriseValueRevenue": 8.9503,
    "EnterpriseValueEbitda": 25.9902
  },
  "SharesStats": {
    "SharesOutstanding": 15037899776,
    "SharesFloat": 15091184209,
    "PercentInsiders": 2.0660000000000003,
    "PercentInstitutions": 62.25000000000001,
    "SharesShort": null,
    "SharesShortPriorMonth": null,
    "ShortRatio": null,
    "ShortPercentOutstanding": null,
    "ShortPercentFloat": 0.0104
  },
  "Technicals": {
    "Beta": 1.24,
    "52WeekHigh": 260.1,
    "52WeekLow": 163.4884,
    "50DayMA": 239.2966,
    "200DayMA": 217.0157,
    "SharesShort": 157008120,
    "SharesShortPriorMonth": 156458273,
    "ShortRatio": 3.37,
    "ShortPercent": 0.0104
  },
  "SplitsDividends": {
    "ForwardAnnualDividendRate": 1,
    "ForwardAnnualDividendYield": 0.0043,
    "PayoutRatio": 0.1467,
    "DividendDate": "2024-11-14",
    "ExDividendDate": "2024-11-08",
    "LastSplitFactor": "4:1",
    "LastSplitDate": "2020-08-31",
    "NumberDividendsByYear": {
      "0": {
        "Year": 1987,
        "Count": 3
      },
      "1": {
        "Year": 1988,
        "Count": 4
      },
      "2": {
        "Year": 1989,
        "Count": 4
      },
      "3": {
        "Year": 1990,
        "Count": 4
      },
      "4": {
        "Year": 1991,
        "Count": 4
      },
      "5": {
        "Year": 1992,
        "Count": 4
      },
      "6": {
        "Year": 1993,
        "Count": 4
      },
      "7": {
        "Year": 1994,
        "Count": 4
      },
      "8": {
        "Year": 1995,
        "Count": 4
      },
      "9": {
        "Year": 2012,
        "Count": 2
      },
      "10": {
        "Year": 2013,
        "Count": 4
      },
      "11": {
        "Year": 2014,
        "Count": 4
      },
      "12": {
        "Year": 2015,
        "Count": 4
      },
      "13": {
        "Year": 2016,
        "Count": 4
      },
      "14": {
        "Year": 2017,
        "Count": 4
      },
      "15": {
        "Year": 2018,
        "Count": 4
      },
      "16": {
        "Year": 2019,
        "Count": 4
      },
      "17": {
        "Year": 2020,
        "Count": 4
      },
      "18": {
        "Year": 2021,
        "Count": 4
      },
      "19": {
        "Year": 2022,
        "Count": 4
      },
      "20": {
        "Year": 2023,
        "Count": 4
      },
      "21": {
        "Year": 2024,
        "Count": 4
      }
    }
  },
  "AnalystRatings": {
    "Rating": 4.1064,
    "TargetPrice": 247.925,
    "StrongBuy": 24,
    "Buy": 8,
    "Hold": 12,
    "Sell": 2,
    "StrongSell": 1
  },
  "Holders": {
    "Institutions": {
      "0": {
        "name": "Vanguard Group Inc",
        "date": "2024-09-30",
        "totalShares": 8.9087,
        "totalAssets": 5.6185,
        "currentShares": 1346616669,
        "change": 21646442,
        "change_p": 1.6337
      },
      "1": {
        "name": "BlackRock Inc",
        "date": "2024-09-30",
        "totalShares": 7.2349,
        "totalAssets": 5.349,
        "currentShares": 1093618174,
        "change": 43402422,
        "change_p": 4.1327
      },
      "2": {
        "name": "State Street Corp",
        "date": "2024-09-30",
        "totalShares": 3.8636,
        "totalAssets": 5.5369,
        "currentShares": 584010284,
        "change": 55935105,
        "change_p": 10.5923
      },
      "3": {
        "name": "FMR Inc",
        "date": "2024-09-30",
        "totalShares": 2.4071,
        "totalAssets": 5.1587,
        "currentShares": 363859362,
        "change": 18224005,
        "change_p": 5.2726
      },
      "4": {
        "name": "Geode Capital Management, LLC",
        "date": "2024-09-30",
        "totalShares": 2.2087,
        "totalAssets": 6.279,
        "currentShares": 333857500,
        "change": 20483787,
        "change_p": 6.5365
      },
      "5": {
        "name": "Berkshire Hathaway Inc",
        "date": "2024-09-30",
        "totalShares": 1.9847,
        "totalAssets": 26.2408,
        "currentShares": 300000000,
        "change": -100000000,
        "change_p": -25
      },
      "6": {
        "name": "T. Rowe Price Associates, Inc.",
        "date": "2024-09-30",
        "totalShares": 1.5585,
        "totalAssets": 6.3197,
        "currentShares": 235581369,
        "change": 7092591,
        "change_p": 3.1041
      },
      "7": {
        "name": "Morgan Stanley - Brokerage Accounts",
        "date": "2024-09-30",
        "totalShares": 1.5312,
        "totalAssets": 3.9098,
        "currentShares": 231460925,
        "change": -230605955,
        "change_p": -49.9075
      },
      "8": {
        "name": "JPMorgan Chase & Co",
        "date": "2024-09-30",
        "totalShares": 1.1829,
        "totalAssets": 3.1757,
        "currentShares": 178809389,
        "change": -1977742,
        "change_p": -1.094
      },
      "9": {
        "name": "NORGES BANK",
        "date": "2024-06-30",
        "totalShares": 1.1745,
        "totalAssets": 5.5863,
        "currentShares": 177534454,
        "change": 1393251,
        "change_p": 0.791
      },
      "10": {
        "name": "Legal & General Group PLC",
        "date": "2024-09-30",
        "totalShares": 1.0255,
        "totalAssets": 7.5272,
        "currentShares": 155016460,
        "change": 9426269,
        "change_p": 6.4745
 },
      "11": {
        "name": "Northern Trust Corp",
        "date": "2024-09-30",
        "totalShares": 1.001,
        "totalAssets": 5.7712,
        "currentShares": 151306059,
        "change": -1653534,
        "change_p": -1.081
      },
      "12": {
        "name": "Bank of New York Mellon Corp",
        "date": "2024-09-30",
        "totalShares": 0.7255,
        "totalAssets": 4.7522,
        "currentShares": 109672738,
        "change": -2720923,
        "change_p": -2.4209
      },
      "13": {
        "name": "Wellington Management Company LLP",
        "date": "2024-09-30",
        "totalShares": 0.6377,
        "totalAssets": 3.9336,
        "currentShares": 96394516,
        "change": -7523962,
        "change_p": -7.2403
      },
      "14": {
        "name": "Charles Schwab Investment Management Inc",
        "date": "2024-09-30",
        "totalShares": 0.6281,
        "totalAssets": 4.2221,
        "currentShares": 94942731,
        "change": 5893741,
        "change_p": 6.6185
      },
      "15": {
        "name": "International Assets Investment Management, LLC",
        "date": "2024-09-30",
        "totalShares": 0.6242,
        "totalAssets": 1.602,
        "currentShares": 94347510,
        "change": 93886664,
        "change_p": 20372.6763
      },
      "16": {
        "name": "UBS Asset Mgmt Americas Inc",
        "date": "2024-09-30",
        "totalShares": 0.6058,
        "totalAssets": 5.4811,
        "currentShares": 91568390,
        "change": 1742087,
        "change_p": 1.9394
      },
      "17": {
        "name": "Goldman Sachs Group Inc",
        "date": "2024-09-30",
        "totalShares": 0.5723,
        "totalAssets": 3.2457,
        "currentShares": 86514737,
        "change": -4060063,
        "change_p": -4.4826
      },
      "18": {
        "name": "Nuveen Asset Management, LLC",
        "date": "2024-09-30",
        "totalShares": 0.5461,
        "totalAssets": 5.3998,
        "currentShares": 82544919,
        "change": 114810,
        "change_p": 0.1393
      },
      "19": {
        "name": "Bank of America Corp",
        "date": "2024-09-30",
        "totalShares": 0.5352,
        "totalAssets": 1.5647,
        "currentShares": 80893112,
        "change": -41754942,
        "change_p": -34.0445
      }
    },
    "Funds": {
      "0": {
        "name": "Vanguard Total Stock Mkt Idx Inv",
        "date": "2024-12-31",
        "totalShares": 3.1349,
        "totalAssets": 6.6656,
        "currentShares": 473862940,
        "change": 19839097,
        "change_p": 4.3696
      },
      "1": {
        "name": "Vanguard Institutional 500 Index Trust",
        "date": "2024-12-31",
        "totalShares": 2.7081,
        "totalAssets": 7.5955,
        "currentShares": 409358272,
        "change": 564051,
        "change_p": 0.138
      },
      "2": {
        "name": "SPDR® S&P 500® ETF Trust",
        "date": "2024-12-31",
        "totalShares": 1.2573,
        "totalAssets": 7.577,
        "currentShares": 190052772,
        "change": 2195583,
        "change_p": 1.1688
      },
      "3": {
        "name": "Fidelity 500 Index",
        "date": "2024-11-30",
        "totalShares": 1.2429,
        "totalAssets": 7.0594,
        "currentShares": 187875400,
        "change": 1276562,
        "change_p": 0.6841
      },
      "4": {
        "name": "iShares Core S&P 500 ETF",
        "date": "2024-12-31",
        "totalShares": 1.1742,
        "totalAssets": 7.5829,
        "currentShares": 177489633,
        "change": 124754,
        "change_p": 0.0703
      },
      "5": {
        "name": "Vanguard Growth Index Investor",
        "date": "2024-12-31",
        "totalShares": 1.0081,
        "totalAssets": 13.3816,
        "currentShares": 152389527,
        "change": 15492874,
        "change_p": 11.3172
      },
      "6": {
        "name": "Invesco QQQ Trust",
        "date": "2024-12-31",
        "totalShares": 0.8242,
        "totalAssets": 9.7861,
        "currentShares": 124587040,
        "change": 1318284,
        "change_p": 1.0694
      },
      "7": {
        "name": "Vanguard Institutional Index I",
        "date": "2024-12-31",
        "totalShares": 0.6311,
        "totalAssets": 7.5888,
        "currentShares": 95397328,
        "change": -843973,
        "change_p": -0.8769
      },
      "8": {
        "name": "State St S&P 500® Indx SL Cl III",
        "date": "2024-12-31",
        "totalShares": 0.4803,
        "totalAssets": 7.5299,
        "currentShares": 72601766,
        "change": -1068251,
        "change_p": -1.45
      },
      "9": {
        "name": "Vanguard Information Technology ETF",
        "date": "2024-12-31",
        "totalShares": 0.4498,
        "totalAssets": 17.0521,
        "currentShares": 67990581,
        "change": 984400,
        "change_p": 1.4691
      },
      "10": {
        "name": "Blackrock Eq Idx Fund CF",
        "date": "2024-12-31",
        "totalShares": 0.3756,
        "totalAssets": 7.5672,
        "currentShares": 56769608,
        "change": -776204,
        "change_p": -1.3488
      },
      "11": {
        "name": "iShares Russell 1000 Growth ETF",
        "date": "2024-12-31",
        "totalShares": 0.3424,
        "totalAssets": 12.1741,
        "currentShares": 51756198,
        "change": 29274,
        "change_p": 0.0566
      },
      "12": {
        "name": "Blackrock Russ 1000 Eq Idx Composite",
        "date": "2024-09-30",
        "totalShares": 0.2988,
        "totalAssets": 6.417,
        "currentShares": 45164357,
        "change": 951090,
        "change_p": 2.1511
      },
      "13": {
        "name": "The Technology Select Sector SPDR® ETF",
        "date": "2024-12-31",
        "totalShares": 0.2963,
        "totalAssets": 15.4199,
        "currentShares": 44794398,
        "change": -71720,
        "change_p": -0.1599
      },
      "14": {
        "name": "Russell 1000 Index Fund",
        "date": "2024-12-31",
        "totalShares": 0.2912,
        "totalAssets": 6.5995,
        "currentShares": 44017897,
        "change": -572224,
        "change_p": -1.2833
      },
      "15": {
        "name": "Fidelity Growth Compy Commingled Pl S",
        "date": "2024-11-30",
        "totalShares": 0.2344,
        "totalAssets": 8.9357,
        "currentShares": 35427666,
        "change": -1414616,
        "change_p": -3.8397
      },
      "16": {
        "name": "iShares Core S&P 500 ETF USD Acc",
        "date": "2024-12-31",
        "totalShares": 0.2219,
        "totalAssets": 7.592,
        "currentShares": 33539284,
        "change": 16640,
        "change_p": 0.0496
      },
      "17": {
        "name": "Fidelity Blue Chip Growth",
        "date": "2024-11-30",
        "totalShares": 0.2187,
        "totalAssets": 10.7883,
        "currentShares": 33053745,
        "change": -586300,
        "change_p": -1.7429
      },
      "18": {
        "name": "Schwab® S&P 500 Index",
        "date": "2024-12-31",
        "totalShares": 0.218,
        "totalAssets": 7.5465,
        "currentShares": 32947697,
        "change": -28502,
        "change_p": -0.0864
      },
      "19": {
        "name": "Capital Group Growth Fnd of Amer Comp",
        "date": "2024-09-30",
        "totalShares": 0.1977,
        "totalAssets": 2.385,
        "currentShares": 29887753,
        "change": 1726645,
        "change_p": 6.1313
      }
    }
  },
  "InsiderTransactions": {
    "0": {
      "date": "2025-01-02",
      "ownerCik": null,
      "ownerName": "James Comer",
      "transactionDate": "2025-01-02",
      "transactionCode": "P",
      "transactionAmount": 0,
      "transactionPrice": 243.85,
      "transactionAcquiredDisposed": "A",
      "postTransactionAmount": null,
      "secLink": null
    },
    "1": {
      "date": "2024-12-31",
      "ownerCik": null,
      "ownerName": "Nancy Pelosi",
      "transactionDate": "2024-12-31",
      "transactionCode": "S",
      "transactionAmount": 0,
      "transactionPrice": 250.42,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": null
    },
    "2": {
      "date": "2024-12-19",
      "ownerCik": null,
      "ownerName": "Josh Gottheimer",
      "transactionDate": "2024-12-19",
      "transactionCode": "P",
      "transactionAmount": 0,
      "transactionPrice": 249.79,
      "transactionAcquiredDisposed": "A",
      "postTransactionAmount": null,
      "secLink": null
    },
    "3": {
      "date": "2024-12-19",
      "ownerCik": null,
      "ownerName": "Sheldon Whitehouse",
      "transactionDate": "2024-12-19",
      "transactionCode": "S",
      "transactionAmount": 0,
      "transactionPrice": 249.79,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": null
    },
    "4": {
      "date": "2024-12-16",
      "ownerCik": null,
      "ownerName": "Jeffrey E Williams",
      "transactionDate": "2024-12-16",
      "transactionCode": "S",
      "transactionAmount": 100000,
      "transactionPrice": 249.97,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": "http://www.sec.gov/Archives/edgar/data/320193/000032019324000132/xslF345X05/wk-form4_1734564614.xml"
    },
    "5": {
      "date": "2024-11-18",
      "ownerCik": null,
      "ownerName": "Chris Kondo",
      "transactionDate": "2024-11-18",
      "transactionCode": "S",
      "transactionAmount": 4130,
      "transactionPrice": 228.87,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": "http://www.sec.gov/Archives/edgar/data/320193/000032019324000129/xslF345X05/wk-form4_1732059042.xml"
    },
    "6": {
      "date": "2024-11-01",
      "ownerCik": null,
      "ownerName": "Marjorie Taylor Greene",
      "transactionDate": "2024-11-01",
      "transactionCode": "P",
      "transactionAmount": 0,
      "transactionPrice": 222.91,
      "transactionAcquiredDisposed": "A",
      "postTransactionAmount": null,
      "secLink": null
    },
    "7": {
      "date": "2024-10-29",
      "ownerCik": null,
      "ownerName": "Tommy Tuberville",
      "transactionDate": "2024-10-29",
      "transactionCode": "S",
      "transactionAmount": 0,
      "transactionPrice": 233.67,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": null
    },
    "8": {
      "date": "2024-10-07",
      "ownerCik": null,
      "ownerName": "Laurel M. Lee",
      "transactionDate": "2024-10-07",
      "transactionCode": "P",
      "transactionAmount": 0,
      "transactionPrice": 221.69,
      "transactionAcquiredDisposed": "A",
      "postTransactionAmount": null,
      "secLink": null
    },
    "9": {
      "date": "2024-10-07",
      "ownerCik": null,
      "ownerName": "Thomas R. Suozzi",
      "transactionDate": "2024-10-07",
      "transactionCode": "S",
      "transactionAmount": 0,
      "transactionPrice": 221.69,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": null
    },
    "10": {
      "date": "2024-10-04",
      "ownerCik": null,
      "ownerName": "Luca Maestri",
      "transactionDate": "2024-10-04",
      "transactionCode": "S",
      "transactionAmount": 59305,
      "transactionPrice": 226.52,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": "http://www.sec.gov/Archives/edgar/data/320193/000032019324000114/xslF345X05/wk-form4_1728426607.xml"
    },
    "11": {
      "date": "2024-10-02",
      "ownerCik": null,
      "ownerName": "Josh Gottheimer",
      "transactionDate": "2024-10-02",
      "transactionCode": "P",
      "transactionAmount": 0,
      "transactionPrice": 226.78,
      "transactionAcquiredDisposed": "A",
      "postTransactionAmount": null,
      "secLink": null
    },
    "12": {
      "date": "2024-10-02",
      "ownerCik": null,
      "ownerName": "Timothy D Cook",
      "transactionDate": "2024-10-02",
      "transactionCode": "S",
      "transactionAmount": 223986,
      "transactionPrice": 224.46,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": "http://www.sec.gov/Archives/edgar/data/320193/000032019324000109/xslF345X05/wk-form4_1727994624.xml"
    },
    "13": {
      "date": "2024-10-02",
      "ownerCik": null,
      "ownerName": "Jeffrey E Williams",
      "transactionDate": "2024-10-02",
      "transactionCode": "S",
      "transactionAmount": 59730,
      "transactionPrice": 226.86,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": "http://www.sec.gov/Archives/edgar/data/320193/000032019324000112/xslF345X05/wk-form4_1727994654.xml"
    },
    "14": {
      "date": "2024-10-02",
      "ownerCik": null,
      "ownerName": "Katherine L Adams",
      "transactionDate": "2024-10-02",
      "transactionCode": "S",
      "transactionAmount": 61019,
      "transactionPrice": 226.2,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": "http://www.sec.gov/Archives/edgar/data/320193/000032019324000108/xslF345X05/wk-form4_1727994612.xml"
    },
    "15": {
      "date": "2024-09-20",
      "ownerCik": null,
      "ownerName": "Shelley Moore Capito",
      "transactionDate": "2024-09-20",
      "transactionCode": "S",
      "transactionAmount": 0,
      "transactionPrice": 228.2,
      "transactionAcquiredDisposed": "D",
      "postTransactionAmount": null,
      "secLink": null
.....
```

```text
...
"HistoricalComponents": {
    "2020-01-28": {
      "0": {
        "Date": "2020-01-28",
        "Code": "AIZ",
        "Exchange": "US",
        "Name": "Assurant Inc",
        "Sector": "Financial Services",
        "Industry": "Insurance - Property & Casualty"
      },
      "1": {
        "Date": "2020-01-28",
        "Code": "MNST",
        "Exchange": "US",
        "Name": "Monster Beverage Corp",
        "Sector": "Consumer Defensive",
        "Industry": "Beverages - Non-Alcoholic"
      },
      "2": {
        "Date": "2020-01-28",
        "Code": "GPS",
        "Exchange": "US",
        "Name": "Gap Inc",
        "Sector": "Consumer Cyclical",
        "Industry": "Apparel Retail"
      },
      "3": {
        "Date": "2020-01-28",
        "Code": "UNM",
        "Exchange": "US",
        "Name": "Unum Group",
        "Sector": "Financial Services",
        "Industry": "Insurance - Life"
      },
      "4": {
        "Date": "2020-01-28",
        "Code": "PGR",
        "Exchange": "US",
        "Name": "Progressive Corp",
        "Sector": "Financial Services",
        "Industry": "Insurance - Property & Casualty"
      },
      "5": {
        "Date": "2020-01-28",
        "Code": "CSX",
        "Exchange": "US",
        "Name": "CSX Corporation",
        "Sector": "Industrials",
        "Industry": "Railroads"
      },
      "6": {
        "Date": "2020-01-28",
        "Code": "ADP",
        "Exchange": "US",
        "Name": "Automatic Data Processing Inc",
        "Sector": "Technology",
        "Industry": "Software - Application"
      },
      "7": {
        "Date": "2020-01-28",
        "Code": "ANSS",
        "Exchange": "US",
        "Name": "ANSYS Inc",
        "Sector": "Technology",
        "Industry": "Software - Application"
...
```

## Related APIs

- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)
- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)
- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)
- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)
- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)
- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)
- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)
- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)
- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)
- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)
