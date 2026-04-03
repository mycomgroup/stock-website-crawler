"""
finance_data/cashflow.py
现金流量表数据获取模块。
参考 backtrader_base_strategy.get_cashflow_sina 的逻辑封装。
"""

import os

try:
    from ..utils.cache import fetch_and_cache_data
except ImportError:
    from utils.cache import fetch_and_cache_data


def get_cashflow(symbol, cache_dir="finance_cache", force_update=False):
    """
    获取 A 股现金流量表（新浪接口），支持缓存。

    参数
    ----
    symbol     : 股票代码，支持 'sh600519'、'sz000001'、'sh600519' 等格式
    cache_dir  : 缓存目录
    force_update: True 时强制重新下载

    返回
    ----
    pandas DataFrame，字段与新浪接口一致
    """
    # 转为 akshare 接受的带前缀小写格式（如 sh600519）
    akshare_symbol = symbol.lower() if symbol.startswith(("sh", "sz")) else symbol
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{akshare_symbol}_cashflow_sina.pkl")

    def download_func():
        try:
            import akshare as ak
        except ImportError:
            raise ImportError("请安装 akshare: pip install akshare")
        return ak.stock_financial_report_sina(stock=akshare_symbol, symbol="现金流量表")

    df = fetch_and_cache_data(
        symbol=symbol,
        start=None,
        end=None,
        cache_file=cache_file,
        download_func=download_func,
        date_col=None,
        columns_map=None,
        select_cols=None,
        force_update=force_update,
    )
    return df
