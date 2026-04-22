#!/usr/bin/env python3
"""
实盘执行脚本
用途：记录买入、卖出、管理持仓
"""

import pandas as pd
import argparse
from datetime import datetime
import os


class TradeExecutor:
    """
    交易执行器
    """

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.trade_file = os.path.join(self.data_dir, "trade_records.csv")
        os.makedirs(self.data_dir, exist_ok=True)

        # 初始化交易记录
        self.init_trade_records()

    def init_trade_records(self):
        """
        初始化交易记录CSV
        """
        if not os.path.exists(self.trade_file):
            df = pd.DataFrame(
                columns=[
                    "trade_id",
                    "stock_code",
                    "stock_name",
                    "buy_date",
                    "buy_price",
                    "buy_time",
                    "sell_date",
                    "sell_price",
                    "sell_time",
                    "pnl",
                    "holding_days",
                    "status",
                    "备注",
                ]
            )
            df.to_csv(self.trade_file, index=False)
            print(f"交易记录文件已创建: {self.trade_file}")

    def buy(self, date, stock_code, stock_name, price, time="09:35", 备注=""):
        """
        记录买入

        参数：
            date: 日期
            stock_code: 股票代码
            stock_name: 股票名称
            price: 买入价格
            time: 买入时间
            备注: 备注
        """
        df = pd.read_csv(self.trade_file)

        # 生成交易编号
        trade_id = f"T{date.replace('-', '')}{len(df) + 1:03d}"

        # 添加买入记录
        new_row = {
            "trade_id": trade_id,
            "stock_code": stock_code,
            "stock_name": stock_name,
            "buy_date": date,
            "buy_price": price,
            "buy_time": time,
            "sell_date": "",
            "sell_price": "",
            "sell_time": "",
            "pnl": "",
            "holding_days": 0,
            "status": "holding",
            "备注": 备注,
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.trade_file, index=False)

        print(f"\n✓ 买入记录已保存")
        print(f"  交易编号: {trade_id}")
        print(f"  股票: {stock_code} {stock_name}")
        print(f"  价格: {price}")
        print(f"  时间: {time}")
        print(f"  状态: 持有中")

    def sell(self, date, stock_code, price, time="09:35", 备注=""):
        """
        记录卖出

        参数：
            date: 卖出日期
            stock_code: 股票代码
            price: 卖出价格
            time: 卖出时间
            备注: 备注
        """
        df = pd.read_csv(self.trade_file)

        # 查找持有中的股票
        holding = df[(df["stock_code"] == stock_code) & (df["status"] == "holding")]

        if len(holding) == 0:
            print(f"\n⚠️  未找到持有中的股票: {stock_code}")
            return None

        # 取第一条持有记录
        idx = holding.index[0]
        buy_price = float(df.loc[idx, "buy_price"])
        buy_date = df.loc[idx, "buy_date"]

        # 计算盈亏
        pnl = round((price - buy_price) / buy_price * 100, 2)

        # 计算持有天数
        buy_dt = datetime.strptime(buy_date, "%Y-%m-%d")
        sell_dt = datetime.strptime(date, "%Y-%m-%d")
        holding_days = (sell_dt - buy_dt).days

        # 更新记录
        df.loc[idx, "sell_date"] = date
        df.loc[idx, "sell_price"] = price
        df.loc[idx, "sell_time"] = time
        df.loc[idx, "pnl"] = pnl
        df.loc[idx, "holding_days"] = holding_days
        df.loc[idx, "status"] = "sold"
        df.loc[idx, "备注"] = 备注

        df.to_csv(self.trade_file, index=False)

        print(f"\n✓ 卖出记录已保存")
        print(f"  股票: {stock_code}")
        print(f"  买入价: {buy_price}")
        print(f"  卖出价: {price}")
        print(f"  盈亏: {pnl:+.2f}%")
        print(f"  持有天数: {holding_days}")
        print(f"  状态: 已卖出")

        return pnl

    def get_holding_stocks(self):
        """
        获取当前持有股票列表

        返回：
            list: 持有股票列表
        """
        df = pd.read_csv(self.trade_file)
        holding = df[df["status"] == "holding"]

        if len(holding) == 0:
            print("\n当前无持有股票")
            return []

        print(f"\n当前持有股票:")
        for idx, row in holding.iterrows():
            print(f"  {row['stock_code']} {row['stock_name']}")
            print(f"    买入日期: {row['buy_date']}")
            print(f"    买入价格: {row['buy_price']}")
            print(f"    持有天数: {row['holding_days']}")

        return holding.to_dict("records")

    def check_buy_signal(self, open_pct):
        """
        检查买入信号

        参数：
            open_pct: 开盘涨跌幅（百分比）

        返回：
            bool: 是否符合假弱高开
        """
        # 假弱高开：+0.5%~+1.5%
        if 0.5 <= open_pct <= 1.5:
            return True, "假弱高开（+0.5%~+1.5%）"
        else:
            return False, f"开盘涨幅{open_pct:+.2f}%，不符合假弱高开"

    def show_summary(self):
        """
        显示交易总结
        """
        df = pd.read_csv(self.trade_file)

        sold = df[df["status"] == "sold"]
        holding = df[df["status"] == "holding"]

        print(f"\n===== 交易总结 =====")
        print(f"总交易数: {len(df)}")
        print(f"已卖出: {len(sold)}")
        print(f"持有中: {len(holding)}")

        if len(sold) > 0:
            wins = sold[sold["pnl"] > 0]
            losses = sold[sold["pnl"] < 0]

            win_rate = len(wins) / len(sold) * 100
            avg_pnl = sold["pnl"].mean()
            max_win = sold["pnl"].max()
            max_loss = sold["pnl"].min()

            print(f"\n已交易统计:")
            print(f"  胜率: {win_rate:.1f}%")
            print(f"  平均收益: {avg_pnl:+.2f}%")
            print(f"  最大盈利: {max_win:+.2f}%")
            print(f"  最大亏损: {max_loss:+.2f}%")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="实盘执行脚本")
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=["buy", "sell", "holding", "summary"],
        help="执行模式",
    )
    parser.add_argument("--date", type=str, help="日期，格式 YYYY-MM-DD")
    parser.add_argument("--stock", type=str, help="股票代码")
    parser.add_argument("--name", type=str, help="股票名称")
    parser.add_argument("--price", type=float, help="价格")
    parser.add_argument("--time", type=str, default="09:35", help="时间")
    parser.add_argument("--open-pct", type=float, help="开盘涨跌幅（买入前检查）")
    parser.add_argument("--备注", type=str, default="", help="备注")

    args = parser.parse_args()

    executor = TradeExecutor()

    if args.mode == "buy":
        # 检查开盘涨幅
        if args.open_pct:
            is_signal, reason = executor.check_buy_signal(args.open_pct)
            if not is_signal:
                print(f"\n⚠️  {reason}")
                print(f"  不建议买入")
                return

        # 执行买入
        if args.stock and args.price:
            executor.buy(
                date=args.date,
                stock_code=args.stock,
                stock_name=args.name or args.stock,
                price=args.price,
                time=args.time,
                备注=args.备注,
            )
        else:
            print("\n⚠️  请提供股票代码和价格")
            print(
                "示例: python execute_trade.py --mode buy --date 2026-04-01 --stock 000001 --name 平安银行 --price 12.50"
            )

    elif args.mode == "sell":
        if args.stock and args.price:
            pnl = executor.sell(
                date=args.date,
                stock_code=args.stock,
                price=args.price,
                time=args.time,
                备注=args.备注,
            )
        else:
            print("\n⚠️  请提供股票代码和价格")
            print(
                "示例: python execute_trade.py --mode sell --date 2026-04-02 --stock 000001 --price 12.60"
            )

    elif args.mode == "holding":
        executor.get_holding_stocks()

    elif args.mode == "summary":
        executor.show_summary()


if __name__ == "__main__":
    main()
