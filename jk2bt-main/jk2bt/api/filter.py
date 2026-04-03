"""
股票过滤 API 模块（权威文件）

合并自 filter_api.py 和 enhancements.py，提供完整的股票过滤功能：
- ST 股票过滤
- 停牌股票过滤
- 涨跌停过滤
- 新股过滤
- 股息率筛选
- 两融标的筛选
- 组合过滤

数据源说明:
- ST/停牌等数据为特殊数据，使用 akshare 作为数据源
- 采用延迟导入，避免顶层依赖耦合
"""

import pandas as pd
import warnings
from datetime import datetime


def _get_akshare():
    """延迟导入 akshare，避免顶层依赖耦合"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        warnings.warn("AkShare 未安装，部分过滤功能将不可用")
        return None


def _get_code_num(stock):
    """将股票代码转换为 6 位纯数字格式"""
    if stock.startswith("sh") or stock.startswith("sz"):
        stock = stock[2:]
    if stock.endswith(".XSHG") or stock.endswith(".XSHE"):
        stock = stock[:6]
    return stock.zfill(6)


# ---------------------------------------------------------------------------
# 来自 enhancements.py 的过滤函数
# ---------------------------------------------------------------------------

def filter_st(stock_list, date=None):
    """
    过滤 ST 股票

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        过滤后的股票列表（排除 ST 股票）
    """
    ak = _get_akshare()
    if ak is None:
        warnings.warn("AkShare 未安装，filter_st 不可用")
        return stock_list

    try:
        st_df = ak.stock_zh_a_st_em()

        if st_df is None or st_df.empty:
            return stock_list

        st_codes = set(st_df["代码"].astype(str).str.zfill(6).values)

        from jk2bt.core.strategy_base import format_stock_symbol_for_akshare

        clean_stocks = []
        for stock in stock_list:
            code_num = format_stock_symbol_for_akshare(stock)
            if code_num not in st_codes:
                clean_stocks.append(stock)

        return clean_stocks

    except Exception as e:
        warnings.warn(f"filter_st 失败: {e}")
        return stock_list


def filter_paused(stock_list, date=None):
    """
    过滤停牌股票

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        过滤后的股票列表（排除停牌股票）
    """
    ak = _get_akshare()
    if ak is None:
        warnings.warn("AkShare 未安装，filter_paused 不可用")
        return stock_list

    try:
        stop_df = ak.stock_zh_a_stop_em()

        if stop_df is None or stop_df.empty:
            return stock_list

        paused_codes = set(stop_df["代码"].astype(str).str.zfill(6).values)

        from jk2bt.core.strategy_base import format_stock_symbol_for_akshare

        active_stocks = []
        for stock in stock_list:
            code_num = format_stock_symbol_for_akshare(stock)
            if code_num not in paused_codes:
                active_stocks.append(stock)

        return active_stocks

    except Exception as e:
        warnings.warn(f"filter_paused 失败: {e}")
        return stock_list


def filter_limit_up(stock_list, date=None):
    """
    过滤涨停股票（当日已涨停的股票）

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        过滤后的股票列表（排除涨停股票）
    """
    from jk2bt.core.strategy_base import get_current_data

    current_data = get_current_data()

    clean_stocks = []
    for stock in stock_list:
        try:
            cd = current_data[stock]
            if cd.last_price < cd.high_limit:
                clean_stocks.append(stock)
        except Exception:
            clean_stocks.append(stock)

    return clean_stocks


def filter_limit_down(stock_list, date=None):
    """
    过滤跌停股票（当日已跌停的股票）

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        过滤后的股票列表（排除跌停股票）
    """
    from jk2bt.core.strategy_base import get_current_data

    current_data = get_current_data()

    clean_stocks = []
    for stock in stock_list:
        try:
            cd = current_data[stock]
            if cd.last_price > cd.low_limit:
                clean_stocks.append(stock)
        except Exception:
            clean_stocks.append(stock)

    return clean_stocks


def filter_new_stocks(stock_list, days=180):
    """
    过滤次新股（上市不足指定天数的股票）

    参数:
        stock_list: 股票代码列表
        days: 最小上市天数，默认 180 天

    返回:
        过滤后的股票列表
    """
    from jk2bt.core.strategy_base import get_all_securities_jq

    try:
        securities = get_all_securities_jq()

        today = datetime.now()
        cutoff_date = today - pd.Timedelta(days=days)

        clean_stocks = []
        for stock in stock_list:
            try:
                info = securities[securities["code"] == stock]
                if not info.empty:
                    start_date = pd.to_datetime(
                        info.iloc[0]["start_date"]
                        if "start_date" in info.columns
                        else info.iloc[0]["上市日期"]
                    )
                    if start_date <= cutoff_date:
                        clean_stocks.append(stock)
            except Exception:
                clean_stocks.append(stock)

        return clean_stocks

    except Exception as e:
        warnings.warn(f"filter_new_stocks 失败: {e}")
        return stock_list


# ---------------------------------------------------------------------------
# 来自 filter_api.py 的过滤函数
# ---------------------------------------------------------------------------

def get_dividend_ratio_filter_list(threshold=0.03, date=None):
    """
    股息率筛选

    返回股息率 >= threshold 的股票列表

    参数:
        threshold: 股息率阈值，默认 0.03 (3%)
        date: 查询日期（可选）

    返回:
        list: 符合条件的股票代码列表（6 位数字格式）
    """
    ak = _get_akshare()
    if ak is None:
        warnings.warn("AkShare 未安装，get_dividend_ratio_filter_list 不可用")
        return []

    try:
        df = ak.stock_dividend_cninfo()

        if df is None or df.empty:
            warnings.warn("获取股息率数据失败")
            return []

        dividend_col = None
        for col in df.columns:
            if "股息率" in str(col) or "分红" in str(col):
                dividend_col = col
                break

        if dividend_col is None:
            for col in ["股息率", "dividend_yield", "分红比例", "分红率"]:
                if col in df.columns:
                    dividend_col = col
                    break

        code_col = None
        for col in df.columns:
            if "代码" in str(col) or "code" in str(col).lower():
                code_col = col
                break
        if code_col is None:
            code_col = df.columns[0]

        if dividend_col is not None:
            dividend_values = pd.to_numeric(df[dividend_col], errors="coerce")
            sample_val = dividend_values.dropna().iloc[0] if len(dividend_values.dropna()) > 0 else 0
            is_percentage = sample_val > 1

            if is_percentage:
                mask = dividend_values >= threshold * 100
            else:
                mask = dividend_values >= threshold

            result_df = df[mask]
            return result_df[code_col].astype(str).str.zfill(6).tolist()
        else:
            warnings.warn("未找到股息率数据列")
            return []

    except Exception as e:
        warnings.warn(f"get_dividend_ratio_filter_list 失败: {e}")
        return []


def get_margine_stocks(date=None):
    """
    获取两融标的股票列表

    参数:
        date: 查询日期（可选）

    返回:
        list: 两融标的股票代码列表（6 位数字格式）
    """
    ak = _get_akshare()
    if ak is None:
        warnings.warn("AkShare 未安装，get_margine_stocks 不可用")
        return []

    try:
        all_stocks = []

        try:
            sse_df = ak.stock_margin_underlying_info_sse()
            if sse_df is not None and not sse_df.empty:
                code_col = next(
                    (c for c in sse_df.columns if "代码" in str(c) or "code" in str(c).lower()),
                    sse_df.columns[0],
                )
                all_stocks.extend(sse_df[code_col].astype(str).str.zfill(6).tolist())
        except Exception:
            pass

        try:
            szse_df = ak.stock_margin_underlying_info_szse()
            if szse_df is not None and not szse_df.empty:
                code_col = next(
                    (c for c in szse_df.columns if "代码" in str(c) or "code" in str(c).lower()),
                    szse_df.columns[0],
                )
                all_stocks.extend(szse_df[code_col].astype(str).str.zfill(6).tolist())
        except Exception:
            pass

        all_stocks = list(set(all_stocks))

        if not all_stocks:
            try:
                margin_df = ak.stock_margin_detail(
                    date=date if date else datetime.now().strftime("%Y%m%d")
                )
                if margin_df is not None and not margin_df.empty:
                    code_col = next(
                        (c for c in margin_df.columns if "代码" in str(c) or "code" in str(c).lower()),
                        margin_df.columns[0],
                    )
                    all_stocks = margin_df[code_col].astype(str).str.zfill(6).tolist()
            except Exception:
                pass

        return all_stocks

    except Exception as e:
        warnings.warn(f"get_margine_stocks 失败: {e}")
        return []


def filter_new_stock(stock_list, days=250, date=None):
    """
    过滤新股（上市不足指定天数的股票）

    参数:
        stock_list: 股票代码列表
        days: 最小上市天数，默认 250 天（约一年）
        date: 基准日期（可选）

    返回:
        list: 过滤后的股票列表（排除新股）
    """
    if not stock_list:
        return []

    try:
        from jk2bt.core.strategy_base import get_all_securities_jq

        securities = get_all_securities_jq()

        if date is None:
            ref_date = datetime.now()
        elif isinstance(date, str):
            ref_date = pd.to_datetime(date)
        else:
            ref_date = date

        cutoff_date = ref_date - pd.Timedelta(days=days)

        clean_stocks = []
        for stock in stock_list:
            try:
                code_num = _get_code_num(stock)

                info = securities[securities["code"] == stock]
                if info.empty:
                    info = securities[securities["code"] == code_num]
                if info.empty:
                    prefix = "sh" if stock.endswith(".XSHG") else "sz"
                    info = securities[securities["code"] == f"{prefix}{code_num}"]

                if not info.empty:
                    start_date_col = next(
                        (c for c in info.columns
                         if "start_date" in str(c).lower() or "上市日期" in str(c) or "start" in str(c).lower()),
                        info.columns[1] if len(info.columns) > 1 else info.columns[0],
                    )
                    start_date = pd.to_datetime(info.iloc[0][start_date_col])
                    if start_date <= cutoff_date:
                        clean_stocks.append(stock)
                else:
                    clean_stocks.append(stock)

            except Exception:
                clean_stocks.append(stock)

        return clean_stocks

    except Exception as e:
        warnings.warn(f"filter_new_stock 失败: {e}")
        return stock_list


def filter_st_stock(stock_list, date=None):
    """
    过滤 ST 股票（标准版，供策略直接调用）

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        list: 过滤后的股票列表（排除 ST 股票）
    """
    if not stock_list:
        return []

    ak = _get_akshare()
    if ak is None:
        warnings.warn("AkShare 未安装，filter_st_stock 不可用")
        return stock_list

    try:
        st_df = ak.stock_zh_a_st_em()

        if st_df is None or st_df.empty:
            return stock_list

        st_codes = set(st_df["代码"].astype(str).str.zfill(6).values)

        clean_stocks = []
        for stock in stock_list:
            code_num = _get_code_num(stock)
            if code_num not in st_codes:
                clean_stocks.append(stock)

        return clean_stocks

    except Exception as e:
        warnings.warn(f"filter_st_stock 失败: {e}")
        return stock_list


def filter_paused_stock(stock_list, date=None):
    """
    过滤停牌股票（标准版）

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        list: 过滤后的股票列表（排除停牌股票）
    """
    if not stock_list:
        return []

    ak = _get_akshare()
    if ak is None:
        warnings.warn("AkShare 未安装，filter_paused_stock 不可用")
        return stock_list

    try:
        stop_df = ak.stock_zh_a_stop_em()

        if stop_df is None or stop_df.empty:
            return stock_list

        paused_codes = set(stop_df["代码"].astype(str).str.zfill(6).values)

        clean_stocks = []
        for stock in stock_list:
            code_num = _get_code_num(stock)
            if code_num not in paused_codes:
                clean_stocks.append(stock)

        return clean_stocks

    except Exception as e:
        warnings.warn(f"filter_paused_stock 失败: {e}")
        return stock_list


def apply_common_filters(
    stock_list,
    date=None,
    filter_st=True,
    filter_paused=True,
    filter_new=True,
    new_stock_days=250,
):
    """
    应用常用筛选条件组合

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）
        filter_st: 是否过滤 ST 股票，默认 True
        filter_paused: 是否过滤停牌股票，默认 True
        filter_new: 是否过滤新股，默认 True
        new_stock_days: 新股最小上市天数，默认 250

    返回:
        list: 过滤后的股票列表
    """
    result = list(stock_list)

    if filter_st:
        result = filter_st_stock(result, date)

    if filter_paused:
        result = filter_paused_stock(result, date)

    if filter_new:
        result = filter_new_stock(result, new_stock_days, date)

    return result


def filter_limitup_stock(stock_list, date=None):
    """
    过滤涨停股票（当日已涨停的股票）

    别名: filter_limit_up

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        过滤后的股票列表（排除涨停股票）
    """
    return filter_limit_up(stock_list, date)


def filter_limitdown_stock(stock_list, date=None):
    """
    过滤跌停股票（当日已跌停的股票）

    别名: filter_limit_down

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        过滤后的股票列表（排除跌停股票）
    """
    return filter_limit_down(stock_list, date)


def filter_kcbj_stock(stock_list, date=None):
    """
    过滤科创板和北交所股票

    科创板代码以 688 开头（上海）
    北交所代码以 8 开头（北京）

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        过滤后的股票列表（排除科创板和北交所股票）
    """
    if not stock_list:
        return []

    clean_stocks = []
    for stock in stock_list:
        code_num = _get_code_num(stock)

        # 科创板: 688xxx
        if code_num.startswith('688'):
            continue

        # 北交所: 8xxxxx (4开头或8开头)
        if code_num.startswith('4') or code_num.startswith('8'):
            # 但要排除正常的沪市B股和深市股票
            # 北交所: 43xxxx, 83xxxx, 87xxxx
            if code_num.startswith('43') or code_num.startswith('83') or code_num.startswith('87'):
                continue

        clean_stocks.append(stock)

    return clean_stocks


def filter_kcb_stock(stock_list, date=None):
    """
    过滤科创板股票（仅科创板，不含北交所）

    科创板代码以 688 开头

    参数:
        stock_list: 股票代码列表
        date: 查询日期（可选）

    返回:
        过滤后的股票列表（排除科创板股票）
    """
    if not stock_list:
        return []

    clean_stocks = []
    for stock in stock_list:
        code_num = _get_code_num(stock)
        if not code_num.startswith('688'):
            clean_stocks.append(stock)

    return clean_stocks


__all__ = [
    # 来自 filter_api.py
    "get_dividend_ratio_filter_list",
    "get_margine_stocks",
    "filter_new_stock",
    "filter_st_stock",
    "filter_paused_stock",
    "apply_common_filters",
    # 来自 enhancements.py
    "filter_st",
    "filter_paused",
    "filter_limit_up",
    "filter_limit_down",
    "filter_new_stocks",
    # 新增别名和函数
    "filter_limitup_stock",
    "filter_limitdown_stock",
    "filter_kcbj_stock",
    "filter_kcb_stock",
]
