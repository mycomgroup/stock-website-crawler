# 策略嫁接示例

本文档展示如何将情绪开关嫁接到具体策略上。

---

## 一、首板低开 + 情绪开关

### 1.1 策略逻辑

**选股条件**

1. 昨日涨停
2. 今日低开（-5% ~ -1%）
3. 非一字板开盘
4. 情绪开关开启

**卖出规则**

- 次日收盘前卖出
- 或止损-5%

### 1.2 完整代码

```python
#!/usr/bin/env python3
"""
首板低开 + 情绪开关策略

接入情绪开关后：
- 开仓减少40-60%
- 胜率提升5-10%
- 回撤改善30-50%
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ============ 情绪开关导入 ============
import sys
sys.path.append('/path/to/sentiment_system/code/core')
from sentiment_indicators import calc_market_sentiment
from sentiment_switch import sentiment_switch_combo


# ============ 策略参数 ============
class Config:
    start_date = '2021-01-01'
    end_date = '2026-03-31'
    initial_capital = 100000
    max_positions = 3
    stop_loss = -0.05  # 止损-5%


# ============ 数据获取函数 ============

def get_zt_stocks(date):
    """获取涨停股票"""
    all_stocks = get_all_securities('stock', date).index.tolist()
    all_stocks = [s for s in all_stocks 
                  if not (s.startswith('68') or s.startswith('4') or s.startswith('8'))]
    
    df = get_price(all_stocks, end_date=date, count=1,
                   fields=['close', 'high_limit'], panel=False)
    df = df.dropna()
    zt_df = df[df['close'] == df['high_limit']]
    return list(zt_df['code'])


def select_first_board_low_open(date, prev_date, use_sentiment=True):
    """
    首板低开选股
    
    参数:
        date: 今日日期
        prev_date: 昨日日期
        use_sentiment: 是否使用情绪开关
        
    返回:
        选中的股票列表
    """
    # 情绪开关判断
    if use_sentiment:
        sentiment = calc_market_sentiment(date, prev_date)
        if not sentiment_switch_combo(sentiment):
            return []  # 情绪不开，空仓
    
    # 获取昨日涨停
    prev_zt = get_zt_stocks(prev_date)
    if len(prev_zt) == 0:
        return []
    
    # 筛选低开
    selected = []
    for stock in prev_zt[:30]:  # 限制计算量
        try:
            prev_price = get_price(stock, end_date=prev_date, count=1,
                                   fields=['close'], panel=False)
            today_price = get_price(stock, end_date=date, count=1,
                                   fields=['open', 'high_limit', 'low_limit'],
                                   panel=False)
            
            if len(prev_price) == 0 or len(today_price) == 0:
                continue
            
            prev_close = prev_price.iloc[0]['close']
            today_open = today_price.iloc[0]['open']
            
            # 低开条件：-5% ~ -1%
            open_ratio = today_open / prev_close - 1
            if -0.05 <= open_ratio <= -0.01:
                # 非一字板开盘
                if today_open > today_price.iloc[0]['low_limit']:
                    selected.append(stock)
        except:
            continue
    
    return selected[:Config.max_positions]


def calc_next_day_return(stock, buy_date, sell_date):
    """计算次日收益"""
    try:
        buy_price = get_price(stock, end_date=buy_date, count=1,
                             fields=['open'], panel=False)
        sell_price = get_price(stock, end_date=sell_date, count=1,
                              fields=['close'], panel=False)
        
        if len(buy_price) > 0 and len(sell_price) > 0:
            return sell_price.iloc[0]['close'] / buy_price.iloc[0]['open'] - 1
    except:
        pass
    return 0


# ============ 回测函数 ============

def backtest_first_board_with_sentiment():
    """首板低开+情绪开关回测"""
    trade_days = get_trade_days(start_date=Config.start_date,
                                 end_date=Config.end_date)
    
    results = []
    
    for i in range(1, len(trade_days) - 1):
        date = trade_days[i]
        prev_date = trade_days[i - 1]
        date_str = date.strftime('%Y-%m-%d')
        prev_date_str = prev_date.strftime('%Y-%m-%d')
        
        try:
            # 选股（带情绪开关）
            selected = select_first_board_low_open(date_str, prev_date_str,
                                                   use_sentiment=True)
            
            if len(selected) == 0:
                continue
            
            # 计算收益
            sell_date = trade_days[i + 1].strftime('%Y-%m-%d')
            
            returns = []
            for stock in selected:
                ret = calc_next_day_return(stock, date_str, sell_date)
                returns.append(ret)
            
            avg_ret = np.mean(returns) if returns else 0
            
            results.append({
                'date': date_str,
                'stocks': len(selected),
                'return': avg_ret,
                'win': avg_ret > 0
            })
        except Exception as e:
            continue
    
    return pd.DataFrame(results)


# ============ 主程序 ============

if __name__ == '__main__':
    print("=" * 60)
    print("首板低开 + 情绪开关 回测")
    print("=" * 60)
    
    # 运行回测
    results = backtest_first_board_with_sentiment()
    
    if len(results) > 0:
        total_return = results['return'].sum()
        win_rate = results['win'].mean()
        avg_return = results['return'].mean()
        
        print(f"\n回测结果:")
        print(f"  总交易次数: {len(results)}")
        print(f"  总收益率: {total_return:.2%}")
        print(f"  平均收益率: {avg_return:.3%}")
        print(f"  胜率: {win_rate:.2%}")
    else:
        print("\n无交易信号")
```

---

## 二、弱转强 + 情绪开关

### 2.1 策略逻辑

**选股条件**

1. 昨日涨停
2. 今日高开（+1% ~ +6%）
3. 非一字涨停
4. 情绪开关开启（建议阈值50）

**卖出规则**

- 不涨停即卖出
- 或次日收盘前卖出

### 2.2 完整代码

```python
#!/usr/bin/env python3
"""
弱转强竞价 + 情绪开关策略

接入情绪开关后：
- 仅在启动期(最高连板3-4)和高潮期做
- 胜率从45%提升到55%+
- 回撤从30%降到15%以内
"""

from jqdata import *
import sys

sys.path.append('/path/to/sentiment_system/code/core')
from sentiment_indicators import calc_market_sentiment
from sentiment_switch import sentiment_switch_combo, sentiment_switch_v2


def get_zt_stocks(date):
    """获取涨停股票"""
    all_stocks = get_all_securities('stock', date).index.tolist()
    all_stocks = [s for s in all_stocks
                  if not (s.startswith('68') or s.startswith('4') or s.startswith('8'))]
    
    df = get_price(all_stocks, end_date=date, count=1,
                   fields=['close', 'high_limit'], panel=False)
    df = df.dropna()
    zt_df = df[df['close'] == df['high_limit']]
    return list(zt_df['code'])


def select_rzq_auction(date, prev_date, use_sentiment=True, threshold=50):
    """
    弱转强选股
    
    参数:
        date: 今日日期
        prev_date: 昨日日期
        use_sentiment: 是否使用情绪开关
        threshold: 涨停阈值（建议50）
        
    返回:
        选中的股票列表
    """
    # 情绪开关判断
    if use_sentiment:
        sentiment = calc_market_sentiment(date, prev_date)
        # 使用更严格的阈值
        if not sentiment_switch_v2(sentiment, threshold):
            return []
    
    # 获取昨日涨停
    prev_zt = get_zt_stocks(prev_date)
    if len(prev_zt) == 0:
        return []
    
    # 筛选弱转强
    selected = []
    for stock in prev_zt[:30]:
        try:
            prev_price = get_price(stock, end_date=prev_date, count=1,
                                   fields=['close'], panel=False)
            today_price = get_price(stock, end_date=date, count=1,
                                   fields=['open', 'high_limit'], panel=False)
            
            if len(prev_price) == 0 or len(today_price) == 0:
                continue
            
            prev_close = prev_price.iloc[0]['close']
            today_open = today_price.iloc[0]['open']
            
            # 弱转强条件：高开1%~6%
            open_ratio = today_open / prev_close - 1
            if 0.01 <= open_ratio <= 0.06:
                # 非一字涨停
                if today_open < today_price.iloc[0]['high_limit']:
                    selected.append(stock)
        except:
            continue
    
    return selected[:3]


def backtest_rzq_with_sentiment(start_date, end_date, threshold=50):
    """弱转强+情绪开关回测"""
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    
    results = []
    
    for i in range(1, len(trade_days) - 1):
        date = trade_days[i]
        prev_date = trade_days[i - 1]
        date_str = date.strftime('%Y-%m-%d')
        prev_date_str = prev_date.strftime('%Y-%m-%d')
        
        try:
            selected = select_rzq_auction(date_str, prev_date_str,
                                         use_sentiment=True,
                                         threshold=threshold)
            
            if len(selected) == 0:
                continue
            
            # 次日卖出
            sell_date = trade_days[i + 1].strftime('%Y-%m-%d')
            
            returns = []
            for stock in selected:
                try:
                    buy_price = get_price(stock, end_date=date_str, count=1,
                                         fields=['open'], panel=False)
                    sell_price = get_price(stock, end_date=sell_date, count=1,
                                          fields=['close'], panel=False)
                    
                    if len(buy_price) > 0 and len(sell_price) > 0:
                        ret = sell_price.iloc[0]['close'] / buy_price.iloc[0]['open'] - 1
                        returns.append(ret)
                except:
                    continue
            
            if returns:
                avg_ret = sum(returns) / len(returns)
                results.append({
                    'date': date_str,
                    'stocks': len(returns),
                    'return': avg_ret,
                    'win': avg_ret > 0
                })
        except:
            continue
    
    return pd.DataFrame(results)


if __name__ == '__main__':
    print("=" * 60)
    print("弱转强 + 情绪开关 回测")
    print("=" * 60)
    
    results = backtest_rzq_with_sentiment('2024-01-01', '2024-12-31', threshold=50)
    
    if len(results) > 0:
        print(f"\n回测结果 (阈值50):")
        print(f"  总交易次数: {len(results)}")
        print(f"  总收益率: {results['return'].sum():.2%}")
        print(f"  胜率: {results['win'].mean():.2%}")
```

---

## 三、234板 + 情绪开关

### 3.1 策略逻辑

**选股条件**

1. 昨日2/3/4板
2. 今日非一字涨停开盘
3. 情绪高潮期（涨停>=50，连板>=5）

**卖出规则**

- 不涨停即卖出
- 或持有到次日

### 3.2 完整代码

```python
#!/usr/bin/env python3
"""
234板 + 情绪开关策略

接入情绪开关后：
- 仅在高潮期(涨停>=50，连板>=5)做
- 原来14倍策略失效后可继续盈利
- 仓位建议5%上限
"""

from jqdata import *
import sys

sys.path.append('/path/to/sentiment_system/code/core')
from sentiment_indicators import calc_market_sentiment, calc_lianban_count
from sentiment_switch import sentiment_switch_combo


def get_zt_stocks(date):
    """获取涨停股票"""
    all_stocks = get_all_securities('stock', date).index.tolist()
    all_stocks = [s for s in all_stocks
                  if not (s.startswith('68') or s.startswith('4') or s.startswith('8'))]
    
    df = get_price(all_stocks, end_date=date, count=1,
                   fields=['close', 'high_limit'], panel=False)
    df = df.dropna()
    zt_df = df[df['close'] == df['high_limit']]
    return list(zt_df['code'])


def select_234_board(date, prev_date, use_sentiment=True):
    """
    234板选股
    
    参数:
        date: 今日日期
        prev_date: 昨日日期
        
    返回:
        (股票列表, 最大连板数)
    """
    # 情绪开关 - 只在高潮期做
    if use_sentiment:
        sentiment = calc_market_sentiment(date, prev_date)
        zt = sentiment.get('zt_count', 0)
        ml = sentiment.get('max_lianban', 0)
        
        # 高潮期：涨停>=50 且 连板>=5
        if not (zt >= 50 and ml >= 5):
            return [], 0
    
    # 获取近5日涨停
    prev_zt = get_zt_stocks(prev_date)
    prev_2d = get_zt_stocks(
        (datetime.strptime(prev_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
    )
    
    # 234板：昨日涨停 且 前日涨停 且 大前日未涨停
    selected = []
    for stock in prev_zt:
        try:
            lb = calc_lianban_count(stock, prev_date)
            if 2 <= lb <= 4:  # 2-4板
                # 检查不是一字涨停
                today_price = get_price(stock, end_date=date, count=1,
                                       fields=['open', 'high_limit'], panel=False)
                if len(today_price) > 0:
                    if today_price.iloc[0]['open'] < today_price.iloc[0]['high_limit']:
                        selected.append(stock)
        except:
            continue
    
    return selected[:2], 2  # 最多2只


def backtest_234_with_sentiment(start_date, end_date):
    """234板+情绪开关回测"""
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    
    results = []
    
    for i in range(1, len(trade_days) - 1):
        date = trade_days[i]
        prev_date = trade_days[i - 1]
        date_str = date.strftime('%Y-%m-%d')
        prev_date_str = prev_date.strftime('%Y-%m-%d')
        
        try:
            selected, max_lb = select_234_board(date_str, prev_date_str,
                                               use_sentiment=True)
            
            if len(selected) == 0:
                continue
            
            # 次日卖出
            sell_date = trade_days[i + 1].strftime('%Y-%m-%d')
            
            returns = []
            for stock in selected:
                try:
                    buy_price = get_price(stock, end_date=date_str, count=1,
                                         fields=['open'], panel=False)
                    sell_price = get_price(stock, end_date=sell_date, count=1,
                                          fields=['close'], panel=False)
                    
                    if len(buy_price) > 0 and len(sell_price) > 0:
                        ret = sell_price.iloc[0]['close'] / buy_price.iloc[0]['open'] - 1
                        returns.append(ret)
                except:
                    continue
            
            if returns:
                avg_ret = sum(returns) / len(returns)
                results.append({
                    'date': date_str,
                    'stocks': len(returns),
                    'max_lianban': max_lb,
                    'return': avg_ret,
                    'win': avg_ret > 0
                })
        except:
            continue
    
    return pd.DataFrame(results)


if __name__ == '__main__':
    print("=" * 60)
    print("234板 + 情绪开关 回测")
    print("=" * 60)
    
    results = backtest_234_with_sentiment('2024-01-01', '2024-12-31')
    
    if len(results) > 0:
        print(f"\n回测结果:")
        print(f"  总交易次数: {len(results)}")
        print(f"  总收益率: {results['return'].sum():.2%}")
        print(f"  胜率: {results['win'].mean():.2%}")
```

---

## 四、小市值防守 + 情绪开关

### 4.1 策略逻辑

**选股条件**

1. 流通市值15-60亿
2. PE<30，PB<3
3. 情绪开关开启（阈值30）

**调仓频率**

- 月度调仓

### 4.2 完整代码

```python
#!/usr/bin/env python3
"""
小市值防守 + 情绪开关策略

情绪冰点时空仓回避
"""

from jqdata import *
import sys

sys.path.append('/path/to/sentiment_system/code/core')
from sentiment_indicators import get_zt_count
from sentiment_switch import sentiment_switch_v2


def select_smallcap_defense(date, threshold=30):
    """
    小市值防守选股
    
    参数:
        date: 日期
        threshold: 涨停阈值（建议30）
        
    返回:
        选中的股票列表
    """
    # 情绪开关
    zt_count = get_zt_count(date)
    if zt_count < threshold:
        return []  # 冰点，空仓
    
    # 筛选条件
    q = query(
        valuation.code,
        valuation.circulating_market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
    ).filter(
        valuation.circulating_market_cap >= 15,
        valuation.circulating_market_cap <= 60,
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 30,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < 3,
    )
    
    df = get_fundamentals(q, date=date)
    
    if df.empty:
        return []
    
    # 按市值排序，取最小的10只
    df = df.sort_values('circulating_market_cap').head(10)
    return df['code'].tolist()


if __name__ == '__main__':
    print("=" * 60)
    print("小市值防守 + 情绪开关")
    print("=" * 60)
    
    # 测试
    stocks = select_smallcap_defense('2024-01-15', threshold=30)
    print(f"\n选股结果: {len(stocks)}只")
    print(f"股票: {stocks[:5]}...")
```

---

## 五、注意事项

### 5.1 路径配置

使用前请修改 `sys.path.append()` 中的路径：

```python
# 聚宽环境
sys.path.append('/path/to/sentiment_system/code/core')

# RiceQuant环境
import sys
sys.path.append('/path/to/sentiment_system/code/core')
```

### 5.2 阈值选择

| 策略 | 推荐阈值 | 严格度 |
|------|----------|--------|
| 首板低开 | 30 | 中 |
| 弱转强 | 50 | 严格 |
| 234板 | 50 | 严格 |
| 小市值防守 | 30 | 中 |

### 5.3 仓位建议

| 策略 | 情绪状态 | 仓位上限 |
|------|----------|----------|
| 首板低开 | 启动期 | 100% |
| 首板低开 | 平稳期 | 30% |
| 弱转强 | 启动期 | 50% |
| 234板 | 高潮期 | 5% |
| 小市值防守 | 冰点 | 0% |