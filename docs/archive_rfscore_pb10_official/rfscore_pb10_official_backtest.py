#!/usr/bin/env python3
"""
RFScore PB10 正式基线 - Notebook 回测

测试期间: 2023-01-01 至 2025-12-31
股票池: 中证800
调仓频率: 月度
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("RFScore PB10 正式基线 - Notebook 回测")
print("测试期间: 2023-01-01 至 2025-12-31")
print("=" * 80)


# ==================== 参数配置 ====================
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"
HOLD_NUM = 20
IPO_DAYS = 180


def sign(ser):
    """符号函数：正数为1，其他为0"""
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    """RFScore7 因子计算"""

    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa",
        "roa_4",
        "net_operate_cash_flow",
        "net_operate_cash_flow_1",
        "net_operate_cash_flow_2",
        "net_operate_cash_flow_3",
        "total_assets",
        "total_assets_1",
        "total_assets_2",
        "total_assets_3",
        "total_assets_4",
        "total_assets_5",
        "total_non_current_liability",
        "total_non_current_liability_1",
        "gross_profit_margin",
        "gross_profit_margin_4",
        "operating_revenue",
        "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1

        cfo_sum = (
            data["net_operate_cash_flow"]
            + data["net_operate_cash_flow_1"]
            + data["net_operate_cash_flow_2"]
            + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (
            data["total_assets"]
            + data["total_assets_1"]
            + data["total_assets_2"]
            + data["total_assets_3"]
        ) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01

        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)

        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1

        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = turnover / turnover_1 - 1

        indicator_tuple = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


def get_monthly_dates(start_date, end_date):
    """获取月度调仓日期"""
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    dates = []
    current_month = None
    for day in trade_days:
        if day.month != current_month:
            dates.append(day)
            current_month = day.month
    return dates


def get_universe(date):
    """获取股票池（中证800）"""
    hs300 = set(get_index_stocks("000300.XSHG", date=date))
    zz500 = set(get_index_stocks("000905.XSHG", date=date))
    stocks = list(hs300 | zz500)

    # 过滤科创板
    stocks = [s for s in stocks if not s.startswith("688")]

    # 过滤新股
    sec = get_all_securities(types=["stock"], date=date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= date - pd.Timedelta(days=IPO_DAYS)]
    stocks = sec.index.tolist()

    # 过滤ST
    is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    # 过滤停牌
    paused = get_price(stocks, end_date=date, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def calc_market_state(date):
    """计算市场宽度"""
    hs300 = get_index_stocks("000300.XSHG", date=date)
    prices = get_price(hs300, end_date=date, count=20, fields=["close"], panel=False)
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=date, count=20, fields=["close"])
    trend_on = float(idx["close"].iloc[-1]) > float(idx["close"].mean())

    return breadth, trend_on


def calc_rfscore_frame(stocks, date):
    """计算 RFScore 和估值数据"""
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=date, end_date=date)

    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    val = get_valuation(stocks, end_date=date, fields=["pb_ratio", "pe_ratio"], count=1)
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    df = df.join(val, how="left")

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])

    # PB 分组 (10组)
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    return df


def pick_stocks_pb10(df, hold_num):
    """PB10 选股逻辑"""
    # 主选：RFScore=7 且 PB<=10%
    primary = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )
    picks = primary.index.tolist()

    # 次选：RFScore>=6 且 PB<=20%
    if len(picks) < hold_num:
        secondary = df[(df["RFScore"] >= 6) & (df["pb_group"] <= 2)].copy()
        secondary = secondary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break

    return picks[:hold_num]


def get_forward_return(stocks, start_date, end_date):
    """计算下期收益"""
    if not stocks:
        return 0.0
    px0 = get_price(stocks, end_date=start_date, count=1, fields=["close"], panel=False)
    px1 = get_price(stocks, end_date=end_date, count=1, fields=["close"], panel=False)
    px0 = px0.pivot(index="time", columns="code", values="close").iloc[-1]
    px1 = px1.pivot(index="time", columns="code", values="close").iloc[-1]
    ret = (px1 / px0 - 1).dropna()
    if len(ret) == 0:
        return 0.0
    return float(ret.mean())


def summarize(name, rets, counts):
    """汇总统计"""
    ser = pd.Series(rets)
    nav = (1 + ser).cumprod()
    dd = (nav / nav.cummax() - 1).min()
    cum = nav.iloc[-1] - 1
    ann = (1 + cum) ** (12 / len(ser)) - 1
    avg_count = np.mean(counts) if counts else 0

    print(f"\n{name}:")
    print(f"  累计收益: {cum:.2%}")
    print(f"  年化收益: {ann:.2%}")
    print(f"  最大回撤: {dd:.2%}")
    print(
        f"  夏普比率: {ann / (ser.std() * np.sqrt(12)):.2f}"
        if ser.std() > 0
        else "  夏普比率: N/A"
    )
    print(f"  月胜率: {(ser > 0).mean():.1%}")
    print(f"  平均持仓: {avg_count:.1f} 只")
    print(f"  调仓次数: {len(ser)}")

    return {
        "name": name,
        "cum_return": cum,
        "ann_return": ann,
        "max_dd": dd,
        "sharpe": ann / (ser.std() * np.sqrt(12)) if ser.std() > 0 else 0,
        "win_rate": (ser > 0).mean(),
        "avg_count": avg_count,
    }


# ==================== 主程序 ====================
print("\n开始回测...")

dates = get_monthly_dates(START_DATE, END_DATE)
print(f"月度调仓次数: {len(dates) - 1}")

results = []
stock_counts = []
market_states = []

for i in range(len(dates) - 1):
    date = pd.Timestamp(dates[i]).date()
    next_date = pd.Timestamp(dates[i + 1]).date()
    date_str = str(date)
    next_date_str = str(next_date)

    # 市场状态
    breadth, trend_on = calc_market_state(date_str)
    market_states.append({"date": date_str, "breadth": breadth, "trend_on": trend_on})

    # 选股
    stocks = get_universe(date)
    if len(stocks) == 0:
        results.append(0.0)
        stock_counts.append(0)
        continue

    df = calc_rfscore_frame(stocks, date_str)
    selected = pick_stocks_pb10(df, HOLD_NUM)

    # 计算收益
    period_return = get_forward_return(selected, date_str, next_date_str)
    results.append(period_return)
    stock_counts.append(len(selected))

    if i % 6 == 0:
        print(
            f"进度: {i}/{len(dates) - 1} ({i / (len(dates) - 1) * 100:.1f}%) - {date_str}"
        )

# ==================== 结果汇总 ====================
print("\n" + "=" * 80)
print("回测结果汇总")
print("=" * 80)

summary = summarize("RFScore PB10", results, stock_counts)

# 保存详细结果
result_data = {
    "strategy": "RFScore PB10",
    "start_date": START_DATE,
    "end_date": END_DATE,
    "summary": summary,
    "monthly_returns": results,
    "stock_counts": stock_counts,
    "market_states": market_states,
}

print("\n" + "=" * 80)
print("回测完成!")
print("=" * 80)

# 输出结果供外部解析
print("\n【RESULT_JSON_START】")
print(json.dumps(result_data, indent=2, default=str))
print("【RESULT_JSON_END】")
