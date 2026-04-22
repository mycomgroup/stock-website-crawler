#!/usr/bin/env python3
"""
停手机制管理脚本
用途：记录连亏次数、管理停手天数、判断是否可交易
"""

import pandas as pd
import argparse
from datetime import datetime, timedelta
import os


class PauseManager:
    """
    停手机制管理器

    规则：
    - 连亏3笔 → 停手3天
    - 停手期间不交易
    - 3天后自动恢复
    """

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.pause_file = os.path.join(self.data_dir, "pause_status.csv")
        self.trade_file = os.path.join(self.data_dir, "trade_records.csv")
        os.makedirs(self.data_dir, exist_ok=True)

        # 初始化停手状态
        self.init_pause_status()

    def init_pause_status(self):
        """
        初始化停手状态CSV
        """
        if not os.path.exists(self.pause_file):
            df = pd.DataFrame(
                columns=[
                    "date",
                    "trade_count",
                    "win_count",
                    "loss_count",
                    "consecutive_loss",
                    "pause_days",
                    "can_trade",
                    "备注",
                ]
            )
            df.to_csv(self.pause_file, index=False)
            print(f"停手状态文件已创建: {self.pause_file}")

    def record_trade(self, date, pnl):
        """
        记录交易结果，更新连亏计数

        参数：
            date: 日期
            pnl: 盈亏比例（正数为盈利，负数为亏损）

        返回：
            dict: 更新后的状态
        """
        df = pd.read_csv(self.pause_file)

        # 获取上一日状态（如果存在）
        if len(df) > 0:
            prev_row = df.iloc[-1]
            prev_consecutive_loss = int(prev_row["consecutive_loss"])
            prev_pause_days = int(prev_row["pause_days"])
        else:
            prev_consecutive_loss = 0
            prev_pause_days = 0

        # 更新连亏计数
        if pnl < 0:
            consecutive_loss = prev_consecutive_loss + 1
        else:
            consecutive_loss = 0

        # 判断是否触发停手
        if consecutive_loss >= 3 and prev_pause_days == 0:
            pause_days = 3
            备注 = f"连亏{consecutive_loss}笔，触发停手3天"
        elif prev_pause_days > 0:
            # 停手期间，天数递减
            pause_days = prev_pause_days - 1
            consecutive_loss = prev_consecutive_loss  # 保持连亏计数
            备注 = f"停手第{3 - pause_days}天"
        else:
            pause_days = 0
            备注 = "可交易"

        # 判断是否可交易
        can_trade = pause_days == 0

        # 统计总交易数
        trade_count = len(df) + 1
        win_count = len(df[df["备注"].str.contains("盈利", na=False)]) + (
            1 if pnl > 0 else 0
        )
        loss_count = len(df[df["备注"].str.contains("亏损", na=False)]) + (
            1 if pnl < 0 else 0
        )

        # 添加新记录
        new_row = {
            "date": date,
            "trade_count": trade_count,
            "win_count": win_count,
            "loss_count": loss_count,
            "consecutive_loss": consecutive_loss,
            "pause_days": pause_days,
            "can_trade": can_trade,
            "备注": 备注,
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.pause_file, index=False)

        print(f"\n✓ 交易结果已记录")
        print(f"  盈亏: {pnl:+.2f}%")
        print(f"  连亏次数: {consecutive_loss}")
        print(f"  停手天数: {pause_days}")
        print(f"  是否可交易: {'✓ 是' if can_trade else '✗ 否'}")

        if pause_days > 0:
            print(f"\n⚠️  触发停手机制！")
            print(f"  原因: {备注}")
            print(f"  建议: 强制休息，不交易")

        return new_row

    def check_can_trade(self):
        """
        检查是否可交易

        返回：
            bool: 是否可交易
            dict: 当前状态
        """
        df = pd.read_csv(self.pause_file)

        if len(df) == 0:
            print("\n✓ 可交易")
            print("  状态: 初次交易")
            return True, {}

        # 获取最新状态
        latest = df.iloc[-1]

        can_trade = latest["can_trade"]
        consecutive_loss = int(latest["consecutive_loss"])
        pause_days = int(latest["pause_days"])

        print(f"\n===== 今日交易状态检查 =====")
        print(f"  总交易数: {latest['trade_count']}")
        print(
            f"  胜率: {int(latest['win_count']) / int(latest['trade_count']) * 100:.1f}%"
        )
        print(f"  连亏次数: {consecutive_loss}")
        print(f"  停手天数: {pause_days}")

        if can_trade:
            print(f"\n✓ 今日可交易")
            print(f"  建议: 检查情绪开关，筛选假弱高开股票")
        else:
            print(f"\n✗ 今日不可交易")
            print(f"  原因: {latest['备注']}")
            print(f"  建议: 强制休息{pause_days}天")

        return bool(can_trade), latest.to_dict()

    def update_pause_days(self):
        """
        每日更新：减少停手天数

        用途：每天收盘后调用，递减停手天数
        """
        df = pd.read_csv(self.pause_file)

        if len(df) == 0:
            print("\n无停手状态")
            return

        latest = df.iloc[-1]
        pause_days = int(latest["pause_days"])

        if pause_days > 0:
            # 递减停手天数
            new_pause_days = pause_days - 1

            # 更新最新记录
            df.loc[df.index[-1], "pause_days"] = new_pause_days
            df.loc[df.index[-1], "can_trade"] = new_pause_days == 0

            if new_pause_days == 0:
                df.loc[df.index[-1], "备注"] = "停手结束，恢复交易"
                print(f"\n✓ 停手结束")
                print(f"  明日可恢复交易")
            else:
                df.loc[df.index[-1], "备注"] = f"停手第{3 - new_pause_days}天"
                print(f"\n停手天数更新: {pause_days} → {new_pause_days}")
                print(f"  还需休息{new_pause_days}天")

            df.to_csv(self.pause_file, index=False)
        else:
            print(f"\n当前非停手状态，无需更新")

    def get_statistics(self):
        """
        获取统计数据

        返回：
            dict: 统计数据
        """
        df = pd.read_csv(self.pause_file)

        if len(df) == 0:
            print("\n暂无交易数据")
            return None

        # 计算统计指标
        trade_count = int(df.iloc[-1]["trade_count"])
        win_count = int(df.iloc[-1]["win_count"])
        loss_count = int(df.iloc[-1]["loss_count"])

        win_rate = win_count / trade_count * 100 if trade_count > 0 else 0

        # 最大连亏
        max_consecutive_loss = df["consecutive_loss"].max()

        # 停手触发次数
        pause_triggers = len(df[df["备注"].str.contains("触发停手", na=False)])

        stats = {
            "trade_count": trade_count,
            "win_count": win_count,
            "loss_count": loss_count,
            "win_rate": win_rate,
            "max_consecutive_loss": max_consecutive_loss,
            "pause_triggers": pause_triggers,
        }

        print(f"\n===== 停手机制统计 =====")
        print(f"总交易数: {trade_count}")
        print(f"盈利: {win_count}笔")
        print(f"亏损: {loss_count}笔")
        print(f"胜率: {win_rate:.1f}%")
        print(f"最大连亏: {max_consecutive_loss}笔")
        print(f"停手触发次数: {pause_triggers}次")

        return stats


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="停手机制管理脚本")
    parser.add_argument(
        "--action",
        type=str,
        required=True,
        choices=["record", "check", "update", "stats"],
        help="执行动作",
    )
    parser.add_argument("--date", type=str, help="日期，格式 YYYY-MM-DD")
    parser.add_argument("--pnl", type=float, help="盈亏比例（正数为盈利，负数为亏损）")

    args = parser.parse_args()

    manager = PauseManager()

    if args.action == "record":
        if args.date and args.pnl:
            manager.record_trade(args.date, args.pnl)
        else:
            print("\n⚠️  请提供日期和盈亏比例")
            print(
                "示例: python pause_manager.py --action record --date 2026-04-02 --pnl -2.5"
            )

    elif args.action == "check":
        manager.check_can_trade()

    elif args.action == "update":
        manager.update_pause_days()

    elif args.action == "stats":
        manager.get_statistics()


if __name__ == "__main__":
    main()
