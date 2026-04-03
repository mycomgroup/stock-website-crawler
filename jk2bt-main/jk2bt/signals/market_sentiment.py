"""
indicators/market_sentiment.py
市场情绪指标模块。

功能:
- 拥挤率指标（资金集中度）
- GSISI 投资者情绪指数
- FED 模型（股债性价比）
- 格雷厄姆指数
- 破净占比
- 创新高/新低比例
"""

import warnings
from typing import Optional, Dict, List
import pandas as pd
import numpy as np
from datetime import datetime


def compute_crowding_ratio(
    date: Optional[str] = None,
    threshold_pct: float = 0.05,
) -> Dict[str, float]:
    """
    计算拥挤率指标（成交额前5%股票的成交额占比）。

    参数
    ----
    date : str, optional
        查询日期
    threshold_pct : float
        阈值百分比（默认前5%）

    返回
    ----
    Dict[str, float]
        {'crowding_ratio': 拥挤率百分比, 'description': 描述}
    """
    try:
        import akshare as ak
    except ImportError:
        return {"crowding_ratio": 0.0, "description": "请安装 akshare: pip install akshare"}

    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    else:
        date = date.replace("-", "")

    try:
        df = ak.stock_zh_a_spot_em()

        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "代码": "code",
                    "名称": "name",
                    "成交额": "amount",
                }
            )

            total_amount = df["amount"].sum()

            df_sorted = df.sort_values("amount", ascending=False)
            top_n = int(len(df) * threshold_pct)
            top_amount = df_sorted["amount"].head(top_n).sum()

            crowding_ratio = (top_amount / total_amount) * 100

            if crowding_ratio > 60:
                desc = f"拥挤率={crowding_ratio:.2f}%，资金过度集中，注意轮动"
            elif crowding_ratio < 40:
                desc = f"拥挤率={crowding_ratio:.2f}%，资金分散，可能见底"
            else:
                desc = f"拥挤率={crowding_ratio:.2f}%，资金分布正常"

            return {
                "crowding_ratio": crowding_ratio,
                "total_amount": total_amount,
                "description": desc,
            }
    except Exception as e:
        warnings.warn(f"计算拥挤率失败: {e}")

    return {"crowding_ratio": 0.0, "description": "计算失败"}


def compute_gisi(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    window: int = 35,
    pct_window: int = 15,
    index_code: str = "000300",
) -> pd.DataFrame:
    """
    计算 GSISI（国信投资者情绪指数）。

    核心: 行业收益率与Beta系数的Spearman秩相关系数

    参数
    ----
    window : int
        Beta计算窗口（默认35日）
    pct_window : int
        收益率计算窗口（默认15日）

    返回
    ----
    pd.DataFrame
        包含 GSISI 指标和择时信号
    """
    try:
        import akshare as ak
    except ImportError:
        return pd.DataFrame()

    from market_data.industry import SW_LEVEL1_CODES, get_industry_daily

    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    need_days = window + pct_window + 50
    if start_date is None:
        start_dt = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = (start_dt - pd.Timedelta(days=need_days * 1.5)).strftime(
            "%Y-%m-%d"
        )

    try:
        index_df = ak.stock_zh_index_daily(symbol=f"sh{index_code}")
        if index_df is None or index_df.empty:
            return pd.DataFrame()

        index_df = index_df.rename(columns={"date": "date", "close": "close"})
        index_df["date"] = pd.to_datetime(index_df["date"])
        index_df = index_df[index_df["date"] >= pd.to_datetime(start_date)]
        index_df = index_df.sort_values("date").reset_index(drop=True)

        industry_returns = {}
        for industry_name, industry_code in list(SW_LEVEL1_CODES.items())[:10]:
            try:
                ind_df = get_industry_daily(industry_name, start_date, end_date)
                if ind_df is not None and len(ind_df) >= pct_window:
                    ind_df["return"] = ind_df["close"].pct_change(pct_window)
                    industry_returns[industry_name] = ind_df["return"]
            except Exception:
                continue

        if len(industry_returns) < 5:
            return pd.DataFrame()

        returns_df = pd.DataFrame(industry_returns)
        returns_df = returns_df.dropna()

        index_df["return"] = index_df["close"].pct_change()

        dates = returns_df.index

        gisi_values = pd.Series(index=dates, data=np.nan)

        for i in range(window, len(dates)):
            window_returns = returns_df.iloc[i - window : i]
            window_index_returns = index_df["return"].iloc[i - window : i]

            betas = []
            recent_returns = []

            for col in window_returns.columns:
                try:
                    cov = np.cov(window_returns[col], window_index_returns)[0, 1]
                    var_index = window_index_returns.var()
                    beta = cov / var_index if var_index > 0 else 0

                    recent_return = window_returns[col].iloc[-1]

                    betas.append(beta)
                    recent_returns.append(recent_return)
                except Exception:
                    continue

            if len(betas) >= 5:
                corr = pd.Series(betas).corr(
                    pd.Series(recent_returns), method="spearman"
                )
                gisi_values.iloc[i] = corr

        result = pd.DataFrame({"date": dates, "gisi": gisi_values})

        result["signal"] = 0
        result.loc[result["gisi"] >= 0.301, "signal"] = 1
        result.loc[result["gisi"] <= -0.301, "signal"] = -1

        return result[["date", "gisi", "signal"]]

    except Exception as e:
        warnings.warn(f"计算GSISI失败: {e}")

    return pd.DataFrame()


def compute_fed_model(
    date: Optional[str] = None,
    index_code: str = "000300",
    bond_rate: Optional[float] = None,
) -> Dict[str, float]:
    """
    计算 FED 模型（股债性价比）。

    公式: FED = 1/PE - 国债收益率

    参数
    ----
    date : str, optional
        查询日期
    bond_rate : float, optional
        国债收益率（默认取当前10年期国债收益率）

    返回
    ----
    Dict[str, float]
        {'fed_value': FED值, 'pe': PE值, 'bond_rate': 国债收益率, 'description': 描述}
    """
    try:
        import akshare as ak
    except ImportError:
        return {"fed_value": 0.0, "description": "请安装 akshare: pip install akshare"}

    if date is None:
        date = datetime.now().strftime("%Y%m%d")

    try:
        df = ak.stock_a_pe_and_pb(symbol="沪深300")

        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "date": "date",
                    "pe": "pe",
                    "pb": "pb",
                }
            )

            df["date"] = pd.to_datetime(df["date"])
            df = df[df["date"] <= pd.to_datetime(date)]

            if df.empty:
                return {"fed_value": 0.0, "description": "无PE数据"}

            latest_pe = df["pe"].iloc[-1]

            if bond_rate is None:
                try:
                    bond_df = ak.bond_china_yield(
                        start_date=date.replace("-", ""), end_date=date.replace("-", "")
                    )
                    if bond_df is not None and not bond_df.empty:
                        bond_rate = float(bond_df["10年期国债收益率"].iloc[-1]) / 100
                except Exception:
                    bond_rate = 0.025

            fed_value = 1.0 / latest_pe - bond_rate

            if fed_value > 0.05:
                desc = f"FED={fed_value:.2f}，股票极具吸引力"
            elif fed_value > 0:
                desc = f"FED={fed_value:.2f}，股票优于债券"
            else:
                desc = f"FED={fed_value:.2f}，债券优于股票"

            return {
                "fed_value": fed_value,
                "pe": latest_pe,
                "bond_rate": bond_rate,
                "description": desc,
            }
    except Exception as e:
        warnings.warn(f"计算FED模型失败: {e}")

    return {"fed_value": 0.0, "description": "计算失败"}


def compute_graham_index(
    date: Optional[str] = None,
    index_code: str = "000300",
    bond_rate: Optional[float] = None,
) -> Dict[str, float]:
    """
    计算格雷厄姆指数。

    公式: 格雷厄姆指数 = (1/PE) / 国债收益率

    返回
    ----
    Dict[str, float]
        {'graham_index': 格雷厄姆指数, 'description': 描述}
    """
    fed_result = compute_fed_model(date, index_code, bond_rate)

    if fed_result["fed_value"] == 0.0:
        return {"graham_index": 0.0, "description": "计算失败"}

    pe = fed_result.get("pe", 15)
    bond_rate = fed_result.get("bond_rate", 0.025)

    graham_index = (1.0 / pe) / bond_rate

    if graham_index > 1.5:
        desc = f"格雷厄姆指数={graham_index:.2f}，股票低估"
    elif graham_index > 1:
        desc = f"格雷厄姆指数={graham_index:.2f}，股票合理"
    else:
        desc = f"格雷厄姆指数={graham_index:.2f}，股票高估"

    return {
        "graham_index": graham_index,
        "pe": pe,
        "bond_rate": bond_rate,
        "description": desc,
    }


def compute_below_net_ratio(
    date: Optional[str] = None,
) -> Dict[str, float]:
    """
    计算破净股占比（股价低于净资产的股票比例）。

    返回
    ----
    Dict[str, float]
        {'below_net_ratio': 破净占比, 'below_net_count': 破净股数量, 'description': 描述}
    """
    try:
        import akshare as ak
    except ImportError:
        return {"below_net_ratio": 0.0, "description": "请安装 akshare: pip install akshare"}

    if date is None:
        date = datetime.now().strftime("%Y%m%d")

    try:
        df = ak.stock_zh_a_spot_em()

        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "代码": "code",
                    "名称": "name",
                    "市净率": "pb",
                }
            )

            if "pb" in df.columns:
                below_net = df[df["pb"] < 1.0]

                below_net_count = len(below_net)
                total_count = len(df)
                below_net_ratio = below_net_count / total_count * 100

                if below_net_ratio > 10:
                    desc = f"破净占比={below_net_ratio:.2f}%，市场极度悲观"
                elif below_net_ratio > 5:
                    desc = f"破净占比={below_net_ratio:.2f}%，市场偏悲观"
                else:
                    desc = f"破净占比={below_net_ratio:.2f}%，市场正常"

                return {
                    "below_net_ratio": below_net_ratio,
                    "below_net_count": below_net_count,
                    "total_count": total_count,
                    "description": desc,
                }
    except Exception as e:
        warnings.warn(f"计算破净占比失败: {e}")

    return {"below_net_ratio": 0.0, "description": "计算失败"}


def compute_new_high_ratio(
    date: Optional[str] = None,
    window: int = 60,
) -> Dict[str, float]:
    """
    计算创新高股票占比。

    参数
    ----
    window : int
        创新高周期（默认60日）

    返回
    ----
    Dict[str, float]
        {'new_high_ratio': 创新高占比, 'description': 描述}
    """
    try:
        import akshare as ak
    except ImportError:
        return {"new_high_ratio": 0.0, "description": "请安装 akshare: pip install akshare"}

    if date is None:
        date = datetime.now().strftime("%Y%m%d")

    try:
        df = ak.stock_zh_a_spot_em()

        if df is not None and not df.empty:
            new_high_count = 0
            total_count = 0

            for idx, row in df.head(100).iterrows():
                code = row["代码"]

                try:
                    hist_df = ak.stock_zh_a_hist(
                        symbol=code, period="daily", adjust="qfq", count=window
                    )

                    if hist_df is not None and len(hist_df) >= window:
                        latest_close = hist_df["收盘"].iloc[-1]
                        max_close = hist_df["收盘"].iloc[:-1].max()

                        if latest_close >= max_close:
                            new_high_count += 1
                        total_count += 1
                except Exception:
                    continue

            if total_count > 0:
                new_high_ratio = new_high_count / total_count * 100

                if new_high_ratio > 5:
                    desc = f"创新高占比={new_high_ratio:.2f}%，市场强势"
                elif new_high_ratio < 1:
                    desc = f"创新高占比={new_high_ratio:.2f}%，市场弱势"
                else:
                    desc = f"创新高占比={new_high_ratio:.2f}%，市场中性"

                return {
                    "new_high_ratio": new_high_ratio,
                    "new_high_count": new_high_count,
                    "total_count": total_count,
                    "description": desc,
                }
    except Exception as e:
        warnings.warn(f"计算创新高占比失败: {e}")

    return {"new_high_ratio": 0.0, "description": "计算失败"}


def get_all_sentiment_indicators(
    date: Optional[str] = None,
) -> Dict[str, Dict[str, float]]:
    """
    获取所有市场情绪指标。

    返回
    ----
    Dict[str, Dict]
        各情绪指标的完整数据
    """
    return {
        "crowding_ratio": compute_crowding_ratio(date),
        "fed_model": compute_fed_model(date),
        "graham_index": compute_graham_index(date),
        "below_net_ratio": compute_below_net_ratio(date),
        "new_high_ratio": compute_new_high_ratio(date),
    }


__all__ = [
    "compute_crowding_ratio",
    "compute_gisi",
    "compute_fed_model",
    "compute_graham_index",
    "compute_below_net_ratio",
    "compute_new_high_ratio",
    "get_all_sentiment_indicators",
]
