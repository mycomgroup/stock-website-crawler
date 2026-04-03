---
id: "url-60286575"
type: "api"
title: "Python Financial Library: Installation, Functions, Examples"
url: "https://eodhd.com/financial-apis/python-financial-libraries-and-code-samples"
description: "Python is one of the most popular programming languages, especially when dealing with vast amounts of financial data. Whether you’re developing a standalone app for finance or applying analytical methods to financial data, Python offers numerous solutions. While tools like Google Sheets and Excel add-ons cater to those less familiar with coding, we’ve made significant efforts to enhance the lives of developers by providing EODHD’s official library for API for Python to pull financial statement data and many more. In this article, we will cover installation, all functions, and provide examples, catering to developers in the finance industry who seek the best solutions for various tasks, including scraping financial data from several sources."
source: ""
tags: []
crawl_time: "2026-03-18T09:20:46.426Z"
metadata:
  endpoint: ""
  parameters:
    - {"name":"Live (Delayed) Stock Prices and Macroeconomic Data (doc)","description":"resp = api.get_live_stock_prices(date_from = '2020-01-05', date_to = '2020-02-10', ticker = 'AAPL.US')print(resp)"}
    - {"name":"Bonds Fundamentals (doc)","description":"bonds = api.get_bonds_fundamentals_data (isin = \"US36166NAJ28\")bf = pd.DataFrame(bonds) print(bf)"}
    - {"name":"Intraday Historical Data (doc)","description":"d_by_datetime = api.get_intraday_historical_data(symbol=\"BTC-USD.CC\", interval=\"1m\", from_unix_time='1637982000', to_unix_time=\"1637982900\")print(d_by_datetime)"}
    - {"name":"Historical Dividends (doc)","description":"hd_by_datetime = api.get_historical_dividends_data(ticker = \"GS\", date_from = \"2020-12-10\", date_to = \"2021-04-10\")hd_m = pd.DataFrame(hd_by_datetime)print(hd_m)"}
    - {"name":"Historical Splits (doc)","description":"sd_by_datetime = api.get_historical_splits_data(ticker = \"MS\", date_from = \"2000-01-01\")sd_m = pd.DataFrame(sd_by_datetime)print(sd_m)"}
    - {"name":"Bulk API for EOD, Splits and Dividends (doc)","description":"eod_splits_dividends_extended = api.get_eod_splits_dividends_data (type = \"dividends\", date = \"2020-12-10\", symbols = \"AAPL.US\")esd_m = pd.DataFrame(eod_splits_dividends_extended) print(esd_m) # for Dividendseod_splits_dividends_extended = api.get_eod_splits_dividends_data (type = \"splits\", date = \"2020-12-10\", symbols = \"AAPL.US\")esd_m = pd.DataFrame(eod_splits_dividends_extended) print(esd_m)# for Splits"}
    - {"name":"Calendar. Upcoming Earnings, Trends, IPOs and Splits (doc)","description":"earnings_trends = api.get_earning_trends_data (symbols = \"AAPL.US, MS\") et = pd.DataFrame(earnings_trends)print(et) # for Earnings Trends Dataup_earnings_extended = api.get_upcoming_earnings_data (from_date = \"2020-12-10\", to_date = \"2021-04-10\", symbols = \"AAPL.US\")ue_m = pd.DataFrame (up_earnings_extended)print(ue_m) # for Upcoming Earnings Dataup_ipos_extended = api.get_upcoming_IPOs_data (from_date = \"2020-12-10\", to_date = \"2021-04-10\")ui_m = pd.DataFrame (up_ipos_extended)print(ui_m) # for Upcoming IPOsup_splits_extended = api.get_upcoming_splits_data (from_date = \"2020-12-10\", to_date = \"2021-04-10\")u_split_m = pd.DataFrame (up_splits_extended)print(u_split_m) # for Upcoming Splits"}
    - {"name":"Economic Events (doc)","description":"events_extended = api.get_economic_events_data (date_from = \"2020-12-10\", date_to = \"2021-04-10\", limit = \"200\", country = \"US\", comparison = \"qoq\")ee_m = pd.DataFrame(events_extended) print(ee_m)"}
    - {"name":"Stock Market and Financial News (doc)","description":"news_extended = api.financial_news (from_date = \"2020-12-10\", to_date = \"2021-04-10\", t = \"financial results\", offset = \"200\", limit = \"100\")fn_m = pd.DataFrame(news_extended) print(fn_m)"}
    - {"name":"End of the Day Historical Stock Market Data (doc)","description":"resp = api.get_eod_historical_stock_market_data(symbol = 'AAPL.MX', period='d', from_date = '2023-01-01', to_date = '2023-01-15', order='a')print(resp)"}
    - {"name":"List of supported Exchanges (doc)","description":"l_e = api.get_list_of_exchanges()list_exchages = pd.DataFrame(l_e)print(list_exchages)"}
    - {"name":"Insider Transactions (doc)","description":"insider_extended = api.get_insider_transactions_data(date_from = \"2020-12-10\", date_to = \"2021-04-10\", limit = \"200\")ie_m = pd.DataFrame(insider_extended) print(ie_m)"}
    - {"name":"Macro Indicators (doc)","description":"indicator_extended = api.get_macro_indicators_data (country = \"USA\", indicator = \"real_interest_rate\")indicator_m = pd.DataFrame(indicator_extended) print(indicator_m)"}
    - {"name":"Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History (doc)","description":"exchange_extended = api.get_details_trading_hours_stock_market_holidays (code = \"US\", from_date = \"2023-10-15\", to_date = \"2023-11-15\")e_m = pd.DataFrame (exchange_extended) print(e_m) # for Trading hours and Stock market holidayssymbol_extended = api.symbol_change_history(from_date = \"2022-07-22\", to_date = \"2022-08-10\")s_m = pd.DataFrame(symbol_extended) print(s_m) # for Symbol change history"}
    - {"name":"Stock Market Screener (doc)","description":"screener_extended = api.stock_market_screener (filters = [[\"market_capitalization\",\">\",1000]], limit = \"100\", offset = \"200\")screener_m = pd.DataFrame(screener_extended) print(screener_m)"}
    - {"name":"Technical Indicator (doc)","description":"resp = api.get_technical_indicator_data(ticker = 'AAPL.US', function = 'avgvolccy', period = 100, date_from = '2020-01-05', date_to = '2020-02-10',order = 'a', splitadjusted_only = '0')print(resp)"}
    - {"name":"Historical Market Capitalization (doc)","description":"resp = api.get_historical_market_capitalization_data(ticker = 'AAPL.US', from_date = '2023-01-01', to_date = '2023-01-15')print(resp)"}
    - {"name":"Fundamental Data: Stocks, ETFs, Mutual Funds, Indices and Cryptocurrencies (doc)","description":"resp = api.get_fundamentals_data(ticker = \"AAPL\")fundamental = pd.DataFrame(resp)print(fundamental)"}
  markdownContent: "# Python Financial Library: Installation, Functions, Examples\n\nPython is one of the most popular programming languages, especially when dealing with vast amounts of financial data. Whether you’re developing a standalone app for finance or applying analytical methods to financial data, Python offers numerous solutions. While tools like Google Sheets and Excel add-ons cater to those less familiar with coding, we’ve made significant efforts to enhance the lives of developers by providing EODHD’s official library for API for Python to pull financial statement data and many more. In this article, we will cover installation, all functions, and provide examples, catering to developers in the finance industry who seek the best solutions for various tasks, including scraping financial data from several sources.\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| Live (Delayed) Stock Prices and Macroeconomic Data (doc) | resp = api.get_live_stock_prices(date_from = '2020-01-05', date_to = '2020-02-10', ticker = 'AAPL.US')print(resp) |\n| Bonds Fundamentals (doc) | bonds = api.get_bonds_fundamentals_data (isin = \"US36166NAJ28\")bf = pd.DataFrame(bonds) print(bf) |\n| Intraday Historical Data (doc) | d_by_datetime = api.get_intraday_historical_data(symbol=\"BTC-USD.CC\", interval=\"1m\", from_unix_time='1637982000', to_unix_time=\"1637982900\")print(d_by_datetime) |\n| Historical Dividends (doc) | hd_by_datetime = api.get_historical_dividends_data(ticker = \"GS\", date_from = \"2020-12-10\", date_to = \"2021-04-10\")hd_m = pd.DataFrame(hd_by_datetime)print(hd_m) |\n| Historical Splits (doc) | sd_by_datetime = api.get_historical_splits_data(ticker = \"MS\", date_from = \"2000-01-01\")sd_m = pd.DataFrame(sd_by_datetime)print(sd_m) |\n| Bulk API for EOD, Splits and Dividends (doc) | eod_splits_dividends_extended = api.get_eod_splits_dividends_data (type = \"dividends\", date = \"2020-12-10\", symbols = \"AAPL.US\")esd_m = pd.DataFrame(eod_splits_dividends_extended) print(esd_m) # for Dividendseod_splits_dividends_extended = api.get_eod_splits_dividends_data (type = \"splits\", date = \"2020-12-10\", symbols = \"AAPL.US\")esd_m = pd.DataFrame(eod_splits_dividends_extended) print(esd_m)# for Splits |\n| Calendar. Upcoming Earnings, Trends, IPOs and Splits (doc) | earnings_trends = api.get_earning_trends_data (symbols = \"AAPL.US, MS\") et = pd.DataFrame(earnings_trends)print(et) # for Earnings Trends Dataup_earnings_extended = api.get_upcoming_earnings_data (from_date = \"2020-12-10\", to_date = \"2021-04-10\", symbols = \"AAPL.US\")ue_m = pd.DataFrame (up_earnings_extended)print(ue_m) # for Upcoming Earnings Dataup_ipos_extended = api.get_upcoming_IPOs_data (from_date = \"2020-12-10\", to_date = \"2021-04-10\")ui_m = pd.DataFrame (up_ipos_extended)print(ui_m) # for Upcoming IPOsup_splits_extended = api.get_upcoming_splits_data (from_date = \"2020-12-10\", to_date = \"2021-04-10\")u_split_m = pd.DataFrame (up_splits_extended)print(u_split_m) # for Upcoming Splits |\n| Economic Events (doc) | events_extended = api.get_economic_events_data (date_from = \"2020-12-10\", date_to = \"2021-04-10\", limit = \"200\", country = \"US\", comparison = \"qoq\")ee_m = pd.DataFrame(events_extended) print(ee_m) |\n| Stock Market and Financial News (doc) | news_extended = api.financial_news (from_date = \"2020-12-10\", to_date = \"2021-04-10\", t = \"financial results\", offset = \"200\", limit = \"100\")fn_m = pd.DataFrame(news_extended) print(fn_m) |\n| End of the Day Historical Stock Market Data (doc) | resp = api.get_eod_historical_stock_market_data(symbol = 'AAPL.MX', period='d', from_date = '2023-01-01', to_date = '2023-01-15', order='a')print(resp) |\n| List of supported Exchanges (doc) | l_e = api.get_list_of_exchanges()list_exchages = pd.DataFrame(l_e)print(list_exchages) |\n| Insider Transactions (doc) | insider_extended = api.get_insider_transactions_data(date_from = \"2020-12-10\", date_to = \"2021-04-10\", limit = \"200\")ie_m = pd.DataFrame(insider_extended) print(ie_m) |\n| Macro Indicators (doc) | indicator_extended = api.get_macro_indicators_data (country = \"USA\", indicator = \"real_interest_rate\")indicator_m = pd.DataFrame(indicator_extended) print(indicator_m) |\n| Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History (doc) | exchange_extended = api.get_details_trading_hours_stock_market_holidays (code = \"US\", from_date = \"2023-10-15\", to_date = \"2023-11-15\")e_m = pd.DataFrame (exchange_extended) print(e_m) # for Trading hours and Stock market holidayssymbol_extended = api.symbol_change_history(from_date = \"2022-07-22\", to_date = \"2022-08-10\")s_m = pd.DataFrame(symbol_extended) print(s_m) # for Symbol change history |\n| Stock Market Screener (doc) | screener_extended = api.stock_market_screener (filters = [[\"market_capitalization\",\">\",1000]], limit = \"100\", offset = \"200\")screener_m = pd.DataFrame(screener_extended) print(screener_m) |\n| Technical Indicator (doc) | resp = api.get_technical_indicator_data(ticker = 'AAPL.US', function = 'avgvolccy', period = 100, date_from = '2020-01-05', date_to = '2020-02-10',order = 'a', splitadjusted_only = '0')print(resp) |\n| Historical Market Capitalization (doc) | resp = api.get_historical_market_capitalization_data(ticker = 'AAPL.US', from_date = '2023-01-01', to_date = '2023-01-15')print(resp) |\n| Fundamental Data: Stocks, ETFs, Mutual Funds, Indices and Cryptocurrencies (doc) | resp = api.get_fundamentals_data(ticker = \"AAPL\")fundamental = pd.DataFrame(resp)print(fundamental) |\n\n\n## Official EODHD Python Financial Library installation\n\nThe library grants access to all the key features to work with stock market API in Python. You can find the library with it’s updates on our Github page.\n\n1. Installing EODHD library. Start with the following command:\n\nSee the screenshot:\n\nWait until library will be installed – it will be shown when [*] will change to [1].\n\n2. Importing Required Libraries.  Next, let’s import EODHD library for accessing EODHD API’s functions:\n\nPython Financial Library is installed now.\n\n3. Accessing the EODHD API – to access the EODHD API, we need to create an instance of the “APIClient” class and pass it our API key. In this example, we will use the demo API key provided by EODHD, but in a real application, you should use your registered API key.\n\nor via config file:\n\nNext, we are going to activate EODHD’s API key to get an access to stock data API in Python.\n\n## EODHD API access activation: free and payed options\n\n1. You can start with “DEMO” API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. For these tickers, all of our types of data (APIs), including Real-Time Data, are available without limitations.2. Register for the free plan to receive your API key (limited to 20 API calls per day) with access to End-Of-Day Historical Stock Market Data API for any ticker, but within the past year only. Plus a List of tickers per Exchange is available.3. We recommend to explore our plans, starting from $19.99, to access the necessary type of data without limitations.\n\nThe library is now ready for use. Next, we recommend exploring our Academy section and specifically the article “Download EOD, Intraday, and Real-time Prices for Any Cryptocurrency with Python Simply” by Michael Whittle to fully understand what our API offers.\n\n## Example: End of the day historical stock market data\n\nLets retrieve End of the day historical stock market data:\n\nThe function will return the following JSON respond:\n\nAll the parameters for this function are listed and described here.\n\n## Code Examples\n\n```text\npython3 -m pip install eodhd -U\n```\n\n```text\nfrom eodhd import APIClient\n```\n\n```text\nimport pandas as pd\n```\n\n```text\napi = APIClient(\"<Your_API_Key>\")\n```\n\n```text\nimport os\n\napi_key = os.environ.get(\"<Your_API_Key>\")\napi = APIClient(api_key)\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "python-financial-libraries-and-code-samples"
---

# Python Financial Library: Installation, Functions, Examples

## 源URL

https://eodhd.com/financial-apis/python-financial-libraries-and-code-samples

## 描述

Python is one of the most popular programming languages, especially when dealing with vast amounts of financial data. Whether you’re developing a standalone app for finance or applying analytical methods to financial data, Python offers numerous solutions. While tools like Google Sheets and Excel add-ons cater to those less familiar with coding, we’ve made significant efforts to enhance the lives of developers by providing EODHD’s official library for API for Python to pull financial statement data and many more. In this article, we will cover installation, all functions, and provide examples, catering to developers in the finance industry who seek the best solutions for various tasks, including scraping financial data from several sources.

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Live (Delayed) Stock Prices and Macroeconomic Data (doc)` | - | 否 | - | resp = api.get_live_stock_prices(date_from = '2020-01-05', date_to = '2020-02-10', ticker = 'AAPL.US')print(resp) |
| `Bonds Fundamentals (doc)` | - | 否 | - | bonds = api.get_bonds_fundamentals_data (isin = "US36166NAJ28")bf = pd.DataFrame(bonds) print(bf) |
| `Intraday Historical Data (doc)` | - | 否 | - | d_by_datetime = api.get_intraday_historical_data(symbol="BTC-USD.CC", interval="1m", from_unix_time='1637982000', to_unix_time="1637982900")print(d_by_datetime) |
| `Historical Dividends (doc)` | - | 否 | - | hd_by_datetime = api.get_historical_dividends_data(ticker = "GS", date_from = "2020-12-10", date_to = "2021-04-10")hd_m = pd.DataFrame(hd_by_datetime)print(hd_m) |
| `Historical Splits (doc)` | - | 否 | - | sd_by_datetime = api.get_historical_splits_data(ticker = "MS", date_from = "2000-01-01")sd_m = pd.DataFrame(sd_by_datetime)print(sd_m) |
| `Bulk API for EOD, Splits and Dividends (doc)` | - | 否 | - | eod_splits_dividends_extended = api.get_eod_splits_dividends_data (type = "dividends", date = "2020-12-10", symbols = "AAPL.US")esd_m = pd.DataFrame(eod_splits_dividends_extended) print(esd_m) # for Dividendseod_splits_dividends_extended = api.get_eod_splits_dividends_data (type = "splits", date = "2020-12-10", symbols = "AAPL.US")esd_m = pd.DataFrame(eod_splits_dividends_extended) print(esd_m)# for Splits |
| `Calendar. Upcoming Earnings, Trends, IPOs and Splits (doc)` | - | 否 | - | earnings_trends = api.get_earning_trends_data (symbols = "AAPL.US, MS") et = pd.DataFrame(earnings_trends)print(et) # for Earnings Trends Dataup_earnings_extended = api.get_upcoming_earnings_data (from_date = "2020-12-10", to_date = "2021-04-10", symbols = "AAPL.US")ue_m = pd.DataFrame (up_earnings_extended)print(ue_m) # for Upcoming Earnings Dataup_ipos_extended = api.get_upcoming_IPOs_data (from_date = "2020-12-10", to_date = "2021-04-10")ui_m = pd.DataFrame (up_ipos_extended)print(ui_m) # for Upcoming IPOsup_splits_extended = api.get_upcoming_splits_data (from_date = "2020-12-10", to_date = "2021-04-10")u_split_m = pd.DataFrame (up_splits_extended)print(u_split_m) # for Upcoming Splits |
| `Economic Events (doc)` | - | 否 | - | events_extended = api.get_economic_events_data (date_from = "2020-12-10", date_to = "2021-04-10", limit = "200", country = "US", comparison = "qoq")ee_m = pd.DataFrame(events_extended) print(ee_m) |
| `Stock Market and Financial News (doc)` | - | 否 | - | news_extended = api.financial_news (from_date = "2020-12-10", to_date = "2021-04-10", t = "financial results", offset = "200", limit = "100")fn_m = pd.DataFrame(news_extended) print(fn_m) |
| `End of the Day Historical Stock Market Data (doc)` | - | 否 | - | resp = api.get_eod_historical_stock_market_data(symbol = 'AAPL.MX', period='d', from_date = '2023-01-01', to_date = '2023-01-15', order='a')print(resp) |
| `List of supported Exchanges (doc)` | - | 否 | - | l_e = api.get_list_of_exchanges()list_exchages = pd.DataFrame(l_e)print(list_exchages) |
| `Insider Transactions (doc)` | - | 否 | - | insider_extended = api.get_insider_transactions_data(date_from = "2020-12-10", date_to = "2021-04-10", limit = "200")ie_m = pd.DataFrame(insider_extended) print(ie_m) |
| `Macro Indicators (doc)` | - | 否 | - | indicator_extended = api.get_macro_indicators_data (country = "USA", indicator = "real_interest_rate")indicator_m = pd.DataFrame(indicator_extended) print(indicator_m) |
| `Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History (doc)` | - | 否 | - | exchange_extended = api.get_details_trading_hours_stock_market_holidays (code = "US", from_date = "2023-10-15", to_date = "2023-11-15")e_m = pd.DataFrame (exchange_extended) print(e_m) # for Trading hours and Stock market holidayssymbol_extended = api.symbol_change_history(from_date = "2022-07-22", to_date = "2022-08-10")s_m = pd.DataFrame(symbol_extended) print(s_m) # for Symbol change history |
| `Stock Market Screener (doc)` | - | 否 | - | screener_extended = api.stock_market_screener (filters = [["market_capitalization",">",1000]], limit = "100", offset = "200")screener_m = pd.DataFrame(screener_extended) print(screener_m) |
| `Technical Indicator (doc)` | - | 否 | - | resp = api.get_technical_indicator_data(ticker = 'AAPL.US', function = 'avgvolccy', period = 100, date_from = '2020-01-05', date_to = '2020-02-10',order = 'a', splitadjusted_only = '0')print(resp) |
| `Historical Market Capitalization (doc)` | - | 否 | - | resp = api.get_historical_market_capitalization_data(ticker = 'AAPL.US', from_date = '2023-01-01', to_date = '2023-01-15')print(resp) |
| `Fundamental Data: Stocks, ETFs, Mutual Funds, Indices and Cryptocurrencies (doc)` | - | 否 | - | resp = api.get_fundamentals_data(ticker = "AAPL")fundamental = pd.DataFrame(resp)print(fundamental) |

## 文档正文

Python is one of the most popular programming languages, especially when dealing with vast amounts of financial data. Whether you’re developing a standalone app for finance or applying analytical methods to financial data, Python offers numerous solutions. While tools like Google Sheets and Excel add-ons cater to those less familiar with coding, we’ve made significant efforts to enhance the lives of developers by providing EODHD’s official library for API for Python to pull financial statement data and many more. In this article, we will cover installation, all functions, and provide examples, catering to developers in the finance industry who seek the best solutions for various tasks, including scraping financial data from several sources.

## Parameters

| Parameter | Description |
|-----------|-------------|
| Live (Delayed) Stock Prices and Macroeconomic Data (doc) | resp = api.get_live_stock_prices(date_from = '2020-01-05', date_to = '2020-02-10', ticker = 'AAPL.US')print(resp) |
| Bonds Fundamentals (doc) | bonds = api.get_bonds_fundamentals_data (isin = "US36166NAJ28")bf = pd.DataFrame(bonds) print(bf) |
| Intraday Historical Data (doc) | d_by_datetime = api.get_intraday_historical_data(symbol="BTC-USD.CC", interval="1m", from_unix_time='1637982000', to_unix_time="1637982900")print(d_by_datetime) |
| Historical Dividends (doc) | hd_by_datetime = api.get_historical_dividends_data(ticker = "GS", date_from = "2020-12-10", date_to = "2021-04-10")hd_m = pd.DataFrame(hd_by_datetime)print(hd_m) |
| Historical Splits (doc) | sd_by_datetime = api.get_historical_splits_data(ticker = "MS", date_from = "2000-01-01")sd_m = pd.DataFrame(sd_by_datetime)print(sd_m) |
| Bulk API for EOD, Splits and Dividends (doc) | eod_splits_dividends_extended = api.get_eod_splits_dividends_data (type = "dividends", date = "2020-12-10", symbols = "AAPL.US")esd_m = pd.DataFrame(eod_splits_dividends_extended) print(esd_m) # for Dividendseod_splits_dividends_extended = api.get_eod_splits_dividends_data (type = "splits", date = "2020-12-10", symbols = "AAPL.US")esd_m = pd.DataFrame(eod_splits_dividends_extended) print(esd_m)# for Splits |
| Calendar. Upcoming Earnings, Trends, IPOs and Splits (doc) | earnings_trends = api.get_earning_trends_data (symbols = "AAPL.US, MS") et = pd.DataFrame(earnings_trends)print(et) # for Earnings Trends Dataup_earnings_extended = api.get_upcoming_earnings_data (from_date = "2020-12-10", to_date = "2021-04-10", symbols = "AAPL.US")ue_m = pd.DataFrame (up_earnings_extended)print(ue_m) # for Upcoming Earnings Dataup_ipos_extended = api.get_upcoming_IPOs_data (from_date = "2020-12-10", to_date = "2021-04-10")ui_m = pd.DataFrame (up_ipos_extended)print(ui_m) # for Upcoming IPOsup_splits_extended = api.get_upcoming_splits_data (from_date = "2020-12-10", to_date = "2021-04-10")u_split_m = pd.DataFrame (up_splits_extended)print(u_split_m) # for Upcoming Splits |
| Economic Events (doc) | events_extended = api.get_economic_events_data (date_from = "2020-12-10", date_to = "2021-04-10", limit = "200", country = "US", comparison = "qoq")ee_m = pd.DataFrame(events_extended) print(ee_m) |
| Stock Market and Financial News (doc) | news_extended = api.financial_news (from_date = "2020-12-10", to_date = "2021-04-10", t = "financial results", offset = "200", limit = "100")fn_m = pd.DataFrame(news_extended) print(fn_m) |
| End of the Day Historical Stock Market Data (doc) | resp = api.get_eod_historical_stock_market_data(symbol = 'AAPL.MX', period='d', from_date = '2023-01-01', to_date = '2023-01-15', order='a')print(resp) |
| List of supported Exchanges (doc) | l_e = api.get_list_of_exchanges()list_exchages = pd.DataFrame(l_e)print(list_exchages) |
| Insider Transactions (doc) | insider_extended = api.get_insider_transactions_data(date_from = "2020-12-10", date_to = "2021-04-10", limit = "200")ie_m = pd.DataFrame(insider_extended) print(ie_m) |
| Macro Indicators (doc) | indicator_extended = api.get_macro_indicators_data (country = "USA", indicator = "real_interest_rate")indicator_m = pd.DataFrame(indicator_extended) print(indicator_m) |
| Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History (doc) | exchange_extended = api.get_details_trading_hours_stock_market_holidays (code = "US", from_date = "2023-10-15", to_date = "2023-11-15")e_m = pd.DataFrame (exchange_extended) print(e_m) # for Trading hours and Stock market holidayssymbol_extended = api.symbol_change_history(from_date = "2022-07-22", to_date = "2022-08-10")s_m = pd.DataFrame(symbol_extended) print(s_m) # for Symbol change history |
| Stock Market Screener (doc) | screener_extended = api.stock_market_screener (filters = [["market_capitalization",">",1000]], limit = "100", offset = "200")screener_m = pd.DataFrame(screener_extended) print(screener_m) |
| Technical Indicator (doc) | resp = api.get_technical_indicator_data(ticker = 'AAPL.US', function = 'avgvolccy', period = 100, date_from = '2020-01-05', date_to = '2020-02-10',order = 'a', splitadjusted_only = '0')print(resp) |
| Historical Market Capitalization (doc) | resp = api.get_historical_market_capitalization_data(ticker = 'AAPL.US', from_date = '2023-01-01', to_date = '2023-01-15')print(resp) |
| Fundamental Data: Stocks, ETFs, Mutual Funds, Indices and Cryptocurrencies (doc) | resp = api.get_fundamentals_data(ticker = "AAPL")fundamental = pd.DataFrame(resp)print(fundamental) |

## Official EODHD Python Financial Library installation

The library grants access to all the key features to work with stock market API in Python. You can find the library with it’s updates on our Github page.

1. Installing EODHD library. Start with the following command:

See the screenshot:

Wait until library will be installed – it will be shown when [*] will change to [1].

2. Importing Required Libraries.  Next, let’s import EODHD library for accessing EODHD API’s functions:

Python Financial Library is installed now.

3. Accessing the EODHD API – to access the EODHD API, we need to create an instance of the “APIClient” class and pass it our API key. In this example, we will use the demo API key provided by EODHD, but in a real application, you should use your registered API key.

or via config file:

Next, we are going to activate EODHD’s API key to get an access to stock data API in Python.

## EODHD API access activation: free and payed options

1. You can start with “DEMO” API key to test the data for a few tickers only: AAPL.US, TSLA.US , VTI.US, AMZN.US, BTC-USD and EUR-USD. For these tickers, all of our types of data (APIs), including Real-Time Data, are available without limitations.2. Register for the free plan to receive your API key (limited to 20 API calls per day) with access to End-Of-Day Historical Stock Market Data API for any ticker, but within the past year only. Plus a List of tickers per Exchange is available.3. We recommend to explore our plans, starting from $19.99, to access the necessary type of data without limitations.

The library is now ready for use. Next, we recommend exploring our Academy section and specifically the article “Download EOD, Intraday, and Real-time Prices for Any Cryptocurrency with Python Simply” by Michael Whittle to fully understand what our API offers.

## Example: End of the day historical stock market data

Lets retrieve End of the day historical stock market data:

The function will return the following JSON respond:

All the parameters for this function are listed and described here.

## Code Examples

```text
python3 -m pip install eodhd -U
```

```text
from eodhd import APIClient
```

```text
import pandas as pd
```

```text
api = APIClient("<Your_API_Key>")
```

```text
import os

api_key = os.environ.get("<Your_API_Key>")
api = APIClient(api_key)
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
