"""
test_code_converter.py
股票代码格式转换测试 - 验证三种格式统一转换
"""

import pytest
from jk2bt.utils.code_converter import (
    normalize_to_jq_format,
    normalize_to_akshare_format,
    get_exchange_from_code,
    is_valid_stock_code,
)


class TestNormalizeToJqFormat:
    """测试聚宽格式转换"""

    def test_akshare_sh_format(self):
        """测试 akshare sh 前缀格式"""
        assert normalize_to_jq_format("sh600519") == "600519.XSHG"
        assert normalize_to_jq_format("sh000001") == "000001.XSHG"
        assert normalize_to_jq_format("SH600036") == "600036.XSHG"  # 大写也支持

    def test_akshare_sz_format(self):
        """测试 akshare sz 前缀格式"""
        assert normalize_to_jq_format("sz000858") == "000858.XSHE"
        assert normalize_to_jq_format("sz000333") == "000333.XSHE"
        assert normalize_to_jq_format("SZ000002") == "000002.XSHE"  # 大写也支持

    def test_jq_format(self):
        """测试聚宽格式输入"""
        assert normalize_to_jq_format("600519.XSHG") == "600519.XSHG"
        assert normalize_to_jq_format("000858.XSHE") == "000858.XSHE"

    def test_pure_digit_format(self):
        """测试纯数字格式"""
        assert normalize_to_jq_format("600519") == "600519.XSHG"  # 6开头 -> 上交所
        assert normalize_to_jq_format("000858") == "000858.XSHE"  # 0开头 -> 深交所
        assert normalize_to_jq_format("300001") == "300001.XSHE"  # 3开头 -> 深交所

    def test_short_code_padding(self):
        """测试短代码补零"""
        assert normalize_to_jq_format("sh600") == "000600.XSHG"  # sh前缀 -> 上交所
        assert normalize_to_jq_format("sz1") == "000001.XSHE"    # sz前缀 -> 深交所
        assert normalize_to_jq_format("600") == "000600.XSHE"    # 补零后0开头 -> 深交所
        assert normalize_to_jq_format("6") == "000006.XSHE"      # 补零后0开头 -> 深交所
        assert normalize_to_jq_format("sh6") == "000006.XSHG"    # sh前缀 -> 上交所

    def test_none_input(self):
        """测试 None 输入"""
        assert normalize_to_jq_format(None) is None

    def test_whitespace(self):
        """测试带空格的输入"""
        assert normalize_to_jq_format(" sh600519 ") == "600519.XSHG"


class TestNormalizeToAkshareFormat:
    """测试 akshare 格式转换"""

    def test_jq_to_akshare(self):
        """测试聚宽格式转 akshare"""
        assert normalize_to_akshare_format("600519.XSHG") == "sh600519"
        assert normalize_to_akshare_format("000858.XSHE") == "sz000858"

    def test_akshare_to_akshare(self):
        """测试 akshare 格式保持"""
        assert normalize_to_akshare_format("sh600519") == "sh600519"
        assert normalize_to_akshare_format("sz000858") == "sz000858"

    def test_digit_to_akshare(self):
        """测试纯数字转 akshare"""
        assert normalize_to_akshare_format("600519") == "sh600519"
        assert normalize_to_akshare_format("000858") == "sz000858"


class TestGetExchangeFromCode:
    """测试交易所判断"""

    def test_sh_exchange(self):
        """测试上交所代码"""
        assert get_exchange_from_code("sh600519") == "XSHG"
        assert get_exchange_from_code("600519.XSHG") == "XSHG"
        assert get_exchange_from_code("600519") == "XSHG"

    def test_sz_exchange(self):
        """测试深交所代码"""
        assert get_exchange_from_code("sz000858") == "XSHE"
        assert get_exchange_from_code("000858.XSHE") == "XSHE"
        assert get_exchange_from_code("000858") == "XSHE"


class TestIsValidStockCode:
    """测试股票代码有效性验证"""

    def test_valid_akshare_format(self):
        """测试有效 akshare 格式"""
        assert is_valid_stock_code("sh600519") is True
        assert is_valid_stock_code("sz000858") is True

    def test_valid_jq_format(self):
        """测试有效聚宽格式"""
        assert is_valid_stock_code("600519.XSHG") is True
        assert is_valid_stock_code("000858.XSHE") is True

    def test_valid_digit_format(self):
        """测试有效纯数字格式"""
        assert is_valid_stock_code("600519") is True
        assert is_valid_stock_code("000858") is True

    def test_invalid_codes(self):
        """测试无效代码"""
        assert is_valid_stock_code(None) is False
        assert is_valid_stock_code("") is False
        assert is_valid_stock_code("abc") is False
        assert is_valid_stock_code("123") is False  # 太短
        assert is_valid_stock_code("sh123") is False  # 代码部分不是数字