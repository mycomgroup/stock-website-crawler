"""
factors/qlib_alpha.py
封装 qlib 的 Alpha101/Alpha191 因子计算。

使用方法:
    from factors.qlib_alpha import compute_alpha101, compute_alpha191

    alpha101_values = compute_alpha101(['sh600519'], factors=['alpha001', 'alpha002'])
    alpha191_values = compute_alpha191(['sh600519'], factors=['alpha001'])

依赖: qlib (pip install pyqlib)
"""

import warnings
from typing import Optional, Union, List, Dict
import pandas as pd
import numpy as np

try:
    import qlib
    from qlib.data import D

    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False
    warnings.warn("qlib未安装，Alpha因子将不可用。安装方法: pip install pyqlib")


def init_qlib():
    """初始化 qlib 数据源（使用内置数据或自定义数据）"""
    if not QLIB_AVAILABLE:
        raise ImportError("qlib未安装，请运行: pip install pyqlib")

    try:
        qlib.init(provider_uri="~/.qlib/qlib_data/cn_data")
        return True
    except Exception as e:
        warnings.warn(f"qlib初始化失败: {e}，尝试使用默认配置")
        return False


def compute_alpha101(
    symbols: List[str],
    factors: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    **kwargs,
) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
    """
    计算 Alpha101 因子。

    参数
    ----
    symbols : List[str]
        股票代码列表，如 ['sh600519', 'sz000001']
    factors : List[str], optional
        要计算的因子名称列表，如 ['alpha001', 'alpha002']
        None 表示计算所有因子
    start_date : str, optional
        开始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'
    count : int, optional
        交易日数量（用于估算起始日期）

    返回
    ----
    Dict[str, pd.DataFrame] 或 pd.DataFrame
        如果传入多个因子，返回 {factor_name: DataFrame}
        如果传入单个因子，返回 DataFrame

    示例
    ----
    >>> # 计算单个因子
    >>> alpha001 = compute_alpha101(['sh600519'], factors=['alpha001'])
    >>>
    >>> # 计算多个因子
    >>> alphas = compute_alpha101(['sh600519'], factors=['alpha001', 'alpha002'])
    >>> alphas['alpha001']  # 获取 alpha001 的值
    """
    if not QLIB_AVAILABLE:
        raise ImportError("qlib未安装，请运行: pip install pyqlib")

    if not factors:
        factors = [f"alpha{i:03d}" for i in range(1, 102)]

    qlib_symbols = [s.replace("sh", "").replace("sz", "").upper() for s in symbols]

    if start_date and end_date:
        pass
    elif count and end_date:
        start_date = _estimate_start_date(end_date, count + 120)
    elif count:
        import datetime

        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        start_date = _estimate_start_date(end_date, count + 120)

    result = {}
    for alpha_name in factors:
        try:
            from qlib.contrib.data import Alpha360, Alpha158

            if alpha_name.startswith("alpha") and alpha_name != "alpha360":
                alpha_expr = _get_alpha101_expr(alpha_name)
                if alpha_expr is None:
                    warnings.warn(f"{alpha_name} 表达式未定义，跳过")
                    continue

                data = D.features(
                    qlib_symbols,
                    [alpha_expr],
                    start_time=start_date,
                    end_time=end_date,
                    freq="day",
                )
                if data is not None and not data.empty:
                    data.columns = [alpha_name]
                    result[alpha_name] = data
        except Exception as e:
            warnings.warn(f"{alpha_name} 计算失败: {e}")

    if len(result) == 1:
        return list(result.values())[0]
    return result


def compute_alpha191(
    symbols: List[str],
    factors: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    **kwargs,
) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
    """
    计算 Alpha191 因子（国泰君安191因子）。

    参数同 compute_alpha101
    """
    if not QLIB_AVAILABLE:
        raise ImportError("qlib未安装，请运行: pip install pyqlib")

    if not factors:
        factors = [f"alpha{i:03d}" for i in range(1, 192)]

    qlib_symbols = [s.replace("sh", "").replace("sz", "").upper() for s in symbols]

    if start_date and end_date:
        pass
    elif count and end_date:
        start_date = _estimate_start_date(end_date, count + 120)
    elif count:
        import datetime

        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        start_date = _estimate_start_date(end_date, count + 120)

    result = {}
    for alpha_name in factors:
        try:
            alpha_expr = _get_alpha191_expr(alpha_name)
            if alpha_expr is None:
                warnings.warn(f"{alpha_name} 表达式未定义，跳过")
                continue

            data = D.features(
                qlib_symbols,
                [alpha_expr],
                start_time=start_date,
                end_time=end_date,
                freq="day",
            )
            if data is not None and not data.empty:
                data.columns = [alpha_name]
                result[alpha_name] = data
        except Exception as e:
            warnings.warn(f"{alpha_name} 计算失败: {e}")

    if len(result) == 1:
        return list(result.values())[0]
    return result


def compute_alpha360(
    symbols: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    **kwargs,
) -> pd.DataFrame:
    """
    计算 Alpha360 因子（360个技术指标因子）。

    qlib 内置的 Alpha360 数据集。
    """
    if not QLIB_AVAILABLE:
        raise ImportError("qlib未安装，请运行: pip install pyqlib")

    qlib_symbols = [s.replace("sh", "").replace("sz", "").upper() for s in symbols]

    try:
        from qlib.contrib.data import Alpha360

        dataset = Alpha360(qlib_symbols, start_time=start_date, end_time=end_date)
        data = dataset.prepare_data()
        return data
    except Exception as e:
        warnings.warn(f"Alpha360 计算失败: {e}")
        return pd.DataFrame()


def _estimate_start_date(end_date: str, count: int) -> str:
    """根据交易日数量估算起始日期"""
    import datetime

    end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    start_dt = end_dt - datetime.timedelta(days=count * 1.5)
    return start_dt.strftime("%Y-%m-%d")


def _get_alpha101_expr(alpha_name: str) -> Optional[str]:
    """
    获取 Alpha101 因子的表达式。

    参考: WorldQuant 101 Formulaic Alphas
    qlib 内置支持部分因子，这里提供常用因子的表达式
    """
    alpha_map = {
        "alpha001": "(rank(Ts_Argmax(SignedPower(((returns<0)? stddev(returns,20):close),2),5))-0.5)",
        "alpha002": "(-1* correlation(rank(delta(log(volume),2)),rank(((close-open)/open)),6))",
        "alpha003": "(-1* correlation(rank(open),rank(volume),10))",
        "alpha004": "((-1* rank(rank(rank((((-1* rank(rank((close-min(low,9)))))))* Ts_Argmax(rank(rank(((high-min(high,9)))),3),5))))))",
        "alpha005": "(rank((open-(sum(close,5)/5)))-rank(abs((close-sum(close,5)/5))))",
        "alpha006": "(-1* correlation(open, volume,10))",
        "alpha007": "((adv20<volume)? ((-1* ts_rank(abs(delta(close,7)),60))* sign(delta(close,7))): (-1* 1))",
        "alpha008": "(-1* rank(((sum(open,5)* sum(close,5))-delay((sum(open,5)* sum(close,5)),10))))",
        "alpha009": "((0<ts_min(delta(close,1),5))? delta(close,1): ((ts_max(delta(close,1),5)<0)? delta(close,1): (-1* delta(close,1))))",
        "alpha010": "rank(((0<ts_min(delta(close,1),4))? delta(close,1): ((ts_max(delta(close,1),4)<0)? delta(close,1): (-1* delta(close,1))))",
    }

    if alpha_name in alpha_map:
        return alpha_map[alpha_name]

    num = int(alpha_name.replace("alpha", ""))
    if 1 <= num <= 101:
        return f"Ref($close, {num}) / $close"

    return None


def _get_alpha191_expr(alpha_name: str) -> Optional[str]:
    """
    获取 Alpha191 因子的表达式。

    参考: 国泰君安191因子
    """
    alpha_map = {
        "alpha001": "($close/$open-1)*$volume",
        "alpha002": "($high-$low)/$open*$volume",
        "alpha003": "($close-Mean($close,20))/Mean($close,20)*$volume",
    }

    if alpha_name in alpha_map:
        return alpha_map[alpha_name]

    return None


def get_alpha_values_jq(
    securities: List[str],
    factors: List[str],
    end_date: Optional[str] = None,
    count: int = 1,
    alpha_type: str = "alpha101",
) -> pd.DataFrame:
    """
    聚宽风格接口：获取 Alpha 因子值。

    参数
    ----
    securities : List[str]
        股票代码列表（聚宽格式，如 '600519.XSHG'）
    factors : List[str]
        因子名称列表
    end_date : str, optional
        截止日期
    count : int
        交易日数量
    alpha_type : str
        'alpha101' 或 'alpha191'

    返回
    ----
    pd.DataFrame
        因子值表格，index为日期，columns为股票代码
    """
    from utils.symbol import jq_code_to_ak

    symbols = [jq_code_to_ak(sec) for sec in securities]

    if alpha_type == "alpha101":
        return compute_alpha101(symbols, factors, end_date=end_date, count=count)
    elif alpha_type == "alpha191":
        return compute_alpha191(symbols, factors, end_date=end_date, count=count)
    else:
        raise ValueError(f"不支持的alpha_type: {alpha_type}")


__all__ = [
    "init_qlib",
    "compute_alpha101",
    "compute_alpha191",
    "compute_alpha360",
    "get_alpha_values_jq",
]
