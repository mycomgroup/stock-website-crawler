#!/usr/bin/env python3
"""
RFScore PB10 过滤器终审回测 - 简化可靠版
测试期间: 2022-01-01 至 2025-03-31
"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("RFScore PB10 过滤器终审回测")
print("=" * 80)

# 参数
START_DATE = "2022-01-01"
END_DATE = "2025-03-31"
HOLD_NUM = 20
IPO_DAYS = 180


def get_monthly_dates(start_date, end_date):
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    dates = []
    current_month = None
    for day in trade_days:
        if day.month != current_month:
            dates.append(day)
            current_month = day.month
    return dates


def get_universe(date):
    hs300 = set(get_index_stocks("000300.XSHG", date=date))
    zz500 = set(get_index_stocks("000905.XSHG", date=date))
    stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]

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


def calc_rfscore_simple(stocks, date):
    """简化版RFScore计算"""
    q = query(valuation.code, valuation.pb_ratio, indicator.roa, indicator.roe).filter(
        valuation.code.in_(stocks)
    )

    df = get_fundamentals(q, date=date)
    df = df.set_index("code")
    df = df.dropna()

    # 简化：使用ROA>0作为代理
    df["RFScore"] = (df["roa"] > 0).astype(int)

    # PB分组
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    return df


def calc_turnover(stocks, date):
    df = get_price(stocks, end_date=date, count=20, fields=["money"], panel=False)
    if df.empty:
        return pd.Series(dtype=float)
    avg_money = df.pivot(index="time", columns="code", values="money").mean()
    cap = get_valuation(
        stocks, end_date=date, fields=["circulating_market_cap"], count=1
    )
    cap = cap.drop_duplicates("code").set_index("code")["circulating_market_cap"]
    return avg_money / (cap * 1e8 + 1)


def calc_cgo(stocks, date, lookback=60):
    """简化版CGO - 使用60日"""
    prices = get_price(
        stocks, end_date=date, count=lookback, fields=["close"], panel=False
    )
    if prices.empty:
        return pd.Series(dtype=float)
    close = prices.pivot(index="time", columns="code", values="close")
    return (close.iloc[-1] - close.mean()) / (close.iloc[-1] + 1e-10)


def get_industry_map(stocks, date):
    industry = get_industry(stocks, date=date)
    return {
        s: industry.get(s, {}).get("sw_l1", {}).get("industry_name", "Unknown")
        for s in stocks
    }


def select_stocks(df, variant, turnover=None, cgo=None, industry_map=None):
    """选股逻辑"""
    # 基础筛选: ROA>0 + PB最低组
    base = df[(df["RFScore"] > 0) & (df["pb_group"] == 1)]

    if variant == "baseline":
        return base.index.tolist()[:HOLD_NUM]

    elif variant == "turnover" and turnover is not None:
        base = base.join(turnover.rename("turnover"), how="left")
        threshold = base["turnover"].quantile(0.8) if len(base) > 0 else 0
        filtered = base[base["turnover"] < threshold]
        return filtered.index.tolist()[:HOLD_NUM]

    elif variant == "cgo" and cgo is not None:
        base = base.join(cgo.rename("cgo"), how="left")
        threshold = base["cgo"].quantile(0.8) if len(base) > 0 else 0
        filtered = base[base["cgo"] < threshold]
        return filtered.index.tolist()[:HOLD_NUM]

    elif variant == "combined" and turnover is not None and cgo is not None:
        base = base.join(turnover.rename("turnover"), how="left").join(
            cgo.rename("cgo"), how="left"
        )
        t_threshold = base["turnover"].quantile(0.8) if len(base) > 0 else 0
        c_threshold = base["cgo"].quantile(0.8) if len(base) > 0 else 0
        filtered = base[(base["turnover"] < t_threshold) & (base["cgo"] < c_threshold)]
        return filtered.index.tolist()[:HOLD_NUM]

    elif variant == "industry_cap" and industry_map is not None:
        stocks = base.index.tolist()
        industry_count = {}
        result = []
        for stock in stocks:
            ind = industry_map.get(stock, "Unknown")
            if industry_count.get(ind, 0) < 5:
                result.append(stock)
                industry_count[ind] = industry_count.get(ind, 0) + 1
            if len(result) >= HOLD_NUM:
                break
        return result

    return base.index.tolist()[:HOLD_NUM]


def calc_return(stocks, start_date, end_date):
    if not stocks:
        return 0.0
    try:
        p1 = get_price(
            stocks, end_date=start_date, count=1, fields=["close"], panel=False
        )
        p2 = get_price(
            stocks, end_date=end_date, count=1, fields=["close"], panel=False
        )
        ret = (p2["close"].values / p1["close"].values - 1).mean()
        return float(ret)
    except:
        return 0.0


def calc_metrics(returns):
    if not returns:
        return {"cum": 0, "ann": 0, "mdd": 0, "sharpe": 0}

    ser = pd.Series(returns)
    nav = (1 + ser).cumprod()
    cum = nav.iloc[-1] - 1
    ann = (1 + cum) ** (12 / len(ser)) - 1 if len(ser) > 0 else 0
    mdd = ((nav - nav.cummax()) / nav.cummax()).min()
    sharpe = ser.mean() / ser.std() * np.sqrt(12) if ser.std() > 0 else 0

    return {"cum": cum, "ann": ann, "mdd": mdd, "sharpe": sharpe}


# 主回测
print(f"\n回测期间: {START_DATE} 至 {END_DATE}")
dates = get_monthly_dates(START_DATE, END_DATE)
print(f"调仓次数: {len(dates) - 1}")

variants = ["baseline", "turnover", "cgo", "combined", "industry_cap"]
results = {v: [] for v in variants}
counts = {v: [] for v in variants}

print("\n开始回测...")
for i in range(len(dates) - 1):
    if i % 6 == 0:
        print(f"进度: {i}/{len(dates) - 1}")

    date = dates[i]
    next_date = dates[i + 1]
    date_str = str(date)
    next_date_str = str(next_date)

    try:
        stocks = get_universe(date)
        df = calc_rfscore_simple(stocks, date_str)

        turnover = calc_turnover(stocks, date_str)
        cgo = calc_cgo(stocks, date_str)
        industry_map = get_industry_map(stocks, date_str)

        for variant in variants:
            selected = select_stocks(df, variant, turnover, cgo, industry_map)
            counts[variant].append(len(selected))
            ret = calc_return(selected, date_str, next_date_str)
            results[variant].append(ret)

    except Exception as e:
        print(f"错误 {date_str}: {e}")
        for variant in variants:
            counts[variant].append(0)
            results[variant].append(0.0)

# 汇总
print("\n" + "=" * 80)
print("回测结果")
print("=" * 80)

final_results = {}
for variant in variants:
    metrics = calc_metrics(results[variant])
    final_results[variant] = metrics
    avg_count = np.mean(counts[variant]) if counts[variant] else 0

    print(f"\n{variant}:")
    print(f"  年化收益: {metrics['ann']:.2%}")
    print(f"  最大回撤: {metrics['mdd']:.2%}")
    print(f"  夏普比率: {metrics['sharpe']:.2f}")
    print(f"  平均持仓: {avg_count:.1f}")

# 对比
print("\n" + "=" * 80)
print("相对基准 (baseline)")
print("=" * 80)
baseline_metrics = final_results["baseline"]
for variant in variants[1:]:
    metrics = final_results[variant]
    ann_diff = metrics["ann"] - baseline_metrics["ann"]
    mdd_diff = metrics["mdd"] - baseline_metrics["mdd"]
    sharpe_diff = metrics["sharpe"] - baseline_metrics["sharpe"]

    print(f"\n{variant}:")
    print(f"  年化收益变化: {ann_diff:+.2%}")
    print(f"  最大回撤变化: {mdd_diff:+.2%}")
    print(f"  夏普比率变化: {sharpe_diff:+.2f}")

print("\n" + "=" * 80)
print("完成!")
print("=" * 80)
