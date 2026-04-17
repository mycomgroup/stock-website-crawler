"""
test_financials.py
财务指标字段补充模块测试。

测试覆盖：
- INDICATOR_FIELD_MAPPING 字段映射
- get_indicator_data 获取财务指标数据
- get_indicator_field_description 获取字段描述
- get_supported_indicator_fields 获取支持的字段
- get_indicator_batch 批量获取
- get_indicator_ranking 指标排名
- filter_by_indicator 按指标筛选
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestIndicatorFieldMapping:
    """测试指标字段映射。"""

    def test_mapping_not_empty(self):
        """测试映射不为空。"""
        from jk2bt.analysis.factors.financials import INDICATOR_FIELD_MAPPING

        assert len(INDICATOR_FIELD_MAPPING) > 0

    def test_required_fields_present(self):
        """测试必需字段存在。"""
        from jk2bt.analysis.factors.financials import INDICATOR_FIELD_MAPPING

        required_fields = ["roe", "roa", "gross_profit_margin", "net_profit_margin"]

        for field in required_fields:
            assert field in INDICATOR_FIELD_MAPPING

    def test_field_structure(self):
        """测试字段结构。"""
        from jk2bt.analysis.factors.financials import INDICATOR_FIELD_MAPPING

        for field, info in INDICATOR_FIELD_MAPPING.items():
            assert "akshare_field" in info
            assert "description" in info
            assert "data_source" in info


class TestGetIndicatorFieldDescription:
    """测试获取字段描述。"""

    def test_known_field(self):
        """测试已知字段。"""
        from jk2bt.analysis.factors.financials import get_indicator_field_description

        desc = get_indicator_field_description("roe")
        assert desc is not None
        assert isinstance(desc, str)

    def test_unknown_field(self):
        """测试未知字段。"""
        from jk2bt.analysis.factors.financials import get_indicator_field_description

        desc = get_indicator_field_description("nonexistent_field")
        assert desc is None


class TestGetSupportedIndicatorFields:
    """测试获取支持的字段列表。"""

    def test_returns_list(self):
        """测试返回列表。"""
        from jk2bt.analysis.factors.financials import get_supported_indicator_fields

        fields = get_supported_indicator_fields()

        assert isinstance(fields, list)
        assert len(fields) > 0

    def test_contains_expected_fields(self):
        """测试包含预期字段。"""
        from jk2bt.analysis.factors.financials import get_supported_indicator_fields

        fields = get_supported_indicator_fields()

        assert "roe" in fields
        assert "roa" in fields
        assert "gross_profit_margin" in fields


class TestGetIndicatorData:
    """测试获取财务指标数据。"""

    def test_no_symbol(self):
        """测试无symbol参数。"""
        from jk2bt.analysis.factors.financials import get_indicator_data

        result = get_indicator_data(None)
        assert result.empty

    def test_format_stock_symbol_mock(self, monkeypatch):
        """测试股票代码格式化。"""
        from jk2bt.analysis.factors.financials import get_indicator_data

        monkeypatch.setattr(
            "jk2bt.analysis.factors.financials.format_stock_symbol_for_akshare",
            lambda s: "600519",
        )
        monkeypatch.setattr(
            "jk2bt.analysis.factors.financials._resolve_cache_dir", lambda s: "/tmp"
        )

        result = get_indicator_data("sh600519")
        assert isinstance(result, pd.DataFrame)

    def test_fields_filter(self, monkeypatch):
        """测试字段过滤。"""
        from jk2bt.analysis.factors.financials import get_indicator_data

        monkeypatch.setattr(
            "jk2bt.analysis.factors.financials.format_stock_symbol_for_akshare",
            lambda s: "600519",
        )
        monkeypatch.setattr(
            "jk2bt.analysis.factors.financials._resolve_cache_dir", lambda s: "/tmp"
        )

        result = get_indicator_data("sh600519", fields=["roe"])
        assert isinstance(result, pd.DataFrame)


class TestGetIndicatorBatch:
    """测试批量获取财务指标。"""

    def test_empty_symbols(self):
        """测试空股票列表。"""
        from jk2bt.analysis.factors.financials import get_indicator_batch

        result = get_indicator_batch([])
        assert result.empty

    def test_returns_dataframe(self):
        """测试返回DataFrame。"""
        from jk2bt.analysis.factors.financials import get_indicator_batch

        with patch("jk2bt.analysis.factors.financials.get_indicator_data") as mock_get:
            mock_get.return_value = pd.DataFrame(
                {
                    "code": ["600519"],
                    "roe": [15.0],
                }
            )

            result = get_indicator_batch(["sh600519"], fields=["roe"])

            assert isinstance(result, pd.DataFrame)


class TestGetIndicatorRanking:
    """测试指标排名。"""

    def test_empty_result(self):
        """测试空结果。"""
        from jk2bt.analysis.factors.financials import get_indicator_ranking

        with patch(
            "jk2bt.analysis.factors.financials.get_indicator_batch"
        ) as mock_batch:
            mock_batch.return_value = pd.DataFrame()

            result = get_indicator_ranking(["sh600519"], "roe")

            assert result.empty

    def test_ranking_result(self):
        """测试排名结果。"""
        from jk2bt.analysis.factors.financials import get_indicator_ranking

        with patch(
            "jk2bt.analysis.factors.financials.get_indicator_batch"
        ) as mock_batch:
            mock_batch.return_value = pd.DataFrame(
                {
                    "roe": [10.0, 15.0, 20.0],
                },
                index=["600001", "600002", "600003"],
            )

            result = get_indicator_ranking(
                ["sh600001", "sh600002", "sh600003"], "roe", top_n=2
            )

            assert isinstance(result, pd.DataFrame)
            assert len(result) <= 2


class TestFilterByIndicator:
    """测试按指标筛选。"""

    def test_returns_symbols(self):
        """测试返回股票列表。"""
        from jk2bt.analysis.factors.financials import filter_by_indicator

        with patch(
            "jk2bt.analysis.factors.financials.get_indicator_batch"
        ) as mock_batch:
            mock_batch.return_value = pd.DataFrame(
                {
                    "roe": [10.0, 15.0, 20.0],
                },
                index=["600001", "600002", "600003"],
            )

            result = filter_by_indicator(
                ["sh600001", "sh600002", "sh600003"], "roe", min_value=15.0
            )

            assert isinstance(result, list)

    def test_no_filter_result(self):
        """测试无筛选条件返回原列表。"""
        from jk2bt.analysis.factors.financials import filter_by_indicator

        with patch(
            "jk2bt.analysis.factors.financials.get_indicator_batch"
        ) as mock_batch:
            mock_batch.return_value = pd.DataFrame()

            symbols = ["sh600001", "sh600002"]
            result = filter_by_indicator(symbols, "roe")

            assert result == symbols


class TestFinancialsFindDateColumn:
    """测试日期列查找函数。"""

    def test_find_date_column(self):
        """测试查找日期列。"""
        from jk2bt.analysis.factors.financials import _find_date_column

        df = pd.DataFrame(
            {
                "日期": ["2023-01-01", "2023-01-02"],
                "value": [1, 2],
            }
        )

        col = _find_date_column(df)
        assert col == "日期"

    def test_find_date_column_not_found(self):
        """测试未找到日期列。"""
        from jk2bt.analysis.factors.financials import _find_date_column

        df = pd.DataFrame(
            {
                "value1": [1, 2],
                "value2": [3, 4],
            }
        )

        col = _find_date_column(df)
        assert col is None
