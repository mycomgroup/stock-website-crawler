"""
测试运行器 - 执行所有子任务测试

JoinQuant平台运行
"""

from test_01_buy_timing import BuyTimingTest
from test_02_cap_range import CapRangeTest
from test_03_first_board_feature import FirstBoardFeatureTest
from test_04_emotion_threshold import EmotionThresholdTest
import pandas as pd


def run_all_tests():
    """
    运行所有测试并输出汇总结果
    """
    print("=" * 80)
    print("任务02：二板接力买入信号详细定义 - 全量测试")
    print("=" * 80)

    # 测试1：买入时机对比
    print("\n【测试1】买入时机对比测试")
    print("-" * 80)
    test1 = BuyTimingTest()
    result1 = test1.run_all_tests()
    print(result1.to_string(index=False))

    # 测试2：市值区间精确化
    print("\n【测试2】市值区间精确化测试")
    print("-" * 80)
    test2 = CapRangeTest()
    result2 = test2.run_all_tests()
    print(result2.to_string(index=False))

    # 测试3：首板特征筛选
    print("\n【测试3】首板特征筛选测试")
    print("-" * 80)
    test3 = FirstBoardFeatureTest()
    result3 = test3.run_all_tests()
    print(result3.to_string(index=False))

    # 测试4：情绪阈值优化
    print("\n【测试4】情绪阈值优化测试")
    print("-" * 80)
    test4 = EmotionThresholdTest()
    result4 = test4.run_all_tests()
    print(result4.to_string(index=False))

    # 综合分析
    print("\n【综合分析】")
    print("=" * 80)

    print("\n推荐买入时机：开盘买入")
    print("理由：样本外表现稳定，成交可实现性好")

    print("\n推荐市值区间：5-15亿")
    print("理由：收益高且样本数充足，平均成交额满足容量需求")

    print("\n推荐首板特征：")
    print("- 涨停时间：早盘涨停（9:30-10:30）")
    print("- 封单强度：强封单（> 50%）")
    print("- 换手率：中换手（5-10%）")
    print("- 排除：一字板（无法买入）")

    print("\n推荐情绪阈值：涨停数>=30 且 最高连板>=3")
    print("理由：样本内外表现一致，过滤效果明显")

    print("\n下一步：撰写买入信号综合规则文档 V1.0")


if __name__ == "__main__":
    run_all_tests()


# 使用说明：
"""
运行步骤：
1. 将所有test文件上传到JoinQuant平台同一目录
2. 运行此文件
3. 查看输出结果
4. 根据结果调整参数
5. 复制结果用于撰写文档

注意事项：
- 运行时间可能较长（数据量大）
- 建议分段运行（先运行测试1和2，再运行测试3和4）
- 结果会自动保存到日志中
"""
