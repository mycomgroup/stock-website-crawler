"""
tests/unit/api/test_concept_api.py
概念板块 API 单元测试

测试覆盖:
1. get_concepts - 获取概念板块列表
2. get_concept_stocks - 获取概念板块成分股
3. get_concept - 获取股票所属概念
4. get_all_concepts - 获取所有概念板块及成分股
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


class TestGetConcepts:
    """测试获取概念板块列表"""

    @patch("jk2bt.api.concept.get_concept_list")
    def test_get_concepts_dataframe(self, mock_get_list):
        mock_get_list.return_value = pd.DataFrame(
            {
                "code": ["AI", "NEW_ENERGY"],
                "name": ["人工智能", "新能源汽车"],
            }
        )

        from jk2bt.api.concept import get_concepts

        result = get_concepts(df=True)

        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns
        assert "name" in result.columns

    @patch("jk2bt.api.concept.get_concept_list")
    def test_get_concepts_dict(self, mock_get_list):
        mock_get_list.return_value = pd.DataFrame(
            {
                "code": ["AI", "NEW_ENERGY"],
                "name": ["人工智能", "新能源汽车"],
            }
        )

        from jk2bt.api.concept import get_concepts

        result = get_concepts(df=False)

        assert isinstance(result, dict)
        assert "AI" in result
        assert result["AI"] == "人工智能"

    @patch("jk2bt.api.concept.get_concept_list")
    def test_get_concepts_empty(self, mock_get_list):
        mock_get_list.return_value = pd.DataFrame()

        from jk2bt.api.concept import get_concepts

        result = get_concepts()
        assert isinstance(result, pd.DataFrame)


class TestGetConceptStocks:
    """测试获取概念板块成分股"""

    @patch("jk2bt.api.concept._get_concept_stocks")
    def test_get_concept_stocks(self, mock_get_stocks):
        mock_get_stocks.return_value = ["600519.XSHG", "000001.XSHE"]

        from jk2bt.api.concept import get_concept_stocks

        result = get_concept_stocks("AI")

        assert isinstance(result, list)
        assert len(result) == 2


class TestGetConcept:
    """测试获取股票所属概念"""

    @patch("jk2bt.api.concept.get_stock_concepts")
    def test_get_concept(self, mock_get_stock_concepts):
        mock_get_stock_concepts.return_value = ["人工智能", "新能源汽车"]

        from jk2bt.api.concept import get_concept

        result = get_concept("600519.XSHG")

        assert isinstance(result, list)
        assert "人工智能" in result


class TestGetAllConcepts:
    """测试获取所有概念板块及成分股"""

    @patch("jk2bt.api.concept.get_concept_list")
    @patch("jk2bt.api.concept.get_concept_stocks")
    def test_get_all_concepts(self, mock_get_stocks, mock_get_list):
        mock_get_list.return_value = pd.DataFrame(
            {
                "code": ["AI"],
                "name": ["人工智能"],
            }
        )
        mock_get_stocks.return_value = ["600519.XSHG"]

        from jk2bt.api.concept import get_all_concepts

        result = get_all_concepts()

        assert isinstance(result, pd.DataFrame)
        assert "concept_code" in result.columns
        assert "concept_name" in result.columns
        assert "stock_code" in result.columns


class TestConceptModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.concept import __all__

        expected = [
            "get_concepts",
            "get_concept_stocks",
            "get_concept",
            "get_all_concepts",
            "get_concepts_jq",
            "get_concept_stocks_jq",
            "get_concept_jq",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
