"""
finance_data/forecast.py
业绩预告数据获取模块。
"""

import pandas as pd

from jk2bt.utils.symbol import extract_code_num, ak_code_to_jq


def get_forecast_data(symbol, force_update=False):
    """
    获取业绩预告数据。

    参数
    ----
    symbol     : 股票代码，支持 '600519.XSHG', '000001.XSHE', 'sh600519', '600519' 等格式
    force_update: True 时强制重新下载

    返回
    ----
    pandas DataFrame，标准化字段：
    - code: 股票代码（聚宽格式）
    - year: 预测年度
    - type: 预测类型（业绩预告/业绩快报/预测每股收益等）
    - forecast_min: 预测最小值
    - forecast_mean: 预测均值
    - forecast_max: 预测最大值
    - agency_count: 预测机构数
    - industry_avg: 行业平均数
    """
    code_num = extract_code_num(symbol)

    from jk2bt.data.sources import get_adapter

    try:
        dfs = []

        try:
            df_predict = get_adapter().get_forecast_ths(
                symbol=code_num, indicator="预测年报每股收益"
            )
            if df_predict is not None and not df_predict.empty:
                df_norm = _normalize_predict_data(df_predict, symbol)
                dfs.append(df_norm)
        except Exception as e:
            print(f"[forecast] 预测每股收益获取失败: {e}")

        try:
            df_forecast = get_adapter().get_forecast_ths(
                symbol=code_num, indicator="业绩预告"
            )
            if df_forecast is not None and not df_forecast.empty:
                df_norm = _normalize_forecast_data(df_forecast, symbol)
                dfs.append(df_norm)
        except Exception:
            pass

        try:
            df_quick = get_adapter().get_forecast_ths(
                symbol=code_num, indicator="业绩快报"
            )
            if df_quick is not None and not df_quick.empty:
                df_norm = _normalize_quick_data(df_quick, symbol)
                dfs.append(df_norm)
        except Exception:
            pass

        if dfs:
            result = pd.concat(dfs, ignore_index=True)
            return result
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"[forecast] 下载失败: {e}")
        return pd.DataFrame()


def _normalize_predict_data(df, symbol):
    """标准化预测每股收益数据"""
    result = pd.DataFrame()
    result["code"] = [ak_code_to_jq(symbol)] * len(df)

    if "年度" in df.columns:
        result["year"] = df["年度"]

    result["type"] = ["预测年报每股收益"] * len(df)

    if "预测机构数" in df.columns:
        result["agency_count"] = df["预测机构数"]
    if "最小值" in df.columns:
        result["forecast_min"] = df["最小值"]
    if "均值" in df.columns:
        result["forecast_mean"] = df["均值"]
    if "最大值" in df.columns:
        result["forecast_max"] = df["最大值"]
    if "行业平均数" in df.columns:
        result["industry_avg"] = df["行业平均数"]

    return result


def _normalize_forecast_data(df, symbol):
    """标准化业绩预告数据"""
    result = pd.DataFrame()
    result["code"] = [ak_code_to_jq(symbol)] * len(df)
    result["type"] = ["业绩预告"] * len(df)

    if "年度" in df.columns:
        result["year"] = df["年度"]

    col_map = {
        "预告净利润变动范围": "profit_change_range",
        "预告净利润上限": "profit_forecast_max",
        "预告净利润下限": "profit_forecast_min",
        "预告净利润增幅上限": "profit_growth_max",
        "预告净利润增幅下限": "profit_growth_min",
        "预告类型": "forecast_type",
        "预告摘要": "forecast_summary",
        "公告日期": "pub_date",
    }

    for src_col, target_col in col_map.items():
        if src_col in df.columns:
            result[target_col] = df[src_col]

    return result


def _normalize_quick_data(df, symbol):
    """标准化业绩快报数据"""
    result = pd.DataFrame()
    result["code"] = [ak_code_to_jq(symbol)] * len(df)
    result["type"] = ["业绩快报"] * len(df)

    if "年度" in df.columns:
        result["year"] = df["年度"]

    col_map = {
        "营业总收入": "total_revenue",
        "营业总收入同比": "revenue_growth",
        "净利润": "net_profit",
        "净利润同比": "profit_growth",
        "每股收益": "eps",
        "每股净资产": "nav_per_share",
        "净资产收益率": "roe",
        "公告日期": "pub_date",
    }

    for src_col, target_col in col_map.items():
        if src_col in df.columns:
            result[target_col] = df[src_col]

    return result


from jk2bt.utils.symbol import extract_code_num as _extract_code_num
from jk2bt.utils.symbol import ak_code_to_jq as _normalize_to_jq
