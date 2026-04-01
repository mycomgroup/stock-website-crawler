"""
市场状态分类器模块
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


class MarketStateClassifier:
    """市场状态分类器"""

    # 默认状态标签
    STATE_LABELS = {
        "bull": "牛市",
        "mild_up": "温和上涨",
        "mild_down": "温和下跌",
        "bear": "熊市",
        "unknown": "未知",
    }

    def __init__(self, thresholds: Optional[Dict[str, float]] = None):
        """
        Args:
            thresholds: 阈值配置
                - bull: 牛市阈值 (默认 0.05)
                - mild_down: 温和下跌阈值 (默认 -0.05)
        """
        self.thresholds = thresholds or {
            "bull": 0.05,
            "mild_down": -0.05,
        }

    def classify_single(self, ret: float) -> str:
        """分类单期市场状态

        Args:
            ret: 收益率

        Returns:
            市场状态标识: bull / mild_up / mild_down / bear / unknown
        """
        if pd.isna(ret):
            return "unknown"

        bull_threshold = self.thresholds.get("bull", 0.05)
        mild_down_threshold = self.thresholds.get("mild_down", -0.05)

        if ret > bull_threshold:
            return "bull"
        elif ret > 0:
            return "mild_up"
        elif ret > mild_down_threshold:
            return "mild_down"
        else:
            return "bear"

    def classify_series(self, ret_series: pd.Series) -> pd.Series:
        """批量分类市场状态

        Args:
            ret_series: 收益率序列

        Returns:
            市场状态序列
        """
        return ret_series.apply(self.classify_single)

    def get_state_label(self, state: str) -> str:
        """获取状态中文标签"""
        thresholds = self.thresholds
        bull = thresholds.get("bull", 0.05)
        mild_down = thresholds.get("mild_down", -0.05)

        labels = {
            "bull": f"牛市(涨>{bull:.0%})",
            "mild_up": f"温和上涨(0~{bull:.0%})",
            "mild_down": f"温和下跌({mild_down:.0%}~0)",
            "bear": f"熊市(跌<{mild_down:.0%})",
            "unknown": "未知",
        }
        return labels.get(state, state)

    def get_all_states(self) -> list:
        """获取所有状态列表 (按风险从低到高)"""
        return ["bull", "mild_up", "mild_down", "bear"]

    def get_state_stats(self, df: pd.DataFrame, state_col: str) -> pd.DataFrame:
        """统计各状态出现次数

        Args:
            df: 数据框
            state_col: 状态列名

        Returns:
            统计结果
        """
        stats = df[state_col].value_counts().reset_index()
        stats.columns = ["state", "count"]
        stats["label"] = stats["state"].apply(self.get_state_label)
        stats["pct"] = stats["count"] / stats["count"].sum()
        return stats.sort_values("state")
