"""
test_symbol.py
符号工具模块测试（补充 symbol.py 中其他函数的测试）

注: symbol.py 中的 code_converter 相关函数测试已在 test_code_converter.py 中
本文件测试剩余函数: extract_code_num, normalize_symbol, is_gem_or_star, calculate_limit_price
"""

import pytest
from jk2bt.utils.symbol import (
    extract_code_num,
    normalize_symbol,
    normalize_code,
    get_symbol_prefix,
    is_gem_or_star,
    calculate_limit_price,
    format_stock_symbol,
)


class TestExtractCodeNum:
    """测试股票代码提取"""

    def test_extract_from_sh_format(self):
        """测试从 sh 格式提取"""
        assert extract_code_num("sh600519") == "600519"

    def test_extract_from_sz_format(self):
        """测试从 sz 格式提取"""
        assert extract_code_num("sz000858") == "000858"

    def test_extract_from_jq_format(self):
        """测试从聚宽格式提取"""
        assert extract_code_num("600519.XSHG") == "600519"
        assert extract_code_num("000858.XSHE") == "000858"

    def test_extract_from_pure_digit(self):
        """测试从纯数字提取"""
        assert extract_code_num("600519") == "600519"
        assert extract_code_num("1") == "000001"

    def test_extract_from_bj_format(self):
        """测试从 bj 格式提取"""
        assert extract_code_num("bj430001") == "430001"

    def test_extract_none_returns_none(self):
        """测试 None 输入"""
        assert extract_code_num(None) is None


class TestNormalizeSymbol:
    """测试符号标准化"""

    def test_normalize_sh(self):
        """测试 sh 格式标准化"""
        assert normalize_symbol("sh600000") == "600000"

    def test_normalize_sz(self):
        """测试 sz 格式标准化"""
        assert normalize_symbol("sz000001") == "000001"

    def test_normalize_jq(self):
        """测试聚宽格式标准化"""
        assert normalize_symbol("600000.XSHG") == "600000"

    def test_normalize_of_fund(self):
        """测试场外基金格式"""
        assert normalize_symbol("159001.OF") == "159001"

    def test_normalize_ccfx_futures(self):
        """测试期货格式保留原样"""
        result = normalize_symbol("IF2301.CCFX")
        assert result == "IF2301"


class TestNormalizeCode:
    """测试 normalize_code 别名"""

    def test_normalize_code_alias(self):
        """测试 normalize_code 是 normalize_symbol 的别名"""
        assert normalize_code("sh600000") == normalize_symbol("sh600000")


class TestGetSymbolPrefix:
    """测试获取股票前缀"""

    def test_sh_prefix(self):
        """测试上交所前缀"""
        assert get_symbol_prefix("600519") == "sh"
        assert get_symbol_prefix("600519.XSHG") == "sh"
        assert get_symbol_prefix("sh600519") == "sh"

    def test_sz_prefix(self):
        """测试深交所前缀"""
        assert get_symbol_prefix("000001") == "sz"
        assert get_symbol_prefix("000001.XSHE") == "sz"
        assert get_symbol_prefix("sz000001") == "sz"

    def test_gem_prefix(self):
        """测试创业板前缀"""
        assert get_symbol_prefix("300001") == "sz"
        assert get_symbol_prefix("300750") == "sz"


class TestIsGemOrStar:
    """测试创业板/科创板判断"""

    def test_gem_code(self):
        """测试创业板代码"""
        assert is_gem_or_star("300001") is True
        assert is_gem_or_star("300750") is True
        assert is_gem_or_star("sz300001") is True

    def test_star_code(self):
        """测试科创板代码"""
        assert is_gem_or_star("688001") is True
        assert is_gem_or_star("sh688001") is True

    def test_main_board(self):
        """测试主板代码"""
        assert is_gem_or_star("600000") is False
        assert is_gem_or_star("000001") is False
        assert is_gem_or_star("sh600000") is False
        assert is_gem_or_star("sz000001") is False


class TestCalculateLimitPrice:
    """测试涨跌停价计算"""

    def test_main_board_up_limit(self):
        """测试主板涨停价（10%）"""
        prev_close = 100.0
        result = calculate_limit_price(prev_close, "600000", direction="up")
        assert result == 110.0

    def test_main_board_down_limit(self):
        """测试主板跌停价（10%）"""
        prev_close = 100.0
        result = calculate_limit_price(prev_close, "600000", direction="down")
        assert result == 90.0

    def test_gem_up_limit(self):
        """测试创业板涨停价（20%）"""
        prev_close = 50.0
        result = calculate_limit_price(prev_close, "300001", direction="up")
        assert result == 60.0

    def test_gem_down_limit(self):
        """测试创业板跌停价（20%）"""
        prev_close = 50.0
        result = calculate_limit_price(prev_close, "300001", direction="down")
        assert result == 40.0

    def test_star_up_limit(self):
        """测试科创板涨停价（20%）"""
        prev_close = 100.0
        result = calculate_limit_price(prev_close, "688001", direction="up")
        assert result == 120.0

    def test_invalid_prev_close_returns_none(self):
        """测试无效前收盘价返回 None"""
        assert calculate_limit_price(None, "600000") is None
        assert calculate_limit_price(0, "600000") is None
        assert calculate_limit_price(-10, "600000") is None

    def test_with_prefix(self):
        """测试带前缀的代码"""
        prev_close = 100.0
        result = calculate_limit_price(prev_close, "sh600000", direction="up")
        assert result == 110.0


class TestFormatStockSymbol:
    """测试股票代码格式化"""

    def test_format_sh(self):
        """测试 sh 格式"""
        assert format_stock_symbol("sh600000") == "600000"

    def test_format_sz(self):
        """测试 sz 格式"""
        assert format_stock_symbol("sz000001") == "000001"

    def test_format_jq_sh(self):
        """测试聚宽上交所格式"""
        assert format_stock_symbol("600000.XSHG") == "600000"

    def test_format_jq_sz(self):
        """测试聚赢深交所格式"""
        assert format_stock_symbol("000001.XSHE") == "000001"

    def test_format_pure_digit(self):
        """测试纯数字格式"""
        assert format_stock_symbol("600000") == "600000"

    def test_format_of_fund(self):
        """测试场外基金"""
        assert format_stock_symbol("159001.OF") == "159001"

    def test_format_ccfx_futures(self):
        """测试期货保留原始格式"""
        assert format_stock_symbol("IF2301.CCFX") == "IF2301"

    def test_format_none(self):
        """测试 None 输入"""
        assert format_stock_symbol(None) is None

    def test_format_padding(self):
        """测试短码补零"""
        assert format_stock_symbol("sh6") == "000006"
        assert format_stock_symbol("1") == "000001"
