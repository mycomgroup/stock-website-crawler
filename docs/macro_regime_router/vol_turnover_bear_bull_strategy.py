# 波动率+换手率牛熊指标策略 - Notebook可运行版本
# 基于华泰证券研报：波动率和换手率构建牛熊指标
# 原文：https://www.joinquant.com/view/community/detail/23605

from jqdata import *
import numpy as np
import pandas as pd
import datetime as dt
import warnings

warnings.filterwarnings("ignore")

print("=" * 70)
print("波动率+换手率牛熊指标策略 - 完整回测验证")
print("=" * 70)

# ---- 参数设置 ----
END_DATE = "2026-03-28"
START_DATE = "2018-01-01"  # 约8年回测周期
PERIODS = 200  # 波动率和换手率计算周期

print(f"\n回测区间: {START_DATE} 至 {END_DATE}")
print(f"计算周期: {PERIODS}日")

# ---- 获取数据 ----
print("\n【1】获取数据...")
try:
    # 获取上证指数数据
    close_df = get_price(
        "000001.XSHG",
        start_date=START_DATE,
        end_date=END_DATE,
        fields=["close", "pre_close"],
    )

    # 计算收益率
    close_df["pct"] = close_df["close"] / close_df["pre_close"] - 1

    print(f"  上证指数数据: {len(close_df)} 条")
    print(f"  起始日期: {close_df.index[0]}")
    print(f"  结束日期: {close_df.index[-1]}")

except Exception as e:
    print(f"  数据获取失败: {e}")
    import traceback

    traceback.print_exc()

# ---- 计算波动率 ----
print("\n【2】计算波动率指标...")
try:
    # 计算N日波动率
    close_df[f"std_{PERIODS}"] = close_df["pct"].rolling(PERIODS).std()

    print(f"  {PERIODS}日波动率计算完成")
    print(f"  最新波动率: {close_df[f'std_{PERIODS}'].iloc[-1]:.4f}")
    print(f"  波动率均值: {close_df[f'std_{PERIODS}'].mean():.4f}")
    print(f"  波动率最小: {close_df[f'std_{PERIODS}'].min():.4f}")
    print(f"  波动率最大: {close_df[f'std_{PERIODS}'].max():.4f}")

except Exception as e:
    print(f"  波动率计算失败: {e}")

# ---- 计算换手率 ----
print("\n【3】计算换手率指标...")
try:
    # 获取交易日期列表
    trade_dates = get_trade_days(start_date=START_DATE, end_date=END_DATE)
    print(f"  交易日数量: {len(trade_dates)}")

    # 计算每日换手率（基于总流通股本）
    turnover_data = {}
    sample_dates = trade_dates[-500:]  # 取最近500个交易日加快计算

    for i, trade_date in enumerate(sample_dates):
        try:
            # 获取指数成分股
            security = get_index_stocks("000001.XSHG", date=trade_date)
            if len(security) == 0:
                continue

            # 查询总流通股本
            q_circulating_cap = query(valuation.code, valuation.circulating_cap).filter(
                valuation.code.in_(security)
            )
            circulating_cap = get_fundamentals(q_circulating_cap, date=trade_date)

            if len(circulating_cap) == 0:
                continue

            # 获取成交量
            volume = get_price(
                "000001.XSHG", end_date=trade_date, count=1, fields="volume"
            )

            # 计算换手率
            turnover = volume["volume"].sum() / circulating_cap["circulating_cap"].sum()
            turnover_data[trade_date] = turnover

            if i % 50 == 0:
                print(
                    f"  进度: {i}/{len(sample_dates)} ({i / len(sample_dates) * 100:.0f}%)"
                )

        except Exception as e:
            continue

    turnover_series = pd.Series(turnover_data, name="turnover_rate")
    print(f"  换手率数据: {len(turnover_series)} 条")

    if len(turnover_series) > 0:
        print(f"  最新换手率: {turnover_series.iloc[-1]:.4f}")
        print(f"  换手率均值: {turnover_series.mean():.4f}")

except Exception as e:
    print(f"  换手率计算失败: {e}")

# ---- 构建牛熊指标 ----
print("\n【4】构建牛熊指标...")
try:
    # 合并数据
    if len(turnover_series) > 0:
        close_df["turnover_rate"] = turnover_series

        # 计算换手率移动平均
        close_df[f"turnover_rate_{PERIODS}"] = (
            close_df["turnover_rate"].rolling(PERIODS).mean()
        )

        # 构建牛熊指标 = 波动率 / 换手率
        close_df["kernel_index"] = (
            close_df[f"std_{PERIODS}"] / close_df[f"turnover_rate_{PERIODS}"]
        )

        # 计算与指数的相关性
        corr = close_df[["kernel_index", "close"]].corr().iloc[0, 1]

        print(f"  牛熊指标计算完成")
        print(f"  最新牛熊指标: {close_df['kernel_index'].iloc[-1]:.4f}")
        print(f"  与指数相关性: {corr:.4f}")

        # 判断当前市场状态
        latest_vol = close_df[f"std_{PERIODS}"].iloc[-1]
        latest_turn = close_df[f"turnover_rate_{PERIODS}"].iloc[-1]
        vol_mean = close_df[f"std_{PERIODS}"].mean()
        turn_mean = close_df[f"turnover_rate_{PERIODS}"].mean()

        vol_state = "高位" if latest_vol > vol_mean else "低位"
        turn_state = "高位" if latest_turn > turn_mean else "低位"

        print(f"\n  === 当前市场状态判断 ===")
        print(f"  波动率状态: {vol_state} (最新:{latest_vol:.4f}, 均值:{vol_mean:.4f})")
        print(
            f"  换手率状态: {turn_state} (最新:{latest_turn:.4f}, 均值:{turn_mean:.4f})"
        )

        if vol_state == "高位" and turn_state == "低位":
            market_regime = "熊市特征"
            strategy = "防守为主，高股息策略"
        elif vol_state == "高位" and turn_state == "高位":
            market_regime = "牛市特征"
            strategy = "动量策略满仓"
        elif vol_state == "低位" and turn_state == "高位":
            market_regime = "上升初期"
            strategy = "逢低布局，行业轮动"
        else:  # 低位+低位
            market_regime = "震荡市"
            strategy = "降低仓位，观望为主"

        print(f"  市场状态: {market_regime}")
        print(f"  建议策略: {strategy}")

    else:
        print("  换手率数据不足，无法构建完整牛熊指标")

except Exception as e:
    print(f"  牛熊指标构建失败: {e}")

# ---- 市场状态历史分析 ----
print("\n【5】市场状态历史分析...")
try:
    if "kernel_index" in close_df.columns and not close_df["kernel_index"].isna().all():
        # 计算牛熊指标的分位数
        ki_values = close_df["kernel_index"].dropna()

        if len(ki_values) > 0:
            q25 = ki_values.quantile(0.25)
            q50 = ki_values.quantile(0.50)
            q75 = ki_values.quantile(0.75)

            latest_ki = ki_values.iloc[-1]

            if latest_ki < q25:
                ki_state = "极低 (强烈看多)"
                position = "80-100%"
            elif latest_ki < q50:
                ki_state = "偏低 (看多)"
                position = "60-80%"
            elif latest_ki < q75:
                ki_state = "偏高 (看空)"
                position = "30-50%"
            else:
                ki_state = "极高 (强烈看空)"
                position = "0-20%"

            print(f"\n  === 牛熊指标分位分析 ===")
            print(f"  25分位: {q25:.4f}")
            print(f"  50分位: {q50:.4f}")
            print(f"  75分位: {q75:.4f}")
            print(f"  当前值: {latest_ki:.4f}")
            print(f"  指标状态: {ki_state}")
            print(f"  建议仓位: {position}")

except Exception as e:
    print(f"  历史分析失败: {e}")

print("\n" + "=" * 70)
print("波动率+换手率牛熊指标策略回测完成!")
print("=" * 70)
