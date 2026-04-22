"""
背离信号

检测价格与指标之间的背离
"""
from typing import Optional, Tuple
import pandas as pd
import numpy as np

from .base import SignalBase
from ..core.indicators import rsi, macd
from ..data.fetcher import get_ohlcv


def _find_local_extrema(series: pd.Series, window: int = 5) -> Tuple[pd.Series, pd.Series]:
    """
    找局部极值点
    
    Args:
        series: 数据序列
        window: 判断窗口
    
    Returns:
        (局部高点, 局部低点) 布尔序列
    """
    local_high = pd.Series(False, index=series.index)
    local_low = pd.Series(False, index=series.index)
    
    for i in range(window, len(series) - window):
        # 局部高点：比前后window个点都高
        if series.iloc[i] >= series.iloc[i-window:i].max() and \
           series.iloc[i] >= series.iloc[i+1:i+window+1].max():
            local_high.iloc[i] = True
        
        # 局部低点：比前后window个点都低
        if series.iloc[i] <= series.iloc[i-window:i].min() and \
           series.iloc[i] <= series.iloc[i+1:i+window+1].min():
            local_low.iloc[i] = True
    
    return local_high, local_low


class RSIDivergenceSignal(SignalBase):
    """
    RSI背离信号
    
    检测价格与RSI之间的背离：
    - 顶背离：价格创新高，RSI未创新高 → 卖出信号
    - 底背离：价格创新低，RSI未创新低 → 买入信号
    
    使用示例:
        signal = RSIDivergenceSignal(window=14, lookback=30)
        result = signal.detect("000001.SZ")
    """
    
    name = "rsi_divergence"
    signal_type = "divergence"
    description = "RSI背离信号"
    
    def __init__(self, window: int = 14, lookback: int = 30, data_source=None):
        super().__init__(data_source)
        self.window = window
        self.lookback = lookback
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测RSI背离信号"""
        df = get_ohlcv(symbol, end_date=end_date, count=self.lookback + self.window + 10)
        
        if df.empty:
            return pd.DataFrame()
        
        close = df['close']
        rsi_value = rsi(close, self.window)
        
        # 找局部极值
        price_high, price_low = _find_local_extrema(close, window=5)
        rsi_high, rsi_low = _find_local_extrema(rsi_value, window=5)
        
        signals = []
        
        # 检测顶背离
        high_indices = price_high[price_high].index
        if len(high_indices) >= 2:
            last_high_idx = high_indices[-1]
            prev_high_idx = high_indices[-2]
            
            # 价格创新高但RSI未创新高
            if close.loc[last_high_idx] > close.loc[prev_high_idx] and \
               rsi_value.loc[last_high_idx] < rsi_value.loc[prev_high_idx]:
                signals.append({
                    'date': last_high_idx if 'date' not in df.columns else df['date'].loc[last_high_idx],
                    'type': 'rsi_top_divergence',
                    'direction': 'sell',
                    'strength': 0.8,
                    'metadata': {
                        'price_high_1': close.loc[prev_high_idx],
                        'price_high_2': close.loc[last_high_idx],
                        'rsi_high_1': rsi_value.loc[prev_high_idx],
                        'rsi_high_2': rsi_value.loc[last_high_idx]
                    }
                })
        
        # 检测底背离
        low_indices = price_low[price_low].index
        if len(low_indices) >= 2:
            last_low_idx = low_indices[-1]
            prev_low_idx = low_indices[-2]
            
            # 价格创新低但RSI未创新低
            if close.loc[last_low_idx] < close.loc[prev_low_idx] and \
               rsi_value.loc[last_low_idx] > rsi_value.loc[prev_low_idx]:
                signals.append({
                    'date': last_low_idx if 'date' not in df.columns else df['date'].loc[last_low_idx],
                    'type': 'rsi_bottom_divergence',
                    'direction': 'buy',
                    'strength': 0.8,
                    'metadata': {
                        'price_low_1': close.loc[prev_low_idx],
                        'price_low_2': close.loc[last_low_idx],
                        'rsi_low_1': rsi_value.loc[prev_low_idx],
                        'rsi_low_2': rsi_value.loc[last_low_idx]
                    }
                })
        
        return pd.DataFrame(signals)


class MACDDivergenceSignal(SignalBase):
    """
    MACD背离信号
    
    检测价格与MACD柱之间的背离
    
    使用示例:
        signal = MACDDivergenceSignal()
        result = signal.detect("000001.SZ")
    """
    
    name = "macd_divergence"
    signal_type = "divergence"
    description = "MACD背离信号"
    
    def __init__(self, lookback: int = 30, data_source=None):
        super().__init__(data_source)
        self.lookback = lookback
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测MACD背离信号"""
        df = get_ohlcv(symbol, end_date=end_date, count=self.lookback + 50)
        
        if df.empty:
            return pd.DataFrame()
        
        close = df['close']
        dif, dea, hist = macd(close)
        
        # 找局部极值
        price_high, price_low = _find_local_extrema(close, window=5)
        hist_high, hist_low = _find_local_extrema(hist, window=5)
        
        signals = []
        
        # 检测顶背离（价格新高，MACD柱未新高）
        high_indices = price_high[price_high].index
        if len(high_indices) >= 2:
            last_high_idx = high_indices[-1]
            prev_high_idx = high_indices[-2]
            
            if close.loc[last_high_idx] > close.loc[prev_high_idx] and \
               hist.loc[last_high_idx] < hist.loc[prev_high_idx]:
                signals.append({
                    'date': last_high_idx if 'date' not in df.columns else df['date'].loc[last_high_idx],
                    'type': 'macd_top_divergence',
                    'direction': 'sell',
                    'strength': 0.8,
                    'metadata': {
                        'hist_1': hist.loc[prev_high_idx],
                        'hist_2': hist.loc[last_high_idx]
                    }
                })
        
        # 检测底背离（价格新低，MACD柱未新低）
        low_indices = price_low[price_low].index
        if len(low_indices) >= 2:
            last_low_idx = low_indices[-1]
            prev_low_idx = low_indices[-2]
            
            if close.loc[last_low_idx] < close.loc[prev_low_idx] and \
               hist.loc[last_low_idx] > hist.loc[prev_low_idx]:
                signals.append({
                    'date': last_low_idx if 'date' not in df.columns else df['date'].loc[last_low_idx],
                    'type': 'macd_bottom_divergence',
                    'direction': 'buy',
                    'strength': 0.8,
                    'metadata': {
                        'hist_1': hist.loc[prev_low_idx],
                        'hist_2': hist.loc[last_low_idx]
                    }
                })
        
        return pd.DataFrame(signals)