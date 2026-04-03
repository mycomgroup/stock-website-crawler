"""
RSRS 复合过滤增量验证脚本
=========================

用途：在同一底座（RFScore7 PB10 Optimized）上，对比 4 档过滤方案：
  Tier 0: 无过滤
  Tier 1: RSRS 单独过滤
  Tier 2: RSRS + 宽度
  Tier 3: RSRS + 宽度 + 情绪

运行环境：聚宽 JoinQuant 研究环境
回测区间：2018-01-01 至 2025-12-31
"""

from jqdata import *
import numpy as np
import pandas as pd
import statsmodels.api as sm


# ============================================================
# 一、RSRS 模块（与 05_rsrs_optimized.py 同源口径）
# ============================================================
class RSRSFilter:
    """RSRS 右偏标准分过滤器"""

    def __init__(self, N=18, M=300, buy_threshold=0.8, sell_threshold=-0.8):
        self.N = N
        self.M = M
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.beta_history = []
        self.r2_history = []
        self._initialized = False

    def update(self, end_date):
        """更新 RSRS 值，返回 (rsrs_right_skew, zscore, beta, r2)"""
        lookback = self.M + self.N + 50
        prices = get_price(
            "000300.XSHG",
            end_date=end_date,
            count=lookback,
            fields=["high", "low", "close"],
            panel=False,
        )
        if prices is None or len(prices) < self.M:
            return None, None, None, None

        highs = prices["high"].values
        lows = prices["low"].values

        # 初始化或增量更新
        if not self._initialized:
            for i in range(self.N, min(len(prices), self.M + self.N)):
                h = highs[i - self.N : i]
                l = lows[i - self.N : i]
                X = sm.add_constant(l)
                try:
                    model = sm.OLS(h, X).fit()
                    self.beta_history.append(model.params[1])
                    self.r2_history.append(model.rsquared)
                except:
                    continue
            self._initialized = True
            if len(self.beta_history) < self.M:
                return None, None, None, None
        else:
            h = highs[-self.N :]
            l = lows[-self.N :]
            X = sm.add_constant(l)
            try:
                model = sm.OLS(h, X).fit()
                self.beta_history.append(model.params[1])
                self.r2_history.append(model.rsquared)
            except:
                return None, None, None, None

        # 保持长度
        if len(self.beta_history) > self.M:
            self.beta_history = self.beta_history[-self.M :]
            self.r2_history = self.r2_history[-self.M :]

        beta_arr = np.array(self.beta_history)
        mu, sigma = np.mean(beta_arr), np.std(beta_arr)
        if sigma == 0:
            return None, None, None, None

        zscore = (beta_arr[-1] - mu) / sigma
        beta = beta_arr[-1]
        r2 = self.r2_history[-1] if self.r2_history else 0.5

        # 右偏标准分
        rsrs_right = zscore * beta * r2

        return rsrs_right, zscore, beta, r2

    def is_allowed(self, end_date):
        """RSRS 单独过滤：rsrs > sell_threshold 才允许持仓"""
        rsrs, _, _, _ = self.update(end_date)
        if rsrs is None:
            return True  # 数据不足时不拦截
        return rsrs > self.sell_threshold


# ============================================================
# 二、宽度模块（与任务02冻结口径一致）
# ============================================================
def calc_breadth(end_date, window=20):
    """沪深300成分股 close > MA20 的比例"""
    hs300 = get_index_stocks("000300.XSHG", date=end_date)
    prices = get_price(
        hs300, end_date=end_date, count=window, fields=["close"], panel=False
    )
    if prices is None or prices.empty:
        return 0.5
    close = prices.pivot(index="time", columns="code", values="close")
    if len(close) < window:
        return 0.5
    return float((close.iloc[-1] > close.mean()).mean())


# ============================================================
# 三、情绪模块（与择时集成文档V1.0一致）
# ============================================================
def calc_sentiment(end_date):
    """涨停数量（涨幅>=9.5%）"""
    all_stocks = get_all_securities("stock", date=end_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in ("4", "8") and s[:2] != "68"]
    sample = all_stocks[:500]

    df = get_price(
        sample,
        end_date=end_date,
        count=1,
        fields=["close", "high_limit", "low_limit"],
        panel=False,
    )
    if df is None or df.empty:
        return 30
    df = df.dropna()
    hl_count = len(df[df["close"] >= df["high_limit"] * 0.995])
    return hl_count


# ============================================================
# 四、RFScore7 因子计算（与底座同源）
# ============================================================
from jqfactor import Factor, calc_factors


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

        indicators = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicators).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(lambda x: np.where(x > 0, 1, 0)).sum(axis=1)


def get_universe(watch_date):
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]
    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=180)]
    stocks = sec.index.tolist()
    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()
    return stocks


def calc_rfscore_table(stocks, watch_date):
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)
    df = factor.basic.copy()
    df["RFScore"] = factor.fscore
    val = get_valuation(
        stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1
    )
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    df = df.join(val, how="left")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "ROA", "OCFOA", "pb_ratio", "pe_ratio"])
    df = df[
        (df["pb_ratio"] > 0)
        & (df["pe_ratio"] > 0)
        & (df["pe_ratio"] < 100)
        & (df["ROA"] > 0.5)
    ].copy()
    if df.empty:
        return df
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    return df


def choose_stocks(df, target_hold_num=15):
    if target_hold_num <= 0 or df.empty:
        return []
    primary = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()
    primary["score"] = (
        primary["RFScore"] * 100
        + primary["ROA"].rank(pct=True) * 30
        + primary["OCFOA"].rank(pct=True) * 20
        + primary["DELTA_MARGIN"].rank(pct=True) * 10
        - primary["pb_ratio"].rank(pct=True) * 10
    )
    primary = primary.sort_values("score", ascending=False)

    secondary = df[(df["RFScore"] >= 6) & (df["pb_group"] <= 3)].copy()
    secondary["score"] = (
        secondary["RFScore"] * 100
        + secondary["ROA"].rank(pct=True) * 30
        + secondary["OCFOA"].rank(pct=True) * 20
        + secondary["DELTA_MARGIN"].rank(pct=True) * 10
        - secondary["pb_ratio"].rank(pct=True) * 10
    )
    secondary = secondary.sort_values("score", ascending=False)

    picks = []
    for code in primary.index.tolist():
        if len(picks) >= target_hold_num:
            break
        picks.append(code)
    for code in secondary.index.tolist():
        if len(picks) >= target_hold_num:
            break
        if code not in picks:
            picks.append(code)
    return picks[:target_hold_num]


# ============================================================
# 五、4 档过滤逻辑
# ============================================================
def tier0_filter(end_date):
    """Tier 0: 无过滤 — 始终允许交易"""
    return True, {}


def tier1_filter(end_date, rsrs_filter):
    """Tier 1: RSRS 单独过滤"""
    allowed = rsrs_filter.is_allowed(end_date)
    rsrs, zscore, beta, r2 = rsrs_filter.update(end_date)
    return allowed, {"rsrs": rsrs, "zscore": zscore, "beta": beta, "r2": r2}


def tier2_filter(end_date, rsrs_filter, breadth_threshold=0.15):
    """Tier 2: RSRS + 宽度"""
    rsrs_allowed = rsrs_filter.is_allowed(end_date)
    breadth = calc_breadth(end_date)
    allowed = rsrs_allowed and (breadth >= breadth_threshold)
    rsrs, zscore, beta, r2 = rsrs_filter.update(end_date)
    return allowed, {"rsrs": rsrs, "zscore": zscore, "breadth": breadth}


def tier3_filter(end_date, rsrs_filter, breadth_threshold=0.15, sentiment_threshold=30):
    """Tier 3: RSRS + 宽度 + 情绪"""
    rsrs_allowed = rsrs_filter.is_allowed(end_date)
    breadth = calc_breadth(end_date)
    sentiment = calc_sentiment(end_date)
    allowed = (
        rsrs_allowed
        and (breadth >= breadth_threshold)
        and (sentiment >= sentiment_threshold)
    )
    rsrs, zscore, beta, r2 = rsrs_filter.update(end_date)
    return allowed, {
        "rsrs": rsrs,
        "zscore": zscore,
        "breadth": breadth,
        "sentiment": sentiment,
    }


# ============================================================
# 六、月度回测引擎
# ============================================================
def run_monthly_backtest(
    start_date,
    end_date,
    tier_func,
    tier_name,
    rsrs_filter=None,
    breadth_threshold=0.15,
    sentiment_threshold=30,
):
    """月度回测：记录每次调仓的信号、持仓、收益"""
    dates = get_trade_days(start_date=start_date, end_date=end_date, count=None)
    # 取每月第一个交易日
    monthly_dates = []
    last_month = None
    for d in dates:
        if d.month != last_month:
            monthly_dates.append(d)
            last_month = d.month

    results = []
    for dt in monthly_dates:
        if tier_func.__name__ == "tier0_filter":
            allowed, meta = tier0_filter(dt)
        elif tier_func.__name__ == "tier1_filter":
            allowed, meta = tier1_filter(dt, rsrs_filter)
        elif tier_func.__name__ == "tier2_filter":
            allowed, meta = tier2_filter(dt, rsrs_filter, breadth_threshold)
        else:
            allowed, meta = tier3_filter(
                dt, rsrs_filter, breadth_threshold, sentiment_threshold
            )

        # 选股
        if allowed:
            universe = get_universe(dt)
            if universe:
                df = calc_rfscore_table(universe, dt)
                picks = choose_stocks(df, target_hold_num=15)
            else:
                picks = []
        else:
            picks = []

        results.append(
            {
                "date": dt,
                "allowed": allowed,
                "hold_count": len(picks),
                "stocks": picks,
                **meta,
            }
        )

    return results


# ============================================================
# 七、主入口：运行4档对比
# ============================================================
def main():
    print("=" * 60)
    print("RSRS 复合过滤增量验证")
    print("=" * 60)

    start_date = "2018-01-01"
    end_date = "2025-12-31"

    rsrs_filter = RSRSFilter(N=18, M=300, buy_threshold=0.8, sell_threshold=-0.8)

    tiers = [
        ("Tier0_无过滤", tier0_filter, {}),
        ("Tier1_RSRS单独", tier1_filter, {"rsrs_filter": rsrs_filter}),
        (
            "Tier2_RSRS+宽度",
            tier2_filter,
            {"rsrs_filter": rsrs_filter, "breadth_threshold": 0.15},
        ),
        (
            "Tier3_RSRS+宽度+情绪",
            tier3_filter,
            {
                "rsrs_filter": rsrs_filter,
                "breadth_threshold": 0.15,
                "sentiment_threshold": 30,
            },
        ),
    ]

    all_results = {}
    for name, func, kwargs in tiers:
        print(f"\n运行 {name} ...")
        results = run_monthly_backtest(start_date, end_date, func, name, **kwargs)
        all_results[name] = results

        allowed_count = sum(1 for r in results if r["allowed"])
        avg_hold = np.mean([r["hold_count"] for r in results]) if results else 0
        print(
            f"  信号数: {allowed_count}/{len(results)} ({allowed_count / len(results) * 100:.1f}%)"
        )
        print(f"  平均持仓: {avg_hold:.1f}")

    # 输出对比摘要
    print("\n" + "=" * 60)
    print("4 档对比摘要")
    print("=" * 60)
    print(f"{'方案':<20} {'信号数':>8} {'信号率':>8} {'平均持仓':>10}")
    print("-" * 50)
    for name, results in all_results.items():
        allowed_count = sum(1 for r in results if r["allowed"])
        signal_rate = allowed_count / len(results) * 100 if results else 0
        avg_hold = np.mean([r["hold_count"] for r in results]) if results else 0
        print(f"{name:<20} {allowed_count:>8} {signal_rate:>7.1f}% {avg_hold:>10.1f}")

    # 保存结果供后续分析
    import json

    output = {}
    for name, results in all_results.items():
        output[name] = []
        for r in results:
            row = {
                "date": str(r["date"]),
                "allowed": r["allowed"],
                "hold_count": r["hold_count"],
            }
            if "rsrs" in r and r["rsrs"] is not None:
                row["rsrs"] = round(r["rsrs"], 4)
            if "breadth" in r and r["breadth"] is not None:
                row["breadth"] = round(r["breadth"], 4)
            if "sentiment" in r and r["sentiment"] is not None:
                row["sentiment"] = r["sentiment"]
            output[name].append(row)

    with open("/tmp/rsrs_4tier_comparison.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n结果已保存至 /tmp/rsrs_4tier_comparison.json")

    return all_results


# 在聚宽研究环境中直接运行
if __name__ == "__main__":
    main()
