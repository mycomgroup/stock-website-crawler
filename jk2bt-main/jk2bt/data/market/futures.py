"""
futures.py
期货数据获取模块

支持:
- 股指期货 (IF, IC, IH, IM)
- 商品期货
- 主力合约识别
- 合约乘数和保证金信息
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import re
import warnings
from typing import Optional
try:
    from jk2bt.data.sources import get_adapter as _get_adapter

    _ADAPTER_AVAILABLE = True
except ImportError:
    _ADAPTER_AVAILABLE = False

logger = logging.getLogger(__name__)

CHINA_FUTURE_EXCHANGE_INFO = {
    "CFFEX": {
        "name": "中国金融期货交易所",
        "products": ["IF", "IC", "IH", "IM", "TS", "TF", "T"],
        "multipliers": {
            "IF": 300,
            "IC": 200,
            "IH": 300,
            "IM": 200,
            "TS": 200,
            "TF": 10000,
            "T": 10000,
        },
        "margin_rates": {
            "IF": 0.12,
            "IC": 0.14,
            "IH": 0.12,
            "IM": 0.14,
            "TS": 0.02,
            "TF": 0.02,
            "T": 0.02,
        },
    },
    "SHFE": {
        "name": "上海期货交易所",
        "products": [
            "AU",
            "AG",
            "CU",
            "AL",
            "ZN",
            "PB",
            "NI",
            "SN",
            "SS",
            "RB",
            "HC",
            "WR",
            "SP",
        ],
        "multipliers": {
            "AU": 1000,
            "AG": 15,
            "CU": 5,
            "AL": 5,
            "ZN": 5,
            "PB": 5,
            "NI": 1,
            "SN": 1,
            "SS": 1,
            "RB": 10,
            "HC": 10,
            "WR": 10,
            "SP": 1,
        },
        "margin_rates": {
            "AU": 0.08,
            "AG": 0.08,
            "CU": 0.08,
            "AL": 0.08,
            "ZN": 0.08,
            "PB": 0.08,
            "NI": 0.10,
            "SN": 0.10,
            "SS": 0.10,
            "RB": 0.08,
            "HC": 0.08,
            "WR": 0.08,
            "SP": 0.08,
        },
    },
    "DCE": {
        "name": "大连商品交易所",
        "products": [
            "C",
            "CS",
            "A",
            "B",
            "M",
            "Y",
            "P",
            "JD",
            "L",
            "V",
            "PP",
            "J",
            "JM",
            "I",
            "FB",
            "BB",
            "PG",
            "EG",
            "EB",
        ],
        "multipliers": {
            "C": 10,
            "CS": 10,
            "A": 10,
            "B": 10,
            "M": 10,
            "Y": 10,
            "P": 10,
            "JD": 10,
            "L": 1,
            "V": 5,
            "PP": 5,
            "J": 100,
            "JM": 60,
            "I": 100,
            "FB": 500,
            "BB": 500,
            "PG": 20,
            "EG": 10,
            "EB": 5,
        },
        "margin_rates": {
            "C": 0.08,
            "CS": 0.08,
            "A": 0.08,
            "B": 0.08,
            "M": 0.08,
            "Y": 0.08,
            "P": 0.08,
            "JD": 0.08,
            "L": 0.08,
            "V": 0.08,
            "PP": 0.08,
            "J": 0.08,
            "JM": 0.08,
            "I": 0.08,
            "FB": 0.08,
            "BB": 0.08,
            "PG": 0.08,
            "EG": 0.08,
            "EB": 0.08,
        },
    },
    "CZCE": {
        "name": "郑州商品交易所",
        "products": [
            "CF",
            "SR",
            "TA",
            "MA",
            "FG",
            "RM",
            "OI",
            "ZC",
            "JR",
            "LR",
            "PM",
            "WH",
            "RI",
            "RS",
            "AP",
            "CJ",
            "UR",
            "SA",
            "SF",
            "SM",
        ],
        "multipliers": {
            "CF": 5,
            "SR": 10,
            "TA": 5,
            "MA": 10,
            "FG": 20,
            "RM": 10,
            "OI": 10,
            "ZC": 100,
            "JR": 20,
            "LR": 10,
            "PM": 50,
            "WH": 20,
            "RI": 20,
            "RS": 10,
            "AP": 10,
            "CJ": 5,
            "UR": 5,
            "SA": 5,
            "SF": 1,
            "SM": 1,
        },
        "margin_rates": {
            "CF": 0.08,
            "SR": 0.08,
            "TA": 0.08,
            "MA": 0.08,
            "FG": 0.08,
            "RM": 0.08,
            "OI": 0.08,
            "ZC": 0.08,
            "JR": 0.08,
            "LR": 0.08,
            "PM": 0.08,
            "WH": 0.08,
            "RI": 0.08,
            "RS": 0.08,
            "AP": 0.08,
            "CJ": 0.08,
            "UR": 0.08,
            "SA": 0.08,
            "SF": 0.08,
            "SM": 0.08,
        },
    },
    "INE": {
        "name": "上海国际能源交易中心",
        "products": ["SC", "NR"],
        "multipliers": {
            "SC": 1000,
            "NR": 10,
        },
        "margin_rates": {
            "SC": 0.10,
            "NR": 0.08,
        },
    },
}

INDEX_FUTURE_PRODUCT_MAP = {
    "IF": "沪深300股指期货",
    "IC": "中证500股指期货",
    "IH": "上证50股指期货",
    "IM": "中证1000股指期货",
}

PRODUCT_TO_INDEX_CODE = {
    "IF": "000300.XSHG",
    "IC": "000905.XSHG",
    "IH": "000016.XSHG",
    "IM": "000852.XSHG",
}


def parse_future_contract(contract_code):
    """
    解析期货合约代码

    Parameters
    ----------
    contract_code : str
        合约代码，如 'IF2312', 'IC2401', 'AU2312'

    Returns
    -------
    dict
        {
            'product': 'IF',
            'year': '23',
            'month': '12',
            'exchange': 'CFFEX',
            'full_code': 'IF2312'
        }
    """
    contract_code = contract_code.strip().upper()

    if ".CCFX" in contract_code:
        contract_code = contract_code.replace(".CCFX", "")

    match = re.match(r"^([A-Z]+)(\d{4})$", contract_code)
    if not match:
        logger.warning(f"无法解析合约代码: {contract_code}")
        return None

    product = match.group(1)
    year_month = match.group(2)

    year = year_month[:2]
    month = year_month[2:]

    exchange = None
    for exch, info in CHINA_FUTURE_EXCHANGE_INFO.items():
        if product in info["products"]:
            exchange = exch
            break

    return {
        "product": product,
        "year": year,
        "month": month,
        "exchange": exchange,
        "full_code": contract_code,
    }


def get_future_contracts(product=None, exchange=None, date=None, include_expired=False):
    """
    获取期货合约列表

    Parameters
    ----------
    product : str, optional
        产品代码，如 'IF', 'IC', 'IH', 'IM'，不指定则返回所有
    exchange : str, optional
        交易所代码，如 'CFFEX', 'SHFE', 'DCE', 'CZCE', 'INE'
    date : str, optional
        查询日期，如 '2023-12-01'
    include_expired : bool
        是否包含已过期合约

    Returns
    -------
    DataFrame
        columns: ['contract', 'product', 'exchange', 'year', 'month', 'is_trading', 'expire_date']

    Example
    -------
    >>> df = get_future_contracts(product='IF')
    >>> df = get_future_contracts(exchange='CFFEX')
    """
    if not _ADAPTER_AVAILABLE:
        raise ImportError("AkShare 未安装")

    try:
        if exchange and exchange.upper() == "CFFEX":
            contracts = _get_cffex_contracts(product, date, include_expired)
        elif exchange:
            contracts = _get_exchange_contracts(
                exchange, product, date, include_expired
            )
        elif product:
            contracts = _get_contracts_by_product(product, date, include_expired)
        else:
            contracts = _get_all_contracts(date, include_expired)

        return contracts

    except Exception as e:
        logger.error(f"获取期货合约失败: {e}")
        return pd.DataFrame()


def _get_cffex_contracts(product=None, date=None, include_expired=False):
    """
    获取中金所期货合约列表

    股指期货合约月份: 当月、下月、随后两个季月
    """
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)

    current_year = date.year
    current_month = date.month

    cffex_products = CHINA_FUTURE_EXCHANGE_INFO["CFFEX"]["products"]

    if product:
        products = [product.upper()] if product.upper() in cffex_products else []
    else:
        products = cffex_products

    contracts_list = []

    for prod in products:
        contract_months = _generate_index_future_months(current_year, current_month)

        for year, month in contract_months:
            contract_code = f"{prod}{str(year)[-2:]}{str(month).zfill(2)}"
            expire_date = _get_expire_date(year, month)

            is_expired = date > expire_date if expire_date else False
            is_trading = not is_expired

            if not include_expired and is_expired:
                continue

            contracts_list.append(
                {
                    "contract": contract_code,
                    "product": prod,
                    "exchange": "CFFEX",
                    "year": str(year)[-2:],
                    "month": str(month).zfill(2),
                    "is_trading": is_trading,
                    "expire_date": expire_date,
                    "display_name": f"{INDEX_FUTURE_PRODUCT_MAP.get(prod, prod)}{month}月",
                }
            )

    return pd.DataFrame(contracts_list)


def _generate_index_future_months(year, month):
    """
    生成股指期货合约月份

    规则: 当月、下月、随后两个季月（3, 6, 9, 12）
    """
    months = []

    months.append((year, month))

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    months.append((next_year, next_month))

    quarter_months = [3, 6, 9, 12]
    for qm in quarter_months:
        if qm >= month:
            months.append((year, qm))
        else:
            months.append((year + 1, qm))

    unique_months = sorted(set(months), key=lambda x: (x[0], x[1]))[:4]

    return unique_months


def _get_expire_date(year, month):
    """
    获取股指期货合约到期日

    规则: 合约到期月份的第三个周五
    """
    import calendar

    weekday = calendar.weekday(year, month, 1)

    first_friday = 1 + (4 - weekday) % 7

    third_friday = first_friday + 14

    return datetime(year, month, third_friday)


def _get_exchange_contracts(exchange, product=None, date=None, include_expired=False):
    """
    获取指定交易所的合约列表
    """
    exchange = exchange.upper()

    if exchange not in CHINA_FUTURE_EXCHANGE_INFO:
        logger.warning(f"不支持交易所: {exchange}")
        return pd.DataFrame()

    try:
        df = _get_adapter().get_futures_spot()

        if df is None or df.empty:
            return pd.DataFrame()

        df = df.copy()

        exchange_map = {
            "XSHFE": "SHFE",
            "XDCE": "DCE",
            "XZCE": "CZCE",
            "CFFEX": "CFFEX",
            "INE": "INE",
        }

        if "exchange" in df.columns:
            df["exchange"] = df["exchange"].map(exchange_map)
            df = df[df["exchange"] == exchange]

        contracts_list = []
        for row in df.itertuples():
            contract_code = getattr(row, "symbol", "")
            if not contract_code:
                continue

            parsed = parse_future_contract(contract_code)
            if not parsed:
                continue

            if product and parsed["product"] != product.upper():
                continue

            contracts_list.append(
                {
                    "contract": contract_code,
                    "product": parsed["product"],
                    "exchange": parsed["exchange"],
                    "year": parsed["year"],
                    "month": parsed["month"],
                    "is_trading": True,
                    "expire_date": None,
                }
            )

        return pd.DataFrame(contracts_list)

    except Exception as e:
        logger.error(f"获取交易所合约失败: {e}")
        return pd.DataFrame()


def _get_contracts_by_product(product, date=None, include_expired=False):
    """
    根据产品代码获取合约列表
    """
    product = product.upper()

    exchange = None
    for exch, info in CHINA_FUTURE_EXCHANGE_INFO.items():
        if product in info["products"]:
            exchange = exch
            break

    if exchange == "CFFEX":
        return _get_cffex_contracts(product, date, include_expired)
    elif exchange:
        return _get_exchange_contracts(exchange, product, date, include_expired)

    logger.warning(f"未知产品: {product}")
    return pd.DataFrame()


def _get_all_contracts(date=None, include_expired=False):
    """
    获取所有交易所的合约列表
    """
    all_contracts = []

    for exchange in CHINA_FUTURE_EXCHANGE_INFO.keys():
        df = _get_exchange_contracts(exchange, None, date, include_expired)
        if not df.empty:
            all_contracts.append(df)

    if all_contracts:
        return pd.concat(all_contracts, ignore_index=True)

    return pd.DataFrame()


def get_dominant_contract(product, date=None):
    """
    获取主力合约

    Parameters
    ----------
    product : str
        产品代码，如 'IF', 'IC', 'AU'
    date : str, optional
        查询日期

    Returns
    -------
    str
        主力合约代码

    Example
    -------
    >>> contract = get_dominant_contract('IF')
    >>> contract = get_dominant_contract('IC', date='2023-12-01')
    """
    if not _ADAPTER_AVAILABLE:
        raise ImportError("AkShare 未安装")

    product = product.upper()

    try:
        if product in INDEX_FUTURE_PRODUCT_MAP:
            return _get_index_future_dominant(product, date)
        else:
            return _get_commodity_future_dominant(product, date)

    except Exception as e:
        logger.error(f"获取主力合约失败: {e}")
        return None


def _get_index_future_dominant(product, date=None):
    """
    获取股指期货主力合约

    规则: 成交量最大的合约
    """
    contracts_df = get_future_contracts(
        product=product, date=date, include_expired=False
    )

    if contracts_df.empty:
        logger.warning(f"未找到 {product} 的合约列表")
        return None

    try:
        spot_df = _get_adapter().get_futures_spot()

        if spot_df.empty:
            trading_contracts = contracts_df[contracts_df["is_trading"]][
                "contract"
            ].tolist()
            return trading_contracts[0] if trading_contracts else None

        product_contracts = contracts_df["contract"].tolist()

        volume_data = {}
        for row in spot_df.itertuples():
            symbol = getattr(row, "symbol", "")
            volume = getattr(row, "volume", 0)

            if symbol in product_contracts and volume:
                try:
                    volume_num = float(volume) if volume else 0
                    volume_data[symbol] = volume_num
                except:
                    pass

        if volume_data:
            dominant = max(volume_data.items(), key=lambda x: x[1])
            return dominant[0]

        trading_contracts = contracts_df[contracts_df["is_trading"]][
            "contract"
        ].tolist()
        return trading_contracts[0] if trading_contracts else None

    except Exception as e:
        logger.error(f"获取股指期货主力合约失败: {e}")
        trading_contracts = contracts_df[contracts_df["is_trading"]][
            "contract"
        ].tolist()
        return trading_contracts[0] if trading_contracts else None


def _get_commodity_future_dominant(product, date=None):
    """
    获取商品期货主力合约
    """
    try:
        df = _get_adapter().get_futures_spot()

        if df is None or df.empty:
            return None

        product = product.upper()

        volume_data = {}
        for row in df.itertuples():
            symbol = getattr(row, "symbol", "")
            if not symbol.startswith(product):
                continue

            volume = getattr(row, "volume", 0)
            try:
                volume_num = float(volume) if volume else 0
                volume_data[symbol] = volume_num
            except:
                pass

        if volume_data:
            dominant = max(volume_data.items(), key=lambda x: x[1])
            return dominant[0]

        return None

    except Exception as e:
        logger.error(f"获取商品期货主力合约失败: {e}")
        return None


def get_contract_multiplier(contract_code):
    """
    获取合约乘数

    Parameters
    ----------
    contract_code : str
        合约代码，如 'IF2312', 'IC2401'

    Returns
    -------
    float
        合约乘数

    Example
    -------
    >>> multiplier = get_contract_multiplier('IF2312')  # 300
    >>> multiplier = get_contract_multiplier('IC2401')  # 200
    """
    parsed = parse_future_contract(contract_code)

    if not parsed:
        logger.warning(f"无法解析合约: {contract_code}")
        return None

    product = parsed["product"]
    exchange = parsed["exchange"]

    if exchange and exchange in CHINA_FUTURE_EXCHANGE_INFO:
        multipliers = CHINA_FUTURE_EXCHANGE_INFO[exchange]["multipliers"]
        return multipliers.get(product, None)

    return None


def get_margin_rate(contract_code):
    """
    获取保证金比例

    Parameters
    ----------
    contract_code : str
        合约代码

    Returns
    -------
    float
        保证金比例

    Example
    -------
    >>> rate = get_margin_rate('IF2312')  # 0.12
    """
    parsed = parse_future_contract(contract_code)

    if not parsed:
        logger.warning(f"无法解析合约: {contract_code}")
        return None

    product = parsed["product"]
    exchange = parsed["exchange"]

    if exchange and exchange in CHINA_FUTURE_EXCHANGE_INFO:
        margin_rates = CHINA_FUTURE_EXCHANGE_INFO[exchange]["margin_rates"]
        return margin_rates.get(product, None)

    return None


def calculate_position_value(price, quantity, contract_code):
    """
    计算持仓价值

    Parameters
    ----------
    price : float
        合约价格
    quantity : int
        持仓手数（正数为多头，负数为空头）
    contract_code : str
        合约代码

    Returns
    -------
    float
        持仓价值

    Example
    -------
    >>> value = calculate_position_value(4000, 10, 'IF2312')
    >>> # 价值 = 4000 * 300 * 10 = 12000000
    """
    multiplier = get_contract_multiplier(contract_code)

    if multiplier is None:
        logger.warning(f"无法获取合约乘数: {contract_code}")
        return None

    position_value = price * multiplier * abs(quantity)
    return position_value


def calculate_required_margin(price, quantity, contract_code):
    """
    计算所需保证金

    Parameters
    ----------
    price : float
        合约价格
    quantity : int
        持仓手数
    contract_code : str
        合约代码

    Returns
    -------
    float
        所需保证金

    Example
    -------
    >>> margin = calculate_required_margin(4000, 10, 'IF2312')
    >>> # 保证金 = 4000 * 300 * 10 * 0.12 = 1440000
    """
    position_value = calculate_position_value(price, quantity, contract_code)

    if position_value is None:
        return None

    margin_rate = get_margin_rate(contract_code)

    if margin_rate is None:
        logger.warning(f"无法获取保证金比例: {contract_code}")
        return None

    required_margin = position_value * margin_rate
    return required_margin


def get_future_daily(contract_code, start_date=None, end_date=None, adjust=True):
    """
    获取期货日线数据

    Parameters
    ----------
    contract_code : str
        合约代码，如 'IF2312'
    start_date : str
        起始日期 'YYYY-MM-DD'
    end_date : str
        结束日期 'YYYY-MM-DD'
    adjust : bool
        是否调整为标准格式

    Returns
    -------
    DataFrame
        columns: ['datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest', 'settle']

    Example
    -------
    >>> df = get_future_daily('IF2312', '2023-01-01', '2023-12-31')
    """
    if not _ADAPTER_AVAILABLE:
        raise ImportError("AkShare 未安装")

    try:
        contract_code = contract_code.replace(".CCFX", "")

        start_str = start_date.replace("-", "") if start_date else "20000101"
        end_str = (
            end_date.replace("-", "") if end_date else datetime.now().strftime("%Y%m%d")
        )

        df = _get_adapter().get_futures_daily(symbol=contract_code)

        if df.empty:
            logger.warning(f"未找到合约 {contract_code} 的日线数据")
            return pd.DataFrame()

        df = df.copy()

        if "date" in df.columns:
            df["datetime"] = pd.to_datetime(df["date"])
            df = df.drop(columns=["date"])
        elif "日期" in df.columns:
            df["datetime"] = pd.to_datetime(df["日期"])
            df = df.drop(columns=["日期"])

        col_map = {
            "open": "open",
            "开盘": "open",
            "high": "high",
            "最高": "high",
            "low": "low",
            "最低": "low",
            "close": "close",
            "收盘": "close",
            "volume": "volume",
            "成交量": "volume",
            "openinterest": "openinterest",
            "持仓量": "openinterest",
            "settle": "settle",
            "结算价": "settle",
        }

        for old_col, new_col in col_map.items():
            if old_col in df.columns and new_col not in df.columns:
                df[new_col] = df[old_col]

        if start_date:
            start_dt = pd.to_datetime(start_date)
            df = df[df["datetime"] >= start_dt]

        if end_date:
            end_dt = pd.to_datetime(end_date)
            df = df[df["datetime"] <= end_dt]

        df = df.sort_values("datetime").reset_index(drop=True)

        if "openinterest" not in df.columns:
            df["openinterest"] = 0

        default_cols = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "openinterest",
            "settle",
        ]
        available_cols = [c for c in default_cols if c in df.columns]
        df = df[available_cols]

        return df

    except Exception as e:
        logger.error(f"获取期货日线数据失败: {e}")
        return pd.DataFrame()


def get_future_spot(contract_code=None):
    """
    获取期货实时行情

    Parameters
    ----------
    contract_code : str, optional
        合约代码，不指定则返回所有

    Returns
    -------
    DataFrame
        columns: ['symbol', 'exchange', 'open', 'high', 'low', 'last_price', 'volume', 'openinterest', 'settle']

    Example
    -------
    >>> df = get_future_spot()
    >>> df = get_future_spot('IF2312')
    """
    if not _ADAPTER_AVAILABLE:
        raise ImportError("AkShare 未安装")

    try:
        df = _get_adapter().get_futures_spot()

        if df.empty:
            return pd.DataFrame()

        df = df.copy()

        col_map = {
            "symbol": "symbol",
            "exchange": "exchange",
            "open": "open",
            "开盘价": "open",
            "high": "high",
            "最高价": "high",
            "low": "low",
            "最低价": "low",
            "last_price": "last_price",
            "最新价": "last_price",
            "close": "close",
            "收盘价": "close",
            "volume": "volume",
            "成交量": "volume",
            "openinterest": "openinterest",
            "持仓量": "openinterest",
            "settle": "settle",
            "结算价": "settle",
        }

        for old_col, new_col in col_map.items():
            if old_col in df.columns and new_col not in df.columns:
                df[new_col] = df[old_col]

        if contract_code:
            contract_code = contract_code.replace(".CCFX", "").upper()
            df = df[df["symbol"].str.upper() == contract_code]

        default_cols = [
            "symbol",
            "exchange",
            "open",
            "high",
            "low",
            "last_price",
            "volume",
            "openinterest",
            "settle",
        ]
        available_cols = [c for c in default_cols if c in df.columns]
        df = df[available_cols]

        return df.reset_index(drop=True)

    except Exception as e:
        logger.error(f"获取期货实时行情失败: {e}")
        return pd.DataFrame()


__all__ = [
    "parse_future_contract",
    "get_future_contracts",
    "get_dominant_contract",
    "get_contract_multiplier",
    "get_margin_rate",
    "calculate_position_value",
    "calculate_required_margin",
    "get_future_daily",
    "get_future_spot",
    "CHINA_FUTURE_EXCHANGE_INFO",
    "INDEX_FUTURE_PRODUCT_MAP",
    "PRODUCT_TO_INDEX_CODE",
]

# =============================================================================
# Functions from futures_data.py that api/futures.py needs
# =============================================================================

# 期货品种代码映射 (Chinese name mapping)
FUTURE_UNDERLYING_MAP = {
    # 金融期货
    "IF": "沪深300股指期货",
    "IC": "中证500股指期货",
    "IH": "上证50股指期货",
    "IM": "中证1000股指期货",
    "T": "10年期国债期货",
    "TF": "5年期国债期货",
    "TS": "2年期国债期货",
    "TL": "30年期国债期货",
    # 商品期货
    "AU": "黄金",
    "AG": "白银",
    "CU": "铜",
    "AL": "铝",
    "ZN": "锌",
    "PB": "铅",
    "NI": "镍",
    "SN": "锡",
    "RB": "螺纹钢",
    "HC": "热轧卷板",
    "SS": "不锈钢",
    "I": "铁矿石",
    "J": "焦炭",
    "JM": "焦煤",
    "ZC": "动力煤",
    "A": "豆一",
    "B": "豆二",
    "M": "豆粕",
    "Y": "豆油",
    "P": "棕榈油",
    "C": "玉米",
    "CS": "玉米淀粉",
    "JD": "鸡蛋",
    "L": "塑料",
    "V": "PVC",
    "PP": "PP",
    "EG": "乙二醇",
    "MA": "甲醇",
    "TA": "PTA",
    "OI": "菜油",
    "RM": "菜粕",
    "SR": "白糖",
    "CF": "棉花",
}


def _infer_dominant_contract(underlying: str, date: str) -> str:
    """根据日期推算主力合约"""
    from datetime import datetime
    date_dt = datetime.strptime(date, "%Y-%m-%d")
    year = date_dt.year % 100
    month = date_dt.month

    # 期货主力合约通常是最近的交割月
    # 股指期货: 当月、下月、下季、隔季
    if underlying in ["IF", "IC", "IH", "IM"]:
        contract_month = month
        if contract_month > 15:
            contract_month = month % 12 + 1
            if month == 12:
                year += 1
        return f"{underlying}{year:02d}{contract_month:02d}"

    # 商品期货: 使用最近的活跃月份
    active_months = [1, 5, 9]
    for am in active_months:
        if am >= month:
            return f"{underlying}{year:02d}{am:02d}"

    return f"{underlying}{(year + 1):02d}01"


def _get_exchange_by_underlying(underlying: str) -> str:
    """根据品种获取交易所"""
    if underlying in ["IF", "IC", "IH", "IM", "T", "TF", "TS", "TL"]:
        return "CFFEX"
    if underlying in ["AU", "AG", "CU", "AL", "ZN", "PB", "NI", "SN", "RB", "HC", "SS"]:
        return "SHFE"
    if underlying in ["I", "J", "JM", "ZC", "A", "B", "M", "Y", "P", "C", "CS", "JD", "L", "V", "PP", "EG", "MA"]:
        return "DCE"
    if underlying in ["TA", "OI", "RM", "SR", "CF"]:
        return "CZCE"
    return "UNKNOWN"


def _get_multiplier(underlying: str) -> int:
    """获取合约乘数"""
    multipliers = {
        "IF": 300, "IC": 200, "IH": 300, "IM": 200,
        "T": 10000, "TF": 10000, "TS": 20000, "TL": 10000,
        "AU": 1000, "AG": 15, "CU": 5, "AL": 5, "ZN": 5,
        "RB": 10, "HC": 10, "I": 100, "J": 100, "JM": 60,
    }
    return multipliers.get(underlying.upper(), 10)


def get_futures_info(
    contract_code: Optional[str] = None,
    exchange: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货合约信息。

    参数
    ----
    contract_code : str, optional
        合约代码，如 'IF2401'，None 表示获取所有合约
    exchange : str, optional
        交易所代码: 'CFFEX', 'SHFE', 'DCE', 'CZCE'

    返回
    ----
    pd.DataFrame
        合约信息: code, name, exchange, multiplier
    """
    try:
        results = []
        try:
            df = _get_adapter().get_futures_daily(contract_code="IF2312")
            if df is not None and not df.empty:
                column_mapping = {
                    "合约代码": "code",
                    "合约名称": "name",
                    "交易所": "exchange",
                    "合约乘数": "multiplier",
                    "最小变动价位": "min_change",
                    "交易保证金": "trading_margin",
                }
                df = df.rename(columns=column_mapping)
                if contract_code:
                    df = df[df["code"].str.contains(contract_code, case=False, na=False)]
                if exchange:
                    df = df[df["exchange"].str.contains(exchange, case=False, na=False)]
                return df
        except Exception:
            pass

        # 使用主力合约列表
        for underlying in list(FUTURE_UNDERLYING_MAP.keys())[:10]:
            try:
                dominant = get_dominant_contract(underlying, None)
                if dominant:
                    results.append({
                        "code": dominant,
                        "name": f"{FUTURE_UNDERLYING_MAP.get(underlying, underlying)}主力",
                        "exchange": _get_exchange_by_underlying(underlying),
                        "multiplier": _get_multiplier(underlying),
                    })
            except Exception:
                continue

        if results:
            return pd.DataFrame(results)

    except Exception as e:
        warnings.warn(f"获取期货合约信息失败: {e}")

    return pd.DataFrame(columns=["code", "name", "exchange", "multiplier"])


def _generate_commodity_future_months(year: int, month: int) -> list:
    """生成商品期货合约月份"""
    months = []
    active_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    for am in active_months:
        if am >= month:
            months.append((year, am))
        else:
            months.append((year + 1, am))
        if len(months) >= 4:
            break
    if len(months) < 4:
        for am in active_months:
            if (year + 1, am) not in months:
                months.append((year + 1, am))
                if len(months) >= 4:
                    break
    return months[:4]


def _get_order_contracts(
    product: str,
    date: Optional[str] = None,
) -> list:
    """
    获取期货品种的顺序合约列表（当月/次月/当季/隔季）。

    参数
    ----
    product : str
        期货品种代码，如 'IF', 'IC', 'AU', 'AG' 等
    date : str, optional
        查询日期

    返回
    ----
    List[str]
        合约代码列表，按到期月份排序
    """
    from datetime import datetime as dt

    product = product.upper()

    if date is None:
        date = dt.now()
    else:
        date = pd.to_datetime(date)

    year = date.year % 100
    month = date.month

    if product in ["IF", "IC", "IH", "IM"]:
        contract_months = _generate_index_future_months(year, month)
    else:
        contract_months = _generate_commodity_future_months(year, month)

    contracts = []
    for y, m in contract_months:
        contract_code = f"{product}{y:02d}{m:02d}"
        contracts.append(contract_code)

    return contracts


# =============================================================================
# Re-export compatible functions from futures_data.py style
# These have different signatures than futures.py's versions, but match
# what api/futures.py expects
# =============================================================================

def get_future_contracts_list(underlying_symbol: str, exchange: Optional[str] = None) -> list:
    """
    获取期货合约列表 (list return version).

    参数
    ----
    underlying_symbol : str
        期货品种代码
    exchange : str, optional
        交易所代码

    返回
    ----
    List[str]
        合约代码列表
    """
    try:
        df = _get_adapter().get_futures_display_main(symbol=underlying_symbol)
        if df is not None and not df.empty:
            contracts = []
            code_col = None
            for col in ["symbol", "合约", "代码"]:
                if col in df.columns:
                    code_col = col
                    break
            if code_col:
                contracts = df[code_col].tolist()
            return [str(c) for c in contracts if c]
    except Exception as e:
        warnings.warn(f"获取期货合约列表失败 {underlying_symbol}: {e}")
    return []


def get_futures_daily_list(
    contract_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货日线行情 (list-based version).

    参数
    ----
    contract_code : str
        合约代码
    start_date : str, optional
        开始日期
    end_date : str, optional
        结束日期

    返回
    ----
    pd.DataFrame
        日线行情数据
    """
    try:
        df = _get_adapter().get_futures_main_em(symbol=contract_code)
        if df is not None and not df.empty:
            column_mapping = {
                "日期": "date",
                "开盘": "open",
                "最高": "high",
                "最低": "low",
                "收盘": "close",
                "成交量": "volume",
                "持仓量": "open_interest",
            }
            df = df.rename(columns=column_mapping)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                if start_date:
                    df = df[df["date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["date"] <= pd.to_datetime(end_date)]
            return df
    except Exception as e:
        warnings.warn(f"获取期货行情失败 {contract_code}: {e}")
    return pd.DataFrame()


__all__ = [
    # Original exports
    "parse_future_contract",
    "get_future_contracts",  # DataFrame version
    "get_dominant_contract",
    "get_contract_multiplier",
    "get_margin_rate",
    "calculate_position_value",
    "calculate_required_margin",
    "get_future_daily",
    "get_future_spot",
    "CHINA_FUTURE_EXCHANGE_INFO",
    "INDEX_FUTURE_PRODUCT_MAP",
    "PRODUCT_TO_INDEX_CODE",
    # Added exports from futures_data.py
    "FUTURE_UNDERLYING_MAP",
    "get_futures_info",
    "get_future_contracts_list",
    "get_futures_daily_list",
    "_infer_dominant_contract",
    "_get_exchange_by_underlying",
    "_get_multiplier",
    "_get_order_contracts",
]
