"""
tests/test_index_industry_api.py
指数成分股与行业 API 测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.market_data.index_components import (
    get_index_components,
    get_index_weights,
)
from jk2bt.market_data.industry_sw import (
    get_industry_category,
    get_industry_stocks,
)


class TestIndexIndustryAPI:
    """测试指数成分股与行业 API"""

    def test_get_index_components(self):
        """测试指数成分股"""
        df = get_index_components("000300", force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"沪深300成分股: {len(df)} 条记录")

    def test_get_index_weights(self):
        """测试指数权重"""
        df = get_index_weights("000016", force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"上证50权重: {len(df)} 条记录")

    def test_get_industry_category(self):
        """测试行业分类"""
        df = get_industry_category("600000", force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"行业分类: {len(df)} 条记录")

    def test_get_industry_stocks(self):
        """测试行业成分股"""
        df = get_industry_stocks("银行", force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"银行业成分股: {len(df)} 条记录")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
