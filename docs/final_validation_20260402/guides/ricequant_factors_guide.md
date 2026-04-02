# RiceQuant 平台因子使用指南

## 📊 核心问题：因子能不能用平台的，不用自己算？

### ✅ 答案：可以！RiceQuant 平台提供了大量现成的因子

---

## 一、平台直接提供的因子（无需计算）

### 1. **财务因子**（fundamentals）

使用 `get_fundamentals()` 直接查询：

| 因子类别 | API 路径 | 说明 | 使用频率 |
|---------|---------|------|---------|
| **市值因子** | `fundamentals.eod_market_cap` | 流通市值 | ⭐⭐⭐⭐⭐ |
| **总市值** | `fundamentals.eod_derivative_indicator.market_cap` | 总市值 | ⭐⭐⭐⭐ |
| **PE市盈率** | `fundamentals.eod_derivative_indicator.pe_ratio` | 市盈率 | ⭐⭐⭐⭐⭐ |
| **PB市净率** | `fundamentals.eod_derivative_indicator.pb_ratio` | 市净率 | ⭐⭐⭐⭐⭐ |
| **换手率** | `fundamentals.eod_derivative_indicator.turnover_rate` | 换手率 | ⭐⭐⭐⭐ |
| **ROE** | `fundamentals.financial_indicator.roe` | 净资产收益率 | ⭐⭐⭐⭐⭐ |
| **ROA** | `fundamentals.financial_indicator.roa` | 总资产收益率 | ⭐⭐⭐⭐ |
| **营收增长** | `fundamentals.financial_indicator.inc_revenue_year` | 营收增长率 | ⭐⭐⭐⭐ |
| **净利润增长** | `fundamentals.financial_indicator.inc_net_profit_year` | 净利润增长率 | ⭐⭐⭐⭐ |
| **毛利率** | `fundamentals.financial_indicator.gross_profit_margin` | 毛利率 | ⭐⭐⭐⭐ |
| **净利率** | `fundamentals.financial_indicator.net_profit_margin` | 净利率 | ⭐⭐⭐⭐ |
| **资产负债率** | `fundamentals.financial_indicator.debt_to_asset_ratio` | 资产负债率 | ⭐⭐⭐⭐ |

**使用示例**:
```python
# 获取市值因子
cap_data = get_fundamentals(
    query(fundamentals.eod_market_cap).filter(fundamentals.stockcode == "000001.XSHE"),
    "2024-12-31"
)
market_cap = cap_data["eod_market_cap"].iloc[0] / 100000000  # 转换为亿元

# 获取PE因子
pe_data = get_fundamentals(
    query(fundamentals.eod_derivative_indicator.pe_ratio).filter(fundamentals.stockcode == "000001.XSHE"),
    "2024-12-31"
)
pe_ratio = pe_data["pe_ratio"].iloc[0]
```

---

### 2. **价格因子**（history_bars / get_price）

使用 `history_bars()` 或 `get_price()` 直接获取：

| 字段名 | 说明 | 是否重要 |
|-------|------|---------|
| `open` | 开盘价 | ⭐⭐⭐⭐⭐ |
| `close` | 收盘价 | ⭐⭐⭐⭐⭐ |
| `high` | 最高价 | ⭐⭐⭐⭐ |
| `low` | 最低价 | ⭐⭐⭐⭐ |
| `volume` | 成交量 | ⭐⭐⭐⭐⭐ |
| `total_turnover` | 成交额 | ⭐⭐⭐⭐ |
| `limit_up` | **涨停价** | ⭐⭐⭐⭐⭐（重要！） |
| `limit_down` | **跌停价** | ⭐⭐⭐⭐⭐（重要！） |

**使用示例**:
```python
# 获取涨停价（平台直接提供！）
bars = history_bars(stock, 1, "1d", ["close", "limit_up"])
close_price = bars[0]["close"]
limit_up_price = bars[0]["limit_up"]  # 直接获取涨停价！

# 判断涨停
is_zt = close_price >= limit_up_price * 0.995
```

---

## 二、需要简单计算的因子

虽然平台提供了原始数据，但以下因子需要自己计算：

| 因子名称 | 计算公式 | 难度 | 建议 |
|---------|---------|------|------|
| **涨停判断** | `close >= limit_up * 0.995` | 简单 | ✅ 使用平台 limit_up |
| **开盘涨幅** | `(open - prev_close) / prev_close` | 简单 | ⚠️ 需要自己算 |
| **动量因子** | `(close[-1] / close[-20] - 1) * 100` | 简单 | ⚠️ 需要自己算 |
| **量比** | `mean(volume[-5:]) / mean(volume)` | 简单 | ⚠️ 需要自己算 |
| **价格位置** | `(close - min) / (max - min)` | 简单 | ⚠️ 需要自己算 |

**计算示例**:
```python
import numpy as np

# 获取历史数据
bars = history_bars(stock, 20, "1d", ["close", "volume"])

# 计算动量因子
momentum = (bars["close"][-1] / bars["close"][0] - 1) * 100

# 计算量比因子
vol_ratio = np.mean(bars["volume"][-5:]) / np.mean(bars["volume"])

# 计算价格位置因子
price_pos = (bars["close"][-1] - np.min(bars["close"])) / (np.max(bars["close"]) - np.min(bars["close"]))
```

---

## 三、高级因子库（需要付费）

RiceQuant 还提供了专业的量化因子库（需要高级账户）：

### 1. **动量因子系列**
```
momentum_1m   # 1个月动量
momentum_3m   # 3个月动量
momentum_6m   # 6个月动量
momentum_12m  # 12个月动量
```

### 2. **波动率因子**
```
volatility_1m  # 1个月波动率
volatility_3m  # 3个月波动率
volatility_6m  # 6个月波动率
```

### 3. **技术指标因子**
```
ma_5     # 5日均线
ma_10    # 10日均线
ma_20    # 20日均线
ema_12   # 12日EMA
ema_26   # 26日EMA
macd     # MACD指标
rsi_14   # RSI指标
kdj_k    # KDJ K值
kdj_d    # KDJ D值
kdj_j    # KDJ J值
```

### 4. **流动性因子**
```
turnover_rate   # 换手率
liquidity_score # 流动性评分
amihud_illiq    # Amihud非流动性指标
```

---

## 四、对比：平台因子 vs 自己计算

### ✅ 优先使用平台因子（推荐）

| 因子类型 | 平台提供 | 优势 |
|---------|---------|------|
| **财务因子** | ✅ 完整提供 | 数据准确、更新及时、无需维护 |
| **估值因子** | ✅ 完整提供 | 直接查询、避免计算错误 |
| **涨跌停价** | ✅ 完整提供 | **最重要！避免自己计算涨停价** |
| **市值因子** | ✅ 完整提供 | 市值变化频繁，平台数据更准确 |

### ⚠️ 需要自己计算（但很简单）

| 因子类型 | 需要计算 | 难度 |
|---------|---------|------|
| **动量因子** | ⚠️ 自己算 | 简单（只需收盘价） |
| **量比因子** | ⚠️ 自己算 | 简单（只需成交量） |
| **技术指标** | ⚠️ 自己算或付费 | 中等（可用 numpy/pandas） |
| **组合因子** | ⚠️ 自己算 | 简单（如开盘涨幅） |

---

## 五、最佳实践建议

### 💡 推荐策略

**1. 财务选股因子**（优先使用平台）
```python
# ✅ 使用平台财务因子
cap = get_fundamentals(query(fundamentals.eod_market_cap), date)
pe = get_fundamentals(query(fundamentals.eod_derivative_indicator.pe_ratio), date)
roe = get_fundamentals(query(fundamentals.financial_indicator.roe), date)

# 筛选条件
if cap < 100 and pe < 20 and roe > 15:
    # 小市值 + 低估值 + 高ROE
    pass
```

**2. 涨停策略因子**（优先使用平台）
```python
# ✅ 使用平台涨停价（重要！）
bars = history_bars(stock, 1, "1d", ["close", "limit_up"])
close = bars[0]["close"]
limit_up = bars[0]["limit_up"]  # 直接获取涨停价

# 判断涨停（只需简单计算）
is_zt = close >= limit_up * 0.995
```

**3. 技术因子**（自己计算或付费）
```python
# ⚠️ 自己计算（简单）
bars = history_bars(stock, 20, "1d", ["close"])
momentum = (bars["close"][-1] / bars["close"][0] - 1) * 100

# 💰 或使用付费因子库
momentum = get_factor("momentum_1m", stock, date)  # 需要高级账户
```

---

## 六、实际案例对比

### ❌ 错误做法：重复造轮子

```python
# 错误：自己计算市值
stock_info = get_all_securities()
for stock in stocks:
    price = get_price(stock, date)["close"]
    shares = get_shares(stock)  # 需要额外查询
    market_cap = price * shares  # 自己计算，容易出错
```

### ✅ 正确做法：使用平台因子

```python
# 正确：直接查询市值
for stock in stocks:
    cap_data = get_fundamentals(
        query(fundamentals.eod_market_cap).filter(fundamentals.stockcode == stock),
        date
    )
    market_cap = cap_data["eod_market_cap"].iloc[0]  # 直接获取，准确可靠
```

---

## 七、总结

### 核心结论

| 问题 | 答案 |
|------|------|
| **财务因子能用平台吗？** | ✅ **可以！直接查询 `get_fundamentals()`** |
| **估值因子能用平台吗？** | ✅ **可以！PE、PB、ROE 全都有** |
| **涨停价能用平台吗？** | ✅ **可以！`limit_up` 直接获取** |
| **动量因子能用平台吗？** | ⚠️ **免费版需自己算，付费版可直接获取** |
| **技术指标能用平台吗？** | ⚠️ **免费版需自己算，付费版可直接获取** |

### 推荐策略

**✅ 优先使用**:
1. 财务因子（市值、ROE、营收增长）
2. 估值因子（PE、PB、换手率）
3. 涨停价（`limit_up` 字段）

**⚠️ 简单计算**:
1. 动量因子（收盘价比值）
2. 量比因子（成交量比值）
3. 开盘涨幅（开盘价减昨收）

**💰 付费使用**:
1. 高级动量因子系列
2. MACD、RSI、KDJ等技术指标
3. 波动率因子

---

## 八、最新 Notebook

### RiceQuant 平台因子测试 Notebook

**Notebook URL**: https://www.ricequant.com/research/user/user_497381/notebooks/%E7%AD%96%E7%95%A5%E6%B5%8B%E8%AF%95_20260331_163633.ipynb

**创建时间**: 2026-03-31 16:36:33

**内容**:
- 平台财务因子列表
- 平台价格因子列表
- 需要自己计算的因子
- 最佳实践建议

---

**最后更新**: 2026-03-31  
**结论**: RiceQuant 提供了丰富的财务和估值因子，无需自己计算！优先使用平台能力，提高效率和准确性！