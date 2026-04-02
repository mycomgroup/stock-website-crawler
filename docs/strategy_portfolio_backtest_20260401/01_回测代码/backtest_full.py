# 完整回测代码（因超时未完成，仅供参考）
# 此代码会遍历所有交易日进行回测，数据量较大

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 70)
print("首批实跑组合 - 完整回测验证")
print("=" * 70)

# ============ 配置参数 ============
START_DATE = "2022-01-01"
END_DATE = "2025-12-31"
INITIAL_CAPITAL = 1000000

# ============ 1. RFScore7 + PB10% 策略回测 ============
print("\n【1. RFScore7 + PB10% 策略回测】")
print("-" * 50)


def calc_rfscore7(df):
    """计算RFScore7得分"""
    score = (
        (df["roe"] > 0).astype(int)
        + (df["roa"] > 0).astype(int)
        + (df["gross_profit_margin"] > df["gross_profit_margin"].median()).astype(int)
        + (df["net_profit_margin"] > 0).astype(int)
        + (df["inc_net_profit_year_on_year"] > 0).astype(int)
        + (df["inc_revenue_year_on_year"] > 0).astype(int)
        + (df["pe_ratio"] > 0).astype(int)
    )
    return score


def rfscore7_pb10_backtest(start_date, end_date, pb_percentile=0.10, hold_num=20):
    """RFScore7 + PB10% 回测"""
    # 获取交易日
    trade_days = get_trade_days(start_date, end_date)

    # 初始化
    portfolio_value = [INITIAL_CAPITAL]
    dates = [trade_days[0]]
    positions = {}

    # 月度调仓
    last_month = None

    for i, date in enumerate(trade_days):
        current_date = str(date)
        current_month = date.month

        # 月度调仓
        if last_month is None or current_month != last_month:
            try:
                # 获取中证800成分股
                stocks_300 = get_index_stocks("000300.XSHG", date=current_date)
                stocks_500 = get_index_stocks("000905.XSHG", date=current_date)
                universe = list(set(stocks_300 + stocks_500))

                # 获取财务数据
                q = query(
                    valuation.code,
                    indicator.roe,
                    indicator.roa,
                    indicator.gross_profit_margin,
                    indicator.net_profit_margin,
                    indicator.inc_net_profit_year_on_year,
                    indicator.inc_revenue_year_on_year,
                    valuation.pe_ratio,
                    valuation.pb_ratio,
                ).filter(valuation.code.in_(universe))

                df = get_fundamentals(q, date=current_date).set_index("code")
                df = df.dropna(subset=["roe", "pb_ratio", "roa"])

                # 过滤ST和负PE
                if len(df) > 0:
                    is_st = get_extras(
                        "is_st", df.index.tolist(), end_date=current_date, count=1
                    ).iloc[-1]
                    df = df[~is_st.reindex(df.index).fillna(True)]
                    df = df[df["pe_ratio"] > 0]

                if len(df) >= hold_num:
                    # 计算RFScore7
                    df["rfscore7"] = calc_rfscore7(df)

                    # PB分位数筛选
                    pb_thresh = df["pb_ratio"].quantile(pb_percentile)
                    candidates = df[df["pb_ratio"] <= pb_thresh]

                    # 选出得分最高的
                    if len(candidates) >= hold_num:
                        selected = candidates.nlargest(hold_num, "rfscore7")
                        new_positions = selected.index.tolist()
                    else:
                        selected = df.nlargest(hold_num, "rfscore7")
                        new_positions = selected.index.tolist()

                    positions = {
                        stock: 1.0 / len(new_positions) for stock in new_positions
                    }

            except Exception as e:
                pass

            last_month = current_month

        # 计算当日组合价值（省略具体实现）
        # ...

    return dates, portfolio_value


# 注意：此代码因超时未完成，仅供参考
print("注意：完整回测需要较长时间，建议使用简化版本")
print("=" * 70)
