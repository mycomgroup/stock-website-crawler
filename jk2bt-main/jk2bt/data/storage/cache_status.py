"""
db/cache_status.py
数据缓存状态检查器，提供统一的缓存预热、查询和状态检查接口。

主要功能：
1. 检查缓存状态（是否存在、是否完整）
2. 批量预热数据
3. 离线模式支持
4. 缓存范围统计

格式兼容 (GATE-3):
- 支持 akshare 格式 (sh600519)、聚宽格式 (600519.XSHG)、纯数字 (600519) 三种格式输入
- 内部统一转换为聚宽格式查询数据库
"""

import os
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import pandas as pd

from .parquet_adapter import ParquetAdapter
from jk2bt.utils.symbol import ak_code_to_jq as normalize_to_jq_format

logger = logging.getLogger(__name__)


class CacheManager:
    """数据缓存管理器"""

    def __init__(self, db_path: str = None):
        self.db = ParquetAdapter(db_path=db_path, read_only=True)
        self.db_path = (
            db_path
            or getattr(self.db, "db_path", None)
            or getattr(self.db, "_base_dir", None)
        )

    def _get_date_range(
        self, table: str, where: dict
    ) -> Tuple[Optional[str], Optional[str]]:
        """获取指定表的日期范围"""
        df = self.db.query(table, where=where)
        if df.empty or "datetime" not in df.columns:
            return None, None
        min_date = str(df["datetime"].min())
        max_date = str(df["datetime"].max())
        return min_date, max_date

    def check_stock_daily_cache(
        self, symbol: str, start: str, end: str, adjust: str = "qfq"
    ) -> Dict:
        """
        检查股票日线缓存状态。

        参数:
            symbol: 股票代码，支持多种格式（sh600519, 600519.XSHG, 600519）

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

        # 统一转换为聚宽格式查询数据库
        jq_symbol = normalize_to_jq_format(symbol)

        try:
            count = self.db.count_records("stock_daily", jq_symbol, adjust)
            if count > 0:
                result["has_data"] = True
                result["count"] = count

                min_date, max_date = self._get_date_range(
                    "stock_daily", {"symbol": jq_symbol}
                )
                if min_date:
                    result["min_date"] = min_date
                    result["max_date"] = max_date

                    min_dt = pd.to_datetime(min_date)
                    max_dt = pd.to_datetime(max_date)
                    start_dt = pd.to_datetime(start)
                    end_dt = pd.to_datetime(end)

                    result["is_complete"] = min_dt <= start_dt and max_dt >= end_dt
        except Exception as e:
            logger.warning(f"检查缓存状态失败 {symbol}: {e}")

        return result

    def check_etf_daily_cache(self, symbol: str, start: str, end: str) -> Dict:
        """
        检查ETF日线缓存状态。

        参数:
            symbol: ETF代码，支持多种格式（510300.XSHG, 510300）
        """
        result = {
            "has_data": False,
            "is_complete": False,
            "min_date": None,
            "max_date": None,
            "count": 0,
        }

        # 统一转换为聚宽格式查询数据库
        jq_symbol = normalize_to_jq_format(symbol)

        try:
            count = self.db.count_records("etf_daily", jq_symbol)
            if count > 0:
                result["has_data"] = True
                result["count"] = count

                min_date, max_date = self._get_date_range(
                    "etf_daily", {"symbol": jq_symbol}
                )
                if min_date:
                    result["min_date"] = min_date
                    result["max_date"] = max_date

                    min_dt = pd.to_datetime(min_date)
                    max_dt = pd.to_datetime(max_date)
                    start_dt = pd.to_datetime(start)
                    end_dt = pd.to_datetime(end)

                    result["is_complete"] = min_dt <= start_dt and max_dt >= end_dt
        except Exception as e:
            logger.warning(f"检查ETF缓存状态失败 {symbol}: {e}")

        return result

    def check_index_daily_cache(self, symbol: str, start: str, end: str) -> Dict:
        """
        检查指数日线缓存状态。

        参数:
            symbol: 指数代码，支持多种格式（000300.XSHG, 000300）
        """
        result = {
            "has_data": False,
            "is_complete": False,
            "min_date": None,
            "max_date": None,
            "count": 0,
        }

        # 统一转换为聚宽格式查询数据库
        jq_symbol = normalize_to_jq_format(symbol)

        try:
            count = self.db.count_records("index_daily", jq_symbol)
            if count > 0:
                result["has_data"] = True
                result["count"] = count

                min_date, max_date = self._get_date_range(
                    "index_daily", {"symbol": jq_symbol}
                )
                if min_date:
                    result["min_date"] = min_date
                    result["max_date"] = max_date

                    min_dt = pd.to_datetime(min_date)
                    max_dt = pd.to_datetime(max_date)
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
                'index_weights': Dict[str, bool],
                'trade_days_date': str|None,
                'securities_date': str|None,
            }
        """
        if cache_base_dir is None:
            # 从统一配置获取缓存目录
            try:
                from jk2bt.utils.config import get_config

                config = get_config()
                cache_base_dir = config.cache.cache_dir
            except Exception:
                # fallback 到原有逻辑（向后兼容）
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                cache_base_dir = os.path.join(base_dir, "cache")

        result = {
            "trade_days": False,
            "securities": False,
            "index_weights": {},
            "trade_days_date": None,
            "securities_date": None,
        }

        # 通过 parquet_cache 查询元数据状态
        try:
            from .meta_cache_api import check_meta_cache_status

            meta_status = check_meta_cache_status()

            if meta_status.get("trade_calendar", 0) > 0:
                result["trade_days"] = True
                result["trade_days_date"] = datetime.now().strftime("%Y-%m-%d")

            if meta_status.get("securities", 0) > 0:
                result["securities"] = True
                result["securities_date"] = datetime.now().strftime("%Y-%m-%d")

            # 通过 parquet_cache 查询 index_weights
            try:
                df = self.db.query("index_weights")
                if not df.empty and "index_code" in df.columns:
                    for code in df["index_code"].unique():
                        result["index_weights"][str(code)] = True
            except Exception:
                pass

            # 如果 parquet 中有任何元数据，直接返回
            if result["trade_days"] or result["securities"] or result["index_weights"]:
                return result
        except Exception as e:
            logger.warning(f"检查 parquet 元数据缓存失败: {e}")

        # 向后兼容：检查遗留的 .pkl 文件
        meta_cache_dir = os.path.join(cache_base_dir, "meta_cache")
        index_cache_dir = os.path.join(cache_base_dir, "index_cache")

        has_legacy = False
        if os.path.exists(meta_cache_dir):
            if os.path.exists(os.path.join(meta_cache_dir, "trade_days.pkl")):
                has_legacy = True
            if any(f.startswith("securities_") for f in os.listdir(meta_cache_dir)):
                has_legacy = True
        if os.path.exists(index_cache_dir):
            if any(f.endswith("_weights.pkl") for f in os.listdir(index_cache_dir)):
                has_legacy = True

        if has_legacy:
            logger.warning(
                "检测到遗留的 .pkl 缓存文件，请执行 "
                "`python -m jk2bt.db.migrate` 进行迁移"
            )

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

        参数:
            stock_pool: 股票代码列表，支持多种格式（600519.XSHG, sh600519, 600519）

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
            # 直接传递原始格式，check_stock_daily_cache内部会处理格式转换
            status = self.check_stock_daily_cache(stock, start_date, end_date, adjust)

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
