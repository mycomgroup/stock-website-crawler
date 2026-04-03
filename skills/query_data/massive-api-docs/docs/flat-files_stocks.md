# Stocks Overview

## 源URL

https://massive.com/docs/flat-files/stocks

## 描述

Massive offers comprehensive historical U.S. stock market data through convenient, compressed CSV Flat Files. These datasets include daily and historical trade, quote, and aggregated market data sourced directly from all major U.S. exchanges, FINRA trading facilities, and dark pools. By leveraging our Flat Files, you can efficiently download large historical datasets for robust market analysis, research, backtesting strategies, and more, without the need for extensive API requests.

## 内容

All stock Flat Files contain unadjusted data. Prices and volumes are not adjusted for stock splits, dividends, or other corporate actions. If you require adjusted data for backtesting or analysis, you can retrieve it via the REST API by setting the adjusted flag to true, or apply adjustments manually using data from the Splits endpoint.

Data Availability and Frequency

Stocks Flat Files are generated daily after the close of the full market session, capturing all trading activity from:

Pre-Market Trading: 4:00 AM to 9:30 AM Eastern Time (ET)
Regular Market Hours: 9:30 AM to 4:00 PM ET
After-Hours Trading: 4:00 PM to 8:00 PM ET

The finalized daily datasets become available for download by approximately 11:00 AM ET the following day. All timestamps in the datasets are provided as Unix timestamps (seconds since epoch, UTC). When converting these timestamps into human-readable form (e.g., market open at 9:30 AM), remember they represent UTC time, not Eastern Time (ET). To correctly align data with market hours or dates, you'll need to explicitly convert timestamps from UTC to ET during your analysis.

Reliable and Comprehensive Historical Data

Our Flat Files include comprehensive market coverage, ensuring you receive an accurate historical record from the entire U.S. stock market ecosystem. Data sources include:

All 19 major U.S. stock exchanges, including NYSE, Nasdaq, Cboe, MIAX, MEMX, IEX, LTSE, and others.
FINRA trading facilities such as NYSE TRF, Nasdaq TRF Carteret, and Nasdaq TRF Chicago, which capture off-exchange trade reporting.
Dark pools for comprehensive trade visibility.

Massive consolidates and processes data sourced directly from regulated Securities Information Processors (SIPs), ensuring the highest standards of data integrity and compliance with U.S. market regulations. SIPs aggregate and standardize data across multiple exchanges, providing official trade records and the National Best Bid and Offer (NBBO).

How Flat Files Streamline Your Workflow

Utilizing Flat Files simplifies accessing and handling extensive historical datasets. Instead of managing numerous individual API requests, you can download structured historical datasets quickly and conveniently. This simplifies data management, accelerates your analysis, and reduces integration complexity, particularly beneficial for:

Historical market analysis and financial research
Strategy backtesting and quantitative modeling
Data-driven application development
Compliance and audit reporting
Data Structure and Formats

Stocks Flat Files are provided in CSV format with headers across all files, ensuring straightforward integration. The datasets cover key market metrics including:

Trades: Individual trade executions with price, volume, and timestamps
Quotes: Bid and ask prices, sizes, and exchange
Aggregates: Minute and daily Aggregates, with open, high, low, close, and volume data

These structured datasets enable rapid ingestion and analysis, supporting both manual exploration and automated workflows.

Regulatory Compliance

Massive ensures compliance with U.S. stock market data regulations. Historical Flat Files are available to both individual retail users and institutional clients under licensing terms tailored to specific needs. We closely adhere to exchange licensing and regulatory requirements, providing users clarity and confidence in utilizing our data.

Next Steps

Explore our Stocks Flat Files through the integrated File Browser or configure your preferred S3-compatible client for automated downloads. Our comprehensive documentation provides detailed guidance to help you integrate extensive historical market data seamlessly into your analysis and workflows.
