"""
test_code_converter.py
股票代码格式转换测试 - 验证三种格式统一转换

注: 原 code_converter 模块已合并到 symbol 模块，此测试更新为直接测试 symbol 模块。
"""

import pytest
from jk2bt.utils.symbol import (
    ak_code_to_jq,
    jq_code_to_ak,
    get_symbol_prefix,
    is_valid_stock_code,
)


def _get_exchange_from_code(symbol: str) -> str:
    """兼容测试: 等同于原 code_converter.get_exchange_from_code"""
    prefix = get_symbol_prefix(symbol)
    return "XSHG" if prefix == "sh" else "XSHE"


class TestNormalizeToJqFormat:
    """测试聚宽格式转换 (ak_code_to_jq)"""

    def test_akshare_sh_format(self):
        """测试 akshare sh 前缀格式"""
        assert ak_code_to_jq("sh600519") == "600519.XSHG"
        assert ak_code_to_jq("sh000001") == "000001.XSHG"
        assert ak_code_to_jq("SH600036") == "600036.XSHG"

    def test_akshare_sz_format(self):
        """测试 akshare sz 前缀格式"""
        assert ak_code_to_jq("sz000858") == "000858.XSHE"
        assert ak_code_to_jq("sz000333") == "000333.XSHE"
        assert ak_code_to_jq("SZ000002") == "000002.XSHE"

    def test_jq_format(self):
        """测试聚宽格式输入"""
        assert ak_code_to_jq("600519.XSHG") == "600519.XSHG"
        assert ak_code_to_jq("000858.XSHE") == "000858.XSHE"

    def test_pure_digit_format(self):
        """测试纯数字格式"""
        assert ak_code_to_jq("600519") == "600519.XSHG"
        assert ak_code_to_jq("000858") == "000858.XSHE"
        assert ak_code_to_jq("300001") == "300001.XSHE"

    def test_short_code_padding(self):
        """测试短代码补零"""
        assert ak_code_to_jq("sh600") == "000600.XSHG"
        assert ak_code_to_jq("sz1") == "000001.XSHE"
        assert ak_code_to_jq("600") == "000600.XSHE"
        assert ak_code_to_jq("6") == "000006.XSHE"
        assert ak_code_to_jq("sh6") == "000006.XSHG"

    def test_none_input(self):
        """测试 None 输入"""
        assert ak_code_to_jq(None) is None

    def test_whitespace(self):
        """测试带空格的输入"""
        assert ak_code_to_jq(" sh600519 ") == "600519.XSHG"


class TestNormalizeToAkshareFormat:
    """测试 akshare 格式转换 (jq_code_to_ak)"""

    def test_jq_to_akshare(self):
        """测试聚宽格式转 akshare"""
        assert jq_code_to_ak("600519.XSHG") == "sh600519"
        assert jq_code_to_ak("000858.XSHE") == "sz000858"

    def test_akshare_to_akshare(self):
        """测试 akshare 格式保持"""
        assert jq_code_to_ak("sh600519") == "sh600519"
        assert jq_code_to_ak("sz000858") == "sz000858"

    def test_digit_to_akshare(self):
        """测试纯数字转 akshare"""
        assert jq_code_to_ak("600519") == "sh600519"
        assert jq_code_to_ak("000858") == "sz000858"


class TestGetExchangeFromCode:
    """测试交易所判断"""

    def test_sh_exchange(self):
        """测试上交所代码"""
        assert _get_exchange_from_code("sh600519") == "XSHG"
        assert _get_exchange_from_code("600519.XSHG") == "XSHG"
        assert _get_exchange_from_code("600519") == "XSHG"

    def test_sz_exchange(self):
        """测试深交所代码"""
        assert _get_exchange_from_code("sz000858") == "XSHE"
        assert _get_exchange_from_code("000858.XSHE") == "XSHE"
        assert _get_exchange_from_code("000858") == "XSHE"


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
        assert is_valid_stock_code("123") is False
        assert is_valid_stock_code("sh123") is False
