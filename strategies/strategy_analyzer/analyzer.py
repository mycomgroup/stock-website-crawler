"""
核心分析框架 - StrategyRegimeAnalyzer
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Callable, Optional
from .config import AnalyzerConfig
from .backtest_engine import BacktestEngine
from .analysis_modules import AnalysisModules
from .report_generator import ReportGenerator


class StrategyRegimeAnalyzer:
    """通用策略分行情验证框架"""

    def __init__(self, config: Optional[AnalyzerConfig] = None, **kwargs):
        """
        Args:
            config: AnalyzerConfig 配置对象
            **kwargs: 直接传入配置参数 (会覆盖 config 中的值)
        """
        if config is None:
            config = AnalyzerConfig()

        # 覆盖配置
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)

        self.config = config
        self.engine = BacktestEngine(config)
        self.analyzer = AnalysisModules(config)

        # 存储策略
        self.strategies: Dict[str, Dict] = {}
        self.strategy_names: List[str] = []

        # 存储结果
        self.strategy_results: Dict[str, pd.DataFrame] = {}
        self.benchmark_results: Dict[str, pd.DataFrame] = {}
        self.merged_data: Optional[pd.DataFrame] = None

        # 分析结果
        self.yearly_results: Optional[pd.DataFrame] = None
        self.risk_results: Optional[Dict] = None
        self.regime_results: Optional[Dict] = None
        self.timing_results: Optional[Dict] = None
        self.lag_results: Optional[Dict] = None
        self.recent_results: Optional[Dict] = None
        self.condition_results: Optional[Dict] = None

        self.total_periods: int = 0

    def register(self, name: str, select_fn: Callable, hold_n: int = 10):
        """注册策略

        Args:
            name: 策略名称
            select_fn: 选股函数 (date: str, n: int) -> List[str]
            hold_n: 持仓数量
        """
        self.strategies[name] = {
            "select_fn": select_fn,
            "hold_n": hold_n,
        }
        if name not in self.strategy_names:
            self.strategy_names.append(name)

    def run(self):
        """执行所有策略回测"""
        print("=" * 60)
        print("执行策略回测...")
        print("=" * 60)

        # 执行策略回测
        self.strategy_results = self.engine.run_all(self.strategies)

        # 获取基准数据
        print("\n获取基准数据...")
        self.benchmark_results = self.engine.run_benchmarks(self.config.benchmarks)

        # 合并数据
        self._merge_data()

        print(f"\n回测完成! 共{self.total_periods}个周期")

    def _merge_data(self):
        """合并策略和基准数据"""
        # 以第一个策略的结果为基准
        first_strategy = list(self.strategy_results.keys())[0]
        merged = self.strategy_results[first_strategy][["date"]].copy()

        # 添加策略收益
        for name, df in self.strategy_results.items():
            merged = merged.merge(
                df[["date", "ret"]].rename(columns={"ret": name}), on="date", how="left"
            )

        # 添加基准收益
        for code, df in self.benchmark_results.items():
            bench_name = self.config.get_benchmark_name(code)
            merged = merged.merge(
                df[["date", "ret"]].rename(columns={"ret": bench_name}),
                on="date",
                how="left",
            )

        self.merged_data = merged
        self.total_periods = len(merged)

    def analyze(self):
        """执行全部分析"""
        if self.merged_data is None:
            raise ValueError("请先执行 run()")

        print("\n" + "=" * 60)
        print("执行分析...")
        print("=" * 60)

        # 基准列名
        benchmark_cols = [
            self.config.get_benchmark_name(b) for b in self.config.benchmarks
        ]
        benchmark_col = benchmark_cols[0] if benchmark_cols else None

        # 年度分析
        print("\n1. 年度收益分析...")
        self.yearly_results = self.analyzer.yearly_analysis(
            self.merged_data, self.strategy_names, benchmark_cols
        )

        # 风险分析
        print("2. 风险指标分析...")
        self.risk_results = self.analyzer.risk_analysis(
            self.merged_data, self.strategy_names, benchmark_cols
        )

        # 市场状态分析
        if benchmark_col:
            print("3. 市场状态分析...")
            self.regime_results = self.analyzer.regime_analysis(
                self.merged_data, self.strategy_names, benchmark_col
            )

            # 择时分析
            print("4. 择时效果分析...")
            self.timing_results = self.analyzer.timing_analysis(
                self.merged_data, self.strategy_names, benchmark_col
            )

            # 前期影响分析
            print("5. 前期涨跌影响分析...")
            self.lag_results = self.analyzer.lag_analysis(
                self.merged_data, self.strategy_names, benchmark_col
            )

            # 条件总结
            print("6. 适合条件总结...")
            self.condition_results = {}
            for strat in self.strategy_names:
                self.condition_results[strat] = self.analyzer.condition_summary(
                    self.merged_data, strat, benchmark_col
                )

        # 近期分析
        print("7. 近期表现分析...")
        self.recent_results = self.analyzer.recent_analysis(
            self.merged_data, self.strategy_names, benchmark_cols
        )

        print("\n分析完成!")

    def report(self, output_path: Optional[str] = None) -> str:
        """生成报告

        Args:
            output_path: 输出文件路径 (可选)

        Returns:
            Markdown 内容
        """
        generator = ReportGenerator(self.config, self)
        return generator.generate(output_path)

    def print_summary(self):
        """打印摘要"""
        print("\n" + "=" * 60)
        print("策略验证摘要")
        print("=" * 60)

        # 年度收益
        if self.yearly_results is not None:
            print("\n【年度收益】")
            print(self.yearly_results.to_string())

        # 风险指标
        if self.risk_results:
            print("\n【风险指标】")
            for name in self.strategy_names:
                if name in self.risk_results:
                    risk = self.risk_results[name]
                    print(f"\n{name}:")
                    print(f"  年化收益: {risk.get('annualized_return', 0):.1%}")
                    print(f"  夏普比率: {risk.get('sharpe_ratio', 0):.2f}")
                    print(f"  最大回撤: {risk.get('max_drawdown', 0):.1%}")
                    print(f"  胜率: {risk.get('win_rate', 0):.0%}")

        # 近期表现
        if self.recent_results:
            print(f"\n【近期表现 ({self.recent_results.get('since', '')}至今)】")
            for name in self.strategy_names:
                if name in self.recent_results:
                    info = self.recent_results[name]
                    print(
                        f"  {name}: 累计{info.get('cum_ret', 0):.1%}, "
                        f"平均{info.get('mean_ret', 0):.2%}"
                    )

    def get_data(self) -> pd.DataFrame:
        """获取合并后的数据"""
        return self.merged_data

    def get_yearly(self) -> pd.DataFrame:
        """获取年度分析结果"""
        return self.yearly_results

    def get_risk(self) -> Dict:
        """获取风险分析结果"""
        return self.risk_results

    def get_regime(self) -> Dict:
        """获取市场状态分析结果"""
        return self.regime_results
