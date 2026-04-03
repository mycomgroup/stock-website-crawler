"""
tests/regression/test_api_compatibility.py
API 兼容性回归测试（迁移自 tests/test_api_compatibility.py）

验证：
- 重构后 src.api 导出符号集合 ⊇ 重构前导出符号集合
- 兼容层文件触发 DeprecationWarning
- strategy_base 核心函数可调用
- 证券代码格式兼容性
"""

import pytest
import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"),
)

pytestmark = pytest.mark.regression


# ---------------------------------------------------------------------------
# src.api 导出符号完整性
# ---------------------------------------------------------------------------

class TestApiExportCompleteness:
    """src.api 导出符号完整性测试"""

    def test_market_functions_exported(self):
        """行情函数可从 src.api 导入"""
        from jk2bt.api import get_price, history, attribute_history, get_bars
        for fn in [get_price, history, attribute_history, get_bars]:
            assert callable(fn)

    def test_order_functions_exported(self):
        """订单函数可从 src.api 导入"""
        from jk2bt.api import order_shares, order_target_percent
        assert callable(order_shares)
        assert callable(order_target_percent)

    def test_filter_functions_exported(self):
        """过滤函数可从 src.api 导入"""
        from jk2bt.api import filter_st, filter_paused, filter_limit_up, filter_limit_down
        from jk2bt.api import filter_new_stocks
        for fn in [filter_st, filter_paused, filter_limit_up, filter_limit_down, filter_new_stocks]:
            assert callable(fn)

    def test_date_functions_exported(self):
        """日期函数可从 src.api 导入"""
        from jk2bt.api import (get_shifted_date, get_previous_trade_date, get_next_trade_date,
                              transform_date, is_trade_date, get_trade_dates_between,
                              count_trade_dates_between, clear_trade_days_cache)
        for fn in [get_shifted_date, get_previous_trade_date, get_next_trade_date,
                   transform_date, is_trade_date, get_trade_dates_between,
                   count_trade_dates_between, clear_trade_days_cache]:
            assert callable(fn)

    def test_indicator_functions_exported(self):
        """技术指标函数可从 src.api 导入"""
        from jk2bt.api import MA, EMA, MACD, KDJ, RSI, BOLL, ATR
        for fn in [MA, EMA, MACD, KDJ, RSI, BOLL, ATR]:
            assert callable(fn)

    def test_finance_functions_exported(self):
        """财务函数可从 src.api 导入"""
        from jk2bt.api import get_locked_shares, get_fund_info, get_fundamentals_continuously
        for fn in [get_locked_shares, get_fund_info, get_fundamentals_continuously]:
            assert callable(fn)

    def test_stats_functions_exported(self):
        """统计函数可从 src.api 导入"""
        from jk2bt.api import get_ols, get_zscore, get_rank, get_beta
        for fn in [get_ols, get_zscore, get_rank, get_beta]:
            assert callable(fn)

    def test_cache_classes_exported(self):
        """缓存类可从 src.api 导入"""
        from jk2bt.api import CurrentDataCache, BatchDataLoader, DataPreloader
        for cls in [CurrentDataCache, BatchDataLoader, DataPreloader]:
            assert cls is not None

    def test_internal_symbols_not_in_all(self):
        """_internal 符号不在 src.api.__all__ 中"""
        import jk2bt.api as api
        if hasattr(api, "__all__"):
            for name in api.__all__:
                assert not name.startswith("_"), f"私有符号 {name!r} 不应出现在 __all__ 中"

    def test_api_gap_analyzer_not_exported(self):
        """APIGapAnalyzer 不在 src.api 导出中"""
        import jk2bt.api as api
        if hasattr(api, "__all__"):
            assert "APIGapAnalyzer" not in api.__all__


# ---------------------------------------------------------------------------
# 兼容层 DeprecationWarning 测试
# 注：兼容层文件已删除，此测试类已弃用
# ---------------------------------------------------------------------------

class TestCompatLayerDeprecationWarning:
    """兼容层触发 DeprecationWarning 测试（已弃用 - 兼容层文件已删除）"""

    def test_market_api_compat_warns(self):
        """market_api 兼容层已删除，跳过测试"""
        pytest.skip("market_api.py 兼容层已删除")

    def test_enhancements_compat_warns(self):
        """enhancements 不再是兼容层"""
        # enhancements.py 仍然存在但不再是兼容层
        pass

    def test_filter_api_compat_warns(self):
        """filter_api 兼容层已删除，跳过测试"""
        pytest.skip("filter_api.py 兼容层已删除")


# ---------------------------------------------------------------------------
# strategy_base 核心函数可调用性
# ---------------------------------------------------------------------------

class TestStrategyBaseFunctions:
    """strategy_base 核心函数可调用性测试"""

    def test_required_functions_callable(self):
        """strategy_base 必需函数均可调用"""
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
        for fn in [get_price_jq, get_fundamentals_jq, get_history_fundamentals_jq,
                   get_all_securities_jq, get_security_info_jq, get_all_trade_days_jq,
                   get_extras_jq, get_factor_values_jq]:
            assert callable(fn)

    def test_get_all_securities_returns_dataframe(self):
        """get_all_securities_jq 返回 DataFrame"""
        import pandas as pd
        from jk2bt.core.strategy_base import get_all_securities_jq
        result = get_all_securities_jq()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    def test_get_all_trade_days_returns_list(self):
        """get_all_trade_days_jq 返回非空列表"""
        from jk2bt.core.strategy_base import get_all_trade_days_jq
        result = get_all_trade_days_jq()
        assert isinstance(result, list)
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
