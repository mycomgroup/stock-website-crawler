"""
test_market_api_unit.py
行情 API 单元测试（不依赖网络）

使用 mock 数据测试内部逻辑
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src",
    ),
)


class TestNormalizeSymbol:
    """股票代码标准化测试"""

    def test_sh_prefix(self):
        """sh 前缀"""
        from jk2bt.api.market import _normalize_symbol

        assert _normalize_symbol("sh600000") == "600000"
        assert _normalize_symbol("sh000001") == "000001"

    def test_sz_prefix(self):
        """sz 前缀"""
        from jk2bt.api.market import _normalize_symbol

        assert _normalize_symbol("sz000001") == "000001"
        assert _normalize_symbol("sz300750") == "300750"

    def test_xshg_suffix(self):
        """.XSHG 后缀"""
        from jk2bt.api.market import _normalize_symbol

        assert _normalize_symbol("600000.XSHG") == "600000"
        assert _normalize_symbol("600519.XSHG") == "600519"

    def test_xshe_suffix(self):
        """.XSHE 后缀"""
        from jk2bt.api.market import _normalize_symbol

        assert _normalize_symbol("000001.XSHE") == "000001"
        assert _normalize_symbol("300750.XSHE") == "300750"

    def test_pure_6_digit(self):
        """纯 6 位数字"""
        from jk2bt.api.market import _normalize_symbol

        assert _normalize_symbol("600000") == "600000"
        assert _normalize_symbol("000001") == "000001"

    def test_pure_5_digit_zfill(self):
        """纯 5 位数字自动补零"""
        from jk2bt.api.market import _normalize_symbol

        assert _normalize_symbol("60000") == "060000"
        assert _normalize_symbol("00001") == "000001"

    def test_code_with_dot_only(self):
        """仅带点的格式"""
        from jk2bt.api.market import _normalize_symbol

        assert _normalize_symbol("600519") == "600519"


class TestGetSymbolPrefix:
    """股票代码前缀测试"""

    def test_sh_prefix_for_6(self):
        """6 开头代码返回 sh"""
        from jk2bt.api.market import _get_symbol_prefix

        assert _get_symbol_prefix("600000") == "sh"
        assert _get_symbol_prefix("601318") == "sh"
        assert _get_symbol_prefix("688981") == "sh"

    def test_sz_prefix_for_0(self):
        """0 开头代码返回 sz"""
        from jk2bt.api.market import _get_symbol_prefix

        assert _get_symbol_prefix("000001") == "sz"
        assert _get_symbol_prefix("000858") == "sz"

    def test_sz_prefix_for_3(self):
        """3 开头代码返回 sz"""
        from jk2bt.api.market import _get_symbol_prefix

        assert _get_symbol_prefix("300750") == "sz"
        assert _get_symbol_prefix("300001") == "sz"


class TestFqToAdjust:
    """复权参数转换测试"""

    def test_pre_to_qfq(self):
        """pre -> qfq"""
        from jk2bt.api.market import _fq_to_adjust

        assert _fq_to_adjust("pre") == "qfq"

    def test_post_to_hfq(self):
        """post -> hfq"""
        from jk2bt.api.market import _fq_to_adjust

        assert _fq_to_adjust("post") == "hfq"

    def test_none_to_empty(self):
        """none -> ''"""
        from jk2bt.api.market import _fq_to_adjust

        assert _fq_to_adjust("none") == ""

    def test_none_value_to_qfq(self):
        """None -> qfq"""
        from jk2bt.api.market import _fq_to_adjust

        assert _fq_to_adjust(None) == "qfq"

    def test_invalid_value_to_qfq(self):
        """无效值 -> qfq"""
        from jk2bt.api.market import _fq_to_adjust

        assert _fq_to_adjust("invalid") == "qfq"


class TestIsGemOrStar:
    """创业板/科创板判断测试"""

    def test_gem_code(self):
        """创业板代码"""
        from jk2bt.api.market import _is_gem_or_star

        assert _is_gem_or_star("300750") == True
        assert _is_gem_or_star("300001") == True
        assert _is_gem_or_star("300xxx") == True

    def test_star_code(self):
        """科创板代码"""
        from jk2bt.api.market import _is_gem_or_star

        assert _is_gem_or_star("688981") == True
        assert _is_gem_or_star("688001") == True
        assert _is_gem_or_star("688xxx") == True

    def test_mainboard_code(self):
        """主板代码"""
        from jk2bt.api.market import _is_gem_or_star

        assert _is_gem_or_star("600000") == False
        assert _is_gem_or_star("000001") == False
        assert _is_gem_or_star("601318") == False


class TestCalculateLimitPrice:
    """涨跌停价计算测试"""

    def test_mainboard_up(self):
        """主板涨停 10%"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(100.0, "600000", "up")
        assert result == 110.0

    def test_mainboard_down(self):
        """主板跌停 10%"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(100.0, "600000", "down")
        assert result == 90.0

    def test_gem_up(self):
        """创业板涨停 20%"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(100.0, "300750", "up")
        assert result == 120.0

    def test_gem_down(self):
        """创业板跌停 20%"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(100.0, "300750", "down")
        assert result == 80.0

    def test_star_up(self):
        """科创板涨停 20%"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(100.0, "688981", "up")
        assert result == 120.0

    def test_star_down(self):
        """科创板跌停 20%"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(100.0, "688981", "down")
        assert result == 80.0

    def test_none_prev_close(self):
        """prev_close 为 None"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(None, "600000", "up")
        assert result is None

    def test_zero_prev_close(self):
        """prev_close 为 0"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(0, "600000", "up")
        assert result is None

    def test_negative_prev_close(self):
        """prev_close 为负"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(-10.0, "600000", "up")
        assert result is None

    def test_rounding(self):
        """价格取整"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(10.123, "600000", "up")
        assert result == round(10.123 * 1.10, 2)

    def test_decimal_places(self):
        """小数位数"""
        from jk2bt.api.market import _calculate_limit_price

        result = _calculate_limit_price(123.45, "600000", "up")
        assert isinstance(result, float)
        assert len(str(result).split(".")[-1]) <= 2


class TestStandardizeColumns:
    """列名标准化测试"""

    def test_chinese_to_english(self):
        """中文列名转英文"""
        from jk2bt.api.market import _standardize_columns

        df = pd.DataFrame({"日期": ["2023-01-01"], "开盘": [100], "收盘": [102]})
        result = _standardize_columns(df)

        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "close" in result.columns

    def test_datetime_conversion(self):
        """datetime 列转换"""
        from jk2bt.api.market import _standardize_columns

        df = pd.DataFrame({"日期": ["2023-01-01", "2023-01-02"]})
        result = _standardize_columns(df)

        assert "datetime" in result.columns
        assert result["datetime"].dtype.kind in ["M", "O"]

    def test_preserve_existing_columns(self):
        """保留已存在的英文列"""
        from jk2bt.api.market import _standardize_columns

        df = pd.DataFrame({"datetime": [1], "open": [2], "close": [3]})
        result = _standardize_columns(df)

        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "close" in result.columns

    def test_volume_to_money(self):
        """成交额列转换"""
        from jk2bt.api.market import _standardize_columns

        df = pd.DataFrame({"成交额": [1000000]})
        result = _standardize_columns(df)

        assert "money" in result.columns


class TestAddDerivedFields:
    """推导字段添加测试"""

    def test_pre_close_shift(self):
        """pre_close 为前一天 close"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame(
            {"close": [100.0, 101.0, 102.0, 103.0], "volume": [1000, 1000, 1000, 1000]}
        )
        result = _add_derived_fields(df.copy(), "600000")

        assert "pre_close" in result.columns
        assert pd.isna(result.iloc[0]["pre_close"])
        assert result.iloc[1]["pre_close"] == 100.0
        assert result.iloc[2]["pre_close"] == 101.0

    def test_paused_from_volume_zero(self):
        """volume=0 标记为停牌"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame({"close": [100.0, 101.0], "volume": [1000, 0]})
        result = _add_derived_fields(df.copy(), "600000")

        assert "paused" in result.columns
        assert result.iloc[0]["paused"] == 0
        assert result.iloc[1]["paused"] == 1

    def test_paused_all_zero_when_volume_positive(self):
        """volume>0 时 paused=0"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame({"close": [100.0, 101.0], "volume": [1000, 1000]})
        result = _add_derived_fields(df.copy(), "600000")

        assert "paused" in result.columns
        assert result["paused"].sum() == 0

    def test_high_limit_calculation(self):
        """涨停价计算"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame({"close": [100.0, 101.0], "volume": [1000, 1000]})
        result = _add_derived_fields(df.copy(), "600000")

        assert "high_limit" in result.columns

    def test_low_limit_calculation(self):
        """跌停价计算"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame({"close": [100.0, 101.0], "volume": [1000, 1000]})
        result = _add_derived_fields(df.copy(), "600000")

        assert "low_limit" in result.columns

    def test_paused_row_no_limit(self):
        """停牌行无涨跌停价"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame({"close": [100.0, 101.0], "volume": [1000, 0]})
        result = _add_derived_fields(df.copy(), "600000")

        assert pd.isna(result.iloc[1]["high_limit"])
        assert pd.isna(result.iloc[1]["low_limit"])

    def test_empty_dataframe(self):
        """空 DataFrame"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame()
        result = _add_derived_fields(df, "600000")

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_gem_20_percent(self):
        """创业板 20%"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame({"close": [100.0, 101.0], "volume": [1000, 1000]})
        result = _add_derived_fields(df.copy(), "300750")

        assert "high_limit" in result.columns
        assert "low_limit" in result.columns

        assert result.iloc[1]["high_limit"] == round(100.0 * 1.20, 2)
        assert result.iloc[1]["low_limit"] == round(100.0 * 0.80, 2)

    def test_star_20_percent(self):
        """科创板 20%"""
        from jk2bt.api.market import _add_derived_fields

        df = pd.DataFrame({"close": [100.0, 101.0], "volume": [1000, 1000]})
        result = _add_derived_fields(df.copy(), "688981")

        assert result.iloc[1]["high_limit"] == round(100.0 * 1.20, 2)
        assert result.iloc[1]["low_limit"] == round(100.0 * 0.80, 2)


class TestReturnStructureValidation:
    """返回结构验证测试"""

    def test_single_security_dataframe(self):
        """单标的返回 DataFrame"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2099-01-01",
            end_date="2099-01-10",
        )
        assert isinstance(result, pd.DataFrame)

    def test_multiple_security_dict(self):
        """多标的返回 dict"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2099-01-01",
            end_date="2099-01-10",
            panel=True,
        )
        assert isinstance(result, dict)

    def test_dict_keys_match_input(self):
        """dict 键与输入匹配"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2099-01-01",
            end_date="2099-01-10",
            panel=True,
        )
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result

    def test_dict_values_dataframe(self):
        """dict 值为 DataFrame"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2099-01-01",
            end_date="2099-01-10",
            panel=True,
        )
        for df in result.values():
            assert isinstance(df, pd.DataFrame)

    def test_panel_false_dataframe(self):
        """panel=False 返回 DataFrame"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2099-01-01",
            end_date="2099-01-10",
            panel=False,
        )
        assert isinstance(result, pd.DataFrame)

    def test_history_dataframe(self):
        """history 返回 DataFrame"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE"],
        )
        assert isinstance(result, pd.DataFrame)

    def test_history_columns_match_input(self):
        """history 列与输入匹配"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE"],
        )
        assert "600519.XSHG" in result.columns
        assert "000001.XSHE" in result.columns

    def test_history_df_false_dict(self):
        """history df=False 返回 dict"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG"],
            df=False,
        )
        assert isinstance(result, dict)

    def test_attribute_history_dataframe(self):
        """attribute_history 返回 DataFrame"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            fields=["close"],
        )
        assert isinstance(result, pd.DataFrame)

    def test_attribute_history_df_false_dict(self):
        """attribute_history df=False 返回 dict"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            fields=["close"],
            df=False,
        )
        assert isinstance(result, dict)

    def test_get_bars_dataframe(self):
        """get_bars 返回 DataFrame"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG",
            count=10,
            unit="1d",
        )
        assert isinstance(result, pd.DataFrame)

    def test_get_bars_multiple_dict(self):
        """get_bars 多标的返回 dict"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security=["600519.XSHG", "000001.XSHE"],
            count=10,
            unit="1d",
        )
        assert isinstance(result, dict)


class TestEdgeCases:
    """边界情况测试"""

    def test_empty_security_list(self):
        """空 security 列表"""
        from jk2bt.api.market import get_price

        result = get_price(security=[], start_date="2023-01-01", end_date="2023-01-10")
        assert isinstance(result, dict)
        assert len(result) == 0

    def test_empty_security_list_history(self):
        """空 security_list"""
        from jk2bt.api.market import history

        result = history(count=10, unit="1d", field="close", security_list=[])
        assert isinstance(result, pd.DataFrame)

    def test_count_zero(self):
        """count=0"""
        from jk2bt.api.market import get_price

        result = get_price(security="600519.XSHG", end_date="2023-01-10", count=0)
        assert isinstance(result, pd.DataFrame)

    def test_invalid_field(self):
        """无效字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2099-01-01",
            end_date="2099-01-10",
            fields=["invalid_field"],
        )
        assert isinstance(result, pd.DataFrame)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
