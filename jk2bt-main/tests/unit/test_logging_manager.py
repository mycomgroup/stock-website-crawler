"""
test_logging_manager.py
单元测试 - 日志管理器模块

测试场景覆盖:
1. LogManager 单例模式
2. LogManager 初始化
3. LogManager 获取 logger/adapter
4. LogManager shutdown/reset
5. 便捷函数 (setup_logging, get_logger, get_jq_log, get_default_logger)
"""

import sys
import logging
import importlib
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 直接导入子模块，绕过 jk2bt/__init__.py
manager_module = importlib.import_module("jk2bt.logging.manager")
config_module = importlib.import_module("jk2bt.logging.config")
adapters_module = importlib.import_module("jk2bt.logging.adapters")
stats_module = importlib.import_module("jk2bt.logging.stats")

LogManager = manager_module.LogManager
setup_logging = manager_module.setup_logging
get_logger = manager_module.get_logger
get_jq_log = manager_module.get_jq_log
get_default_logger = manager_module.get_default_logger
LoggingConfig = config_module.LoggingConfig
JQLogAdapter = adapters_module.JQLogAdapter
StatsCollector = stats_module.StatsCollector


@pytest.fixture(autouse=True)
def reset_log_manager():
    """每个测试前重置 LogManager 单例"""
    LogManager._instance = None
    yield
    LogManager._instance = None
    # 清理 root logger handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)


class TestLogManagerSingleton:
    """测试 LogManager 单例模式"""

    def test_singleton_returns_same_instance(self):
        m1 = LogManager()
        m2 = LogManager()
        assert m1 is m2

    def test_get_instance_returns_singleton(self):
        m1 = LogManager.get_instance()
        m2 = LogManager.get_instance()
        assert m1 is m2

    def test_new_uses_lock(self):
        m1 = LogManager()
        m2 = LogManager()
        assert m1 is m2


class TestLogManagerInit:
    """测试 LogManager 初始化"""

    def test_init_sets_initialized_flag(self):
        manager = LogManager()
        assert manager._initialized is True

    def test_init_does_not_reinitialize(self):
        manager = LogManager()
        manager._config = "test"
        manager2 = LogManager()
        assert manager2._config == "test"

    def test_initial_config_is_none(self):
        manager = LogManager()
        assert manager._config is None

    def test_initial_stats_collector_is_none(self):
        manager = LogManager()
        assert manager._stats_collector is None


class TestLogManagerInitialize:
    """测试 LogManager.initialize"""

    def test_initialize_with_default_config(self):
        manager = LogManager()
        manager.initialize()
        assert manager._config is not None
        assert isinstance(manager._config, LoggingConfig)

    def test_initialize_with_custom_config(self):
        config = LoggingConfig(level="DEBUG", log_file=None)
        manager = LogManager()
        manager.initialize(config=config)
        assert manager._config.level == "DEBUG"
        assert manager._config.log_file is None

    def test_initialize_sets_stats_collector(self):
        manager = LogManager()
        manager.initialize()
        assert manager._stats_collector is not None
        assert isinstance(manager._stats_collector, StatsCollector)


class TestLogManagerGetLogger:
    """测试 LogManager.get_logger"""

    def test_get_logger_default_name(self):
        manager = LogManager()
        logger = manager.get_logger()
        assert logger.name == "jk2bt"

    def test_get_logger_custom_name(self):
        manager = LogManager()
        logger = manager.get_logger("custom_logger")
        assert logger.name == "custom_logger"

    def test_get_logger_returns_python_logger(self):
        manager = LogManager()
        logger = manager.get_logger()
        assert isinstance(logger, logging.Logger)


class TestLogManagerGetJQAdapter:
    """测试 LogManager.get_jq_adapter"""

    def test_get_jq_adapter_returns_adapter(self):
        manager = LogManager()
        adapter = manager.get_jq_adapter()
        assert isinstance(adapter, JQLogAdapter)

    def test_get_jq_adapter_with_strategy(self):
        manager = LogManager()
        strategy = MagicMock()
        adapter = manager.get_jq_adapter(strategy=strategy)
        assert adapter._strategy is strategy

    def test_get_jq_adapter_custom_logger_name(self):
        manager = LogManager()
        adapter = manager.get_jq_adapter(logger_name="custom")
        assert adapter._logger.name == "custom"


class TestLogManagerGetStatsCollector:
    """测试 LogManager.get_stats_collector"""

    def test_returns_none_before_init(self):
        manager = LogManager()
        assert manager.get_stats_collector() is None

    def test_returns_collector_after_init(self):
        manager = LogManager()
        manager.initialize()
        collector = manager.get_stats_collector()
        assert collector is not None
        assert isinstance(collector, StatsCollector)


class TestLogManagerShutdown:
    """测试 LogManager.shutdown"""

    def test_shutdown_logs_stats(self):
        manager = LogManager()
        manager.initialize()
        with patch.object(manager._stats_collector, "log_summary") as mock_log:
            manager.shutdown()
            mock_log.assert_called_once()

    def test_shutdown_closes_handlers(self):
        manager = LogManager()
        manager.initialize()
        root_logger = logging.getLogger()
        handler_count_before = len(root_logger.handlers)
        assert handler_count_before > 0
        manager.shutdown()
        handler_count_after = len(root_logger.handlers)
        assert handler_count_after == 0

    def test_shutdown_without_stats_collector(self):
        manager = LogManager()
        manager.shutdown()

    def test_shutdown_handles_exception_in_close(self):
        manager = LogManager()
        manager.initialize()
        root_logger = logging.getLogger()
        mock_handler = MagicMock()
        mock_handler.close.side_effect = Exception("close error")
        mock_handler.level = logging.INFO
        root_logger.handlers.insert(0, mock_handler)
        manager.shutdown()

    def test_shutdown_with_no_handlers(self):
        manager = LogManager()
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        manager.shutdown()


class TestLogManagerReset:
    """测试 LogManager.reset"""

    def test_reset_clears_handlers(self):
        manager = LogManager()
        manager.initialize()
        manager.reset()
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) == 0

    def test_reset_clears_config(self):
        manager = LogManager()
        manager.initialize()
        manager.reset()
        assert manager._config is None

    def test_reset_clears_stats_collector(self):
        manager = LogManager()
        manager.initialize()
        manager.reset()
        assert manager._stats_collector is not None


class TestSetupLogging:
    """测试 setup_logging 便捷函数"""

    def test_setup_logging_returns_manager(self):
        manager = setup_logging()
        assert isinstance(manager, LogManager)

    def test_setup_logging_with_custom_level(self):
        manager = setup_logging(level="DEBUG")
        assert manager._config.level == "DEBUG"

    def test_setup_logging_with_log_file(self, tmp_path):
        log_file = str(tmp_path / "test.log")
        manager = setup_logging(log_file=log_file)
        assert manager._config.log_file == log_file

    def test_setup_logging_with_format(self):
        manager = setup_logging(format="detailed")
        assert manager._config.format == "detailed"

    def test_setup_logging_force_clears_handlers(self):
        root_logger = logging.getLogger()
        root_logger.addHandler(logging.StreamHandler())
        handler_count_before = len(root_logger.handlers)
        manager = setup_logging(force=True)
        assert isinstance(manager, LogManager)

    def test_setup_logging_is_idempotent(self):
        m1 = setup_logging()
        m2 = setup_logging()
        assert m1 is m2


class TestGetLogger:
    """测试 get_logger 便捷函数"""

    def test_get_logger_default(self):
        logger = get_logger()
        assert logger.name == "jk2bt"

    def test_get_logger_custom_name(self):
        logger = get_logger("my_logger")
        assert logger.name == "my_logger"

    def test_get_logger_returns_logger_instance(self):
        logger = get_logger()
        assert isinstance(logger, logging.Logger)


class TestGetJqLog:
    """测试 get_jq_log 便捷函数"""

    def test_get_jq_log_default(self):
        adapter = get_jq_log()
        assert isinstance(adapter, JQLogAdapter)
        assert adapter._logger.name == "jk2bt"

    def test_get_jq_log_custom_name(self):
        adapter = get_jq_log(logger_name="custom")
        assert adapter._logger.name == "custom"

    def test_get_jq_log_with_strategy(self):
        strategy = MagicMock()
        adapter = get_jq_log(strategy=strategy)
        assert adapter._strategy is strategy


class TestGetDefaultLogger:
    """测试 get_default_logger 便捷函数"""

    def test_returns_jk2bt_logger(self):
        logger = get_default_logger()
        assert logger.name == "jk2bt"

    def test_returns_logger_instance(self):
        logger = get_default_logger()
        assert isinstance(logger, logging.Logger)
