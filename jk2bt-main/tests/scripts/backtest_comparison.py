"""
backtest_comparison.py
回测结果对比方案。

提供：
- 回测结果对比框架
- 对比指标计算
- 差异分析报告
- 可视化对比图表
"""

import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import warnings


class BacktestResult:
    """回测结果数据结构。"""

    def __init__(
        self,
        name: str,
        total_return: float,
        annual_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        win_rate: float,
        profit_factor: float,
        trade_count: int,
        start_date: str,
        end_date: str,
        daily_returns: Optional[pd.Series] = None,
        equity_curve: Optional[pd.Series] = None,
        trades: Optional[pd.DataFrame] = None,
        metadata: Optional[Dict] = None,
    ):
        self.name = name
        self.total_return = total_return
        self.annual_return = annual_return
        self.max_drawdown = max_drawdown
        self.sharpe_ratio = sharpe_ratio
        self.win_rate = win_rate
        self.profit_factor = profit_factor
        self.trade_count = trade_count
        self.start_date = start_date
        self.end_date = end_date
        self.daily_returns = daily_returns
        self.equity_curve = equity_curve
        self.trades = trades
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        """转换为字典。"""
        return {
            "name": self.name,
            "total_return": self.total_return,
            "annual_return": self.annual_return,
            "max_drawdown": self.max_drawdown,
            "sharpe_ratio": self.sharpe_ratio,
            "win_rate": self.win_rate,
            "profit_factor": self.profit_factor,
            "trade_count": self.trade_count,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "BacktestResult":
        """从字典创建。"""
        return cls(
            name=data["name"],
            total_return=data["total_return"],
            annual_return=data["annual_return"],
            max_drawdown=data["max_drawdown"],
            sharpe_ratio=data["sharpe_ratio"],
            win_rate=data["win_rate"],
            profit_factor=data["profit_factor"],
            trade_count=data["trade_count"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            metadata=data.get("metadata", {}),
        )

    def save(self, filepath: str) -> None:
        """保存到文件。"""
        data = self.to_dict()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: str) -> "BacktestResult":
        """从文件加载。"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


class BacktestComparator:
    """回测结果对比器。"""

    COMPARISON_METRICS = [
        ("total_return", "总收益率", "%"),
        ("annual_return", "年化收益率", "%"),
        ("max_drawdown", "最大回撤", "%"),
        ("sharpe_ratio", "夏普比率", ""),
        ("win_rate", "胜率", "%"),
        ("profit_factor", "盈亏比", ""),
        ("trade_count", "交易次数", ""),
    ]

    def __init__(self, results: List[BacktestResult]):
        self.results = results
        self.comparison_table = None
        self.diff_report = None

    def compare(self) -> pd.DataFrame:
        """生成对比表格。"""
        data = []
        for result in self.results:
            row = {"name": result.name}
            for metric, label, unit in self.COMPARISON_METRICS:
                value = getattr(result, metric)
                if unit == "%":
                    row[label] = f"{value:.2f}%"
                else:
                    row[label] = (
                        f"{value:.4f}" if metric == "sharpe_ratio" else f"{value:.2f}"
                    )
            data.append(row)

        self.comparison_table = pd.DataFrame(data)
        return self.comparison_table

    def compute_differences(self, baseline: str) -> pd.DataFrame:
        """计算与基准的差异。"""
        baseline_result = next((r for r in self.results if r.name == baseline), None)
        if baseline_result is None:
            raise ValueError(f"基准 '{baseline}' 不存在")

        data = []
        for result in self.results:
            if result.name == baseline:
                continue

            row = {"name": result.name, "baseline": baseline}
            for metric, label, unit in self.COMPARISON_METRICS:
                baseline_val = getattr(baseline_result, metric)
                result_val = getattr(result, metric)
                diff = result_val - baseline_val
                diff_pct = safe_divide(diff, baseline_val) * 100

                row[f"{label}_差异"] = f"{diff:.4f}"
                row[f"{label}_差异%"] = f"{diff_pct:.2f}%"

            data.append(row)

        self.diff_report = pd.DataFrame(data)
        return self.diff_report

    def generate_report(self, output_dir: str, baseline: Optional[str] = None) -> str:
        """生成对比报告。"""
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(output_dir, f"comparison_report_{timestamp}.txt")

        with open(report_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("回测结果对比报告\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            f.write("1. 基本对比表\n")
            f.write("-" * 80 + "\n")
            comparison = self.compare()
            f.write(comparison.to_string(index=False))
            f.write("\n\n")

            if baseline:
                f.write(f"2. 与基准 '{baseline}' 的差异分析\n")
                f.write("-" * 80 + "\n")
                try:
                    diff = self.compute_differences(baseline)
                    f.write(diff.to_string(index=False))
                    f.write("\n\n")
                except ValueError as e:
                    f.write(f"错误: {e}\n\n")

            f.write("3. 结果详情\n")
            f.write("-" * 80 + "\n")
            for result in self.results:
                f.write(f"\n【{result.name}】\n")
                f.write(f"  回测区间: {result.start_date} ~ {result.end_date}\n")
                for metric, label, unit in self.COMPARISON_METRICS:
                    value = getattr(result, metric)
                    if unit == "%":
                        f.write(f"  {label}: {value:.2f}%\n")
                    else:
                        f.write(f"  {label}: {value:.4f}\n")
                if result.metadata:
                    f.write("  元数据:\n")
                    for k, v in result.metadata.items():
                        f.write(f"    {k}: {v}\n")

        return report_file

    def plot_comparison(self, output_dir: str) -> List[str]:
        """绘制对比图表。"""
        try:
            import matplotlib.pyplot as plt

            plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei"]
            plt.rcParams["axes.unicode_minus"] = False
        except ImportError:
            warnings.warn("matplotlib 未安装，跳过绘图")
            return []

        os.makedirs(output_dir, exist_ok=True)
        plot_files = []

        metrics_for_plot = [
            ("total_return", "总收益率 (%)"),
            ("annual_return", "年化收益率 (%)"),
            ("max_drawdown", "最大回撤 (%)"),
            ("sharpe_ratio", "夏普比率"),
            ("win_rate", "胜率 (%)"),
        ]

        for metric, label in metrics_for_plot:
            fig, ax = plt.subplots(figsize=(10, 6))

            names = [r.name for r in self.results]
            values = [getattr(r, metric) for r in self.results]

            bars = ax.bar(
                names, values, color=["steelblue", "coral", "green", "purple", "orange"]
            )

            ax.set_xlabel("策略")
            ax.set_ylabel(label)
            ax.set_title(f"{label} 对比")
            ax.grid(axis="y", linestyle="--", alpha=0.7)

            for bar, val in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"{val:.2f}",
                    ha="center",
                    va="bottom",
                )

            plot_file = os.path.join(output_dir, f"{metric}_comparison.png")
            plt.savefig(plot_file, dpi=150, bbox_inches="tight")
            plt.close()
            plot_files.append(plot_file)

        if self.results[0].equity_curve is not None:
            fig, ax = plt.subplots(figsize=(12, 6))
            for result in self.results:
                if result.equity_curve is not None:
                    ax.plot(
                        result.equity_curve.index,
                        result.equity_curve.values,
                        label=result.name,
                        linewidth=1.5,
                    )

            ax.set_xlabel("日期")
            ax.set_ylabel("净值")
            ax.set_title("净值曲线对比")
            ax.legend()
            ax.grid(linestyle="--", alpha=0.7)

            plot_file = os.path.join(output_dir, "equity_curve_comparison.png")
            plt.savefig(plot_file, dpi=150, bbox_inches="tight")
            plt.close()
            plot_files.append(plot_file)

        return plot_files


def safe_divide(
    a: Union[float, np.ndarray], b: Union[float, np.ndarray]
) -> Union[float, np.ndarray]:
    """安全除法。"""
    with np.errstate(divide="ignore", invalid="ignore"):
        result = np.divide(a, b)
        if isinstance(result, np.ndarray):
            result = np.where((b == 0) | np.isnan(b), np.nan, result)
        else:
            if b == 0 or np.isnan(b):
                return np.nan
    return result


def extract_backtest_result_from_bt(
    cerebro,
    name: str,
    start_date: str,
    end_date: str,
    metadata: Optional[Dict] = None,
) -> BacktestResult:
    """从 Backtrader cerebro 提取回测结果。"""
    final_value = cerebro.broker.getvalue()
    initial_value = cerebro.broker.startingcash

    total_return = safe_divide(final_value - initial_value, initial_value) * 100

    trades = []
    daily_returns = pd.Series()

    if hasattr(cerebro, "runs"):
        for run in cerebro.runs:
            if hasattr(run, "_trades"):
                trades.extend(run._trades)

    trade_count = len(trades)

    win_trades = [t for t in trades if t.get("profit", 0) > 0]
    loss_trades = [t for t in trades if t.get("profit", 0) < 0]
    win_rate = safe_divide(len(win_trades), trade_count) * 100 if trade_count > 0 else 0

    total_profit = sum(t.get("profit", 0) for t in win_trades)
    total_loss = abs(sum(t.get("profit", 0) for t in loss_trades))
    profit_factor = safe_divide(total_profit, total_loss) if total_loss > 0 else np.nan

    days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
    annual_return = safe_divide(total_return, days) * 365 if days > 0 else 0

    if not daily_returns.empty:
        sharpe_ratio = (
            daily_returns.mean() / daily_returns.std() * np.sqrt(252)
            if daily_returns.std() > 0
            else 0
        )
        equity_curve = (1 + daily_returns).cumprod()

        rolling_max = equity_curve.cummax()
        drawdown = equity_curve / rolling_max - 1
        max_drawdown = drawdown.min() * 100
    else:
        sharpe_ratio = 0
        max_drawdown = 0
        equity_curve = None

    return BacktestResult(
        name=name,
        total_return=total_return,
        annual_return=annual_return,
        max_drawdown=max_drawdown,
        sharpe_ratio=sharpe_ratio,
        win_rate=win_rate,
        profit_factor=profit_factor,
        trade_count=trade_count,
        start_date=start_date,
        end_date=end_date,
        daily_returns=daily_returns,
        equity_curve=equity_curve,
        trades=pd.DataFrame(trades) if trades else None,
        metadata=metadata,
    )


def compare_jq_local_backtest(
    jq_result: BacktestResult,
    local_result: BacktestResult,
    tolerance: float = 0.05,
) -> Dict[str, Any]:
    """
    对比聚宽与本地回测结果。

    Parameters
    ----------
    jq_result : BacktestResult
        聚宽回测结果
    local_result : BacktestResult
        本地回测结果
    tolerance : float
        容差阈值（相对差异）

    Returns
    -------
    dict
        对比结果，包含各项指标的差异和是否符合预期
    """
    comparison = {
        "jq_name": jq_result.name,
        "local_name": local_result.name,
        "metrics": {},
        "overall_match": True,
        "warnings": [],
    }

    key_metrics = [
        "total_return",
        "annual_return",
        "max_drawdown",
        "win_rate",
        "trade_count",
    ]

    for metric in key_metrics:
        jq_val = getattr(jq_result, metric)
        local_val = getattr(local_result, metric)

        diff = abs(jq_val - local_val)
        rel_diff = safe_divide(diff, jq_val) if jq_val != 0 else diff

        is_match = rel_diff <= tolerance or diff <= 0.01
        comparison["metrics"][metric] = {
            "jq_value": jq_val,
            "local_value": local_val,
            "absolute_diff": diff,
            "relative_diff": rel_diff,
            "within_tolerance": is_match,
        }

        if not is_match:
            comparison["overall_match"] = False
            comparison["warnings"].append(
                f"{metric} 差异过大: 聚宽={jq_val:.4f}, 本地={local_val:.4f}, 差异={rel_diff:.2%}"
            )

    return comparison


class BacktestValidator:
    """回测验证器，验证本地回测与聚宽的一致性。"""

    def __init__(self, tolerance: float = 0.05):
        self.tolerance = tolerance
        self.validation_results = []

    def validate_signal_consistency(
        self,
        jq_signals: pd.DataFrame,
        local_signals: pd.DataFrame,
    ) -> Dict:
        """验证信号一致性。"""
        if jq_signals.empty or local_signals.empty:
            return {"match_rate": 0, "details": "数据缺失"}

        aligned_jq = jq_signals.reindex(local_signals.index)
        aligned_local = local_signals

        signal_match = (aligned_jq["signal"] == aligned_local["signal"]).sum()
        total_signals = len(aligned_local)
        match_rate = safe_divide(signal_match, total_signals)

        return {
            "match_rate": match_rate,
            "total_signals": total_signals,
            "matched_signals": signal_match,
            "mismatch_details": aligned_jq[
                aligned_jq["signal"] != aligned_local["signal"]
            ],
        }

    def validate_trade_consistency(
        self,
        jq_trades: pd.DataFrame,
        local_trades: pd.DataFrame,
    ) -> Dict:
        """验证交易一致性。"""
        if jq_trades.empty or local_trades.empty:
            return {"match_rate": 0, "details": "数据缺失"}

        jq_count = len(jq_trades)
        local_count = len(local_trades)

        count_diff = abs(jq_count - local_count)
        count_match = safe_divide(count_diff, jq_count) <= self.tolerance

        if "profit" in jq_trades.columns and "profit" in local_trades.columns:
            jq_total_profit = jq_trades["profit"].sum()
            local_total_profit = local_trades["profit"].sum()
            profit_diff = abs(jq_total_profit - local_total_profit)
            profit_match = safe_divide(profit_diff, jq_total_profit) <= self.tolerance
        else:
            profit_match = True
            profit_diff = np.nan

        return {
            "trade_count_match": count_match,
            "jq_trade_count": jq_count,
            "local_trade_count": local_count,
            "profit_match": profit_match,
            "profit_diff": profit_diff,
        }

    def validate_performance_consistency(
        self,
        jq_result: BacktestResult,
        local_result: BacktestResult,
    ) -> Dict:
        """验证绩效一致性。"""
        return compare_jq_local_backtest(jq_result, local_result, self.tolerance)

    def generate_validation_report(
        self,
        jq_result: BacktestResult,
        local_result: BacktestResult,
        jq_signals: Optional[pd.DataFrame] = None,
        local_signals: Optional[pd.DataFrame] = None,
        jq_trades: Optional[pd.DataFrame] = None,
        local_trades: Optional[pd.DataFrame] = None,
        output_file: Optional[str] = None,
    ) -> str:
        """生成验证报告。"""
        report_lines = []

        report_lines.append("=" * 80)
        report_lines.append("聚宽与本地回测一致性验证报告")
        report_lines.append("=" * 80)
        report_lines.append(f"\n验证容差: {self.tolerance:.2%}")
        report_lines.append(f"\n聚宽策略: {jq_result.name}")
        report_lines.append(f"本地策略: {local_result.name}")
        report_lines.append(f"回测区间: {jq_result.start_date} ~ {jq_result.end_date}")

        report_lines.append("\n" + "-" * 80)
        report_lines.append("\n【绩效一致性】")
        perf_result = self.validate_performance_consistency(jq_result, local_result)

        for metric, details in perf_result["metrics"].items():
            status = "✓" if details["within_tolerance"] else "✗"
            report_lines.append(
                f"  {status} {metric}: 聚宽={details['jq_value']:.4f}, "
                f"本地={details['local_value']:.4f}, 差异={details['relative_diff']:.2%}"
            )

        if perf_result["warnings"]:
            report_lines.append("\n  警告:")
            for w in perf_result["warnings"]:
                report_lines.append(f"    - {w}")

        overall_status = "通过" if perf_result["overall_match"] else "不通过"
        report_lines.append(f"\n  整体状态: {overall_status}")

        if jq_signals is not None and local_signals is not None:
            report_lines.append("\n" + "-" * 80)
            report_lines.append("\n【信号一致性】")
            signal_result = self.validate_signal_consistency(jq_signals, local_signals)
            report_lines.append(f"  匹配率: {signal_result['match_rate']:.2%}")
            report_lines.append(
                f"  匹配信号数: {signal_result['matched_signals']}/{signal_result['total_signals']}"
            )

        if jq_trades is not None and local_trades is not None:
            report_lines.append("\n" + "-" * 80)
            report_lines.append("\n【交易一致性】")
            trade_result = self.validate_trade_consistency(jq_trades, local_trades)
            report_lines.append(
                f"  交易次数匹配: {'✓' if trade_result['trade_count_match'] else '✗'} "
                f"(聚宽={trade_result['jq_trade_count']}, 本地={trade_result['local_trade_count']})"
            )
            report_lines.append(
                f"  利润匹配: {'✓' if trade_result['profit_match'] else '✗'} "
                f"(差异={trade_result['profit_diff']:.2f})"
            )

        report_lines.append("\n" + "=" * 80)

        report = "\n".join(report_lines)

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(report)

        return report


def demo_comparison():
    """对比示例。"""
    jq_result = BacktestResult(
        name="聚宽策略",
        total_return=45.6,
        annual_return=18.5,
        max_drawdown=-15.3,
        sharpe_ratio=1.25,
        win_rate=62.5,
        profit_factor=2.1,
        trade_count=156,
        start_date="2020-01-01",
        end_date="2023-12-31",
    )

    local_result = BacktestResult(
        name="本地策略",
        total_return=44.2,
        annual_return=17.8,
        max_drawdown=-16.1,
        sharpe_ratio=1.18,
        win_rate=61.8,
        profit_factor=2.05,
        trade_count=158,
        start_date="2020-01-01",
        end_date="2023-12-31",
    )

    comparator = BacktestComparator([jq_result, local_result])
    comparison_table = comparator.compare()
    print(comparison_table)

    diff_table = comparator.compute_differences("聚宽策略")
    print("\n差异分析:")
    print(diff_table)

    validator = BacktestValidator(tolerance=0.05)
    validation = validator.validate_performance_consistency(jq_result, local_result)
    print("\n验证结果:")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    demo_comparison()
