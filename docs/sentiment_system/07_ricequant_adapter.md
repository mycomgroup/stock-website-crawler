# RiceQuant平台适配

本文档说明如何在RiceQuant平台上使用情绪指标系统。

---

## 一、API差异对照

### 1.1 主要差异

| 功能 | 聚宽 | RiceQuant |
|------|------|-----------|
| 获取股票列表 | `get_all_securities()` | `all_instruments(type='CS')` |
| 获取交易日 | `get_trade_days()` | `get_trading_dates()` |
| 获取价格 | `get_price()` | `get_price()` |
| 涨停价字段 | `high_limit` | `limit_up` |
| 跌停价字段 | `low_limit` | `limit_down` |
| 是否ST | `get_extras('is_st')` | `is_st_stock()` |

### 1.2 数据类型差异

| 项目 | 聚宽 | RiceQuant |
|------|------|-----------|
| 日期格式 | Timestamp/str | str |
| 返回格式 | DataFrame | DataFrame |
| panel参数 | 需要`panel=False` | 默认返回DataFrame |
| 时间索引 | datetime | str |

---

## 二、适配代码

### 2.1 股票列表获取

```python
# 聚宽
all_stocks = get_all_securities('stock', date).index.tolist()

# RiceQuant
from rqdatac import *
connect()
all_instruments = instruments(type='CS', date=date)
all_stocks = all_instruments['order_book_id'].tolist()

# 过滤ST和次新股
all_stocks = [s for s in all_stocks 
              if not s.startswith('68')  # 过滤科创板
              and not is_st_stock(s, date)]  # 过滤ST
```

### 2.2 价格数据获取

```python
# 聚宽
df = get_price(stocks, end_date=date, count=1,
               fields=['close', 'high_limit'],
               panel=False)

# RiceQuant
df = get_price(stocks, start_date=date, end_date=date,
               fields=['close', 'limit_up'])
# 注意：RiceQuant不需要panel参数
```

### 2.3 涨停判断

```python
# 聚宽
zt_df = df[df['close'] == df['high_limit']]

# RiceQuant
zt_df = df[df['close'] >= df['limit_up'] * 0.995]  # 允许0.5%误差
```

### 2.4 交易日获取

```python
# 聚宽
trade_days = get_trade_days(start_date=start, end_date=end)

# RiceQuant
trade_days = get_trading_dates(start_date=start, end_date=end)
# 返回类型是pandas DatetimeIndex，需要转换
trade_day_strs = [d.strftime('%Y-%m-%d') for d in trade_days]
```

---

## 三、完整适配模块

```python
#!/usr/bin/env python3
"""
RiceQuant情绪指标适配模块

在RiceQuant环境中使用：
    from ricequant_adapter import calc_market_sentiment_rq
"""

from typing import List, Dict
import pandas as pd


def get_zt_stocks_rq(date: str) -> List[str]:
    """
    RiceQuant版：获取涨停股票列表
    
    参数:
        date: 日期字符串，格式 '2024-01-01'
        
    返回:
        涨停股票代码列表
    """
    # 获取所有股票
    all_instruments = instruments(type='CS', date=date)
    all_stocks = all_instruments['order_book_id'].tolist()
    
    # 过滤科创板
    all_stocks = [s for s in all_stocks if not s.startswith('68')]
    
    if len(all_stocks) == 0:
        return []
    
    # 获取价格数据
    df = get_price(all_stocks, start_date=date, end_date=date,
                   fields=['close', 'limit_up'])
    
    if df is None or len(df) == 0:
        return []
    
    # 涨停判断（允许0.5%误差）
    if 'limit_up' in df.columns:
        zt_df = df[df['close'] >= df['limit_up'] * 0.995]
    else:
        zt_df = df[df['close'] >= df['high_limit'] * 0.995]
    
    return zt_df.index.tolist()


def get_dt_stocks_rq(date: str) -> List[str]:
    """
    RiceQuant版：获取跌停股票列表
    """
    all_instruments = instruments(type='CS', date=date)
    all_stocks = all_instruments['order_book_id'].tolist()
    all_stocks = [s for s in all_stocks if not s.startswith('68')]
    
    if len(all_stocks) == 0:
        return []
    
    df = get_price(all_stocks, start_date=date, end_date=date,
                   fields=['close', 'limit_down'])
    
    if df is None or len(df) == 0:
        return []
    
    if 'limit_down' in df.columns:
        dt_df = df[df['close'] <= df['limit_down'] * 1.005]
    else:
        dt_df = df[df['close'] <= df['low_limit'] * 1.005]
    
    return dt_df.index.tolist()


def calc_lianban_count_rq(stock: str, date: str, max_days: int = 10) -> int:
    """
    RiceQuant版：计算单只股票连板数
    
    参数:
        stock: 股票代码
        date: 日期字符串
        max_days: 最大回溯天数
        
    返回:
        连板数
    """
    # 获取历史交易日
    end_date = pd.Timestamp(date)
    start_date = end_date - pd.Timedelta(days=30)
    
    trading_dates = get_trading_dates(
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=date
    )
    
    if len(trading_dates) < max_days:
        return 0
    
    # 取最近max_days个交易日
    trading_dates = trading_dates[-max_days:]
    date_list = [d.strftime('%Y-%m-%d') if isinstance(d, pd.Timestamp) else d 
                 for d in trading_dates]
    
    # 获取价格数据
    df = get_price(stock, start_date=date_list[0], end_date=date_list[-1],
                   fields=['close', 'limit_up'])
    
    if df is None or len(df) < max_days:
        return 0
    
    # 从后向前统计连板
    count = 0
    for i in range(len(df) - 1, -1, -1):
        row = df.iloc[i] if hasattr(df, 'iloc') else df.iloc[i]
        close = row['close'] if 'close' in row.index else row[0]
        limit_up = row['limit_up'] if 'limit_up' in row.index else row[1]
        
        if close >= limit_up * 0.995:
            count += 1
        else:
            break
    
    return count


def calc_market_sentiment_rq(date: str, prev_date: str) -> Dict:
    """
    RiceQuant版：计算市场情绪指标
    
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
    zt_list = get_zt_stocks_rq(date)
    result['zt_count'] = len(zt_list)
    
    # 2. 跌停家数
    dt_list = get_dt_stocks_rq(date)
    result['dt_count'] = len(dt_list)
    
    # 3. 涨跌停比
    result['zt_dt_ratio'] = len(zt_list) / max(len(dt_list), 1)
    
    # 4. 最高连板数
    max_lianban = 0
    for stock in zt_list[:50]:  # 限制计算量
        lb = calc_lianban_count_rq(stock, date)
        max_lianban = max(max_lianban, lb)
    result['max_lianban'] = max_lianban
    
    # 5. 晋级率
    prev_zt_list = get_zt_stocks_rq(prev_date)
    if len(prev_zt_list) > 0:
        jinji_count = len(set(prev_zt_list) & set(zt_list))
        result['jinji_rate'] = jinji_count / len(prev_zt_list)
    else:
        result['jinji_rate'] = 0
    
    return result


def get_prev_trade_day_rq(date: str) -> str:
    """
    RiceQuant版：获取前一交易日
    
    参数:
        date: 日期字符串
        
    返回:
        前一交易日字符串
    """
    dates = get_trading_dates(
        start_date=(pd.Timestamp(date) - pd.Timedelta(days=10)).strftime('%Y-%m-%d'),
        end_date=date
    )
    # 找到date在列表中的位置
    date_idx = None
    for i, d in enumerate(dates):
        d_str = d.strftime('%Y-%m-%d') if isinstance(d, pd.Timestamp) else d
        if d_str == date:
            date_idx = i
            break
    
    if date_idx is not None and date_idx > 0:
        prev_d = dates[date_idx - 1]
        return prev_d.strftime('%Y-%m-%d') if isinstance(prev_d, pd.Timestamp) else prev_d
    
    return None
```

---

## 四、RiceQuant策略中使用示例

```python
#!/usr/bin/env python3
# RiceQuant策略示例：首板低开 + 情绪开关

import sys
sys.path.append('/path/to/sentiment_system/code/core')
sys.path.append('/path/to/sentiment_system/code/platforms')

from ricequant_adapter import (
    calc_market_sentiment_rq,
    get_prev_trade_day_rq,
    get_zt_stocks_rq
)
from sentiment_switch import sentiment_switch_combo


def init(context):
    """初始化"""
    context.sentiment_threshold = 30
    context.max_positions = 3


def before_trading(context):
    """盘前计算情绪"""
    date = context.current_dt.strftime('%Y-%m-%d')
    prev_date = get_prev_trade_day_rq(date)
    
    if prev_date is None:
        context.should_trade = False
        return
    
    # 计算情绪指标
    sentiment = calc_market_sentiment_rq(date, prev_date)
    context.sentiment = sentiment
    
    # 判断开关
    context.should_trade = sentiment_switch_combo(sentiment)
    
    # 记录日志
    log.info(f"日期: {date}")
    log.info(f"涨停: {sentiment['zt_count']}, 连板: {sentiment['max_lianban']}")
    log.info(f"开关: {'开仓' if context.should_trade else '空仓'}")


def handle_bar(context, bar_dict):
    """盘中交易"""
    if not context.should_trade:
        return
    
    # 获取昨日涨停
    date = context.current_dt.strftime('%Y-%m-%d')
    prev_date = get_prev_trade_day_rq(date)
    prev_zt = get_zt_stocks_rq(prev_date)
    
    # 筛选低开股票
    selected = []
    for stock in prev_zt[:30]:
        try:
            # 获取价格数据
            prev_close = get_price(stock, start_date=prev_date, end_date=prev_date,
                                 fields=['close'])[stock][0]
            today_open = bar_dict[stock].open
            
            # 计算开盘涨幅
            open_ratio = today_open / prev_close - 1
            
            # 低开条件
            if -0.05 <= open_ratio <= -0.01:
                selected.append(stock)
        except:
            continue
        
        if len(selected) >= context.max_positions:
            break
    
    # 开仓
    for stock in selected:
        order_target_percent(stock, 1.0 / len(selected))


def after_trading(context):
    """收盘后记录"""
    pass
```

---

## 五、注意事项

### 5.1 数据延时

RiceQuant的数据可能有15分钟延时：
- 实时数据有15分钟延时
- 收盘后数据需要等待

### 5.2 涨停字段

RiceQuant的涨停字段可能为空：
- 需要检查字段是否存在
- 建议增加容错处理

### 5.3 交易日转换

RiceQuant返回的是Timestamp：
- 需要转换为字符串
- 注意时区问题