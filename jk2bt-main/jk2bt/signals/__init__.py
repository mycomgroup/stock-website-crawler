"""
signals 模块
信号检测模块 - 离散事件，择时用。

模块结构：
- __init__.py           : 信号聚合器、统一接口
- cross_signals.py      : 交叉类信号（MA/MACD/KDJ/EMA金叉死叉）
- extreme_signals.py    : 极值类信号（RSI/CCI/BIAS超买超卖）
- breakthrough_signals.py: 突破类信号（价格/成交量/布林带突破）
- divergence_signals.py : 背离类信号（MACD/RSI/KDJ背离）
- rsrs.py              : RSRS择时信号（阻力支撑相对强度）
- market_sentiment.py  : 市场情绪信号（拥挤率、GSISI、FED等）
- fields.py            : 指标数据获取

信号分类：
- 交叉信号：快线穿越慢线，从"没交叉"变"交叉"
- 极值信号：指标进入极端区域，从"正常"变"极端"
- 突破信号：价格或成交量突破阈值，从"没突破"变"突破"
- 背离信号：价格与指标走势背离
- RSRS信号：阻力支撑相对强度择时
- 情绪信号：市场情绪指标

职责边界：
- factors/ 用于选股因子（连续值，打分排序）
- signals/ 用于择时信号（离散事件，买卖触发）
- api/indicators.py 用于聚宽兼容技术指标API（MA/MACD/KDJ等）
"""

from typing import List, Dict, Optional, Union
import pandas as pd
import numpy as np

from .cross_signals import (
    detect_ma_cross,
    detect_macd_cross,
    detect_kdj_cross,
    detect_ema_cross,
    detect_vmacd_cross,
    detect_all_cross_signals,
)

from .extreme_signals import (
    detect_rsi_extreme,
    detect_cci_extreme,
    detect_bias_extreme,
    detect_kdj_extreme,
    detect_all_extreme_signals,
)

from .breakthrough_signals import (
    detect_price_breakout,
    detect_volume_breakout,
    detect_boll_breakout,
    detect_ma_breakout,
    detect_all_breakthrough_signals,
)

from .divergence_signals import (
    detect_macd_divergence,
    detect_rsi_divergence,
    detect_bear_power_divergence,
    detect_kdj_divergence,
    detect_all_divergence_signals,
)

# RSRS择时信号
from .rsrs import (
    compute_rsrs,
    compute_rsrs_signal,
    get_rsrs_for_index,
    get_current_rsrs_signal,
    compute_rsrs钝化,
    compute_rsrs_weighted,
)

# 市场情绪信号
from .market_sentiment import (
    compute_crowding_ratio,
    compute_gisi,
    compute_fed_model,
    compute_graham_index,
    compute_below_net_ratio,
    compute_new_high_ratio,
    get_all_sentiment_indicators,
)

# 指标数据获取
from .fields import (
    get_indicator_data,
    get_indicator_batch,
    get_indicator_ranking,
    filter_by_indicator,
)


# 信号检测函数映射
SIGNAL_DETECTORS = {
    # 交叉类
    "ma_cross": detect_ma_cross,
    "macd_cross": detect_macd_cross,
    "kdj_cross": detect_kdj_cross,
    "ema_cross": detect_ema_cross,
    "vmacd_cross": detect_vmacd_cross,
    # 极值类
    "rsi_extreme": detect_rsi_extreme,
    "cci_extreme": detect_cci_extreme,
    "bias_extreme": detect_bias_extreme,
    "kdj_extreme": detect_kdj_extreme,
    # 突破类
    "price_breakout": detect_price_breakout,
    "volume_breakout": detect_volume_breakout,
    "boll_breakout": detect_boll_breakout,
    "ma_breakout": detect_ma_breakout,
    # 背离类
    "macd_divergence": detect_macd_divergence,
    "rsi_divergence": detect_rsi_divergence,
    "kdj_divergence": detect_kdj_divergence,
}


class SignalDetector:
    """
    信号检测器。

    用于检测多种类型的交易信号，并提供聚合功能。

    Examples
    --------
    >>> detector = SignalDetector(['ma_cross', 'macd_cross', 'rsi_extreme'])
    >>> signals = detector.detect('sh600519', end_date='2024-12-31')
    >>> combined = detector.get_combined_signal('sh600519', method='vote')
    """

    def __init__(self, signal_types: Optional[List[str]] = None):
        """
        初始化信号检测器。

        Parameters
        ----------
        signal_types : list of str, optional
            需要检测的信号类型。可选值：
            - 'ma_cross': MA金叉/死叉
            - 'macd_cross': MACD金叉/死叉
            - 'kdj_cross': KDJ金叉/死叉
            - 'ema_cross': EMA金叉/死叉
            - 'vmacd_cross': VMACD翻红/翻绿
            - 'rsi_extreme': RSI超买超卖
            - 'cci_extreme': CCI极端
            - 'bias_extreme': BIAS极端偏离
            - 'kdj_extreme': KDJ极端
            - 'price_breakout': 价格突破
            - 'volume_breakout': 成交量突破
            - 'boll_breakout': 布林带突破
            - 'ma_breakout': 均线突破
            - 'macd_divergence': MACD背离
            - 'rsi_divergence': RSI背离
            - 'kdj_divergence': KDJ背离

            默认为全部信号类型。
        """
        if signal_types is None:
            self.signal_types = list(SIGNAL_DETECTORS.keys())
        else:
            # 验证信号类型
            invalid = [s for s in signal_types if s not in SIGNAL_DETECTORS]
            if invalid:
                raise ValueError(f"未知的信号类型: {invalid}")
            self.signal_types = signal_types

    def detect(
        self,
        symbol: str,
        end_date: Optional[str] = None,
        cache_dir: str = "stock_cache",
        force_update: bool = False,
    ) -> pd.DataFrame:
        """
        检测所有配置的信号。

        Parameters
        ----------
        symbol : str
            股票代码
        end_date : str, optional
            截止日期
        cache_dir : str
            缓存目录
        force_update : bool
            是否强制更新

        Returns
        -------
        pd.DataFrame
            columns: date, signal_type, signal, type
        """
        all_signals = []

        for signal_type in self.signal_types:
            detector = SIGNAL_DETECTORS[signal_type]
            try:
                df = detector(
                    symbol,
                    end_date=end_date,
                    cache_dir=cache_dir,
                    force_update=force_update,
                )
                if not df.empty:
                    df["signal_type"] = signal_type
                    all_signals.append(df)
            except Exception as e:
                import warnings
                warnings.warn(f"{signal_type} 检测失败: {e}")

        if not all_signals:
            return pd.DataFrame(columns=["date", "signal_type", "signal", "type"])

        result = pd.concat(all_signals, ignore_index=True)
        result = result.sort_values("date").reset_index(drop=True)

        return result

    def get_combined_signal(
        self,
        symbol: str,
        end_date: Optional[str] = None,
        method: str = "vote",
        cache_dir: str = "stock_cache",
        force_update: bool = False,
    ) -> Dict[str, Union[int, float, pd.DataFrame]]:
        """
        获取聚合后的综合信号。

        Parameters
        ----------
        symbol : str
            股票代码
        end_date : str, optional
            截止日期
        method : str
            聚合方法：
            - 'vote': 多数投票（看涨信号数量 vs 看跌信号数量）
            - 'weighted': 加权平均（可自定义权重）
            - 'any': 任一信号触发即返回
            - 'latest': 最近一次信号的值
        cache_dir : str
            缓存目录
        force_update : bool
            是否强制更新

        Returns
        -------
        dict
            {
                'combined_signal': 1/-1/0,
                'bull_count': 看涨信号数量,
                'bear_count': 看跌信号数量,
                'neutral_count': 中性信号数量,
                'details': 详细信号DataFrame
            }
        """
        signals = self.detect(
            symbol,
            end_date=end_date,
            cache_dir=cache_dir,
            force_update=force_update,
        )

        if signals.empty:
            return {
                "combined_signal": 0,
                "bull_count": 0,
                "bear_count": 0,
                "neutral_count": 0,
                "details": pd.DataFrame(),
            }

        # 计算各类信号数量
        bull_count = (signals["signal"] > 0).sum()
        bear_count = (signals["signal"] < 0).sum()
        neutral_count = (signals["signal"] == 0).sum()

        # 聚合信号
        if method == "vote":
            if bull_count > bear_count:
                combined = 1
            elif bear_count > bull_count:
                combined = -1
            else:
                combined = 0
        elif method == "weighted":
            # 简单加权：看涨信号权重为正，看跌为负
            total = bull_count + bear_count
            if total > 0:
                score = (bull_count - bear_count) / total
                if score > 0.3:
                    combined = 1
                elif score < -0.3:
                    combined = -1
                else:
                    combined = 0
            else:
                combined = 0
        elif method == "any":
            if bull_count > 0 and bear_count > 0:
                combined = 0  # 信号冲突
            elif bull_count > 0:
                combined = 1
            elif bear_count > 0:
                combined = -1
            else:
                combined = 0
        elif method == "latest":
            # 最近一次信号
            latest = signals.iloc[-1]
            combined = int(latest["signal"])
        else:
            raise ValueError(f"未知的聚合方法: {method}")

        return {
            "combined_signal": combined,
            "bull_count": int(bull_count),
            "bear_count": int(bear_count),
            "neutral_count": int(neutral_count),
            "details": signals,
        }

    def get_latest_signals(
        self,
        symbol: str,
        n: int = 5,
        end_date: Optional[str] = None,
        cache_dir: str = "stock_cache",
        force_update: bool = False,
    ) -> pd.DataFrame:
        """
        获取最近N个信号。

        Parameters
        ----------
        symbol : str
            股票代码
        n : int
            返回信号数量
        end_date : str, optional
            截止日期

        Returns
        -------
        pd.DataFrame
            最近N个信号
        """
        signals = self.detect(
            symbol,
            end_date=end_date,
            cache_dir=cache_dir,
            force_update=force_update,
        )

        if signals.empty:
            return pd.DataFrame()

        return signals.tail(n).reset_index(drop=True)


def get_all_signals(
    symbol: str,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取某股票所有可用信号。

    Parameters
    ----------
    symbol : str
        股票代码
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        所有信号汇总
    """
    detector = SignalDetector()
    return detector.detect(symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update)


def get_signal_summary(
    symbol: str,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> Dict:
    """
    获取信号摘要。

    Parameters
    ----------
    symbol : str
        股票代码
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        信号摘要统计
    """
    signals = get_all_signals(symbol, end_date, cache_dir, force_update)

    if signals.empty:
        return {
            "symbol": symbol,
            "total_signals": 0,
            "bull_signals": 0,
            "bear_signals": 0,
            "signal_types": {},
            "latest_signal": None,
        }

    # 按信号类型统计
    type_counts = signals.groupby("signal_type")["signal"].agg(["sum", "count"]).to_dict()

    # 最近信号
    latest = signals.iloc[-1]

    return {
        "symbol": symbol,
        "total_signals": len(signals),
        "bull_signals": int((signals["signal"] > 0).sum()),
        "bear_signals": int((signals["signal"] < 0).sum()),
        "signal_types": type_counts,
        "latest_signal": {
            "date": latest["date"],
            "type": latest.get("type", ""),
            "signal": int(latest["signal"]),
        },
    }


__all__ = [
    # 信号检测器
    "SignalDetector",
    # 统一接口
    "get_all_signals",
    "get_signal_summary",
    # 交叉信号
    "detect_ma_cross",
    "detect_macd_cross",
    "detect_kdj_cross",
    "detect_ema_cross",
    "detect_vmacd_cross",
    "detect_all_cross_signals",
    # 极值信号
    "detect_rsi_extreme",
    "detect_cci_extreme",
    "detect_bias_extreme",
    "detect_kdj_extreme",
    "detect_all_extreme_signals",
    # 突破信号
    "detect_price_breakout",
    "detect_volume_breakout",
    "detect_boll_breakout",
    "detect_ma_breakout",
    "detect_all_breakthrough_signals",
    # 背离信号
    "detect_macd_divergence",
    "detect_rsi_divergence",
    "detect_bear_power_divergence",
    "detect_kdj_divergence",
    "detect_all_divergence_signals",
    # RSRS择时信号
    "compute_rsrs",
    "compute_rsrs_signal",
    "get_rsrs_for_index",
    "get_current_rsrs_signal",
    "compute_rsrs钝化",
    "compute_rsrs_weighted",
    # 市场情绪信号
    "compute_crowding_ratio",
    "compute_gisi",
    "compute_fed_model",
    "compute_graham_index",
    "compute_below_net_ratio",
    "compute_new_high_ratio",
    "get_all_sentiment_indicators",
    # 指标数据
    "get_indicator_data",
    "get_indicator_batch",
    "get_indicator_ranking",
    "filter_by_indicator",
]