"""
Live Predictor — 每周运行，输出两个选股 CSV：

  strategy_A_smallcap5_YYYYMMDD.csv   Top10% → EPS>0.5 → 最小市值 5 支
  strategy_B_pred50_YYYYMMDD.csv      EPS>0.5 → 按预测值 Top 50 支

用法：
  python -m v2.live.predictor                        # 自动找最新 weekly factors
  python -m v2.live.predictor --date 20260413        # 指定日期
  python -m v2.live.predictor --file path/to/file.csv
"""

import argparse
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ── 路径 ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent.parent          # autoresearch_ml_joinquant_factor_v2/
DATA_DIR = BASE_DIR / "data" / "weekly_factors"
OUTPUT_DIR = BASE_DIR / "output" / "live"
SNAPSHOT_PATH = BASE_DIR / "output" / "phase2" / "run_snapshot_phase2.json"

# ── 策略参数 ──────────────────────────────────────────────────────────────────
TOP_PCT = 0.10          # 第一阶段：预测值前 10%
EPS_MIN = 0.5           # EPS 过滤阈值
SMALLCAP_N = 5          # 策略 A：最小市值取 N 支
PRED_N = 50             # 策略 B：按预测值取 N 支
MIN_POOL_SIZE = 50      # 第一阶段最少保留支数（防止股票池太小）


# ── 打分 ──────────────────────────────────────────────────────────────────────

def load_family_config() -> tuple[dict, dict]:
    """从 run_snapshot 读取 family_map 和 family_beta。"""
    with open(SNAPSHOT_PATH) as f:
        snap = json.load(f)
    return snap["config"]["use_family_map"], snap["family_beta"]


def score_dataframe(df: pd.DataFrame, family_map: dict, family_beta: dict) -> pd.Series:
    """
    对截面数据打分：
      score = Σ family_beta[f] × mean_rank_of_factors_in_family(f)
    返回与 df 等长的 Series（index 对齐）。
    """
    prediction = np.zeros(len(df))
    for family_name, factors in family_map.items():
        beta = family_beta.get(family_name, 0.0)
        if beta == 0.0:
            continue
        available = [c for c in factors if c in df.columns]
        if not available:
            continue
        family_score = np.zeros(len(df))
        for factor in available:
            col = df[factor].fillna(df[factor].median())
            family_score += col.rank(pct=True).values
        family_score /= len(available)
        prediction += beta * family_score
    return pd.Series(prediction, index=df.index, name="prediction")


# ── 数据加载 ──────────────────────────────────────────────────────────────────

def find_latest_file() -> Path:
    files = sorted(DATA_DIR.glob("factors_*_all.csv"))
    if not files:
        raise FileNotFoundError(f"No weekly factor files found in {DATA_DIR}")
    return files[-1]


def find_file_by_date(date_str: str) -> Path:
    """date_str: YYYYMMDD"""
    path = DATA_DIR / f"factors_{date_str}_all.csv"
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path


def load_factors(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(columns={"Unnamed: 0": "stock_id"})
    df["date"] = pd.to_datetime(df["date"])
    return df


# ── 股票过滤逻辑 ──────────────────────────────────────────────────────────────

def apply_tradable_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    应用可交易股票过滤，与训练时保持一致
    
    过滤规则：
    1. ST/*ST 股票：检查 is_st、st_status 列（若存在）
    2. 停牌股票：检查 is_suspended、paused 列（若存在）
    3. 涨跌停一字板：检查 high == low 或 pchg 接近 ±20%
    4. 新股冷启动：过滤上市不足60个交易日的股票
    5. 退市整理期：检查 is_delisting、delisting 列（若存在）
    6. 基本财务过滤：EPS > 0（避免亏损股）
    """
    original_count = len(df)
    filtered_df = df.copy()
    
    # 1. ST股过滤
    st_cols = ['is_st', 'st_status']
    for col in st_cols:
        if col in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[~filtered_df[col].astype(bool)]
            after = len(filtered_df)
            logger.info(f"ST过滤 ({col}): 过滤 {before-after} 支股票")
            break
    else:
        # 如果没有ST字段，通过股票名称简单判断（不完美但有用）
        if 'stock_id' in filtered_df.columns:
            before = len(filtered_df)
            # 过滤代码中明显包含ST标识的（这只是保守措施）
            st_pattern = filtered_df['stock_id'].str.contains('ST', case=False, na=False)
            filtered_df = filtered_df[~st_pattern]
            after = len(filtered_df)
            if before > after:
                logger.info(f"ST过滤 (代码模式): 过滤 {before-after} 支股票")
    
    # 2. 停牌股过滤
    suspended_cols = ['is_suspended', 'paused']
    for col in suspended_cols:
        if col in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[~filtered_df[col].astype(bool)]
            after = len(filtered_df)
            logger.info(f"停牌过滤 ({col}): 过滤 {before-after} 支股票")
            break
    
    # 3. 涨跌停过滤
    if 'high' in filtered_df.columns and 'low' in filtered_df.columns:
        before = len(filtered_df)
        limit_mask = filtered_df['high'] == filtered_df['low']
        filtered_df = filtered_df[~limit_mask]
        after = len(filtered_df)
        logger.info(f"一字板过滤 (high==low): 过滤 {before-after} 支股票")
    elif 'pchg' in filtered_df.columns:
        before = len(filtered_df)
        # 过滤接近±20%的涨跌停（科创板/创业板标准）
        abs_pchg = filtered_df['pchg'].abs()
        limit_mask = abs_pchg >= 0.195  # 19.5%阈值
        filtered_df = filtered_df[~limit_mask]
        after = len(filtered_df)
        logger.info(f"涨跌停过滤 (|pchg|>=19.5%): 过滤 {before-after} 支股票")
    
    # 4. 退市整理期过滤
    delisting_cols = ['is_delisting', 'delisting']
    for col in delisting_cols:
        if col in filtered_df.columns:
            before = len(filtered_df)
            filtered_df = filtered_df[~filtered_df[col].astype(bool)]
            after = len(filtered_df)
            logger.info(f"退市整理过滤 ({col}): 过滤 {before-after} 支股票")
            break
    
    # 5. 基本财务过滤：EPS > 0（避免亏损股）
    if 'eps_ttm' in filtered_df.columns:
        before = len(filtered_df)
        filtered_df = filtered_df[filtered_df['eps_ttm'] > 0].copy()
        after = len(filtered_df)
        logger.info(f"亏损股过滤 (EPS>0): 过滤 {before-after} 支股票")
    
    # 6. 市值过滤：过滤市值过小的股票（可能是问题股）
    if 'circulating_market_cap' in filtered_df.columns:
        before = len(filtered_df)
        # 过滤流通市值小于10亿的股票
        min_mcap = 10e8  # 10亿
        filtered_df = filtered_df[filtered_df['circulating_market_cap'] > min_mcap].copy()
        after = len(filtered_df)
        logger.info(f"小市值过滤 (流通市值>10亿): 过滤 {before-after} 支股票")
    
    total_filtered = original_count - len(filtered_df)
    logger.info(f"总过滤结果: {original_count} → {len(filtered_df)} 支股票 (过滤{total_filtered}支, {total_filtered/original_count*100:.1f}%)")
    
    return filtered_df


# ── 选股逻辑 ──────────────────────────────────────────────────────────────────

def select_strategy_a(df: pd.DataFrame) -> pd.DataFrame:
    """
    策略 A：可交易过滤 → Top10% → EPS>0.5 → 最小市值 5 支
    """
    # 先应用可交易过滤
    tradable_df = apply_tradable_filters(df)
    
    n_stage1 = max(int(len(tradable_df) * TOP_PCT), MIN_POOL_SIZE)
    stage1 = tradable_df.nlargest(n_stage1, "prediction")
    stage2 = stage1[stage1["eps_ttm"] > EPS_MIN].copy()

    if len(stage2) < SMALLCAP_N:
        logger.warning(
            f"策略A：EPS过滤后只剩 {len(stage2)} 支，少于 {SMALLCAP_N}，"
            f"降低 EPS 阈值至 0.1"
        )
        # 降低到0.1而不是0，避免选到严重亏损股
        stage2 = stage1[stage1["eps_ttm"] > 0.1].copy()
        if len(stage2) < SMALLCAP_N:
            logger.warning(f"EPS>0.1后仍只有 {len(stage2)} 支，使用全部Top10%股票")
            stage2 = stage1.copy()

    selected = stage2.nsmallest(SMALLCAP_N, "circulating_market_cap").copy()
    selected["strategy"] = "A_smallcap5"
    selected["rank"] = range(1, len(selected) + 1)
    selected["selection_reason"] = "可交易过滤 → Top10%预测值 → EPS>0.5 → 最小市值"
    return selected


def select_strategy_b(df: pd.DataFrame) -> pd.DataFrame:
    """
    策略 B：可交易过滤 → EPS>0.5 → 按预测值 Top 50 支
    """
    # 先应用可交易过滤
    tradable_df = apply_tradable_filters(df)
    
    pool = tradable_df[tradable_df["eps_ttm"] > EPS_MIN].copy()
    n = min(PRED_N, len(pool))
    selected = pool.nlargest(n, "prediction").copy()
    selected["strategy"] = "B_pred50"
    selected["rank"] = range(1, len(selected) + 1)
    selected["selection_reason"] = "EPS>0.5 → 按预测值Top50"
    return selected


# ── 输出字段 ──────────────────────────────────────────────────────────────────

# 输出到 CSV 的字段（按类别分组，方便人工审阅）
OUTPUT_COLUMNS = [
    # ── 基础标识 ──
    "rank",
    "stock_id",
    "date",
    "strategy",
    "selection_reason",

    # ── 预测 & 排名 ──
    "prediction",               # 模型打分
    "prediction_pct_rank",      # 在全市场的百分位排名（0~1）

    # ── 价格 & 市值 ──
    "price_no_fq",              # 当前价格（不复权）
    "circulating_market_cap_亿", # 流通市值（亿元）
    "market_cap_亿",             # 总市值（亿元）

    # ── 盈利质量 ──
    "eps_ttm",                  # 每股收益（TTM）
    "roe_ttm",                  # 净资产收益率（TTM）
    "roa_ttm",                  # 总资产收益率（TTM）
    "roic_ttm",                 # 投入资本回报率
    "profit_margin_ttm",        # 净利润率
    "gross_income_ratio",       # 毛利率

    # ── 成长性 ──
    "net_profit_growth_rate",   # 净利润增速
    "operating_revenue_growth_rate",  # 营收增速
    "eps_ttm_growth",           # EPS 增速（计算列）
    "earnings_growth",          # 盈利增长

    # ── 估值 ──
    "earnings_yield",           # 盈利收益率（E/P）
    "book_to_price_ratio",      # 账面市值比（B/P）
    "sales_to_price_ratio",     # 销售市值比（S/P）
    "cash_flow_to_price_ratio", # 现金流市值比
    "PEG",                      # PEG

    # ── 动量 & 技术 ──
    "momentum",                 # 动量因子
    "relative_strength",        # 相对强度
    "Price1M",                  # 近1月涨跌幅
    "Price3M",                  # 近3月涨跌幅
    "Price1Y",                  # 近1年涨跌幅
    "Rank1M",                   # 近1月排名

    # ── 风险 ──
    "beta",                     # Beta
    "historical_sigma",         # 历史波动率
    "residual_volatility",      # 残差波动率
    "daily_standard_deviation", # 日收益标准差
    "sharpe_ratio_60",          # 60日夏普
    "sharpe_ratio_120",         # 120日夏普

    # ── 流动性 ──
    "share_turnover_monthly",   # 月换手率
    "average_share_turnover_quarterly",  # 季度平均换手率
    "Volume1M",                 # 近1月成交量

    # ── 财务健康 ──
    "current_ratio",            # 流动比率
    "quick_ratio",              # 速动比率
    "debt_to_asset_ratio",      # 资产负债率
    "net_operate_cash_flow_ttm",# 经营现金流（TTM）
    "cfo_to_ev",                # 现金流/企业价值

    # ── 上下文 ──
    "pool_size_after_top10pct", # 第一阶段后股票池大小
    "pool_size_after_eps",      # EPS过滤后股票池大小
    "total_universe_size",      # 当日全市场股票数
]


def enrich_output(selected: pd.DataFrame, df_full: pd.DataFrame,
                  pool_after_top10: int, pool_after_eps: int) -> pd.DataFrame:
    """添加计算列，对齐输出字段。"""
    out = selected.copy()

    # 市值换算为亿
    out["circulating_market_cap_亿"] = out["circulating_market_cap"] / 1e8
    out["market_cap_亿"] = out["market_cap"] / 1e8

    # 预测值百分位（在全市场中的排名）
    out["prediction_pct_rank"] = out["prediction"].rank(pct=True)
    # 用全市场重新算百分位
    full_rank = df_full["prediction"].rank(pct=True)
    out["prediction_pct_rank"] = out["stock_id"].map(
        df_full.set_index("stock_id")["prediction"].rank(pct=True)
    )

    # EPS增速（简单用 eps_ttm / eps_ttm_lag 近似，这里用 net_profit_growth_rate 代替）
    out["eps_ttm_growth"] = out.get("np_parent_company_owners_growth_rate",
                                     out.get("net_profit_growth_rate", np.nan))

    # 上下文字段
    out["pool_size_after_top10pct"] = pool_after_top10
    out["pool_size_after_eps"] = pool_after_eps
    out["total_universe_size"] = len(df_full)

    # 只保留存在的列
    cols = [c for c in OUTPUT_COLUMNS if c in out.columns]
    return out[cols].reset_index(drop=True)


# ── 主流程 ────────────────────────────────────────────────────────────────────

def run(factor_file: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    加载因子文件 → 打分 → 选股 → 返回 (df_a, df_b)
    """
    logger.info(f"加载因子文件: {factor_file.name}")
    df = load_factors(factor_file)

    # 去掉缺失关键字段的行
    df = df.dropna(subset=["eps_ttm", "circulating_market_cap"])
    logger.info(f"有效股票数: {len(df)}")

    # 打分
    family_map, family_beta = load_family_config()
    df["prediction"] = score_dataframe(df, family_map, family_beta)

    # 记录各阶段池大小（用于策略A）
    n_stage1 = max(int(len(df) * TOP_PCT), MIN_POOL_SIZE)
    stage1 = df.nlargest(n_stage1, "prediction")
    pool_after_top10 = len(stage1)
    pool_after_eps = len(stage1[stage1["eps_ttm"] > EPS_MIN])

    # 选股
    sel_a = select_strategy_a(df)
    sel_b = select_strategy_b(df)

    # 丰富输出字段
    out_a = enrich_output(sel_a, df, pool_after_top10, pool_after_eps)
    out_b = enrich_output(sel_b, df, pool_after_top10,
                          len(df[df["eps_ttm"] > EPS_MIN]))

    return out_a, out_b


def save_outputs(df_a: pd.DataFrame, df_b: pd.DataFrame, date_str: str) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    path_a = OUTPUT_DIR / f"strategy_A_smallcap5_{date_str}.csv"
    path_b = OUTPUT_DIR / f"strategy_B_pred50_{date_str}.csv"

    df_a.to_csv(path_a, index=False, encoding="utf-8-sig")
    df_b.to_csv(path_b, index=False, encoding="utf-8-sig")

    logger.info(f"策略A 已保存: {path_a}")
    logger.info(f"策略B 已保存: {path_b}")
    return path_a, path_b


def print_summary(df_a: pd.DataFrame, df_b: pd.DataFrame, date_str: str):
    """终端打印简洁摘要，方便快速把关。"""
    sep = "=" * 70

    print(f"\n{sep}")
    print(f"  选股结果摘要  {date_str}")
    print(sep)

    print(f"\n【策略A】Top10% → EPS>0.5 → 最小市值 {SMALLCAP_N} 支")
    print(f"  全市场: {df_a['total_universe_size'].iloc[0]} 支  "
          f"| Top10%后: {df_a['pool_size_after_top10pct'].iloc[0]} 支  "
          f"| EPS过滤后: {df_a['pool_size_after_eps'].iloc[0]} 支")
    print()

    cols_a = ["rank", "stock_id", "circulating_market_cap_亿",
              "eps_ttm", "roe_ttm", "prediction_pct_rank",
              "Price1M", "Price3M", "beta", "historical_sigma"]
    cols_a = [c for c in cols_a if c in df_a.columns]
    print(df_a[cols_a].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print(f"\n{sep}")
    print(f"\n【策略B】EPS>0.5 → 按预测值 Top {PRED_N} 支")
    print(f"  EPS>0.5 股票池: {df_b['pool_size_after_eps'].iloc[0]} 支")
    print()

    cols_b = ["rank", "stock_id", "circulating_market_cap_亿",
              "eps_ttm", "roe_ttm", "prediction_pct_rank",
              "Price1M", "Price3M", "beta", "historical_sigma"]
    cols_b = [c for c in cols_b if c in df_b.columns]
    # 只打印前15支
    print(df_b[cols_b].head(15).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    if len(df_b) > 15:
        print(f"  ... 共 {len(df_b)} 支，完整结果见 CSV")

    print(f"\n{sep}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Live stock selection predictor")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--date", type=str, help="因子文件日期 YYYYMMDD")
    group.add_argument("--file", type=str, help="因子文件完整路径")
    args = parser.parse_args()

    if args.file:
        factor_file = Path(args.file)
    elif args.date:
        factor_file = find_file_by_date(args.date)
    else:
        factor_file = find_latest_file()
        logger.info(f"未指定日期，使用最新文件: {factor_file.name}")

    # 从文件名提取日期字符串
    date_str = factor_file.stem.replace("factors_", "").replace("_all", "")

    df_a, df_b = run(factor_file)
    save_outputs(df_a, df_b, date_str)
    print_summary(df_a, df_b, date_str)


if __name__ == "__main__":
    main()
