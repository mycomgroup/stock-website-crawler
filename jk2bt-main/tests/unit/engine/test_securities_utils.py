"""
test_securities_utils.py
securities_utils.py 单元测试

测试场景覆盖:
1. _find_date_column 日期列查找
2. _stock_code_to_jq 股票代码转聚宽格式
"""

import pytest
import pandas as pd
from jk2bt.api.securities_utils import (
    _find_date_column,
    _stock_code_to_jq,
)


class TestFindDateColumn:
    """测试 _find_date_column 日期列查找"""

    def test_find_date_column_basic(self):
        """测试基本查找"""
        df = pd.DataFrame({"日期": [1, 2, 3], "close": [10, 20, 30]})
        result = _find_date_column(df, "market")
        assert result == "日期"

    def test_find_date_column_trade_date(self):
        """测试trade_date列"""
        df = pd.DataFrame({"trade_date": [1, 2, 3], "close": [10, 20, 30]})
        result = _find_date_column(df, "market")
        assert result == "trade_date"

    def test_find_date_column_not_found(self):
        """测试未找到返回None"""
        df = pd.DataFrame({"close": [10, 20, 30]})
        result = _find_date_column(df, "market")
        assert result is None

    def test_find_date_column_financial(self):
        """测试财务数据日期列"""
        df = pd.DataFrame({"报告期": [1, 2, 3], "close": [10, 20, 30]})
        result = _find_date_column(df, "financial")
        assert result == "报告期"

    def test_find_date_column_common(self):
        """测试通用日期列"""
        df = pd.DataFrame({"datetime": [1, 2, 3], "close": [10, 20, 30]})
        result = _find_date_column(df, "common")
        assert result == "datetime"


class TestStockCodeToJQ:
    """测试 _stock_code_to_jq 股票代码转聚宽格式"""

    def test_shanghai_code(self):
        """测试上海股票代码"""
        assert _stock_code_to_jq("600519") == "600519.XSHG"
        assert _stock_code_to_jq("600000") == "600000.XSHG"

    def test_shenzhen_code(self):
        """测试深圳股票代码"""
        assert _stock_code_to_jq("000001") == "000001.XSHE"
        assert _stock_code_to_jq("002594") == "002594.XSHE"

    def test_strips_whitespace(self):
        """测试去除空白"""
        assert _stock_code_to_jq(" 600519 ") == "600519.XSHG"

    def test_converts_to_string(self):
        """测试转换为字符串"""
        assert _stock_code_to_jq(600519) == "600519.XSHG"
