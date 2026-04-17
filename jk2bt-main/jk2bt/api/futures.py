"""
jk2bt/api/futures.py
期货数据 API 模块

提供 JQData 兼容的期货数据查询接口。
数据源: AkShare

主要功能:
- get_dominant_future: 获取主力合约代码
- get_futures_info: 获取期货合约信息
- get_future_contracts: 获取期货合约列表
- get_order_future_bar: 获取连续合约bar行情
"""

import pandas as pd
from typing import Optional, List, Union
import warnings
import re


FUTURE_EXCHANGE_MAP = {
    "IF": "CCFX",
    "IC": "CCFX",
    "IH": "CCFX",
    "IM": "CCFX",
    "T": "CCFX",
    "TF": "CCFX",
    "TS": "CCFX",
    "TL": "CCFX",
    "AU": "XSGE",
    "AG": "XSGE",
    "CU": "XSGE",
    "AL": "XSGE",
    "ZN": "XSGE",
    "PB": "XSGE",
    "NI": "XSGE",
    "SN": "XSGE",
    "RB": "XSGE",
    "HC": "XSGE",
    "SS": "XSGE",
    "I": "XDCE",
    "J": "XDCE",
    "JM": "XDCE",
    "ZC": "XDCE",
    "A": "XDCE",
    "B": "XDCE",
    "M": "XDCE",
    "Y": "XDCE",
    "P": "XDCE",
    "C": "XDCE",
    "CS": "XDCE",
    "JD": "XDCE",
    "L": "XDCE",
    "V": "XDCE",
    "PP": "XDCE",
    "EG": "XDCE",
    "MA": "XDCE",
    "TA": "XZCE",
    "OI": "XZCE",
    "RM": "XZCE",
    "SR": "XZCE",
    "CF": "XZCE",
    "SC": "XINE",
    "NR": "XINE",
}


def _is_index_code(symbol: str) -> bool:
    """判断是否为品种指数代码（如 AG8888.XSGE）"""
    if not symbol:
        return False
    match = re.match(r"^([A-Z]+)8888\.([A-Z]+)$", symbol.upper())
    if match:
        product = match.group(1)
        return product in FUTURE_EXCHANGE_MAP
    return False


def _get_product_from_index(symbol: str) -> Optional[str]:
    """从品种指数代码提取品种代码"""
    match = re.match(r"^([A-Z]+)8888\.([A-Z]+)$", symbol.upper())
    if match:
        return match.group(1)
    return None


def get_dominant_future(
    underlying_symbol: str,
    date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Union[str, pd.Series]:
    """
    获取主力合约代码。

    聚宽兼容接口

    参数
    ----
    underlying_symbol : str
        标的合约代码，如 'IF', 'IC', 'IH', 'AU', 'CU' 等
        也支持品种指数格式如 'AG8888.XSGE'
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'。如果提供，返回主力合约代码序列

    返回
    ----
    str or pd.Series
        - 如果只提供 date: 返回主力合约代码字符串
        - 如果提供 end_date: 返回 Series，index 为日期，value 为主力合约代码

    示例
    ----
    >>> contract = get_dominant_future('IF')
    >>> print(contract)
    'IF2401'
    >>> series = get_dominant_future('IF', date='2024-01-01', end_date='2024-01-31')
    >>> print(series)
    2024-01-01    IF2401
    2024-01-02    IF2401
    ...
    """
    if _is_index_code(underlying_symbol):
        product = _get_product_from_index(underlying_symbol)
        if product:
            exchange = FUTURE_EXCHANGE_MAP.get(product, "CCFX")
            result = f"{product}8888.{exchange}"
            if end_date is not None:
                from jk2bt.api.date import get_trade_dates_between

                trade_dates = get_trade_dates_between(date, end_date)
                return pd.Series(
                    [result] * len(trade_dates),
                    index=[
                        d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
                        for d in trade_dates
                    ],
                )
            return result
        return ""

    from jk2bt.data.market.futures_data import get_dominant_contract

    if end_date is not None:
        from jk2bt.api.date import get_trade_dates_between

        trade_dates = get_trade_dates_between(date, end_date)
        if not trade_dates:
            return pd.Series(dtype=str)

        results = {}
        cache = {}
        for trade_date in trade_dates:
            date_str = (
                trade_date.strftime("%Y-%m-%d")
                if hasattr(trade_date, "strftime")
                else str(trade_date)
            )
            cached = cache.get(date_str)
            if cached is not None:
                results[date_str] = cached
                continue
            contract = get_dominant_contract(underlying_symbol, date_str)
            contract = contract or ""
            cache[date_str] = contract
            results[date_str] = contract

        return pd.Series(results, name=underlying_symbol)

    result = get_dominant_contract(underlying_symbol, date)
    return result or ""


def get_futures_info(
    contract_code: Optional[str] = None,
    exchange: Optional[str] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    获取期货合约信息。

    聚宽兼容接口

    参数
    ----
    contract_code : str, optional
        合约代码，如 'IF2401'，None 表示获取所有合约
    exchange : str, optional
        交易所代码:
        - 'CFFEX': 中金所
        - 'SHFE': 上期所
        - 'DCE': 大商所
        - 'CZCE': 郑商所
    fields : list of str, optional
        返回字段列表

    返回
    ----
    pd.DataFrame
        合约信息:
        - code: 合约代码
        - name: 合约名称
        - exchange: 交易所
        - multiplier: 合约乘数
        - min_change: 最小变动价位

    示例
    ----
    >>> df = get_futures_info('IF')
    >>> print(df.head())
    """
    from jk2bt.data.market.futures_data import get_futures_info as _get_futures_info

    result = _get_futures_info(contract_code, exchange)

    if fields and not result.empty:
        available_fields = [f for f in fields if f in result.columns]
        if available_fields:
            result = result[available_fields]

    return result


def get_future_contracts(
    underlying_symbol: str,
    date: Optional[str] = None,
    exchange: Optional[str] = None,
) -> List[str]:
    """
    获取期货合约列表。

    聚宽兼容接口

    参数
    ----
    underlying_symbol : str
        标的合约代码，如 'IF', 'IC', 'AU' 等
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'
    exchange : str, optional
        交易所代码

    返回
    ----
    List[str]
        合约代码列表

    示例
    ----
    >>> contracts = get_future_contracts('IF')
    >>> print(contracts)
    ['IF2401', 'IF2402', 'IF2403', ...]
    """
    from jk2bt.data.market.futures_data import (
        get_future_contracts as _get_future_contracts,
    )

    return _get_future_contracts(underlying_symbol, date, exchange)


def get_dominant_contracts(
    underlying_symbols: List[str],
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    批量获取主力合约。

    参数
    ----
    underlying_symbols : List[str]
        标的合约代码列表
    date : str, optional
        查询日期

    返回
    ----
    pd.DataFrame
        主力合约信息
    """
    from jk2bt.data.market.futures_data import (
        get_dominant_contract,
        FUTURE_UNDERLYING_MAP,
        _get_exchange_by_underlying,
        _get_multiplier,
    )

    results = []
    for underlying in underlying_symbols:
        contract = get_dominant_contract(underlying, date)
        if contract:
            results.append(
                {
                    "underlying": underlying,
                    "contract": contract,
                    "name": FUTURE_UNDERLYING_MAP.get(underlying, ""),
                    "exchange": _get_exchange_by_underlying(underlying),
                    "multiplier": _get_multiplier(underlying),
                }
            )

    return pd.DataFrame(results)


def get_settlement_price(
    contract_code: str,
    date: Optional[str] = None,
) -> float:
    """
    获取期货结算价。

    参数
    ----
    contract_code : str
        合约代码
    date : str, optional
        查询日期

    返回
    ----
    float
        结算价
    """
    from jk2bt.data.market.futures_data import get_futures_daily

    df = get_futures_daily(contract_code, start_date=date, end_date=date)

    if not df.empty:
        return float(df["close"].iloc[0])

    return 0.0


def get_order_future_bar(
    product: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    bar_count: Optional[int] = None,
    fields: Optional[List[str]] = None,
    include_now: bool = True,
) -> pd.DataFrame:
    """
    获取当月/次月/当季/隔季等合约拼接而成的bar行情。

    聚宽兼容接口

    参数
    ----
    product : str
        期货品种代码，如 'IF', 'IC', 'AU', 'AG' 等
    start_date : str, optional
        起始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'
    bar_count : int, optional
        获取bar数量（从 end_date 往前计算）
    fields : list of str, optional
        返回字段列表
    include_now : bool
        是否包含当前交易日

    返回
    ----
    pd.DataFrame
        连续合约bar行情:
        - datetime: 日期时间
        - open: 开盘价
        - high: 最高价
        - low: 最低价
        - close: 收盘价
        - volume: 成交量

    示例
    ----
    >>> df = get_order_future_bar('AG', start_date='2023-01-01', end_date='2023-12-31')
    >>> df = get_order_future_bar('IF', bar_count=100)
    """
    from jk2bt.data.market.futures_data import (
        get_futures_daily,
        _get_order_contracts,
    )
    from datetime import datetime

    product = product.upper()

    if bar_count and bar_count > 0 and end_date:
        end_dt = pd.to_datetime(end_date)
        all_dates = pd.date_range(end=end_dt, periods=bar_count, freq="B")
        start_date = all_dates[0].strftime("%Y-%m-%d")
    elif not start_date:
        start_date = "2020-01-01"
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        order_contracts = _get_order_contracts(product)
        if not order_contracts:
            warnings.warn(f"无法获取 {product} 的顺序合约列表")
            return pd.DataFrame()

        all_bars = []
        for contract in order_contracts:
            df = get_futures_daily(contract, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                if "datetime" in df.columns:
                    df["datetime"] = pd.to_datetime(df["datetime"])
                elif "date" in df.columns:
                    df["datetime"] = pd.to_datetime(df["date"])
                df = (
                    df.rename(columns={"date": "datetime"})
                    if "date" in df.columns
                    else df
                )
                df["contract"] = contract
                all_bars.append(df)

        if not all_bars:
            return pd.DataFrame()

        combined = pd.concat(all_bars, ignore_index=True)
        combined = combined.sort_values("datetime").drop_duplicates(
            subset=["datetime"], keep="last"
        )
        combined = combined.reset_index(drop=True)

        if fields:
            available = [f for f in fields if f in combined.columns]
            if "datetime" not in available and "datetime" in combined.columns:
                available = ["datetime"] + available
            combined = combined[available]

        return combined

    except Exception as e:
        warnings.warn(f"获取连续合约bar行情失败 {product}: {e}")
        return pd.DataFrame()


def get_future_ticks(
    contract: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货合约 tick 数据。

    聚宽兼容接口

    参数
    ----
    contract : str
        合约代码，如 'IF2401', 'AU2401' 等
    start_date : str, optional
        起始日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD' 或 'YYYYMMDD'

    返回
    ----
    pd.DataFrame
        Tick 数据，包含:
        - datetime: 时间戳
        - price: 最新价
        - volume: 成交量
        - bid_price1~bid_price5: 买盘价格
        - ask_price1~ask_price5: 卖盘价格
        - bid_volume1~bid_volume5: 买盘量
        - ask_volume1~ask_volume5: 卖盘量

    示例
    ----
    >>> df = get_future_ticks('IF2401', start_date='2024-01-15', end_date='2024-01-15')
    >>> print(df.head())
    """
    import akshare as ak

    contract = contract.upper().replace(".", "")

    if not start_date:
        start_date = pd.Timestamp.now().strftime("%Y%m%d")
    if not end_date:
        end_date = start_date

    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")

    try:
        all_ticks = []
        current = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        while current <= end:
            date_str = current.strftime("%Y%m%d")
            try:
                df = ak.futures_zh_tick_sina(symbol=contract, trade_date=date_str)
                if df is not None and not df.empty:
                    all_ticks.append(df)
            except Exception:
                pass
            current += pd.Timedelta(days=1)

        if not all_ticks:
            return pd.DataFrame()

        result = pd.concat(all_ticks, ignore_index=True)
        result = (
            result.drop_duplicates()
            .sort_values(
                by=list(result.columns[:1])
                if len(result.columns) > 0
                else result.columns[0]
            )
            .reset_index(drop=True)
        )

        return result

    except Exception as e:
        warnings.warn(f"获取期货 tick 数据失败 {contract}: {e}")
        return pd.DataFrame()


def get_future_index_bar(
    product: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    bar_count: Optional[int] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    获取期货品种指数bar行情。

    参数
    ----
    product : str
        期货品种代码，如 'AG', 'AU', 'CU' 等
    start_date : str, optional
        起始日期
    end_date : str, optional
        结束日期
    bar_count : int, optional
        获取bar数量
    fields : list of str, optional
        返回字段列表

    返回
    ----
    pd.DataFrame
        品种指数bar行情

    示例
    ----
    >>> df = get_future_index_bar('AG', start_date='2023-01-01', end_date='2023-12-31')
    """
    warnings.warn(
        "get_future_index_bar 需要专业数据源（如聚宽JQData），akshare暂无品种指数接口"
    )
    return pd.DataFrame()


def get_futures_margin(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货保证金数据。

    参数
    ----
    code : str, optional
        合约代码或品种代码
    start_date : str, optional
        起始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        期货保证金数据:
        - day: 日期
        - code: 合约代码
        - exchange: 交易所
        - exchange_name: 交易所名称
        - specul_buy_margin_rate: 投机买保证金比例
        - specul_sell_margin_rate: 投机卖保证金比例
        - hedg_buy_margin_rate: 套保买保证金比例
        - hedg_sell_margin_rate: 套保卖保证金比例

    示例
    ----
    >>> df = get_futures_margin('IF')
    >>> df = get_futures_margin(start_date='2024-01-01', end_date='2024-12-31')
    """
    from jk2bt.data.finance.tables import get_futures_margin as _get_futures_margin

    return _get_futures_margin(code=code, start_date=start_date, end_date=end_date)


def get_futures_charge(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货手续费数据。

    参数
    ----
    code : str, optional
        合约代码或品种代码
    start_date : str, optional
        起始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        期货手续费数据:
        - day: 日期
        - code: 合约代码
        - exchange: 交易所
        - exchange_name: 交易所名称
        - unit: 计费方式 (按手/按金额)
        - clearance_charge: 平仓手续费
        - opening_charge: 开仓手续费
        - short_clearance_charge: 平今仓手续费
        - short_opening_charge: 开今仓手续费

    示例
    ----
    >>> df = get_futures_charge('IF')
    >>> df = get_futures_charge(start_date='2024-01-01', end_date='2024-12-31')
    """
    from jk2bt.data.finance.tables import get_futures_charge as _get_futures_charge

    return _get_futures_charge(code=code, start_date=start_date, end_date=end_date)


def get_futures_warehouse(
    symbol: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货仓单数据。

    参数
    ----
    symbol : str, optional
        品种代码
    start_date : str, optional
        起始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        期货仓单数据:
        - day: 日期
        - symbol: 品种
        - warehouse_receipt: 仓单数量
        - warehouse_name: 仓库名称
        - region: 地区

    示例
    ----
    >>> df = get_futures_warehouse('CU')
    >>> df = get_futures_warehouse(start_date='2024-01-01', end_date='2024-12-31')
    """
    from jk2bt.data.finance.tables import (
        get_futures_warehouse as _get_futures_warehouse,
    )

    return _get_futures_warehouse(
        symbol=symbol, start_date=start_date, end_date=end_date
    )


def get_futures_member_position(
    symbol: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    exchange: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货会员持仓数据（龙虎榜）。

    参数
    ----
    symbol : str, optional
        合约代码
    start_date : str, optional
        起始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'
    exchange : str, optional
        交易所代码 (CFFEX/SHFE/DCE/CZCE)

    返回
    ----
    pd.DataFrame
        期货会员持仓数据:
        - day: 日期
        - symbol: 合约代码
        - broker: 会员名称
        - long_holding: 多头持仓
        - long_change: 多头变化
        - short_holding: 空头持仓
        - short_change: 空头变化
        - volume: 成交量
        - volume_change: 成交量变化

    示例
    ----
    >>> df = get_futures_member_position('IF2401')
    >>> df = get_futures_member_position(exchange='CFFEX')
    """
    from jk2bt.data.finance.tables import (
        get_futures_member_position as _get_futures_member_position,
    )

    return _get_futures_member_position(
        symbol=symbol, start_date=start_date, end_date=end_date, exchange=exchange
    )


# 聚宽风格别名
get_dominant_future_jq = get_dominant_future
get_futures_info_jq = get_futures_info
get_future_contracts_jq = get_future_contracts


__all__ = [
    "get_dominant_future",
    "get_futures_info",
    "get_future_contracts",
    "get_dominant_contracts",
    "get_settlement_price",
    "get_order_future_bar",
    "get_future_ticks",
    "get_future_index_bar",
    "get_futures_margin",
    "get_futures_charge",
    "get_futures_warehouse",
    "get_futures_member_position",
    "get_dominant_future_jq",
    "get_futures_info_jq",
    "get_future_contracts_jq",
]
