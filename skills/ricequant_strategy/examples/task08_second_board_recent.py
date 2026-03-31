"""
二板策略最近日期测试 - RiceQuant Notebook
测试时间：2025-01-01 至 2026-03-31
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("二板策略最近日期测试（RiceQuant）")
print("测试时间：2025-01-01 至 2026-03-31")
print("=" * 80)

# RiceQuant API 差异：
# - get_all_securities(["stock"]) 不需要日期参数
# - index_components("000300.XSHG") 不需要日期参数
# - get_price 使用 order_book_id 而非 code

def get_second_board_stocks_ricequant(date):
    """获取昨日二板股票（RiceQuant 版本）"""
    try:
        # 获取交易日列表
        dates = get_trading_dates(date, date)
        if len(dates) == 0:
            return None
        
        current_date = dates[0]
        
        # 获取前几天的交易日
        prev_dates = get_trading_dates("2024-01-01", date)
        if len(prev_dates) < 3:
            return None
        
        prev_date = prev_dates[-2] if len(prev_dates) >= 2 else None
        prev_prev_date = prev_dates[-3] if len(prev_dates) >= 3 else None
        
        if not prev_date or not prev_prev_date:
            return None
        
        # 获取所有股票
        all_stocks = get_all_securities(["stock"])
        stock_list = list(all_stocks.index)[:500]  # 限制数量
        
        results = []
        
        for stock in stock_list:
            try:
                # 获取行情数据
                prices = get_price(stock, start_date=prev_prev_date, end_date=date, 
                                   fields=['open', 'close', 'high', 'low', 'volume'])
                
                if len(prices) < 3:
                    continue
                
                # 昨日数据
                prev_data = prices.iloc[-2]
                prev_close = prev_data['close']
                prev_high = prev_data['high']
                prev_volume = prev_data['volume']
                prev_open = prev_data['open']
                
                # 前日数据
                prev_prev_data = prices.iloc[-3]
                prev_prev_close = prev_prev_data['close']
                prev_prev_high = prev_prev_data['high']
                prev_prev_volume = prev_prev_data['volume']
                
                # 今日数据
                today_data = prices.iloc[-1]
                today_open = today_data['open']
                today_close = today_data['close']
                
                # 检查昨日涨停
                prev_limit_up = (prev_close >= prev_high * 0.995) and (prev_close >= prev_prev_close * 1.095)
                
                # 检查前日涨停
                prev_prev_limit_up = (prev_prev_close >= prev_prev_high * 0.995)
                
                if not (prev_limit_up and prev_prev_limit_up):
                    continue
                
                # 排除一字板
                if abs(prev_open - prev_close) < 0.01:
                    continue
                
                # 检查缩量条件
                if prev_volume > prev_prev_volume * 1.875:
                    continue
                
                # 排除今日涨停开盘
                if today_open >= prev_close * 1.095:
                    continue
                
                # 计算收益
                buy_price = today_open
                sell_price = today_close
                ret = (sell_price - buy_price) / buy_price - 0.005  # 滑点
                
                results.append({
                    'stock': stock,
                    'date': current_date,
                    'return': ret,
                    'buy_price': buy_price,
                    'sell_price': sell_price
                })
                
            except Exception as e:
                continue
        
        if results:
            return results
        
        return None
        
    except Exception as e:
        print(f"Error getting second board stocks for {date}: {e}")
        return None

def get_market_sentiment_ricequant(date):
    """获取市场情绪：涨停家数（RiceQuant 版本）"""
    try:
        all_stocks = get_all_securities(["stock"])
        stock_list = list(all_stocks.index)[:1000]
        
        limit_up_count = 0
        
        for stock in stock_list:
            try:
                prices = get_price(stock, start_date=date, end_date=date, 
                                   fields=['close', 'high'])
                
                if len(prices) < 2:
                    continue
                
                prev_prices = get_price(stock, start_date=date, end_date=date, count=2,
                                        fields=['close', 'high'])
                
                if len(prev_prices) < 2:
                    continue
                
                today_close = prev_prices.iloc[-1]['close']
                today_high = prev_prices.iloc[-1]['high']
                prev_close = prev_prices.iloc[-2]['close']
                
                if (today_close >= today_high * 0.995) and (today_close >= prev_close * 1.095):
                    limit_up_count += 1
                    
            except:
                continue
        
        return limit_up_count
        
    except Exception as e:
        print(f"Error getting market sentiment for {date}: {e}")
        return 0

# 主测试逻辑
test_dates = [
    "2025-01-15",
    "2025-02-15",
    "2025-03-15",
    "2025-04-15",
    "2025-05-15",
    "2025-06-15",
    "2025-07-15",
    "2025-08-15",
    "2025-09-15",
    "2025-10-15",
    "2025-11-15",
    "2025-12-15",
    "2026-01-15",
    "2026-02-15",
    "2026-03-15"
]

print(f"\n测试日期数: {len(test_dates)}")

all_results = []

for test_date in test_dates:
    print(f"\n处理日期: {test_date}")
    
    # 获取市场情绪
    sentiment = get_market_sentiment_ricequant(test_date)
    print(f"  涨停家数: {sentiment}")
    
    if sentiment < 10:
        print(f"  情绪开关未触发（涨停<10），跳过")
        continue
    
    # 获取二板股票
    stocks = get_second_board_stocks_ricequant(test_date)
    
    if stocks:
        for stock_info in stocks:
            all_results.append(stock_info)
            print(f"  找到股票: {stock_info['stock']}, 收益: {stock_info['return']*100:.2f}%")

# 统计结果
if all_results:
    df = pd.DataFrame(all_results)
    
    print("\n" + "=" * 80)
    print("统计结果:")
    print("=" * 80)
    
    total_trades = len(df)
    win_count = (df['return'] > 0).sum()
    win_rate = win_count / total_trades * 100 if total_trades > 0 else 0
    
    avg_return = df['return'].mean() * 100
    cumulative_return = (1 + df['return']).prod() - 1
    
    print(f"总交易次数: {total_trades}")
    print(f"盈利次数: {win_count}")
    print(f"胜率: {win_rate:.2f}%")
    print(f"平均收益: {avg_return:.2f}%")
    print(f"累计收益: {cumulative_return*100:.2f}%")
    
    print("\n详细交易记录:")
    for idx, row in df.iterrows():
        print(f"  {row['date']}: {row['stock']} 买入{row['buy_price']:.2f} 卖出{row['sell_price']:.2f} 收益{row['return']*100:+.2f}%")
    
    # 保存结果到文件
    result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/task08_ricequant_recent_result.json"
    
    import json
    result_data = {
        'test_period': '2025-01-15 至 2026-03-15',
        'total_trades': total_trades,
        'win_rate': win_rate,
        'avg_return': avg_return,
        'cumulative_return': cumulative_return * 100,
        'trades': df.to_dict('records')
    }
    
    try:
        with open(result_file, 'w') as f:
            json.dump(result_data, f, indent=2)
        print(f"\n结果已保存至: {result_file}")
    except:
        print("\n无法保存结果到本地文件")
    
else:
    print("\n未找到符合条件的二板股票")

print("\n=" * 80)
print("测试完成")
print("=" * 80)
