"""
market_data/industry.py
行业数据模块，使用 AkShare 获取行业分类、行业成分股、行业指数数据。

功能:
- 申万一级行业分类
- 行业成分股列表
- 行业指数行情
- 行业涨跌幅统计
"""

import warnings
from typing import Optional, List, Dict
import pandas as pd
import numpy as np
from datetime import datetime

try:
    import akshare as ak

    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    warnings.warn("akshare未安装，行业数据将不可用")


SW_LEVEL1_NAMES = [
    "农林牧渔",
    "采掘",
    "化工",
    "钢铁",
    "有色金属",
    "电子",
    "家用电器",
    "食品饮料",
    "纺织服装",
    "轻工制造",
    "医药生物",
    "公用事业",
    "交通运输",
    "房地产",
    "商业贸易",
    "休闲服务",
    "综合",
    "建筑材料",
    "建筑装饰",
    "电气设备",
    "国防军工",
    "计算机",
    "传媒",
    "通信",
    "银行",
    "非银金融",
    "汽车",
    "机械设备",
    "煤炭",
    "石油石化",
    "环保",
    "美容护理",
]

SW_LEVEL1_CODES = {
    "农林牧渔": "801010",
    "采掘": "801020",
    "化工": "801030",
    "钢铁": "801040",
    "有色金属": "801050",
    "电子": "801080",
    "家用电器": "801110",
    "食品饮料": "801120",
    "纺织服装": "801130",
    "轻工制造": "801140",
    "医药生物": "801150",
    "公用事业": "801160",
    "交通运输": "801170",
    "房地产": "801180",
    "商业贸易": "801190",
    "休闲服务": "801200",
    "综合": "801210",
    "建筑材料": "801710",
    "建筑装饰": "801720",
    "电气设备": "801730",
    "国防军工": "801740",
    "计算机": "801750",
    "传媒": "801760",
    "通信": "801770",
    "银行": "801780",
    "非银金融": "801790",
    "汽车": "801880",
    "机械设备": "801890",
}


def get_industry_classify(
    level: str = "sw_l1",
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取行业分类列表。

    参数
    ----
    level : str
        行业分类级别: 'sw_l1' (申万一级), 'sw_l2' (申万二级), 'sw_l3' (申万三级)
    date : str, optional
        查询日期，默认当前日期

    返回
    ----
    pd.DataFrame
        行业分类表，包含行业代码、行业名称等
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        if level == "sw_l1":
            df = ak.sw_index_info()
            if df is not None and not df.empty:
                df = df.rename(
                    columns={
                        "指数代码": "industry_code",
                        "指数名称": "industry_name",
                    }
                )
                return df[["industry_code", "industry_name"]]
        elif level in ["sw_l2", "sw_l3"]:
            df = ak.sw_index_info()
            return df
    except Exception as e:
        warnings.warn(f"获取行业分类失败: {e}")

    df = pd.DataFrame(
        {
            "industry_code": list(SW_LEVEL1_CODES.values()),
            "industry_name": list(SW_LEVEL1_CODES.keys()),
        }
    )
    return df


def get_industry_stocks(
    industry_name: str,
    date: Optional[str] = None,
) -> List[str]:
    """
    获取某行业的成分股列表。

    参数
    ----
    industry_name : str
        行业名称，如 '电子', '医药生物'
    date : str, optional
        查询日期

    返回
    ----
    List[str]
        股票代码列表（聚宽格式）
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    else:
        date = date.replace("-", "")

    industry_code = SW_LEVEL1_CODES.get(industry_name)
    if not industry_code:
        warnings.warn(f"未找到行业 {industry_name} 的代码")
        return []

    try:
        df = ak.sw_index_cons(index_code=industry_code)
        if df is not None and not df.empty:
            stocks = []
            for code in df["成分券代码"]:
                if code.startswith("6"):
                    stocks.append(f"{code}.XSHG")
                else:
                    stocks.append(f"{code}.XSHE")
            return stocks
    except Exception as e:
        warnings.warn(f"获取行业成分股失败: {e}")

    return []


def get_all_industry_stocks(
    date: Optional[str] = None,
) -> Dict[str, List[str]]:
    """
    获取所有行业的成分股列表。

    返回
    ----
    Dict[str, List[str]]
        {行业名称: 股票代码列表}
    """
    result = {}
    for industry_name in SW_LEVEL1_CODES.keys():
        stocks = get_industry_stocks(industry_name, date)
        if stocks:
            result[industry_name] = stocks
    return result


def get_stock_industry(
    symbol: str,
    level: str = "sw_l1",
) -> Optional[str]:
    """
    获取某股票所属的行业。

    参数
    ----
    symbol : str
        股票代码（支持多种格式）
    level : str
        行业级别

    返回
    ----
    str 或 None
        行业名称
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    code = (
        symbol.replace("sh", "")
        .replace("sz", "")
        .replace(".XSHG", "")
        .replace(".XSHE", "")
        .zfill(6)
    )

    try:
        df = ak.stock_individual_info_em(symbol=code)
        if df is not None and not df.empty:
            for item in df["item"]:
                if "行业" in item or "所属" in item:
                    industry = df[df["item"] == item]["value"].iloc[0]
                    if isinstance(industry, str):
                        for sw_name in SW_LEVEL1_CODES.keys():
                            if sw_name in industry:
                                return sw_name
                    return industry
    except Exception as e:
        warnings.warn(f"获取股票行业失败 {symbol}: {e}")

    return None


def get_industry_daily(
    industry_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取行业指数日线行情。

    参数
    ----
    industry_name : str
        行业名称
    start_date : str
        开始日期 'YYYY-MM-DD'
    end_date : str
        结束日期 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        行业指数行情数据
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    industry_code = SW_LEVEL1_CODES.get(industry_name)
    if not industry_code:
        raise ValueError(f"未找到行业 {industry_name} 的代码")

    try:
        df = ak.sw_index_daily(index_code=industry_code)
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "日期": "date",
                    "开盘": "open",
                    "最高": "high",
                    "最低": "low",
                    "收盘": "close",
                    "成交量": "volume",
                    "成交额": "amount",
                }
            )

            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]

            return df
    except Exception as e:
        warnings.warn(f"获取行业指数行情失败: {e}")

    return pd.DataFrame()


def get_industry_performance(
    date: Optional[str] = None,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    获取行业涨跌幅排名。

    参数
    ----
    date : str, optional
        查询日期
    top_n : int
        返回前N个行业

    返回
    ----
    pd.DataFrame
        行业涨跌幅排名表
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    else:
        date = date.replace("-", "")

    try:
        df = ak.sw_index_daily_spot()
        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "指数代码": "industry_code",
                    "指数名称": "industry_name",
                    "涨跌幅": "pct_change",
                }
            )

            if "pct_change" in df.columns:
                df = df.sort_values("pct_change", ascending=False)
                return df.head(top_n)
    except Exception as e:
        warnings.warn(f"获取行业涨跌幅失败: {e}")

    return pd.DataFrame()


def get_industry_stocks_performance(
    industry_name: str,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取行业内所有股票的涨跌幅。

    返回
    ----
    pd.DataFrame
        股票涨跌幅表
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    else:
        date = date.replace("-", "")

    stocks = get_industry_stocks(industry_name, date)
    if not stocks:
        return pd.DataFrame()

    try:
        codes = [s.replace(".XSHG", "").replace(".XSHE", "").zfill(6) for s in stocks]
        df = ak.stock_zh_a_spot_em()

        if df is not None and not df.empty:
            df = df[df["代码"].isin(codes)]
            df = df.rename(
                columns={
                    "代码": "code",
                    "名称": "name",
                    "涨跌幅": "pct_change",
                    "最新价": "close",
                }
            )
            return df[["code", "name", "close", "pct_change"]]
    except Exception as e:
        warnings.warn(f"获取行业内股票涨跌幅失败: {e}")

    return pd.DataFrame()


def get_market_breadth(
    date: Optional[str] = None,
    method: str = "method2",
) -> float:
    """
    计算市场宽度指标。

    参数
    ----
    date : str, optional
        查询日期
    method : str
        计算方法:
        - 'method1': 各行业及格率直接加总
        - 'method2': 行业及格率取平均（推荐）
        - 'method3': 全市场整体比例

    返回
    ----
    float
        市场宽度值（百分比，如 0.45 表示 45%）
    """
    if not AKSHARE_AVAILABLE:
        raise ImportError("请安装 akshare: pip install akshare")

    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    else:
        date = date.replace("-", "")

    breadth_values = []

    try:
        all_stocks = get_all_industry_stocks(date)

        for industry_name, stocks in all_stocks.items():
            if len(stocks) == 0:
                continue

            above_ma_count = 0
            total_count = 0

            for stock in stocks[:30]:
                try:
                    code = stock.replace(".XSHG", "").replace(".XSHE", "").zfill(6)
                    df = ak.stock_zh_a_hist(
                        symbol=code, period="daily", adjust="qfq", count=30
                    )

                    if df is not None and len(df) >= 20:
                        close = df["收盘"].iloc[-1]
                        ma20 = df["收盘"].tail(20).mean()

                        if close > ma20:
                            above_ma_count += 1
                        total_count += 1
                except Exception:
                    continue

            if total_count > 0:
                industry_breadth = above_ma_count / total_count
                breadth_values.append(industry_breadth)
    except Exception as e:
        warnings.warn(f"计算市场宽度失败: {e}")

    if len(breadth_values) == 0:
        return 0.0

    if method == "method1":
        return sum(breadth_values)
    elif method == "method2":
        return np.mean(breadth_values)
    elif method == "method3":
        return np.mean(breadth_values)

    return np.mean(breadth_values)


__all__ = [
    "get_industry_classify",
    "get_industry_stocks",
    "get_all_industry_stocks",
    "get_stock_industry",
    "get_industry_daily",
    "get_industry_performance",
    "get_industry_stocks_performance",
    "get_market_breadth",
    "SW_LEVEL1_CODES",
    "SW_LEVEL1_NAMES",
]
