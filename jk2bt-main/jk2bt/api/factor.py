"""
因子 API 模块
提供北向资金因子、组合因子等高级因子接口

聚宽兼容风格
"""

import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional
import warnings
from datetime import datetime, timedelta


def get_north_factor(
    security: Optional[Union[str, List[str]]] = None,
    end_date: Optional[str] = None,
    count: int = 1,
    window: int = 20,
    factor_type: str = "net_inflow",
) -> Union[float, pd.DataFrame, Dict[str, float]]:
    """
    获取北向资金因子

    北向资金是A股市场重要的资金流向指标，反映了外资对市场的看法

    参数:
        security: 股票代码或股票列表（可选，None表示获取整体北向资金因子）
        end_date: 截止日期，格式 'YYYY-MM-DD'
        count: 返回数据条数
        window: 计算窗口期
        factor_type: 因子类型
            - 'net_inflow': 净流入因子（默认）
            - 'flow_ratio': 流入占比因子
            - 'momentum': 北向资金动量因子
            - 'stock_flow': 个股北向资金流入因子

    返回:
        当 security 为 None: 返回整体北向资金因子值
        当 security 为单个股票: 返回该股票的北向资金因子值
        当 security 为列表: 返回 DataFrame 或 Dict

    示例:
        # 获取整体北向资金因子
        factor = get_north_factor(end_date='2024-01-01')

        # 获取个股北向资金因子
        factor = get_north_factor('600519.XSHG', end_date='2024-01-01', factor_type='stock_flow')

        # 获取多只股票的北向资金因子
        factors = get_north_factor(['600519.XSHG', '000858.XSHE'], end_date='2024-01-01')
    """
    from jk2bt.market_data.north_money import (
        get_north_money_flow,
        get_north_money_stock_flow,
        get_north_money_holdings,
    )

    # 整体北向资金因子
    if security is None:
        try:
            df = get_north_money_flow(end_date=end_date)

            if df.empty or len(df) < window:
                return 0.0

            df = df.tail(window + count)

            if factor_type == "net_inflow":
                # 净流入因子：近N日平均净流入
                factor = df["net_inflow"].tail(window).mean()
                if count == 1:
                    return float(factor)
                return df["net_inflow"].tail(count)

            elif factor_type == "flow_ratio":
                # 流入占比因子
                total_inflow = df["inflow"].tail(window).sum()
                total_outflow = df["outflow"].tail(window).sum()
                factor = (total_inflow - total_outflow) / (total_inflow + total_outflow) if (total_inflow + total_outflow) > 0 else 0
                if count == 1:
                    return float(factor)
                return pd.Series([factor], index=[end_date or "latest"])

            elif factor_type == "momentum":
                # 北向资金动量因子：近期流入 vs 远期流入
                recent = df["net_inflow"].tail(window // 2).mean()
                earlier = df["net_inflow"].iloc[-window:-window//2].mean()

                if earlier == 0:
                    factor = 1.0 if recent > 0 else -1.0
                else:
                    factor = (recent - earlier) / abs(earlier)

                if count == 1:
                    return float(factor)
                return pd.Series([factor], index=[end_date or "latest"])

            else:
                return 0.0

        except Exception as e:
            warnings.warn(f"获取北向资金因子失败: {e}")
            return 0.0

    # 个股北向资金因子
    else:
        if isinstance(security, str):
            securities = [security]
            single_security = True
        else:
            securities = security
            single_security = False

        result = {}

        for sec in securities:
            try:
                if factor_type == "stock_flow":
                    # 个股北向资金流入
                    df = get_north_money_stock_flow(sec, end_date=end_date)

                    if df.empty or len(df) < window:
                        result[sec] = 0.0
                        continue

                    # 计算个股北向资金因子
                    recent_inflow = df["net_inflow"].tail(window).mean()
                    result[sec] = float(recent_inflow)

                elif factor_type == "holding_change":
                    # 持股变化因子
                    holdings = get_north_money_holdings(date=end_date, top_n=500)

                    if holdings.empty:
                        result[sec] = 0.0
                        continue

                    code = sec.replace(".XSHG", "").replace(".XSHE", "").zfill(6)
                    stock_holding = holdings[holdings["code"] == code]

                    if stock_holding.empty:
                        result[sec] = 0.0
                    else:
                        change = stock_holding.iloc[0].get("holdings_change", 0)
                        result[sec] = float(change) if change is not None else 0.0

                else:
                    # 默认使用整体因子
                    overall_factor = get_north_factor(
                        security=None,
                        end_date=end_date,
                        count=1,
                        window=window,
                        factor_type="net_inflow",
                    )
                    result[sec] = float(overall_factor)

            except Exception as e:
                warnings.warn(f"获取 {sec} 北向资金因子失败: {e}")
                result[sec] = 0.0

        if single_security:
            return result.get(security, 0.0)
        return result


def get_comb_factor(
    securities: Union[str, List[str]],
    factors: Union[str, List[str]],
    end_date: Optional[str] = None,
    count: int = 1,
    method: str = "weighted",
    weights: Optional[Dict[str, float]] = None,
    normalize: bool = True,
) -> Union[pd.DataFrame, Dict[str, float]]:
    """
    获取组合因子

    将多个因子按指定方法组合，生成综合因子值

    参数:
        securities: 股票代码或股票列表
        factors: 因子名称或因子列表，支持：
            - 估值因子: PE_ratio, PB_ratio, PS_ratio, market_cap
            - 技术因子: MACD, RSI, KDJ, BOLL, MA
            - 财务因子: ROE, ROA, net_profit_ratio
            - 北向资金因子: north_inflow, north_holding
        end_date: 截止日期
        count: 返回数据条数
        method: 组合方法
            - 'weighted': 加权平均（默认）
            - 'equal': 等权平均
            - 'rank': 排名加权
            - 'zscore': Z-score标准化后组合
        weights: 因子权重字典 {'因子名': 权重}，method='weighted'时使用
        normalize: 是否对因子进行标准化

    返回:
        组合因子值

    示例:
        # 获取多因子组合（等权）
        comb = get_comb_factor(
            securities=['600519.XSHG', '000858.XSHE'],
            factors=['PE_ratio', 'ROE', 'RSI'],
            end_date='2024-01-01',
            method='equal'
        )

        # 获取多因子组合（加权）
        comb = get_comb_factor(
            securities='600519.XSHG',
            factors=['PE_ratio', 'ROE', 'north_inflow'],
            weights={'PE_ratio': 0.3, 'ROE': 0.4, 'north_inflow': 0.3},
            end_date='2024-01-01'
        )
    """
    from jk2bt.factors import get_factor_values_jq
    from jk2bt.api.indicators import MACD, RSI, KDJ, BOLL

    # 统一为列表格式
    if isinstance(securities, str):
        security_list = [securities]
        single_security = True
    else:
        security_list = securities
        single_security = False

    if isinstance(factors, str):
        factor_list = [factors]
    else:
        factor_list = factors

    # 收集各因子数据
    factor_data = {}

    for factor_name in factor_list:
        try:
            # 尝试从因子库获取
            if factor_name.lower() in [
                "pe_ratio", "pb_ratio", "ps_ratio", "market_cap",
                "roe", "roa", "net_profit_ratio", "bias_5", "bias_10",
                "emac_10", "emac_20", "roc_6", "vol_20", "macd",
            ]:
                result = get_factor_values_jq(
                    securities=[s.replace(".XSHG", ".XSHG").replace(".XSHE", ".XSHE") for s in security_list],
                    factors=factor_name,
                    end_date=end_date,
                    count=count,
                )
                if result and factor_name.lower() in result:
                    factor_data[factor_name] = result[factor_name.lower()]

            # 技术指标因子
            elif factor_name.upper() == "MACD":
                result = MACD(security_list, check_date=end_date)
                factor_data[factor_name] = pd.Series(result["MACD"])

            elif factor_name.upper() == "RSI":
                result = {}
                for sec in security_list:
                    result[sec] = RSI(sec, timeperiod=14, check_date=end_date)
                factor_data[factor_name] = pd.Series(result)

            elif factor_name.upper() == "KDJ":
                result = KDJ(security_list, check_date=end_date)
                factor_data[factor_name] = pd.Series(result["K"])

            elif factor_name.upper() == "BOLL":
                result = BOLL(security_list, check_date=end_date)
                factor_data[factor_name] = pd.Series(result["MIDDLE"])

            # 北向资金因子
            elif factor_name.lower() in ["north_inflow", "north_factor"]:
                result = get_north_factor(
                    security=security_list,
                    end_date=end_date,
                    factor_type="stock_flow",
                )
                factor_data[factor_name] = pd.Series(result)

            elif factor_name.lower() == "north_holding":
                result = get_north_factor(
                    security=security_list,
                    end_date=end_date,
                    factor_type="holding_change",
                )
                factor_data[factor_name] = pd.Series(result)

            else:
                warnings.warn(f"未知因子: {factor_name}")

        except Exception as e:
            warnings.warn(f"获取因子 {factor_name} 失败: {e}")

    if not factor_data:
        if single_security:
            return 0.0
        return {sec: 0.0 for sec in security_list}

    # 转换为 DataFrame
    factor_df = pd.DataFrame(factor_data)

    # 标准化
    if normalize and len(factor_list) > 1:
        for col in factor_df.columns:
            mean = factor_df[col].mean()
            std = factor_df[col].std()
            if std != 0:
                factor_df[col] = (factor_df[col] - mean) / std

    # 计算组合因子
    if method == "equal":
        # 等权平均
        comb_factor = factor_df.mean(axis=1)

    elif method == "weighted":
        # 加权平均
        if weights is None:
            weights = {f: 1.0 / len(factor_list) for f in factor_df.columns}

        weighted_sum = 0
        weight_sum = 0
        for col in factor_df.columns:
            w = weights.get(col, 1.0 / len(factor_list))
            weighted_sum += factor_df[col].fillna(0) * w
            weight_sum += w

        comb_factor = weighted_sum / weight_sum if weight_sum > 0 else factor_df.mean(axis=1)

    elif method == "rank":
        # 排名加权
        rank_df = factor_df.rank(pct=True)
        comb_factor = rank_df.mean(axis=1)

    else:
        comb_factor = factor_df.mean(axis=1)

    # 返回结果
    if single_security:
        return float(comb_factor.iloc[0])
    return comb_factor.to_dict()


def get_factor_momentum(
    securities: Union[str, List[str]],
    factor: str,
    window: int = 20,
    end_date: Optional[str] = None,
) -> Union[float, Dict[str, float]]:
    """
    计算因子动量

    因子动量 = (当前因子值 - N日前因子值) / N日前因子值

    参数:
        securities: 股票代码或股票列表
        factor: 因子名称
        window: 动量计算窗口
        end_date: 截止日期

    返回:
        因子动量值

    示例:
        momentum = get_factor_momentum('600519.XSHG', 'PE_ratio', window=20)
    """
    from jk2bt.factors import get_factor_values_jq

    if isinstance(securities, str):
        security_list = [securities]
        single_security = True
    else:
        security_list = securities
        single_security = False

    try:
        # 获取当前因子值
        current = get_factor_values_jq(
            securities=security_list,
            factors=factor,
            end_date=end_date,
            count=1,
        )

        # 获取历史因子值
        past = get_factor_values_jq(
            securities=security_list,
            factors=factor,
            end_date=end_date,
            count=window + 1,
        )

        if not current or not past:
            return 0.0 if single_security else {sec: 0.0 for sec in security_list}

        factor_key = factor.lower()
        result = {}

        for sec in security_list:
            try:
                current_val = current[factor_key][sec].iloc[-1] if factor_key in current else 0
                past_val = past[factor_key][sec].iloc[0] if factor_key in past and len(past[factor_key]) > window else current_val

                if past_val != 0:
                    momentum = (current_val - past_val) / abs(past_val)
                else:
                    momentum = 0.0

                result[sec] = float(momentum)
            except Exception:
                result[sec] = 0.0

        if single_security:
            return result.get(securities, 0.0)
        return result

    except Exception as e:
        warnings.warn(f"计算因子动量失败: {e}")
        return 0.0 if single_security else {sec: 0.0 for sec in security_list}


__all__ = [
    "get_north_factor",
    "get_comb_factor",
    "get_factor_momentum",
]