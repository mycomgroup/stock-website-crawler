"""
提示词8.3：状态路由器设计

状态定义：关闭/防守/正常/进攻
基于广度+情绪综合判定
每种状态下有不同的策略行为
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("提示词8.3：状态路由器设计")
print("=" * 80)
print("配置:")
print("  状态: 关闭/防守/正常/进攻")
print("  输入: 广度+情绪")
print("  输出: 仓位+信号选择")
print("=" * 80)

ROUTER_CONFIG = {
    "states": ["关闭", "防守", "正常", "进攻"],
    "breadth_thresholds": {
        "关闭": 0.15,
        "防守": 0.25,
        "正常": 0.35,
        "进攻": 0.35,
    },
    "emotion_thresholds": {
        "关闭": 0,
        "防守": 30,
        "正常": 50,
        "进攻": 80,
    },
    "position_sizes": {
        "关闭": 0.0,
        "防守": 0.50,
        "正常": 1.0,
        "进攻": 1.2,
    },
    "signal_strictness": {
        "关闭": "无",
        "防守": "最强",
        "正常": "正常",
        "进攻": "放宽",
    },
    "min_duration": {
        "关闭": 1,
        "防守": 1,
        "正常": 1,
        "进攻": 1,
    },
    "confirmation_days": 2,
}


class MarketStateRouter:
    def __init__(self, config):
        self.config = config
        self.current_state = "正常"
        self.state_history = []
        self.confirmation_buffer = []

    def determine_state(self, breadth_pct, emotion_value):
        """
        根据广度+情绪判定状态

        规则:
        - 关闭: 广度<15% 或 情绪<30且广度<25%
        - 防守: 广度15-25% 或 情绪30-50
        - 正常: 广度25-35% 且 情绪50-80
        - 进攻: 广度>=35% 且 情绪>=80
        """
        if breadth_pct < self.config["breadth_thresholds"]["关闭"]:
            return "关闭"

        if breadth_pct < self.config["breadth_thresholds"]["防守"]:
            return "防守"

        if emotion_value < self.config["emotion_thresholds"]["防守"]:
            if breadth_pct < self.config["breadth_thresholds"]["防守"]:
                return "关闭"
            return "防守"

        if (
            breadth_pct >= self.config["breadth_thresholds"]["进攻"]
            and emotion_value >= self.config["emotion_thresholds"]["进攻"]
        ):
            return "进攻"

        if (
            breadth_pct >= self.config["breadth_thresholds"]["正常"]
            and emotion_value >= self.config["emotion_thresholds"]["正常"]
        ):
            return "进攻"

        return "正常"

    def update_state(self, breadth_pct, emotion_value, date):
        """
        更新状态（带滞后机制）
        """
        new_state = self.determine_state(breadth_pct, emotion_value)

        self.confirmation_buffer.append(
            {
                "date": date,
                "state": new_state,
                "breadth": breadth_pct,
                "emotion": emotion_value,
            }
        )

        if len(self.confirmation_buffer) >= self.config["confirmation_days"]:
            recent_states = [
                item["state"]
                for item in self.confirmation_buffer[
                    -self.config["confirmation_days"] :
                ]
            ]

            if all(s == new_state for s in recent_states):
                if new_state != self.current_state:
                    old_state = self.current_state
                    self.current_state = new_state

                    self.state_history.append(
                        {
                            "date": date,
                            "old_state": old_state,
                            "new_state": new_state,
                            "breadth": breadth_pct,
                            "emotion": emotion_value,
                        }
                    )

                    return True, old_state, new_state

        return False, self.current_state, self.current_state

    def get_strategy_behavior(self):
        """
        获取当前状态下的策略行为
        """
        return {
            "state": self.current_state,
            "position_size": self.config["position_sizes"][self.current_state],
            "signal_strictness": self.config["signal_strictness"][self.current_state],
            "min_duration": self.config["min_duration"][self.current_state],
        }


print("\n步骤1: 状态定义")
print("-" * 80)

print("\n| 状态 | 判定条件 | 仓位 | 信号选择 | 持续时间 |")
print("|------|---------|------|---------|---------|")

for state in ROUTER_CONFIG["states"]:
    breadth_cond = ""
    emotion_cond = ""

    if state == "关闭":
        breadth_cond = "广度<15%"
        emotion_cond = "或情绪<30且广度<25%"
    elif state == "防守":
        breadth_cond = "广度15-25%"
        emotion_cond = "或情绪30-50"
    elif state == "正常":
        breadth_cond = "广度25-35%"
        emotion_cond = "且情绪50-80"
    elif state == "进攻":
        breadth_cond = "广度>=35%"
        emotion_cond = "且情绪>=80"

    position = ROUTER_CONFIG["position_sizes"][state]
    signal = ROUTER_CONFIG["signal_strictness"][state]
    duration = ROUTER_CONFIG["min_duration"][state]

    print(
        f"| {state} | {breadth_cond} | {position * 100:.0f}% | {signal} | 最短{duration}日 |"
    )

print("\n步骤2: 状态转换规则")
print("-" * 80)

print("\n状态转换规则:")
print("\n上行转换:")
print("- 关闭 -> 防守: 广度回升至15%以上 且 情绪改善（连续2日确认）")
print("- 防守 -> 正常: 广度回升至25%以上（连续2日确认）")
print("- 正常 -> 进攻: 广度>=35% 且 情绪>=80（连续2日确认）")

print("\n下行转换:")
print("- 进攻 -> 正常: 广度下降或情绪回落（连续2日确认）")
print("- 正常 -> 防守: 广度下降至25%以下（连续2日确认）")
print("- 防守 -> 关闭: 广度下降至15%以下（连续2日确认）")

print("\n步骤3: 每种状态下的策略行为")
print("-" * 80)

print("\n[关闭状态]")
print("- 行为: 不交易")
print("- 仓位: 0%")
print("- 信号: 无")
print("- 触发: 广度<15% 或 情绪冰点")
print("- 持续: 最短1日")

print("\n[防守状态]")
print("- 行为: 降低仓位，只选最强信号")
print("- 仓位: 50%")
print("- 信号: 只选择最强信号（如假弱高开+题材热点）")
print("- 触发: 广度15-25% 或 情绪启动")
print("- 持续: 最短1日")

print("\n[正常状态]")
print("- 行为: 正常交易")
print("- 仓位: 100%")
print("- 信号: 正常信号选择")
print("- 触发: 广度25-35% 且 情绪发酵")
print("- 持续: 最短1日")

print("\n[进攻状态]")
print("- 行为: 增加仓位，放宽信号")
print("- 仓位: 120%（适度加杠杆）")
print("- 信号: 可放宽信号标准（如降低市值要求）")
print("- 触发: 广度>=35% 且 情绪高潮")
print("- 持续: 最短1日")

print("\n步骤4: 滞后机制设计")
print("-" * 80)

print("\n滞后机制:")
print("- 状态转换需连续2日确认")
print("- 避免频繁切换")
print("- 最短持续时间: 1日")

print("\n转换确认逻辑:")
print("1. 每日判定新状态")
print("2. 记录最近2日的状态")
print("3. 若最近2日状态相同且与当前状态不同")
print("4. 则转换至新状态")
print("5. 否则保持当前状态")

print("\n步骤5: 状态路由器实例测试")
print("-" * 80)

router = MarketStateRouter(ROUTER_CONFIG)

test_cases = [
    {"breadth": 0.10, "emotion": 20, "expected": "关闭"},
    {"breadth": 0.18, "emotion": 25, "expected": "防守"},
    {"breadth": 0.20, "emotion": 40, "expected": "防守"},
    {"breadth": 0.28, "emotion": 60, "expected": "正常"},
    {"breadth": 0.30, "emotion": 70, "expected": "进攻"},
    {"breadth": 0.40, "emotion": 85, "expected": "进攻"},
]

print("\n| 广度 | 情绪 | 预期状态 | 实际状态 | 匹配 |")
print("|------|------|---------|---------|------|")

for i, case in enumerate(test_cases, 1):
    actual_state = router.determine_state(case["breadth"], case["emotion"])
    match = "✓" if actual_state == case["expected"] else "✗"
    print(
        f"| {case['breadth'] * 100:.0f}% | {case['emotion']}只 | {case['expected']} | {actual_state} | {match} |"
    )

print("\n步骤6: 状态路由器与策略集成")
print("-" * 80)

print("\n集成步骤:")
print("\n1. 每日收盘后:")
print("   - 计算广度指标（沪深300站上20日线占比）")
print("   - 计算情绪指标（涨停家数）")
print("   - 更新状态路由器")
print("   - 获取策略行为（仓位、信号选择）")

print("\n2. 次日开盘前:")
print("   - 检查当前状态")
print("   - 根据状态调整仓位上限")
print("   - 根据状态调整信号筛选标准")

print("\n3. 信号筛选:")
print("   - 关闭: 无信号")
print("   - 防守: 只选最强信号（如假弱高开+题材）")
print("   - 正常: 正常信号筛选")
print("   - 进攻: 放宽信号标准")

print("\n4. 仓位控制:")
print("   - 关闭: 0%仓位")
print("   - 防守: 单票<=2.5%，总仓<=15%")
print("   - 正常: 单票<=5%，总仓<=30%")
print("   - 进攻: 单票<=6%，总仓<=36%")

print("\n" + "=" * 80)
print("状态路由器设计完成")
print("=" * 80)

print("\n核心设计:")
print("  四级状态: 关闭/防守/正常/进攻")
print("  双重输入: 广度+情绪")
print("  滞后机制: 连续2日确认")
print("  行为输出: 仓位+信号选择")
