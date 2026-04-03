#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务07：2025年Q1样本外验证 - JoinQuant Notebook格式

目的：验证二板接力策略在2025年Q1的表现
参数：稳健优先方案（市值5-50亿，情绪涨停≥10）
基准：2024年实测（年化394%，胜率87.95%，回撤0.60%）

作者：AI量化研究助手
日期：2026-04-03
阶段：阶段4 - 最终验证
平台：JoinQuant Notebook
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务07：2025年Q1样本外验证")
print("=" * 80)
print("\n策略：二板接力策略（稳健优先方案）")
print("参数：市值5-50亿，情绪涨停≥10，缩量1.875，次日收盘卖出")
print("基准：2024年实测 年化394%，胜率87.95%，回撤0.60%")
print("时间：2025-01-01 至 2025-03-31（Q1）")
print("=" * 80)

# ============ 参数配置 ============
MARKET_CAP_LOWER = 5  # 市值下限（亿）
MARKET_CAP_UPPER = 50  # 市值上限（亿）
SENTIMENT_THRESHOLD = 10  # 情绪阈值（涨停家数）
VOLUME_RATIO = 1.875  # 缩量倍数
TURNOVER_LIMIT = 30  # 换手率上限（%）
SINGLE_POSITION_PCT = 5  # 单票仓位（%）

BACKTEST_START = "2025-01-01"
BACKTEST_END = "2025-03-31"

print(f"\n【参数配置】")
print(f"  市值范围：{MARKET_CAP_LOWER}-{MARKET_CAP_UPPER}亿")
print(f"  情绪阈值：涨停≥{SENTIMENT_THRESHOLD}")
print(f"  缩量倍数：{VOLUME_RATIO}")
print(f"  换手率上限：{TURNOVER_LIMIT}%")
print(f"  单票仓位：{SINGLE_POSITION_PCT}%")


# ============ 辅助函数 ============
def filter_kcbj_stock(initial_list):
    """过滤科创板和北交所"""
    return [
        stock
        for stock in initial_list
        if stock[0] not in ["4", "8"] and stock[:2] != "68"
    ]


def filter_new_stock(initial_list, date, days=250):
    """过滤新股"""
    d_date = pd.to_datetime(date).date()
    return [
        stock
        for stock in initial_list
        if d_date - get_security_info(stock).start_date > timedelta(days=days)
    ]


def filter_st_stock(initial_list, date):
    """过滤ST股票"""
    str_date = pd.to_datetime(date).strftime("%Y-%m-%d")
    try:
        df = get_extras(
            "is_st", initial_list, start_date=str_date, end_date=str_date, df=True
        )
        df = df.T
        df.columns = ["is_st"]
        df = df[df["is_st"] == False]
        return list(df.index)
    except:
        return initial_list


def filter_paused_stock(initial_list, date):
    """过滤停牌股票"""
    try:
        df = get_price(
            initial_list,
            end_date=date,
            frequency="daily",
            fields=["paused"],
            count=1,
            panel=False,
        )
        df = df[df["paused"] == 0]
        return list(df.code)
    except:
        return initial_list


def get_hl_stock(initial_list, date):
    """获取涨停股票"""
    date_str = pd.to_datetime(date).strftime("%Y-%m-%d")
    df = get_price(
        initial_list,
        end_date=date_str,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    return list(df.code)


def get_zt_count(date):
    """获取涨停家数"""
    date_str = pd.to_datetime(date).strftime("%Y-%m-%d")
    all_stocks = get_all_securities("stock", date_str).index.tolist()
    all_stocks = filter_kcbj_stock(all_stocks)
    all_stocks = filter_new_stock(all_stocks, date_str)
    all_stocks = filter_st_stock(all_stocks, date_str)
    all_stocks = filter_paused_stock(all_stocks, date_str)

    df = get_price(
        all_stocks,
        end_date=date_str,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    return len(df)


def prepare_stock_list(date):
    """准备股票池"""
    date_str = pd.to_datetime(date).strftime("%Y-%m-%d")
    initial_list = get_all_securities("stock", date_str).index.tolist()
    initial_list = filter_kcbj_stock(initial_list)
    initial_list = filter_new_stock(initial_list, date_str)
    initial_list = filter_st_stock(initial_list, date_str)
    initial_list = filter_paused_stock(initial_list, date_str)
    return initial_list


print("\n【辅助函数】已定义")


# ============ 核心选股逻辑 ============
def get_second_board_signals(date):
    """
    二板选股逻辑

    条件：
    1. 连续2日涨停（前日涨停+昨日涨停）
    2. 非一字板
    3. 换手率<30%
    4. 缩量条件：昨日量≤前日×1.875
    5. 市值排序：选择小市值
    """
    date_str = pd.to_datetime(date).strftime("%Y-%m-%d")

    # 前一个交易日
    all_trade_days = list(get_all_trade_days())
    date_idx = all_trade_days.index(pd.to_datetime(date_str).date())
    prev_date = all_trade_days[date_idx - 1]
    prev_date_str = prev_date.strftime("%Y-%m-%d")

    # 准备股票池
    all_stocks = prepare_stock_list(prev_date_str)

    # 前日涨停
    hl_prev = get_hl_stock(all_stocks, prev_date_str)

    # 昨日涨停
    hl_curr = get_hl_stock(all_stocks, date_str)

    # 二板股票（连续2日涨停）
    second_board = [s for s in hl_curr if s in hl_prev]

    if len(second_board) == 0:
        return []

    # 1. 非一字板过滤
    df = get_price(
        second_board,
        end_date=date_str,
        frequency="daily",
        fields=["low", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    df = df[df["low"] < df["high_limit"]]  # 非一字板
    second_board = list(df.code)

    if len(second_board) == 0:
        return []

    # 2. 换手率过滤
    q = query(valuation.code, valuation.turnover_ratio).filter(
        valuation.code.in_(second_board)
    )
    df_turnover = get_fundamentals(q, date=date_str)
    df_turnover = df_turnover.dropna()
    df_turnover = df_turnover[df_turnover["turnover_ratio"] < TURNOVER_LIMIT]
    second_board = list(df_turnover["code"])

    if len(second_board) == 0:
        return []

    # 3. 缩量条件
    df_volume = get_price(
        second_board,
        end_date=date_str,
        frequency="daily",
        fields=["volume"],
        count=2,
        panel=False,
    )

    volume_filtered = []
    for stock in second_board:
        stock_data = df_volume[df_volume["code"] == stock]
        if len(stock_data) == 2:
            vol_prev = stock_data.iloc[0]["volume"]  # 前日成交量
            vol_curr = stock_data.iloc[1]["volume"]  # 昨日成交量
            if vol_curr <= vol_prev * VOLUME_RATIO:
                volume_filtered.append(stock)

    second_board = volume_filtered

    if len(second_board) == 0:
        return []

    # 4. 市值排序（选择小市值）
    q = query(valuation.code, valuation.market_cap).filter(
        valuation.code.in_(second_board)
    )
    df_cap = get_fundamentals(q, date=date_str)
    df_cap = df_cap.dropna()
    df_cap["market_cap_yi"] = df_cap["market_cap"]  # 已经是亿元单位

    # 市值范围过滤
    df_cap = df_cap[
        (df_cap["market_cap_yi"] >= MARKET_CAP_LOWER)
        & (df_cap["market_cap_yi"] <= MARKET_CAP_UPPER)
    ]

    # 按市值排序
    df_cap = df_cap.sort_values("market_cap_yi", ascending=True)

    second_board_final = list(df_cap["code"])

    return second_board_final


print("\n【选股逻辑】已定义")

# ============ 回测主逻辑 ============
print("\n" + "=" * 80)
print("开始回测...")
print("=" * 80)

try:
    # 获取交易日
    trade_days = get_trade_days(start_date=BACKTEST_START, end_date=BACKTEST_END)
    trade_days = [d.strftime("%Y-%m-%d") for d in trade_days]

    print(f"\n【时间范围】")
    print(f"  开始日期：{BACKTEST_START}")
    print(f"  结束日期：{BACKTEST_END}")
    print(f"  总交易日：{len(trade_days)} 天")

    # 初始化
    INITIAL_CAPITAL = 1000000  # 初始资金100万
    capital = INITIAL_CAPITAL
    positions = {}  # 持仓 {stock: {'buy_date': date, 'buy_price': price, 'volume': volume}}
    trade_records = []  # 交易记录
    daily_nav = []  # 每日净值

    print(f"\n【初始资金】{INITIAL_CAPITAL:,.0f} 元")

    # 回测循环
    for i, date in enumerate(trade_days):
        if i == 0:
            continue

        prev_date = trade_days[i - 1]

        # 情绪过滤
        zt_count = get_zt_count(prev_date)

        if i % 10 == 0:  # 每10天输出一次
            print(f"\n  [{date}] 涨停家数：{zt_count}")

        # 情绪阈值判断
        if zt_count < SENTIMENT_THRESHOLD:
            # 卖出持仓
            if positions:
                for stock in list(positions.keys()):
                    pos = positions[stock]
                    # 获取当日收盘价
                    df_sell = get_price(
                        stock,
                        end_date=date,
                        frequency="daily",
                        fields=["close"],
                        count=1,
                        panel=False,
                    )
                    if len(df_sell) > 0:
                        sell_price = df_sell.iloc[0]["close"]
                        sell_amount = sell_price * pos["volume"]
                        capital += sell_amount

                        # 计算收益
                        profit = sell_amount - pos["buy_amount"]
                        profit_pct = profit / pos["buy_amount"] * 100

                        trade_records.append(
                            {
                                "stock": stock,
                                "buy_date": pos["buy_date"],
                                "sell_date": date,
                                "buy_price": pos["buy_price"],
                                "sell_price": sell_price,
                                "profit_pct": profit_pct,
                            }
                        )

                        del positions[stock]

            daily_nav.append({"date": date, "nav": capital, "positions": 0})
            continue

        # 卖出昨日持仓（次日收盘卖出）
        if positions:
            for stock in list(positions.keys()):
                pos = positions[stock]
                # 获取当日收盘价
                df_sell = get_price(
                    stock,
                    end_date=date,
                    frequency="daily",
                    fields=["close"],
                    count=1,
                    panel=False,
                )
                if len(df_sell) > 0:
                    sell_price = df_sell.iloc[0]["close"]
                    sell_amount = sell_price * pos["volume"]
                    capital += sell_amount

                    # 计算收益
                    profit = sell_amount - pos["buy_amount"]
                    profit_pct = profit / pos["buy_amount"] * 100

                    trade_records.append(
                        {
                            "stock": stock,
                            "buy_date": pos["buy_date"],
                            "sell_date": date,
                            "buy_price": pos["buy_price"],
                            "sell_price": sell_price,
                            "profit_pct": profit_pct,
                        }
                    )

                    del positions[stock]

        # 选股
        signals = get_second_board_signals(prev_date)

        # 买入
        if signals:
            # 选择市值最小的1只
            buy_stock = signals[0]

            # 检查是否涨停开盘
            df_open = get_price(
                buy_stock,
                end_date=date,
                frequency="daily",
                fields=["open", "high_limit"],
                count=1,
                panel=False,
            )
            if len(df_open) > 0:
                open_price = df_open.iloc[0]["open"]
                high_limit = df_open.iloc[0]["high_limit"]

                # 非涨停开盘买入
                if open_price < high_limit:
                    buy_amount = capital * SINGLE_POSITION_PCT / 100
                    volume = int(buy_amount / open_price / 100) * 100  # 整手数

                    if volume > 0:
                        actual_buy_amount = open_price * volume
                        capital -= actual_buy_amount

                        positions[buy_stock] = {
                            "buy_date": date,
                            "buy_price": open_price,
                            "volume": volume,
                            "buy_amount": actual_buy_amount,
                        }

        # 记录每日净值
        total_value = capital
        for stock, pos in positions.items():
            df_price = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["close"],
                count=1,
                panel=False,
            )
            if len(df_price) > 0:
                total_value += df_price.iloc[0]["close"] * pos["volume"]

        daily_nav.append(
            {"date": date, "nav": total_value, "positions": len(positions)}
        )

    # ============ 统计结果 ============
    print("\n" + "=" * 80)
    print("回测完成！统计结果...")
    print("=" * 80)

    # 计算风险指标
    nav_df = pd.DataFrame(daily_nav)
    nav_df["return"] = nav_df["nav"].pct_change()

    # 累计收益
    total_return = (nav_df.iloc[-1]["nav"] / INITIAL_CAPITAL - 1) * 100

    # 年化收益
    days = len(nav_df)
    annual_return = (nav_df.iloc[-1]["nav"] / INITIAL_CAPITAL) ** (252 / days) - 1
    annual_return_pct = annual_return * 100

    # 最大回撤
    nav_df["cummax"] = nav_df["nav"].cummax()
    nav_df["drawdown"] = (nav_df["nav"] - nav_df["cummax"]) / nav_df["cummax"]
    max_drawdown = nav_df["drawdown"].min() * 100

    # 胜率
    win_trades = [t for t in trade_records if t["profit_pct"] > 0]
    lose_trades = [t for t in trade_records if t["profit_pct"] <= 0]
    win_rate = len(win_trades) / len(trade_records) * 100 if trade_records else 0

    # 平均收益
    avg_profit = (
        np.mean([t["profit_pct"] for t in trade_records]) if trade_records else 0
    )

    # 夏普比率
    sharpe = (
        nav_df["return"].mean() / nav_df["return"].std() * np.sqrt(252)
        if nav_df["return"].std() > 0
        else 0
    )

    # 输出结果
    print("\n【2025年Q1实测结果】")
    print("=" * 60)
    print(f"  交易次数：{len(trade_records)} 次")
    print(f"  胜率：{win_rate:.2f}%")
    print(f"  平均单笔收益：{avg_profit:.2f}%")
    print(f"  累计收益：{total_return:.2f}%")
    print(f"  年化收益：{annual_return_pct:.2f}%")
    print(f"  最大回撤：{max_drawdown:.2f}%")
    print(f"  夏普比率：{sharpe:.2f}")
    print("=" * 60)

    # 对比基准
    print("\n【对比基准（2024年实测）】")
    print("=" * 60)
    print("  年化收益：394%")
    print("  胜率：87.95%")
    print("  最大回撤：0.60%")
    print("=" * 60)

    # Go/Watch/No-Go判断
    print("\n【Go/Watch/No-Go判断】")
    print("=" * 60)

    if annual_return_pct > 200 and win_rate > 80 and max_drawdown < 15:
        judgment = "✅ Go"
        reason = "策略在2025年Q1表现优秀，参数稳健，可进入实盘准备"
    elif annual_return_pct > 100 and win_rate > 70 and max_drawdown < 25:
        judgment = "⚠️ Watch"
        reason = "策略在2025年Q1表现一般，需要进一步观察和优化"
    else:
        judgment = "❌ No-Go"
        reason = "策略在2025年Q1表现不佳，建议暂停或重新评估"

    print(f"  判断：{judgment}")
    print(f"  理由：{reason}")
    print("=" * 60)

    # 保存结果
    result = {
        "test_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platform": "JoinQuant Notebook",
        "test_period": f"{BACKTEST_START} to {BACKTEST_END}",
        "params": {
            "market_cap_range": f"{MARKET_CAP_LOWER}-{MARKET_CAP_UPPER}亿",
            "sentiment_threshold": SENTIMENT_THRESHOLD,
            "volume_ratio": VOLUME_RATIO,
            "turnover_limit": TURNOVER_LIMIT,
            "single_position_pct": SINGLE_POSITION_PCT,
        },
        "results": {
            "trade_count": len(trade_records),
            "win_rate": round(win_rate, 2),
            "avg_profit": round(avg_profit, 2),
            "total_return": round(total_return, 2),
            "annual_return": round(annual_return_pct, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe, 2),
        },
        "benchmark": {"annual_return": 394, "win_rate": 87.95, "max_drawdown": 0.60},
        "judgment": judgment,
        "reason": reason,
    }

    # 输出JSON
    print("\n【JSON结果】")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 保存到文件
    output_file = "/Users/fengzhi/Downloads/git/testlixingren/output/task07_2025q1_validation_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 结果已保存到：{output_file}")

except Exception as e:
    print(f"\n❌ 错误：{e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("回测结束")
print("=" * 80)
