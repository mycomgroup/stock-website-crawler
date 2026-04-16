#!/usr/bin/env python3
"""
setup.py - ML弱因子搜索实验初始化（独立实现）

目标：
1) 初始化实验目录
2) 生成防过拟合版 strategy.py 模板
3) 运行 baseline
4) 生成 search_notes.md / program.md
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from factor_categories import FACTOR_TO_CATEGORY, calculate_diversity_score

AUTORESEARCH_DIR = Path(__file__).parent


def _default_dates() -> tuple[str, str]:
    today = datetime.today()
    end = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    start = (today - timedelta(days=365 * 6 + 30)).strftime("%Y-%m-%d")
    return start, end


DEFAULT_START, DEFAULT_END = _default_dates()

DEFAULT_SEED_FACTORS = [
    ["size", "roe_ttm", "momentum", "liquidity"],
    ["sales_to_price_ratio", "cfo_to_ev", "cube_of_size"],
    ["TVSTD20", "VOL20", "residual_volatility"],
]

STRATEGY_TEMPLATE = '''#!/usr/bin/env python
# coding: utf-8
"""
独立ML弱因子组合评估策略（防过拟合版）
当前因子组合：{factors}
"""

from jqdata import *
from jqfactor import get_factor_values

import json
import numpy as np
import pandas as pd
from sklearn.linear_model import BayesianRidge
from scipy.stats import spearmanr

FACTOR_COMBO = {factors}
IC_WINDOW = {ic_window}
CLUSTER_COUNT = {cluster_count}
WEIGHT_SMOOTH = {weight_smooth}
BUY_COST_BPS = {buy_cost_bps}
SELL_COST_BPS = {sell_cost_bps}
SLIPPAGE_BPS = {slippage_bps}

FACTOR_CATEGORIES = {
    "basics": ["administration_expense_ttm", "asset_impairment_loss_ttm", "cash_flow_to_price_ratio", "circulating_market_cap", "EBIT", "EBITDA", "financial_assets", "financial_expense_ttm", "financial_liability", "goods_sale_and_service_render_cash_ttm", "gross_profit_ttm", "interest_carry_current_liability", "interest_free_current_liability", "market_cap", "net_debt", "net_finance_cash_flow_ttm", "net_interest_expense", "net_invest_cash_flow_ttm", "net_operate_cash_flow_ttm", "net_profit_ttm", "net_working_capital", "non_operating_net_profit_ttm", "non_recurring_gain_loss", "np_parent_company_owners_ttm", "OperateNetIncome", "operating_assets", "operating_cost_ttm", "operating_liability", "operating_profit_ttm", "operating_revenue_ttm", "retained_earnings", "sales_to_price_ratio", "sale_expense_ttm", "total_operating_cost_ttm", "total_operating_revenue_ttm", "total_profit_ttm", "value_change_profit_ttm"],
    "emotion": ["AR", "ARBR", "ATR14", "ATR6", "BR", "DAVOL10", "DAVOL20", "DAVOL5", "MAWVAD", "money_flow_20", "PSY", "turnover_volatility", "TVMA20", "TVMA6", "TVSTD20", "TVSTD6", "VDEA", "VDIFF", "VEMA10", "VEMA12", "VEMA26", "VEMA5", "VMACD", "VOL10", "VOL120", "VOL20", "VOL240", "VOL5", "VOL60", "VOSC", "VR", "VROC12", "VROC6", "VSTD10", "VSTD20", "WVAD"],
    "growth": ["financing_cash_growth_rate", "net_asset_growth_rate", "net_operate_cashflow_growth_rate", "net_profit_growth_rate", "np_parent_company_owners_growth_rate", "operating_revenue_growth_rate", "PEG", "total_asset_growth_rate", "total_profit_growth_rate"],
    "momentum": ["arron_down_25", "arron_up_25", "BBIC", "bear_power", "BIAS10", "BIAS20", "BIAS5", "BIAS60", "bull_power", "CCI10", "CCI15", "CCI20", "CCI88", "CR20", "fifty_two_week_close_rank", "MASS", "PLRC12", "PLRC24", "PLRC6", "Price1M", "Price1Y", "Price3M", "Rank1M", "ROC12", "ROC120", "ROC20", "ROC6", "ROC60", "single_day_VPT", "single_day_VPT_12", "single_day_VPT_6", "TRIX10", "TRIX5", "Volume1M"],
    "pershare": ["capital_reserve_fund_per_share", "cashflow_per_share_ttm", "cash_and_equivalents_per_share", "eps_ttm", "net_asset_per_share", "net_operate_cash_flow_per_share", "operating_profit_per_share", "operating_profit_per_share_ttm", "operating_revenue_per_share", "operating_revenue_per_share_ttm", "retained_earnings_per_share", "retained_profit_per_share", "surplus_reserve_fund_per_share", "total_operating_revenue_per_share", "total_operating_revenue_per_share_ttm"],
    "quality": ["ACCA", "accounts_payable_turnover_days", "accounts_payable_turnover_rate", "account_receivable_turnover_days", "account_receivable_turnover_rate", "adjusted_profit_to_total_profit", "admin_expense_rate", "asset_turnover_ttm", "cash_rate_of_sales", "cash_to_current_liability", "cfo_to_ev", "current_asset_turnover_rate", "current_ratio", "debt_to_asset_ratio", "debt_to_equity_ratio", "debt_to_tangible_equity_ratio", "DEGM", "DEGM_8y", "DSRI", "equity_to_asset_ratio", "equity_to_fixed_asset_ratio", "equity_turnover_rate", "financial_expense_rate", "fixed_assets_turnover_rate", "fixed_asset_ratio", "GMI", "goods_service_cash_to_operating_revenue_ttm", "gross_income_ratio", "intangible_asset_ratio", "inventory_turnover_days", "inventory_turnover_rate", "invest_income_associates_to_total_profit", "long_debt_to_asset_ratio", "long_debt_to_working_capital_ratio", "long_term_debt_to_asset_ratio", "LVGI", "margin_stability", "maximum_margin", "MLEV", "net_non_operating_income_to_total_profit", "net_operate_cash_flow_to_asset", "net_operate_cash_flow_to_net_debt", "net_operate_cash_flow_to_operating_income", "net_operate_cash_flow_to_total_current_liability", "net_operate_cash_flow_to_total_liability", "net_operating_cash_flow_coverage", "net_profit_ratio", "net_profit_to_total_operate_revenue_ttm", "non_current_asset_ratio", "OperatingCycle", "operating_cost_to_operating_revenue_ratio", "operating_profit_growth_rate", "operating_profit_ratio", "operating_profit_to_operating_revenue", "operating_profit_to_total_profit", "operating_tax_to_operating_revenue_ratio_ttm", "profit_margin_ttm", "quick_ratio", "rnoa_ttm", "ROAEBITTTM", "roa_ttm", "roa_ttm_8y", "roe_ttm", "roe_ttm_8y", "roic_ttm", "sale_expense_to_operating_revenue", "SGAI", "SGI", "super_quick_ratio", "total_asset_turnover_rate", "total_profit_to_cost_ratio"],
    "risk": ["Kurtosis120", "Kurtosis20", "Kurtosis60", "sharpe_ratio_120", "sharpe_ratio_20", "sharpe_ratio_60", "Skewness120", "Skewness20", "Skewness60", "Variance120", "Variance20", "Variance60"],
    "style": ["average_share_turnover_annual", "average_share_turnover_quarterly", "beta", "book_leverage", "book_to_price_ratio", "cash_earnings_to_price_ratio", "cube_of_size", "cumulative_range", "daily_standard_deviation", "debt_to_assets", "earnings_growth", "earnings_to_price_ratio", "earnings_yield", "growth", "historical_sigma", "leverage", "liquidity", "long_term_predicted_earnings_growth", "market_leverage", "momentum", "natural_log_of_market_cap", "non_linear_size", "predicted_earnings_to_price_ratio", "raw_beta", "relative_strength", "residual_volatility", "sales_growth", "share_turnover_monthly", "short_term_predicted_earnings_growth", "size"],
    "technical": ["boll_down", "boll_up", "EMA5", "EMAC10", "EMAC12", "EMAC120", "EMAC20", "EMAC26", "MAC10", "MAC120", "MAC20", "MAC5", "MAC60", "MACDC", "MFI14", "price_no_fq"],
}}
FACTOR_TO_CAT = {}
for cat, fs in FACTOR_CATEGORIES.items():
    for f in fs:
        FACTOR_TO_CAT[f] = cat


def get_period_dates(period, start_date, end_date):
    stock_data = get_price("000001.XSHE", start_date, end_date, "daily", fields=["close"], panel=False)
    stock_data["date"] = stock_data.index
    period_data = stock_data.resample(period).last()
    period_data = period_data.set_index("date").dropna()
    date_index = period_data.index
    date_only_array = np.vectorize(lambda s: s.strftime("%Y-%m-%d"))(date_index.to_pydatetime())
    date_list = pd.Series(date_only_array).tolist()
    date_list.insert(0, (pd.to_datetime(start_date) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
    return date_list


def get_stock_pool(pool, begin_date):
    import datetime

    def filter_new(stocks, begin_date_str, n=90):
        result = []
        begin_dt = datetime.datetime.strptime(begin_date_str, "%Y-%m-%d")
        for stock in stocks:
            if get_security_info(stock).start_date < (begin_dt - datetime.timedelta(days=n)).date():
                result.append(stock)
        return result

    if pool == "small":
        stocks = get_index_stocks("399101.XSHE", begin_date)
        stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]
    elif pool == "HS300":
        stocks = get_index_stocks("000300.XSHG", begin_date)
    elif pool == "ZZ500":
        stocks = get_index_stocks("399905.XSHE", begin_date)
    else:
        stocks = get_index_stocks("000985.XSHE", begin_date)
        stocks = [s for s in stocks if not s.startswith(("3", "68", "4", "8"))]

    st_data = get_extras("is_st", stocks, count=1, end_date=begin_date)
    stocks = [s for s in stocks if not st_data[s][0]]
    return filter_new(stocks, begin_date)


def fetch_factor_frame(stocks, date, factors):
    data = get_factor_values(securities=stocks, factors=factors, count=1, end_date=date)
    out = pd.DataFrame(index=stocks)
    for f in data.keys():
        out[f] = data[f].iloc[0, :]
    return out


def rank_zscore_cross_section(df):
    """截面归一：先rank到[-1,1]，再截尾。"""
    result = df.copy()
    for c in result.columns:
        s = result[c]
        r = s.rank(pct=True)
        result[c] = (r * 2 - 1).clip(-3, 3)
    return result


def factor_corr_prune(factor_df, max_corr=0.8):
    """简单去相关：按绝对相关阈值贪心保留。"""
    if factor_df.shape[1] <= 1:
        return factor_df.columns.tolist()

    corr = factor_df.corr().abs().fillna(0)
    selected = []
    for col in corr.columns:
        if not selected:
            selected.append(col)
            continue
        if corr.loc[col, selected].max() < max_corr:
            selected.append(col)
    return selected


def rolling_ic(signal_series, future_ret_series, window):
    return signal_series.rolling(window).corr(future_ret_series)


def calculate_diversity(factors):
    cats = [FACTOR_TO_CAT.get(f, "unknown") for f in factors]
    return len(set(cats)) / len(factors) if factors else 0.0


def compute_metrics(pred, future_ret, group_n=10):
    long_short = []
    top_ret = []
    ic_list = []
    all_group_means = []

    for dt in pred.index:
        s = pred.loc[dt].dropna()
        r = future_ret.loc[dt].dropna()
        common = s.index.intersection(r.index)
        if len(common) < group_n * 2:
            continue

        tmp = pd.DataFrame({"sig": s[common], "ret": r[common]}).sort_values("sig", ascending=False)
        groups = np.array_split(tmp, group_n)
        gm = [g["ret"].mean() for g in groups]

        long_short.append(gm[0] - gm[-1])
        top_ret.append(gm[0])
        all_group_means.append(gm)

        ic, _ = spearmanr(tmp["sig"], tmp["ret"])
        if not np.isnan(ic):
            ic_list.append(ic)

    ic_arr = np.array(ic_list) if ic_list else np.array([0.0])
    ls_sum = float(np.sum(long_short)) if long_short else 0.0
    top_sharpe = float(np.mean(top_ret) / (np.std(top_ret) + 1e-10) * np.sqrt(252)) if len(top_ret) > 1 else 0.0
    ic_mean = float(np.mean(ic_arr))
    icir = float(ic_mean / (np.std(ic_arr) + 1e-10)) if len(ic_arr) > 1 else 0.0
    ic_win = float(np.mean(ic_arr > 0)) if len(ic_arr) else 0.0

    monotonicity = 0.0
    if all_group_means:
        avg = np.mean(all_group_means, axis=0)
        monotonicity = float(sum(1 for i in range(group_n - 1) if avg[i] > avg[i + 1]) / (group_n - 1))

    return {
        "long_short_return": ls_sum,
        "top_sharpe": top_sharpe,
        "ic_mean": ic_mean,
        "icir": icir,
        "ic_win_rate": ic_win,
        "monotonicity": monotonicity,
    }


def score_from_metrics(metrics, diversity, turnover_mean, net_penalty):
    raw = (
        0.15 * np.tanh(metrics["long_short_return"] / 8.0)
        + 0.15 * np.tanh(metrics["top_sharpe"] / 4.0)
        + 0.15 * np.tanh(metrics["ic_mean"] / 0.08)
        + 0.15 * np.tanh(metrics["icir"] / 2.0)
        + 0.10 * metrics["ic_win_rate"]
        + 0.10 * metrics["monotonicity"]
        + 0.10 * diversity
        - 0.05 * np.tanh(turnover_mean * 4.0)
    )
    return float(raw - net_penalty)


def main():
    start_date = "{start_date}"
    end_date = "{end_date}"
    pool = "{pool}"

    period = "W"
    dates = get_period_dates(period, start_date, end_date)
    split_idx = int(len(dates) * 0.66)

    rows = []
    for i, date in enumerate(dates[:-1]):
        try:
            stocks = get_stock_pool(pool, date)
            if len(stocks) < 30:
                continue

            next_date = dates[i + 1]
            fdf = fetch_factor_frame(stocks, date, FACTOR_COMBO)
            px = get_price(stocks, date, next_date, "1d", "close", panel=False)["close"]
            if px.shape[0] < 2:
                continue

            fdf["future_ret"] = (px.iloc[-1] / px.iloc[1] - 1).clip(-0.5, 0.5)
            fdf["date"] = date
            rows.append(fdf)
        except:
            pass

    if not rows:
        print(json.dumps({"error": "no_data", "score": 0.0}))
        return

    data = pd.concat(rows).reset_index().rename(columns={"index": "stock"})

    # 划分训练/测试
    all_dates = sorted(data["date"].unique())
    train_dates = set(all_dates[:max(1, int(len(all_dates) * 0.66))])
    test_dates = set(all_dates[max(1, int(len(all_dates) * 0.66)):])

    train = data[data["date"].isin(train_dates)].copy()
    test = data[data["date"].isin(test_dates)].copy()
    if test.empty:
        print(json.dumps({"error": "empty_test", "score": 0.0}))
        return

    # 截面预处理
    factor_cols = [f for f in FACTOR_COMBO if f in test.columns]
    train[factor_cols] = train.groupby("date")[factor_cols].transform(lambda x: x.fillna(x.median()))
    test[factor_cols] = test.groupby("date")[factor_cols].transform(lambda x: x.fillna(x.median()))

    # 去相关（只用训练集估计）
    train_cs = rank_zscore_cross_section(train[factor_cols])
    selected = factor_corr_prune(train_cs, max_corr=0.8)
    if not selected:
        selected = factor_cols[:1]

    train[selected] = rank_zscore_cross_section(train[selected])
    test[selected] = rank_zscore_cross_section(test[selected])

    X_train = train[selected].copy()
    y_train = train["future_ret"].copy()
    X_test = test[selected].copy()

    # 清理 NaN/inf，确保模型训练数据有效
    train_valid_mask = ~(X_train.isna().any(axis=1) | y_train.isna() | np.isinf(y_train))
    X_train = X_train[train_valid_mask].replace([np.inf, -np.inf], 0).fillna(0)
    y_train = y_train[train_valid_mask]

    if len(y_train) < 50:
        print(json.dumps({"error": "insufficient_train_data", "score": 0.0, "train_size": len(y_train)}))
        return

    # 模型训练
    model = BayesianRidge()
    model.fit(X_train.values, y_train.values)
    test_valid_mask = ~(X_test.isna().any(axis=1))
    X_test_valid = X_test[test_valid_mask].replace([np.inf, -np.inf], 0).fillna(0)
    test["pred_raw"] = np.nan
    test.loc[test_valid_mask, "pred_raw"] = np.dot(X_test_valid.values, model.coef_)

    # 动态IC-IR权重（按单因子近端IC给组合再缩放）
    test = test.sort_values(["date", "stock"])
    pred_panel = test.pivot(index="date", columns="stock", values="pred_raw")
    ret_panel = test.pivot(index="date", columns="stock", values="future_ret")

    ic_ts = []
    for dt in pred_panel.index:
        s = pred_panel.loc[dt].dropna()
        r = ret_panel.loc[dt].dropna()
        common = s.index.intersection(r.index)
        if len(common) < 20:
            ic_ts.append(np.nan)
            continue
        ic, _ = spearmanr(s[common], r[common])
        ic_ts.append(ic if not np.isnan(ic) else np.nan)

    ic_ser = pd.Series(ic_ts, index=pred_panel.index)
    ic_mean = ic_ser.rolling(IC_WINDOW).mean()
    ic_std = ic_ser.rolling(IC_WINDOW).std()
    ir = (ic_mean / (ic_std + 1e-8)).fillna(0)
    # 缩放系数平滑
    scale = (0.5 + ir.clip(-1, 1)).ewm(alpha=(1 - WEIGHT_SMOOTH)).mean().clip(0.2, 1.8)

    pred_panel_scaled = pred_panel.mul(scale, axis=0)

    # 交易成本近似：基于Top分组换手
    rank_panel = pred_panel_scaled.rank(axis=1, pct=True)
    pos_panel = (rank_panel >= 0.9).astype(float)
    turnover = pos_panel.diff().abs().sum(axis=1).fillna(0)
    turnover_mean = float(turnover.mean()) if len(turnover) else 0.0

    total_cost_rate = turnover_mean * ((BUY_COST_BPS + SELL_COST_BPS + SLIPPAGE_BPS) / 10000.0)

    metrics = compute_metrics(pred_panel_scaled, ret_panel)
    diversity = calculate_diversity(FACTOR_COMBO)

    net_penalty = min(0.2, total_cost_rate * 10)

    if diversity < 0.5 or metrics["ic_mean"] < 0:
        score = 0.0
    else:
        score = score_from_metrics(metrics, diversity=diversity, turnover_mean=turnover_mean, net_penalty=net_penalty)

    result = {
        "factors": FACTOR_COMBO,
        "selected_after_prune": selected,
        "score": score,
        "metrics": metrics,
        "diversity": diversity,
        "turnover_mean": turnover_mean,
        "cost_penalty": net_penalty,
        "data_points": int(len(test)),
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
'''


def parse_seed_factors(seed_factors: str | None) -> list[list[str]]:
    if not seed_factors:
        return DEFAULT_SEED_FACTORS
    try:
        parsed = ast.literal_eval(seed_factors)
        if isinstance(parsed, list) and parsed:
            return parsed
    except Exception:
        pass
    print("[警告] seed-factors 解析失败，回退默认值")
    return DEFAULT_SEED_FACTORS


def generate_search_notes(
    seed_factors: list[list[str]],
    start_date: str,
    end_date: str,
    pool: str,
    baseline: float,
    top_k: int,
) -> str:
    top = seed_factors[0] if seed_factors else []
    top_k_seed = seed_factors[: max(1, top_k)]
    lines = []
    for i, factors in enumerate(top_k_seed, start=1):
        score = baseline if i == 1 else 0.0
        lines.append(f"| {i} | {score:.4f} | {factors} | seed | 0 |")
    pool_table = "\n".join(lines) if lines else "| 1 | 0.0000 | [] | seed | 0 |"
    return f"""## 当前状态
- best_score: {baseline:.4f}
- best_factors: {top}
- current_iter: 0
- top_k: {top_k}

## 回测配置
- 日期范围: {start_date} ~ {end_date}
- 选股池: {pool}

## 风险守则
- [x] 因子去相关后再组合
- [x] 标签严格使用 t -> t+1 对齐
- [x] 动态缩放必须平滑
- [x] 交易成本必须入分数

## 多策略池（Top-K）
| rank | score | factors | source | iter |
|------|-------|---------|--------|------|
{pool_table}

## 搜索地图

### 已验证有效（keep）
（初始化为空）

### 已验证无效（rollback）
（初始化为空）

### 待探索方向
- [ ] 从高分组合变异，替换单个因子
- [ ] 随机采样新组合（多样性优先）
- [ ] 频率优先采样
- [ ] 组合不同类别因子（分散度优先）

## 最近一轮候选结果
| idx | score | factors | success |
|-----|-------|---------|---------|
"""


def run_baseline(strategy_file: Path, notebook_dir: str | None):
    from notebook_executor import execute_strategy

    print("[baseline] start")
    result = execute_strategy(
        str(strategy_file), timeout_ms=600_000, notebook_dir=notebook_dir
    )
    if result.get("success"):
        return float(result.get("score", 0.0)), result
    print(f"[baseline] failed: {result.get('error')}")
    return 0.0, result


def main():
    parser = argparse.ArgumentParser(description="初始化 ML 弱因子 JoinQuant 实验目录")
    parser.add_argument("--name", required=True, help="实验名称")
    parser.add_argument(
        "--start-date", default=DEFAULT_START, help=f"默认 {DEFAULT_START}"
    )
    parser.add_argument("--end-date", default=DEFAULT_END, help=f"默认 {DEFAULT_END}")
    parser.add_argument(
        "--pool",
        default="small",
        choices=["small", "HS300", "ZZ500", "ZZ800"],
        help="选股池",
    )
    parser.add_argument("--seed-factors", default=None, help="二维列表字符串")
    parser.add_argument("--notebook-dir", default=None, help="joinquant notebook 目录")

    parser.add_argument(
        "--ic-window", type=int, default=26, help="IC rolling窗口（周频约半年）"
    )
    parser.add_argument(
        "--cluster-count", type=int, default=20, help="聚类簇数（预留参数）"
    )
    parser.add_argument("--weight-smooth", type=float, default=0.8, help="权重平滑系数")
    parser.add_argument("--buy-cost-bps", type=float, default=15.0, help="买入成本bp")
    parser.add_argument("--sell-cost-bps", type=float, default=15.0, help="卖出成本bp")
    parser.add_argument("--slippage-bps", type=float, default=5.0, help="滑点bp")
    parser.add_argument("--top-k", type=int, default=5, help="保留前K组策略")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d")
    exp_name = f"strategy_autoresearch_ml_factor_{args.name}_{ts}"
    exp_dir = AUTORESEARCH_DIR / exp_name

    if exp_dir.exists():
        print(f"[错误] 目录已存在: {exp_dir}")
        sys.exit(1)

    exp_dir.mkdir(parents=True)
    subprocess.run(["git", "init"], cwd=str(exp_dir), capture_output=True)

    seeds = parse_seed_factors(args.seed_factors)
    strategy_file = exp_dir / "strategy.py"
    strategy_content = STRATEGY_TEMPLATE
    strategy_content = strategy_content.replace("{factors}", repr(seeds[0]))
    strategy_content = strategy_content.replace("{start_date}", args.start_date)
    strategy_content = strategy_content.replace("{end_date}", args.end_date)
    strategy_content = strategy_content.replace("{pool}", args.pool)
    strategy_content = strategy_content.replace("{ic_window}", str(args.ic_window))
    strategy_content = strategy_content.replace(
        "{cluster_count}", str(args.cluster_count)
    )
    strategy_content = strategy_content.replace(
        "{weight_smooth}", str(args.weight_smooth)
    )
    strategy_content = strategy_content.replace(
        "{buy_cost_bps}", str(args.buy_cost_bps)
    )
    strategy_content = strategy_content.replace(
        "{sell_cost_bps}", str(args.sell_cost_bps)
    )
    strategy_content = strategy_content.replace(
        "{slippage_bps}", str(args.slippage_bps)
    )
    strategy_content = strategy_content.replace("{{", "{")
    strategy_content = strategy_content.replace("}}", "}")
    strategy_file.write_text(strategy_content, encoding="utf-8")

    subprocess.run(["git", "add", "strategy.py"], cwd=str(exp_dir), capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "iter_0000_baseline: init ml weak-factor strategy"],
        cwd=str(exp_dir),
        capture_output=True,
    )

    src_program = AUTORESEARCH_DIR / "program.md"
    if src_program.exists():
        (exp_dir / "program.md").write_text(
            src_program.read_text(encoding="utf-8"), encoding="utf-8"
        )

    baseline_score, baseline_result = run_baseline(strategy_file, args.notebook_dir)

    notes = generate_search_notes(
        seeds,
        args.start_date,
        args.end_date,
        args.pool,
        baseline_score,
        max(1, args.top_k),
    )
    (exp_dir / "search_notes.md").write_text(notes, encoding="utf-8")

    (exp_dir / "seed_config.json").write_text(
        json.dumps(
            {
                "seed_factors": seeds,
                "start_date": args.start_date,
                "end_date": args.end_date,
                "pool": args.pool,
                "ic_window": args.ic_window,
                "cluster_count": args.cluster_count,
                "weight_smooth": args.weight_smooth,
                "buy_cost_bps": args.buy_cost_bps,
                "sell_cost_bps": args.sell_cost_bps,
                "slippage_bps": args.slippage_bps,
                "top_k": max(1, args.top_k),
                "baseline_result": baseline_result,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    init_pool = []
    for i, combo in enumerate(seeds[: max(1, args.top_k)], start=1):
        init_pool.append(
            {
                "rank": i,
                "score": baseline_score if i == 1 else 0.0,
                "factors": combo,
                "source": "seed",
                "iter": 0,
            }
        )
    (exp_dir / "strategy_pool.json").write_text(
        json.dumps(init_pool, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("[setup] 完成")
    print(f"[setup] 实验目录: {exp_dir}")


if __name__ == "__main__":
    main()
