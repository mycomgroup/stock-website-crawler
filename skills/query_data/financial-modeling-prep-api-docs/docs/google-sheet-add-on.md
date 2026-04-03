---
id: "url-46dc3043"
type: "api"
title: "Integrate FMP Data with Excel / Google Sheets"
url: "https://site.financialmodelingprep.com/developer/docs/google-sheet-add-on"
description: "FMP is the ultimate Excel and Google Sheets add-on for investors. FMP was built with one goal, to allow anyone to quickly find good investment opportunities. Our add-on has many different features and data available such as financials, key metrics, dividend data, live price data, crypto data, commodities and more. We have built these docs to help you get the most value out of FMP."
source: ""
tags: []
crawl_time: "2026-03-18T05:10:15.940Z"
metadata:
  markdownContent: "# Integrate FMP Data with Excel / Google Sheets\n\nFMP is the ultimate Excel and Google Sheets add-on for investors. FMP was built with one goal, to allow anyone to quickly find good investment opportunities. Our add-on has many different features and data available such as financials, key metrics, dividend data, live price data, crypto data, commodities and more. We have built these docs to help you get the most value out of FMP.\n\n\n#### Important Information\n\n1. The add-on offers the same functionality across Excel, Google Sheets, and Excel online.\n\n2. Currently, we do not have any data quotas. The only quota imposed is by Google Sheets - you can only make 20k requests per day on regular accounts and 100k on paid accounts. This limit resets automatically every 24 hours. However, we do ask users to be mindful of making too many simultaneous requests. If we see any type of system abuse, we may choose to freeze your account.\n\n\n#### Excel\n\nInstalling FMP on Excel is very simple. All you need to do is follow these steps:\n\n1. Open a new Excel spreadsheet\n\n2. Navigate to Add-ins on the Home tab\n\n3. Click on More Add-ins\n\n1. Search for the FMP add-on.\n\n2. Click on Add\n\nNow you will be able to access the add-in at any time under the Home tab as shown below:\n\n\n#### Google Sheets\n\nInstalling FMP on Google Sheets is very simple. All you need to do is follow these steps:\n\n1. Open a new Google Sheet\n\n2. Navigate to the Extensions menu and select Add-ons from the dropdown, then Get add-ons (this will open Google Workspace Marketplace within a pop-up modal)\n\n1. Search for FMP\n\n2. Select the FMP add-on and  click Install\n\nNow you will be able to access the add-on at any time under the extensions menu as shown below:\n\n\n#### Support\n\nIf you have any feedback or come across any issues, feel free to reach out to us by email at info@financialmodelingprep.com.\n\n\n#### Statement Dump\n\nIf you are looking to get an overview of a company's financials, one of the best ways to do this is to use statement dump. In a few clicks, you can get the income statement, balance sheet, cash flow statement, key metrics, and growth metrics annually or quarterly right on your spreadsheet. You will get either the last 19 years of data or 72 quarters, depending on your preference.\n\nBy default, the order of the data will be sorted from most recent data to oldest. However, with a pro account, you can click on the advanced option to reverse the order of the statements.\n\nBetter yet, you can access the financial statements exactly as they were reported to the SEC. Simply select SEC as reported financials and select whether you want annual or quarterly data.\n\nNote: this only applies to companies that report to the SEC (Securities Exchange Commission).\n\nTipsUse the statement dump search to find the tickers to use for the functions.The tickers that appear in the search suggestions are not the only ones available with data coverage.\n\n\n#### FMP Function\n\nThis function is best used for obtaining financials, key metrics, revenue segments, analyst estimates, etc. (see data available per function).\n\nThe FMP function syntax is =FMP(\"ticker/s\", \"parameter/s\", \"period/s\", [\"quarter\"], [divisor])\n\nTicker/s [required]: The symbol/s of the company you are looking to get data for. It can be hardcoded i.e \"AAPL\" or a cell reference i.e. A1.Parameter/s [required]: The data you are looking to get with the function. This accepts multiple parameters or a single parameter. It can be hard coded i.e. \"Revenue\", or a cell reference i.e B1:D1.Period/s [required]: The year or time period you would like to select. This accepts multiple periods or a single period. It can be hard coded i.e. 2020, or a cell reference i.e. B1:D1.The periods include specific years like: 2020, \"TTM\" (Trailing Twelve Months), \"LY\", \"LY-1\" etc (The latest fiscal year of data available, the previous and so on), \"LQ\", \"LQ-1\" etc (The latest fiscal quarter of data available, the previous and so on).Quarter [optional]: The quarter you are looking to get data for (only for quarterly data). It can be hard coded i.e. \"Q2\", or a cell reference i.e. B1.Divisor [optional]: If you would like to get the output in millions, billions or any other data unit, you can use this parameter to get the data in that format. It can be hard coded i.e. 1000000, or a cell reference i.e. B1.\n\nHere are a few examples of valid function calls:\n\n=FMP(\"AAPL\",\"ROE\",\"TTM\")\n\n=FMP(\"TSLA\", \"Revenue\", \"LY\",,1000000)\n\n=FMP(\"AAPL\",\"Free Cash Flow\",2019,\"Q3\")\n\nTipsWhen requesting a lot of data, enter multiple tickers, parameters and periods in the function using cell references.Use the divisor parameter instead of dividing every cell by a value.For numbers in the function like 2020 you don't need to use quotes (\" \") only for text like \"Revenue\", tickers etc.\n\n\n#### Large Data Requests\n\nInstead of making many function requests at once, you can get data faster by using ranges in the functions.\n\nAll you need to do is enter a range of tickers instead of a singular ticker, enter a range of parameters instead of a single parameter or enter a range of periods instead of a single period. You can see how it works in this example:\n\nAs you can see, the function is getting all these key metrics for multiple companies across the different periods in a single function call. This saves you a lot of time and makes your spreadsheet faster.\n\n\n#### FMPPRICE Function\n\nThis function is best used for obtaining live price data, historical price data, dividend payment information, etc (see data available per function).\n\nThe FMPPRICE function syntax is =FMPPRICE(\"ticker/s\", \"parameter/s\", number of days to end, \"start date\", \"end date\").\n\nTicker/s [required]: The symbol/s of the company you are looking to get data. It can be hardcoded i.e \"AAPL\" or a cell reference i.e. A1:A20.Parameter/s [required]: The data you are looking to get with the function. This accepts multiple parameters or a single parameter. It can be hard coded i.e. \"Price\", or a cell reference i.e. B1:D1Number of days to end [optional]: For historical price data you can select the number of days to get data for. For example, 5 will return the last 5 days of historical price data. It can be hard coded i.e. 5, or a cell reference i.e. B2.Start Date [optional]: For historical stock price data you can select a specific start date. The start date must be in a date format from a cell or follow the \"mm/dd/yyyy\" format. It can be hard coded i.e. \"01/30/2022\", or a cell reference i.e. B1. If you only enter a start date this will return the historical attribute you are looking for for that specific date.End date [optional]: For historical stock price data you can select a specific end date. The end date must be in a date format from a cell or follow the \"mm/dd/yyyy\" format. It can be hard coded i.e. \"01/30/2022\", or a cell reference i.e. B1.\n\nHere are a few examples of valid function calls:\n\n=FMPPRICE(\"TSLA\",\"Price\") \\n =FMPPRICE(\"AAPL\", \"Close\",,\"01/01/2022\", \"01/30/2022\") \\n =FMPPRICE(\"AMZN\", \"Open\", 2) \\n\n\nTipsWhen requesting a lot of data, enter multiple tickers, parameters and periods in the function using cell references.For numbers in the function like 5 you don't need to use quotes (\" \") only for text like \"Close\", \"Dividend\", etc.Use the SUM function to get only one value for historical stock data. For example =SUM(FMPPRICE(\"AAPL\", \"Close\", , \"01/28/2022\"))\n\n\n#### Large Data Requests\n\nInstead of making many function requests at once, you can get data faster by using ranges in the functions.\n\nAll you need to do is enter a range of tickers instead of a singular ticker or enter a range of parameters instead of a single parameter. You can see how that works in this example:\n\nAs you can see, the function is getting all these real-time values for many different companies in a single function call. This saves you a lot of time and makes your spreadsheet faster.\n\nYou can also enter multiple tickers in the function to get historical price data for many securities at once.\n\n\n#### FMPFUNDS Function\n\nThis function is best used for obtaining ETF and fund data like expense ratio, net asset value, assets under management, etc. (see data available per function).\n\nThe FMPFUNDS function syntax is =FMPFUNDS(\"ticker/s\", \"parameter/s\")\n\nTicker/s [required]: The symbol/s of the ETF/Fund you are looking to get data for. It can be hardcoded i.e. \"SPY\" or a cell reference i.e A1.Parameter/s [required]: The data you are looking to get with the function. This accepts multiple parameters or a single parameter. It can be hard coded i.e \"expense ratio\", or a cell reference i.e. B1:D1.\n\nHere are a few examples of valid function calls:\n\n=FMPFUNDS(\"SPY\",\"Expense Ratio\")\n\n=FMPFUNDS(\"PICK\",\"Nav\")\n\nTipsUse the statement dump search to find the tickers to use for the functions.The tickers that appear in the search suggestions are not the only ones available with data coverage.When requesting a lot of data, enter multiple parameters in the function using cell references.\n\n\n#### Large Data Requests\n\nInstead of making many function data requests at once, you can get data faster by using ranges in the functions.\n\nAll you need to do is enter a range of parameters and/or tickers instead of a single parameter. You can see how that works in this example:\n\nAs you can see, the function is getting all these real-time parameters for many different funds in a single function call. This saves you a lot of time and makes your spreadsheet faster.\n\n\n#### Refresh Data\n\nAt any time you can use the refresh data button at the top right of the add-on to refresh live data you may have on your spreadsheet.\n\nThis includes:\n\nLive price dataTTM metricsETF/Fund data\n\n\n#### Refresh Errors\n\nOccasionally when requesting large amounts of data at once, you may get an #error on Google Sheets or \"too many simultaneous requests\" in Excel.\n\nInstead of manually having to go to each cell that contains this and fix this, you can press the refresh errors button at the top right of the add-on (wrench icon).\n\nThis will fix them all at once.\n\n\n#### Trending Stocks\n\nYou can now track trending and popular stocks right from the main panel. It’s designed to make keeping up with the markets faster and easier.\n\nTop Gainers: Discover which stocks are soaring.\n\nTop Losers: See which stocks have taken a hit.\n\nMost Active: Find the stocks with the highest trading volume.\n\nClicking the dropdown arrow in a specific category will reveal more stocks within that list, whether it’s gainers, losers, or the most active.\n\nClick on any stock ticker to see the important stuff, like:\n\nPrice, market cap, and volume, all updated live.Performance metrics like YTD returns and P/E ratios.Company news headlines to help you stay in the loop.For U.S. companies, you can even access official filings for more in-depth analysis.\n\n\n#### Function Builder\n\nInstead of figuring out which function to use for each data point you want to access, you can use the function builder to generate it for you.\n\nHere’s a breakdown of how it works:\n\nSymbols: Begin by entering the ticker symbol(s) of the company or companies you want to analyze. This can be a single ticker like \"AAPL\" or a list if you’re analyzing multiple stocks simultaneously.\n\nNote: You can also change from search to select a range of tickers, for example A2:A5.\n\nParameters (if applicable): Choose the financial metric or data parameter you need. Options include metrics like \"Revenue,\" \"Net Income,\" and others from the company’s financials. This flexibility allows you to build custom reports by specifying exactly which data points to pull.\n\nNote: Certain parameters cannot be selected at the same time with others. If that's the case, they will appear grayed out.\n\nPeriods (if applicable): Select the period, such as the year or quarter, for which you need the data. For example, entering \"2021\" will fetch the annual data for that year.\n\nSpecific dates (if applicable): Enter the exact start and end dates to define the timeframe for your data request. For instance, setting \"2024-10-31\" as both the start and end date will fetch data for that particular day only. This option is perfect for obtaining precise daily metrics, and you can choose to include a date column in the results to ensure your data is well-documented. Alternatively, you can specify a broader range to capture historical trends within your selected period.\n\nNote: Alternatively, use the \"Number of days\" feature to retrieve data over a recent period, such as the last 10 days. Simply select this option and specify the number of days, and FMPsheets will automatically pull the data from the past 10 business days up to the current date. This is useful for quick analysis of short-term trends without needing to manually enter date ranges.\n\nQuarter Selection (if applicable): For quarterly data, you can specify the particular quarter to narrow down the timeframe, allowing for targeted analysis within the fiscal year.\n\nGenerated Formula: Once you’ve made your selections, FMPsheets automatically generates the appropriate formula. For instance, entering \"AAPL\" as the symbol, \"Revenue\" as the parameter, and \"2021\" as the period results in the formula =FMP(\"AAPL\", \"Revenue\", 2021), which you can copy directly.\n\n\n#### Analyzing Stock Financials\n\nThere are 2 ways to analyze stock financials. The first is to use the statement dump function to get them all at once annually or quarterly in our standardized format or as reported to the SEC:\n\nThe second is to use the function to get only the financial data you care about. For this use case, we recommend selecting the financial data you'd like from our available data and then building a spreadsheet model like this:\n\nAs you can see, in one function call you can get the all the financial data you need. You can substitute the LY, LY-1, etc, for specific years or you can also use LQ, LQ-1 etc. to get the data for many quarters.\n\nTipsAdd sparklines, graphs, conditional formatting, or formulas to make your analysis easier.Link the formulas to the ticker cell so you can change it and have all data populated for you.Use the statement dump search to find the tickers to use for the function.\n\n\n#### Analyzing Live Price Data\n\nIt is easy to analyze real-time price data for stocks, ETF funds, and more with FMP. A typical use case involves gathering a list of stocks from your portfolio or watchlist and gathering all the real-time metrics you are interested in (see available data).\n\nTo get real-time data you need to use the FMPPRICE function. Here is an image showing how to use it to get real-time data.\n\nAssuming you are looking to get real-time data for multiple securities, this is the best way to do it. You will get data faster, and you can refresh it anytime you'd like by pressing the refresh data button at the top right of the add-on.\n\nTipsUse the statement dump search to find the tickers to use for the function.When requesting a lot of data, enter multiple parameters and tickers in the function using cell references.\n\n\n#### Historical Price Data Analysis\n\nThere are 2 main ways of getting historical price data for stocks, ETFs, and other securities covered. The first is for individual assets.\n\nFor example, to get the last 30 days of close and open price for Apple, you can do the following:\n\n=FMPPRICE(\"AAPL\", \"Close\", 30)\n\nYou can also enter a specific date to get data in the function. For example =FMPPRICE(\"AMZN\", \"close\", , \"01/01/2019\", \"01/10/2019\")\n\nFor multiple stocks, you can enter multiple tickers in the function as shown in the images below:\n\nTipsUse spreadsheet formulas to get historical calculations. For example =AVERAGE(\"AAPL\", \"close\", 30) provides you with the average close price for the past 30 days.For getting the stock price of a particular date, you can do something like =SUM(FMPPRICE(\"AAPL\", \"close\", , \"01/03/2019\"))Use =TRANSPOSE(INDEX(FMPPRICE(A1, \"close\", 30),,2)) to get the price data horizontally.\n\n\n#### Historical Dividend Payment History\n\nWith the =FMPPRICE function, you can get all of the dividend data in a single function call. All you have to do is enter =FMPPRICE(\"AAPL\", \"dividend\")\n\nThis provides you with the ex-date, dividend, adjusted dividend, payment date, and declaration date.\n\nYou can also enter a specific date to get data in the function. For example =FMPPRICE(\"aapl\", \"dividend\", , \"01/01/2017\", \"01/01/2022\")\n\nTipsUse this function only to get one column like the adjusted dividend column =INDEX(FMPPRICE(\"aapl\", \"dividend\"),,2)\n\n\n#### Annual Dividend Payments\n\nGetting the annual dividend payment for a particular stock or ETF is simple. Using the FMP function, you can get the data like this:\n\n=FMP(\"AAPL\", \"Dividend\", 2022)\n\nThis will provide you with the SUM of all the dividend payments made during that year.\n\nIf you'd like to get the adjusted dividend amount, you can do this like this:\n\n=FMP(\"AAPL\", \"Adjusted Dividend\", 2022)\n\nYou can also get this number for multiple years at once:\n\n\n#### Quarterly Dividend Payments\n\nUsing the FMP function, it is simple to get past stock and ETF dividend payments. You can get individual quarterly dividend payments as follows:\n\n=FMP(\"AAPL\", \"dividend\", \"LQ\")\n\nThis will return the latest dividend paid by a stock or ETF. The same applies to the adjusted dividend.\n\nTipsYou can get the sum of the past 4 dividend payments like this =SUM(FMP(\"AAPL\", \"dividend\", {\"LQ\", \"LQ-1\", \"LQ-2\", \"LQ-3\"}))You can calculate the expected dividend amount paid by taking the LQ dividend payment and multiplying it by the regular payment interval for example 4 for quarterly paying securities.\n\n\n#### Segment & Geographic Revenues\n\nYou can get a specific company’s revenue breakdown across key business segments and geographic markets.\n\nUsing the FMP function, you can get this data on a quarterly and annual basis.\n\nTo get segment revenue breakdowns, all you have to do is use the function as follows:\n\n=FMP(\"AAPL\", \"segment revenues\", 2020)\n\nYou can also substitute the specific year for “LY”, “LY-1”, “LY-2”, etc, which provides you with the latest fiscal year data or the previous fiscal years.\n\nThe same concept applies to geographic revenues.\n\n=FMP(\"AAPL\", \"geographic revenues\", \"LQ-2\")\n\nDue to some technical constraints for quarterly data, you can only use the LQ, LQ-1 period system.\n\n*This feature is only for companies that report to the SEC since the data comes from these reports.\n\nTipsYou can get this data for multiple periods in one function call, for example, =FMP(\"AAPL\", \"segment revenues\", {2022, 2021, 2020})\n\n\n#### Analyst Estimates\n\nWith FMP, you can get analyst estimates for specific financial metrics like revenue, EBITDA, Net income, and more (see available data).\n\nThe estimates are sourced from reports made by top analysts from financial firms such as Morgan Stanley, Citigroup, JP Morgan, amongst others.\n\nTo get many analyst estimates at once for a particular company, you can do this:\n\nNote that analyst estimates are currently limited up to 2029. Historical data from previous years is also available.\n\nTipsYou can get this data for multiple years in one function call, for example, =FMP(\"AAPL\", \"Estimated Revenue AVG\", {2029, 2028, 2027})\n\n\n#### ETF/Fund Data\n\nBesides being able to get live price data, historical price data, and dividend data using the FMP and FMPPRICE functions. You can now use the FMPFUNDS function to get ETF specific data like nav, expense ratios, assets under management, etc (see available data).\n\nFor example to get the nav, aum and expense ratio for the SPY ETF you can do the following:\n\nThis provides you with the data you need for your funds in real-time.\n\nNote that this function is in beta, and more funds and ETFs will be added.\n\n\n#### Custom Screener (Get List)\n\nFMP Elite plan members can find companies that meet their specific criteria. Here is how that works:\n\nNavigate to the screener tab of the add-on and select Get List.Enter the filters you would like to search for. This includes market cap, dividend yield, sector, industry, exchange, etc.Click on Get data once you are ready.\n\nThis will return a list of companies, ETFs and or funds that meet your desired criteria, along with available information such as company name, sector, industry, beta price, etc.\n\nYou can take this list of tickers and get any additional information and metrics you want at once following the method below.\n\n\n#### Custom Screener (Get Data)\n\nBuilding a custom-made stock screener and obtaining the necessary data is made simple with FMP (Pro and Elite members). Here's all you need to do:\n\nGet a list of stocks in your Excel or Google Sheets spreadsheet. You can also use the screener get list data functionality from above.Select the parameters for which you'd like to retrieve data. This includes the income statement, balance sheet, cash flow statement, key metrics, growth metrics, and real-time price data. You can refer to this link for the full list of items.\n\nOnce you have the list of stocks and parameters set up, you can easily proceed to the next steps. Simply navigate to the FMP Screener section of the add-in.\n\nIn the FMP Screener section, use your mouse to select the list of tickers you would like to gather data for. Once selected, click on the 4 square icon to proceed.\n\nNext, do the same for the parameters you've chosen. Don't forget to include the period in the parameter. This currently includes:\n\nTTM (trailing twelve months)LY (latest fiscal year)LY-1 etc (previous fiscal year) up to LY-17LQ (latest fiscal quarter)LQ-1 etc (previous fiscal quarter) up to LQ-71Specific years like 2020Specific year and quarter like 2020 Q4\n\nIf you omit the period, the default value returned will be LY (latest fiscal year value). Capitalization and spacing do not matter. You do not need to specify any period for real-time data.\n\nOnce you've completed the steps above, it's time to retrieve the data. Simply click on the \"Get Data\" button, and your screener will be generated. You will notice a bucket created, holding the tickers and parameters you've selected.\n\nYou can easily refresh the screener data by utilizing the refresh button in the bucket, which allows you to obtain the latest data at any time. Additionally, you have the option to rename the bucket for future reference or delete it when no longer needed.\n\nPlease keep in mind that the bucket can only be refreshed in the spreadsheet tab where you have the tickers and parameters located together. Refreshing the data in another tab of your spreadsheet will not work.\n\nThe beauty of using FMP for stock screening is that it returns and updates the data more quickly compared to using functions. It also provides the flexibility to apply filters, such as sorting companies by highest revenue, without the functions automatically refreshing.\n\n\n#### Track/Compare Crypto\n\nComparing or tracking cryptocurrencies with FMP is very simple. Here is a full list of the cryptocurrencies currently offered (over 4,700).\n\nYou can also simply use the ticker without the \"-\". For example, BTC-USD for Bitcoin's price in US dollars. We use BTCUSD.\n\nThere are two types of data you can get from cryptocurrencies live data and historical price data.\n\nUsing live data you can track or compare cryptocurrencies using the FMPPRICE function like this:\n\nThis will allow you to access the live price and other relevant information about the cryptocurrencies you have chosen. You can use the refresh data button at the top of the right add-on at any time to update the functions and view the latest live data.\n\nHistorical price data is equally easy to access with the FMPPRICE function.\n\nFor example, to get the close price for the last 10 days of Bitcoin in US dollars, you need to enter =FMPPRICE(\"BTCUSD\", \"Close\", 10)\n\nOr you can also get this data in a specific timeframe, for example, =FMPPRICE(\"BTCUSD\",  \"Close\", \"01/01/2024\", \"01/30/2024\")\n\nYou can get historical data for many cryptocurrencies at once like this:\n\n\n#### Forex Currency Rates\n\nComparing or tracking foreign exchange currencies with FMP is very simple. Here is a full list of the currencies currently offered (over 1,540).\n\nYou can also simply use the ticker without the \"=x\". For example, CADUSD=X for the Canadian dollar price in US dollars. We use CADUSD.\n\nThere are two types of data you can get from foreign currencies live data and historical price data.\n\nUsing live data you can track or compare currency rates using the FMPPRICE function like this:\n\nThis allows you to access the live price and other relevant information about the currency rates you have chosen. You can use the refresh data button at the top of the right add-on at any time to update the functions and view the latest live data.\n\nHistorical price data is equally easy to access with the FMPPRICE function.\n\nFor example, to get the currency rate close for the last 10 days of US dollars to Canadian dollars, you need to enter =FMPPRICE(\"USDCAD\", \"Close\", 10)\n\nOr you can also get this data in a specific timeframe, for example, =FMPPRICE(\"USDCAD\", \"Close\", \"01/01/2024\", \"01/30/2024\")\n\nYou can get historical data for many currencies at once like this:\n\n\n#### Commodities/Futures Analysis\n\nAnalyzing commodities and futures with FMP is very simple. Here is a full list of commodities/futures currently offered (over 40).\n\nJust make sure to use the exact symbols outlined in the list.\n\nThere are two types of data you can get from commodities and futures live data and historical price data.\n\nUsing live data you can track or compare prices using the FMPPRICE function like this:\n\nThis allows you to access the live price and other relevant information about the commodities you have chosen. You can use the refresh data button at the top of the right add-on at any time to update the functions and view the latest live data.\n\nHistorical price data is equally easy to access with the FMPPRICE function.\n\nFor example, to get the commodity close price for the last 10 days of soybean meal futures, you need to enter =FMPPRICE(\"ZMUSD\", \"Close\", 10)\n\nOr you can also get this data in a specific timeframe, for example, =FMPPRICE(\"ZMUSD\", \"Close\", \"01/01/2024\", \"01/30/2024\")\n\nYou can get historical data for many commodities at once like this:\n\n\n#### Indices Tracking\n\nWhether you'd like to compare your investment performance or track your investment in indices like the S&P 500, getting data for indices with FMP is very simple. Here is a full list of the currencies currently offered (over 190).\n\nJust make sure to use the exact symbols outlined in the list.\n\nThere are two types of data you can get from indices: live data and historical price data.\n\nUsing live data, you can track or compare indices prices using the FMPPRICE function like this:\n\nThis allows you to access the live price and other relevant information about the indices you have chosen. You can use the refresh data button at the top of the right add-on at any time to update the functions and view the latest live data.\n\nHistorical price data is equally easy to access with the FMPPRICE function.\n\nFor example, to get the S&P 500 close price for the last 10 days, you need to enter =FMPPRICE(\"^GSPC\", \"Close\", 10)\n\nOr you can also get this data in a specific timeframe, for example, =FMPPRICE(\"^GSPC\", \"Close\", \"01/01/2024\", \"01/30/2024\")\n\nYou can get historical data for many indices at once like this:\n\n\n#### Common Issues\n\nThese are the most common issues when using the add-on along with their solutions.\n\n\n#### Cannot Find Stock Ticker to use for International Stocks\n\nFMP uses the same ticker system as per documentation. You can use search or, better yet, the statement dump search to find the right ticker to use.\n\nYou can enter the regular ticker followed by the exchange extension. For example, for Telus, a Canadian company listed in the TSX, the ticker is \"T\" and the extension is \".TO\". You can enter \"T.TO\" to get the data for this company (see available exchanges and their extensions).\n\n\n#### Unable to Login on Google Sheets\n\nSometimes Chrome extensions or adblockers may block our authentication system, which allows us to recognize your account.\n\nAlernatively there is an issue with Google allowing us to authenticate your account when being logged into multiple Google accounts at once.\n\nIn either case don't worry you can fix this by following these simple solutions.\n\nSolutions\n\nSolution 1:\n\nDelete the add-onRefresh the pageDisable your Adblock on Google SheetsClear your cacheReinstall FMP\n\nSolution 2:\n\nCreate a new Google Chrome profileOpen your spreadsheet in the new profileUse FMP as you'd like\n\n\n#### Functions Return #name Not Recognized by Excel\n\nIt is possible that when you download FMP on Excel, you are able to use the statement dump function but unable to use the custom functions.\n\nIn most cases, this is because Microsoft requires users to have an Office 365 account to access custom spreadsheet functions.\n\nSolutions\n\nUse FMP on Excel Online or Google Sheets (no Office 365 subscription is required)Use an Office 365 account from work, school, or any other organization if you have access.\n\n\n#### Cells Contain _xldufd_ in Excel\n\nThis typically happens when you save your Excel files on a cloud server like one drive or have an existing add-on affecting the custom function.\n\nDon't worry. There is an easy way to fix all the function calls at once and a way to prevent this from happening altogether.\n\nSolutions\n\n1. Press the “Refresh Errors” button at the top right of the add-on; this will identify those cells and clean them up for you at once:\n\n2. Excel allows you to replace all the cell contents in a tab at once.\n\nSimply head to replace.\n\nReplace all with everything behind the function like _xlduf_ … with nothing.\n\nThis will fix all cells at once.\n\nPrevention\n\nTo prevent this from happening altogether here are two different things you can try:\n\nGo to File / OptionsSelect Add-ins (near bottom on left), Manage (near bottom), and \"Go\"Uncheck to remove any Add-ins you are currently not using that may be interfering with the FMP COMSave your Excel files locally as opposed to the cloud\n\n\n#### URL Fetch Error\n\nURL fetch is a limit that Google Sheets has for requesting data.\n\nEvery time you make a function call, a URL fetch call is made to retrieve the data.\n\nGoogle limits these calls to 20k per day for regular users and 100k for paid accounts. This limit resets automatically every day.\n\nSolutions\n\nThere are two solutions. The first is to use the screener functionality as shown here.\n\nThe second is using ranges in the functions so you can get more data faster while making fewer function calls.\n\nAlternatively, you can use FMP on Excel, where there are no URL fetch limits, or upgrade your Google account to an enterprise account.\n\n\n#### #SPILL Error\n\nThe spill error happens in Excel or Google Sheets when the function you use returns an array (multiple values in one single function), and there is no space for the data to be displayed.\n\nFor example, if you do =FMPPRICE(\"AAPL\", \"close\", 3), this will return an array with the date and close price for the past 3 trading days.\n\nAs you can see, this returns in the #spill error because there is data blocking the function from showing the values.\n\nSolution\n\nFixing this error is simple, all you need to do is clear all the data that interferes with the function calls you are making, and you will see the cell will clear and you will be able to get the data you want.\n\n\n#### Stay Ahead with Fresh Data!\n\nYour session has been inactive. For the latest financial insights, please refresh.\n\nRefresh Now\n"
  rawContent: ""
  suggestedFilename: "google-sheet-add-on"
---

# Integrate FMP Data with Excel / Google Sheets

## 源URL

https://site.financialmodelingprep.com/developer/docs/google-sheet-add-on

## 描述

FMP is the ultimate Excel and Google Sheets add-on for investors. FMP was built with one goal, to allow anyone to quickly find good investment opportunities. Our add-on has many different features and data available such as financials, key metrics, dividend data, live price data, crypto data, commodities and more. We have built these docs to help you get the most value out of FMP.

## 文档正文

FMP is the ultimate Excel and Google Sheets add-on for investors. FMP was built with one goal, to allow anyone to quickly find good investment opportunities. Our add-on has many different features and data available such as financials, key metrics, dividend data, live price data, crypto data, commodities and more. We have built these docs to help you get the most value out of FMP.

#### Important Information

1. The add-on offers the same functionality across Excel, Google Sheets, and Excel online.

2. Currently, we do not have any data quotas. The only quota imposed is by Google Sheets - you can only make 20k requests per day on regular accounts and 100k on paid accounts. This limit resets automatically every 24 hours. However, we do ask users to be mindful of making too many simultaneous requests. If we see any type of system abuse, we may choose to freeze your account.

#### Excel

Installing FMP on Excel is very simple. All you need to do is follow these steps:

1. Open a new Excel spreadsheet

2. Navigate to Add-ins on the Home tab

3. Click on More Add-ins

1. Search for the FMP add-on.

2. Click on Add

Now you will be able to access the add-in at any time under the Home tab as shown below:

#### Google Sheets

Installing FMP on Google Sheets is very simple. All you need to do is follow these steps:

1. Open a new Google Sheet

2. Navigate to the Extensions menu and select Add-ons from the dropdown, then Get add-ons (this will open Google Workspace Marketplace within a pop-up modal)

1. Search for FMP

2. Select the FMP add-on and  click Install

Now you will be able to access the add-on at any time under the extensions menu as shown below:

#### Support

If you have any feedback or come across any issues, feel free to reach out to us by email at info@financialmodelingprep.com.

#### Statement Dump

If you are looking to get an overview of a company's financials, one of the best ways to do this is to use statement dump. In a few clicks, you can get the income statement, balance sheet, cash flow statement, key metrics, and growth metrics annually or quarterly right on your spreadsheet. You will get either the last 19 years of data or 72 quarters, depending on your preference.

By default, the order of the data will be sorted from most recent data to oldest. However, with a pro account, you can click on the advanced option to reverse the order of the statements.

Better yet, you can access the financial statements exactly as they were reported to the SEC. Simply select SEC as reported financials and select whether you want annual or quarterly data.

Note: this only applies to companies that report to the SEC (Securities Exchange Commission).

TipsUse the statement dump search to find the tickers to use for the functions.The tickers that appear in the search suggestions are not the only ones available with data coverage.

#### FMP Function

This function is best used for obtaining financials, key metrics, revenue segments, analyst estimates, etc. (see data available per function).

The FMP function syntax is =FMP("ticker/s", "parameter/s", "period/s", ["quarter"], [divisor])

Ticker/s [required]: The symbol/s of the company you are looking to get data for. It can be hardcoded i.e "AAPL" or a cell reference i.e. A1.Parameter/s [required]: The data you are looking to get with the function. This accepts multiple parameters or a single parameter. It can be hard coded i.e. "Revenue", or a cell reference i.e B1:D1.Period/s [required]: The year or time period you would like to select. This accepts multiple periods or a single period. It can be hard coded i.e. 2020, or a cell reference i.e. B1:D1.The periods include specific years like: 2020, "TTM" (Trailing Twelve Months), "LY", "LY-1" etc (The latest fiscal year of data available, the previous and so on), "LQ", "LQ-1" etc (The latest fiscal quarter of data available, the previous and so on).Quarter [optional]: The quarter you are looking to get data for (only for quarterly data). It can be hard coded i.e. "Q2", or a cell reference i.e. B1.Divisor [optional]: If you would like to get the output in millions, billions or any other data unit, you can use this parameter to get the data in that format. It can be hard coded i.e. 1000000, or a cell reference i.e. B1.

Here are a few examples of valid function calls:

=FMP("AAPL","ROE","TTM")

=FMP("TSLA", "Revenue", "LY",,1000000)

=FMP("AAPL","Free Cash Flow",2019,"Q3")

TipsWhen requesting a lot of data, enter multiple tickers, parameters and periods in the function using cell references.Use the divisor parameter instead of dividing every cell by a value.For numbers in the function like 2020 you don't need to use quotes (" ") only for text like "Revenue", tickers etc.

#### Large Data Requests

Instead of making many function requests at once, you can get data faster by using ranges in the functions.

All you need to do is enter a range of tickers instead of a singular ticker, enter a range of parameters instead of a single parameter or enter a range of periods instead of a single period. You can see how it works in this example:

As you can see, the function is getting all these key metrics for multiple companies across the different periods in a single function call. This saves you a lot of time and makes your spreadsheet faster.

#### FMPPRICE Function

This function is best used for obtaining live price data, historical price data, dividend payment information, etc (see data available per function).

The FMPPRICE function syntax is =FMPPRICE("ticker/s", "parameter/s", number of days to end, "start date", "end date").

Ticker/s [required]: The symbol/s of the company you are looking to get data. It can be hardcoded i.e "AAPL" or a cell reference i.e. A1:A20.Parameter/s [required]: The data you are looking to get with the function. This accepts multiple parameters or a single parameter. It can be hard coded i.e. "Price", or a cell reference i.e. B1:D1Number of days to end [optional]: For historical price data you can select the number of days to get data for. For example, 5 will return the last 5 days of historical price data. It can be hard coded i.e. 5, or a cell reference i.e. B2.Start Date [optional]: For historical stock price data you can select a specific start date. The start date must be in a date format from a cell or follow the "mm/dd/yyyy" format. It can be hard coded i.e. "01/30/2022", or a cell reference i.e. B1. If you only enter a start date this will return the historical attribute you are looking for for that specific date.End date [optional]: For historical stock price data you can select a specific end date. The end date must be in a date format from a cell or follow the "mm/dd/yyyy" format. It can be hard coded i.e. "01/30/2022", or a cell reference i.e. B1.

Here are a few examples of valid function calls:

=FMPPRICE("TSLA","Price") \n =FMPPRICE("AAPL", "Close",,"01/01/2022", "01/30/2022") \n =FMPPRICE("AMZN", "Open", 2) \n

TipsWhen requesting a lot of data, enter multiple tickers, parameters and periods in the function using cell references.For numbers in the function like 5 you don't need to use quotes (" ") only for text like "Close", "Dividend", etc.Use the SUM function to get only one value for historical stock data. For example =SUM(FMPPRICE("AAPL", "Close", , "01/28/2022"))

#### Large Data Requests

Instead of making many function requests at once, you can get data faster by using ranges in the functions.

All you need to do is enter a range of tickers instead of a singular ticker or enter a range of parameters instead of a single parameter. You can see how that works in this example:

As you can see, the function is getting all these real-time values for many different companies in a single function call. This saves you a lot of time and makes your spreadsheet faster.

You can also enter multiple tickers in the function to get historical price data for many securities at once.

#### FMPFUNDS Function

This function is best used for obtaining ETF and fund data like expense ratio, net asset value, assets under management, etc. (see data available per function).

The FMPFUNDS function syntax is =FMPFUNDS("ticker/s", "parameter/s")

Ticker/s [required]: The symbol/s of the ETF/Fund you are looking to get data for. It can be hardcoded i.e. "SPY" or a cell reference i.e A1.Parameter/s [required]: The data you are looking to get with the function. This accepts multiple parameters or a single parameter. It can be hard coded i.e "expense ratio", or a cell reference i.e. B1:D1.

Here are a few examples of valid function calls:

=FMPFUNDS("SPY","Expense Ratio")

=FMPFUNDS("PICK","Nav")

TipsUse the statement dump search to find the tickers to use for the functions.The tickers that appear in the search suggestions are not the only ones available with data coverage.When requesting a lot of data, enter multiple parameters in the function using cell references.

#### Large Data Requests

Instead of making many function data requests at once, you can get data faster by using ranges in the functions.

All you need to do is enter a range of parameters and/or tickers instead of a single parameter. You can see how that works in this example:

As you can see, the function is getting all these real-time parameters for many different funds in a single function call. This saves you a lot of time and makes your spreadsheet faster.

#### Refresh Data

At any time you can use the refresh data button at the top right of the add-on to refresh live data you may have on your spreadsheet.

This includes:

Live price dataTTM metricsETF/Fund data

#### Refresh Errors

Occasionally when requesting large amounts of data at once, you may get an #error on Google Sheets or "too many simultaneous requests" in Excel.

Instead of manually having to go to each cell that contains this and fix this, you can press the refresh errors button at the top right of the add-on (wrench icon).

This will fix them all at once.

#### Trending Stocks

You can now track trending and popular stocks right from the main panel. It’s designed to make keeping up with the markets faster and easier.

Top Gainers: Discover which stocks are soaring.

Top Losers: See which stocks have taken a hit.

Most Active: Find the stocks with the highest trading volume.

Clicking the dropdown arrow in a specific category will reveal more stocks within that list, whether it’s gainers, losers, or the most active.

Click on any stock ticker to see the important stuff, like:

Price, market cap, and volume, all updated live.Performance metrics like YTD returns and P/E ratios.Company news headlines to help you stay in the loop.For U.S. companies, you can even access official filings for more in-depth analysis.

#### Function Builder

Instead of figuring out which function to use for each data point you want to access, you can use the function builder to generate it for you.

Here’s a breakdown of how it works:

Symbols: Begin by entering the ticker symbol(s) of the company or companies you want to analyze. This can be a single ticker like "AAPL" or a list if you’re analyzing multiple stocks simultaneously.

Note: You can also change from search to select a range of tickers, for example A2:A5.

Parameters (if applicable): Choose the financial metric or data parameter you need. Options include metrics like "Revenue," "Net Income," and others from the company’s financials. This flexibility allows you to build custom reports by specifying exactly which data points to pull.

Note: Certain parameters cannot be selected at the same time with others. If that's the case, they will appear grayed out.

Periods (if applicable): Select the period, such as the year or quarter, for which you need the data. For example, entering "2021" will fetch the annual data for that year.

Specific dates (if applicable): Enter the exact start and end dates to define the timeframe for your data request. For instance, setting "2024-10-31" as both the start and end date will fetch data for that particular day only. This option is perfect for obtaining precise daily metrics, and you can choose to include a date column in the results to ensure your data is well-documented. Alternatively, you can specify a broader range to capture historical trends within your selected period.

Note: Alternatively, use the "Number of days" feature to retrieve data over a recent period, such as the last 10 days. Simply select this option and specify the number of days, and FMPsheets will automatically pull the data from the past 10 business days up to the current date. This is useful for quick analysis of short-term trends without needing to manually enter date ranges.

Quarter Selection (if applicable): For quarterly data, you can specify the particular quarter to narrow down the timeframe, allowing for targeted analysis within the fiscal year.

Generated Formula: Once you’ve made your selections, FMPsheets automatically generates the appropriate formula. For instance, entering "AAPL" as the symbol, "Revenue" as the parameter, and "2021" as the period results in the formula =FMP("AAPL", "Revenue", 2021), which you can copy directly.

#### Analyzing Stock Financials

There are 2 ways to analyze stock financials. The first is to use the statement dump function to get them all at once annually or quarterly in our standardized format or as reported to the SEC:

The second is to use the function to get only the financial data you care about. For this use case, we recommend selecting the financial data you'd like from our available data and then building a spreadsheet model like this:

As you can see, in one function call you can get the all the financial data you need. You can substitute the LY, LY-1, etc, for specific years or you can also use LQ, LQ-1 etc. to get the data for many quarters.

TipsAdd sparklines, graphs, conditional formatting, or formulas to make your analysis easier.Link the formulas to the ticker cell so you can change it and have all data populated for you.Use the statement dump search to find the tickers to use for the function.

#### Analyzing Live Price Data

It is easy to analyze real-time price data for stocks, ETF funds, and more with FMP. A typical use case involves gathering a list of stocks from your portfolio or watchlist and gathering all the real-time metrics you are interested in (see available data).

To get real-time data you need to use the FMPPRICE function. Here is an image showing how to use it to get real-time data.

Assuming you are looking to get real-time data for multiple securities, this is the best way to do it. You will get data faster, and you can refresh it anytime you'd like by pressing the refresh data button at the top right of the add-on.

TipsUse the statement dump search to find the tickers to use for the function.When requesting a lot of data, enter multiple parameters and tickers in the function using cell references.

#### Historical Price Data Analysis

There are 2 main ways of getting historical price data for stocks, ETFs, and other securities covered. The first is for individual assets.

For example, to get the last 30 days of close and open price for Apple, you can do the following:

=FMPPRICE("AAPL", "Close", 30)

You can also enter a specific date to get data in the function. For example =FMPPRICE("AMZN", "close", , "01/01/2019", "01/10/2019")

For multiple stocks, you can enter multiple tickers in the function as shown in the images below:

TipsUse spreadsheet formulas to get historical calculations. For example =AVERAGE("AAPL", "close", 30) provides you with the average close price for the past 30 days.For getting the stock price of a particular date, you can do something like =SUM(FMPPRICE("AAPL", "close", , "01/03/2019"))Use =TRANSPOSE(INDEX(FMPPRICE(A1, "close", 30),,2)) to get the price data horizontally.

#### Historical Dividend Payment History

With the =FMPPRICE function, you can get all of the dividend data in a single function call. All you have to do is enter =FMPPRICE("AAPL", "dividend")

This provides you with the ex-date, dividend, adjusted dividend, payment date, and declaration date.

You can also enter a specific date to get data in the function. For example =FMPPRICE("aapl", "dividend", , "01/01/2017", "01/01/2022")

TipsUse this function only to get one column like the adjusted dividend column =INDEX(FMPPRICE("aapl", "dividend"),,2)

#### Annual Dividend Payments

Getting the annual dividend payment for a particular stock or ETF is simple. Using the FMP function, you can get the data like this:

=FMP("AAPL", "Dividend", 2022)

This will provide you with the SUM of all the dividend payments made during that year.

If you'd like to get the adjusted dividend amount, you can do this like this:

=FMP("AAPL", "Adjusted Dividend", 2022)

You can also get this number for multiple years at once:

#### Quarterly Dividend Payments

Using the FMP function, it is simple to get past stock and ETF dividend payments. You can get individual quarterly dividend payments as follows:

=FMP("AAPL", "dividend", "LQ")

This will return the latest dividend paid by a stock or ETF. The same applies to the adjusted dividend.

TipsYou can get the sum of the past 4 dividend payments like this =SUM(FMP("AAPL", "dividend", {"LQ", "LQ-1", "LQ-2", "LQ-3"}))You can calculate the expected dividend amount paid by taking the LQ dividend payment and multiplying it by the regular payment interval for example 4 for quarterly paying securities.

#### Segment & Geographic Revenues

You can get a specific company’s revenue breakdown across key business segments and geographic markets.

Using the FMP function, you can get this data on a quarterly and annual basis.

To get segment revenue breakdowns, all you have to do is use the function as follows:

=FMP("AAPL", "segment revenues", 2020)

You can also substitute the specific year for “LY”, “LY-1”, “LY-2”, etc, which provides you with the latest fiscal year data or the previous fiscal years.

The same concept applies to geographic revenues.

=FMP("AAPL", "geographic revenues", "LQ-2")

Due to some technical constraints for quarterly data, you can only use the LQ, LQ-1 period system.

*This feature is only for companies that report to the SEC since the data comes from these reports.

TipsYou can get this data for multiple periods in one function call, for example, =FMP("AAPL", "segment revenues", {2022, 2021, 2020})

#### Analyst Estimates

With FMP, you can get analyst estimates for specific financial metrics like revenue, EBITDA, Net income, and more (see available data).

The estimates are sourced from reports made by top analysts from financial firms such as Morgan Stanley, Citigroup, JP Morgan, amongst others.

To get many analyst estimates at once for a particular company, you can do this:

Note that analyst estimates are currently limited up to 2029. Historical data from previous years is also available.

TipsYou can get this data for multiple years in one function call, for example, =FMP("AAPL", "Estimated Revenue AVG", {2029, 2028, 2027})

#### ETF/Fund Data

Besides being able to get live price data, historical price data, and dividend data using the FMP and FMPPRICE functions. You can now use the FMPFUNDS function to get ETF specific data like nav, expense ratios, assets under management, etc (see available data).

For example to get the nav, aum and expense ratio for the SPY ETF you can do the following:

This provides you with the data you need for your funds in real-time.

Note that this function is in beta, and more funds and ETFs will be added.

#### Custom Screener (Get List)

FMP Elite plan members can find companies that meet their specific criteria. Here is how that works:

Navigate to the screener tab of the add-on and select Get List.Enter the filters you would like to search for. This includes market cap, dividend yield, sector, industry, exchange, etc.Click on Get data once you are ready.

This will return a list of companies, ETFs and or funds that meet your desired criteria, along with available information such as company name, sector, industry, beta price, etc.

You can take this list of tickers and get any additional information and metrics you want at once following the method below.

#### Custom Screener (Get Data)

Building a custom-made stock screener and obtaining the necessary data is made simple with FMP (Pro and Elite members). Here's all you need to do:

Get a list of stocks in your Excel or Google Sheets spreadsheet. You can also use the screener get list data functionality from above.Select the parameters for which you'd like to retrieve data. This includes the income statement, balance sheet, cash flow statement, key metrics, growth metrics, and real-time price data. You can refer to this link for the full list of items.

Once you have the list of stocks and parameters set up, you can easily proceed to the next steps. Simply navigate to the FMP Screener section of the add-in.

In the FMP Screener section, use your mouse to select the list of tickers you would like to gather data for. Once selected, click on the 4 square icon to proceed.

Next, do the same for the parameters you've chosen. Don't forget to include the period in the parameter. This currently includes:

TTM (trailing twelve months)LY (latest fiscal year)LY-1 etc (previous fiscal year) up to LY-17LQ (latest fiscal quarter)LQ-1 etc (previous fiscal quarter) up to LQ-71Specific years like 2020Specific year and quarter like 2020 Q4

If you omit the period, the default value returned will be LY (latest fiscal year value). Capitalization and spacing do not matter. You do not need to specify any period for real-time data.

Once you've completed the steps above, it's time to retrieve the data. Simply click on the "Get Data" button, and your screener will be generated. You will notice a bucket created, holding the tickers and parameters you've selected.

You can easily refresh the screener data by utilizing the refresh button in the bucket, which allows you to obtain the latest data at any time. Additionally, you have the option to rename the bucket for future reference or delete it when no longer needed.

Please keep in mind that the bucket can only be refreshed in the spreadsheet tab where you have the tickers and parameters located together. Refreshing the data in another tab of your spreadsheet will not work.

The beauty of using FMP for stock screening is that it returns and updates the data more quickly compared to using functions. It also provides the flexibility to apply filters, such as sorting companies by highest revenue, without the functions automatically refreshing.

#### Track/Compare Crypto

Comparing or tracking cryptocurrencies with FMP is very simple. Here is a full list of the cryptocurrencies currently offered (over 4,700).

You can also simply use the ticker without the "-". For example, BTC-USD for Bitcoin's price in US dollars. We use BTCUSD.

There are two types of data you can get from cryptocurrencies live data and historical price data.

Using live data you can track or compare cryptocurrencies using the FMPPRICE function like this:

This will allow you to access the live price and other relevant information about the cryptocurrencies you have chosen. You can use the refresh data button at the top of the right add-on at any time to update the functions and view the latest live data.

Historical price data is equally easy to access with the FMPPRICE function.

For example, to get the close price for the last 10 days of Bitcoin in US dollars, you need to enter =FMPPRICE("BTCUSD", "Close", 10)

Or you can also get this data in a specific timeframe, for example, =FMPPRICE("BTCUSD",  "Close", "01/01/2024", "01/30/2024")

You can get historical data for many cryptocurrencies at once like this:

#### Forex Currency Rates

Comparing or tracking foreign exchange currencies with FMP is very simple. Here is a full list of the currencies currently offered (over 1,540).

You can also simply use the ticker without the "=x". For example, CADUSD=X for the Canadian dollar price in US dollars. We use CADUSD.

There are two types of data you can get from foreign currencies live data and historical price data.

Using live data you can track or compare currency rates using the FMPPRICE function like this:

This allows you to access the live price and other relevant information about the currency rates you have chosen. You can use the refresh data button at the top of the right add-on at any time to update the functions and view the latest live data.

Historical price data is equally easy to access with the FMPPRICE function.

For example, to get the currency rate close for the last 10 days of US dollars to Canadian dollars, you need to enter =FMPPRICE("USDCAD", "Close", 10)

Or you can also get this data in a specific timeframe, for example, =FMPPRICE("USDCAD", "Close", "01/01/2024", "01/30/2024")

You can get historical data for many currencies at once like this:

#### Commodities/Futures Analysis

Analyzing commodities and futures with FMP is very simple. Here is a full list of commodities/futures currently offered (over 40).

Just make sure to use the exact symbols outlined in the list.

There are two types of data you can get from commodities and futures live data and historical price data.

Using live data you can track or compare prices using the FMPPRICE function like this:

This allows you to access the live price and other relevant information about the commodities you have chosen. You can use the refresh data button at the top of the right add-on at any time to update the functions and view the latest live data.

Historical price data is equally easy to access with the FMPPRICE function.

For example, to get the commodity close price for the last 10 days of soybean meal futures, you need to enter =FMPPRICE("ZMUSD", "Close", 10)

Or you can also get this data in a specific timeframe, for example, =FMPPRICE("ZMUSD", "Close", "01/01/2024", "01/30/2024")

You can get historical data for many commodities at once like this:

#### Indices Tracking

Whether you'd like to compare your investment performance or track your investment in indices like the S&P 500, getting data for indices with FMP is very simple. Here is a full list of the currencies currently offered (over 190).

Just make sure to use the exact symbols outlined in the list.

There are two types of data you can get from indices: live data and historical price data.

Using live data, you can track or compare indices prices using the FMPPRICE function like this:

This allows you to access the live price and other relevant information about the indices you have chosen. You can use the refresh data button at the top of the right add-on at any time to update the functions and view the latest live data.

Historical price data is equally easy to access with the FMPPRICE function.

For example, to get the S&P 500 close price for the last 10 days, you need to enter =FMPPRICE("^GSPC", "Close", 10)

Or you can also get this data in a specific timeframe, for example, =FMPPRICE("^GSPC", "Close", "01/01/2024", "01/30/2024")

You can get historical data for many indices at once like this:

#### Common Issues

These are the most common issues when using the add-on along with their solutions.

#### Cannot Find Stock Ticker to use for International Stocks

FMP uses the same ticker system as per documentation. You can use search or, better yet, the statement dump search to find the right ticker to use.

You can enter the regular ticker followed by the exchange extension. For example, for Telus, a Canadian company listed in the TSX, the ticker is "T" and the extension is ".TO". You can enter "T.TO" to get the data for this company (see available exchanges and their extensions).

#### Unable to Login on Google Sheets

Sometimes Chrome extensions or adblockers may block our authentication system, which allows us to recognize your account.

Alernatively there is an issue with Google allowing us to authenticate your account when being logged into multiple Google accounts at once.

In either case don't worry you can fix this by following these simple solutions.

Solutions

Solution 1:

Delete the add-onRefresh the pageDisable your Adblock on Google SheetsClear your cacheReinstall FMP

Solution 2:

Create a new Google Chrome profileOpen your spreadsheet in the new profileUse FMP as you'd like

#### Functions Return #name Not Recognized by Excel

It is possible that when you download FMP on Excel, you are able to use the statement dump function but unable to use the custom functions.

In most cases, this is because Microsoft requires users to have an Office 365 account to access custom spreadsheet functions.

Solutions

Use FMP on Excel Online or Google Sheets (no Office 365 subscription is required)Use an Office 365 account from work, school, or any other organization if you have access.

#### Cells Contain _xldufd_ in Excel

This typically happens when you save your Excel files on a cloud server like one drive or have an existing add-on affecting the custom function.

Don't worry. There is an easy way to fix all the function calls at once and a way to prevent this from happening altogether.

Solutions

1. Press the “Refresh Errors” button at the top right of the add-on; this will identify those cells and clean them up for you at once:

2. Excel allows you to replace all the cell contents in a tab at once.

Simply head to replace.

Replace all with everything behind the function like _xlduf_ … with nothing.

This will fix all cells at once.

Prevention

To prevent this from happening altogether here are two different things you can try:

Go to File / OptionsSelect Add-ins (near bottom on left), Manage (near bottom), and "Go"Uncheck to remove any Add-ins you are currently not using that may be interfering with the FMP COMSave your Excel files locally as opposed to the cloud

#### URL Fetch Error

URL fetch is a limit that Google Sheets has for requesting data.

Every time you make a function call, a URL fetch call is made to retrieve the data.

Google limits these calls to 20k per day for regular users and 100k for paid accounts. This limit resets automatically every day.

Solutions

There are two solutions. The first is to use the screener functionality as shown here.

The second is using ranges in the functions so you can get more data faster while making fewer function calls.

Alternatively, you can use FMP on Excel, where there are no URL fetch limits, or upgrade your Google account to an enterprise account.

#### #SPILL Error

The spill error happens in Excel or Google Sheets when the function you use returns an array (multiple values in one single function), and there is no space for the data to be displayed.

For example, if you do =FMPPRICE("AAPL", "close", 3), this will return an array with the date and close price for the past 3 trading days.

As you can see, this returns in the #spill error because there is data blocking the function from showing the values.

Solution

Fixing this error is simple, all you need to do is clear all the data that interferes with the function calls you are making, and you will see the cell will clear and you will be able to get the data you want.

#### Stay Ahead with Fresh Data!

Your session has been inactive. For the latest financial insights, please refresh.

Refresh Now
