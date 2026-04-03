"""
utils/cache.py
通用数据缓存模块，供 market_data/* 和 finance_data/* 子模块调用。
核心函数 fetch_and_cache_data 封装了"检查缓存→下载→保存→切片→重命名"的完整流程。
"""
import os
import pandas as pd


def fetch_and_cache_data(
    symbol,
    start,
    end,
    cache_file,
    download_func,
    date_col=None,
    columns_map=None,
    select_cols=None,
    force_update=False,
) -> pd.DataFrame:
    """
    通用缓存工具函数。

    参数
    ----
    symbol       : 股票/ETF/指数代码，仅用于日志打印
    start        : 起始日期字符串 'YYYY-MM-DD'，当 date_col 不为 None 时用于时间范围检查
    end          : 结束日期字符串 'YYYY-MM-DD'，同上
    cache_file   : pickle 缓存文件路径（含文件名）
    download_func: 无参可调用对象，调用后返回原始 DataFrame
    date_col     : 原始 DataFrame 中的日期列名，None 表示不做时间范围校验（财务数据等）
    columns_map  : dict，重命名规则 {原列名: 新列名}，None 表示不重命名
    select_cols  : list，需要保留的列名列表（重命名后），None 表示保留全部列
    force_update : True 时强制重新下载，忽略缓存

    返回
    ----
    pd.DataFrame，经过重命名和列筛选的结果
    """
    os.makedirs(os.path.dirname(cache_file) if os.path.dirname(cache_file) else '.', exist_ok=True)

    start_dt = pd.to_datetime(start) if start else None
    end_dt = pd.to_datetime(end) if end else None

    need_download = force_update or (not os.path.exists(cache_file))

    if not need_download:
        try:
            df = pd.read_pickle(cache_file)
            # 若有日期列，校验时间范围是否覆盖所需区间
            if date_col is not None and date_col in df.columns and start_dt and end_dt:
                dates = pd.to_datetime(df[date_col])
                if dates.min() > start_dt or dates.max() < end_dt:
                    print(f"[cache] {symbol} 缓存时间段不足 {dates.min().date()}~{dates.max().date()}，重新下载")
                    need_download = True
        except Exception as e:
            print(f"[cache] {symbol} 读取缓存失败: {e}，重新下载")
            need_download = True

    if need_download:
        print(f"[cache] 下载数据: {symbol}")
        df = download_func()
        if df is None or df.empty:
            raise ValueError(f"[cache] {symbol} 下载返回空数据")
        df.to_pickle(cache_file)

    # 日期范围切片
    if date_col is not None and date_col in df.columns and start_dt and end_dt:
        df = df.copy()
        df['_date_tmp'] = pd.to_datetime(df[date_col])
        df = df[(df['_date_tmp'] >= start_dt) & (df['_date_tmp'] <= end_dt)]
        df = df.drop(columns=['_date_tmp'])
        if df.empty:
            raise ValueError(f"[cache] {symbol} 在 {start}~{end} 范围内无数据")

    # 列重命名
    if columns_map:
        df = df.rename(columns=columns_map)

    # 列筛选
    if select_cols:
        keep = [c for c in select_cols if c in df.columns]
        df = df[keep]

    return df.reset_index(drop=True)
