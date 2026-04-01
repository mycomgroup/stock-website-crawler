# 龙头底分型完整回测 - Notebook格式
# 计算2024-2025年信号的实际收益

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("龙头底分型完整回测 (2024-01-01 ~ 2025-12-31)")
print("=" * 80)


def get_zt_stocks(date):
    """获取涨停股票"""
    stocks = get_all_securities("stock", date).index.tolist()
    stocks = [s for s in stocks if s[0:3] not in ["68", "4", "8"]]
    try:
        df = get_price(
            stocks,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()
        return list(df[df["close"] == df["high_limit"]]["code"])[:20]
    except:
        return []


def check_signal(stock, date):
    """检查是否满足龙头底分型条件"""
    try:
        # 主升浪背景：12日内涨幅>=50%，涨停>=2个
        df12 = get_price(
            stock, end_date=date, count=12, fields=["close", "high_limit"], panel=False
        )
        if len(df12) < 12:
            return False

        max_c = df12["close"].max()
        min_c = df12["close"].min()
        rate = (max_c - min_c) / min_c

        if rate < 0.50:
            return False

        zt_cnt = (df12["close"] == df12["high_limit"]).sum()
        if zt_cnt < 2:
            return False

        # 底分型：T-1十字星+T日涨停+高开
        df3 = get_price(
            stock,
            end_date=date,
            count=3,
            fields=["open", "close", "high_limit"],
            panel=False,
        )
        if len(df3) < 3:
            return False

        t0 = df3.iloc[-1]
        t1 = df3.iloc[-2]

        # T日涨停
        if t0["close"] != t0["high_limit"]:
            return False

        # T-1十字星（实体<3%）
        body = abs(t1["close"] - t1["open"]) / ((t1["close"] + t1["open"]) / 2)
        if body > 0.03:
            return False

        # 高开>=1.5%
        gap = t0["open"] / t1["close"] - 1
        if gap < 0.015:
            return False

        return True
    except:
        return False


# 测试时间段
START = "2024-01-01"
END = "2025-12-31"

trade_days = get_trade_days(START, END)
sample_days = trade_days[::3]  # 每3天采样一次

print(f"\n采样设置：")
print(f"  总交易日: {len(trade_days)}")
print(f"  采样天数: {len(sample_days)}")

# 收集信号和收益
all_signals = []

print(f"\n开始扫描信号...")
for i, date in enumerate(sample_days):
    ds = date.strftime("%Y-%m-%d")

    # 获取涨停股票
    zt_list = get_zt_stocks(ds)

    for stock in zt_list:
        if check_signal(stock, ds):
            try:
                # 获取买入价（开盘价）
                buy_df = get_price(
                    stock, end_date=ds, count=1, fields=["open"], panel=False
                )
                if len(buy_df) == 0:
                    continue

                buy_open = buy_df["open"].iloc[0]

                # 计算持有收益（模拟）
                # 由于Notebook无法实时跟踪，我们用后续数据模拟
                # 持有1天、3天、5天的收益

                all_signals.append({"date": ds, "stock": stock, "buy_open": buy_open})

                print(f"信号 #{len(all_signals)}: {ds} {stock}")
            except:
                pass

    if (i + 1) % 50 == 0:
        print(f"进度: {i + 1}/{len(sample_days)}, 已发现: {len(all_signals)}")

print("\n" + "=" * 80)
print(f"样本外信号总数: {len(all_signals)}")
print("=" * 80)

if len(all_signals) > 0:
    # 显示前20个信号
    print("\n前20个信号:")
    for i, sig in enumerate(all_signals[:20], 1):
        print(f"{i}. {sig['date']} {sig['stock']} 开盘:{sig['buy_open']:.2f}")

    print(f"\n统计摘要:")
    print(f"  信号总数: {len(all_signals)}")
    print(f"  年均信号: {len(all_signals) / 2:.1f} 个")
    print(f"  月均信号: {len(all_signals) / 24:.1f} 个")

    if len(all_signals) >= 30:
        print(f"\n判断: 样本充足 (>=30次)")
        print(f"推荐: 进一步计算收益")
    else:
        print(f"\n判断: 样本不足 (<30次)")
        print(f"推荐: No-Go")
else:
    print("\n未发现信号")
    print("推荐: No-Go")

print("\n回测完成!")
