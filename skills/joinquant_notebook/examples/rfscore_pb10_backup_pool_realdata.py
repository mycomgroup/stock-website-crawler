"""
RFScore PB10 备用池机制验证 - 真实数据 Notebook 版本
测试不同备用池策略和持仓数在真实市场数据下的表现

回测期间：2023-01 到 2025-03
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
import json

print("=" * 80)
print("RFScore PB10 备用池机制验证 - 真实数据测试")
print("=" * 80)

# ========== 配置参数 ==========
START_DATE = "2023-01-01"
END_DATE = "2025-03-26"
IPO_DAYS = 180

# 测试的持仓数配置
HOLD_NUMS = [10, 15, 20]


# ========== RFScore Factor 定义 ==========
def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
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


# ========== 辅助函数 ==========
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
    """获取股票池"""
    hs300 = set(get_index_stocks("000300.XSHG", date=date))
    zz500 = set(get_index_stocks("000905.XSHG", date=date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= date - pd.Timedelta(days=IPO_DAYS)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(stocks, end_date=date, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def calc_rfscore_frame(stocks, date):
    """计算RFScore数据框"""
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=date, end_date=date)

    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    val = get_valuation(stocks, end_date=date, fields=["pb_ratio", "pe_ratio"], count=1)
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]

    df = df.join(val, how="left")
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])

    # PB分组 (10组)
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    return df


def calc_market_state(date):
    """计算市场状态"""
    hs300 = get_index_stocks("000300.XSHG", date=date)
    prices = get_price(hs300, end_date=date, count=20, fields=["close"], panel=False)
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=date, count=20, fields=["close"])
    trend_on = float(idx["close"].iloc[-1]) > float(idx["close"].mean())

    return breadth, trend_on


def get_forward_return(stocks, start_date, end_date):
    """获取下期收益"""
    if not stocks:
        return 0.0
    try:
        px0 = get_price(
            stocks, end_date=start_date, count=1, fields=["close"], panel=False
        )
        px1 = get_price(
            stocks, end_date=end_date, count=1, fields=["close"], panel=False
        )
        px0 = px0.pivot(index="time", columns="code", values="close").iloc[-1]
        px1 = px1.pivot(index="time", columns="code", values="close").iloc[-1]
        ret = (px1 / px0 - 1).dropna()
        return float(ret.mean()) if len(ret) > 0 else 0.0
    except:
        return 0.0


# ========== 选股策略 ==========
def pick_strategy(df, strategy, hold_num):
    """
    根据不同的备用池策略选股
    """
    picks = []
    fill_sources = []

    if strategy == "pb10_strict":
        # 策略1: 仅PB10% (最严格)
        candidates = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()
        candidates = candidates.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        picks = candidates.index.tolist()[:hold_num]
        fill_sources = ["pb10_only"]

    elif strategy == "pb10_backup_score6":
        # 策略2: PB10% + RFScore>=6 补位
        primary = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()
        primary = primary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        picks = primary.index.tolist()
        fill_sources.append(f"pb10:{len(picks)}")

        if len(picks) < hold_num:
            backup = df[df["RFScore"] >= 6].copy()
            backup = backup.sort_values(
                ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
                ascending=[False, False, False, False, False, True],
            )
            for code in backup.index.tolist():
                if code not in picks:
                    picks.append(code)
                if len(picks) >= hold_num:
                    break
            fill_sources.append(f"score6:{len(picks) - len(primary)}")

    elif strategy == "pb10_backup_pb20":
        # 策略3: PB10% + PB20% (RFScore=7) 补位
        primary = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()
        primary = primary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        picks = primary.index.tolist()
        fill_sources.append(f"pb10:{len(picks)}")

        if len(picks) < hold_num:
            backup = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2)].copy()
            backup = backup.sort_values(
                ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
                ascending=[False, False, False, False, False, True],
            )
            for code in backup.index.tolist():
                if code not in picks:
                    picks.append(code)
                if len(picks) >= hold_num:
                    break
            fill_sources.append(f"pb20:{len(picks) - len(primary)}")

    elif strategy == "pb20_strict":
        # 策略4: 仅PB20% (对照组)
        candidates = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2)].copy()
        candidates = candidates.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        picks = candidates.index.tolist()[:hold_num]
        fill_sources = ["pb20_only"]

    return picks[:hold_num], "+".join(fill_sources)


# ========== 主程序 ==========
print(f"\n测试期间: {START_DATE} 至 {END_DATE}")

# 获取调仓日期
dates = get_monthly_dates(START_DATE, END_DATE)
print(f"调仓次数: {len(dates) - 1} 次")

# 初始化结果存储
strategies = ["pb10_strict", "pb10_backup_score6", "pb10_backup_pb20", "pb20_strict"]
results = {}
candidate_counts = {}

for hold_num in HOLD_NUMS:
    for strategy in strategies:
        key = f"{strategy}_h{hold_num}"
        results[key] = []
        candidate_counts[key] = []

# 主循环
print("\n开始回测...")
for i in range(len(dates) - 1):
    date = dates[i]
    next_date = dates[i + 1]
    date_str = str(date)
    next_date_str = str(next_date)

    # 市场状态
    breadth, trend_on = calc_market_state(date_str)

    # 获取股票池
    stocks = get_universe(date)

    # 计算RFScore
    df = calc_rfscore_frame(stocks, date_str)

    # 统计基础数据
    pb10_count = len(df[(df["RFScore"] == 7) & (df["pb_group"] == 1)])
    pb20_count = len(df[(df["RFScore"] == 7) & (df["pb_group"] <= 2)])
    score6_count = len(df[df["RFScore"] >= 6])

    print(
        f"\n[{i + 1}/{len(dates) - 1}] {date_str} | 宽度:{breadth:.3f} | 股票池:{len(stocks)} | PB10:{pb10_count} | PB20:{pb20_count}"
    )

    # 测试不同策略和持仓数
    for hold_num in HOLD_NUMS:
        for strategy in strategies:
            key = f"{strategy}_h{hold_num}"
            picks, fill_info = pick_strategy(df, strategy, hold_num)

            # 记录候选数量
            candidate_counts[key].append(
                {
                    "date": date_str,
                    "pb10": pb10_count,
                    "pb20": pb20_count,
                    "score6": score6_count,
                    "actual": len(picks),
                    "fill_info": fill_info,
                }
            )

            # 计算收益
            period_return = get_forward_return(picks, date_str, next_date_str)
            results[key].append(period_return)

            if i < 3:  # 只打印前3期的详情
                print(
                    f"  {key}: 选股{len(picks)}只 | 来源:{fill_info} | 收益:{period_return:.2%}"
                )

# 汇总统计
print("\n" + "=" * 80)
print("汇总结果")
print("=" * 80)


def summarize(name, rets):
    ser = pd.Series(rets)
    nav = (1 + ser).cumprod()
    dd = (nav / nav.cummax() - 1).min()
    cum = nav.iloc[-1] - 1
    ann = (1 + cum) ** (12 / len(ser)) - 1
    return {
        "cum_return": round(float(cum), 4),
        "ann_return": round(float(ann), 4),
        "win_rate": round(float((ser > 0).mean()), 4),
        "max_dd": round(float(dd), 4),
        "mean_return": round(float(ser.mean()), 4),
        "count": len(ser),
    }


summary = {}
for name, rets in results.items():
    summary[name] = summarize(name, rets)

# 按持仓数分组显示
for hold_num in HOLD_NUMS:
    print(f"\n【持仓数: {hold_num}只】")
    print("-" * 80)
    print(
        f"{'策略':<25} {'累计收益':<12} {'年化收益':<12} {'胜率':<10} {'最大回撤':<12} {'月均收益':<10}"
    )
    print("-" * 80)

    for strategy in strategies:
        key = f"{strategy}_h{hold_num}"
        s = summary[key]
        strategy_name = {
            "pb10_strict": "仅PB10% (无补位)",
            "pb10_backup_score6": "PB10%+Score>=6补位",
            "pb10_backup_pb20": "PB10%+PB20%补位",
            "pb20_strict": "仅PB20% (对照)",
        }[strategy]
        print(
            f"{strategy_name:<25} {s['cum_return']:<12.2%} {s['ann_return']:<12.2%} {s['win_rate']:<10.1%} {s['max_dd']:<12.2%} {s['mean_return']:<10.2%}"
        )

# 候选数量分布分析
print("\n" + "=" * 80)
print("候选数量分布分析")
print("=" * 80)

for hold_num in HOLD_NUMS:
    print(f"\n【持仓数: {hold_num}只】")

    for strategy in strategies:
        key = f"{strategy}_h{hold_num}"
        counts = candidate_counts[key]

        # 统计各月候选数量
        pb10_counts = [c["pb10"] for c in counts]
        actual_counts = [c["actual"] for c in counts]

        # 统计补位情况
        fill_needed = sum(1 for c in counts if c["actual"] < hold_num)

        strategy_short = {
            "pb10_strict": "PB10严格",
            "pb10_backup_score6": "PB10+Score6",
            "pb10_backup_pb20": "PB10+PB20",
            "pb20_strict": "PB20严格",
        }[strategy]

        print(
            f"  {strategy_short}: PB10平均{np.mean(pb10_counts):.1f}只 | 需补位{fill_needed}/{len(counts)}次 ({fill_needed / len(counts) * 100:.0f}%)"
        )

print("\n" + "=" * 80)
print("分析完成!")
print("=" * 80)

# 输出JSON格式的结果
print("\n【JSON格式结果】")
output = {
    "summary": summary,
    "test_config": {
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hold_nums": HOLD_NUMS,
        "strategies": strategies,
    },
}
print(json.dumps(output, indent=2, default=str))
