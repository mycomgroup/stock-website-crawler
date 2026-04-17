"""
资金流向相关API模块

提供：
- get_money_flow: 个股资金流向数据
- get_sector_money_flow: 板块资金流向

数据源说明:
- 资金流向为特殊数据，使用 akshare 作为数据源
- 采用延迟导入，避免顶层依赖耦合
"""

import pandas as pd
import warnings
from datetime import datetime

from jk2bt.data.sources import get_adapter
from jk2bt.utils.symbol import normalize_symbol as _normalize_code


def get_money_flow(
    security=None,
    start_date=None,
    end_date=None,
    count=None,
):
    """
    获取个股资金流向数据

    参数:
        security: 股票代码，可以是单个代码或列表。如果为None则返回全部
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        count: 返回最近N天数据

    返回:
        DataFrame: 资金流向数据
            columns包含: code, date, main_net_inflow, retail_net_inflow, etc.
    """
    try:
        # 使用 adapter 获取个股资金流
        if security is not None:
            # 单个股票
            if isinstance(security, str):
                code = _normalize_code(security)
                df = _get_single_stock_money_flow(code, start_date, end_date, count)
            else:
                # 股票列表
                results = []
                for s in security:
                    code = _normalize_code(s)
                    single_df = _get_single_stock_money_flow(
                        code, start_date, end_date, count
                    )
                    if not single_df.empty:
                        results.append(single_df)
                df = (
                    pd.concat(results, ignore_index=True) if results else pd.DataFrame()
                )
        else:
            # 全部股票 - 返回当日资金流排名
            df = _get_all_stocks_money_flow()

        return df

    except Exception as e:
        warnings.warn(f"get_money_flow 失败: {e}")
        return pd.DataFrame()


def _get_single_stock_money_flow(code, start_date=None, end_date=None, count=None):
    """获取单个股票的资金流向"""
    try:
        # 尝试使用 adapter 的个股资金流接口
        try:
            # 个股资金流向历史数据
            market = "sh" if code.startswith("6") else "sz"
            df = get_adapter().get_individual_fund_flow(stock=code, market=market)
            if df is not None and not df.empty:
                # 标准化列名
                df = _standardize_columns(df)
                df["code"] = code

                # 日期过滤
                if start_date:
                    df = df[df["date"] >= start_date]
                if end_date:
                    df = df[df["date"] <= end_date]
                if count:
                    df = df.tail(count)

                return df
        except Exception:
            pass

        # 备用接口：当日资金流
        try:
            df = get_adapter().get_individual_fund_flow_rank(indicator="今日")
            if df is not None and not df.empty:
                df = _standardize_columns(df)
                df = df[df["code"] == code]
                return df
        except Exception:
            pass

        return pd.DataFrame()

    except Exception as e:
        warnings.warn(f"获取 {code} 资金流向失败: {e}")
        return pd.DataFrame()


def _get_all_stocks_money_flow():
    """获取全部股票资金流向排名"""
    try:
        # 个股资金流排名
        df = get_adapter().get_individual_fund_flow_rank(indicator="今日")
        if df is not None and not df.empty:
            df = _standardize_columns(df)
            return df
    except Exception:
        pass

    return pd.DataFrame()


def _standardize_columns(df):
    """标准化列名"""
    column_mapping = {
        "代码": "code",
        "名称": "name",
        "日期": "date",
        "收盘价": "close",
        "涨跌幅": "pct_change",
        "主力净流入": "main_net_inflow",
        "小单净流入": "small_net_inflow",
        "中单净流入": "medium_net_inflow",
        "大单净流入": "large_net_inflow",
        "超大单净流入": "xlarge_net_inflow",
        "主力净流入占比": "main_net_inflow_pct",
        "净流入": "net_inflow",
        "主力净流入-净额": "main_net_inflow",
        "主力净流入-净占比": "main_net_inflow_pct",
        "超大单净流入-净额": "xlarge_net_inflow",
        "大单净流入-净额": "large_net_inflow",
        "中单净流入-净额": "medium_net_inflow",
        "小单净流入-净额": "small_net_inflow",
    }

    # 重命名列
    new_columns = {}
    for col in df.columns:
        col_str = str(col)
        if col_str in column_mapping:
            new_columns[col] = column_mapping[col_str]
        else:
            # 尝试模糊匹配
            for key, value in column_mapping.items():
                if key in col_str:
                    new_columns[col] = value
                    break

    if new_columns:
        df = df.rename(columns=new_columns)

    return df


def get_sector_money_flow(sector=None, date=None):
    """
    获取板块资金流向

    参数:
        sector: 板块名称或代码（可选）
        date: 查询日期（可选）

    返回:
        DataFrame: 板块资金流向数据
    """
    try:
        # 行业资金流
        try:
            df = get_adapter().get_sector_money_flow(
                sector_type="industry", indicator="今日"
            )
            if df is not None and not df.empty:
                df = _standardize_columns(df)
                if sector:
                    name_col = "name" if "name" in df.columns else df.columns[0]
                    code_col = (
                        "code"
                        if "code" in df.columns
                        else df.columns[1]
                        if len(df.columns) > 1
                        else df.columns[0]
                    )
                    df = df[
                        df[name_col].str.contains(sector, na=False)
                        | df[code_col].str.contains(sector, na=False)
                    ]
                return df
        except Exception:
            pass

        # 概念资金流
        try:
            df = get_adapter().get_sector_money_flow(
                sector_type="concept", indicator="今日"
            )
            if df is not None and not df.empty:
                df = _standardize_columns(df)
                if sector:
                    name_col = "name" if "name" in df.columns else df.columns[0]
                    code_col = (
                        "code"
                        if "code" in df.columns
                        else df.columns[1]
                        if len(df.columns) > 1
                        else df.columns[0]
                    )
                    df = df[
                        df[name_col].str.contains(sector, na=False)
                        | df[code_col].str.contains(sector, na=False)
                    ]
                return df
        except Exception:
            pass

        return pd.DataFrame()

    except Exception as e:
        warnings.warn(f"get_sector_money_flow 失败: {e}")
        return pd.DataFrame()


def get_money_flow_rank(top_n=50, direction="inflow"):
    """
    获取资金流向排名

    参数:
        top_n: 返回前N只股票
        direction: 'inflow' 净流入排名, 'outflow' 净流出排名

    返回:
        DataFrame: 资金流向排名
    """
    df = get_money_flow()

    if df.empty:
        return df

    # 排序
    if "main_net_inflow" in df.columns:
        if direction == "inflow":
            df = df.sort_values("main_net_inflow", ascending=False).head(top_n)
        else:
            df = df.sort_values("main_net_inflow", ascending=True).head(top_n)

    return df


def get_money_flow_pro(
    security_list=None,
    start_date=None,
    end_date=None,
    frequency="daily",
    fields=None,
    count=None,
    data_type="money",
):
    """
    获取个股资金流向数据 (Pro版，返回12个字段的完整体系)

    参数:
        security_list: 股票代码列表，如 ['600519.XSHG', '000858.XSHE']
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        frequency: 数据频率，目前仅支持 'daily' (日线)
        fields: 字段列表，默认返回全部12个字段
        count: 返回最近N天数据
        data_type: 'money' | 'volume' | 'deal' 三种统计类型

    返回:
        DataFrame: 资金流向数据，包含12个字段
            - inflow_xl: 超大单流入
            - inflow_l: 大单流入
            - inflow_m: 中单流入
            - inflow_s: 小单流入
            - outflow_xl: 超大单流出
            - outflow_l: 大单流出
            - outflow_m: 中单流出
            - outflow_s: 小单流出
            - netflow_xl: 超大单净流入
            - netflow_l: 大单净流入
            - netflow_m: 中单净流入
            - netflow_s: 小单净流入
    """
    try:
        import akshare as ak
        import pandas as pd
        from jk2bt.utils.symbol import normalize_symbol

        if security_list is None:
            return pd.DataFrame()

        if isinstance(security_list, str):
            security_list = [security_list]

        all_results = []
        for security in security_list:
            code = normalize_symbol(security)
            market = "sh" if code.startswith("6") else "sz"
            akshare_code = code.zfill(6)

            try:
                df = ak.stock_individual_fund_flow(stock=akshare_code, market=market)
                if df is None or df.empty:
                    continue

                df = _standardize_pro_columns(df)
                df["code"] = code

                if start_date:
                    df = df[df["date"] >= start_date]
                if end_date:
                    df = df[df["date"] <= end_date]
                if count:
                    df = df.tail(count)

                all_results.append(df)
            except Exception:
                continue

        if not all_results:
            return pd.DataFrame()

        result = pd.concat(all_results, ignore_index=True)

        target_fields = [
            "code",
            "date",
            "inflow_xl",
            "inflow_l",
            "inflow_m",
            "inflow_s",
            "outflow_xl",
            "outflow_l",
            "outflow_m",
            "outflow_s",
            "netflow_xl",
            "netflow_l",
            "netflow_m",
            "netflow_s",
        ]

        if fields:
            available_fields = [f for f in fields if f in target_fields]
            if available_fields:
                result = result[available_fields]
        else:
            result = result[target_fields]

        return result

    except Exception as e:
        warnings.warn(f"get_money_flow_pro 失败: {e}")
        return pd.DataFrame()


def _standardize_pro_columns(df):
    """标准化 akshare 的资金流向数据到 inflow/outflow/netflow 体系"""
    column_mapping = {
        "超超大单流入": "inflow_xl",
        "超大单流入": "inflow_xl",
        "大单流入": "inflow_l",
        "中单流入": "inflow_m",
        "小单流入": "inflow_s",
        "超超大单流出": "outflow_xl",
        "超大单流出": "outflow_xl",
        "大单流出": "outflow_l",
        "中单流出": "outflow_m",
        "小单流出": "outflow_s",
        "超超大单净流入": "netflow_xl",
        "超大单净流入": "netflow_xl",
        "大单净流入": "netflow_l",
        "中单净流入": "netflow_m",
        "小单净流入": "netflow_s",
        "主力净流入": "netflow_xl",
        "主力净流入-净额": "netflow_xl",
    }

    new_columns = {}
    for col in df.columns:
        col_str = str(col)
        if col_str in column_mapping:
            new_columns[col] = column_mapping[col_str]
        else:
            for key, value in column_mapping.items():
                if key in col_str:
                    new_columns[col] = value
                    break

    if new_columns:
        df = df.rename(columns=new_columns)

    if "date" not in df.columns:
        date_col = None
        for col in df.columns:
            if "日期" in str(col) or "date" in str(col).lower():
                date_col = col
                break
        if date_col:
            df = df.rename(columns={date_col: "date"})

    for field in [
        "inflow_xl",
        "inflow_l",
        "inflow_m",
        "inflow_s",
        "outflow_xl",
        "outflow_l",
        "outflow_m",
        "outflow_s",
        "netflow_xl",
        "netflow_l",
        "netflow_m",
        "netflow_s",
    ]:
        if field not in df.columns:
            df[field] = 0.0

    return df


__all__ = [
    "get_money_flow",
    "get_sector_money_flow",
    "get_money_flow_rank",
    "get_money_flow_pro",
]
