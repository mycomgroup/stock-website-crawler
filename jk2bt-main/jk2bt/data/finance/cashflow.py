"""
finance_data/cashflow.py
现金流量表数据获取模块。
参考 backtrader_base_strategy.get_cashflow_sina 的逻辑封装。
"""


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
    try:
        from jk2bt.data.sources import get_adapter
    except ImportError:
        from data_access import get_adapter

    akshare_symbol = symbol.lower() if symbol.startswith(("sh", "sz")) else symbol
    return get_adapter().get_cashflow(symbol=akshare_symbol)
