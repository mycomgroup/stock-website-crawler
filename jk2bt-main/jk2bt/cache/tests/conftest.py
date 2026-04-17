import pytest
import tempfile
import pandas as pd
from pathlib import Path


@pytest.fixture
def tmp_dir():
    """临时目录，测试后自动清理"""
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def sample_stock_data():
    """示例股票日线数据"""
    return pd.DataFrame(
        {
            "symbol": ["600519", "600519", "000001"],
            "date": pd.to_datetime(["2024-04-01", "2024-04-02", "2024-04-01"]).date,
            "open": [1800.0, 1810.0, 15.5],
            "high": [1820.0, 1830.0, 15.8],
            "low": [1790.0, 1800.0, 15.3],
            "close": [1815.0, 1825.0, 15.6],
            "volume": [1000000.0, 1200000.0, 5000000.0],
            "amount": [1.8e9, 2.2e9, 7.8e7],
            "adjust": ["qfq", "qfq", "qfq"],
        }
    )


@pytest.fixture
def sample_etf_data():
    """示例 ETF 数据"""
    return pd.DataFrame(
        {
            "symbol": ["510300", "510500"],
            "date": pd.to_datetime(["2024-04-01", "2024-04-01"]).date,
            "open": [3.8, 6.2],
            "high": [3.85, 6.25],
            "low": [3.78, 6.18],
            "close": [3.82, 6.22],
            "volume": [10000000.0, 8000000.0],
            "amount": [3.82e7, 4.98e7],
        }
    )
