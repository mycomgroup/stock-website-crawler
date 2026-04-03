"""
股票池工具函数
"""
import os
import sys
import logging

logger = logging.getLogger(__name__)

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

DEFAULT_STOCKS = [
    "600519.XSHG",  # 贵州茅台
    "000858.XSHE",  # 五粮液
    "000333.XSHE",  # 美的集团
    "600036.XSHG",  # 招商银行
    "601318.XSHG",  # 中国平安
    "000001.XSHE",  # 平安银行
    "601166.XSHG",  # 兴业银行
    "600000.XSHG",  # 浦发银行
    "000002.XSHE",  # 万科A
    "601398.XSHG",  # 工商银行
]

DEFAULT_INDEXES = [
    "000300.XSHG",  # 沪深300
    "000905.XSHG",  # 中证500
    "000016.XSHG",  # 上证50
]


def get_stock_pool(pool_name: str = "custom", config: dict = None) -> list:
    """
    获取股票池。
    
    参数
    ----
    pool_name : 股票池名称 (custom/core/extended)
    config : 配置字典
    
    返回
    ----
    list : 股票代码列表
    """
    if config and "stock_pool" in config:
        pool_config = config["stock_pool"].get(pool_name, {})
        
        if pool_config.get("source") == "index":
            index_code = pool_config.get("index_code")
            if index_code:
                return get_index_stocks(index_code)
        
        if pool_name in config["stock_pool"]:
            stocks = config["stock_pool"][pool_name]
            if isinstance(stocks, list):
                return stocks
    
    return DEFAULT_STOCKS


def get_index_stocks(index_code: str) -> list:
    """
    获取指数成分股。
    
    参数
    ----
    index_code : 指数代码
    
    返回
    ----
    list : 成分股代码列表
    """
    try:
        from jk2bt.market_data.index_components import get_index_components
        df = get_index_components(index_code)
        if not df.empty and "stock_code" in df.columns:
            return list(df["stock_code"].unique())
    except Exception as e:
        logger.warning(f"获取指数成分股失败 {index_code}: {e}")
    
    return DEFAULT_STOCKS


def get_all_a_stocks() -> list:
    """获取全部A股股票列表"""
    try:
        import akshare as ak
        df = ak.stock_info_a_code_name()
        stocks = []
        for code in df["code"]:
            if code.startswith("6"):
                stocks.append(code + ".XSHG")
            else:
                stocks.append(code + ".XSHE")
        return stocks
    except Exception as e:
        logger.warning(f"获取全部A股失败: {e}")
        return DEFAULT_STOCKS
