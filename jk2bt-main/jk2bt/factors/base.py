"""
factors/base.py
因子计算基础设施模块。

提供：
- 因子别名标准化
- 因子注册表基类
- 缓存读写工具
- 交易日对齐与窗口切片
"""

import os
import pickle
import hashlib
import warnings
from typing import Callable, Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np

# 尝试从父模块导入交易日历，若失败则用简化版本
_TRADE_DAYS_AVAILABLE = False
_ALL_TRADE_DAYS_CACHE = None

try:
    from ..core.strategy_base import get_all_trade_days_jq

    _TRADE_DAYS_AVAILABLE = True
except ImportError:
    try:
        from jk2bt.core.strategy_base import get_all_trade_days_jq

        _TRADE_DAYS_AVAILABLE = True
    except Exception:
        _TRADE_DAYS_AVAILABLE = False
        warnings.warn("无法导入 get_all_trade_days_jq，因子模块将使用简化日期处理。")


# =====================================================================
# 因子别名标准化
# =====================================================================

# 聚宽风格 → 内部规范名 的别名映射表
FACTOR_ALIAS_MAP: Dict[str, str] = {
    # 估值因子
    "PE_ratio": "pe_ratio",
    "pe_ratio": "pe_ratio",
    "PB_ratio": "pb_ratio",
    "pb_ratio": "pb_ratio",
    "PS_ratio": "ps_ratio",
    "ps_ratio": "ps_ratio",
    "market_cap": "market_cap",
    "circulating_market_cap": "circulating_market_cap",
    "natural_log_of_market_cap": "natural_log_of_market_cap",
    "cube_of_size": "cube_of_size",
    "size": "size",
    "book_to_price_ratio": "book_to_price",
    "book_to_price": "book_to_price",
    # 财务因子
    "ROE": "roe",
    "roe": "roe",
    "ROA_TTM": "roa_ttm",
    "roa_ttm": "roa_ttm",
    "RNOA_TTM": "rnoa_ttm",
    "rnoa_ttm": "rnoa_ttm",
    "net_profit_ratio": "net_profit_ratio",
    "gross_income_ratio": "gross_income_ratio",
    "gross_profit_margin": "gross_income_ratio",
    # 技术因子 - BIAS
    "BIAS5": "bias_5",
    "BIAS10": "bias_10",
    "BIAS20": "bias_20",
    "BIAS60": "bias_60",
    "bias_5": "bias_5",
    "bias_10": "bias_10",
    "bias_20": "bias_20",
    "bias_60": "bias_60",
    # 技术因子 - EMAC
    "EMAC10": "emac_10",
    "EMAC20": "emac_20",
    "EMAC26": "emac_26",
    "EMAC60": "emac_60",
    "emac_10": "emac_10",
    "emac_20": "emac_20",
    "emac_26": "emac_26",
    "emac_60": "emac_60",
    # 技术因子 - ROC
    "ROC6": "roc_6",
    "ROC12": "roc_12",
    "ROC20": "roc_20",
    "ROC60": "roc_60",
    "ROC120": "roc_120",
    "roc_6": "roc_6",
    "roc_12": "roc_12",
    "roc_20": "roc_20",
    "roc_60": "roc_60",
    "roc_120": "roc_120",
    # 技术因子 - MAC
    "MAC60": "mac_60",
    "MAC120": "mac_120",
    "mac_60": "mac_60",
    "mac_120": "mac_120",
    # 技术因子 - VOL
    "VOL5": "vol_5",
    "VOL10": "vol_10",
    "VOL20": "vol_20",
    "VOL60": "vol_60",
    "VOL120": "vol_120",
    "VOL240": "vol_240",
    "vol_5": "vol_5",
    "vol_10": "vol_10",
    "vol_20": "vol_20",
    "vol_60": "vol_60",
    "vol_120": "vol_120",
    "vol_240": "vol_240",
    # 技术因子 - DAVOL
    "DAVOL5": "davol_5",
    "DAVOL10": "davol_10",
    "DAVOL20": "davol_20",
    "davol_5": "davol_5",
    "davol_10": "davol_10",
    "davol_20": "davol_20",
    # 技术因子 - VSTD
    "VSTD10": "vstd_10",
    "VSTD20": "vstd_20",
    "vstd_10": "vstd_10",
    "vstd_20": "vstd_20",
    # 技术因子 - VROC
    "VROC6": "vroc_6",
    "VROC12": "vroc_12",
    "vroc_6": "vroc_6",
    "vroc_12": "vroc_12",
    # 技术因子 - VEMA
    "VEMA5": "vema_5",
    "VEMA10": "vema_10",
    "VEMA12": "vema_12",
    "VEMA26": "vema_26",
    "vema_5": "vema_5",
    "vema_10": "vema_10",
    "vema_12": "vema_12",
    "vema_26": "vema_26",
    # 技术因子 - VOSC
    "VOSC": "vosc",
    "vosc": "vosc",
    # 技术因子 - TVMA/TVSTD
    "TVMA6": "tvma_6",
    "TVMA20": "tvma_20",
    "TVSTD6": "tvstd_6",
    "TVSTD20": "tvstd_20",
    "tvma_6": "tvma_6",
    "tvma_20": "tvma_20",
    "tvstd_6": "tvstd_6",
    "tvstd_20": "tvstd_20",
    # 技术因子 - CCI
    "CCI10": "cci_10",
    "CCI15": "cci_15",
    "CCI20": "cci_20",
    "CCI88": "cci_88",
    "cci_10": "cci_10",
    "cci_15": "cci_15",
    "cci_20": "cci_20",
    "cci_88": "cci_88",
    # 技术因子 - AR/BR
    "AR": "ar",
    "BR": "br",
    "ARBR": "arbr",
    "ar": "ar",
    "br": "br",
    "arbr": "arbr",
    # 技术因子 - 其他
    "WVAD": "wvad",
    "MAWVAD": "mawvad",
    "PSY": "psy",
    "VR": "vr",
    "MACD": "macd",
    "MFI14": "mfi_14",
    "money_flow_20": "money_flow_20",
    "Price1M": "price_1m",
    "Price3M": "price_3m",
    "Price1Y": "price_1y",
    "price_1m": "price_1m",
    "price_3m": "price_3m",
    "price_1y": "price_1y",
    # 技术因子 - PLRC
    "PLRC6": "plrc_6",
    "PLRC12": "plrc_12",
    "PLRC24": "plrc_24",
    "plrc_6": "plrc_6",
    "plrc_12": "plrc_12",
    "plrc_24": "plrc_24",
    # 技术因子 - Aroon
    "AroonUp": "aroon_up",
    "AroonDown": "aroon_down",
    "aroon_up": "aroon_up",
    "aroon_down": "aroon_down",
    # 技术因子 - 52周
    "fifty_two_week_close_rank": "fifty_two_week_close_rank",
    # 技术因子 - Bull/Bear
    "bull_power": "bull_power",
    "bear_power": "bear_power",
    "BBIC": "bbic",
    "bbic": "bbic",
    "Volume1M": "volume_1m",
    "volume_1m": "volume_1m",
    # 技术因子 - VPT
    "VPT": "single_day_vpt",
    "single_day_VPT": "single_day_vpt",
    "single_day_VPT_6": "single_day_vpt_6",
    "single_day_VPT_12": "single_day_vpt_12",
    "single_day_vpt": "single_day_vpt",
    "single_day_vpt_6": "single_day_vpt_6",
    "single_day_vpt_12": "single_day_vpt_12",
    # 技术因子 - TRIX
    "TRIX5": "trix_5",
    "TRIX10": "trix_10",
    "trix_5": "trix_5",
    "trix_10": "trix_10",
    # 成长因子
    "np_parent_company_owners_growth_rate": "np_parent_company_owners_growth_rate",
    "operating_revenue_growth_rate": "operating_revenue_growth_rate",
    "earnings_growth": "earnings_growth",
    # 流动性因子
    "average_share_turnover_annual": "average_share_turnover_annual",
    "share_turnover_monthly": "share_turnover_monthly",
    # 质量/杠杆因子
    "debt_to_assets": "debt_to_assets",
    "equity_to_asset_ratio": "equity_to_asset_ratio",
    "leverage": "leverage",
    "super_quick_ratio": "super_quick_ratio",
    "current_ratio": "current_ratio",
    "liquidity": "liquidity",
    "long_term_debt_to_asset_ratio": "long_term_debt_to_asset_ratio",
    "financial_liability": "financial_liability",
    "quick_ratio": "super_quick_ratio",
    # 扩展技术因子
    "BOLL_UP": "boll_up",
    "BOLL_DOWN": "boll_down",
    "boll_up": "boll_up",
    "boll_down": "boll_down",
    "ATR6": "atr_6",
    "ATR14": "atr_14",
    "atr_6": "atr_6",
    "atr_14": "atr_14",
    # 风险因子
    "Variance20": "variance_20",
    "Variance60": "variance_60",
    "Variance120": "variance_120",
    "variance_20": "variance_20",
    "variance_60": "variance_60",
    "variance_120": "variance_120",
    "Skewness20": "skewness_20",
    "Skewness60": "skewness_60",
    "Skewness120": "skewness_120",
    "skewness_20": "skewness_20",
    "skewness_60": "skewness_60",
    "skewness_120": "skewness_120",
    "Kurtosis20": "kurtosis_20",
    "Kurtosis60": "kurtosis_60",
    "Kurtosis120": "kurtosis_120",
    "kurtosis_20": "kurtosis_20",
    "kurtosis_60": "kurtosis_60",
    "kurtosis_120": "kurtosis_120",
    "Sharpe20": "sharpe_ratio_20",
    "Sharpe60": "sharpe_ratio_60",
    "Sharpe120": "sharpe_ratio_120",
    "sharpe_ratio_20": "sharpe_ratio_20",
    "sharpe_ratio_60": "sharpe_ratio_60",
    "sharpe_ratio_120": "sharpe_ratio_120",
    # CR
    "CR20": "cr_20",
    "cr_20": "cr_20",
    # Barra风格因子
    "beta": "beta",
    "momentum": "momentum",
    "residual_volatility": "residual_volatility",
    "liquidity_barra": "liquidity_barra",
    "earnings_yield": "earnings_yield",
}


def normalize_factor_name(name: str) -> str:
    """
    将外部因子名标准化为内部规范名。

    若未在别名映射中找到，则原样返回（允许后续扩展）。

    Parameters
    ----------
    name : str
        外部因子名（聚宽风格或实验脚本风格）

    Returns
    -------
    str
        内部规范名
    """
    if name in FACTOR_ALIAS_MAP:
        return FACTOR_ALIAS_MAP[name]
    name_lower = name.lower()
    if name_lower in FACTOR_ALIAS_MAP:
        return FACTOR_ALIAS_MAP[name_lower]
    for key in FACTOR_ALIAS_MAP:
        if key.lower() == name_lower:
            return FACTOR_ALIAS_MAP[key]
    return name


def normalize_factor_names(names: Union[str, List[str]]) -> List[str]:
    """
    批量标准化因子名。

    Parameters
    ----------
    names : str or list of str
        单个因子名或因子名列表

    Returns
    -------
    list of str
        标准化后的因子名列表
    """
    if isinstance(names, str):
        names = [names]
    return [normalize_factor_name(n) for n in names]


# =====================================================================
# 缓存工具
# =====================================================================


def _ensure_cache_dir(cache_dir: str) -> None:
    """确保缓存目录存在。"""
    if cache_dir and not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)


def _cache_key(
    factor_name: str, symbol: str, end_date: str, count: Optional[int] = None
) -> str:
    """
    生成缓存文件名。

    Parameters
    ----------
    factor_name : str
        因子规范名
    symbol : str
        证券代码（如 'sh600519'）
    end_date : str
        截止日期 'YYYY-MM-DD'
    count : int, optional
        窗口长度

    Returns
    -------
    str
        缓存文件名（不含目录）
    """
    key = f"{factor_name}_{symbol}_{end_date}"
    if count is not None:
        key += f"_{count}"
    # 避免路径中出现非法字符
    key = key.replace(":", "-").replace("/", "_")
    return key + ".pkl"


def load_factor_cache(
    factor_name: str,
    symbol: str,
    end_date: str,
    count: Optional[int] = None,
    cache_dir: str = "factors_cache",
) -> Optional[pd.DataFrame]:
    """
    尝试从缓存读取因子结果。

    Parameters
    ----------
    factor_name : str
        因子规范名
    symbol : str
        证券代码
    end_date : str
        截止日期
    count : int, optional
        窗口长度
    cache_dir : str
        缓存目录

    Returns
    -------
    pd.DataFrame or None
        缓存命中时返回 DataFrame，否则返回 None
    """
    _ensure_cache_dir(cache_dir)
    fname = _cache_key(factor_name, symbol, end_date, count)
    fpath = os.path.join(cache_dir, fname)
    if os.path.exists(fpath):
        try:
            with open(fpath, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            warnings.warn(f"读取因子缓存失败 {fpath}: {e}")
    return None


def save_factor_cache(
    df: pd.DataFrame,
    factor_name: str,
    symbol: str,
    end_date: str,
    count: Optional[int] = None,
    cache_dir: str = "factors_cache",
) -> None:
    """
    将因子结果写入缓存。

    Parameters
    ----------
    df : pd.DataFrame
        因子结果
    factor_name : str
        因子规范名
    symbol : str
        证券代码
    end_date : str
        截止日期
    count : int, optional
        窗口长度
    cache_dir : str
        缓存目录
    """
    _ensure_cache_dir(cache_dir)
    fname = _cache_key(factor_name, symbol, end_date, count)
    fpath = os.path.join(cache_dir, fname)
    try:
        with open(fpath, "wb") as f:
            pickle.dump(df, f)
    except Exception as e:
        warnings.warn(f"写入因子缓存失败 {fpath}: {e}")


# =====================================================================
# 交易日与窗口处理
# =====================================================================


def get_trade_days(start_date: str, end_date: str) -> List[str]:
    """
    获取指定区间内的交易日列表。

    Parameters
    ----------
    start_date : str
        起始日期 'YYYY-MM-DD'
    end_date : str
        截止日期 'YYYY-MM-DD'

    Returns
    -------
    list of str
        交易日列表（'YYYY-MM-DD' 字符串）
    """
    if _TRADE_DAYS_AVAILABLE:
        try:
            days = get_all_trade_days_jq()
            if isinstance(days, pd.DatetimeIndex):
                days = days.strftime("%Y-%m-%d").tolist()
            elif isinstance(days, list):
                days = [
                    d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10]
                    for d in days
                ]
            result = [d for d in days if start_date <= d <= end_date]
            if result:
                return result
            warnings.warn(
                f"从交易日历获取到的区间 {start_date}~{end_date} 为空，回退到工作日"
            )
        except Exception as e:
            warnings.warn(f"获取交易日失败: {e}，回退到工作日计算")

    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    return [d.strftime("%Y-%m-%d") for d in dates]


def align_to_trade_days(
    df: pd.DataFrame,
    date_col: str = "date",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fill_method: str = "ffill",
) -> pd.DataFrame:
    """
    将 DataFrame 按交易日对齐，缺失值用指定方法填充。

    Parameters
    ----------
    df : pd.DataFrame
        原始数据
    date_col : str
        日期列名
    start_date : str, optional
        起始日期
    end_date : str, optional
        截止日期
    fill_method : str
        缺失值填充方法，'ffill' / 'bfill' / 'none'

    Returns
    -------
    pd.DataFrame
        对齐后的数据
    """
    if df is None or df.empty:
        return df

    if date_col not in df.columns:
        return df

    # 确保日期为字符串格式
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")

    # 确定区间
    if start_date is None:
        start_date = df[date_col].min()
    if end_date is None:
        end_date = df[date_col].max()

    trade_days = get_trade_days(start_date, end_date)

    # 重建索引
    df = df.set_index(date_col)
    df = df.reindex(trade_days)

    if fill_method == "ffill":
        df = df.ffill()
    elif fill_method == "bfill":
        df = df.bfill()

    df.index.name = date_col
    return df.reset_index()


def slice_window(
    df: pd.DataFrame,
    end_date: str,
    count: int,
    date_col: str = "date",
) -> pd.DataFrame:
    """
    从 DataFrame 中截取指定窗口。

    Parameters
    ----------
    df : pd.DataFrame
        原始数据（已按日期排序）
    end_date : str
        截止日期
    count : int
        窗口长度（交易日数量）
    date_col : str
        日期列名

    Returns
    -------
    pd.DataFrame
        窗口内数据
    """
    if df is None or df.empty:
        return df

    df = df.copy()
    if date_col in df.columns:
        df = df[df[date_col] <= end_date]
        df = df.tail(count)
    else:
        df = df.tail(count)

    return df


# =====================================================================
# 因子注册表基类
# =====================================================================


class FactorRegistry:
    """
    因子注册表，管理因子名 → 计算函数的映射。

    使用方式：
        registry = FactorRegistry()
        registry.register('pe_ratio', compute_pe_ratio)
        registry.register('bias_5', compute_bias_5)
        ...
        func = registry.get('pe_ratio')
    """

    def __init__(self):
        self._factors: Dict[str, Callable] = {}
        self._metadata: Dict[str, Dict] = {}  # 可扩展：窗口、依赖、说明等

    def register(
        self,
        name: str,
        func: Callable,
        window: Optional[int] = None,
        dependencies: Optional[List[str]] = None,
        description: str = "",
    ) -> None:
        """
        注册因子。

        Parameters
        ----------
        name : str
            因子规范名
        func : Callable
            计算函数，签名通常为 (symbol, end_date, count, **kwargs) -> float/Series/DataFrame
        window : int, optional
            默认回溯窗口
        dependencies : list of str, optional
            数据依赖（如 'valuation', 'income', 'daily_ohlcv'）
        description : str
            因子说明
        """
        norm_name = normalize_factor_name(name)
        self._factors[norm_name] = func
        self._metadata[norm_name] = {
            "window": window,
            "dependencies": dependencies or [],
            "description": description,
        }

    def get(self, name: str) -> Optional[Callable]:
        """获取因子计算函数。"""
        norm_name = normalize_factor_name(name)
        return self._factors.get(norm_name)

    def get_metadata(self, name: str) -> Dict:
        """获取因子元信息。"""
        norm_name = normalize_factor_name(name)
        return self._metadata.get(norm_name, {})

    def list_factors(self) -> List[str]:
        """列出已注册因子名。"""
        return list(self._factors.keys())

    def is_registered(self, name: str) -> bool:
        """检查因子是否已注册。"""
        norm_name = normalize_factor_name(name)
        return norm_name in self._factors


# 全局注册表实例（供各因子模块注册）
global_factor_registry = FactorRegistry()


# =====================================================================
# 辅助：安全除法与空值处理
# =====================================================================


def safe_divide(
    a: Union[float, np.ndarray, pd.Series], b: Union[float, np.ndarray, pd.Series]
) -> Union[float, np.ndarray, pd.Series]:
    """
    安全除法，分母为零时返回 NaN。

    Parameters
    ----------
    a : float or array-like
        分子
    b : float or array-like
        分母

    Returns
    -------
    float or array-like
        商，分母为零处为 NaN
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        result = np.divide(a, b)
        if isinstance(result, np.ndarray):
            result = np.where((b == 0) | np.isnan(b), np.nan, result)
        elif isinstance(result, pd.Series):
            result = result.where((b != 0) & (~np.isnan(b)), np.nan)
        else:
            if b == 0 or np.isnan(b):
                return np.nan
    return result


def fill_missing_with_warning(
    series: pd.Series,
    method: str = "ffill",
    limit: Optional[int] = None,
    warn_threshold: float = 0.1,
) -> pd.Series:
    """
    填充缺失值并在缺失率超过阈值时发出警告。

    Parameters
    ----------
    series : pd.Series
        输入序列
    method : str
        填充方法，'ffill' / 'bfill' / 'zero' / 'mean'
    limit : int, optional
        最大连续填充数
    warn_threshold : float
        缺失率警告阈值（0-1）

    Returns
    -------
    pd.Series
        填充后序列
    """
    missing_rate = series.isna().sum() / len(series) if len(series) > 0 else 0
    if missing_rate > warn_threshold:
        warnings.warn(f"序列缺失率 {missing_rate:.1%} 超过阈值 {warn_threshold:.1%}")

    if method == "ffill":
        return series.ffill(limit=limit)
    elif method == "bfill":
        return series.bfill(limit=limit)
    elif method == "zero":
        return series.fillna(0)
    elif method == "mean":
        return series.fillna(series.mean())
    else:
        return series
