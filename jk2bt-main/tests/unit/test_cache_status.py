"""
test_cache_status.py
缓存校验回归测试 - TEST-2

测试场景覆盖:
1. 目录不存在时的行为
2. 空缓存目录时的行为
3. 预热后目录时的行为
4. 自定义cache_dir参数测试
5. 缓存摘要和报告格式测试
"""

import os
import sys
import tempfile
import shutil
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pandas as pd

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from jk2bt.data.storage.cache_status import (
    CacheManager,
    get_cache_manager,
    check_cache_status,
)
from jk2bt.data.storage.cache_config import init_default_cache
from jk2bt.cache import get_cache_manager as parquet_get_cache_manager


class TestCacheManagerInit:
    """测试 CacheManager 初始化"""

    def test_init_default_path(self):
        """测试默认路径初始化"""
        manager = CacheManager()
        assert manager.db is not None
        assert manager.db_path is not None

    def test_init_custom_path(self, tmp_path):
        """测试自定义数据库路径"""
        custom_db = tmp_path / "custom_cache_parquet"
        manager = CacheManager(db_path=str(custom_db))
        assert manager.db_path == str(custom_db)

    def test_get_cache_manager_singleton(self):
        """测试工厂函数返回有效实例"""
        manager = get_cache_manager()
        assert isinstance(manager, CacheManager)


class TestCheckStockDailyCache:
    """测试股票日线缓存检查"""

    @pytest.fixture
    def mock_db(self, tmp_path):
        """创建模拟数据库和测试数据"""
        db_path = tmp_path / "test_cache_parquet"

        # 创建模拟数据
        dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        return {"db_path": str(db_path), "df": df, "symbol": "sh600519"}

    def test_check_empty_cache(self, tmp_path):
        """测试空缓存目录时的检查行为"""
        manager = CacheManager(db_path=str(tmp_path / "empty_parquet"))

        result = manager.check_stock_daily_cache(
            "sh600519", "2023-01-01", "2023-12-31", "qfq"
        )

        assert result["has_data"] is False
        assert result["is_complete"] is False
        assert result["count"] == 0
        assert result["min_date"] is None
        assert result["max_date"] is None

    def test_check_partial_cache(self, tmp_path):
        """测试部分缓存时的检查行为"""
        db_path = tmp_path / "partial_cache_parquet"

        # 创建部分数据（只有一半的时间范围）
        dates = pd.date_range("2023-06-01", "2023-12-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        # 写入数据库
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sh600519", df, "qfq")

        manager = CacheManager(db_path=str(db_path))
        result = manager.check_stock_daily_cache(
            "sh600519", "2023-01-01", "2023-12-31", "qfq"
        )

        assert result["has_data"] is True
        assert result["is_complete"] is False  # 缺少 2023-01-01 到 2023-05-31
        assert result["count"] > 0
        assert result["min_date"] is not None
        assert result["max_date"] is not None

    def test_check_complete_cache(self, tmp_path):
        """测试完整缓存时的检查行为"""
        db_path = tmp_path / "complete_cache_parquet"

        # 创建完整数据
        dates = pd.date_range("2022-12-01", "2024-01-31", freq="D")  # 覆盖更多范围
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        # 写入数据库
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sh600519", df, "qfq")

        manager = CacheManager(db_path=str(db_path))
        result = manager.check_stock_daily_cache(
            "sh600519", "2023-01-01", "2023-12-31", "qfq"
        )

        assert result["has_data"] is True
        assert result["is_complete"] is True  # 完整覆盖
        assert result["count"] > 0

    def test_check_with_different_adjust_types(self, tmp_path):
        """测试不同复权类型的缓存检查"""
        db_path = tmp_path / "adjust_cache_parquet"

        dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
        df_qfq = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        # 写入数据库
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sh600519", df_qfq, "qfq")

        manager = CacheManager(db_path=str(db_path))

        # qfq 有数据
        result_qfq = manager.check_stock_daily_cache(
            "sh600519", "2023-01-01", "2023-12-31", "qfq"
        )
        assert result_qfq["has_data"] is True

        # hfq 没有数据
        result_hfq = manager.check_stock_daily_cache(
            "sh600519", "2023-01-01", "2023-12-31", "hfq"
        )
        assert result_hfq["has_data"] is False


class TestCheckETFAndIndexCache:
    """测试ETF和指数缓存检查"""

    def test_check_etf_empty_cache(self, tmp_path):
        """测试ETF空缓存"""
        manager = CacheManager(db_path=str(tmp_path / "empty_parquet"))
        result = manager.check_etf_daily_cache("510300", "2023-01-01", "2023-12-31")
        assert result["has_data"] is False

    def test_check_etf_with_data(self, tmp_path):
        """测试ETF有数据"""
        db_path = tmp_path / "etf_cache_parquet"
        dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [3.0] * len(dates),
                "high": [3.1] * len(dates),
                "low": [2.9] * len(dates),
                "close": [3.05] * len(dates),
                "volume": [1000000] * len(dates),
                "amount": [3000000.0] * len(dates),
            }
        )

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_etf_daily("510300", df)

        manager = CacheManager(db_path=str(db_path))
        result = manager.check_etf_daily_cache("510300", "2023-01-01", "2023-12-31")
        assert result["has_data"] is True
        assert result["is_complete"] is True

    def test_check_index_empty_cache(self, tmp_path):
        """测试指数空缓存"""
        manager = CacheManager(db_path=str(tmp_path / "empty_parquet"))
        result = manager.check_index_daily_cache("000300", "2023-01-01", "2023-12-31")
        assert result["has_data"] is False

    def test_check_index_with_data(self, tmp_path):
        """测试指数有数据"""
        db_path = tmp_path / "index_cache_parquet"
        dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [3800.0] * len(dates),
                "high": [3850.0] * len(dates),
                "low": [3750.0] * len(dates),
                "close": [3820.0] * len(dates),
                "volume": [0] * len(dates),
                "amount": [0.0] * len(dates),
            }
        )

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_index_daily("000300", df)

        manager = CacheManager(db_path=str(db_path))
        result = manager.check_index_daily_cache("000300", "2023-01-01", "2023-12-31")
        assert result["has_data"] is True


class TestCheckMetaCache:
    """测试元数据缓存检查（基于全局 parquet_cache 的正向测试）"""

    def test_check_meta_with_global_trade_calendar(self, tmp_path):
        """测试全局 parquet_cache 有交易日历数据"""
        cache = parquet_get_cache_manager()
        trade_days_df = pd.DataFrame(
            {
                "date": pd.date_range("2023-01-01", "2023-12-31", freq="B").date,
                "is_trading_day": [True] * 260,
            }
        )
        cache.put("trade_calendar", trade_days_df)

        manager = CacheManager(db_path=str(tmp_path / "test_parquet"))
        result = manager.check_meta_cache(str(tmp_path / "any_dir"))

        assert result["trade_days"] is True
        assert result["trade_days_date"] is not None

    def test_check_meta_with_global_securities(self, tmp_path):
        """测试全局 parquet_cache 有证券数据"""
        cache = parquet_get_cache_manager()
        securities_df = pd.DataFrame(
            {
                "symbol": ["sh600519", "sz000858"],
                "name": ["贵州茅台", "五粮液"],
                "type": ["stock", "stock"],
                "list_date": [
                    pd.Timestamp("2001-01-01").date(),
                    pd.Timestamp("1998-04-27").date(),
                ],
                "delist_date": [None, None],
                "exchange": ["XSHG", "XSHE"],
            }
        )
        cache.put("securities", securities_df)

        manager = CacheManager(db_path=str(tmp_path / "test_parquet"))
        result = manager.check_meta_cache(str(tmp_path / "any_dir"))

        assert result["securities"] is True
        assert result["securities_date"] is not None

    def test_check_meta_with_index_weights(self, tmp_path):
        """测试有指数权重缓存"""
        weights_df = pd.DataFrame(
            {
                "index_code": ["000300", "000300"],
                "stock_code": ["600519", "000858"],
                "weight": [0.05, 0.03],
                "update_date": [
                    pd.Timestamp("2023-01-01").date(),
                    pd.Timestamp("2023-01-01").date(),
                ],
                "update_time": pd.Timestamp.now(),
            }
        )

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(tmp_path / "test_parquet"), read_only=False)
        db._init_database()
        db.insert_index_weights("000300", weights_df)

        manager = CacheManager(db_path=str(tmp_path / "test_parquet"))
        result = manager.check_meta_cache(str(tmp_path / "any_dir"))

        assert "000300" in result["index_weights"]
        assert result["index_weights"]["000300"] is True

    def test_check_meta_with_all_meta_data(self, tmp_path):
        """测试全局缓存有完整元数据"""
        cache = parquet_get_cache_manager()
        trade_days_df = pd.DataFrame(
            {
                "date": pd.date_range("2023-01-01", "2023-12-31", freq="B").date,
                "is_trading_day": [True] * 260,
            }
        )
        securities_df = pd.DataFrame(
            {
                "symbol": ["sh600519"],
                "name": ["贵州茅台"],
                "type": ["stock"],
                "list_date": [pd.Timestamp("2001-01-01").date()],
                "delist_date": [None],
                "exchange": ["XSHG"],
            }
        )
        cache.put("trade_calendar", trade_days_df)
        cache.put("securities", securities_df)

        weights_df = pd.DataFrame(
            {
                "index_code": ["000300"],
                "stock_code": ["600519"],
                "weight": [0.05],
                "update_date": [pd.Timestamp("2023-01-01").date()],
                "update_time": pd.Timestamp.now(),
            }
        )
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(tmp_path / "test_parquet"), read_only=False)
        db._init_database()
        db.insert_index_weights("000300", weights_df)

        manager = CacheManager(db_path=str(tmp_path / "test_parquet"))
        result = manager.check_meta_cache(str(tmp_path / "any_dir"))

        assert result["trade_days"] is True
        assert result["securities"] is True
        assert "000300" in result["index_weights"]


class TestValidateCacheForOffline:
    """测试离线缓存验证"""

    def test_validate_empty_directory(self, tmp_path):
        """测试目录不存在/空目录时的离线验证"""
        nonexistent_dir = tmp_path / "nonexistent"
        db_path = tmp_path / "empty_parquet"

        manager = CacheManager(db_path=str(db_path))
        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=["600519.XSHG", "000858.XSHE"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(nonexistent_dir),
        )

        assert is_valid is False
        assert len(report["missing_stocks"]) == 2
        assert "trade_days" in report["missing_meta"]
        assert "securities" in report["missing_meta"]

    def test_validate_partial_cache(self, tmp_path):
        """测试部分缓存时的离线验证"""
        db_path = tmp_path / "partial_parquet"
        cache_dir = tmp_path / "partial_cache"

        trade_days_df = pd.DataFrame(
            {"date": pd.date_range("2023-01-01", "2024-12-31", freq="B").date}
        )
        securities_df = pd.DataFrame(
            {"code": ["sh600519", "sz000858"], "name": ["贵州茅台", "五粮液"]}
        )
        cache = parquet_get_cache_manager()
        cache.put("trade_calendar", trade_days_df)
        cache.put("securities", securities_df)

        dates = pd.date_range("2023-06-01", "2023-12-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sh600519", df, "qfq")

        manager = CacheManager(db_path=str(db_path))
        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=["600519.XSHG", "000858.XSHE"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(cache_dir),
        )

        assert is_valid is False
        assert "000858.XSHE" in report["missing_stocks"]
        assert len(report["incomplete_stocks"]) >= 1
        assert "trade_days" not in report["missing_meta"]
        assert "securities" not in report["missing_meta"]

    def test_validate_complete_cache(self, tmp_path):
        """测试完整缓存时的离线验证"""
        db_path = tmp_path / "complete_parquet"
        cache_dir = tmp_path / "complete_cache"

        trade_days_df = pd.DataFrame(
            {"date": pd.date_range("2022-01-01", "2024-12-31", freq="B").date}
        )
        securities_df = pd.DataFrame(
            {"code": ["sh600519", "sz000858"], "name": ["贵州茅台", "五粮液"]}
        )
        cache = parquet_get_cache_manager()
        cache.put("trade_calendar", trade_days_df)
        cache.put("securities", securities_df)

        dates = pd.date_range("2022-12-01", "2024-01-31", freq="D")
        df1 = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )
        df2 = df1.copy()

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sh600519", df1, "qfq")
        db.insert_stock_daily("sz000858", df2, "qfq")

        manager = CacheManager(db_path=str(db_path))
        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=["600519.XSHG", "000858.XSHE"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(cache_dir),
        )

        assert is_valid is True
        assert len(report["missing_stocks"]) == 0
        assert len(report["incomplete_stocks"]) == 0
        assert len(report["missing_meta"]) == 0

    def test_validate_with_custom_cache_dir(self, tmp_path):
        """测试自定义 cache_dir 参数"""
        custom_cache_dir = tmp_path / "custom_location"

        trade_days_df = pd.DataFrame(
            {"date": pd.date_range("2023-01-01", "2023-12-31", freq="B").date}
        )
        cache = parquet_get_cache_manager()
        cache.put("trade_calendar", trade_days_df)

        db_path = tmp_path / "custom_parquet"

        manager = CacheManager(db_path=str(db_path))
        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=["600519.XSHG"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(custom_cache_dir),
        )

        assert "trade_days" not in report["missing_meta"]
        assert is_valid is False

    def test_validate_report_format(self, tmp_path):
        """测试报告格式正确性"""
        db_path = tmp_path / "test_parquet"
        manager = CacheManager(db_path=str(db_path))

        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=["600519.XSHG"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(tmp_path),
        )

        assert "is_valid" in report
        assert "missing_stocks" in report
        assert "incomplete_stocks" in report
        assert "missing_meta" in report
        assert "cache_summary" in report

        assert isinstance(report["missing_stocks"], list)
        assert isinstance(report["incomplete_stocks"], list)
        assert isinstance(report["missing_meta"], list)
        assert isinstance(report["cache_summary"], dict)


class TestGetCacheSummary:
    """测试缓存摘要获取"""

    def test_get_summary_empty_database(self, tmp_path):
        """测试空数据库的摘要"""
        manager = CacheManager(db_path=str(tmp_path / "empty_parquet"))
        summary = manager.get_cache_summary()

        assert summary["stock_count"] == 0
        assert summary["etf_count"] == 0
        assert summary["index_count"] == 0
        assert summary["total_records"] == 0
        assert summary["symbols"] == []

    def test_get_summary_with_data(self, tmp_path):
        """测试有数据的摘要"""
        db_path = tmp_path / "summary_parquet"

        # 创建测试数据
        dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sh600519", df, "qfq")
        db.insert_stock_daily("sz000858", df, "qfq")
        db.insert_etf_daily("510300", df)
        db.insert_index_daily("000300", df)

        manager = CacheManager(db_path=str(db_path))
        summary = manager.get_cache_summary()

        assert summary["stock_count"] >= 2
        assert summary["etf_count"] >= 1
        assert summary["index_count"] >= 1
        assert summary["total_records"] > 0
        assert len(summary["symbols"]) >= 4


class TestSymbolConversion:
    """测试股票代码格式转换"""

    def test_jq_code_conversion_xshg(self, tmp_path):
        """测试 XSHG 格式代码转换 - validate_cache_for_offline 会转换"""
        db_path = tmp_path / "symbol_test_parquet"
        cache_dir = tmp_path / "symbol_cache"

        trade_days_df = pd.DataFrame(
            {"date": pd.date_range("2022-01-01", "2024-12-31", freq="B").date}
        )
        securities_df = pd.DataFrame({"code": ["sh600519"], "name": ["贵州茅台"]})
        cache = parquet_get_cache_manager()
        cache.put("trade_calendar", trade_days_df)
        cache.put("securities", securities_df)

        dates = pd.date_range("2022-12-01", "2024-01-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sh600519", df, "qfq")

        manager = CacheManager(db_path=str(db_path))

        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=["600519.XSHG"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(cache_dir),
        )
        assert is_valid is True

    def test_jq_code_conversion_xshe(self, tmp_path):
        """测试 XSHE 格式代码转换 - validate_cache_for_offline 会转换"""
        db_path = tmp_path / "symbol_test2_parquet"
        cache_dir = tmp_path / "symbol_cache2"

        trade_days_df = pd.DataFrame(
            {"date": pd.date_range("2022-01-01", "2024-12-31", freq="B").date}
        )
        securities_df = pd.DataFrame({"code": ["sz000858"], "name": ["五粮液"]})
        cache = parquet_get_cache_manager()
        cache.put("trade_calendar", trade_days_df)
        cache.put("securities", securities_df)

        dates = pd.date_range("2022-12-01", "2024-01-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sz000858", df, "qfq")

        manager = CacheManager(db_path=str(db_path))

        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=["000858.XSHE"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(cache_dir),
        )
        assert is_valid is True

    def test_validate_with_mixed_code_formats(self, tmp_path):
        """测试混合代码格式的离线验证"""
        db_path = tmp_path / "mixed_format_parquet"
        cache_dir = tmp_path / "mixed_cache"

        trade_days_df = pd.DataFrame(
            {"date": pd.date_range("2022-01-01", "2024-12-31", freq="B").date}
        )
        securities_df = pd.DataFrame({"code": ["sh600519"], "name": ["贵州茅台"]})
        cache = parquet_get_cache_manager()
        cache.put("trade_calendar", trade_days_df)
        cache.put("securities", securities_df)

        dates = pd.date_range("2022-12-01", "2024-01-31", freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * len(dates),
                "high": [11.0] * len(dates),
                "low": [9.0] * len(dates),
                "close": [10.5] * len(dates),
                "volume": [100000] * len(dates),
                "amount": [1000000.0] * len(dates),
            }
        )

        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        db = ParquetAdapter(db_path=str(db_path), read_only=False)
        db.insert_stock_daily("sh600519", df, "qfq")

        manager = CacheManager(db_path=str(db_path))

        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=["600519.XSHG"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(cache_dir),
        )
        assert is_valid is True


class TestConvenienceFunctions:
    """测试便捷函数"""

    def test_check_cache_status_function(self, tmp_path):
        """测试 check_cache_status 便捷函数"""
        result = check_cache_status(db_path=str(tmp_path / "test_parquet"))
        assert isinstance(result, dict)
        assert "stock_count" in result
        assert "total_records" in result

    def test_get_cache_manager_function(self):
        """测试 get_cache_manager 便捷函数"""
        manager = get_cache_manager()
        assert isinstance(manager, CacheManager)


class TestEdgeCases:
    """测试边界情况"""

    def test_validate_empty_stock_pool(self, tmp_path):
        """测试空股票池"""
        cache_dir = tmp_path / "edge_cache"

        trade_days_df = pd.DataFrame(
            {"date": pd.date_range("2023-01-01", "2023-12-31", freq="B").date}
        )
        securities_df = pd.DataFrame({"code": [], "name": []})
        cache = parquet_get_cache_manager()
        cache.put("trade_calendar", trade_days_df)
        cache.put("securities", securities_df)

        manager = CacheManager(db_path=str(tmp_path / "test_parquet"))
        is_valid, report = manager.validate_cache_for_offline(
            stock_pool=[],
            start_date="2023-01-01",
            end_date="2023-12-31",
            cache_base_dir=str(cache_dir),
        )

        assert is_valid is True
        assert len(report["missing_stocks"]) == 0

    def test_check_cache_with_invalid_symbol(self, tmp_path):
        """测试无效股票代码"""
        manager = CacheManager(db_path=str(tmp_path / "test_parquet"))

        # 无效代码应该返回空结果
        result = manager.check_stock_daily_cache(
            "INVALID_CODE", "2023-01-01", "2023-12-31", "qfq"
        )
        assert result["has_data"] is False

    def test_check_meta_cache_with_securities(self, tmp_path):
        """测试有证券信息缓存"""
        cache_dir = tmp_path / "old_cache"

        trade_days_df = pd.DataFrame(
            {"date": pd.date_range("2023-01-01", "2023-12-31", freq="B").date}
        )
        securities_df = pd.DataFrame({"code": ["sh600519"], "name": ["贵州茅台"]})
        cache = parquet_get_cache_manager()
        cache.put("trade_calendar", trade_days_df)
        cache.put("securities", securities_df)

        manager = CacheManager(db_path=str(tmp_path / "test_parquet"))
        result = manager.check_meta_cache(str(cache_dir))

        assert result["securities"] is True
        assert result["securities_date"] is not None
