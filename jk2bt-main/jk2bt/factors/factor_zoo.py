"""
factors/factor_zoo.py
因子库总入口，对外暴露聚宽风格的 get_factor_values_jq 接口。

职责：
- 汇总所有子模块注册的因子
- 批量调度因子计算
- 组装聚宽兼容的返回结构
"""

import os
import warnings
from typing import Dict, List, Optional, Union
import pandas as pd
import numpy as np

from .base import (
    normalize_factor_names,
    global_factor_registry,
    load_factor_cache,
    save_factor_cache,
    get_trade_days,
)

from . import valuation
from . import technical
from . import fundamentals
from . import growth


# =====================================================================
# 核心接口：get_factor_values_jq
# =====================================================================


def get_factor_values_jq(
    securities: Union[str, List[str]],
    factors: Union[str, List[str]],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "factors_cache",
    force_update: bool = False,
    **kwargs,
) -> Dict[str, pd.DataFrame]:
    """
    聚宽风格因子查询接口。

    Parameters
    ----------
    securities : str or list of str
        证券代码，如 'sh600519' 或 ['sh600519', 'sz000001']
    factors : str or list of str
        因子名，如 'PE_ratio' 或 ['PE_ratio', 'EMAC26', 'VOL240']
    start_date : str, optional
        起始日期 'YYYY-MM-DD'，与 count 二选一
    end_date : str, optional
        截止日期 'YYYY-MM-DD'，默认今日
    count : int, optional
        需要的历史交易日数量，与 start_date 二选一
    cache_dir : str
        因子缓存目录
    force_update : bool
        是否强制重新计算（忽略缓存）
    **kwargs
        传递给具体因子计算函数的额外参数

    Returns
    -------
    dict[str, pd.DataFrame]
        返回格式：
        {
            'PE_ratio': pd.DataFrame(index=dates, columns=securities),
            'EMAC26': pd.DataFrame(index=dates, columns=securities),
            ...
        }
        单因子时仍返回单 key 的字典，不降维。
    """
    # -----------------------------------------------------------------
    # 参数标准化
    # -----------------------------------------------------------------
    if isinstance(securities, str):
        securities = [securities]
    if isinstance(factors, str):
        factors = [factors]

    factor_names = normalize_factor_names(factors)

    # 确定日期范围
    if end_date is None:
        end_date = pd.Timestamp.today().strftime("%Y-%m-%d")

    if start_date is not None:
        # start_date 模式：计算区间内每日因子
        dates = get_trade_days(start_date, end_date)
        if not dates:
            warnings.warn(f"无法获取交易日：{start_date} ~ {end_date}")
            return {f: pd.DataFrame() for f in factor_names}
    elif count is not None:
        # count 模式：需要回溯足够交易日获取窗口数据
        # 此处先按 end_date 向前推 count 天估算起日，再按实际交易日截取
        approx_start = (
            pd.to_datetime(end_date) - pd.Timedelta(days=count * 2)
        ).strftime("%Y-%m-%d")
        dates = get_trade_days(approx_start, end_date)
        dates = dates[-count:] if len(dates) >= count else dates
        if not dates:
            warnings.warn(f"无法获取足够交易日：count={count}, end_date={end_date}")
            return {f: pd.DataFrame() for f in factor_names}
        start_date = dates[0]
    else:
        # 无 start_date 也无 count：仅返回 end_date 当日
        dates = [end_date]
        start_date = end_date

    # -----------------------------------------------------------------
    # 结果容器
    # -----------------------------------------------------------------
    result: Dict[str, pd.DataFrame] = {}

    for factor_name in factor_names:
        # 检查因子是否已注册
        compute_func = global_factor_registry.get(factor_name)
        if compute_func is None:
            warnings.warn(f"因子 '{factor_name}' 未注册，跳过")
            result[factor_name] = pd.DataFrame(index=dates, columns=securities)
            continue

        # 收集每个证券的因子值
        factor_df = pd.DataFrame(index=dates, columns=securities, dtype=float)

        for symbol in securities:
            # 尝试读取缓存
            cached = None
            if not force_update:
                cached = load_factor_cache(
                    factor_name,
                    symbol,
                    end_date,
                    count=count,
                    cache_dir=cache_dir,
                )

            if cached is not None and not cached.empty:
                # 缓存命中，直接使用
                # 注意：缓存的 index 可能是日期字符串，需要与 dates 对齐
                if isinstance(cached.index, pd.DatetimeIndex):
                    cached.index = cached.index.strftime("%Y-%m-%d")
                for d in dates:
                    if d in cached.index:
                        factor_df.loc[d, symbol] = (
                            cached.loc[d, cached.columns[0]]
                            if len(cached.columns) == 1
                            else cached.loc[d, symbol]
                        )
            else:
                # 缓存未命中，调用计算函数
                try:
                    # 计算函数签名：func(symbol, end_date, count, **kwargs)
                    # 返回：float（单值）或 pd.Series（日期序列）或 pd.DataFrame
                    calc_result = compute_func(
                        symbol=symbol,
                        end_date=end_date,
                        count=count,
                        **kwargs,
                    )

                    # 处理返回值
                    if isinstance(calc_result, (int, float, np.floating)):
                        # 单值：填充所有日期
                        factor_df.loc[:, symbol] = calc_result
                    elif isinstance(calc_result, pd.Series):
                        # Series：按日期对齐
                        if isinstance(calc_result.index, pd.DatetimeIndex):
                            calc_result.index = calc_result.index.strftime("%Y-%m-%d")
                        for d in dates:
                            if d in calc_result.index:
                                factor_df.loc[d, symbol] = calc_result.loc[d]
                    elif isinstance(calc_result, pd.DataFrame):
                        # DataFrame：假设 index 为日期，取第一列或与 symbol 对应的列
                        if isinstance(calc_result.index, pd.DatetimeIndex):
                            calc_result.index = calc_result.index.strftime("%Y-%m-%d")
                        col = (
                            calc_result.columns[0]
                            if len(calc_result.columns) >= 1
                            else symbol
                        )
                        for d in dates:
                            if d in calc_result.index:
                                factor_df.loc[d, symbol] = calc_result.loc[d, col]
                    else:
                        warnings.warn(
                            f"因子 '{factor_name}' 返回值类型异常: {type(calc_result)}"
                        )

                    # 写入缓存
                    if factor_df[symbol].notna().any():
                        cache_df = factor_df[[symbol]].copy()
                        cache_df.columns = [factor_name]
                        save_factor_cache(
                            cache_df,
                            factor_name,
                            symbol,
                            end_date,
                            count=count,
                            cache_dir=cache_dir,
                        )

                except Exception as e:
                    warnings.warn(f"计算因子 '{factor_name}' 失败 [{symbol}]: {e}")

        result[factor_name] = factor_df

    return result


# =====================================================================
# 兼容层导出函数
# =====================================================================

__all__ = [
    "get_factor_values_jq",
    "global_factor_registry",
]
