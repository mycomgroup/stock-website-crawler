"""
market_data/call_auction.py
集合竞价数据获取模块

能力边界说明：
- akshare 的 stock_zh_a_hist_pre_min_em 只能获取实时竞价数据，无法获取历史日期数据
- 对于历史日期的请求：
  - 如果 simulated=False（默认），返回空 DataFrame 并标记 capability='limited'
  - 如果 simulated=True，基于日线数据模拟竞价数据，标记 capability='simulated'

模拟器算法：
- current: 使用开盘价
- volume: 使用开盘成交量 × 估算系数（默认 0.3）
- money: volume × current
- time: 09:25:00
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

CALL_AUCTION_COLUMNS = ["code", "time", "current", "volume", "money"]

AUCTION_VOLUME_RATIO = 0.3


def get_call_auction(
    stock_list,
    start_date=None,
    end_date=None,
    fields=None,
    simulated=False,
    volume_ratio=AUCTION_VOLUME_RATIO,
    **kwargs,
):
    """
    获取集合竞价数据（JQData 风格接口）

    参数
    ----
    stock_list : str or list
        股票代码，如 '000001.XSHE' 或 ['000001.XSHE', '600000.XSHG']
    start_date : str or datetime or date
        开始日期
    end_date : str or datetime or date
        结束日期
    fields : list
        需要的字段，如 ['time', 'current', 'volume', 'money']
    simulated : bool
        是否使用模拟器获取历史竞价数据（基于日线估算）
        - False（默认）: 历史日期返回空表
        - True: 历史日期使用日线数据模拟竞价
    volume_ratio : float
        竞价成交量估算系数（默认 0.3），仅在 simulated=True 时使用

    返回
    ----
    pd.DataFrame
        包含以下字段：
        - code: 股票代码（JQData 格式，如 000001.XSHE）
        - time: 时间
        - current: 竞价价格
        - volume: 竞价成交量
        - money: 竞价成交额
        - capability: 数据能力标记
          - 'full': 当日实时数据
          - 'limited': 无数据
          - 'simulated': 基于日线模拟的历史数据

    能力边界
    --------
    1. 当日实时数据：可获取（capability='full'）
    2. 历史日期数据：
       - simulated=False: 返回空 DataFrame（capability='limited'）
       - simulated=True: 返回模拟数据（capability='simulated'）
    3. 模拟数据准确性：
       - 价格基于开盘价（准确度高）
       - 成交量基于估算系数（准确度中等）
    """
    if stock_list is None:
        return _empty_call_auction_df(fields)

    if isinstance(stock_list, str):
        stock_list = [stock_list]

    if fields is None:
        fields = CALL_AUCTION_COLUMNS

    start_date = _normalize_date(start_date)
    end_date = _normalize_date(end_date)

    if start_date is None:
        start_date = datetime.now().date()

    if end_date is None:
        end_date = datetime.now().date()

    today = datetime.now().date()
    can_fetch_realtime = start_date == today and end_date == today

    if not can_fetch_realtime:
        if simulated:
            logger.info(
                f"get_call_auction: 历史日期 {start_date}~{end_date} 使用模拟器"
                f"（volume_ratio={volume_ratio})"
            )
            return _simulate_call_auction(
                stock_list, start_date, end_date, fields, volume_ratio
            )
        else:
            logger.warning(
                f"get_call_auction: 历史日期 {start_date}~{end_date} 无法获取竞价数据，"
                f"仅支持当日实时数据。启用 simulated=True 可获取模拟数据。"
            )
            return _empty_call_auction_df(fields, stock_list, capability="limited")

    df_list = []
    for stock in stock_list:
        try:
            stock_df = _fetch_realtime_auction(stock, fields)
            if stock_df is not None and not stock_df.empty:
                df_list.append(stock_df)
        except Exception as e:
            logger.warning(f"get_call_auction: {stock} 获取失败: {e}")

    if not df_list:
        return _empty_call_auction_df(fields, stock_list, capability="limited")

    result = pd.concat(df_list, ignore_index=True)

    required_base_cols = ["code", "time", "current", "volume", "money"]
    for f in required_base_cols:
        if f not in result.columns:
            result[f] = 0.0 if f != "code" else ""

    result["capability"] = "full"

    output_cols = ["code"] + [f for f in fields if f != "code"]
    output_cols += ["capability"]

    return result[output_cols]


def _normalize_date(dt):
    if dt is None:
        return None
    if hasattr(dt, "date"):
        if callable(getattr(dt, "date")):
            return dt.date()
        return dt
    if isinstance(dt, str):
        try:
            return pd.to_datetime(dt).date()
        except Exception:
            return None
    return dt


def _fetch_realtime_auction(stock, fields):
    from akshare import stock_zh_a_hist_pre_min_em

    ak_code = _jq_code_to_ak(stock)

    try:
        df = stock_zh_a_hist_pre_min_em(
            symbol=ak_code, start_time="09:15:00", end_time="09:25:00"
        )
    except Exception as e:
        logger.warning(f"_fetch_realtime_auction: {stock} akshare 调用失败: {e}")
        return None

    if df is None or df.empty:
        return None

    df = df.copy()

    df = df[
        (pd.to_datetime(df["时间"]).dt.hour == 9)
        & (pd.to_datetime(df["时间"]).dt.minute >= 15)
        & (pd.to_datetime(df["时间"]).dt.minute <= 25)
    ]

    if df.empty:
        return None

    result = pd.DataFrame()
    result["code"] = stock
    result["time"] = pd.to_datetime(df["时间"])
    result["current"] = df["最新价"].astype(float)
    result["volume"] = df["成交量"].astype(float)
    result["money"] = df["成交额"].astype(float)

    return result


def _jq_code_to_ak(jq_code):
    if "." in jq_code:
        code, suffix = jq_code.split(".", 1)
        if suffix.upper() in ("XSHG", "SH"):
            return code
        elif suffix.upper() in ("XSHE", "SZ"):
            return code
        else:
            return code
    return jq_code


def _simulate_call_auction(stock_list, start_date, end_date, fields, volume_ratio):
    """
    基于日线数据模拟历史竞价数据

    算法：
    - current: 使用开盘价
    - volume: 使用开盘成交量 × volume_ratio
    - money: volume × current
    - time: 09:25:00
    - capability: 'simulated'

    参数
    ----
    stock_list : list
        股票代码列表
    start_date : date
        开始日期
    end_date : date
        结束日期
    fields : list
        需要的字段
    volume_ratio : float
        竞价成交量估算系数

    返回
    ----
    pd.DataFrame
        模拟的竞价数据
    """
    try:
        from ..db.duckdb_manager import DuckDBManager
    except ImportError:
        from jk2bt.db.duckdb_manager import DuckDBManager

    if fields is None:
        fields = CALL_AUCTION_COLUMNS

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    db = DuckDBManager(read_only=True)

    df_list = []

    for stock in stock_list:
        try:
            db_symbol = _jq_code_to_db_symbol(stock)

            with db._get_connection(read_only=True) as conn:
                query = f"""
                    SELECT datetime, open, volume
                    FROM stock_daily
                    WHERE symbol = '{db_symbol}'
                    AND datetime >= '{start_str}'
                    AND datetime <= '{end_str}'
                    AND adjust = 'qfq'
                    ORDER BY datetime
                """

                daily_df = conn.execute(query).fetchdf()

            if daily_df is None or daily_df.empty:
                logger.warning(f"_simulate_call_auction: {stock} 无日线数据")
                continue

            for idx, row in daily_df.iterrows():
                date_val = row.get("datetime")

                if hasattr(date_val, "strftime"):
                    time_str = date_val.strftime("%Y-%m-%d 09:25:00")
                else:
                    time_str = f"{str(date_val)[:10]} 09:25:00"

                auction_time = pd.to_datetime(time_str)
                open_price = float(row.get("open", 0))
                open_volume = float(row.get("volume", 0))

                auction_volume = open_volume * volume_ratio
                auction_money = auction_volume * open_price

                sim_row = {
                    "code": stock,
                    "time": auction_time,
                    "current": open_price,
                    "volume": auction_volume,
                    "money": auction_money,
                    "capability": "simulated",
                }

                df_list.append(sim_row)

        except Exception as e:
            logger.warning(f"_simulate_call_auction: {stock} 模拟失败: {e}")
            continue

    if not df_list:
        return _empty_call_auction_df(fields, stock_list, capability="simulated")

    result = pd.DataFrame(df_list)

    output_cols = ["code"] + [f for f in fields if f != "code"] + ["capability"]

    for col in output_cols:
        if col not in result.columns:
            if col == "code":
                result[col] = ""
            elif col == "capability":
                result[col] = "simulated"
            else:
                result[col] = 0.0

    return result[output_cols]


def _jq_code_to_db_symbol(jq_code):
    """
    将 JQData 格式的股票代码转换为 DuckDB 格式

    例如：
    - '000001.XSHE' -> 'sz000001'
    - '600000.XSHG' -> 'sh600000'
    """
    if "." in jq_code:
        code, suffix = jq_code.split(".", 1)
        if suffix.upper() in ("XSHG", "SH"):
            return f"sh{code}"
        elif suffix.upper() in ("XSHE", "SZ"):
            return f"sz{code}"
        else:
            return code
    return jq_code


def _empty_call_auction_df(fields=None, stock_list=None, capability="limited"):
    if fields is None:
        fields = CALL_AUCTION_COLUMNS

    output_cols = ["code"] + [f for f in fields if f != "code"] + ["capability"]

    empty_df = pd.DataFrame(columns=output_cols)

    # 设置 capability 列的类型为 object，并标记值
    empty_df["capability"] = pd.Series(dtype="object")
    empty_df["capability"].attrs["default_value"] = capability

    return empty_df


get_call_auction_jq = get_call_auction
