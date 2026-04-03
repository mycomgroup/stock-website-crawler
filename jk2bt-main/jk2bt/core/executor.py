"""
数据加载和股票池发现模块

负责:
- 从缓存加载股票数据
- 加载分钟数据
- 策略股票池自动发现
- 静态分析策略代码识别股票需求
"""

import os
import re
import logging
import pandas as pd
import backtrader as bt

logger = logging.getLogger(__name__)

# 导入策略包装器（延迟导入避免循环依赖）
_JQStrategyWrapper = None


def _get_strategy_wrapper():
    """延迟导入策略包装器"""
    global _JQStrategyWrapper
    if _JQStrategyWrapper is None:
        try:
            from .strategy_wrapper import JQStrategyWrapper
            _JQStrategyWrapper = JQStrategyWrapper
        except ImportError:
            from jk2bt.core.strategy_wrapper import JQStrategyWrapper
            _JQStrategyWrapper = JQStrategyWrapper
    return _JQStrategyWrapper


def _load_stock_data_from_cache(stock, start_date, end_date, adjust="qfq"):
    """
    从DuckDB缓存加载股票日线数据（离线模式专用）。

    不访问网络，仅读取本地数据库。
    """
    ak_code = stock
    if stock.endswith(".XSHG"):
        ak_code = "sh" + stock[:6]
    elif stock.endswith(".XSHE"):
        ak_code = "sz" + stock[:6]
    elif not stock.startswith("sh") and not stock.startswith("sz"):
        ak_code = ("sh" if stock.startswith("6") else "sz") + stock.zfill(6)

    try:
        from .db.duckdb_manager import DuckDBManager
        db = DuckDBManager(read_only=True, use_cache=True)
        df = db.get_stock_daily(ak_code, start_date, end_date, adjust)
    except ImportError:
        from jk2bt.core.db.duckdb_manager import DuckDBManager
        db = DuckDBManager(read_only=True, use_cache=True)
        df = db.get_stock_daily(ak_code, start_date, end_date, adjust)

    if df is None or df.empty:
        return None

    df = df.copy()
    if "datetime" in df.columns:
        df = df.set_index("datetime")

    class PandasData(bt.feeds.PandasData):
        params = (
            ("datetime", None),
            ("open", "open"),
            ("high", "high"),
            ("low", "low"),
            ("close", "close"),
            ("volume", "volume"),
            ("openinterest", None),
        )

    return PandasData(dataname=df, name=stock)


def _load_minute_data(stock, start_date, end_date, frequency="5m"):
    """
    加载股票分钟数据。

    参数:
        stock: 股票代码，如 '600519.XSHG' 或 'sh600519'
        start_date: 起始日期
        end_date: 结束日期
        frequency: 分钟周期 '1m', '5m', '15m', '30m', '60m'

    返回:
        bt.feeds.PandasData 对象
    """
    ak_code = stock
    if stock.endswith(".XSHG"):
        ak_code = "sh" + stock[:6]
    elif stock.endswith(".XSHE"):
        ak_code = "sz" + stock[:6]
    elif not stock.startswith("sh") and not stock.startswith("sz"):
        ak_code = ("sh" if stock.startswith("6") else "sz") + stock.zfill(6)

    try:
        from .market_data.minute import get_stock_minute
        df = get_stock_minute(ak_code, start_date, end_date, period=frequency)
    except ImportError:
        from jk2bt.market_data.minute import get_stock_minute
        df = get_stock_minute(ak_code, start_date, end_date, period=frequency)

    if df is None or df.empty:
        return None

    df = df.copy()
    if "datetime" in df.columns:
        df = df.set_index("datetime")

    class PandasData(bt.feeds.PandasData):
        params = (
            ("datetime", None),
            ("open", "open"),
            ("high", "high"),
            ("low", "low"),
            ("close", "close"),
            ("volume", "volume"),
            ("openinterest", "openinterest"),
        )

    return PandasData(dataname=df, name=stock)


# 常用指数代码映射
_COMMON_INDICES = {
    "000300.XSHG": "沪深300",
    "000300": "沪深300",
    "399300.XSHE": "沪深300",
    "000905.XSHG": "中证500",
    "000905": "中证500",
    "399905.XSHE": "中证500",
    "000852.XSHG": "中证1000",
    "000852": "中证1000",
    "399852.XSHE": "中证1000",
    "000016.XSHG": "上证50",
    "000016": "上证50",
    "399006.XSHE": "创业板指",
    "399006": "创业板指",
    "399303.XSHE": "国证2000",
    "399303": "国证2000",
}

# 常用ETF代码映射
_COMMON_ETFS = {
    "510500.XSHG": "中证500ETF",
    "510300.XSHG": "沪深300ETF",
    "510050.XSHG": "上证50ETF",
    "512900.XSHG": "证券ETF",
    "512880.XSHG": "证券ETF",
    "518880.XSHG": "黄金ETF",
    "513100.XSHG": "纳指ETF",
    "510880.XSHG": "红利ETF",
    "159915.XSHE": "创业板ETF",
    "159919.XSHE": "沪深300ETF",
    "159949.XSHE": "创业板50ETF",
}


def _static_analyze_stock_pool(strategy_functions, strategy_source=None):
    """
    静态分析策略代码，识别股票池调用

    参数:
        strategy_functions: 策略函数字典
        strategy_source: 策略完整源代码字符串（用于ETF/指数代码识别）
    """
    discovered_stocks = set()

    # 优先使用完整源代码进行分析（因为 exec() 创建的函数无法使用 inspect.getsource）
    if strategy_source:
        source = strategy_source

        # 识别 get_index_stocks 调用
        index_patterns = [
            r'get_index_stocks\s*\(\s*["\']([^"\']+)["\']',
            r'get_index_stocks\s*\(\s*(["\'][^"\']+["\'])',
        ]
        for pattern in index_patterns:
            matches = re.findall(pattern, source)
            for match in matches:
                index_code = match.strip("'\"")
                # 标准化指数代码
                for key in _COMMON_INDICES:
                    if index_code == key or index_code.startswith(key[:6]):
                        # 尝试获取该指数成分股
                        try:
                            try:
                                from .strategy_base import get_index_stocks
                            except ImportError:
                                from jk2bt.core.strategy_base import get_index_stocks
                            stocks = get_index_stocks(key, robust=False)
                            if stocks:
                                discovered_stocks.update(stocks)
                                logger.info(f"    发现指数调用: {key} ({_COMMON_INDICES.get(key, key)}) -> {len(stocks)}只")
                        except Exception as e:
                            logger.warning(f"    获取指数{key}失败: {e}")
                        break

        # 识别 get_all_securities 调用
        if "get_all_securities" in source:
            # 如果策略使用全市场股票，尝试获取常用股票池
            try:
                try:
                    from .strategy_base import get_all_securities_jq
                except ImportError:
                    from jk2bt.core.strategy_base import get_all_securities_jq
                all_secs = get_all_securities_jq()
                if all_secs is not None and not all_secs.empty:
                    # 限制数量，只取前100只活跃股票
                    sample_stocks = list(all_secs.keys())[:100]
                    discovered_stocks.update(sample_stocks)
                    logger.info(f"    发现全市场调用: 获取 {len(sample_stocks)} 只样本股票")
            except Exception as e:
                logger.warning(f"    获取全市场股票失败: {e}")

        # 识别ETF代码 (51xxxx.XSHG, 159xxx.XSHE)
        etf_patterns = [
            r'["\']51[0-9]{4}\.[A-Z]{4}["\']',   # 沪市ETF: 510xxx, 511xxx, 512xxx...
            r'["\']159[0-9]{3}\.[A-Z]{4}["\']',  # 深市ETF: 159xxx
            r'["\']50[0-9]{4}\.[A-Z]{4}["\']',   # 沪市ETF: 50xxxx
            r'["\']51[0-9]{4}["\']',             # 不带后缀的ETF代码
            r'["\']159[0-9]{3}["\']',            # 不带后缀的深市ETF
        ]
        for pattern in etf_patterns:
            matches = re.findall(pattern, source)
            for match in matches:
                match = match.strip("'\"")
                # 补全后缀（如果需要）
                if '.' not in match:
                    if match.startswith('6') or match.startswith('5'):
                        match = match + '.XSHG'
                    else:
                        match = match + '.XSHE'
                # ETF代码直接加入股票池
                if match not in discovered_stocks:
                    discovered_stocks.add(match)
                    logger.info(f"    发现ETF代码: {match} ({_COMMON_ETFS.get(match, '未知ETF')})")

        # 识别指数代码 (000xxx.XSHG, 399xxx.XSHE)
        index_code_patterns = [
            r'["\']000[0-9]{3}\.[A-Z]{4}["\']',  # 上证指数: 000xxx
            r'["\']399[0-9]{3}\.[A-Z]{4}["\']',  # 深证指数: 399xxx
        ]
        for pattern in index_code_patterns:
            matches = re.findall(pattern, source)
            for match in matches:
                match = match.strip("'\"")
                # 指数代码需要获取成分股
                if match in _COMMON_INDICES or match[:6] in _COMMON_INDICES:
                    try:
                        try:
                            from .strategy_base import get_index_stocks
                        except ImportError:
                            from jk2bt.core.strategy_base import get_index_stocks
                        index_key = match if match in _COMMON_INDICES else match[:6]
                        stocks = get_index_stocks(index_key, robust=False)
                        if stocks:
                            discovered_stocks.update(stocks)
                            logger.info(f"    发现指数代码: {match} -> {len(stocks)}只成分股")
                    except Exception as e:
                        logger.warning(f"    获取指数{match}失败: {e}")

        # 识别直接的股票代码引用（排除已识别的ETF/指数）
        stock_patterns = [
            r'["\']([0-9]{6}\.[A-Z]{4})["\']',  # 如 '600519.XSHG'
            r'["\']([0-9]{6})["\']',  # 如 '600519'
        ]
        for pattern in stock_patterns:
            matches = re.findall(pattern, source)
            for match in matches:
                # 跳过ETF和指数代码
                if match.startswith('51') or match.startswith('159') or match.startswith('50'):
                    continue
                if match.startswith('000') or match.startswith('399'):
                    continue
                if len(match) == 6:
                    # 补全股票代码
                    if match.startswith("6"):
                        stock = match + ".XSHG"
                    else:
                        stock = match + ".XSHE"
                    if stock not in discovered_stocks:
                        discovered_stocks.add(stock)
                        logger.info(f"    发现股票代码: {stock}")
                else:
                    if match not in discovered_stocks:
                        discovered_stocks.add(match)
                        logger.info(f"    发现股票代码: {match}")

        return discovered_stocks

    # 如果没有提供源代码，尝试使用 inspect.getsource（用于兼容旧调用方式）
    import inspect
    for name, func in strategy_functions.items():
        try:
            source = inspect.getsource(func)

            # 识别 get_index_stocks 调用
            index_patterns = [
                r'get_index_stocks\s*\(\s*["\']([^"\']+)["\']',
                r'get_index_stocks\s*\(\s*(["\'][^"\']+["\'])',
            ]
            for pattern in index_patterns:
                matches = re.findall(pattern, source)
                for match in matches:
                    index_code = match.strip("'\"")
                    # 标准化指数代码
                    for key in _COMMON_INDICES:
                        if index_code == key or index_code.startswith(key[:6]):
                            # 尝试获取该指数成分股
                            try:
                                try:
                                    from .strategy_base import get_index_stocks
                                except ImportError:
                                    from jk2bt.core.strategy_base import get_index_stocks
                                stocks = get_index_stocks(key, robust=False)
                                if stocks:
                                    discovered_stocks.update(stocks)
                                    logger.info(f"    发现指数调用: {key} ({_COMMON_INDICES.get(key, key)}) -> {len(stocks)}只")
                            except Exception as e:
                                logger.warning(f"    获取指数{key}失败: {e}")
                            break

            # 识别 get_all_securities 调用
            if "get_all_securities" in source:
                # 如果策略使用全市场股票，尝试获取常用股票池
                try:
                    try:
                        from .strategy_base import get_all_securities_jq
                    except ImportError:
                        from jk2bt.core.strategy_base import get_all_securities_jq
                    all_secs = get_all_securities_jq()
                    if all_secs is not None and not all_secs.empty:
                        # 限制数量，只取前100只活跃股票
                        sample_stocks = list(all_secs.keys())[:100]
                        discovered_stocks.update(sample_stocks)
                        logger.info(f"    发现全市场调用: 获取 {len(sample_stocks)} 只样本股票")
                except Exception as e:
                    logger.warning(f"    获取全市场股票失败: {e}")

            # 识别直接的股票代码引用
            stock_patterns = [
                r'["\']([0-9]{6}\.[A-Z]{4})["\']',  # 如 '600519.XSHG'
                r'["\']([0-9]{6})["\']',  # 如 '600519'
            ]
            for pattern in stock_patterns:
                matches = re.findall(pattern, source)
                for match in matches:
                    if len(match) == 6:
                        # 补全股票代码
                        if match.startswith("6"):
                            stock = match + ".XSHG"
                        else:
                            stock = match + ".XSHE"
                        discovered_stocks.add(stock)
                    else:
                        discovered_stocks.add(match)

            # 识别ETF代码 (51xxxx.XSHG, 159xxx.XSHE)
            etf_patterns = [
                r'["\']51[0-9]{4}\.[A-Z]{4}["\']',   # 沪市ETF: 510xxx, 511xxx, 512xxx...
                r'["\']159[0-9]{3}\.[A-Z]{4}["\']',  # 深市ETF: 159xxx
                r'["\']50[0-9]{4}\.[A-Z]{4}["\']',   # 沪市ETF: 50xxxx
            ]
            for pattern in etf_patterns:
                matches = re.findall(pattern, source)
                for match in matches:
                    match = match.strip("'\"")
                    # ETF代码直接加入股票池
                    if match not in discovered_stocks:
                        discovered_stocks.add(match)
                        logger.info(f"    发现ETF代码: {match} ({_COMMON_ETFS.get(match, '未知ETF')})")

            # 识别指数代码 (000xxx.XSHG, 399xxx.XSHE)
            index_code_patterns = [
                r'["\']000[0-9]{3}\.[A-Z]{4}["\']',  # 上证指数: 000xxx
                r'["\']399[0-9]{3}\.[A-Z]{4}["\']',  # 深证指数: 399xxx
            ]
            for pattern in index_code_patterns:
                matches = re.findall(pattern, source)
                for match in matches:
                    match = match.strip("'\"")
                    # 指数代码需要获取成分股
                    if match in _COMMON_INDICES or match[:6] in _COMMON_INDICES:
                        try:
                            try:
                                from .strategy_base import get_index_stocks
                            except ImportError:
                                from jk2bt.core.strategy_base import get_index_stocks
                            index_key = match if match in _COMMON_INDICES else match[:6]
                            stocks = get_index_stocks(index_key, robust=False)
                            if stocks:
                                discovered_stocks.update(stocks)
                                logger.info(f"    发现指数代码: {match} -> {len(stocks)}只成分股")
                        except Exception as e:
                            logger.warning(f"    获取指数{match}失败: {e}")

        except Exception as e:
            pass

    return discovered_stocks


def _discover_strategy_stocks(strategy_functions, start_date, end_date, strategy_source=None):
    """
    发现策略需要的股票池

    通过静态分析和动态预运行来识别策略需要的股票。

    参数:
        strategy_functions: 策略函数字典
        start_date: 回测开始日期
        end_date: 回测结束日期
        strategy_source: 策略源代码字符串

    返回:
        set: 发现的股票代码集合
    """
    discovered_stocks = set()

    # 1. 首先进行静态分析，识别策略代码中的股票池调用
    static_discovered = _static_analyze_stock_pool(strategy_functions, strategy_source)
    if static_discovered:
        discovered_stocks.update(static_discovered)
        logger.info(f"  [静态分析] 发现股票池调用: {len(static_discovered)} 只股票")

    # 2. 动态预运行 - 设置预运行模式
    try:
        from .strategy_base import set_prerun_mode, get_prerun_stocks, clear_prerun_stocks
    except ImportError:
        from jk2bt.core.strategy_base import set_prerun_mode, get_prerun_stocks, clear_prerun_stocks

    clear_prerun_stocks()
    set_prerun_mode(True)

    dummy_dates = pd.date_range(start=start_date, periods=10, freq="B")
    dummy_df = pd.DataFrame(
        {
            "open": [100.0] * 10,
            "high": [101.0] * 10,
            "low": [99.0] * 10,
            "close": [100.0] * 10,
            "volume": [1000000] * 10,
        },
        index=dummy_dates,
    )

    class DummyData(bt.feeds.PandasData):
        params = (("datetime", None),)

    dummy_data = DummyData(dataname=dummy_df, name="DUMMY.XSHG")

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000000)
    cerebro.adddata(dummy_data)

    # 导入 JQStrategyWrapper（延迟导入）
    JQStrategyWrapper = _get_strategy_wrapper()

    cerebro.addstrategy(
        JQStrategyWrapper,
        strategy_functions=strategy_functions,
        prerun_mode=True,
        max_prerun_days=5,
        printlog=False,
    )

    try:
        results = cerebro.run()
        if results:
            strategy = results[0]
            dynamic_stocks = getattr(strategy, "_requested_stocks", set())
            if dynamic_stocks:
                discovered_stocks.update(dynamic_stocks)
                logger.info(f"  [动态预运行-下单] 发现股票: {len(dynamic_stocks)} 只")
    except Exception as e:
        logger.error(f"预运行异常: {e}")
    finally:
        # 结束预运行模式，获取全局捕获的股票
        set_prerun_mode(False)
        prerun_stocks = get_prerun_stocks()
        if prerun_stocks:
            discovered_stocks.update(prerun_stocks)
            logger.info(f"  [动态预运行-API] 发现股票: {len(prerun_stocks)} 只")

    return discovered_stocks


__all__ = [
    '_load_stock_data_from_cache',
    '_load_minute_data',
    '_static_analyze_stock_pool',
    '_discover_strategy_stocks',
    '_COMMON_INDICES',
    '_COMMON_ETFS',
]