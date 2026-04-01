"""
首板低开策略验证 - 历史期（2024-07-01 至 2025-03-31）
"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("首板低开策略验证 - 历史期")
print("=" * 80)

start_date = "2024-07-01"
end_date = "2025-03-31"

trading_dates = get_trade_days(start_date, end_date)
print(f"交易日数量: {len(trading_dates)}")

print("\n第一步：批量获取涨停股票")

all_zt_data = []
for i, date in enumerate(trading_dates):
    if i % 10 == 0:
        print(f"  处理进度: {i}/{len(trading_dates)} ({date})")
    
    prev_dates = get_trade_days(end_date=date, count=2)
    if len(prev_dates) < 2:
        continue
    prev_date = prev_dates[0]
    
    all_stocks = get_all_securities(types=["stock"], date=date)
    stocks_list = [s for s in all_stocks.index.tolist() 
                   if not (s.startswith("688") or s.startswith("300") or 
                          s.startswith("4") or s.startswith("8"))]
    
    df = get_price(stocks_list, end_date=prev_date, frequency="daily",
                   fields=["close", "high_limit"], count=1, panel=False)
    
    df = df.dropna()
    zt_df = df[df["close"] == df["high_limit"]]
    
    for stock in zt_df["code"].values:
        all_zt_data.append({
            "stock": stock,
            "zt_date": prev_date,
            "signal_date": date
        })

print(f"涨停总数: {len(all_zt_data)}")

print("\n第二步：筛选首板（非连板）")

first_board_data = []
for i, item in enumerate(all_zt_data):
    if i % 200 == 0:
        print(f"  处理进度: {i}/{len(all_zt_data)}")
    
    stock = item["stock"]
    zt_date = item["zt_date"]
    
    prev_prev_dates = get_trade_days(end_date=zt_date, count=2)
    if len(prev_prev_dates) < 2:
        first_board_data.append(item)
        continue
    
    prev_prev_date = prev_prev_dates[0]
    
    df_prev = get_price(stock, end_date=prev_prev_date, frequency="daily",
                        fields=["close", "high_limit"], count=1, panel=False)
    
    if df_prev.empty:
        first_board_data.append(item)
        continue
    
    prev_close = float(df_prev["close"].iloc[0])
    prev_high_limit = float(df_prev["high_limit"].iloc[0])
    
    if abs(prev_close - prev_high_limit) / prev_high_limit >= 0.01:
        first_board_data.append(item)

print(f"首板总数: {len(first_board_data)}")

print("\n第三步：筛选低开+市值+位置")

valid_signals = []
for i, item in enumerate(first_board_data):
    if i % 100 == 0:
        print(f"  处理进度: {i}/{len(first_board_data)}")
    
    stock = item["stock"]
    signal_date = item["signal_date"]
    zt_date = item["zt_date"]
    
    df_open = get_price(stock, end_date=zt_date, frequency="daily",
                        fields=["close"], count=1, panel=False)
    
    if df_open.empty:
        continue
    
    zt_close = float(df_open["close"].iloc[0])
    
    df_curr = get_price(stock, end_date=signal_date, frequency="daily",
                        fields=["open"], count=1, panel=False)
    
    if df_curr.empty:
        continue
    
    curr_open = float(df_curr["open"].iloc[0])
    
    open_pct = (curr_open - zt_close) / zt_close * 100
    
    if not (-2.0 <= open_pct <= 1.5):
        continue
    
    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.code == stock
    )
    df_cap = get_fundamentals(q, signal_date)
    
    if df_cap.empty:
        continue
    
    market_cap = float(df_cap["circulating_market_cap"].iloc[0])
    
    if not (5 <= market_cap <= 15):
        continue
    
    df_pos = get_price(stock, end_date=signal_date, frequency="daily",
                       fields=["close"], count=15, panel=False)
    
    if len(df_pos) < 5:
        continue
    
    high_15d = df_pos["close"].max()
    low_15d = df_pos["close"].min()
    curr_close = df_pos["close"].iloc[-1]
    
    if high_15d == low_15d:
        continue
    
    position = (curr_close - low_15d) / (high_15d - low_15d)
    
    if position > 0.30:
        continue
    
    valid_signals.append({
        "stock": stock,
        "signal_date": signal_date,
        "open_pct": open_pct,
        "buy_price": curr_open,
        "market_cap": market_cap,
        "position": position
    })

print(f"有效信号数: {len(valid_signals)}")

print("\n第四步：计算收益")

for i, signal in enumerate(valid_signals):
    if i % 20 == 0:
        print(f"  处理进度: {i}/{len(valid_signals)}")
    
    signal_date = signal["signal_date"]
    stock = signal["stock"]
    
    next_dates = get_trade_days(end_date=signal_date, count=2)
    if len(next_dates) < 2:
        signal["return_high"] = None
        signal["return_close"] = None
        continue
    
    next_date = next_dates[1]
    
    df_next = get_price(stock, end_date=next_date, frequency="daily",
                        fields=["high", "close"], count=1, panel=False)
    
    if df_next.empty:
        signal["return_high"] = None
        signal["return_close"] = None
        continue
    
    buy_price = signal["buy_price"]
    next_high = float(df_next["high"].iloc[0])
    next_close = float(df_next["close"].iloc[0])
    
    signal["return_high"] = (next_high - buy_price) / buy_price * 100
    signal["return_close"] = (next_close - buy_price) / buy_price * 100

print(f"\n{'=' * 80}")
print("历史期统计结果")
print(f"{'=' * 80}")

if valid_signals:
    df_results = pd.DataFrame(valid_signals)
    df_valid = df_results.dropna(subset=["return_high"])
    
    if len(df_valid) > 0:
        trading_days = len(trading_dates)
        
        print(f"\n信号特征:")
        print(f"  总信号数: {len(df_valid)}")
        print(f"  日均信号: {len(df_valid) / trading_days:.2f}")
        print(f"  平均开盘涨跌幅: {df_valid['open_pct'].mean():.2f}%")
        print(f"  平均市值: {df_valid['market_cap'].mean():.1f}亿")
        print(f"  平均位置: {df_valid['position'].mean():.2f}")
        
        print(f"\n收益统计（次日最高卖出）:")
        avg_return_high = df_valid['return_high'].mean()
        win_rate_high = (df_valid['return_high'] > 0).sum() / len(df_valid) * 100
        profit_factor = abs(df_valid[df_valid['return_high'] > 0]['return_high'].sum() / 
                           abs(df_valid[df_valid['return_high'] < 0]['return_high'].sum()))
                           if df_valid[df_valid['return_high'] < 0]['return_high'].sum() != 0 else 0
        
        print(f"  平均收益: {avg_return_high:.2f}%")
        print(f"  胜率: {win_rate_high:.1f}%")
        print(f"  盈亏比: {profit_factor:.2f}")
        
        print(f"\n收益统计（次日收盘卖出）:")
        avg_return_close = df_valid['return_close'].mean()
        win_rate_close = (df_valid['return_close'] > 0).sum() / len(df_valid) * 100
        print(f"  平均收益: {avg_return_close:.2f}%")
        print(f"  胜率: {win_rate_close:.1f}%")
        
        print(f"\n年化收益估算:")
        annual_return = avg_return_high * (len(df_valid) / trading_days) * 250
        print(f"  年化收益（次日最高）: {annual_return:.1f}%")
        
        print(f"\n历史期完整数据已生成")
    else:
        print("无有效收益数据")
else:
    print("无有效信号")

print("\n" + "=" * 80)
print("历史期验证完成")
print("=" * 80)