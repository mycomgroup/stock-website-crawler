"""
Tests for jk2bt/validation/config.py - ValidationConfig
"""

import pytest
import tempfile
import os
from datetime import datetime, timedelta
from jk2bt.validation.config import ValidationConfig


class TestValidationConfig:
    """Test ValidationConfig dataclass"""

    def test_default_values(self):
        config = ValidationConfig()
        assert len(config.stocks) > 0
        assert "600519.XSHG" in config.stocks
        assert config.data_types == ["valuation", "trade_status"]
        assert config.batch_size == 50
        assert config.concurrency == 3

    def test_custom_values(self):
        config = ValidationConfig(
            stocks=["000001.XSHE"],
            start_date="2024-01-01",
            end_date="2024-12-31",
            batch_size=100,
        )
        assert config.stocks == ["000001.XSHE"]
        assert config.batch_size == 100

    def test_tolerance_config(self):
        config = ValidationConfig()
        assert config.tolerance["pe_ratio"] == 0.01
        assert config.tolerance["is_st"] == 0.0

    def test_get_tolerance(self):
        config = ValidationConfig()
        assert config.get_tolerance("pe_ratio") == 0.01
        assert config.get_tolerance("unknown") == 0.01

    def test_get_dates_fallback(self):
        config = ValidationConfig(
            start_date="2024-01-01",
            end_date="2024-01-10",
        )
        dates = config.get_dates()
        assert len(dates) > 0


class TestValidationConfigFileOperations:
    """Test ValidationConfig file operations"""

    def test_to_file_json(self):
        config = ValidationConfig(stocks=["000001.XSHE"], batch_size=100)
        fd, filepath = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        try:
            config.to_file(filepath)
            assert os.path.exists(filepath)

            loaded = ValidationConfig.from_file(filepath)
            assert loaded.stocks == ["000001.XSHE"]
            assert loaded.batch_size == 100
        finally:
            os.unlink(filepath)

    def test_from_file_nonexistent(self):
        with pytest.raises(FileNotFoundError):
            ValidationConfig.from_file("/nonexistent/config.json")


class TestDefaultConfig:
    """Test default_config module-level instance"""

    def test_default_config_exists(self):
        from jk2bt.validation.config import default_config

        assert isinstance(default_config, ValidationConfig)
        assert len(default_config.stocks) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
