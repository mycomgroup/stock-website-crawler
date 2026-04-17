"""
Tests for jk2bt/logging/config.py - LoggingConfig
"""

import pytest
import logging
import os
from unittest.mock import patch, MagicMock
from jk2bt.logging.config import (
    LoggingConfig,
    apply_config,
    get_default_config,
)


class TestLoggingConfig:
    """Test LoggingConfig dataclass"""

    def test_default_values(self):
        config = LoggingConfig()
        assert config.level == "INFO"
        assert config.log_file == "logs/jk2bt.log"
        assert config.format == "standard"
        assert config.max_bytes == 10 * 1024 * 1024
        assert config.backup_count == 5

    def test_custom_values(self):
        config = LoggingConfig(
            level="DEBUG",
            log_file="/tmp/custom.log",
            format="simple",
        )
        assert config.level == "DEBUG"
        assert config.log_file == "/tmp/custom.log"
        assert config.format == "simple"

    def test_from_dict(self):
        data = {
            "level": "WARNING",
            "log_file": "/tmp/test.log",
            "max_bytes": 5000000,
            "unknown_field": "should_be_ignored",
        }
        config = LoggingConfig.from_dict(data)
        assert config.level == "WARNING"
        assert config.log_file == "/tmp/test.log"
        assert config.max_bytes == 5000000


class TestApplyConfig:
    """Test apply_config function"""

    def test_apply_config_creates_handlers(self):
        config = LoggingConfig(
            level="INFO",
            log_file="logs/test.log",
            suppress_third_party=False,
        )

        with patch("jk2bt.logging.config.get_formatter") as mock_formatter:
            with patch("jk2bt.logging.config.create_rotating_file_handler"):
                mock_formatter.return_value = MagicMock()
                logger = apply_config(config)

                assert logger.level == logging.INFO

    def test_apply_config_suppresses_third_party(self):
        config = LoggingConfig(
            level="INFO",
            suppress_third_party=True,
        )

        with patch("jk2bt.logging.config.get_formatter") as mock_formatter:
            with patch("jk2bt.logging.config.create_rotating_file_handler"):
                mock_formatter.return_value = MagicMock()
                apply_config(config)

                for logger_name in ("matplotlib", "PIL", "urllib3", "requests"):
                    assert logging.getLogger(logger_name).level == logging.WARNING


class TestGetDefaultConfig:
    """Test get_default_config function"""

    def test_default_values(self):
        with patch.dict(os.environ, {}, clear=True):
            config = get_default_config()
            assert config.level == "INFO"
            assert config.log_file == "logs/jk2bt.log"

    def test_env_override_level(self):
        with patch.dict(os.environ, {"JK2BT_LOG_LEVEL": "DEBUG"}):
            config = get_default_config()
            assert config.level == "DEBUG"

    def test_env_override_log_file(self):
        with patch.dict(os.environ, {"JK2BT_LOG_FILE": "/tmp/custom.log"}):
            config = get_default_config()
            assert config.log_file == "/tmp/custom.log"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
