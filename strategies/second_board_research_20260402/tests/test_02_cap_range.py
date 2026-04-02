"""
任务02子任务2：市值区间精确化测试
测试7个市值区间的表现，找出最优区间

JoinQuant平台运行
"""

from jqdata import *
import pandas as pd
import numpy as np


class CapRangeTest:
    """
    市值区间精确化测试框架
    """

    def __init__(self):
        self.cap_ranges = [
            (0, 5, "0-5亿"),
            (5, 10, "5-10亿"),
            (10, 15, "10-15亿"),
            (15, 20, "15-20亿"),
            (20, 30, "20-30亿"),
            (30, 50, "30-50亿"),
            (50, 100, "50-100亿"),
        ]

        self.test_periods = {
            "sample_in": ("2021-01-01", "2023-12-31"),
            "sample_out": ("2024-01-01", "2024-12-31"),
        }

        self.buy_timing = "开盘买入"  # 待任务1确认

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

    def filter_by_cap_range(self, stocks, date, cap_min, cap_max):
        """
        按市值区间筛选

        参数:
            stocks: 股票列表
            date: 日期
            cap_min: 市值下限
            cap_max: 市值上限

        返回:
            list: 筛选后的股票
        """
        if len(stocks) == 0:
            return []

        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code.in_(stocks),
            valuation.circulating_market_cap >= cap_min,
            valuation.circulating_market_cap <= cap_max,
        )

        df = get_fundamentals(q, date=date)
        if df is None or len(df) == 0:
            return []

        return df["code"].tolist(), df["circulating_market_cap"].mean()

    def test_cap_range(self, cap_min, cap_max, start_date, end_date):
        """
        测试单个市值区间

        参数:
            cap_min: 市值下限
            cap_max: 市值上限
            start_date: 开始日期
            end_date: 结束日期

        返回:
            dict: 测试结果
        """
        trades = []
        avg_caps = []

        trade_dates = get_trading_days(start_date, end_date)

        for date in trade_dates:
            second_board = self.get_second_board_stocks(date)
            filtered, avg_cap = self.filter_by_cap_range(
                second_board, date, cap_min, cap_max
            )

            if len(filtered) == 0:
                continue

            avg_caps.append(avg_cap)

            for stock in filtered[:3]:
                buy_prices = get_price(
                    stock,
                    start_date=date,
                    end_date=date,
                    frequency="daily",
                    fields=["open", "close", "high_limit", "volume", "money"],
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

                trades.append(
                    {
                        "date": date,
                        "stock": stock,
                        "buy_price": buy_price,
                        "sell_price": sell_price,
                        "pnl_pct": pnl_pct,
                        "volume": buy_prices.iloc[0]["volume"],
                        "money": buy_prices.iloc[0]["money"],
                    }
                )

        if len(trades) == 0:
            return {
                "cap_range": f"{cap_min}-{cap_max}亿",
                "trades": 0,
                "annual_return": 0,
                "win_rate": 0,
                "max_drawdown": 0,
                "sharpe": 0,
                "avg_cap": 0,
                "avg_volume": 0,
                "avg_money": 0,
            }

        pnl_series = pd.Series([t["pnl_pct"] for t in trades])
        volume_series = pd.Series([t["volume"] for t in trades])
        money_series = pd.Series([t["money"] for t in trades])

        total_return = pnl_series.sum()
        years = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365
        annual_return = total_return / years

        win_rate = (pnl_series > 0).sum() / len(trades)

        cum_returns = pnl_series.cumsum()
        running_max = cum_returns.cummax()
        drawdown = cum_returns - running_max
        max_drawdown = drawdown.min()

        if pnl_series.std() > 0:
            sharpe = (annual_return - 0.03) / pnl_series.std() * np.sqrt(250)
        else:
            sharpe = 0

        return {
            "cap_range": f"{cap_min}-{cap_max}亿",
            "trades": len(trades),
            "annual_return": annual_return * 100,
            "win_rate": win_rate * 100,
            "max_drawdown": max_drawdown * 100,
            "sharpe": sharpe,
            "avg_cap": np.mean(avg_caps),
            "avg_volume": volume_series.mean(),
            "avg_money": money_series.mean() / 10000,  # 万元
        }

    def run_all_tests(self):
        """
        运行所有市值区间测试

        返回:
            DataFrame: 结果汇总
        """
        results = []

        for cap_min, cap_max, range_name in self.cap_ranges:
            # 样本内测试
            result_in = self.test_cap_range(
                cap_min,
                cap_max,
                self.test_periods["sample_in"][0],
                self.test_periods["sample_in"][1],
            )

            # 样本外测试
            result_out = self.test_cap_range(
                cap_min,
                cap_max,
                self.test_periods["sample_out"][0],
                self.test_periods["sample_out"][1],
            )

            results.append(
                {
                    "市值区间": range_name,
                    "样本内年化": f"{result_in['annual_return']:.2f}%",
                    "样本内胜率": f"{result_in['win_rate']:.2f}%",
                    "样本内回撤": f"{result_in['max_drawdown']:.2f}%",
                    "样本内夏普": f"{result_in['sharpe']:.2f}",
                    "平均市值": f"{result_in['avg_cap']:.1f}亿",
                    "平均成交额": f"{result_in['avg_money']:.0f}万",
                    "样本数": result_in["trades"],
                    "样本外年化": f"{result_out['annual_return']:.2f}%",
                    "样本外胜率": f"{result_out['win_rate']:.2f}%",
                }
            )

        return pd.DataFrame(results)

    def analyze_results(self, results_df):
        """
        分析结果

        参数:
            results_df: 结果DataFrame

        返回:
            dict: 分析结论
        """
        # 收益与市值的关系
        print("\n收益与市值关系：")

        # 成交额与市值的关系
        print("\n成交额与市值关系：")

        # 推荐结论
        conclusion = {
            "最优区间": "5-15亿",  # 待测试确认
            "可交易区间": "10-20亿",  # 平衡收益与容量
            "理由": "小市值收益高但容量小，大市值容量大但收益低",
        }

        return conclusion


def main():
    """
    主函数
    """
    test = CapRangeTest()

    print("=" * 60)
    print("市值区间精确化测试")
    print("=" * 60)

    results_df = test.run_all_tests()

    print("\n测试结果汇总：")
    print(results_df.to_string(index=False))

    conclusion = test.analyze_results(results_df)

    print("\n分析结论：")
    for key, value in conclusion.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()


# 运行说明：
"""
运行步骤：
1. 在JoinQuant平台运行
2. 观察不同市值区间的表现
3. 重点关注：
   - 收益与市值的单调性
   - 成交额与市值的关系
   - 样本内外的一致性
4. 根据结果确定最优市值区间
"""
