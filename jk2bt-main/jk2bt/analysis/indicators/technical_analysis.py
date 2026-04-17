"""
technical_analysis - 综合技术指标模块

提供50+技术指标计算，涵盖：
- 趋势指标: MA, EMA, SMA, WMA, MACD, DMI, SAR
- 动量指标: RSI, KDJ, CCI, WR, ROC, MTM
- 波动率指标: BOLL, ATR, STD, VR
- 成交量指标: OBV, VR, EMV, WVAD
- 能量指标: BRAR, CR, PSY
- 压力/支撑: BBI, TRIX, DMA, EXPMA

所有函数遵循聚宽风格接口，支持单标的/多标的输入
"""

import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional
import warnings


def _get_price_data(
    security: str,
    check_date: Optional[str] = None,
    count: int = 250,
    unit: str = "1d",
    include_now: bool = True,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """获取历史价格数据"""
    from jk2bt.api.market import history

    if fields is None:
        fields = ["open", "high", "low", "close", "volume"]

    df = history(
        count=count,
        unit=unit,
        field=",".join(fields),
        security_list=[security],
        end_dt=check_date,
        include_now=include_now,
    )
    return df


def _process_result(
    security: Union[str, List[str]],
    values: Dict[str, float],
    single_value: bool = False,
) -> Union[float, Dict[str, float], Dict[str, Dict[str, float]]]:
    """处理返回结果格式"""
    if isinstance(security, str):
        if single_value:
            return values.get(security, np.nan)
        return values
    return values


def MA(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 5,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算简单移动平均线 (Moving Average)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认5
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
        single = True
    else:
        securities = security
        single = False

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            ma = close.rolling(window=timeperiod, min_periods=timeperiod).mean()
            if check_date:
                result[sec] = float(ma.iloc[-1])
            else:
                result[sec] = ma
        except Exception as e:
            warnings.warn(f"MA计算失败 {sec}: {e}")
            result[sec] = np.nan

    if single and check_date:
        return result.get(security, np.nan)
    if single and not check_date:
        val = result.get(security)
        return val if val is not None else pd.Series(dtype=float)
    return result


def EMA(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 12,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算指数移动平均线 (Exponential Moving Average)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认12
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
        single = True
    else:
        securities = security
        single = False

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            ema = close.ewm(span=timeperiod, adjust=False).mean()
            if check_date:
                result[sec] = float(ema.iloc[-1])
            else:
                result[sec] = ema
        except Exception as e:
            warnings.warn(f"EMA计算失败 {sec}: {e}")
            result[sec] = np.nan

    if single and check_date:
        return result.get(security, np.nan)
    if single and not check_date:
        val = result.get(security)
        return val if val is not None else pd.Series(dtype=float)
    return result


def SMA(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 5,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算简单移动平均 (Simple Moving Average)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认5
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    return MA(security, check_date, timeperiod, unit, include_now)


def WMA(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 10,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算加权移动平均 (Weighted Moving Average)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认10
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
        single = True
    else:
        securities = security
        single = False

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            weights = np.arange(1, timeperiod + 1)

            def weighted_avg(window):
                return np.dot(window, weights) / weights.sum()

            wma = close.rolling(window=timeperiod, min_periods=timeperiod).apply(
                weighted_avg, raw=True
            )
            if check_date:
                result[sec] = float(wma.iloc[-1])
            else:
                result[sec] = wma
        except Exception as e:
            warnings.warn(f"WMA计算失败 {sec}: {e}")
            result[sec] = np.nan

    if single and check_date:
        return result.get(security, np.nan)
    if single and not check_date:
        val = result.get(security)
        return val if val is not None else pd.Series(dtype=float)
    return result


def MACD(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    SHORT: int = 12,
    LONG: int = 26,
    MID: int = 9,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算MACD指标

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        SHORT: 短期EMA周期，默认12
        LONG: 长期EMA周期，默认26
        MID: DEA周期，默认9
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {'DIFF': {股票: 值}, 'DEA': {股票: 值}, 'MACD': {股票: 值}}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"DIFF": {}, "DEA": {}, "MACD": {}}
    need_count = LONG + MID + 10

    for sec in securities:
        try:
            df = history(
                count=need_count,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < LONG:
                result["DIFF"][sec] = np.nan
                result["DEA"][sec] = np.nan
                result["MACD"][sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            ema_short = close.ewm(span=SHORT, adjust=False).mean()
            ema_long = close.ewm(span=LONG, adjust=False).mean()
            diff = ema_short - ema_long
            dea = diff.ewm(span=MID, adjust=False).mean()
            macd = 2 * (diff - dea)
            result["DIFF"][sec] = float(diff.iloc[-1])
            result["DEA"][sec] = float(dea.iloc[-1])
            result["MACD"][sec] = float(macd.iloc[-1])
        except Exception as e:
            warnings.warn(f"MACD计算失败 {sec}: {e}")
            result["DIFF"][sec] = np.nan
            result["DEA"][sec] = np.nan
            result["MACD"][sec] = np.nan

    return result


def DMI(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    N: int = 14,
    M: int = 6,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算趋向指标 (Directional Movement Index)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        N: 计算周期，默认14
        M: ADX平滑周期，默认6
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {'PDI': {...}, 'MDI': {...}, 'ADX': {...}, 'ADXR': {...}}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"PDI": {}, "MDI": {}, "ADX": {}, "ADXR": {}}

    for sec in securities:
        try:
            df = history(
                count=N + M + 20,
                unit=unit,
                field="open,high,low,close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < N + M:
                for k in result:
                    result[k][sec] = np.nan
                continue

            high = df["high"] if "high" in df.columns else df.iloc[:, 1]
            low = df["low"] if "low" in df.columns else df.iloc[:, 2]
            close = df["close"] if "close" in df.columns else df.iloc[:, 3]

            high_diff = high.diff()
            low_diff = -low.diff()

            plus_dm = high_diff.where((high_diff > low_diff) & (high_diff > 0), 0)
            minus_dm = low_diff.where((low_diff > high_diff) & (low_diff > 0), 0)

            atr = pd.concat(
                [high - low, abs(high - close.shift(1)), abs(low - close.shift(1))],
                axis=1,
            ).max(axis=1)

            plus_dm_smooth = plus_dm.ewm(span=N, adjust=False).mean()
            minus_dm_smooth = minus_dm.ewm(span=N, adjust=False).mean()
            atr_smooth = atr.ewm(span=N, adjust=False).mean()

            pdi = 100 * plus_dm_smooth / atr_smooth
            mdi = 100 * minus_dm_smooth / atr_smooth

            dx = 100 * abs(pdi - mdi) / (pdi + mdi)
            adx = dx.ewm(span=M, adjust=False).mean()
            adxr = (adx + adx.shift(M)) / 2

            result["PDI"][sec] = float(pdi.iloc[-1])
            result["MDI"][sec] = float(mdi.iloc[-1])
            result["ADX"][sec] = float(adx.iloc[-1])
            result["ADXR"][sec] = float(adxr.iloc[-1])
        except Exception as e:
            warnings.warn(f"DMI计算失败 {sec}: {e}")
            for k in result:
                result[k][sec] = np.nan

    return result


def SAR(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 4,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算抛物线转向指标 (Parabolic SAR)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 加速因子步长，默认4
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: SAR值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    af_step = timeperiod / 100.0
    af_max = 0.2

    for sec in securities:
        try:
            df = history(
                count=50,
                unit=unit,
                field="high,low",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < 10:
                result[sec] = np.nan
                continue

            high = df["high"].values if "high" in df.columns else df.iloc[:, 0].values
            low = df["low"].values if "low" in df.columns else df.iloc[:, 1].values

            is_long = high[-1] > high[-2]
            ep = high[0] if is_long else low[0]
            sar = low[0] if is_long else high[0]
            af = af_step

            for i in range(1, len(high)):
                sar = sar + af * (ep - sar)
                if is_long:
                    if low[i] < sar:
                        is_long = False
                        sar = ep
                        ep = low[i]
                        af = af_step
                    else:
                        if high[i] > ep:
                            ep = high[i]
                            af = min(af + af_step, af_max)
                        if low[i] < sar:
                            sar = low[i]
                else:
                    if high[i] > sar:
                        is_long = True
                        sar = ep
                        ep = high[i]
                        af = af_step
                    else:
                        if low[i] < ep:
                            ep = low[i]
                            af = min(af + af_step, af_max)
                        if high[i] > sar:
                            sar = high[i]

            result[sec] = float(sar)
        except Exception as e:
            warnings.warn(f"SAR计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def RSI(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 6,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算相对强弱指标 (Relative Strength Index)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认6
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
        single = True
    else:
        securities = security
        single = False

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 20,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod + 1:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            delta = close.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.ewm(alpha=1 / timeperiod, adjust=False).mean()
            avg_loss = loss.ewm(alpha=1 / timeperiod, adjust=False).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            if check_date:
                result[sec] = float(rsi.iloc[-1])
            else:
                result[sec] = rsi
        except Exception as e:
            warnings.warn(f"RSI计算失败 {sec}: {e}")
            result[sec] = np.nan

    if single and check_date:
        return result.get(security, np.nan)
    if single and not check_date:
        val = result.get(security)
        return val if val is not None else pd.Series(dtype=float)
    return result


def KDJ(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    N: int = 9,
    M1: int = 3,
    M2: int = 3,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算随机指标 (Stochastic Oscillator)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        N: RSV周期，默认9
        M1: K值平滑周期，默认3
        M2: D值平滑周期，默认3
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {'K': {...}, 'D': {...}, 'J': {...}}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"K": {}, "D": {}, "J": {}}
    need_count = N + M1 + M2 + 10

    for sec in securities:
        try:
            df = history(
                count=need_count,
                unit=unit,
                field="high,low,close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < N:
                for k in result:
                    result[k][sec] = np.nan
                continue

            high = df["high"] if "high" in df.columns else df.iloc[:, 0]
            low = df["low"] if "low" in df.columns else df.iloc[:, 1]
            close = df["close"] if "close" in df.columns else df.iloc[:, 2]

            lowest_low = low.rolling(window=N, min_periods=N).min()
            highest_high = high.rolling(window=N, min_periods=N).max()
            rsv = (close - lowest_low) / (highest_high - lowest_low) * 100
            rsv = rsv.fillna(50)

            k = rsv.ewm(alpha=1 / M1, adjust=False).mean()
            d = k.ewm(alpha=1 / M2, adjust=False).mean()
            j = 3 * k - 2 * d

            result["K"][sec] = float(k.iloc[-1])
            result["D"][sec] = float(d.iloc[-1])
            result["J"][sec] = float(j.iloc[-1])
        except Exception as e:
            warnings.warn(f"KDJ计算失败 {sec}: {e}")
            for k in result:
                result[k][sec] = np.nan

    return result


def CCI(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 14,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算顺势指标 (Commodity Channel Index)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认14
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: CCI值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="high,low,close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue

            high = df["high"] if "high" in df.columns else df.iloc[:, 0]
            low = df["low"] if "low" in df.columns else df.iloc[:, 1]
            close = df["close"] if "close" in df.columns else df.iloc[:, 2]

            tp = (high + low + close) / 3
            ma = tp.rolling(window=timeperiod, min_periods=timeperiod).mean()
            md = tp.rolling(window=timeperiod, min_periods=timeperiod).apply(
                lambda x: np.abs(x - x.mean()).mean(), raw=False
            )
            cci = (tp - ma) / (0.015 * md)
            result[sec] = float(cci.iloc[-1])
        except Exception as e:
            warnings.warn(f"CCI计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def WR(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    N: int = 14,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算威廉指标 (Williams %R)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        N: 计算周期，默认14
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: WR值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=N + 10,
                unit=unit,
                field="high,low,close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < N:
                result[sec] = np.nan
                continue

            high = df["high"] if "high" in df.columns else df.iloc[:, 0]
            low = df["low"] if "low" in df.columns else df.iloc[:, 1]
            close = df["close"] if "close" in df.columns else df.iloc[:, 2]

            highest_high = high.rolling(window=N, min_periods=N).max()
            lowest_low = low.rolling(window=N, min_periods=N).min()
            wr = -100 * (highest_high - close) / (highest_high - lowest_low)
            result[sec] = float(wr.iloc[-1])
        except Exception as e:
            warnings.warn(f"WR计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def ROC(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 12,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算变动率指标 (Rate of Change)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认12
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: ROC值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            roc = (close - close.shift(timeperiod)) / close.shift(timeperiod) * 100
            result[sec] = float(roc.iloc[-1])
        except Exception as e:
            warnings.warn(f"ROC计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def MTM(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 12,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算动量指标 (Momentum)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认12
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: MTM值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            mtm = close - close.shift(timeperiod)
            result[sec] = float(mtm.iloc[-1])
        except Exception as e:
            warnings.warn(f"MTM计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def BOLL(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 20,
    nbdevup: int = 2,
    nbdevdn: int = 2,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算布林带指标 (Bollinger Bands)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认20
        nbdevup: 上轨标准差倍数，默认2
        nbdevdn: 下轨标准差倍数，默认2
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {'UPPER': {...}, 'MID': {...}, 'LOWER': {...}}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"UPPER": {}, "MID": {}, "LOWER": {}}

    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                for k in result:
                    result[k][sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            mid = close.rolling(window=timeperiod, min_periods=timeperiod).mean()
            std = close.rolling(window=timeperiod, min_periods=timeperiod).std()
            upper = mid + nbdevup * std
            lower = mid - nbdevdn * std
            result["UPPER"][sec] = float(upper.iloc[-1])
            result["MID"][sec] = float(mid.iloc[-1])
            result["LOWER"][sec] = float(lower.iloc[-1])
        except Exception as e:
            warnings.warn(f"BOLL计算失败 {sec}: {e}")
            for k in result:
                result[k][sec] = np.nan

    return result


def ATR(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 14,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算平均真实波幅 (Average True Range)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认14
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: ATR值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 20,
                unit=unit,
                field="high,low,close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod + 1:
                result[sec] = np.nan
                continue

            high = df["high"] if "high" in df.columns else df.iloc[:, 0]
            low = df["low"] if "low" in df.columns else df.iloc[:, 1]
            close = df["close"] if "close" in df.columns else df.iloc[:, 2]

            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=timeperiod, min_periods=timeperiod).mean()
            result[sec] = float(atr.iloc[-1])
        except Exception as e:
            warnings.warn(f"ATR计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def STD(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 20,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算标准差指标 (Standard Deviation)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认20
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
        single = True
    else:
        securities = security
        single = False

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            std = close.rolling(window=timeperiod, min_periods=timeperiod).std()
            if check_date:
                result[sec] = float(std.iloc[-1])
            else:
                result[sec] = std
        except Exception as e:
            warnings.warn(f"STD计算失败 {sec}: {e}")
            result[sec] = np.nan

    if single and check_date:
        return result.get(security, np.nan)
    if single and not check_date:
        val = result.get(security)
        return val if val is not None else pd.Series(dtype=float)
    return result


def VR(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 26,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算成交量比率指标 (Volume Ratio)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认26
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: VR值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close,volume",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue

            close = df["close"] if "close" in df.columns else df.iloc[:, 0]
            volume = df["volume"] if "volume" in df.columns else df.iloc[:, 1]

            up_vol = volume.where(close > close.shift(1), 0)
            down_vol = volume.where(close < close.shift(1), 0)
            flat_vol = volume.where(close == close.shift(1), 0)

            av = up_vol.rolling(window=timeperiod, min_periods=timeperiod).sum()
            bv = down_vol.rolling(window=timeperiod, min_periods=timeperiod).sum()
            cv = flat_vol.rolling(window=timeperiod, min_periods=timeperiod).sum()

            vr = (av + cv / 2) / (bv + cv / 2) * 100
            result[sec] = float(vr.iloc[-1])
        except Exception as e:
            warnings.warn(f"VR计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def OBV(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 30,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算能量潮指标 (On Balance Volume)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期（用于MA平滑），默认30
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
        single = True
    else:
        securities = security
        single = False

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 30,
                unit=unit,
                field="close,volume",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < 2:
                result[sec] = np.nan
                continue

            close = df["close"] if "close" in df.columns else df.iloc[:, 0]
            volume = df["volume"] if "volume" in df.columns else df.iloc[:, 1]

            sign = np.sign(close - close.shift(1)).fillna(0)
            obv = (sign * volume).cumsum()

            if check_date:
                result[sec] = float(obv.iloc[-1])
            else:
                result[sec] = obv
        except Exception as e:
            warnings.warn(f"OBV计算失败 {sec}: {e}")
            result[sec] = np.nan

    if single and check_date:
        return result.get(security, np.nan)
    if single and not check_date:
        val = result.get(security)
        return val if val is not None else pd.Series(dtype=float)
    return result


def EMV(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 14,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算简易波动指标 (Ease of Movement Value)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认14
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: EMV值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 20,
                unit=unit,
                field="high,low,volume",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod + 1:
                result[sec] = np.nan
                continue

            high = df["high"] if "high" in df.columns else df.iloc[:, 0]
            low = df["low"] if "low" in df.columns else df.iloc[:, 1]
            volume = df["volume"] if "volume" in df.columns else df.iloc[:, 2]

            a = (high + low) / 2 - (high.shift(1) + low.shift(1)) / 2
            b = volume / 10000 / (high - low)
            emv = a / b
            emv_ma = emv.rolling(window=timeperiod, min_periods=timeperiod).mean()
            result[sec] = float(emv_ma.iloc[-1])
        except Exception as e:
            warnings.warn(f"EMV计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def WVAD(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 24,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算威廉变异离散量 (Williams Variable Accumulation Distribution)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认24
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: WVAD值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="open,high,low,close,volume",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue

            open_ = df["open"] if "open" in df.columns else df.iloc[:, 0]
            high = df["high"] if "high" in df.columns else df.iloc[:, 1]
            low = df["low"] if "low" in df.columns else df.iloc[:, 2]
            close = df["close"] if "close" in df.columns else df.iloc[:, 3]
            volume = df["volume"] if "volume" in df.columns else df.iloc[:, 4]

            wvad = (close - open_) / (high - low) * volume
            wvad_sum = wvad.rolling(window=timeperiod, min_periods=timeperiod).sum()
            result[sec] = float(wvad_sum.iloc[-1])
        except Exception as e:
            warnings.warn(f"WVAD计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def BRAR(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 26,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算情绪指标 (BR and AR)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认26
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {'BR': {...}, 'AR': {...}}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"BR": {}, "AR": {}}

    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="open,high,low,close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod + 1:
                result["BR"][sec] = np.nan
                result["AR"][sec] = np.nan
                continue

            open_ = df["open"] if "open" in df.columns else df.iloc[:, 0]
            high = df["high"] if "high" in df.columns else df.iloc[:, 1]
            low = df["low"] if "low" in df.columns else df.iloc[:, 2]
            prev_close = open_.shift(1)

            br_numerator = (high - prev_close).clip(lower=0)
            br_denominator = (prev_close - low).clip(lower=0)
            ar_numerator = high - open_
            ar_denominator = (open_ - low).clip(lower=0.0001)

            br = (
                br_numerator.rolling(window=timeperiod, min_periods=timeperiod).sum()
                / br_denominator.rolling(
                    window=timeperiod, min_periods=timeperiod
                ).sum()
                * 100
            )
            ar = (
                ar_numerator.rolling(window=timeperiod, min_periods=timeperiod).sum()
                / ar_denominator.rolling(
                    window=timeperiod, min_periods=timeperiod
                ).sum()
                * 100
            )

            result["BR"][sec] = float(br.iloc[-1])
            result["AR"][sec] = float(ar.iloc[-1])
        except Exception as e:
            warnings.warn(f"BRAR计算失败 {sec}: {e}")
            result["BR"][sec] = np.nan
            result["AR"][sec] = np.nan

    return result


def CR(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 26,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算能量指标 (Energy Indicator)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认26
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: CR值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="high,low,close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod + 1:
                result[sec] = np.nan
                continue

            high = df["high"] if "high" in df.columns else df.iloc[:, 0]
            low = df["low"] if "low" in df.columns else df.iloc[:, 1]
            prev_mid = (high.shift(1) + low.shift(1)) / 2

            up = (high - prev_mid).clip(lower=0)
            down = (prev_mid - low).clip(lower=0)

            cr = (
                up.rolling(window=timeperiod, min_periods=timeperiod).sum()
                / down.rolling(window=timeperiod, min_periods=timeperiod).sum()
                * 100
            )
            result[sec] = float(cr.iloc[-1])
        except Exception as e:
            warnings.warn(f"CR计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def PSY(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 12,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float]]:
    """
    计算心理线指标 (Psychological Line)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认12
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {股票: PSY值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod + 1:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            up = (close > close.shift(1)).astype(int)
            psy = (
                up.rolling(window=timeperiod, min_periods=timeperiod).sum()
                / (timeperiod)
                * 100
            )
            result[sec] = float(psy.iloc[-1])
        except Exception as e:
            warnings.warn(f"PSY计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def BBI(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算多空指标 (Bull Bear Index)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
        single = True
    else:
        securities = security
        single = False

    result = {}
    periods = [3, 6, 12, 24]

    for sec in securities:
        try:
            df = history(
                count=30,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < 24:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            ma3 = close.rolling(window=3, min_periods=3).mean()
            ma6 = close.rolling(window=6, min_periods=6).mean()
            ma12 = close.rolling(window=12, min_periods=12).mean()
            ma24 = close.rolling(window=24, min_periods=24).mean()
            bbi = (ma3 + ma6 + ma12 + ma24) / 4
            if check_date:
                result[sec] = float(bbi.iloc[-1])
            else:
                result[sec] = bbi
        except Exception as e:
            warnings.warn(f"BBI计算失败 {sec}: {e}")
            result[sec] = np.nan

    if single and check_date:
        return result.get(security, np.nan)
    if single and not check_date:
        val = result.get(security)
        return val if val is not None else pd.Series(dtype=float)
    return result


def TRIX(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 12,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算三重指数平滑平均线 (Triple Exponential Average)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认12
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
        single = True
    else:
        securities = security
        single = False

    result = {}
    for sec in securities:
        try:
            df = history(
                count=timeperiod * 3 + 20,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < timeperiod * 3:
                result[sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            ema1 = close.ewm(span=timeperiod, adjust=False).mean()
            ema2 = ema1.ewm(span=timeperiod, adjust=False).mean()
            ema3 = ema2.ewm(span=timeperiod, adjust=False).mean()
            trix = ema3.diff() / ema3.shift(1) * 100
            if check_date:
                result[sec] = float(trix.iloc[-1])
            else:
                result[sec] = trix
        except Exception as e:
            warnings.warn(f"TRIX计算失败 {sec}: {e}")
            result[sec] = np.nan

    if single and check_date:
        return result.get(security, np.nan)
    if single and not check_date:
        val = result.get(security)
        return val if val is not None else pd.Series(dtype=float)
    return result


def DMA(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    short_period: int = 10,
    long_period: int = 50,
    ama_period: int = 10,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算平均线差指标 (Different of Moving Average)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        short_period: 短期均线周期，默认10
        long_period: 长期均线周期，默认50
        ama_period: AMA平滑周期，默认10
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        Dict: {'DDD': {...}, 'AMA': {...}}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"DDD": {}, "AMA": {}}
    need_count = max(short_period, long_period) + ama_period + 10

    for sec in securities:
        try:
            df = history(
                count=need_count,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            if df.empty or len(df) < need_count - ama_period:
                result["DDD"][sec] = np.nan
                result["AMA"][sec] = np.nan
                continue
            close = df[sec] if sec in df.columns else df.iloc[:, 0]
            ma_short = close.rolling(
                window=short_period, min_periods=short_period
            ).mean()
            ma_long = close.rolling(window=long_period, min_periods=long_period).mean()
            ddd = ma_short - ma_long
            ama = ddd.ewm(span=ama_period, adjust=False).mean()
            result["DDD"][sec] = float(ddd.iloc[-1])
            result["AMA"][sec] = float(ama.iloc[-1])
        except Exception as e:
            warnings.warn(f"DMA计算失败 {sec}: {e}")
            result["DDD"][sec] = np.nan
            result["AMA"][sec] = np.nan

    return result


def EXPMA(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 12,
    unit: str = "1d",
    include_now: bool = True,
) -> Union[float, Dict[str, float], pd.Series]:
    """
    计算指数平滑移动平均线 (Exponential Moving Average)

    参数:
        security: 股票代码或列表
        check_date: 查询日期
        timeperiod: 计算周期，默认12
        unit: 时间单位
        include_now: 是否包含当前bar

    返回:
        单股票+日期: float
        多股票+日期: dict
        单股票无日期: Series
    """
    return EMA(security, check_date, timeperiod, unit, include_now)


__all__ = [
    "MA",
    "EMA",
    "SMA",
    "WMA",
    "MACD",
    "DMI",
    "SAR",
    "RSI",
    "KDJ",
    "CCI",
    "WR",
    "ROC",
    "MTM",
    "BOLL",
    "ATR",
    "STD",
    "VR",
    "OBV",
    "EMV",
    "WVAD",
    "BRAR",
    "CR",
    "PSY",
    "BBI",
    "TRIX",
    "DMA",
    "EXPMA",
]
