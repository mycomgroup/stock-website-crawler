# Alpha Vantage API Skill

## 概述

Alpha Vantage 是一个提供金融数据的免费/付费 API，覆盖股票、外汇、加密货币、技术指标、经济指标和基本面数据。

**API 基础 URL:** `https://www.alphavantage.co/query`

**注册地址:** https://www.alphavantage.co/support/#api-key

**官方文档:** https://www.alphavantage.co/documentation/

---

## API 认证与限制

所有请求都需要 `apikey` 参数：
- **免费版**：5次调用/分钟，500次/天
- **付费版**：更高频率限制，无每日限额

**速率限制说明**：
- 免费用户：每分钟最多5次请求，每天最多500次
- 超出限制会返回错误提示或需要等待

---

## 免费 vs 付费接口分布

在总计 **114个** API 端点中：

- **免费接口**：约 **105个** (92%)
- **付费(Premium)接口**：**9个** (8%)

### 付费接口列表 (Premium)

以下接口需要付费订阅才能访问：

| 接口名称 | 类别 | 说明 |
|---------|------|------|
| `TIME_SERIES_INTRADAY` | 核心时间序列 | 日内高频数据 (1/5/15/30/60分钟) |
| `TIME_SERIES_DAILY_ADJUSTED` | 核心时间序列 | 调整后日线数据（含分红拆股） |
| `REALTIME_BULK_QUOTES` | 实时报价 | 批量实时报价（最多100个代码） |
| `REALTIME_OPTIONS` | 期权数据 | 实时期权链数据 |
| `HISTORICAL_OPTIONS` | 期权数据 | 历史期权数据 |
| `FX_INTRADAY` | 外汇数据 | 外汇日内高频数据 |
| `CRYPTO_INTRADAY` | 加密货币 | 数字货币日内高频数据 |
| `VWAP` | 技术指标 | 成交量加权平均价 |
| `MACD` | 技术指标 | MACD指标（虽然免费版可用，但文档标注为Premium） |

### 免费接口类别

**核心时间序列** (4个免费)：
- `TIME_SERIES_DAILY` - 原始日线数据
- `TIME_SERIES_WEEKLY` - 周线数据
- `TIME_SERIES_MONTHLY` - 月线数据
- `TIME_SERIES_WEEKLY_ADJUSTED` / `TIME_SERIES_MONTHLY_ADJUSTED` - 调整后周线/月线

**基本面数据** (4个全部免费)：
- `INCOME_STATEMENT` - 利润表
- `BALANCE_SHEET` - 资产负债表
- `CASH_FLOW` - 现金流量表
- `SHARES_OUTSTANDING` - 流通股数

**外汇数据** (3个免费)：
- `CURRENCY_EXCHANGE_RATE` - 实时汇率
- `FX_DAILY` - 外汇日线
- `FX_WEEKLY` / `FX_MONTHLY` - 外汇周线/月线

**加密货币** (3个免费)：
- `DIGITAL_CURRENCY_DAILY` - 数字货币日线
- `DIGITAL_CURRENCY_WEEKLY` - 数字货币周线
- `DIGITAL_CURRENCY_MONTHLY` - 数字货币月线

**经济指标** (9个全部免费)：
- `REAL_GDP` / `REAL_GDP_PER_CAPITA` - GDP数据
- `CPI` / `INFLATION` - 通胀指标
- `UNEMPLOYMENT` - 失业率
- `FEDERAL_FUNDS_RATE` / `TREASURY_YIELD` - 利率数据
- `RETAIL_SALES` / `DURABLES` / `NONFARM_PAYROLL` - 经济活动指标

**技术指标** (约50+个免费)：
- 移动平均线：SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA
- 振荡器：RSI, CCI, STOCH, WILLR, ULTOSC
- 趋势指标：ADX, AROON, BBANDS, OBV
- 波动率指标：ATR, NATR
- 等等...

**其他实用工具** (全部免费)：
- `GLOBAL_QUOTE` - 实时报价
- `SYMBOL_SEARCH` - 代码搜索
- `MARKET_STATUS` - 市场状态
- `IPO_CALENDAR` - IPO日历
- 新闻情绪、财报日历、公司概览等

---

## 数据提供情况

### 市场覆盖
- **美股**：完整覆盖，包括NYSE、NASDAQ、AMEX等
- **全球市场**：支持伦敦、多伦多、德国、印度、中国上海/深圳等交易所
- **股票代码格式**：
  - 美股：`AAPL`, `IBM`
  - 伦敦：`TSCO.LON`
  - 多伦多：`SHOP.TRT`
  - 中国上海：`600104.SHH`
  - 中国深圳：`000002.SHZ`
  - 印度：`RELIANCE.BSE`

### 数据时效性
- **免费版**：美股数据通常有15分钟延迟
- **付费版**：可获取实时数据（通过`entitlement=realtime`参数）

### 历史数据范围
- 时间序列数据：20+年历史数据（付费版可获取`full`输出）
- 免费版默认`compact`输出：最近100条数据

### 数据格式
- JSON（默认）
- CSV（通过`datatype=csv`参数）

---

## 核心 API 分类

### 1. 时间序列股票数据 (Core Time Series)

用于获取股票的历史价格数据（OHLCV）。

**常用函数：**

| 函数名 | 描述 | 主要参数 |
|--------|------|----------|
| `TIME_SERIES_INTRADAY` | 日内数据（1min/5min/15min/30min/60min） | `symbol`, `interval` |
| `TIME_SERIES_DAILY` | 日线数据（原始价格） | `symbol`, `outputsize` |
| `TIME_SERIES_DAILY_ADJUSTED` | 调整后日线（含分红拆股） | `symbol`, `outputsize` |
| `TIME_SERIES_WEEKLY` | 周线数据 | `symbol` |
| `TIME_SERIES_MONTHLY` | 月线数据 | `symbol` |

**示例请求：**
```
GET https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=YOUR_API_KEY
```

**响应结构：**
```json
{
  "Meta Data": {
    "1. Information": "Daily Prices",
    "2. Symbol": "IBM",
    "3. Last Refreshed": "2024-01-15",
    "4. Output Size": "Compact",
    "5. Time Zone": "US/Eastern"
  },
  "Time Series (Daily)": {
    "2024-01-15": {
      "1. open": "150.00",
      "2. high": "152.50",
      "3. low": "149.80",
      "4. close": "151.20",
      "5. volume": "5000000"
    }
  }
}
```

**重要参数说明：**
- `outputsize`: `compact` (最近100条) 或 `full` (20+年历史)
- `datatype`: `json` 或 `csv`
- `symbol`: 支持全球交易所 (如 `TSCO.LON`, `600104.SHH`, `RELIANCE.BSE`)

---

### 2. 基本面数据 (Fundamental Data)

获取公司财务报表。

| 函数名 | 描述 |
|--------|------|
| `INCOME_STATEMENT` | 利润表 |
| `BALANCE_SHEET` | 资产负债表 |
| `CASH_FLOW` | 现金流量表 |
| `SHARES_OUTSTANDING` | 流通股数 |

**示例请求：**
```
GET https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=YOUR_API_KEY
```

---

### 3. 技术指标 (Technical Indicators)

提供 50+ 种技术分析指标。

**常用指标：**

| 函数名 | 描述 | 必需参数 |
|--------|------|----------|
| `SMA` | 简单移动平均线 | `symbol`, `interval`, `time_period`, `series_type` |
| `EMA` | 指数移动平均线 | `symbol`, `interval`, `time_period`, `series_type` |
| `MACD` | MACD 指标 | `symbol`, `interval`, `series_type` |
| `RSI` | 相对强弱指数 | `symbol`, `interval`, `time_period`, `series_type` |
| `BBANDS` | 布林带 | `symbol`, `interval`, `time_period`, `series_type` |
| `ATR` | 真实波动幅度均值 | `symbol`, `interval`, `time_period` |
| `OBV` | 能量潮指标 | `symbol`, `interval` |
| `STOCH` | 随机指标 | `symbol`, `interval` |

**指标参数说明：**
- `interval`: `1min`, `5min`, `15min`, `30min`, `60min`, `daily`, `weekly`, `monthly`
- `series_type`: `close`, `open`, `high`, `low`
- `time_period`: 计算周期（正整数）

**示例请求：**
```
GET https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=close&apikey=YOUR_API_KEY
```

---

### 4. 外汇数据 (Foreign Exchange)

| 函数名 | 描述 |
|--------|------|
| `CURRENCY_EXCHANGE_RATE` | 实时汇率 |
| `FX_DAILY` | 日线汇率 |
| `FX_WEEKLY` | 周线汇率 |
| `FX_MONTHLY` | 月线汇率 |

**示例请求：**
```
GET https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=YOUR_API_KEY
```

---

### 5. 加密货币数据 (Digital Currency)

| 函数名 | 描述 |
|--------|------|
| `DIGITAL_CURRENCY_DAILY` | 数字货币日线 |
| `DIGITAL_CURRENCY_WEEKLY` | 数字货币周线 |
| `DIGITAL_CURRENCY_MONTHLY` | 数字货币月线 |

**示例请求：**
```
GET https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=YOUR_API_KEY
```

---

### 6. 经济指标 (Economic Indicators)

| 函数名 | 描述 |
|--------|------|
| `REAL_GDP` | 实际 GDP |
| `REAL_GDP_PER_CAPITA` | 人均 GDP |
| `CPI` | 消费者物价指数 |
| `INFLATION` | 通货膨胀率 |
| `UNEMPLOYMENT` | 失业率 |
| `FEDERAL_FUNDS_RATE` | 联邦基金利率 |
| `TREASURY_YIELD` | 国债收益率 |

**示例请求：**
```
GET https://www.alphavantage.co/query?function=REAL_GDP&apikey=YOUR_API_KEY
```

---

### 7. 工具类 API (Utility)

| 函数名 | 描述 |
|--------|------|
| `GLOBAL_QUOTE` | 实时报价（单个股票） |
| `SYMBOL_SEARCH` | 股票代码搜索 |
| `MARKET_STATUS` | 市场状态 |

---

## 快速参考代码示例

### Python

```python
import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://www.alphavantage.co/query"

# 获取日线数据
def get_daily_stock(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# 获取技术指标
def get_technical_indicator(symbol, indicator="RSI", interval="daily", period=14):
    params = {
        "function": indicator,
        "symbol": symbol,
        "interval": interval,
        "time_period": period,
        "series_type": "close",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# 获取汇率
def get_exchange_rate(from_currency, to_currency):
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_currency,
        "to_currency": to_currency,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# 获取基本面数据
def get_fundamental(symbol, report_type="INCOME_STATEMENT"):
    params = {
        "function": report_type,
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_KEY = "YOUR_API_KEY";
const BASE_URL = "https://www.alphavantage.co/query";

// 获取股票数据
async function getStockData(symbol) {
  const params = {
    function: "TIME_SERIES_DAILY",
    symbol: symbol,
    apikey: API_KEY
  };
  const response = await axios.get(BASE_URL, { params });
  return response.data;
}

// 获取技术指标
async function getTechnicalIndicator(symbol, indicator = "RSI") {
  const params = {
    function: indicator,
    symbol: symbol,
    interval: "daily",
    time_period: 14,
    series_type: "close",
    apikey: API_KEY
  };
  const response = await axios.get(BASE_URL, { params });
  return response.data;
}
```

### cURL

```bash
# 获取股票日线数据
curl "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=YOUR_API_KEY"

# 获取 MACD 指标
curl "https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=close&apikey=YOUR_API_KEY"

# 获取汇率
curl "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=EUR&apikey=YOUR_API_KEY"

# 获取 CSV 格式
curl "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=YOUR_API_KEY&datatype=csv"
```

---

## 数据解析指南

### 时间序列数据

```python
def parse_time_series(data, time_series_key):
    """解析时间序列数据为结构化格式"""
    meta_data = data.get("Meta Data", {})
    time_series = data.get(time_series_key, {})
    
    parsed_data = []
    for date, values in time_series.items():
        parsed_data.append({
            "date": date,
            "open": float(values.get("1. open", 0)),
            "high": float(values.get("2. high", 0)),
            "low": float(values.get("3. low", 0)),
            "close": float(values.get("4. close", 0)),
            "volume": int(values.get("5. volume", 0))
        })
    
    return sorted(parsed_data, key=lambda x: x["date"])

# 使用示例
data = get_daily_stock("IBM")
df = parse_time_series(data, "Time Series (Daily)")
```

### 技术指标数据

```python
def parse_technical_indicator(data, indicator_key):
    """解析技术指标数据"""
    meta_data = data.get("Meta Data", {})
    indicator_data = data.get(indicator_key, {})
    
    parsed = []
    for date, values in indicator_data.items():
        entry = {"date": date}
        entry.update({k: float(v) for k, v in values.items()})
        parsed.append(entry)
    
    return sorted(parsed, key=lambda x: x["date"])

# 使用示例
macd_data = get_technical_indicator("IBM", "MACD")
parsed_macd = parse_technical_indicator(macd_data, "Technical Analysis: MACD")
```

---

## 常见使用场景

### 场景1：获取股票历史价格并计算涨跌幅

```python
def get_price_change(symbol, days=30):
    data = get_daily_stock(symbol)
    time_series = data.get("Time Series (Daily)", {})
    
    dates = sorted(time_series.keys(), reverse=True)[:days]
    if len(dates) < 2:
        return None
    
    latest_close = float(time_series[dates[0]]["4. close"])
    past_close = float(time_series[dates[-1]]["4. close"])
    
    change_pct = ((latest_close - past_close) / past_close) * 100
    return {
        "symbol": symbol,
        "change_percent": round(change_pct, 2),
        "latest_price": latest_close,
        "past_price": past_close
    }
```

### 场景2：多股票实时报价

```python
def get_multiple_quotes(symbols):
    quotes = []
    for symbol in symbols:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        quote = data.get("Global Quote", {})
        if quote:
            quotes.append({
                "symbol": quote.get("01. symbol"),
                "price": float(quote.get("05. price", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": quote.get("10. change percent", "")
            })
    return quotes
```

### 场景3：计算移动平均线交叉

```python
def calculate_ma_crossover(symbol, short_period=20, long_period=50):
    # 获取价格数据
    data = get_daily_stock(symbol)
    prices = parse_time_series(data, "Time Series (Daily)")
    closes = [p["close"] for p in prices]
    
    if len(closes) < long_period:
        return None
    
    short_ma = sum(closes[:short_period]) / short_period
    long_ma = sum(closes[:long_period]) / long_period
    
    return {
        "symbol": symbol,
        "short_ma": round(short_ma, 2),
        "long_ma": round(long_ma, 2),
        "signal": "Bullish" if short_ma > long_ma else "Bearish"
    }
```

---

## 注意事项

1. **速率限制**：免费版 25 次/分钟，超出会返回错误
2. **数据延迟**：免费版可能有 15 分钟延迟
3. **股票代码格式**：
   - 美股：`AAPL`, `IBM`
   - 伦敦：`TSCO.LON`
   - 多伦多：`SHOP.TRT`
   - 中国上海：`600104.SHH`
   - 中国深圳：`000002.SHZ`
   - 印度：`RELIANCE.BSE`

4. **错误处理**：
```python
def safe_api_call(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        if "Error Message" in result:
            print(f"API Error: {result['Error Message']}")
            return None
        if "Note" in result and "API call frequency" in result["Note"]:
            print("Rate limit exceeded. Please wait.")
            return None
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None
```

5. **数据完整性**：检查返回数据是否为空或包含 "Information" 字段（表示需要升级订阅）

---

## 完整 API 列表

### 时间序列
- `TIME_SERIES_INTRADAY` - 日内数据
- `TIME_SERIES_DAILY` - 日线
- `TIME_SERIES_DAILY_ADJUSTED` - 调整后日线
- `TIME_SERIES_WEEKLY` - 周线
- `TIME_SERIES_WEEKLY_ADJUSTED` - 调整后周线
- `TIME_SERIES_MONTHLY` - 月线
- `TIME_SERIES_MONTHLY_ADJUSTED` - 调整后月线

### 技术指标 (部分)
- `SMA`, `EMA`, `WMA`, `DEMA`, `TEMA`, `TRIMA`, `KAMA`, `MAMA`
- `MACD`, `MACDEXT`
- `RSI`, `CCI`, `ADX`, `ADXR`, `AROON`, `AROONOSC`
- `BBANDS` (布林带)
- `STOCH`, `STOCHF`, `STOCHRSI`
- `ATR`, `NATR`
- `OBV`, `AD`, `ADOSC`
- `MOM`, `ROC`, `ROCR`
- `WILLR`, `ULTOSC`
- `MFI`, `PPO`, `APO`, `CMO`, `DX`, `BOP`
- `HT_TRENDLINE`, `HT_SINE`, `HT_TRENDMODE`, `HT_DCPHASE`, `HT_PHASOR`

### 基本面
- `INCOME_STATEMENT`
- `BALANCE_SHEET`
- `CASH_FLOW`
- `SHARES_OUTSTANDING`

### 外汇
- `CURRENCY_EXCHANGE_RATE`
- `FX_DAILY`, `FX_WEEKLY`, `FX_MONTHLY`

### 加密货币
- `DIGITAL_CURRENCY_DAILY`, `DIGITAL_CURRENCY_WEEKLY`, `DIGITAL_CURRENCY_MONTHLY`

### 经济指标
- `REAL_GDP`, `REAL_GDP_PER_CAPITA`
- `CPI`, `INFLATION`
- `UNEMPLOYMENT`
- `FEDERAL_FUNDS_RATE`, `TREASURY_YIELD`
- `RETAIL_SALES`, `DURABLES`, `NONFARM_PAYROLL`

### 其他
- `GLOBAL_QUOTE` - 实时报价
- `SYMBOL_SEARCH` - 代码搜索
- `MARKET_STATUS` - 市场状态
- `IPO_CALENDAR` - IPO 日历

---

**文档生成时间：** 2024年
**数据源：** Alpha Vantage API
**文档路径：** /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/query_data/alphavantage-api-docs/

---

## 使用建议

### 免费用户最佳实践
1. **合理分配API配额**：每天500次调用，优先获取核心数据
2. **使用日线而非日内数据**：免费版`TIME_SERIES_DAILY`已能满足大部分需求
3. **批量处理**：利用`outputsize=full`（付费版）或缓存数据减少调用
4. **避免实时查询**：使用缓存策略，在需要时才调用API

### 何时需要付费升级
- 需要**高频日内数据**（1/5/15分钟级别）进行日内交易
- 需要**调整后价格数据**（含分红拆股）进行长期回测
- 需要**批量实时报价**监控大量股票
- 需要**期权链数据**进行期权策略分析
- 需要**实时数据**而非15分钟延迟数据
- 日调用量超过500次

### 数据质量说明
- **可靠性**：Alpha Vantage是业界广泛使用的数据源，数据质量较高
- **延迟**：免费版15分钟延迟，适合非高频交易场景
- **覆盖度**：美股数据完整，国际股票代码支持良好
- **历史数据**：20+年历史数据，适合回测和长期分析
