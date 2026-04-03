#!/usr/bin/env python3
"""市场情绪指标实测 - 聚宽平台执行"""

from jqdata import *
import pandas as pd
import numpy as np
import talib as tb
from datetime import datetime, timedelta
import json

print("=" * 60)
print("市场情绪指标实测 - 2024年最新数据")
print("=" * 60)

end_date = "2024-12-20"
benchmark = "000300.XSHG"

# ============ 1. 市场宽度 (BIAS>0比例) ============
print("\n【1】市场宽度 (BIAS>0 行业占比)")
print("-" * 40)

try:
    # 获取申万行业
    sw_industries = get_industries(name="sw_l1")
    trade_days = get_trade_days(end_date=end_date, count=10)[-10:]

    breadth_results = []
    for day in trade_days:
        stocks = get_index_stocks("000902.XSHG", date=day)
        if len(stocks) == 0:
            continue

        # 批量获取价格计算MA20
        prices = get_price(
            stocks, end_date=day, count=21, fields=["close"], panel=False
        )
        if len(prices) == 0:
            continue

        pivot = prices.pivot(index="time", columns="code", values="close")
        if len(pivot) < 21:
            continue

        ma20 = pivot.rolling(20).mean()
        last_close = pivot.iloc[-1]
        last_ma = ma20.iloc[-1]

        # BIAS > 0 的股票比例
        positive = (last_close > last_ma).sum()
        total = len(pivot.columns)
        ratio = round(100 * positive / total, 1)

        breadth_results.append({"date": str(day), "breadth_pct": ratio})
        print(f"  {day}: {ratio}% 个行业在MA20之上")

    # 最新值
    if breadth_results:
        latest = breadth_results[-1]["breadth_pct"]
        status = (
            "极度悲观(底部)"
            if latest < 30
            else ("极度乐观(顶部)" if latest > 70 else "中性")
        )
        print(f"\n  => 当前状态: {status}")
except Exception as e:
    print(f"  计算失败: {e}")

# ============ 2. 拥挤率 ============
print("\n【2】拥挤率 (前5%股票资金集中度)")
print("-" * 40)

try:
    crowding_results = []
    check_days = get_trade_days(end_date=end_date, count=10)

    for day in check_days:
        all_stocks = get_all_securities(date=day).index.tolist()
        df = get_price(all_stocks, end_date=day, count=1, fields=["money"], panel=False)
        df = df.dropna().sort_values("money", ascending=False)

        n_top = max(1, int(len(df) * 0.05))
        crowd = round(df.iloc[:n_top]["money"].sum() / df["money"].sum() * 100, 2)

        crowding_results.append({"date": str(day), "crowding": crowd})
        print(f"  {day}: {crowd}%")

    if crowding_results:
        latest_crowd = crowding_results[-1]["crowding"]
        status = (
            "资金过度集中(过热)"
            if latest_crowd > 60
            else ("资金分散(底部)" if latest_crowd < 40 else "正常")
        )
        print(f"\n  => 当前状态: {status}")
except Exception as e:
    print(f"  计算失败: {e}")

# ============ 3. 底部特征指标 ============
print("\n【3】底部特征指标")
print("-" * 40)

try:
    # 3.1 破净占比
    val_df = get_fundamentals(
        query(valuation.code, valuation.pb_ratio).filter(valuation.pb_ratio < 1),
        date=end_date,
    )
    all_stocks = get_all_securities(types="stock", date=end_date)
    pb_ratio = round(len(val_df) / len(all_stocks) * 100, 2)
    print(f"  破净占比: {pb_ratio}% {'(底部信号)' if pb_ratio > 10 else ''}")

    # 3.2 股价<2元占比
    prices_1d = get_price(
        all_stocks.index.tolist(),
        end_date=end_date,
        count=1,
        fields=["close"],
        panel=False,
    )
    low_price_count = len(prices_1d[prices_1d["close"] < 2])
    low_price_ratio = round(low_price_count / len(prices_1d) * 100, 2)
    print(
        f"  股价<2元占比: {low_price_ratio}% {'(底部信号)' if low_price_ratio > 5 else ''}"
    )

    # 3.3 成交额萎缩程度
    money_data = history(
        250,
        unit="1d",
        field="money",
        security_list=["399001.XSHE", "000001.XSHG"],
        df=True,
        skip_paused=False,
        fq=None,
    )
    money_data["total"] = money_data["399001.XSHE"] + money_data["000001.XSHG"]
    shrinkage = round(money_data["total"].iloc[-1] / money_data["total"].max() * 100, 2)
    print(
        f"  成交额萎缩: {shrinkage}% of 历史峰值 {'(地量信号)' if shrinkage < 20 else ''}"
    )

    # 3.4 PE中位数
    pe_df = get_fundamentals(query(valuation.code, valuation.pe_ratio), date=end_date)
    pe_median = round(pe_df["pe_ratio"].median(), 2)
    print(f"  全市场PE中位数: {pe_median}")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 4. FED指标 & 格雷厄姆指数 ============
print("\n【4】FED指标 & 格雷厄姆指数")
print("-" * 40)

try:
    # 获取沪深300 PE
    hs300_stocks = get_index_stocks(benchmark, date=end_date)
    pe_data = get_fundamentals(
        query(valuation.code, valuation.pe_ratio).filter(
            valuation.code.in_(hs300_stocks)
        ),
        date=end_date,
    )

    hs300_pe = round(pe_data["pe_ratio"].median(), 2)
    earnings_yield = round(100 / hs300_pe, 4)

    # 近似10年国债收益率(实际应从chinabond获取)
    bond_yield = 2.0  # 2024年底约2.0%

    fed = round(earnings_yield - bond_yield, 4)
    graham = round(earnings_yield / bond_yield, 4)

    print(f"  沪深300 PE中位数: {hs300_pe}")
    print(f"  盈利收益率(1/PE): {earnings_yield}%")
    print(f"  10年国债收益率(近似): {bond_yield}%")
    print(f"  FED指标: {fed} {'(低估)' if fed > 0 else '(高估)'}")
    print(
        f"  格雷厄姆指数: {graham} {'(低估)' if graham > 1.5 else '(中性)' if graham > 1 else '(高估)'}"
    )

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 5. 创新高个股比例 ============
print("\n【5】创新高个股比例")
print("-" * 40)

try:
    window = 120  # 半年
    check_days = 5

    by_date = get_trade_days(end_date=end_date, count=window + check_days)[0]
    stock_list = get_all_securities(date=by_date).index.tolist()

    prices = (
        get_price(
            stock_list,
            end_date=end_date,
            frequency="daily",
            fields="close",
            count=window + check_days,
            panel=False,
        )
        .pivot(index="time", columns="code", values="close")
        .dropna(axis=1)
    )

    for i in range(check_days):
        check_date = prices.index[window + i]
        price_slice = prices.iloc[i + 1 : window + i + 1]

        is_new_high = price_slice.apply(lambda x: np.argmax(x.values) == (len(x) - 1))
        new_high_count = is_new_high.sum()
        pct = round(100 * new_high_count / len(stock_list), 2)
        print(f"  {check_date.date()}: {pct}% 创{window}日新高")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 6. GSISI投资者情绪指数 ============
print("\n【6】GSISI投资者情绪指数")
print("-" * 40)

try:
    # 获取沪深300和申万行业数据
    start_date = (
        datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=180)
    ).strftime("%Y-%m-%d")

    index_price = get_price(
        benchmark,
        start_date=start_date,
        end_date=end_date,
        fields=["close"],
        panel=False,
    )
    index_price = index_price.set_index("time")["close"]

    # 获取申万一级行业
    sw_codes = sw_industries.index.tolist()
    sw_data = {}
    for code in sw_codes:
        try:
            stocks = get_industry_stocks(code, date=end_date)
            if len(stocks) > 0:
                sw_prices = get_price(
                    stocks,
                    start_date=start_date,
                    end_date=end_date,
                    fields=["close"],
                    panel=False,
                )
                if len(sw_prices) > 0:
                    pivot = sw_prices.pivot(
                        index="time", columns="code", values="close"
                    )
                    sw_data[code] = pivot.mean(axis=1)
        except:
            continue

    sw_df = pd.DataFrame(sw_data)
    sw_df.index = pd.to_datetime(sw_df.index)
    index_price.index = pd.to_datetime(index_price.index)

    # 计算5日收益率
    pct_window = 5
    sw_pct = sw_df.pct_change(pct_window)
    index_pct = index_price.pct_change(pct_window)

    # 计算50日滚动Beta
    beta_window = 50
    beta_df = sw_pct.apply(lambda x: tb.BETA(x, index_pct, beta_window))

    # Spearman秩相关
    gsisi_series = sw_pct.corrwith(beta_df, method="spearman", axis=1)
    gsisi_latest = gsisi_series.dropna().iloc[-1]

    print(f"  最新GSISI: {gsisi_latest:.4f}")
    status = (
        "乐观(看多)"
        if gsisi_latest > 0.3
        else ("悲观(看空)" if gsisi_latest < -0.3 else "中性")
    )
    print(f"  情绪状态: {status}")

    # 最近5天趋势
    print(f"  最近5天GSISI趋势:")
    for d, v in gsisi_series.dropna().tail(5).items():
        print(f"    {d.date()}: {v:.4f}")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 综合判断 ============
print("\n" + "=" * 60)
print("【综合判断】")
print("=" * 60)
print("""
指标组合判断逻辑:
1. 市场宽度 < 30% + 拥挤率 < 40% + 创新高 < 1% → 底部区域
2. 市场宽度 > 70% + 创新高 > 5% → 顶部区域
3. FED > 0 + 格雷厄姆 > 1.5 → 估值偏低
4. GSISI连续 < -0.3 → 情绪悲观(可能底部)
""")
print("实测完成!")
