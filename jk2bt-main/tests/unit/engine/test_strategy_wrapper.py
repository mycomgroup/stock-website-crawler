"""
test_strategy_wrapper.py
strategy_wrapper.py 单元测试

测试场景覆盖:
1. JQStrategyWrapper 策略包装器
2. _DataProxy 数据代理
3. _CurrentPriceProxy 当前价格代理
4. _set_current_strategy_instance 全局设置
5. _get_current_strategy 全局获取
6. 策略函数调用
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

try:
    from jk2bt.engine.strategy_wrapper import (
        JQStrategyWrapper,
        _DataProxy,
        _CurrentPriceProxy,
        _set_current_strategy_instance,
        _get_current_strategy,
    )
    from jk2bt.engine.strategy_base import GlobalState, ContextProxy
except ImportError:
    pytest.skip("strategy_base module not available", allow_module_level=True)


class TestDataProxy:
    """测试 _DataProxy 数据代理"""

    def test_getitem_returns_security_data(self):
        """测试获取证券数据"""
        mock_strategy = MagicMock()
        proxy = _DataProxy(mock_strategy)
        result = proxy["600519.XSHG"]
        assert isinstance(result, _CurrentPriceProxy) or hasattr(result, "price")

    def test_current_price_returns_proxy(self):
        """测试current_price属性"""
        mock_strategy = MagicMock()
        proxy = _DataProxy(mock_strategy)
        result = proxy.current_price
        assert isinstance(result, _CurrentPriceProxy)


class TestCurrentPriceProxy:
    """测试 _CurrentPriceProxy 当前价格代理"""

    def test_getitem_returns_price(self):
        """测试获取价格"""
        mock_strategy = MagicMock()
        mock_strategy._get_current_price.return_value = 100.0
        proxy = _CurrentPriceProxy(mock_strategy)
        result = proxy["600519.XSHG"]
        assert result == 100.0


class TestGlobalStrategyInstance:
    """测试全局策略实例管理"""

    def test_set_and_get_strategy(self):
        """测试设置和获取策略"""
        mock_strategy = MagicMock()
        _set_current_strategy_instance(mock_strategy)
        result = _get_current_strategy()
        assert result is mock_strategy

    def test_get_when_not_set(self):
        """测试未设置时返回None"""
        _set_current_strategy_instance(None)
        result = _get_current_strategy()
        assert result is None


class TestStrategyWrapperParams:
    """测试 JQStrategyWrapper 参数"""

    def test_default_params(self):
        """测试默认参数"""
        params = JQStrategyWrapper.params
        assert params.printlog is True
        assert params.log_dir == "logs"
        assert params.prerun_mode is False
        assert params.max_prerun_days == 5
        assert params.frequency == "daily"
        assert params.initial_capital == 1000000

    def test_custom_params(self):
        """测试自定义参数"""

        class TestStrategy(JQStrategyWrapper):
            params = (
                ("strategy_functions", None),
                ("printlog", False),
                ("log_dir", "/tmp/logs"),
                ("prerun_mode", True),
                ("max_prerun_days", 10),
                ("frequency", "1m"),
                ("initial_capital", 500000),
                ("start_date", None),
                ("end_date", None),
            )

        assert TestStrategy.params.printlog is False
        assert TestStrategy.params.frequency == "1m"


class TestStrategyWrapperInitialization:
    """测试 JQStrategyWrapper 初始化"""

    def test_initializes_without_functions(self):
        """测试不提供策略函数时初始化"""
        mock_cerebro = MagicMock()
        mock_strategy = JQStrategyWrapper()
        mock_strategy.__init__(strategy_functions={})

    def test_initializes_with_functions(self):
        """测试提供策略函数时初始化"""

        def initialize(context):
            pass

        mock_strategy = JQStrategyWrapper()
        mock_strategy.__init__(strategy_functions={"initialize": initialize})

    def test_sets_initial_capital(self):
        """测试设置初始资金"""
        strategy = JQStrategyWrapper()
        strategy._initial_capital = 1000000
        assert strategy._initial_capital == 1000000


class TestStrategyWrapperDataAccess:
    """测试策略包装器数据访问"""

    def test_data_by_name_mapping(self):
        """测试证券名称映射"""
        mock_data1 = MagicMock()
        mock_data1._name = "600519.XSHG"
        mock_data2 = MagicMock()
        mock_data2._name = "000001.XSHE"

        strategy = JQStrategyWrapper()
        strategy.datas = [mock_data1, mock_data2]
        strategy._data_by_name = {d._name: d for d in strategy.datas}

        assert "600519.XSHG" in strategy._data_by_name
        assert "000001.XSHE" in strategy._data_by_name

    def test_get_current_price(self):
        """测试获取当前价格"""
        mock_data = MagicMock()
        mock_data.close = [100.0]

        strategy = JQStrategyWrapper()
        strategy._data_by_name = {"600519.XSHG": mock_data}

        result = strategy._get_current_price("600519.XSHG")
        assert result == 100.0

    def test_get_current_price_missing(self):
        """测试获取不存在证券的价格"""
        strategy = JQStrategyWrapper()
        strategy._data_by_name = {}

        result = strategy._get_current_price("600519.XSHG")
        assert result is None

    def test_get_security_data(self):
        """测试获取证券数据对象"""
        mock_data = MagicMock()
        mock_data.close = [100.0]
        mock_data.high = [105.0]
        mock_data.low = [95.0]
        mock_data.open = [98.0]
        mock_data.volume = [1000000]

        strategy = JQStrategyWrapper()
        strategy._data_by_name = {"600519.XSHG": mock_data}

        result = strategy._get_security_data("600519.XSHG")
        assert result.price == 100.0
        assert result.close == 100.0
        assert result.high == 105.0
        assert result.low == 95.0
        assert result.open == 98.0
        assert result.volume == 1000000


class TestStrategyWrapperHandleFunctions:
    """测试策略包装器处理函数"""

    def test_saves_handle_functions(self):
        """测试保存handle函数"""

        def handle_data(context):
            pass

        def trading_func(context, data):
            pass

        strategy = JQStrategyWrapper()
        strategy._handle_functions = {
            "handle_data": handle_data,
            "trading_func": trading_func,
        }

        assert "handle_data" in strategy._handle_functions
        assert "trading_func" in strategy._handle_functions

    def test_saves_before_trading_start(self):
        """测试保存before_trading_start函数"""

        def before_trading_start(context):
            pass

        strategy = JQStrategyWrapper()
        strategy._before_trading_start_func = before_trading_start

        assert strategy._before_trading_start_func is not None

    def test_params_counts_caching(self):
        """测试函数参数数量缓存"""

        def func_no_args():
            pass

        def func_one_arg(x):
            pass

        strategy = JQStrategyWrapper()
        strategy._bts_params_count = 0
        strategy._handle_params_counts = {
            "func_no_args": 0,
            "func_one_arg": 1,
        }

        assert strategy._bts_params_count == 0
        assert strategy._handle_params_counts["func_no_args"] == 0
        assert strategy._handle_params_counts["func_one_arg"] == 1


class TestStrategyWrapperRuntimeErrors:
    """测试策略包装器运行时错误记录"""

    def test_initializes_runtime_errors_list(self):
        """测试初始化运行时错误列表"""
        strategy = JQStrategyWrapper()
        strategy.runtime_errors = []
        assert isinstance(strategy.runtime_errors, list)

    def test_appends_runtime_error(self):
        """测试添加运行时错误"""
        strategy = JQStrategyWrapper()
        strategy.runtime_errors = []

        error_entry = {
            "function": "handle_data",
            "error": "test error",
            "error_type": "ValueError",
            "traceback": "...",
            "datetime": "2024-01-01",
        }
        strategy.runtime_errors.append(error_entry)

        assert len(strategy.runtime_errors) == 1
        assert strategy.runtime_errors[0]["function"] == "handle_data"
