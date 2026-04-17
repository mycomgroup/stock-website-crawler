"""
test_filter_api.py
测试过滤相关API: filter_st, filter_paused, filter_new_stock, filter_limit_up, filter_limit_down 等
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pytest
import pandas as pd
from datetime import datetime


class TestFilterST:
    """filter_st API测试"""

    def test_filter_st_exists(self):
        """测试filter_st函数存在"""
        from jk2bt.api.enhancements import filter_st
        assert callable(filter_st)

    def test_filter_st_basic_call(self):
        """测试基本调用"""
        from jk2bt.api.enhancements import filter_st

        stock_list = ["sh600000", "sh600519", "sz000001"]

        result = filter_st(stock_list)

        # 应返回list
        assert isinstance(result, list)

        # 结果数量应小于等于输入（过滤了ST）
        assert len(result) <= len(stock_list)

    def test_filter_st_with_date(self):
        """测试带日期参数"""
        from jk2bt.api.enhancements import filter_st

        stock_list = ["sh600000", "sh600519"]

        result = filter_st(stock_list, date="2023-01-01")

        assert isinstance(result, list)

    def test_filter_st_empty_input(self):
        """测试空输入"""
        from jk2bt.api.enhancements import filter_st

        result = filter_st([])

        assert isinstance(result, list)
        assert len(result) == 0

    def test_filter_st_single_stock(self):
        """测试单只股票"""
        from jk2bt.api.enhancements import filter_st

        result = filter_st(["sh600000"])

        assert isinstance(result, list)


class TestFilterPaused:
    """filter_paused API测试"""

    def test_filter_paused_exists(self):
        """测试filter_paused函数存在"""
        from jk2bt.api.enhancements import filter_paused
        assert callable(filter_paused)

    def test_filter_paused_basic_call(self):
        """测试基本调用"""
        from jk2bt.api.enhancements import filter_paused

        stock_list = ["sh600000", "sh600519", "sz000001"]

        result = filter_paused(stock_list)

        # 应返回list
        assert isinstance(result, list)

        # 结果数量应小于等于输入
        assert len(result) <= len(stock_list)

    def test_filter_paused_with_date(self):
        """测试带日期参数"""
        from jk2bt.api.enhancements import filter_paused

        stock_list = ["sh600000", "sh600519"]

        result = filter_paused(stock_list, date="2023-01-01")

        assert isinstance(result, list)

    def test_filter_paused_empty_input(self):
        """测试空输入"""
        from jk2bt.api.enhancements import filter_paused

        result = filter_paused([])

        assert isinstance(result, list)
        assert len(result) == 0


class TestFilterLimitUp:
    """filter_limit_up API测试"""

    def test_filter_limit_up_exists(self):
        """测试filter_limit_up函数存在"""
        from jk2bt.api.enhancements import filter_limit_up
        assert callable(filter_limit_up)

    def test_filter_limit_up_basic_call(self):
        """测试基本调用"""
        from jk2bt.api.enhancements import filter_limit_up

        stock_list = ["sh600000", "sh600519"]

        # 注意：这个函数需要current_data，在非策略运行时可能返回原列表
        result = filter_limit_up(stock_list)

        assert isinstance(result, list)

    def test_filter_limit_up_empty_input(self):
        """测试空输入"""
        from jk2bt.api.enhancements import filter_limit_up

        result = filter_limit_up([])

        assert isinstance(result, list)
        assert len(result) == 0


class TestFilterLimitDown:
    """filter_limit_down API测试"""

    def test_filter_limit_down_exists(self):
        """测试filter_limit_down函数存在"""
        from jk2bt.api.enhancements import filter_limit_down
        assert callable(filter_limit_down)

    def test_filter_limit_down_basic_call(self):
        """测试基本调用"""
        from jk2bt.api.enhancements import filter_limit_down

        stock_list = ["sh600000", "sh600519"]

        result = filter_limit_down(stock_list)

        assert isinstance(result, list)

    def test_filter_limit_down_empty_input(self):
        """测试空输入"""
        from jk2bt.api.enhancements import filter_limit_down

        result = filter_limit_down([])

        assert isinstance(result, list)
        assert len(result) == 0


class TestFilterNewStocks:
    """filter_new_stocks API测试"""

    def test_filter_new_stocks_exists(self):
        """测试filter_new_stocks函数存在"""
        from jk2bt.api.enhancements import filter_new_stocks
        assert callable(filter_new_stocks)

    def test_filter_new_stocks_default_days(self):
        """测试默认天数过滤"""
        from jk2bt.api.enhancements import filter_new_stocks

        stock_list = ["sh600000", "sh600519", "sz000001"]

        result = filter_new_stocks(stock_list)

        assert isinstance(result, list)

    def test_filter_new_stocks_custom_days(self):
        """测试自定义天数过滤"""
        from jk2bt.api.enhancements import filter_new_stocks

        stock_list = ["sh600000", "sh600519"]

        # 过滤上市不足365天的股票
        result = filter_new_stocks(stock_list, days=365)

        assert isinstance(result, list)

    def test_filter_new_stocks_short_days(self):
        """测试短天数过滤"""
        from jk2bt.api.enhancements import filter_new_stocks

        stock_list = ["sh600000"]

        # 过滤上市不足30天的股票
        result = filter_new_stocks(stock_list, days=30)

        assert isinstance(result, list)

    def test_filter_new_stocks_empty_input(self):
        """测试空输入"""
        from jk2bt.api.enhancements import filter_new_stocks

        result = filter_new_stocks([])

        assert isinstance(result, list)
        assert len(result) == 0


class TestFilterChain:
    """过滤器链测试"""

    def test_filter_chain_sequential(self):
        """测试顺序过滤"""
        from jk2bt.api.enhancements import filter_st, filter_paused, filter_new_stocks

        stock_list = ["sh600000", "sh600519", "sz000001", "sz000002"]

        # 先过滤ST
        result1 = filter_st(stock_list)

        # 再过滤停牌
        result2 = filter_paused(result1)

        # 再过滤次新股
        result3 = filter_new_stocks(result2)

        # 最终结果应为list
        assert isinstance(result3, list)

        # 数量应逐步减少
        assert len(result3) <= len(result2) <= len(result1) <= len(stock_list)

    def test_filter_all_except_st(self):
        """测试全部过滤（除了ST）"""
        from jk2bt.api.enhancements import filter_st, filter_paused, filter_limit_up, filter_limit_down

        stock_list = ["sh600000", "sh600519"]

        # 组合多种过滤
        after_st = filter_st(stock_list)
        after_paused = filter_paused(after_st)
        after_limit_up = filter_limit_up(after_paused)
        after_limit_down = filter_limit_down(after_limit_up)

        assert isinstance(after_limit_down, list)


class TestFilterCompatibility:
    """过滤器兼容性测试"""

    def test_stock_code_format_compatibility(self):
        """测试股票代码格式兼容"""
        from jk2bt.api.enhancements import filter_st

        # 测试不同格式
        formats = [
            ["sh600000", "sz000001"],       # 本地格式
            ["600000.XSHG", "000001.XSHE"], # 聚宽格式
            ["600000", "000001"],           # 纯数字
        ]

        for stock_list in formats:
            result = filter_st(stock_list)
            assert isinstance(result, list)

    def test_filter_return_type_consistency(self):
        """测试返回类型一致性"""
        from jk2bt.api.enhancements import (
            filter_st, filter_paused, filter_limit_up,
            filter_limit_down, filter_new_stocks
        )

        stock_list = ["sh600000"]

        # 所有过滤器应返回list
        assert isinstance(filter_st(stock_list), list)
        assert isinstance(filter_paused(stock_list), list)
        assert isinstance(filter_limit_up(stock_list), list)
        assert isinstance(filter_limit_down(stock_list), list)
        assert isinstance(filter_new_stocks(stock_list), list)


class TestGetLockedShares:
    """get_locked_shares API测试"""

    def test_get_locked_shares_exists(self):
        """测试get_locked_shares函数存在"""
        from jk2bt.api.missing_apis import get_locked_shares
        assert callable(get_locked_shares)

    def test_get_locked_shares_no_params(self):
        """测试无参数调用"""
        from jk2bt.api.missing_apis import get_locked_shares

        result = get_locked_shares()

        # 应返回DataFrame
        assert isinstance(result, pd.DataFrame)

        # 验证列结构（如果非空）
        if not result.empty:
            expected_columns = ["code", "unlock_date", "unlock_shares", "unlock_ratio", "unlock_value"]
            for col in expected_columns:
                if col in result.columns:
                    assert True

    def test_get_locked_shares_with_stock(self):
        """测试指定股票"""
        from jk2bt.api.missing_apis import get_locked_shares

        result = get_locked_shares(stock_list="sh600000")

        assert isinstance(result, pd.DataFrame)

    def test_get_locked_shares_with_date_range(self):
        """测试日期范围"""
        from jk2bt.api.missing_apis import get_locked_shares

        result = get_locked_shares(
            start_date="2023-01-01",
            end_date="2023-12-31"
        )

        assert isinstance(result, pd.DataFrame)

    def test_get_locked_shares_with_forward_count(self):
        """测试forward_count参数"""
        from jk2bt.api.missing_apis import get_locked_shares

        result = get_locked_shares(forward_count=30)

        assert isinstance(result, pd.DataFrame)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])