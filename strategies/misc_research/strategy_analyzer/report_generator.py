"""
报告生成器模块 - Markdown 格式
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


class ReportGenerator:
    """Markdown 报告生成器"""

    def __init__(self, config, analyzer):
        """
        Args:
            config: AnalyzerConfig 配置对象
            analyzer: StrategyRegimeAnalyzer 实例
        """
        self.config = config
        self.analyzer = analyzer

    def generate(self, output_path: Optional[str] = None) -> str:
        """生成完整报告

        Args:
            output_path: 输出文件路径 (可选)

        Returns:
            Markdown 内容
        """
        sections = [
            self._header(),
            self._yearly_section(),
            self._risk_section(),
            self._regime_section(),
            self._timing_section(),
            self._lag_section(),
            self._recent_section(),
            self._condition_section(),
            self._conclusion_section(),
            self._footer(),
        ]

        content = "\n".join(sections)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"报告已生成: {output_path}")

        return content

    def _header(self) -> str:
        """报告头部"""
        return f"""# 策略分行情验证报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**验证区间**: {self.config.start} ~ {self.config.end}  
**调仓频率**: {"月度" if self.config.freq == "monthly" else "季度"}  
**交易成本**: {self.config.cost:.2%}/次  
**基准指数**: {", ".join(self.config.get_benchmark_name(b) for b in self.config.benchmarks)}

---
"""

    def _yearly_section(self) -> str:
        """年度收益统计"""
        if not self.analyzer.yearly_results:
            return ""

        lines = ["## 一、按年度收益统计", ""]

        # 构建表头
        yearly = self.analyzer.yearly_results
        cols = yearly.columns.tolist()
        header = "| 年份 | " + " | ".join(cols) + " |"
        separator = "|------|" + "|".join(["------"] * len(cols)) + "|"

        lines.append(header)
        lines.append(separator)

        for year, row in yearly.iterrows():
            values = [f"{row[col]:.1%}" for col in cols]
            lines.append(f"| {year} | " + " | ".join(values) + " |")

        lines.append("")
        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def _risk_section(self) -> str:
        """风险指标统计"""
        if not self.analyzer.risk_results:
            return ""

        lines = ["## 二、风险指标", ""]

        # 策略风险指标
        lines.append("### 2.1 策略风险指标")
        lines.append("")

        risk_data = self.analyzer.risk_results
        strategy_names = [k for k in risk_data.keys() if "_vs_" not in k]

        if strategy_names:
            # 构建表格
            metrics = [
                ("累计收益", "cumulative_return", ".1%"),
                ("年化收益", "annualized_return", ".1%"),
                ("年化波动", "annualized_volatility", ".1%"),
                ("夏普比率", "sharpe_ratio", ".2f"),
                ("Sortino比率", "sortino_ratio", ".2f"),
                ("最大回撤", "max_drawdown", ".1%"),
                ("Calmar比率", "calmar_ratio", ".2f"),
                ("胜率", "win_rate", ".0%"),
                ("盈亏比", "profit_loss_ratio", ".2f"),
            ]

            header = "| 指标 | " + " | ".join(strategy_names) + " |"
            separator = "|------|" + "|".join(["------"] * len(strategy_names)) + "|"

            lines.append(header)
            lines.append(separator)

            for label, key, fmt in metrics:
                values = []
                for name in strategy_names:
                    val = risk_data[name].get(key, 0)
                    values.append(f"{val:{fmt}}")
                lines.append(f"| {label} | " + " | ".join(values) + " |")

        lines.append("")

        # 相对基准指标
        vs_keys = [k for k in risk_data.keys() if "_vs_" in k]
        if vs_keys:
            lines.append("### 2.2 相对基准指标")
            lines.append("")

            rel_metrics = [
                ("超额收益", "excess_return", ".1%"),
                ("年化超额", "annualized_excess", ".1%"),
                ("跟踪误差", "tracking_error", ".1%"),
                ("信息比率", "information_ratio", ".2f"),
                ("Beta", "beta", ".2f"),
                ("Alpha", "alpha", ".1%"),
            ]

            header = "| 指标 | " + " | ".join(vs_keys) + " |"
            separator = "|------|" + "|".join(["------"] * len(vs_keys)) + "|"

            lines.append(header)
            lines.append(separator)

            for label, key, fmt in rel_metrics:
                values = []
                for name in vs_keys:
                    val = risk_data[name].get(key, 0)
                    values.append(f"{val:{fmt}}")
                lines.append(f"| {label} | " + " | ".join(values) + " |")

        lines.append("")
        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def _regime_section(self) -> str:
        """市场状态分析"""
        if not self.analyzer.regime_results:
            return ""

        lines = ["## 三、按市场状态分类", ""]

        regime_data = self.analyzer.regime_results
        strategy_names = self.analyzer.strategy_names

        for regime_label, regime_info in regime_data.items():
            count = regime_info.get("count", 0)
            lines.append(f"### {regime_label} (共{count}个周期)")
            lines.append("")

            header = "| 策略 | 季均收益 | 累计收益 | 胜率 |"
            separator = "|------|----------|----------|------|"

            lines.append(header)
            lines.append(separator)

            for strat in strategy_names:
                if strat in regime_info:
                    info = regime_info[strat]
                    mean_ret = info.get("mean_ret", 0)
                    cum_ret = info.get("cum_ret", 0)
                    pos_rate = info.get("positive_rate", 0)
                    lines.append(
                        f"| {strat} | {mean_ret:.2%} | {cum_ret:.1%} | {pos_rate:.0%} |"
                    )

            lines.append("")

        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def _timing_section(self) -> str:
        """择时效果分析"""
        if not self.analyzer.timing_results:
            return ""

        lines = ["## 四、择时效果对比", ""]

        timing_data = self.analyzer.timing_results
        total_periods = self.analyzer.total_periods
        years = total_periods * (1 / 12 if self.config.freq == "monthly" else 1 / 4)

        for strat, timing_modes in timing_data.items():
            lines.append(f"### {strat}")
            lines.append("")

            header = "| 策略 | 累计收益 | 年化收益 | 操作时间 |"
            separator = "|------|----------|----------|----------|"

            lines.append(header)
            lines.append(separator)

            for mode, info in timing_modes.items():
                cum_ret = info.get("cum_ret", 0)
                ann_ret = info.get("ann_ret", 0)
                pct = info.get("pct", 0)
                lines.append(f"| {mode} | {cum_ret:.1%} | {ann_ret:.1%} | {pct:.0%} |")

            lines.append("")

        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def _lag_section(self) -> str:
        """前N期影响分析"""
        if not self.analyzer.lag_results:
            return ""

        lines = ["## 五、前期涨跌影响", ""]

        lag_data = self.analyzer.lag_results
        strategy_names = self.analyzer.strategy_names

        for lag_label, conditions in lag_data.items():
            lines.append(f"### {lag_label}")
            lines.append("")

            header = "| 条件 | " + " | ".join(strategy_names) + " | 期数 |"
            separator = (
                "|------|" + "|".join(["------"] * len(strategy_names)) + "|------|"
            )

            lines.append(header)
            lines.append(separator)

            for condition, data in conditions.items():
                values = [f"{data.get(s, 0):.2%}" for s in strategy_names]
                count = data.get("count", 0)
                lines.append(f"| {condition} | " + " | ".join(values) + f" | {count} |")

            lines.append("")

        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def _recent_section(self) -> str:
        """近期表现"""
        if not self.analyzer.recent_results:
            return ""

        lines = ["## 六、近期表现", ""]

        recent = self.analyzer.recent_results
        since = recent.get("since", "")
        periods = recent.get("periods", 0)

        lines.append(f"### {since} 至今 ({periods}个周期)")
        lines.append("")

        strategy_names = self.analyzer.strategy_names
        benchmark_names = [
            self.config.get_benchmark_name(b) for b in self.config.benchmarks
        ]

        header = "| 策略 | 累计收益 | 平均收益 | 胜率 |"
        separator = "|------|----------|----------|------|"

        lines.append(header)
        lines.append(separator)

        for strat in strategy_names:
            if strat in recent:
                info = recent[strat]
                cum_ret = info.get("cum_ret", 0)
                mean_ret = info.get("mean_ret", 0)
                win_rate = info.get("win_rate", 0)
                lines.append(
                    f"| {strat} | {cum_ret:.1%} | {mean_ret:.2%} | {win_rate:.0%} |"
                )

        for bench in self.config.benchmarks:
            if bench in recent:
                info = recent[bench]
                name = self.config.get_benchmark_name(bench)
                cum_ret = info.get("cum_ret", 0)
                mean_ret = info.get("mean_ret", 0)
                lines.append(f"| {name} | {cum_ret:.1%} | {mean_ret:.2%} | - |")

        lines.append("")

        # 逐期明细
        details = recent.get("details", [])
        if details:
            lines.append("### 逐期明细")
            lines.append("")

            all_cols = strategy_names + [
                self.config.get_benchmark_name(b) for b in self.config.benchmarks
            ]
            header = "| 周期 | " + " | ".join(all_cols) + " |"
            separator = "|------|" + "|".join(["------"] * len(all_cols)) + "|"

            lines.append(header)
            lines.append(separator)

            for detail in details:
                date_str = detail.get("date", "")
                values = []
                for col in all_cols:
                    val = detail.get(col, 0)
                    values.append(f"{val:.1%}")
                lines.append(f"| {date_str} | " + " | ".join(values) + " |")

        lines.append("")
        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def _condition_section(self) -> str:
        """适合条件总结"""
        if not self.analyzer.condition_results:
            return ""

        lines = ["## 七、适合条件总结", ""]

        condition_data = self.analyzer.condition_results

        for strat, conditions in condition_data.items():
            lines.append(f"### {strat}")
            lines.append("")

            pos = conditions.get("positive", {})
            neg = conditions.get("negative", {})

            lines.append(
                f"- **正收益期** ({pos.get('count', 0)}个, {pos.get('pct', 0):.0%}):"
            )
            lines.append(
                f"  - 基准当期均值: {pos.get('benchmark_current_mean', 0):.2%}"
            )
            lines.append(f"  - 基准前期均值: {pos.get('benchmark_lag1_mean', 0):.2%}")
            lines.append("")
            lines.append(
                f"- **负收益期** ({neg.get('count', 0)}个, {neg.get('pct', 0):.0%}):"
            )
            lines.append(
                f"  - 基准当期均值: {neg.get('benchmark_current_mean', 0):.2%}"
            )
            lines.append(f"  - 基准前期均值: {neg.get('benchmark_lag1_mean', 0):.2%}")
            lines.append("")

        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def _conclusion_section(self) -> str:
        """结论"""
        lines = ["## 八、结论", ""]

        # 自动总结最佳/最差策略
        if self.analyzer.risk_results:
            strategy_names = self.analyzer.strategy_names
            strategy_returns = {}

            for strat in strategy_names:
                if strat in self.analyzer.risk_results:
                    strategy_returns[strat] = self.analyzer.risk_results[strat].get(
                        "annualized_return", 0
                    )

            if strategy_returns:
                best = max(strategy_returns, key=strategy_returns.get)
                worst = min(strategy_returns, key=strategy_returns.get)

                lines.append(
                    f"- **最佳策略**: {best} (年化{strategy_returns[best]:.1%})"
                )
                lines.append(
                    f"- **最差策略**: {worst} (年化{strategy_returns[worst]:.1%})"
                )

        lines.append("")
        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def _footer(self) -> str:
        """报告尾部"""
        return f"""---

**报告生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**框架版本**: Strategy Regime Analyzer v1.0
"""
