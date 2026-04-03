"""
tests/mock_data.py
测试模拟数据提供者

功能：
1. 提供固定的测试数据，避免网络依赖
2. 支持离线测试
3. 数据可重复验证
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any
import os
import pickle
from pathlib import Path

MOCK_DATA_DIR = Path(__file__).parent / "mock_data_cache"


class MockDataProvider:
    """模拟数据提供者"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self._cache: Dict[str, pd.DataFrame] = {}
        self._ensure_dir()
        self._load_cached_data()

    def _ensure_dir(self):
        MOCK_DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _load_cached_data(self):
        """加载缓存的测试数据"""
        cache_file = MOCK_DATA_DIR / "mock_cache.pkl"
        if cache_file.exists():
            try:
                with open(cache_file, "rb") as f:
                    self._cache = pickle.load(f)
            except Exception:
                self._cache = {}

    def _save_cache(self):
        """保存测试数据到缓存"""
        cache_file = MOCK_DATA_DIR / "mock_cache.pkl"
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(self._cache, f)
        except Exception:
            pass

    def get_company_info(self, code: str) -> pd.DataFrame:
        """获取公司基本信息模拟数据"""
        key = f"company_info_{code}"

        if key in self._cache:
            return self._cache[key].copy()

        data = {
            "600519": {
                "code": "600519.XSHG",
                "company_name": "贵州茅台酒股份有限公司",
                "establish_date": "1999-11-20",
                "list_date": "2001-08-27",
                "main_business": "茅台酒及系列酒的生产与销售",
                "industry": "饮料制造",
                "registered_address": "贵州省仁怀市茅台镇",
                "company_status": "正常交易",
                "status_change_date": None,
                "change_type": None,
            },
            "000001": {
                "code": "000001.XSHE",
                "company_name": "平安银行股份有限公司",
                "establish_date": "1987-12-22",
                "list_date": "1991-04-03",
                "main_business": "商业银行业务",
                "industry": "银行",
                "registered_address": "广东省深圳市福田区",
                "company_status": "正常交易",
                "status_change_date": None,
                "change_type": None,
            },
            "600036": {
                "code": "600036.XSHG",
                "company_name": "招商银行股份有限公司",
                "establish_date": "1987-03-31",
                "list_date": "2002-04-09",
                "main_business": "商业银行业务",
                "industry": "银行",
                "registered_address": "广东省深圳市福田区",
                "company_status": "正常交易",
                "status_change_date": None,
                "change_type": None,
            },
        }

        if code in data:
            df = pd.DataFrame([data[code]])
            self._cache[key] = df
            self._save_cache()
            return df

        return pd.DataFrame()

    def get_security_status(self, code: str, date: str = None) -> pd.DataFrame:
        """获取证券状态模拟数据"""
        key = f"security_status_{code}_{date}"

        if key in self._cache:
            return self._cache[key].copy()

        data = {
            "code": [code + ".XSHG" if code.startswith("6") else code + ".XSHE"],
            "status_date": [date or datetime.now().strftime("%Y-%m-%d")],
            "status_type": ["正常交易"],
            "reason": [None],
        }

        df = pd.DataFrame(data)
        self._cache[key] = df
        self._save_cache()
        return df

    def get_shareholder_data(self, code: str) -> pd.DataFrame:
        """获取股东数据模拟数据"""
        key = f"shareholder_{code}"

        if key in self._cache:
            return self._cache[key].copy()

        data = {
            "code": [code] * 5,
            "shareholder_name": [
                "中国贵州茅台酒厂(集团)有限责任公司",
                "香港中央结算有限公司",
                "贵州省国有资本运营有限责任公司",
                "茅台酒厂集团技术开发公司",
                "中央汇金资产管理有限责任公司",
            ],
            "share_count": [678000000, 125000000, 56000000, 28000000, 15000000],
            "share_ratio": [54.06, 9.96, 4.46, 2.23, 1.20],
            "shareholder_type": ["国有股", "境外投资者", "国有股", "国有股", "国有股"],
            "report_date": ["2024-09-30"] * 5,
        }

        df = pd.DataFrame(data)
        self._cache[key] = df
        self._save_cache()
        return df

    def get_dividend_data(self, code: str) -> pd.DataFrame:
        """获取分红数据模拟数据"""
        key = f"dividend_{code}"

        if key in self._cache:
            return self._cache[key].copy()

        data = {
            "code": [code] * 3,
            "board_plan_pub_date": ["2024-03-15", "2023-03-20", "2022-03-25"],
            "bonus_amount_rmb": [308.76, 259.11, 216.75],
            "bonus_rmb": [30.876, 25.911, 21.675],
            "ex_dividend_date": ["2024-06-19", "2023-06-30", "2022-06-30"],
        }

        df = pd.DataFrame(data)
        self._cache[key] = df
        self._save_cache()
        return df

    def get_stock_daily(self, code: str, start: str, end: str) -> pd.DataFrame:
        """获取股票日线模拟数据"""
        key = f"stock_daily_{code}_{start}_{end}"

        if key in self._cache:
            return self._cache[key].copy()

        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        dates = pd.date_range(start=start_dt, end=end_dt, freq="B")  # 工作日

        import numpy as np

        np.random.seed(42)

        base_price = 1800.0 if "600519" in code else 100.0
        changes = np.random.randn(len(dates)) * 0.02
        prices = base_price * (1 + changes).cumprod()

        data = {
            "datetime": dates,
            "open": prices * (1 + np.random.rand(len(dates)) * 0.02),
            "high": prices * (1 + np.random.rand(len(dates)) * 0.03),
            "low": prices * (1 - np.random.rand(len(dates)) * 0.02),
            "close": prices,
            "volume": np.random.randint(1000000, 10000000, len(dates)),
            "money": prices * np.random.randint(1000000, 10000000, len(dates)),
        }

        df = pd.DataFrame(data)
        self._cache[key] = df
        self._save_cache()
        return df

    def get_unlock_data(self, code: str) -> pd.DataFrame:
        """获取解禁数据模拟数据"""
        key = f"unlock_{code}"

        if key in self._cache:
            return self._cache[key].copy()

        data = {
            "code": [code],
            "unlock_date": ["2025-06-15"],
            "unlock_share": [10000000],
            "unlock_ratio": [0.08],
            "unlock_type": ["定向增发"],
        }

        df = pd.DataFrame(data)
        self._cache[key] = df
        self._save_cache()
        return df


MOCK_PROVIDER = MockDataProvider()


def use_mock_data(func):
    """装饰器：使用模拟数据进行测试"""

    def wrapper(*args, **kwargs):
        if "force_update" in kwargs:
            kwargs["force_update"] = False
        if "use_mock" in kwargs and kwargs["use_mock"]:
            return getattr(MOCK_PROVIDER, func.__name__)(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper
