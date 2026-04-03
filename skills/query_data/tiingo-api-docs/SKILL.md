# Tiingo API Skill

## Overview

Tiingo API provides financial data including stock prices, cryptocurrencies, forex, fundamentals, and news. This skill helps you query Tiingo's data quickly using its RESTful API.

**Base URL**: `https://api.tiingo.com`
**Official Documentation**: https://www.tiingo.com/documentation/

## Authentication

All API requests require an API Token. You can get one by signing up at https://www.tiingo.com

**Two ways to authenticate:**

1. **Via URL parameter:**
   ```
   GET https://api.tiingo.com/endpoint?token=YOUR_API_TOKEN
   ```

2. **Via HTTP Header (Recommended):**
   ```
   Authorization: Token YOUR_API_TOKEN
   ```

## Response Formats

- **JSON** (default) - Includes metadata and debugging info
- **CSV** - 4-5x faster, bare-bones format

Add `format=csv` or `format=json` to your request parameters.

## Data Symbology

### Equities
- Use hyphens (`-`) instead of periods for share classes
  - Example: `BRK.A` → `BRK-A`
- Preferred shares format: `{SYMBOL}-P-{CLASS}`
  - Example: `SPG-P-J` for Simon Property Group's Preferred J
- Mutual Funds: typically end with "X" (e.g., `VFINX`)
- CEFs: begin and end with "X" (e.g., `XAIFX`)

### Cryptocurrency & FX
- Remove forward slashes
  - Example: `EUR/USD` → `EURUSD`
  - Example: `BTC/ETH` → `BTCETH`

---

## Data Availability & Pricing Tiers

Tiingo provides **free access to most data endpoints** with usage limits. All accounts start with the **Basic Plan (Free)** and can be upgraded for higher limits or commercial use.

### Pricing Plans Overview

| Plan | Cost | Use Case | Redistribution |
|------|------|----------|----------------|
| **Basic** | Free | Internal & Personal | Not Allowed |
| **Power** | Paid | Internal & Personal | Not Allowed |
| **Commercial** | Paid | Internal Commercial Use | Not Allowed |
| **Redistribution** | Contact Sales | Data Distribution | Allowed |

### Free vs Paid Endpoints

#### Free Endpoints (Basic Plan)
All endpoints below are available with the free Basic plan, subject to usage limits:

- ✅ End-of-Day (EOD) Prices - US Equities, ETFs, Mutual Funds
- ✅ Cryptocurrency Prices - 60+ exchanges, 8000+ pairs
- ✅ Forex Rates - 140+ currency pairs
- ✅ Search & Meta Data
- ✅ News Feed (with limit of 100 articles per request)
- ✅ Corporate Actions (Dividends, Splits)
- ✅ Mutual Fund & ETF Fees
- ✅ All WebSocket Streams (IEX, Crypto, Forex)

#### Limited/Paid Endpoints

**Fundamentals Data** - Limited free tier, full access requires Power/Commercial:
- Dow 30 tickers: 3 years of historical data (free)
- All other tickers: Requires paid plan
- Endpoints: `/tiingo/fundamentals/*`

**IEX Full TOPS Feed** - Requires IEX Market Data Agreement:
- Free tier provides derived reference prices
- Full TOPS data requires agreement with IEX (institutional)

**News Bulk Download** - Institutional only:
- `/tiingo/news/bulk_download`
- Available only for Commercial plan customers

---

## Endpoints

### 1. End-of-Day Prices (EOD)

**Daily OHLCV data for US equities, ETFs, and mutual funds.**

**Latest Price:**
```
GET /tiingo/daily/{ticker}/prices
```

**Historical Prices:**
```
GET /tiingo/daily/{ticker}/prices?startDate=2012-1-1&endDate=2016-1-1
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ticker | string | Y | Stock ticker (e.g., `AAPL`) |
| startDate | date | N | Format: YYYY-MM-DD |
| endDate | date | N | Format: YYYY-MM-DD |
| resampleFreq | string | N | `daily`, `weekly`, `monthly`, `annually` |
| format | string | N | `json` or `csv` |
| columns | string[] | N | Specific columns to return |
| sort | string | N | Sort column (prepend `-` for descending) |

**Response Fields:**
- `date`, `open`, `high`, `low`, `close`, `volume`
- `adjOpen`, `adjHigh`, `adjLow`, `adjClose`, `adjVolume`
- `divCash`, `splitFactor`

### 2. IEX Real-Time & Historical

**Real-time and intraday data from IEX Exchange.**

**Current Top-of-Book & Last Price:**
```
GET /iex                    # All tickers
GET /iex/{ticker}           # Specific ticker
GET /iex/?tickers=aapl,spy  # Multiple tickers
```

**Historical Intraday:**
```
GET /iex/{ticker}/prices?startDate=2019-01-02&resampleFreq=5min
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tickers | string | N | Single ticker or comma-separated list |
| format | string | N | `json` or `csv` |
| startDate | date | N | Format: YYYY-MM-DD |
| resampleFreq | string | N | Resampling frequency (e.g., `5min`) |

**Response Fields:**
- `ticker`, `timestamp`, `last`, `lastSize`, `tngoLast`
- `bidPrice`, `bidSize`, `askPrice`, `askSize`
- `open`, `high`, `low`, `prevClose`, `volume`, `mid`

### 3. Cryptocurrency

**Price data from 60+ crypto exchanges.**

**Meta Data:**
```
GET /tiingo/crypto
GET /tiingo/crypto?tickers={ticker}
```

**Real-time & Historical Prices:**
```
GET /tiingo/crypto/prices
GET /tiingo/crypto/prices?tickers={ticker}&startDate=2019-01-02&resampleFreq=5min
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tickers | string | Y | Crypto pair (e.g., `btcusd`) |
| exchanges | string[] | N | Limit to specific exchanges |
| startDate | date | N | Format: YYYY-MM-DD |
| endDate | date | N | Format: YYYY-MM-DD |
| resampleFreq | string | N | Default: `5min` (e.g., `1min`, `1hour`, `1day`) |

**Response Fields:**
- `ticker`, `baseCurrency`, `quoteCurrency`
- `priceData`: `date`, `open`, `high`, `low`, `close`, `volume`, `tradesDone`, `volumeNotional`

### 4. Forex

**Institutional-grade FX quotes from tier-1 banks.**

**Current Top-of-Book:**
```
GET /tiingo/fx/top?tickers=audusd,eurusd
GET /tiingo/fx/{ticker}/top
```

**Intraday Prices:**
```
GET /tiingo/fx/{ticker}/prices?resampleFreq=1day
GET /tiingo/fx/{ticker}/prices?startDate=2019-06-30&resampleFreq=5min
```

**Response Fields:**
- `ticker`, `quoteTimestamp`, `bidPrice`, `askPrice`, `bidSize`, `askSize`, `midPrice`

### 5. Fundamentals

**Financial statements and metrics for 5,500+ US equities and ADRs.**

**Definitions:**
```
GET /tiingo/fundamentals/definitions
```

**Statement Data:**
```
GET /tiingo/fundamentals/{ticker}/statements
GET /tiingo/fundamentals/{ticker}/statements?startDate=2019-06-30
```

**Daily Metrics:**
```
GET /tiingo/fundamentals/{ticker}/daily
```

**Meta Data:**
```
GET /tiingo/fundamentals/meta
GET /tiingo/fundamentals/meta?tickers=aapl,msft
```

**Parameters for Statements:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| asReported | boolean | N | `true` = as reported, `false` (default) = most recent including revisions |
| startDate | date | N | Format: YYYY-MM-DD |
| endDate | date | N | Format: YYYY-MM-DD |
| format | string | N | `json` or `csv` |

**Statement Types:**
- `balanceSheet` - Balance sheet data
- `incomeStatement` - Income statement data
- `cashFlow` - Cash flow statement data
- `overview` - Metrics and ratios

### 6. News

**Financial news with AI tagging (8,000-12,000 articles/day).**

**Latest News:**
```
GET /tiingo/news
GET /tiingo/news?tickers=aapl,googl
GET /tiingo/news?tags=election,argentina
```

**Bulk Download (Institutional only):**
```
GET /tiingo/news/bulk_download
GET /tiingo/news/bulk_download/{id}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tickers | string[] | N | Filter by tickers |
| source | string[] | N | Filter by news source domains |
| tags | string[] | N | Filter by tags |
| startDate | date | N | Format: YYYY-MM-DD |
| endDate | date | N | Format: YYYY-MM-DD |
| limit | int32 | N | Max 1000 (default: 100) |
| offset | int32 | N | Pagination offset |
| sortBy | string | N | `publishedDate` or `crawlDate` |

**Response Fields:**
- `id`, `title`, `url`, `description`, `publishedDate`, `crawlDate`
- `source`, `tickers`, `tags`

### 7. Search

**Search for assets by ticker or name.**
```
GET /tiingo/utilities/search/{query}
GET /tiingo/utilities/search?query=apple
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Y | Search query |
| exactTickerMatch | boolean | N | Only exact ticker matches |
| includeDelisted | boolean | N | Include delisted tickers |
| limit | int32 | N | Max 100 (default: 10) |

**Response Fields:**
- `ticker`, `name`, `assetType`, `isActive`, `permaTicker`, `openFIGI`

### 8. Corporate Actions

**Dividends:**
```
GET /tiingo/daily/{ticker}/dividends
```

**Splits:**
```
GET /tiingo/daily/{ticker}/splits
```

---

## WebSocket Real-Time Streaming

Connect to `wss://api.tiingo.com` for real-time data streams.

### IEX WebSocket
```python
from websocket import create_connection
import json

ws = create_connection("wss://api.tiingo.com/iex")

subscribe = {
    'eventName': 'subscribe',
    'authorization': 'YOUR_API_TOKEN',
    'eventData': {
        'thresholdLevel': 6,  # 6 = Reference price, 0-5 = Full TOPS feed
        'tickers': ['spy', 'uso']  # Use ['*'] for all tickers
    }
}

ws.send(json.dumps(subscribe))
while True:
    print(ws.recv())
```

### Crypto WebSocket
```python
ws = create_connection("wss://api.tiingo.com/crypto")

subscribe = {
    'eventName': 'subscribe',
    'authorization': 'YOUR_API_TOKEN',
    'eventData': {
        'thresholdLevel': 6,
        'tickers': ['btcusd']
    }
}
```

### Forex WebSocket
```python
ws = create_connection("wss://api.tiingo.com/fx")

subscribe = {
    'eventName': 'subscribe',
    'authorization': 'YOUR_API_TOKEN',
    'eventData': {
        'thresholdLevel': 6,
        'tickers': ['eurusd']
    }
}
```

**Message Types:**
- `A` - New data
- `U` - Update existing data
- `D` - Delete data
- `I` - Informational/meta data
- `E` - Error messages
- `H` - Heartbeats (sent every 30 seconds)

---

## Python Code Examples

### End-of-Day Prices
```python
import requests

headers = {'Content-Type': 'application/json'}
url = "https://api.tiingo.com/tiingo/daily/aapl/prices"
params = {
    'startDate': '2019-01-02',
    'token': 'YOUR_API_TOKEN'
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
```

### Real-Time IEX Quotes
```python
import requests

headers = {'Content-Type': 'application/json'}
url = "https://api.tiingo.com/iex/"
params = {
    'tickers': 'aapl,spy',
    'token': 'YOUR_API_TOKEN'
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
```

### Cryptocurrency Prices
```python
import requests

headers = {'Content-Type': 'application/json'}
url = "https://api.tiingo.com/tiingo/crypto/prices"
params = {
    'tickers': 'btcusd',
    'startDate': '2019-01-02',
    'resampleFreq': '5min',
    'token': 'YOUR_API_TOKEN'
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
```

### News Articles
```python
import requests

headers = {'Content-Type': 'application/json'}
url = "https://api.tiingo.com/tiingo/news"
params = {
    'tickers': 'aapl,googl',
    'limit': 100,
    'token': 'YOUR_API_TOKEN'
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
```

### Search Assets
```python
import requests

headers = {'Content-Type': 'application/json'}
url = "https://api.tiingo.com/tiingo/utilities/search"
params = {
    'query': 'apple',
    'limit': 10,
    'token': 'YOUR_API_TOKEN'
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
```

---

## Rate Limits

Rate limits depend on your plan (Basic, Power, or Commercial):

- **Hourly Requests** - Reset every hour
- **Daily Requests** - Reset every day at midnight EST
- **Monthly Bandwidth** - Reset the first of every month at midnight EST

There are no per-minute or per-second limits.

---

## Usage Restrictions

- **Basic/Power accounts**: Internal and personal use only
- **Commercial accounts**: Internal commercial usage only
- **Redistribution**: Contact sales@tiingo.com for redistribution licenses

---

## Quick Reference

| Data Type | Endpoint | Use Case |
|-----------|----------|----------|
| Daily Stock Prices | `/tiingo/daily/{ticker}/prices` | Historical OHLCV |
| Real-time Quotes | `/iex/{ticker}` | Live bid/ask/last |
| Intraday Bars | `/iex/{ticker}/prices` | Minute-by-minute data |
| Crypto Prices | `/tiingo/crypto/prices` | 8000+ crypto pairs |
| Forex Rates | `/tiingo/fx/{ticker}/top` | 140+ FX pairs |
| Fundamentals | `/tiingo/fundamentals/{ticker}/statements` | Financial statements |
| News | `/tiingo/news` | Financial news feed |
| Search | `/tiingo/utilities/search` | Find tickers |

### Free vs Paid Endpoints Summary

| Endpoint | Free Tier | Paid Tier Required | Notes |
|----------|-----------|-------------------|-------|
| EOD Prices | ✅ | No | Basic plan includes all tickers |
| IEX Real-time | ✅ (derived) | Full TOPS feed | IEX agreement required for full data |
| Crypto Prices | ✅ | No | 60+ exchanges available |
| Forex Rates | ✅ | No | 140+ currency pairs |
| Fundamentals | ⚠️ Limited | Full access | Dow 30 only for free tier (3 years) |
| News | ✅ | Bulk download only | 100 articles/request limit |
| Search | ✅ | No | Full search capability |
| Corporate Actions | ✅ | No | Included with EOD |
| WebSockets | ✅ | No | All streams available on free tier |
