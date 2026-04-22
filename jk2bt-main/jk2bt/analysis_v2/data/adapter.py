"""
数据源适配器 - 对接 jk2bt.data

此模块是 analysis_v2 唯一依赖 jk2bt.data 的地方，
其他模块通过 DataSource 接口使用数据。
"""
from typing import List, Optional
from datetime import datetime
import pandas as pd

from ..core.interface import DataSource


class Jk2btDataAdapter(DataSource):
    """聚宽风格数据适配器"""
    
    def __init__(self):
        """初始化适配器，延迟导入 jk2bt.data"""
        try:
            from jk2bt.data.sources import get_adapter
            self._adapter = get_adapter()
            self._available = True
        except ImportError:
            self._adapter = None
            self._available = False
    
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        return self._available
    
    def get_ohlcv(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> pd.DataFrame:
        """获取OHLCV数据"""
        if not self._available:
            raise RuntimeError("jk2bt.data is not available")
        
        from jk2bt.data.market.stock import get_stock_daily
        
        df = get_stock_daily(
            symbol,
            start_date=start_date,
            end_date=end_date,
            count=count
        )
        return self._normalize_ohlcv(df)
    
    def get_ohlcv_batch(
        self,
        symbols: List[str],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> dict[str, pd.DataFrame]:
        """批量获取OHLCV数据"""
        result = {}
        for symbol in symbols:
            try:
                result[symbol] = self.get_ohlcv(symbol, start_date, end_date, count)
            except Exception:
                result[symbol] = pd.DataFrame()
        return result
    
    def get_index_daily(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """获取指数日线数据"""
        if not self._available:
            raise RuntimeError("jk2bt.data is not available")
        
        return self._adapter.get_index_daily(
            symbol,
            start_date=start_date,
            end_date=end_date
        )
    
    def get_valuation(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """获取估值数据"""
        if not self._available:
            raise RuntimeError("jk2bt.data is not available")
        
        indicators = ['pe_ratio', 'pb_ratio', 'market_cap', 'circulating_market_cap']
        return self._adapter.get_stock_valuation_baidu(
            symbol,
            indicators=indicators
        )
    
    def get_financial(
        self,
        symbol: str,
        table: str
    ) -> pd.DataFrame:
        """获取财务数据"""
        if not self._available:
            raise RuntimeError("jk2bt.data is not available")
        
        table_map = {
            "income": "get_income_statement",
            "balance": "get_balance_sheet",
            "cashflow": "get_cashflow_statement"
        }
        
        method_name = table_map.get(table)
        if not method_name:
            raise ValueError(f"Unknown financial table: {table}")
        
        method = getattr(self._adapter, method_name, None)
        if method is None:
            raise AttributeError(f"Method {method_name} not found in adapter")
        
        return method(symbol)
    
    def get_index_components(self, index_symbol: str) -> List[str]:
        """获取指数成分股"""
        if not self._available:
            raise RuntimeError("jk2bt.data is not available")
        
        return self._adapter.get_index_stocks(index_symbol)
    
    def _normalize_ohlcv(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化OHLCV数据"""
        if df.empty:
            return df
        
        df = df.copy()
        
        # 统一列名为小写
        df.columns = [col.lower() for col in df.columns]
        
        # 确保有date列
        if 'date' not in df.columns and df.index.name == 'date':
            df = df.reset_index()
        
        # 确保date是datetime类型
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        return df


def init_data_source() -> None:
    """
    初始化默认数据源
    
    使用示例:
        from analysis_v2.data.adapter import init_data_source
        init_data_source()
    """
    from ..core.interface import DataSourceContext
    
    adapter = Jk2btDataAdapter()
    DataSourceContext.set_data_source(adapter)