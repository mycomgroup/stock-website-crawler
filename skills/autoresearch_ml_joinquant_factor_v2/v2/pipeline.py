"""WeakFactorPipelineV2 — 完整 pipeline 集成 (Task 8.1)

串联 L0→L1→L2→L3→L4→L7，确保严格串行因果链。

**Validates: Requirements 1-8, 12**
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from .data.pit_panel import FactorPanel, build_pit_panel
from .family.family_map import FAMILY_MAP, get_family_factors
from .portfolio.optimizer import TopNEqualWeightOptimizer
from .preprocessing.factor_preprocessor import (
    impute_factors,
    standardize_factors,
    winsorize_cross_section,
)
from .synthesis.cross_family import CrossFamilyModel
from .synthesis.intra_family import (
    equal_rank_score,
    pc1_score_with_sign_anchor,
    ridge_family_score,
    stack_family_scores_oof,
)
from .validation.walk_forward import FinalHoldoutPartition, WalkForwardSplitter

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Pipeline configuration parameters."""

    # L0: Data governance
    csv_path: str | Path = "skills/autoresearch_ml_joinquant_factor_v2/train_merged_all.csv"
    new_stock_cooldown_days: int = 60

    # L1: Preprocessing
    mad_multiplier: float = 5.0
    missing_rate_threshold: float = 0.30

    # L2: Family mapping (frozen)
    use_family_map: dict = field(default_factory=lambda: FAMILY_MAP)

    # L3: Intra-family synthesis
    intra_family_method: str = "stack"  # "equal_rank" | "ridge" | "pc1" | "stack"

    # L4: Cross-family synthesis
    alpha_reg_grid: list[float] = field(
        default_factory=lambda: [0.001, 0.01, 0.1, 1.0, 10.0]
    )
    l1_ratio_grid: list[float] = field(default_factory=lambda: [0.0, 0.1, 0.5])
    max_single_family_weight: float = 0.4
    weight_smoothing_halflife: int = 4

    # L7: Portfolio optimization
    n_stocks: int = 50
    max_single_weight: float = 0.03
    max_turnover: float = 0.30

    # OOF validation
    min_train_periods: int = 260
    test_block: int = 52
    step: int = 4
    embargo: int = 1
    holdout_periods: int = 104

    # Reproducibility
    random_state: int = 42


class WeakFactorPipelineV2:
    """弱因子组合量化策略 v2 完整 pipeline。

    严格串行因果链：L0 → L1 → L2 → L3 → L4 → L7

    **Validates: Requirements 1-8, 12**
    """

    def __init__(self, config: PipelineConfig | None = None):
        self.config = config or PipelineConfig()
        self.panel: FactorPanel | None = None
        self.holdout_partition = FinalHoldoutPartition(
            holdout_periods=self.config.holdout_periods
        )
        logger.info("WeakFactorPipelineV2 initialized with config: %s", self.config)

    def run(self, use_holdout: bool = False) -> dict:
        """运行完整 pipeline。

        Parameters
        ----------
        use_holdout : bool
            是否使用 final holdout（默认 False，研究阶段使用 research OOS）

        Returns
        -------
        dict
            Pipeline 运行结果，包含：
            - "oof_predictions": OOF alpha 预测
            - "weights": 组合权重
            - "metrics": 评估指标
        """
        logger.info("=" * 80)
        logger.info("WeakFactorPipelineV2.run: 开始运行 pipeline")
        logger.info("=" * 80)

        # ---- L0: 数据治理 ----------------------------------------
        logger.info("[L0] 数据治理：加载点时一致因子面板")
        self.panel = build_pit_panel(
            self.config.csv_path,
            new_stock_cooldown_days=self.config.new_stock_cooldown_days,
        )
        logger.info(
            "[L0] 完成：%s", self.panel
        )

        # 分区：research vs holdout
        if use_holdout:
            logger.warning(
                "[L0] 使用 final holdout（访问次数=%d）",
                self.holdout_partition.access_count,
            )
            df_partition = self.holdout_partition.get_holdout_data(self.panel.df)
        else:
            logger.info("[L0] 使用 research OOS（不访问 final holdout）")
            df_partition = self.holdout_partition.get_research_data(self.panel.df)

        tradable_mask = self.panel.tradable_mask.reindex(
            df_partition.index,
            fill_value=False,
        )
        df = df_partition.loc[tradable_mask].copy()
        logger.info("[L0] 应用可交易掩码后：%d 行", len(df))

        # ---- L1: 因子预处理 --------------------------------------
        logger.info("[L1] 因子预处理：winsor → impute → standardize")

        factor_cols = self.panel.factor_cols

        # Step 1: Winsorization
        df_winsor = winsorize_cross_section(
            df, factor_cols, mad_multiplier=self.config.mad_multiplier
        )
        logger.info("[L1.1] Winsorization 完成")

        # Step 2: Imputation
        df_imputed, factor_weights = impute_factors(
            df_winsor,
            factor_cols,
            missing_rate_threshold=self.config.missing_rate_threshold,
        )
        logger.info(
            "[L1.2] Imputation 完成，%d 个因子降权（缺失率 > %.1f%%）",
            sum(1 for w in factor_weights.values() if w < 1.0),
            self.config.missing_rate_threshold * 100,
        )

        # Step 3: Standardization (use rank representation)
        df_rank, df_zscore = standardize_factors(df_imputed, factor_cols)
        logger.info("[L1.3] Standardization 完成（双轨：rank + zscore）")

        # Use rank representation for downstream (more robust)
        df_clean = df_rank

        # ---- L2: 因子家族划分（冻结映射）------------------------
        logger.info("[L2] 因子家族划分：使用冻结的 9 家族映射")
        family_map = self.config.use_family_map
        logger.info(
            "[L2] 完成：%d 个家族，%d 个因子",
            len(family_map),
            sum(len(f) for f in family_map.values()),
        )

        # ---- L3: 组内合成 ----------------------------------------
        logger.info("[L3] 组内合成：为每个家族生成代表分数")

        family_scores = {}
        label_series = df_clean.set_index(["date", "stock_id"])["pchg"]
        for family_name, family_factors in family_map.items():
            # Filter factors that exist in df_clean
            available_factors = [f for f in family_factors if f in df_clean.columns]
            if not available_factors:
                logger.warning(
                    "[L3] 家族 '%s' 无可用因子，跳过", family_name
                )
                continue

            logger.info(
                "[L3] 处理家族 '%s'（%d 个因子）",
                family_name,
                len(available_factors),
            )

            if self.config.intra_family_method == "equal_rank":
                family_score = equal_rank_score(df_clean, available_factors)
            elif self.config.intra_family_method == "ridge":
                family_score = ridge_family_score(
                    df_clean,
                    available_factors,
                    label_col="pchg",
                    min_train_periods=self.config.min_train_periods,
                    test_block=self.config.test_block,
                    step=self.config.step,
                    embargo=self.config.embargo,
                )
            elif self.config.intra_family_method == "pc1":
                family_score = pc1_score_with_sign_anchor(df_clean, available_factors)
            elif self.config.intra_family_method == "stack":
                eq_score = equal_rank_score(df_clean, available_factors)
                ridge_score = ridge_family_score(
                    df_clean,
                    available_factors,
                    label_col="pchg",
                    min_train_periods=self.config.min_train_periods,
                    test_block=self.config.test_block,
                    step=self.config.step,
                    embargo=self.config.embargo,
                )
                pc1_score = pc1_score_with_sign_anchor(
                    df_clean,
                    available_factors,
                    anchor_score=eq_score,
                )
                family_score = stack_family_scores_oof(
                    eq_score,
                    ridge_score,
                    pc1_score,
                    label_series,
                )
            else:
                raise ValueError(
                    f"Unknown intra_family_method: {self.config.intra_family_method}"
                )
            family_scores[family_name] = family_score

        logger.info("[L3] 完成：生成 %d 个家族分数", len(family_scores))

        # ---- L4: 组间收缩合成 ------------------------------------
        logger.info("[L4] 组间收缩合成：rolling ridge/elastic net")

        # Assemble family scores matrix
        y = label_series
        S = pd.DataFrame(family_scores)

        # Align S and y
        common_idx = S.index.intersection(y.index)
        S = S.loc[common_idx]
        y = y.loc[common_idx]

        logger.info(
            "[L4] 家族分数矩阵：%d 行 × %d 列（家族）", len(S), len(S.columns)
        )

        # Fit cross-family model (simplified: use default params for Phase 1)
        cross_family_model = CrossFamilyModel(
            alpha_reg_grid=self.config.alpha_reg_grid,
            l1_ratio_grid=self.config.l1_ratio_grid,
            max_single_family_weight=self.config.max_single_family_weight,
            weight_smoothing_halflife=self.config.weight_smoothing_halflife,
        )

        # For Phase 1, use a simple train/test split (full OOF walk-forward in task 8.4)
        dates = sorted(S.index.get_level_values("date").unique())
        split_idx = int(len(dates) * 0.7)
        train_dates = dates[:split_idx]
        test_dates = dates[split_idx:]

        S_train = S[S.index.get_level_values("date").isin(train_dates)]
        y_train = y[y.index.isin(S_train.index)]

        best_alpha, best_l1_ratio = cross_family_model.select_hyperparams(S_train, y_train)
        cross_family_model.fit(
            S_train,
            y_train,
            best_alpha=best_alpha,
            best_l1_ratio=best_l1_ratio,
        )
        logger.info("[L4] CrossFamilyModel 训练完成，beta=%s", cross_family_model.current_beta)

        # 仅对测试区间预测，避免训练样本内推断造成评价口径污染
        S_test = S[S.index.get_level_values("date").isin(test_dates)]
        alpha_linear = cross_family_model.predict(S_test if len(S_test) > 0 else S)
        logger.info("[L4] 完成：生成 %d 个 alpha_linear 预测", len(alpha_linear))

        # ---- L7: 组合优化 ----------------------------------------
        logger.info("[L7] 组合优化：Top-N 等权")

        optimizer = TopNEqualWeightOptimizer(
            n_stocks=self.config.n_stocks,
            max_single_weight=self.config.max_single_weight,
            max_turnover=self.config.max_turnover,
        )

        # For each date, compute weights
        all_weights = []
        for date in sorted(alpha_linear.index.get_level_values("date").unique()):
            date_alpha = alpha_linear.xs(date, level="date")
            date_rows = df_partition["date"] == date
            date_stock_ids = df_partition.loc[date_rows, "stock_id"].values
            date_tradable_values = tradable_mask.loc[df_partition.index[date_rows]].values
            date_tradable = pd.Series(
                date_tradable_values,
                index=date_stock_ids,
                dtype=bool,
            ).groupby(level=0).max()

            # Get prev weights (if available)
            if all_weights:
                prev_w = all_weights[-1]
            else:
                prev_w = None

            weights = optimizer.optimize(date_alpha, date_tradable, prev_weights=prev_w)
            weights.name = date
            all_weights.append(weights)

        logger.info("[L7] 完成：生成 %d 个再平衡日的权重", len(all_weights))

        # ---- 返回结果 --------------------------------------------
        result = {
            "oof_predictions": alpha_linear,
            "weights": all_weights,
            "family_scores": S,
            "family_beta": cross_family_model.current_beta,
            "config": self.config,
        }

        logger.info("=" * 80)
        logger.info("WeakFactorPipelineV2.run: pipeline 运行完成")
        logger.info("=" * 80)

        return result
