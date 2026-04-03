"""
src/data_access/mock_data_source.py
Mock 数据源 - 用于测试和开发。

提供模拟数据，无需实际访问外部 API。
支持:
- 预设数据注入
- 随机数据生成
- 测试场景模拟
"""

import logging
import random
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any, Union, Callable
import pandas as pd
import numpy as np

from .data_source import DataSource, DataSourceError

logger = logging.getLogger(__name__)


class MockDataSource(DataSource):
    """
    Mock 数据源 - 用于测试。

    提供模拟数据，无需实际网络请求。
    支持:
    - 预设数据 (可注入特定数据)
    - 随机数据生成 (用于通用测试)
    - 错误模拟 (测试异常处理)

    使用方式:
        # 创建 Mock 数据源
        mock = MockDataSource()

        # 获取模拟日线数据
        df = mock.get_daily_data('sh600000', '2020-01-01', '2020-12-31')

        # 注入预设数据
        mock.set_mock_data('daily', 'sh600000', preset_df)

        # 模拟错误
        mock.set_error_mode('network_error')

        # 注册到 DataRegistry
        from jk2bt.data_access import set_data_source
        set_data_source(mock)

    特性:
        1. 完全离线运行 - 无网络依赖
        2. 数据可预测 - 便于测试验证
        3. 支持错误模拟 - 测试异常处理
        4. 线程安全 - 多线程环境下安全使用
    """

    name = "mock"
    source_type = "mock"

    # 预设的指数成分股
    DEFAULT_INDEX_STOCKS = {
        "000300.XSHG": [  # 沪深300
            "600519.XSHG", "600036.XSHG", "601318.XSHG",
            "000858.XSHE", "000333.XSHE", "000651.XSHE",
        ],
        "000905.XSHG": [  # 中证500
            "002415.XSHE", "002230.XSHE", "300059.XSHE",
            "600703.XSHG", "600837.XSHG",
        ],
        "000016.XSHG": [  # 上证50
            "600519.XSHG", "600036.XSHG", "601318.XSHG",
            "600276.XSHG", "600887.XSHG",
        ],
        "000852.XSHG": [  # 中证1000
            "002230.XSHE", "300059.XSHE", "300750.XSHE",
        ],
    }

    # 预设的行业成分股
    DEFAULT_INDUSTRY_STOCKS = {
        "801010": ["600519.XSHG", "000858.XSHE"],  # 农林牧渔
        "801030": ["600426.XSHG", "000333.XSHE"],  # 基础化工
        "801080": ["600036.XSHG", "601318.XSHG"],  # 电子
    }

    # 预设的交易日
    DEFAULT_TRADING_DAYS = [
        "2020-01-02", "2020-01-03", "2020-01-06", "2020-01-07", "2020-01-08",
        "2020-01-09", "2020-01-10", "2020-01-13", "2020-01-14", "2020-01-15",
        "2020-01-16", "2020-01-17", "2020-01-20", "2020-01-21", "2020-01-22",
    ]

    def __init__(
        self,
        seed: int = 42,
        generate_random: bool = True,
        error_mode: str = None,
        preset_data: Dict[str, Dict] = None,
    ):
        """
        初始化 Mock 数据源。

        Args:
            seed: 随机种子 (确保数据可复现)
            generate_random: 是否生成随机数据 (无预设数据时)
            error_mode: 错误模式
                - None: 正常模式
                - 'network_error': 模拟网络错误
                - 'data_error': 模拟数据错误
                - 'timeout': 模拟超时
            preset_data: 预设数据字典
                {'daily': {'sh600000': df}, 'index_stocks': {'000300': ['...']}}
        """
        self._seed = seed
        self._generate_random = generate_random
        self._error_mode = error_mode
        self._preset_data = preset_data or {}

        # 初始化随机数生成器
        self._rng = np.random.RandomState(seed)

        # 数据存储
        self._daily_data: Dict[str, pd.DataFrame] = {}
        self._index_stocks: Dict[str, List[str]] = {}
        self._industry_stocks: Dict[str, List[str]] = {}
        self._trading_days: List[str] = []

        # 初始化默认数据
        self._init_defaults()

    def _init_defaults(self):
        """初始化默认数据"""
        # 复制预设数据
        self._index_stocks = dict(self.DEFAULT_INDEX_STOCKS)
        self._industry_stocks = dict(self.DEFAULT_INDUSTRY_STOCKS)
        self._trading_days = list(self.DEFAULT_TRADING_DAYS)

        # 合合用户预设数据
        if self._preset_data:
            if "daily" in self._preset_data:
                self._daily_data.update(self._preset_data["daily"])
            if "index_stocks" in self._preset_data:
                self._index_stocks.update(self._preset_data["index_stocks"])
            if "industry_stocks" in self._preset_data:
                self._industry_stocks.update(self._preset_data["industry_stocks"])
            if "trading_days" in self._preset_data:
                self._trading_days = self._preset_data["trading_days"]

    def set_error_mode(self, mode: str):
        """设置错误模式"""
        self._error_mode = mode

    def clear_error_mode(self):
        """清除错误模式"""
        self._error_mode = None

    def set_mock_data(self, data_type: str, key: str, data):
        """
        设置 Mock 数据。

        Args:
            data_type: 数据类型 ('daily', 'index_stocks', 'industry_stocks', 'trading_days')
            key: 数据键 (如 'sh600000', '000300.XSHG')
            data: 数据 (DataFrame 或 List)
        """
        if data_type == "daily":
            self._daily_data[key] = data
        elif data_type == "index_stocks":
            self._index_stocks[key] = data
        elif data_type == "industry_stocks":
            self._industry_stocks[key] = data
        elif data_type == "trading_days":
            self._trading_days = data

    def _check_error(self, symbol: str = None):
        """检查错误模式"""
        if self._error_mode == "network_error":
            raise DataSourceError("模拟网络错误", source=self.name, symbol=symbol)
        if self._error_mode == "data_error":
            raise DataSourceError("模拟数据错误", source=self.name, symbol=symbol)
        if self._error_mode == "timeout":
            raise DataSourceError("模拟超时", source=self.name, symbol=symbol)

    def _generate_daily_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        adjust: str = "qfq",
    ) -> pd.DataFrame:
        """生成随机日线数据"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        # 生成日期序列
        days = []
        current = start
        while current <= end:
            # 跳过周末
            if current.weekday() < 5:
                days.append(current)
            current += timedelta(days=1)

        if not days:
            return pd.DataFrame()

        # 基准价格 (随机)
        base_price = 10 + self._rng.random() * 90  # 10-100 元

        # 生成价格序列
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []

        for i, day in enumerate(days):
            # 每日波动 (模拟真实市场)
            daily_change = self._rng.randn() * 0.02  # 2% 日波动

            if i == 0:
                o = base_price
            else:
                o = closes[-1] * (1 + self._rng.randn() * 0.01)

            c = o * (1 + daily_change)
            h = max(o, c) * (1 + self._rng.random() * 0.01)
            l = min(o, c) * (1 - self._rng.random() * 0.01)

            # 成交量 (随机)
            v = int(1000000 + self._rng.randint(0, 5000000))

            opens.append(round(o, 2))
            highs.append(round(h, 2))
            lows.append(round(l, 2))
            closes.append(round(c, 2))
            volumes.append(v)

        df = pd.DataFrame({
            "datetime": days,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "amount": [o * v for o, v in zip(opens, volumes)],
        })

        return df

    # === 实现 DataSource 接口 ===

    def get_daily_data(
        self,
        symbol: str,
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime],
        adjust: str = "qfq",
        **kwargs,
    ) -> pd.DataFrame:
        """获取日线行情数据"""
        self._check_error(symbol)

        # 标准化日期
        if isinstance(start_date, (date, datetime)):
            start = start_date.strftime("%Y-%m-%d") if isinstance(start_date, date) else start_date.strftime("%Y-%m-%d")
        else:
            start = start_date

        if isinstance(end_date, (date, datetime)):
            end = end_date.strftime("%Y-%m-%d") if isinstance(end_date, date) else end_date.strftime("%Y-%m-%d")
        else:
            end = end_date

        # 标准化代码
        code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "")
        key = f"{symbol}_{adjust}"

        # 检查预设数据
        if key in self._daily_data:
            df = self._daily_data[key].copy()
            # 过滤日期范围
            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"])
                df = df[
                    (df["datetime"] >= pd.to_datetime(start))
                    & (df["datetime"] <= pd.to_datetime(end))
                ]
            return df

        # 检查无 adjust 的预设数据
        if symbol in self._daily_data:
            df = self._daily_data[symbol].copy()
            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"])
                df = df[
                    (df["datetime"] >= pd.to_datetime(start))
                    & (df["datetime"] <= pd.to_datetime(end))
                ]
            return df

        # 生成随机数据
        if self._generate_random:
            df = self._generate_daily_data(code, start, end, adjust)
            self._daily_data[key] = df  # 缓存
            return df

        return pd.DataFrame()

    def get_index_stocks(self, index_code: str, **kwargs) -> List[str]:
        """获取指数成分股列表"""
        self._check_error(index_code)

        # 标准化代码
        jq_code = index_code
        if ".XSHG" not in index_code and ".XSHE" not in index_code:
            # 添加聚宽格式
            if index_code.startswith("6") or index_code.startswith("000"):
                jq_code = f"{index_code.zfill(6)}.XSHG"
            else:
                jq_code = f"{index_code.zfill(6)}.XSHE"

        if jq_code in self._index_stocks:
            return self._index_stocks[jq_code]

        # 返回默认成分股或生成随机
        if self._generate_random:
            stocks = [f"600{self._rng.randint(100, 999)}.XSHG" for _ in range(5)]
            stocks.extend([f"000{self._rng.randint(100, 999)}.XSHE" for _ in range(5)])
            self._index_stocks[jq_code] = stocks
            return stocks

        return []

    def get_index_components(
        self,
        index_code: str,
        include_weights: bool = True,
        **kwargs,
    ) -> pd.DataFrame:
        """获取指数成分股详情"""
        self._check_error(index_code)

        stocks = self.get_index_stocks(index_code)

        if not stocks:
            return pd.DataFrame()

        result = pd.DataFrame()
        jq_code = index_code if "." in index_code else f"{index_code.zfill(6)}.XSHG"
        result["index_code"] = [jq_code] * len(stocks)
        result["code"] = stocks

        # 生成随机名称
        result["stock_name"] = [f"Mock股票{i}" for i in range(len(stocks))]

        if include_weights:
            # 等权重
            result["weight"] = [100.0 / len(stocks)] * len(stocks)

        result["effective_date"] = datetime.now().strftime("%Y-%m-%d")

        return result

    def get_trading_days(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> List[str]:
        """获取交易日列表"""
        self._check_error()

        days = self._trading_days.copy()

        # 过滤日期范围
        if start_date:
            if isinstance(start_date, (date, datetime)):
                start = start_date.strftime("%Y-%m-%d")
            else:
                start = start_date
            days = [d for d in days if d >= start]

        if end_date:
            if isinstance(end_date, (date, datetime)):
                end = end_date.strftime("%Y-%m-%d")
            else:
                end = end_date
            days = [d for d in days if d <= end]

        return days

    def get_securities_list(
        self,
        security_type: str = "stock",
        date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取证券列表"""
        self._check_error()

        # 生成模拟列表
        if self._generate_random:
            codes = []
            names = []

            if security_type == "stock":
                for i in range(10):
                    if self._rng.random() > 0.5:
                        codes.append(f"600{self._rng.randint(100, 999)}.XSHG")
                    else:
                        codes.append(f"000{self._rng.randint(100, 999)}.XSHE")
                    names.append(f"Mock股票{i}")
            elif security_type == "etf":
                for i in range(5):
                    codes.append(f"51{self._rng.randint(1, 9999):04d}.XSHG")
                    names.append(f"MockETF{i}")
            elif security_type == "index":
                codes = ["000300.XSHG", "000905.XSHG", "000016.XSHG"]
                names = ["沪深300", "中证500", "上证50"]
            else:
                codes = []
                names = []

            return pd.DataFrame({
                "code": codes,
                "display_name": names,
                "type": security_type,
            })

        return pd.DataFrame()

    def get_security_info(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取单个证券基本信息"""
        self._check_error(symbol)

        return {
            "code": symbol,
            "display_name": f"Mock{symbol}",
            "type": "stock",
            "start_date": "2020-01-01",
            "industry": "Mock行业",
        }

    def get_minute_data(
        self,
        symbol: str,
        freq: str = "1min",
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取分钟线数据"""
        self._check_error(symbol)

        if not self._generate_random:
            return pd.DataFrame()

        # 生成模拟分钟数据
        if start_date is None:
            start_date = datetime.now().strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")

        if isinstance(start_date, (date, datetime)):
            start = start_date.strftime("%Y-%m-%d")
        else:
            start = start_date

        start_dt = datetime.strptime(start, "%Y-%m-%d")

        # 生成一天的分时数据 (240 分钟)
        times = []
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []

        base_price = 10 + self._rng.random() * 90

        for i in range(240):
            t = start_dt + timedelta(minutes=i * 1)
            times.append(t)

            o = base_price * (1 + self._rng.randn() * 0.001)
            c = o * (1 + self._rng.randn() * 0.001)
            h = max(o, c) * (1 + self._rng.random() * 0.0005)
            l = min(o, c) * (1 - self._rng.random() * 0.0005)
            v = int(10000 + self._rng.randint(0, 50000))

            opens.append(round(o, 2))
            highs.append(round(h, 2))
            lows.append(round(l, 2))
            closes.append(round(c, 2))
            volumes.append(v)

        return pd.DataFrame({
            "datetime": times,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
        })

    def get_money_flow(
        self,
        symbol: str,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取资金流向数据"""
        self._check_error(symbol)

        if not self._generate_random:
            return pd.DataFrame()

        days = self.get_trading_days(start_date, end_date)

        return pd.DataFrame({
            "date": days,
            "main_buy": [self._rng.randint(1000000, 5000000) for _ in days],
            "main_sell": [self._rng.randint(1000000, 5000000) for _ in days],
            "main_net": [self._rng.randint(-2000000, 2000000) for _ in days],
            "retail_net": [self._rng.randint(-1000000, 1000000) for _ in days],
        })

    def get_north_money_flow(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取北向资金流向"""
        self._check_error()

        days = self.get_trading_days(start_date, end_date)

        return pd.DataFrame({
            "date": days,
            "north_buy": [self._rng.randint(50000000, 200000000) for _ in days],
            "north_sell": [self._rng.randint(50000000, 200000000) for _ in days],
            "north_net": [self._rng.randint(-50000000, 50000000) for _ in days],
        })

    def get_industry_stocks(
        self,
        industry_code: str,
        level: int = 1,
        **kwargs,
    ) -> List[str]:
        """获取行业成分股"""
        self._check_error(industry_code)

        code = industry_code.replace(".SI", "").zfill(6)

        if code in self._industry_stocks:
            return self._industry_stocks[code]

        if self._generate_random:
            stocks = [f"600{self._rng.randint(100, 999)}.XSHG" for _ in range(3)]
            stocks.extend([f"000{self._rng.randint(100, 999)}.XSHE" for _ in range(2)])
            self._industry_stocks[code] = stocks
            return stocks

        return []

    def get_industry_mapping(
        self,
        symbol: str,
        level: int = 1,
        **kwargs,
    ) -> str:
        """获取股票所属行业"""
        self._check_error(symbol)
        return "801010"  # 默认返回农林牧渔

    def get_finance_indicator(
        self,
        symbol: str,
        fields: Optional[List[str]] = None,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取财务指标数据"""
        self._check_error(symbol)

        if not self._generate_random:
            return pd.DataFrame()

        # 生成模拟财务数据
        return pd.DataFrame({
            "date": ["2020-03-31", "2020-06-30", "2020-09-30", "2020-12-31"],
            "roe": [0.15, 0.16, 0.17, 0.18],
            "pe_ratio": [10 + self._rng.random() * 20 for _ in range(4)],
            "pb_ratio": [1 + self._rng.random() * 3 for _ in range(4)],
        })

    def get_call_auction(
        self,
        symbol: str,
        date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """获取集合竞价数据"""
        self._check_error(symbol)

        if not self._generate_random:
            return pd.DataFrame()

        return pd.DataFrame({
            "time": ["09:15:00", "09:20:00", "09:25:00"],
            "price": [10.0, 10.5, 11.0],
            "volume": [10000, 20000, 30000],
        })

    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "status": "ok",
            "message": "Mock 数据源运行正常",
            "latency_ms": 0,
        }

    def get_source_info(self) -> Dict[str, Any]:
        """获取数据源信息"""
        return {
            "name": self.name,
            "type": self.source_type,
            "description": "Mock 数据源 (用于测试)",
            "error_mode": self._error_mode,
            "generate_random": self._generate_random,
            "seed": self._seed,
        }


# 预设 Mock 数据工厂函数
def create_mock_with_sample_data() -> MockDataSource:
    """
    创建带预设示例数据的 Mock 数据源。

    Returns:
        MockDataSource: 带预设数据的 Mock 数据源
    """
    # 创建示例日线数据
    sample_daily = pd.DataFrame({
        "datetime": pd.to_datetime([
            "2020-01-02", "2020-01-03", "2020-01-06", "2020-01-07", "2020-01-08",
        ]),
        "open": [10.0, 10.2, 10.5, 10.3, 10.6],
        "high": [10.5, 10.5, 11.0, 10.8, 11.0],
        "low": [9.8, 10.0, 10.2, 10.0, 10.4],
        "close": [10.2, 10.3, 10.8, 10.5, 10.8],
        "volume": [1000000, 1100000, 1200000, 1050000, 1150000],
    })

    preset_data = {
        "daily": {
            "sh600000": sample_daily,
            "600000.XSHG": sample_daily,
        },
        "index_stocks": dict(MockDataSource.DEFAULT_INDEX_STOCKS),
        "trading_days": MockDataSource.DEFAULT_TRADING_DAYS,
    }

    return MockDataSource(seed=42, preset_data=preset_data)


__all__ = ["MockDataSource", "create_mock_with_sample_data"]