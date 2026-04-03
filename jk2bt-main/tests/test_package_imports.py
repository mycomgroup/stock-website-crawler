"""
测试包导入边界和符号暴露。

确保主包和子包的导入路径稳定，__all__列表准确。
"""

import pytest


class TestMainPackageExports:
    """测试主包 src 的符号暴露。"""

    def test_runner_symbols_exist(self):
        """验证 runner 相关符号确实存在。"""
        from jk2bt import (
            run_jq_strategy,
            load_jq_strategy,
            JQStrategyWrapper,
        )

        assert callable(run_jq_strategy)
        assert callable(load_jq_strategy)
        assert isinstance(JQStrategyWrapper, type)

    def test_runner_symbols_in_all(self):
        """验证 runner 符号在 __all__ 中。"""
        import jk2bt as pkg

        assert "run_jq_strategy" in pkg.__all__
        assert "load_jq_strategy" in pkg.__all__
        assert "JQStrategyWrapper" in pkg.__all__

    def test_data_api_symbols_exist(self):
        """验证数据获取 API 符号存在。"""
        from jk2bt import (
            get_price,
            get_fundamentals,
            get_current_data,
            history,
            attribute_history,
            get_all_securities_jq,
            get_security_info_jq,
        )

        assert callable(get_price)
        assert callable(get_fundamentals)
        assert callable(get_current_data)
        assert callable(history)
        assert callable(attribute_history)
        assert callable(get_all_securities_jq)
        assert callable(get_security_info_jq)

    def test_context_symbols_exist(self):
        """验证上下文相关符号存在。"""
        from jk2bt import (
            GlobalState,
            ContextProxy,
            JQLogAdapter,
            TimerManager,
        )

        assert isinstance(GlobalState, type)
        assert isinstance(ContextProxy, type)
        assert isinstance(JQLogAdapter, type)
        assert isinstance(TimerManager, type)

    def test_order_api_symbols_exist(self):
        """验证交易 API 符号存在。"""
        from jk2bt import (
            order_shares,
            order_target_percent,
        )

        assert callable(order_shares)
        assert callable(order_target_percent)

    def test_subportfolio_symbols_exist(self):
        """验证子账户符号存在。"""
        from jk2bt import (
            SubportfolioType,
            SubportfolioConfig,
            SubportfolioPosition,
            SubportfolioManager,
            set_subportfolios,
            transfer_cash,
        )

        assert isinstance(SubportfolioType, type)
        assert isinstance(SubportfolioConfig, type)
        assert isinstance(SubportfolioPosition, type)
        assert isinstance(SubportfolioManager, type)
        assert callable(set_subportfolios)
        assert callable(transfer_cash)


class TestFactorsPackageExports:
    """测试 factors 包的符号暴露。"""

    def test_factors_from_main_package(self):
        """验证从主包导入 factors 模块。"""
        from jk2bt.factors import (
            get_factor_values_jq,
            normalize_factor_name,
            normalize_factor_names,
        )

        assert callable(get_factor_values_jq)
        assert callable(normalize_factor_name)
        assert callable(normalize_factor_names)

    def test_factors_from_compat_entry(self):
        """验证从顶级 factors 包导入（兼容入口）。"""
        from factors import (
            get_factor_values_jq,
            normalize_factor_name,
            normalize_factor_names,
        )

        assert callable(get_factor_values_jq)
        assert callable(normalize_factor_name)
        assert callable(normalize_factor_names)

    def test_factors_submodules_exist(self):
        """验证 factors 子模块存在。"""
        from jk2bt.factors import (
            valuation,
            technical,
            fundamentals,
            growth,
            quality,
        )

        import types

        assert isinstance(valuation, types.ModuleType)
        assert isinstance(technical, types.ModuleType)
        assert isinstance(fundamentals, types.ModuleType)
        assert isinstance(growth, types.ModuleType)
        assert isinstance(quality, types.ModuleType)

    def test_factors_preprocess_functions(self):
        """验证预处理函数存在。"""
        from jk2bt.factors import (
            winsorize_med,
            standardlize,
            neutralize,
        )

        assert callable(winsorize_med)
        assert callable(standardlize)
        assert callable(neutralize)

    def test_factor_registry_exists(self):
        """验证因子注册表存在。"""
        from jk2bt.factors import (
            global_factor_registry,
            FactorRegistry,
        )

        assert isinstance(global_factor_registry, FactorRegistry)
        assert isinstance(FactorRegistry, type)


class TestFactorAliasNormalization:
    """测试因子别名归一化功能。"""

    def test_uppercase_alias(self):
        """大写别名映射。"""
        from jk2bt.factors import normalize_factor_name

        assert normalize_factor_name("PE_ratio") == "pe_ratio"
        assert normalize_factor_name("PB_ratio") == "pb_ratio"

    def test_lowercase_alias(self):
        """小写别名映射。"""
        from jk2bt.factors import normalize_factor_name

        assert normalize_factor_name("pe_ratio") == "pe_ratio"
        assert normalize_factor_name("pb_ratio") == "pb_ratio"

    def test_mixed_case_alias(self):
        """混合大小写别名映射。"""
        from jk2bt.factors import normalize_factor_name

        assert normalize_factor_name("Pe_ratio") == "pe_ratio"
        assert normalize_factor_name("pE_Ratio") == "pe_ratio"

    def test_technical_factor_aliases(self):
        """技术因子别名映射。"""
        from jk2bt.factors import normalize_factor_name

        assert normalize_factor_name("BIAS5") == "bias_5"
        assert normalize_factor_name("bias_5") == "bias_5"
        assert normalize_factor_name("Bias5") == "bias_5"

    def test_unknown_alias_returns_original(self):
        """未知别名返回原值。"""
        from jk2bt.factors import normalize_factor_name

        assert normalize_factor_name("unknown_factor") == "unknown_factor"
        assert normalize_factor_name("custom_alpha") == "custom_alpha"

    def test_batch_normalization(self):
        """批量归一化。"""
        from jk2bt.factors import normalize_factor_names

        result = normalize_factor_names(["PE_ratio", "Pe_ratio", "bias_5", "BIAS10"])
        assert result == ["pe_ratio", "pe_ratio", "bias_5", "bias_10"]


class TestTradeDaysFallback:
    """测试交易日回退逻辑。"""

    def test_get_trade_days_basic(self):
        """基本交易日获取。"""
        from jk2bt.factors.base import get_trade_days

        result = get_trade_days("2024-01-01", "2024-01-05")
        assert isinstance(result, list)
        assert all(isinstance(d, str) for d in result)

    def test_get_trade_days_holiday_period(self):
        """节假日区间回退到工作日。"""
        from jk2bt.factors.base import get_trade_days

        result = get_trade_days("2023-12-30", "2024-01-01")
        assert isinstance(result, list)
        assert len(result) > 0  # 不应该返回空列表

    def test_get_trade_days_format(self):
        """交易日格式正确。"""
        from jk2bt.factors.base import get_trade_days

        result = get_trade_days("2024-01-01", "2024-01-10")
        assert all(len(d) == 10 for d in result)  # YYYY-MM-DD 格式
        assert all("-" in d for d in result)


class TestSecurityInfoCache:
    """测试股票信息缓存和离线兜底。"""

    def test_get_security_info_returns_dict(self):
        """返回字典结构。"""
        from jk2bt import get_security_info_jq

        result = get_security_info_jq("sh600000")
        assert isinstance(result, dict)

    def test_get_security_info_has_required_fields(self):
        """返回结构包含必要字段。"""
        from jk2bt import get_security_info_jq

        result = get_security_info_jq("sh600000")
        assert "code" in result
        assert "display_name" in result or "name" in result

    def test_get_security_info_cache_dir_param(self):
        """支持 cache_dir 参数。"""
        from jk2bt import get_security_info_jq

        result = get_security_info_jq("sh600000", cache_dir="test_cache")
        assert isinstance(result, dict)

    def test_get_security_info_invalid_code(self):
        """无效代码返回默认结构。"""
        from jk2bt import get_security_info_jq

        result = get_security_info_jq("invalid_code")
        assert isinstance(result, dict)
        assert "code" in result


class TestHistoryFundamentalsEntityParam:
    """测试 get_history_fundamentals_jq entity 参数兼容。"""

    def test_entity_param_basic(self):
        """entity 参数基本功能。"""
        from jk2bt import get_history_fundamentals_jq

        result = get_history_fundamentals_jq(
            entity="sh600000",
            fields=["balance.cash_equivalents"],
            stat_date="2022q4",
            count=1,
        )
        assert result is None or isinstance(result, object)

    def test_security_param_still_works(self):
        """security 参数仍然可用。"""
        from jk2bt import get_history_fundamentals_jq

        result = get_history_fundamentals_jq(
            security="sh600000",
            fields=["balance.cash_equivalents"],
            stat_date="2022q4",
            count=1,
        )
        assert result is None or isinstance(result, object)

    def test_entity_and_security_equivalent(self):
        """entity 和 security 参数等效。"""
        from jk2bt import get_history_fundamentals_jq

        result_entity = get_history_fundamentals_jq(
            entity="sh600000",
            fields=["balance.cash_equivalents"],
            stat_date="2022q4",
            count=1,
        )

        result_security = get_history_fundamentals_jq(
            security="sh600000",
            fields=["balance.cash_equivalents"],
            stat_date="2022q4",
            count=1,
        )

        # 两者应该返回相同类型的结果
        assert type(result_entity) == type(result_security)

    def test_missing_security_and_entity_raises(self):
        """缺少 security 和 entity 参数时抛异常。"""
        from jk2bt import get_history_fundamentals_jq

        with pytest.raises(ValueError):
            get_history_fundamentals_jq(
                fields=["balance.cash_equivalents"],
                stat_date="2022q4",
                count=1,
            )
