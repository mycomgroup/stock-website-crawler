"""
RSRS择时信号

Resistance Support Relative Strength (阻力支撑相对强度)
"""
from typing import Optional
import pandas as pd
import numpy as np
from scipy import stats

from .base import SignalBase
from ..data.fetcher import get_ohlcv, get_index_daily


class RSSRSSignal(SignalBase):
    """
    RSRS择时信号
    
    通过线性回归计算阻力支撑相对强度，判断市场趋势
    
    原理：
    - 对N日最高价和最低价进行线性回归
    - 斜率β代表阻力支撑强度
    - β大表示支撑强于阻力（看涨）
    - β小表示阻力强于支撑（看跌）
    
    使用示例:
        signal = RSSRSSignal(window=18, threshold=0.8)
        result = signal.detect("000001.SZ")
    """
    
    name = "rsrs"
    signal_type = "timing"
    description = "RSRS阻力支撑相对强度择时信号"
    
    def __init__(
        self,
        window: int = 18,
        upper_threshold: float = 0.7,
        lower_threshold: float = -0.7,
        right_slope_threshold: float = 0.4,
        data_source=None
    ):
        super().__init__(data_source)
        self.window = window
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        self.right_slope_threshold = right_slope_threshold
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测RSRS信号"""
        need_count = self.window * 2 + 30
        df = get_ohlcv(symbol, end_date=end_date, count=need_count)
        
        if df.empty or len(df) < self.window:
            return pd.DataFrame()
        
        high = df['high']
        low = df['low']
        
        # 计算每日的β值
        betas = []
        rsquared = []
        
        for i in range(self.window, len(df)):
            high_window = high.iloc[i-self.window:i].values
            low_window = low.iloc[i-self.window:i].values
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                low_window, high_window
            )
            
            betas.append(slope)
            rsquared.append(r_value ** 2)
        
        beta_series = pd.Series(betas, index=df.index[self.window:])
        r2_series = pd.Series(rsquared, index=df.index[self.window:])
        
        # 标准化β值
        beta_mean = beta_series.rolling(window=self.window).mean()
        beta_std = beta_series.rolling(window=self.window).std()
        z_score = (beta_series - beta_mean) / beta_std
        
        # 右偏修正（考虑R²）
        right_slope = z_score * (beta_series > 0) * r2_series
        
        signals = []
        
        for i in range(self.window * 2, len(df)):
            date = df.index[i] if 'date' not in df.columns else df['date'].iloc[i]
            
            z = z_score.iloc[i]
            right = right_slope.iloc[i]
            
            if pd.isna(z) or pd.isna(right):
                continue
            
            # 看涨信号
            if z > self.upper_threshold:
                strength = min(z / 2, 1.0)
                signals.append({
                    'date': date,
                    'type': 'rsrs_buy',
                    'direction': 'buy',
                    'strength': strength,
                    'metadata': {
                        'beta': beta_series.iloc[i],
                        'z_score': z,
                        'r_squared': r2_series.iloc[i]
                    }
                })
            
            # 看跌信号
            elif z < self.lower_threshold:
                strength = min(abs(z) / 2, 1.0)
                signals.append({
                    'date': date,
                    'type': 'rsrs_sell',
                    'direction': 'sell',
                    'strength': strength,
                    'metadata': {
                        'beta': beta_series.iloc[i],
                        'z_score': z,
                        'r_squared': r2_series.iloc[i]
                    }
                })
            
            # 右偏修正信号（更强信号）
            if right > self.right_slope_threshold:
                signals.append({
                    'date': date,
                    'type': 'rsrs_right_buy',
                    'direction': 'buy',
                    'strength': 1.0,
                    'metadata': {
                        'right_slope': right,
                        'beta': beta_series.iloc[i]
                    }
                })
        
        return pd.DataFrame(signals)


class RSSRSIndexSignal(SignalBase):
    """
    RSRS指数择时信号
    
    使用指数数据而非个股数据，更适合判断大盘趋势
    
    使用示例:
        signal = RSSRSIndexSignal(index_symbol="000300.SH")
        result = signal.detect("000300.SH")
    """
    
    name = "rsrs_index"
    signal_type = "timing"
    description = "RSRS指数择时信号"
    
    def __init__(
        self,
        window: int = 18,
        upper_threshold: float = 0.7,
        lower_threshold: float = -0.7,
        data_source=None
    ):
        super().__init__(data_source)
        self.window = window
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测指数RSRS信号"""
        need_count = self.window * 2 + 30
        df = get_index_daily(symbol, end_date=end_date)
        
        if df.empty or len(df) < need_count:
            df = get_index_daily(symbol, end_date=end_date)
        
        if df.empty or len(df) < self.window:
            return pd.DataFrame()
        
        # 取最近的足够数据
        df = df.tail(need_count)
        
        high = df['high']
        low = df['low']
        
        # 计算β值序列
        betas = []
        for i in range(self.window, len(df)):
            high_window = high.iloc[i-self.window:i].values
            low_window = low.iloc[i-self.window:i].values
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                low_window, high_window
            )
            betas.append(slope)
        
        beta_series = pd.Series(betas, index=df.index[self.window:])
        
        # 标准化
        beta_mean = beta_series.rolling(window=self.window).mean()
        beta_std = beta_series.rolling(window=self.window).std()
        z_score = (beta_series - beta_mean) / beta_std
        
        signals = []
        for i in range(self.window, len(beta_series)):
            date = beta_series.index[i]
            z = z_score.iloc[i]
            
            if pd.isna(z):
                continue
            
            if z > self.upper_threshold:
                signals.append({
                    'date': date,
                    'type': 'rsrs_index_buy',
                    'direction': 'buy',
                    'strength': min(z / 2, 1.0),
                    'metadata': {'z_score': z, 'beta': beta_series.iloc[i]}
                })
            elif z < self.lower_threshold:
                signals.append({
                    'date': date,
                    'type': 'rsrs_index_sell',
                    'direction': 'sell',
                    'strength': min(abs(z) / 2, 1.0),
                    'metadata': {'z_score': z, 'beta': beta_series.iloc[i]}
                })
        
        return pd.DataFrame(signals)