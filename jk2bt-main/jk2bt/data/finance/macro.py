"""
finance_data/macro.py
宏观经济数据获取模块。

主要功能：
1. 宏观数据查询 - finance.MACRO_CHINA_*
2. FinanceQuery 类提供 finance.run_query 兼容接口
3. get_macro_indicator() - 统一接口，返回 RobustResult
4. get_macro_gdp/cpi/ppi/m2/interest_rate() - 各类宏观数据获取

数据字段：
- indicator: 指标名称
- value: 指标值
- date: 日期
- unit: 单位

缓存策略:
- Parquet 缓存：存储在 data/macro_parquet 中
- adapter 内置缓存
- 按发布周期缓存（30天）
"""

import os
import pandas as pd
from datetime import datetime
from typing import Optional, List, Union
import logging

logger = logging.getLogger(__name__)

_CACHE_AVAILABLE = False
try:
    from jk2bt.cache import get_cache_manager

    _CACHE_AVAILABLE = True
except ImportError:
    logger.warning("parquet_cache 模块不可用")

from jk2bt.utils.result import RobustResult
from jk2bt.utils.date_utils import parse_date as _parse_date, parse_num


_MACRO_SCHEMA = [
    "indicator",
    "date",
    "value",
    "unit",
    "YoY",
    "MoM",
]


class MacroCacheManager:
    """宏观数据 parquet_cache 管理器"""

    _instance = None

    def __new__(cls, base_dir: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_manager(base_dir)
        return cls._instance

    def _init_manager(self, base_dir: str = None):
        if not _CACHE_AVAILABLE:
            self._cache = None
            return

        if base_dir is None:
            base_dir = os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ),
                "data",
                "cache",
            )

        self.base_dir = base_dir
        self._cache = None

        try:
            self._cache = get_cache_manager(base_dir=base_dir)
        except Exception as e:
            logger.warning(f"parquet_cache 初始化失败: {e}")
            self._cache = None

    def insert_macro(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return

        df = df.copy()
        rename_map = {"yoy": "change_pct"}
        df = df.rename(columns=rename_map)

        for col in ["indicator", "date", "value", "change_pct"]:
            if col not in df.columns:
                df[col] = None

        cols = ["indicator", "date", "value", "change_pct"]
        df = df[cols]

        try:
            self._cache.put("macro_data", df)
            logger.info(f"插入/更新 {len(df)} 条宏观数据")
        except Exception as e:
            logger.warning(f"插入宏观数据失败: {e}")

    def get_macro(
        self, indicator: str, start_date: str = None, end_date: str = None
    ) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_MACRO_SCHEMA)

        try:
            result = self._cache.get("macro_data", where={"indicator": indicator})
            if result is not None and not result.empty:
                rename_map = {"change_pct": "yoy"}
                result = result.rename(columns=rename_map)
                for col in _MACRO_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                result = result[_MACRO_SCHEMA]
                if start_date and end_date and "date" in result.columns:
                    result = result[
                        (result["date"] >= start_date) & (result["date"] <= end_date)
                    ]
                return result.sort_values("date", ascending=False)
            return pd.DataFrame(columns=_MACRO_SCHEMA)
        except Exception as e:
            logger.warning(f"查询宏观数据失败: {e}")
            return pd.DataFrame(columns=_MACRO_SCHEMA)

    def is_cache_valid(self, indicator: str, cache_days: int = 30) -> bool:
        if self._cache is None:
            return False
        try:
            result = self._cache.get("macro_data", where={"indicator": indicator})
            return result is not None and not result.empty
        except Exception:
            return False


_db_manager = MacroCacheManager() if _CACHE_AVAILABLE else None


def get_macro_china_gdp(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取GDP数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    df = get_macro_gdp(force_update=force_update)
    if not df.empty:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_china_cpi(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取CPI数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    df = get_macro_cpi(force_update=force_update)
    if not df.empty:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_china_ppi(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取PPI数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    df = get_macro_ppi(force_update=force_update)
    if not df.empty:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_china_pmi(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取PMI数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame
    """
    indicator = "PMI"

    if _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_macro_raw("pmi")
        if df is not None and not df.empty:
            result = _normalize_macro_data(df, indicator, "%")
            if not result.empty:
                if _db_manager is not None:
                    _db_manager.insert_macro(result)
                return result
    except Exception as e:
        logger.warning(f"[macro_pmi] 获取PMI数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_china_interest_rate(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取利率数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame，包含LPR等利率数据
    """
    df = get_macro_interest_rate(force_update=force_update)
    if not df.empty:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_china_exchange_rate(
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取汇率数据。

    参数
    ----
    start_date   : 起始日期
    end_date     : 结束日期
    force_update : 强制更新

    返回
    ----
    DataFrame，包含人民币汇率数据
    """
    indicator = "EXCHANGE_RATE"

    if _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=7):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_macro_raw("exchange_rate")
        if df is not None and not df.empty:
            result = _normalize_macro_data(df, indicator, "")
            if not result.empty:
                if _db_manager is not None:
                    _db_manager.insert_macro(result)
                return result
    except Exception as e:
        logger.warning(f"[macro_exchange_rate] 获取汇率数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def query_macro_data(
    indicator: str = None,
    start_date: str = None,
    end_date: str = None,
) -> pd.DataFrame:
    """
    查询宏观经济数据（finance.MACRO_ECONOMIC_DATA 表兼容接口）。

    参数
    ----
    indicator  : 指标类型（可选，不指定则返回全部）
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame
    """
    if _db_manager is None:
        return pd.DataFrame(columns=_MACRO_SCHEMA)

    try:
        where = {}
        if indicator:
            where["indicator"] = indicator.upper()
        result = _db_manager.get_macro(indicator if indicator else "")
        if result is not None and not result.empty:
            if indicator:
                result = result[result["indicator"] == indicator.upper()]
            if start_date and "date" in result.columns:
                result = result[result["date"] >= start_date]
            if end_date and "date" in result.columns:
                result = result[result["date"] <= end_date]
            result = result.sort_values(["indicator", "date"])
            result = result.rename(columns={"yoy": "YoY", "mom": "MoM"})
            return result
        return pd.DataFrame(columns=_MACRO_SCHEMA)
    except Exception as e:
        logger.warning(f"查询宏观数据失败: {e}")
        return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_cpi(
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国CPI数据。

    参数
    ----
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，CPI数据
    """
    indicator = "CPI"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_macro_raw("cpi")
        if df is not None and not df.empty:
            result = _normalize_macro_data(df, indicator, "%")
            if not result.empty:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(result)
                return result
    except Exception as e:
        logger.warning(f"[macro_cpi] 获取CPI数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_ppi(
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国PPI数据。
    """
    indicator = "PPI"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_macro_raw("ppi")
        if df is not None and not df.empty:
            result = _normalize_macro_data(df, indicator, "%")
            if not result.empty:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(result)
                return result
    except Exception as e:
        logger.warning(f"[macro_ppi] 获取PPI数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_gdp(
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国GDP数据。
    """
    indicator = "GDP"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=90):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_macro_raw("gdp")
        if df is not None and not df.empty:
            result = _normalize_macro_data(df, indicator, "亿元")
            if not result.empty:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(result)
                return result
    except Exception as e:
        logger.warning(f"[macro_gdp] 获取GDP数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def _normalize_macro_data(df: pd.DataFrame, indicator: str, unit: str) -> pd.DataFrame:
    """标准化宏观数据"""
    if df is None or df.empty:
        return pd.DataFrame(columns=_MACRO_SCHEMA)

    result = pd.DataFrame()

    result["indicator"] = [indicator] * len(df)

    value_col = None
    for col in ["数值", "value", "当月", "当月值"]:
        if col in df.columns:
            value_col = col
            break
    if value_col:
        result["value"] = df[value_col].apply(_parse_num)
    else:
        result["value"] = None

    date_col = None
    for col in ["日期", "date", "月份", "统计时间"]:
        if col in df.columns:
            date_col = col
            break
    if date_col:
        result["date"] = df[date_col].apply(_parse_date)
    else:
        result["date"] = None

    result["unit"] = [unit] * len(df)

    yoy_col = None
    for col in ["同比增长", "YoY", "同比", "同比增速"]:
        if col in df.columns:
            yoy_col = col
            break
    if yoy_col:
        result["YoY"] = df[yoy_col].apply(_parse_num)
    else:
        result["YoY"] = None

    mom_col = None
    for col in ["环比增长", "MoM", "环比", "环比增速"]:
        if col in df.columns:
            mom_col = col
            break
    if mom_col:
        result["MoM"] = df[mom_col].apply(_parse_num)
    else:
        result["MoM"] = None

    result = result.dropna(subset=["date"])
    return result


def get_macro_m2(
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国M2货币供应量数据。

    参数
    ----
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，M2数据
    """
    indicator = "M2"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_macro_raw("m2")
        if df is not None and not df.empty:
            result = _normalize_macro_data(df, indicator, "亿元")
            if not result.empty:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(result)
                return result
    except Exception as e:
        logger.warning(f"[macro_m2] 获取M2数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def get_macro_interest_rate(
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取中国利率数据（央行基准利率）。

    参数
    ----
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    pandas DataFrame，利率数据
    """
    indicator = "INTEREST_RATE"

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(indicator, cache_days=30):
            df_cached = _db_manager.get_macro(indicator)
            if not df_cached.empty:
                return df_cached[_MACRO_SCHEMA]

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_macro_raw("interest_rate")
        if df is not None and not df.empty:
            result = _normalize_macro_data(df, indicator, "%")
            if not result.empty:
                if use_duckdb and _db_manager is not None:
                    _db_manager.insert_macro(result)
                return result
    except Exception as e:
        logger.warning(f"[macro_interest_rate] 获取利率数据失败: {e}")

    return pd.DataFrame(columns=_MACRO_SCHEMA)


def query_macro(
    indicators: List[str],
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    批量查询宏观数据。

    参数
    ----
    indicators  : 指标列表 ['CPI', 'PPI', 'GDP', 'M2', 'INTEREST_RATE']
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，宏观数据
    """
    if indicators is None or len(indicators) == 0:
        return pd.DataFrame(columns=_MACRO_SCHEMA)

    dfs = []

    for indicator in indicators:
        try:
            result = get_macro_indicator_robust(
                indicator,
                force_update=force_update,
                use_duckdb=use_duckdb,
            )
            if result.success and not result.data.empty:
                dfs.append(result.data)
        except Exception as e:
            logger.warning(f"[query_macro] 获取 {indicator} 失败: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_MACRO_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def get_macro_indicator_robust(
    indicator_name: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> RobustResult:
    """
    统一接口：获取宏观经济指标数据（返回 RobustResult）。

    参数
    ----
    indicator_name: 指标名称，支持: 'GDP', 'CPI', 'PPI', 'M2', 'INTEREST_RATE'
    force_update  : 强制更新
    use_duckdb    : 是否使用 DuckDB 缓存

    返回
    ----
    RobustResult，包含：
        - success: bool - 是否成功
        - data: DataFrame - 指标数据
        - reason: str - 失败原因或成功说明
        - source: str - 数据来源（'cache'/'network'/'error'）
    """
    indicator_map = {
        "GDP": (get_macro_gdp, "亿元"),
        "CPI": (get_macro_cpi, "%"),
        "PPI": (get_macro_ppi, "%"),
        "M2": (get_macro_m2, "亿元"),
        "INTEREST_RATE": (get_macro_interest_rate, "%"),
    }

    if indicator_name is None:
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_MACRO_SCHEMA),
            reason="指标名称不能为空",
            source="error",
        )

    indicator_upper = indicator_name.upper().strip()
    if indicator_upper not in indicator_map:
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_MACRO_SCHEMA),
            reason=f"不支持的指标: {indicator_name}。支持的指标: {', '.join(indicator_map.keys())}",
            source="error",
        )

    func, unit = indicator_map[indicator_upper]

    try:
        df = func(force_update=force_update, use_duckdb=use_duckdb)
        if df is not None and not df.empty:
            return RobustResult(
                success=True,
                data=df,
                reason=f"获取{indicator_upper}数据成功，共{len(df)}条记录",
                source="network",
            )
        else:
            return RobustResult(
                success=False,
                data=pd.DataFrame(columns=_MACRO_SCHEMA),
                reason=f"{indicator_upper}数据为空，请检查数据源或稍后重试",
                source="network",
            )
    except Exception as e:
        logger.error(f"获取{indicator_upper}数据异常: {e}")
        return RobustResult(
            success=False,
            data=pd.DataFrame(columns=_MACRO_SCHEMA),
            reason=f"获取{indicator_upper}数据失败: {str(e)}",
            source="error",
        )


class FinanceQuery:
    """聚宽 finance 模块模拟器"""

    class MACRO_ECONOMIC_DATA:
        indicator = None
        date = None
        value = None
        unit = None
        yoy = None
        mom = None

    class MACRO_CHINA_CPI:
        indicator = None
        value = None
        date = None
        unit = None

    class MACRO_CHINA_PPI:
        indicator = None
        value = None
        date = None
        unit = None

    class MACRO_CHINA_GDP:
        indicator = None
        value = None
        date = None
        unit = None

    class MACRO_CHINA_PMI:
        indicator = None
        value = None
        date = None
        unit = None

    class MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER:
        """农业产值季度数据表"""

        id = None
        date = None
        output_value = None
        yoy = None
        unit = None

    class MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR:
        """农业产值年度数据表"""

        id = None
        date = None
        output_value = None
        yoy = None
        unit = None

    class MAC_INDUSTRY_FINANCE_INSURANCE:
        """金融业数据表"""

        id = None
        date = None
        indicator = None
        value = None
        yoy = None
        unit = None

    class MAC_INDUSTRY_REAL_ESTATE:
        """房地产业数据表"""

        id = None
        date = None
        indicator = None
        value = None
        yoy = None
        unit = None

    class MAC_POPULATION_AGE:
        """人口年龄结构表"""

        id = None
        date = None
        age_group = None
        population = None
        ratio = None
        unit = None

    class MAC_POPULATION_EMPLOYMENT:
        """人口就业表"""

        id = None
        date = None
        indicator = None
        value = None
        unit = None

    class MAC_FISCAL_REVENUE:
        """财政收入表"""

        id = None
        date = None
        indicator = None
        value = None
        yoy = None
        unit = None

    class MAC_FISCAL_EXPENDITURE:
        """财政支出表"""

        id = None
        date = None
        indicator = None
        value = None
        yoy = None
        unit = None

    class CCTV_NEWS:
        """新闻联播文本数据表"""

        id = None
        day = None
        title = None
        content = None

    MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER_SCHEMA = [
        "id",
        "date",
        "output_value",
        "yoy",
        "unit",
    ]

    MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR_SCHEMA = [
        "id",
        "date",
        "output_value",
        "yoy",
        "unit",
    ]

    MAC_INDUSTRY_FINANCE_INSURANCE_SCHEMA = [
        "id",
        "date",
        "indicator",
        "value",
        "yoy",
        "unit",
    ]

    MAC_INDUSTRY_REAL_ESTATE_SCHEMA = [
        "id",
        "date",
        "indicator",
        "value",
        "yoy",
        "unit",
    ]

    MAC_POPULATION_AGE_SCHEMA = [
        "id",
        "date",
        "age_group",
        "population",
        "ratio",
        "unit",
    ]

    MAC_POPULATION_EMPLOYMENT_SCHEMA = [
        "id",
        "date",
        "indicator",
        "value",
        "unit",
    ]

    MAC_FISCAL_REVENUE_SCHEMA = [
        "id",
        "date",
        "indicator",
        "value",
        "yoy",
        "unit",
    ]

    MAC_FISCAL_EXPENDITURE_SCHEMA = [
        "id",
        "date",
        "indicator",
        "value",
        "yoy",
        "unit",
    ]

    CCTV_NEWS_SCHEMA = [
        "id",
        "day",
        "title",
        "content",
    ]

    def run_query(
        self,
        query_obj,
        force_update=False,
        use_duckdb=True,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        table_name = None

        if hasattr(query_obj, "__name__"):
            table_name = query_obj.__name__
        elif hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__name__"):
                table_name = query_obj.left.__name__
            elif hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__

        if table_name == "MACRO_ECONOMIC_DATA":
            return query_macro_data(start_date=start_date, end_date=end_date)
        elif table_name == "MACRO_CHINA_CPI":
            return get_macro_china_cpi(start_date, end_date, force_update)
        elif table_name == "MACRO_CHINA_PPI":
            return get_macro_china_ppi(start_date, end_date, force_update)
        elif table_name == "MACRO_CHINA_GDP":
            return get_macro_china_gdp(start_date, end_date, force_update)
        elif table_name == "MACRO_CHINA_PMI":
            return get_macro_china_pmi(start_date, end_date, force_update)
        elif table_name == "MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER":
            return pd.DataFrame(
                columns=self.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER_SCHEMA
            )
        elif table_name == "MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR":
            return pd.DataFrame(
                columns=self.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_YEAR_SCHEMA
            )
        elif table_name == "MAC_INDUSTRY_FINANCE_INSURANCE":
            return pd.DataFrame(columns=self.MAC_INDUSTRY_FINANCE_INSURANCE_SCHEMA)
        elif table_name == "MAC_INDUSTRY_REAL_ESTATE":
            return pd.DataFrame(columns=self.MAC_INDUSTRY_REAL_ESTATE_SCHEMA)
        elif table_name == "MAC_POPULATION_AGE":
            return pd.DataFrame(columns=self.MAC_POPULATION_AGE_SCHEMA)
        elif table_name == "MAC_POPULATION_EMPLOYMENT":
            return pd.DataFrame(columns=self.MAC_POPULATION_EMPLOYMENT_SCHEMA)
        elif table_name == "MAC_FISCAL_REVENUE":
            return pd.DataFrame(columns=self.MAC_FISCAL_REVENUE_SCHEMA)
        elif table_name == "MAC_FISCAL_EXPENDITURE":
            return pd.DataFrame(columns=self.MAC_FISCAL_EXPENDITURE_SCHEMA)
        elif table_name == "CCTV_NEWS":
            return pd.DataFrame(columns=self.CCTV_NEWS_SCHEMA)
        else:
            raise ValueError(f"不支持的表: {table_name}")

    def run_offset_query(
        self,
        query_obj,
        offset: int = 0,
        limit: int = 5000,
        force_update: bool = False,
        use_duckdb: bool = True,
        start_date: str = None,
        end_date: str = None,
    ) -> pd.DataFrame:
        """分页查询，突破5000行限制。

        参数
        ----
        query_obj : Query 对象
            查询对象
        offset : int
            起始偏移量，默认 0
        limit : int
            每页条数，默认 5000
        force_update : bool
            是否强制更新
        use_duckdb : bool
            是否使用 DuckDB 缓存
        start_date : str, optional
            起始日期
        end_date : str, optional
            结束日期

        返回
        ----
        DataFrame
            拼接后的完整结果集，最大 200,000 行
        """
        max_total = 200000
        all_dfs = []
        total_rows = 0

        # Fetch data ONCE
        full_df = self.run_query(
            query_obj,
            force_update=force_update,
            use_duckdb=use_duckdb,
            start_date=start_date,
            end_date=end_date,
        )
        if full_df is None or full_df.empty:
            return pd.DataFrame()

        # Paginate through the already-fetched data
        current_offset = offset
        while total_rows < max_total and current_offset < len(full_df):
            page_limit = min(limit, max_total - total_rows)
            page_slice = full_df.iloc[current_offset : current_offset + page_limit]
            if page_slice.empty:
                break

            all_dfs.append(page_slice)
            total_rows += len(page_slice)
            current_offset += page_limit

        if not all_dfs:
            return pd.DataFrame()

        return pd.concat(all_dfs, ignore_index=True)


finance = FinanceQuery()


def get_macro_data(
    indicator_type: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取宏观经济指标数据（统一接口）。

    参数
    ----
    indicator_type : 指标类型，支持 cpi, ppi, gdp, m2, interest_rate
    start_date     : 起始日期
    end_date       : 结束日期
    force_update   : 强制更新

    返回
    ----
    DataFrame
    """
    result = get_macro_indicator_robust(indicator_type, force_update)
    df = result.data
    if not df.empty and "date" in df.columns:
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
    return df


def get_macro_series(
    indicator_type: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """获取宏观时间序列数据"""
    df = get_macro_data(indicator_type, force_update=force_update)
    if df.empty or "date" not in df.columns:
        return df

    if start_date:
        df["_date"] = pd.to_datetime(df["date"])
        df = df[df["_date"] >= pd.to_datetime(start_date)]
        df = df.drop(columns=["_date"])

    if end_date:
        df["_date"] = pd.to_datetime(df["date"])
        df = df[df["_date"] <= pd.to_datetime(end_date)]
        df = df.drop(columns=["_date"])

    return df.sort_values("date", ascending=True).reset_index(drop=True)


def get_macro_indicators() -> pd.DataFrame:
    """
    获取可用的宏观指标列表。

    返回
    ----
    DataFrame: 包含指标代码、名称、频率、描述
    """
    data = [
        {"code": "GDP", "name": "GDP", "frequency": "季度", "desc": "国内生产总值"},
        {"code": "CPI", "name": "CPI", "frequency": "月度", "desc": "消费者物价指数"},
        {"code": "PPI", "name": "PPI", "frequency": "月度", "desc": "生产者物价指数"},
        {"code": "PMI", "name": "PMI", "frequency": "月度", "desc": "采购经理指数"},
        {"code": "M2", "name": "M2", "frequency": "月度", "desc": "广义货币供应量"},
        {
            "code": "INTEREST_RATE",
            "name": "利率",
            "frequency": "不定期",
            "desc": "央行基准利率",
        },
        {
            "code": "EXCHANGE_RATE",
            "name": "汇率",
            "frequency": "日度",
            "desc": "人民币汇率",
        },
    ]
    return pd.DataFrame(data)


def get_gdp_data(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取GDP数据。

    参数
    ----
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame，包含日期、数值
    """
    return get_macro_china_gdp(start_date=start_date, end_date=end_date)


def get_cpi_data(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取CPI数据。

    参数
    ----
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame，包含日期、数值
    """
    return get_macro_china_cpi(start_date=start_date, end_date=end_date)


def get_pmi_data(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取PMI数据。

    参数
    ----
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame，包含日期、数值
    """
    return get_macro_china_pmi(start_date=start_date, end_date=end_date)


def get_interest_rate(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取利率数据（包含SHIBOR、LPR等）。

    参数
    ----
    start_date : 起始日期
    end_date   : 结束日期

    返回
    ----
    DataFrame，包含利率数据
    """
    return get_macro_china_interest_rate(start_date=start_date, end_date=end_date)


def get_macro_indicator(
    indicator_name: str,
    force_update: bool = False,
) -> RobustResult:
    """
    统一接口：获取宏观经济指标数据（返回 RobustResult）。

    参数
    ----
    indicator_name: 指标名称，支持: 'GDP', 'CPI', 'PPI', 'M2', 'INTEREST_RATE'
    force_update  : 强制更新

    返回
    ----
    RobustResult，包含：
        - success: bool - 是否成功
        - data: DataFrame - 指标数据
        - reason: str - 失败原因或成功说明
        - source: str - 数据来源
    """
    return get_macro_indicator_robust(indicator_name, force_update, use_duckdb=True)


def run_query_simple(
    table: str,
    force_update: bool = False,
    start_date: str = None,
    end_date: str = None,
) -> pd.DataFrame:
    """简化的查询接口"""
    if table == "MACRO_ECONOMIC_DATA":
        return query_macro_data(start_date=start_date, end_date=end_date)
    elif table == "MACRO_CHINA_CPI":
        return get_macro_china_cpi(start_date, end_date, force_update)
    elif table == "MACRO_CHINA_PPI":
        return get_macro_china_ppi(start_date, end_date, force_update)
    elif table == "MACRO_CHINA_GDP":
        return get_macro_china_gdp(start_date, end_date, force_update)
    elif table == "MACRO_CHINA_PMI":
        return get_macro_china_pmi(start_date, end_date, force_update)
    elif table == "MACRO_CHINA_M2":
        return get_macro_m2(force_update=force_update)
    elif table == "MACRO_CHINA_INTEREST_RATE":
        return get_macro_interest_rate(force_update=force_update)
    else:
        raise ValueError(f"不支持的表: {table}")


def run_offset_query(
    query_obj,
    offset: int = 0,
    limit: int = 5000,
    force_update: bool = False,
    use_duckdb: bool = True,
    start_date: str = None,
    end_date: str = None,
) -> pd.DataFrame:
    """分页查询函数，突破5000行限制。

    参数
    ----
    query_obj : Query 对象
        查询对象
    offset : int
        起始偏移量，默认 0
    limit : int
        每页条数，默认 5000
    force_update : bool
        是否强制更新
    use_duckdb : bool
        是否使用 DuckDB 缓存
    start_date : str, optional
        起始日期
    end_date : str, optional
        结束日期

    返回
    ----
    DataFrame
        拼接后的完整结果集，最大 200,000 行
    """
    return finance.run_offset_query(
        query_obj,
        offset=offset,
        limit=limit,
        force_update=force_update,
        use_duckdb=use_duckdb,
        start_date=start_date,
        end_date=end_date,
    )


# 向后兼容别名
MacroDBManager = MacroCacheManager
