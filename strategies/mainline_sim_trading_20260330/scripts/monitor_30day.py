#!/usr/bin/env python3
"""
30天监控脚本
用途：统计核心指标、生成监控报告、对比回测预期
"""

import pandas as pd
import argparse
from datetime import datetime
import os


class Monitor30Day:
    """
    30天监控器

    功能：
    - 统计交易次数、胜率、平均收益
    - 计算最大回撤、最大单笔亏损
    - 对比回测预期，判断策略有效性
    """

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.trade_file = os.path.join(self.data_dir, "trade_records.csv")
        self.pause_file = os.path.join(self.data_dir, "pause_status.csv")
        self.sentiment_file = os.path.join(self.data_dir, "sentiment_daily.csv")

    def calculate_metrics(self, day_num=None):
        """
        计算核心指标

        参数：
            day_num: 统计天数（None表示全部）

        返回：
            dict: 核心指标
        """
        # 读取交易记录
        if not os.path.exists(self.trade_file):
            print("\n⚠️  无交易记录文件")
            return None

        df = pd.read_csv(self.trade_file)

        # 筛选已卖出交易
        sold = df[df["status"] == "sold"]

        if len(sold) == 0:
            print("\n暂无已卖出交易")
            return None

        # 计算指标
        trade_count = len(sold)
        wins = sold[sold["pnl"] > 0]
        losses = sold[sold["pnl"] < 0]

        win_count = len(wins)
        loss_count = len(losses)
        win_rate = win_count / trade_count * 100

        avg_pnl = sold["pnl"].mean()
        avg_win = wins["pnl"].mean() if len(wins) > 0 else 0
        avg_loss = losses["pnl"].mean() if len(losses) > 0 else 0

        max_win = sold["pnl"].max()
        max_loss = sold["pnl"].min()

        # 计算累计收益和最大回撤
        cumulative_pnl = []
        cum_sum = 0
        for pnl in sold["pnl"]:
            cum_sum += pnl
            cumulative_pnl.append(cum_sum)

        max_cumulative = max(cumulative_pnl)
        min_cumulative = min(cumulative_pnl)
        max_drawdown = (
            max_cumulative - min_cumulative if max_cumulative > min_cumulative else 0
        )

        # 计算最大连亏
        consecutive_loss = 0
        max_consecutive_loss = 0
        for pnl in sold["pnl"]:
            if pnl < 0:
                consecutive_loss += 1
                max_consecutive_loss = max(max_consecutive_loss, consecutive_loss)
            else:
                consecutive_loss = 0

        metrics = {
            "day_num": day_num or trade_count,
            "trade_count": trade_count,
            "win_count": win_count,
            "loss_count": loss_count,
            "win_rate": win_rate,
            "avg_pnl": avg_pnl,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "max_win": max_win,
            "max_loss": max_loss,
            "cumulative_pnl": cum_sum,
            "max_drawdown": max_drawdown,
            "max_consecutive_loss": max_consecutive_loss,
        }

        return metrics

    def compare_with_backtest(self, metrics):
        """
        对比回测预期

        参数：
            metrics: 实际指标

        返回：
            dict: 对比结果
        """
        # 回测预期值（来自 result_01）
        backtest_expected = {
            "win_rate": 48.5,  # 胜率预期
            "avg_pnl": 0.77,  # 日内收益预期
            "max_drawdown": 15.0,  # 最大回撤预期
            "max_loss": -3.0,  # 最大单笔亏损预期
        }

        # 计算偏差
        deviation = {
            "win_rate": metrics["win_rate"] - backtest_expected["win_rate"],
            "avg_pnl": metrics["avg_pnl"] - backtest_expected["avg_pnl"],
            "max_drawdown": metrics["max_drawdown"] - backtest_expected["max_drawdown"],
            "max_loss": metrics["max_loss"] - backtest_expected["max_loss"],
        }

        # 判断是否达标
        is_pass = {
            "win_rate": abs(deviation["win_rate"]) <= 5.0,  # ±5%范围内
            "avg_pnl": abs(deviation["avg_pnl"]) <= 0.3,  # ±0.3%范围内
            "max_drawdown": deviation["max_drawdown"] <= 5.0,  # 回撤增加不超过5%
            "max_loss": deviation["max_loss"] >= -1.0,  # 单笔亏损不超过预期-1%
        }

        overall_pass = all(is_pass.values())

        comparison = {
            "actual": metrics,
            "expected": backtest_expected,
            "deviation": deviation,
            "is_pass": is_pass,
            "overall_pass": overall_pass,
        }

        return comparison

    def generate_report(self, day_num=None):
        """
        生成监控报告

        参数：
            day_num: 统计天数
        """
        metrics = self.calculate_metrics(day_num)

        if metrics is None:
            return

        comparison = self.compare_with_backtest(metrics)

        print(f"\n===== {day_num or '全部'} 天监控报告 =====")

        print(f"\n📊 核心指标:")
        print(f"  交易次数: {metrics['trade_count']}")
        print(f"  盈利次数: {metrics['win_count']}")
        print(f"  亏损次数: {metrics['loss_count']}")
        print(f"  胜率: {metrics['win_rate']:.1f}%")
        print(f"  平均收益: {metrics['avg_pnl']:+.2f}%")
        print(f"  平均盈利: {metrics['avg_win']:+.2f}%")
        print(f"  平均亏损: {metrics['avg_loss']:+.2f}%")
        print(f"  最大盈利: {metrics['max_win']:+.2f}%")
        print(f"  最大亏损: {metrics['max_loss']:+.2f}%")
        print(f"  累计收益: {metrics['cumulative_pnl']:+.2f}%")
        print(f"  最大回撤: {metrics['max_drawdown']:.2f}%")
        print(f"  最大连亏: {metrics['max_consecutive_loss']}笔")

        print(f"\n📈 对比回测预期:")
        print(f"  胜率:")
        print(f"    实际: {metrics['win_rate']:.1f}%")
        print(f"    预期: {comparison['expected']['win_rate']:.1f}%")
        print(f"    偏差: {comparison['deviation']['win_rate']:+.1f}%")
        print(
            f"    判断: {'✓ 达标' if comparison['is_pass']['win_rate'] else '✗ 警戒'}"
        )

        print(f"  平均收益:")
        print(f"    实际: {metrics['avg_pnl']:+.2f}%")
        print(f"    预期: {comparison['expected']['avg_pnl']:+.2f}%")
        print(f"    偏差: {comparison['deviation']['avg_pnl']:+.2f}%")
        print(f"    判断: {'✓ 达标' if comparison['is_pass']['avg_pnl'] else '✗ 警戒'}")

        print(f"  最大回撤:")
        print(f"    实际: {metrics['max_drawdown']:.2f}%")
        print(f"    预期: {comparison['expected']['max_drawdown']:.2f}%")
        print(f"    偏差: {comparison['deviation']['max_drawdown']:+.2f}%")
        print(
            f"    判断: {'✓ 达标' if comparison['is_pass']['max_drawdown'] else '✗ 警戒'}"
        )

        print(f"  最大单笔亏损:")
        print(f"    实际: {metrics['max_loss']:+.2f}%")
        print(f"    预期: {comparison['expected']['max_loss']:+.2f}%")
        print(f"    偏差: {comparison['deviation']['max_loss']:+.2f}%")
        print(
            f"    判断: {'✓ 达标' if comparison['is_pass']['max_loss'] else '✗ 警戒'}"
        )

        print(f"\n🎯 总体判断:")
        if comparison["overall_pass"]:
            print(f"  ✓ 策略表现达标")
            print(f"  建议: 继续执行，观察后续表现")
        else:
            print(f"  ✗ 策略表现警戒")
            print(f"  建议: 复盘检查，暂停交易")

        return comparison

    def check_pause_triggers(self):
        """
        检查停手触发情况
        """
        if not os.path.exists(self.pause_file):
            print("\n无停手记录")
            return

        df = pd.read_csv(self.pause_file)

        triggers = df[df["备注"].str.contains("触发停手", na=False)]

        print(f"\n===== 停手触发检查 =====")
        print(f"停手触发次数: {len(triggers)}次")

        if len(triggers) > 0:
            print(f"\n触发详情:")
            for idx, row in triggers.iterrows():
                print(f"  {row['date']}: 连亏{row['consecutive_loss']}笔")

    def check_sentiment_accuracy(self):
        """
        检查情绪开关准确率
        """
        if not os.path.exists(self.sentiment_file):
            print("\n无情绪数据")
            return

        sentiment_df = pd.read_csv(self.sentiment_file)

        # 统计情绪判断
        allow_buy_count = len(sentiment_df[sentiment_df["allow_buy"] == True])
        total_count = len(sentiment_df)

        print(f"\n===== 情绪开关准确率 =====")
        print(f"统计天数: {total_count}")
        print(f"开仓天数: {allow_buy_count}")
        print(f"空仓天数: {total_count - allow_buy_count}")
        print(f"开仓比例: {allow_buy_count / total_count * 100:.1f}%")

        # 分析情绪分布
        zt_counts = sentiment_df["zt_count"]
        print(f"\n涨停家数分布:")
        print(f"  最大: {zt_counts.max()}")
        print(f"  最小: {zt_counts.min()}")
        print(f"  平均: {zt_counts.mean():.1f}")

    def save_30day_report(self, output_file=None):
        """
        保存30天报告

        参数：
            output_file: 输出文件路径
        """
        if output_file is None:
            output_file = os.path.join(self.data_dir, "..", "docs", "30day_report.md")

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        metrics = self.calculate_metrics(30)
        if metrics is None:
            return

        comparison = self.compare_with_backtest(metrics)

        # 生成报告内容
        report_content = f"""# 30天模拟盘报告

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> 统计周期: 前30天

---

## 一、核心指标

| 指标 | 实际值 | 回测预期 | 偏差 | 判断 |
|------|--------|----------|------|------|
| 交易次数 | {metrics["trade_count"]} | ≥15 | - | - |
| 胜率 | {metrics["win_rate"]:.1f}% | 48.5% | {comparison["deviation"]["win_rate"]:+.1f}% | {"达标" if comparison["is_pass"]["win_rate"] else "警戒"} |
| 平均收益 | {metrics["avg_pnl"]:+.2f}% | +0.77% | {comparison["deviation"]["avg_pnl"]:+.2f}% | {"达标" if comparison["is_pass"]["avg_pnl"] else "警戒"} |
| 最大回撤 | {metrics["max_drawdown"]:.2f}% | 15.0% | {comparison["deviation"]["max_drawdown"]:+.2f}% | {"达标" if comparison["is_pass"]["max_drawdown"] else "警戒"} |
| 最大单笔亏损 | {metrics["max_loss"]:+.2f}% | -3.0% | {comparison["deviation"]["max_loss"]:+.2f}% | {"达标" if comparison["is_pass"]["max_loss"] else "警戒"} |

---

## 二、总体判断

**{"✓ 策略表现达标" if comparison["overall_pass"] else "✗ 策略表现警戒"}**

---

## 三、建议

{"- 继续执行模拟盘\n- 观察后续表现\n- 准备小实盘申请" if comparison["overall_pass"] else "- 暂停交易\n- 复盘检查异常交易\n- 重新验证策略有效性"}

---

**报告生成时间**: {datetime.now().strftime("%Y-%m-%d")}
"""

        with open(output_file, "w") as f:
            f.write(report_content)

        print(f"\n✓ 30天报告已保存至: {output_file}")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="30天监控脚本")
    parser.add_argument("--day", type=int, help="统计天数")
    parser.add_argument("--report", action="store_true", help="生成报告")
    parser.add_argument("--pause", action="store_true", help="检查停手触发")
    parser.add_argument("--sentiment", action="store_true", help="检查情绪准确率")

    args = parser.parse_args()

    monitor = Monitor30Day()

    if args.report:
        monitor.save_30day_report()
    elif args.pause:
        monitor.check_pause_triggers()
    elif args.sentiment:
        monitor.check_sentiment_accuracy()
    else:
        monitor.generate_report(args.day)


if __name__ == "__main__":
    main()
