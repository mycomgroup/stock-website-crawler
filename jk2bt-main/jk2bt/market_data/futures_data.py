"""
jk2bt/market_data/futures_data.py
期货数据模块

使用 AkShare 获取期货相关数据。

功能:
- 主力合约获取
- 期货合约信息
- 期货合约列表
- 期货行情数据
"""

import warnings
from typing import Optional, List, Dict
import pandas as pd
from datetime import datetime

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    warnings.warn("akshare未安装，期货数据将不可用")


# 期货品种代码映射
FUTURE_UNDERLYING_MAP = {
    # 金融期货
    "IF": "沪深300股指期货",
    "IC": "中证500股指期货",
    "IH": "上证50股指期货",
    "IM": "中证1000股指期货",
    "T": "10年期国债期货",
    "TF": "5年期国债期货",
    "TS": "2年期国债期货",
    "TL": "30年期国债期货",
    # 商品期货
    "AU": "黄金",
    "AG": "白银",
    "CU": "铜",
    "AL": "铝",
    "ZN": "锌",
    "PB": "铅",
    "NI": "镍",
    "SN": "锡",
    "RB": "螺纹钢",
    "HC": "热轧卷板",
    "SS": "不锈钢",
    "I": "铁矿石",
    "J": "焦炭",
    "JM": "焦煤",
    "ZC": "动力煤",
    "A": "豆一",
    "B": "豆二",
    "M": "豆粕",
    "Y": "豆油",
    "P": "棕榈油",
    "C": "玉米",
    "CS": "玉米淀粉",
    "JD": "鸡蛋",
    "L": "塑料",
    "V": "PVC",
    "PP": "PP",
    "EG": "乙二醇",
    "MA": "甲醇",
    "TA": "PTA",
    "OI": "菜油",
    "RM": "菜粕",
    "SR": "白糖",
    "CF": "棉花",
}


def get_dominant_contract(
    underlying_symbol: str,
    date: Optional[str] = None,
) -> Optional[str]:
    """
    获取主力合约代码。

    参数
    ----
    underlying_symbol : str
        期货品种代码，如 'IF', 'IC', 'IH', 'AU', 'CU' 等
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'

    返回
    ----
    str or None
        主力合约代码，如 'IF2401'
    """
    if not AKSHARE_AVAILABLE:
        return None

    underlying = underlying_symbol.upper()

    try:
        # 方法1: 使用新浪主力合约接口
        try:
            df = ak.futures_sina_main_sina(symbol=underlying)
            if df is not None and not df.empty:
                # 获取最新主力合约
                latest = df.iloc[-1]
                contract = latest.get("symbol", latest.get("合约", ""))
                if contract:
                    return str(contract)
        except Exception:
            pass

        # 方法2: 使用交易所数据
        try:
            # 根据品种获取主力合约
            if underlying in ["IF", "IC", "IH", "IM"]:
                # 中金所
                df = ak.futures_zx_sp_500(symbol=underlying)
                if df is not None and not df.empty:
                    # 获取成交量最大的合约
                    df = df.sort_values("成交量", ascending=False)
                    return df.iloc[0].get("合约", "")
            else:
                # 商品期货
                df = ak.futures_main_em(symbol=underlying)
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    contract = latest.get("symbol", latest.get("合约", ""))
                    if contract:
                        return str(contract)
        except Exception:
            pass

        # 方法3: 根据日期推算
        if date:
            return _infer_dominant_contract(underlying, date)

    except Exception as e:
        warnings.warn(f"获取主力合约失败 {underlying}: {e}")

    return None


def _infer_dominant_contract(underlying: str, date: str) -> str:
    """根据日期推算主力合约"""
    date_dt = datetime.strptime(date, "%Y-%m-%d")
    year = date_dt.year % 100
    month = date_dt.month

    # 期货主力合约通常是最近的交割月
    # 股指期货: 当月、下月、下季、隔季
    if underlying in ["IF", "IC", "IH", "IM"]:
        # 股指期货交割日为第三个周五
        # 主力合约通常是当月或下月
        contract_month = month
        if contract_month > 15:
            # 如果过了交割日，主力切换到下月
            contract_month = month % 12 + 1
            if month == 12:
                year += 1
        return f"{underlying}{year:02d}{contract_month:02d}"

    # 商品期货: 交割月份因品种而异
    # 简化处理，使用最近的活跃月份
    active_months = [1, 5, 9]  # 大多数商品期货的活跃月份
    for am in active_months:
        if am >= month:
            return f"{underlying}{year:02d}{am:02d}"

    # 使用下一年
    return f"{underlying}{(year + 1):02d}01"


def get_futures_info(
    contract_code: Optional[str] = None,
    exchange: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货合约信息。

    参数
    ----
    contract_code : str, optional
        合约代码，如 'IF2401'，None 表示获取所有合约
    exchange : str, optional
        交易所代码: 'CFFEX' (中金所), 'SHFE' (上期所), 'DCE' (大商所), 'CZCE' (郑商所)

    返回
    ----
    pd.DataFrame
        合约信息:
        - code: 合约代码
        - name: 合约名称
        - exchange: 交易所
        - multiplier: 合约乘数
        - min_change: 最小变动价位
        - trading_margin: 交易保证金
    """
    if not AKSHARE_AVAILABLE:
        return pd.DataFrame(columns=["code", "name", "exchange", "multiplier"])

    try:
        # 获取期货合约信息
        results = []

        # 尝试从不同接口获取
        try:
            df = ak.futures_contract_detail()
            if df is not None and not df.empty:
                # 标准化列名
                column_mapping = {
                    "合约代码": "code",
                    "合约名称": "name",
                    "交易所": "exchange",
                    "合约乘数": "multiplier",
                    "最小变动价位": "min_change",
                    "交易保证金": "trading_margin",
                }
                df = df.rename(columns=column_mapping)

                # 筛选
                if contract_code:
                    df = df[df["code"].str.contains(contract_code, case=False, na=False)]
                if exchange:
                    df = df[df["exchange"].str.contains(exchange, case=False, na=False)]

                return df
        except Exception:
            pass

        # 使用主力合约列表
        for underlying in list(FUTURE_UNDERLYING_MAP.keys())[:10]:  # 限制数量
            try:
                dominant = get_dominant_contract(underlying)
                if dominant:
                    results.append({
                        "code": dominant,
                        "name": f"{FUTURE_UNDERLYING_MAP.get(underlying, underlying)}主力",
                        "exchange": _get_exchange_by_underlying(underlying),
                        "multiplier": _get_multiplier(underlying),
                    })
            except Exception:
                continue

        if results:
            return pd.DataFrame(results)

    except Exception as e:
        warnings.warn(f"获取期货合约信息失败: {e}")

    return pd.DataFrame(columns=["code", "name", "exchange", "multiplier"])


def _get_exchange_by_underlying(underlying: str) -> str:
    """根据品种获取交易所"""
    # 中金所
    if underlying in ["IF", "IC", "IH", "IM", "T", "TF", "TS", "TL"]:
        return "CFFEX"
    # 上期所
    if underlying in ["AU", "AG", "CU", "AL", "ZN", "PB", "NI", "SN", "RB", "HC", "SS"]:
        return "SHFE"
    # 大商所
    if underlying in ["I", "J", "JM", "ZC", "A", "B", "M", "Y", "P", "C", "CS", "JD", "L", "V", "PP", "EG", "MA"]:
        return "DCE"
    # 郑商所
    if underlying in ["TA", "OI", "RM", "SR", "CF"]:
        return "CZCE"
    return "UNKNOWN"


def _get_multiplier(underlying: str) -> int:
    """获取合约乘数"""
    multipliers = {
        "IF": 300, "IC": 200, "IH": 300, "IM": 200,
        "T": 10000, "TF": 10000, "TS": 20000, "TL": 10000,
        "AU": 1000, "AG": 15, "CU": 5, "AL": 5, "ZN": 5,
        "RB": 10, "HC": 10, "I": 100, "J": 100, "JM": 60,
    }
    return multipliers.get(underlying.upper(), 10)


def get_future_contracts(
    underlying_symbol: str,
    exchange: Optional[str] = None,
) -> List[str]:
    """
    获取期货合约列表。

    参数
    ----
    underlying_symbol : str
        期货品种代码
    exchange : str, optional
        交易所代码

    返回
    ----
    List[str]
        合约代码列表
    """
    if not AKSHARE_AVAILABLE:
        return []

    try:
        # 获取品种下所有合约
        df = ak.futures_display_main_sina(symbol=underlying_symbol)

        if df is not None and not df.empty:
            contracts = []
            code_col = None
            for col in ["symbol", "合约", "代码"]:
                if col in df.columns:
                    code_col = col
                    break

            if code_col:
                contracts = df[code_col].tolist()

            return [str(c) for c in contracts if c]

    except Exception as e:
        warnings.warn(f"获取期货合约列表失败 {underlying_symbol}: {e}")

    return []


def get_futures_daily(
    contract_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货日线行情。

    参数
    ----
    contract_code : str
        合约代码
    start_date : str, optional
        开始日期
    end_date : str, optional
        结束日期

    返回
    ----
    pd.DataFrame
        日线行情数据
    """
    if not AKSHARE_AVAILABLE:
        return pd.DataFrame()

    try:
        # 使用新浪期货数据
        df = ak.futures_main_em(symbol=contract_code)

        if df is not None and not df.empty:
            # 标准化列名
            column_mapping = {
                "日期": "date",
                "开盘": "open",
                "最高": "high",
                "最低": "low",
                "收盘": "close",
                "成交量": "volume",
                "持仓量": "open_interest",
            }
            df = df.rename(columns=column_mapping)

            # 过滤日期
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                if start_date:
                    df = df[df["date"] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df["date"] <= pd.to_datetime(end_date)]

            return df

    except Exception as e:
        warnings.warn(f"获取期货行情失败 {contract_code}: {e}")

    return pd.DataFrame()


__all__ = [
    "get_dominant_contract",
    "get_futures_info",
    "get_future_contracts",
    "get_futures_daily",
    "FUTURE_UNDERLYING_MAP",
]