"""
test_market_sentiment.py
market_sentiment.py 模块核心函数单元测试。

测试目标：
- compute_crowding_ratio: 拥挤率指标
- compute_gisi: GSISI 投资者情绪指数
- compute_fed_model: FED 模型（股债性价比）
- compute_graham_index: 格雷厄姆指数
- compute_below_net_ratio: 破净占比
- compute_new_high_ratio: 创新高占比
- get_all_sentiment_indicators: 所有情绪指标汇总
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

import importlib.util


def _load_ms_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_base = os.path.join(os.path.dirname(__file__), "../../../jk2bt/signals")
_ms_mod = _load_ms_module(
    "market_sentiment", os.path.join(_base, "market_sentiment.py")
)

compute_crowding_ratio = _ms_mod.compute_crowding_ratio
compute_gisi = _ms_mod.compute_gisi
compute_fed_model = _ms_mod.compute_fed_model
compute_graham_index = _ms_mod.compute_graham_index
compute_below_net_ratio = _ms_mod.compute_below_net_ratio
compute_new_high_ratio = _ms_mod.compute_new_high_ratio
get_all_sentiment_indicators = _ms_mod.get_all_sentiment_indicators


# =====================================================================
# Fixtures
# =====================================================================


@pytest.fixture
def sample_spot_df():
    """生成模拟实时行情数据。"""
    np.random.seed(42)
    n = 200
    codes = [f"sh{600000 + i}" for i in range(n)]
    names = [f"股票{i}" for i in range(n)]
    amounts = np.random.exponential(1e8, n)
    pb_values = np.random.uniform(0.5, 5.0, n)
    closes = np.random.uniform(10, 100, n)

    df = pd.DataFrame(
        {
            "代码": codes,
            "名称": names,
            "成交额": amounts,
            "市净率": pb_values,
            "收盘": closes,
        }
    )
    return df


@pytest.fixture
def sample_pe_pb_df():
    """生成模拟PE/PB数据。"""
    dates = pd.date_range("2023-01-01", periods=50, freq="B")
    pes = np.linspace(12, 18, 50)
    pbs = np.linspace(1.2, 1.8, 50)

    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "pe": pes,
            "pb": pbs,
        }
    )
    return df


@pytest.fixture
def sample_bond_yield_df():
    """生成模拟国债收益率数据。"""
    dates = pd.date_range("2023-01-01", periods=10, freq="B")
    yields = np.linspace(2.5, 2.8, 10)

    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "10年期国债收益率": yields,
        }
    )
    return df


@pytest.fixture
def sample_hist_df():
    """生成模拟历史行情数据。"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=80, freq="B")
    closes = 50 + np.cumsum(np.random.randn(80) * 0.5)
    closes = np.abs(closes)

    df = pd.DataFrame(
        {
            "日期": dates.strftime("%Y-%m-%d"),
            "收盘": closes,
            "开盘": closes * 0.99,
            "最高": closes * 1.02,
            "最低": closes * 0.98,
            "成交量": np.random.randint(1e6, 1e7, 80),
        }
    )
    return df


# =====================================================================
# compute_crowding_ratio Tests
# =====================================================================


class TestComputeCrowdingRatio:
    """测试拥挤率指标计算。"""

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_normal(self, mock_get_adapter, sample_spot_df):
        """验证拥挤率基本计算。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = sample_spot_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_crowding_ratio(date="2023-06-01")

        assert isinstance(result, dict)
        assert "crowding_ratio" in result
        assert "description" in result
        assert result["crowding_ratio"] > 0

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_high_concentration(self, mock_get_adapter):
        """测试资金高度集中场景（拥挤率>60%）。"""
        df = pd.DataFrame(
            {
                "代码": [f"sh{i}" for i in range(100)],
                "名称": [f"股票{i}" for i in range(100)],
                "成交额": [1e10] * 5 + [1e6] * 95,
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_crowding_ratio(date="2023-06-01")

        assert result["crowding_ratio"] > 60
        assert "资金过度集中" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_low_concentration(self, mock_get_adapter):
        """测试资金分散场景（拥挤率<40%）。"""
        df = pd.DataFrame(
            {
                "代码": [f"sh{i}" for i in range(100)],
                "名称": [f"股票{i}" for i in range(100)],
                "成交额": [1e8] * 100,
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_crowding_ratio(date="2023-06-01")

        assert result["crowding_ratio"] < 40
        assert "资金分散" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_empty_data(self, mock_get_adapter):
        """测试空数据返回默认值。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        result = compute_crowding_ratio(date="2023-06-01")

        assert result["crowding_ratio"] == 0.0
        assert "计算失败" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_none_data(self, mock_get_adapter):
        """测试None数据返回默认值。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = None
        mock_get_adapter.return_value = mock_adapter

        result = compute_crowding_ratio(date="2023-06-01")

        assert result["crowding_ratio"] == 0.0

    def test_crowding_ratio_import_error(self):
        """测试当data_access模块不可用时的行为（跳过，因为模块已安装）。"""
        # 由于jk2bt.data_access已安装，此测试验证正常路径
        # 实际import错误只在未安装时发生
        pytest.skip("jk2bt.data_access is installed")

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_date_format(self, mock_get_adapter, sample_spot_df):
        """测试日期格式处理（带横杠和不带横杠）。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = sample_spot_df
        mock_get_adapter.return_value = mock_adapter

        result1 = compute_crowding_ratio(date="2023-06-01")
        result2 = compute_crowding_ratio(date="20230601")

        assert result1["crowding_ratio"] == result2["crowding_ratio"]

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_default_date(self, mock_get_adapter, sample_spot_df):
        """测试不传日期时使用当前日期。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = sample_spot_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_crowding_ratio()

        assert isinstance(result, dict)
        assert "crowding_ratio" in result

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_with_threshold(self, mock_get_adapter):
        """测试不同阈值百分比。"""
        df = pd.DataFrame(
            {
                "代码": [f"sh{i}" for i in range(100)],
                "名称": [f"股票{i}" for i in range(100)],
                "成交额": list(range(1, 101)),
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result_5pct = compute_crowding_ratio(date="2023-06-01", threshold_pct=0.05)
        result_10pct = compute_crowding_ratio(date="2023-06-01", threshold_pct=0.10)

        assert result_10pct["crowding_ratio"] >= result_5pct["crowding_ratio"]

    @patch("jk2bt.data_access.get_adapter")
    def test_crowding_ratio_exception(self, mock_get_adapter):
        """测试异常处理。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.side_effect = Exception("Network error")
        mock_get_adapter.return_value = mock_adapter

        result = compute_crowding_ratio(date="2023-06-01")

        assert result["crowding_ratio"] == 0.0
        assert "计算失败" in result["description"]


# =====================================================================
# compute_fed_model Tests
# =====================================================================


class TestComputeFedModel:
    """测试 FED 模型计算。"""

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_normal(
        self, mock_get_adapter, sample_pe_pb_df, sample_bond_yield_df
    ):
        """验证FED模型基本计算。"""
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.return_value = sample_pe_pb_df
        mock_adapter.get_bond_yield.return_value = sample_bond_yield_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model(date="2023-06-01")

        assert isinstance(result, dict)
        assert "fed_value" in result
        assert "pe" in result
        assert "bond_rate" in result
        assert "description" in result

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_with_bond_rate(self, mock_get_adapter, sample_pe_pb_df):
        """测试传入国债收益率。"""
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.return_value = sample_pe_pb_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model(date="2023-06-01", bond_rate=0.03)

        assert result["bond_rate"] == 0.03
        assert result["pe"] > 0

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_stock_attractive(self, mock_get_adapter):
        """测试股票极具吸引力场景（FED>0.05）。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "pe": [10.0],
                "pb": [1.0],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model(date="2023-06-01", bond_rate=0.02)

        assert result["fed_value"] > 0.05
        assert "极具吸引力" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_bond_better(self, mock_get_adapter):
        """测试债券优于股票场景（FED<0）。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "pe": [30.0],
                "pb": [3.0],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model(date="2023-06-01", bond_rate=0.04)

        assert result["fed_value"] < 0
        assert "债券优于股票" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_empty_pe_data(self, mock_get_adapter):
        """测试空PE数据。"""
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model(date="2023-06-01")

        assert result["fed_value"] == 0.0
        assert "计算失败" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_no_pe_data(self, mock_get_adapter):
        """测试无PE数据场景。"""
        df = pd.DataFrame(
            {
                "date": ["2025-01-01"],
                "pe": [15.0],
                "pb": [1.5],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model(date="2023-06-01")

        assert result["fed_value"] == 0.0
        assert "无PE数据" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_bond_yield_exception(self, mock_get_adapter, sample_pe_pb_df):
        """测试国债收益率获取异常时使用默认值。"""
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.return_value = sample_pe_pb_df
        mock_adapter.get_bond_yield.side_effect = Exception("Bond error")
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model(date="2023-06-01")

        assert result["bond_rate"] == 0.025

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_exception(self, mock_get_adapter):
        """测试异常处理。"""
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.side_effect = Exception("API error")
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model(date="2023-06-01")

        assert result["fed_value"] == 0.0
        assert "计算失败" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_fed_model_default_date(self, mock_get_adapter, sample_pe_pb_df):
        """测试不传日期时使用当前日期。"""
        mock_adapter = MagicMock()
        mock_adapter.get_stock_pe_pb.return_value = sample_pe_pb_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_fed_model()

        assert isinstance(result, dict)
        assert "fed_value" in result


# =====================================================================
# compute_graham_index Tests
# =====================================================================


class TestComputeGrahamIndex:
    """测试格雷厄姆指数计算。"""

    @patch("market_sentiment.compute_fed_model")
    def test_graham_index_normal(self, mock_fed_model):
        """验证格雷厄姆指数基本计算。"""
        mock_fed_model.return_value = {
            "fed_value": 0.04,
            "pe": 15.0,
            "bond_rate": 0.025,
            "description": "test",
        }

        result = compute_graham_index(date="2023-06-01")

        assert isinstance(result, dict)
        assert "graham_index" in result
        expected = (1.0 / 15.0) / 0.025
        np.testing.assert_almost_equal(result["graham_index"], expected, decimal=6)

    @patch("market_sentiment.compute_fed_model")
    def test_graham_index_undervalued(self, mock_fed_model):
        """测试股票低估场景（指数>1.5）。"""
        mock_fed_model.return_value = {
            "fed_value": 0.05,
            "pe": 10.0,
            "bond_rate": 0.03,
            "description": "test",
        }

        result = compute_graham_index(date="2023-06-01")

        assert result["graham_index"] > 1.5
        assert "股票低估" in result["description"]

    @patch("market_sentiment.compute_fed_model")
    def test_graham_index_reasonable(self, mock_fed_model):
        """测试股票合理场景（1<指数<1.5）。"""
        mock_fed_model.return_value = {
            "fed_value": 0.03,
            "pe": 15.0,
            "bond_rate": 0.05,
            "description": "test",
        }

        result = compute_graham_index(date="2023-06-01")

        assert 1 < result["graham_index"] < 1.5
        assert "股票合理" in result["description"]

    @patch("market_sentiment.compute_fed_model")
    def test_graham_index_overvalued(self, mock_fed_model):
        """测试股票高估场景（指数<1）。"""
        mock_fed_model.return_value = {
            "fed_value": 0.01,
            "pe": 30.0,
            "bond_rate": 0.04,
            "description": "test",
        }

        result = compute_graham_index(date="2023-06-01")

        assert result["graham_index"] < 1
        assert "股票高估" in result["description"]

    @patch("market_sentiment.compute_fed_model")
    def test_graham_index_fed_failed(self, mock_fed_model):
        """测试FED模型失败时返回默认值。"""
        mock_fed_model.return_value = {
            "fed_value": 0.0,
            "description": "计算失败",
        }

        result = compute_graham_index(date="2023-06-01")

        assert result["graham_index"] == 0.0
        assert "计算失败" in result["description"]


# =====================================================================
# compute_below_net_ratio Tests
# =====================================================================


class TestComputeBelowNetRatio:
    """测试破净占比计算。"""

    @patch("jk2bt.data_access.get_adapter")
    def test_below_net_ratio_normal(self, mock_get_adapter, sample_spot_df):
        """验证破净占比基本计算。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = sample_spot_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_below_net_ratio(date="2023-06-01")

        assert isinstance(result, dict)
        assert "below_net_ratio" in result
        assert "below_net_count" in result
        assert "total_count" in result
        assert "description" in result

    @patch("jk2bt.data_access.get_adapter")
    def test_below_net_ratio_high(self, mock_get_adapter):
        """测试破净占比高场景（>10%）。"""
        df = pd.DataFrame(
            {
                "代码": [f"sh{i}" for i in range(100)],
                "名称": [f"股票{i}" for i in range(100)],
                "市净率": [0.8] * 15 + [1.5] * 85,
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_below_net_ratio(date="2023-06-01")

        assert result["below_net_ratio"] > 10
        assert "极度悲观" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_below_net_ratio_medium(self, mock_get_adapter):
        """测试破净占比中等场景（5%-10%）。"""
        df = pd.DataFrame(
            {
                "代码": [f"sh{i}" for i in range(100)],
                "名称": [f"股票{i}" for i in range(100)],
                "市净率": [0.9] * 8 + [1.5] * 92,
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_below_net_ratio(date="2023-06-01")

        assert 5 < result["below_net_ratio"] < 10
        assert "偏悲观" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_below_net_ratio_low(self, mock_get_adapter):
        """测试破净占比低场景（<5%）。"""
        df = pd.DataFrame(
            {
                "代码": [f"sh{i}" for i in range(100)],
                "名称": [f"股票{i}" for i in range(100)],
                "市净率": [0.9] * 2 + [1.5] * 98,
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_below_net_ratio(date="2023-06-01")

        assert result["below_net_ratio"] < 5
        assert "市场正常" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_below_net_ratio_empty_data(self, mock_get_adapter):
        """测试空数据返回默认值。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        result = compute_below_net_ratio(date="2023-06-01")

        assert result["below_net_ratio"] == 0.0
        assert "计算失败" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_below_net_ratio_no_pb_column(self, mock_get_adapter):
        """测试缺少市净率列。"""
        df = pd.DataFrame(
            {
                "代码": ["sh600000"],
                "名称": ["股票"],
                "成交额": [1e8],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = compute_below_net_ratio(date="2023-06-01")

        assert result["below_net_ratio"] == 0.0

    @patch("jk2bt.data_access.get_adapter")
    def test_below_net_ratio_exception(self, mock_get_adapter):
        """测试异常处理。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.side_effect = Exception("API error")
        mock_get_adapter.return_value = mock_adapter

        result = compute_below_net_ratio(date="2023-06-01")

        assert result["below_net_ratio"] == 0.0
        assert "计算失败" in result["description"]


# =====================================================================
# compute_new_high_ratio Tests
# =====================================================================


class TestComputeNewHighRatio:
    """测试创新高占比计算。"""

    @patch("jk2bt.data_access.get_adapter")
    def test_new_high_ratio_normal(
        self, mock_get_adapter, sample_spot_df, sample_hist_df
    ):
        """验证创新高占比基本计算。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = sample_spot_df
        mock_adapter.get_stock_hist.return_value = sample_hist_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_new_high_ratio(date="2023-06-01", window=60)

        assert isinstance(result, dict)
        assert "new_high_ratio" in result
        assert "new_high_count" in result
        assert "total_count" in result
        assert "description" in result

    @patch("jk2bt.data_access.get_adapter")
    def test_new_high_ratio_strong_market(self, mock_get_adapter):
        """测试市场强势场景（创新高占比>5%）。"""
        spot_df = pd.DataFrame(
            {
                "代码": [f"sh{i}" for i in range(10)],
                "名称": [f"股票{i}" for i in range(10)],
            }
        )

        hist_df = pd.DataFrame(
            {
                "收盘": list(range(1, 61)) + [100],
            }
        )

        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = spot_df
        mock_adapter.get_stock_hist.return_value = hist_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_new_high_ratio(date="2023-06-01", window=60)

        assert result["new_high_ratio"] > 5
        assert "市场强势" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_new_high_ratio_weak_market(self, mock_get_adapter):
        """测试市场弱势场景（创新高占比<1%）。"""
        spot_df = pd.DataFrame(
            {
                "代码": [f"sh{i}" for i in range(100)],
                "名称": [f"股票{i}" for i in range(100)],
            }
        )

        hist_df = pd.DataFrame(
            {
                "收盘": list(range(100, 0, -1)) + [1],
            }
        )

        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = spot_df
        mock_adapter.get_stock_hist.return_value = hist_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_new_high_ratio(date="2023-06-01", window=60)

        assert result["new_high_ratio"] < 1
        assert "市场弱势" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_new_high_ratio_empty_data(self, mock_get_adapter):
        """测试空数据返回默认值。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        result = compute_new_high_ratio(date="2023-06-01")

        assert result["new_high_ratio"] == 0.0
        assert "计算失败" in result["description"]

    @patch("jk2bt.data_access.get_adapter")
    def test_new_high_ratio_insufficient_history(self, mock_get_adapter):
        """测试历史数据不足场景。"""
        spot_df = pd.DataFrame(
            {
                "代码": ["sh600000"],
                "名称": ["股票"],
            }
        )

        hist_df = pd.DataFrame(
            {
                "收盘": [100, 101, 102],
            }
        )

        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.return_value = spot_df
        mock_adapter.get_stock_hist.return_value = hist_df
        mock_get_adapter.return_value = mock_adapter

        result = compute_new_high_ratio(date="2023-06-01", window=60)

        assert result["new_high_ratio"] == 0.0

    @patch("jk2bt.data_access.get_adapter")
    def test_new_high_ratio_exception(self, mock_get_adapter):
        """测试异常处理。"""
        mock_adapter = MagicMock()
        mock_adapter.get_spot_em.side_effect = Exception("API error")
        mock_get_adapter.return_value = mock_adapter

        result = compute_new_high_ratio(date="2023-06-01")

        assert result["new_high_ratio"] == 0.0
        assert "计算失败" in result["description"]


# =====================================================================
# get_all_sentiment_indicators Tests
# =====================================================================


class TestGetAllSentimentIndicators:
    """测试获取所有情绪指标。"""

    @patch("market_sentiment.compute_new_high_ratio")
    @patch("market_sentiment.compute_below_net_ratio")
    @patch("market_sentiment.compute_graham_index")
    @patch("market_sentiment.compute_fed_model")
    @patch("market_sentiment.compute_crowding_ratio")
    def test_get_all_indicators(
        self,
        mock_crowding,
        mock_fed,
        mock_graham,
        mock_below_net,
        mock_new_high,
    ):
        """验证返回所有情绪指标。"""
        mock_crowding.return_value = {"crowding_ratio": 50.0, "description": "正常"}
        mock_fed.return_value = {
            "fed_value": 0.03,
            "pe": 15,
            "bond_rate": 0.03,
            "description": "正常",
        }
        mock_graham.return_value = {"graham_index": 1.2, "description": "合理"}
        mock_below_net.return_value = {
            "below_net_ratio": 3.0,
            "below_net_count": 10,
            "total_count": 300,
            "description": "正常",
        }
        mock_new_high.return_value = {
            "new_high_ratio": 2.0,
            "new_high_count": 5,
            "total_count": 100,
            "description": "中性",
        }

        result = get_all_sentiment_indicators(date="2023-06-01")

        assert isinstance(result, dict)
        assert "crowding_ratio" in result
        assert "fed_model" in result
        assert "graham_index" in result
        assert "below_net_ratio" in result
        assert "new_high_ratio" in result

    @patch("market_sentiment.compute_new_high_ratio")
    @patch("market_sentiment.compute_below_net_ratio")
    @patch("market_sentiment.compute_graham_index")
    @patch("market_sentiment.compute_fed_model")
    @patch("market_sentiment.compute_crowding_ratio")
    def test_get_all_indicators_passes_date(
        self,
        mock_crowding,
        mock_fed,
        mock_graham,
        mock_below_net,
        mock_new_high,
    ):
        """验证日期参数正确传递给各子函数。"""
        mock_crowding.return_value = {"crowding_ratio": 50.0, "description": "正常"}
        mock_fed.return_value = {
            "fed_value": 0.03,
            "pe": 15,
            "bond_rate": 0.03,
            "description": "正常",
        }
        mock_graham.return_value = {"graham_index": 1.2, "description": "合理"}
        mock_below_net.return_value = {
            "below_net_ratio": 3.0,
            "below_net_count": 10,
            "total_count": 300,
            "description": "正常",
        }
        mock_new_high.return_value = {
            "new_high_ratio": 2.0,
            "new_high_count": 5,
            "total_count": 100,
            "description": "中性",
        }

        get_all_sentiment_indicators(date="2023-12-25")

        mock_crowding.assert_called_with("2023-12-25")
        mock_fed.assert_called_with("2023-12-25")
        mock_graham.assert_called_with("2023-12-25")
        mock_below_net.assert_called_with("2023-12-25")
        mock_new_high.assert_called_with("2023-12-25")


# =====================================================================
# compute_gisi Tests
# =====================================================================


class TestComputeGISI:
    """测试 GSISI 投资者情绪指数计算。"""

    def test_gisi_import_error(self):
        """测试导入industry模块失败时抛出异常。"""
        with patch.dict(sys.modules, {"market_data.industry": None}):
            with pytest.raises((ImportError, ModuleNotFoundError)):
                compute_gisi()

    @patch("jk2bt.data_access.get_adapter")
    def test_gisi_empty_index_data(self, mock_get_adapter):
        """测试指数数据为空时返回空DataFrame。"""
        mock_adapter = MagicMock()
        mock_adapter.get_index_daily_raw.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        mock_industry = MagicMock()
        mock_industry.SW_LEVEL1_CODES = {"金融": "801100"}
        mock_industry.get_industry_daily.return_value = None
        with patch.dict(sys.modules, {"market_data.industry": mock_industry}):
            result = compute_gisi()

        assert result.empty

    @patch("jk2bt.data_access.get_adapter")
    def test_gisi_insufficient_industries(self, mock_get_adapter):
        """测试行业数据不足时返回空DataFrame。"""
        index_df = pd.DataFrame(
            {
                "date": pd.date_range("2023-01-01", periods=100, freq="B"),
                "close": 3000 + np.cumsum(np.random.randn(100) * 10),
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_index_daily_raw.return_value = index_df
        mock_get_adapter.return_value = mock_adapter

        mock_industry = MagicMock()
        mock_industry.SW_LEVEL1_CODES = {"金融": "801100"}
        mock_industry.get_industry_daily.return_value = None
        with patch.dict(sys.modules, {"market_data.industry": mock_industry}):
            result = compute_gisi()

        assert result.empty
