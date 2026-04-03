"""
tests/test_package_import.py
包入口导入测试 - 验证所有对外符号可正常导入并具有正确行为
"""

import pytest
import inspect
import pandas as pd
import numpy as np


class TestPackageImport:
    """测试包导入"""

    def test_package_import(self):
        """测试包可以正常导入"""
        import jk2bt as pkg

        assert pkg is not None

    def test_version_info(self):
        """测试版本信息存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "__version__")
        assert hasattr(pkg, "__author__")
        assert isinstance(pkg.__version__, str)
        assert len(pkg.__version__) > 0


class TestAllSymbolsExported:
    """测试所有符号都已导出"""

    def test_all_symbols_in__all__are_accessible(self):
        """测试__all__中的符号都能正常访问"""
        import jk2bt as pkg

        for sym in pkg.__all__:
            obj = getattr(pkg, sym, None)
            assert obj is not None, f"{sym} in __all__ but not accessible"


class TestRunnerSymbols:
    """测试核心运行器符号"""

    def test_run_jq_strategy_exists(self):
        """测试 run_jq_strategy 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "run_jq_strategy")
        assert callable(pkg.run_jq_strategy)

    def test_run_jq_strategy_signature(self):
        """测试 run_jq_strategy 签名"""
        import jk2bt as pkg

        sig = inspect.signature(pkg.run_jq_strategy)
        params = list(sig.parameters.keys())
        assert "strategy_file" in params
        assert "start_date" in params
        assert "end_date" in params

    def test_load_jq_strategy_exists(self):
        """测试 load_jq_strategy 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "load_jq_strategy")
        assert callable(pkg.load_jq_strategy)

    def test_load_jq_strategy_signature(self):
        """测试 load_jq_strategy 签名"""
        import jk2bt as pkg

        sig = inspect.signature(pkg.load_jq_strategy)
        params = list(sig.parameters.keys())
        assert "strategy_file" in params

    def test_jq_strategy_wrapper_exists(self):
        """测试 JQStrategyWrapper 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "JQStrategyWrapper")
        assert isinstance(pkg.JQStrategyWrapper, type)

    def test_jq_strategy_wrapper_is_strategy(self):
        """测试 JQStrategyWrapper 是策略类"""
        import jk2bt as pkg

        import backtrader as bt

        assert issubclass(pkg.JQStrategyWrapper, bt.Strategy)


class TestBaseStrategySymbols:
    """测试基础策略类"""

    def test_jq2bt_base_strategy_exists(self):
        """测试 JQ2BTBaseStrategy 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "JQ2BTBaseStrategy")
        assert isinstance(pkg.JQ2BTBaseStrategy, type)

    def test_jq2bt_base_strategy_is_strategy(self):
        """测试 JQ2BTBaseStrategy 是策略类"""
        import jk2bt as pkg
        import backtrader as bt

        assert issubclass(pkg.JQ2BTBaseStrategy, bt.Strategy)

    def test_global_state_exists(self):
        """测试 GlobalState 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "GlobalState")
        assert isinstance(pkg.GlobalState, type)

    def test_global_state_can_instantiate(self):
        """测试 GlobalState 可以实例化"""
        import jk2bt as pkg

        g = pkg.GlobalState()
        assert hasattr(g, "__dict__")

    def test_context_proxy_exists(self):
        """测试 ContextProxy 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "ContextProxy")
        assert isinstance(pkg.ContextProxy, type)

    def test_jq_log_adapter_exists(self):
        """测试 JQLogAdapter 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "JQLogAdapter")
        assert isinstance(pkg.JQLogAdapter, type)

    def test_timer_manager_exists(self):
        """测试 TimerManager 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "TimerManager")
        assert isinstance(pkg.TimerManager, type)


class TestDataAPISymbols:
    """测试数据API符号"""

    def test_get_price_exists(self):
        """测试 get_price 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_price")
        assert callable(pkg.get_price)

    def test_get_price_variants_exist(self):
        """测试 get_price 变体存在"""
        import jk2bt as pkg

        # 实际存在的 get_price 变体
        for sym in ["get_price", "get_price_jq"]:
            assert hasattr(pkg, sym), f"{sym} should exist"

    def test_get_fundamentals_exists(self):
        """测试 get_fundamentals 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_fundamentals")
        assert callable(pkg.get_fundamentals)

    def test_get_current_data_exists(self):
        """测试 get_current_data 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_current_data")
        assert callable(pkg.get_current_data)

    def test_get_current_data_variants_exist(self):
        """测试 get_current_data 变体存在"""
        import jk2bt as pkg

        for sym in ["get_current_data_cached", "get_current_data_batch"]:
            assert hasattr(pkg, sym), f"{sym} should exist"

    def test_history_exists(self):
        """测试 history 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "history")
        assert callable(pkg.history)

    def test_attribute_history_exists(self):
        """测试 attribute_history 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "attribute_history")
        assert callable(pkg.attribute_history)

    def test_get_index_weights_exists(self):
        """测试 get_index_weights 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_index_weights")
        assert callable(pkg.get_index_weights)

    def test_get_index_stocks_exists(self):
        """测试 get_index_stocks 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_index_stocks")
        assert callable(pkg.get_index_stocks)

    def test_get_all_securities_jq_exists(self):
        """测试 get_all_securities_jq 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_all_securities_jq")
        assert callable(pkg.get_all_securities_jq)

    def test_get_security_info_jq_exists(self):
        """测试 get_security_info_jq 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_security_info_jq")
        assert callable(pkg.get_security_info_jq)

    def test_get_factor_values_jq_exists(self):
        """测试 get_factor_values_jq 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_factor_values_jq")
        assert callable(pkg.get_factor_values_jq)

    def test_get_bars_variants_exist(self):
        """测试 get_bars 变体存在"""
        import jk2bt as pkg

        # 实际存在的 get_bars 变体
        for sym in ["get_bars", "get_bars_jq"]:
            assert hasattr(pkg, sym), f"{sym} should exist"


class TestFinanceSymbols:
    """测试财务数据符号"""

    def test_query_exists(self):
        """测试 query 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "query")
        assert callable(pkg.query)

    def test_finance_tables_exist(self):
        """测试财务表对象存在"""
        import jk2bt as pkg

        for sym in [
            "valuation",
            "income",
            "balance",
            "cash_flow",
            "indicator",
            "finance",
        ]:
            assert hasattr(pkg, sym), f"{sym} should exist"

    def test_indicator_functions_exist(self):
        """测试指标函数存在"""
        import jk2bt as pkg

        for sym in [
            "get_indicator_data",
            "get_indicator_batch",
            "get_indicator_ranking",
            "filter_by_indicator",
        ]:
            assert hasattr(pkg, sym), f"{sym} should exist"


class TestTradingSymbols:
    """测试交易API符号"""

    def test_order_shares_exists(self):
        """测试 order_shares 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "order_shares")
        assert callable(pkg.order_shares)

    def test_order_target_percent_exists(self):
        """测试 order_target_percent 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "order_target_percent")
        assert callable(pkg.order_target_percent)

    def test_filter_functions_exist(self):
        """测试过滤函数存在"""
        import jk2bt as pkg

        for sym in [
            "filter_st",
            "filter_paused",
            "filter_limit_up",
            "filter_limit_down",
            "filter_new_stocks",
        ]:
            assert hasattr(pkg, sym), f"{sym} should exist"

    def test_limit_functions_exist(self):
        """测试涨跌停函数存在"""
        import jk2bt as pkg

        for sym in ["get_high_limit", "get_low_limit"]:
            assert hasattr(pkg, sym), f"{sym} should exist"


class TestStrategyHelperSymbols:
    """测试策略辅助符号"""

    def test_calculate_ma_exists(self):
        """测试 calculate_ma 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "calculate_ma")
        assert callable(pkg.calculate_ma)

    def test_calculate_ma_works(self):
        """测试 calculate_ma 基本工作"""
        import jk2bt as pkg

        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result = pkg.calculate_ma(data, window=3)
        assert isinstance(result, pd.Series)
        assert len(result) == len(data)

    def test_calculate_ema_exists(self):
        """测试 calculate_ema 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "calculate_ema")
        assert callable(pkg.calculate_ema)

    def test_calculate_std_exists(self):
        """测试 calculate_std 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "calculate_std")
        assert callable(pkg.calculate_std)

    def test_calculate_boll_exists(self):
        """测试 calculate_boll 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "calculate_boll")
        assert callable(pkg.calculate_boll)

    def test_calculate_rsi_exists(self):
        """测试 calculate_rsi 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "calculate_rsi")
        assert callable(pkg.calculate_rsi)

    def test_calculate_macd_exists(self):
        """测试 calculate_macd 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "calculate_macd")
        assert callable(pkg.calculate_macd)

    def test_calculate_kdj_exists(self):
        """测试 calculate_kdj 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "calculate_kdj")
        assert callable(pkg.calculate_kdj)

    def test_calculate_atr_exists(self):
        """测试 calculate_atr 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "calculate_atr")
        assert callable(pkg.calculate_atr)

    def test_performance_functions_exist(self):
        """测试绩效函数存在"""
        import jk2bt as pkg

        for sym in [
            "calculate_sharpe",
            "calculate_max_drawdown",
            "calculate_annualized_return",
            "calculate_volatility",
        ]:
            assert hasattr(pkg, sym), f"{sym} should exist"


class TestPositionSymbols:
    """测试持仓相关符号"""

    def test_position_functions_exist(self):
        """测试持仓函数存在"""
        import jk2bt as pkg

        for sym in [
            "calculate_position_value",
            "get_position_ratio",
            "get_portfolio_weights",
            "rebalance_portfolio",
            "rebalance_equally",
            "get_top_holdings",
        ]:
            assert hasattr(pkg, sym), f"{sym} should exist"


class TestOrderStyles:
    """测试订单类型"""

    def test_limit_order_style_exists(self):
        """测试 LimitOrderStyle 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "LimitOrderStyle")
        assert isinstance(pkg.LimitOrderStyle, type)

    def test_limit_order_style_can_instantiate(self):
        """测试 LimitOrderStyle 可以实例化"""
        import jk2bt as pkg

        order = pkg.LimitOrderStyle(100.0)
        assert hasattr(order, "limit_price")
        assert order.limit_price == 100.0

    def test_market_order_style_exists(self):
        """测试 MarketOrderStyle 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "MarketOrderStyle")
        assert isinstance(pkg.MarketOrderStyle, type)

    def test_market_order_style_can_instantiate(self):
        """测试 MarketOrderStyle 可以实例化"""
        import jk2bt as pkg

        order = pkg.MarketOrderStyle()
        assert order is not None


class TestRuntimeIOSymbols:
    """测试运行时IO符号"""

    def test_record_exists(self):
        """测试 record 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "record")
        assert callable(pkg.record)

    def test_send_message_exists(self):
        """测试 send_message 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "send_message")
        assert callable(pkg.send_message)

    def test_file_functions_exist(self):
        """测试文件函数存在"""
        import jk2bt as pkg

        for sym in [
            "read_file",
            "write_file",
            "get_record_data",
            "get_messages",
            "clear_runtime_data",
            "set_runtime_dir",
        ]:
            assert hasattr(pkg, sym), f"{sym} should exist"


class TestOptimizationSymbols:
    """测试性能优化符号"""

    def test_preload_data_for_strategy_exists(self):
        """测试 preload_data_for_strategy 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "preload_data_for_strategy")
        assert callable(pkg.preload_data_for_strategy)

    def test_cache_functions_exist(self):
        """测试缓存函数存在"""
        import jk2bt as pkg

        for sym in ["warm_up_cache", "cleanup_memory", "get_memory_usage"]:
            assert hasattr(pkg, sym), f"{sym} should exist"

    def test_cache_classes_exist(self):
        """测试缓存类存在"""
        import jk2bt as pkg

        for sym in ["CurrentDataCache", "BatchDataLoader", "DataPreloader"]:
            assert hasattr(pkg, sym), f"{sym} should exist"
            assert isinstance(getattr(pkg, sym), type)


class TestAssetRouterSymbols:
    """测试资产路由符号"""

    def test_asset_type_exists(self):
        """测试 AssetType 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "AssetType")
        from enum import Enum

        assert issubclass(pkg.AssetType, Enum)

    def test_asset_category_exists(self):
        """测试 AssetCategory 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "AssetCategory")
        from enum import Enum

        assert issubclass(pkg.AssetCategory, Enum)

    def test_trading_status_exists(self):
        """测试 TradingStatus 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "TradingStatus")
        from enum import Enum

        assert issubclass(pkg.TradingStatus, Enum)

    def test_asset_info_exists(self):
        """测试 AssetInfo 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "AssetInfo")
        from dataclasses import dataclass

        assert isinstance(pkg.AssetInfo, type)

    def test_asset_router_exists(self):
        """测试 AssetRouter 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "AssetRouter")
        assert isinstance(pkg.AssetRouter, type)

    def test_asset_functions_exist(self):
        """测试资产函数存在"""
        import jk2bt as pkg

        for sym in [
            "get_asset_router",
            "identify_asset",
            "is_etf",
            "is_stock",
            "is_fund_of",
            "is_future",
            "is_index",
            "get_trading_status_desc",
        ]:
            assert hasattr(pkg, sym), f"{sym} should exist"


class TestSubportfolioSymbols:
    """测试子账户符号"""

    def test_subportfolio_type_exists(self):
        """测试 SubportfolioType 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "SubportfolioType")
        from enum import Enum

        assert issubclass(pkg.SubportfolioType, Enum)

    def test_subportfolio_classes_exist(self):
        """测试子账户类存在"""
        import jk2bt as pkg

        for sym in [
            "SubportfolioConfig",
            "SubportfolioPosition",
            "SubportfolioCashAccount",
            "SubportfolioProxy",
            "SubportfolioManager",
        ]:
            assert hasattr(pkg, sym), f"{sym} should exist"
            assert isinstance(getattr(pkg, sym), type)

    def test_subportfolio_functions_exist(self):
        """测试子账户函数存在"""
        import jk2bt as pkg

        for sym in ["set_subportfolios", "transfer_cash", "get_subportfolio_summary"]:
            assert hasattr(pkg, sym), f"{sym} should exist"


class TestSymbolConversion:
    """测试符号转换函数"""

    def test_format_stock_symbol_for_akshare_exists(self):
        """测试 format_stock_symbol_for_akshare 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "format_stock_symbol_for_akshare")
        assert callable(pkg.format_stock_symbol_for_akshare)

    def test_jq_code_to_ak_exists(self):
        """测试 jq_code_to_ak 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "jq_code_to_ak")
        assert callable(pkg.jq_code_to_ak)

    def test_jq_code_to_ak_works(self):
        """测试 jq_code_to_ak 基本工作"""
        import jk2bt as pkg

        result = pkg.jq_code_to_ak("600519.XSHG")
        assert result == "sh600519"

    def test_ak_code_to_jq_exists(self):
        """测试 ak_code_to_jq 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "ak_code_to_jq")
        assert callable(pkg.ak_code_to_jq)

    def test_ak_code_to_jq_works(self):
        """测试 ak_code_to_jq 基本工作"""
        import jk2bt as pkg

        result = pkg.ak_code_to_jq("sh600519")
        assert result == "600519.XSHG"

    def test_get_akshare_stock_data_exists(self):
        """测试 get_akshare_stock_data 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_akshare_stock_data")
        assert callable(pkg.get_akshare_stock_data)

    def test_get_akshare_etf_data_exists(self):
        """测试 get_akshare_etf_data 存在"""
        import jk2bt as pkg

        assert hasattr(pkg, "get_akshare_etf_data")
        assert callable(pkg.get_akshare_etf_data)


class TestImportFromSubmodules:
    """测试从子模块导入"""

    def test_import_from_market_data(self):
        """测试从 market_data 导入"""
        from jk2bt.market_data import (
            get_stock_daily,
            get_etf_daily,
            get_index_daily,
        )

        assert callable(get_stock_daily)
        assert callable(get_etf_daily)
        assert callable(get_index_daily)

    def test_import_from_finance_data(self):
        """测试从 finance_data 导入"""
        from jk2bt.finance_data import (
            get_income,
            get_cashflow,
        )

        assert callable(get_income)
        assert callable(get_cashflow)

    def test_import_from_factors(self):
        """测试从 factors 导入"""
        from jk2bt.factors import get_factor_values_jq

        assert callable(get_factor_values_jq)

    def test_import_from_indicators(self):
        """测试从 indicators 导入"""
        from jk2bt.indicators import (
            compute_rsrs,
            compute_crowding_ratio,
        )

        assert callable(compute_rsrs)
        assert callable(compute_crowding_ratio)

    def test_import_from_utils(self):
        """测试从 utils 导入"""
        from jk2bt.utils import (
            format_stock_symbol,
            find_date_column,
        )

        assert callable(format_stock_symbol)
        assert callable(find_date_column)

    def test_import_from_db(self):
        """测试从 db 导入"""
        from jk2bt.db import DuckDBManager

        assert isinstance(DuckDBManager, type)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
