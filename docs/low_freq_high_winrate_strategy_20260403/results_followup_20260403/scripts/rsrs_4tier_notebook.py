"""
RSRS 复合过滤增量验证 — JoinQuant Notebook 格式
================================================

用途：在 JoinQuant Notebook 中运行 4 档过滤对比
  Tier 0: 无过滤
  Tier 1: RSRS 单独过滤
  Tier 2: RSRS + 宽度
  Tier 3: RSRS + 宽度 + 情绪

底座：RFScore7 PB10 Optimized
回测区间：2023-01-01 至 2025-12-31（3年验证期，控制超时）
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import numpy as np
import pandas as pd
import statsmodels.api as sm
import json

print("=" * 60)
print("RSRS 复合过滤增量验证 — JoinQuant Notebook")
print("=" * 60)


# ============================================================
# 一、RSRS 模块
# ============================================================
class RSRSFilter:
    def __init__(self, N=18, M=300, buy_threshold=0.8, sell_threshold=-0.8):
        self.N = N
        self.M = M
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.beta_history = []
        self.r2_history = []
        self._initialized = False

    def update(self, end_date):
        lookback = self.M + self.N + 50
        try:
            prices = get_price(
                "000300.XSHG",
                end_date=end_date,
                count=lookback,
                fields=["high", "low", "close"],
                panel=False,
            )
        except:
            return None, None, None, None
        if prices is None or len(prices) < self.M:
            return None, None, None, None

        highs = prices["high"].values
        lows = prices["low"].values

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
        rsrs_right = zscore * beta * r2

        return rsrs_right, zscore, beta, r2

    def is_allowed(self, end_date):
        rsrs, _, _, _ = self.update(end_date)
        if rsrs is None:
            return True
        return rsrs > self.sell_threshold


# ============================================================
# 二、宽度 & 情绪
# ============================================================
def calc_breadth(end_date, window=20):
    try:
        hs300 = get_index_stocks("000300.XSHG", date=end_date)
        prices = get_price(
            hs300[:100], end_date=end_date, count=window, fields=["close"], panel=False
        )
        if prices is None or prices.empty or len(prices) < window:
            return 0.5
        close = prices.pivot(index="time", columns="code", values="close")
        return float((close.iloc[-1] > close.mean()).mean())
    except:
        return 0.5


def calc_sentiment(end_date):
    try:
        all_stocks = get_all_securities("stock", date=end_date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in ("4", "8") and s[:2] != "68"]
        sample = all_stocks[:300]
        df = get_price(
            sample,
            end_date=end_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        if df is None or df.empty:
            return 30
        df = df.dropna()
        hl_count = len(df[df["close"] >= df["high_limit"] * 0.995])
        return hl_count
    except:
        return 30


# ============================================================
# 三、RFScore 因子
# ============================================================
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
    try:
        hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
        stocks = list(hs300)
        stocks = [s for s in stocks if not s.startswith("688")]
        sec = get_all_securities(types=["stock"], date=watch_date)
        sec = sec.loc[sec.index.intersection(stocks)]
        sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=180)]
        stocks = sec.index.tolist()
        is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()
        return stocks[:200]  # 限制规模控制超时
    except:
        return []


def calc_rfscore_table(stocks, watch_date):
    if not stocks:
        return pd.DataFrame()
    try:
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
        df = df.dropna(subset=["RFScore", "pb_ratio"])
        df = df[(df["pb_ratio"] > 0) & (df["pe_ratio"] > 0)].copy()
        if df.empty:
            return df
        df["pb_group"] = (
            pd.qcut(
                df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
            )
            + 1
        )
        return df
    except:
        return pd.DataFrame()


def choose_stocks(df, target_hold_num=10):
    if target_hold_num <= 0 or df.empty:
        return []
    try:
        primary = df[(df["RFScore"] >= 6) & (df["pb_group"] <= 2)].copy()
        if primary.empty:
            primary = df[df["RFScore"] >= 5].copy()
        primary["score"] = (
            primary["RFScore"] * 100 - primary["pb_ratio"].rank(pct=True) * 10
        )
        primary = primary.sort_values("score", ascending=False)
        return primary.index.tolist()[:target_hold_num]
    except:
        return []


# ============================================================
# 四、4 档过滤
# ============================================================
def run_comparison():
    start_date = "2023-01-01"
    end_date = "2025-12-31"

    rsrs = RSRSFilter(N=18, M=300, buy_threshold=0.8, sell_threshold=-0.8)

    dates = get_trade_days(start_date=start_date, end_date=end_date, count=None)
    monthly_dates = []
    last_month = None
    for d in dates:
        if d.month != last_month:
            monthly_dates.append(d)
            last_month = d.month

    print(f"\n回测区间: {start_date} ~ {end_date}")
    print(f"月度调仓日: {len(monthly_dates)} 个")

    tiers = {
        "Tier0_无过滤": {
            "allowed": 0,
            "total": 0,
            "holds": [],
            "rsrs_vals": [],
            "breadths": [],
            "sentiments": [],
        },
        "Tier1_RSRS单独": {
            "allowed": 0,
            "total": 0,
            "holds": [],
            "rsrs_vals": [],
            "breadths": [],
            "sentiments": [],
        },
        "Tier2_RSRS+宽度": {
            "allowed": 0,
            "total": 0,
            "holds": [],
            "rsrs_vals": [],
            "breadths": [],
            "sentiments": [],
        },
        "Tier3_RSRS+宽度+情绪": {
            "allowed": 0,
            "total": 0,
            "holds": [],
            "rsrs_vals": [],
            "breadths": [],
            "sentiments": [],
        },
    }

    for i, dt in enumerate(monthly_dates):
        print(f"\n[{i + 1}/{len(monthly_dates)}] {dt} ...")

        # 计算指标
        rsrs_val, zscore, beta, r2 = rsrs.update(dt)
        breadth = calc_breadth(dt)
        sentiment = calc_sentiment(dt)
        rsrs_allowed = rsrs.is_allowed(dt) if rsrs_val is not None else True

        rsrs_str = f"{rsrs_val:.4f}" if rsrs_val is not None else "N/A"
        print(f"  RSRS={rsrs_str:>8}  宽度={breadth:.3f}  情绪={sentiment}")

        # Tier 0: 无过滤
        t0_allowed = True
        # Tier 1: RSRS 单独
        t1_allowed = rsrs_allowed
        # Tier 2: RSRS + 宽度
        t2_allowed = rsrs_allowed and (breadth >= 0.15)
        # Tier 3: RSRS + 宽度 + 情绪
        t3_allowed = rsrs_allowed and (breadth >= 0.15) and (sentiment >= 30)

        tier_results = [
            ("Tier0_无过滤", t0_allowed),
            ("Tier1_RSRS单独", t1_allowed),
            ("Tier2_RSRS+宽度", t2_allowed),
            ("Tier3_RSRS+宽度+情绪", t3_allowed),
        ]

        for tier_name, allowed in tier_results:
            tiers[tier_name]["total"] += 1
            if allowed:
                tiers[tier_name]["allowed"] += 1
                # 选股
                universe = get_universe(dt)
                if universe:
                    df = calc_rfscore_table(universe, dt)
                    picks = choose_stocks(df, target_hold_num=10)
                else:
                    picks = []
                tiers[tier_name]["holds"].append(len(picks))
            else:
                tiers[tier_name]["holds"].append(0)

            tiers[tier_name]["rsrs_vals"].append(
                round(rsrs_val, 4) if rsrs_val is not None else None
            )
            tiers[tier_name]["breadths"].append(round(breadth, 4))
            tiers[tier_name]["sentiments"].append(sentiment)

    # 输出对比
    print("\n" + "=" * 70)
    print("4 档对比结果")
    print("=" * 70)
    print(f"{'方案':<25} {'信号数':>8} {'信号率':>8} {'平均持仓':>10} {'零持仓月':>10}")
    print("-" * 70)

    output = {}
    for name, data in tiers.items():
        signal_rate = data["allowed"] / data["total"] * 100 if data["total"] else 0
        avg_hold = np.mean(data["holds"]) if data["holds"] else 0
        zero_months = sum(1 for h in data["holds"] if h == 0)

        print(
            f"{name:<25} {data['allowed']:>5}/{data['total']} {signal_rate:>7.1f}% {avg_hold:>10.1f} {zero_months:>10}"
        )

        output[name] = {
            "signal_count": data["allowed"],
            "total_months": data["total"],
            "signal_rate": round(signal_rate, 1),
            "avg_hold": round(avg_hold, 1),
            "zero_months": zero_months,
            "monthly_details": [],
        }
        for j, dt in enumerate(monthly_dates):
            output[name]["monthly_details"].append(
                {
                    "date": str(dt),
                    "allowed": True
                    if j < len(data["holds"])
                    and (data["holds"][j] > 0 or name == "Tier0_无过滤")
                    else False,
                    "hold_count": data["holds"][j] if j < len(data["holds"]) else 0,
                    "rsrs": data["rsrs_vals"][j]
                    if j < len(data["rsrs_vals"])
                    else None,
                    "breadth": data["breadths"][j]
                    if j < len(data["breadths"])
                    else None,
                    "sentiment": data["sentiments"][j]
                    if j < len(data["sentiments"])
                    else None,
                }
            )

    print(f"\n结果 JSON 已生成（共 {len(output)} 档方案）")
    print("验证完成 ✓")

    return output


# 运行
try:
    result = run_comparison()
except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
