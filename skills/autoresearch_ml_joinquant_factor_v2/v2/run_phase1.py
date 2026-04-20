"""Phase 1 Pipeline 端到端验证脚本 (Task 8.4)

在测试数据上运行完整 Phase 1 pipeline，验证 OOF rank IC > 0.03。

使用方法（从项目根目录运行）：
    python3 -c "
    import sys; sys.path.insert(0, '.')
    from skills.autoresearch_ml_joinquant_factor_v2.v2.run_phase1 import run_phase1_validation
    result = run_phase1_validation()
    print(result)
    "

或使用小型测试数据（推荐，避免内存溢出）：
    python3 -c "
    import sys; sys.path.insert(0, '.')
    from skills.autoresearch_ml_joinquant_factor_v2.v2.run_phase1 import run_phase1_validation
    result = run_phase1_validation(use_small_data=True)
    print(result)
    "

**Validates: Requirements 8.4**
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# 数据路径
_BASE = Path(__file__).parent.parent
CSV_PATH_FULL = _BASE / "train_merged_all.csv"
CSV_PATH_SMALL = _BASE / "test_data_small.csv"
OUTPUT_DIR = _BASE / "output" / "phase1"


def compute_oof_rank_ic(alpha: pd.Series, label: pd.Series) -> float:
    """计算 OOF rank IC（Spearman 相关系数）。"""
    # Align on common index
    common_idx = alpha.index.intersection(label.index)
    if len(common_idx) < 10:
        return float("nan")
    a = alpha.loc[common_idx].dropna()
    l = label.loc[common_idx].dropna()
    common = a.index.intersection(l.index)
    if len(common) < 10:
        return float("nan")
    # Compute cross-sectional IC per date, then average
    dates = common.get_level_values("date").unique()
    ic_list = []
    for date in dates:
        try:
            a_d = a.xs(date, level="date")
            l_d = l.xs(date, level="date")
            both = a_d.index.intersection(l_d.index)
            if len(both) < 5:
                continue
            corr, _ = stats.spearmanr(a_d.loc[both], l_d.loc[both])
            if not np.isnan(corr):
                ic_list.append(corr)
        except Exception:
            continue
    if not ic_list:
        return float("nan")
    return float(np.mean(ic_list))


def run_phase1_validation(use_small_data: bool = True) -> dict:
    """运行 Phase 1 pipeline 并验证 OOF rank IC > 0.03。

    Parameters
    ----------
    use_small_data : bool
        True = 使用小型测试数据（推荐，避免内存溢出）
        False = 使用完整 train_merged_all.csv

    Returns
    -------
    dict
        验证结果。
    """
    # 选择数据路径
    csv_path = CSV_PATH_SMALL if use_small_data else CSV_PATH_FULL
    if not csv_path.exists():
        if use_small_data:
            logger.info("小型测试数据不存在，正在生成...")
            from .generate_test_data import generate_small_dataset
            generate_small_dataset(output_path=csv_path)
        else:
            return {"error": f"数据文件不存在：{csv_path}"}

    logger.info("=" * 70)
    logger.info("Phase 1 Pipeline 验证开始（数据：%s）", csv_path.name)
    logger.info("=" * 70)

    # ---- 导入模块 ------------------------------------------------
    from .data.pit_panel import build_pit_panel
    from .family.family_map import FAMILY_MAP, ALL_FACTORS
    from .preprocessing.factor_preprocessor import (
        impute_factors,
        standardize_factors,
        winsorize_cross_section,
    )
    from .synthesis.intra_family import equal_rank_score
    from .synthesis.cross_family import CrossFamilyModel
    from .results.persistence import save_oof_predictions, save_run_snapshot
    from .pipeline import PipelineConfig

    # ---- L0: 加载数据 ----------------------------------------
    logger.info("[L0] 加载数据：%s", csv_path)
    panel = build_pit_panel(csv_path)
    df = panel.df
    tradable_mask = panel.tradable_mask
    logger.info("[L0] 完成：%s", panel)

    # 使用 research data（排除最后 104 周作为 final holdout）
    dates = sorted(df["date"].unique())
    n_holdout = min(104, len(dates) // 5)  # 小数据集用 20% 作为 holdout
    if len(dates) > n_holdout + 10:
        research_dates = dates[:-n_holdout]
        df = df[df["date"].isin(research_dates)].copy()
        tradable_mask = tradable_mask.loc[df.index]
        logger.info("[L0] Research data：%d 个截面日期（排除最后 %d 周 holdout）",
                    len(research_dates), n_holdout)

    # 只在可交易样本上训练和评估，确保 OOF 口径与可交易宇宙一致
    if not tradable_mask.empty:
        tradable_mask = tradable_mask.reindex(df.index, fill_value=False)
        df = df.loc[tradable_mask].copy()
        logger.info("[L0] 应用可交易掩码后：%d 行", len(df))

    # ---- L1: 预处理 ------------------------------------------
    logger.info("[L1] 因子预处理（winsor → impute → standardize）")

    # 只使用实际存在于 df 中的因子列
    all_factor_cols = [c for c in ALL_FACTORS if c in df.columns]
    logger.info("[L1] 可用因子：%d / %d", len(all_factor_cols), len(ALL_FACTORS))

    df_winsor = winsorize_cross_section(df, all_factor_cols)
    df_imputed, factor_weights = impute_factors(df_winsor, all_factor_cols)
    df_rank, _ = standardize_factors(df_imputed, all_factor_cols)
    logger.info("[L1] 完成")

    # ---- L2: 家族映射 ----------------------------------------
    logger.info("[L2] 家族映射（冻结 9 家族）")
    # 只保留在 df 中实际存在的因子
    active_family_map = {
        family: [f for f in factors if f in df_rank.columns]
        for family, factors in FAMILY_MAP.items()
    }
    active_families = {k: v for k, v in active_family_map.items() if v}
    logger.info("[L2] 活跃家族：%d，总因子：%d",
                len(active_families),
                sum(len(v) for v in active_families.values()))

    # ---- L3: 组内合成（等权基线）-----------------------------
    logger.info("[L3] 组内合成（等权基线）")
    family_scores = {}
    for family_name, family_factors in active_families.items():
        score = equal_rank_score(df_rank, family_factors)
        family_scores[family_name] = score
    logger.info("[L3] 完成：%d 个家族分数", len(family_scores))

    # ---- L4: 组间合成（walk-forward OOF）--------------------
    logger.info("[L4] 组间合成（walk-forward OOF）")

    # 组装家族分数矩阵
    S = pd.DataFrame(family_scores)
    y = df_rank.set_index(["date", "stock_id"])["pchg"]
    common_idx = S.index.intersection(y.index)
    S = S.loc[common_idx]
    y = y.loc[common_idx]

    all_dates = sorted(S.index.get_level_values("date").unique())
    n_dates = len(all_dates)

    # 根据数据量自适应参数
    min_train = min(200, int(n_dates * 0.6))
    test_block = max(10, int(n_dates * 0.05))
    step = max(4, test_block // 3)
    embargo = 1

    logger.info("[L4] Walk-forward 参数：min_train=%d, test_block=%d, step=%d, embargo=%d",
                min_train, test_block, step, embargo)

    oof_preds: dict = {}
    train_end = min_train - 1
    n_folds = 0

    while True:
        test_start = train_end + embargo + 1
        test_end = test_start + test_block - 1
        if test_end >= n_dates:
            break

        train_dates = all_dates[:train_end + 1]
        test_dates = all_dates[test_start:test_end + 1]

        train_mask = S.index.get_level_values("date").isin(train_dates)
        test_mask = S.index.get_level_values("date").isin(test_dates)

        S_train = S[train_mask]
        y_train = y[y.index.isin(S_train.index)]
        S_test = S[test_mask]

        if len(S_train) < 50:
            train_end += step
            continue

        try:
            model = CrossFamilyModel()
            model.fit(S_train, y_train, best_alpha=1.0, best_l1_ratio=0.0)
            preds = model.predict(S_test)
            for key, val in preds.items():
                if key not in oof_preds:
                    oof_preds[key] = val
            n_folds += 1
        except Exception as e:
            logger.warning("[L4] fold 训练失败：%s", e)

        train_end += step

    logger.info("[L4] 完成：%d 个 fold，%d 个 OOF 预测", n_folds, len(oof_preds))

    if not oof_preds:
        return {"error": "无 OOF 预测生成，数据量可能不足"}

    oof_series = pd.Series(oof_preds)
    # Rebuild proper MultiIndex
    keys = list(oof_preds.keys())
    vals = list(oof_preds.values())
    idx = pd.MultiIndex.from_tuples(keys, names=["date", "stock_id"])
    oof_series = pd.Series(vals, index=idx, name="oof_prediction")

    # ---- 计算 OOF rank IC ------------------------------------
    # y is indexed by (date, stock_id) — align with oof_series
    oof_ic = compute_oof_rank_ic(oof_series, y)
    logger.info("OOF rank IC = %.4f", oof_ic)

    passes = oof_ic > 0.03 if not np.isnan(oof_ic) else False
    logger.info(
        "验收标准（OOF rank IC > 0.03）：%s",
        "✓ 通过" if passes else "✗ 未通过（可能需要更多数据或更强信号）",
    )

    # ---- 保存结果 --------------------------------------------
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    save_oof_predictions(oof_series, OUTPUT_DIR, run_id="phase1")
    config = PipelineConfig(csv_path=str(csv_path))
    save_run_snapshot(config, OUTPUT_DIR, run_id="phase1", csv_path=csv_path)
    logger.info("[结果] 已保存到：%s", OUTPUT_DIR)

    result = {
        "oof_ic": oof_ic,
        "n_oof_predictions": len(oof_series),
        "n_dates_covered": oof_series.index.get_level_values("date").nunique(),
        "n_folds": n_folds,
        "passes_threshold": passes,
        "threshold": 0.03,
        "data_used": csv_path.name,
    }

    logger.info("=" * 70)
    logger.info("Phase 1 验证结果：%s", result)
    logger.info("=" * 70)
    return result


if __name__ == "__main__":
    result = run_phase1_validation(use_small_data=True)
    sys.exit(0 if result.get("passes_threshold", False) else 1)
