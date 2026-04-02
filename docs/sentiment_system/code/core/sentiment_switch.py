#!/usr/bin/env python3
"""
情绪开关判断模块

提供多种情绪开关方案，用于控制策略的开仓/空仓决策。

使用方法:
    from sentiment_switch import sentiment_switch_combo

    # 计算情绪指标
    sentiment = calc_market_sentiment(date, prev_date)

    # 判断是否开仓
    if sentiment_switch_combo(sentiment):
        # 执行开仓
        pass
    else:
        # 空仓等待
        pass
"""

from typing import Dict, Optional


def sentiment_switch_simple(zt_count: int, threshold: int = 30) -> bool:
    """
    简化版：涨停家数单指标开关

    参数:
        zt_count: 涨停家数
        threshold: 阈值，默认30

    返回:
        True: 开仓
        False: 空仓

    使用场景:
        - 快速判断，适合盘前快速决策
        - 阈值建议：30（中等）、50（严格）
    """
    return zt_count >= threshold


def sentiment_switch_lianban(max_lianban: int, threshold: int = 3) -> bool:
    """
    基于最高连板数的开关

    参数:
        max_lianban: 最高连板数
        threshold: 阈值，默认3

    返回:
        True: 开仓
        False: 空仓

    使用场景:
        - 关注市场赚钱效应
        - 连板高度反映接力意愿
    """
    return max_lianban >= threshold


def sentiment_switch_ratio(zt_dt_ratio: float, threshold: float = 2.0) -> bool:
    """
    基于涨跌停比的开关

    参数:
        zt_dt_ratio: 涨跌停比
        threshold: 阈值，默认2.0

    返回:
        True: 开仓
        False: 空仓

    使用场景:
        - 反映多空力量对比
        - 适合判断市场极端状态
    """
    return zt_dt_ratio >= threshold


def sentiment_switch_combo(
    sentiment_data: Dict,
    min_lianban: int = 2,
    min_zt_count: int = 15,
    min_zt_dt_ratio: float = 1.5,
) -> bool:
    """
    组合指标开关（推荐）

    参数:
        sentiment_data: 情绪指标字典，包含:
            - max_lianban: 最高连板数
            - zt_count: 涨停家数
            - zt_dt_ratio: 涨跌停比
        min_lianban: 最低连板数阈值，默认2
        min_zt_count: 最低涨停家数阈值，默认15
        min_zt_dt_ratio: 最低涨跌停比阈值，默认1.5

    返回:
        True: 开仓
        False: 空仓

    推荐理由:
        - 三个指标互相验证，减少假信号
        - 阈值设置合理，不会过于激进
        - 简单可执行，适合开盘前快速判断
    """
    return (
        sentiment_data.get("max_lianban", 0) >= min_lianban
        and sentiment_data.get("zt_count", 0) >= min_zt_count
        and sentiment_data.get("zt_dt_ratio", 0) >= min_zt_dt_ratio
    )


def sentiment_switch_by_phase(sentiment_data: Dict) -> bool:
    """
    基于情绪周期的开关

    参数:
        sentiment_data: 情绪指标字典

    返回:
        True: 开仓（上升期或高潮期）
        False: 空仓（退潮期或平稳期）

    使用场景:
        - 结合情绪周期划分
        - 只在赚钱效应明确的阶段开仓
    """
    from sentiment_phase import classify_sentiment_phase

    phase = classify_sentiment_phase(sentiment_data)
    return phase in ["up", "high"]


def sentiment_switch_three_level(sentiment_data: Dict) -> str:
    """
    三档仓位调节器

    参数:
        sentiment_data: 情绪指标字典

    返回:
        'full': 满仓（情绪热）
        'half': 半仓（情绪中）
        'empty': 空仓（情绪冷）

    使用场景:
        - 组合层仓位管理
        - 根据情绪强度动态调整仓位
    """
    zt = sentiment_data.get("zt_count", 0)
    ml = sentiment_data.get("max_lianban", 0)

    # 满仓档：涨停>50 且 连板>5
    if zt > 50 and ml > 5:
        return "full"
    # 半仓档：涨停30-50 且 连板3-5
    elif 30 <= zt <= 50 and 3 <= ml <= 5:
        return "half"
    # 空仓档：其他情况
    else:
        return "empty"


def get_switch_recommendation(sentiment_data: Dict) -> Dict:
    """
    获取综合开关建议

    参数:
        sentiment_data: 情绪指标字典

    返回:
        {
            'action': 'open'/'close',
            'position': 'full'/'half'/'empty',
            'reason': '原因说明',
            'indicators': '关键指标值'
        }
    """
    zt = sentiment_data.get("zt_count", 0)
    dt = sentiment_data.get("dt_count", 0)
    ml = sentiment_data.get("max_lianban", 0)
    ratio = sentiment_data.get("zt_dt_ratio", 0)

    # 判断仓位
    position = sentiment_switch_three_level(sentiment_data)

    # 判断是否开仓
    should_open = sentiment_switch_combo(sentiment_data)

    # 生成原因
    reasons = []
    if ml >= 3:
        reasons.append(f"连板高度{ml}板")
    if zt >= 30:
        reasons.append(f"涨停{zt}家")
    if ratio >= 2:
        reasons.append(f"涨跌停比{ratio:.1f}")

    reason = "，".join(reasons) if reasons else "情绪指标未达标"

    return {
        "action": "open" if should_open else "close",
        "position": position,
        "reason": reason,
        "indicators": {
            "zt_count": zt,
            "dt_count": dt,
            "max_lianban": ml,
            "zt_dt_ratio": round(ratio, 2),
        },
    }


# ============ 使用示例 ============

if __name__ == "__main__":
    # 模拟情绪数据
    test_sentiment = {
        "zt_count": 45,
        "dt_count": 8,
        "zt_dt_ratio": 5.6,
        "max_lianban": 4,
        "jinji_rate": 0.35,
    }

    print("=" * 60)
    print("情绪开关测试")
    print("=" * 60)

    print(f"\n测试数据: {test_sentiment}")

    print(
        f"\n1. 简化版开关(阈值30): {sentiment_switch_simple(test_sentiment['zt_count'], 30)}"
    )
    print(
        f"2. 连板开关(阈值3): {sentiment_switch_lianban(test_sentiment['max_lianban'], 3)}"
    )
    print(
        f"3. 涨跌停比开关(阈值2): {sentiment_switch_ratio(test_sentiment['zt_dt_ratio'], 2)}"
    )
    print(f"4. 组合指标开关: {sentiment_switch_combo(test_sentiment)}")
    print(f"5. 三档仓位: {sentiment_switch_three_level(test_sentiment)}")

    print(f"\n综合建议:")
    rec = get_switch_recommendation(test_sentiment)
    print(f"  操作: {rec['action']}")
    print(f"  仓位: {rec['position']}")
    print(f"  原因: {rec['reason']}")
    print(f"  指标: {rec['indicators']}")
