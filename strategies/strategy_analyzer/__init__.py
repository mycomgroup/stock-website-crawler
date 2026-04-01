"""
Strategy Regime Analyzer - 通用策略分行情验证框架

支持:
- 任意策略接入
- 多基准对比
- 风险指标计算
- 并行执行
- Markdown报告生成
"""

from .config import AnalyzerConfig
from .analyzer import StrategyRegimeAnalyzer
from .market_classifier import MarketStateClassifier
from .risk_metrics import RiskMetrics
from .backtest_engine import BacktestEngine
from .analysis_modules import AnalysisModules
from .report_generator import ReportGenerator

__version__ = "1.0.0"
__all__ = [
    "AnalyzerConfig",
    "StrategyRegimeAnalyzer",
    "MarketStateClassifier",
    "RiskMetrics",
    "BacktestEngine",
    "AnalysisModules",
    "ReportGenerator",
]
