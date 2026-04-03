"""
tests/test_bond_option_api.py
可转债与期权 API 测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.market_data.conversion_bond import (
    get_conversion_bond_list,
    calculate_conversion_value,
)
from jk2bt.market_data.option import (
    get_option_list,
    get_option_chain,
)


class TestBondOptionAPI:
    """测试可转债与期权 API"""

    def test_get_conversion_bond_list(self):
        """测试可转债列表"""
        df = get_conversion_bond_list(force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"可转债列表: {len(df)} 条记录")

    def test_calculate_conversion_value(self):
        """测试转股价值计算"""
        value = calculate_conversion_value(100.0, 50.0)
        assert value == 50.0
        print(f"转股价值: {value}")

    def test_get_option_list(self):
        """测试期权列表"""
        result = get_option_list("sse", force_update=True)
        assert hasattr(result, "success")
        assert hasattr(result, "data")
        assert isinstance(result.data, pd.DataFrame)
        print(f"期权列表: {len(result.data)} 条记录")

    def test_get_option_chain(self):
        """测试期权链"""
        result = get_option_chain("510050", force_update=True)
        assert hasattr(result, "success")
        assert hasattr(result, "data")
        assert isinstance(result.data, pd.DataFrame)
        print(f"期权链: {len(result.data)} 条记录")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
