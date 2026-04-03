"""
tests/unit/utils/test_symbol_utils.py
symbol_utils 单元测试

测试 src.api._internal.symbol_utils 中的 4 个公开函数：
1. normalize_symbol  - 统一股票代码为 6 位数字
2. get_symbol_prefix - 获取 sh/sz 前缀
3. is_gem_or_star    - 判断创业板/科创板
4. calculate_limit_price - 计算涨跌停价
"""

import pytest
import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"),
)

from jk2bt.api._internal.symbol_utils import (
    normalize_symbol,
    get_symbol_prefix,
    is_gem_or_star,
    calculate_limit_price,
)


# ---------------------------------------------------------------------------
# 1. normalize_symbol
# ---------------------------------------------------------------------------

class TestNormalizeSymbol:
    """normalize_symbol：统一股票代码为 6 位数字"""

    def test_sh_prefix_stripped(self):
        assert normalize_symbol("sh600000") == "600000"

    def test_sz_prefix_stripped(self):
        assert normalize_symbol("sz000001") == "000001"

    def test_xshg_suffix_stripped(self):
        assert normalize_symbol("600519.XSHG") == "600519"

    def test_xshe_suffix_stripped(self):
        assert normalize_symbol("000001.XSHE") == "000001"

    def test_pure_6_digit_unchanged(self):
        assert normalize_symbol("600000") == "600000"
        assert normalize_symbol("000001") == "000001"

    def test_short_code_zero_padded(self):
        # 5 位补零到 6 位
        assert normalize_symbol("60000") == "060000"

    def test_gem_code(self):
        assert normalize_symbol("300750.XSHE") == "300750"

    def test_star_code(self):
        assert normalize_symbol("688981.XSHG") == "688981"

    def test_sh_prefix_gem(self):
        # sz 前缀创业板
        assert normalize_symbol("sz300750") == "300750"


# ---------------------------------------------------------------------------
# 2. get_symbol_prefix
# ---------------------------------------------------------------------------

class TestGetSymbolPrefix:
    """get_symbol_prefix：返回 'sh' 或 'sz'"""

    def test_sh_for_6_prefix(self):
        assert get_symbol_prefix("600000") == "sh"
        assert get_symbol_prefix("601318") == "sh"

    def test_sh_for_star_market(self):
        # 科创板 688xxx 也是上交所
        assert get_symbol_prefix("688981") == "sh"

    def test_sz_for_0_prefix(self):
        assert get_symbol_prefix("000001") == "sz"
        assert get_symbol_prefix("000858") == "sz"

    def test_sz_for_gem(self):
        # 创业板 300xxx 是深交所
        assert get_symbol_prefix("300750") == "sz"

    def test_accepts_jq_format(self):
        assert get_symbol_prefix("600519.XSHG") == "sh"
        assert get_symbol_prefix("000001.XSHE") == "sz"

    def test_accepts_sh_prefix_format(self):
        assert get_symbol_prefix("sh600519") == "sh"
        assert get_symbol_prefix("sz000001") == "sz"


# ---------------------------------------------------------------------------
# 3. is_gem_or_star
# ---------------------------------------------------------------------------

class TestIsGemOrStar:
    """is_gem_or_star：判断创业板（300xxx）或科创板（688xxx）"""

    def test_gem_300_returns_true(self):
        assert is_gem_or_star("300750") is True
        assert is_gem_or_star("300001") is True

    def test_star_688_returns_true(self):
        assert is_gem_or_star("688981") is True
        assert is_gem_or_star("688001") is True

    def test_mainboard_600_returns_false(self):
        assert is_gem_or_star("600000") is False
        assert is_gem_or_star("601318") is False

    def test_mainboard_000_returns_false(self):
        assert is_gem_or_star("000001") is False
        assert is_gem_or_star("000858") is False

    def test_accepts_jq_format(self):
        assert is_gem_or_star("300750.XSHE") is True
        assert is_gem_or_star("600519.XSHG") is False

    def test_accepts_prefix_format(self):
        assert is_gem_or_star("sz300750") is True
        assert is_gem_or_star("sh600519") is False


# ---------------------------------------------------------------------------
# 4. calculate_limit_price
# ---------------------------------------------------------------------------

class TestCalculateLimitPrice:
    """calculate_limit_price：计算涨跌停价"""

    # --- 主板 10% ---

    def test_mainboard_up_10pct(self):
        result = calculate_limit_price(100.0, "600000", "up")
        assert result == pytest.approx(110.0, rel=1e-6)

    def test_mainboard_down_10pct(self):
        result = calculate_limit_price(100.0, "600000", "down")
        assert result == pytest.approx(90.0, rel=1e-6)

    # --- 创业板 20% ---

    def test_gem_up_20pct(self):
        result = calculate_limit_price(100.0, "300750", "up")
        assert result == pytest.approx(120.0, rel=1e-6)

    def test_gem_down_20pct(self):
        result = calculate_limit_price(100.0, "300750", "down")
        assert result == pytest.approx(80.0, rel=1e-6)

    # --- 科创板 20% ---

    def test_star_up_20pct(self):
        result = calculate_limit_price(100.0, "688981", "up")
        assert result == pytest.approx(120.0, rel=1e-6)

    def test_star_down_20pct(self):
        result = calculate_limit_price(100.0, "688981", "down")
        assert result == pytest.approx(80.0, rel=1e-6)

    # --- 无效输入 ---

    def test_none_prev_close_returns_none(self):
        assert calculate_limit_price(None, "600000", "up") is None

    def test_zero_prev_close_returns_none(self):
        assert calculate_limit_price(0, "600000", "up") is None

    def test_negative_prev_close_returns_none(self):
        assert calculate_limit_price(-10.0, "600000", "up") is None

    # --- 精度 ---

    def test_result_rounded_to_2_decimal_places(self):
        result = calculate_limit_price(10.123, "600000", "up")
        assert result == round(10.123 * 1.10, 2)

    def test_result_is_float(self):
        result = calculate_limit_price(100.0, "600000", "up")
        assert isinstance(result, float)

    # --- 接受多种代码格式 ---

    def test_accepts_jq_format(self):
        result = calculate_limit_price(100.0, "600519.XSHG", "up")
        assert result == pytest.approx(110.0, rel=1e-6)

    def test_accepts_sh_prefix(self):
        result = calculate_limit_price(100.0, "sh600519", "up")
        assert result == pytest.approx(110.0, rel=1e-6)

    def test_gem_jq_format(self):
        result = calculate_limit_price(100.0, "300750.XSHE", "up")
        assert result == pytest.approx(120.0, rel=1e-6)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
