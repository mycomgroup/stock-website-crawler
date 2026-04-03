"""
test_api_compatibility.py
接口兼容性测试。

验证：
- 返回结构符合聚宽 API 规范
- 参数签名正确
- 各种输入格式的兼容性
"""

import sys
import os

_utility_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src",
)
if _utility_dir not in sys.path:
    sys.path.insert(0, _utility_dir)

import pytest
import pandas as pd
import numpy as np
from typing import Dict, List, Union


class TestGetFactorValuesJqSignature:
    """get_factor_values_jq 参数签名测试。"""

    def test_single_security_single_factor(self):
        """单标的单因子。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert len(result) == 1
        assert "pe_ratio" in result

    def test_single_security_multiple_factors(self):
        """单标的多因子。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors=["PE_ratio", "PB_ratio", "market_cap"],
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert len(result) == 3
        for key in ["pe_ratio", "pb_ratio", "market_cap"]:
            assert key in result

    def test_multiple_securities_single_factor(self):
        """多标单因子。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities=["sh600519", "sz000001"],
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert "pe_ratio" in result
        assert isinstance(result["pe_ratio"], pd.DataFrame)
        assert "sh600519" in result["pe_ratio"].columns
        assert "sz000001" in result["pe_ratio"].columns

    def test_multiple_securities_multiple_factors(self):
        """多标多因子。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities=["sh600519", "sz000001"],
            factors=["PE_ratio", "PB_ratio"],
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        for factor in ["pe_ratio", "pb_ratio"]:
            assert factor in result
            assert isinstance(result[factor], pd.DataFrame)
            assert len(result[factor].columns) == 2

    def test_count_parameter(self):
        """count 参数测试。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=5,
        )

        assert "pe_ratio" in result
        df = result["pe_ratio"]
        assert len(df) <= 5

    def test_end_date_only(self):
        """仅提供 end_date。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
        )

        assert "pe_ratio" in result
        assert len(result["pe_ratio"]) == 1

    def test_start_date_end_date(self):
        """提供 start_date 和 end_date。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            start_date="2023-12-01",
            end_date="2023-12-31",
        )

        assert "pe_ratio" in result
        df = result["pe_ratio"]
        assert len(df) >= 0

    def test_force_update_parameter(self):
        """force_update 参数。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
            force_update=True,
        )

        assert isinstance(result, dict)

    def test_cache_dir_parameter(self):
        """cache_dir 参数。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
            cache_dir="test_cache",
        )

        assert isinstance(result, dict)


class TestGetFactorValuesJqReturnStructure:
    """get_factor_values_jq 返回结构测试。"""

    def test_return_is_dict(self):
        """返回类型为 dict。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)

    def test_dict_keys_are_factor_names(self):
        """字典键为因子名。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors=["PE_ratio", "PB_ratio"],
            end_date="2024-01-01",
            count=1,
        )

        assert "pe_ratio" in result.keys()
        assert "pb_ratio" in result.keys()

    def test_values_are_dataframe(self):
        """字典值为 DataFrame。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result["pe_ratio"], pd.DataFrame)

    def test_dataframe_index_is_dates(self):
        """DataFrame index 为日期。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=3,
        )

        df = result["pe_ratio"]
        assert df.index.dtype == "object" or df.index.dtype.kind in ["M", "O"]

    def test_dataframe_columns_are_securities(self):
        """DataFrame columns 为证券代码。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities=["sh600519", "sz000001"],
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        df = result["pe_ratio"]
        assert "sh600519" in df.columns
        assert "sz000001" in df.columns

    def test_dataframe_values_are_numeric(self):
        """DataFrame 值为数值类型。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        df = result["pe_ratio"]
        assert df.dtypes.iloc[0] in [np.float64, np.float32, float]


class TestFactorAliasCompatibility:
    """因子别名兼容性测试。"""

    def test_pe_ratio_aliases(self):
        """PE_ratio 别名。"""
        from src.factors import get_factor_values_jq

        aliases = ["PE_ratio", "pe_ratio", "Pe_ratio", "pe_ratio"]

        for alias in aliases:
            result = get_factor_values_jq(
                securities="sh600519",
                factors=alias,
                end_date="2024-01-01",
                count=1,
            )
            assert "pe_ratio" in result

    def test_bias_aliases(self):
        """BIAS 别名。"""
        from src.factors import get_factor_values_jq

        aliases = ["BIAS5", "bias_5"]

        for alias in aliases:
            result = get_factor_values_jq(
                securities="sh600519",
                factors=alias,
                end_date="2024-01-01",
                count=1,
            )
            assert "bias_5" in result

    def test_emac_aliases(self):
        """EMAC 别名。"""
        from src.factors import get_factor_values_jq

        aliases = ["EMAC26", "emac_26"]

        for alias in aliases:
            result = get_factor_values_jq(
                securities="sh600519",
                factors=alias,
                end_date="2024-01-01",
                count=1,
            )
            assert "emac_26" in result


class TestSecurityCodeCompatibility:
    """证券代码格式兼容性测试。"""

    def test_sh_prefix(self):
        """sh 前缀格式。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)

    def test_sz_prefix(self):
        """sz 前缀格式。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sz000001",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)

    def test_xshg_suffix(self):
        """XSHG 后缀格式。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="600519.XSHG",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)

    def test_xshe_suffix(self):
        """XSHE 后缀格式。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="000001.XSHE",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)

    def test_pure_code(self):
        """纯数字格式。"""
        from src.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)


class TestGetPriceJqSignature:
    """get_price_jq 参数签名测试。"""

    def test_required_params(self):
        """必需参数。"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, (pd.DataFrame, dict))

    def test_fields_param(self):
        """fields 参数。"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["open", "close", "high", "low"],
        )

        assert isinstance(result, (pd.DataFrame, dict))

    def test_frequency_param(self):
        """frequency 参数。"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
            frequency="daily",
        )

        assert isinstance(result, (pd.DataFrame, dict))

    def test_count_param(self):
        """count 参数。"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="sh600000",
            end_date="2023-01-10",
            count=5,
        )

        assert isinstance(result, (pd.DataFrame, dict))


class TestGetPriceJqReturnStructure:
    """get_price_jq 返回结构测试。"""

    def test_single_security_returns_dataframe(self):
        """单标的返回 DataFrame。"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)

    def test_multiple_securities_returns_dict(self):
        """多标的返回 dict。"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols=["sh600000", "sz000001"],
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, dict)

    def test_dataframe_has_datetime_column(self):
        """DataFrame 包含 datetime 列。"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        if isinstance(result, pd.DataFrame) and not result.empty:
            assert "datetime" in result.columns or result.index.name == "datetime"

    def test_dataframe_has_price_columns(self):
        """DataFrame 包含价格列。"""
        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["open", "close", "high", "low"],
        )

        if isinstance(result, pd.DataFrame) and not result.empty:
            for col in ["open", "close", "high", "low"]:
                assert col in result.columns


class TestGetFundamentalsJqSignature:
    """get_fundamentals_jq 参数签名测试。"""

    def test_query_object_param(self):
        """query 对象参数。"""
        from jk2bt.core.strategy_base import get_fundamentals_jq, valuation

        query = valuation.code == "sh600000"
        result = get_fundamentals_jq(query, statDate="2022-12-31")

        assert isinstance(result, (pd.DataFrame, dict)) or result is None

    def test_statdate_param(self):
        """statDate 参数。"""
        from jk2bt.core.strategy_base import get_fundamentals_jq

        query = {"table": "balance", "symbol": "sh600000"}
        result = get_fundamentals_jq(query, statDate="2022-12-31")

        assert isinstance(result, pd.DataFrame) or result is None

    def test_statdate_quarter_format(self):
        """statDate 季度格式。"""
        from jk2bt.core.strategy_base import get_fundamentals_jq

        query = {"table": "balance", "symbol": "sh600000"}
        result = get_fundamentals_jq(query, statDate="2022q4")

        assert isinstance(result, pd.DataFrame) or result is None


class TestGetHistoryFundamentalsJqSignature:
    """get_history_fundamentals_jq 参数签名测试。"""

    def test_basic_params(self):
        """基本参数。"""
        from jk2bt.core.strategy_base import get_history_fundamentals_jq

        result = get_history_fundamentals_jq(
            entity="sh600000",
            fields=["balance.cash_equivalents", "income.total_operating_revenue"],
            stat_date="2022q4",
            count=1,
        )

        assert isinstance(result, pd.DataFrame) or result is None

    def test_count_param(self):
        """count 参数。"""
        from jk2bt.core.strategy_base import get_history_fundamentals_jq

        result = get_history_fundamentals_jq(
            entity="sh600000",
            fields=["balance.cash_equivalents"],
            stat_date="2022q4",
            count=4,
        )

        assert isinstance(result, pd.DataFrame) or result is None


class TestGetAllSecuritiesJqSignature:
    """get_all_securities_jq 参数签名测试。"""

    def test_no_params(self):
        """无参数调用。"""
        from jk2bt.core.strategy_base import get_all_securities_jq

        result = get_all_securities_jq()

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    def test_return_structure(self):
        """返回结构。"""
        from jk2bt.core.strategy_base import get_all_securities_jq

        result = get_all_securities_jq()

        assert "code" in result.columns
        assert "display_name" in result.columns or "name" in result.columns


class TestGetSecurityInfoJqSignature:
    """get_security_info_jq 参数签名测试。"""

    def test_single_security(self):
        """单标的。"""
        from jk2bt.core.strategy_base import get_security_info_jq

        result = get_security_info_jq("sh600000")

        assert isinstance(result, dict) or result is None

    def test_return_structure(self):
        """返回结构。"""
        from jk2bt.core.strategy_base import get_security_info_jq

        result = get_security_info_jq("sh600000")

        if result is not None:
            assert "code" in result


class TestGetAllTradeDaysJqSignature:
    """get_all_trade_days_jq 参数签名测试。"""

    def test_no_params(self):
        """无参数调用。"""
        from jk2bt.core.strategy_base import get_all_trade_days_jq

        result = get_all_trade_days_jq()

        assert isinstance(result, list)
        assert len(result) > 0

    def test_return_type(self):
        """返回类型。"""
        from jk2bt.core.strategy_base import get_all_trade_days_jq

        result = get_all_trade_days_jq()

        assert all(isinstance(d, pd.Timestamp) for d in result)


class TestGetExtrasJqSignature:
    """get_extras_jq 参数签名测试。"""

    def test_is_st_param(self):
        """is_st 参数。"""
        from jk2bt.core.strategy_base import get_extras_jq

        result = get_extras_jq("is_st", ["sh600000"])

        assert isinstance(result, pd.DataFrame)

    def test_is_paused_param(self):
        """is_paused 参数。"""
        from jk2bt.core.strategy_base import get_extras_jq

        result = get_extras_jq("is_paused", ["sh600000"])

        assert isinstance(result, pd.DataFrame)


class TestGetBarsJqSignature:
    """get_bars_jq 参数签名测试。"""

    def test_unit_param(self):
        """unit 参数。"""
        from jk2bt.core.strategy_base import get_bars_jq

        result = get_bars_jq(
            security="sh600000",
            count=5,
            unit="1d",
        )

        assert isinstance(result, pd.DataFrame)

    def test_fields_param(self):
        """fields 参数。"""
        from jk2bt.core.strategy_base import get_bars_jq

        result = get_bars_jq(
            security="sh600000",
            count=5,
            unit="1d",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)


class TestBacktraderIntegration:
    """Backtrader 集成测试。"""

    def test_factor_values_available_in_strategy(self):
        """策略中可获取因子值。"""
        from jk2bt.core.strategy_base import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="market_cap",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert "market_cap" in result

    def test_strategy_has_required_functions(self):
        """策略包含必需函数。"""
        from jk2bt.core.strategy_base import (
            get_price_jq,
            get_fundamentals_jq,
            get_history_fundamentals_jq,
            get_all_securities_jq,
            get_security_info_jq,
            get_all_trade_days_jq,
            get_extras_jq,
            get_factor_values_jq,
        )

        assert callable(get_price_jq)
        assert callable(get_fundamentals_jq)
        assert callable(get_history_fundamentals_jq)
        assert callable(get_all_securities_jq)
        assert callable(get_security_info_jq)
        assert callable(get_all_trade_days_jq)
        assert callable(get_extras_jq)
        assert callable(get_factor_values_jq)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
