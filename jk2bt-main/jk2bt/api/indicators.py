"""
聚宽兼容技术指标 API 模块
实现 MA、MACD、KDJ、RSI 等常用技术指标函数

聚宽风格接口，支持策略中直接调用
"""

import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional, Tuple
import warnings


def MA(
    closeArray: Union[pd.Series, np.ndarray, list],
    timeperiod: int = 30,
) -> Union[pd.Series, np.ndarray]:
    """
    计算简单移动平均线 (Moving Average)

    聚宽兼容接口

    参数:
        closeArray: 收盘价序列 (Series/ndarray/list)
        timeperiod: 移动平均周期，默认 30

    返回:
        移动平均值序列，类型与输入相同

    示例:
        # 计算收盘价的5日均线
        ma5 = MA(close, timeperiod=5)

        # 计算成交量的20日均线
        vol_ma20 = MA(volume, timeperiod=20)
    """
    if isinstance(closeArray, pd.Series):
        return closeArray.rolling(window=timeperiod, min_periods=timeperiod).mean()
    elif isinstance(closeArray, np.ndarray):
        series = pd.Series(closeArray)
        result = series.rolling(window=timeperiod, min_periods=timeperiod).mean()
        return result.values
    elif isinstance(closeArray, list):
        series = pd.Series(closeArray)
        result = series.rolling(window=timeperiod, min_periods=timeperiod).mean()
        return result.tolist()
    else:
        raise TypeError(f"不支持的类型: {type(closeArray)}")


def EMA(
    closeArray: Union[pd.Series, np.ndarray, list],
    timeperiod: int = 30,
) -> Union[pd.Series, np.ndarray]:
    """
    计算指数移动平均线 (Exponential Moving Average)

    参数:
        closeArray: 收盘价序列
        timeperiod: 移动平均周期，默认 30

    返回:
        指数移动平均值序列

    示例:
        ema12 = EMA(close, timeperiod=12)
    """
    if isinstance(closeArray, pd.Series):
        return closeArray.ewm(span=timeperiod, adjust=False).mean()
    elif isinstance(closeArray, np.ndarray):
        series = pd.Series(closeArray)
        result = series.ewm(span=timeperiod, adjust=False).mean()
        return result.values
    elif isinstance(closeArray, list):
        series = pd.Series(closeArray)
        result = series.ewm(span=timeperiod, adjust=False).mean()
        return result.tolist()
    else:
        raise TypeError(f"不支持的类型: {type(closeArray)}")


def MACD(
    security_list: Union[str, List[str]],
    check_date: Optional[str] = None,
    SHORT: int = 12,
    LONG: int = 26,
    MID: int = 9,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, Union[float, pd.DataFrame]]]:
    """
    计算 MACD 指标 (Moving Average Convergence Divergence)

    聚宽兼容接口，支持单标的或多标的

    参数:
        security_list: 股票代码或股票列表
        check_date: 查询日期，格式 'YYYY-MM-DD'
        SHORT: 短期EMA周期，默认 12
        LONG: 长期EMA周期，默认 26
        MID: DEA周期，默认 9
        unit: 时间单位，默认 '1d'
        include_now: 是否包含当前日期

    返回:
        Dict 结构:
        {
            'MACD': {'股票代码': macd值},
            'DIFF': {'股票代码': diff值},
            'DEA': {'股票代码': dea值}
        }
        或多日期时返回 DataFrame

    示例:
        # 获取单只股票的MACD
        result = MACD('600519.XSHG', check_date='2024-01-01')
        macd_value = result['MACD']['600519.XSHG']

        # 获取多只股票的MACD
        result = MACD(['600519.XSHG', '000858.XSHE'], check_date='2024-01-01')
    """
    from jk2bt.api.market import history

    # 统一为列表格式
    if isinstance(security_list, str):
        securities = [security_list]
        single_security = True
    else:
        securities = security_list
        single_security = False

    # 计算所需数据量
    need_count = LONG + MID + 10

    result = {
        "MACD": {},
        "DIFF": {},
        "DEA": {},
    }

    for security in securities:
        try:
            # 获取历史数据
            df = history(
                count=need_count,
                unit=unit,
                field="close",
                security_list=[security],
                end_dt=check_date,
                include_now=include_now,
            )

            if df.empty or len(df) < LONG:
                result["MACD"][security] = np.nan
                result["DIFF"][security] = np.nan
                result["DEA"][security] = np.nan
                continue

            close = df[security] if security in df.columns else df.iloc[:, 0]

            # 计算 MACD
            ema_short = close.ewm(span=SHORT, adjust=False).mean()
            ema_long = close.ewm(span=LONG, adjust=False).mean()
            diff = ema_short - ema_long
            dea = diff.ewm(span=MID, adjust=False).mean()
            macd = 2 * (diff - dea)

            # 取最新值
            result["DIFF"][security] = float(diff.iloc[-1])
            result["DEA"][security] = float(dea.iloc[-1])
            result["MACD"][security] = float(macd.iloc[-1])

        except Exception as e:
            warnings.warn(f"MACD计算失败 {security}: {e}")
            result["MACD"][security] = np.nan
            result["DIFF"][security] = np.nan
            result["DEA"][security] = np.nan

    return result


def KDJ(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    unit: str = "1d",
    N: int = 9,
    M1: int = 3,
    M2: int = 3,
    include_now: bool = True,
) -> Dict[str, Dict[str, Union[float, Tuple[float, float, float]]]]:
    """
    计算 KDJ 指标 (Stochastic Oscillator)

    聚宽兼容接口

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期，格式 'YYYY-MM-DD'
        unit: 时间单位，默认 '1d'
        N: RSV周期，默认 9
        M1: K值平滑周期，默认 3
        M2: D值平滑周期，默认 3
        include_now: 是否包含当前日期

    返回:
        Dict 结构:
        {
            'K': {'股票代码': K值},
            'D': {'股票代码': D值},
            'J': {'股票代码': J值}
        }

    示例:
        # 获取单只股票的KDJ
        result = KDJ('600519.XSHG', check_date='2024-01-01')
        k_value = result['K']['600519.XSHG']
    """
    from jk2bt.api.market import history

    # 统一为列表格式
    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {
        "K": {},
        "D": {},
        "J": {},
    }

    for sec in securities:
        try:
            # 获取历史数据
            df_high = history(
                count=N + M1 + M2 + 10,
                unit=unit,
                field="high",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_low = history(
                count=N + M1 + M2 + 10,
                unit=unit,
                field="low",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_close = history(
                count=N + M1 + M2 + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )

            if df_high.empty or df_low.empty or df_close.empty:
                result["K"][sec] = np.nan
                result["D"][sec] = np.nan
                result["J"][sec] = np.nan
                continue

            high = df_high[sec] if sec in df_high.columns else df_high.iloc[:, 0]
            low = df_low[sec] if sec in df_low.columns else df_low.iloc[:, 0]
            close = df_close[sec] if sec in df_close.columns else df_close.iloc[:, 0]

            # 计算 RSV
            lowest_low = low.rolling(window=N, min_periods=N).min()
            highest_high = high.rolling(window=N, min_periods=N).max()

            rsv = (close - lowest_low) / (highest_high - lowest_low) * 100
            rsv = rsv.fillna(50)  # 处理除零情况

            # 计算 K、D、J
            k = rsv.ewm(alpha=1 / M1, adjust=False).mean()
            d = k.ewm(alpha=1 / M2, adjust=False).mean()
            j = 3 * k - 2 * d

            result["K"][sec] = float(k.iloc[-1])
            result["D"][sec] = float(d.iloc[-1])
            result["J"][sec] = float(j.iloc[-1])

        except Exception as e:
            warnings.warn(f"KDJ计算失败 {sec}: {e}")
            result["K"][sec] = np.nan
            result["D"][sec] = np.nan
            result["J"][sec] = np.nan

    return result


def RSI(
    price: Union[pd.Series, np.ndarray, list, str],
    timeperiod: int = 14,
    check_date: Optional[str] = None,
) -> Union[pd.Series, float, Dict[str, float]]:
    """
    计算 RSI 指标 (Relative Strength Index)

    聚宽兼容接口

    参数:
        price: 价格序列或股票代码
        timeperiod: 计算周期，默认 14
        check_date: 查询日期（当 price 为股票代码时使用）

    返回:
        RSI 值（0-100之间）

    示例:
        # 使用价格序列
        rsi = RSI(close_prices, timeperiod=14)

        # 使用股票代码
        rsi = RSI('600519.XSHG', timeperiod=14, check_date='2024-01-01')
    """
    # 如果输入是字符串（股票代码），则获取数据
    if isinstance(price, str):
        from jk2bt.api.market import history

        try:
            df = history(
                count=timeperiod + 20,
                unit="1d",
                field="close",
                security_list=[price],
                end_dt=check_date,
            )
            if df.empty:
                return np.nan
            close = df[price] if price in df.columns else df.iloc[:, 0]
        except Exception as e:
            warnings.warn(f"RSI数据获取失败 {price}: {e}")
            return np.nan
    elif isinstance(price, (pd.Series, np.ndarray, list)):
        close = pd.Series(price) if not isinstance(price, pd.Series) else price
    else:
        raise TypeError(f"不支持的类型: {type(price)}")

    # 计算 RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=timeperiod, min_periods=timeperiod).mean()
    avg_loss = loss.rolling(window=timeperiod, min_periods=timeperiod).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # 返回最新值或序列
    if isinstance(price, str):
        return float(rsi.iloc[-1])
    elif isinstance(price, (np.ndarray, list)):
        return rsi.values if isinstance(price, np.ndarray) else rsi.tolist()
    else:
        return rsi


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
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 20
        nbdevup: 上轨标准差倍数，默认 2
        nbdevdn: 下轨标准差倍数，默认 2
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict 结构:
        {
            'UPPER': {'股票代码': 上轨值},
            'MIDDLE': {'股票代码': 中轨值},
            'LOWER': {'股票代码': 下轨值}
        }

    示例:
        result = BOLL('600519.XSHG', check_date='2024-01-01')
        upper = result['UPPER']['600519.XSHG']
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {
        "UPPER": {},
        "MIDDLE": {},
        "LOWER": {},
    }

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
                result["UPPER"][sec] = np.nan
                result["MIDDLE"][sec] = np.nan
                result["LOWER"][sec] = np.nan
                continue

            close = df[sec] if sec in df.columns else df.iloc[:, 0]

            # 计算布林带
            middle = close.rolling(window=timeperiod, min_periods=timeperiod).mean()
            std = close.rolling(window=timeperiod, min_periods=timeperiod).std()

            upper = middle + nbdevup * std
            lower = middle - nbdevdn * std

            result["UPPER"][sec] = float(upper.iloc[-1])
            result["MIDDLE"][sec] = float(middle.iloc[-1])
            result["LOWER"][sec] = float(lower.iloc[-1])

        except Exception as e:
            warnings.warn(f"BOLL计算失败 {sec}: {e}")
            result["UPPER"][sec] = np.nan
            result["MIDDLE"][sec] = np.nan
            result["LOWER"][sec] = np.nan

    return result


def ATR(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 14,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, float]:
    """
    计算平均真实波幅指标 (Average True Range)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 14
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: {'股票代码': ATR值}

    示例:
        atr = ATR('600519.XSHG', check_date='2024-01-01', timeperiod=14)
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}

    for sec in securities:
        try:
            df_high = history(
                count=timeperiod + 20,
                unit=unit,
                field="high",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_low = history(
                count=timeperiod + 20,
                unit=unit,
                field="low",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_close = history(
                count=timeperiod + 20,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )

            if df_high.empty or df_low.empty or df_close.empty:
                result[sec] = np.nan
                continue

            high = df_high[sec] if sec in df_high.columns else df_high.iloc[:, 0]
            low = df_low[sec] if sec in df_low.columns else df_low.iloc[:, 0]
            close = df_close[sec] if sec in df_close.columns else df_close.iloc[:, 0]

            # 计算 True Range
            tr1 = high - low
            tr2 = np.abs(high - close.shift(1))
            tr3 = np.abs(low - close.shift(1))

            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=timeperiod, min_periods=timeperiod).mean()

            result[sec] = float(atr.iloc[-1])

        except Exception as e:
            warnings.warn(f"ATR计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def BIAS(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 12,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, float]:
    """
    计算乖离率指标 (Bias)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 12
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: {'股票代码': BIAS值}
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
            ma = close.rolling(window=timeperiod, min_periods=timeperiod).mean()
            bias = (close - ma) / ma * 100

            result[sec] = float(bias.iloc[-1])

        except Exception as e:
            warnings.warn(f"BIAS计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def DKX(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 10,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算多空线指标 (DKX)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 10
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: {'DKX': {'股票代码': DKX值}, 'MADKX': {'股票代码': MADKX值}}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"DKX": {}, "MADKX": {}}

    for sec in securities:
        try:
            df_high = history(
                count=timeperiod + 20,
                unit=unit,
                field="high",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_low = history(
                count=timeperiod + 20,
                unit=unit,
                field="low",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_close = history(
                count=timeperiod + 20,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_open = history(
                count=timeperiod + 20,
                unit=unit,
                field="open",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )

            if df_high.empty or df_low.empty or df_close.empty or df_open.empty:
                result["DKX"][sec] = np.nan
                result["MADKX"][sec] = np.nan
                continue

            high = df_high[sec] if sec in df_high.columns else df_high.iloc[:, 0]
            low = df_low[sec] if sec in df_low.columns else df_low.iloc[:, 0]
            close = df_close[sec] if sec in df_close.columns else df_close.iloc[:, 0]
            open_price = df_open[sec] if sec in df_open.columns else df_open.iloc[:, 0]

            dkx = (3 * close + 2 * high + low + open_price) / 7
            dkx = dkx.rolling(window=timeperiod, min_periods=timeperiod).mean()
            madkx = dkx.rolling(window=timeperiod, min_periods=timeperiod).mean()

            result["DKX"][sec] = float(dkx.iloc[-1])
            result["MADKX"][sec] = float(madkx.iloc[-1])

        except Exception as e:
            warnings.warn(f"DKX计算失败 {sec}: {e}")
            result["DKX"][sec] = np.nan
            result["MADKX"][sec] = np.nan

    return result


def DPO(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 20,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, float]:
    """
    计算去趋势价格摆动指标 (Detrended Price Oscillator)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 20
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: {'股票代码': DPO值}
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
            ma = close.rolling(window=timeperiod, min_periods=timeperiod).mean()
            dpo = close.shift(int(timeperiod / 2) + 1) - ma

            result[sec] = float(dpo.iloc[-1])

        except Exception as e:
            warnings.warn(f"DPO计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def ADTM(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    N: int = 23,
    M: int = 8,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算动态买卖气指标 (ADTM)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        N: 计算周期，默认 23
        M: 平滑周期，默认 8
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: {'ADTM': {'股票代码': ADTM值}, 'ADTMMA': {'股票代码': ADTMMA值}}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"ADTM": {}, "ADTMMA": {}}

    for sec in securities:
        try:
            df_high = history(
                count=N + 20,
                unit=unit,
                field="high",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_low = history(
                count=N + 20,
                unit=unit,
                field="low",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_open = history(
                count=N + 20,
                unit=unit,
                field="open",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )

            if df_high.empty or df_low.empty or df_open.empty:
                result["ADTM"][sec] = np.nan
                result["ADTMMA"][sec] = np.nan
                continue

            high = df_high[sec] if sec in df_high.columns else df_high.iloc[:, 0]
            low = df_low[sec] if sec in df_low.columns else df_low.iloc[:, 0]
            open_price = df_open[sec] if sec in df_open.columns else df_open.iloc[:, 0]

            dtm = np.where(
                open_price <= open_price.shift(1),
                np.maximum(high - open_price, open_price - open_price.shift(1)),
                0,
            )
            dbm = np.where(
                open_price >= open_price.shift(1),
                np.maximum(open_price - low, open_price - open_price.shift(1)),
                0,
            )

            dtm = pd.Series(dtm, index=high.index)
            dbm = pd.Series(dbm, index=high.index)

            stm = dtm.rolling(window=N, min_periods=N).sum()
            sbm = dbm.rolling(window=N, min_periods=N).sum()

            adtm = (stm - sbm) / np.where(stm > sbm, stm, sbm)
            adtm = adtm.fillna(0)
            adtmma = adtm.rolling(window=M, min_periods=M).mean()

            result["ADTM"][sec] = float(adtm.iloc[-1])
            result["ADTMMA"][sec] = float(adtmma.iloc[-1])

        except Exception as e:
            warnings.warn(f"ADTM计算失败 {sec}: {e}")
            result["ADTM"][sec] = np.nan
            result["ADTMMA"][sec] = np.nan

    return result


def GDX(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 9,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, float]:
    """
    计算广德线指标 (GDX)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 9
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: {'股票代码': GDX值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}

    for sec in securities:
        try:
            df_high = history(
                count=timeperiod + 20,
                unit=unit,
                field="high",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_low = history(
                count=timeperiod + 20,
                unit=unit,
                field="low",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )

            if df_high.empty or df_low.empty:
                result[sec] = np.nan
                continue

            high = df_high[sec] if sec in df_high.columns else df_high.iloc[:, 0]
            low = df_low[sec] if sec in df_low.columns else df_low.iloc[:, 0]

            highest = high.rolling(window=timeperiod, min_periods=timeperiod).max()
            lowest = low.rolling(window=timeperiod, min_periods=timeperiod).min()
            gdx = (highest - lowest) / lowest * 100

            result[sec] = float(gdx.iloc[-1])

        except Exception as e:
            warnings.warn(f"GDX计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def MIKE(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 10,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    计算麦克指标 (MIKE)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 10
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: 包含 WR, MR, SR, WS, MS, SS 等支撑压力位
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {"WR": {}, "MR": {}, "SR": {}, "WS": {}, "MS": {}, "SS": {}}

    for sec in securities:
        try:
            df_high = history(
                count=timeperiod + 10,
                unit=unit,
                field="high",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_low = history(
                count=timeperiod + 10,
                unit=unit,
                field="low",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_close = history(
                count=timeperiod + 10,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )

            if df_high.empty or df_low.empty or df_close.empty:
                for k in result:
                    result[k][sec] = np.nan
                continue

            high = df_high[sec] if sec in df_high.columns else df_high.iloc[:, 0]
            low = df_low[sec] if sec in df_low.columns else df_low.iloc[:, 0]
            close = df_close[sec] if sec in df_close.columns else df_close.iloc[:, 0]

            highest = high.rolling(window=timeperiod, min_periods=timeperiod).max()
            lowest = low.rolling(window=timeperiod, min_periods=timeperiod).min()
            typ = (close + high + low) / 3
            typ_avg = typ.rolling(window=timeperiod, min_periods=timeperiod).mean()

            result["WR"][sec] = float(
                typ_avg.iloc[-1] - (highest.iloc[-1] - lowest.iloc[-1])
            )
            result["MR"][sec] = float(typ_avg.iloc[-1])
            result["SR"][sec] = float(
                typ_avg.iloc[-1] + (highest.iloc[-1] - lowest.iloc[-1])
            )
            result["WS"][sec] = float(
                typ_avg.iloc[-1] - 2 * (highest.iloc[-1] - lowest.iloc[-1])
            )
            result["MS"][sec] = float(
                typ_avg.iloc[-1] - (highest.iloc[-1] - lowest.iloc[-1])
            )
            result["SS"][sec] = float(
                typ_avg.iloc[-1] - 2 * (highest.iloc[-1] - lowest.iloc[-1])
            )

        except Exception as e:
            warnings.warn(f"MIKE计算失败 {sec}: {e}")
            for k in result:
                result[k][sec] = np.nan

    return result


def RAD(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 26,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, float]:
    """
    计算威力指标 (RAD)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 26
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: {'股票代码': RAD值}
    """
    from jk2bt.api.market import history

    if isinstance(security, str):
        securities = [security]
    else:
        securities = security

    result = {}

    for sec in securities:
        try:
            df_close = history(
                count=timeperiod + 20,
                unit=unit,
                field="close",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_high = history(
                count=timeperiod + 20,
                unit=unit,
                field="high",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )
            df_low = history(
                count=timeperiod + 20,
                unit=unit,
                field="low",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )

            if df_close.empty or df_high.empty or df_low.empty:
                result[sec] = np.nan
                continue

            close = df_close[sec] if sec in df_close.columns else df_close.iloc[:, 0]
            high = df_high[sec] if sec in df_high.columns else df_high.iloc[:, 0]
            low = df_low[sec] if sec in df_low.columns else df_low.iloc[:, 0]

            pm = (close - close.shift(1)) / close.shift(1)
            pm = pm.fillna(0)
            tm = ((high - low) / low).shift(1).fillna(0)
            rad = (pm / tm).replace([np.inf, -np.inf], 0).fillna(0)
            rad = rad.rolling(window=timeperiod, min_periods=timeperiod).sum()

            result[sec] = float(rad.iloc[-1])

        except Exception as e:
            warnings.warn(f"RAD计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


def AMO(
    security: Union[str, List[str]],
    check_date: Optional[str] = None,
    timeperiod: int = 6,
    unit: str = "1d",
    include_now: bool = True,
) -> Dict[str, float]:
    """
    计算成交金额指标 (Amount Oscillator)

    参数:
        security: 股票代码或股票列表
        check_date: 查询日期
        timeperiod: 计算周期，默认 6
        unit: 时间单位
        include_now: 是否包含当前日期

    返回:
        Dict: {'股票代码': AMO值}
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
                field="money",
                security_list=[sec],
                end_dt=check_date,
                include_now=include_now,
            )

            if df.empty or len(df) < timeperiod:
                result[sec] = np.nan
                continue

            money = df[sec] if sec in df.columns else df.iloc[:, 0]
            amo = money.rolling(window=timeperiod, min_periods=timeperiod).mean()

            result[sec] = float(amo.iloc[-1])

        except Exception as e:
            warnings.warn(f"AMO计算失败 {sec}: {e}")
            result[sec] = np.nan

    return result


__all__ = [
    "MA",
    "EMA",
    "MACD",
    "KDJ",
    "RSI",
    "BOLL",
    "ATR",
    "BIAS",
    "DKX",
    "DPO",
    "ADTM",
    "GDX",
    "MIKE",
    "RAD",
    "AMO",
]
