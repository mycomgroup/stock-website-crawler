"""
src/data_access/data_source.py
数据源抽象基类 - 定义统一的数据访问接口。

所有数据源实现必须继承此基类并实现所有抽象方法。
这确保了不同数据源（AkShare, Tushare, Mock 等）提供一致的 API。
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
import pandas as pd


class DataSourceError(Exception):
    """数据源相关错误"""

    def __init__(self, message: str, source: str = None, symbol: str = None):
        self.message = message
        self.source = source
        self.symbol = symbol
        super().__init__(f"[{source or 'Unknown'}] {symbol or ''}: {message}")


class DataSource(ABC):
    """
    数据源抽象基类。

    定义了所有数据源必须实现的接口，包括:
    - 日线数据获取
    - 指数成分股查询
    - 交易日历
    - 股票列表
    - 分钟数据
    - 资金流向
    - 财务数据

    所有方法返回 pandas DataFrame 或标准 Python 类型。
    """

    # 数据源名称标识
    name: str = "abstract"

    # 数据源类型
    source_type: str = "abstract"

    @abstractmethod
    def get_daily_data(
        self,
        symbol: str,
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime],
        adjust: str = "qfq",
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取日线行情数据。

        Args:
            symbol: 股票/ETF/指数代码，支持多种格式
                - 'sh600000' / 'sz000001' (前缀格式)
                - '600000.XSHG' / '000001.XSHE' (聚宽格式)
                - '600000' / '000001' (纯代码)
            start_date: 起始日期，支持 'YYYY-MM-DD' / datetime / date
            end_date: 结束日期
            adjust: 复权类型
                - 'qfq': 前复权 (默认)
                - 'hfq': 后复权
                - 'none': 不复权

        Returns:
            DataFrame 标准化字段:
                - datetime: 日期 (datetime)
                - open: 开盘价 (float)
                - high: 最高价 (float)
                - low: 最低价 (float)
                - close: 收盘价 (float)
                - volume: 成交量 (int)
                - amount: 成交额 (float, 可选)

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_index_stocks(self, index_code: str, **kwargs) -> List[str]:
        """
        获取指数成分股列表。

        Args:
            index_code: 指数代码，支持:
                - '000300.XSHG' (沪深300)
                - '000905.XSHG' (中证500)
                - '000016.XSHG' (上证50)
                - '000852.XSHG' (中证1000)
                - '399006.XSHE' (创业板指)

        Returns:
            List[str]: 成分股代码列表（聚宽格式）
            如 ['600519.XSHG', '000858.XSHE', ...]

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_index_components(
        self,
        index_code: str,
        include_weights: bool = True,
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取指数成分股详情（含权重）。

        Args:
            index_code: 指数代码
            include_weights: 是否包含权重信息

        Returns:
            DataFrame:
                - index_code: 指数代码
                - code: 成分股代码
                - stock_name: 股票名称
                - weight: 权重 (如果 include_weights=True)
                - effective_date: 生效日期

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_trading_days(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> List[str]:
        """
        获取交易日列表。

        Args:
            start_date: 起始日期 (可选)
            end_date: 结束日期 (可选)

        Returns:
            List[str]: 交易日列表 ['2020-01-02', '2020-01-03', ...]

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_securities_list(
        self,
        security_type: str = "stock",
        date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取证券列表。

        Args:
            security_type: 证券类型
                - 'stock': A股股票
                - 'etf': ETF基金
                - 'index': 指数
                - 'lof': LOF基金
                - 'fund': 场内基金
            date: 查询日期 (可选，默认最新)

        Returns:
            DataFrame:
                - code: 证券代码
                - display_name: 证券名称
                - type: 证券类型
                - start_date: 上市日期

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_security_info(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """
        获取单个证券基本信息。

        Args:
            symbol: 证券代码

        Returns:
            Dict:
                - code: 代码
                - display_name: 名称
                - type: 类型
                - start_date: 上市日期
                - end_date: 退市日期 (如有)
                - industry: 行业 (如有)

        Raises:
            DataSourceError: 信息获取失败
        """
        pass

    @abstractmethod
    def get_minute_data(
        self,
        symbol: str,
        freq: str = "1min",
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取分钟线数据。

        Args:
            symbol: 证券代码
            freq: 频率
                - '1min': 1分钟
                - '5min': 5分钟
                - '15min': 15分钟
                - '30min': 30分钟
                - '60min': 60分钟
            start_date: 起始日期
            end_date: 结束日期

        Returns:
            DataFrame:
                - datetime: 时间戳
                - open, high, low, close, volume

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_money_flow(
        self,
        symbol: str,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取资金流向数据。

        Args:
            symbol: 股票代码
            start_date: 起始日期
            end_date: 结束日期

        Returns:
            DataFrame:
                - date: 日期
                - main_buy: 主力买入
                - main_sell: 主力卖出
                - main_net: 主力净额
                - retail_net: 散户净额

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_north_money_flow(
        self,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取北向资金流向。

        Args:
            start_date: 起始日期
            end_date: 结束日期

        Returns:
            DataFrame:
                - date: 日期
                - north_buy: 北向买入
                - north_sell: 北向卖出
                - north_net: 北向净额

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_industry_stocks(
        self,
        industry_code: str,
        level: int = 1,
        **kwargs,
    ) -> List[str]:
        """
        获取行业成分股。

        Args:
            industry_code: 行业代码 (申万行业)
                - '801010': 农林牧渔
                - '801030': 基础化工
                等
            level: 行业级别 (1/2/3)

        Returns:
            List[str]: 股票代码列表

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_industry_mapping(
        self,
        symbol: str,
        level: int = 1,
        **kwargs,
    ) -> str:
        """
        获取股票所属行业。

        Args:
            symbol: 股票代码
            level: 行业级别 (1/2/3)

        Returns:
            str: 行业代码

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_finance_indicator(
        self,
        symbol: str,
        fields: Optional[List[str]] = None,
        start_date: Optional[Union[str, date]] = None,
        end_date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取财务指标数据。

        Args:
            symbol: 股票代码
            fields: 需要的字段列表 (可选)
            start_date: 起始日期
            end_date: 结束日期

        Returns:
            DataFrame: 财务指标数据

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    @abstractmethod
    def get_call_auction(
        self,
        symbol: str,
        date: Optional[Union[str, date]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取集合竞价数据。

        Args:
            symbol: 股票代码
            date: 查询日期

        Returns:
            DataFrame: 集合竞价数据

        Raises:
            DataSourceError: 数据获取失败
        """
        pass

    # 可选方法 - 提供默认实现或抛出 NotImplementedError

    def get_etf_daily(
        self,
        symbol: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取 ETF 日线数据。

        默认使用 get_daily_data 实现。
        """
        return self.get_daily_data(symbol, start_date, end_date, adjust="none", **kwargs)

    def get_index_daily(
        self,
        symbol: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取指数日线数据。

        默认使用 get_daily_data 实现。
        """
        return self.get_daily_data(symbol, start_date, end_date, adjust="none", **kwargs)

    def get_lof_daily(
        self,
        symbol: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取 LOF 日线数据。
        """
        return self.get_daily_data(symbol, start_date, end_date, adjust="none", **kwargs)

    def get_conversion_bond_list(self, **kwargs) -> pd.DataFrame:
        """
        获取可转债列表。
        """
        raise NotImplementedError(f"{self.name} 不支持可转债数据")

    def get_option_list(self, **kwargs) -> pd.DataFrame:
        """
        获取期权列表。
        """
        raise NotImplementedError(f"{self.name} 不支持期权数据")

    def get_option_daily(
        self,
        symbol: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
        **kwargs,
    ) -> pd.DataFrame:
        """
        获取期权日线数据。
        """
        raise NotImplementedError(f"{self.name} 不支持期权日线数据")

    def health_check(self) -> Dict[str, Any]:
        """
        数据源健康检查。

        Returns:
            Dict:
                - status: 'ok' / 'error'
                - message: 状态信息
                - latency_ms: 响应延迟 (毫秒)
        """
        try:
            import time
            start = time.time()
            # 尝试获取一个简单的数据
            days = self.get_trading_days()
            latency = (time.time() - start) * 1000
            return {
                "status": "ok",
                "message": f"获取到 {len(days)} 个交易日",
                "latency_ms": round(latency, 2),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "latency_ms": None,
            }

    def get_source_info(self) -> Dict[str, Any]:
        """
        获取数据源信息。
        """
        return {
            "name": self.name,
            "type": self.source_type,
            "description": f"数据源: {self.name}",
        }


__all__ = ["DataSource", "DataSourceError"]