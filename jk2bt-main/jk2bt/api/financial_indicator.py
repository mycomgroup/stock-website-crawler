"""
jk2bt/api/financial_indicator.py
金融行业指标 API 模块

提供银行、证券、保险专项财务指标查询接口。
数据源: AkShare

主要功能:
- bank_indicator: 银行专项指标
- security_indicator: 证券公司专项指标
- insurance_indicator: 保险公司专项指标
"""

import pandas as pd
from typing import Optional, List, Union
import warnings


def _get_akshare():
    """延迟导入 akshare"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        warnings.warn("akshare 未安装")
        return None


def _normalize_code(code: str) -> str:
    """标准化股票代码"""
    return (
        code.replace(".XSHG", "")
        .replace(".XSHE", "")
        .replace("sh", "")
        .replace("sz", "")
        .zfill(6)
    )


def _to_jq_code(code: str) -> str:
    """转换为聚宽格式"""
    code = _normalize_code(code)
    if code.startswith("6"):
        return f"{code}.XSHG"
    elif code.startswith(("0", "3")):
        return f"{code}.XSHE"
    return code


def bank_indicator(
    security: Optional[Union[str, List[str]]] = None,
    fields: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取银行专项指标。

    聚宽兼容接口

    银行专项指标包括:
    - 资本充足率
    - 不良贷款率
    - 拨备覆盖率
    - 净息差
    - 存贷比
    等

    参数
    ----
    security : str or list of str, optional
        银行股票代码，None 表示获取所有银行
    fields : list of str, optional
        返回字段列表
    start_date : str, optional
        开始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        银行专项指标数据

    示例
    ----
    >>> df = bank_indicator('600036.XSHG')  # 招商银行
    >>> print(df.columns.tolist())
    """
    ak = _get_akshare()
    if ak is None:
        return _get_empty_indicator_frame("bank")

    results = []

    try:
        # 方法1: 使用银行专项指标接口
        try:
            df = ak.stock_bank_indicator_em()
            if df is not None and not df.empty:
                results.append(_process_bank_data(df, security, fields))
        except Exception:
            pass

        # 方法2: 使用财务分析接口
        if not results or all(r.empty for r in results):
            securities = _get_bank_list() if security is None else (
                [security] if isinstance(security, str) else security
            )

            for sec in securities:
                try:
                    code = _normalize_code(sec)
                    df = ak.stock_financial_analysis_indicator(symbol=code)
                    if df is not None and not df.empty:
                        processed = _process_financial_data(df, sec, "bank", fields)
                        if not processed.empty:
                            results.append(processed)
                except Exception:
                    continue

    except Exception as e:
        warnings.warn(f"获取银行指标失败: {e}")

    if not results or all(r.empty for r in results):
        return _get_empty_indicator_frame("bank")

    return pd.concat([r for r in results if not r.empty], ignore_index=True)


def _get_bank_list() -> List[str]:
    """获取银行股列表"""
    # 主要上市银行代码
    banks = [
        "601398.XSHG",  # 工商银行
        "601288.XSHG",  # 农业银行
        "601939.XSHG",  # 建设银行
        "601988.XSHG",  # 中国银行
        "600036.XSHG",  # 招商银行
        "601166.XSHG",  # 兴业银行
        "600000.XSHG",  # 浦发银行
        "600016.XSHG",  # 民生银行
        "600015.XSHG",  # 华夏银行
        "601818.XSHG",  # 光大银行
        "600030.XSHG",  # 中信银行
        "601998.XSHG",  # 中信银行
        "002142.XSHE",  # 宁波银行
        "002807.XSHE",  # 江阴银行
        "600908.XSHG",  # 无锡银行
    ]
    return banks


def _process_bank_data(
    df: pd.DataFrame,
    security: Optional[Union[str, List[str]]],
    fields: Optional[List[str]],
) -> pd.DataFrame:
    """处理银行数据"""
    result = df.copy()

    # 筛选股票
    if security:
        securities = [security] if isinstance(security, str) else security
        code_col = None
        for col in ["股票代码", "代码", "code"]:
            if col in result.columns:
                code_col = col
                break
        if code_col:
            mask = result[code_col].apply(lambda x: _to_jq_code(str(x)) in securities)
            result = result[mask]

    # 筛选字段
    if fields:
        available_fields = ["code", "date"] + [f for f in fields if f in result.columns]
        result = result[[f for f in available_fields if f in result.columns]]

    return result


def _process_financial_data(
    df: pd.DataFrame,
    security: str,
    industry: str,
    fields: Optional[List[str]],
) -> pd.DataFrame:
    """处理财务数据"""
    result = pd.DataFrame()
    result["code"] = [security]

    # 提取关键指标
    for col in df.columns:
        if fields and col not in fields:
            continue

        if "日期" in col or "date" in col.lower():
            result["date"] = df[col].iloc[-1] if len(df) > 0 else None
        else:
            result[col] = df[col].iloc[-1] if len(df) > 0 else None

    return result


def security_indicator(
    security: Optional[Union[str, List[str]]] = None,
    fields: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取证券公司专项指标。

    聚宽兼容接口

    证券公司专项指标包括:
    - 净资本
    - 净资本/负债
    - 净资本/各项风险资本准备之和
    - 自营权益类证券及证券衍生品/净资本
    等

    参数
    ----
    security : str or list of str, optional
        证券公司股票代码，None 表示获取所有证券公司
    fields : list of str, optional
        返回字段列表
    start_date : str, optional
        开始日期
    end_date : str, optional
        结束日期

    返回
    ----
    pd.DataFrame
        证券公司专项指标数据

    示例
    ----
    >>> df = security_indicator('600030.XSHG')  # 中信证券
    """
    ak = _get_akshare()
    if ak is None:
        return _get_empty_indicator_frame("security")

    results = []

    try:
        # 使用财务分析接口
        securities = _get_security_list() if security is None else (
            [security] if isinstance(security, str) else security
        )

        for sec in securities:
            try:
                code = _normalize_code(sec)
                df = ak.stock_financial_analysis_indicator(symbol=code)
                if df is not None and not df.empty:
                    processed = _process_financial_data(df, sec, "security", fields)
                    if not processed.empty:
                        results.append(processed)
            except Exception:
                continue

    except Exception as e:
        warnings.warn(f"获取证券公司指标失败: {e}")

    if not results or all(r.empty for r in results):
        return _get_empty_indicator_frame("security")

    return pd.concat([r for r in results if not r.empty], ignore_index=True)


def _get_security_list() -> List[str]:
    """获取证券公司股列表"""
    securities = [
        "600030.XSHG",  # 中信证券
        "601211.XSHG",  # 国泰君安
        "600837.XSHG",  # 海通证券
        "600066.XSHG",  # 华鑫股份
        "601688.XSHG",  # 华泰证券
        "600109.XSHG",  # 国金证券
        "601788.XSHG",  # 光大证券
        "601377.XSHG",  # 兴业证券
        "600018.XSHG",  # 招商证券
        "601198.XSHG",  # 东兴证券
    ]
    return securities


def insurance_indicator(
    security: Optional[Union[str, List[str]]] = None,
    fields: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取保险公司专项指标。

    聚宽兼容接口

    保险公司专项指标包括:
    - 总资产
    - 净资产
    - 保费收入
    - 赔付支出
    - 投资收益率
    等

    参数
    ----
    security : str or list of str, optional
        保险公司股票代码，None 表示获取所有保险公司
    fields : list of str, optional
        返回字段列表
    start_date : str, optional
        开始日期
    end_date : str, optional
        结束日期

    返回
    ----
    pd.DataFrame
        保险公司专项指标数据

    示例
    ----
    >>> df = insurance_indicator('601318.XSHG')  # 中国平安
    """
    ak = _get_akshare()
    if ak is None:
        return _get_empty_indicator_frame("insurance")

    results = []

    try:
        # 使用财务分析接口
        securities = _get_insurance_list() if security is None else (
            [security] if isinstance(security, str) else security
        )

        for sec in securities:
            try:
                code = _normalize_code(sec)
                df = ak.stock_financial_analysis_indicator(symbol=code)
                if df is not None and not df.empty:
                    processed = _process_financial_data(df, sec, "insurance", fields)
                    if not processed.empty:
                        results.append(processed)
            except Exception:
                continue

    except Exception as e:
        warnings.warn(f"获取保险公司指标失败: {e}")

    if not results or all(r.empty for r in results):
        return _get_empty_indicator_frame("insurance")

    return pd.concat([r for r in results if not r.empty], ignore_index=True)


def _get_insurance_list() -> List[str]:
    """获取保险公司股列表"""
    insurances = [
        "601318.XSHG",  # 中国平安
        "601601.XSHG",  # 中国太保
        "601336.XSHG",  # 新华保险
        "601628.XSHG",  # 中国人寿
        "000001.XSHE",  # 平安银行
    ]
    return insurances


def _get_empty_indicator_frame(industry: str) -> pd.DataFrame:
    """返回空的指标 DataFrame"""
    return pd.DataFrame(columns=["code", "date"])


# 聚宽风格别名
bank_indicator_jq = bank_indicator
security_indicator_jq = security_indicator
insurance_indicator_jq = insurance_indicator


__all__ = [
    "bank_indicator",
    "security_indicator",
    "insurance_indicator",
    "bank_indicator_jq",
    "security_indicator_jq",
    "insurance_indicator_jq",
]