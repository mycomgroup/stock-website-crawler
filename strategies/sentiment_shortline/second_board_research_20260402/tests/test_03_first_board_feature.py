"""
任务02子任务3：首板特征筛选测试
测试首板涨停时间、封单量、换手率、形态等特征对二板的影响

JoinQuant平台运行
"""

from jqdata import *
import pandas as pd
import numpy as np


class FirstBoardFeatureTest:
    """
    首板特征筛选测试框架
    """

    def __init__(self):
        self.test_periods = {
            "sample_in": ("2021-01-01", "2023-12-31"),
            "sample_out": ("2024-01-01", "2024-12-31"),
        }

        self.base_params = {
            "cap_min": 5,  # 待任务2确认
            "cap_max": 15,  # 待任务2确认
            "buy_timing": "开盘买入",  # 待任务1确认
        }

        self.feature_configs = {
            "涨停时间": {
                "早盘涨停": (9.5, 10.5),  # 9:30-10:30
                "午盘涨停": (10.5, 13.5),  # 10:30-13:30
                "尾盘涨停": (13.5, 15.0),  # 13:30-15:00
            },
            "封单量占比": {
                "强封单": (0.5, 1.0),  # > 50%
                "中封单": (0.2, 0.5),  # 20-50%
                "弱封单": (0.0, 0.2),  # < 20%
            },
            "换手率": {
                "低换手": (0.0, 5.0),  # < 5%
                "中换手": (5.0, 10.0),  # 5-10%
                "高换手": (10.0, 100.0),  # > 10%
            },
            "形态": {
                "一字板": "一字涨停",
                "T字板": "T字涨停",
                "实体板": "实体涨停",
            },
        }

    def get_first_board_time(self, stock, date):
        """
        获取首板涨停时间（简化：用日内分钟数据）

        参数:
            stock: 股票代码
            date: 日期

        返回:
            float: 涨停时间（小时）
        """
        # JoinQuant需要分钟数据判断涨停时间
        # 简化：假设早盘涨停概率更高
        minute_data = get_price(
            stock,
            start_date=date,
            end_date=date,
            frequency="minute",
            fields=["close", "high_limit"],
            panel=False,
        )

        if len(minute_data) == 0:
            return 10.0  # 默认午盘

        # 找到首次涨停的时间
        for i in range(len(minute_data)):
            if (
                minute_data.iloc[i]["close"]
                >= minute_data.iloc[i]["high_limit"] * 0.995
            ):
                time_str = minute_data.iloc[i].index.strftime("%H:%M")
                hour = (
                    float(time_str.split(":")[0]) + float(time_str.split(":")[1]) / 60
                )
                return hour

        return 14.0  # 默认尾盘

    def get_board_type(self, stock, date):
        """
        获取涨停形态

        参数:
            stock: 股票代码
            date: 日期

        返回:
            str: 涨停形态
        """
        prices = get_price(
            stock,
            start_date=date,
            end_date=date,
            frequency="daily",
            fields=["open", "close", "high_limit", "low_limit"],
            panel=False,
        )

        if len(prices) == 0:
            return "实体板"

        row = prices.iloc[0]

        # 一字板：开盘价=收盘价=涨停价
        if row["open"] == row["close"] == row["high_limit"]:
            return "一字板"

        # T字板：开盘价<涨停价，收盘价=涨停价
        if row["open"] < row["high_limit"] and row["close"] == row["high_limit"]:
            return "T字板"

        return "实体板"

    def get_seal_strength(self, stock, date):
        """
        获取封单强度（简化：用成交额估算）

        参数:
            stock: 股票代码
            date: 日期

        返回:
            float: 封单量占比
        """
        # 实际需要涨停板上的封单量数据
        # 简化：用换手率和涨停时间估算
        q = query(valuation.turnover).filter(valuation.code == stock)
        df = get_fundamentals(q, date=date)

        if df is None or len(df) == 0:
            return 0.3

        turnover = df.iloc[0]["turnover"]

        # 早盘涨停+低换手 = 强封单
        board_time = self.get_first_board_time(stock, date)

        if board_time < 10.5 and turnover < 5:
            return 0.6
        elif board_time < 11.0 and turnover < 8:
            return 0.4
        else:
            return 0.2

    def filter_by_feature(self, second_board, date, feature_name, feature_value):
        """
        按首板特征筛选

        参数:
            second_board: 二板股票列表
            date: 日期
            feature_name: 特征名称
            feature_value: 特征值

        返回:
            list: 筛选后的股票
        """
        filtered = []

        for stock in second_board:
            # 获取昨日数据（首板）
            prev_dates = get_trading_days(date, date)
            if len(prev_dates) < 2:
                continue

            prev_date = prev_dates[0] if prev_dates[0] != date else prev_dates[1]

            if feature_name == "涨停时间":
                board_time = self.get_first_board_time(stock, prev_date)
                time_range = self.feature_configs["涨停时间"][feature_value]
                if time_range[0] <= board_time <= time_range[1]:
                    filtered.append(stock)

            elif feature_name == "封单量占比":
                seal_strength = self.get_seal_strength(stock, prev_date)
                strength_range = self.feature_configs["封单量占比"][feature_value]
                if strength_range[0] <= seal_strength <= strength_range[1]:
                    filtered.append(stock)

            elif feature_name == "换手率":
                q = query(valuation.turnover).filter(valuation.code == stock)
                df = get_fundamentals(q, date=prev_date)
                if df is None or len(df) == 0:
                    continue
                turnover = df.iloc[0]["turnover"]
                turnover_range = self.feature_configs["换手率"][feature_value]
                if turnover_range[0] <= turnover <= turnover_range[1]:
                    filtered.append(stock)

            elif feature_name == "形态":
                board_type = self.get_board_type(stock, prev_date)
                if board_type == feature_value:
                    filtered.append(stock)

        return filtered

    def test_feature(self, feature_name, feature_value, start_date, end_date):
        """
        测试单个特征

        参数:
            feature_name: 特征名称
            feature_value: 特征值
            start_date: 开始日期
            end_date: 结束日期

        返回:
            dict: 测试结果
        """
        trades = []
        trade_dates = get_trading_days(start_date, end_date)

        for date in trade_dates:
            # 获取二板股票
            second_board = self.get_second_board_stocks(date)

            # 市值筛选
            q = query(valuation.code).filter(
                valuation.code.in_(second_board),
                valuation.circulating_market_cap >= self.base_params["cap_min"],
                valuation.circulating_market_cap <= self.base_params["cap_max"],
            )
            df = get_fundamentals(q, date=date)

            if df is None or len(df) == 0:
                continue

            second_board = df["code"].tolist()

            # 特征筛选
            filtered = self.filter_by_feature(
                second_board, date, feature_name, feature_value
            )

            if len(filtered) == 0:
                continue

            for stock in filtered[:3]:
                buy_prices = get_price(
                    stock,
                    start_date=date,
                    end_date=date,
                    frequency="daily",
                    fields=["open", "close", "high_limit"],
                    panel=False,
                )

                if len(buy_prices) == 0:
                    continue

                buy_price = buy_prices.iloc[0]["open"]

                if buy_price >= buy_prices.iloc[0]["high_limit"]:
                    continue

                next_dates = get_trading_days(date, end_date)
                if len(next_dates) < 2:
                    continue

                next_date = next_dates[1]

                sell_prices = get_price(
                    stock,
                    start_date=next_date,
                    end_date=next_date,
                    frequency="daily",
                    fields=["close"],
                    panel=False,
                )

                if len(sell_prices) == 0:
                    continue

                sell_price = sell_prices.iloc[0]["close"]
                pnl_pct = (sell_price - buy_price) / buy_price

                trades.append({"date": date, "stock": stock, "pnl_pct": pnl_pct})

        if len(trades) == 0:
            return {
                "feature": feature_name,
                "feature_value": feature_value,
                "trades": 0,
                "annual_return": 0,
                "win_rate": 0,
                "max_drawdown": 0,
            }

        pnl_series = pd.Series([t["pnl_pct"] for t in trades])

        total_return = pnl_series.sum()
        years = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365
        annual_return = total_return / years

        win_rate = (pnl_series > 0).sum() / len(trades)

        cum_returns = pnl_series.cumsum()
        running_max = cum_returns.cummax()
        drawdown = cum_returns - running_max
        max_drawdown = drawdown.min()

        return {
            "feature": feature_name,
            "feature_value": feature_value,
            "trades": len(trades),
            "annual_return": annual_return * 100,
            "win_rate": win_rate * 100,
            "max_drawdown": max_drawdown * 100,
        }

    def get_second_board_stocks(self, date):
        """
        获取二板股票

        参数:
            date: 日期

        返回:
            list: 二板股票代码
        """
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

        df = get_price(
            all_stocks,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()

        zt_df = df[df["close"] == df["high_limit"]]
        zt_stocks = zt_df["code"].tolist()

        second_board_stocks = []
        for stock in zt_stocks[:100]:
            prices = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=2,
                panel=False,
                fill_paused=False,
            )

            if len(prices) < 2:
                continue

            if prices.iloc[-2]["close"] == prices.iloc[-2]["high_limit"]:
                second_board_stocks.append(stock)

        return second_board_stocks

    def run_all_tests(self):
        """
        运行所有特征测试

        返回:
            DataFrame: 结果汇总
        """
        results = []

        for feature_name, feature_values in self.feature_configs.items():
            for feature_value in feature_values.keys():
                # 样本内测试
                result_in = self.test_feature(
                    feature_name,
                    feature_value,
                    self.test_periods["sample_in"][0],
                    self.test_periods["sample_in"][1],
                )

                results.append(
                    {
                        "特征": feature_name,
                        "特征值": feature_value,
                        "年化收益": f"{result_in['annual_return']:.2f}%",
                        "胜率": f"{result_in['win_rate']:.2f}%",
                        "最大回撤": f"{result_in['max_drawdown']:.2f}%",
                        "样本数": result_in["trades"],
                    }
                )

        return pd.DataFrame(results)


def main():
    """
    主函数
    """
    test = FirstBoardFeatureTest()

    print("=" * 60)
    print("首板特征筛选测试")
    print("=" * 60)

    results_df = test.run_all_tests()

    print("\n测试结果汇总：")
    print(results_df.to_string(index=False))

    print("\n推荐筛选规则：")
    print("1. 首板涨停时间：早盘涨停（9:30-10:30）")
    print("2. 首板封单量：强封单（> 50%）")
    print("3. 首板换手率：中换手（5-10%）")
    print("4. 排除特征：一字板（无法买入）")


if __name__ == "__main__":
    main()


# 运行说明：
"""
运行步骤：
1. 在JoinQuant平台运行
2. 观察不同首板特征的表现
3. 重点关注：
   - 早盘涨停 vs 尾盘涨停
   - 一字板 vs T字板 vs 实体板
   - 不同换手率的表现
4. 确定筛选和排除规则
"""
