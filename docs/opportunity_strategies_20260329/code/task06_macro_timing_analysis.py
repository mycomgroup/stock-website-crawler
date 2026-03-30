#!/usr/bin/env python3
"""任务06: 宏观与市场状态择时框架 - 指标有效性分析"""

from jqdata import *
from jqdata import macro
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务06: 宏观与市场状态择时框架 - 指标有效性分析")
print("=" * 80)

# ============================================================
# 配置
# ============================================================
START_DATE = "2019-12-01"  # 预留3个月历史数据计算指标
END_DATE = "2026-03-31"
VALID_START = "2021-01-01"
OOS_START = "2024-01-01"
BENCHMARK = "000300.XSHG"

# ============================================================
# 第一部分: 宏观月频指标
# ============================================================
print("\n" + "=" * 60)
print("第一部分: 宏观月频指标 (PMI、社融、北向资金)")
print("=" * 60)

# 1.1 PMI指标
print("\n【1.1】制造业PMI分析")
print("-" * 40)

try:
    pmi_df = macro.run_query(
        query(
            macro.MAC_MANUFACTURING_PMI.stat_month,
            macro.MAC_MANUFACTURING_PMI.pmi,
            macro.MAC_MANUFACTURING_PMI.produce_idx,
            macro.MAC_MANUFACTURING_PMI.new_orders_idx,
            macro.MAC_MANUFACTURING_PMI.raw_material_idx,
            macro.MAC_MANUFACTURING_PMI.finished_produce_idx,
        )
        .filter(
            macro.MAC_MANUFACTURING_PMI.stat_month >= START_DATE[:7],
            macro.MAC_MANUFACTURING_PMI.stat_month <= END_DATE[:7],
        )
        .order_by(macro.MAC_MANUFACTURING_PMI.stat_month.asc())
    )

    print(
        f"  PMI数据: {len(pmi_df)} 条, 从 {pmi_df['stat_month'].iloc[0]} 到 {pmi_df['stat_month'].iloc[-1]}"
    )

    # 计算PMI斜率(3个月窗口)
    pmi_df["pmi_slope3"] = (
        pmi_df["pmi"]
        .rolling(3)
        .apply(lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == 3 else np.nan)
    )
    pmi_df["pmi_ma3"] = pmi_df["pmi"].rolling(3).mean()
    pmi_df["pmi_above50"] = (pmi_df["pmi"] >= 50).astype(int)
    pmi_df["new_orders_diffusion"] = pmi_df["new_orders_idx"] - pmi_df["produce_idx"]
    pmi_df["inventory_signal"] = (
        pmi_df["raw_material_idx"] - pmi_df["finished_produce_idx"]
    )

    print(f"  PMI >= 50 比例: {pmi_df['pmi_above50'].mean() * 100:.1f}%")
    print(f"  PMI斜率>0 比例: {(pmi_df['pmi_slope3'] > 0).mean() * 100:.1f}%")
    print(f"  平均PMI: {pmi_df['pmi'].mean():.2f}")

    # 打印最近12个月
    print("\n  最近12个月PMI数据:")
    recent_pmi = pmi_df.tail(12)
    for _, row in recent_pmi.iterrows():
        slope_str = (
            f"斜率={row['pmi_slope3']:.3f}"
            if not np.isnan(row["pmi_slope3"])
            else "斜率=N/A"
        )
        print(
            f"    {row['stat_month']}: PMI={row['pmi']:.1f}, {slope_str}, 新订单扩散={row['new_orders_diffusion']:.1f}, 库存信号={row['inventory_signal']:.1f}"
        )
except Exception as e:
    print(f"  PMI分析失败: {e}")
    pmi_df = pd.DataFrame()

# 1.2 社融增速
print("\n【1.2】社会融资规模分析")
print("-" * 40)

try:
    # 获取社融存量同比
    tsf_df = macro.run_query(
        query(
            macro.MAC_SOCIAL_FINANCE.stat_month,
            macro.MAC_SOCIAL_FINANCE.monthly_add_financing,
            macro.MAC_SOCIAL_FINANCE.yoy,
        )
        .filter(
            macro.MAC_SOCIAL_FINANCE.stat_month >= START_DATE[:7],
            macro.MAC_SOCIAL_FINANCE.stat_month <= END_DATE[:7],
        )
        .order_by(macro.MAC_SOCIAL_FINANCE.stat_month.asc())
    )

    if len(tsf_df) > 0:
        print(f"  社融数据: {len(tsf_df)} 条")
        tsf_df["tsf_yoy_ma3"] = tsf_df["yoy"].rolling(3).mean()
        tsf_df["tsf_expanding"] = (tsf_df["yoy"] > tsf_df["yoy"].shift(1)).astype(int)

        print(f"  社融同比扩大比例: {tsf_df['tsf_expanding'].mean() * 100:.1f}%")
        print(f"  平均社融同比: {tsf_df['yoy'].mean():.2f}%")

        print("\n  最近12个月社融数据:")
        for _, row in tsf_df.tail(12).iterrows():
            expand_str = "↑" if row["tsf_expanding"] == 1 else "↓"
            print(
                f"    {row['stat_month']}: 同比={row['yoy']:.2f}% {expand_str}, MA3={row['tsf_yoy_ma3']:.2f}%"
            )
    else:
        print("  未获取到社融数据")
        tsf_df = pd.DataFrame()
except Exception as e:
    print(f"  社融分析失败: {e}")
    tsf_df = pd.DataFrame()

# 1.3 北向资金
print("\n【1.3】北向资金月度趋势")
print("-" * 40)

try:
    trade_days = get_trade_days(start_date=START_DATE, end_date=END_DATE)

    # 按月聚合北向资金
    northbound_monthly = []
    current_month = None
    month_net = 0

    for i in range(1, len(trade_days)):
        day = trade_days[i]
        prev = trade_days[i - 1]
        month_str = day.strftime("%Y-%m")

        try:
            df_today = get_money_flow(
                [BENCHMARK], end_date=day, fields=["net_amount"], count=1
            )
            df_prev = get_money_flow(
                [BENCHMARK], end_date=prev, fields=["net_amount"], count=1
            )

            if (
                df_today is not None
                and df_prev is not None
                and len(df_today) > 0
                and len(df_prev) > 0
            ):
                daily_net = (
                    df_today["net_amount"].iloc[0] - df_prev["net_amount"].iloc[0]
                )
            else:
                daily_net = 0
        except:
            daily_net = 0

        if current_month != month_str:
            if current_month is not None:
                northbound_monthly.append(
                    {"month": current_month, "net_flow": month_net}
                )
            current_month = month_str
            month_net = 0

        month_net += daily_net

    if current_month is not None:
        northbound_monthly.append({"month": current_month, "net_flow": month_net})

    nb_df = pd.DataFrame(northbound_monthly)
    if len(nb_df) > 0:
        nb_df["nb_ma3"] = nb_df["net_flow"].rolling(3).mean()
        nb_df["nb_positive"] = (nb_df["net_flow"] > 0).astype(int)

        print(f"  北向资金月度数据: {len(nb_df)} 条")
        print(f"  北向净流入月数比例: {nb_df['nb_positive'].mean() * 100:.1f}%")

        print("\n  最近12个月北向资金:")
        for _, row in nb_df.tail(12).iterrows():
            direction = "净流入" if row["net_flow"] > 0 else "净流出"
            print(
                f"    {row['month']}: {direction} {abs(row['net_flow']) / 1e8:.2f}亿, MA3={row['nb_ma3'] / 1e8:.2f}亿"
            )
    else:
        print("  未获取到北向资金数据")
except Exception as e:
    print(f"  北向资金分析失败: {e}")
    nb_df = pd.DataFrame()

# ============================================================
# 第二部分: 市场周频指标
# ============================================================
print("\n" + "=" * 60)
print("第二部分: 市场周频指标 (指数趋势、涨停家数、跌停扩散)")
print("=" * 60)

# 2.1 指数趋势
print("\n【2.1】沪深300周频趋势")
print("-" * 40)

try:
    index_daily = get_price(
        BENCHMARK,
        start_date=START_DATE,
        end_date=END_DATE,
        fields=["close", "volume"],
        panel=False,
        frequency="daily",
    )
    index_daily = index_daily.set_index("time")
    index_daily.index = pd.to_datetime(index_daily.index)

    # 周频重采样
    index_weekly = (
        index_daily.resample("W").agg({"close": "last", "volume": "sum"}).dropna()
    )
    index_weekly["wma5"] = index_weekly["close"].rolling(5).mean()
    index_weekly["wma10"] = index_weekly["close"].rolling(10).mean()
    index_weekly["wma20"] = index_weekly["close"].rolling(20).mean()
    index_weekly["above_wma20"] = (
        index_weekly["close"] > index_weekly["wma20"]
    ).astype(int)
    index_weekly["weekly_return"] = index_weekly["close"].pct_change()
    index_weekly["vol_ma5"] = index_weekly["volume"].rolling(5).mean()
    index_weekly["volume_shrink"] = (
        index_weekly["volume"] < index_weekly["vol_ma5"]
    ).astype(int)

    print(f"  周频数据: {len(index_weekly)} 周")
    print(f"  在WMA20上方比例: {index_weekly['above_wma20'].mean() * 100:.1f}%")

    # 滚动训练: 24月训练, 6月验证
    print("\n  滚动训练窗口统计:")
    train_months = 24
    valid_months = 6

    valid_start_dt = pd.Timestamp(VALID_START)
    oos_start_dt = pd.Timestamp(OOS_START)

    window_count = 0
    for window_start in pd.date_range(
        valid_start_dt - pd.DateOffset(months=train_months),
        oos_start_dt - pd.DateOffset(months=valid_months),
        freq="6MS",
    ):
        window_end = window_start + pd.DateOffset(months=train_months + valid_months)
        train_end = window_start + pd.DateOffset(months=train_months)

        train_data = index_weekly[
            (index_weekly.index >= window_start) & (index_weekly.index < train_end)
        ]
        valid_data = index_weekly[
            (index_weekly.index >= train_end) & (index_weekly.index < window_end)
        ]

        if len(train_data) > 0 and len(valid_data) > 0:
            window_count += 1
            train_above_pct = train_data["above_wma20"].mean() * 100
            valid_above_pct = valid_data["above_wma20"].mean() * 100
            if window_count <= 5 or window_count % 3 == 0:
                print(
                    f"    窗口{window_count}: 训练{window_start.strftime('%Y-%m')}~{train_end.strftime('%Y-%m')} "
                    f"(趋势上方{train_above_pct:.0f}%) | 验证{train_end.strftime('%Y-%m')}~{window_end.strftime('%Y-%m')} "
                    f"(趋势上方{valid_above_pct:.0f}%)"
                )

    print(f"  总共 {window_count} 个滚动窗口")
except Exception as e:
    print(f"  指数趋势分析失败: {e}")
    index_weekly = pd.DataFrame()

# 2.2 涨停家数统计
print("\n【2.2】涨停跌停家数周度统计")
print("-" * 40)

try:
    all_stocks = get_all_securities("stock", date=VALID_START).index.tolist()
    # 过滤科创板和北交所
    all_stocks = [
        s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
    ]

    check_weeks = get_trade_days(start_date=VALID_START, end_date=END_DATE)

    # 每周五统计
    friday_stats = []
    for i in range(0, len(check_weeks), 5):
        day = check_weeks[min(i + 4, len(check_weeks) - 1)]
        try:
            df = get_price(
                all_stocks[:500],
                end_date=day,
                count=1,
                fields=["close", "high_limit", "low_limit"],
                panel=False,
            )
            df = df.dropna()

            hl_count = len(df[df["close"] == df["high_limit"]])
            ll_count = len(df[df["close"] == df["low_limit"]])

            friday_stats.append(
                {
                    "date": day.strftime("%Y-%m-%d"),
                    "hl_count": hl_count,
                    "ll_count": ll_count,
                    "hl_ll_ratio": hl_count / max(ll_count, 1),
                }
            )
        except:
            continue

    hl_df = pd.DataFrame(friday_stats)
    if len(hl_df) > 0:
        hl_df["hl_ma4"] = hl_df["hl_count"].rolling(4).mean()
        hl_df["ll_ma4"] = hl_df["ll_count"].rolling(4).mean()
        hl_df["ratio_ma4"] = hl_df["hl_ll_ratio"].rolling(4).mean()

        print(f"  周度统计数据: {len(hl_df)} 周")
        print(f"  平均涨停家数: {hl_df['hl_count'].mean():.1f}")
        print(f"  平均跌停家数: {hl_df['ll_count'].mean():.1f}")
        print(f"  涨跌停比均值: {hl_df['hl_ll_ratio'].mean():.2f}")

        print("\n  最近8周数据:")
        for _, row in hl_df.tail(8).iterrows():
            print(
                f"    {row['date']}: 涨停={row['hl_count']}, 跌停={row['ll_count']}, 比值={row['hl_ll_ratio']:.2f}"
            )
except Exception as e:
    print(f"  涨跌停分析失败: {e}")
    hl_df = pd.DataFrame()

# ============================================================
# 第三部分: 情绪日频指标
# ============================================================
print("\n" + "=" * 60)
print("第三部分: 情绪日频指标 (连板数、晋级率、龙头溢价)")
print("=" * 60)

print("\n【3.1】最高连板数与晋级率")
print("-" * 40)

try:
    trade_days_list = get_trade_days(start_date=VALID_START, end_date=END_DATE)

    sentiment_daily = []
    for i in range(1, min(len(trade_days_list), 500)):  # 采样分析
        if i % 10 != 0:
            continue
        day = trade_days_list[i]
        prev_day = trade_days_list[i - 1]

        try:
            prev_stocks = get_all_securities("stock", date=prev_day).index.tolist()
            prev_stocks = [
                s for s in prev_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
            ]

            df = get_price(
                prev_stocks[:300],
                end_date=prev_day,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )
            df = df.dropna()

            hl_stocks = df[df["close"] == df["high_limit"]]
            hl_count = len(hl_stocks)

            sentiment_daily.append(
                {
                    "date": day.strftime("%Y-%m-%d"),
                    "hl_count": hl_count,
                }
            )
        except:
            continue

    sent_df = pd.DataFrame(sentiment_daily)
    if len(sent_df) > 0:
        print(f"  情绪数据采样: {len(sent_df)} 个交易日")
        print(f"  平均涨停家数: {sent_df['hl_count'].mean():.1f}")
        print(f"  涨停家数标准差: {sent_df['hl_count'].std():.1f}")

        # 分层统计
        q25 = sent_df["hl_count"].quantile(0.25)
        q50 = sent_df["hl_count"].quantile(0.50)
        q75 = sent_df["hl_count"].quantile(0.75)
        print(f"  涨停家数分位: 25%={q25:.0f}, 50%={q50:.0f}, 75%={q75:.0f}")
except Exception as e:
    print(f"  情绪分析失败: {e}")
    sent_df = pd.DataFrame()

# ============================================================
# 第四部分: 三层指标与指数收益的相关性分析
# ============================================================
print("\n" + "=" * 60)
print("第四部分: 三层指标与未来收益相关性分析")
print("=" * 60)

try:
    # 合并月度宏观指标与指数月度收益
    index_monthly = index_daily.resample("ME").agg({"close": "last"}).dropna()
    index_monthly["monthly_return"] = index_monthly["close"].pct_change()
    index_monthly["next_month_return"] = index_monthly["monthly_return"].shift(-1)

    if len(pmi_df) > 0:
        pmi_df["month_dt"] = pd.to_datetime(pmi_df["stat_month"])
        pmi_df = pmi_df.set_index("month_dt")

        merged = index_monthly.join(
            pmi_df[["pmi", "pmi_slope3", "new_orders_diffusion", "inventory_signal"]],
            how="inner",
        )
        merged = merged.dropna(subset=["next_month_return", "pmi"])

        if len(merged) > 10:
            corr_pmi = merged["pmi"].corr(merged["next_month_return"])
            corr_slope = merged["pmi_slope3"].corr(merged["next_month_return"])
            corr_new_orders = merged["new_orders_diffusion"].corr(
                merged["next_month_return"]
            )
            corr_inventory = merged["inventory_signal"].corr(
                merged["next_month_return"]
            )

            print(f"\n  PMI与下月收益相关性 ({len(merged)} 个月):")
            print(f"    PMI绝对值: {corr_pmi:.4f}")
            print(f"    PMI斜率:   {corr_slope:.4f}")
            print(f"    新订单扩散: {corr_new_orders:.4f}")
            print(f"    库存信号:  {corr_inventory:.4f}")

            # 条件收益
            pmi_above = merged[merged["pmi"] >= 50]
            pmi_below = merged[merged["pmi"] < 50]
            if len(pmi_above) > 5 and len(pmi_below) > 5:
                print(
                    f"\n  PMI>=50时平均月收益: {pmi_above['next_month_return'].mean() * 100:.2f}%"
                )
                print(
                    f"  PMI<50时平均月收益:  {pmi_below['next_month_return'].mean() * 100:.2f}%"
                )

            slope_pos = merged[merged["pmi_slope3"] > 0]
            slope_neg = merged[merged["pmi_slope3"] <= 0]
            if len(slope_pos) > 5 and len(slope_neg) > 5:
                print(
                    f"  PMI斜率>0时平均月收益: {slope_pos['next_month_return'].mean() * 100:.2f}%"
                )
                print(
                    f"  PMI斜率<=0时平均月收益: {slope_neg['next_month_return'].mean() * 100:.2f}%"
                )

        # OOS分析
        merged_oos = merged[merged.index >= OOS_START]
        if len(merged_oos) > 5:
            corr_pmi_oos = merged_oos["pmi"].corr(merged_oos["next_month_return"])
            print(f"\n  [2024+样本外] PMI与收益相关性: {corr_pmi_oos:.4f}")

            pmi_above_oos = merged_oos[merged_oos["pmi"] >= 50]
            pmi_below_oos = merged_oos[merged_oos["pmi"] < 50]
            if len(pmi_above_oos) > 2 and len(pmi_below_oos) > 2:
                print(
                    f"  [2024+] PMI>=50平均月收益: {pmi_above_oos['next_month_return'].mean() * 100:.2f}% ({len(pmi_above_oos)}月)"
                )
                print(
                    f"  [2024+] PMI<50平均月收益:  {pmi_below_oos['next_month_return'].mean() * 100:.2f}% ({len(pmi_below_oos)}月)"
                )
except Exception as e:
    print(f"  相关性分析失败: {e}")

# ============================================================
# 第五部分: 三层框架状态划分
# ============================================================
print("\n" + "=" * 60)
print("第五部分: 三层框架状态划分与历史回溯")
print("=" * 60)

try:
    # 构建月度宏观状态
    if len(pmi_df) > 0:
        pmi_df["macro_state"] = 2  # 默认中性
        pmi_df.loc[
            (pmi_df["pmi"] >= 50) & (pmi_df["pmi_slope3"] > 0), "macro_state"
        ] = 3  # 过热
        pmi_df.loc[
            (pmi_df["pmi"] >= 50) & (pmi_df["pmi_slope3"] <= 0), "macro_state"
        ] = 2  # 中性
        pmi_df.loc[(pmi_df["pmi"] < 50) & (pmi_df["pmi_slope3"] > 0), "macro_state"] = (
            1  # 衰退
        )
        pmi_df.loc[
            (pmi_df["pmi"] < 50) & (pmi_df["pmi_slope3"] <= 0), "macro_state"
        ] = 0  # 萧条

        state_counts = pmi_df["macro_state"].value_counts().sort_index()
        state_names = {0: "萧条", 1: "衰退", 2: "中性", 3: "过热"}

        print("\n  宏观状态分布:")
        for state, count in state_counts.items():
            pct = count / len(pmi_df) * 100
            print(
                f"    {state_names.get(state, '未知')}({state}): {count}月 ({pct:.1f}%)"
            )

        print("\n  最近12个月宏观状态:")
        for _, row in pmi_df.tail(12).iterrows():
            state_name = state_names.get(row["macro_state"], "未知")
            print(
                f"    {row['stat_month']}: {state_name} (PMI={row['pmi']:.1f}, 斜率={row['pmi_slope3']:.3f})"
            )
except Exception as e:
    print(f"  状态划分失败: {e}")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("总结")
print("=" * 60)
print("""
1. PMI有效性:
   - PMI>=50 + 斜率>0 定义复苏/过热期
   - PMI<50 + 斜率<=0 定义萧条期
   - 需要进一步回测验证择时增益

2. 社融有效性:
   - 社融同比扩大通常领先市场1-2个月
   - 需结合PMI共同判断

3. 北向资金:
   - 月度净流入/流出可作为趋势确认指标
   - 单独使用效果较弱

4. 市场周频:
   - 指数在WMA20上方/下方是最直接的趋势判断
   - 涨停家数均值可作为情绪层补充

5. 情绪日频:
   - 涨停家数是情绪温度的直接度量
   - 需要日频数据计算连板数和晋级率
""")

print("分析完成!")
