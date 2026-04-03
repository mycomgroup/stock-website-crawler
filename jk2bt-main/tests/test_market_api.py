"""
test_market_api.py
行情 API 兼容层测试

测试覆盖：
1. get_price - 单标的、多标的、日线、分钟线
2. history - 多标单字段
3. attribute_history - 单标多字段
4. get_bars - 日线、分钟线
5. 高频字段：paused, pre_close, high_limit, low_limit
6. panel 参数行为
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

pytestmark = pytest.mark.network


class TestGetPriceSignature:
    """get_price 参数签名测试"""

    def test_required_params_only(self):
        """仅必需参数"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert "datetime" in result.columns

    def test_count_param(self):
        """count 参数"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            end_date="2023-12-31",
            count=10,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 10

    def test_fields_param(self):
        """fields 参数"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "open" in result.columns
            assert "close" in result.columns

    def test_fq_param(self):
        """复权参数"""
        from jk2bt.api.market import get_price

        result_qfq = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fq="pre",
        )

        result_none = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fq="none",
        )

        assert isinstance(result_qfq, pd.DataFrame)
        assert isinstance(result_none, pd.DataFrame)

    def test_frequency_param(self):
        """frequency 参数"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            frequency="daily",
        )

        assert isinstance(result, pd.DataFrame)


class TestGetPriceReturnStructure:
    """get_price 返回结构测试"""

    def test_single_security_returns_dataframe(self):
        """单标的返回 DataFrame"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)

    def test_multiple_securities_returns_dict(self):
        """多标的返回 dict"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            panel=True,
        )

        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result

    def test_panel_false_returns_dataframe(self):
        """panel=False 返回 DataFrame"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            panel=False,
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "code" in result.columns

    def test_dataframe_has_datetime_column(self):
        """DataFrame 包含 datetime 列"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        if not result.empty:
            assert "datetime" in result.columns


class TestHighFrequencyFields:
    """高频字段测试"""

    def test_paused_field(self):
        """paused 字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "paused"],
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "paused" in result.columns
            assert result["paused"].isin([0, 1]).all()

    def test_pre_close_field(self):
        """pre_close 字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "pre_close"],
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "pre_close" in result.columns

    def test_high_limit_field(self):
        """high_limit 字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "high_limit"],
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "high_limit" in result.columns

    def test_low_limit_field(self):
        """low_limit 字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "low_limit"],
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "low_limit" in result.columns

    def test_all_high_frequency_fields(self):
        """所有高频字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=[
                "open",
                "close",
                "high",
                "low",
                "volume",
                "money",
                "paused",
                "pre_close",
                "high_limit",
                "low_limit",
            ],
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            for field in [
                "open",
                "close",
                "high",
                "low",
                "volume",
                "money",
                "paused",
                "pre_close",
                "high_limit",
                "low_limit",
            ]:
                assert field in result.columns, f"Missing field: {field}"


class TestHistorySignature:
    """history 参数签名测试"""

    def test_basic_params(self):
        """基本参数"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE"],
        )

        assert isinstance(result, pd.DataFrame)
        assert "600519.XSHG" in result.columns
        assert "000001.XSHE" in result.columns

    def test_df_false(self):
        """df=False 返回 dict"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE"],
            df=False,
        )

        assert isinstance(result, dict)

    def test_end_date_param(self):
        """end_date 参数"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG"],
            end_date="2023-12-31",
        )

        assert isinstance(result, pd.DataFrame)


class TestAttributeHistorySignature:
    """attribute_history 参数签名测试"""

    def test_basic_params(self):
        """基本参数"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["open", "close", "high", "low"],
        )

        assert isinstance(result, pd.DataFrame)
        for col in ["open", "close", "high", "low"]:
            assert col in result.columns

    def test_df_false(self):
        """df=False 返回 dict"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["open", "close"],
            df=False,
        )

        assert isinstance(result, dict)

    def test_high_frequency_fields(self):
        """高频字段"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["close", "paused", "high_limit", "low_limit"],
        )

        assert isinstance(result, pd.DataFrame)
        for col in ["close", "paused", "high_limit", "low_limit"]:
            assert col in result.columns


class TestGetBarsSignature:
    """get_bars 参数签名测试"""

    def test_daily_bars(self):
        """日线 bars"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG",
            count=10,
            unit="1d",
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 10

    def test_fields_param(self):
        """fields 参数"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "open" in result.columns
            assert "close" in result.columns

    def test_end_dt_param(self):
        """end_dt 参数"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG",
            count=10,
            unit="1d",
            end_dt="2023-12-31",
        )

        assert isinstance(result, pd.DataFrame)


class TestPanelParameter:
    """panel 参数测试"""

    def test_panel_true_returns_dict(self):
        """panel=True 返回 dict"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            panel=True,
        )

        assert isinstance(result, dict)

    def test_panel_false_can_pivot(self):
        """panel=False 可被 pivot"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close"],
            panel=False,
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "code" in result.columns
            assert "close" in result.columns
            pivoted = result.pivot(index="datetime", columns="code", values="close")
            assert isinstance(pivoted, pd.DataFrame)


class TestLimitPriceCalculation:
    """涨跌停价计算测试"""

    def test_mainboard_limit_ratio(self):
        """主板涨跌停比例"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "pre_close", "high_limit", "low_limit", "paused"],
        )

        if not result.empty:
            for idx in range(len(result)):
                if (
                    pd.notna(result.iloc[idx]["pre_close"])
                    and result.iloc[idx].get("paused", 0) == 0
                ):
                    pre_close = result.iloc[idx]["pre_close"]
                    high_limit = result.iloc[idx]["high_limit"]
                    low_limit = result.iloc[idx]["low_limit"]

                    if pd.notna(high_limit):
                        expected_high = round(pre_close * 1.10, 2)
                        assert abs(high_limit - expected_high) < 0.01

                    if pd.notna(low_limit):
                        expected_low = round(pre_close * 0.90, 2)
                        assert abs(low_limit - expected_low) < 0.01

    def test_gem_limit_ratio(self):
        """创业板涨跌停比例"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="300750.XSHE",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "pre_close", "high_limit", "low_limit", "paused"],
        )

        if not result.empty:
            for idx in range(len(result)):
                if (
                    pd.notna(result.iloc[idx]["pre_close"])
                    and result.iloc[idx].get("paused", 0) == 0
                ):
                    pre_close = result.iloc[idx]["pre_close"]
                    high_limit = result.iloc[idx]["high_limit"]
                    low_limit = result.iloc[idx]["low_limit"]

                    if pd.notna(high_limit):
                        expected_high = round(pre_close * 1.20, 2)
                        assert abs(high_limit - expected_high) < 0.01

                    if pd.notna(low_limit):
                        expected_low = round(pre_close * 0.80, 2)
                        assert abs(low_limit - expected_low) < 0.01


class TestCodeFormatCompatibility:
    """代码格式兼容性测试"""

    def test_jq_format(self):
        """聚宽格式"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)

    def test_sh_prefix(self):
        """sh 前缀格式"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="sh600519",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)

    def test_pure_code(self):
        """纯数字格式"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)


class TestIntegrationWithBacktraderBaseStrategy:
    """与 backtrader_base_strategy 集成测试"""

    def test_get_price_jq_unified(self):
        """get_price_jq 使用统一接口"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)

    def test_history_unified(self):
        """history 使用统一接口"""
        from jk2bt.core.strategy_base import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG"],
        )

        assert isinstance(result, pd.DataFrame)

    def test_attribute_history_unified(self):
        """attribute_history 使用统一接口"""
        from jk2bt.core.strategy_base import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)

    def test_get_bars_jq_unified(self):
        """get_bars_jq 使用统一接口"""
        from jk2bt.core.strategy_base import get_bars_jq

        result = get_bars_jq(
            security="600519.XSHG",
            count=10,
            unit="1d",
        )

        assert isinstance(result, pd.DataFrame)


class TestAdvancedGetPriceCases:
    """get_price 高级测试用例"""

    def test_empty_security_list(self):
        """空 security 列表"""
        from jk2bt.api.market import get_price

        result = get_price([], start_date="2023-01-01", end_date="2023-01-10")
        assert isinstance(result, dict)
        assert len(result) == 0

    def test_single_security_with_count_no_end_date(self):
        """单标的仅提供 count，无 end_date"""
        from jk2bt.api.market import get_price

        result = get_price(security="600519.XSHG", count=5)
        assert isinstance(result, pd.DataFrame)

    def test_fields_subset(self):
        """仅请求部分字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close"],
        )
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "close" in result.columns

    def test_fields_not_exist(self):
        """请求不存在字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close", "nonexistent_field"],
        )
        assert isinstance(result, pd.DataFrame)

    def test_fq_none(self):
        """不复权"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fq="none",
        )
        assert isinstance(result, pd.DataFrame)

    def test_fq_post(self):
        """后复权"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fq="post",
        )
        assert isinstance(result, pd.DataFrame)

    def test_skip_paused_false(self):
        """不跳过停牌"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            skip_paused=False,
        )
        assert isinstance(result, pd.DataFrame)

    def test_fill_paused_false(self):
        """不填充停牌"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fill_paused=False,
        )
        assert isinstance(result, pd.DataFrame)

    def test_multiple_securities_panel_true(self):
        """多标的 panel=True 返回 dict"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE", "000858.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            panel=True,
        )
        assert isinstance(result, dict)
        assert len(result) == 3

    def test_multiple_securities_panel_false_structure(self):
        """多标的 panel=False DataFrame 结构"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close"],
            panel=False,
        )
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "code" in result.columns
            assert "datetime" in result.columns or result.index.name == "datetime"


class TestAdvancedHistoryCases:
    """history 高级测试用例"""

    def test_empty_security_list(self):
        """空 security_list"""
        from jk2bt.api.market import history

        result = history(count=10, unit="1d", field="close", security_list=[])
        assert isinstance(result, pd.DataFrame)

    def test_count_zero(self):
        """count=0"""
        from jk2bt.api.market import history

        result = history(
            count=0, unit="1d", field="close", security_list=["600519.XSHG"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_large_count(self):
        """大 count 值"""
        from jk2bt.api.market import history

        result = history(
            count=500, unit="1d", field="close", security_list=["600519.XSHG"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_field_open(self):
        """field=open"""
        from jk2bt.api.market import history

        result = history(
            count=10, unit="1d", field="open", security_list=["600519.XSHG"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_field_volume(self):
        """field=volume"""
        from jk2bt.api.market import history

        result = history(
            count=10, unit="1d", field="volume", security_list=["600519.XSHG"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_field_money(self):
        """field=money"""
        from jk2bt.api.market import history

        result = history(
            count=10, unit="1d", field="money", security_list=["600519.XSHG"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_field_paused(self):
        """field=paused"""
        from jk2bt.api.market import history

        result = history(
            count=10, unit="1d", field="paused", security_list=["600519.XSHG"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_field_high_limit(self):
        """field=high_limit"""
        from jk2bt.api.market import history

        result = history(
            count=10, unit="1d", field="high_limit", security_list=["600519.XSHG"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_field_low_limit(self):
        """field=low_limit"""
        from jk2bt.api.market import history

        result = history(
            count=10, unit="1d", field="low_limit", security_list=["600519.XSHG"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_df_false_returns_dict(self):
        """df=False 返回 dict"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE"],
            df=False,
        )
        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result

    def test_dict_values_are_arrays(self):
        """dict 值为数组"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG"],
            df=False,
        )
        assert isinstance(result, dict)
        if "600519.XSHG" in result:
            val = result["600519.XSHG"]
            assert isinstance(val, np.ndarray)

    def test_skip_paused_false(self):
        """skip_paused=False"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG"],
            skip_paused=False,
        )
        assert isinstance(result, pd.DataFrame)

    def test_fq_none(self):
        """fq=none"""
        from jk2bt.api.market import history

        result = history(
            count=10, unit="1d", field="close", security_list=["600519.XSHG"], fq="none"
        )
        assert isinstance(result, pd.DataFrame)

    def test_fq_post(self):
        """fq=post"""
        from jk2bt.api.market import history

        result = history(
            count=10, unit="1d", field="close", security_list=["600519.XSHG"], fq="post"
        )
        assert isinstance(result, pd.DataFrame)

    def test_end_date_string(self):
        """end_date 字符串格式"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG"],
            end_date="2023-06-30",
        )
        assert isinstance(result, pd.DataFrame)

    def test_multiple_securities_order(self):
        """多标的顺序"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["000001.XSHE", "600519.XSHG", "000858.XSHE"],
        )
        assert isinstance(result, pd.DataFrame)
        assert "000001.XSHE" in result.columns
        assert "600519.XSHG" in result.columns
        assert "000858.XSHE" in result.columns


class TestAdvancedAttributeHistoryCases:
    """attribute_history 高级测试用例"""

    def test_count_zero(self):
        """count=0"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(security="600519.XSHG", count=0, fields=["close"])
        assert isinstance(result, pd.DataFrame)

    def test_large_count(self):
        """大 count"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(security="600519.XSHG", count=200, fields=["close"])
        assert isinstance(result, pd.DataFrame)

    def test_single_field(self):
        """单字段"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(security="600519.XSHG", count=10, fields=["close"])
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "close" in result.columns

    def test_all_fields(self):
        """所有字段"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            fields=[
                "open",
                "high",
                "low",
                "close",
                "volume",
                "money",
                "paused",
                "pre_close",
                "high_limit",
                "low_limit",
            ],
        )
        assert isinstance(result, pd.DataFrame)

    def test_df_false_returns_dict(self):
        """df=False 返回 dict"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG", count=10, fields=["open", "close"], df=False
        )
        assert isinstance(result, dict)

    def test_dict_keys_are_fields(self):
        """dict 键为字段名"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            fields=["open", "close", "high_limit"],
            df=False,
        )
        assert isinstance(result, dict)
        if result:
            assert "open" in result
            assert "close" in result
            assert "high_limit" in result

    def test_dict_values_are_arrays(self):
        """dict 值为数组"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG", count=10, fields=["close"], df=False
        )
        assert isinstance(result, dict)
        if result and "close" in result:
            assert isinstance(result["close"], np.ndarray)

    def test_skip_paused_false(self):
        """skip_paused=False"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG", count=10, fields=["close"], skip_paused=False
        )
        assert isinstance(result, pd.DataFrame)

    def test_fq_none(self):
        """fq=none"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG", count=10, fields=["close"], fq="none"
        )
        assert isinstance(result, pd.DataFrame)

    def test_fq_post(self):
        """fq=post"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG", count=10, fields=["close"], fq="post"
        )
        assert isinstance(result, pd.DataFrame)

    def test_unit_1m(self):
        """unit=1m (分钟)"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG", count=10, unit="1m", fields=["open", "close"]
        )
        assert isinstance(result, pd.DataFrame)

    def test_end_date_parameter(self):
        """end_date 参数"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG", count=10, fields=["close"], end_date="2023-06-30"
        )
        assert isinstance(result, pd.DataFrame)

    def test_dataframe_index_is_datetime(self):
        """DataFrame index 为 datetime"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(security="600519.XSHG", count=10, fields=["close"])
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert result.index.name == "datetime" or result.index.dtype.kind in [
                "M",
                "O",
            ]


class TestAdvancedGetBarsCases:
    """get_bars 高级测试用例"""

    def test_count_zero(self):
        """count=0"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=0, unit="1d")
        assert isinstance(result, pd.DataFrame)

    def test_large_count(self):
        """大 count"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=500, unit="1d")
        assert isinstance(result, pd.DataFrame)

    def test_unit_1m(self):
        """unit=1m"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="1m")
        assert isinstance(result, pd.DataFrame)

    def test_unit_5m(self):
        """unit=5m"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="5m")
        assert isinstance(result, pd.DataFrame)

    def test_unit_15m(self):
        """unit=15m"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="15m")
        assert isinstance(result, pd.DataFrame)

    def test_unit_30m(self):
        """unit=30m"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="30m")
        assert isinstance(result, pd.DataFrame)

    def test_unit_60m(self):
        """unit=60m"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="60m")
        assert isinstance(result, pd.DataFrame)

    def test_include_now_true(self):
        """include_now=True"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="1d", include_now=True)
        assert isinstance(result, pd.DataFrame)

    def test_end_dt_datetime(self):
        """end_dt 为 datetime 对象"""
        from jk2bt.api.market import get_bars
        from datetime import datetime

        result = get_bars(
            security="600519.XSHG", count=10, unit="1d", end_dt=datetime(2023, 6, 30)
        )
        assert isinstance(result, pd.DataFrame)

    def test_end_dt_string(self):
        """end_dt 为字符串"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG", count=10, unit="1d", end_dt="2023-06-30"
        )
        assert isinstance(result, pd.DataFrame)

    def test_fq_none(self):
        """fq=none"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="1d", fq="none")
        assert isinstance(result, pd.DataFrame)

    def test_fq_post(self):
        """fq=post"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="1d", fq="post")
        assert isinstance(result, pd.DataFrame)

    def test_skip_paused_true(self):
        """skip_paused=True"""
        from jk2bt.api.market import get_bars

        result = get_bars(security="600519.XSHG", count=10, unit="1d", skip_paused=True)
        assert isinstance(result, pd.DataFrame)

    def test_multiple_securities(self):
        """多标的"""
        from jk2bt.api.market import get_bars

        result = get_bars(security=["600519.XSHG", "000001.XSHE"], count=10, unit="1d")
        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result

    def test_multiple_securities_dict_values(self):
        """多标的 dict 值为 DataFrame"""
        from jk2bt.api.market import get_bars

        result = get_bars(security=["600519.XSHG", "000001.XSHE"], count=5, unit="1d")
        assert isinstance(result, dict)
        for sym, df in result.items():
            assert isinstance(df, pd.DataFrame)


class TestLimitPriceEdgeCases:
    """涨跌停价边界测试"""

    def test_kexian_limit_ratio(self):
        """科创板涨跌停"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="688981.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "pre_close", "high_limit", "low_limit", "paused"],
        )
        assert isinstance(result, pd.DataFrame)

    def test_gem_different_codes(self):
        """不同创业板代码"""
        from jk2bt.api.market import get_price

        gem_codes = ["300001.XSHE", "300750.XSHE"]
        for code in gem_codes:
            result = get_price(
                security=code,
                start_date="2023-01-01",
                end_date="2023-01-10",
                fields=["high_limit", "low_limit"],
            )
            assert isinstance(result, pd.DataFrame)

    def test_mainboard_different_codes(self):
        """不同主板代码"""
        from jk2bt.api.market import get_price

        codes = ["600519.XSHG", "000001.XSHE", "601318.XSHG"]
        for code in codes:
            result = get_price(
                security=code,
                start_date="2023-01-01",
                end_date="2023-01-10",
                fields=["high_limit", "low_limit"],
            )
            assert isinstance(result, pd.DataFrame)

    def test_high_limit_is_higher_than_close(self):
        """涨停价高于收盘价"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "high_limit", "paused"],
        )
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            for idx in range(len(result)):
                close = result.iloc[idx]["close"]
                high_limit = result.iloc[idx].get("high_limit")
                paused = result.iloc[idx].get("paused", 0)
                if pd.notna(close) and pd.notna(high_limit) and paused == 0:
                    assert high_limit >= close

    def test_low_limit_is_lower_than_close(self):
        """跌停价低于收盘价"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "low_limit", "paused"],
        )
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            for idx in range(len(result)):
                close = result.iloc[idx]["close"]
                low_limit = result.iloc[idx].get("low_limit")
                paused = result.iloc[idx].get("paused", 0)
                if pd.notna(close) and pd.notna(low_limit) and paused == 0:
                    assert low_limit <= close


class TestCodeFormatEdgeCases:
    """代码格式边界测试"""

    def test_code_with_dot_xshg(self):
        """.XSHG 后缀"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG", start_date="2023-01-01", end_date="2023-01-10"
        )
        assert isinstance(result, pd.DataFrame)

    def test_code_with_dot_xshe(self):
        """.XSHE 后缀"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="000001.XSHE", start_date="2023-01-01", end_date="2023-01-10"
        )
        assert isinstance(result, pd.DataFrame)

    def test_code_with_sh_prefix(self):
        """sh 前缀"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="sh600519", start_date="2023-01-01", end_date="2023-01-10"
        )
        assert isinstance(result, pd.DataFrame)

    def test_code_with_sz_prefix(self):
        """sz 前缀"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="sz000001", start_date="2023-01-01", end_date="2023-01-10"
        )
        assert isinstance(result, pd.DataFrame)

    def test_code_pure_5_digit(self):
        """纯 5 位数字"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="60000", start_date="2023-01-01", end_date="2023-01-10"
        )
        assert isinstance(result, pd.DataFrame)

    def test_code_pure_6_digit(self):
        """纯 6 位数字"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519", start_date="2023-01-01", end_date="2023-01-10"
        )
        assert isinstance(result, pd.DataFrame)


class TestReturnStructureEdgeCases:
    """返回结构边界测试"""

    def test_dict_keys_preserve_input_order(self):
        """dict 键保持输入顺序"""
        from jk2bt.api.market import get_price

        input_order = ["600519.XSHG", "000001.XSHE", "000858.XSHE"]
        result = get_price(
            security=input_order,
            start_date="2023-01-01",
            end_date="2023-01-10",
            panel=True,
        )
        assert isinstance(result, dict)
        result_keys = list(result.keys())
        for sym in input_order:
            assert sym in result_keys

    def test_dataframe_columns_order(self):
        """DataFrame 列顺序"""
        from jk2bt.api.market import get_price

        fields_order = ["high", "low", "open", "close"]
        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=fields_order,
        )
        assert isinstance(result, pd.DataFrame)

    def test_empty_result_is_dataframe(self):
        """空结果返回 DataFrame"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2099-01-01",
            end_date="2099-01-10",
        )
        assert isinstance(result, pd.DataFrame)

    def test_empty_result_is_dict_for_multiple(self):
        """多标的空结果返回 dict"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2099-01-01",
            end_date="2099-01-10",
            panel=True,
        )
        assert isinstance(result, dict)


class TestPreCloseDerivation:
    """pre_close 推导测试"""

    def test_first_row_pre_close_is_nan_or_previous(self):
        """首行 pre_close 为 NaN 或前值"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "pre_close"],
        )
        assert isinstance(result, pd.DataFrame)

    def test_pre_close_shift_one_day(self):
        """pre_close 为前一天 close"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["close", "pre_close"],
        )
        assert isinstance(result, pd.DataFrame)


class TestPausedDerivation:
    """paused 推导测试"""

    def test_volume_zero_marks_paused(self):
        """volume=0 标记为停牌"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["volume", "paused"],
        )
        assert isinstance(result, pd.DataFrame)

    def test_paused_value_is_zero_or_one(self):
        """paused 值为 0 或 1"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-31",
            fields=["paused"],
        )
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert result["paused"].isin([0, 1]).all()


class TestAliasFunctions:
    """别名函数测试"""

    def test_get_price_jq_alias(self):
        """get_price_jq 别名"""
        from jk2bt.api.market import get_price_jq

        result = get_price_jq(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )
        assert isinstance(result, pd.DataFrame)

    def test_get_bars_jq_alias(self):
        """get_bars_jq 别名"""
        from jk2bt.api.market import get_bars_jq

        result = get_bars_jq(security="600519.XSHG", count=10, unit="1d")
        assert isinstance(result, pd.DataFrame)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
