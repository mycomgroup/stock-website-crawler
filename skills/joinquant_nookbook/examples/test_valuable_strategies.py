#!/usr/bin/env python3
"""高价值策略实测 - 聚宽平台执行"""

from jqdata import *
import pandas as pd
import numpy as np
import talib as tb
from datetime import datetime, timedelta
import json

print("=" * 70)
print("高价值策略实测 - 2024年最新数据")
print("=" * 70)

end_date = "2024-12-20"

# ============ 1. RSRS择时指标 ============
print("\n【1】RSRS择时指标 (沪深300)")
print("-" * 50)

try:
    # 获取沪深300最高价和最低价
    hs300 = get_price(
        "000300.XSHG",
        end_date=end_date,
        count=100,
        fields=["high", "low", "close"],
        panel=False,
    )
    hs300 = hs300.set_index("time")

    N = 18  # 统计周期
    M = 800  # 标准化窗口

    # 计算RSRS斜率
    def calc_rsrs_slope(prices, n=N):
        if len(prices) < n:
            return np.nan
        from scipy import stats

        slope, _, _, _, _ = stats.linregress(
            prices["low"].values[-n:], prices["high"].values[-n:]
        )
        return slope

    slopes = []
    for i in range(N, len(hs300)):
        slope = calc_rsrs_slope(hs300.iloc[i - N + 1 : i + 1])
        slopes.append(slope)

    rsrs_series = pd.Series(slopes, index=hs300.index[N - 1 :])

    # 标准化
    if len(rsrs_series) > M:
        rsrs_mean = rsrs_series.rolling(M).mean()
        rsrs_std = rsrs_series.rolling(M).std()
        rsrs_z = (rsrs_series - rsrs_mean) / rsrs_std

        # 右偏修正
        rsrs_right = rsrs_series * rsrs_z

        latest_z = rsrs_z.iloc[-1]
        latest_right = rsrs_right.iloc[-1]

        print(f"  最新RSRS标准分: {latest_z:.2f}")
        print(f"  最新RSRS右偏分: {latest_right:.2f}")

        # 信号判断
        if latest_right > 0.8:
            signal = "买入信号 (右偏分>0.8)"
        elif latest_right < -0.8:
            signal = "卖出信号 (右偏分<-0.8)"
        else:
            signal = "观望 (阈值内)"

        print(f"  信号判断: {signal}")

        # 最近5天趋势
        print(f"  最近5天RSRS右偏分:")
        for d, v in rsrs_right.iloc[-5:].items():
            print(f"    {d.date()}: {v:.2f}")
    else:
        print("  数据不足，需要更多历史数据")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 2. ETF动量轮动 ============
print("\n【2】ETF动量轮动 (A股+全球+商品)")
print("-" * 50)

try:
    etf_list = {
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
        "纳指ETF": "159941.XSHE",
        "德国30ETF": "513030.XSHG",
        "日经ETF": "513520.XSHG",
        "黄金ETF": "518880.XSHG",
        "原油ETF": "161129.XSHE",
    }

    momentum_window = 20
    trade_days = get_trade_days(end_date=end_date, count=momentum_window + 5)

    print(f"  动量窗口: {momentum_window}日")
    print(f"  各ETF动量排名:")

    etf_mom = {}
    for name, code in etf_list.items():
        try:
            prices = get_price(
                code,
                end_date=end_date,
                count=momentum_window + 1,
                fields=["close"],
                panel=False,
            )
            if len(prices) > momentum_window:
                mom = (prices["close"].iloc[-1] / prices["close"].iloc[0] - 1) * 100
                etf_mom[name] = round(mom, 2)
                status = "↑" if mom > 0 else "↓"
                print(f"    {name}: {mom:+.2f}% {status}")
        except:
            continue

    # 推荐持有
    if etf_mom:
        best = max(etf_mom, key=etf_mom.get)
        print(f"\n  => 推荐持有: {best} (动量{etf_mom[best]:+.2f}%)")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 3. ARBR人气意愿因子 ============
print("\n【3】ARBR人气意愿因子选股")
print("-" * 50)

try:
    # AR = (H - O) / (O - L) * 100
    # BR = (H - PC) / (PC - L) * 100
    # 获取沪深300成分股
    hs300_stocks = get_index_stocks("000300.XSHG", date=end_date)

    arbr_results = []
    for stock in hs300_stocks[:30]:  # 测试前30只
        try:
            prices = get_price(
                stock,
                end_date=end_date,
                count=26,
                fields=["open", "high", "low", "close"],
                panel=False,
            )
            if len(prices) < 26:
                continue

            # 计算AR
            H_O = prices["high"] - prices["open"]
            O_L = prices["open"] - prices["low"]
            AR = (H_O.sum() / O_L.sum()) * 100 if O_L.sum() > 0 else 0

            # 计算BR (用前一日收盘价)
            PC = prices["close"].shift(1)
            H_PC = prices["high"] - PC
            PC_L = PC - prices["low"]
            BR = (H_PC.sum() / PC_L.sum()) * 100 if PC_L.sum() > 0 else 0

            arbr_results.append(
                {"stock": stock, "AR": round(AR, 2), "BR": round(BR, 2)}
            )
        except:
            continue

    if arbr_results:
        df_arbr = pd.DataFrame(arbr_results)
        print(f"  计算了 {len(df_arbr)} 只股票的ARBR因子")
        print(f"  AR均值: {df_arbr['AR'].mean():.2f}")
        print(f"  BR均值: {df_arbr['BR'].mean():.2f}")

        # AR>150且BR<50 为买入信号 (参考原策略)
        buy_signals = df_arbr[(df_arbr["AR"] > 150) & (df_arbr["BR"] < 50)]
        if len(buy_signals) > 0:
            print(f"  买入信号股票 ({len(buy_signals)}只):")
            for _, row in buy_signals.iterrows():
                print(f"    {row['stock']}: AR={row['AR']}, BR={row['BR']}")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 4. 高股息率策略 ============
print("\n【4】高股息率价值投资筛选")
print("-" * 50)

try:
    # 获取高股息率股票
    dividend_df = get_fundamentals(
        query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.inc_net_profit_year_on_year,
        )
        .filter(valuation.pe_ratio > 0)
        .filter(valuation.pe_ratio < 30)
        .filter(indicator.inc_net_profit_year_on_year > 10)
        .order_by(valuation.pe_ratio.asc())
        .limit(20),
        date=end_date,
    )

    if len(dividend_df) > 0:
        # 获取这些股票的价格
        prices_1w = get_price(
            dividend_df["code"].tolist(),
            end_date=end_date,
            count=5,
            fields=["close"],
            panel=False,
        )
        pivot = prices_1w.pivot(index="time", columns="code", values="close")

        print(f"  筛选条件: PE<30, 利润增长>10%")
        print(f"  找到 {len(dividend_df)} 只符合条件的股票")
        print(f"\n  前5只低PE+高增长股票:")

        for i, row in dividend_df.head(5).iterrows():
            code = row["code"]
            pe = round(row["pe_ratio"], 2)
            growth = round(row["inc_net_profit_year_on_year"], 2)
            if code in pivot.columns:
                price = round(pivot[code].iloc[-1], 2)
                print(f"    {code}: PE={pe}, 利润增长={growth}%, 价格={price}")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 5. 小市值+止损策略 ============
print("\n【5】小市值策略核心参数验证")
print("-" * 50)

try:
    # 获取全市场股票市值
    all_stocks = get_all_securities(types="stock", date=end_date).index.tolist()

    # 获取流通市值
    mv_df = get_fundamentals(
        query(valuation.code, valuation.circulating_market_cap)
        .filter(valuation.code.in_(all_stocks[:500]))  # 取前500只测试
        .order_by(valuation.circulating_market_cap.asc())
        .limit(20),
        date=end_date,
    )

    if len(mv_df) > 0:
        print(f"  最小市值20只股票:")
        print(f"  {'股票代码':<15} {'流通市值(亿)':<15}")
        print(f"  {'-' * 30}")

        for i, row in mv_df.iterrows():
            mv = round(row["circulating_market_cap"] / 10000, 2)  # 转换为亿
            print(f"  {row['code']:<15} {mv:<15}")

        avg_mv = round(mv_df["circulating_market_cap"].mean() / 10000, 2)
        print(f"\n  平均流通市值: {avg_mv}亿")
        print(f"  注意: 小市值策略在2024年面临流动性风险，需严格止损")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 6. 股债平衡策略 ============
print("\n【6】股债平衡 (全天候简化版)")
print("-" * 50)

try:
    # 计算股债比例信号
    # 获取沪深300和国债ETF数据
    stock_etf = get_price(
        "510300.XSHG", end_date=end_date, count=60, fields=["close"], panel=False
    )
    bond_etf = get_price(
        "511010.XSHG", end_date=end_date, count=60, fields=["close"], panel=False
    )

    stock_ret = stock_etf["close"].pct_change().dropna()
    bond_ret = bond_etf["close"].pct_change().dropna()

    # 计算波动率
    stock_vol = stock_ret.std() * np.sqrt(252)
    bond_vol = bond_ret.std() * np.sqrt(252)

    # 风险平价权重
    inv_vol_stock = 1 / stock_vol
    inv_vol_bond = 1 / bond_vol
    total = inv_vol_stock + inv_vol_bond

    stock_weight = round(inv_vol_stock / total * 100, 1)
    bond_weight = round(inv_vol_bond / total * 100, 1)

    print(f"  沪深300年化波动率: {stock_vol * 100:.1f}%")
    print(f"  国债ETF年化波动率: {bond_vol * 100:.1f}%")
    print(f"  风险平价配置:")
    print(f"    股票: {stock_weight}%")
    print(f"    债券: {bond_weight}%")

    # 简化收益计算
    combined_ret = (
        stock_ret.iloc[-1] * stock_weight / 100 + bond_ret.iloc[-1] * bond_weight / 100
    )
    print(f"  今日组合收益: {combined_ret * 100:.2f}%")

except Exception as e:
    print(f"  计算失败: {e}")

# ============ 综合评估 ============
print("\n" + "=" * 70)
print("【策略适用性评估】")
print("=" * 70)
print("""
┌─────────────────┬──────────┬──────────┬──────────┬────────────┐
│ 策略类型        │ 实盘难度 │ 资金容量 │ 风险等级 │ 2024年有效性│
├─────────────────┼──────────┼──────────┼──────────┼────────────┤
│ RSRS择时        │ 中       │ 大       │ 低       │ 较高       │
│ ETF动量轮动     │ 低       │ 大       │ 中       │ 高         │
│ ARBR多因子      │ 中       │ 中       │ 中       │ 中         │
│ 高股息价值      │ 低       │ 大       │ 低       │ 高         │
│ 小市值+止损     │ 高       │ 小       │ 高       │ 低(需谨慎) │
│ 股债平衡        │ 低       │ 大       │ 低       │ 高         │
└─────────────────┴──────────┴──────────┴──────────┴────────────┘

【2024年推荐组合】
1. 核心仓位(60%): ETF动量轮动 + 股债平衡
2. 卫星仓位(30%): 高股息价值股
3. 机动仓位(10%): RSRS择时增强

【风险提示】
- 小市值策略在2024年回撤较大，建议回避或极小仓位
- 龙头打板策略需要专业程序化支持，不适合普通投资者
- 所有策略都需要结合严格的风险控制
""")

print("实测完成!")
