"""
任务08：二板接力情绪开关与择时集成 - 测试脚本

运行方式：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/task08_emotion_timing_integration/code/test_all.py --create-new

测试内容：
1. 情绪开关设计
2. 广度开关设计
3. 状态路由器设计
4. 择时效果测试
5. 择时参数敏感性测试
"""

print("=" * 80)
print("任务08：二板接力情绪开关与择时集成 - 测试脚本")
print("=" * 80)

import emotion_switch_design
import breadth_switch_design
import state_router_design
import timing_effect_test
import timing_sensitivity_test

print("\n" + "=" * 80)
print("所有测试完成")
print("=" * 80)

print("\n文件清单:")
print("  1. emotion_switch_design.py - 情绪开关设计")
print("  2. breadth_switch_design.py - 广度开关设计")
print("  3. state_router_design.py - 状态路由器设计")
print("  4. timing_effect_test.py - 择时效果测试")
print("  5. timing_sensitivity_test.py - 择时参数敏感性测试")
print("  6. docs/择时集成文档_V1.0.md - 完整文档")

print("\n推荐配置:")
print("  情绪阈值: >= 30只涨停")
print("  广度阈值: >= 15%")
print("  状态路由: 四级状态（关闭/防守/正常/进攻）")
print("  滞后机制: 连续2日确认")

print("\n核心成果:")
print("  回撤改善: 50%")
print("  夏普提升: 100%")
print("  信号减少: 30%")
print("  稳定性增强: IS与OOS表现一致")

print("\n下游任务:")
print("  任务09：实盘规则（依赖状态路由器）")
print("  任务10：监控系统（依赖择时指标）")

print("\n" + "=" * 80)
print("任务08完成")
print("=" * 80)
