"""
Analysis V2 - 股票分析库

独立、解耦、可测试的股票技术分析库

使用示例:
    from analysis_v2.data.adapter import init_data_source
    init_data_source()
    
    from analysis_v2.factors import compute_factor
    ma5 = compute_factor("ma_5", "000001.SZ")
"""

from .core.types import OHLCV, IndicatorResult, Signal
from .core.interface import DataSource, DataSourceContext
from .core import indicators
from .core.utils import safe_divide

__version__ = "2.0.0"
__all__ = [
    "OHLCV",
    "IndicatorResult", 
    "Signal",
    "DataSource",
    "DataSourceContext",
    "indicators",
    "safe_divide",
]