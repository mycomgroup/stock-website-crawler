#!/usr/bin/env python3
"""
setup.py - 因子搜索实验初始化

用法：
    python setup.py --name my_search \\
        --start-date 2020-01-01 \\
        --end-date 2025-03-28 \\
        --pool small \\
        --seed-factors "['size','roe_ttm'],['momentum','beta','liquidity']"

流程：
    1. 创建实验目录
    2. git init
    3. 生成 strategy.py
    4. 生成 search_notes.md
    5. 生成 program.md
    6. 运行 baseline
"""

import argparse
import ast
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from config import PERIOD_CONFIG, DEFAULT_PERIOD

AUTORESEARCH_DIR = Path(__file__).parent
PARENT_DIR = AUTORESEARCH_DIR


def _default_dates(period=None):
    period = period or DEFAULT_PERIOD
    config = PERIOD_CONFIG[period]
    today = datetime.today()
    backtest_end = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    test_days = config["test_months"] * 30
    backtest_start = (today - timedelta(days=test_days + 7)).strftime("%Y-%m-%d")
    train_days = config["train_years"] * 365
    train_start = (today - timedelta(days=train_days + test_days + 7)).strftime(
        "%Y-%m-%d"
    )
    return train_start, backtest_start, backtest_end


_train_start, _backtest_start, _backtest_end = _default_dates()

TSV_HEADER = "iter\tscore\tdiversity\tannual_return\tmax_drawdown\tdecision\tmutation\n"

DEFAULT_SEED_FACTORS = [
    [
        "inventory_turnover_rate",
        "sales_to_price_ratio",
        "share_turnover_monthly",
        "natural_log_of_market_cap",
    ],
    ["size", "roe_ttm", "TVSTD20", "current_asset_turnover_rate"],
    ["TVMA6", "financial_expense_ttm"],
    ["VOL10", "circulating_market_cap", "single_day_VPT_12"],
    ["money_flow_20", "adjusted_profit_to_total_profit"],
    ["super_quick_ratio", "cube_of_size", "cfo_to_ev"],
]

STRATEGY_TEMPLATE = '''#!/usr/bin/env python
# coding: utf-8
"""
因子组合评估策略
当前因子组合：{factors}
"""

FACTOR_COMBO = {factors}
PERIOD = "{period}"
PERIODS_PER_YEAR = {periods_per_year}

from jqdata import *
from jqlib.technical_analysis import *
from jqfactor import get_factor_values
import pandas as pd
import numpy as np
from sklearn.linear_model import BayesianRidge
from scipy.stats import spearmanr
import json


def get_period_date(peroid, start_date, end_date):
    import datetime
    stock_data = get_price("000001.XSHE", start_date, end_date, "daily", fields=["close"])
    stock_data["date"] = stock_data.index
    period_stock_data = stock_data.resample(peroid, how="last")
    period_stock_data = period_stock_data.set_index("date").dropna()
    date = period_stock_data.index
    pydate_array = date.to_pydatetime()
    date_only_array = np.vectorize(lambda s: s.strftime("%Y-%m-%d"))(pydate_array)
    date_only_series = pd.Series(date_only_array)
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date - datetime.timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")
    date_list = date_only_series.values.tolist()
    date_list.insert(0, start_date)
    return date_list


def get_stock(stockPool, begin_date):
    import datetime
    def delect_stop(stocks, beginDate, n=90):
        stockList = []
        beginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
        for stock in stocks:
            start_date = get_security_info(stock).start_date
            if start_date < (beginDate - datetime.timedelta(days=n)).date():
                stockList.append(stock)
        return stockList
    
    if stockPool == "small":
        stockList = get_index_stocks("399101.XSHE", begin_date)
        stockList = [s for s in stockList if not s.startswith(("68", "4", "8"))]
    elif stockPool == "A":
        stockList = get_index_stocks("000002.XSHG", begin_date) + get_index_stocks("399107.XSHE", begin_date)
        stockList = [s for s in stockList if not s.startswith(("68", "4", "8"))]
    elif stockPool == "HS300":
        stockList = get_index_stocks("000300.XSHG", begin_date)
    elif stockPool == "ZZ500":
        stockList = get_index_stocks("399905.XSHE", begin_date)
    else:
        stockList = get_index_stocks("000985.XSHE", begin_date)
        stockList = [s for s in stockList if not s.startswith(("3", "68", "4", "8"))]
    
    st_data = get_extras("is_st", stockList, count=1, end_date=begin_date)
    stockList = [s for s in stockList if not st_data[s][0]]
    stockList = delect_stop(stockList, begin_date)
    return stockList


def get_factor_data(securities_list, date, factors):
    factor_data = get_factor_values(securities=securities_list, factors=factors, count=1, end_date=date)
    df = pd.DataFrame(index=securities_list)
    for k in factor_data.keys():
        df[k] = factor_data[k].iloc[0, :]
    return df


def calculate_metrics(factor_df, ret_df, num_layers=10):
    import numpy as np
    
    periods_per_year = PERIODS_PER_YEAR
    
    long_short_returns = []
    top_returns = []
    ic_list = []
    all_group_means = []
    layer_returns_all = []
    
    for date in factor_df.index:
        factors = factor_df.loc[date].dropna()
        returns = ret_df.loc[date].dropna()
        common = factors.index.intersection(returns.index)
        if len(common) < num_layers * 2:
            continue
        
        f = factors[common]
        r = returns[common]
        combined = pd.DataFrame(dict([("factor", f), ("return", r)])).sort_values("factor", ascending=False)
        
        n = len(combined)
        gs = n // num_layers
        rem = n % num_layers
        groups = []
        start = 0
        for i in range(num_layers):
            end = start + gs + (1 if i < rem else 0)
            groups.append(combined.iloc[start:end])
            start = end
        
        group_means = [g["return"].mean() for g in groups]
        all_group_means.append(group_means)
        long_short_returns.append(group_means[0] - group_means[-1])
        top_returns.append(groups[0]["return"].mean())
        layer_returns_all.append(group_means)
        
        ic, _ = spearmanr(f, r)
        if not np.isnan(ic):
            ic_list.append(ic)
    
    ic_arr = np.array(ic_list) if ic_list else np.array([0])
    
    long_short = np.sum(long_short_returns) if long_short_returns else 0
    top_sharpe = (np.mean(top_returns) / (np.std(top_returns) + 1e-10) * np.sqrt(252)) if len(top_returns) > 1 else 0
    ic_mean = float(np.mean(ic_arr))
    icir = float(ic_mean / (np.std(ic_arr) + 1e-10)) if len(ic_arr) > 1 else 0
    ic_win = float(np.sum(ic_arr > 0) / len(ic_arr)) if len(ic_arr) > 0 else 0
    
    mono = 0
    if all_group_means:
        avg = np.mean(all_group_means, axis=0)
        mono = sum(1 for i in range(num_layers - 1) if avg[i] > avg[i + 1]) / (num_layers - 1)
    
    vol = float(np.std(top_returns)) if len(top_returns) > 1 else 1.0
    
    annual_return = 0.0
    max_drawdown = 0.0
    if top_returns:
        top_returns_arr = np.array(top_returns)
        cumulative = (1 + top_returns_arr).cumprod()
        total_return = cumulative[-1] - 1 if len(cumulative) > 0 else 0
        num_periods = len(top_returns)
        annual_return = float((1 + total_return) ** (periods_per_year / num_periods) - 1) if num_periods > 0 else 0
        
        peak = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - peak) / peak
        max_drawdown = float(abs(np.min(drawdown))) if len(drawdown) > 0 else 0
    
    return dict(
        long_short_return=float(long_short),
        top_sharpe=float(top_sharpe),
        ic_mean=ic_mean,
        icir=icir,
        ic_win_rate=ic_win,
        monotonicity=float(mono),
        return_volatility=vol,
        annual_return=annual_return,
        max_drawdown=max_drawdown,
    )


def calculate_diversity(factors):
    # 完整因子分类（来自 factor_categories.py）
    FACTOR_CATEGORIES = dict(
        basics=["administration_expense_ttm", "asset_impairment_loss_ttm", "cash_flow_to_price_ratio", "circulating_market_cap", "EBIT", "EBITDA", "financial_assets", "financial_expense_ttm", "financial_liability", "goods_sale_and_service_render_cash_ttm", "gross_profit_ttm", "interest_carry_current_liability", "interest_free_current_liability", "market_cap", "net_debt", "net_finance_cash_flow_ttm", "net_interest_expense", "net_invest_cash_flow_ttm", "net_operate_cash_flow_ttm", "net_profit_ttm", "net_working_capital", "non_operating_net_profit_ttm", "non_recurring_gain_loss", "np_parent_company_owners_ttm", "OperateNetIncome", "operating_assets", "operating_cost_ttm", "operating_liability", "operating_profit_ttm", "operating_revenue_ttm", "retained_earnings", "sales_to_price_ratio", "sale_expense_ttm", "total_operating_cost_ttm", "total_operating_revenue_ttm", "total_profit_ttm", "value_change_profit_ttm"],
        emotion=["AR", "ARBR", "ATR14", "ATR6", "BR", "DAVOL10", "DAVOL20", "DAVOL5", "MAWVAD", "money_flow_20", "PSY", "turnover_volatility", "TVMA20", "TVMA6", "TVSTD20", "TVSTD6", "VDEA", "VDIFF", "VEMA10", "VEMA12", "VEMA26", "VEMA5", "VMACD", "VOL10", "VOL120", "VOL20", "VOL240", "VOL5", "VOL60", "VOSC", "VR", "VROC12", "VROC6", "VSTD10", "VSTD20", "WVAD"],
        growth=["financing_cash_growth_rate", "net_asset_growth_rate", "net_operate_cashflow_growth_rate", "net_profit_growth_rate", "np_parent_company_owners_growth_rate", "operating_revenue_growth_rate", "PEG", "total_asset_growth_rate", "total_profit_growth_rate"],
        momentum=["arron_down_25", "arron_up_25", "BBIC", "bear_power", "BIAS10", "BIAS20", "BIAS5", "BIAS60", "bull_power", "CCI10", "CCI15", "CCI20", "CCI88", "CR20", "fifty_two_week_close_rank", "MASS", "PLRC12", "PLRC24", "PLRC6", "Price1M", "Price1Y", "Price3M", "Rank1M", "ROC12", "ROC120", "ROC20", "ROC6", "ROC60", "single_day_VPT", "single_day_VPT_12", "single_day_VPT_6", "TRIX10", "TRIX5", "Volume1M"],
        pershare=["capital_reserve_fund_per_share", "cashflow_per_share_ttm", "cash_and_equivalents_per_share", "eps_ttm", "net_asset_per_share", "net_operate_cash_flow_per_share", "operating_profit_per_share", "operating_profit_per_share_ttm", "operating_revenue_per_share", "operating_revenue_per_share_ttm", "retained_earnings_per_share", "retained_profit_per_share", "surplus_reserve_fund_per_share", "total_operating_revenue_per_share", "total_operating_revenue_per_share_ttm"],
        quality=["ACCA", "accounts_payable_turnover_days", "accounts_payable_turnover_rate", "account_receivable_turnover_days", "account_receivable_turnover_rate", "adjusted_profit_to_total_profit", "admin_expense_rate", "asset_turnover_ttm", "cash_rate_of_sales", "cash_to_current_liability", "cfo_to_ev", "current_asset_turnover_rate", "current_ratio", "debt_to_asset_ratio", "debt_to_equity_ratio", "debt_to_tangible_equity_ratio", "DEGM", "DEGM_8y", "DSRI", "equity_to_asset_ratio", "equity_to_fixed_asset_ratio", "equity_turnover_rate", "financial_expense_rate", "fixed_assets_turnover_rate", "fixed_asset_ratio", "GMI", "goods_service_cash_to_operating_revenue_ttm", "gross_income_ratio", "intangible_asset_ratio", "inventory_turnover_days", "inventory_turnover_rate", "invest_income_associates_to_total_profit", "long_debt_to_asset_ratio", "long_debt_to_working_capital_ratio", "long_term_debt_to_asset_ratio", "LVGI", "margin_stability", "maximum_margin", "MLEV", "net_non_operating_income_to_total_profit", "net_operate_cash_flow_to_asset", "net_operate_cash_flow_to_net_debt", "net_operate_cash_flow_to_operate_income", "net_operate_cash_flow_to_total_current_liability", "net_operate_cash_flow_to_total_liability", "net_operating_cash_flow_coverage", "net_profit_ratio", "net_profit_to_total_operate_revenue_ttm", "non_current_asset_ratio", "OperatingCycle", "operating_cost_to_operating_revenue_ratio", "operating_profit_growth_rate", "operating_profit_ratio", "operating_profit_to_operating_revenue", "operating_profit_to_total_profit", "operating_tax_to_operating_revenue_ratio_ttm", "profit_margin_ttm", "quick_ratio", "rnoa_ttm", "ROAEBITTTM", "roa_ttm", "roa_ttm_8y", "roe_ttm", "roe_ttm_8y", "roic_ttm", "sale_expense_to_operating_revenue", "SGAI", "SGI", "super_quick_ratio", "total_asset_turnover_rate", "total_profit_to_cost_ratio"],
        risk=["Kurtosis120", "Kurtosis20", "Kurtosis60", "sharpe_ratio_120", "sharpe_ratio_20", "sharpe_ratio_60", "Skewness120", "Skewness20", "Skewness60", "Variance120", "Variance20", "Variance60"],
        style=["average_share_turnover_annual", "average_share_turnover_quarterly", "beta", "book_leverage", "book_to_price_ratio", "cash_earnings_to_price_ratio", "cube_of_size", "cumulative_range", "daily_standard_deviation", "debt_to_assets", "earnings_growth", "earnings_to_price_ratio", "earnings_yield", "growth", "historical_sigma", "leverage", "liquidity", "long_term_predicted_earnings_growth", "market_leverage", "momentum", "natural_log_of_market_cap", "non_linear_size", "predicted_earnings_to_price_ratio", "raw_beta", "relative_strength", "residual_volatility", "sales_growth", "share_turnover_monthly", "short_term_predicted_earnings_growth", "size"],
        technical=["boll_down", "boll_up", "EMA5", "EMAC10", "EMAC12", "EMAC120", "EMAC20", "EMAC26", "MAC10", "MAC120", "MAC20", "MAC5", "MAC60", "MACDC", "MFI14", "price_no_fq"],
    )
    FACTOR_TO_CAT = dict()
    for cat, fs in FACTOR_CATEGORIES.items():
        for f in fs:
            FACTOR_TO_CAT[f] = cat
    
    cats = [FACTOR_TO_CAT.get(f, "unknown") for f in factors]
    return len(set(cats)) / len(factors) if factors else 0


def calculate_score(metrics, diversity):
    import numpy as np
    def norm(v, s=1.0):
        return float(np.tanh(v / s))
    
    weights = dict(
        long_short_return=0.25, top_sharpe=0.15, ic_mean=0.15,
        icir=0.10, ic_win_rate=0.05, monotonicity=0.10,
        return_volatility=0.10, diversity=0.10,
    )
    
    normalized = dict(
        long_short_return=norm(metrics["long_short_return"], 10.0),
        top_sharpe=norm(metrics["top_sharpe"], 5.0),
        ic_mean=norm(metrics["ic_mean"], 0.1),
        icir=norm(metrics["icir"], 2.0),
        ic_win_rate=metrics["ic_win_rate"],
        monotonicity=metrics["monotonicity"],
        return_volatility=1.0 / (1.0 + metrics["return_volatility"] * 10),
        diversity=diversity,
    )
    
    return sum(normalized[k] * weights[k] for k in weights)


def main():
    train_start = "{train_start}"
    backtest_start = "{backtest_start}"
    backtest_end = "{backtest_end}"
    pool = "{pool}"
    
    peroid = "{period}"
    dateList = get_period_date(peroid, train_start, backtest_end)
    
    train_dateList = [d for d in dateList if d <= backtest_start]
    test_dateList = [d for d in dateList if d > backtest_start]
    
    train_data = pd.DataFrame()
    test_data = pd.DataFrame()
    
    for date in train_dateList:
        try:
            stocks = get_stock(pool, date)
            if len(stocks) < 20:
                continue
            fd = get_factor_data(stocks, date, FACTOR_COMBO)
            next_idx = dateList.index(date) + 1
            if next_idx >= len(dateList):
                continue
            dc = get_price(stocks, date, dateList[next_idx], "1d", "close")["close"]
            fd["pchg"] = dc.iloc[-1] / dc.iloc[1] - 1
            fd["date"] = date
            train_data = pd.concat([train_data, fd]) if not train_data.empty else fd
        except:
            pass
    
    for date in test_dateList[:-1]:
        try:
            stocks = get_stock(pool, date)
            if len(stocks) < 20:
                continue
            fd = get_factor_data(stocks, date, FACTOR_COMBO)
            next_idx = dateList.index(date) + 1
            if next_idx >= len(dateList):
                continue
            dc = get_price(stocks, date, dateList[next_idx], "1d", "close")["close"]
            fd["pchg"] = dc.iloc[-1] / dc.iloc[1] - 1
            fd["date"] = date
            test_data = pd.concat([test_data, fd]) if not test_data.empty else fd
        except:
            pass
    
    if test_data.empty:
        print(json.dumps(dict(error="no test data", score=0)))
        return
    
    for col in FACTOR_COMBO:
        if col in test_data.columns:
            test_data[col] = test_data.groupby("date")[col].transform(lambda x: x.fillna(x.median()))
    test_data = test_data.dropna()
    
    if len(test_data) < 50:
        print(json.dumps(dict(error="insufficient data", score=0)))
        return
    
    X = test_data[FACTOR_COMBO]
    y = test_data["pchg"]
    
    model = BayesianRidge()
    model.fit(X, y)
    preds = np.dot(X, model.coef_)
    
    test_data["factor"] = preds
    test_data = test_data.reset_index()
    if "id" not in test_data.columns and "index" in test_data.columns:
        test_data.rename(columns=dict([("index", "id")]), inplace=True)
    if "id" not in test_data.columns:
        test_data["id"] = range(len(test_data))
    
    factor_df = test_data.set_index(["id", "date"])["factor"].unstack(level="id")
    ret_df = test_data.set_index(["id", "date"])["pchg"].unstack(level="id")
    
    metrics = calculate_metrics(factor_df, ret_df)
    diversity = calculate_diversity(FACTOR_COMBO)
    score = calculate_score(metrics, diversity)
    
    result = dict(
        factors=FACTOR_COMBO,
        score=score,
        metrics=metrics,
        diversity=diversity,
        annual_return=metrics.get("annual_return", 0),
        max_drawdown=metrics.get("max_drawdown", 0),
        data_points=len(test_data),
    )
    
    print(json.dumps(result))


if __name__ == "__main__":
    main()
'''


def parse_seed_factors(s: str) -> list:
    if not s:
        return DEFAULT_SEED_FACTORS
    try:
        return ast.literal_eval(s)
    except:
        print(f"[警告] 无法解析种子因子，使用默认值")
        return DEFAULT_SEED_FACTORS


def init_iterations_tsv(base: Path) -> None:
    tsv = base / "iterations.tsv"
    if not tsv.exists():
        tsv.write_text(TSV_HEADER, encoding="utf-8")


def append_tsv(base: Path, row: dict) -> None:
    tsv = base / "iterations.tsv"
    line = (
        "\t".join(
            [
                str(row.get("iter", "")),
                f"{row.get('score', 0):.4f}",
                f"{row.get('diversity', 0):.2f}",
                f"{row.get('annual_return', 0):.4f}",
                f"{row.get('max_drawdown', 0):.4f}",
                str(row.get("decision", "")),
                str(row.get("mutation", "")),
            ]
        )
        + "\n"
    )
    with open(tsv, "a", encoding="utf-8") as f:
        f.write(line)


def generate_search_notes(
    seed_factors,
    train_start,
    backtest_start,
    backtest_end,
    pool,
    baseline_score=0,
    notebook_info=None,
):
    seed_str = ", ".join([str(f) for f in seed_factors])

    notebook_section = ""
    if notebook_info:
        notebook_section = f"""## Notebook 信息
- notebook_path: {notebook_info.get("notebook_path", "")}
- notebook_url: {notebook_info.get("notebook_url", "")}

"""

    return f"""## 当前状态
- champion_score: {baseline_score:.4f}
- champion_factors: {seed_factors[0] if seed_factors else []}
- current_iter: 0
- consecutive_failures: 0
- phase: explore

## 回测配置
- 训练区间: {train_start} ~ {backtest_start}（约1年）
- 回测区间: {backtest_start} ~ {backtest_end}（约3个月）
- 选股池: {pool}

{notebook_section}## 已尝试组合
| iter | score | factors | strategy |
|------|-------|---------|----------|
| 0000 | {baseline_score:.4f} | {seed_factors[0] if seed_factors else []} | seed |

## 搜索地图

### 已验证有效（keep）
- {seed_factors[0] if seed_factors else []}: score={baseline_score:.4f}

### 已验证无效（rollback）
- （无）

### 待探索方向
- [ ] 从高分组合变异，替换1个因子
- [ ] 随机采样新组合
- [ ] 频率优先采样
"""


def run_baseline(strategy_file, notebook_dir=None):
    from notebook_executor import execute_strategy

    print("[baseline] 执行 baseline 回测...")
    result = execute_strategy(
        str(strategy_file), timeout_ms=600000, notebook_dir=notebook_dir
    )

    if result["success"]:
        return result.get("score", 0), result.get("diversity", 0), result
    else:
        print(f"[baseline] 执行失败: {result.get('error')}")
        return 0, 0, result


def main():
    parser = argparse.ArgumentParser(
        description="因子搜索实验初始化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python setup.py --name my_search
  python setup.py --name my_search --period D
  python setup.py --name my_search --period W
  python setup.py --name my_search --period M
  python setup.py --name my_search --train-start 2024-04-01 --backtest-start 2025-01-01 --backtest-end 2025-04-01
  python setup.py --name my_search --pool HS300 --seed-factors "[['size','roe_ttm'],['momentum','beta']]"
        """,
    )
    parser.add_argument("--name", required=True, help="实验名称")
    parser.add_argument(
        "--train-start",
        default=_train_start,
        help=f"训练开始日期（默认 {_train_start}）",
    )
    parser.add_argument(
        "--backtest-start",
        default=_backtest_start,
        help=f"回测开始日期（默认 {_backtest_start}）",
    )
    parser.add_argument(
        "--backtest-end",
        default=_backtest_end,
        help=f"回测结束日期（默认 {_backtest_end}）",
    )
    parser.add_argument(
        "--pool",
        default="small",
        choices=["small", "A", "HS300", "ZZ500", "ZZ800"],
        help="选股池",
    )
    parser.add_argument(
        "--seed-factors", default=None, help="种子因子组合（JSON 格式）"
    )
    parser.add_argument(
        "--period",
        default=DEFAULT_PERIOD,
        choices=["D", "W", "M"],
        help=f"周期频率（默认 {DEFAULT_PERIOD}）",
    )
    parser.add_argument(
        "--notebook-dir", default=None, help="joinquant_notebook 目录路径"
    )
    args = parser.parse_args()

    period_config = PERIOD_CONFIG[args.period]

    ts = datetime.now().strftime("%Y%m%d")
    exp_name = f"strategy_autoresearch_factor_{args.name}_{ts}"
    base = PARENT_DIR / exp_name

    print(f"[setup] 实验目录: {base}")
    print(f"[setup] 周期频率: {args.period}（{period_config['name']}）")
    print(
        f"[setup] 训练区间: {args.train_start} ~ {args.backtest_start}（约{period_config['train_years']}年）"
    )
    print(
        f"[setup] 回测区间: {args.backtest_start} ~ {args.backtest_end}（约{period_config['test_months']}个月）"
    )
    print(f"[setup] 选股池: {args.pool}")

    if base.exists():
        print(f"[错误] 目录已存在: {base}")
        sys.exit(1)

    base.mkdir(parents=True)
    print("[setup] 创建实验目录")

    subprocess.run(["git", "init"], cwd=str(base), capture_output=True)
    print("[setup] git init")

    seed_factors = parse_seed_factors(args.seed_factors)
    print(f"[setup] 种子组合数: {len(seed_factors)}")

    strategy_file = base / "strategy.py"
    strategy_content = STRATEGY_TEMPLATE.format(
        factors=seed_factors[0],
        train_start=args.train_start,
        backtest_start=args.backtest_start,
        backtest_end=args.backtest_end,
        pool=args.pool,
        period=args.period,
        periods_per_year=period_config["periods_per_year"],
    )
    strategy_file.write_text(strategy_content, encoding="utf-8")
    print("[setup] 生成 strategy.py")

    subprocess.run(["git", "add", "strategy.py"], cwd=str(base), capture_output=True)
    r = subprocess.run(
        ["git", "commit", "-m", "iter_0000_baseline: initial seed factors"],
        cwd=str(base),
        capture_output=True,
        text=True,
    )
    if r.returncode == 0:
        print("[setup] git commit baseline")

    src_program = AUTORESEARCH_DIR / "program.md"
    if src_program.exists():
        content = src_program.read_text(encoding="utf-8")
        content = content.replace("AUTORESEARCH_DIR_PLACEHOLDER", str(AUTORESEARCH_DIR))
        (base / "program.md").write_text(content, encoding="utf-8")
        print("[setup] 生成 program.md")

    baseline_score, baseline_diversity, baseline_result = run_baseline(
        strategy_file, args.notebook_dir
    )
    print(f"[baseline] score={baseline_score:.4f}, diversity={baseline_diversity:.2f}")

    init_iterations_tsv(base)
    append_tsv(
        base,
        {
            "iter": "0000",
            "score": baseline_score,
            "diversity": baseline_diversity,
            "annual_return": baseline_result.get("metrics", {}).get("annual_return", 0),
            "max_drawdown": baseline_result.get("metrics", {}).get("max_drawdown", 0),
            "decision": "keep",
            "mutation": f"【L0-建立基准】初始因子组合 {seed_factors[0]}",
        },
    )
    print("[setup] 生成 iterations.tsv")

    search_notes = generate_search_notes(
        seed_factors,
        args.train_start,
        args.backtest_start,
        args.backtest_end,
        args.pool,
        baseline_score,
        None,
    )
    (base / "search_notes.md").write_text(search_notes, encoding="utf-8")
    print("[setup] 生成 search_notes.md")

    print(f"\n[setup] 全部完成！")
    print(f"  实验目录: {base}")
    print(f"  下一步：cd {base} 然后阅读 program.md 开始迭代")


if __name__ == "__main__":
    main()
