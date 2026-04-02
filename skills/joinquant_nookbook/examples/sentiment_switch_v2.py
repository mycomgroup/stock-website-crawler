#!/usr/bin/env python3
"""
情绪层v2：动态阈值 + 过热过滤 + 5档仓位
适用于首板低开、弱转强等机会仓策略
"""

from jqdata import *
import numpy as np
from collections import deque


class SentimentSwitchV2:
    """
    情绪开关v2

    功能：
    1. 动态阈值：根据趋势调整开仓阈值
    2. 过热过滤：涨停>100时回避
    3. 5档仓位：根据情绪强度调整仓位

    使用方法：
        switch = SentimentSwitchV2()
        should_trade, position_ratio = switch.check(zt_count)
    """

    def __init__(
        self, base_threshold=20, overheat_threshold=100, trend_adjustment=0.15
    ):
        """
        参数:
            base_threshold: 基准阈值（默认20）
            overheat_threshold: 过热阈值（默认100）
            trend_adjustment: 趋势调整比例（默认15%）
        """
        self.base_threshold = base_threshold
        self.overheat_threshold = overheat_threshold
        self.trend_adjustment = trend_adjustment

        # 历史涨停家数缓存
        self.zt_history = deque(maxlen=10)

        # 仓位档位配置
        self.position_levels = [
            (80, 1.0),  # 极高情绪，满仓
            (50, 0.8),  # 高情绪
            (30, 0.5),  # 中情绪
            (20, 0.25),  # 低情绪
            (0, 0.0),  # 极低情绪，空仓
        ]

    def update_history(self, zt_count):
        """更新历史涨停家数"""
        self.zt_history.append(zt_count)

    def get_trend(self):
        """
        判断情绪趋势

        返回: 'up', 'down', 'stable'
        """
        if len(self.zt_history) < 5:
            return "stable"

        counts = list(self.zt_history)

        # 计算MA5和MA10
        ma5 = sum(counts[-5:]) / 5
        ma10 = sum(counts) / len(counts) if len(counts) >= 5 else ma5

        if ma5 > ma10 * 1.1:
            return "up"
        elif ma5 < ma10 * 0.9:
            return "down"
        else:
            return "stable"

    def get_dynamic_threshold(self):
        """
        获取动态阈值

        返回: 调整后的阈值
        """
        trend = self.get_trend()

        if trend == "up":
            # 趋势上升，放宽阈值
            return self.base_threshold * (1 - self.trend_adjustment)
        elif trend == "down":
            # 趋势下降，收紧阈值
            return self.base_threshold * (1 + self.trend_adjustment)
        else:
            return self.base_threshold

    def get_position_ratio(self, zt_count):
        """
        根据涨停家数获取仓位比例

        参数:
            zt_count: 涨停家数

        返回:
            仓位比例 (0.0 ~ 1.0)
        """
        for threshold, ratio in self.position_levels:
            if zt_count >= threshold:
                return ratio
        return 0.0

    def check(self, zt_count, use_trend=True):
        """
        检查是否开仓及仓位比例

        参数:
            zt_count: 当日涨停家数
            use_trend: 是否使用趋势调整（默认True）

        返回:
            (should_trade, position_ratio, info)
            - should_trade: 是否开仓
            - position_ratio: 仓位比例
            - info: 详细信息字典
        """
        # 更新历史
        self.update_history(zt_count)

        # 1. 过热过滤（硬规则）
        if zt_count > self.overheat_threshold:
            return (
                False,
                0.0,
                {
                    "reason": "overheat",
                    "zt_count": zt_count,
                    "threshold": self.overheat_threshold,
                    "trend": "N/A",
                },
            )

        # 2. 趋势判断
        trend = self.get_trend() if use_trend else "stable"

        # 3. 动态阈值
        threshold = self.get_dynamic_threshold() if use_trend else self.base_threshold

        # 4. 阈值判断
        if zt_count < threshold:
            return (
                False,
                0.0,
                {
                    "reason": "below_threshold",
                    "zt_count": zt_count,
                    "threshold": threshold,
                    "trend": trend,
                },
            )

        # 5. 仓位计算
        position_ratio = self.get_position_ratio(zt_count)

        if position_ratio <= 0:
            return (
                False,
                0.0,
                {
                    "reason": "low_position",
                    "zt_count": zt_count,
                    "threshold": threshold,
                    "trend": trend,
                },
            )

        return (
            True,
            position_ratio,
            {
                "reason": "ok",
                "zt_count": zt_count,
                "threshold": threshold,
                "trend": trend,
                "position_ratio": position_ratio,
            },
        )

    def reset(self):
        """重置历史数据"""
        self.zt_history.clear()


# ============================================================
# 工具函数
# ============================================================


def get_zt_count(date):
    """
    获取指定日期的涨停家数

    参数:
        date: 日期字符串，如 "2024-01-15"

    返回:
        涨停家数
    """
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        # 排除科创板、北交所
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ][:500]

        df = get_price(
            all_stocks,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()

        return len(df[df["close"] == df["high_limit"]])
    except:
        return 0


def get_zt_counts_history(end_date, days=10):
    """
    获取历史涨停家数列表

    参数:
        end_date: 结束日期
        days: 获取天数

    返回:
        涨停家数列表
    """
    trade_days = get_trade_days(end_date=end_date, count=days)
    counts = []

    for d in trade_days:
        count = get_zt_count(str(d))
        counts.append(count)

    return counts


# ============================================================
# 测试函数
# ============================================================


def test_sentiment_switch_v2():
    """测试情绪开关v2"""
    print("=" * 60)
    print("情绪开关v2测试")
    print("=" * 60)

    switch = SentimentSwitchV2(
        base_threshold=20, overheat_threshold=100, trend_adjustment=0.15
    )

    # 模拟测试数据
    test_cases = [
        (10, "极低情绪"),
        (15, "低情绪"),
        (20, "阈值边界"),
        (25, "低情绪+"),
        (30, "中情绪"),
        (50, "高情绪"),
        (80, "极高情绪"),
        (100, "过热边界"),
        (120, "过热"),
    ]

    print("\n测试结果:")
    print("-" * 60)
    print(f"{'涨停家数':>8} | {'状态':>8} | {'开仓':>4} | {'仓位':>6} | {'原因':<15}")
    print("-" * 60)

    for zt_count, label in test_cases:
        should_trade, position_ratio, info = switch.check(zt_count, use_trend=False)

        trade_str = "是" if should_trade else "否"
        pos_str = f"{position_ratio:.0%}" if position_ratio > 0 else "-"

        print(
            f"{zt_count:>8} | {label:>8} | {trade_str:>4} | {pos_str:>6} | {info['reason']:<15}"
        )

    print("-" * 60)
    print("\n测试完成")


if __name__ == "__main__":
    test_sentiment_switch_v2()
