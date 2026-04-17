"""
test_securities_utils.py
securities_utils.py 单元测试

测试场景覆盖:
1. _find_date_column 日期列查找
2. _resolve_cache_dir 缓存目录解析
3. _stock_code_to_jq 股票代码转聚宽格式
"""

import pytest
import pandas as pd
import os
from jk2bt.api.securities_utils import (
    _find_date_column,
    _stock_code_to_jq,
)
from jk2bt.utils.date_utils import _resolve_cache_dir


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


class TestResolveCacheDir:
    """测试 _resolve_cache_dir 缓存目录解析"""

    def test_resolve_absolute_path(self):
        """测试绝对路径"""
        abs_path = "/tmp/cache"
        result = _resolve_cache_dir(abs_path)
        assert result == abs_path

    def test_resolve_relative_path(self):
        """测试相对路径"""
        result = _resolve_cache_dir("my_cache")
        assert result.endswith("my_cache")
        assert os.path.isabs(result)


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


class TestFormatIndexCode:
    """测试 _format_index_code 指数代码格式化"""

    def test_hs300_variants(self):
        """测试沪深300各种格式"""
        assert _format_index_code("000300") == "000300"
        assert _format_index_code("sh000300") == "000300"
        assert _format_index_code("000300.XSHG") == "000300"
        assert _format_index_code("hs300") == "000300"
        assert _format_index_code("沪深300") == "000300"

    def test_cyb_variants(self):
        """测试创业板各种格式"""
        assert _format_index_code("399006") == "399006"
        assert _format_index_code("sz399006") == "399006"
        assert _format_index_code("399006.XSHE") == "399006"
        assert _format_index_code("cyb") == "399006"
        assert _format_index_code("创业板") == "399006"

    def test_zeros_padding(self):
        """测试零填充"""
        assert _format_index_code("300") == "000300"
        assert _format_index_code("6") == "000006"

    def test_399_preserved(self):
        """测试399开头保持不变"""
        assert _format_index_code("399001") == "399001"


class TestNormalizeIndexWeights:
    """测试 _normalize_index_weights 指数权重标准化"""

    def test_normalize_basic(self):
        """测试基本标准化"""
        df = pd.DataFrame({"成分券代码": ["600519", "000001"], "权重": [0.6, 0.4]})
        result = _normalize_index_weights(df)
        assert "code" in result.columns
        assert "weight" in result.columns

    def test_normalize_with_aliases(self):
        """测试列名别名"""
        df = pd.DataFrame({"证券代码": ["600519", "000001"], "weight": [0.6, 0.4]})
        result = _normalize_index_weights(df)
        assert "code" in result.columns
        assert "weight" in result.columns

    def test_normalize_converts_jq_codes(self):
        """测试转换聚宽代码"""
        df = pd.DataFrame({"成分券代码": ["600519", "000001"], "权重": [0.5, 0.5]})
        result = _normalize_index_weights(df)
        assert result.index[0] == "600519.XSHG"
        assert result.index[1] == "000001.XSHE"

    def test_normalize_empty(self):
        """测试空DataFrame"""
        df = pd.DataFrame()
        result = _normalize_index_weights(df)
        assert result.empty


class TestSupportedIndexes:
    """测试 SUPPORTED_INDEXES 常量"""

    def test_not_empty(self):
        """测试不为空"""
        assert len(SUPPORTED_INDEXES) > 0

    def test_contains_key_indices(self):
        """测试包含关键指数"""
        assert "000300" in SUPPORTED_INDEXES
        assert "399006" in SUPPORTED_INDEXES


class TestDateColumnCandidates:
    """测试 _DATE_COLUMN_CANDIDATES 常量"""

    def test_not_empty(self):
        """测试不为空"""
        assert len(_DATE_COLUMN_CANDIDATES) > 0

    def test_has_market_category(self):
        """测试有market类别"""
        assert "market" in _DATE_COLUMN_CANDIDATES

    def test_has_financial_category(self):
        """测试有financial类别"""
        assert "financial" in _DATE_COLUMN_CANDIDATES
