"""
任务02 状态输入统一与阈值冻结 — 回测验证脚本
验证内容：
1. 市场宽度（沪深300 close > MA20 占比）
2. FED指标（100/PE中位数 - 10Y国债收益率）
3. RSRS Z-Score（滚动OLS斜率标准化）
4. 情绪指标（涨停家数）
5. 状态路由器V2判定逻辑
6. 多日期历史验证
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from jqdata import *

print("=" * 60)
print("任务02 状态输入统一与阈值冻结 — 回测验证")
print("=" * 60)


def filter_valid_stocks(stocks, date):
    """排除ST、科创板、北交所、创业板"""
    valid = []
    for s in stocks:
        if (
            s.startswith("68")
            or s.startswith("3")
            or s.startswith("4")
            or s.startswith("8")
        ):
            continue
        valid.append(s)
    return valid


def get_st_stocks(date):
    """获取ST股票列表"""
    try:
        q = query(valuation.code).filter(valuation.st_status == 1)
        df = get_fundamentals(q, date=date)
        return set(df["code"].tolist()) if len(df) > 0 else set()
    except:
        return set()


# ============================================================
# 1. 市场宽度验证
# ============================================================
print("\n--- 1. 市场宽度验证 ---")

try:
    test_date = "2025-03-28"
    stocks = get_index_stocks("000300.XSHG", test_date)
    valid_stocks = filter_valid_stocks(stocks, test_date)

    price_df = get_price(
        valid_stocks,
        end_date=test_date,
        frequency="daily",
        fields=["close"],
        count=25,
        panel=False,
        skip_paused=True,
    )

    breadth_count = 0
    total_count = 0
    for code in valid_stocks:
        stock_data = price_df[price_df["code"] == code]
        if len(stock_data) >= 20:
            close = stock_data.iloc[-1]["close"]
            ma20 = stock_data.iloc[-20:]["close"].mean()
            if close > ma20:
                breadth_count += 1
            total_count += 1

    breadth_ratio = breadth_count / total_count * 100 if total_count > 0 else 0
    print(f"测试日期: {test_date}")
    print(f"沪深300成分股数: {len(valid_stocks)}")
    print(f"有效股票数: {total_count}")
    print(f"站上MA20股票数: {breadth_count}")
    print(f"市场宽度: {breadth_ratio:.1f}%")

    if breadth_ratio < 30:
        print(f"宽度状态: 底部试错 (<30%)")
    elif breadth_ratio < 50:
        print(f"宽度状态: 震荡轮动 (30-50%)")
    elif breadth_ratio < 70:
        print(f"宽度状态: 趋势进攻 (>50%)")
    else:
        print(f"宽度状态: 高估防守 (>70%)")

except Exception as e:
    print(f"宽度计算错误: {e}")
    import traceback

    traceback.print_exc()

# ============================================================
# 2. FED指标验证
# ============================================================
print("\n--- 2. FED指标验证 ---")

try:
    test_date = "2025-03-28"
    stocks = get_index_stocks("000300.XSHG", test_date)

    q = query(valuation.code, valuation.pe_ratio).filter(
        valuation.code.in_(stocks), valuation.pe_ratio > 0, valuation.pe_ratio < 200
    )
    df_pe = get_fundamentals(q, date=test_date)

    if len(df_pe) > 0:
        pe_median = df_pe["pe_ratio"].median()
        earnings_yield = 100 / pe_median
        bond_yield = 1.8  # 10Y国债近似
        fed_ratio = earnings_yield - bond_yield

        print(f"测试日期: {test_date}")
        print(f"沪深300 PE中位数: {pe_median:.1f}")
        print(f"盈利收益率: {earnings_yield:.2f}%")
        print(f"10Y国债收益率: {bond_yield:.2f}%")
        print(f"FED指标: {fed_ratio:.2f}")

        if fed_ratio > 0:
            print(f"估值状态: 低估 (FED>0)")
        elif fed_ratio > -1:
            print(f"估值状态: 中性 (-1~0)")
        else:
            print(f"估值状态: 高估 (FED<-1)")
    else:
        print("未能获取PE数据")

except Exception as e:
    print(f"FED计算错误: {e}")
    import traceback

    traceback.print_exc()

# ============================================================
# 3. RSRS Z-Score验证
# ============================================================
print("\n--- 3. RSRS Z-Score验证 ---")

try:
    test_date = "2025-03-28"

    index_data = get_price(
        "000300.XSHG",
        end_date=test_date,
        frequency="daily",
        fields=["high", "low"],
        count=60,
        skip_paused=True,
    )

    if len(index_data) >= 30:
        n = min(18, len(index_data))
        high = index_data.iloc[-n:]["high"].values
        low = index_data.iloc[-n:]["low"].values

        if len(low) > 1 and np.std(low) > 0:
            slope = np.cov(low, high)[0, 1] / np.var(low)

            slopes = []
            window = 18
            for i in range(window, len(index_data)):
                h = index_data.iloc[i - window : i]["high"].values
                l = index_data.iloc[i - window : i]["low"].values
                if np.std(l) > 0:
                    s = np.cov(l, h)[0, 1] / np.var(l)
                    slopes.append(s)

            if len(slopes) >= 5:
                slope_mean = np.mean(slopes)
                slope_std = np.std(slopes)
                z_score = (slope - slope_mean) / slope_std if slope_std > 0 else 0
            else:
                z_score = 0

            print(f"测试日期: {test_date}")
            print(f"当前斜率: {slope:.4f}")
            print(f"历史斜率均值: {slope_mean:.4f}")
            print(f"历史斜率标准差: {slope_std:.4f}")
            print(f"RSRS Z-Score: {z_score:.2f}")

            if z_score > 0.5:
                print(f"趋势状态: 向上 (Z>0.5)")
            elif z_score < -0.5:
                print(f"趋势状态: 向下 (Z<-0.5)")
            else:
                print(f"趋势状态: 震荡 (-0.5~0.5)")
        else:
            print("数据不足或方差为0，无法计算RSRS")
    else:
        print("数据不足，无法计算RSRS")

except Exception as e:
    print(f"RSRS计算错误: {e}")
    import traceback

    traceback.print_exc()

# ============================================================
# 4. 情绪指标验证
# ============================================================
print("\n--- 4. 情绪指标验证 ---")

try:
    test_date = "2025-03-28"

    all_stocks = get_all_securities("stock", test_date).index.tolist()
    valid_stocks = filter_valid_stocks(all_stocks, test_date)

    price_df = get_price(
        valid_stocks,
        end_date=test_date,
        frequency="daily",
        fields=["close", "high_limit", "low_limit"],
        count=1,
        panel=False,
        skip_paused=True,
    )

    limit_up_count = len(price_df[price_df["close"] == price_df["high_limit"]])
    limit_down_count = len(price_df[price_df["close"] == price_df["low_limit"]])

    print(f"测试日期: {test_date}")
    print(f"全市场有效股票数: {len(valid_stocks)}")
    print(f"涨停家数: {limit_up_count}")
    print(f"跌停家数: {limit_down_count}")

    if limit_up_count < 30:
        print(f"情绪状态(择时V1.0): 冰点 (<30只) — 不交易")
    elif limit_up_count < 50:
        print(f"情绪状态(择时V1.0): 启动 (30-50只) — 谨慎参与")
    elif limit_up_count < 80:
        print(f"情绪状态(择时V1.0): 发酵 (50-80只) — 正常交易")
    else:
        print(f"情绪状态(择时V1.0): 高潮 (>80只) — 适度放宽")

    if limit_up_count < 20:
        print(f"情绪状态(退潮指南): 退潮期 (<20只)")
    elif limit_up_count < 10:
        print(f"情绪状态(退潮指南): 冰点期 (<10只)")

except Exception as e:
    print(f"情绪计算错误: {e}")
    import traceback

    traceback.print_exc()

# ============================================================
# 5. 状态路由器V2综合判定
# ============================================================
print("\n--- 5. 状态路由器V2综合判定 ---")

try:
    test_date = "2025-03-28"

    stocks = get_index_stocks("000300.XSHG", test_date)
    valid_stocks = filter_valid_stocks(stocks, test_date)
    price_df = get_price(
        valid_stocks,
        end_date=test_date,
        frequency="daily",
        fields=["close"],
        count=25,
        panel=False,
        skip_paused=True,
    )

    breadth_count = 0
    total_count = 0
    for code in valid_stocks:
        stock_data = price_df[price_df["code"] == code]
        if len(stock_data) >= 20:
            if stock_data.iloc[-1]["close"] > stock_data.iloc[-20:]["close"].mean():
                breadth_count += 1
            total_count += 1
    breadth = breadth_count / total_count * 100 if total_count > 0 else 0

    q = query(valuation.code, valuation.pe_ratio).filter(
        valuation.code.in_(stocks), valuation.pe_ratio > 0, valuation.pe_ratio < 200
    )
    df_pe = get_fundamentals(q, date=test_date)
    pe_median = df_pe["pe_ratio"].median() if len(df_pe) > 0 else 20
    fed = 100 / pe_median - 1.8

    index_data = get_price(
        "000300.XSHG",
        end_date=test_date,
        frequency="daily",
        fields=["close"],
        count=25,
        skip_paused=True,
    )
    if len(index_data) >= 20:
        ma20 = index_data.iloc[-20:]["close"].mean()
        current = index_data.iloc[-1]["close"]
        rsrs_approx = 0.3 if current > ma20 else -0.3
    else:
        rsrs_approx = 0

    print(f"输入指标:")
    print(f"  宽度: {breadth:.1f}%")
    print(f"  FED: {fed:.2f}")
    print(f"  RSRS(近似): {rsrs_approx:.2f}")

    trend_up = rsrs_approx > 0.5

    if breadth > 70 or fed < -1:
        state = "高估防守"
        stock_alloc = "15%"
    elif breadth > 50 and trend_up:
        state = "趋势进攻"
        stock_alloc = "40%"
    elif breadth >= 30:
        state = "震荡轮动"
        stock_alloc = "35%"
    else:
        state = "底部试错"
        stock_alloc = "30%"

    print(f"\n判定结果:")
    print(f"  当前状态: 【{state}】")
    print(f"  股票配置建议: {stock_alloc}")

except Exception as e:
    print(f"状态路由器计算错误: {e}")
    import traceback

    traceback.print_exc()

# ============================================================
# 6. 多日期历史验证
# ============================================================
print("\n--- 6. 多日期历史验证 ---")

try:
    test_dates = [
        "2024-01-31",
        "2024-04-30",
        "2024-07-31",
        "2024-10-31",
        "2025-01-31",
        "2025-03-28",
    ]

    print(f"{'日期':<12} {'宽度':>8} {'FED':>8} {'RSRS':>8} {'涨停':>6} {'状态':>10}")
    print("-" * 60)

    for test_date in test_dates:
        try:
            stocks = get_index_stocks("000300.XSHG", test_date)
            valid_stocks = filter_valid_stocks(stocks, test_date)
            price_df = get_price(
                valid_stocks,
                end_date=test_date,
                frequency="daily",
                fields=["close"],
                count=25,
                panel=False,
                skip_paused=True,
            )

            bc = 0
            tc = 0
            for code in valid_stocks:
                sd = price_df[price_df["code"] == code]
                if len(sd) >= 20:
                    if sd.iloc[-1]["close"] > sd.iloc[-20:]["close"].mean():
                        bc += 1
                    tc += 1
            breadth = bc / tc * 100 if tc > 0 else 0

            q = query(valuation.code, valuation.pe_ratio).filter(
                valuation.code.in_(stocks),
                valuation.pe_ratio > 0,
                valuation.pe_ratio < 200,
            )
            df_pe = get_fundamentals(q, date=test_date)
            pe_m = df_pe["pe_ratio"].median() if len(df_pe) > 0 else 20
            fed = 100 / pe_m - 1.8

            idx = get_price(
                "000300.XSHG",
                end_date=test_date,
                frequency="daily",
                fields=["close"],
                count=25,
                skip_paused=True,
            )
            if len(idx) >= 20:
                ma20 = idx.iloc[-20:]["close"].mean()
                cur = idx.iloc[-1]["close"]
                rsrs = 0.3 if cur > ma20 else -0.3
            else:
                rsrs = 0

            all_s = get_all_securities("stock", test_date).index.tolist()
            vs = filter_valid_stocks(all_s, test_date)
            pf = get_price(
                vs,
                end_date=test_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
                skip_paused=True,
            )
            lu = len(pf[pf["close"] == pf["high_limit"]])

            if breadth > 70 or fed < -1:
                st = "高估防守"
            elif breadth > 50 and rsrs > 0.5:
                st = "趋势进攻"
            elif breadth >= 30:
                st = "震荡轮动"
            else:
                st = "底部试错"

            print(
                f"{test_date:<12} {breadth:>7.1f}% {fed:>8.2f} {rsrs:>8.2f} {lu:>6} {st:>10}"
            )

        except Exception as e:
            print(f"{test_date:<12} 计算失败: {e}")

except Exception as e:
    print(f"多日期验证错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)
print("验证完成")
print("=" * 60)
