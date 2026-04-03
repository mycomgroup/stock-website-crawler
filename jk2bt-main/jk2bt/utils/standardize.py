"""
utils/standardize.py
OHLCV 数据标准化模块。
将来自不同数据源的行情 DataFrame 统一转为 Backtrader 可直接使用的标准格式。

统一处理：
- 中文列名 -> 英文列名
- 时间戳格式统一
- 缺失字段补充
- 数据类型转换
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)

COLUMN_MAP_COMMON = {
    "日期": "datetime",
    "时间": "datetime",
    "day": "datetime",
    "开盘": "open",
    "最高": "high",
    "最低": "low",
    "收盘": "close",
    "成交量": "volume",
    "成交额": "money",
    "amount": "money",
}

COLUMN_MAP_DAILY = {
    "日期": "datetime",
    "开盘": "open",
    "最高": "high",
    "最低": "low",
    "收盘": "close",
    "成交量": "volume",
    "成交额": "amount",
}


def normalize_columns(df: pd.DataFrame, column_map: dict = None) -> pd.DataFrame:
    """
    统一列名映射（中文 -> 英文）。

    参数
    ----
    df : pd.DataFrame
        原始数据
    column_map : dict
        列名映射表，默认使用通用映射

    返回
    ----
    pd.DataFrame
        列名标准化后的 DataFrame
    """
    if column_map is None:
        column_map = COLUMN_MAP_COMMON

    df = df.copy()

    for old_col, new_col in column_map.items():
        if old_col in df.columns and new_col not in df.columns:
            df[new_col] = df[old_col]

    return df


def normalize_datetime(df: pd.DataFrame, errors: str = "coerce") -> pd.DataFrame:
    """
    统一时间戳格式处理。

    参数
    ----
    df : pd.DataFrame
        包含 datetime 列的 DataFrame
    errors : str
        pd.to_datetime 的 errors 参数

    返回
    ----
    pd.DataFrame
        datetime 列转换为 pd.Timestamp 类型
    """
    df = df.copy()

    if "datetime" not in df.columns:
        return df

    df["datetime"] = pd.to_datetime(df["datetime"], errors=errors)
    df = df.dropna(subset=["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)

    return df


def validate_required_columns(df: pd.DataFrame, required_cols: list) -> None:
    """
    验证必要列是否存在。

    参数
    ----
    df : pd.DataFrame
        数据 DataFrame
    required_cols : list
        必须存在的列名列表

    异常
    ----
    ValueError
        如果缺少必要列
    """
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"数据缺少必要列: {missing}")


def convert_numeric_columns(
    df: pd.DataFrame, numeric_cols: list, dtype: str = "float64"
) -> pd.DataFrame:
    """
    统一数值列类型转换。

    参数
    ----
    df : pd.DataFrame
        数据 DataFrame
    numeric_cols : list
        需要转换为数值的列名列表
    dtype : str
        目标数据类型

    返回
    ----
    pd.DataFrame
        数值列已转换的 DataFrame
    """
    df = df.copy()

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype(dtype)

    return df


def standardize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """
    标准化日线 OHLCV 行情 DataFrame。

    要求输入列中至少包含 datetime、open、high、low、close、volume（已经过列重命名）。

    处理内容
    --------
    1. 将 datetime 列转为 pd.Timestamp，并按升序排序
    2. 将 open/high/low/close/volume 转为 float64
    3. 若不存在 openinterest 列，补充并置 0（Backtrader 要求）
    4. 重置索引

    返回
    ----
    标准化后的 DataFrame，列：datetime/open/high/low/close/volume/amount/openinterest
    """
    df = normalize_columns(df, COLUMN_MAP_DAILY)
    df = normalize_datetime(df)

    if df.empty:
        logger.warning("日线数据为空")
        return df

    validate_required_columns(df, ["datetime", "open", "high", "low", "close"])

    numeric_cols = ["open", "high", "low", "close", "volume", "amount"]
    df = convert_numeric_columns(df, numeric_cols)

    if "volume" not in df.columns:
        df["volume"] = 0.0
    if "amount" not in df.columns:
        df["amount"] = 0.0
    if "openinterest" not in df.columns:
        df["openinterest"] = 0.0

    result_cols = [
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "openinterest",
    ]
    df = df[[c for c in result_cols if c in df.columns]]

    return df.reset_index(drop=True)


def standardize_minute_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """
    标准化分钟级 OHLCV 行情 DataFrame。

    标准输出列：datetime, open, high, low, close, volume, money, openinterest

    处理内容
    --------
    1. 使用统一列名映射（中文 -> 英文）
    2. 将 datetime 列转为 pd.Timestamp，并按升序排序
    3. 将数值列转为 float64
    4. 若不存在 money/amount 列，补充并置 0
    5. 若不存在 openinterest 列，补充并置 0（Backtrader 要求）
    6. 重置索引

    返回
    ----
    标准化后的 DataFrame，列：datetime/open/high/low/close/volume/money/openinterest
    """
    df = normalize_columns(df, COLUMN_MAP_COMMON)
    df = normalize_datetime(df)

    if df.empty:
        logger.warning("分钟数据为空")
        return df

    validate_required_columns(df, ["datetime", "open", "high", "low", "close"])

    numeric_cols = ["open", "high", "low", "close", "volume", "money", "amount"]
    df = convert_numeric_columns(df, numeric_cols)

    if "money" not in df.columns and "amount" in df.columns:
        df["money"] = df["amount"]
    elif "money" not in df.columns:
        df["money"] = 0.0

    if "volume" not in df.columns:
        df["volume"] = 0.0

    if "openinterest" not in df.columns:
        df["openinterest"] = 0.0

    result_cols = [
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "money",
        "openinterest",
    ]
    df = df[[c for c in result_cols if c in df.columns]]

    return df.reset_index(drop=True)


def standardize_financial(df: pd.DataFrame) -> pd.DataFrame:
    """
    对财务数据 DataFrame 做基础清洗：
    - 重置索引
    - 去除全空行
    """
    df = df.copy()
    df = df.dropna(how="all").reset_index(drop=True)
    return df
