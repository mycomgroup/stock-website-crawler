# Stocks Overview

## 源URL

https://massive.com/docs/rest/stocks

## 描述

At Massive, we provide a comprehensive suite of U.S. stock market data through a standardized and intuitive API, offering unparalleled coverage of the U.S. stock market landscape. Our offerings encompass real-time prices, historical data, company information, and news from all 19 major stock exchanges, additional dark pools, FINRA trading facilities, and OTC markets. Accessible via REST APIs, WebSocket streams, and flat files, this rich dataset supports the development of sophisticated applications tailored for both retail and professional trading environments. Leveraging detailed trade data and reference information, our platform delivers a robust analytical toolset crucial for comprehensive market analysis and decision-making.

## 内容

Market Hours and Timezone

Data is available for all U.S. market sessions, which are segmented into pre-market, regular market, and after-hours:

Pre-Market Trading Hours: From 4:00 AM to 9:30 AM Eastern Time (ET).
Regular Market Hours: From 9:30 AM to 4:00 PM ET.
After-Hours Trading: From 4:00 PM to 8:00 PM ET.

All timestamps in the datasets are provided as Unix timestamps (seconds since epoch, UTC). When converting these timestamps into human-readable form (e.g., market open at 9:30 AM), remember they represent UTC time, not Eastern Time (ET). To correctly align data with market hours or dates, you'll need to explicitly convert timestamps from UTC to ET during your analysis.

Infrastructure and Reliability

Our platform's robustness begins with our primary data facility at the Equinix Data Center in New Jersey, strategically co-located with the exchanges. This setup allows us to receive data through direct physical connections, significantly reducing latency and enhancing the reliability of the data. Initially established in New Jersey, our infrastructure has expanded to include full redundancy at the ORD11 data center in Chicago. This expansion ensures uninterrupted service and data availability, even under adverse conditions, across multiple geographic locations.

Our data is sourced directly from proprietary exchange feeds and government-regulated consolidators known as Securities Information Processors (SIPs). By combining direct exchange access with regulated data consolidation, we ensure the provision of the most accurate and timely market data available. This infrastructure supports a wide range of financial data services and applications, offering our clients resilience, speed, and compliance with the highest industry standards.

Data Flow: From Exchanges to You

Our stock market data journey begins at the numerous trading venues across the U.S., encompassing all 19 major stock exchanges and additional dark pools. We maintain direct relationships with each exchange and comply with all licensing requirements, ensuring our data includes every trade, quote, and market event as it occurs.

Our data facility, co-located with the exchanges in the Equinix Data Center in New Jersey, receives this data through direct physical connections. This setup not only guarantees the fastest possible data transmission due to our proximity to the source but also enhances the reliability and integrity of the data we deliver.

This extensive coverage includes major platforms such as:

New York Stock Exchange (NYSE, NYSE American, NYSE Arca, NYSE Chicago, NYSE National)
Nasdaq (OMX, BX, PSX, Philadelphia)
Cboe Global Markets (BZX, BYX, EDGX, EDGA)
MIAX Exchange Group (Pearl, Emerald, Equities)
Members Exchange (MEMX)
Investors Exchange (IEX)
Long-Term Stock Exchange (LTSE)

Additionally, our dataset is enriched with trade data from:

FINRA Trading Facilities: including FINRA NYSE TRF, FINRA Nasdaq TRF Carteret, and FINRA Nasdaq TRF Chicago, which provide comprehensive trade reporting but not quotes.
OTC Reporting Facility: captures trades from over-the-counter markets but not quotes.

While our core data includes every trade and quote from the major stock exchanges, it's important to note that for the FINRA and OTC platforms, we exclusively capture trade information. This distinction is crucial for users relying on our data for accurate market analysis and decision-making.

From these diverse sources, the raw data is channeled to Securities Information Processors (SIPs). Our broad coverage across these platforms allows us to offer a complete view of the U.S. stock market landscape, making our data essential for those requiring comprehensive market insights. By integrating and processing this data, we ensure that all market participants have access to the full spectrum of market activities, empowering them with the data needed to make informed decisions.

What are Securities Information Processors (SIPs)?

Securities Information Processors (SIPs) are integral to the U.S. market data system, consolidating trade and quote data from all exchanges into a single feed, which includes the official National Best Bid and Offer (NBBO) and last sale data. We receive this consolidated data directly from S

... (内容已截断)
