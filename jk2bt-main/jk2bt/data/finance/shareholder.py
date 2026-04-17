"""
finance_data/shareholder.py
上市公司股东信息数据获取模块。

主要功能：
1. 十大股东查询 - get_top_shareholders(security, count=10)
2. 十大流通股东查询 - get_top_float_shareholders(security, count=10)
3. 股东结构查询 - get_shareholder_structure(security)
4. 股东集中度分析 - get_shareholder_concentration(security)
5. finance.run_query 兼容接口（支持 TOP10_SHAREHOLDERS, TOP10_FLOAT_SHAREHOLDERS 表）
6. get_shareholders(code) - 稳健版股东信息获取（返回 RobustResult）

缓存策略：
- Parquet 缓存：按周缓存，存储在 data/shareholder_parquet 中
- adapter 内置缓存
- 网络失败时使用 Parquet 缓存兜底
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Union, Dict
import logging

from jk2bt.utils.symbol import extract_code_num, ak_code_to_jq

try:
    from jk2bt.utils.standardize import standardize_financial
except ImportError:
    try:
        from jk2bt.utils.standardize import standardize_financial
    except ImportError:

        def standardize_financial(df: pd.DataFrame) -> pd.DataFrame:
            df = df.copy()
            df = df.dropna(how="all").reset_index(drop=True)
            return df


from jk2bt.utils.result import RobustResult
from jk2bt.utils.date_utils import parse_date


_CACHE_AVAILABLE = False
try:
    from jk2bt.cache import get_cache_manager

    _CACHE_AVAILABLE = True
except ImportError:
    pass

logger = logging.getLogger(__name__)

SHAREHOLDER_CACHE_DAYS = 7

_SHAREHOLDER_SCHEMA = [
    "code",
    "report_date",
    "ann_date",
    "shareholder_name",
    "shareholder_code",
    "shareholder_type",
    "hold_amount",
    "hold_ratio",
    "change_type",
    "change_amount",
    "rank",
]

_SHAREHOLDER_NUM_SCHEMA = [
    "code",
    "report_date",
    "ann_date",
    "holder_num",
    "a_holder_num",
    "b_holder_num",
    "h_holder_num",
    "holder_num_change",
    "holder_num_change_ratio",
]

_SHAREHOLDER_STRUCTURE_SCHEMA = [
    "code",
    "shareholder_type",
    "hold_ratio",
    "report_date",
]

SHAREHOLDER_TYPE_MAP = {
    "国有股": "国有",
    "国家股": "国有",
    "国有法人股": "国有",
    "国有": "国有",
    "基金": "基金",
    "QFII": "QFII",
    "社保": "社保基金",
    "社保基金": "社保基金",
    "券商": "券商",
    "保险": "保险",
    "信托": "信托",
    "个人": "个人",
    "自然人": "个人",
    "高管": "高管",
    "流通A股": "流通股",
    "流通股": "流通股",
    "境外可流通股": "境外流通",
    "境外流通": "境外流通",
    "机构": "机构",
    "企业": "企业",
    "法人": "法人",
    "未知": "未知",
}

CHANGE_TYPE_MAP = {
    "新进": "新进",
    "新增": "新进",
    "增持": "增持",
    "增加": "增持",
    "减持": "减持",
    "减少": "减持",
    "不变": "不变",
    "持平": "不变",
    "不变": "不变",
}


def _normalize_shareholder_type(type_str: str) -> str:
    """标准化股东类型"""
    if not type_str or pd.isna(type_str):
        return "未知"
    type_str = str(type_str).strip()
    for key, value in SHAREHOLDER_TYPE_MAP.items():
        if key in type_str:
            return value
    return type_str if type_str else "未知"


def _normalize_change_type(change_str: str) -> str:
    """标准化变动类型"""
    if not change_str or pd.isna(change_str):
        return "不变"
    change_str = str(change_str).strip()
    for key, value in CHANGE_TYPE_MAP.items():
        if key in change_str:
            return value
    return change_str if change_str else "不变"


class ShareholderCacheManager:
    """股东信息 parquet_cache 管理器（按周缓存）"""

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

    def insert_top10_shareholders(self, df: pd.DataFrame):
        if self._cache is None or df.empty:
            return

        df = df.copy()
        rename_map = {
            "code": "symbol",
            "shareholder_name": "holder_name",
            "hold_amount": "hold_count",
            "shareholder_type": "holder_type",
        }
        df = df.rename(columns=rename_map)

        for col in [
            "symbol",
            "report_date",
            "holder_name",
            "hold_count",
            "hold_ratio",
            "holder_type",
        ]:
            if col not in df.columns:
                df[col] = None

        cols = [
            "symbol",
            "report_date",
            "holder_name",
            "hold_count",
            "hold_ratio",
            "holder_type",
        ]
        df = df[cols]

        try:
            if "report_date" in df.columns:
                for value, group in df.groupby("report_date"):
                    self._cache.put("holder", group, partition_value=str(value))
            else:
                self._cache.put("holder", df)
            logger.info(f"插入/更新 {len(df)} 条十大股东信息")
        except Exception as e:
            logger.warning(f"插入十大股东信息失败: {e}")

    def insert_top10_float_shareholders(self, df: pd.DataFrame):
        self.insert_top10_shareholders(df)

    def insert_shareholder_structure(self, df: pd.DataFrame):
        self.insert_top10_shareholders(df)

    def get_top10_shareholders(self, code: str) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)

        try:
            result = self._cache.get("holder", where={"symbol": code})
            if result is not None and not result.empty:
                rename_map = {
                    "symbol": "code",
                    "holder_name": "shareholder_name",
                    "hold_count": "hold_amount",
                    "holder_type": "shareholder_type",
                }
                result = result.rename(columns=rename_map)
                for col in _SHAREHOLDER_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                return result.sort_values("rank")
            return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
        except Exception as e:
            logger.warning(f"查询十大股东信息失败: {e}")
            return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)

    def get_top10_float_shareholders(self, code: str) -> pd.DataFrame:
        return self.get_top10_shareholders(code)

    def get_shareholder_structure(self, code: str) -> pd.DataFrame:
        if self._cache is None:
            return pd.DataFrame(columns=_SHAREHOLDER_STRUCTURE_SCHEMA)

        try:
            result = self._cache.get("holder", where={"symbol": code})
            if result is not None and not result.empty:
                rename_map = {
                    "symbol": "code",
                    "holder_type": "shareholder_type",
                }
                result = result.rename(columns=rename_map)
                for col in _SHAREHOLDER_STRUCTURE_SCHEMA:
                    if col not in result.columns:
                        result[col] = None
                return result.sort_values("report_date", ascending=False)
            return pd.DataFrame(columns=_SHAREHOLDER_STRUCTURE_SCHEMA)
        except Exception as e:
            logger.warning(f"查询股东结构信息失败: {e}")
            return pd.DataFrame(columns=_SHAREHOLDER_STRUCTURE_SCHEMA)

    def is_cache_valid(
        self, code: str, table: str = "top10_shareholders", cache_days: int = 7
    ) -> bool:
        if self._cache is None:
            return False
        try:
            result = self._cache.get("holder", where={"symbol": code})
            return result is not None and not result.empty
        except Exception:
            return False

    def prewarm_cache(self, codes: List[str]) -> Dict[str, bool]:
        """缓存预热：批量获取股东信息并缓存"""
        results = {}
        for code in codes:
            try:
                df = get_top_shareholders(code, use_duckdb=True, force_update=True)
                results[code] = not df.empty
            except Exception as e:
                logger.warning(f"预热缓存失败 {code}: {e}")
                results[code] = False
        logger.info(f"缓存预热完成: {sum(results.values())}/{len(codes)} 成功")
        return results


_db_manager = ShareholderCacheManager() if _CACHE_AVAILABLE else None


def get_top_shareholders(
    security: str,
    count: int = 10,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取前十大股东。

    参数
    ----
    security    : 股票代码，支持多种格式（600519.XSHG, sh600519, 600519 等）
    count       : 返回数量，默认10
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含：
    - code: 股票代码（聚宽格式）
    - shareholder_name: 股东名称
    - shareholder_type: 股东类型
    - hold_amount: 持股数量
    - hold_ratio: 持股比例
    - change_type: 变动类型
    - report_date: 报告期
    - ann_date: 公告日期
    - rank: 排名
    """
    code_num = extract_code_num(security)
    jq_code = ak_code_to_jq(security)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(
            jq_code, "top10_shareholders", SHAREHOLDER_CACHE_DAYS
        ):
            df_cached = _db_manager.get_top10_shareholders(jq_code)
            if not df_cached.empty:
                return df_cached.head(count)

    from jk2bt.data.sources import get_adapter

    try:
        df_raw = None
        try:
            df_raw = get_adapter().get_top10_holders_em(symbol=code_num)
        except Exception as e1:
            logger.warning(f"stock_gdfx_holding_detail_em 失败: {e1}")
            try:
                df_raw = get_adapter().get_top10_holders(symbol=code_num)
            except Exception as e2:
                logger.warning(f"stock_zh_a_gdhs 失败: {e2}")

        if df_raw is not None and not df_raw.empty:
            df = _normalize_top10_holders(df_raw, jq_code)
            df = standardize_financial(df)
            if use_duckdb and _db_manager is not None:
                _db_manager.insert_top10_shareholders(df)
            return df.head(count)
    except Exception as e:
        logger.warning(f"十大股东获取失败 {security}: {e}")
        raise ValueError(f"无法获取股东信息，数据缺失: {security}")

    return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)


def get_top_float_shareholders(
    security: str,
    count: int = 10,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取前十大流通股东。

    参数
    ----
    security    : 股票代码
    count       : 返回数量，默认10
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含股东名称、持股数、持股比例等
    """
    code_num = extract_code_num(security)
    jq_code = ak_code_to_jq(security)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(
            jq_code, "top10_float_shareholders", SHAREHOLDER_CACHE_DAYS
        ):
            df_cached = _db_manager.get_top10_float_shareholders(jq_code)
            if not df_cached.empty:
                return df_cached.head(count)

    from jk2bt.data.sources import get_adapter

    try:
        df_raw = None
        try:
            df_raw = get_adapter().get_top10_float_holders_em(symbol=code_num)
        except Exception as e1:
            logger.warning(f"stock_gdfx_free_holding_detail_em 失败: {e1}")
            # Fallback: try the general top10 holders interface
            try:
                df_raw = get_adapter().get_top10_holders_em(symbol=code_num)
            except Exception as e2:
                logger.warning(f"get_top10_holders_em fallback 失败: {e2}")
                try:
                    df_raw = get_adapter().get_top10_holders(symbol=code_num)
                except Exception as e3:
                    logger.warning(f"get_top10_holders fallback 失败: {e3}")

        if df_raw is not None and not df_raw.empty:
            df = _normalize_top10_float_holders(df_raw, jq_code)
            df = standardize_financial(df)
            if use_duckdb and _db_manager is not None:
                _db_manager.insert_top10_float_shareholders(df)
            return df.head(count)
    except Exception as e:
        logger.warning(f"十大流通股东获取失败 {security}: {e}")

    return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)


def get_shareholder_structure(
    security: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    获取股东结构（按股东类型统计持股比例）。

    参数
    ----
    security    : 股票代码
    force_update: 强制更新
    use_duckdb  : 是否使用 DuckDB 缓存

    返回
    ----
    DataFrame，包含：
    - code: 股票代码
    - shareholder_type: 股东类型（国有、机构、个人等）
    - hold_ratio: 持股比例
    - report_date: 报告期
    """
    code_num = extract_code_num(security)
    jq_code = ak_code_to_jq(security)

    if use_duckdb and _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(
            jq_code, "shareholder_structure", SHAREHOLDER_CACHE_DAYS
        ):
            df_cached = _db_manager.get_shareholder_structure(jq_code)
            if not df_cached.empty:
                return df_cached

    try:
        df_top = get_top_shareholders(
            security, count=20, use_duckdb=use_duckdb, force_update=force_update
        )

        if df_top.empty:
            return pd.DataFrame(columns=_SHAREHOLDER_STRUCTURE_SCHEMA)

        structure_data = []
        type_ratio_map = {}

        for _, row in df_top.iterrows():
            stype = row.get("shareholder_type", "未知")
            ratio = row.get("hold_ratio", 0)
            if pd.notna(ratio):
                if stype not in type_ratio_map:
                    type_ratio_map[stype] = 0
                type_ratio_map[stype] += float(ratio)

        for stype, total_ratio in type_ratio_map.items():
            structure_data.append(
                {
                    "code": jq_code,
                    "shareholder_type": stype,
                    "hold_ratio": total_ratio,
                    "report_date": df_top.iloc[0].get("report_date")
                    if len(df_top) > 0
                    else None,
                }
            )

        df_structure = pd.DataFrame(structure_data)
        df_structure = standardize_financial(df_structure)

        if use_duckdb and _db_manager is not None and not df_structure.empty:
            _db_manager.insert_shareholder_structure(df_structure)

        return df_structure

    except Exception as e:
        logger.warning(f"股东结构获取失败 {security}: {e}")
        return pd.DataFrame(columns=_SHAREHOLDER_STRUCTURE_SCHEMA)


def get_shareholder_concentration(
    security: str,
    force_update: bool = False,
) -> Dict:
    """
    股东集中度分析。

    参数
    ----
    security    : 股票代码
    force_update: 强制更新

    返回
    ----
    dict，包含：
    - top1_ratio: 第一大股东持股比例
    - top3_ratio: 前三大股东持股比例合计
    - top5_ratio: 前五大股东持股比例合计
    - top10_ratio: 前十大股东持股比例合计
    - concentration_level: 集中度等级（高/中/低）
    - holder_count: 股东户数（如有）
    """
    try:
        df_top = get_top_shareholders(security, count=10, force_update=force_update)
        df_float = get_top_float_shareholders(
            security, count=10, force_update=force_update
        )

        result = {
            "top1_ratio": 0.0,
            "top3_ratio": 0.0,
            "top5_ratio": 0.0,
            "top10_ratio": 0.0,
            "top1_float_ratio": 0.0,
            "top3_float_ratio": 0.0,
            "top5_float_ratio": 0.0,
            "top10_float_ratio": 0.0,
            "concentration_level": "未知",
            "holder_count": None,
        }

        if not df_top.empty and "hold_ratio" in df_top.columns:
            ratios = df_top["hold_ratio"].dropna().tolist()
            if ratios:
                result["top1_ratio"] = float(ratios[0]) if len(ratios) >= 1 else 0.0
                result["top3_ratio"] = (
                    sum(ratios[:3]) if len(ratios) >= 3 else sum(ratios)
                )
                result["top5_ratio"] = (
                    sum(ratios[:5]) if len(ratios) >= 5 else sum(ratios)
                )
                result["top10_ratio"] = (
                    sum(ratios[:10]) if len(ratios) >= 10 else sum(ratios)
                )

        if not df_float.empty and "hold_ratio" in df_float.columns:
            ratios = df_float["hold_ratio"].dropna().tolist()
            if ratios:
                result["top1_float_ratio"] = (
                    float(ratios[0]) if len(ratios) >= 1 else 0.0
                )
                result["top3_float_ratio"] = (
                    sum(ratios[:3]) if len(ratios) >= 3 else sum(ratios)
                )
                result["top5_float_ratio"] = (
                    sum(ratios[:5]) if len(ratios) >= 5 else sum(ratios)
                )
                result["top10_float_ratio"] = (
                    sum(ratios[:10]) if len(ratios) >= 10 else sum(ratios)
                )

        try:
            df_count = get_shareholder_count(security, force_update=force_update)
            if not df_count.empty and "holder_num" in df_count.columns:
                result["holder_count"] = int(df_count.iloc[0]["holder_num"])
        except Exception:
            pass

        if result["top10_ratio"] >= 60:
            result["concentration_level"] = "高"
        elif result["top10_ratio"] >= 40:
            result["concentration_level"] = "中"
        else:
            result["concentration_level"] = "低"

        return result

    except Exception as e:
        logger.warning(f"股东集中度分析失败 {security}: {e}")
        return {
            "top1_ratio": 0.0,
            "top3_ratio": 0.0,
            "top5_ratio": 0.0,
            "top10_ratio": 0.0,
            "concentration_level": "未知",
            "error": str(e),
        }


def prewarm_shareholder_cache(
    codes: List[str],
) -> Dict[str, bool]:
    """
    缓存预热：批量获取股东信息并缓存到 DuckDB。

    参数
    ----
    codes   : 股票代码列表

    返回
    ----
    dict，每只股票的缓存结果
    """
    results = {}
    total = len(codes)

    for i, code in enumerate(codes):
        try:
            get_top_shareholders(code, use_duckdb=True, force_update=True)
            get_top_float_shareholders(code, use_duckdb=True, force_update=True)
            results[code] = True
            logger.info(f"缓存预热 [{i + 1}/{total}] {code} 成功")
        except Exception as e:
            results[code] = False
            logger.warning(f"缓存预热 [{i + 1}/{total}] {code} 失败: {e}")

    success_count = sum(results.values())
    logger.info(f"缓存预热完成: {success_count}/{total} 成功")
    return results


def get_shareholders(
    symbol: str,
    date: Union[str, datetime] = None,
    force_update: bool = False,
) -> RobustResult:
    """
    稳健版股东信息获取，返回 RobustResult。

    获取十大股东、持股比例、股东类型等综合信息。
    使用 akshare 的 stock_zh_a_gdhs 或 stock_share_change_cninfo 接口。

    参数
    ----
    symbol      : 股票代码，支持多种格式（600519.XSHG, sh600519, 600519 等）
    date        : 查询日期，默认最近报告期
    force_update: 强制更新

    返回
    ----
    RobustResult，包含：
    - success: 是否成功获取数据
    - data: DataFrame，字段：
        - code: 股票代码（聚宽格式）
        - shareholder_name: 股东名称
        - shareholder_type: 股东类型
        - hold_amount: 持股数量
        - hold_ratio: 持股比例
        - change_type: 变动类型
        - report_date: 报告期
        - ann_date: 公告日期
        - rank: 排名
    - reason: 失败原因或成功说明
    - source: 数据来源（'cache'/'network'/'fallback'）

    缓存策略
    --------
    - DuckDB 缓存（优先）
    - 网络失败时使用 DuckDB 缓存兜底

    示例
    ----
    >>> result = get_shareholders('600519.XSHG')
    >>> if result.success:
    >>>     df = result.data
    >>>     print(f"获取到 {len(df)} 条股东记录")
    >>> else:
    >>>     print(f"获取失败: {result.reason}")
    """
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    if _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(
            jq_code, "top10_shareholders", SHAREHOLDER_CACHE_DAYS
        ):
            cached_df = _db_manager.get_top10_shareholders(jq_code)
            if not cached_df.empty:
                if date is None:
                    return RobustResult(
                        success=True,
                        data=cached_df,
                        reason="从 DuckDB 缓存获取股东信息",
                        source="cache",
                    )
                else:
                    df_filtered = _filter_by_date(cached_df, date)
                    if not df_filtered.empty:
                        return RobustResult(
                            success=True,
                            data=df_filtered,
                            reason="从 DuckDB 缓存获取股东信息",
                            source="cache",
                        )

    from jk2bt.data.sources import get_adapter

    df_raw = get_adapter().get_shareholders_with_fallback(symbol=code_num)
    source_used = "network"

    if df_raw is not None and not df_raw.empty:
        df = _normalize_shareholders_robust(df_raw, jq_code)
        if not df.empty:
            if _db_manager is not None:
                _db_manager.insert_top10_shareholders(df)
            if date is None:
                return RobustResult(
                    success=True,
                    data=df,
                    reason=f"成功获取 {len(df)} 条股东记录",
                    source=source_used,
                )
            else:
                df_filtered = _filter_by_date(df, date)
                if not df_filtered.empty:
                    return RobustResult(
                        success=True,
                        data=df_filtered,
                        reason=f"成功获取 {len(df_filtered)} 条股东记录",
                        source=source_used,
                    )
                else:
                    return RobustResult(
                        success=False,
                        data=pd.DataFrame(columns=_SHAREHOLDER_SCHEMA),
                        reason=f"指定日期 {date} 无股东记录",
                        source=source_used,
                    )

    return RobustResult(
        success=False,
        data=pd.DataFrame(columns=_SHAREHOLDER_SCHEMA),
        reason=f"无法获取股东信息 (股票: {symbol})",
        source="network",
    )


def _normalize_shareholders_robust(df_raw: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    """标准化股东数据（稳健版）"""
    if df_raw is None or df_raw.empty:
        return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)

    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df_raw)

    date_col = None
    for col in ["股东户数统计截止日", "截止日期", "报告期", "日期", "变动日期"]:
        if col in df_raw.columns:
            date_col = col
            break
    if date_col:
        result["report_date"] = df_raw[date_col].apply(parse_date)
    else:
        result["report_date"] = None

    ann_col = None
    for col in ["公告日期", "发布公告日期", "ann_date"]:
        if col in df_raw.columns:
            ann_col = col
            break
    if ann_col:
        result["ann_date"] = df_raw[ann_col].apply(parse_date)
    else:
        result["ann_date"] = result["report_date"]

    name_col = None
    for col in ["股东名称", "十大股东名称", "股东", "name", "变动的股东名称"]:
        if col in df_raw.columns:
            name_col = col
            break
    if name_col:
        result["shareholder_name"] = df_raw[name_col]
    else:
        result["shareholder_name"] = ""

    type_col = None
    for col in ["股东类型", "股东性质", "type", "股东性质分类"]:
        if col in df_raw.columns:
            type_col = col
            break
    if type_col:
        result["shareholder_type"] = df_raw[type_col]
    else:
        result["shareholder_type"] = "未知"

    amount_col = None
    for col in [
        "持股数量",
        "持有数量",
        "hold_amount",
        "变动的持股数量",
        "持股变动数量",
    ]:
        if col in df_raw.columns:
            amount_col = col
            break
    if amount_col:
        result["hold_amount"] = pd.to_numeric(df_raw[amount_col], errors="coerce")
    else:
        result["hold_amount"] = 0

    ratio_col = None
    for col in ["持股比例", "占比", "hold_ratio", "变动的持股比例", "持股变动比例"]:
        if col in df_raw.columns:
            ratio_col = col
            break
    if ratio_col:
        result["hold_ratio"] = pd.to_numeric(df_raw[ratio_col], errors="coerce")
    else:
        result["hold_ratio"] = 0

    change_col = None
    for col in ["增减", "变动情况", "change_type", "变动方向", "增减变动"]:
        if col in df_raw.columns:
            change_col = col
            break
    if change_col:
        result["change_type"] = df_raw[change_col]
    else:
        result["change_type"] = "不变"

    rank_col = None
    for col in ["排名", "序号", "股东排名", "rank"]:
        if col in df_raw.columns:
            rank_col = col
            break
    if rank_col:
        result["rank"] = pd.to_numeric(df_raw[rank_col], errors="coerce")
    else:
        result["rank"] = range(1, len(df_raw) + 1)

    return result


def _filter_by_date(df: pd.DataFrame, date: Union[str, datetime]) -> pd.DataFrame:
    """按日期筛选数据"""
    if df.empty:
        return df

    if isinstance(date, str):
        date = parse_date(date, as_datetime=True)

    if date is None:
        return df

    if "report_date" in df.columns:
        df = df.copy()
        df["_date"] = pd.to_datetime(df["report_date"])
        date_ts = pd.Timestamp(date)

        df_exact = df[df["_date"] == date_ts]
        if not df_exact.empty:
            return df_exact.drop(columns=["_date"])

        df_before = df[df["_date"] <= date_ts]
        if not df_before.empty:
            latest_date = df_before["_date"].max()
            return df_before[df_before["_date"] == latest_date].drop(columns=["_date"])

    return df


def get_top10_shareholders(
    symbol: str,
    date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """获取十大股东快照"""
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    if _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(
            jq_code, "top10_shareholders", SHAREHOLDER_CACHE_DAYS
        ):
            df_cached = _db_manager.get_top10_shareholders(jq_code)
            if not df_cached.empty:
                return df_cached

    from jk2bt.data.sources import get_adapter

    df = get_adapter().get_top10_shareholders_with_fallback(symbol=code_num)
    if df is not None and not df.empty:
        result = _normalize_top10_holders(df, jq_code)
        if _db_manager is not None:
            _db_manager.insert_top10_shareholders(result)
        return result

    return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)


def get_top10_float_shareholders(
    symbol: str,
    date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """获取十大流通股东快照"""
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    if _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(
            jq_code, "top10_float_shareholders", SHAREHOLDER_CACHE_DAYS
        ):
            df_cached = _db_manager.get_top10_float_shareholders(jq_code)
            if not df_cached.empty:
                return df_cached

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_top10_float_holders_em(symbol=code_num)
        if df is not None and not df.empty:
            result = _normalize_top10_float_holders(df, jq_code)
            if _db_manager is not None:
                _db_manager.insert_top10_float_shareholders(result)
            return result
    except Exception as e:
        logger.warning(f"十大流通股东获取失败 {symbol}: {e}")

    return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)


def get_shareholder_count(symbol: str, force_update: bool = False) -> pd.DataFrame:
    """获取股东户数时间序列"""
    code_num = extract_code_num(symbol)
    jq_code = ak_code_to_jq(symbol)

    if _db_manager is not None and not force_update:
        if _db_manager.is_cache_valid(
            jq_code, "shareholder_num", SHAREHOLDER_CACHE_DAYS
        ):
            df_cached = _db_manager.get_shareholder_structure(jq_code)
            if not df_cached.empty:
                return df_cached

    from jk2bt.data.sources import get_adapter

    try:
        df = get_adapter().get_holder_count(symbol=code_num)
        if df is not None and not df.empty:
            result = _normalize_holder_count(df, jq_code)
            if _db_manager is not None:
                _db_manager.insert_shareholder_structure(result)
            return result
    except Exception as e:
        logger.warning(f"股东户数获取失败 {symbol}: {e}")

    return pd.DataFrame(columns=_SHAREHOLDER_NUM_SCHEMA)


def _normalize_top10_holders(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    col_map = {
        "股东名称": "shareholder_name",
        "股东性质": "shareholder_type",
        "持股数量": "hold_amount",
        "持股比例": "hold_ratio",
        "增减": "change_type",
        "报告期": "report_date",
        "公告日期": "ann_date",
    }

    for src, target in col_map.items():
        if src in df.columns:
            result[target] = df[src]

    if "报告期" in df.columns:
        result["report_date"] = df["报告期"]
    else:
        result["report_date"] = None

    if "公告日期" in df.columns:
        result["ann_date"] = df["公告日期"]
    else:
        result["ann_date"] = None

    result["shareholder_code"] = None

    if "持股变动" in df.columns:
        result["change_amount"] = pd.to_numeric(df["持股变动"], errors="coerce")
    elif "增持股数" in df.columns:
        result["change_amount"] = pd.to_numeric(df["增持股数"], errors="coerce")
    elif "减持股数" in df.columns:
        result["change_amount"] = pd.to_numeric(df["减持股数"], errors="coerce")
    else:
        result["change_amount"] = None

    if len(df) > 0:
        result["rank"] = range(1, len(df) + 1)

    return result


def _normalize_top10_float_holders(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    return _normalize_top10_holders(df, jq_code)


def _normalize_holder_count(df: pd.DataFrame, jq_code: str) -> pd.DataFrame:
    result = pd.DataFrame()
    result["code"] = [jq_code] * len(df)

    if "股东户数" in df.columns:
        result["holder_num"] = df["股东户数"]
    elif "户数" in df.columns:
        result["holder_num"] = df["户数"]
    else:
        result["holder_num"] = None

    if "A股股东户数" in df.columns:
        result["a_holder_num"] = df["A股股东户数"]
    elif "A股东户数" in df.columns:
        result["a_holder_num"] = df["A股东户数"]
    else:
        result["a_holder_num"] = None

    if "B股股东户数" in df.columns:
        result["b_holder_num"] = df["B股股东户数"]
    elif "B股东户数" in df.columns:
        result["b_holder_num"] = df["B股东户数"]
    else:
        result["b_holder_num"] = None

    if "H股股东户数" in df.columns:
        result["h_holder_num"] = df["H股股东户数"]
    elif "H股东户数" in df.columns:
        result["h_holder_num"] = df["H股东户数"]
    else:
        result["h_holder_num"] = None

    if "报告期" in df.columns:
        result["report_date"] = df["报告期"]
    elif "截止日期" in df.columns:
        result["report_date"] = df["截止日期"]
    else:
        result["report_date"] = None

    if "公告日期" in df.columns:
        result["ann_date"] = df["公告日期"]
    else:
        result["ann_date"] = result["report_date"]

    if "股东户数变化" in df.columns:
        result["holder_num_change"] = pd.to_numeric(df["股东户数变化"], errors="coerce")
    elif "变化" in df.columns:
        result["holder_num_change"] = pd.to_numeric(df["变化"], errors="coerce")
    else:
        if "holder_num" in result.columns and len(result) > 1:
            holder_nums = pd.to_numeric(result["holder_num"], errors="coerce")
            result["holder_num_change"] = holder_nums.diff()
        else:
            result["holder_num_change"] = None

    if "股东户数变化比例" in df.columns:
        result["holder_num_change_ratio"] = pd.to_numeric(
            df["股东户数变化比例"], errors="coerce"
        )
    else:
        if "holder_num_change" in result.columns and "holder_num" in result.columns:
            holder_nums = pd.to_numeric(result["holder_num"], errors="coerce")
            changes = pd.to_numeric(result["holder_num_change"], errors="coerce")
            result["holder_num_change_ratio"] = (
                changes / holder_nums.shift(1) * 100
            ).round(2)
        else:
            result["holder_num_change_ratio"] = None

    return result


def query_shareholder_top10(symbols: list, force_update: bool = False) -> pd.DataFrame:
    """批量查询十大股东（finance.STK_SHAREHOLDER_TOP10）"""
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_top10_shareholders(symbol, force_update=force_update)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"查询十大股东失败 {symbol}: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def query_shareholder_float_top10(
    symbols: list, force_update: bool = False
) -> pd.DataFrame:
    """批量查询十大流通股东（finance.STK_SHAREHOLDER_FLOAT_TOP10）"""
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_top10_float_shareholders(symbol, force_update=force_update)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"查询十大流通股东失败 {symbol}: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


def query_shareholder_num(symbols: list, force_update: bool = False) -> pd.DataFrame:
    """批量查询股东户数（finance.STK_SHAREHOLDER_NUM）"""
    if symbols is None or len(symbols) == 0:
        return pd.DataFrame(columns=_SHAREHOLDER_NUM_SCHEMA)

    dfs = []
    for symbol in symbols:
        try:
            df = get_shareholder_count(symbol, force_update=force_update)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            logger.warning(f"查询股东户数失败 {symbol}: {e}")
            continue

    if not dfs:
        return pd.DataFrame(columns=_SHAREHOLDER_NUM_SCHEMA)

    return pd.concat(dfs, ignore_index=True)


class FinanceQuery:
    """
    聚宽 finance 模块模拟器。
    提供 finance.run_query 兼容的查询接口。

    使用示例：
    >>> finance = FinanceQuery()
    >>> df = finance.run_query(finance.STK_SHAREHOLDER.code == '600000.XSHG')
    >>> df = finance.run_query(finance.STK_SHAREHOLDER_TOP10.code == '000001.XSHE')
    """

    class STK_SHAREHOLDER:
        """股东信息表（综合）"""

        code = None
        report_date = None
        ann_date = None
        shareholder_name = None
        shareholder_code = None
        shareholder_type = None
        hold_amount = None
        hold_ratio = None
        change_type = None
        change_amount = None
        rank = None

    class STK_SHAREHOLDER_TOP10:
        """十大股东表"""

        code = None
        report_date = None
        ann_date = None
        shareholder_name = None
        shareholder_code = None
        shareholder_type = None
        hold_amount = None
        hold_ratio = None
        change_type = None
        change_amount = None
        rank = None

    class STK_SHAREHOLDER_FLOAT_TOP10:
        """十大流通股东表"""

        code = None
        report_date = None
        ann_date = None
        shareholder_name = None
        shareholder_code = None
        shareholder_type = None
        hold_amount = None
        hold_ratio = None
        change_type = None
        change_amount = None
        rank = None

    # Alias for JQData compatibility
    STK_SHAREHOLDER_FLOATING_TOP10 = STK_SHAREHOLDER_FLOAT_TOP10

    class STK_SHAREHOLDER_NUM:
        """股东户数表"""

        code = None
        report_date = None
        ann_date = None
        holder_num = None
        a_holder_num = None
        b_holder_num = None
        h_holder_num = None
        holder_num_change = None
        holder_num_change_ratio = None

    # Alias for JQData compatibility
    STK_HOLDER_NUM = STK_SHAREHOLDER_NUM

    class TOP10_SHAREHOLDERS:
        """前十大股东表（新API）"""

        code = None
        report_date = None
        ann_date = None
        shareholder_name = None
        shareholder_code = None
        shareholder_type = None
        hold_amount = None
        hold_ratio = None
        change_type = None
        change_amount = None
        rank = None

    class TOP10_FLOAT_SHAREHOLDERS:
        """前十大流通股东表（新API）"""

        code = None
        report_date = None
        ann_date = None
        shareholder_name = None
        shareholder_code = None
        shareholder_type = None
        hold_amount = None
        hold_ratio = None
        change_type = None
        change_amount = None
        rank = None

    def run_query(
        self,
        query_obj,
        force_update: bool = False,
        robust: bool = False,
    ) -> Union[pd.DataFrame, RobustResult]:
        """
        执行查询（模拟聚宽 finance.run_query）。

        参数
        ----
        query_obj    : 查询对象（表对象或查询表达式）
        force_update : 强制更新
        robust       : 是否返回 RobustResult

        返回
        ----
        pd.DataFrame 或 RobustResult

        示例
        ----
        >>> finance = FinanceQuery()
        >>> df = finance.run_query(finance.STK_SHAREHOLDER.code == '600000.XSHG')
        >>> result = finance.run_query(finance.STK_SHAREHOLDER.code == '600000.XSHG', robust=True)
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
            field_name = None
            if hasattr(query_obj.left, "name"):
                field_name = query_obj.left.name
            elif hasattr(query_obj, "left"):
                for attr in [
                    "code",
                    "report_date",
                    "shareholder_name",
                    "holder_num",
                ]:
                    if (
                        hasattr(query_obj.left, attr)
                        and query_obj.left.__dict__.get(attr) is not None
                    ):
                        field_name = attr
                        break

            if field_name and hasattr(query_obj, "right"):
                conditions[field_name] = query_obj.right

        if table_name == "STK_SHAREHOLDER":
            if "code" in conditions:
                return get_shareholders(
                    conditions["code"],
                    force_update=force_update,
                )
            else:
                empty_df = pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
                return RobustResult(
                    success=False,
                    data=empty_df,
                    reason="未指定股票代码",
                    source="input",
                )

        elif table_name == "STK_SHAREHOLDER_TOP10":
            if "code" in conditions:
                df = get_top10_shareholders(
                    conditions["code"],
                    force_update=force_update,
                )
                if robust:
                    if df.empty:
                        return RobustResult(
                            success=False,
                            data=df,
                            reason=f"十大股东查询返回空数据 (股票: {conditions['code']})",
                            source="network",
                        )
                    return RobustResult(
                        success=True,
                        data=df,
                        reason=f"成功获取 {len(df)} 条十大股东记录",
                        source="network",
                    )
                return df
            else:
                empty_df = pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
                if robust:
                    return RobustResult(
                        success=False,
                        data=empty_df,
                        reason="未指定股票代码",
                        source="input",
                    )
                return empty_df

        elif table_name == "STK_SHAREHOLDER_FLOAT_TOP10":
            if "code" in conditions:
                df = get_top10_float_shareholders(
                    conditions["code"],
                    force_update=force_update,
                )
                if robust:
                    if df.empty:
                        return RobustResult(
                            success=False,
                            data=df,
                            reason=f"十大流通股东查询返回空数据 (股票: {conditions['code']})",
                            source="network",
                        )
                    return RobustResult(
                        success=True,
                        data=df,
                        reason=f"成功获取 {len(df)} 条十大流通股东记录",
                        source="network",
                    )
                return df
            else:
                empty_df = pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
                if robust:
                    return RobustResult(
                        success=False,
                        data=empty_df,
                        reason="未指定股票代码",
                        source="input",
                    )
                return empty_df

        elif table_name == "STK_SHAREHOLDER_NUM":
            if "code" in conditions:
                df = get_shareholder_count(
                    conditions["code"],
                    force_update=force_update,
                )
                if robust:
                    if df.empty:
                        return RobustResult(
                            success=False,
                            data=df,
                            reason=f"股东户数查询返回空数据 (股票: {conditions['code']})",
                            source="network",
                        )
                    return RobustResult(
                        success=True,
                        data=df,
                        reason=f"成功获取 {len(df)} 条股东户数记录",
                        source="network",
                    )
                return df
            else:
                empty_df = pd.DataFrame(columns=_SHAREHOLDER_NUM_SCHEMA)
                if robust:
                    return RobustResult(
                        success=False,
                        data=empty_df,
                        reason="未指定股票代码",
                        source="input",
                    )
                return empty_df

        elif table_name == "TOP10_SHAREHOLDERS":
            if "code" in conditions:
                df = get_top_shareholders(
                    conditions["code"],
                    force_update=force_update,
                )
                if robust:
                    if df.empty:
                        return RobustResult(
                            success=False,
                            data=df,
                            reason=f"十大股东查询返回空数据 (股票: {conditions['code']})",
                            source="network",
                        )
                    return RobustResult(
                        success=True,
                        data=df,
                        reason=f"成功获取 {len(df)} 条十大股东记录",
                        source="network",
                    )
                return df
            else:
                empty_df = pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
                if robust:
                    return RobustResult(
                        success=False,
                        data=empty_df,
                        reason="未指定股票代码",
                        source="input",
                    )
                return empty_df

        elif table_name == "TOP10_FLOAT_SHAREHOLDERS":
            if "code" in conditions:
                df = get_top_float_shareholders(
                    conditions["code"],
                    force_update=force_update,
                )
                if robust:
                    if df.empty:
                        return RobustResult(
                            success=False,
                            data=df,
                            reason=f"十大流通股东查询返回空数据 (股票: {conditions['code']})",
                            source="network",
                        )
                    return RobustResult(
                        success=True,
                        data=df,
                        reason=f"成功获取 {len(df)} 条十大流通股东记录",
                        source="network",
                    )
                return df
            else:
                empty_df = pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
                if robust:
                    return RobustResult(
                        success=False,
                        data=empty_df,
                        reason="未指定股票代码",
                        source="input",
                    )
                return empty_df

        else:
            raise ValueError(f"不支持的表: {table_name}")


finance = FinanceQuery()


def run_query_simple(
    table: str,
    code: str = None,
    force_update: bool = False,
    robust: bool = False,
) -> Union[pd.DataFrame, RobustResult]:
    """
    简化的查询接口（不依赖查询表达式）。

    参数
    ----
    table       : 表名 ('STK_SHAREHOLDER', 'STK_SHAREHOLDER_TOP10', 'STK_SHAREHOLDER_FLOAT_TOP10', 'STK_SHAREHOLDER_NUM')
    code        : 股票代码
    force_update: 强制更新
    robust      : 是否返回 RobustResult

    返回
    ----
    pd.DataFrame 或 RobustResult

    示例
    ----
    >>> df = run_query_simple('STK_SHAREHOLDER', code='600000.XSHG')
    >>> result = run_query_simple('STK_SHAREHOLDER', code='600000.XSHG', robust=True)
    """
    if table == "STK_SHAREHOLDER":
        if code:
            return get_shareholders(code, force_update=force_update)
        else:
            empty_df = pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
            return RobustResult(
                success=False,
                data=empty_df,
                reason="未指定股票代码",
                source="input",
            )

    elif table == "STK_SHAREHOLDER_TOP10":
        if code:
            df = get_top10_shareholders(code, force_update=force_update)
            if robust:
                if df.empty:
                    return RobustResult(
                        success=False,
                        data=df,
                        reason=f"十大股东查询返回空数据",
                        source="network",
                    )
                return RobustResult(
                    success=True,
                    data=df,
                    reason=f"成功获取 {len(df)} 条记录",
                    source="network",
                )
            return df
        else:
            empty_df = pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
            if robust:
                return RobustResult(
                    success=False,
                    data=empty_df,
                    reason="未指定股票代码",
                    source="input",
                )
            return empty_df

    elif table == "STK_SHAREHOLDER_FLOAT_TOP10":
        if code:
            df = get_top10_float_shareholders(code, force_update=force_update)
            if robust:
                if df.empty:
                    return RobustResult(
                        success=False,
                        data=df,
                        reason=f"十大流通股东查询返回空数据",
                        source="network",
                    )
                return RobustResult(
                    success=True,
                    data=df,
                    reason=f"成功获取 {len(df)} 条记录",
                    source="network",
                )
            return df
        else:
            empty_df = pd.DataFrame(columns=_SHAREHOLDER_SCHEMA)
            if robust:
                return RobustResult(
                    success=False,
                    data=empty_df,
                    reason="未指定股票代码",
                    source="input",
                )
            return empty_df

    elif table == "STK_SHAREHOLDER_NUM":
        if code:
            df = get_shareholder_count(code, force_update=force_update)
            if robust:
                if df.empty:
                    return RobustResult(
                        success=False,
                        data=df,
                        reason=f"股东户数查询返回空数据",
                        source="network",
                    )
                return RobustResult(
                    success=True,
                    data=df,
                    reason=f"成功获取 {len(df)} 条记录",
                    source="network",
                )
            return df
        else:
            empty_df = pd.DataFrame(columns=_SHAREHOLDER_NUM_SCHEMA)
            if robust:
                return RobustResult(
                    success=False,
                    data=empty_df,
                    reason="未指定股票代码",
                    source="input",
                )
            return empty_df

    else:
        raise ValueError(f"不支持的表: {table}")


from jk2bt.utils.symbol import extract_code_num as _extract_code_num
from jk2bt.utils.symbol import ak_code_to_jq as _normalize_to_jq
