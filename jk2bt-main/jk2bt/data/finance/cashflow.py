"""
finance_data/cashflow.py
现金流量表数据获取模块。
参考 backtrader_base_strategy.get_cashflow_sina 的逻辑封装。
"""

from jk2bt.utils.cache import fetch_and_cache_data


def get_cashflow(symbol, force_update=False):
    """
    获取 A 股现金流量表（新浪接口），支持缓存。

    参数
    ----
    symbol     : 股票代码，支持 'sh600519'、'sz000001'、'sh600519' 等格式
    force_update: True 时强制重新下载

    返回
    ----
    pandas DataFrame，字段与新浪接口一致
    """
    akshare_symbol = symbol.lower() if symbol.startswith(("sh", "sz")) else symbol

    def download_func():
        from jk2bt.data.sources import get_adapter

        return get_adapter().get_cashflow(symbol=akshare_symbol)

    df = fetch_and_cache_data(
        symbol=symbol,
        start=None,
        end=None,
        cache_file=None,
        download_func=download_func,
        date_col=None,
        columns_map=None,
        select_cols=None,
        force_update=force_update,
    )
    return df
