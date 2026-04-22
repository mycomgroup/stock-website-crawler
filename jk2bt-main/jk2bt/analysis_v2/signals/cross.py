"""
均线交叉信号

示例信号实现，展示如何基于 core.indicators 构建
"""
from typing import Optional, Tuple
import pandas as pd

from .base import SignalBase
from ..core.indicators import ma, ema, cross_up, cross_down
from ..data.fetcher import get_ohlcv


class MACrossSignal(SignalBase):
    """
    均线交叉信号
    
    检测两条移动平均线的交叉，作为买入/卖出信号
    
    使用示例:
        signal = MACrossSignal(fast=5, slow=20)
        result = signal.detect("000001.SZ")
    """
    
    name = "ma_cross"
    signal_type = "cross"
    description = "均线交叉信号"
    
    def __init__(
        self,
        fast: int = 5,
        slow: int = 20,
        ma_type: str = "sma",
        data_source=None
    ):
        """
        Args:
            fast: 快线周期
            slow: 慢线周期
            ma_type: 移动平均类型 ("sma" 或 "ema")
            data_source: 数据源
        """
        super().__init__(data_source)
        self.fast = fast
        self.slow = slow
        self.ma_type = ma_type
    
    def detect(
        self,
        symbol: str,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """检测均线交叉信号"""
        need_count = self.slow + 10
        df = get_ohlcv(symbol, end_date=end_date, count=need_count)
        
        if df.empty or len(df) < self.slow:
            return pd.DataFrame()
        
        close = df['close']
        
        if self.ma_type == "ema":
            fast_line = ema(close, self.fast)
            slow_line = ema(close, self.slow)
        else:
            fast_line = ma(close, self.fast)
            slow_line = ma(close, self.slow)
        
        # 检测上穿和下穿
        buy_signals = cross_up(fast_line, slow_line)
        sell_signals = cross_down(fast_line, slow_line)
        
        signals = []
        for i in range(len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            
            if buy_signals.iloc[i]:
                signals.append({
                    'date': date,
                    'type': 'ma_cross_up',
                    'direction': 'buy',
                    'strength': 1.0,
                    'metadata': {
                        'fast_period': self.fast,
                        'slow_period': self.slow,
                        'fast_value': fast_line.iloc[i],
                        'slow_value': slow_line.iloc[i]
                    }
                })
            elif sell_signals.iloc[i]:
                signals.append({
                    'date': date,
                    'type': 'ma_cross_down',
                    'direction': 'sell',
                    'strength': 1.0,
                    'metadata': {
                        'fast_period': self.fast,
                        'slow_period': self.slow,
                        'fast_value': fast_line.iloc[i],
                        'slow_value': slow_line.iloc[i]
                    }
                })
        
        return pd.DataFrame(signals)


class MACDSignal(SignalBase):
    """
    MACD交叉信号
    
    检测MACD的DIF与DEA交叉
    
    使用示例:
        signal = MACDSignal(fast=12, slow=26, signal=9)
        result = signal.detect("000001.SZ")
    """
    
    name = "macd_cross"
    signal_type = "cross"
    description = "MACD交叉信号"
    
    def __init__(
        self,
        fast: int = 12,
        slow: int = 26,
        signal_period: int = 9,
        data_source=None
    ):
        super().__init__(data_source)
        self.fast = fast
        self.slow = slow
        self.signal_period = signal_period
    
    def detect(
        self,
        symbol: str,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """检测MACD交叉信号"""
        need_count = self.slow + self.signal_period + 10
        df = get_ohlcv(symbol, end_date=end_date, count=need_count)
        
        if df.empty:
            return pd.DataFrame()
        
        close = df['close']
        dif, dea, hist = macd(close, self.fast, self.slow, self.signal_period)
        
        buy_signals = cross_up(dif, dea)
        sell_signals = cross_down(dif, dea)
        
        signals = []
        for i in range(len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            
            if buy_signals.iloc[i]:
                signals.append({
                    'date': date,
                    'type': 'macd_cross_up',
                    'direction': 'buy',
                    'strength': 1.0,
                    'metadata': {
                        'dif': dif.iloc[i],
                        'dea': dea.iloc[i],
                        'hist': hist.iloc[i]
                    }
                })
            elif sell_signals.iloc[i]:
                signals.append({
                    'date': date,
                    'type': 'macd_cross_down',
                    'direction': 'sell',
                    'strength': 1.0,
                    'metadata': {
                        'dif': dif.iloc[i],
                        'dea': dea.iloc[i],
                        'hist': hist.iloc[i]
                    }
                })
        
        return pd.DataFrame(signals)


class RSISignal(SignalBase):
    """
    RSI超买超卖信号
    
    使用示例:
        signal = RSISignal(window=14, overbought=70, oversold=30)
        result = signal.detect("000001.SZ")
    """
    
    name = "rsi_signal"
    signal_type = "extreme"
    description = "RSI超买超卖信号"
    
    def __init__(
        self,
        window: int = 14,
        overbought: float = 70,
        oversold: float = 30,
        data_source=None
    ):
        super().__init__(data_source)
        self.window = window
        self.overbought = overbought
        self.oversold = oversold
    
    def detect(
        self,
        symbol: str,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """检测RSI超买超卖信号"""
        df = get_ohlcv(symbol, end_date=end_date, count=self.window + 10)
        
        if df.empty:
            return pd.DataFrame()
        
        close = df['close']
        rsi_value = rsi(close, self.window)
        
        signals = []
        for i in range(len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            rsi_val = rsi_value.iloc[i]
            
            if pd.isna(rsi_val):
                continue
            
            if rsi_val >= self.overbought:
                signals.append({
                    'date': date,
                    'type': 'rsi_overbought',
                    'direction': 'sell',
                    'strength': (rsi_val - self.overbought) / (100 - self.overbought),
                    'metadata': {'rsi': rsi_val}
                })
            elif rsi_val <= self.oversold:
                signals.append({
                    'date': date,
                    'type': 'rsi_oversold',
                    'direction': 'buy',
                    'strength': (self.oversold - rsi_val) / self.oversold,
                    'metadata': {'rsi': rsi_val}
                })
        
        return pd.DataFrame(signals)