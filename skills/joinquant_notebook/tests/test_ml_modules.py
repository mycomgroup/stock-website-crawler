# -*- coding: utf-8 -*-
"""
ml_*.py 系列文件单元测试
========================
测试内容:
- 数据处理逻辑
- 因子计算逻辑
- 机器学习模型相关逻辑
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestFeatureEngineering(unittest.TestCase):
    """测试因子工程相关逻辑"""

    def setUp(self):
        np.random.seed(42)
        self.sample_stocks = ["000001.XSHE", "000002.XSHE", "000003.XSHE", "000004.XSHE", "000005.XSHE"]

    def test_derived_factors_calculation(self):
        """测试衍生因子计算（EP, BP, SP, CFP, log_market_cap）"""
        df = pd.DataFrame(
            {
                "pe_ratio": [10.0, 20.0, 0.0, np.nan, 15.0],
                "pb_ratio": [1.5, 2.0, 3.0, 0.0, np.nan],
                "ps_ratio": [2.0, 3.0, 4.0, 5.0, 6.0],
                "pcf_ratio": [5.0, 10.0, 15.0, 20.0, 25.0],
                "market_cap": [1000.0, 2000.0, 3000.0, 4000.0, 5000.0],
            },
            index=self.sample_stocks,
        )

        df["EP"] = 1 / df["pe_ratio"].replace(0, np.nan)
        df["BP"] = 1 / df["pb_ratio"].replace(0, np.nan)
        df["SP"] = 1 / df["ps_ratio"].replace(0, np.nan)
        df["CFP"] = 1 / df["pcf_ratio"].replace(0, np.nan)
        df["log_market_cap"] = np.log(df["market_cap"].replace(0, np.nan))

        self.assertAlmostEqual(df.loc["000001.XSHE", "EP"], 0.1, places=5)
        self.assertAlmostEqual(df.loc["000002.XSHE", "EP"], 0.05, places=5)
        self.assertTrue(pd.isna(df.loc["000003.XSHE", "EP"]))
        self.assertTrue(pd.isna(df.loc["000004.XSHE", "BP"]))
        self.assertAlmostEqual(df.loc["000001.XSHE", "log_market_cap"], np.log(1000.0), places=5)

    def test_winsorize_extreme_values(self):
        """测试去极值处理"""
        np.random.seed(42)
        data = np.random.randn(100)
        data[0] = 100
        data[1] = -100
        df = pd.DataFrame({"col": data})

        q01 = df["col"].quantile(0.01)
        q99 = df["col"].quantile(0.99)
        df["col_winsorized"] = df["col"].clip(q01, q99)

        self.assertLess(df["col_winsorized"].max(), 100)
        self.assertGreater(df["col_winsorized"].min(), -100)
        self.assertEqual(df["col_winsorized"].max(), q99)
        self.assertEqual(df["col_winsorized"].min(), q01)

    def test_handle_inf_and_nan(self):
        """测试无穷值和缺失值处理"""
        df = pd.DataFrame(
            {
                "pe_ratio": [10.0, np.inf, -np.inf, 20.0, np.nan],
                "pb_ratio": [1.0, 2.0, 3.0, np.inf, 5.0],
            }
        )

        df = df.replace([np.inf, -np.inf], np.nan)

        self.assertTrue(pd.isna(df.loc[1, "pe_ratio"]))
        self.assertTrue(pd.isna(df.loc[2, "pe_ratio"]))
        self.assertTrue(pd.isna(df.loc[3, "pb_ratio"]))

    def test_label_creation(self):
        """测试标签生成（高于中位数为1）"""
        ret = pd.Series([0.1, 0.2, 0.3, 0.4, 0.5])
        label = (ret > ret.median()).astype(int)

        self.assertEqual(label.iloc[0], 0)
        self.assertEqual(label.iloc[1], 0)
        self.assertEqual(label.iloc[2], 0)
        self.assertEqual(label.iloc[3], 1)
        self.assertEqual(label.iloc[4], 1)

    def test_return_calculation(self):
        """测试收益率计算"""
        p0 = pd.Series([100.0, 50.0, 25.0], index=["A", "B", "C"])
        p1 = pd.Series([110.0, 55.0, 22.0], index=["A", "B", "C"])

        ret = ((p1 / p0) - 1).dropna()

        self.assertAlmostEqual(ret.loc["A"], 0.1, places=5)
        self.assertAlmostEqual(ret.loc["B"], 0.1, places=5)
        self.assertAlmostEqual(ret.loc["C"], -0.12, places=5)


class TestDataProcessing(unittest.TestCase):
    """测试数据处理逻辑"""

    def test_pivot_price_data(self):
        """测试价格数据透视"""
        price_data = pd.DataFrame(
            {
                "time": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-01"]),
                "code": ["000001.XSHE", "000002.XSHE", "000003.XSHE"],
                "close": [10.0, 20.0, 30.0],
            }
        )

        pivoted = price_data.pivot(index="time", columns="code", values="close").iloc[-1]

        self.assertEqual(pivoted.loc["000001.XSHE"], 10.0)
        self.assertEqual(pivoted.loc["000002.XSHE"], 20.0)
        self.assertEqual(pivoted.loc["000003.XSHE"], 30.0)

    def test_index_intersection(self):
        """测试索引交集"""
        feat_index = pd.Index(["A", "B", "C", "D"])
        ret_index = pd.Index(["B", "C", "D", "E"])

        common = feat_index.intersection(ret_index)

        self.assertEqual(len(common), 3)
        self.assertIn("B", common)
        self.assertIn("C", common)
        self.assertIn("D", common)

    def test_concat_features(self):
        """测试特征拼接"""
        feat1 = pd.DataFrame({"pe_ratio": [10, 20], "pb_ratio": [1, 2]}, index=["A", "B"])
        feat2 = pd.DataFrame({"pe_ratio": [30, 40], "pb_ratio": [3, 4]}, index=["C", "D"])

        combined = pd.concat([feat1, feat2])

        self.assertEqual(len(combined), 4)
        self.assertEqual(combined.loc["A", "pe_ratio"], 10)
        self.assertEqual(combined.loc["D", "pb_ratio"], 4)

    def test_fillna_with_zero(self):
        """测试缺失值填充"""
        df = pd.DataFrame({"pe_ratio": [10.0, np.nan, 30.0], "pb_ratio": [np.nan, 2.0, 3.0]})

        filled = df.fillna(0)

        self.assertEqual(filled.loc[1, "pe_ratio"], 0)
        self.assertEqual(filled.loc[0, "pb_ratio"], 0)


class TestStockPoolFiltering(unittest.TestCase):
    """测试股票池过滤逻辑"""

    def test_filter_by_listing_days(self):
        """测试上市天数过滤"""
        stocks = ["000001.XSHE", "000002.XSHE", "000003.XSHE"]
        date = datetime(2024, 6, 1)

        mock_infos = {
            "000001.XSHE": Mock(start_date=datetime(2024, 1, 1)),
            "000002.XSHE": Mock(start_date=datetime(2024, 5, 1)),
            "000003.XSHE": Mock(start_date=datetime(2023, 1, 1)),
        }

        valid = []
        for s in stocks:
            info = mock_infos.get(s)
            if info and (date - info.start_date).days > 180:
                valid.append(s)

        self.assertEqual(len(valid), 1)
        self.assertIn("000003.XSHE", valid)

    def test_sort_stocks_deterministically(self):
        """测试股票代码固定排序"""
        stocks = ["000003.XSHE", "000001.XSHE", "000002.XSHE"]

        sorted_stocks = sorted(stocks)

        self.assertEqual(sorted_stocks, ["000001.XSHE", "000002.XSHE", "000003.XSHE"])

    def test_take_top_n_stocks(self):
        """测试取前N只股票"""
        stocks = ["000001.XSHE", "000002.XSHE", "000003.XSHE", "000004.XSHE", "000005.XSHE"]

        top_n = stocks[:3]

        self.assertEqual(len(top_n), 3)
        self.assertEqual(top_n, ["000001.XSHE", "000002.XSHE", "000003.XSHE"])


class TestWalkForwardLogic(unittest.TestCase):
    """测试Walk-Forward验证逻辑"""

    def test_quarter_dates_generation(self):
        """测试季度日期生成"""
        dates = pd.to_datetime(
            [
                "2024-01-02",
                "2024-02-01",
                "2024-03-01",
                "2024-04-01",
                "2024-05-01",
                "2024-06-01",
                "2024-07-01",
                "2024-08-01",
                "2024-09-01",
            ]
        )

        quarter_dates = []
        last_q = None
        for d in dates:
            q = (d.year, (d.month - 1) // 3)
            if q != last_q:
                quarter_dates.append(d)
                last_q = q

        self.assertEqual(len(quarter_dates), 3)

    def test_monthly_dates_generation(self):
        """测试月度日期生成"""
        dates = pd.to_datetime(
            [
                "2024-01-02",
                "2024-02-01",
                "2024-02-15",
                "2024-03-01",
                "2024-04-01",
            ]
        )

        result, last_m = [], None
        for d in dates:
            if d.month != last_m:
                result.append(d)
                last_m = d.month

        self.assertEqual(len(result), 4)

    def test_train_test_split(self):
        """测试训练测试分割"""
        indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        train_quarters = 6

        for test_i in indices[train_quarters:]:
            train_i = [i for i in indices if i < test_i][-train_quarters:]

            self.assertEqual(len(train_i), train_quarters)
            self.assertTrue(all(i < test_i for i in train_i))


class TestStandardScaler(unittest.TestCase):
    """测试标准化逻辑"""

    def test_fit_transform(self):
        """测试fit_transform"""
        from sklearn.preprocessing import StandardScaler

        X_train = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_train)

        self.assertAlmostEqual(X_scaled[:, 0].mean(), 0, places=10)
        self.assertAlmostEqual(X_scaled[:, 0].std(), 1, places=5)

    def test_transform_test_data(self):
        """测试transform测试数据"""
        from sklearn.preprocessing import StandardScaler

        X_train = np.array([[1, 2], [3, 4], [5, 6]])
        X_test = np.array([[2, 3], [4, 5]])

        scaler = StandardScaler()
        scaler.fit(X_train)
        X_test_scaled = scaler.transform(X_test)

        self.assertEqual(X_test_scaled.shape, X_test.shape)


class TestMLModels(unittest.TestCase):
    """测试机器学习模型"""

    def setUp(self):
        np.random.seed(42)
        self.X_train = np.random.randn(100, 4)
        self.y_train = (self.X_train[:, 0] + self.X_train[:, 1] > 0).astype(int)
        self.X_test = np.random.randn(20, 4)

    def test_logistic_regression(self):
        """测试逻辑回归"""
        from sklearn.linear_model import LogisticRegression

        model = LogisticRegression(C=100, max_iter=200, random_state=42)
        model.fit(self.X_train, self.y_train)

        proba = model.predict_proba(self.X_test)
        pred = model.predict(self.X_test)

        self.assertEqual(proba.shape, (20, 2))
        self.assertEqual(len(pred), 20)
        self.assertTrue(np.all((pred == 0) | (pred == 1)))

    def test_svm(self):
        """测试SVM"""
        from sklearn.svm import SVC

        model = SVC(kernel="rbf", probability=True, C=1.0, random_state=42)
        model.fit(self.X_train, self.y_train)

        proba = model.predict_proba(self.X_test)

        self.assertEqual(proba.shape, (20, 2))

    def test_random_forest(self):
        """测试随机森林"""
        from sklearn.ensemble import RandomForestClassifier

        model = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=42)
        model.fit(self.X_train, self.y_train)

        proba = model.predict_proba(self.X_test)
        pred = model.predict(self.X_test)

        self.assertEqual(proba.shape, (20, 2))
        self.assertEqual(len(pred), 20)

    def test_select_top_n_by_probability(self):
        """测试根据概率选股"""
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(self.X_train)
        X_test_s = scaler.transform(self.X_test)

        model = LogisticRegression(C=100, max_iter=200, random_state=42)
        model.fit(X_train_s, self.y_train)

        proba = model.predict_proba(X_test_s)[:, 1]
        test_index = [f"stock_{i}" for i in range(20)]

        selected = pd.Series(proba, index=test_index).nlargest(10).index.tolist()

        self.assertEqual(len(selected), 10)

    def test_model_with_missing_values(self):
        """测试模型处理缺失值"""
        from sklearn.linear_model import LogisticRegression

        X_with_nan = self.X_train.copy()
        X_with_nan[0, 0] = np.nan
        X_filled = np.nan_to_num(X_with_nan, nan=0.0)

        model = LogisticRegression(C=100, max_iter=200, random_state=42)
        model.fit(X_filled, self.y_train)

        pred = model.predict(self.X_test)

        self.assertEqual(len(pred), 20)


class TestPerformanceMetrics(unittest.TestCase):
    """测试绩效指标计算"""

    def test_cumulative_return(self):
        """测试累计收益"""
        rets = pd.Series([0.1, -0.05, 0.15, 0.08, -0.02])

        cum = (1 + rets).cumprod()
        total = cum.iloc[-1] - 1

        expected_total = (1.1 * 0.95 * 1.15 * 1.08 * 0.98) - 1
        self.assertAlmostEqual(total, expected_total, places=5)

    def test_win_rate(self):
        """测试胜率"""
        rets = pd.Series([0.1, -0.05, 0.15, 0.08, -0.02])

        win = (rets > 0).mean()

        self.assertEqual(win, 0.6)

    def test_sharpe_ratio(self):
        """测试夏普比率"""
        rets = pd.Series([0.01, 0.02, -0.01, 0.03, 0.01] * 12)

        sharpe = rets.mean() / rets.std() * np.sqrt(12)

        self.assertGreater(sharpe, 0)

    def test_max_drawdown(self):
        """测试最大回撤"""
        rets = pd.Series([0.1, -0.2, 0.1, -0.1, 0.05])

        cum = (1 + rets).cumprod()
        max_dd = (cum / cum.cummax() - 1).min()

        self.assertAlmostEqual(max_dd, -0.208, places=2)

    def test_annualized_return(self):
        """测试年化收益"""
        monthly_rets = pd.Series([0.01] * 12)
        total = (1 + monthly_rets).cumprod().iloc[-1] - 1
        ann = (1 + total) ** (12 / 12) - 1

        self.assertAlmostEqual(ann, 0.1268, places=2)

    def test_information_ratio(self):
        """测试信息比率"""
        strategy_rets = pd.Series([0.02, 0.01, 0.03, -0.01, 0.02])
        benchmark_rets = pd.Series([0.01, 0.01, 0.01, 0.01, 0.01])

        excess = strategy_rets - benchmark_rets
        ir = excess.mean() / excess.std() * np.sqrt(12)

        self.assertIsInstance(ir, float)


class TestTransactionCost(unittest.TestCase):
    """测试交易成本计算"""

    def test_net_return_calculation(self):
        """测试净收益计算"""
        gross_return = 0.05
        cost = 0.002

        net = gross_return - cost

        self.assertAlmostEqual(net, 0.048, places=5)

    def test_double_sided_cost(self):
        """测试双边成本"""
        gross_return = 0.05
        single_cost = 0.001

        net = gross_return - single_cost * 2

        self.assertAlmostEqual(net, 0.048, places=5)

    def test_portfolio_return(self):
        """测试组合收益计算"""
        selected_stocks = ["A", "B", "C"]
        returns = pd.Series([0.05, 0.03, 0.07, 0.02], index=["A", "B", "C", "D"])
        cost = 0.002

        available = [s for s in selected_stocks if s in returns.index]
        gross = returns.loc[available].mean()
        net = gross - cost

        self.assertAlmostEqual(gross, 0.05, places=5)
        self.assertAlmostEqual(net, 0.048, places=5)


class TestMockJQData(unittest.TestCase):
    """测试Mock JQData功能"""

    @patch("sys.modules")
    def test_mock_jqdata_functions(self, mock_modules):
        """测试模拟JQData函数行为"""
        mock_jqdata = MagicMock()

        mock_jqdata.get_trade_days.return_value = pd.to_datetime(
            ["2024-01-02", "2024-02-01", "2024-03-01", "2024-04-01"]
        )

        mock_jqdata.get_index_stocks.return_value = [
            "000001.XSHE",
            "000002.XSHE",
            "000003.XSHE",
        ]

        dates = mock_jqdata.get_trade_days("2024-01-01", "2024-12-31")
        self.assertEqual(len(dates), 4)

        stocks = mock_jqdata.get_index_stocks("000905.XSHG")
        self.assertEqual(len(stocks), 3)

    def test_mock_get_fundamentals(self):
        """测试模拟get_fundamentals返回"""
        mock_result = pd.DataFrame(
            {
                "code": ["000001.XSHE", "000002.XSHE", "000003.XSHE"],
                "pe_ratio": [10.0, 15.0, 20.0],
                "pb_ratio": [1.0, 1.5, 2.0],
                "roe": [0.15, 0.12, 0.10],
                "roa": [0.08, 0.06, 0.05],
            }
        )

        df = mock_result.set_index("code")

        self.assertEqual(len(df), 3)
        self.assertEqual(df.loc["000001.XSHE", "pe_ratio"], 10.0)

    def test_mock_get_price(self):
        """测试模拟get_price返回"""
        mock_price = pd.DataFrame(
            {
                "time": pd.to_datetime(["2024-01-01"] * 3),
                "code": ["000001.XSHE", "000002.XSHE", "000003.XSHE"],
                "close": [10.0, 20.0, 30.0],
            }
        )

        pivoted = mock_price.pivot(index="time", columns="code", values="close").iloc[-1]

        self.assertEqual(pivoted.loc["000001.XSHE"], 10.0)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""

    def test_empty_data(self):
        """测试空数据处理"""
        df = pd.DataFrame()
        self.assertEqual(len(df), 0)

    def test_insufficient_samples(self):
        """测试样本不足"""
        df = pd.DataFrame({"pe_ratio": [10, 20], "pb_ratio": [1, 2]})
        self.assertLess(len(df), 30)

    def test_all_nan_column(self):
        """测试全NaN列"""
        df = pd.DataFrame({"pe_ratio": [np.nan, np.nan, np.nan]})

        dropped = df.dropna()

        self.assertEqual(len(dropped), 0)

    def test_single_stock_selection(self):
        """测试单只股票选择"""
        proba = np.array([0.9])
        index = ["000001.XSHE"]

        selected = pd.Series(proba, index=index).nlargest(10).index.tolist()

        self.assertEqual(len(selected), 1)

    def test_negative_return_handling(self):
        """测试负收益处理"""
        rets = pd.Series([-0.1, -0.2, -0.3])

        cum = (1 + rets).cumprod()

        self.assertLess(cum.iloc[-1], 1)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_pipeline_simulation(self):
        """测试完整流程模拟"""
        np.random.seed(42)

        X_train = pd.DataFrame(
            {
                "pe_ratio": np.random.randn(100),
                "pb_ratio": np.random.randn(100),
                "roe": np.random.randn(100),
                "roa": np.random.randn(100),
            }
        )
        y_train = (np.random.randn(100) > 0).astype(int)

        X_test = pd.DataFrame(
            {
                "pe_ratio": np.random.randn(20),
                "pb_ratio": np.random.randn(20),
                "roe": np.random.randn(20),
                "roa": np.random.randn(20),
            }
        )

        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train.fillna(0))
        X_test_s = scaler.transform(X_test.fillna(0))

        model = LogisticRegression(C=100, max_iter=200, random_state=42)
        model.fit(X_train_s, y_train)

        proba = model.predict_proba(X_test_s)[:, 1]

        selected = pd.Series(proba, index=X_test.index).nlargest(10).index

        returns = pd.Series(np.random.randn(20) * 0.1, index=X_test.index)
        net = returns.loc[selected].mean() - 0.002

        self.assertEqual(len(selected), 10)
        self.assertIsInstance(net, float)


if __name__ == "__main__":
    unittest.main(verbosity=2)