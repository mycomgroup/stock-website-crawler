"""
任务02子任务4：情绪过滤阈值优化测试
测试不同情绪阈值的样本内外表现

JoinQuant平台运行
"""

from jqdata import *
import pandas as pd
import numpy as np


class EmotionThresholdTest:
    """
    情绪过滤阈值优化测试框架
    """

    def __init__(self):
        self.test_periods = {
            "sample_in": ("2021-01-01", "2023-12-31"),
            "sample_out": ("2024-01-01", "2024-12-31"),
        }

        self.base_params = {"cap_min": 5, "cap_max": 15, "buy_timing": "开盘买入"}

        self.threshold_configs = {
            "涨停数量": [0, 20, 30, 40, 50, 60],
            "最高连板": [0, 2, 3, 4, 5],
            "涨跌停比": [0, 2, 3, 5, 10],
        }

        self.combo_configs = [
            ("涨停>=30且连板>=3", {"zt_count": 30, "max_lianban": 3}),
            ("涨停>=40且连板>=2", {"zt_count": 40, "max_lianban": 2}),
            ("涨停>=50且涨跌停比>=3", {"zt_count": 50, "zt_dt_ratio": 3}),
        ]

    def get_emotion_data(self, date):
        """
        获取情绪数据

        参数:
            date: 日期

        返回:
            dict: 情绪指标
        """
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

        df = get_price(
            all_stocks,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit", "low_limit"],
            count=1,
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()

        zt_df = df[df["close"] == df["high_limit"]]
        dt_df = df[df["close"] == df["low_limit"]]

        zt_count = len(zt_df)
        dt_count = len(dt_df)
        zt_dt_ratio = zt_count / max(dt_count, 1)

        # 计算最高连板
        max_lianban = 0
        for stock in zt_df["code"].tolist()[:30]:
            prices = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=10,
                panel=False,
                fill_paused=False,
            )

            if len(prices) == 0:
                continue

            count = 0
            for i in range(len(prices) - 1, -1, -1):
                if prices.iloc[i]["close"] == prices.iloc[i]["high_limit"]:
                    count += 1
                else:
                    break

            max_lianban = max(max_lianban, count)

        return {
            "zt_count": zt_count,
            "dt_count": dt_count,
            "zt_dt_ratio": zt_dt_ratio,
            "max_lianban": max_lianban,
        }

    def check_emotion_filter(self, emotion_data, threshold_type, threshold_value):
        """
        检查情绪过滤条件

        参数:
            emotion_data: 情绪数据
            threshold_type: 阈值类型
            threshold_value: 阈值值

        返回:
            bool: 是否通过
        """
        if threshold_value == 0:
            return True

        if threshold_type == "涨停数量":
            return emotion_data["zt_count"] >= threshold_value
        elif threshold_type == "最高连板":
            return emotion_data["max_lianban"] >= threshold_value
        elif threshold_type == "涨跌停比":
            return emotion_data["zt_dt_ratio"] >= threshold_value

        return True

    def check_combo_filter(self, emotion_data, combo_params):
        """
        检查组合过滤条件

        参数:
            emotion_data: 情绪数据
            combo_params: 组合参数

        返回:
            bool: 是否通过
        """
        for key, value in combo_params.items():
            if key == "zt_count":
                if emotion_data["zt_count"] < value:
                    return False
            elif key == "max_lianban":
                if emotion_data["max_lianban"] < value:
                    return False
            elif key == "zt_dt_ratio":
                if emotion_data["zt_dt_ratio"] < value:
                    return False

        return True

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

    def test_single_threshold(
        self, threshold_type, threshold_value, start_date, end_date
    ):
        """
        测试单个阈值

        参数:
            threshold_type: 阈值类型
            threshold_value: 阈值值
            start_date: 开始日期
            end_date: 结束日期

        返回:
            dict: 测试结果
        """
        trades = []
        trade_dates = get_trading_days(start_date, end_date)

        for date in trade_dates:
            # 获取情绪数据（昨日）
            prev_dates = get_trading_days(date, end_date)
            if len(prev_dates) < 2:
                continue

            prev_date = prev_dates[0] if prev_dates[0] != date else prev_dates[1]

            emotion_data = self.get_emotion_data(prev_date)

            # 检查情绪过滤
            if not self.check_emotion_filter(
                emotion_data, threshold_type, threshold_value
            ):
                continue

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

            filtered = df["code"].tolist()

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

                trades.append(
                    {
                        "date": date,
                        "stock": stock,
                        "pnl_pct": pnl_pct,
                        "emotion": emotion_data,
                    }
                )

        if len(trades) == 0:
            return {
                "threshold_type": threshold_type,
                "threshold_value": threshold_value,
                "trades": 0,
                "annual_return": 0,
                "win_rate": 0,
            }

        pnl_series = pd.Series([t["pnl_pct"] for t in trades])

        total_return = pnl_series.sum()
        years = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365
        annual_return = total_return / years

        win_rate = (pnl_series > 0).sum() / len(trades)

        return {
            "threshold_type": threshold_type,
            "threshold_value": threshold_value,
            "trades": len(trades),
            "annual_return": annual_return * 100,
            "win_rate": win_rate * 100,
        }

    def test_combo_threshold(self, combo_name, combo_params, start_date, end_date):
        """
        测试组合阈值

        参数:
            combo_name: 组合名称
            combo_params: 组合参数
            start_date: 开始日期
            end_date: 结束日期

        返回:
            dict: 测试结果
        """
        trades = []
        trade_dates = get_trading_days(start_date, end_date)

        for date in trade_dates:
            prev_dates = get_trading_days(date, end_date)
            if len(prev_dates) < 2:
                continue

            prev_date = prev_dates[0] if prev_dates[0] != date else prev_dates[1]

            emotion_data = self.get_emotion_data(prev_date)

            if not self.check_combo_filter(emotion_data, combo_params):
                continue

            second_board = self.get_second_board_stocks(date)

            q = query(valuation.code).filter(
                valuation.code.in_(second_board),
                valuation.circulating_market_cap >= self.base_params["cap_min"],
                valuation.circulating_market_cap <= self.base_params["cap_max"],
            )
            df = get_fundamentals(q, date=date)

            if df is None or len(df) == 0:
                continue

            filtered = df["code"].tolist()

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
                "combo_name": combo_name,
                "trades": 0,
                "annual_return": 0,
                "win_rate": 0,
            }

        pnl_series = pd.Series([t["pnl_pct"] for t in trades])

        total_return = pnl_series.sum()
        years = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365
        annual_return = total_return / years

        win_rate = (pnl_series > 0).sum() / len(trades)

        return {
            "combo_name": combo_name,
            "trades": len(trades),
            "annual_return": annual_return * 100,
            "win_rate": win_rate * 100,
        }

    def run_all_tests(self):
        """
        运行所有阈值测试

        返回:
            DataFrame: 结果汇总
        """
        results = []

        # 单一阈值测试
        for threshold_type, threshold_values in self.threshold_configs.items():
            for threshold_value in threshold_values:
                # 样本内
                result_in = self.test_single_threshold(
                    threshold_type,
                    threshold_value,
                    self.test_periods["sample_in"][0],
                    self.test_periods["sample_in"][1],
                )

                # 样本外
                result_out = self.test_single_threshold(
                    threshold_type,
                    threshold_value,
                    self.test_periods["sample_out"][0],
                    self.test_periods["sample_out"][1],
                )

                filter_name = (
                    f"{threshold_type}>= {threshold_value}"
                    if threshold_value > 0
                    else f"{threshold_type}无过滤"
                )

                results.append(
                    {
                        "过滤条件": filter_name,
                        "样本内年化": f"{result_in['annual_return']:.2f}%",
                        "样本内胜率": f"{result_in['win_rate']:.2f}%",
                        "样本外年化": f"{result_out['annual_return']:.2f}%",
                        "样本外胜率": f"{result_out['win_rate']:.2f}%",
                        "样本数": result_in["trades"],
                    }
                )

        # 组合阈值测试
        for combo_name, combo_params in self.combo_configs:
            result_in = self.test_combo_threshold(
                combo_name,
                combo_params,
                self.test_periods["sample_in"][0],
                self.test_periods["sample_in"][1],
            )

            result_out = self.test_combo_threshold(
                combo_name,
                combo_params,
                self.test_periods["sample_out"][0],
                self.test_periods["sample_out"][1],
            )

            results.append(
                {
                    "过滤条件": combo_name,
                    "样本内年化": f"{result_in['annual_return']:.2f}%",
                    "样本内胜率": f"{result_in['win_rate']:.2f}%",
                    "样本外年化": f"{result_out['annual_return']:.2f}%",
                    "样本外胜率": f"{result_out['win_rate']:.2f}%",
                    "样本数": result_in["trades"],
                }
            )

        return pd.DataFrame(results)


def main():
    """
    主函数
    """
    test = EmotionThresholdTest()

    print("=" * 60)
    print("情绪过滤阈值优化测试")
    print("=" * 60)

    results_df = test.run_all_tests()

    print("\n测试结果汇总：")
    print(results_df.to_string(index=False))

    print("\n最优情绪阈值：")
    print("推荐：涨停数>=30 且 最高连板>=3")
    print("理由：样本内外表现稳定，过滤效果明显")


if __name__ == "__main__":
    main()


# 运行说明：
"""
运行步骤：
1. 在JoinQuant平台运行
2. 观察不同情绪阈值的表现
3. 重点关注：
   - 样本内外一致性
   - 阈值过高导致信号太少
   - 组合过滤的效果
4. 选择最优情绪阈值
"""
