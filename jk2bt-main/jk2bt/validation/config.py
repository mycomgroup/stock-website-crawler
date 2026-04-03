"""
validation/config.py
数据验证配置管理
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import yaml
import os


@dataclass
class ValidationConfig:
    """数据验证配置"""

    # 股票池配置
    stocks: List[str] = field(default_factory=lambda: [
        "600519.XSHG",  # 贵州茅台
        "000858.XSHE",  # 五粮液
        "000333.XSHE",  # 美的集团
        "600036.XSHG",  # 招商银行
        "601318.XSHG",  # 中国平安
    ])

    # 日期范围
    start_date: str = field(default_factory=lambda: (
        datetime.now() - timedelta(days=365)
    ).strftime("%Y-%m-%d"))
    end_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    # 数据类型
    data_types: List[str] = field(default_factory=lambda: [
        "valuation",      # 估值数据
        "trade_status",   # 交易状态
        # "factors",      # 因子数据（可选）
    ])

    # 容差配置
    tolerance: Dict[str, float] = field(default_factory=lambda: {
        "pe_ratio": 0.01,        # PE 容差 1%
        "pb_ratio": 0.01,        # PB 容差 1%
        "market_cap": 0.01,      # 市值容差 1%
        "circulating_market_cap": 0.01,
        "high_limit": 0.01,      # 涨停价容差 0.01元
        "low_limit": 0.01,       # 跌停价容差 0.01元
        "is_st": 0.0,            # ST状态精确匹配
        "paused": 0.0,           # 停牌状态精确匹配
        "factor": 0.05,          # 因子容差 5%
    })

    # 输出配置
    output_dir: str = "validation_results"
    output_json: bool = True
    output_markdown: bool = True
    output_log: bool = True

    # 并发配置
    batch_size: int = 50        # 每批处理股票数
    concurrency: int = 3        # 并发数

    # JoinQuant Notebook 配置
    jq_notebook_timeout: int = 300000  # 5分钟超时

    @classmethod
    def from_file(cls, config_path: str) -> "ValidationConfig":
        """从配置文件加载"""
        with open(config_path, "r", encoding="utf-8") as f:
            if config_path.endswith(".yaml") or config_path.endswith(".yml"):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        return cls(**data)

    def to_file(self, config_path: str):
        """保存配置到文件"""
        os.makedirs(os.path.dirname(config_path) if os.path.dirname(config_path) else ".", exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            if config_path.endswith(".yaml") or config_path.endswith(".yml"):
                yaml.dump(self.__dict__, f, allow_unicode=True, default_flow_style=False)
            else:
                json.dump(self.__dict__, f, ensure_ascii=False, indent=2)

    def get_dates(self) -> List[str]:
        """获取验证日期列表"""
        from jk2bt.core.strategy_base import get_all_trade_days
        try:
            trade_days = get_all_trade_days()
            start = datetime.strptime(self.start_date, "%Y-%m-%d")
            end = datetime.strptime(self.end_date, "%Y-%m-%d")
            dates = [d for d in trade_days if start <= datetime.strptime(d, "%Y-%m-%d") <= end]
            return dates
        except Exception:
            # 简单生成日期列表
            start = datetime.strptime(self.start_date, "%Y-%m-%d")
            end = datetime.strptime(self.end_date, "%Y-%m-%d")
            dates = []
            current = start
            while current <= end:
                if current.weekday() < 5:  # 工作日
                    dates.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)
            return dates

    def get_tolerance(self, field_name: str) -> float:
        """获取字段容差"""
        return self.tolerance.get(field_name, 0.01)


# 默认配置实例
default_config = ValidationConfig()