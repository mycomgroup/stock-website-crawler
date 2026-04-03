"""
utils/data_source_backup.py
统一数据源备份系统

数据源优先级:
1. Sina (sina) - 优先使用，稳定可靠
2. 东方财富 (east_money) - 备用数据源
3. Tushare (tushare) - 备用数据源 (需要 Token)
4. Baostock (baostock) - 备用数据源 (免费)
5. 本地缓存 (cache) - 最后备份

支持的数据类型:
- 股票日线: sina/east_money/tushare/baostock
- 股票分钟: east_money (无稳定备用源)
- ETF日线: sina/east_money/tushare
- ETF分钟: east_money (无稳定备用源)
- 指数成分股: sina/csindex
- 期货日线: sina (已稳定)
- 期权数据: sina (已稳定)

注意: 此模块为底层多数据源备份实现，保留顶层 akshare import 以便于各数据源函数内部直接使用。
"""

import logging
import pandas as pd
import time
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime
import warnings

# 底层多数据源备份模块：保留顶层 import 以便于各 fetcher 函数直接使用 akshare API
import akshare as ak

logger = logging.getLogger(__name__)

# 数据源状态记录
_SOURCE_STATUS: Dict[str, Dict] = {
    "sina": {"available": True, "last_error": None, "error_count": 0},
    "east_money": {"available": True, "last_error": None, "error_count": 0},
    "tushare": {"available": True, "token": None, "last_error": None, "error_count": 0},
    "baostock": {"available": True, "last_error": None, "error_count": 0},
    "csindex": {"available": True, "last_error": None, "error_count": 0},
}

# 错误计数阈值，超过后临时禁用该数据源
_ERROR_THRESHOLD = 5
# 临时禁用时间（秒）
_DISABLE_DURATION = 300

# 默认数据源优先级 (Sina 优先)
DEFAULT_STOCK_DAILY_SOURCES = ["sina", "east_money", "tushare", "baostock"]
DEFAULT_ETF_DAILY_SOURCES = ["sina", "east_money", "tushare"]
DEFAULT_INDEX_SOURCES = ["sina", "csindex"]
DEFAULT_MINUTE_SOURCES = ["east_money"]  # 分钟数据只有东方财富


def _update_source_status(source: str, success: bool, error: Optional[str] = None):
    """更新数据源状态"""
    if source not in _SOURCE_STATUS:
        return

    status = _SOURCE_STATUS[source]
    if success:
        status["available"] = True
        status["error_count"] = 0
        status["last_error"] = None
    else:
        status["error_count"] += 1
        status["last_error"] = error
        if status["error_count"] >= _ERROR_THRESHOLD:
            status["available"] = False
            logger.warning(f"数据源 {source} 被临时禁用（错误次数过多）")


def _is_source_available(source: str) -> bool:
    """检查数据源是否可用"""
    if source not in _SOURCE_STATUS:
        return True

    status = _SOURCE_STATUS[source]
    if not status["available"]:
        # 检查是否应该恢复
        if status.get("disabled_at"):
            elapsed = time.time() - status["disabled_at"]
            if elapsed > _DISABLE_DURATION:
                status["available"] = True
                status["error_count"] = 0
                logger.info(f"数据源 {source} 已恢复")

    return status["available"]


def set_tushare_token(token: str):
    """设置 Tushare API Token"""
    _SOURCE_STATUS["tushare"]["token"] = token


# ============================================================================
# 股票日线数据 - Sina 优先
# ============================================================================


def fetch_stock_daily_sina(symbol: str, start: str, end: str, adjust: str = "qfq") -> pd.DataFrame:
    """
    从新浪财经获取股票日线数据（优先数据源）

    使用 akshare.stock_zh_a_daily
    注意: Sina 数据不提供复权，返回原始价格
    """
    try:
        import akshare as ak

        code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "").zfill(6)

        # Sina 接口格式
        sina_symbol = f"sh{code}" if code.startswith("6") else f"sz{code}"

        df = ak.stock_zh_a_daily(symbol=sina_symbol)

        if df is not None and not df.empty:
            # 确保日期列是 datetime 类型
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                start_dt = pd.to_datetime(start)
                end_dt = pd.to_datetime(end)
                df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

            _update_source_status("sina", True)
            logger.info(f"[sina] 成功获取 {symbol} 日线数据 {len(df)} 条")
            return _normalize_sina_daily(df)

    except Exception as e:
        _update_source_status("sina", False, str(e))
        logger.warning(f"[Sina] 获取 {symbol} 日线失败: {e}")

    return pd.DataFrame()


def fetch_stock_daily_eastmoney(symbol: str, start: str, end: str, adjust: str = "qfq") -> pd.DataFrame:
    """
    从东方财富获取股票日线数据（备用数据源）

    使用 akshare.stock_zh_a_hist
    支持复权
    """
    import akshare as ak

    # 标准化代码格式
    code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date=start.replace("-", ""),
            end_date=end.replace("-", ""),
            adjust=adjust,
        )
        if df is not None and not df.empty:
            _update_source_status("east_money", True)
            logger.info(f"[east_money] 成功获取 {symbol} 日线数据 {len(df)} 条")
            return _normalize_stock_daily(df)
    except Exception as e:
        _update_source_status("east_money", False, str(e))
        logger.warning(f"[东方财富] 获取 {symbol} 日线失败: {e}")

    return pd.DataFrame()


def fetch_stock_daily_tushare(symbol: str, start: str, end: str, adjust: str = "qfq") -> pd.DataFrame:
    """
    从 Tushare 获取股票日线数据（备用数据源）

    需要 Tushare Token: https://tushare.pro/register
    """
    token = _SOURCE_STATUS["tushare"].get("token")
    if not token:
        logger.debug("[Tushare] 未配置 Token，跳过")
        return pd.DataFrame()

    try:
        import tushare as ts

        ts.set_token(token)
        pro = ts.pro_api()

        code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "").zfill(6)
        ts_code = f"{code}.SH" if code.startswith("6") else f"{code}.SZ"

        df = pro.daily(
            ts_code=ts_code,
            start_date=start.replace("-", ""),
            end_date=end.replace("-", ""),
        )

        if df is not None and not df.empty:
            _update_source_status("tushare", True)
            return _normalize_tushare_daily(df)

    except ImportError:
        logger.debug("[Tushare] 未安装")
    except Exception as e:
        _update_source_status("tushare", False, str(e))
        logger.warning(f"[Tushare] 获取 {symbol} 日线失败: {e}")

    return pd.DataFrame()


def fetch_stock_daily_baostock(symbol: str, start: str, end: str, adjust: str = "qfq") -> pd.DataFrame:
    """
    从 Baostock 获取股票日线数据（备用数据源）

    免费，无需注册
    """
    try:
        import baostock as bs

        # 登录
        lg = bs.login()
        if lg.error_code != "0":
            logger.warning(f"[Baostock] 登录失败: {lg.error_msg}")
            return pd.DataFrame()

        code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "").zfill(6)
        bs_code = f"sh.{code}" if code.startswith("6") else f"sz.{code}"

        # 复权类型映射
        adjust_map = {"qfq": "2", "hfq": "1", "none": "3"}
        adjust_type = adjust_map.get(adjust, "3")

        rs = bs.query_history_k_data_plus(
            bs_code,
            "date,open,high,low,close,volume,amount,adjustflag",
            start_date=start,
            end_date=end,
            frequency="d",
            adjustflag=adjust_type,
        )

        if rs.error_code != "0":
            logger.warning(f"[Baostock] 查询失败: {rs.error_msg}")
            return pd.DataFrame()

        data_list = []
        while (rs.error_code == "0") & rs.next():
            data_list.append(rs.get_row_data())

        if data_list:
            df = pd.DataFrame(data_list, columns=rs.fields)
            _update_source_status("baostock", True)
            return _normalize_baostock_daily(df)

    except ImportError:
        logger.debug("[Baostock] 未安装: pip install baostock")
    except Exception as e:
        _update_source_status("baostock", False, str(e))
        logger.warning(f"[Baostock] 获取 {symbol} 日线失败: {e}")

    return pd.DataFrame()


def get_stock_daily_with_fallback(
    symbol: str,
    start: str,
    end: str,
    adjust: str = "qfq",
    sources: List[str] = None,
    fallback_to_cache: bool = True,
    cache_getter: Optional[Callable] = None,
) -> pd.DataFrame:
    """
    带备用数据源的股票日线数据获取

    默认优先级: sina > east_money > tushare > baostock > cache
    """
    if sources is None:
        sources = DEFAULT_STOCK_DAILY_SOURCES

    source_fetchers = {
        "sina": fetch_stock_daily_sina,
        "east_money": fetch_stock_daily_eastmoney,
        "tushare": fetch_stock_daily_tushare,
        "baostock": fetch_stock_daily_baostock,
    }

    for source in sources:
        if not _is_source_available(source):
            logger.debug(f"数据源 {source} 不可用，跳过")
            continue

        fetcher = source_fetchers.get(source)
        if fetcher is None:
            continue

        try:
            df = fetcher(symbol, start, end, adjust)
            if df is not None and not df.empty:
                return df
        except Exception as e:
            logger.warning(f"[{source}] 异常: {e}")

    # 所有数据源失败，回退到本地缓存
    if fallback_to_cache and cache_getter:
        logger.info(f"[fallback] 所有数据源失败，使用本地缓存")
        try:
            df = cache_getter(symbol, start, end, adjust)
            if df is not None and not df.empty:
                return df
        except Exception as e:
            logger.error(f"本地缓存获取失败: {e}")

    return pd.DataFrame()


# ============================================================================
# ETF 数据 - Sina 优先
# ============================================================================


def fetch_etf_daily_sina(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    从新浪财经获取 ETF 日线数据（优先数据源）

    使用 akshare.fund_etf_hist_sina
    注意: Sina 需要带前缀的代码格式，如 sh510300, sz159915
    """
    try:
        import akshare as ak

        # Sina 需要带前缀的代码格式
        code = symbol.replace("sh", "").replace("sz", "").zfill(6)
        sina_symbol = f"sh{code}" if code.startswith("51") else f"sz{code}"

        df = ak.fund_etf_hist_sina(symbol=sina_symbol)

        if df is not None and not df.empty:
            # 标准化列名
            df = df.copy()
            column_map = {
                "date": "datetime",
                "open": "open",
                "high": "high",
                "low": "low",
                "close": "close",
                "volume": "volume",
                "amount": "amount",
            }

            for old, new in column_map.items():
                if old in df.columns:
                    df[new] = df[old]

            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
                start_dt = pd.to_datetime(start)
                end_dt = pd.to_datetime(end)
                df = df[(df["datetime"] >= start_dt) & (df["datetime"] <= end_dt)]

            _update_source_status("sina", True)
            logger.info(f"[sina] 成功获取 ETF {symbol} 日线数据 {len(df)} 条")
            return df

    except Exception as e:
        _update_source_status("sina", False, str(e))
        logger.warning(f"[Sina] 获取 ETF {symbol} 日线失败: {e}")

    return pd.DataFrame()


def fetch_etf_daily_eastmoney(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    从东方财富获取 ETF 日线数据（备用数据源）
    """
    try:
        import akshare as ak

        df = ak.fund_etf_hist_em(symbol=symbol)
        if df is not None and not df.empty:
            df = _normalize_etf_daily(df)
            df = df[(df["datetime"] >= pd.to_datetime(start)) & (df["datetime"] <= pd.to_datetime(end))]
            _update_source_status("east_money", True)
            logger.info(f"[east_money] 成功获取 ETF {symbol} 日线数据 {len(df)} 条")
            return df
    except Exception as e:
        _update_source_status("east_money", False, str(e))
        logger.warning(f"[东方财富] 获取 ETF {symbol} 日线失败: {e}")

    return pd.DataFrame()


def get_etf_daily_with_fallback(
    symbol: str,
    start: str,
    end: str,
    sources: List[str] = None,
    fallback_to_cache: bool = True,
    cache_getter: Optional[Callable] = None,
) -> pd.DataFrame:
    """
    带备用数据源的 ETF 日线数据获取
    """
    if sources is None:
        sources = DEFAULT_ETF_DAILY_SOURCES

    source_fetchers = {
        "sina": fetch_etf_daily_sina,
        "east_money": fetch_etf_daily_eastmoney,
    }

    for source in sources:
        if not _is_source_available(source):
            continue

        fetcher = source_fetchers.get(source)
        if fetcher is None:
            continue

        try:
            df = fetcher(symbol, start, end)
            if df is not None and not df.empty:
                return df
        except Exception as e:
            logger.warning(f"[{source}] ETF 异常: {e}")

    if fallback_to_cache and cache_getter:
        try:
            df = cache_getter(symbol, start, end)
            if df is not None and not df.empty:
                return df
        except Exception as e:
            logger.error(f"本地缓存获取失败: {e}")

    return pd.DataFrame()


# ============================================================================
# 分钟数据 - 仅东方财富
# ============================================================================


def fetch_stock_minute_eastmoney(symbol: str, start: str, end: str, period: str = "1", adjust: str = "qfq") -> pd.DataFrame:
    """
    从东方财富获取股票分钟数据
    """
    import akshare as ak

    code = symbol.replace("sh", "").replace("sz", "").replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = ak.stock_zh_a_hist_min_em(
            symbol=code,
            period=period,
            start_date=start,
            end_date=end,
            adjust=adjust,
        )
        if df is not None and not df.empty:
            _update_source_status("east_money", True)
            return _normalize_minute_data(df)
    except Exception as e:
        _update_source_status("east_money", False, str(e))
        logger.warning(f"[东方财富] 获取 {symbol} 分钟数据失败: {e}")

    return pd.DataFrame()


def get_stock_minute_with_fallback(
    symbol: str,
    start: str,
    end: str,
    period: str = "1",
    adjust: str = "qfq",
    fallback_to_cache: bool = True,
    cache_getter: Optional[Callable] = None,
) -> pd.DataFrame:
    """
    带备用数据源的分钟数据获取

    注意: 分钟数据备用源很少，主要依赖本地缓存
    """
    if _is_source_available("east_money"):
        df = fetch_stock_minute_eastmoney(symbol, start, end, period, adjust)
        if df is not None and not df.empty:
            return df

    if fallback_to_cache and cache_getter:
        logger.info(f"[fallback] 分钟数据源失败，使用本地缓存")
        try:
            df = cache_getter(symbol, start, end, period, adjust)
            if df is not None and not df.empty:
                return df
        except Exception as e:
            logger.error(f"分钟缓存获取失败: {e}")

    return pd.DataFrame()


# ============================================================================
# 指数成分股 - Sina 优先
# ============================================================================


def fetch_index_components_sina(index_code: str) -> pd.DataFrame:
    """
    从新浪获取成分股（优先数据源，无权重）
    """
    import akshare as ak

    code = index_code.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = ak.index_stock_cons_sina(symbol=code)
        if df is not None and not df.empty:
            _update_source_status("sina", True)
            # 新浪没有权重，使用等权重
            df = df.copy()
            df["权重"] = 100.0 / len(df)
            logger.info(f"[sina] 成功获取 {index_code} 成分股 {len(df)} 只（等权重）")
            return df
    except Exception as e:
        _update_source_status("sina", False, str(e))
        logger.warning(f"[Sina] 获取 {index_code} 成分股失败: {e}")

    return pd.DataFrame()


def fetch_index_components_csindex(index_code: str) -> pd.DataFrame:
    """
    从中证指数公司获取成分股及权重（备用数据源）
    """
    import akshare as ak

    code = index_code.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

    try:
        df = ak.index_stock_cons_weight_csindex(symbol=code)
        if df is not None and not df.empty:
            _update_source_status("csindex", True)
            logger.info(f"[csindex] 成功获取 {index_code} 成分股 {len(df)} 只")
            return df
    except Exception as e:
        _update_source_status("csindex", False, str(e))
        logger.warning(f"[中证指数] 获取 {index_code} 成分股失败: {e}")

    return pd.DataFrame()


def get_index_components_with_fallback(
    index_code: str,
    sources: List[str] = None,
    fallback_to_cache: bool = True,
    cache_getter: Optional[Callable] = None,
) -> pd.DataFrame:
    """
    带备用数据源的指数成分股获取
    """
    if sources is None:
        sources = DEFAULT_INDEX_SOURCES

    source_fetchers = {
        "sina": fetch_index_components_sina,
        "csindex": fetch_index_components_csindex,
    }

    for source in sources:
        if not _is_source_available(source):
            continue

        fetcher = source_fetchers.get(source)
        if fetcher is None:
            continue

        try:
            df = fetcher(index_code)
            if df is not None and not df.empty:
                logger.info(f"[{source}] 成功获取 {index_code} 成分股")
                return df
        except Exception as e:
            logger.warning(f"[{source}] 成分股异常: {e}")

    if fallback_to_cache and cache_getter:
        try:
            df = cache_getter(index_code)
            if df is not None and not df.empty:
                return df
        except Exception as e:
            logger.error(f"成分股缓存获取失败: {e}")

    return pd.DataFrame()


# ============================================================================
# 期货数据 - Sina 已稳定
# ============================================================================


def fetch_futures_daily_sina(contract_code: str, start: str = None, end: str = None) -> pd.DataFrame:
    """
    从新浪获取期货日线数据（Sina 已稳定）
    """
    try:
        import akshare as ak

        code = contract_code.replace(".CCFX", "")
        df = ak.futures_zh_daily_sina(symbol=code)

        if df is not None and not df.empty:
            _update_source_status("sina", True)
            df = _normalize_futures_daily(df)

            if start and "datetime" in df.columns:
                df = df[df["datetime"] >= pd.to_datetime(start)]
            if end and "datetime" in df.columns:
                df = df[df["datetime"] <= pd.to_datetime(end)]

            logger.info(f"[sina] 成功获取期货 {code} 日线数据 {len(df)} 条")
            return df
    except Exception as e:
        _update_source_status("sina", False, str(e))
        logger.warning(f"[Sina] 获取期货 {contract_code} 日线失败: {e}")

    return pd.DataFrame()


# ============================================================================
# 期权数据 - Sina 已稳定
# ============================================================================


def fetch_option_daily_sina(option_code: str, start: str = None, end: str = None) -> pd.DataFrame:
    """
    从新浪获取期权日线数据（Sina 已稳定）
    """
    try:
        import akshare as ak

        df = ak.option_sse_daily_sina(symbol=str(option_code))

        if df is not None and not df.empty:
            _update_source_status("sina", True)
            df = _normalize_option_daily(df)

            if start and "datetime" in df.columns:
                df = df[df["datetime"] >= pd.to_datetime(start)]
            if end and "datetime" in df.columns:
                df = df[df["datetime"] <= pd.to_datetime(end)]

            logger.info(f"[sina] 成功获取期权 {option_code} 日线数据 {len(df)} 条")
            return df
    except Exception as e:
        _update_source_status("sina", False, str(e))
        logger.warning(f"[Sina] 获取期权 {option_code} 日线失败: {e}")

    return pd.DataFrame()


# ============================================================================
# 北向资金 - 仅东方财富
# ============================================================================


def fetch_north_money_eastmoney() -> pd.DataFrame:
    """
    从东方财富获取北向资金数据
    """
    try:
        import akshare as ak

        df = ak.stock_em_hsgt_north_net_flow_in(symbol="北上")
        if df is not None and not df.empty:
            _update_source_status("east_money", True)
            return df
    except Exception as e:
        _update_source_status("east_money", False, str(e))
        logger.warning(f"[东方财富] 获取北向资金失败: {e}")

    return pd.DataFrame()


def get_north_money_with_fallback(
    fallback_to_cache: bool = True,
    cache_getter: Optional[Callable] = None,
) -> pd.DataFrame:
    """
    北向资金获取（无稳定备用源，主要依赖缓存）
    """
    if _is_source_available("east_money"):
        df = fetch_north_money_eastmoney()
        if df is not None and not df.empty:
            return df

    if fallback_to_cache and cache_getter:
        logger.info(f"[fallback] 北向数据源失败，使用本地缓存")
        try:
            df = cache_getter()
            if df is not None and not df.empty:
                return df
        except Exception as e:
            logger.error(f"北向缓存获取失败: {e}")

    return pd.DataFrame()


# ============================================================================
# 行业数据 - 仅东方财富
# ============================================================================


def fetch_industry_list_eastmoney() -> pd.DataFrame:
    """
    从东方财富获取行业列表
    """
    try:
        import akshare as ak

        df = ak.stock_board_industry_name_em()
        if df is not None and not df.empty:
            _update_source_status("east_money", True)
            return df
    except Exception as e:
        _update_source_status("east_money", False, str(e))
        logger.warning(f"[东方财富] 获取行业列表失败: {e}")

    return pd.DataFrame()


def fetch_industry_stocks_eastmoney(industry_name: str) -> pd.DataFrame:
    """
    从东方财富获取行业内股票
    """
    try:
        import akshare as ak

        df = ak.stock_board_industry_cons_em(symbol=industry_name)
        if df is not None and not df.empty:
            _update_source_status("east_money", True)
            return df
    except Exception as e:
        _update_source_status("east_money", False, str(e))
        logger.warning(f"[东方财富] 获取 {industry_name} 行业股票失败: {e}")

    return pd.DataFrame()


# ============================================================================
# 数据标准化函数
# ============================================================================


def _normalize_stock_daily(df: pd.DataFrame) -> pd.DataFrame:
    """标准化股票日线数据"""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    column_map = {
        "日期": "datetime",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
        "成交额": "amount",
        "date": "datetime",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
        "amount": "amount",
    }

    for old, new in column_map.items():
        if old in df.columns:
            df[new] = df[old]

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    select_cols = ["datetime", "open", "high", "low", "close", "volume"]
    if "amount" in df.columns:
        select_cols.append("amount")

    available = [c for c in select_cols if c in df.columns]
    return df[available].copy()


def _normalize_sina_daily(df: pd.DataFrame) -> pd.DataFrame:
    """标准化新浪日线数据"""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    column_map = {
        "date": "datetime",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
        "amount": "amount",
    }

    for old, new in column_map.items():
        if old in df.columns:
            df[new] = df[old]

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    select_cols = ["datetime", "open", "high", "low", "close", "volume", "amount"]
    available = [c for c in select_cols if c in df.columns]
    return df[available].copy()


def _normalize_tushare_daily(df: pd.DataFrame) -> pd.DataFrame:
    """标准化 Tushare 日线数据"""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    column_map = {
        "trade_date": "datetime",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "vol": "volume",
        "amount": "amount",
    }

    for old, new in column_map.items():
        if old in df.columns:
            df[new] = df[old]

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    select_cols = ["datetime", "open", "high", "low", "close", "volume", "amount"]
    available = [c for c in select_cols if c in df.columns]
    return df[available].copy()


def _normalize_baostock_daily(df: pd.DataFrame) -> pd.DataFrame:
    """标准化 Baostock 日线数据"""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    column_map = {
        "date": "datetime",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
        "amount": "amount",
    }

    for old, new in column_map.items():
        if old in df.columns:
            df[new] = df[old]

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # 转换数值类型
    for col in ["open", "high", "low", "close", "volume", "amount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    select_cols = ["datetime", "open", "high", "low", "close", "volume", "amount"]
    available = [c for c in select_cols if c in df.columns]
    return df[available].copy()


def _normalize_etf_daily(df: pd.DataFrame) -> pd.DataFrame:
    """标准化 ETF 日线数据"""
    return _normalize_stock_daily(df)


def _normalize_minute_data(df: pd.DataFrame) -> pd.DataFrame:
    """标准化分钟数据"""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    column_map = {
        "时间": "datetime",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
        "成交额": "money",
    }

    for old, new in column_map.items():
        if old in df.columns:
            df[new] = df[old]

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    select_cols = ["datetime", "open", "high", "low", "close", "volume", "money"]
    available = [c for c in select_cols if c in df.columns]
    return df[available].copy()


def _normalize_futures_daily(df: pd.DataFrame) -> pd.DataFrame:
    """标准化期货日线数据"""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    if "date" in df.columns:
        df["datetime"] = pd.to_datetime(df["date"])
    elif "日期" in df.columns:
        df["datetime"] = pd.to_datetime(df["日期"])

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

    default_cols = ["datetime", "open", "high", "low", "close", "volume", "openinterest", "settle"]
    available = [c for c in default_cols if c in df.columns]
    return df[available].copy()


def _normalize_option_daily(df: pd.DataFrame) -> pd.DataFrame:
    """标准化期权日线数据"""
    return _normalize_futures_daily(df)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    # 默认配置
    "DEFAULT_STOCK_DAILY_SOURCES",
    "DEFAULT_ETF_DAILY_SOURCES",
    "DEFAULT_INDEX_SOURCES",
    "DEFAULT_MINUTE_SOURCES",
    # 股票日线
    "get_stock_daily_with_fallback",
    "fetch_stock_daily_sina",
    "fetch_stock_daily_eastmoney",
    "fetch_stock_daily_tushare",
    "fetch_stock_daily_baostock",
    # ETF
    "get_etf_daily_with_fallback",
    "fetch_etf_daily_sina",
    "fetch_etf_daily_eastmoney",
    # 分钟数据
    "get_stock_minute_with_fallback",
    "fetch_stock_minute_eastmoney",
    # 指数成分股
    "get_index_components_with_fallback",
    "fetch_index_components_sina",
    "fetch_index_components_csindex",
    # 期货
    "fetch_futures_daily_sina",
    # 期权
    "fetch_option_daily_sina",
    # 北向资金
    "get_north_money_with_fallback",
    "fetch_north_money_eastmoney",
    # 行业数据
    "fetch_industry_list_eastmoney",
    "fetch_industry_stocks_eastmoney",
    # 配置
    "set_tushare_token",
    "_SOURCE_STATUS",
]