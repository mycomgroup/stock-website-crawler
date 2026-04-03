"""
test_compat_import.py
兼容导入层测试 - 验证旧导入路径仍然可用

测试覆盖：
- factors 模块（含子模块）
- backtrader_base_strategy 模块
- subportfolios 模块
- db 模块
- 导入后符号可访问性
- 新旧导入路径一致性
"""

import pytest


class TestFactorsCompatImport:
    """factors 兼容导入测试"""

    def test_factors_main_import(self):
        """测试 factors 主模块导入"""
        from factors import get_factor_values_jq

        assert callable(get_factor_values_jq)

    def test_factors_preprocess_import(self):
        """测试 factors 预处理函数导入"""
        from factors import winsorize_med, standardlize, neutralize

        assert callable(winsorize_med)
        assert callable(standardlize)
        assert callable(neutralize)

    def test_factors_registry_import(self):
        """测试 factors 注册表导入"""
        from factors import global_factor_registry, FactorRegistry

        assert global_factor_registry is not None
        assert FactorRegistry is not None

    def test_factors_normalize_import(self):
        """测试 factors 名称规范化函数导入"""
        from factors import normalize_factor_name, normalize_factor_names

        assert callable(normalize_factor_name)
        assert callable(normalize_factor_names)

    def test_factors_submodule_valuation(self):
        """测试 factors.valuation 子模块导入"""
        from factors import valuation

        assert valuation is not None

    def test_factors_submodule_technical(self):
        """测试 factors.technical 子模块导入"""
        from factors import technical

        assert technical is not None

    def test_factors_submodule_fundamentals(self):
        """测试 factors.fundamentals 子模块导入"""
        from factors import fundamentals

        assert fundamentals is not None

    def test_factors_submodule_growth(self):
        """测试 factors.growth 子模块导入"""
        from factors import growth

        assert growth is not None

    def test_factors_submodule_quality(self):
        """测试 factors.quality 子模块导入"""
        from factors import quality

        assert quality is not None

    def test_factors_star_import(self):
        """测试 factors 星号导入"""
        import factors

        exported = factors.__all__
        assert "get_factor_values_jq" in exported
        assert "winsorize_med" in exported
        assert "standardlize" in exported
        assert "neutralize" in exported

    def test_factors_consistency_with_new_path(self):
        """测试 factors 新旧导入路径一致性"""
        from factors import get_factor_values_jq as old_import
        from jk2bt.factors import (
            get_factor_values_jq as new_import,
        )

        assert old_import is new_import


class TestBacktraderBaseStrategyCompatImport:
    """backtrader_base_strategy 兼容导入测试"""

    def test_bbs_main_import(self):
        """测试 backtrader_base_strategy 主模块导入"""
        from jk2bt.core.strategy_base import get_price_jq

        assert callable(get_price_jq)

    def test_bbs_price_functions(self):
        """测试行情函数导入"""
        from jk2bt.core.strategy_base import (
            get_price,
            get_price_jq,
            get_price_unified,
            history,
            attribute_history,
        )

        assert callable(get_price)
        assert callable(get_price_jq)
        assert callable(get_price_unified)
        assert callable(history)
        assert callable(attribute_history)

    def test_bbs_fundamentals_functions(self):
        """测试财务函数导入"""
        from jk2bt.core.strategy_base import (
            get_fundamentals,
            get_fundamentals_jq,
            get_history_fundamentals,
            get_history_fundamentals_jq,
        )

        assert callable(get_fundamentals)
        assert callable(get_fundamentals_jq)
        assert callable(get_history_fundamentals)
        assert callable(get_history_fundamentals_jq)

    def test_bbs_meta_functions(self):
        """测试元数据函数导入"""
        from jk2bt.core.strategy_base import (
            get_all_securities_jq,
            get_security_info_jq,
            get_all_trade_days_jq,
        )

        assert callable(get_all_securities_jq)
        assert callable(get_security_info_jq)
        assert callable(get_all_trade_days_jq)

    def test_bbs_extras_functions(self):
        """测试额外数据函数导入"""
        from jk2bt.core.strategy_base import (
            get_extras_jq,
            get_bars_jq,
            get_billboard_list_jq,
        )

        assert callable(get_extras_jq)
        assert callable(get_bars_jq)
        assert callable(get_billboard_list_jq)

    def test_bbs_factor_functions(self):
        """测试因子函数导入"""
        from jk2bt.core.strategy_base import (
            get_factor_values_jq,
            winsorize_med,
            standardlize,
            neutralize,
        )

        assert callable(get_factor_values_jq)
        assert callable(winsorize_med)
        assert callable(standardlize)
        assert callable(neutralize)

    def test_bbs_index_functions(self):
        """测试指数函数导入"""
        from jk2bt.core.strategy_base import (
            get_index_weights,
            get_index_stocks,
        )

        assert callable(get_index_weights)
        assert callable(get_index_stocks)

    def test_bbs_data_functions(self):
        """测试数据获取函数导入"""
        from jk2bt.core.strategy_base import (
            get_akshare_stock_data,
            get_akshare_etf_data,
            get_current_data,
        )

        assert callable(get_akshare_stock_data)
        assert callable(get_akshare_etf_data)
        assert callable(get_current_data)

    def test_bbs_code_conversion(self):
        """测试代码转换函数导入"""
        from jk2bt.core.strategy_base import (
            format_stock_symbol_for_akshare,
            jq_code_to_ak,
            ak_code_to_jq,
        )

        assert callable(format_stock_symbol_for_akshare)
        assert callable(jq_code_to_ak)
        assert callable(ak_code_to_jq)

    def test_bbs_order_functions(self):
        """测试下单函数导入"""
        from jk2bt.core.strategy_base import (
            order_target,
            order_value,
            order,
        )

        assert callable(order_target)
        assert callable(order_value)
        assert callable(order)

    def test_bbs_table_proxies(self):
        """测试表代理对象导入"""
        from jk2bt.core.strategy_base import (
            valuation,
            income,
            balance,
            cash_flow,
            indicator,
            finance,
            query,
        )

        assert valuation is not None
        assert income is not None
        assert balance is not None
        assert cash_flow is not None
        assert indicator is not None
        assert finance is not None
        assert callable(query)

    def test_bbs_classes(self):
        """测试类导入"""
        from jk2bt.core.strategy_base import (
            JQ2BTBaseStrategy,
            GlobalState,
            ContextProxy,
            JQLogAdapter,
            TimerManager,
        )

        assert JQ2BTBaseStrategy is not None
        assert GlobalState is not None
        assert ContextProxy is not None
        assert JQLogAdapter is not None
        assert TimerManager is not None

    def test_bbs_log_object(self):
        """测试 log 对象导入"""
        from jk2bt.core.strategy_base import log

        assert log is not None
        assert hasattr(log, "info")
        assert hasattr(log, "warn")
        assert hasattr(log, "error")

    def test_bbs_finance_db(self):
        """测试 finance_db 对象导入"""
        from jk2bt.core.strategy_base import finance_db

        assert finance_db is not None
        assert hasattr(finance_db, "run_query")

    def test_bbs_analysis_functions(self):
        """测试分析函数导入"""
        from jk2bt.core.strategy_base import (
            analyze_performance,
            run_bt_framework,
        )

        assert callable(analyze_performance)
        assert callable(run_bt_framework)

    def test_bbs_consistency_with_new_path(self):
        """测试 backtrader_base_strategy 新旧导入路径一致性"""
        from jk2bt.core.strategy_base import get_price_jq as old_import
        from jk2bt.core.strategy_base import (
            get_price_jq as new_import,
        )

        assert old_import is new_import


class TestSubportfoliosCompatImport:
    """subportfolios 兼容导入测试"""

    def test_subportfolios_classes(self):
        """测试子账户类导入"""
        from subportfolios import (
            SubportfolioType,
            SubportfolioConfig,
            SubportfolioPosition,
            SubportfolioCashAccount,
            SubportfolioProxy,
            SubportfolioManager,
        )

        assert SubportfolioType is not None
        assert SubportfolioConfig is not None
        assert SubportfolioPosition is not None
        assert SubportfolioCashAccount is not None
        assert SubportfolioProxy is not None
        assert SubportfolioManager is not None

    def test_subportfolios_enums(self):
        """测试枚举类型"""
        from subportfolios import SubportfolioType

        assert hasattr(SubportfolioType, "STOCK")
        assert hasattr(SubportfolioType, "ETF")
        assert hasattr(SubportfolioType, "FUTURE")
        assert hasattr(SubportfolioType, "FUND")
        assert hasattr(SubportfolioType, "MIXED")

    def test_subportfolios_functions(self):
        """测试子账户函数导入"""
        from subportfolios import (
            set_subportfolios,
            transfer_cash,
            get_subportfolio_summary,
        )

        assert callable(set_subportfolios)
        assert callable(transfer_cash)
        assert callable(get_subportfolio_summary)

    def test_subportfolios_manager_creation(self):
        """测试子账户管理器创建"""
        from subportfolios import SubportfolioManager

        manager = SubportfolioManager()
        assert manager is not None
        assert len(manager) == 0

    def test_subportfolios_config_creation(self):
        """测试子账户配置创建"""
        from subportfolios import SubportfolioConfig, SubportfolioType

        config = SubportfolioConfig(
            name="test",
            type=SubportfolioType.STOCK,
            initial_cash=100000,
        )
        assert config.name == "test"
        assert config.type == SubportfolioType.STOCK
        assert config.initial_cash == 100000

    def test_subportfolios_consistency_with_new_path(self):
        """测试 subportfolios 新旧导入路径一致性"""
        from subportfolios import SubportfolioManager as old_import
        from jk2bt.strategy.subportfolios import (
            SubportfolioManager as new_import,
        )

        assert old_import is new_import


class TestDbCompatImport:
    """db 兼容导入测试"""

    def test_db_main_import(self):
        """测试 db 主模块导入"""
        from jk2bt.db import DuckDBManager

        assert DuckDBManager is not None

    def test_db_duckdb_manager_import(self):
        """测试 db.duckdb_manager 导入"""
        from jk2bt.db.duckdb_manager import DuckDBManager

        assert DuckDBManager is not None

    def test_db_duckdb_manager_functions(self):
        """测试 db.duckdb_manager 函数导入"""
        from jk2bt.db.duckdb_manager import (
            DuckDBManager,
            LocalCache,
            clear_global_cache,
            get_shared_read_only_manager,
            get_writer_manager,
        )

        assert DuckDBManager is not None
        assert LocalCache is not None
        assert callable(clear_global_cache)
        assert callable(get_shared_read_only_manager)
        assert callable(get_writer_manager)

    def test_db_cache_manager_import(self):
        """测试 db.CacheManager 导入"""
        from jk2bt.db import CacheManager, get_cache_manager, check_cache_status

        assert CacheManager is not None
        assert callable(get_cache_manager)
        assert callable(check_cache_status)

    def test_db_migrate_import(self):
        """测试 db 迁移函数导入"""
        from jk2bt.db import (
            auto_migrate,
            migrate_stock_pickles,
            migrate_etf_pickles,
            migrate_index_pickles,
        )

        assert callable(auto_migrate)
        assert callable(migrate_stock_pickles)
        assert callable(migrate_etf_pickles)
        assert callable(migrate_index_pickles)

    def test_db_manager_creation(self):
        """测试 DuckDBManager 创建"""
        from jk2bt.db import DuckDBManager

        manager = DuckDBManager()
        assert manager is not None

    def test_db_consistency_with_new_path(self):
        """测试 db 新旧导入路径一致性"""
        from jk2bt.db import DuckDBManager as old_import
        from jk2bt.db import DuckDBManager as new_import

        assert old_import is new_import


class TestMixedCompatImport:
    """混合兼容导入测试"""

    def test_mixed_import_session1(self):
        """测试混合导入会话1"""
        from factors import get_factor_values_jq
        from jk2bt.core.strategy_base import get_price_jq
        from subportfolios import SubportfolioManager
        from jk2bt.db import DuckDBManager

        assert callable(get_factor_values_jq)
        assert callable(get_price_jq)
        assert SubportfolioManager is not None
        assert DuckDBManager is not None

    def test_mixed_import_session2(self):
        """测试混合导入会话2"""
        from factors import valuation, technical
        from jk2bt.core.strategy_base import query, get_fundamentals

        assert valuation is not None
        assert technical is not None
        assert callable(query)
        assert callable(get_fundamentals)

    def test_mixed_import_with_new_package(self):
        """测试新旧导入混合使用"""
        from factors import normalize_factor_name as old_factors
        from jk2bt.factors import (
            normalize_factor_name as new_factors,
        )
        from jk2bt.core.strategy_base import jq_code_to_ak as old_code
        from jk2bt import jq_code_to_ak as new_code

        assert old_factors is new_factors
        assert old_code is new_code


class TestCompatImportCallable:
    """兼容导入可调用性测试"""

    def test_factors_callable_basic(self):
        """测试 factors 函数基本可调用"""
        from factors import normalize_factor_name

        result = normalize_factor_name("PE_ratio")
        assert result == "pe_ratio"

    def test_factors_callable_batch(self):
        """测试 factors 函数批量处理"""
        from factors import normalize_factor_names

        result = normalize_factor_names(["PE_ratio", "PB_ratio"])
        assert result == ["pe_ratio", "pb_ratio"]

    def test_backtrader_code_conversion_callable(self):
        """测试代码转换函数可调用"""
        from jk2bt.core.strategy_base import jq_code_to_ak, ak_code_to_jq

        result1 = jq_code_to_ak("600519.XSHG")
        assert result1 == "sh600519"
        result2 = ak_code_to_jq("sh600519")
        assert result2 == "600519.XSHG"

    def test_backtrader_format_stock_symbol_callable(self):
        """测试股票代码格式化可调用"""
        from jk2bt.core.strategy_base import format_stock_symbol_for_akshare

        result = format_stock_symbol_for_akshare("sh600519")
        assert result == "600519"

    def test_subportfolios_enum_callable(self):
        """测试子账户枚举值使用"""
        from subportfolios import SubportfolioType

        assert SubportfolioType.STOCK.value == "stock"
        assert SubportfolioType.ETF.value == "etf"
        assert SubportfolioType.FUTURE.value == "future"


class TestCompatImportAllSymbols:
    """兼容导入 __all__ 测试"""

    def test_factors_all_symbols(self):
        """测试 factors __all__ 符号"""
        import factors

        for sym in factors.__all__:
            obj = getattr(factors, sym, None)
            assert obj is not None, f"factors.{sym} not accessible"

    def test_backtrader_base_strategy_all_symbols(self):
        """测试 backtrader_base_strategy __all__ 符号"""
        import backtrader_base_strategy

        for sym in backtrader_base_strategy.__all__:
            obj = getattr(backtrader_base_strategy, sym, None)
            assert obj is not None, f"backtrader_base_strategy.{sym} not accessible"

    def test_subportfolios_all_symbols(self):
        """测试 subportfolios __all__ 符号"""
        import subportfolios

        for sym in subportfolios.__all__:
            obj = getattr(subportfolios, sym, None)
            assert obj is not None, f"subportfolios.{sym} not accessible"

    def test_db_all_symbols(self):
        """测试 db __all__ 符号"""
        import db

        for sym in db.__all__:
            obj = getattr(db, sym, None)
            assert obj is not None, f"db.{sym} not accessible"


class TestAssetRouterCompat:
    """资产路由兼容测试"""

    def test_identify_stock(self):
        """测试股票识别"""
        from jk2bt.core.strategy_base import identify_asset, AssetType

        info = identify_asset("sh600519")
        assert info.asset_type == AssetType.STOCK
        assert info.is_supported()

    def test_identify_etf(self):
        """测试 ETF 识别"""
        from jk2bt.core.strategy_base import identify_asset, AssetType

        info = identify_asset("510300")
        assert info.asset_type == AssetType.ETF
        assert info.is_supported()

    def test_identify_fund_of(self):
        """测试场外基金识别"""
        from jk2bt.core.strategy_base import identify_asset, AssetType

        info = identify_asset("000001.OF")
        assert info.asset_type == AssetType.FUND_OF
        assert info.is_identified_only()
        assert not info.is_supported()

    def test_identify_future_ccfx(self):
        """测试股指期货识别"""
        from jk2bt.core.strategy_base import identify_asset, AssetType

        info = identify_asset("IF2312.CCFX")
        assert info.asset_type == AssetType.FUTURE_CCFX
        assert info.is_identified_only()
        assert not info.is_supported()

    def test_identify_index(self):
        """测试指数识别"""
        from jk2bt.core.strategy_base import identify_asset, AssetType

        info = identify_asset("000300.XSHG")
        assert info.asset_type == AssetType.INDEX
        assert info.is_identified_only()

    def test_is_stock_function(self):
        """测试 is_stock 函数"""
        from jk2bt.core.strategy_base import is_stock

        assert is_stock("sh600519") is True
        assert is_stock("510300") is False

    def test_is_etf_function(self):
        """测试 is_etf 函数"""
        from jk2bt.core.strategy_base import is_etf

        assert is_etf("510300") is True
        assert is_etf("sh600519") is False

    def test_is_fund_of_function(self):
        """测试 is_fund_of 函数"""
        from jk2bt.core.strategy_base import is_fund_of

        assert is_fund_of("000001.OF") is True
        assert is_fund_of("sh600519") is False

    def test_is_future_function(self):
        """测试 is_future 函数"""
        from jk2bt.core.strategy_base import is_future

        assert is_future("IF2312.CCFX") is True
        assert is_future("sh600519") is False

    def test_is_index_function(self):
        """测试 is_index 函数"""
        from jk2bt.core.strategy_base import is_index

        assert is_index("000300.XSHG") is True
        assert is_index("sh600519") is False


class TestDeepImportChain:
    """深度导入链测试"""

    def test_factors_to_backtrader_chain(self):
        """测试 factors -> backtrader_base_strategy 链功能一致"""
        from factors import winsorize_med
        from jk2bt.core.strategy_base import winsorize_med as bbs_wm

        assert callable(winsorize_med)
        assert callable(bbs_wm)

    def test_package_to_factors_chain(self):
        """测试 package -> factors 链功能一致"""
        from jk2bt.factors import winsorize_med as pkg_wm
        from factors import winsorize_med as fac_wm

        assert pkg_wm is fac_wm

    def test_full_chain_consistency(self):
        """测试完整导入链功能一致"""
        from jk2bt.factors import winsorize_med as src
        from factors import winsorize_med as compat

        assert src is compat


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
