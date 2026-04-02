#!/usr/bin/env python3
"""
情绪周期划分模块

将市场情绪划分为四个阶段：启动期、发酵期、高潮期、退潮期。
用于判断当前市场所处状态，辅助策略决策。

使用方法:
    from sentiment_phase import classify_sentiment_phase

    sentiment = calc_market_sentiment(date, prev_date)
    phase = classify_sentiment_phase(sentiment)

    if phase in ['up', 'high']:
        # 积极开仓
        pass
    elif phase == 'down':
        # 空仓观望
        pass
"""

from typing import Dict, Literal

# 情绪周期类型
PhaseType = Literal["up", "high", "normal", "down"]


def classify_sentiment_phase(sentiment_data: Dict) -> PhaseType:
    """
    根据情绪指标划分情绪周期

    参数:
        sentiment_data: 情绪指标字典，包含:
            - zt_count: 涨停家数
            - max_lianban: 最高连板数
            - jinji_rate: 晋级率（可选）

    返回:
        'up': 上升期（启动期）
        'high': 高潮期
        'normal': 平稳期（发酵期）
        'down': 退潮期

    划分规则:
        - 高潮期：最高连板>=5 且 涨停>=40
        - 上升期：最高连板>=3 且 涨停>=25 且 晋级率>=30%
        - 退潮期：涨停<15 或 (最高连板<=2 且 涨停<20)
        - 平稳期：其他情况
    """
    zt = sentiment_data.get("zt_count", 0)
    ml = sentiment_data.get("max_lianban", 0)
    jr = sentiment_data.get("jinji_rate", 0)

    # 高潮期
    if ml >= 5 and zt >= 40:
        return "high"

    # 上升期
    elif ml >= 3 and zt >= 25 and jr >= 0.3:
        return "up"

    # 退潮期
    elif zt < 15 or (ml <= 2 and zt < 20):
        return "down"

    # 平稳期
    else:
        return "normal"


def get_phase_description(phase: PhaseType) -> Dict:
    """
    获取情绪周期描述

    参数:
        phase: 周期类型

    返回:
        {
            'name': '中文名称',
            'description': '详细描述',
            'suggestion': '策略建议',
            'risk_level': '风险等级(1-5)'
        }
    """
    descriptions = {
        "up": {
            "name": "上升期",
            "description": "情绪开始转暖，赚钱效应扩散，龙头确立",
            "suggestion": "积极开仓，重点关注龙头和题材",
            "risk_level": 2,
        },
        "high": {
            "name": "高潮期",
            "description": "情绪亢奋，涨停众多，连板高度较高",
            "suggestion": "谨慎开仓，注意风险，避免追高",
            "risk_level": 4,
        },
        "normal": {
            "name": "平稳期",
            "description": "情绪平稳，无明显方向",
            "suggestion": "小仓位试探，快进快出",
            "risk_level": 3,
        },
        "down": {
            "name": "退潮期",
            "description": "赚钱效应消失，涨停稀少，龙头断板",
            "suggestion": "空仓观望，等待机会",
            "risk_level": 5,
        },
    }
    return descriptions.get(phase, descriptions["normal"])


def get_phase_position_limit(phase: PhaseType) -> float:
    """
    获取各周期的仓位上限建议

    参数:
        phase: 周期类型

    返回:
        仓位上限比例 (0.0 - 1.0)
    """
    limits = {
        "up": 1.0,  # 上升期：满仓
        "high": 0.5,  # 高潮期：半仓（注意风险）
        "normal": 0.3,  # 平稳期：三成仓
        "down": 0.0,  # 退潮期：空仓
    }
    return limits.get(phase, 0.3)


def analyze_phase_transition(prev_phase: PhaseType, curr_phase: PhaseType) -> Dict:
    """
    分析情绪周期转换

    参数:
        prev_phase: 前一日周期
        curr_phase: 当前周期

    返回:
        {
            'direction': 'up'/'down'/'stable',
            'description': '转换描述',
            'action': '建议操作'
        }
    """
    phase_order = {"down": 0, "normal": 1, "up": 2, "high": 3}

    prev_order = phase_order.get(prev_phase, 1)
    curr_order = phase_order.get(curr_phase, 1)

    if curr_order > prev_order:
        direction = "up"
        description = f"情绪上升: {get_phase_description(prev_phase)['name']} → {get_phase_description(curr_phase)['name']}"
        action = "可以逐步加仓"
    elif curr_order < prev_order:
        direction = "down"
        description = f"情绪下降: {get_phase_description(prev_phase)['name']} → {get_phase_description(curr_phase)['name']}"
        action = "建议减仓或空仓"
    else:
        direction = "stable"
        description = f"情绪稳定: {get_phase_description(curr_phase)['name']}"
        action = "维持当前策略"

    return {"direction": direction, "description": description, "action": action}


def get_market_status_report(
    sentiment_data: Dict, prev_phase: PhaseType = None
) -> Dict:
    """
    生成市场状态报告

    参数:
        sentiment_data: 情绪指标字典
        prev_phase: 前一日周期（可选）

    返回:
        完整的市场状态报告
    """
    curr_phase = classify_sentiment_phase(sentiment_data)
    phase_desc = get_phase_description(curr_phase)
    position_limit = get_phase_position_limit(curr_phase)

    report = {
        "phase": curr_phase,
        "phase_name": phase_desc["name"],
        "description": phase_desc["description"],
        "suggestion": phase_desc["suggestion"],
        "risk_level": phase_desc["risk_level"],
        "position_limit": position_limit,
        "indicators": {
            "zt_count": sentiment_data.get("zt_count", 0),
            "max_lianban": sentiment_data.get("max_lianban", 0),
            "jinji_rate": sentiment_data.get("jinji_rate", 0),
        },
    }

    if prev_phase:
        transition = analyze_phase_transition(prev_phase, curr_phase)
        report["transition"] = transition

    return report


# ============ 使用示例 ============

if __name__ == "__main__":
    # 测试不同情绪状态
    test_cases = [
        {"zt_count": 8, "max_lianban": 1, "jinji_rate": 0.1, "name": "极端冰点"},
        {"zt_count": 18, "max_lianban": 2, "jinji_rate": 0.2, "name": "退潮期"},
        {"zt_count": 30, "max_lianban": 3, "jinji_rate": 0.35, "name": "上升期"},
        {"zt_count": 55, "max_lianban": 6, "jinji_rate": 0.4, "name": "高潮期"},
    ]

    print("=" * 70)
    print("情绪周期划分测试")
    print("=" * 70)

    for case in test_cases:
        name = case.pop("name")
        phase = classify_sentiment_phase(case)
        desc = get_phase_description(phase)
        limit = get_phase_position_limit(phase)

        print(f"\n【{name}】")
        print(
            f"  涨停={case['zt_count']}, 连板={case['max_lianban']}, 晋级率={case['jinji_rate']:.0%}"
        )
        print(f"  → 周期: {desc['name']}")
        print(f"  → 描述: {desc['description']}")
        print(f"  → 建议: {desc['suggestion']}")
        print(f"  → 风险: {'★' * desc['risk_level']}")
        print(f"  → 仓位上限: {limit:.0%}")
