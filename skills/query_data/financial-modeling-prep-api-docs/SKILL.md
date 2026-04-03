# Financial Modeling Prep API Documentation

A comprehensive API documentation for accessing financial market data, company information, and analytical tools.

## Overview

Financial Modeling Prep (FMP) API provides extensive financial data for investors, traders, analysts, and developers. The API offers real-time and historical data for stocks, ETFs, forex, cryptocurrencies, commodities, and more.

### Key Features
- Real-time stock quotes and market data
- Comprehensive financial statements (Income, Balance Sheet, Cash Flow)
- Historical price data with multiple intervals
- Technical indicators and charting data
- News, SEC filings, and earnings data
- ETF and mutual fund holdings
- Insider trading and institutional ownership
- Analyst ratings and price targets
- ESG scores and sustainability metrics

### Base URL
```
https://financialmodelingprep.com/stable
```

### Authentication
All API requests require an API key passed as a query parameter:
```
?apikey=YOUR_API_KEY
```

**Example:**
```
https://financialmodelingprep.com/stable/quote?symbol=AAPL&apikey=YOUR_API_KEY
```

### Response Format
All API responses are returned in JSON format.

---

## 1. Stock Quotes & Real-Time Data

Real-time stock quotes and market data for individual stocks and batch requests.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Stock Quote** | `GET /quote?symbol={symbol}` | Real-time stock quote with price, change, volume, market cap, and key metrics |
| **Stock Quote Short** | `GET /quote-short?symbol={symbol}` | Lightweight stock quote with essential fields |
| **Batch Quote** | `GET /batch-quote?symbols={symbols}` | Multiple stock quotes in a single request |
| **Batch Quote Short** | `GET /batch-quote-short?symbols={symbols}` | Lightweight batch quotes |
| **Quote Change** | `GET /quote-change?symbol={symbol}` | Stock price change data |
| **All Real-Time Prices** | `GET /quote` | Quotes for all available stocks |
| **Market Leaders** | | |
| - Biggest Gainers | `GET /biggest-gainers` | Top gaining stocks for the day |
| - Biggest Losers | `GET /biggest-losers` | Top losing stocks for the day |
| - Most Active | `GET /most-active` | Most actively traded stocks |

**Example Response (Quote):**
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "price": 232.8,
  "changePercentage": 2.1008,
  "change": 4.79,
  "volume": 44489128,
  "dayLow": 226.65,
  "dayHigh": 233.13,
  "yearHigh": 260.1,
  "yearLow": 164.08,
  "marketCap": 3500823120000,
  "exchange": "NASDAQ",
  "open": 227.2,
  "previousClose": 228.01,
  "timestamp": 1738702801
}
```

---

## 2. Historical Prices & Charts

End-of-day and intraday historical price data for technical analysis.

### 2.1 End-of-Day Prices

| API | Endpoint | Description |
|-----|----------|-------------|
| **EOD Full** | `GET /historical-price-eod/full?symbol={symbol}` | Complete daily price data with OHLCV, change, VWAP |
| **EOD Light** | `GET /historical-price-eod/light?symbol={symbol}` | Lightweight daily price data |
| **EOD Dividend Adjusted** | `GET /historical-price-eod/dividend-adjusted?symbol={symbol}` | Dividend-adjusted historical prices |
| **EOD Non-Split Adjusted** | `GET /historical-price-eod/non-split-adjusted?symbol={symbol}` | Non-split adjusted historical prices |

### 2.2 Intraday Charts

| Interval | Endpoint | Description |
|----------|----------|-------------|
| **1 Minute** | `GET /historical-chart/1min?symbol={symbol}` | 1-minute interval data |
| **5 Minutes** | `GET /historical-chart/5min?symbol={symbol}` | 5-minute interval data |
| **15 Minutes** | `GET /historical-chart/15min?symbol={symbol}` | 15-minute interval data |
| **30 Minutes** | `GET /historical-chart/30min?symbol={symbol}` | 30-minute interval data |
| **1 Hour** | `GET /historical-chart/1hour?symbol={symbol}` | 1-hour interval data |
| **4 Hours** | `GET /historical-chart/4hour?symbol={symbol}` | 4-hour interval data |

**Parameters:**
- `symbol` (required): Stock symbol
- `from`: Start date (YYYY-MM-DD)
- `to`: End date (YYYY-MM-DD)

**Example Response:**
```json
{
  "symbol": "AAPL",
  "date": "2025-02-04",
  "open": 227.2,
  "high": 233.13,
  "low": 226.65,
  "close": 232.8,
  "volume": 44489128,
  "change": 5.6,
  "changePercent": 2.46479,
  "vwap": 230.86
}
```

---

## 3. Financial Statements

Comprehensive financial statement data including income statements, balance sheets, and cash flow statements.

### 3.1 Standard Financial Statements

| Statement | Endpoint | Description |
|-----------|----------|-------------|
| **Income Statement** | `GET /income-statement?symbol={symbol}` | Quarterly/annual income statements |
| **Income Statement TTM** | `GET /income-statements-ttm?symbol={symbol}` | Trailing twelve months income data |
| **Balance Sheet** | `GET /balance-sheet-statement?symbol={symbol}` | Quarterly/annual balance sheets |
| **Balance Sheet TTM** | `GET /balance-sheet-statements-ttm?symbol={symbol}` | TTM balance sheet data |
| **Cash Flow Statement** | `GET /cash-flow-statement?symbol={symbol}` | Quarterly/annual cash flow statements |
| **Cash Flow TTM** | `GET /cashflow-statements-ttm?symbol={symbol}` | TTM cash flow data |

### 3.2 As-Reported Statements (Unadjusted)

| Statement | Endpoint |
|-----------|----------|
| **As-Reported Income** | `GET /as-reported-income-statements?symbol={symbol}` |
| **As-Reported Balance** | `GET /as-reported-balance-statements?symbol={symbol}` |
| **As-Reported Cash Flow** | `GET /as-reported-cashflow-statements?symbol={symbol}` |
| **Full As-Reported** | `GET /as-reported-financial-statements?symbol={symbol}` |

### 3.3 Growth & Bulk Data

| API | Endpoint | Description |
|-----|----------|-------------|
| **Income Growth** | `GET /income-statement-growth?symbol={symbol}` | Income statement growth rates |
| **Balance Growth** | `GET /balance-sheet-statement-growth?symbol={symbol}` | Balance sheet growth rates |
| **Cash Flow Growth** | `GET /cashflow-statement-growth?symbol={symbol}` | Cash flow growth rates |
| **Income Bulk** | `GET /income-statement-bulk` | Bulk income statements |
| **Balance Bulk** | `GET /balance-sheet-statement-bulk` | Bulk balance sheets |
| **Cash Flow Bulk** | `GET /cash-flow-statement-bulk` | Bulk cash flow statements |
| **Income Growth Bulk** | `GET /income-statement-growth-bulk` | Bulk income growth |
| **Balance Growth Bulk** | `GET /balance-sheet-statement-growth-bulk` | Bulk balance growth |
| **Cash Flow Growth Bulk** | `GET /cash-flow-statement-growth-bulk` | Bulk cash flow growth |
| **Financial Growth** | `GET /financial-statement-growth?symbol={symbol}` | Combined financial growth metrics |
| **Latest Financials** | `GET /financials-latest` | Most recent financial statements |

**Parameters:**
- `symbol` (required): Stock symbol
- `period`: `annual` or `quarter` (default: annual)
- `limit`: Number of periods to return

---

## 4. Company Information & Profile

Detailed company profiles, executive information, and corporate data.

### 4.1 Company Profile

| API | Endpoint | Description |
|-----|----------|-------------|
| **Company Profile** | `GET /profile?symbol={symbol}` | Comprehensive company profile with financial metrics |
| **Profile by CIK** | `GET /profile-cik?cik={cik}` | Company profile by CIK number |
| **Profile Bulk** | `GET /profile-bulk` | Bulk company profiles |

**Profile Response Fields:**
- Company name, description, industry, sector
- CEO, website, contact information
- Market cap, stock price, beta, dividend
- CIK, ISIN, CUSIP identifiers
- Exchange, country, employees
- IPO date, trading status flags

### 4.2 Company Data

| API | Endpoint | Description |
|-----|----------|-------------|
| **Company Executives** | `GET /company-executives?symbol={symbol}` | Key executives and officers |
| **Employee Count** | `GET /employee-count?symbol={symbol}` | Current employee count |
| **Historical Employee Count** | `GET /historical-employee-count?symbol={symbol}` | Employee count history |
| **Company Notes** | `GET /company-notes?symbol={symbol}` | Company debt notes and obligations |
| **Enterprise Value** | `GET /enterprise-values?symbol={symbol}` | Enterprise value metrics |
| **Market Cap** | `GET /market-cap?symbol={symbol}` | Market capitalization data |
| **Historical Market Cap** | `GET /historical-market-cap?symbol={symbol}` | Historical market cap |
| **Shares Float** | `GET /shares-float?symbol={symbol}` | Shares float information |
| **All Shares Float** | `GET /all-shares-float` | Float data for all companies |
| **Stock Peers** | `GET /peers?symbol={symbol}` | Comparable companies |
| **Peers Bulk** | `GET /peers-bulk` | Bulk peer data |
| **Delisted Companies** | `GET /delisted-companies` | List of delisted companies |
| **Actively Trading List** | `GET /actively-trading-list` | All actively trading companies |

### 4.3 Revenue Segmentation

| API | Endpoint | Description |
|-----|----------|-------------|
| **Revenue Geographic** | `GET /revenue-geographic-segments?symbol={symbol}` | Revenue by geographic region |
| **Revenue Product** | `GET /revenue-product-segmentation?symbol={symbol}` | Revenue by product line |

### 4.4 SEC Company Profile

| API | Endpoint | Description |
|-----|----------|-------------|
| **SEC Full Profile** | `GET /sec-company-full-profile?symbol={symbol}` | Complete SEC profile data |

---

## 5. Key Metrics & Financial Ratios

Pre-calculated financial metrics and ratios for analysis.

### 5.1 Key Metrics

| API | Endpoint | Description |
|-----|----------|-------------|
| **Key Metrics** | `GET /key-metrics?symbol={symbol}` | Comprehensive financial ratios and KPIs |
| **Key Metrics TTM** | `GET /key-metrics-ttm?symbol={symbol}` | Trailing twelve months metrics |
| **Key Metrics TTM Bulk** | `GET /key-metrics-ttm-bulk` | Bulk TTM metrics |

**Metrics Include:**
- Valuation: Market cap, enterprise value, P/E ratios, EV multiples
- Profitability: ROA, ROE, ROIC, margins
- Liquidity: Current ratio, working capital
- Efficiency: Asset turnover, inventory days
- Graham metrics, FCF yield, earnings yield

### 5.2 Financial Ratios

| API | Endpoint | Description |
|-----|----------|-------------|
| **Ratios** | `GET /metrics-ratios?symbol={symbol}` | Financial ratio analysis |
| **Ratios TTM** | `GET /metrics-ratios-ttm?symbol={symbol}` | TTM financial ratios |
| **Ratios TTM Bulk** | `GET /ratios-ttm-bulk` | Bulk TTM ratios |

### 5.3 Financial Scores

| API | Endpoint | Description |
|-----|----------|-------------|
| **Financial Scores** | `GET /financial-scores?symbol={symbol}` | Altman Z-score, Piotroski F-score |
| **Scores Bulk** | `GET /scores-bulk` | Bulk financial scores |
| **Owner Earnings** | `GET /owner-earnings?symbol={symbol}` | Owner earnings calculation |

---

## 6. Calendars & Corporate Events

Upcoming and historical corporate events and calendars.

### 6.1 Earnings

| API | Endpoint | Description |
|-----|----------|-------------|
| **Earnings Calendar** | `GET /earnings-calendar` | Upcoming earnings announcements |
| **Earnings by Company** | `GET /earnings-company?symbol={symbol}` | Company-specific earnings |
| **Earnings Surprises** | `GET /earnings-surprises-bulk` | Earnings surprise data |

### 6.2 Dividends & Splits

| API | Endpoint | Description |
|-----|----------|-------------|
| **Dividends Calendar** | `GET /dividends-calendar` | Upcoming dividend payments |
| **Dividends by Company** | `GET /dividends-company?symbol={symbol}` | Company dividend history |
| **Stock Splits Calendar** | `GET /splits-calendar` | Upcoming stock splits |
| **Splits by Company** | `GET /splits-company?symbol={symbol}` | Company split history |

### 6.3 IPOs

| API | Endpoint | Description |
|-----|----------|-------------|
| **IPOs Calendar** | `GET /ipos-calendar` | Upcoming IPOs |
| **IPOs Disclosure** | `GET /ipos-disclosure` | IPO disclosure filings |
| **IPOs Prospectus** | `GET /ipos-prospectus` | IPO prospectus documents |

### 6.4 Economics Calendar

| API | Endpoint | Description |
|-----|----------|-------------|
| **Economics Calendar** | `GET /economics-calendar` | Economic events and releases |

---

## 7. News & Press Releases

Real-time news and press releases for stocks and markets.

### 7.1 Stock News

| API | Endpoint | Description |
|-----|----------|-------------|
| **Stock News** | `GET /news/stock-latest` | Latest stock market news |
| **Search Stock News** | `GET /search-stock-news` | Search stock news articles |
| **FMP Articles** | `GET /fmp-articles` | FMP editorial content |

### 7.2 Press Releases

| API | Endpoint | Description |
|-----|----------|-------------|
| **Press Releases** | `GET /press-releases?symbol={symbol}` | Company press releases |
| **Search Press Releases** | `GET /search-press-releases` | Search press releases |
| **General News** | `GET /general-news` | General financial news |

### 7.3 Crypto & Forex News

| API | Endpoint | Description |
|-----|----------|-------------|
| **Crypto News** | `GET /crypto-news` | Cryptocurrency news |
| **Search Crypto News** | `GET /search-crypto-news` | Search crypto news |
| **Forex News** | `GET /forex-news` | Forex market news |
| **Search Forex News** | `GET /search-forex-news` | Search forex news |

**News Response Fields:**
```json
{
  "symbol": "AAPL",
  "publishedDate": "2025-02-03 23:53:40",
  "publisher": "Seeking Alpha",
  "title": "Article Title",
  "image": "https://images.financialmodelingprep.com/news/...",
  "site": "seekingalpha.com",
  "text": "Article summary text...",
  "url": "https://seekingalpha.com/article/..."
}
```

---

## 8. SEC Filings

SEC filing data and document access.

### 8.1 Latest Filings

| API | Endpoint | Description |
|-----|----------|-------------|
| **Latest Filings** | `GET /latest-filings` | Most recent SEC filings |
| **Latest 8-K** | `GET /8k-latest` | Latest 8-K filings |

### 8.2 Filing Search & Access

| API | Endpoint | Description |
|-----|----------|-------------|
| **Search by CIK** | `GET /search-by-cik` | Search filings by CIK |
| **Search by Symbol** | `GET /search-by-symbol` | Search filings by symbol |
| **Search by Name** | `GET /search-by-name` | Search filings by company name |
| **Search by Form Type** | `GET /search-by-form-type` | Search by filing type |
| **Filings Extract** | `GET /filings-extract` | Extract filing data |
| **Filings with Analytics** | `GET /filings-extract-with-analytics-by-holder` | Filing analytics |

### 8.3 Form 13F (Institutional Holdings)

| API | Endpoint | Description |
|-----|----------|-------------|
| **Form 13F Dates** | `GET /form-13f-filings-dates` | Available 13F filing dates |

### 8.4 Financial Reports

| API | Endpoint | Description |
|-----|----------|-------------|
| **Financial Reports Dates** | `GET /financial-reports-dates?symbol={symbol}` | Available report dates |
| **Form 10-K JSON** | `GET /financial-reports-form-10-k-json` | 10-K filing data (JSON) |
| **Form 10-K XLSX** | `GET /financial-reports-form-10-k-xlsx` | 10-K filing data (Excel) |

---

## 9. Earnings Transcripts

Earnings call transcripts and related data.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Transcript List** | `GET /earnings-transcript-list` | Available transcripts |
| **Latest Transcripts** | `GET /latest-transcripts` | Most recent transcripts |
| **Search Transcripts** | `GET /search-transcripts` | Search transcripts |
| **Transcript Symbols** | `GET /available-transcript-symbols` | Symbols with transcripts |
| **Transcript Dates** | `GET /transcripts-dates-by-symbol?symbol={symbol}` | Available transcript dates |

---

## 10. ETFs & Mutual Funds

ETF holdings, mutual fund data, and related information.

### 10.1 ETFs

| API | Endpoint | Description |
|-----|----------|-------------|
| **ETFs List** | `GET /etfs-list` | List of all ETFs |
| **ETF Holder Bulk** | `GET /etf-holder-bulk` | Complete ETF holdings data |
| **ETF Asset Exposure** | `GET /etf-asset-exposure?symbol={symbol}` | ETF asset breakdown |
| **Country Weighting** | `GET /country-weighting?symbol={symbol}` | Geographic allocation |
| **Sector Weighting** | `GET /sector-weighting?symbol={symbol}` | Sector allocation |
| **Full ETF Quotes** | `GET /full-etf-quotes` | Complete ETF quotes |

### 10.2 Mutual Funds

| API | Endpoint | Description |
|-----|----------|-------------|
| **Mutual Fund Disclosures** | `GET /mutual-fund-disclosures` | Fund disclosures |
| **Full Mutual Fund Quotes** | `GET /full-mutualfund-quotes` | Complete mutual fund quotes |

---

## 11. Market Indices

Major market indices data and historical information.

### 11.1 Index Lists & Quotes

| API | Endpoint | Description |
|-----|----------|-------------|
| **Indexes List** | `GET /indexes-list` | Available market indices |
| **All Index Quotes** | `GET /all-index-quotes` | Quotes for all indices |
| **Index Quote** | `GET /index-quote?symbol={symbol}` | Specific index quote |
| **Index Quote Short** | `GET /index-quote-short?symbol={symbol}` | Lightweight index quote |
| **Full Index Quotes** | `GET /full-index-quotes` | Complete index data |

### 11.2 Major Indices

| Index | Description |
|-------|-------------|
| **S&P 500** | S&P 500 companies and data |
| **Dow Jones** | Dow Jones Industrial Average |
| **NASDAQ** | NASDAQ Composite data |

| API | Endpoint | Description |
|-----|----------|-------------|
| **S&P 500** | `GET /sp-500` | S&P 500 constituents |
| **Dow Jones** | `GET /dow-jones` | Dow Jones constituents |
| **NASDAQ** | `GET /nasdaq` | NASDAQ constituents |
| **Historical S&P 500** | `GET /historical-sp-500` | Historical S&P 500 data |
| **Historical Dow Jones** | `GET /historical-dow-jones` | Historical Dow Jones data |
| **Historical NASDAQ** | `GET /historical-nasdaq` | Historical NASDAQ data |

### 11.3 Index Historical Data

| API | Endpoint | Description |
|-----|----------|-------------|
| **Index EOD Full** | `GET /index-historical-price-eod/full` | Complete index history |
| **Index EOD Light** | `GET /index-historical-price-eod/light` | Lightweight index history |
| **Index Intraday 1min** | `GET /index-intraday-1-min` | 1-minute index data |
| **Index Intraday 5min** | `GET /index-intraday-5-min` | 5-minute index data |
| **Index Intraday 1hour** | `GET /index-intraday-1-hour` | Hourly index data |

---

## 12. Technical Indicators

Calculated technical indicators for technical analysis.

| Indicator | Endpoint | Description |
|-----------|----------|-------------|
| **Simple Moving Average** | `GET /technical-indicators/sma` | SMA calculation |
| **Exponential Moving Average** | `GET /technical-indicators/ema` | EMA calculation |
| **Weighted Moving Average** | `GET /technical-indicators/wma` | WMA calculation |
| **Double EMA** | `GET /technical-indicators/dema` | DEMA calculation |
| **Triple EMA** | `GET /technical-indicators/tema` | TEMA calculation |
| **Relative Strength Index** | `GET /technical-indicators/rsi` | RSI calculation |
| **Average Directional Index** | `GET /technical-indicators/adx` | ADX calculation |
| **Standard Deviation** | `GET /technical-indicators/std` | Standard deviation |

**Parameters:**
- `symbol` (required): Stock symbol
- `periodLength`: Indicator period (default: 14)
- `timeframe`: `1min`, `5min`, `15min`, `30min`, `1hour`, `4hour`, `1day`

**Example Response:**
```json
{
  "date": "2025-02-04 00:00:00",
  "open": 227.2,
  "high": 233.13,
  "low": 226.65,
  "close": 232.8,
  "volume": 44489128,
  "rsi": 47.64507340768903
}
```

---

## 13. Industry & Sector Data

Industry classifications, performance metrics, and sector analysis.

### 13.1 Classifications

| API | Endpoint | Description |
|-----|----------|-------------|
| **All Industry Classification** | `GET /all-industry-classification` | Complete industry taxonomy |
| **Industry Classification List** | `GET /industry-classification-list` | Industry categories |
| **Industry Search** | `GET /industry-classification-search` | Search industries |
| **Available Sectors** | `GET /available-sectors` | All sectors |
| **Available Industries** | `GET /available-industries` | All industries |
| **Available Exchanges** | `GET /available-exchanges` | All exchanges |
| **Available Countries** | `GET /available-countries` | All countries |

### 13.2 Performance & Valuation

| API | Endpoint | Description |
|-----|----------|-------------|
| **Industry Performance** | `GET /industry-performance-snapshot` | Real-time industry performance |
| **Historical Industry Performance** | `GET /historical-industry-performance` | Historical performance |
| **Industry PE Snapshot** | `GET /industry-pe-snapshot` | Current industry P/E ratios |
| **Historical Industry PE** | `GET /historical-industry-pe` | Historical P/E by industry |
| **Sector Performance** | `GET /sector-performance-snapshot` | Real-time sector performance |
| **Historical Sector Performance** | `GET /historical-sector-performance` | Historical sector data |
| **Sector PE Snapshot** | `GET /sector-pe-snapshot` | Current sector P/E ratios |
| **Historical Sector PE** | `GET /historical-sector-pe` | Historical P/E by sector |
| **Industry Summary** | `GET /industry-summary` | Industry overview data |

---

## 14. Insider Trading

Insider trading data and transaction tracking.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Latest Insider Trades** | `GET /latest-insider-trade` | Most recent insider transactions |
| **Insider Trade Statistics** | `GET /insider-trade-statistics` | Insider trading analytics |
| **Search Insider Trades** | `GET /search-insider-trades` | Search insider transactions |
| **All Transaction Types** | `GET /all-transaction-types` | Types of insider transactions |

---

## 15. Institutional Holdings

Institutional ownership and 13F filing data.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Institutional Holders** | `GET /institutional-holders` | List of institutional holders |
| **Institutional Holders Search** | `GET /institutional-holders-search` | Search holders |
| **Holdings Date Available** | `GET /institutional-holdings-date-available` | Available filing dates |
| **Holdings List** | `GET /institutional-holdings-list` | Holdings data |
| **Portfolio Composition** | `GET /institutional-holdings-portfolio-composition` | Portfolio breakdown |
| **Industry Summary** | `GET /institutional-holdings-portfolio-industry-summary` | Industry allocation |
| **Positions Summary** | `GET /institutional-holdings-portfolio-positions-summary` | Position details |
| **Holders Industry Breakdown** | `GET /holders-industry-breakdown` | Industry breakdown |
| **Holder Performance Summary** | `GET /holder-performance-summary` | Performance analytics |
| **Institutional Ownership** | `GET /institutional-ownership-by-shares-held-and-date` | Ownership data |

---

## 16. Analyst Data & Ratings

Analyst ratings, price targets, and estimates.

### 16.1 Ratings & Grades

| API | Endpoint | Description |
|-----|----------|-------------|
| **Grades** | `GET /grades?symbol={symbol}` | Analyst grades |
| **Grades Summary** | `GET /grades-summary?symbol={symbol}` | Grade summary |
| **Historical Grades** | `GET /historical-grades?symbol={symbol}` | Historical ratings |
| **Ratings Snapshot** | `GET /ratings-snapshot` | Current ratings overview |
| **Historical Ratings** | `GET /historical-ratings?symbol={symbol}` | Historical rating changes |
| **Rating Bulk** | `GET /rating-bulk` | Bulk ratings data |

### 16.2 Price Targets

| API | Endpoint | Description |
|-----|----------|-------------|
| **Price Target Summary** | `GET /price-target-summary?symbol={symbol}` | Price target overview |
| **Price Target Summary Bulk** | `GET /price-target-summary-bulk` | Bulk price targets |
| **Price Target Consensus** | `GET /price-target-consensus?symbol={symbol}` | Consensus target |

### 16.3 Upgrades & Downgrades

| API | Endpoint | Description |
|-----|----------|-------------|
| **Upgrades/Downgrades Consensus Bulk** | `GET /upgrades-downgrades-consensus-bulk` | Bulk consensus data |

### 16.4 Financial Estimates

| API | Endpoint | Description |
|-----|----------|-------------|
| **Financial Estimates** | `GET /financial-estimates?symbol={symbol}` | Analyst estimates |

---

## 17. ESG Data

Environmental, Social, and Governance data.

| API | Endpoint | Description |
|-----|----------|-------------|
| **ESG Ratings** | `GET /esg-ratings?symbol={symbol}` | ESG scores and ratings |
| **ESG Benchmark** | `GET /esg-benchmark` | ESG benchmarking data |
| **ESG Search** | `GET /esg-search` | Search ESG data |

---

## 18. DCF Valuation

Discounted Cash Flow valuation models.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Levered DCF** | `GET /dcf-levered?symbol={symbol}` | Levered DCF valuation |
| **Advanced DCF** | `GET /dcf-advanced?symbol={symbol}` | Advanced DCF model |
| **Custom Levered DCF** | `GET /custom-dcf-levered?symbol={symbol}` | Customizable levered DCF |
| **Custom Advanced DCF** | `GET /custom-dcf-advanced?symbol={symbol}` | Customizable advanced DCF |

---

## 19. M&A and Corporate Actions

Merger and acquisition data, corporate actions.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Latest M&A** | `GET /latest-mergers-acquisitions` | Recent M&A activity |
| **Search M&A** | `GET /search-mergers-acquisitions` | Search M&A deals |
| **Acquisition Ownership** | `GET /acquisition-ownership` | Acquisition ownership changes |

---

## 20. Senate & House Trading

Congressional trading disclosure data.

### 20.1 Senate Trading

| API | Endpoint | Description |
|-----|----------|-------------|
| **Senate Latest** | `GET /senate-latest` | Latest Senate disclosures |
| **Senate Trading** | `GET /senate-trading` | Senate trading data |
| **Senate Trading by Name** | `GET /senate-trading-by-name` | Trading by senator name |

### 20.2 House Trading

| API | Endpoint | Description |
|-----|----------|-------------|
| **House Latest** | `GET /house-latest` | Latest House disclosures |
| **House Trading** | `GET /house-trading` | House trading data |
| **House Trading by Name** | `GET /house-trading-by-name` | Trading by representative name |

### 20.3 Disclosures

| API | Endpoint | Description |
|-----|----------|-------------|
| **Latest Disclosures** | `GET /latest-disclosures` | Recent disclosures |
| **Disclosures Dates** | `GET /disclosures-dates` | Available disclosure dates |
| **Disclosures Name Search** | `GET /disclosures-name-search` | Search by name |

---

## 21. Commodities

Commodity prices and historical data.

### 21.1 Commodity Lists & Quotes

| API | Endpoint | Description |
|-----|----------|-------------|
| **Commodities List** | `GET /commodities-list` | Available commodities |
| **Commodities Quote** | `GET /commodities-quote?symbol={symbol}` | Commodity price quote |
| **Commodities Quote Short** | `GET /commodities-quote-short` | Lightweight quote |
| **All Commodities Quotes** | `GET /all-commodities-quotes` | All commodity quotes |
| **Full Commodities Quotes** | `GET /full-commodities-quotes` | Complete commodity data |

### 21.2 Historical Data

| API | Endpoint | Description |
|-----|----------|-------------|
| **Commodities EOD Full** | `GET /commodities-historical-price-eod/full` | Full historical data |
| **Commodities EOD Light** | `GET /commodities-historical-price-eod/light` | Lightweight history |
| **Commodities Intraday 1min** | `GET /commodities-intraday-1-min` | 1-minute data |
| **Commodities Intraday 5min** | `GET /commodities-intraday-5-min` | 5-minute data |
| **Commodities Intraday 1hour** | `GET /commodities-intraday-1-hour` | Hourly data |

---

## 22. Cryptocurrency

Cryptocurrency prices and market data.

### 22.1 Crypto Lists & Quotes

| API | Endpoint | Description |
|-----|----------|-------------|
| **Cryptocurrency List** | `GET /cryptocurrency-list` | Available cryptocurrencies |
| **Cryptocurrency Quote** | `GET /cryptocurrency-quote?symbol={symbol}` | Crypto price quote |
| **Cryptocurrency Quote Short** | `GET /cryptocurrency-quote-short` | Lightweight quote |
| **All Cryptocurrency Quotes** | `GET /all-cryptocurrency-quotes` | All crypto quotes |
| **Full Cryptocurrency Quotes** | `GET /full-cryptocurrency-quotes` | Complete crypto data |

### 22.2 Historical Data

| API | Endpoint | Description |
|-----|----------|-------------|
| **Crypto EOD Full** | `GET /cryptocurrency-historical-price-eod/full` | Full historical data |
| **Crypto EOD Light** | `GET /cryptocurrency-historical-price-eod/light` | Lightweight history |
| **Crypto Intraday 1min** | `GET /cryptocurrency-intraday-1-min` | 1-minute data |
| **Crypto Intraday 5min** | `GET /cryptocurrency-intraday-5-min` | 5-minute data |
| **Crypto Intraday 1hour** | `GET /cryptocurrency-intraday-1-hour` | Hourly data |

---

## 23. Forex

Foreign exchange rates and currency data.

### 23.1 Forex Lists & Quotes

| API | Endpoint | Description |
|-----|----------|-------------|
| **Forex List** | `GET /forex-list` | Available currency pairs |
| **Forex Quote** | `GET /forex-quote?symbol={symbol}` | Forex rate quote |
| **Forex Quote Short** | `GET /forex-quote-short` | Lightweight quote |
| **All Forex Quotes** | `GET /all-forex-quotes` | All forex quotes |
| **Full Forex Quotes** | `GET /full-forex-quotes` | Complete forex data |
| **Batch Forex** | `GET /batch-forex-quotes` | Batch forex quotes |

### 23.2 Historical Data

| API | Endpoint | Description |
|-----|----------|-------------|
| **Forex EOD Full** | `GET /forex-historical-price-eod/full` | Full historical data |
| **Forex EOD Light** | `GET /forex-historical-price-eod/light` | Lightweight history |
| **Forex Intraday 1min** | `GET /forex-intraday-1-min` | 1-minute data |
| **Forex Intraday 5min** | `GET /forex-intraday-5-min` | 5-minute data |
| **Forex Intraday 1hour** | `GET /forex-intraday-1-hour` | Hourly data |

---

## 24. Aftermarket Data

Pre-market and after-hours trading data.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Aftermarket Quote** | `GET /aftermarket-quote?symbol={symbol}` | After-hours quotes |
| **Aftermarket Trade** | `GET /aftermarket-trade?symbol={symbol}` | After-hours trades |
| **Batch Aftermarket Quote** | `GET /batch-aftermarket-quote` | Batch after-hours quotes |
| **Batch Aftermarket Trade** | `GET /batch-aftermarket-trade` | Batch after-hours trades |

---

## 25. Commitment of Traders

COT reports for futures markets.

| API | Endpoint | Description |
|-----|----------|-------------|
| **COT Report** | `GET /cot-report` | COT report data |
| **COT Report List** | `GET /cot-report-list` | Available COT reports |
| **COT Report Analysis** | `GET /cot-report-analysis` | COT analysis |

---

## 26. Search & Lookup

Company and symbol search functionality.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Search by Name** | `GET /search-by-name` | Search by company name |
| **Search Name** | `GET /search-name` | Name search |
| **Search by Symbol** | `GET /search-by-symbol` | Search by ticker |
| **Search Symbol** | `GET /search-symbol` | Symbol lookup |
| **Search CIK** | `GET /search-cik` | CIK lookup |
| **Search ISIN** | `GET /search-isin` | ISIN lookup |
| **Search CUSIP** | `GET /search-cusip` | CUSIP lookup |
| **Search Exchange Variants** | `GET /search-exchange-variants` | Exchange variants |
| **Search Reporting Name** | `GET /search-reporting-name` | Reporting name search |
| **Company Search by CIK** | `GET /company-search-by-cik` | Search by CIK |
| **Company Search by Symbol** | `GET /company-search-by-symbol` | Search by symbol |
| **Company Screener** | `GET /company-screener` | Advanced company screening |

---

## 27. Lists & Reference Data

Reference data and symbol lists.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Company Symbols List** | `GET /company-symbols-list` | All company symbols |
| **Financial Symbols List** | `GET /financial-symbols-list` | All financial symbols |
| **Symbol Changes List** | `GET /symbol-changes-list` | Symbol change history |
| **Exchange Market Hours** | `GET /exchange-market-hours` | Exchange hours |
| **All Exchange Market Hours** | `GET /all-exchange-market-hours` | All exchanges hours |
| **Holidays by Exchange** | `GET /holidays-by-exchange` | Exchange holidays |
| **Market Risk Premium** | `GET /market-risk-premium` | Risk premium data |

---

## 28. Treasury Rates

US Treasury yield data.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Treasury Rates** | `GET /treasury-rates` | US Treasury yields |

---

## 29. Executive Compensation

Executive pay and compensation data.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Executive Compensation** | `GET /executive-compensation?symbol={symbol}` | Executive pay data |
| **Compensation Benchmark** | `GET /executive-compensation-benchmark` | Benchmark data |

---

## 30. Crowdfunding & Offerings

Crowdfunding and equity offering data.

| API | Endpoint | Description |
|-----|----------|-------------|
| **Crowdfunding by CIK** | `GET /crowdfunding-by-cik` | Crowdfunding by CIK |
| **Crowdfunding Search** | `GET /crowdfunding-search` | Search crowdfunding |
| **Latest Crowdfunding** | `GET /latest-crowdfunding` | Recent offerings |
| **Equity Offering by CIK** | `GET /equity-offering-by-cik` | Offerings by CIK |
| **Equity Offering Search** | `GET /equity-offering-search` | Search offerings |
| **Latest Equity Offering** | `GET /latest-equity-offering` | Recent offerings |

---

## Common Parameters

### Date Parameters
- `from`: Start date (YYYY-MM-DD format)
- `to`: End date (YYYY-MM-DD format)

### Period Parameters
- `period`: `annual` or `quarter` (default varies by endpoint)

### Limit Parameters
- `limit`: Number of results to return

### Symbol Parameters
- `symbol`: Stock ticker symbol (e.g., AAPL, MSFT)
- `symbols`: Comma-separated list of symbols for batch requests

### Page Parameters
- `page`: Page number for pagination
- `limit`: Results per page

---

## Data Access Tiers & Pricing

### Subscription Plans Overview

Financial Modeling Prep API offers different access tiers based on subscription level:

| Plan | Monthly Bandwidth | API Calls/Min | Data Range | Features |
|------|------------------|---------------|------------|----------|
| **Free** | 500MB | Low frequency | Limited history | Basic endpoints only |
| **Starter** | 20GB | Standard | Extended | More endpoints, some real-time |
| **Premium** | 50GB | Higher | 30+ years | Most endpoints, real-time data |
| **Ultimate** | 150GB | High | 30+ years | All endpoints, priority data |
| **Enterprise** | 1TB+ | 3,000+ | 30+ years | All features + redistribution rights |

### Free Tier Endpoints (18 Available)

The following endpoints are available with a free API key:

#### Market Data (6)
| Endpoint | Path | Description |
|----------|------|-------------|
| Company Symbols List | `/company-symbols-list` | All available stock symbols |
| Stock Quote Light | `/quote-short` | Basic stock quotes (delayed) |
| Most Active Stocks | `/most-active` | Top volume stocks |
| Biggest Gainers | `/biggest-gainers` | Daily top gainers |
| Biggest Losers | `/biggest-losers` | Daily top losers |
| Sector Performance | `/sector-performance-snapshot` | Sector performance data |

#### Historical Data (1)
| Endpoint | Path | Description |
|----------|------|-------------|
| Historical Price Light | `/historical-price-eod/light` | Daily price (date, close, volume only) |

#### Financial Data (3)
| Endpoint | Path | Description |
|----------|------|-------------|
| Income Statement | `/income-statement` | Quarterly/annual income data |
| Financial Ratios | `/metrics-ratios` | Basic financial ratios |
| Company Key Stats | `/key-metrics` | Key company statistics |

#### Market Indices (3)
| Endpoint | Path | Description |
|----------|------|-------------|
| Dow Jones Quote | `/dow-jones` | Dow Jones index data |
| Index List | `/indexes-list` | Available market indices |
| Index Quote | `/index-quote` | Index quotes |

#### Alternative Data (5)
| Endpoint | Path | Description |
|----------|------|-------------|
| Cryptocurrency List | `/cryptocurrency-list` | Available crypto symbols |
| Crypto Quote | `/cryptocurrency-quote` | Crypto prices |
| Forex Pairs | `/forex-list` | Currency pairs |
| Forex Quote | `/forex-quote` | Exchange rates |
| Bitcoin Price | `/cryptocurrency-quote?symbol=BTCUSD` | Bitcoin spot price |

### Paid Tier Features

#### Starter Plan ($19-29/month)
- Real-time stock quotes
- Full historical price data (OHLCV)
- Complete financial statements (3 statements)
- Basic technical indicators
- SEC filing access
- 20GB monthly bandwidth

#### Premium Plan ($49-79/month)
- All Starter features
- Advanced technical indicators (RSI, MACD, etc.)
- ETF and mutual fund holdings
- Insider trading data
- Analyst ratings and price targets
- 50GB monthly bandwidth

#### Ultimate Plan ($199+/month)
- All Premium features
- ESG data and ratings
- Congressional trading data (Senate/House)
- COT reports
- Earnings transcripts
- Bulk/batch endpoints
- 150GB monthly bandwidth

#### Enterprise Plan (Custom pricing)
- All Ultimate features
- Commercial redistribution license
- 3,000+ calls/minute
- 1TB+ bandwidth
- Priority support
- Custom API solutions

### Access Limitations by Tier

| Feature | Free | Starter | Premium | Ultimate | Enterprise |
|---------|------|---------|---------|----------|------------|
| Real-time quotes | ❌ Delayed | ✅ | ✅ | ✅ | ✅ |
| After-hours data | ❌ | ✅ | ✅ | ✅ | ✅ |
| Full historical OHLCV | ❌ (Light only) | ✅ | ✅ | ✅ | ✅ |
| All 3 financial statements | ❌ (Income only) | ✅ | ✅ | ✅ | ✅ |
| Financial statement growth | ❌ | ✅ | ✅ | ✅ | ✅ |
| Technical indicators | ❌ | Basic | ✅ | ✅ | ✅ |
| SEC filings | ❌ | ✅ | ✅ | ✅ | ✅ |
| Insider trading | ❌ | ❌ | ✅ | ✅ | ✅ |
| ETF holdings | ❌ | ❌ | ✅ | ✅ | ✅ |
| Analyst estimates | ❌ | ❌ | ✅ | ✅ | ✅ |
| ESG data | ❌ | ❌ | ❌ | ✅ | ✅ |
| Congressional trades | ❌ | ❌ | ❌ | ✅ | ✅ |
| Bulk endpoints | ❌ | ❌ | ❌ | ✅ | ✅ |
| Redistribution rights | ❌ | ❌ | ❌ | ❌ | ✅ |

### Data Delay by Tier

| Data Type | Free | Paid Plans |
|-----------|------|------------|
| Stock quotes | 15-20 min delayed | Real-time |
| Financial statements | Quarterly updates | Quarterly updates |
| SEC filings | N/A | Real-time |
| News | Delayed | Near real-time |

---

## Rate Limits

API rate limits vary by subscription tier:

| Tier | Bandwidth/30 Days | Rate Limit |
|------|-------------------|------------|
| Free | 500MB | Low frequency (approx. 250 calls/day) |
| Starter | 20GB | Standard |
| Premium | 50GB | Higher |
| Ultimate | 150GB | High |
| Enterprise | 1TB+ | 3,000+ calls/minute |

**Note:** 
- Bandwidth is calculated on a trailing 30-day basis
- Exceeding bandwidth limits will result in 429 errors until the next period
- Check your FMP dashboard for specific usage statistics
- Free tier users may encounter stricter rate limiting during peak hours

---

## Error Handling

The API returns standard HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Check parameters |
| 401 | Unauthorized - Invalid API key |
| 403 | Forbidden - Subscription required |
| 404 | Not Found - Symbol or resource not found |
| 429 | Rate Limit Exceeded |
| 500 | Server Error |

**Error Response Format:**
```json
{
  "Error": "Invalid API key"
}
```

---

## Common Use Cases

### 1. Building a Stock Screener
```
1. Get all symbols: GET /company-symbols-list
2. Get key metrics: GET /key-metrics?symbol={symbol}
3. Filter by criteria (P/E ratio, market cap, etc.)
4. Get detailed quotes: GET /quote?symbol={symbol}
```

### 2. Portfolio Tracking
```
1. Get batch quotes: GET /batch-quote?symbols=AAPL,MSFT,GOOGL
2. Get historical prices: GET /historical-price-eod/full?symbol={symbol}
3. Get news: GET /news/stock-latest
4. Get financials: GET /income-statement?symbol={symbol}
```

### 3. Technical Analysis
```
1. Get intraday data: GET /historical-chart/1min?symbol={symbol}
2. Calculate indicators: GET /technical-indicators/rsi?symbol={symbol}
3. Get historical prices: GET /historical-price-eod/full?symbol={symbol}
```

### 4. Fundamental Analysis
```
1. Get profile: GET /profile?symbol={symbol}
2. Get financial statements: GET /income-statement?symbol={symbol}
3. Get key metrics: GET /key-metrics?symbol={symbol}
4. Get ratios: GET /metrics-ratios?symbol={symbol}
5. Get peers: GET /peers?symbol={symbol}
```

### 5. News-Based Trading
```
1. Get latest news: GET /news/stock-latest
2. Get company news: GET /stock-news?symbol={symbol}
3. Get quotes: GET /quote?symbol={symbol}
4. Get insider trades: GET /latest-insider-trade
```

---

## Data Frequency Notes

- **Real-time**: Stock quotes, forex, crypto (with appropriate subscription)
- **Delayed**: 15-20 minutes for free tier
- **End-of-Day**: Daily OHLCV data updated after market close
- **Historical**: Available from IPO date or earliest available data
- **Financial Statements**: Updated quarterly/annually after company filings

---

## Support & Resources

- **Website**: https://financialmodelingprep.com
- **Developer Docs**: https://site.financialmodelingprep.com/developer/docs
- **API Status**: Check FMP dashboard for service status

---

## API Coverage Summary

### Documented Endpoints

| Category | Count |
|----------|-------|
| **Total Endpoints Documented** | 258+ |
| **Free Tier Endpoints** | 18 |
| **Paid Tier Endpoints** | 240+ |

### Free Tier Availability by Category

| Data Category | Free Endpoints | Example Endpoints |
|---------------|----------------|-------------------|
| Stock Quotes | 6 | `/quote-short`, `/most-active`, `/biggest-gainers` |
| Historical Data | 1 | `/historical-price-eod/light` |
| Financial Statements | 3 | `/income-statement`, `/metrics-ratios`, `/key-metrics` |
| Market Indices | 3 | `/dow-jones`, `/indexes-list`, `/index-quote` |
| Crypto/Forex | 5 | `/cryptocurrency-list`, `/forex-quote`, BTC price |

### Pricing Reference

- **Free Plan**: 500MB/month, 18 endpoints, delayed data
- **Starter**: $19-29/month, 20GB/month, real-time basics
- **Premium**: $49-79/month, 50GB/month, full market data
- **Ultimate**: $199+/month, 150GB/month, advanced data
- **Enterprise**: Custom pricing, 1TB+/month, commercial use

---

## Changelog

This documentation covers the stable API endpoints as of March 2026. For the latest updates and new endpoints, refer to the official FMP documentation.

**Total Stable Endpoints Documented: 258+**

---

*Generated from Financial Modeling Prep API Documentation*
*Last Updated: March 2026*
