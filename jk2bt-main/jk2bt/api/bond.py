"""
bond 模块 - 可转债专项JQData接口

提供聚宽风格的可转债数据查询接口：
1. bond.CONBOND_CONVERT_PRICE_ADJUST - 可转债转股价格调整
2. bond.CONBOND_DAILY_CONVERT - 可转债每日转股统计
3. bond.BOND_BASIC_INFO - 债券基本信息
4. bond.BOND_COUPON - 债券票面利率
5. bond.BOND_INTEREST_PAYMENT - 债券付息事件
6. bond.REPO_DAILY_PRICE - 国债逆回购日行情
7. bond.CONBOND_BASIC_INFO - 可转债基本资料

使用示例：
>>> from jk2bt.api.bond import bond
>>> df = query(bond.CONBOND_CONVERT_PRICE_ADJUST).filter(bond.CONBOND_CONVERT_PRICE_ADJUST.code == '113009.XSHG')
>>> df = query(bond.BOND_BASIC_INFO).filter(bond.BOND_BASIC_INFO.code == '010001.XSHG')
"""

import pandas as pd
import logging
from typing import Optional

from jk2bt.data.market.conversion_bond import (
    get_conversion_bond_list as _get_conversion_bond_list,
    get_conversion_bond_price as _get_conversion_bond_price,
    get_conversion_bond_info as _get_conversion_bond_info,
    get_conversion_bond_detail as _get_conversion_bond_detail,
    get_conversion_info as _get_conversion_info,
    calculate_conversion_value as _calculate_conversion_value,
    calculate_premium_rate as _calculate_premium_rate,
    get_conversion_bond_history as _get_conversion_bond_history,
    get_conversion_price as _get_conversion_price,
    calculate_conversion_premium as _calculate_conversion_premium,
    get_conversion_bond_daily as _get_conversion_bond_daily,
    get_conversion_value as _get_conversion_value,
    _CB_SCHEMA,
)

logger = logging.getLogger(__name__)


class CONBOND_CONVERT_PRICE_ADJUST:
    """
    可转债转股价格调整表 (CONBOND_CONVERT_PRICE_ADJUST)

    字段说明：
    - code: 可转债代码
    - name: 可转债名称
    - pub_date: 发布日期
    - adjust_date: 调整日期
    - new_convert_price: 新的转股价
    - adjust_reason: 调整原因
    """

    code = None
    name = None
    pub_date = None
    adjust_date = None
    new_convert_price = None
    adjust_reason = None


class CONBOND_DAILY_CONVERT:
    """
    可转债每日转股统计表 (CONBOND_DAILY_CONVERT)

    字段说明：
    - date: 日期
    - code: 可转债代码
    - name: 可转债名称
    - exchange_code: 交易所代码
    - issue_number: 发行量
    - convert_price: 转股价
    - daily_convert_number: 当日转股数量
    - acc_convert_number: 累计转股数量
    - acc_convert_ratio: 累计转股比例
    - convert_premium: 转股溢价
    - convert_premium_rate: 转股溢价率
    """

    date = None
    code = None
    name = None
    exchange_code = None
    issue_number = None
    convert_price = None
    daily_convert_number = None
    acc_convert_number = None
    acc_convert_ratio = None
    convert_premium = None
    convert_premium_rate = None


class BOND_BASIC_INFO:
    """
    债券基本信息表 (BOND_BASIC_INFO)

    字段说明：
    - id: 主键ID
    - code: 债券代码
    - short_name: 债券简称
    - full_name: 债券全称
    - list_status_id: 上市状态ID
    - list_status: 上市状态
    - issuer: 发行人
    - company_code: 公司代码
    - exchange_code: 交易所代码
    - exchange: 交易所
    - bond_type: 债券类型
    - bond_form_id: 债券形态ID
    - bond_form: 债券形态
    - list_date: 上市日期
    - delist_date: 退市日期
    - interest_begin_date: 起息日期
    - maturity_date: 到期日期
    - interest_date: 付息日
    - last_cash_date: 最后付息日
    - cash_comment: 付息说明
    """

    id = None
    code = None
    short_name = None
    full_name = None
    list_status_id = None
    list_status = None
    issuer = None
    company_code = None
    exchange_code = None
    exchange = None
    bond_type = None
    bond_form_id = None
    bond_form = None
    list_date = None
    delist_date = None
    interest_begin_date = None
    maturity_date = None
    interest_date = None
    last_cash_date = None
    cash_comment = None


class BOND_COUPON:
    """
    债券票面利率表 (BOND_COUPON)

    字段说明：
    - id: 主键ID
    - code: 债券代码
    - short_name: 债券简称
    - pub_date: 公布日期
    - exchange_code: 交易所代码
    - exchange: 交易所
    - coupon_type_id: 票面利率类型ID
    - coupon_type: 票面利率类型
    - coupon: 票面利率
    - coupon_start_date: 票面利率开始日期
    - coupon_end_date: 票面利率结束日期
    - reference_rate: 参考利率
    - reference_rate_comment: 参考利率说明
    - margin_rate: 利差
    - coupon_upper_limit: 利率上限
    - coupon_lower_limit: 利率下限
    """

    id = None
    code = None
    short_name = None
    pub_date = None
    exchange_code = None
    exchange = None
    coupon_type_id = None
    coupon_type = None
    coupon = None
    coupon_start_date = None
    coupon_end_date = None
    reference_rate = None
    reference_rate_comment = None
    margin_rate = None
    coupon_upper_limit = None
    coupon_lower_limit = None


class BOND_INTEREST_PAYMENT:
    """
    债券付息事件表 (BOND_INTEREST_PAYMENT)

    字段说明：
    - id: 主键ID
    - code: 债券代码
    - name: 债券名称
    - pub_date: 公布日期
    - exchange_code: 交易所代码
    - exchange: 交易所
    - event_type: 事件类型
    - interest_start_date: 计息开始日期
    - coupon: 票面利率
    - interest_end_date: 计息结束日期
    - autual_interest: 实际利息
    - interest_per_unit: 单位利息
    - register_date: 登记日
    - dividend_date: 除权除息日
    - interest_pay_start_date: 付息开始日期
    - interest_pay_end_date: 付息结束日期
    - payment_date: 兑付日
    - payment_per_unit: 单位兑付金额
    - tax_rate: 税率
    - tax_channel: 税收渠道
    """

    id = None
    code = None
    name = None
    pub_date = None
    exchange_code = None
    exchange = None
    event_type = None
    interest_start_date = None
    coupon = None
    interest_end_date = None
    autual_interest = None
    interest_per_unit = None
    register_date = None
    dividend_date = None
    interest_pay_start_date = None
    interest_pay_end_date = None
    payment_date = None
    payment_per_unit = None
    tax_rate = None
    tax_channel = None


class REPO_DAILY_PRICE:
    """
    国债逆回购日行情表 (REPO_DAILY_PRICE)

    字段说明：
    - id: 主键ID
    - date: 日期
    - code: 代码
    - name: 名称
    - exchange_code: 交易所代码
    - pre_close: 前收盘
    - open: 开盘价
    - high: 最高价
    - low: 最低价
    - close: 收盘价
    - volume: 成交量
    - money: 成交额
    - deal_number: 成交笔数
    """

    id = None
    date = None
    code = None
    name = None
    exchange_code = None
    pre_close = None
    open = None
    high = None
    low = None
    close = None
    volume = None
    money = None
    deal_number = None


class CONBOND_BASIC_INFO:
    """
    可转债基本资料表 (CONBOND_BASIC_INFO)

    字段说明：
    - id: 主键ID
    - code: 可转债代码
    - short_name: 可转债简称
    - full_name: 可转债全称
    - list_status_id: 上市状态ID
    - list_status: 上市状态
    - issuer: 发行人
    - company_code: 公司代码
    - issue_start_date: 发行起始日期
    - issue_end_date: 发行结束日期
    - bond_type: 债券类型
    - bond_form_id: 债券形态ID
    - bond_form: 债券形态
    - list_date: 上市日期
    - delist_date: 退市日期
    - interest_begin_date: 起息日期
    - maturity_date: 到期日期
    - interest_date: 付息日
    - last_cash_date: 最后付息日
    - cash_comment: 付息说明
    - convert_price: 转股价格
    - convert_start_date: 转股起始日期
    - convert_end_date: 转股结束日期
    - redeem_price: 赎回价格
    - put_price: 回售价格
    - coupon_rate: 票面利率
    - par_value: 面值
    - issue_amount: 发行总量
    - remain_amount: 剩余规模
    - rating: 评级
    - guarantee: 担保
    - convert_value: 转股价值
    - premium_rate: 溢价率
    """

    id = None
    code = None
    short_name = None
    full_name = None
    list_status_id = None
    list_status = None
    issuer = None
    company_code = None
    issue_start_date = None
    issue_end_date = None
    bond_type = None
    bond_form_id = None
    bond_form = None
    list_date = None
    delist_date = None
    interest_begin_date = None
    maturity_date = None
    interest_date = None
    last_cash_date = None
    cash_comment = None
    convert_price = None
    convert_start_date = None
    convert_end_date = None
    redeem_price = None
    put_price = None
    coupon_rate = None
    par_value = None
    issue_amount = None
    remain_amount = None
    rating = None
    guarantee = None
    convert_value = None
    premium_rate = None


class BondQuery:
    """
    可转债查询模块 - 模拟聚宽 bond 模块

    提供 run_query 兼容接口，支持 query(bond.XXX).filter(...) 语法

    使用示例：
    >>> from jk2bt.api.bond import bond
    >>> df = bond.run_query(bond.CONBOND_CONVERT_PRICE_ADJUST.code == '113009.XSHG')
    >>> df = bond.run_query(bond.CONBOND_DAILY_CONVERT.date == '2024-01-01')
    """

    CONBOND_CONVERT_PRICE_ADJUST = CONBOND_CONVERT_PRICE_ADJUST
    CONBOND_DAILY_CONVERT = CONBOND_DAILY_CONVERT
    BOND_BASIC_INFO = BOND_BASIC_INFO
    BOND_COUPON = BOND_COUPON
    BOND_INTEREST_PAYMENT = BOND_INTEREST_PAYMENT
    REPO_DAILY_PRICE = REPO_DAILY_PRICE
    CONBOND_BASIC_INFO = CONBOND_BASIC_INFO

    def run_query(
        self,
        query_obj,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """
        执行可转债查询

        参数:
            query_obj: 查询对象（表对象或查询表达式）
            force_update: 强制更新
            use_duckdb: 是否使用DuckDB缓存

        返回:
            pd.DataFrame
        """
        table_name = None
        conditions = {}

        if hasattr(query_obj, "__name__"):
            table_name = query_obj.__name__
        elif hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__name__"):
                table_name = query_obj.left.__name__
            elif hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            if hasattr(query_obj, "right"):
                conditions["value"] = query_obj.right

        if hasattr(query_obj, "left") and hasattr(query_obj.left, "name"):
            conditions["field"] = query_obj.left.name

        if table_name == "CONBOND_CONVERT_PRICE_ADJUST":
            return self._query_convert_price_adjust(
                conditions, force_update, use_duckdb
            )
        elif table_name == "CONBOND_DAILY_CONVERT":
            return self._query_daily_convert(conditions, force_update, use_duckdb)
        elif table_name == "BOND_BASIC_INFO":
            return self._query_bond_basic_info(conditions, force_update, use_duckdb)
        elif table_name == "BOND_COUPON":
            return self._query_bond_coupon(conditions, force_update, use_duckdb)
        elif table_name == "BOND_INTEREST_PAYMENT":
            return self._query_bond_interest_payment(
                conditions, force_update, use_duckdb
            )
        elif table_name == "REPO_DAILY_PRICE":
            return self._query_repo_daily_price(conditions, force_update, use_duckdb)
        elif table_name == "CONBOND_BASIC_INFO":
            return self._query_conbond_basic_info(conditions, force_update, use_duckdb)
        else:
            logger.warning(f"[BondQuery] 不支持的表: {table_name}")
            return pd.DataFrame()

    def _query_bond_basic_info(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """查询债券基本信息"""
        try:
            import akshare as ak

            df = ak.bond_zh_hs_spot()
            if df is not None and not df.empty:
                rename_map = {}
                for col in df.columns:
                    if "代码" in col or col == "code":
                        rename_map[col] = "code"
                    elif "简称" in col:
                        rename_map[col] = "short_name"
                    elif "全称" in col:
                        rename_map[col] = "full_name"
                    elif "上市状态" in col or "状态" in col:
                        rename_map[col] = "list_status"
                    elif "发行人" in col:
                        rename_map[col] = "issuer"
                    elif "公司代码" in col:
                        rename_map[col] = "company_code"
                    elif "交易所" in col:
                        rename_map[col] = "exchange"
                    elif "债券类型" in col or "类型" in col:
                        rename_map[col] = "bond_type"
                    elif "形态" in col:
                        rename_map[col] = "bond_form"
                    elif "上市日期" in col:
                        rename_map[col] = "list_date"
                    elif "退市" in col or "摘牌" in col:
                        rename_map[col] = "delist_date"
                    elif "起息" in col:
                        rename_map[col] = "interest_begin_date"
                    elif "到期" in col:
                        rename_map[col] = "maturity_date"
                    elif "付息" in col:
                        rename_map[col] = "interest_date"

                df = df.rename(columns=rename_map)
                df["id"] = range(len(df))

                required_cols = [
                    "id",
                    "code",
                    "short_name",
                    "full_name",
                    "list_status_id",
                    "list_status",
                    "issuer",
                    "company_code",
                    "exchange_code",
                    "exchange",
                    "bond_type",
                    "bond_form_id",
                    "bond_form",
                    "list_date",
                    "delist_date",
                    "interest_begin_date",
                    "maturity_date",
                    "interest_date",
                    "last_cash_date",
                    "cash_comment",
                ]
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = None

                if "exchange" in df.columns and "exchange_code" not in df.columns:
                    df["exchange_code"] = df["exchange"].apply(
                        lambda x: "XSHG" if "上海" in str(x) else "XSHE"
                    )

                return df[required_cols]
        except Exception as e:
            logger.warning(f"[BondQuery] BOND_BASIC_INFO 获取失败: {e}")

        return pd.DataFrame(
            columns=[
                "id",
                "code",
                "short_name",
                "full_name",
                "list_status_id",
                "list_status",
                "issuer",
                "company_code",
                "exchange_code",
                "exchange",
                "bond_type",
                "bond_form_id",
                "bond_form",
                "list_date",
                "delist_date",
                "interest_begin_date",
                "maturity_date",
                "interest_date",
                "last_cash_date",
                "cash_comment",
            ]
        )

    def _query_bond_coupon(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """查询债券票面利率"""
        try:
            import akshare as ak

            df = ak.bond_info_cm()
            if df is not None and not df.empty:
                rename_map = {}
                for col in df.columns:
                    if "代码" in col or col == "code":
                        rename_map[col] = "code"
                    elif "简称" in col:
                        rename_map[col] = "short_name"
                    elif "公告" in col or "pub" in col.lower():
                        rename_map[col] = "pub_date"
                    elif "交易所" in col:
                        rename_map[col] = "exchange"
                    elif "票面利率" in col or "利率" in col:
                        rename_map[col] = "coupon"
                    elif "开始" in col and "日期" in col:
                        rename_map[col] = "coupon_start_date"
                    elif "结束" in col and "日期" in col:
                        rename_map[col] = "coupon_end_date"
                    elif "参考" in col:
                        rename_map[col] = "reference_rate"
                    elif "利差" in col:
                        rename_map[col] = "margin_rate"
                    elif "上限" in col:
                        rename_map[col] = "coupon_upper_limit"
                    elif "下限" in col:
                        rename_map[col] = "coupon_lower_limit"

                df = df.rename(columns=rename_map)
                df["id"] = range(len(df))

                required_cols = [
                    "id",
                    "code",
                    "short_name",
                    "pub_date",
                    "exchange_code",
                    "exchange",
                    "coupon_type_id",
                    "coupon_type",
                    "coupon",
                    "coupon_start_date",
                    "coupon_end_date",
                    "reference_rate",
                    "reference_rate_comment",
                    "margin_rate",
                    "coupon_upper_limit",
                    "coupon_lower_limit",
                ]
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = None

                if "exchange" in df.columns and "exchange_code" not in df.columns:
                    df["exchange_code"] = df["exchange"].apply(
                        lambda x: "XSHG" if "上海" in str(x) else "XSHE"
                    )

                return df[required_cols]
        except Exception as e:
            logger.warning(f"[BondQuery] BOND_COUPON 获取失败: {e}")

        return pd.DataFrame(
            columns=[
                "id",
                "code",
                "short_name",
                "pub_date",
                "exchange_code",
                "exchange",
                "coupon_type_id",
                "coupon_type",
                "coupon",
                "coupon_start_date",
                "coupon_end_date",
                "reference_rate",
                "reference_rate_comment",
                "margin_rate",
                "coupon_upper_limit",
                "coupon_lower_limit",
            ]
        )

    def _query_bond_interest_payment(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """查询债券付息事件"""
        try:
            import akshare as ak

            df = ak.bond_cash_summary_sina()
            if df is not None and not df.empty:
                rename_map = {}
                for col in df.columns:
                    if "代码" in col or col == "code":
                        rename_map[col] = "code"
                    elif "名称" in col or "name" in col.lower():
                        rename_map[col] = "name"
                    elif "公告" in col or "pub" in col.lower():
                        rename_map[col] = "pub_date"
                    elif "交易所" in col:
                        rename_map[col] = "exchange"
                    elif "事件" in col or "类型" in col:
                        rename_map[col] = "event_type"
                    elif "计息开始" in col:
                        rename_map[col] = "interest_start_date"
                    elif "票面利率" in col or "利率" in col:
                        rename_map[col] = "coupon"
                    elif "计息结束" in col:
                        rename_map[col] = "interest_end_date"
                    elif "利息" in col and "单位" not in col:
                        rename_map[col] = "autual_interest"
                    elif "单位利息" in col or "每份" in col:
                        rename_map[col] = "interest_per_unit"
                    elif "登记" in col:
                        rename_map[col] = "register_date"
                    elif "除权" in col or "除息" in col:
                        rename_map[col] = "dividend_date"
                    elif "付息开始" in col:
                        rename_map[col] = "interest_pay_start_date"
                    elif "付息结束" in col:
                        rename_map[col] = "interest_pay_end_date"
                    elif "兑付" in col and "日期" in col:
                        rename_map[col] = "payment_date"
                    elif "单位兑付" in col:
                        rename_map[col] = "payment_per_unit"
                    elif "税率" in col:
                        rename_map[col] = "tax_rate"
                    elif "税收" in col or "渠道" in col:
                        rename_map[col] = "tax_channel"

                df = df.rename(columns=rename_map)
                df["id"] = range(len(df))

                required_cols = [
                    "id",
                    "code",
                    "name",
                    "pub_date",
                    "exchange_code",
                    "exchange",
                    "event_type",
                    "interest_start_date",
                    "coupon",
                    "interest_end_date",
                    "autual_interest",
                    "interest_per_unit",
                    "register_date",
                    "dividend_date",
                    "interest_pay_start_date",
                    "interest_pay_end_date",
                    "payment_date",
                    "payment_per_unit",
                    "tax_rate",
                    "tax_channel",
                ]
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = None

                if "exchange" in df.columns and "exchange_code" not in df.columns:
                    df["exchange_code"] = df["exchange"].apply(
                        lambda x: "XSHG" if "上海" in str(x) else "XSHE"
                    )

                return df[required_cols]
        except Exception as e:
            logger.warning(f"[BondQuery] BOND_INTEREST_PAYMENT 获取失败: {e}")

        return pd.DataFrame(
            columns=[
                "id",
                "code",
                "name",
                "pub_date",
                "exchange_code",
                "exchange",
                "event_type",
                "interest_start_date",
                "coupon",
                "interest_end_date",
                "autual_interest",
                "interest_per_unit",
                "register_date",
                "dividend_date",
                "interest_pay_start_date",
                "interest_pay_end_date",
                "payment_date",
                "payment_per_unit",
                "tax_rate",
                "tax_channel",
            ]
        )

    def _query_repo_daily_price(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """查询国债逆回购日行情"""
        try:
            import akshare as ak

            df = ak.bond_zh_hs_repo()
            if df is not None and not df.empty:
                rename_map = {}
                for col in df.columns:
                    if "日期" in col or "date" in col.lower():
                        rename_map[col] = "date"
                    elif "代码" in col or "code" in col.lower():
                        rename_map[col] = "code"
                    elif "名称" in col or "name" in col.lower():
                        rename_map[col] = "name"
                    elif "前收" in col or "pre" in col.lower():
                        rename_map[col] = "pre_close"
                    elif "开盘" in col or "open" in col.lower():
                        rename_map[col] = "open"
                    elif "最高" in col or "high" in col.lower():
                        rename_map[col] = "high"
                    elif "最低" in col or "low" in col.lower():
                        rename_map[col] = "low"
                    elif "收盘" in col or "close" in col.lower():
                        rename_map[col] = "close"
                    elif "成交量" in col or "volume" in col.lower():
                        rename_map[col] = "volume"
                    elif "成交额" in col or "money" in col.lower():
                        rename_map[col] = "money"
                    elif "笔数" in col or "deal" in col.lower():
                        rename_map[col] = "deal_number"

                df = df.rename(columns=rename_map)
                df["id"] = range(len(df))
                df["exchange_code"] = "XSHG"
                return df
        except Exception as e:
            logger.warning(f"[BondQuery] REPO_DAILY_PRICE 获取失败: {e}")

        logger.debug(
            "[BondQuery] REPO_DAILY_PRICE: akshare 暂无此接口，返回空DataFrame"
        )
        return pd.DataFrame(
            columns=[
                "id",
                "date",
                "code",
                "name",
                "exchange_code",
                "pre_close",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "money",
                "deal_number",
            ]
        )

    def _query_conbond_basic_info(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """查询可转债基本资料"""
        try:
            import akshare as ak

            df = ak.bond_cb_jsl()
            if df is not None and not df.empty:
                rename_map = {}
                for col in df.columns:
                    if "代码" in col or col == "code":
                        rename_map[col] = "code"
                    elif "简称" in col or col == "short_name":
                        rename_map[col] = "short_name"
                    elif "全称" in col or col == "full_name":
                        rename_map[col] = "full_name"
                    elif "上市状态" in col or col == "list_status":
                        rename_map[col] = "list_status"
                    elif "发行人" in col or col == "issuer":
                        rename_map[col] = "issuer"
                    elif "公司代码" in col or col == "company_code":
                        rename_map[col] = "company_code"
                    elif "发行开始" in col or col == "issue_start_date":
                        rename_map[col] = "issue_start_date"
                    elif "发行结束" in col or col == "issue_end_date":
                        rename_map[col] = "issue_end_date"
                    elif "债券类型" in col or col == "bond_type":
                        rename_map[col] = "bond_type"
                    elif "上市日期" in col or col == "list_date":
                        rename_map[col] = "list_date"
                    elif "退市日期" in col or col == "delist_date":
                        rename_map[col] = "delist_date"
                    elif "起息" in col or col == "interest_begin_date":
                        rename_map[col] = "interest_begin_date"
                    elif "到期" in col or col == "maturity_date":
                        rename_map[col] = "maturity_date"
                    elif "转股价" in col or col == "convert_price":
                        rename_map[col] = "convert_price"
                    elif "转股开始" in col or col == "convert_start_date":
                        rename_map[col] = "convert_start_date"
                    elif "转股结束" in col or col == "convert_end_date":
                        rename_map[col] = "convert_end_date"
                    elif "赎回" in col or col == "redeem_price":
                        rename_map[col] = "redeem_price"
                    elif "回售" in col or col == "put_price":
                        rename_map[col] = "put_price"
                    elif "票面利率" in col or col == "coupon_rate":
                        rename_map[col] = "coupon_rate"
                    elif "面值" in col or col == "par_value":
                        rename_map[col] = "par_value"
                    elif "发行量" in col or col == "issue_amount":
                        rename_map[col] = "issue_amount"
                    elif "剩余" in col or col == "remain_amount":
                        rename_map[col] = "remain_amount"
                    elif "评级" in col or col == "rating":
                        rename_map[col] = "rating"
                    elif "担保" in col or col == "guarantee":
                        rename_map[col] = "guarantee"
                    elif "转股价值" in col or col == "convert_value":
                        rename_map[col] = "convert_value"
                    elif "溢价" in col or col == "premium_rate":
                        rename_map[col] = "premium_rate"

                df = df.rename(columns=rename_map)
                df["id"] = range(len(df))

                required_cols = [
                    "id",
                    "code",
                    "short_name",
                    "full_name",
                    "list_status_id",
                    "list_status",
                    "issuer",
                    "company_code",
                    "issue_start_date",
                    "issue_end_date",
                    "bond_type",
                    "bond_form_id",
                    "bond_form",
                    "list_date",
                    "delist_date",
                    "interest_begin_date",
                    "maturity_date",
                    "interest_date",
                    "last_cash_date",
                    "cash_comment",
                    "convert_price",
                    "convert_start_date",
                    "convert_end_date",
                    "redeem_price",
                    "put_price",
                    "coupon_rate",
                    "par_value",
                    "issue_amount",
                    "remain_amount",
                    "rating",
                    "guarantee",
                    "convert_value",
                    "premium_rate",
                ]
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = None
                return df[required_cols]
        except Exception as e:
            logger.warning(f"[BondQuery] CONBOND_BASIC_INFO 获取失败: {e}")

        logger.debug(
            "[BondQuery] CONBOND_BASIC_INFO: akshare 暂无此接口，返回空DataFrame"
        )
        return pd.DataFrame(
            columns=[
                "id",
                "code",
                "short_name",
                "full_name",
                "list_status_id",
                "list_status",
                "issuer",
                "company_code",
                "issue_start_date",
                "issue_end_date",
                "bond_type",
                "bond_form_id",
                "bond_form",
                "list_date",
                "delist_date",
                "interest_begin_date",
                "maturity_date",
                "interest_date",
                "last_cash_date",
                "cash_comment",
                "convert_price",
                "convert_start_date",
                "convert_end_date",
                "redeem_price",
                "put_price",
                "coupon_rate",
                "par_value",
                "issue_amount",
                "remain_amount",
                "rating",
                "guarantee",
                "convert_value",
                "premium_rate",
            ]
        )

    def _query_convert_price_adjust(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """
        查询可转债转股价格调整数据

        TODO: akshare 目前没有直接提供可转债转股价格调整的接口
        如需实现，可考虑以下数据源：
        - 聚宽自有数据
        - 东方财富可转债详情页
        - 交易所公告数据
        """
        logger.debug(
            "[BondQuery] CONBOND_CONVERT_PRICE_ADJUST: "
            "akshare 暂无此接口，返回空DataFrame"
        )
        return pd.DataFrame(
            columns=[
                "code",
                "name",
                "pub_date",
                "adjust_date",
                "new_convert_price",
                "adjust_reason",
            ]
        )

    def _query_daily_convert(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """
        查询可转债每日转股统计数据

        TODO: akshare 目前没有直接提供可转债每日转股统计的接口
        如需实现，可考虑以下数据源：
        - 聚宽自有数据
        - 东方财富可转债转股详情页
        - 交易所每日转股数据
        """
        logger.debug(
            "[BondQuery] CONBOND_DAILY_CONVERT: akshare 暂无此接口，返回空DataFrame"
        )
        return pd.DataFrame(
            columns=[
                "date",
                "code",
                "name",
                "exchange_code",
                "issue_number",
                "convert_price",
                "daily_convert_number",
                "acc_convert_number",
                "acc_convert_ratio",
                "convert_premium",
                "convert_premium_rate",
            ]
        )


bond = BondQuery()


def query_convert_price_adjust(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    直接查询可转债转股价格调整数据

    参数:
        code: 可转债代码（可选）
        start_date: 开始日期（可选）
        end_date: 结束日期（可选）

    返回:
        pd.DataFrame
    """
    return bond.run_query(CONBOND_CONVERT_PRICE_ADJUST())


def query_daily_convert(
    date: Optional[str] = None,
    code: Optional[str] = None,
) -> pd.DataFrame:
    """
    直接查询可转债每日转股统计数据

    参数:
        date: 日期（可选）
        code: 可转债代码（可选）

    返回:
        pd.DataFrame
    """
    return bond.run_query(CONBOND_DAILY_CONVERT())


def get_conversion_bond_list(
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get conversion bond list.

    JQData compatible interface

    Parameters
    ----
    force_update : bool
        Force update from network
    use_duckdb : bool
        Use DuckDB cache

    Returns
    ----
    pd.DataFrame
        Conversion bond list with columns:
        - bond_code: Bond code
        - bond_name: Bond name
        - stock_code: Stock code
        - close: Close price
        - conversion_price: Conversion price
        - conversion_ratio: Conversion ratio
        - premium_rate: Premium rate
        - date: Date

    Examples
    ----
    >>> df = get_conversion_bond_list()
    """
    df = _get_conversion_bond_list(force_update=force_update, use_duckdb=use_duckdb)
    if df is not None and not df.empty:
        return df
    return pd.DataFrame(columns=_CB_SCHEMA)


def get_conversion_bond_price(
    code: str,
    force_update: bool = False,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Get conversion bond quote data.

    JQData compatible interface

    Parameters
    ----
    code : str
        Bond code (supports multiple formats: 110XXX.XSHG, sh110XXX, 110XXX)
    force_update : bool
        Force update from network
    use_cache : bool
        Use cache

    Returns
    ----
    pd.DataFrame
        Bond quote data

    Examples
    ----
    >>> df = get_conversion_bond_price('113009')
    """
    result = _get_conversion_bond_price(
        code=code, force_update=force_update, use_cache=use_cache
    )
    if result.success and result.data is not None:
        return result.data
    return pd.DataFrame(columns=_CB_SCHEMA)


def get_conversion_bond_info(
    code: str,
    force_update: bool = False,
    use_cache: bool = True,
) -> dict:
    """
    Get conversion bond basic info.

    JQData compatible interface

    Parameters
    ----
    code : str
        Bond code (supports multiple formats)
    force_update : bool
        Force update from network
    use_cache : bool
        Use cache

    Returns
    ----
    dict
        Bond basic info

    Examples
    ----
    >>> info = get_conversion_bond_info('113009')
    """
    result = _get_conversion_bond_info(
        code=code, force_update=force_update, use_cache=use_cache
    )
    if result.success and result.data is not None:
        return result.data
    return {}


def get_conversion_bond_detail(
    code: str,
    use_cache: bool = True,
) -> dict:
    """
    Get conversion bond detailed info.

    JQData compatible interface

    Parameters
    ----
    code : str
        Bond code
    use_cache : bool
        Use cache

    Returns
    ----
    dict
        Bond detailed info including:
        - bond_code, bond_name, stock_code, stock_name
        - close, conversion_price, conversion_ratio, premium_rate
        - bond_value, conversion_value, double_low, remain_years
        - list_date, maturity_date

    Examples
    ----
    >>> detail = get_conversion_bond_detail('113009')
    """
    result = _get_conversion_bond_detail(code=code, use_cache=use_cache)
    if result.success and result.data is not None:
        return result.data
    return {}


def get_conversion_bond_quote(
    bond_code: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get conversion bond quote data (legacy interface compatible).

    JQData compatible interface

    Parameters
    ----
    bond_code : str
        Bond code
    force_update : bool
        Force update from network

    Returns
    ----
    pd.DataFrame
        Bond quote data

    Examples
    ----
    >>> df = get_conversion_bond_quote('113009')
    """
    return get_conversion_bond_price(bond_code, force_update=force_update)


def get_conversion_info(
    bond_code: str,
    force_update: bool = False,
) -> dict:
    """
    Get conversion bond basic info.

    JQData compatible interface

    Parameters
    ----
    bond_code : str
        Bond code
    force_update : bool
        Force update from network

    Returns
    ----
    dict
        Conversion bond info

    Examples
    ----
    >>> info = get_conversion_info('113009')
    """
    df = _get_conversion_info(bond_code=bond_code, force_update=force_update)
    if df is not None and not df.empty:
        return df
    return {}


def calculate_conversion_value(
    conversion_price: float,
    stock_price: float,
) -> float:
    """
    Calculate conversion value.

    Formula: (100 / conversion_price) * stock_price

    JQData compatible interface

    Parameters
    ----
    conversion_price : float
        Conversion price
    stock_price : float
        Stock price

    Returns
    ----
    float
        Conversion value

    Examples
    ----
    >>> value = calculate_conversion_value(10.0, 12.0)
    """
    return _calculate_conversion_value(
        conversion_price=conversion_price, stock_price=stock_price
    )


def calculate_premium_rate(
    bond_price: float,
    conversion_value: float,
) -> float:
    """
    Calculate premium rate.

    Formula: (bond_price / conversion_value - 1) * 100

    JQData compatible interface

    Parameters
    ----
    bond_price : float
        Bond price
    conversion_value : float
        Conversion value

    Returns
    ----
    float
        Premium rate (percentage)

    Examples
    ----
    >>> rate = calculate_premium_rate(120.0, 100.0)
    """
    return _calculate_premium_rate(
        bond_price=bond_price, conversion_value=conversion_value
    )


def get_conversion_bond_history(
    bond_code: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get conversion bond historical daily data.

    JQData compatible interface

    Parameters
    ----
    bond_code : str
        Bond code
    start_date : str, optional
        Start date, format 'YYYY-MM-DD'
    end_date : str, optional
        End date, format 'YYYY-MM-DD'
    force_update : bool
        Force update from network

    Returns
    ----
    pd.DataFrame
        Historical daily data with columns:
        - datetime: Date
        - open: Open price
        - high: High price
        - low: Low price
        - close: Close price
        - volume: Volume

    Examples
    ----
    >>> df = get_conversion_bond_history('113009', start_date='2024-01-01', end_date='2024-12-31')
    """
    df = _get_conversion_bond_history(
        bond_code=bond_code,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
    )
    if df is not None and not df.empty:
        return df
    return pd.DataFrame(columns=["datetime", "open", "high", "low", "close", "volume"])


def get_conversion_price(
    bond_code: str,
    use_cache: bool = True,
) -> float:
    """
    Get conversion bond conversion price.

    JQData compatible interface

    Parameters
    ----
    bond_code : str
        Bond code
    use_cache : bool
        Use cache

    Returns
    ----
    float
        Conversion price, None if not found

    Examples
    ----
    >>> price = get_conversion_price('113009')
    """
    return _get_conversion_price(bond_code=bond_code, use_cache=use_cache)


def calculate_conversion_premium(
    bond_code: str,
    use_cache: bool = True,
) -> float:
    """
    Calculate conversion bond premium rate.

    JQData compatible interface

    Parameters
    ----
    bond_code : str
        Bond code
    use_cache : bool
        Use cache

    Returns
    ----
    float
        Premium rate (percentage), None if not found

    Examples
    ----
    >>> rate = calculate_conversion_premium('113009')
    """
    return _calculate_conversion_premium(bond_code=bond_code, use_cache=use_cache)


def get_conversion_bond_daily(
    bond_code: str,
    start_date: str,
    end_date: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get conversion bond daily bar data.

    JQData compatible interface

    Parameters
    ----
    bond_code : str
        Bond code
    start_date : str
        Start date, format 'YYYY-MM-DD'
    end_date : str
        End date, format 'YYYY-MM-DD'
    force_update : bool
        Force update from network

    Returns
    ----
    pd.DataFrame
        Daily bar data with columns:
        - datetime: Date
        - open: Open price
        - high: High price
        - low: Low price
        - close: Close price
        - volume: Volume

    Examples
    ----
    >>> df = get_conversion_bond_daily('113009', '2024-01-01', '2024-12-31')
    """
    df = _get_conversion_bond_daily(
        bond_code=bond_code,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
    )
    if df is not None and not df.empty:
        return df
    return pd.DataFrame(columns=["datetime", "open", "high", "low", "close", "volume"])


def get_conversion_value(
    code: str,
    stock_price: float = None,
    use_cache: bool = True,
) -> dict:
    """
    Get conversion value for a bond.

    JQData compatible interface

    Parameters
    ----
    code : str
        Bond code
    stock_price : float, optional
        Stock price (auto-fetch if not provided)
    use_cache : bool
        Use cache

    Returns
    ----
    dict
        Result containing:
        - bond_code, bond_name, stock_code
        - conversion_price, stock_price, bond_price
        - conversion_value, premium_rate, conversion_ratio

    Examples
    ----
    >>> result = get_conversion_value('113009')
    """
    result = _get_conversion_value(
        code=code, stock_price=stock_price, use_cache=use_cache
    )
    if result.success and result.data is not None:
        return result.data
    return {}


__all__ = [
    "CONBOND_CONVERT_PRICE_ADJUST",
    "CONBOND_DAILY_CONVERT",
    "BOND_BASIC_INFO",
    "BOND_COUPON",
    "BOND_INTEREST_PAYMENT",
    "REPO_DAILY_PRICE",
    "CONBOND_BASIC_INFO",
    "BondQuery",
    "bond",
    "query_convert_price_adjust",
    "query_daily_convert",
    "get_conversion_bond_list",
    "get_conversion_bond_price",
    "get_conversion_bond_info",
    "get_conversion_bond_detail",
    "get_conversion_bond_quote",
    "get_conversion_info",
    "calculate_conversion_value",
    "calculate_premium_rate",
    "get_conversion_bond_history",
    "get_conversion_price",
    "calculate_conversion_premium",
    "get_conversion_bond_daily",
    "get_conversion_value",
]
