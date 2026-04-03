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


def _get_akshare():
    """延迟导入 akshare，避免顶层依赖耦合"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        warnings.warn("AkShare 未安装，资金流向功能将不可用")
        return None


def get_money_flow(security=None, start_date=None, end_date=None, count=None):
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
    ak = _get_akshare()
    if ak is None:
        warnings.warn("AkShare 未安装，get_money_flow 不可用")
        return pd.DataFrame()

    try:
        # 使用 akshare 获取个股资金流
        # 个股资金流
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
                    single_df = _get_single_stock_money_flow(code, start_date, end_date, count)
                    if not single_df.empty:
                        results.append(single_df)
                df = pd.concat(results, ignore_index=True) if results else pd.DataFrame()
        else:
            # 全部股票 - 返回当日资金流排名
            df = _get_all_stocks_money_flow()

        return df

    except Exception as e:
        warnings.warn(f"get_money_flow 失败: {e}")
        return pd.DataFrame()


def _normalize_code(stock):
    """将聚宽代码转换为6位数字代码"""
    if stock.startswith('sh') or stock.startswith('sz'):
        return stock[2:].zfill(6)
    if stock.endswith('.XSHG') or stock.endswith('.XSHE'):
        return stock[:6]
    return stock.zfill(6)


def _get_single_stock_money_flow(code, start_date=None, end_date=None, count=None):
    """获取单个股票的资金流向"""
    ak = _get_akshare()
    if ak is None:
        return pd.DataFrame()

    try:
        # 尝试使用 akshare 的个股资金流接口
        try:
            # 个股资金流向历史数据
            df = ak.stock_individual_fund_flow(stock=code, market='sh' if code.startswith('6') else 'sz')
            if df is not None and not df.empty:
                # 标准化列名
                df = _standardize_columns(df)
                df['code'] = code

                # 日期过滤
                if start_date:
                    df = df[df['date'] >= start_date]
                if end_date:
                    df = df[df['date'] <= end_date]
                if count:
                    df = df.tail(count)

                return df
        except Exception:
            pass

        # 备用接口：当日资金流
        try:
            df = ak.stock_individual_fund_flow_rank(indicator='今日')
            if df is not None and not df.empty:
                df = _standardize_columns(df)
                df = df[df['code'] == code]
                return df
        except Exception:
            pass

        return pd.DataFrame()

    except Exception as e:
        warnings.warn(f"获取 {code} 资金流向失败: {e}")
        return pd.DataFrame()


def _get_all_stocks_money_flow():
    """获取全部股票资金流向排名"""
    ak = _get_akshare()
    if ak is None:
        return pd.DataFrame()

    try:
        # 个股资金流排名
        df = ak.stock_individual_fund_flow_rank(indicator='今日')
        if df is not None and not df.empty:
            df = _standardize_columns(df)
            return df
    except Exception:
        pass

    return pd.DataFrame()


def _standardize_columns(df):
    """标准化列名"""
    column_mapping = {
        '代码': 'code',
        '名称': 'name',
        '日期': 'date',
        '收盘价': 'close',
        '涨跌幅': 'pct_change',
        '主力净流入': 'main_net_inflow',
        '小单净流入': 'small_net_inflow',
        '中单净流入': 'medium_net_inflow',
        '大单净流入': 'large_net_inflow',
        '超大单净流入': 'xlarge_net_inflow',
        '主力净流入占比': 'main_net_inflow_pct',
        '净流入': 'net_inflow',
        '主力净流入-净额': 'main_net_inflow',
        '主力净流入-净占比': 'main_net_inflow_pct',
        '超大单净流入-净额': 'xlarge_net_inflow',
        '大单净流入-净额': 'large_net_inflow',
        '中单净流入-净额': 'medium_net_inflow',
        '小单净流入-净额': 'small_net_inflow',
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
    ak = _get_akshare()
    if ak is None:
        warnings.warn("AkShare 未安装，get_sector_money_flow 不可用")
        return pd.DataFrame()

    try:
        # 行业资金流
        try:
            df = ak.stock_board_industry_fund_flow_rank(indicator='今日')
            if df is not None and not df.empty:
                df = _standardize_columns(df)
                if sector:
                    df = df[df['name'].str.contains(sector) | df['code'].str.contains(sector)]
                return df
        except Exception:
            pass

        # 概念资金流
        try:
            df = ak.stock_board_concept_fund_flow_rank(indicator='今日')
            if df is not None and not df.empty:
                df = _standardize_columns(df)
                if sector:
                    df = df[df['name'].str.contains(sector) | df['code'].str.contains(sector)]
                return df
        except Exception:
            pass

        return pd.DataFrame()

    except Exception as e:
        warnings.warn(f"get_sector_money_flow 失败: {e}")
        return pd.DataFrame()


def get_money_flow_rank(top_n=50, direction='inflow'):
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
    if 'main_net_inflow' in df.columns:
        if direction == 'inflow':
            df = df.sort_values('main_net_inflow', ascending=False).head(top_n)
        else:
            df = df.sort_values('main_net_inflow', ascending=True).head(top_n)

    return df


__all__ = [
    'get_money_flow',
    'get_sector_money_flow',
    'get_money_flow_rank',
]