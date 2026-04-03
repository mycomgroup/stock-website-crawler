# RSRS 三版本计算与挂接验证脚本（Notebook 格式）
# 验证 V4 右偏标准分 / V10 钝化 RSRS / V11 成交额加权+钝化
# 目标：确认三版本信号质量及挂接接口逻辑正确性

import numpy as np
import pandas as pd
import statsmodels.api as sm

print("=== RSRS 三版本计算与挂接验证开始 ===")

try:
    # ========================
    # 1. 参数配置
    # ========================
    security = "000300.XSHG"
    start_date = "2020-01-01"
    end_date = "2025-12-31"

    # V4 参数
    V4_N = 18
    V4_M = 300
    V4_BUY = 0.8
    V4_SELL = -0.8

    # V10 参数
    V10_N = 18
    V10_M = 700
    V10_BUY = 0.7
    V10_SELL = -0.7

    # V11 参数
    V11_N = 19
    V11_M = 500
    V11_BUY = 0.8
    V11_SELL = -0.8

    print(f"标的: {security}")
    print(f"区间: {start_date} ~ {end_date}")
    print(f"V4: N={V4_N}, M={V4_M}, 阈值=±{V4_BUY}")
    print(f"V10: N={V10_N}, M={V10_M}, 阈值=±{V10_BUY}")
    print(f"V11: N={V11_N}, M={V11_M}, 阈值=±{V11_BUY}")

    # ========================
    # 2. 获取数据
    # ========================
    # 获取足够的历史数据用于初始化
    max_lookback = max(V4_M, V10_M, V11_M) + max(V4_N, V10_N, V11_N) + 100
    print(f"\n需要历史数据: {max_lookback} 根K线")

    bars = get_price(
        security,
        start_date="2015-01-01",
        end_date=end_date,
        frequency="1d",
        fields=["high", "low", "close", "volume", "total_turnover"],
    )

    if bars is None or len(bars) < max_lookback:
        print(f"ERROR: 数据不足，仅获取到 {len(bars) if bars is not None else 0} 根K线")
    else:
        print(f"获取到 {len(bars)} 根K线")

        highs = bars["high"].astype(float).values
        lows = bars["low"].astype(float).values
        closes = bars["close"].astype(float).values
        amounts = bars["total_turnover"].astype(float).values

        # ========================
        # 3. 核心计算函数
        # ========================
        def compute_beta_series(high, low, N, weights=None):
            """计算滚动 OLS 斜率序列: High = α + β × Low"""
            betas = []
            r2s = []
            for i in range(N, len(high)):
                h = high[i - N : i]
                l = low[i - N : i]
                X = sm.add_constant(l)
                try:
                    if weights is not None:
                        w = weights[i - N : i]
                        model = sm.WLS(h, X, weights=w).fit()
                    else:
                        model = sm.OLS(h, X).fit()
                    betas.append(model.params[1])
                    r2s.append(model.rsquared)
                except:
                    betas.append(np.nan)
                    r2s.append(np.nan)
            return np.array(betas), np.array(r2s)

        def zscore_last(series, M):
            """计算最后一个值的 Z-Score"""
            valid = series[-M:][~np.isnan(series[-M:])]
            if len(valid) < M * 0.5:
                return np.nan
            mu = np.mean(valid)
            sigma = np.std(valid)
            if sigma == 0:
                return 0.0
            return (series[-1] - mu) / sigma

        def classify_signal(value, buy_th, sell_th):
            if np.isnan(value):
                return "neutral"
            if value > buy_th:
                return "bullish"
            elif value < sell_th:
                return "bearish"
            return "neutral"

        # ========================
        # 4. 计算 V4 右偏标准分
        # ========================
        print("\n--- 计算 V4 右偏标准分 ---")
        v4_betas, v4_r2s = compute_beta_series(highs, lows, V4_N)
        v4_z = zscore_last(v4_betas, V4_M)
        v4_rsrs = v4_z * v4_betas[-1] * v4_r2s[-1] if not np.isnan(v4_z) else np.nan
        v4_signal = classify_signal(v4_rsrs, V4_BUY, V4_SELL)

        print(f"  beta={v4_betas[-1]:.4f}")
        print(f"  R²={v4_r2s[-1]:.4f}")
        print(f"  Z-Score={v4_z:.4f}")
        print(f"  RSRS(V4)={v4_rsrs:.4f}")
        print(f"  信号: {v4_signal}")

        # ========================
        # 5. 计算 V10 钝化 RSRS
        # ========================
        print("\n--- 计算 V10 钝化 RSRS ---")
        v10_betas, v10_r2s = compute_beta_series(highs, lows, V10_N)

        # 计算收益率波动率分位数
        returns = np.diff(closes) / closes[:-1]
        vol_series = np.full(len(closes), np.nan)
        for i in range(V10_N, len(returns) + 1):
            vol_series[i] = np.std(returns[i - V10_N : i])

        # 滚动分位数
        vol_quantile = np.full(len(vol_series), np.nan)
        for i in range(V10_M, len(vol_series)):
            valid = vol_series[i - V10_M : i][~np.isnan(vol_series[i - V10_M : i])]
            if len(valid) > 0:
                vol_quantile[i] = np.median(valid)  # 50% 分位数

        # 对齐索引
        v10_offset = len(highs) - len(v10_betas)
        vol_q = vol_quantile[-1] if not np.isnan(vol_quantile[-1]) else 0.5
        v10_z = zscore_last(v10_betas, V10_M)
        v10_rsrs = v10_z * v10_r2s[-1] * vol_q if not np.isnan(v10_z) else np.nan
        v10_signal = classify_signal(v10_rsrs, V10_BUY, V10_SELL)

        print(f"  beta={v10_betas[-1]:.4f}")
        print(f"  R²={v10_r2s[-1]:.4f}")
        print(f"  Z-Score={v10_z:.4f}")
        print(f"  Vol Quantile={vol_q:.4f}")
        print(f"  RSRS(V10)={v10_rsrs:.4f}")
        print(f"  信号: {v10_signal}")

        # ========================
        # 6. 计算 V11 成交额加权+钝化 RSRS
        # ========================
        print("\n--- 计算 V11 成交额加权+钝化 RSRS ---")

        # 成交额权重（归一化到窗口内）
        def compute_amount_weights(amounts, N):
            weights = np.full(len(amounts), 1.0 / N)
            for i in range(N, len(amounts)):
                w = amounts[i - N : i]
                w_sum = np.sum(w)
                if w_sum > 0:
                    weights[i] = 1.0  # 标记位，实际在计算时归一化
            return weights

        v11_betas, v11_r2s = compute_beta_series(highs, lows, V11_N, amounts)

        # 钝化：使用高低点收益率的波动率
        hl_returns = (highs - lows) / lows
        hl_vol = np.full(len(hl_returns), np.nan)
        for i in range(V11_N, len(hl_returns)):
            hl_vol[i] = np.std(hl_returns[i - V11_N : i])

        hl_vol_q = np.full(len(hl_vol), np.nan)
        for i in range(V11_M, len(hl_vol)):
            valid = hl_vol[i - V11_M : i][~np.isnan(hl_vol[i - V11_M : i])]
            if len(valid) > 0:
                hl_vol_q[i] = np.median(valid)

        hl_q = hl_vol_q[-1] if not np.isnan(hl_vol_q[-1]) else 0.5
        v11_z = zscore_last(v11_betas, V11_M)
        v11_rsrs = v11_z * v11_r2s[-1] * hl_q if not np.isnan(v11_z) else np.nan
        v11_signal = classify_signal(v11_rsrs, V11_BUY, V11_SELL)

        print(f"  beta={v11_betas[-1]:.4f}")
        print(f"  R²={v11_r2s[-1]:.4f}")
        print(f"  Z-Score={v11_z:.4f}")
        print(f"  HL Vol Quantile={hl_q:.4f}")
        print(f"  RSRS(V11)={v11_rsrs:.4f}")
        print(f"  信号: {v11_signal}")

        # ========================
        # 7. 信号一致性检查
        # ========================
        print("\n=== 信号一致性检查 ===")
        signals = {"V4": v4_signal, "V10": v10_signal, "V11": v11_signal}
        for name, sig in signals.items():
            print(f"  {name}: {sig}")

        bullish_count = sum(1 for s in signals.values() if s == "bullish")
        bearish_count = sum(1 for s in signals.values() if s == "bearish")
        neutral_count = sum(1 for s in signals.values() if s == "neutral")

        print(f"\n  看多: {bullish_count}/3")
        print(f"  看空: {bearish_count}/3")
        print(f"  中性: {neutral_count}/3")

        # ========================
        # 8. 主仓模拟调节
        # ========================
        print("\n=== 主仓仓位模拟 ===")
        regime_states = {
            "底部试错": 0.30,
            "震荡轮动": 0.35,
            "趋势进攻": 0.40,
            "高估防守": 0.15,
        }
        state_caps = {
            "底部试错": 0.35,
            "震荡轮动": 0.40,
            "趋势进攻": 0.45,
            "高估防守": 0.15,
        }

        for state, base in regime_states.items():
            pos = base
            cap = state_caps[state]

            # V11 veto
            if v11_signal == "bearish":
                pos -= 0.05
            # V10 confirm
            elif v10_signal == "bullish":
                pos += 0.05
            # V4 + V10 双重确认
            elif v4_signal == "bullish" and v10_signal == "bullish":
                pos += 0.05

            # V10 反向
            if v10_signal == "bearish" and v11_signal != "bearish":
                pos -= 0.05

            pos = max(0.10, min(pos, cap))
            print(f"  {state}: 基准={base:.0%} → 调节后={pos:.0%} (上限={cap:.0%})")

        # ========================
        # 9. 机会仓模拟调节
        # ========================
        print("\n=== 机会仓仓位模拟 ===")
        opp_states = {"关闭": 0.0, "防守": 0.50, "正常": 1.00, "进攻": 1.20}

        for state, base in opp_states.items():
            if base == 0:
                print(f"  {state}: 基准={base:.0%} → 调节后=0% (已关闭)")
                continue

            discount = 1.0
            if v11_signal == "bearish":
                discount = 0.0
            elif v4_signal == "bearish":
                discount = 0.5

            final = base * discount
            print(
                f"  {state}: 基准={base:.0%} → 折扣={discount:.1f} → 调节后={final:.0%}"
            )

        # ========================
        # 10. 总结
        # ========================
        print("\n=== 验证总结 ===")
        print(f"V4 右偏标准分: RSRS={v4_rsrs:.4f}, 信号={v4_signal}")
        print(f"V10 钝化 RSRS: RSRS={v10_rsrs:.4f}, 信号={v10_signal}")
        print(f"V11 成交额加权+钝化: RSRS={v11_rsrs:.4f}, 信号={v11_signal}")
        print(f"\n主仓 veto 触发: {v11_signal == 'bearish'}")
        print(f"机会仓 veto 触发: {v11_signal == 'bearish' or v4_signal == 'bearish'}")
        print("\n=== RSRS 三版本计算与挂接验证完成 ===")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback

    traceback.print_exc()
    print("\n=== RSRS 验证失败 ===")
