"""
突破信号

检测价格突破支撑/阻力位的信号
"""
from typing import Optional
import pandas as pd
import numpy as np

from .base import SignalBase
from ..core.indicators import hhv, llv
from ..data.fetcher import get_ohlcv


class BreakoutSignal(SignalBase):
    """
    价格突破信号
    
    检测价格突破N日最高/最低
    
    使用示例:
        signal = BreakoutSignal(window=20)
        result = signal.detect("000001.SZ")
    """
    
    name = "breakout"
    signal_type = "breakthrough"
    description = "价格突破信号"
    
    def __init__(self, window: int = 20, data_source=None):
        super().__init__(data_source)
        self.window = window
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测突破信号"""
        df = get_ohlcv(symbol, end_date=end_date, count=self.window + 10)
        
        if df.empty or len(df) < self.window:
            return pd.DataFrame()
        
        high = df['high']
        low = df['low']
        close = df['close']
        
        # N日最高最低（不包含当日）
        prev_high = hhv(high.shift(1), self.window)
        prev_low = llv(low.shift(1), self.window)
        
        signals = []
        for i in range(self.window, len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            
            # 向上突破
            if close.iloc[i] > prev_high.iloc[i]:
                signals.append({
                    'date': date,
                    'type': 'breakout_up',
                    'direction': 'buy',
                    'strength': 1.0,
                    'metadata': {
                        'breakout_level': prev_high.iloc[i],
                        'current_price': close.iloc[i],
                        'window': self.window
                    }
                })
            
            # 向下突破
            elif close.iloc[i] < prev_low.iloc[i]:
                signals.append({
                    'date': date,
                    'type': 'breakout_down',
                    'direction': 'sell',
                    'strength': 1.0,
                    'metadata': {
                        'breakout_level': prev_low.iloc[i],
                        'current_price': close.iloc[i],
                        'window': self.window
                    }
                })
        
        return pd.DataFrame(signals)


class BollingerBreakoutSignal(SignalBase):
    """
    布林带突破信号
    
    检测价格突破布林带上下轨
    
    使用示例:
        signal = BollingerBreakoutSignal(window=20, num_std=2)
        result = signal.detect("000001.SZ")
    """
    
    name = "boll_breakout"
    signal_type = "breakthrough"
    description = "布林带突破信号"
    
    def __init__(self, window: int = 20, num_std: float = 2.0, data_source=None):
        super().__init__(data_source)
        self.window = window
        self.num_std = num_std
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测布林带突破信号"""
        from ..core.indicators import boll
        
        df = get_ohlcv(symbol, end_date=end_date, count=self.window + 10)
        
        if df.empty:
            return pd.DataFrame()
        
        close = df['close']
        upper, mid, lower = boll(close, self.window, self.num_std)
        
        signals = []
        for i in range(self.window, len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            
            # 突破上轨
            if close.iloc[i] > upper.iloc[i]:
                signals.append({
                    'date': date,
                    'type': 'boll_breakout_up',
                    'direction': 'buy',
                    'strength': (close.iloc[i] - upper.iloc[i]) / upper.iloc[i],
                    'metadata': {
                        'upper': upper.iloc[i],
                        'mid': mid.iloc[i],
                        'lower': lower.iloc[i],
                        'price': close.iloc[i]
                    }
                })
            
            # 突破下轨
            elif close.iloc[i] < lower.iloc[i]:
                signals.append({
                    'date': date,
                    'type': 'boll_breakout_down',
                    'direction': 'sell',
                    'strength': (lower.iloc[i] - close.iloc[i]) / lower.iloc[i],
                    'metadata': {
                        'upper': upper.iloc[i],
                        'mid': mid.iloc[i],
                        'lower': lower.iloc[i],
                        'price': close.iloc[i]
                    }
                })
        
        return pd.DataFrame(signals)