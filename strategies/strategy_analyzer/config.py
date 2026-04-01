"""
配置定义模块
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class AnalyzerConfig:
    """分析器配置"""

    # 时间范围
    start: str = "2020-01-01"
    end: str = "2026-03-28"

    # 调仓频率: "monthly" / "quarterly"
    freq: str = "quarterly"

    # 交易成本 (单次)
    cost: float = 0.003

    # 基准指数列表
    benchmarks: List[str] = field(default_factory=lambda: ["399101.XSHE"])

    # 基准名称映射
    benchmark_names: Dict[str, str] = field(
        default_factory=lambda: {
            "399101.XSHE": "中证2000",
            "000300.XSHG": "沪深300",
            "000905.XSHG": "中证500",
            "399006.XSHE": "创业板指",
            "000016.XSHG": "上证50",
        }
    )

    # 近期分析起点
    recent_since: str = "2024-01-01"

    # 市场状态阈值 (季度)
    regime_thresholds: Dict[str, float] = field(
        default_factory=lambda: {
            "bull": 0.05,  # 牛市阈值
            "mild_down": -0.05,  # 温和下跌阈值
        }
    )

    # 月度阈值 (自动调整)
    monthly_thresholds: Dict[str, float] = field(
        default_factory=lambda: {
            "bull": 0.03,
            "mild_down": -0.03,
        }
    )

    # 风险指标配置
    risk_free_rate: float = 0.02  # 无风险利率 (年化)

    # 择时分析阈值
    timing_thresholds: List[float] = field(default_factory=lambda: [0.0, 0.05])

    # 并行执行
    parallel: bool = True
    max_workers: int = 4

    def get_thresholds(self) -> Dict[str, float]:
        """获取当前频率对应的阈值"""
        if self.freq == "monthly":
            return self.monthly_thresholds
        return self.regime_thresholds

    def get_benchmark_name(self, code: str) -> str:
        """获取基准名称"""
        return self.benchmark_names.get(code, code)
