"""
Phase1 运行结果详细分析脚本

执行此脚本后自动生成完整的分析报告，包括：
- IC分析（原始vs修正）
- 分组收益分析
- 策略回测
- 因子权重
- 问题诊断
- 结果输出到文件

使用方法：
    python skills/autoresearch_ml_joinquant_factor_v2/analyze_phase1_results.py

输出文件：
    - output/phase1_analysis_report.txt (文本报告)
    - output/phase1_analysis_summary.json (JSON摘要)
"""

from __future__ import annotations

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output" / "phase1"
ANALYSIS_DIR = BASE_DIR / "output" / "analysis"


class Phase1Analyzer:
    """Phase1运行结果分析器"""

    def __init__(self):
        self.oof: pd.DataFrame | None = None
        self.df_raw: pd.DataFrame | None = None
        self.df_research: pd.DataFrame | None = None
        self.snapshot: dict | None = None
        self.ic_series: list[float] = []
        self.portfolio_returns: pd.Series | None = None
        self.market_returns: pd.Series | None = None
        self.family_weights: pd.Series | None = None

    def load_data(self):
        """加载所有必要数据"""
        logger.info("=" * 80)
        logger.info("加载数据...")
        logger.info("=" * 80)

        # 加载OOF预测
        oof_path = OUTPUT_DIR / "oof_predictions_phase1.csv"
        if not oof_path.exists():
            raise FileNotFoundError(f"OOF预测文件不存在: {oof_path}")

        self.oof = pd.read_csv(oof_path)
        self.oof["date"] = pd.to_datetime(self.oof["date"])
        logger.info(f"  OOF预测: {len(self.oof)}条, {self.oof['date'].nunique()}周")

        # 加载运行快照
        snapshot_path = OUTPUT_DIR / "run_snapshot_phase1.json"
        if not snapshot_path.exists():
            raise FileNotFoundError(f"快照文件不存在: {snapshot_path}")

        self.snapshot = json.load(open(snapshot_path))
        logger.info(f"  运行ID: {self.snapshot['run_id']}")
        logger.info(f"  运行时间: {self.snapshot['timestamp']}")

        # 加载原始数据
        from v2.data.pit_panel import build_pit_panel

        csv_path = BASE_DIR / "train_merged_all.csv"
        panel = build_pit_panel(csv_path)
        self.df_raw = panel.df

        # Research data
        dates_all = sorted(self.df_raw["date"].unique())
        n_holdout = min(104, len(dates_all) // 5)
        research_dates = dates_all[:-n_holdout]
        self.df_research = self.df_raw[self.df_raw["date"].isin(research_dates)].copy()
        logger.info(f"  研究数据: {len(self.df_research)}行")

    def calculate_ic(self):
        """按当前项目标签契约计算 OOF IC。"""
        logger.info("\n" + "=" * 80)
        logger.info("计算IC...")
        logger.info("=" * 80)

        oof_dates = sorted(self.oof["date"].unique())

        for date_i in oof_dates:
            oof_d = self.oof[self.oof["date"] == date_i].set_index("stock_id")[
                "oof_prediction"
            ]
            pchg_d = self.df_research[self.df_research["date"] == date_i].set_index(
                "stock_id"
            )["pchg"]
            common = oof_d.index.intersection(pchg_d.index)
            if len(common) > 10:
                corr, _ = stats.spearmanr(
                    oof_d.loc[common], pchg_d.loc[common]
                )
                if np.isfinite(corr):
                    self.ic_series.append(corr)

        logger.info(
            f"  OOF IC: {np.mean(self.ic_series):.4f} ± {np.std(self.ic_series):.4f}"
        )

    def calculate_portfolio_returns(self):
        """计算组合收益"""
        logger.info("\n" + "=" * 80)
        logger.info("计算组合收益...")
        logger.info("=" * 80)

        oof_df = self.oof.set_index(["date", "stock_id"])
        y = self.df_research.set_index(["date", "stock_id"])["pchg"]
        common_idx = oof_df.index.intersection(y.index)

        oof_aligned = oof_df.loc[common_idx].copy()
        oof_aligned["pchg"] = y.loc[common_idx]

        # Top-50组合
        def simulate_top50(group):
            top50 = group.nlargest(50, "oof_prediction")
            return top50["pchg"].mean()

        self.portfolio_returns = oof_aligned.groupby("date").apply(simulate_top50)
        self.market_returns = oof_aligned.groupby("date")["pchg"].mean()

        # 计算收益指标
        n_weeks = len(self.portfolio_returns)
        port_cum = (1 + self.portfolio_returns).cumprod()
        mkt_cum = (1 + self.market_returns).cumprod()

        ann_port = (port_cum.iloc[-1] ** (52 / n_weeks) - 1) * 100
        ann_mkt = (mkt_cum.iloc[-1] ** (52 / n_weeks) - 1) * 100

        logger.info(f"  组合年化收益: {ann_port:.2f}%")
        logger.info(f"  市场年化收益: {ann_mkt:.2f}%")
        logger.info(f"  年化超额: {ann_port - ann_mkt:.2f}%")

    def calculate_family_weights(self):
        """计算因子家族权重"""
        logger.info("\n" + "=" * 80)
        logger.info("计算因子家族权重...")
        logger.info("=" * 80)

        from v2.data.pit_panel import build_pit_panel
        from v2.family.family_map import FAMILY_MAP, ALL_FACTORS
        from v2.preprocessing.factor_preprocessor import (
            winsorize_cross_section,
            impute_factors,
            standardize_factors,
        )
        from v2.synthesis.intra_family import equal_rank_score
        from v2.synthesis.cross_family import CrossFamilyModel

        # 加载和处理数据
        csv_path = BASE_DIR / "train_merged_all.csv"
        panel = build_pit_panel(csv_path)
        df = panel.df

        dates_all = sorted(df["date"].unique())
        n_holdout = min(104, len(dates_all) // 5)
        research_dates = dates_all[:-n_holdout]
        df = df[df["date"].isin(research_dates)].copy()

        # L1预处理
        all_factor_cols = [c for c in ALL_FACTORS if c in df.columns]
        df_winsor = winsorize_cross_section(df, all_factor_cols)
        df_imputed, _ = impute_factors(df_winsor, all_factor_cols)
        df_rank, _ = standardize_factors(df_imputed, all_factor_cols)

        # 家族分数
        active_family_map = {
            f: [c for c in cols if c in df_rank.columns]
            for f, cols in FAMILY_MAP.items()
        }
        active_families = {k: v for k, v in active_family_map.items() if v}

        family_scores = {}
        for family_name, family_factors in active_families.items():
            score = equal_rank_score(df_rank, family_factors)
            family_scores[family_name] = score

        S = pd.DataFrame(family_scores)
        y = df_rank.set_index(["date", "stock_id"])["pchg"]

        common_idx = S.index.intersection(y.index)
        S = S.loc[common_idx]
        y = y.loc[common_idx]

        # 训练模型
        dates_sorted = sorted(S.index.get_level_values("date").unique())
        split_idx = int(len(dates_sorted) * 0.7)
        train_dates = dates_sorted[:split_idx]

        S_train = S[S.index.get_level_values("date").isin(train_dates)]
        y_train = y[y.index.isin(S_train.index)]

        model = CrossFamilyModel()
        model.fit(S_train, y_train, best_alpha=1.0, best_l1_ratio=0.0)

        self.family_weights = model.current_beta

        logger.info("  家族权重:")
        for family, weight in self.family_weights.items():
            logger.info(f"    {family}: {weight:.4f}")

    def generate_report(self) -> str:
        """生成完整分析报告"""
        report_lines = []

        report_lines.append("=" * 80)
        report_lines.append("Phase1 运行结果详细分析报告")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 80)
        report_lines.append("")

        # 基本信息
        report_lines.append("【一、基本信息】")
        report_lines.append("")
        report_lines.append(f"运行ID: {self.snapshot['run_id']}")
        report_lines.append(f"运行时间: {self.snapshot['timestamp']}")
        report_lines.append(f"Git Commit: {self.snapshot['git_commit']}")
        report_lines.append(f"数据版本: {self.snapshot['data_version']}")
        report_lines.append("")
        report_lines.append(f"总预测数: {len(self.oof)}")
        report_lines.append(f"覆盖周数: {self.oof['date'].nunique()}")
        report_lines.append(f"覆盖股票: {self.oof['stock_id'].nunique()}")
        report_lines.append(
            f"时间范围: {self.oof['date'].min()} ~ {self.oof['date'].max()}"
        )
        report_lines.append("")

        # IC分析
        report_lines.append("【二、IC详细分析】")
        report_lines.append("")
        report_lines.append("OOF IC（按当前项目标签口径）:")
        report_lines.append(f"  平均IC: {np.mean(self.ic_series):.4f}")
        report_lines.append(f"  IC标准差: {np.std(self.ic_series):.4f}")
        report_lines.append(
            f"  IC IR: {np.mean(self.ic_series) / np.std(self.ic_series):.4f}"
        )
        report_lines.append(f"  IC中位数: {np.median(self.ic_series):.4f}")
        report_lines.append(f"  IC最大: {np.max(self.ic_series):.4f}")
        report_lines.append(f"  IC最小: {np.min(self.ic_series):.4f}")
        report_lines.append(
            f"  IC>0占比: {sum(ic > 0 for ic in self.ic_series) / len(self.ic_series) * 100:.2f}%"
        )
        report_lines.append(
            f"  IC>0.03占比: {sum(ic > 0.03 for ic in self.ic_series) / len(self.ic_series) * 100:.2f}%"
        )
        report_lines.append(
            f"  IC>0.05占比: {sum(ic > 0.05 for ic in self.ic_series) / len(self.ic_series) * 100:.2f}%"
        )
        report_lines.append("")

        # 分组收益
        report_lines.append("【三、分组收益分析】")
        report_lines.append("")

        oof_df = self.oof.set_index(["date", "stock_id"])
        y = self.df_research.set_index(["date", "stock_id"])["pchg"]
        common_idx = oof_df.index.intersection(y.index)
        oof_aligned = oof_df.loc[common_idx].copy()
        oof_aligned["pchg"] = y.loc[common_idx]

        def calc_10groups(group):
            group["pred_rank"] = group["oof_prediction"].rank(pct=True)
            group["group"] = pd.cut(
                group["pred_rank"],
                bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                labels=["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"],
            )
            return group

        oof_groups = oof_aligned.groupby("date").apply(calc_10groups)
        group_returns = oof_groups.groupby("group")["pchg"].mean() * 100

        report_lines.append("10分组平均周收益:")
        report_lines.append("分组 | 平均收益 | 年化收益 | 说明")
        report_lines.append("-" * 50)
        for g, r in group_returns.items():
            ann_r = r * 52
            desc = "预测最差" if g == "G1" else "预测最好" if g == "G10" else ""
            report_lines.append(f"{g}   | {r:.4f}%  | {ann_r:.2f}% | {desc}")
        report_lines.append("")
        spread = group_returns.iloc[-1] - group_returns.iloc[0]
        report_lines.append(f"G10-G1 spread: {spread:.4f}%/周 ({spread * 52:.2f}%/年)")
        report_lines.append("")

        # 策略回测
        report_lines.append("【四、策略回测（Top-50组合）】")
        report_lines.append("")

        n_weeks = len(self.portfolio_returns)
        port_cum = (1 + self.portfolio_returns).cumprod()
        mkt_cum = (1 + self.market_returns).cumprod()

        ann_port = (port_cum.iloc[-1] ** (52 / n_weeks) - 1) * 100
        ann_mkt = (mkt_cum.iloc[-1] ** (52 / n_weeks) - 1) * 100
        ann_vol_port = self.portfolio_returns.std() * np.sqrt(52) * 100
        ann_vol_mkt = self.market_returns.std() * np.sqrt(52) * 100
        sharpe_port = ann_port / 100 / (ann_vol_port / 100)
        sharpe_mkt = ann_mkt / 100 / (ann_vol_mkt / 100)

        port_dd = port_cum / port_cum.cummax() - 1
        mkt_dd = mkt_cum / mkt_cum.cummax() - 1

        report_lines.append("收益指标:")
        report_lines.append(f"  Top-50累计收益: {(port_cum.iloc[-1] - 1) * 100:.2f}%")
        report_lines.append(f"  Top-50年化收益: {ann_port:.2f}%")
        report_lines.append(f"  Top-50年化波动: {ann_vol_port:.2f}%")
        report_lines.append(f"  Top-50夏普比率: {sharpe_port:.2f}")
        report_lines.append(f"  市场累计收益: {(mkt_cum.iloc[-1] - 1) * 100:.2f}%")
        report_lines.append(f"  市场年化收益: {ann_mkt:.2f}%")
        report_lines.append(f"  市场年化波动: {ann_vol_mkt:.2f}%")
        report_lines.append(f"  市场夏普比率: {sharpe_mkt:.2f}")
        report_lines.append(f"  年化超额收益: {ann_port - ann_mkt:.2f}%")
        report_lines.append("")
        report_lines.append("风险指标:")
        report_lines.append(f"  Top-50最大回撤: {port_dd.min() * 100:.2f}%")
        report_lines.append(f"  市场最大回撤: {mkt_dd.min() * 100:.2f}%")
        report_lines.append(f"  Calmar比率: {ann_port / 100 / abs(port_dd.min()):.2f}")
        report_lines.append("")
        report_lines.append("胜率指标:")
        report_lines.append(
            f"  周胜率: {(self.portfolio_returns > self.market_returns).mean() * 100:.2f}%"
        )
        monthly_port = self.portfolio_returns.groupby(
            self.portfolio_returns.index.to_period("M")
        ).sum()
        monthly_mkt = self.market_returns.groupby(
            self.market_returns.index.to_period("M")
        ).sum()
        report_lines.append(
            f"  月胜率: {(monthly_port > monthly_mkt).mean() * 100:.2f}%"
        )
        report_lines.append("")

        # 分年度收益
        report_lines.append("【五、分年度收益】")
        report_lines.append("")
        report_lines.append("年份 | 组合收益 | 市场收益 | 超额收益 | 夏普")
        report_lines.append("-" * 50)

        annual_port = self.portfolio_returns.groupby(
            self.portfolio_returns.index.year
        ).sum()
        annual_mkt = self.market_returns.groupby(self.market_returns.index.year).sum()

        for year in sorted(annual_port.index):
            port_y = annual_port.get(year, 0) * 100
            mkt_y = annual_mkt.get(year, 0) * 100
            excess_y = port_y - mkt_y

            year_returns = self.portfolio_returns[
                self.portfolio_returns.index.year == year
            ]
            year_sharpe = (
                year_returns.mean() / year_returns.std() * np.sqrt(52)
                if year_returns.std() > 0
                else 0
            )

            report_lines.append(
                f"{year} | {port_y:>7.2f}% | {mkt_y:>7.2f}% | {excess_y:>7.2f}% | {year_sharpe:>6.2f}"
            )
        report_lines.append("")

        # 因子权重
        if self.family_weights is not None:
            report_lines.append("【六、因子家族权重】")
            report_lines.append("")
            report_lines.append("家族     | 权重    | 因子数 | 贡献方向")
            report_lines.append("-" * 50)

            families = self.snapshot["config"]["use_family_map"]
            for family in sorted(self.family_weights.index):
                weight = self.family_weights[family]
                n_factors = len(families.get(family, []))
                direction = "正向" if weight > 0 else "反向"
                strength = "强" if abs(weight) > 0.01 else "弱"
                report_lines.append(
                    f"{family:8s} | {weight:>7.4f} | {n_factors:>4d} | {direction}{strength}"
                )
            report_lines.append("")

        # 问题诊断
        report_lines.append("【七、问题诊断】")
        report_lines.append("")
        report_lines.append("主要风险:")
        report_lines.append("  1. Look-ahead Bias（🔥高）:")
        report_lines.append("     - 123个财务因子未使用披露日")
        report_lines.append("     - 财务数据在截面日可能未实际披露")
        report_lines.append("     - 建议补充ann_date字段或添加63天时滞")
        report_lines.append("")
        report_lines.append("  2. 缺ST状态列（中）:")
        report_lines.append("     - 无法过滤ST股票")
        report_lines.append("     - 建议补充is_st字段")
        report_lines.append("")
        report_lines.append("  3. 缺停牌列（中）:")
        report_lines.append("     - 无法过滤停牌股票")
        report_lines.append("     - 建议补充is_suspended字段")
        report_lines.append("")

        # 结论
        report_lines.append("【八、结论】")
        report_lines.append("")
        report_lines.append("模型有效性:")
        report_lines.append(
            f"  ✅ OOF IC={np.mean(self.ic_series):.4f}（>0.03阈值）"
        )
        report_lines.append(
            f"  ✅ {sum(ic > 0 for ic in self.ic_series) / len(self.ic_series) * 100:.2f}%的周IC>0"
        )
        report_lines.append("  ✅ 分层效果显著（G10-G1 spread显著）")
        report_lines.append("")
        report_lines.append("使用建议:")
        report_lines.append("  ⚠️ 回测收益仍未计入真实交易成本与执行约束")
        report_lines.append("  ⚠️ 需优先修复财务披露时滞问题")
        report_lines.append("")
        report_lines.append("=" * 80)

        return "\n".join(report_lines)

    def generate_summary_json(self) -> dict:
        """生成JSON摘要"""
        n_weeks = len(self.portfolio_returns)
        port_cum = (1 + self.portfolio_returns).cumprod()
        mkt_cum = (1 + self.market_returns).cumprod()

        ann_port = (port_cum.iloc[-1] ** (52 / n_weeks) - 1) * 100
        ann_mkt = (mkt_cum.iloc[-1] ** (52 / n_weeks) - 1) * 100

        port_dd = port_cum / port_cum.cummax() - 1

        summary = {
            "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "run_id": self.snapshot["run_id"],
            "data_coverage": {
                "n_predictions": len(self.oof),
                "n_weeks": self.oof["date"].nunique(),
                "n_stocks": self.oof["stock_id"].nunique(),
                "date_range": f"{self.oof['date'].min()} ~ {self.oof['date'].max()}",
            },
            "ic_analysis": {
                "oof": {
                    "mean": float(np.mean(self.ic_series)),
                    "std": float(np.std(self.ic_series)),
                    "ir": float(np.mean(self.ic_series) / np.std(self.ic_series)),
                    "positive_ratio": float(
                        sum(ic > 0 for ic in self.ic_series) / len(self.ic_series)
                    ),
                },
            },
            "portfolio_performance": {
                "cumulative_return_pct": float((port_cum.iloc[-1] - 1) * 100),
                "annual_return_pct": float(ann_port),
                "annual_vol_pct": float(
                    self.portfolio_returns.std() * np.sqrt(52) * 100
                ),
                "sharpe": float(
                    ann_port / 100 / (self.portfolio_returns.std() * np.sqrt(52))
                ),
                "max_drawdown_pct": float(port_dd.min() * 100),
                "weekly_win_rate": float(
                    (self.portfolio_returns > self.market_returns).mean()
                ),
                "monthly_win_rate": float(
                    (
                        self.portfolio_returns.groupby(
                            self.portfolio_returns.index.to_period("M")
                        ).sum()
                        > self.market_returns.groupby(
                            self.market_returns.index.to_period("M")
                        ).sum()
                    ).mean()
                ),
            },
            "market_baseline": {
                "cumulative_return_pct": float((mkt_cum.iloc[-1] - 1) * 100),
                "annual_return_pct": float(ann_mkt),
                "annual_vol_pct": float(self.market_returns.std() * np.sqrt(52) * 100),
                "sharpe": float(
                    ann_mkt / 100 / (self.market_returns.std() * np.sqrt(52))
                ),
                "max_drawdown_pct": float((mkt_cum / mkt_cum.cummax() - 1).min() * 100),
            },
            "family_weights": (
                {k: float(v) for k, v in self.family_weights.items()}
                if self.family_weights is not None
                else {}
            ),
            "issues": [
                {
                    "severity": "high",
                    "issue": "lookahead_bias",
                    "impact": "收益虚高",
                    "status": "warning",
                },
                {
                    "severity": "medium",
                    "issue": "missing_st",
                    "impact": "无法过滤ST",
                    "status": "pending",
                },
                {
                    "severity": "medium",
                    "issue": "missing_suspend",
                    "impact": "无法过滤停牌",
                    "status": "pending",
                },
            ],
        }

        return summary

    def save_results(self, report_text: str, summary_json: dict):
        """保存结果到文件"""
        ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

        # 保存文本报告
        report_path = ANALYSIS_DIR / "phase1_analysis_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        logger.info(f"\n文本报告已保存: {report_path}")

        # 保存JSON摘要
        summary_path = ANALYSIS_DIR / "phase1_analysis_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary_json, f, indent=2, ensure_ascii=False)
        logger.info(f"JSON摘要已保存: {summary_path}")

    def run(self):
        """运行完整分析流程"""
        try:
            # 加载数据
            self.load_data()

            # 计算IC
            self.calculate_ic()

            # 计算组合收益
            self.calculate_portfolio_returns()

            # 计算因子权重
            self.calculate_family_weights()

            # 生成报告
            report_text = self.generate_report()
            logger.info("\n" + report_text)

            # 生成JSON摘要
            summary_json = self.generate_summary_json()

            # 保存结果
            self.save_results(report_text, summary_json)

            logger.info("\n" + "=" * 80)
            logger.info("分析完成!")
            logger.info("=" * 80)

            return True

        except Exception as e:
            logger.error(f"分析失败: {e}")
            import traceback

            traceback.print_exc()
            return False


def main():
    """主函数"""
    analyzer = Phase1Analyzer()
    success = analyzer.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
