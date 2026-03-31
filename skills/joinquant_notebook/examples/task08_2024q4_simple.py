"""
二板策略2024-Q4对比测试 - 简化版
测试2024年末行情，对比情绪高涨时段
"""

from jqdata import *

print("=" * 70)
print("2024-Q4对比测试 - 年末行情")
print("=" * 70)

trade_days = get_trade_days(start_date="2024-10-01", end_date="2024-12-31")
test_dates = [d.strftime('%Y-%m-%d') for d in trade_days[:20]]

print(f"测试日期: {len(test_dates)}天")
print(f"情绪阈值: 涨停≥10")

results = []
zt_counts = []

for i, date in enumerate(test_dates[:-1]):
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()[:200]
        df = get_price(all_stocks, end_date=date, count=1, 
                       fields=['close', 'high_limit'], panel=False)
        df = df.dropna()
        zt_df = df[df['close'] == df['high_limit']]
        zt_count = len(zt_df['code'])
        
        zt_counts.append({'date': date, 'zt_count': zt_count})
        
        print(f"{date}: 涨停{zt_count}家 - 阈值10{'✓触发' if zt_count >= 10 else '×未触发'}")
        
        if zt_count < 10:
            continue
        
        prev_date = test_dates[i-1] if i > 0 else None
        if not prev_date:
            continue
        
        prev_zt_df = get_price(all_stocks, end_date=prev_date, count=1, 
                               fields=['close', 'high_limit'], panel=False)
        prev_zt_df = prev_zt_df.dropna()
        prev_zt_stocks = list(prev_zt_df[prev_zt_df['close'] == prev_zt_df['high_limit']]['code'])
        
        zt_stocks = list(zt_df['code'])
        candidates = list(set(zt_stocks) & set(prev_zt_stocks))
        
        if len(candidates) == 0:
            continue
        
        test_stock = candidates[0]
        next_date = test_dates[i+1]
        
        next_prices = get_price(test_stock, end_date=next_date, count=1, 
                                fields=['open', 'close', 'high'], panel=False)
        
        if len(next_prices) > 0:
            buy_price = next_prices['open'].iloc[0] * 1.005
            sell_price = max(next_prices['high'].iloc[0], next_prices['close'].iloc[0])
            profit = (sell_price / buy_price - 1) * 100
            
            results.append({
                'date': next_date,
                'stock': test_stock,
                'profit': profit,
                'zt_count': zt_count
            })
            
            print(f"  → 找到: {test_stock}, 收益{profit:+.2f}%")
    
    except Exception as e:
        print(f"{date}: 错误 {e}")
        continue

print("\n" + "=" * 70)
print("涨停家数分布:")
print("=" * 70)

for item in zt_counts:
    print(f"{item['date']}: 涨停{item['zt_count']}家")

avg_zt = sum(item['zt_count'] for item in zt_counts) / len(zt_counts)
trigger_count = sum(1 for item in zt_counts if item['zt_count'] >= 10)
trigger_rate = trigger_count / len(zt_counts) * 100

print(f"\n平均涨停: {avg_zt:.1f}家")
print(f"阈值10触发率: {trigger_count}/{len(zt_counts)} = {trigger_rate:.1f}%")

print("\n" + "=" * 70)
print("策略结果:")
print("=" * 70)

if results:
    for r in results:
        print(f"{r['date']}: {r['stock']} 涨停{r['zt_count']}家 收益{r['profit']:+.2f}%")
    
    total = sum([r['profit'] for r in results])
    avg = total / len(results)
    win_rate = sum(1 for r in results if r['profit'] > 0) / len(results) * 100
    
    print(f"\n交易: {len(results)}笔")
    print(f"胜率: {win_rate:.1f}%")
    print(f"平均收益: {avg:.2f}%")
    print(f"累计收益: {total:.2f}%")
else:
    print("未找到交易机会")

print("\n=" * 70)
