"""
db/cache_status.py
数据缓存状态检查器，提供统一的缓存预热、查询和状态检查接口。

主要功能：
1. 检查缓存状态（是否存在、是否完整）
2. 批量预热数据
3. 离线模式支持
4. 缓存范围统计
"""

import os
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import pandas as pd

from .duckdb_manager import DuckDBManager

logger = logging.getLogger(__name__)


class CacheManager:
    """数据缓存管理器"""

    def __init__(self, db_path: str = None):
        self.db = DuckDBManager(db_path=db_path, read_only=True)
        self.db_path = db_path or self.db.db_path

    def check_stock_daily_cache(
        self, symbol: str, start: str, end: str, adjust: str = "qfq"
    ) -> Dict:
        """
        检查股票日线缓存状态。

        Returns:
            Dict: {
                'has_data': bool,
                'is_complete': bool,
                'min_date': str,
                'max_date': str,
                'count': int
            }
        """
        result = {
            "has_data": False,
            "is_complete": False,
            "min_date": None,
            "max_date": None,
            "count": 0,
        }

        try:
            count = self.db.count_records("stock_daily", symbol, adjust)
            if count > 0:
                result["has_data"] = True
                result["count"] = count

                with self.db._get_connection(read_only=True) as conn:
                    row = conn.execute(
                        """
                        SELECT MIN(datetime), MAX(datetime)
                        FROM stock_daily
                        WHERE symbol = ? AND adjust = ?
                    """,
                        [symbol, adjust],
                    ).fetchone()

                    if row and row[0]:
                        result["min_date"] = str(row[0])
                        result["max_date"] = str(row[1])

                        min_dt = pd.to_datetime(row[0])
                        max_dt = pd.to_datetime(row[1])
                        start_dt = pd.to_datetime(start)
                        end_dt = pd.to_datetime(end)

                        result["is_complete"] = min_dt <= start_dt and max_dt >= end_dt
        except Exception as e:
            logger.warning(f"检查缓存状态失败 {symbol}: {e}")

        return result

    def check_etf_daily_cache(self, symbol: str, start: str, end: str) -> Dict:
        """检查ETF日线缓存状态"""
        result = {
            "has_data": False,
            "is_complete": False,
            "min_date": None,
            "max_date": None,
            "count": 0,
        }

        try:
            count = self.db.count_records("etf_daily", symbol)
            if count > 0:
                result["has_data"] = True
                result["count"] = count

                with self.db._get_connection(read_only=True) as conn:
                    row = conn.execute(
                        """
                        SELECT MIN(datetime), MAX(datetime)
                        FROM etf_daily
                        WHERE symbol = ?
                    """,
                        [symbol],
                    ).fetchone()

                    if row and row[0]:
                        result["min_date"] = str(row[0])
                        result["max_date"] = str(row[1])

                        min_dt = pd.to_datetime(row[0])
                        max_dt = pd.to_datetime(row[1])
                        start_dt = pd.to_datetime(start)
                        end_dt = pd.to_datetime(end)

                        result["is_complete"] = min_dt <= start_dt and max_dt >= end_dt
        except Exception as e:
            logger.warning(f"检查ETF缓存状态失败 {symbol}: {e}")

        return result

    def check_index_daily_cache(self, symbol: str, start: str, end: str) -> Dict:
        """检查指数日线缓存状态"""
        result = {
            "has_data": False,
            "is_complete": False,
            "min_date": None,
            "max_date": None,
            "count": 0,
        }

        try:
            count = self.db.count_records("index_daily", symbol)
            if count > 0:
                result["has_data"] = True
                result["count"] = count

                with self.db._get_connection(read_only=True) as conn:
                    row = conn.execute(
                        """
                        SELECT MIN(datetime), MAX(datetime)
                        FROM index_daily
                        WHERE symbol = ?
                    """,
                        [symbol],
                    ).fetchone()

                    if row and row[0]:
                        result["min_date"] = str(row[0])
                        result["max_date"] = str(row[1])

                        min_dt = pd.to_datetime(row[0])
                        max_dt = pd.to_datetime(row[1])
                        start_dt = pd.to_datetime(start)
                        end_dt = pd.to_datetime(end)

                        result["is_complete"] = min_dt <= start_dt and max_dt >= end_dt
        except Exception as e:
            logger.warning(f"检查指数缓存状态失败 {symbol}: {e}")

        return result

    def get_cache_summary(self) -> Dict:
        """
        获取缓存整体摘要。

        Returns:
            Dict: {
                'stock_count': int,  # 有数据的股票数
                'etf_count': int,
                'index_count': int,
                'total_records': int,
                'symbols': List[str]
            }
        """
        summary = {
            "stock_count": 0,
            "etf_count": 0,
            "index_count": 0,
            "total_records": 0,
            "symbols": [],
        }

        try:
            stock_symbols = self.db.get_symbols("stock_daily")
            summary["stock_count"] = len(stock_symbols)
            summary["symbols"].extend(stock_symbols)

            etf_symbols = self.db.get_symbols("etf_daily")
            summary["etf_count"] = len(etf_symbols)
            summary["symbols"].extend(etf_symbols)

            index_symbols = self.db.get_symbols("index_daily")
            summary["index_count"] = len(index_symbols)
            summary["symbols"].extend(index_symbols)

            summary["total_records"] = (
                self.db.count_records("stock_daily")
                + self.db.count_records("etf_daily")
                + self.db.count_records("index_daily")
            )
        except Exception as e:
            logger.warning(f"获取缓存摘要失败: {e}")

        return summary

    def check_meta_cache(self, cache_base_dir: str = None) -> Dict:
        """
        检查元数据缓存状态（交易日历、证券信息等）。

        Returns:
            Dict: {
                'trade_days': bool,
                'securities': bool,
                'index_weights': Dict[str, bool]
            }
        """
        if cache_base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_base_dir = os.path.join(base_dir, "cache")

        result = {
            "trade_days": False,
            "securities": False,
            "securities_date": None,
            "index_weights": {},
        }

        meta_cache_dir = os.path.join(cache_base_dir, "meta_cache")
        index_cache_dir = os.path.join(cache_base_dir, "index_cache")

        trade_days_file = os.path.join(meta_cache_dir, "trade_days.pkl")
        if os.path.exists(trade_days_file):
            result["trade_days"] = True
            try:
                mtime = os.path.getmtime(trade_days_file)
                result["trade_days_date"] = datetime.fromtimestamp(mtime).strftime(
                    "%Y-%m-%d"
                )
            except Exception:
                pass

        securities_files = [
            f for f in os.listdir(meta_cache_dir) if f.startswith("securities_")
        ]
        if securities_files:
            result["securities"] = True
            latest = sorted(securities_files)[-1]
            result["securities_date"] = latest.replace("securities_", "").replace(
                ".pkl", ""
            )

        if os.path.exists(index_cache_dir):
            for f in os.listdir(index_cache_dir):
                if f.endswith("_weights.pkl"):
                    index_code = f.replace("_weights.pkl", "")
                    result["index_weights"][index_code] = True

        return result

    def validate_cache_for_offline(
        self,
        stock_pool: List[str],
        start_date: str,
        end_date: str,
        adjust: str = "qfq",
        cache_base_dir: str = None,
    ) -> Tuple[bool, Dict]:
        """
        验证缓存是否足够支持离线运行。

        Returns:
            Tuple[bool, Dict]: (是否可用, 详细报告)
        """
        report = {
            "is_valid": True,
            "missing_stocks": [],
            "incomplete_stocks": [],
            "missing_meta": [],
            "cache_summary": {},
        }

        for stock in stock_pool:
            ak_code = stock
            if stock.endswith(".XSHG") or stock.endswith(".XSHE"):
                ak_code = (
                    "sh" + stock[:6] if stock.endswith(".XSHG") else "sz" + stock[:6]
                )
            elif not stock.startswith("sh") and not stock.startswith("sz"):
                ak_code = ("sh" if stock.startswith("6") else "sz") + stock.zfill(6)

            status = self.check_stock_daily_cache(ak_code, start_date, end_date, adjust)

            if not status["has_data"]:
                report["missing_stocks"].append(stock)
                report["is_valid"] = False
            elif not status["is_complete"]:
                report["incomplete_stocks"].append(
                    {
                        "symbol": stock,
                        "min_date": status["min_date"],
                        "max_date": status["max_date"],
                    }
                )
                report["is_valid"] = False

        meta_status = self.check_meta_cache(cache_base_dir)
        report["cache_summary"] = meta_status

        if not meta_status["trade_days"]:
            report["missing_meta"].append("trade_days")
            report["is_valid"] = False

        if not meta_status["securities"]:
            report["missing_meta"].append("securities")
            report["is_valid"] = False

        return report["is_valid"], report


def get_cache_manager(db_path: str = None) -> CacheManager:
    """获取缓存管理器实例"""
    return CacheManager(db_path=db_path)


def check_cache_status(db_path: str = None) -> Dict:
    """快速检查缓存状态的便捷函数"""
    manager = get_cache_manager(db_path)
    return manager.get_cache_summary()
