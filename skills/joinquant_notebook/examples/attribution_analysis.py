"""
小市值因子 vs 事件策略归因分析 - Notebook版本
在 JoinQuant Notebook 中运行，避免策略编辑器的时间限制
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=== 小市值因子 vs 事件策略归因分析 ===")
print("回测期间: 2022-01-01 ~ 2025-03-30")

# 回测参数
start_date = "2022-01-01"
end_date = "2025-03-30"
initial_capital = 100000

# 获取交易日列表
trade_days = get_trade_days(start_date, end_date)
print(f"交易日总数: {len(trade_days)}")

# ============ 策略A: 纯小市值因子 ============
print("\n=== 策略A: 纯小市值因子 ===")


def strategy_a_pure_smallcap(date):
    """
    纯小市值因子：选市值最小的前10%
    """
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"
    ]

    # 过滤ST
    st_df = get_extras("is_st", all_stocks, start_date=date, end_date=date, df=True).T
    if not st_df.empty:
        st_df.columns = ["is_st"]
        all_stocks = list(st_df[st_df["is_st"] == False].index)

    # 查询市值
    q = (
        query(valuation.code, valuation.circulating_market_cap)
        .filter(valuation.code.in_(all_stocks), valuation.circulating_market_cap > 0)
        .order_by(valuation.circulating_market_cap.asc())
        .limit(300)
    )

    df = get_fundamentals(q, date=date)
    if df.empty:
        return []

    # 选最小的前10%，最多20只
    target_count = max(1, int(len(df) * 0.1))
    target = list(df["code"])[: min(target_count, 20)]

    return target


# 测试策略A（单日）
test_date_a = "2024-01-02"
stocks_a = strategy_a_pure_smallcap(test_date_a)
print(f"测试日期 {test_date_a}: 策略A选股 {len(stocks_a)} 只")

if stocks_a:
    # 查看选股详情
    q_detail = query(
        valuation.code,
        valuation.circulating_market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
    ).filter(valuation.code.in_(stocks_a[:5]))
    detail_a = get_fundamentals(q_detail, date=test_date_a)
    print("\n策略A前5只股票:")
    print(detail_a)

# ============ 策略B: 小市值 + 事件（首板低开） ============
print("\n=== 策略B: 小市值 + 事件（首板低开） ===")


def strategy_b_smallcap_event(prev_date, curr_date):
    """
    小市值+事件：市值5-15亿 + 首板 + 低开
    """
    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"
    ]

    # 过滤ST
    st_df = get_extras(
        "is_st", all_stocks, start_date=prev_date, end_date=prev_date, df=True
    ).T
    if not st_df.empty:
        st_df.columns = ["is_st"]
        all_stocks = list(st_df[st_df["is_st"] == False].index)

    # 市值限制：5-15亿
    q_cap = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.code.in_(all_stocks),
        valuation.circulating_market_cap >= 5,
        valuation.circulating_market_cap <= 15,
    )
    cap_df = get_fundamentals(q_cap, date=prev_date)
    if cap_df.empty:
        return []

    small_cap_stocks = list(cap_df["code"])

    # 首板识别：昨日涨停
    price_df = get_price(
        small_cap_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    if price_df.empty:
        return []

    price_df = price_df.dropna()
    limit_up_df = price_df[price_df["close"] == price_df["high_limit"]]
    first_board_stocks = list(limit_up_df["code"])

    if not first_board_stocks:
        return []

    # 今日低开判断：-3% ~ +1.5%
    current_data = get_price(
        first_board_stocks,
        end_date=curr_date,
        frequency="daily",
        fields=["open", "close"],
        count=1,
        panel=False,
    )

    if current_data.empty:
        return []

    # 计算开盘涨幅
    qualified = []
    for idx, row in current_data.iterrows():
        code = row["code"]
        curr_open = row["open"]
        prev_close = price_df[price_df["code"] == code]["close"].iloc[0]

        if pd.isna(curr_open) or pd.isna(prev_close) or prev_close <= 0:
            continue

        open_pct = (curr_open - prev_close) / prev_close * 100

        if -3.0 <= open_pct <= 1.5:
            qualified.append(code)

    return qualified[:1] if qualified else []


# 测试策略B（单日）
test_prev_date_b = "2024-01-02"
test_curr_date_b = "2024-01-03"
stocks_b = strategy_b_smallcap_event(test_prev_date_b, test_curr_date_b)
print(f"测试日期 {test_curr_date_b}: 策略B选股 {len(stocks_b)} 只")

if stocks_b:
    print(f"策略B选出: {stocks_b}")

# ============ 策略C: 纯事件（全市场首板低开） ============
print("\n=== 策略C: 纯事件（全市场首板低开） ===")


def strategy_c_pure_event(prev_date, curr_date):
    """
    纯事件：全市场首板 + 低开（不限制市值）
    """
    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"
    ]

    # 过滤ST
    st_df = get_extras(
        "is_st", all_stocks, start_date=prev_date, end_date=prev_date, df=True
    ).T
    if not st_df.empty:
        st_df.columns = ["is_st"]
        all_stocks = list(st_df[st_df["is_st"] == False].index)

    # 首板识别：昨日涨停
    price_df = get_price(
        all_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    if price_df.empty:
        return []

    price_df = price_df.dropna()
    limit_up_df = price_df[price_df["close"] == price_df["high_limit"]]
    first_board_stocks = list(limit_up_df["code"])

    if not first_board_stocks:
        return []

    # 今日低开判断：-3% ~ +1.5%
    current_data = get_price(
        first_board_stocks,
        end_date=curr_date,
        frequency="daily",
        fields=["open", "close"],
        count=1,
        panel=False,
    )

    if current_data.empty:
        return []

    # 计算开盘涨幅
    qualified = []
    for idx, row in current_data.iterrows():
        code = row["code"]
        curr_open = row["open"]
        prev_close = price_df[price_df["code"] == code]["close"].iloc[0]

        if pd.isna(curr_open) or pd.isna(prev_close) or prev_close <= 0:
            continue

        open_pct = (curr_open - prev_close) / prev_close * 100

        if -3.0 <= open_pct <= 1.5:
            qualified.append(code)

    return qualified[:1] if qualified else []


# 测试策略C（单日）
test_prev_date_c = "2024-01-02"
test_curr_date_c = "2024-01-03"
stocks_c = strategy_c_pure_event(test_prev_date_c, test_curr_date_c)
print(f"测试日期 {test_curr_date_c}: 策略C选股 {len(stocks_c)} 只")

if stocks_c:
    print(f"策略C选出: {stocks_c}")

# ============ 快速统计：信号数量对比 ============
print("\n=== 信号数量对比（2024年样本） ===")

# 统计策略A月度信号数
monthly_signals_a = {}
for date in trade_days[trade_days.index("2024-01-01") : trade_days.index("2024-12-31")]:
    month = date[:7]
    if month not in monthly_signals_a:
        monthly_signals_a[month] = []

    # 每月第一个交易日
    if len(monthly_signals_a[month]) == 0:
        try:
            stocks = strategy_a_pure_smallcap(date)
            monthly_signals_a[month] = stocks
            print(f"{month}: 策略A选股 {len(stocks)} 只")
        except Exception as e:
            print(f"{month}: 策略A查询失败 - {e}")

# 统计策略B和C的日度信号数（简化版本：只统计部分日期）
print("\n策略B和C信号统计（抽样2024年1月）:")
signal_count_b = 0
signal_count_c = 0

jan_days = trade_days[trade_days.index("2024-01-01") : trade_days.index("2024-02-01")]
for i in range(1, len(jan_days)):
    prev_date = jan_days[i - 1]
    curr_date = jan_days[i]

    try:
        stocks_b = strategy_b_smallcap_event(prev_date, curr_date)
        stocks_c = strategy_c_pure_event(prev_date, curr_date)

        if stocks_b:
            signal_count_b += 1
        if stocks_c:
            signal_count_c += 1
    except Exception as e:
        pass

print(f"2024年1月: 策略B信号 {signal_count_b} 个, 策略C信号 {signal_count_c} 个")

print("\n=== 归因分析完成 ===")
print("注意：这是简化的Notebook版本，主要用于验证选股逻辑")
print("完整回测需使用策略编辑器版本（attribution_a/b/c_*.py）")
