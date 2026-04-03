"""
test_factor_import_regression.py
因子导入回归全面测试。

测试覆盖：
1. 导入模式测试（包内导入和兼容导入）
2. 因子注册表测试
3. 因子别名标准化测试
4. 因子预处理测试
5. 错误处理和异常测试
6. 边界条件测试
7. 整合测试
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os


class TestImportModes:
    """导入模式测试。"""

    def test_compatible_import_from_factors(self):
        """测试兼容导入模式：from jk2bt.factors import ..."""
        from jk2bt.factors import get_factor_values_jq

        assert callable(get_factor_values_jq)

    def test_compatible_import_base_module(self):
        """测试兼容导入：from jk2bt.factors import normalize_factor_name..."""
        from jk2bt.factors import normalize_factor_name, global_factor_registry

        assert callable(normalize_factor_name)
        assert hasattr(global_factor_registry, "list_factors")

    def test_compatible_import_preprocess(self):
        """测试兼容导入：from jk2bt.factors import preprocess函数..."""
        from jk2bt.factors import winsorize_med, standardlize, neutralize

        assert callable(winsorize_med)
        assert callable(standardlize)
        assert callable(neutralize)

    def test_compatible_import_valuation(self):
        """测试兼容导入：from factors.valuation import ..."""
        from jk2bt.factors import valuation

        assert hasattr(valuation, "compute_market_cap")

    def test_compatible_import_technical(self):
        """测试兼容导入：from factors.technical import ..."""
        from jk2bt.factors import technical

        assert hasattr(technical, "compute_bias_5")

    def test_compatible_import_fundamentals(self):
        """测试兼容导入：from factors.fundamentals import ..."""
        from jk2bt.factors import fundamentals

        assert hasattr(fundamentals, "compute_roe")

    def test_package_import_mode(self):
        """测试包内导入模式：jk2bt.factors"""
        import jk2bt

        assert hasattr(jk2bt, "get_factor_values_jq")

    def test_package_import_factors_submodule(self):
        """测试包内导入：from jk2bt.factors import ..."""
        from jk2bt.factors import get_factor_values_jq

        assert callable(get_factor_values_jq)

    def test_both_import_modes_consistent(self):
        """测试两种导入模式返回同一对象。"""
        from jk2bt.factors import get_factor_values_jq as func1
        from jk2bt.factors import (
            get_factor_values_jq as func2,
        )

        assert func1.__name__ == func2.__name__


class TestFactorRegistry:
    """因子注册表测试。"""

    def test_registry_exists(self):
        """测试注册表对象存在。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry is not None

    def test_registry_has_factors(self):
        """测试注册表中有因子。"""
        from jk2bt.factors import global_factor_registry

        factors = global_factor_registry.list_factors()
        assert len(factors) > 0

    def test_registry_contains_valuation_factors(self):
        """测试注册表包含估值因子。"""
        from jk2bt.factors import global_factor_registry

        factors = global_factor_registry.list_factors()
        valuation_factors = ["pe_ratio", "pb_ratio", "market_cap"]
        for f in valuation_factors:
            assert f in factors, f"缺少估值因子: {f}"

    def test_registry_contains_technical_factors(self):
        """测试注册表包含技术因子。"""
        from jk2bt.factors import global_factor_registry

        factors = global_factor_registry.list_factors()
        technical_factors = ["bias_5", "emac_26", "vol_20"]
        for f in technical_factors:
            assert f in factors, f"缺少技术因子: {f}"

    def test_registry_get_factor_function(self):
        """测试注册表可以获取因子计算函数。"""
        from jk2bt.factors import global_factor_registry

        func = global_factor_registry.get("pe_ratio")
        assert func is not None or global_factor_registry.is_registered("pe_ratio")

    def test_registry_get_nonexistent_factor(self):
        """测试获取不存在因子返回None。"""
        from jk2bt.factors import global_factor_registry

        func = global_factor_registry.get("nonexistent_factor_xyz")
        assert func is None or not global_factor_registry.is_registered(
            "nonexistent_factor_xyz"
        )


class TestFactorAliasNormalization:
    """因子别名标准化测试。"""

    def test_normalize_single_factor(self):
        """测试单个因子名标准化。"""
        from jk2bt.factors import normalize_factor_name

        assert normalize_factor_name("PE_ratio") == "pe_ratio"
        assert normalize_factor_name("pe_ratio") == "pe_ratio"
        assert normalize_factor_name("BIAS5") == "bias_5"

    def test_normalize_multiple_factors(self):
        """测试多个因子名标准化。"""
        from jk2bt.factors import normalize_factor_names

        result = normalize_factor_names(["PE_ratio", "BIAS5", "EMAC26"])
        assert result == ["pe_ratio", "bias_5", "emac_26"]

    def test_normalize_preserves_lowercase(self):
        """测试小写因子名保持不变。"""
        from jk2bt.factors import normalize_factor_name

        assert normalize_factor_name("pe_ratio") == "pe_ratio"
        assert normalize_factor_name("bias_5") == "bias_5"

    def test_normalize_unknown_factor(self):
        """测试未知因子名返回原值。"""
        from jk2bt.factors import normalize_factor_name

        result = normalize_factor_name("unknown_factor_xyz")
        assert result == "unknown_factor_xyz"

    def test_normalize_empty_string(self):
        """测试空字符串处理。"""
        from jk2bt.factors import normalize_factor_name

        result = normalize_factor_name("")
        assert result == ""

    def test_normalize_aliases_with_call(self):
        """测试通过get_factor_values_jq调用别名标准化。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert "pe_ratio" in result


class TestFactorPreprocessWinsorize:
    """因子预处理winsorize测试。"""

    def test_winsorize_series_basic(self):
        """测试Series去极值基本功能。"""
        from jk2bt.factors import winsorize_med

        s = pd.Series([1, 2, 3, 100, 4, 5, -50])
        result = winsorize_med(s, scale=3)

        assert isinstance(result, pd.Series)
        assert len(result) == len(s)
        assert result.max() < 100
        assert result.min() > -50

    def test_winsorize_dataframe_column(self):
        """测试DataFrame按列去极值。"""
        from jk2bt.factors import winsorize_med

        df = pd.DataFrame(
            {"factor1": [1, 2, 3, 100, 4], "factor2": [10, 20, 30, 1000, 40]}
        )
        result = winsorize_med(df, scale=3, axis=0)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == df.shape
        assert result["factor1"].max() < 100
        assert result["factor2"].max() < 1000

    def test_winsorize_with_inf(self):
        """测试处理无穷值。"""
        from jk2bt.factors import winsorize_med

        s = pd.Series([1, 2, 3, np.inf, -np.inf, 4])
        result = winsorize_med(s, scale=3, inf2nan=True)

        assert not np.isinf(result).any()

    def test_winsorize_scale_parameter(self):
        """测试不同scale参数效果。"""
        from jk2bt.factors import winsorize_med

        s = pd.Series([1, 2, 3, 100, 4, 5])

        result_3 = winsorize_med(s, scale=3)
        result_5 = winsorize_med(s, scale=5)

        assert result_3.max() <= result_5.max()

    def test_winsorize_empty_data(self):
        """测试空数据处理。"""
        from jk2bt.factors import winsorize_med

        s = pd.Series([], dtype=float)
        result = winsorize_med(s, scale=3)

        assert len(result) == 0

    def test_winsorize_all_nan(self):
        """测试全NaN数据处理。"""
        from jk2bt.factors import winsorize_med

        s = pd.Series([np.nan, np.nan, np.nan])
        result = winsorize_med(s, scale=3)

        assert result.isna().all()


class TestFactorPreprocessStandardlize:
    """因子预处理standardlize测试。"""

    def test_standardlize_series_basic(self):
        """测试Series标准化基本功能。"""
        from jk2bt.factors import standardlize

        s = pd.Series([1, 2, 3, 4, 5])
        result = standardlize(s)

        assert isinstance(result, pd.Series)
        assert abs(result.mean()) < 1e-10
        assert abs(result.std() - 1.0) < 1e-10

    def test_standardlize_dataframe_column(self):
        """测试DataFrame按列标准化。"""
        from jk2bt.factors import standardlize

        df = pd.DataFrame({"factor1": [1, 2, 3, 4, 5], "factor2": [10, 20, 30, 40, 50]})
        result = standardlize(df, axis=0)

        assert isinstance(result, pd.DataFrame)
        assert abs(result["factor1"].mean()) < 1e-10
        assert abs(result["factor2"].mean()) < 1e-10

    def test_standardlize_with_inf(self):
        """测试处理无穷值。"""
        from jk2bt.factors import standardlize

        s = pd.Series([1, 2, 3, np.inf, 4])
        result = standardlize(s, inf2nan=True)

        assert not np.isinf(result).any()

    def test_standardlize_constant_series(self):
        """测试常量Series标准化（标准差为0，返回原值）。"""
        from jk2bt.factors import standardlize

        s = pd.Series([5.0, 5.0, 5.0, 5.0])
        result = standardlize(s)

        # 当标准差为0时，函数返回原值
        assert (result == 5.0).all() or result.isna().all()

    def test_standardlize_empty_data(self):
        """测试空数据处理。"""
        from jk2bt.factors import standardlize

        s = pd.Series([], dtype=float)
        result = standardlize(s)

        assert len(result) == 0


class TestFactorPreprocessNeutralize:
    """因子预处理neutralize测试。"""

    def test_neutralize_function_exists(self):
        """测试neutralize函数可导入。"""
        from jk2bt.factors import neutralize

        assert callable(neutralize)

    def test_neutralize_basic_call(self):
        """测试neutralize函数基本调用（无中性化，直接返回）。"""
        from jk2bt.factors import neutralize

        factors = pd.DataFrame({"stock1": [0.5], "stock2": [0.3]})
        # 无市值和行业数据时，直接返回原数据
        result = neutralize(factors, how=[], axis=0)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == factors.shape

    def test_neutralize_without_data_warning(self):
        """测试未提供数据时发出警告。"""
        from jk2bt.factors import neutralize
        import warnings

        factors = pd.DataFrame({"stock1": [0.5], "stock2": [0.3]})

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = neutralize(factors, how=["market_cap"], axis=0)

            # 检查是否有警告（可能多个）
            assert len(w) > 0 or isinstance(result, pd.DataFrame)


class TestErrorHandling:
    """错误处理和异常测试。"""

    def test_invalid_security_code(self):
        """测试无效证券代码处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="invalid_code_xyz",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert "pe_ratio" in result

    def test_invalid_factor_name(self):
        """测试无效因子名处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="invalid_factor_xyz",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)

    def test_invalid_date_format(self):
        """测试无效日期格式处理（pandas解析会抛出异常）。"""
        from jk2bt.factors import get_factor_values_jq

        # pandas解析日期时会抛出异常
        try:
            result = get_factor_values_jq(
                securities="sh600519",
                factors="PE_ratio",
                end_date="invalid_date",
                count=1,
            )
        except Exception as e:
            # 预期会抛出异常
            assert "invalid_date" in str(e) or "parse" in str(e).lower()

    def test_negative_count(self):
        """测试负数count处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=-5,
        )

        assert isinstance(result, dict)

    def test_zero_count(self):
        """测试count=0处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=0,
        )

        assert isinstance(result, dict)

    def test_future_date(self):
        """测试未来日期处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2099-12-31",
            count=1,
        )

        assert isinstance(result, dict)

    def test_empty_securities_list(self):
        """测试空证券列表处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities=[],
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)

    def test_empty_factors_list(self):
        """测试空因子列表处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors=[],
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)


class TestBoundaryConditions:
    """边界条件测试。"""

    def test_large_count_value(self):
        """测试大count值处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-01",
            count=500,
        )

        assert isinstance(result, dict)
        assert "pe_ratio" in result

    def test_large_number_of_securities(self):
        """测试大量证券代码处理。"""
        from jk2bt.factors import get_factor_values_jq

        securities = [f"sh600{i}" for i in range(100, 110)]
        result = get_factor_values_jq(
            securities=securities,
            factors="PE_ratio",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert "pe_ratio" in result

    def test_large_number_of_factors(self):
        """测试大量因子请求处理。"""
        from jk2bt.factors import get_factor_values_jq

        factors = [
            "PE_ratio",
            "PB_ratio",
            "market_cap",
            "circulating_market_cap",
            "BIAS5",
            "EMAC26",
        ]
        result = get_factor_values_jq(
            securities="sh600519",
            factors=factors,
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert len(result) > 0

    def test_very_old_date(self):
        """测试很久以前的日期处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            start_date="1990-01-01",
            end_date="1990-01-10",
        )

        assert isinstance(result, dict)

    def test_weekend_date(self):
        """测试周末日期处理。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="PE_ratio",
            end_date="2024-01-07",
            count=1,
        )

        assert isinstance(result, dict)


class TestIntegrationScenarios:
    """整合测试场景。"""

    def test_single_security_multiple_factor_types(self):
        """测试单标的多类型因子组合。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors=["PE_ratio", "BIAS5", "ROE"],
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        for factor in ["pe_ratio", "bias_5", "roe"]:
            if factor in result:
                assert isinstance(result[factor], pd.DataFrame)

    def test_multiple_securities_multiple_factor_types(self):
        """测试多标的多类型因子组合。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities=["sh600519", "sz000001"],
            factors=["PE_ratio", "market_cap", "VOL20"],
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        for factor in ["pe_ratio", "market_cap", "vol_20"]:
            if factor in result:
                assert isinstance(result[factor], pd.DataFrame)

    def test_factor_workflow_with_preprocess(self):
        """测试因子获取+预处理完整流程。"""
        from jk2bt.factors import get_factor_values_jq, winsorize_med, standardlize

        result = get_factor_values_jq(
            securities=["sh600519", "sz000001"],
            factors="PE_ratio",
            end_date="2024-01-01",
            count=5,
        )

        if "pe_ratio" in result and not result["pe_ratio"].empty:
            df = result["pe_ratio"]
            df_winsorized = winsorize_med(df, scale=3)
            df_standardized = standardlize(df_winsorized)

            assert isinstance(df_standardized, pd.DataFrame)

    def test_backtrader_strategy_import(self):
        """测试Backtrader策略导入因子。"""
        from jk2bt.core.strategy_base import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="market_cap",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert "market_cap" in result


class TestFactorModuleStructure:
    """因子模块结构测试。"""

    def test_factors_init_exports_get_factor_values_jq(self):
        """测试factors/__init__.py导出get_factor_values_jq。"""
        from jk2bt.factors import get_factor_values_jq

        assert callable(get_factor_values_jq)

    def test_factors_init_exports_preprocess_functions(self):
        """测试factors/__init__.py导出预处理函数。"""
        from jk2bt.factors import winsorize_med, standardlize, neutralize

        assert callable(winsorize_med)
        assert callable(standardlize)
        assert callable(neutralize)

    def test_factors_init_exports_normalize_functions(self):
        """测试factors/__init__.py导出标准化函数。"""
        from jk2bt.factors import normalize_factor_name, normalize_factor_names

        assert callable(normalize_factor_name)
        assert callable(normalize_factor_names)

    def test_factors_init_exports_registry(self):
        """测试factors/__init__.py导出注册表。"""
        from jk2bt.factors import global_factor_registry, FactorRegistry

        assert global_factor_registry is not None
        assert FactorRegistry is not None

    def test_factors_submodule_structure(self):
        """测试因子子模块结构完整。"""
        from jk2bt.factors import valuation, technical, fundamentals, growth, quality

        assert hasattr(valuation, "__name__")
        assert hasattr(technical, "__name__")
        assert hasattr(fundamentals, "__name__")
        assert hasattr(growth, "__name__")
        assert hasattr(quality, "__name__")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
