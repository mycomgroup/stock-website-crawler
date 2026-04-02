# 情绪指标定义与计算

本文档详细定义所有情绪指标及其计算方法。

---

## 一、核心指标

### 1.1 涨停家数 (zt_count)

**定义**

当日收盘价等于涨停价的股票数量。

**计算公式**

```
zt_count = count(close == high_limit)
```

**数据来源**

- 聚宽：`get_price()` 的 `high_limit` 字段
- RiceQuant：`get_price()` 的 `limit_up` 字段
- 东方财富：涨停板行情接口

**阈值参考**

| 阈值 | 含义 | 建议 |
|------|------|------|
| < 15 | 极弱，冰点 | 空仓 |
| 15-30 | 较弱 | 谨慎 |
| 30-50 | 正常 | 可开仓 |
| 50-80 | 活跃 | 积极开仓 |
| > 80 | 亢奋 | 注意风险 |

**代码实现**

```python
def get_zt_count(date):
    """获取涨停家数"""
    all_stocks = get_all_securities('stock', date).index.tolist()
    # 过滤科创板和北交所
    all_stocks = [s for s in all_stocks if not (s.startswith('68') or s.startswith('4') or s.startswith('8'))]
    
    df = get_price(all_stocks, end_date=date, count=1, 
                   fields=['close', 'high_limit'], panel=False)
    df = df.dropna()
    
    # 涨停：收盘价等于涨停价
    zt_df = df[df['close'] == df['high_limit']]
    return len(zt_df)
```

---

### 1.2 跌停家数 (dt_count)

**定义**

当日收盘价等于跌停价的股票数量。

**计算公式**

```
dt_count = count(close == low_limit)
```

**数据来源**

- 聚宽：`get_price()` 的 `low_limit` 字段
- RiceQuant：`get_price()` 的 `limit_down` 字段

**阈值参考**

| 阈值 | 含义 | 建议 |
|------|------|------|
| < 5 | 市场情绪好 | 正常开仓 |
| 5-15 | 正常 | 关注 |
| 15-30 | 较差 | 谨慎 |
| > 30 | 极差 | 空仓 |

**代码实现**

```python
def get_dt_count(date):
    """获取跌停家数"""
    all_stocks = get_all_securities('stock', date).index.tolist()
    all_stocks = [s for s in all_stocks if not (s.startswith('68') or s.startswith('4') or s.startswith('8'))]
    
    df = get_price(all_stocks, end_date=date, count=1, 
                   fields=['close', 'low_limit'], panel=False)
    df = df.dropna()
    
    # 跌停：收盘价等于跌停价
    dt_df = df[df['close'] == df['low_limit']]
    return len(dt_df)
```

---

### 1.3 涨跌停比 (zt_dt_ratio)

**定义**

涨停家数与跌停家数的比值，反映多空力量对比。

**计算公式**

```
zt_dt_ratio = zt_count / max(dt_count, 1)
```

**阈值参考**

| 阈值 | 含义 | 建议 |
|------|------|------|
| < 1 | 空方占优 | 空仓 |
| 1-2 | 均衡 | 谨慎 |
| 2-5 | 多方占优 | 可开仓 |
| > 5 | 极强 | 注意风险 |

**代码实现**

```python
def calc_zt_dt_ratio(zt_count, dt_count):
    """计算涨跌停比"""
    return zt_count / max(dt_count, 1)
```

---

### 1.4 最高连板数 (max_lianban)

**定义**

当日涨停股票中，连续涨停天数的最大值。

**计算方法**

从后向前统计连续涨停天数：

```
连板数 = 从今日向前数，连续涨停的天数
```

**阈值参考**

| 阈值 | 含义 | 建议 |
|------|------|------|
| 1-2 | 无主线 | 谨慎 |
| 3-4 | 主线确立 | 可开仓 |
| 5-6 | 强主线 | 积极开仓 |
| > 6 | 极端亢奋 | 注意风险 |

**代码实现**

```python
def calc_lianban_count(stock, date, max_days=10):
    """计算单只股票连板数"""
    df = get_price(stock, end_date=date, count=max_days, 
                   fields=['close', 'high_limit'], panel=False)
    
    if len(df) < max_days:
        return 0
    
    # 从后向前统计
    count = 0
    for i in range(len(df)-1, -1, -1):
        if df.iloc[i]['close'] == df.iloc[i]['high_limit']:
            count += 1
        else:
            break
    return count

def get_max_lianban(date):
    """获取最高连板数"""
    zt_stocks = get_zt_stocks(date)
    max_lb = 0
    for stock in zt_stocks[:50]:  # 限制计算量
        lb = calc_lianban_count(stock, date)
        max_lb = max(max_lb, lb)
    return max_lb
```

---

### 1.5 晋级率 (jinji_rate)

**定义**

前日涨停股票中，今日继续涨停的比例。反映接力意愿。

**计算公式**

```
jinji_rate = count(今日涨停 ∧ 前日涨停) / count(前日涨停)
```

**阈值参考**

| 阈值 | 含义 | 建议 |
|------|------|------|
| < 20% | 接力意愿弱 | 空仓 |
| 20-30% | 正常 | 谨慎 |
| 30-50% | 接力意愿强 | 可开仓 |
| > 50% | 极强 | 注意分歧 |

**代码实现**

```python
def calc_jinji_rate(date, prev_date):
    """计算晋级率"""
    zt_today = set(get_zt_stocks(date))
    zt_prev = set(get_zt_stocks(prev_date))
    
    if len(zt_prev) == 0:
        return 0
    
    jinji_count = len(zt_today & zt_prev)
    return jinji_count / len(zt_prev)
```

---

## 二、辅助指标

### 2.1 市场宽度 (Breadth)

**定义**

价格在N日均线之上的股票占比。

**计算公式**

```
breadth = count(close > MA20) / count(all_stocks)
```

**阈值参考**

| 阈值 | 含义 |
|------|------|
| < 30% | 极度悲观（底部信号） |
| 30-50% | 悲观 |
| 50-70% | 正常 |
| > 70% | 乐观（注意风险） |

**代码实现**

```python
def calc_market_breadth(date, window=20):
    """计算市场宽度"""
    stocks = get_index_stocks('000902.XSHG', date)  # 中证全指
    
    prices = get_price(stocks, end_date=date, count=window+1, 
                       fields=['close'], panel=False)
    pivot = prices.pivot(index='time', columns='code', values='close')
    
    ma = pivot.rolling(window).mean()
    
    above_ma = (pivot.iloc[-1] > ma.iloc[-1]).sum()
    total = len(pivot.columns)
    
    return above_ma / total
```

---

### 2.2 拥挤率 (Crowding)

**定义**

成交额前5%股票的成交额占比。反映资金集中度。

**计算公式**

```
crowding = sum(top5%_money) / sum(all_money)
```

**阈值参考**

| 阈值 | 含义 |
|------|------|
| < 40% | 资金分散（底部特征） |
| 40-60% | 正常 |
| > 60% | 资金集中（过热） |

**代码实现**

```python
def calc_crowding(date):
    """计算拥挤率"""
    all_stocks = get_all_securities(date).index.tolist()
    df = get_price(all_stocks, end_date=date, count=1, 
                   fields=['money'], panel=False)
    df = df.dropna().sort_values('money', ascending=False)
    
    n_top = max(1, int(len(df) * 0.05))
    top_money = df.iloc[:n_top]['money'].sum()
    total_money = df['money'].sum()
    
    return top_money / total_money
```

---

### 2.3 GSISI投资者情绪指数

**定义**

基于行业收益率与Beta的Spearman秩相关系数，反映投资者情绪状态。

**计算方法**

1. 计算各行业N日收益率
2. 计算各行业对指数的Beta
3. 计算收益率与Beta的Spearman相关系数

**阈值参考**

| 阈值 | 含义 |
|------|------|
| < -0.3 | 悲观（可能底部） |
| -0.3 ~ 0.3 | 中性 |
| > 0.3 | 乐观（注意风险） |

**代码实现**

详见 `code/platforms/joinquant_macro_sentiment.py`

---

### 2.4 FED指标

**定义**

盈利收益率与国债收益率的差值。

**计算公式**

```
FED = 盈利收益率 - 国债收益率
盈利收益率 = 1 / PE
```

**阈值参考**

| 阈值 | 含义 |
|------|------|
| > 0 | 股票低估 |
| < 0 | 股票高估 |

---

### 2.5 格雷厄姆指数

**定义**

盈利收益率与国债收益率的比值。

**计算公式**

```
Graham = 盈利收益率 / 国债收益率
```

**阈值参考**

| 阈值 | 含义 |
|------|------|
| > 1.5 | 低估 |
| 1-1.5 | 中性 |
| < 1 | 高估 |

---

## 三、综合情绪计算

### 3.1 一键计算所有核心指标

```python
def calc_market_sentiment(date, prev_date):
    """
    计算当日市场情绪指标
    
    参数:
        date: 当前日期
        prev_date: 前一交易日
        
    返回:
        {
            'zt_count': 涨停家数,
            'dt_count': 跌停家数,
            'zt_dt_ratio': 涨跌停比,
            'max_lianban': 最高连板数,
            'jinji_rate': 晋级率
        }
    """
    result = {}
    
    # 1. 涨停家数
    zt_list = get_zt_stocks(date)
    result['zt_count'] = len(zt_list)
    
    # 2. 跌停家数
    dt_list = get_dt_stocks(date)
    result['dt_count'] = len(dt_list)
    
    # 3. 涨跌停比
    result['zt_dt_ratio'] = len(zt_list) / max(len(dt_list), 1)
    
    # 4. 最高连板数
    max_lianban = 0
    for stock in zt_list[:50]:
        lb = calc_lianban_count(stock, date)
        max_lianban = max(max_lianban, lb)
    result['max_lianban'] = max_lianban
    
    # 5. 晋级率
    prev_zt_list = get_zt_stocks(prev_date)
    if len(prev_zt_list) > 0:
        jinji_count = len(set(prev_zt_list) & set(zt_list))
        result['jinji_rate'] = jinji_count / len(prev_zt_list)
    else:
        result['jinji_rate'] = 0
    
    return result
```

---

## 四、指标使用优先级

| 优先级 | 指标 | 用途 |
|--------|------|------|
| 1 | 涨停家数 | 最常用，决定是否开仓 |
| 2 | 最高连板数 | 判断主线强度 |
| 3 | 涨跌停比 | 判断多空力量 |
| 4 | 晋级率 | 判断接力意愿 |
| 5 | 市场宽度 | 辅助验证 |
| 6 | 拥挤率 | 辅助验证 |

**推荐组合**：涨停家数 + 最高连板数 + 涨跌停比

---

## 五、指标计算时间

| 时间点 | 可计算指标 | 数据状态 |
|--------|-----------|----------|
| 盘前（9:00前） | 所有核心指标 | 使用T-1日收盘数据 |
| 盘中 | 无法计算 | 等待收盘 |
| 盘后（15:00后） | 当日指标 | 使用当日收盘数据 |

**重要**：情绪指标基于T-1日收盘数据，在T日开盘前计算。