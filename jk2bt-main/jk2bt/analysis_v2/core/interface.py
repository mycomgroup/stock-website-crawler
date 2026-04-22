"""
数据源抽象接口 - 核心解耦层

此模块定义数据源接口，使得计算逻辑与数据获取完全分离。
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Union
from datetime import datetime
import pandas as pd


class DataSource(ABC):
    """数据源抽象接口"""
    
    @abstractmethod
    def get_ohlcv(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> pd.DataFrame:
        """
        获取OHLCV数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            count: 获取数据条数
        
        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        """
        pass
    
    @abstractmethod
    def get_ohlcv_batch(
        self,
        symbols: List[str],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> dict[str, pd.DataFrame]:
        """
        批量获取OHLCV数据
        
        Args:
            symbols: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            count: 获取数据条数
        
        Returns:
            字典: {symbol: DataFrame}
        """
        pass
    
    @abstractmethod
    def get_index_daily(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        获取指数日线数据
        
        Args:
            symbol: 指数代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            DataFrame with columns: date, open, high, low, close, volume
        """
        pass
    
    @abstractmethod
    def get_valuation(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        获取估值数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            DataFrame with columns: date, pe_ratio, pb_ratio, market_cap, etc.
        """
        pass
    
    @abstractmethod
    def get_financial(
        self,
        symbol: str,
        table: str
    ) -> pd.DataFrame:
        """
        获取财务数据
        
        Args:
            symbol: 股票代码
            table: 表名 ("income", "balance", "cashflow")
        
        Returns:
            DataFrame with financial data
        """
        pass
    
    @abstractmethod
    def get_index_components(self, index_symbol: str) -> List[str]:
        """
        获取指数成分股
        
        Args:
            index_symbol: 指数代码
        
        Returns:
            成分股代码列表
        """
        pass


class DataSourceContext:
    """
    数据源上下文管理器
    
    支持依赖注入，使得计算逻辑可以独立测试
    
    使用示例:
        # 设置全局数据源
        DataSourceContext.set_data_source(MyDataSource())
        
        # 获取数据源
        ds = DataSourceContext.get_data_source()
        
        # 测试时清除
        DataSourceContext.clear()
    """
    _instance: Optional[DataSource] = None
    
    @classmethod
    def set_data_source(cls, data_source: DataSource) -> None:
        """设置全局数据源"""
        cls._instance = data_source
    
    @classmethod
    def get_data_source(cls) -> DataSource:
        """获取当前数据源"""
        if cls._instance is None:
            raise RuntimeError(
                "DataSource not initialized. "
                "Call DataSourceContext.set_data_source() first, "
                "or use init_data_source() from analysis_v2.data.adapter"
            )
        return cls._instance
    
    @classmethod
    def clear(cls) -> None:
        """清除数据源（用于测试）"""
        cls._instance = None
    
    @classmethod
    def is_initialized(cls) -> bool:
        """检查是否已初始化"""
        return cls._instance is not None