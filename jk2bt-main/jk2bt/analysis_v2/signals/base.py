"""
信号检测基类
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import pandas as pd

from ..core.interface import DataSource


class SignalBase(ABC):
    """
    信号基类
    
    所有信号都应继承此类并实现 detect 方法。
    
    使用示例:
        class MACrossSignal(SignalBase):
            name = "ma_cross"
            signal_type = "cross"
            description = "均线交叉信号"
            
            def __init__(self, fast=5, slow=20, data_source=None):
                super().__init__(data_source)
                self.fast = fast
                self.slow = slow
            
            def detect(self, symbol, end_date=None):
                from ..data.fetcher import get_ohlcv
                from ..core.indicators import ma, cross_up, cross_down
                
                df = get_ohlcv(symbol, end_date=end_date, count=self.slow + 10)
                fast_ma = ma(df['close'], self.fast)
                slow_ma = ma(df['close'], self.slow)
                
                buy_signals = cross_up(fast_ma, slow_ma)
                sell_signals = cross_down(fast_ma, slow_ma)
                ...
    """
    
    name: str = ""
    signal_type: str = ""
    description: str = ""
    
    def __init__(self, data_source: Optional[DataSource] = None):
        """
        初始化信号
        
        Args:
            data_source: 数据源（可选，用于依赖注入）
        """
        self._data_source = data_source
    
    @abstractmethod
    def detect(
        self,
        symbol: str,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        检测信号
        
        Args:
            symbol: 股票代码
            end_date: 结束日期
        
        Returns:
            信号DataFrame，包含列: date, type, direction, strength, metadata
        """
        pass
    
    @property
    def data_source(self) -> DataSource:
        """获取数据源"""
        if self._data_source is None:
            from ..core.interface import DataSourceContext
            return DataSourceContext.get_data_source()
        return self._data_source


class SignalDetector:
    """
    信号检测器
    
    管理多个信号的检测。
    
    使用示例:
        detector = SignalDetector()
        detector.register(MACrossSignal(fast=5, slow=20))
        detector.register(RSISignal(overbought=70, oversold=30))
        
        signals = detector.detect("ma_cross", "000001.SZ")
        all_signals = detector.detect_all("000001.SZ")
    """
    
    def __init__(self):
        self._signals: Dict[str, SignalBase] = {}
    
    def register(self, signal: SignalBase) -> None:
        """
        注册信号
        
        Args:
            signal: 信号实例
        """
        self._signals[signal.name] = signal
    
    def unregister(self, name: str) -> None:
        """取消注册信号"""
        self._signals.pop(name, None)
    
    def detect(
        self,
        signal_name: str,
        symbol: str,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        检测指定信号
        
        Args:
            signal_name: 信号名称
            symbol: 股票代码
            end_date: 结束日期
        
        Returns:
            信号DataFrame
        """
        signal = self._signals.get(signal_name)
        if signal is None:
            raise ValueError(f"Unknown signal: {signal_name}")
        return signal.detect(symbol, end_date)
    
    def detect_all(
        self,
        symbol: str,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        检测所有已注册的信号
        
        Args:
            symbol: 股票代码
            end_date: 结束日期
        
        Returns:
            所有信号合并后的DataFrame
        """
        results = []
        for name, signal in self._signals.items():
            try:
                df = signal.detect(symbol, end_date)
                if not df.empty:
                    df['signal_name'] = name
                    results.append(df)
            except Exception:
                pass
        
        if results:
            return pd.concat(results, ignore_index=True)
        return pd.DataFrame()
    
    def list_signals(self) -> List[str]:
        """列出所有已注册的信号"""
        return list(self._signals.keys())