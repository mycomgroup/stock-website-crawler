"""
技术因子

基于 core.indicators 实现的技术因子
"""
from typing import Optional
import pandas as pd
import numpy as np

from .base import FactorBase, FactorRegistry
from ..core.indicators import (
    ma, ema, macd, rsi, kdj, boll, atr, obv,
    bias, roc, momentum, adx, dmi, mfi
)
from ..data.fetcher import get_ohlcv


@FactorRegistry.register("ma_5", aliases=["MA5", "ma5"])
class MA5Factor(FactorBase):
    name = "ma_5"
    category = "technical"
    description = "5日移动平均线"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return ma(df['close'], 5)


@FactorRegistry.register("ma_10", aliases=["MA10", "ma10"])
class MA10Factor(FactorBase):
    name = "ma_10"
    category = "technical"
    description = "10日移动平均线"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return ma(df['close'], 10)


@FactorRegistry.register("ma_20", aliases=["MA20", "ma20"])
class MA20Factor(FactorBase):
    name = "ma_20"
    category = "technical"
    description = "20日移动平均线"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return ma(df['close'], 20)


@FactorRegistry.register("ema_12", aliases=["EMA12", "ema12"])
class EMA12Factor(FactorBase):
    name = "ema_12"
    category = "technical"
    description = "12日指数移动平均线"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return ema(df['close'], 12)


@FactorRegistry.register("ema_26", aliases=["EMA26", "ema26"])
class EMA26Factor(FactorBase):
    name = "ema_26"
    category = "technical"
    description = "26日指数移动平均线"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return ema(df['close'], 26)


@FactorRegistry.register("macd", aliases=["MACD"])
class MACDFactor(FactorBase):
    name = "macd"
    category = "technical"
    description = "MACD指标"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.DataFrame:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.DataFrame()
        
        dif, dea, hist = macd(df['close'])
        return pd.DataFrame({
            'macd_dif': dif,
            'macd_dea': dea,
            'macd_hist': hist
        })


@FactorRegistry.register("rsi_6", aliases=["RSI6", "rsi6"])
class RSI6Factor(FactorBase):
    name = "rsi_6"
    category = "technical"
    description = "6日RSI"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return rsi(df['close'], 6)


@FactorRegistry.register("rsi_14", aliases=["RSI14", "rsi14"])
class RSI14Factor(FactorBase):
    name = "rsi_14"
    category = "technical"
    description = "14日RSI"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return rsi(df['close'], 14)


@FactorRegistry.register("kdj", aliases=["KDJ"])
class KDJFactor(FactorBase):
    name = "kdj"
    category = "technical"
    description = "KDJ指标"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.DataFrame:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.DataFrame()
        
        k, d, j = kdj(df['high'], df['low'], df['close'])
        return pd.DataFrame({
            'kdj_k': k,
            'kdj_d': d,
            'kdj_j': j
        })


@FactorRegistry.register("boll", aliases=["BOLL"])
class BollFactor(FactorBase):
    name = "boll"
    category = "technical"
    description = "布林带"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.DataFrame:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.DataFrame()
        
        upper, mid, lower = boll(df['close'])
        return pd.DataFrame({
            'boll_upper': upper,
            'boll_mid': mid,
            'boll_lower': lower
        })


@FactorRegistry.register("atr_14", aliases=["ATR14", "atr14"])
class ATR14Factor(FactorBase):
    name = "atr_14"
    category = "technical"
    description = "14日平均真实波幅"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return atr(df['high'], df['low'], df['close'], 14)


@FactorRegistry.register("bias_6", aliases=["BIAS6", "bias6"])
class BIAS6Factor(FactorBase):
    name = "bias_6"
    category = "technical"
    description = "6日乖离率"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return bias(df['close'], 6)


@FactorRegistry.register("bias_12", aliases=["BIAS12", "bias12"])
class BIAS12Factor(FactorBase):
    name = "bias_12"
    category = "technical"
    description = "12日乖离率"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return bias(df['close'], 12)


@FactorRegistry.register("bias_24", aliases=["BIAS24", "bias24"])
class BIAS24Factor(FactorBase):
    name = "bias_24"
    category = "technical"
    description = "24日乖离率"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return bias(df['close'], 24)


@FactorRegistry.register("roc_12", aliases=["ROC12", "roc12"])
class ROC12Factor(FactorBase):
    name = "roc_12"
    category = "technical"
    description = "12日变动率"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return roc(df['close'], 12)


@FactorRegistry.register("momentum_10", aliases=["MOM10", "mom10"])
class Momentum10Factor(FactorBase):
    name = "momentum_10"
    category = "technical"
    description = "10日动量"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return momentum(df['close'], 10)


@FactorRegistry.register("obv", aliases=["OBV"])
class OBVFactor(FactorBase):
    name = "obv"
    category = "technical"
    description = "能量潮指标"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return obv(df['close'], df['volume'])


@FactorRegistry.register("volatility_20", aliases=["VOL20", "vol20"])
class Volatility20Factor(FactorBase):
    name = "volatility_20"
    category = "technical"
    description = "20日历史波动率"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        
        returns = df['close'].pct_change()
        vol = returns.rolling(window=20).std() * np.sqrt(252)
        return vol


@FactorRegistry.register("adx_14", aliases=["ADX14", "adx14"])
class ADX14Factor(FactorBase):
    name = "adx_14"
    category = "technical"
    description = "14日平均趋向指标"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.DataFrame:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.DataFrame()
        
        adx_val, plus_di, minus_di = adx(df['high'], df['low'], df['close'], 14)
        return pd.DataFrame({
            'adx': adx_val,
            'plus_di': plus_di,
            'minus_di': minus_di
        })


@FactorRegistry.register("mfi_14", aliases=["MFI14", "mfi14"])
class MFI14Factor(FactorBase):
    name = "mfi_14"
    category = "technical"
    description = "14日资金流量指标"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return mfi(df['high'], df['low'], df['close'], df['volume'], 14)