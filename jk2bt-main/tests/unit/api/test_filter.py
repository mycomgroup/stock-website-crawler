"""
tests/unit/api/test_filter.py
过滤 API 单元测试

测试覆盖：
- filter_st / filter_paused / filter_limit_up / filter_limit_down
- filter_new_stocks / filter_new_stock / filter_st_stock / filter_paused_stock
- apply_common_filters
- 模块导入与可调用性
"""

import pytest
import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"),
)


class TestFilterImports:
    """过滤函数导入测试"""

    def test_filter_st_importable(self):
        from jk2bt.api.filter import filter_st
        assert callable(filter_st)

    def test_filter_paused_importable(self):
        from jk2bt.api.filter import filter_paused
        assert callable(filter_paused)

    def test_filter_limit_up_importable(self):
        from jk2bt.api.filter import filter_limit_up
        assert callable(filter_limit_up)

    def test_filter_limit_down_importable(self):
        from jk2bt.api.filter import filter_limit_down
        assert callable(filter_limit_down)

    def test_filter_new_stocks_importable(self):
        from jk2bt.api.filter import filter_new_stocks
        assert callable(filter_new_stocks)

    def test_filter_new_stock_importable(self):
        from jk2bt.api.filter import filter_new_stock
        assert callable(filter_new_stock)

    def test_filter_st_stock_importable(self):
        from jk2bt.api.filter import filter_st_stock
        assert callable(filter_st_stock)

    def test_filter_paused_stock_importable(self):
        from jk2bt.api.filter import filter_paused_stock
        assert callable(filter_paused_stock)

    def test_apply_common_filters_importable(self):
        from jk2bt.api.filter import apply_common_filters
        assert callable(apply_common_filters)

    def test_get_dividend_ratio_filter_list_importable(self):
        from jk2bt.api.filter import get_dividend_ratio_filter_list
        assert callable(get_dividend_ratio_filter_list)

    def test_get_margine_stocks_importable(self):
        from jk2bt.api.filter import get_margine_stocks
        assert callable(get_margine_stocks)


class TestFilterFromApiInit:
    """从 src.api 顶层导入过滤函数"""

    def test_filter_st_from_api(self):
        from jk2bt.api import filter_st
        assert callable(filter_st)

    def test_filter_paused_from_api(self):
        from jk2bt.api import filter_paused
        assert callable(filter_paused)

    def test_filter_limit_up_from_api(self):
        from jk2bt.api import filter_limit_up
        assert callable(filter_limit_up)

    def test_filter_limit_down_from_api(self):
        from jk2bt.api import filter_limit_down
        assert callable(filter_limit_down)

    def test_filter_new_stocks_from_api(self):
        from jk2bt.api import filter_new_stocks
        assert callable(filter_new_stocks)


class TestFilterReturnTypes:
    """过滤函数返回类型测试（空列表输入）"""

    def test_filter_st_empty_list(self):
        from jk2bt.api.filter import filter_st
        result = filter_st([])
        assert isinstance(result, list)
        assert result == []

    def test_filter_paused_empty_list(self):
        from jk2bt.api.filter import filter_paused
        result = filter_paused([])
        assert isinstance(result, list)
        assert result == []

    def test_filter_limit_up_empty_list(self):
        from jk2bt.api.filter import filter_limit_up
        result = filter_limit_up([])
        assert isinstance(result, list)
        assert result == []

    def test_filter_limit_down_empty_list(self):
        from jk2bt.api.filter import filter_limit_down
        result = filter_limit_down([])
        assert isinstance(result, list)
        assert result == []

    def test_filter_new_stocks_empty_list(self):
        from jk2bt.api.filter import filter_new_stocks
        result = filter_new_stocks([])
        assert isinstance(result, list)
        assert result == []

    def test_filter_new_stock_empty_list(self):
        from jk2bt.api.filter import filter_new_stock
        result = filter_new_stock([])
        assert isinstance(result, list)
        assert result == []

    def test_filter_st_stock_empty_list(self):
        from jk2bt.api.filter import filter_st_stock
        result = filter_st_stock([])
        assert isinstance(result, list)
        assert result == []

    def test_filter_paused_stock_empty_list(self):
        from jk2bt.api.filter import filter_paused_stock
        result = filter_paused_stock([])
        assert isinstance(result, list)
        assert result == []

    def test_apply_common_filters_empty_list(self):
        from jk2bt.api.filter import apply_common_filters
        result = apply_common_filters([])
        assert isinstance(result, list)
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
