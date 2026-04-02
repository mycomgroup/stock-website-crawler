# 风险溢价择时策略 - Notebook可运行版本
# 基于国盛证券研报：因子择时系列之一：风险溢价时钟视角下的攻守因子配置
# 原文：https://www.joinquant.com/view/community/detail/25418

from jqdata import *
import numpy as np
import pandas as pd
import datetime as dt
import warnings

warnings.filterwarnings("ignore")

print("=" * 70)
print("风险溢价择时策略 - 完整回测验证")
print("=" * 70)

# ---- 参数设置 ----
END_DATE = "2026-03-28"
START_DATE = "2018-01-01"  # 约8年回测周期

print(f"\n回测区间: {START_DATE} 至 {END_DATE}")

# ---- 获取数据 ----
print("\n【1】获取数据...")
try:
    # 获取银行板块股息率 (申万银行行业代码: 801780)
    guxilv = finance.run_query(
        query(finance.SW1_DAILY_VALUATION)
        .filter(finance.SW1_DAILY_VALUATION.code == "801780")
        .order_by(finance.SW1_DAILY_VALUATION.date.desc())
        .limit(2000)
    )

    # 获取沪深300收盘价
    price = get_price(
        "399300.XSHE",
        count=2000,
        end_date=END_DATE,
        frequency="daily",
        fields=["open", "close"],
    )

    # 获取国债逆回购利率 (GC182)
    huigou = bond.run_query(
        query(bond.REPO_DAILY_PRICE)
        .filter(bond.REPO_DAILY_PRICE.name == "GC182")
        .order_by(bond.REPO_DAILY_PRICE.date.desc())
        .limit(2000)
    )

    print(f"  股息率数据: {len(guxilv)} 条")
    print(f"  沪深300数据: {len(price)} 条")
    print(f"  逆回购数据: {len(huigou)} 条")

except Exception as e:
    print(f"  数据获取失败: {e}")
    import traceback

    traceback.print_exc()

# ---- 数据处理 ----
print("\n【2】数据处理...")
try:
    guxilv_df = guxilv[["date", "dividend_ratio"]].set_index("date").sort_index()
    nihuigou_df = huigou[["date", "close"]].set_index("date").sort_index()

    final_df = guxilv_df.copy()
    final_df["nihuigou"] = nihuigou_df["close"]
    final_df["dividend_ratio"] = final_df["dividend_ratio"] * 0.92  # 修正系数
    final_df["dividend_ratio"] = final_df["dividend_ratio"].fillna(method="pad")
    final_df["nihuigou"] = final_df["nihuigou"].fillna(method="pad")

    price["date"] = price.index
    price.index = pd.to_datetime(price.index)
    final_df["price"] = price["close"]

    # 平滑处理
    final_df["guxi1"] = final_df["dividend_ratio"].rolling(60).mean()
    final_df["lilv1"] = final_df["nihuigou"].rolling(60).mean()

    print(f"  合成数据: {len(final_df)} 条")
    print(f"  最新股息率: {final_df['dividend_ratio'].iloc[-1]:.2f}")
    print(f"  最新逆回购: {final_df['nihuigou'].iloc[-1]:.2f}")

except Exception as e:
    print(f"  数据处理失败: {e}")

# ---- 生成信号 ----
print("\n【3】生成择时信号...")
try:
    final_df["singal1"] = -(final_df["guxi1"] - final_df["lilv1"]) * 1.0

    def get_position(x):
        pre1_date = final_df["pre1_date"][x]
        pre2_date = final_df["pre2_date"][x]

        if type(pre2_date) is float:
            return 0

        try:
            pre1_date_value = final_df["singal1"][pre1_date]
            pre2_date_value = final_df["singal1"][pre2_date]

            if pre1_date_value > pre2_date_value:
                return 1
            else:
                return 0
        except:
            return 0

    final_df["date"] = final_df.index
    final_df["pre1_date"] = final_df["date"].shift(1)
    final_df["pre2_date"] = final_df["date"].shift(2)
    final_df["positon"] = final_df["date"].apply(get_position)

    final_df["ret"] = final_df["price"].pct_change()
    RET = final_df["ret"] * final_df["positon"]
    CUM_RET = (1 + RET).cumprod()

    print(f"  信号生成完成")
    print(f"  持仓天数: {int(final_df['positon'].sum())}")
    print(f"  总交易日: {len(final_df)}")
    print(f"  持仓比例: {final_df['positon'].mean():.1%}")

except Exception as e:
    print(f"  信号生成失败: {e}")

# ---- 收益统计 ----
print("\n【4】收益统计分析...")
try:

    def format_x(x):
        return "{:.2%}".format(x)

    annual_ret = CUM_RET[-1] ** (250 / len(RET)) - 1
    cum_ret_rate = CUM_RET[-1] - 1

    max_nv = np.maximum.accumulate(np.nan_to_num(CUM_RET))
    mdd = -np.min(CUM_RET / max_nv - 1)

    sharpe_ratio = np.mean(RET) / np.nanstd(RET, ddof=1) * np.sqrt(250)

    mark = final_df["positon"]
    pre_mark = np.nan_to_num(final_df["positon"].shift(-1))
    trade = (mark >= 1) & (pre_mark < mark)
    trade_count = np.nansum(trade)

    total = np.sum(mark)
    mean_hold = total / trade_count if trade_count > 0 else 0

    win = np.sum(np.where(RET > 0, 1, 0))
    lose = np.sum(np.where(RET < 0, 1, 0))
    win_ratio = win / total if total > 0 else 0

    print(f"\n  === 核心指标 ===")
    print(f"  年化收益率: {format_x(annual_ret)}")
    print(f"  累计收益率: {format_x(cum_ret_rate)}")
    print(f"  夏普比率:   {sharpe_ratio:.4f}")
    print(f"  最大回撤:   {format_x(mdd)}")
    print(f"  交易次数:   {int(trade_count)}")
    print(f"  平均持仓:   {mean_hold:.1f} 天")
    print(f"  胜率(按天): {format_x(win_ratio)}")

    print(f"\n  === 详细统计 ===")
    print(f"  持仓总天数: {int(total)}")
    print(f"  获利天数:   {int(win)}")
    print(f"  亏损天数:   {int(lose)}")

except Exception as e:
    print(f"  统计分析失败: {e}")

# ---- 当前风险溢价状态 ----
print("\n【5】当前风险溢价状态...")
try:
    latest_guxi = final_df["guxi1"].iloc[-1]
    latest_lilv = final_df["lilv1"].iloc[-1]
    latest_signal = final_df["singal1"].iloc[-1]
    latest_position = final_df["positon"].iloc[-1]

    print(f"  最新股息率(60日均): {latest_guxi:.2f}")
    print(f"  最新逆回购(60日均): {latest_lilv:.2f}")
    print(f"  风险溢价信号:     {latest_signal:.4f}")
    print(f"  当前仓位:         {'满仓' if latest_position == 1 else '空仓'}")
    print(
        f"  风险溢价状态:     {'股息率>逆回购(看多)' if latest_guxi > latest_lilv else '股息率<逆回购(看空)'}"
    )

except Exception as e:
    print(f"  状态计算失败: {e}")

print("\n" + "=" * 70)
print("风险溢价择时策略回测完成!")
print("=" * 70)
