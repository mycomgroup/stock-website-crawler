"""
极值信号

检测指标触及极值区域的信号
"""
from typing import Optional
import pandas as pd
import numpy as np

from .base import SignalBase
from ..core.indicators import kdj, wr, cci
from ..data.fetcher import get_ohlcv


class KDJSignal(SignalBase):
    """
    KDJ超买超卖信号
    
    使用示例:
        signal = KDJSignal(overbought=80, oversold=20)
        result = signal.detect("000001.SZ")
    """
    
    name = "kdj_signal"
    signal_type = "extreme"
    description = "KDJ超买超卖信号"
    
    def __init__(
        self,
        n: int = 9,
        m1: int = 3,
        m2: int = 3,
        overbought: float = 80,
        oversold: float = 20,
        data_source=None
    ):
        super().__init__(data_source)
        self.n = n
        self.m1 = m1
        self.m2 = m2
        self.overbought = overbought
        self.oversold = oversold
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测KDJ信号"""
        df = get_ohlcv(symbol, end_date=end_date, count=self.n + 10)
        
        if df.empty:
            return pd.DataFrame()
        
        k, d, j = kdj(df['high'], df['low'], df['close'], self.n, self.m1, self.m2)
        
        signals = []
        for i in range(self.n, len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            
            if pd.isna(k.iloc[i]) or pd.isna(d.iloc[i]):
                continue
            
            # K线上穿D线（金叉）
            if k.iloc[i] > d.iloc[i] and k.iloc[i-1] <= d.iloc[i-1]:
                if k.iloc[i] < self.oversold:
                    # 低位金叉，更强买入信号
                    signals.append({
                        'date': date,
                        'type': 'kdj_gold_cross_low',
                        'direction': 'buy',
                        'strength': 1.0,
                        'metadata': {'k': k.iloc[i], 'd': d.iloc[i], 'j': j.iloc[i]}
                    })
                else:
                    signals.append({
                        'date': date,
                        'type': 'kdj_gold_cross',
                        'direction': 'buy',
                        'strength': 0.6,
                        'metadata': {'k': k.iloc[i], 'd': d.iloc[i], 'j': j.iloc[i]}
                    })
            
            # K线下穿D线（死叉）
            elif k.iloc[i] < d.iloc[i] and k.iloc[i-1] >= d.iloc[i-1]:
                if k.iloc[i] > self.overbought:
                    # 高位死叉，更强卖出信号
                    signals.append({
                        'date': date,
                        'type': 'kdj_dead_cross_high',
                        'direction': 'sell',
                        'strength': 1.0,
                        'metadata': {'k': k.iloc[i], 'd': d.iloc[i], 'j': j.iloc[i]}
                    })
                else:
                    signals.append({
                        'date': date,
                        'type': 'kdj_dead_cross',
                        'direction': 'sell',
                        'strength': 0.6,
                        'metadata': {'k': k.iloc[i], 'd': d.iloc[i], 'j': j.iloc[i]}
                    })
            
            # J值超买超卖
            elif j.iloc[i] > 100:
                signals.append({
                    'date': date,
                    'type': 'kdj_j_overbought',
                    'direction': 'sell',
                    'strength': 0.8,
                    'metadata': {'k': k.iloc[i], 'd': d.iloc[i], 'j': j.iloc[i]}
                })
            elif j.iloc[i] < 0:
                signals.append({
                    'date': date,
                    'type': 'kdj_j_oversold',
                    'direction': 'buy',
                    'strength': 0.8,
                    'metadata': {'k': k.iloc[i], 'd': d.iloc[i], 'j': j.iloc[i]}
                })
        
        return pd.DataFrame(signals)


class WRSignal(SignalBase):
    """
    威廉指标信号
    
    使用示例:
        signal = WRSignal(window=14, overbought=-20, oversold=-80)
        result = signal.detect("000001.SZ")
    """
    
    name = "wr_signal"
    signal_type = "extreme"
    description = "威廉指标超买超卖信号"
    
    def __init__(
        self,
        window: int = 14,
        overbought: float = -20,
        oversold: float = -80,
        data_source=None
    ):
        super().__init__(data_source)
        self.window = window
        self.overbought = overbought  # WR值高于此为超买
        self.oversold = oversold      # WR值低于此为超卖
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测WR信号"""
        df = get_ohlcv(symbol, end_date=end_date, count=self.window + 10)
        
        if df.empty:
            return pd.DataFrame()
        
        wr_value = wr(df['high'], df['low'], df['close'], self.window)
        
        signals = []
        for i in range(self.window, len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            wr_val = wr_value.iloc[i]
            
            if pd.isna(wr_val):
                continue
            
            # 超买区域（WR > -20）
            if wr_val > self.overbought:
                signals.append({
                    'date': date,
                    'type': 'wr_overbought',
                    'direction': 'sell',
                    'strength': (wr_val - self.overbought) / (-100 - self.overbought),
                    'metadata': {'wr': wr_val}
                })
            
            # 超卖区域（WR < -80）
            elif wr_val < self.oversold:
                signals.append({
                    'date': date,
                    'type': 'wr_oversold',
                    'direction': 'buy',
                    'strength': (self.oversold - wr_val) / (self.oversold - 0),
                    'metadata': {'wr': wr_val}
                })
        
        return pd.DataFrame(signals)


class CCISignal(SignalBase):
    """
    CCI顺势指标信号
    
    使用示例:
        signal = CCISignal(window=14)
        result = signal.detect("000001.SZ")
    """
    
    name = "cci_signal"
    signal_type = "extreme"
    description = "CCI顺势指标信号"
    
    def __init__(
        self,
        window: int = 14,
        overbought: float = 100,
        oversold: float = -100,
        data_source=None
    ):
        super().__init__(data_source)
        self.window = window
        self.overbought = overbought
        self.oversold = oversold
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测CCI信号"""
        df = get_ohlcv(symbol, end_date=end_date, count=self.window + 10)
        
        if df.empty:
            return pd.DataFrame()
        
        cci_value = cci(df['high'], df['low'], df['close'], self.window)
        
        signals = []
        for i in range(self.window, len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            cci_val = cci_value.iloc[i]
            
            if pd.isna(cci_val):
                continue
            
            # CCI > 100 超买
            if cci_val > self.overbought:
                signals.append({
                    'date': date,
                    'type': 'cci_overbought',
                    'direction': 'sell',
                    'strength': min(cci_val / 200, 1.0),
                    'metadata': {'cci': cci_val}
                })
            
            # CCI < -100 超卖
            elif cci_val < self.oversold:
                signals.append({
                    'date': date,
                    'type': 'cci_oversold',
                    'direction': 'buy',
                    'strength': min(abs(cci_val) / 200, 1.0),
                    'metadata': {'cci': cci_val}
                })
        
        return pd.DataFrame(signals)