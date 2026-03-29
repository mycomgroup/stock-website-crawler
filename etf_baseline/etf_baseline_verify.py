# ETF 候选池 + 动量基线验证
# 不叠加择时, 纯动量排序, 固定成本口径
# 运行环境: 聚宽 Research

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 70)
print("ETF 动量基线验证 (2020-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2020-01-01"
END = "2025-12-31"
COST = 0.001  # 单边万一手续费 + 滑点

# ---- 候选池定义 (v1.0) ----
ETF_POOL = {
    "沪深300ETF": "510300.XSHG",
    "中证500ETF": "510500.XSHG",
    "创业板ETF": "159915.XSHE",
    "科创50ETF": "588000.XSHG",
    "中证1000ETF": "512100.XSHG",
    "纳指ETF": "513100.XSHG",
    "标普500ETF": "513500.XSHG",
    "黄金ETF": "518880.XSHG",
    "国债ETF": "511010.XSHG",
    "医疗ETF": "512170.XSHG",
    "消费ETF": "159928.XSHE",
    "新能源ETF": "516160.XSHG",
}


def get_rebal_dates(start, end, freq_days):
    """按固定天数间隔取调仓日"""
    all_days = get_trade_days(start, end)
    result = [all_days[0]]
    for d in all_days[1:]:
        if (d - result[-1]).days >= freq_days:
            result.append(d)
    return result


def run_etf_version(mom_window, hold_days, label, top_n=3):
    """运行一个动量窗口 + 持有周期版本"""
    dates = get_rebal_dates(START, END, hold_days)
    codes = list(ETF_POOL.values())
    monthly_rets = []
    prev_holdings = []
    holding_records = []  # 记录每次持仓

    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i + 1])
        try:
            # 计算动量
            prices = get_price(
                codes,
                end_date=d_str,
                count=mom_window + 1,
                fields=["close"],
                panel=False,
            )
            pivot = prices.pivot(index="time", columns="code", values="close").dropna(
                axis=1
            )
            if len(pivot) < mom_window + 1:
                continue
            mom = pivot.iloc[-1] / pivot.iloc[0] - 1
            selected = mom.nlargest(top_n).index.tolist()

            # 记录持仓
            name_map = dict(zip(ETF_POOL.values(), ETF_POOL.keys()))
            holding_records.append(
                {
                    "date": d_str,
                    "holdings": [name_map.get(c, c) for c in selected],
                    "momentum": {
                        name_map.get(c, c): f"{v:+.2%}"
                        for c, v in mom[selected].items()
                    },
                }
            )

            # 计算持有收益
            p0 = get_price(
                selected, end_date=d_str, count=1, fields=["close"], panel=False
            )
            p1 = get_price(
                selected, end_date=next_d_str, count=1, fields=["close"], panel=False
            )
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            gross_ret = ((p1 / p0) - 1).mean()

            # 扣除换手成本
            turnover = len(set(selected) - set(prev_holdings)) / top_n
            net_ret = gross_ret - turnover * COST * 2
            monthly_rets.append(net_ret)
            prev_holdings = selected
        except Exception as e:
            continue

    if not monthly_rets:
        return None, None
    s = pd.Series(monthly_rets)
    cum = (1 + s).cumprod()
    periods_per_year = 252 / hold_days
    ann = cum.iloc[-1] ** (periods_per_year / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (periods_per_year**0.5) if s.std() > 0 else 0
    win = (s > 0).mean()
    total_turnover = sum(
        [
            len(set(h["holdings"]) - set(prev)) / top_n
            for h, prev in zip(
                holding_records[1:], [h["holdings"] for h in holding_records[:-1]]
            )
        ]
    )
    avg_turnover = total_turnover / len(holding_records) if holding_records else 0

    result = {
        "版本": label,
        "年化(扣费)": f"{ann:.1%}",
        "最大回撤": f"{dd:.1%}",
        "夏普": f"{sharpe:.2f}",
        "胜率": f"{win:.0%}",
        "样本数": len(s),
        "平均换手率": f"{avg_turnover:.1%}",
    }
    return result, holding_records


# 验证矩阵
configs = [
    (10, 5, "动量10d / 持有5d"),
    (10, 10, "动量10d / 持有10d"),
    (20, 10, "动量20d / 持有10d"),
    (20, 20, "动量20d / 持有20d"),
    (30, 10, "动量30d / 持有10d"),
    (30, 20, "动量30d / 持有20d"),
]

rows = []
all_records = {}
for mom_w, hold_d, label in configs:
    print(f"  运行: {label} ...")
    r, records = run_etf_version(mom_w, hold_d, label)
    if r:
        rows.append(r)
        all_records[label] = records
        print(f"    年化={r['年化(扣费)']}  回撤={r['最大回撤']}  夏普={r['夏普']}")

print("\n" + "=" * 70)
print("【ETF 基线对比汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("版本")
    print(df_res.to_string())

# 输出最近5期持仓记录 (推荐版本)
print("\n" + "=" * 70)
print("【推荐版本最近持仓记录: 动量20d / 持有10d】")
print("=" * 70)
if "动量20d / 持有10d" in all_records:
    for rec in all_records["动量20d / 持有10d"][-5:]:
        print(f"  {rec['date']}: {rec['holdings']}")
        print(f"    动量: {rec['momentum']}")

# 当前动量排名
print("\n" + "=" * 70)
print("【当前 ETF 动量排名 (20日)】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
codes = list(ETF_POOL.values())
names = list(ETF_POOL.keys())
prices = get_price(codes, end_date=str(today), count=21, fields=["close"], panel=False)
pivot = prices.pivot(index="time", columns="code", values="close").dropna(axis=1)
mom = (pivot.iloc[-1] / pivot.iloc[0] - 1).sort_values(ascending=False)
name_map = dict(zip(ETF_POOL.values(), ETF_POOL.keys()))
for code, val in mom.items():
    print(f"  {name_map.get(code, code)}: {val:+.2%}")
print("\n验证完成!")
