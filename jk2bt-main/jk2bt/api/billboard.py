"""
龙虎榜 API 模块
实现龙虎榜数据获取和机构持仓数据查询

聚宽兼容接口:
- get_billboard_list: 获取龙虎榜数据
- get_institutional_holdings: 获取机构持仓数据

数据源说明:
- 龙虎榜数据为特殊数据，使用 akshare 作为数据源
- 采用延迟导入，避免顶层依赖耦合
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Union
import warnings
from datetime import datetime, timedelta


def _get_akshare():
    """延迟导入 akshare，避免顶层依赖耦合"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        warnings.warn("AkShare未安装，龙虎榜功能将不可用")
        return None


def _normalize_symbol(symbol: str) -> str:
    """
    将聚宽格式股票代码转换为纯数字代码

    支持: 600519.XSHG -> 600519, 000001.XSHE -> 000001
    """
    if symbol is None:
        return None
    if "." in symbol:
        return symbol.split(".")[0].zfill(6)
    return symbol.zfill(6)


def _jq_symbol(code: str) -> str:
    """
    将纯数字代码转换为聚宽格式

    支持: 600519 -> 600519.XSHG, 000001 -> 000001.XSHE
    """
    if code is None:
        return None
    code = str(code).zfill(6)
    if code.startswith("6"):
        return f"{code}.XSHG"
    return f"{code}.XSHE"


# =====================================================================
# get_billboard_list - 龙虎榜数据
# =====================================================================

def get_billboard_list(
    stock: Optional[Union[str, List[str]]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
) -> pd.DataFrame:
    """
    获取龙虎榜数据

    聚宽兼容接口，数据来源: AkShare

    参数:
        stock: 股票代码或股票列表，None 表示获取全部
               支持格式: '600519', '600519.XSHG', ['600519', '000001']
        start_date: 开始日期，格式 'YYYY-MM-DD'
        end_date: 结束日期，格式 'YYYY-MM-DD'
        count: 获取最近 N 个交易日的数据

    返回:
        DataFrame，包含龙虎榜数据:
        - code: 股票代码 (聚宽格式，如 600519.XSHG)
        - date: 日期
        - direction: 方向 (买入/卖出)
        - broker_name: 券商名称/营业部名称
        - buy_value: 买入金额 (元)
        - sell_value: 卖出金额 (元)
        - net_value: 净买入金额 (元)
        - buy_ratio: 买入金额占总成交比
        - sell_ratio: 卖出金额占总成交比
        - reason: 上榜原因

    示例:
        # 获取最近10天全部龙虎榜数据
        df = get_billboard_list(count=10)

        # 获取特定股票的龙虎榜数据
        df = get_billboard_list(stock='600519.XSHG', start_date='2024-01-01')

        # 获取日期范围内的龙虎榜数据
        df = get_billboard_list(start_date='2024-01-01', end_date='2024-01-31')
    """
    ak = _get_akshare()
    if ak is None:
        return pd.DataFrame(columns=[
            'code', 'date', 'direction', 'broker_name', 'buy_value',
            'sell_value', 'net_value', 'buy_ratio', 'sell_ratio', 'reason'
        ])

    # 处理股票代码参数
    if isinstance(stock, str):
        stock_codes = [_normalize_symbol(stock)]
    elif isinstance(stock, list):
        stock_codes = [_normalize_symbol(s) for s in stock]
    else:
        stock_codes = None

    # 处理日期参数
    if count and not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if count and not start_date:
        # 龙虎榜数据按交易日计算，count个交易日大约需要count*2个自然日
        start_date = (datetime.now() - timedelta(days=count * 3)).strftime("%Y-%m-%d")

    all_data = []

    try:
        # 尝试获取龙虎榜明细数据
        # AkShare 接口: stock_lhb_detail_em
        # 参数: start_date, end_date

        df = ak.stock_lhb_detail_em(
            start_date=start_date.replace("-", "") if start_date else "20200101",
            end_date=end_date.replace("-", "") if end_date else datetime.now().strftime("%Y%m%d"),
        )

        if df is None or df.empty:
            warnings.warn("龙虎榜数据为空")
            return pd.DataFrame(columns=[
                'code', 'date', 'direction', 'broker_name', 'buy_value',
                'sell_value', 'net_value', 'buy_ratio', 'sell_ratio', 'reason'
            ])

        # 中文列名映射到英文
        column_mapping = {
            "代码": "code_raw",
            "名称": "name",
            "收盘价": "close",
            "涨跌幅": "change_pct",
            "龙虎榜净买": "net_value",
            "龙虎榜买入额": "buy_value",
            "龙虎榜卖出额": "sell_value",
            "龙虎榜成交额": "total_value",
            "市场总成交额": "market_value",
            "净买额占总成交比": "net_ratio",
            "成交额占总成交比": "total_ratio",
            "上榜原因": "reason",
            "上榜日期": "date",
        }

        # 重命名已存在的列
        rename_cols = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=rename_cols)

        # 标准化日期
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        elif df.index.name == "日期" or "日期" in df.columns:
            date_col = df.index if df.index.name == "日期" else df["日期"]
            df["date"] = pd.to_datetime(date_col, errors="coerce")

        # 格式化股票代码为聚宽格式
        if "code_raw" in df.columns:
            df["code"] = df["code_raw"].apply(_jq_symbol)
        elif "code" in df.columns:
            df["code"] = df["code"].apply(_jq_symbol)

        # 根据股票过滤
        if stock_codes and "code" in df.columns:
            # 转换 stock_codes 为聚宽格式进行匹配
            jq_codes = [_jq_symbol(c) for c in stock_codes]
            df = df[df["code"].isin(jq_codes)]

        # 日期过滤
        if start_date and "date" in df.columns:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date and "date" in df.columns:
            df = df[df["date"] <= pd.to_datetime(end_date)]

        # 按 count 限制
        if count and "date" in df.columns:
            unique_dates = df["date"].sort_values(ascending=False).unique()[:count]
            df = df[df["date"].isin(unique_dates)]

        # 尝试获取更详细的营业部数据
        try:
            detail_dfs = _get_billboard_detail(start_date, end_date, stock_codes)
            if not detail_dfs.empty:
                all_data.append(detail_dfs)
        except Exception as e:
            warnings.warn(f"获取龙虎榜明细数据失败: {e}")

        # 如果明细数据为空，使用汇总数据
        if not all_data:
            # 添加默认字段
            if "direction" not in df.columns:
                df["direction"] = "综合"
            if "broker_name" not in df.columns:
                df["broker_name"] = "汇总"

            # 确保数值字段存在
            for col in ["buy_value", "sell_value", "net_value"]:
                if col not in df.columns:
                    df[col] = 0.0

            # 选择需要的列
            output_cols = [
                'code', 'date', 'direction', 'broker_name', 'buy_value',
                'sell_value', 'net_value', 'reason'
            ]
            available_cols = [c for c in output_cols if c in df.columns]
            result = df[available_cols].copy()

            # 添加可选列
            if "buy_ratio" in df.columns:
                result["buy_ratio"] = df["buy_ratio"]
            if "sell_ratio" in df.columns:
                result["sell_ratio"] = df["sell_ratio"]

            return result.reset_index(drop=True)

        # 合并明细数据
        result = pd.concat(all_data, ignore_index=True)
        return result

    except Exception as e:
        warnings.warn(f"获取龙虎榜数据失败: {e}")
        return pd.DataFrame(columns=[
            'code', 'date', 'direction', 'broker_name', 'buy_value',
            'sell_value', 'net_value', 'buy_ratio', 'sell_ratio', 'reason'
        ])


def _get_billboard_detail(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    stock_codes: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    获取龙虎榜详细营业部数据

    内部函数，获取买卖营业部明细
    """
    ak = _get_akshare()
    if ak is None:
        return pd.DataFrame()

    all_details = []

    try:
        # 获取龙虎榜每日明细
        # AkShare 接口: stock_lhb_stock_detail_em
        # 按日期遍历获取

        if start_date:
            current_date = pd.to_datetime(start_date)
        else:
            current_date = datetime.now() - timedelta(days=30)

        if end_date:
            end_dt = pd.to_datetime(end_date)
        else:
            end_dt = datetime.now()

        # 限制查询天数，避免过多请求
        max_days = 30
        days_count = 0

        while current_date <= end_dt and days_count < max_days:
            date_str = current_date.strftime("%Y%m%d")

            try:
                # 获取当日龙虎榜股票列表
                daily_df = ak.stock_lhb_stock_detail_em(date=date_str)

                if daily_df is not None and not daily_df.empty:
                    # 中文列名映射
                    column_mapping = {
                        "代码": "code_raw",
                        "名称": "name",
                        "收盘价": "close",
                        "涨跌幅": "change_pct",
                        "龙虎榜净买": "net_value",
                        "龙虎榜买入额": "buy_value",
                        "龙虎榜卖出额": "sell_value",
                        "上榜原因": "reason",
                    }

                    rename_cols = {k: v for k, v in column_mapping.items() if k in daily_df.columns}
                    daily_df = daily_df.rename(columns=rename_cols)
                    daily_df["date"] = current_date

                    # 格式化股票代码
                    if "code_raw" in daily_df.columns:
                        daily_df["code"] = daily_df["code_raw"].apply(_jq_symbol)

                    # 股票过滤
                    if stock_codes and "code" in daily_df.columns:
                        jq_codes = [_jq_symbol(c) for c in stock_codes]
                        daily_df = daily_df[daily_df["code"].isin(jq_codes)]

                    if not daily_df.empty:
                        all_details.append(daily_df)

            except Exception:
                # 该日期可能没有数据，跳过
                pass

            current_date += timedelta(days=1)
            days_count += 1

        if not all_details:
            return pd.DataFrame()

        result = pd.concat(all_details, ignore_index=True)

        # 添加默认字段
        if "direction" not in result.columns:
            result["direction"] = "综合"
        if "broker_name" not in result.columns:
            result["broker_name"] = "汇总"

        return result

    except Exception as e:
        warnings.warn(f"获取龙虎榜明细数据失败: {e}")
        return pd.DataFrame()


# =====================================================================
# get_institutional_holdings - 机构持仓数据
# =====================================================================

def get_institutional_holdings(
    stock: str,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取机构持仓数据

    聚宽兼容接口，数据来源: AkShare

    参数:
        stock: 股票代码，支持 '600519' 或 '600519.XSHG' 格式
        date: 查询日期，格式 'YYYY-MM-DD'，默认获取最新数据

    返回:
        DataFrame，包含机构持仓数据:
        - code: 股票代码 (聚宽格式)
        - institution_name: 机构名称
        - institution_type: 机构类型
        - holding_shares: 持股数量
        - holding_ratio: 持股比例 (%)
        - holding_value: 持股市值
        - change_shares: 变动股数
        - change_ratio: 变动比例 (%)
        - report_date: 报告日期

    示例:
        # 获取某股票的机构持仓
        df = get_institutional_holdings('600519.XSHG')

        # 获取指定日期的机构持仓
        df = get_institutional_holdings('600519', date='2024-03-31')
    """
    ak = _get_akshare()
    if ak is None:
        return pd.DataFrame(columns=[
            'code', 'institution_name', 'institution_type', 'holding_shares',
            'holding_ratio', 'holding_value', 'change_shares', 'change_ratio', 'report_date'
        ])

    # 标准化股票代码
    code = _normalize_symbol(stock)
    jq_code = _jq_symbol(code)

    all_data = []

    try:
        # 尝试获取十大股东数据
        try:
            df_shareholders = ak.stock_zh_a_gdhs(symbol=code)

            if df_shareholders is not None and not df_shareholders.empty:
                # 中文列名映射
                column_mapping = {
                    "股东名称": "institution_name",
                    "持股数量": "holding_shares",
                    "持股比例": "holding_ratio",
                    "增减": "change_shares",
                    "变化": "change_ratio",
                    "报告期": "report_date",
                    "股东性质": "institution_type",
                }

                rename_cols = {k: v for k, v in column_mapping.items() if k in df_shareholders.columns}
                df_shareholders = df_shareholders.rename(columns=rename_cols)

                df_shareholders["code"] = jq_code

                # 添加默认值
                if "holding_value" not in df_shareholders.columns:
                    df_shareholders["holding_value"] = None

                all_data.append(df_shareholders)

        except Exception as e:
            warnings.warn(f"获取股东数据失败: {e}")

        # 尝试获取机构持股数据
        try:
            # 尝试不同的 AkShare 接口
            # stock_institute_hold 接口
            df_institute = ak.stock_institute_hold(stock=code)

            if df_institute is not None and not df_institute.empty:
                # 中文列名映射
                column_mapping = {
                    "机构名称": "institution_name",
                    "机构类型": "institution_type",
                    "持股数": "holding_shares",
                    "持股比例": "holding_ratio",
                    "持股市值": "holding_value",
                    "占流通股比例": "float_ratio",
                    "报告期": "report_date",
                    "持股变动": "change_shares",
                    "变动比例": "change_ratio",
                }

                rename_cols = {k: v for k, v in column_mapping.items() if k in df_institute.columns}
                df_institute = df_institute.rename(columns=rename_cols)

                df_institute["code"] = jq_code

                all_data.append(df_institute)

        except Exception:
            # 该接口可能不存在或返回空，静默失败
            pass

        # 尝试获取基金持股数据
        try:
            df_fund = ak.stock_fund_hold_stock(symbol=code)

            if df_fund is not None and not df_fund.empty:
                # 中文列名映射
                column_mapping = {
                    "基金名称": "institution_name",
                    "基金代码": "fund_code",
                    "持股数": "holding_shares",
                    "持股比例": "holding_ratio",
                    "持股市值": "holding_value",
                    "报告期": "report_date",
                    "占流通股比例": "float_ratio",
                }

                rename_cols = {k: v for k, v in column_mapping.items() if k in df_fund.columns}
                df_fund = df_fund.rename(columns=rename_cols)

                df_fund["code"] = jq_code
                df_fund["institution_type"] = "基金"

                all_data.append(df_fund)

        except Exception:
            pass

        if not all_data:
            return pd.DataFrame(columns=[
                'code', 'institution_name', 'institution_type', 'holding_shares',
                'holding_ratio', 'holding_value', 'change_shares', 'change_ratio', 'report_date'
            ])

        # 合并数据
        result = pd.concat(all_data, ignore_index=True)

        # 标准化日期
        if "report_date" in result.columns:
            result["report_date"] = pd.to_datetime(result["report_date"], errors="coerce")

        # 日期过滤
        if date and "report_date" in result.columns:
            target_date = pd.to_datetime(date)
            result = result[result["report_date"] <= target_date]

        # 选择输出列
        output_cols = [
            'code', 'institution_name', 'institution_type', 'holding_shares',
            'holding_ratio', 'holding_value', 'change_shares', 'change_ratio', 'report_date'
        ]
        available_cols = [c for c in output_cols if c in result.columns]

        result = result[available_cols].copy()

        # 去重
        if "institution_name" in result.columns and "report_date" in result.columns:
            result = result.drop_duplicates(subset=["institution_name", "report_date"], keep="last")

        # 按持股比例降序排列
        if "holding_ratio" in result.columns:
            result = result.sort_values("holding_ratio", ascending=False)

        return result.reset_index(drop=True)

    except Exception as e:
        warnings.warn(f"获取机构持仓数据失败 {stock}: {e}")
        return pd.DataFrame(columns=[
            'code', 'institution_name', 'institution_type', 'holding_shares',
            'holding_ratio', 'holding_value', 'change_shares', 'change_ratio', 'report_date'
        ])


# =====================================================================
# 辅助函数 - 获取龙虎榜热门股票
# =====================================================================

def get_billboard_hot_stocks(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    获取龙虎榜热门股票

    根据龙虎榜净买入金额排序，返回热门股票

    参数:
        start_date: 开始日期
        end_date: 结束日期
        top_n: 返回数量

    返回:
        DataFrame，包含热门股票及其净买入金额
    """
    df = get_billboard_list(start_date=start_date, end_date=end_date)

    if df.empty:
        return pd.DataFrame()

    if "code" in df.columns and "net_value" in df.columns:
        # 按股票汇总净买入
        hot = df.groupby("code").agg({
            "net_value": "sum",
            "buy_value": "sum",
            "sell_value": "sum",
            "date": "count"
        }).reset_index()

        hot.columns = ["code", "total_net_value", "total_buy_value", "total_sell_value", "appearances"]
        hot = hot.sort_values("total_net_value", ascending=False).head(top_n)

        return hot.reset_index(drop=True)

    return pd.DataFrame()


# =====================================================================
# 辅助函数 - 获取营业部买卖统计
# =====================================================================

def get_broker_statistics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    获取营业部买卖统计

    统计营业部的买卖金额和操作次数

    参数:
        start_date: 开始日期
        end_date: 结束日期
        top_n: 返回数量

    返回:
        DataFrame，包含营业部统计数据
    """
    df = get_billboard_list(start_date=start_date, end_date=end_date)

    if df.empty or "broker_name" not in df.columns:
        return pd.DataFrame()

    # 按营业部统计
    broker_stats = df.groupby("broker_name").agg({
        "buy_value": "sum",
        "sell_value": "sum",
        "net_value": "sum",
        "code": "count"
    }).reset_index()

    broker_stats.columns = ["broker_name", "total_buy", "total_sell", "total_net", "trade_count"]
    broker_stats = broker_stats.sort_values("total_net", ascending=False).head(top_n)

    return broker_stats.reset_index(drop=True)


__all__ = [
    "get_billboard_list",
    "get_institutional_holdings",
    "get_billboard_hot_stocks",
    "get_broker_statistics",
]