#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务07下一步：三个验证任务
1. 2025年样本外验证
2. 情绪阈值动态调整机制
3. 30天模拟盘验证

作者：AI量化研究助手
日期：2026-04-02
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class ParameterSensitivityNextSteps:
    """参数敏感性分析下一步任务"""

    def __init__(self):
        self.base_params = {
            "market_cap_lower": 5,  # 市值下限（亿）
            "market_cap_upper": 50,  # 市值上限（亿）
            "sentiment_threshold": 10,  # 情绪阈值（涨停数）
            "volume_ratio": 1.875,  # 缩量倍数
            "turnover_limit": 30,  # 换手率上限
            "buy_timing": "non_limit_open",  # 买入时机
            "sell_timing": "next_close",  # 卖出时机
            "stop_loss": -5,  # 止损阈值
            "single_position": 5,  # 单票仓位（%）
            "total_position": 30,  # 总仓位（%）
        }

        self.results = {
            "task1_2025_oos_validation": {},
            "task2_dynamic_sentiment": {},
            "task3_30day_simulation": {},
        }

    def task1_2025_oos_validation(self):
        """
        任务1：2025年样本外验证

        目标：
        - 验证策略在2025年的表现
        - 确认参数稳健性
        - 检测策略衰减信号
        """
        print("\n" + "=" * 80)
        print("任务1：2025年样本外验证")
        print("=" * 80)

        print("\n【测试方案】")
        print("- 时间范围：2025-01-01 至 2025-03-31（Q1）")
        print("- 参数：稳健优先方案（市值5-50亿，情绪涨停≥10）")
        print("- 对比基准：2024年实测（年化394%，胜率87.95%，回撤0.60%）")

        print("\n【测试代码】")
        print("```python")
        print("# 聚宽Notebook测试代码")
        print("def test_2025_q1():")
        print("    # 参数设置")
        print("    market_cap_range = (5, 50)  # 亿元")
        print("    sentiment_threshold = 10  # 涨停家数")
        print("    volume_ratio = 1.875")
        print("    ")
        print("    # 时间范围")
        print("    start_date = '2025-01-01'")
        print("    end_date = '2025-03-31'")
        print("    ")
        print("    # 二板选股逻辑")
        print("    def get_second_board_signals(date):")
        print("        # 前日涨停股票")
        print("        hl_prev = get_hl_stock(all_stocks, date-1)")
        print("        # 昨日涨停股票")
        print("        hl_curr = get_hl_stock(all_stocks, date)")
        print("        # 二板股票")
        print("        second_board = [s for s in hl_curr if s in hl_prev]")
        print("        ")
        print("        # 过滤条件")
        print("        # 1. 非一字板")
        print("        df = get_price(second_board, end_date=date, count=1,")
        print("                      fields=['low', 'high_limit'], panel=False)")
        print(
            "        second_board = df[df['low'] < df['high_limit']]['code'].tolist()"
        )
        print("        ")
        print("        # 2. 换手率<30%")
        print("        # 3. 缩量条件")
        print("        # 4. 市值排序")
        print("        # ... 详细代码见完整版")
        print("        ")
        print("        return second_board_filtered")
        print("    ")
        print("    # 回测")
        print("    for date in trading_dates:")
        print("        # 情绪过滤")
        print("        zt_count = get_zt_count(date-1)")
        print("        if zt_count < sentiment_threshold:")
        print("            continue")
        print("        ")
        print("        # 选股")
        print("        signals = get_second_board_signals(date)")
        print("        ")
        print("        # 买入")
        print("        for stock in signals:")
        print("            # 非涨停开盘买入")
        print("            # ...")
        print("        ")
        print("        # 次日卖出")
        print("        # ...")
        print("    ")
        print("    return results")
        print("```")

        print("\n【预期结果】")
        print("- 年化收益：200-400%（2025年Q1，假设市场正常）")
        print("- 胜率：80-90%")
        print("- 最大回撤：5-15%")

        print("\n【判断标准】")
        print("- ✅ Go：年化>200%，胜率>80%，回撤<15%")
        print("- ⚠️ Watch：年化100-200%，胜率70-80%，回撤15-25%")
        print("- ❌ No-Go：年化<100%，胜率<70%，回撤>25%")

        print("\n【执行方式】")
        print("- 使用聚宽Notebook运行测试代码")
        print("- 保存结果到：/output/task07_2025_q1_test_result.json")
        print("- 预计耗时：30分钟")

        self.results["task1_2025_oos_validation"] = {
            "status": "pending",
            "test_period": "2025-01-01 to 2025-03-31",
            "params": self.base_params,
            "expected_return": "200-400%",
            "expected_winrate": "80-90%",
            "expected_drawdown": "5-15%",
        }

        return self.results["task1_2025_oos_validation"]

    def task2_dynamic_sentiment_adjustment(self):
        """
        任务2：情绪阈值动态调整机制

        目标：
        - 建立情绪阈值动态调整规则
        - 适应市场环境变化
        - 平衡交易机会与失败率
        """
        print("\n" + "=" * 80)
        print("任务2：情绪阈值动态调整机制")
        print("=" * 80)

        print("\n【市场环境分类】")
        print("\n基于历史涨停均值，划分市场环境：")
        print("- 情绪高涨期：涨停均值>100（建议阈值：涨停≥20）")
        print("- 正常情绪期：涨停均值50-100（建议阈值：涨停≥10）")
        print("- 情绪低迷期：涨停均值<50（建议阈值：涨停≥5或空仓）")

        print("\n【动态调整规则】")
        print("\n```python")
        print("def get_dynamic_sentiment_threshold(date):")
        print('    """动态情绪阈值计算"""')
        print("    ")
        print("    # 计算过去20日涨停均值")
        print("    zt_counts = [get_zt_count(date - i) for i in range(1, 21)]")
        print("    zt_mean = sum(zt_counts) / len(zt_counts)")
        print("    ")
        print("    # 动态阈值")
        print("    if zt_mean > 100:")
        print("        # 情绪高涨期")
        print("        threshold = 20")
        print("        action = 'aggressive'  # 积极交易")
        print("        position_ratio = 1.0  # 满仓")
        print("    elif zt_mean >= 50:")
        print("        # 正常情绪期")
        print("        threshold = 10")
        print("        action = 'normal'  # 正常交易")
        print("        position_ratio = 1.0  # 满仓")
        print("    elif zt_mean >= 30:")
        print("        # 情绪低迷期")
        print("        threshold = 5")
        print("        action = 'cautious'  # 谨慎交易")
        print("        position_ratio = 0.5  # 半仓")
        print("    else:")
        print("        # 情绪冰点")
        print("        threshold = 0  # 无交易")
        print("        action = 'avoid'  # 空仓观望")
        print("        position_ratio = 0.0  # 空仓")
        print("    ")
        print("    return {")
        print("        'threshold': threshold,")
        print("        'action': action,")
        print("        'position_ratio': position_ratio,")
        print("        'zt_mean': zt_mean")
        print("    }")
        print("```")

        print("\n【历史环境回测】")
        print("\n2021-2024年市场环境统计：")
        print("- 2021年：涨停均值30-50，情绪正常期")
        print("- 2022年：涨停均值20-40，情绪低迷期（熊市）")
        print("- 2023年：涨停均值30-50，情绪正常期")
        print("- 2024年：涨停均值70-100，情绪高涨期")
        print("- 2025年Q1：涨停均值48-95，情绪正常期")

        print("\n【调整频率】")
        print("- 每日调整：计算过去20日涨停均值，更新阈值")
        print("- 每周复核：检查调整效果，必要时微调")
        print("- 每月总结：评估动态调整机制有效性")

        print("\n【回测验证】")
        print("对比固定阈值 vs 动态阈值的表现：")
        print("- 固定阈值（涨停≥10）：年化394%，胜率87.95%，回撤0.60%")
        print("- 动态阈值（预计）：年化350-450%，胜率85-90%，回撤5-10%")
        print("- 预期：动态阈值能更好适应市场环境，降低极端行情损失")

        self.results["task2_dynamic_sentiment"] = {
            "status": "designed",
            "rules": {
                "aggressive": {"zt_mean": ">100", "threshold": 20, "position": "100%"},
                "normal": {"zt_mean": "50-100", "threshold": 10, "position": "100%"},
                "cautious": {"zt_mean": "30-50", "threshold": 5, "position": "50%"},
                "avoid": {"zt_mean": "<30", "threshold": 0, "position": "0%"},
            },
            "adjustment_frequency": "daily",
            "expected_improvement": "better adaptability, lower extreme loss",
        }

        return self.results["task2_dynamic_sentiment"]

    def task3_30day_simulation_validation(self):
        """
        任务3：30天模拟盘验证

        目标：
        - 验证真实滑点
        - 验证容量限制
        - 验证成交率
        - 验证实盘可行性
        """
        print("\n" + "=" * 80)
        print("任务3：30天模拟盘验证")
        print("=" * 80)

        print("\n【模拟盘配置】")
        print("\n基础配置：")
        print("- 资金规模：100万（推荐配置）")
        print("- 单票上限：5万（占成交额≤5%）")
        print("- 总仓上限：30万（30%）")
        print("- 模拟时间：30个交易日")
        print("- 平台：聚宽模拟盘 / 实盘模拟")

        print("\n【监控指标】")
        print("\n每日监控：")
        print("1. 实际买入滑点（vs预期25bps）")
        print("   - 开盘后3分钟均价 vs 开盘价")
        print("   - 统计：均值、中位数、90分位")
        print("   - 预警：>50bps暂停交易")
        print("")
        print("2. 实际卖出滑点（vs预期20bps）")
        print("   - 收盘前5分钟均价 vs 收盘价")
        print("   - 统计：均值、中位数、90分位")
        print("   - 预警：>40bps暂停交易")
        print("")
        print("3. 涨停买入失败率（vs预期5%）")
        print("   - 涨停开盘无法买入的比例")
        print("   - 预警：>10%降低仓位")
        print("")
        print("4. 跌停卖出失败率（vs预期2%）")
        print("   - 跌停无法卖出的比例")
        print("   - 预警：>5%停止策略")
        print("")
        print("5. 成交额占比（vs预期≤5%）")
        print("   - 单票买入金额 / 日均成交额")
        print("   - 预警：>10%降低单票仓位")

        print("\n【每周复盘】")
        print("1. 实际年化收益（vs预期280-320%）")
        print("2. 实际回撤（vs预期5-10%）")
        print("3. 容量利用率（vs预期≤30%）")
        print("4. 信号覆盖率（vs预期100%）")
        print("5. 参数表现偏差（vs回测）")

        print("\n【测试代码】")
        print("\n```python")
        print("class SimulationMonitor:")
        print('    """模拟盘监控"""')
        print("    ")
        print("    def __init__(self, initial_capital=1000000):")
        print("        self.capital = initial_capital")
        print("        self.position = 0")
        print("        self.daily_records = []")
        print("        self.slippage_records = []")
        print("    ")
        print(
            "    def record_trade(self, stock, action, expected_price, actual_price, volume):"
        )
        print('        """记录交易"""')
        print("        slippage = (actual_price - expected_price) / expected_price")
        print("        ")
        print("        self.slippage_records.append({")
        print("            'date': datetime.now(),")
        print("            'stock': stock,")
        print("            'action': action,  # 'buy' or 'sell'")
        print("            'expected_price': expected_price,")
        print("            'actual_price': actual_price,")
        print("            'slippage_bps': slippage * 10000,")
        print("            'volume': volume,")
        print("            'amount': actual_price * volume")
        print("        })")
        print("    ")
        print("    def calculate_stats(self):")
        print('        """计算统计指标"""')
        print(
            "        buy_slippages = [r['slippage_bps'] for r in self.slippage_records if r['action'] == 'buy']"
        )
        print(
            "        sell_slippages = [r['slippage_bps'] for r in self.slippage_records if r['action'] == 'sell']"
        )
        print("        ")
        print("        return {")
        print("            'buy_slippage_mean': np.mean(buy_slippages),")
        print("            'buy_slippage_median': np.median(buy_slippages),")
        print("            'sell_slippage_mean': np.mean(sell_slippages),")
        print("            'sell_slippage_median': np.median(sell_slippages),")
        print("            'total_trades': len(self.slippage_records)")
        print("        }")
        print("    ")
        print("    def generate_weekly_report(self, week_num):")
        print('        """生成周报"""')
        print("        stats = self.calculate_stats()")
        print("        ")
        print('        report = f"""')
        print("        # 第{week_num}周模拟盘报告")
        print("        ")
        print("        ## 交易统计")
        print("        - 总交易次数：{stats['total_trades']}")
        print("        - 买入平均滑点：{stats['buy_slippage_mean']:.2f} bps")
        print("        - 卖出平均滑点：{stats['sell_slippage_mean']:.2f} bps")
        print("        ")
        print("        ## 对比预期")
        print("        - 买入滑点预期：25 bps")
        print("        - 买入滑点实际：{stats['buy_slippage_mean']:.2f} bps")
        print("        - 偏差：{stats['buy_slippage_mean'] - 25:.2f} bps")
        print('        """')
        print("        return report")
        print("```")

        print("\n【预期结果】")
        print("- 真实滑点：买入20-30bps，卖出15-25bps")
        print("- 成交率：涨停买入失败率<10%")
        print("- 实际收益：年化250-350%")
        print("- 实际回撤：5-12%")

        print("\n【判断标准】")
        print("- ✅ Go：滑点<预期+10bps，收益>250%，回撤<15%")
        print("- ⚠️ Watch：滑点预期+10-20bps，收益150-250%，回撤15-25%")
        print("- ❌ No-Go：滑点>预期+20bps，收益<150%，回撤>25%")

        print("\n【执行方式】")
        print("1. 在聚宽平台创建模拟盘")
        print("2. 导入策略代码")
        print("3. 设置监控指标")
        print("4. 运行30天")
        print("5. 每周生成报告")
        print("6. 30天后总结")

        self.results["task3_30day_simulation"] = {
            "status": "designed",
            "config": {
                "capital": "1,000,000",
                "single_position_limit": "50,000",
                "total_position_limit": "300,000",
                "duration": "30 trading days",
            },
            "monitors": [
                "buy_slippage_bps",
                "sell_slippage_bps",
                "limit_up_fail_rate",
                "limit_down_fail_rate",
                "volume_ratio",
            ],
            "expected_results": {
                "slippage": "buy 20-30bps, sell 15-25bps",
                "return": "250-350% annualized",
                "drawdown": "5-12%",
            },
        }

        return self.results["task3_30day_simulation"]

    def generate_execution_plan(self):
        """生成执行计划"""
        print("\n" + "=" * 80)
        print("执行计划")
        print("=" * 80)

        print("\n【优先级排序】")
        print("1. ⭐⭐⭐ 任务1：2025年样本外验证（优先级最高）")
        print("   - 时间：立即执行")
        print("   - 耗时：30分钟")
        print("   - 目的：验证策略在2025年的有效性")
        print("")
        print("2. ⭐⭐ 任务2：情绪阈值动态调整（优先级高）")
        print("   - 时间：任务1完成后")
        print("   - 耗时：1小时")
        print("   - 目的：建立动态调整机制")
        print("")
        print("3. ⭐ 任务3：30天模拟盘（优先级中）")
        print("   - 时间：任务1+2完成后")
        print("   - 耗时：30天")
        print("   - 目的：验证真实滑点和容量")

        print("\n【时间表】")
        print("- 第1天：执行任务1（2025年Q1验证）")
        print("- 第2天：设计并编码任务2（动态调整机制）")
        print("- 第3天：启动任务3（30天模拟盘）")
        print("- 第4-33天：监控模拟盘，每周生成报告")
        print("- 第34天：总结三个任务结果，决定实盘方案")

        print("\n【资源需求】")
        print("- 聚宽平台账号（Notebook + 模拟盘）")
        print("- 数据：2025年Q1行情数据")
        print("- 资金：模拟盘100万（虚拟资金）")
        print("- 时间：总计约2小时 + 30天等待")

        print("\n【风险评估】")
        print("- 任务1风险：2025年Q1策略失效 → Watch/No-Go")
        print("- 任务2风险：动态调整效果不佳 → 回退固定阈值")
        print("- 任务3风险：真实滑点超预期 → 降低仓位或停止策略")

        return {
            "priority": ["task1", "task2", "task3"],
            "timeline": {
                "day1": "2025 Q1 validation",
                "day2": "Dynamic sentiment design",
                "day3": "Start 30-day simulation",
                "day4-33": "Monitor simulation",
                "day34": "Summary and decision",
            },
            "resources": {
                "platform": "JoinQuant",
                "data": "2025 Q1 market data",
                "capital": "1M virtual fund",
                "time": "2 hours + 30 days",
            },
        }

    def save_results(self, filename="task07_next_steps_results.json"):
        """保存结果"""
        output_path = f"/Users/fengzhi/Downloads/git/testlixingren/output/{filename}"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 结果已保存到：{output_path}")

        return output_path


def main():
    """主函数"""
    print("=" * 80)
    print("任务07：参数敏感性分析 - 下一步任务")
    print("=" * 80)
    print("\n基于参数敏感性分析报告V1.0的三个关键建议：")
    print("1. 继续样本外验证（2025实测）")
    print("2. 建立情绪阈值动态调整机制")
    print("3. 启动30天模拟盘验证真实滑点")

    # 创建任务实例
    tasks = ParameterSensitivityNextSteps()

    # 执行三个任务
    print("\n" + "▶" * 40)
    print("开始执行三个任务...")
    print("▶" * 40)

    # 任务1
    tasks.task1_2025_oos_validation()

    # 任务2
    tasks.task2_dynamic_sentiment_adjustment()

    # 任务3
    tasks.task3_30day_simulation_validation()

    # 生成执行计划
    tasks.generate_execution_plan()

    # 保存结果
    tasks.save_results()

    print("\n" + "=" * 80)
    print("✅ 三个任务设计方案已完成")
    print("=" * 80)
    print("\n【下一步行动】")
    print("1. 在聚宽Notebook中运行任务1测试代码")
    print("2. 根据任务1结果，调整任务2参数")
    print("3. 启动任务3模拟盘，监控30天")
    print("\n祝测试顺利！")


if __name__ == "__main__":
    main()
