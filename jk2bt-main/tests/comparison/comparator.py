"""
tests/comparison/comparator.py
数据比较核心模块

实现 jk2bt 和 JQ 数据的数值比较逻辑。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import warnings


class DataType(Enum):
    """数据类型枚举"""
    PRICE = "price"
    VOLUME = "volume"
    RATIO = "ratio"
    FACTOR = "factor"
    MONEY = "money"


@dataclass
class DiffResult:
    """差异结果"""
    field: str
    data_type: str
    total_count: int
    match_count: int
    diff_count: int
    nan_diff_count: int
    max_rel_diff: float
    mean_rel_diff: float
    median_rel_diff: float
    pass_rate: float
    tolerance: float
    details: pd.DataFrame = field(default_factory=pd.DataFrame)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "field": self.field,
            "data_type": self.data_type,
            "total_count": self.total_count,
            "match_count": self.match_count,
            "diff_count": self.diff_count,
            "nan_diff_count": self.nan_diff_count,
            "max_rel_diff": self.max_rel_diff,
            "mean_rel_diff": self.mean_rel_diff,
            "median_rel_diff": self.median_rel_diff,
            "pass_rate": self.pass_rate,
            "tolerance": self.tolerance,
        }


class DataComparator:
    """
    数据比较器

    比较 jk2bt 和 JQ 数据的数值差异。

    使用方式:
        comparator = DataComparator()
        results = comparator.compare_dataframes(jk2bt_df, jq_df)
    """

    # 默认容忍度配置
    DEFAULT_TOLERANCE = {
        DataType.PRICE: 0.01,
        DataType.VOLUME: 0.05,
        DataType.RATIO: 0.001,
        DataType.FACTOR: 0.01,
        DataType.MONEY: 0.02,
    }

    # 字段类型映射
    FIELD_TYPE_MAP = {
        # 行情
        "open": DataType.PRICE,
        "high": DataType.PRICE,
        "low": DataType.PRICE,
        "close": DataType.PRICE,
        "volume": DataType.VOLUME,
        "money": DataType.MONEY,
        "amount": DataType.MONEY,
        # 估值
        "pe_ratio": DataType.FACTOR,
        "pb_ratio": DataType.FACTOR,
        "ps_ratio": DataType.FACTOR,
        "market_cap": DataType.FACTOR,
        "circulating_market_cap": DataType.FACTOR,
        "turnover_ratio": DataType.RATIO,
        # 财务
        "revenue": DataType.MONEY,
        "net_profit": DataType.MONEY,
        "total_assets": DataType.MONEY,
        "roe": DataType.RATIO,
        "roa": DataType.RATIO,
    }

    def __init__(
        self,
        tolerance: Optional[Dict[DataType, float]] = None,
        custom_field_types: Optional[Dict[str, DataType]] = None,
    ):
        """
        初始化比较器。

        Parameters
        ----------
        tolerance : dict, optional
            自定义容忍度配置
        custom_field_types : dict, optional
            自定义字段类型映射
        """
        self.tolerance = tolerance or self.DEFAULT_TOLERANCE.copy()
        if custom_field_types:
            self.FIELD_TYPE_MAP.update(custom_field_types)

    def get_field_type(self, field_name: str) -> DataType:
        """获取字段类型"""
        return self.FIELD_TYPE_MAP.get(field_name, DataType.FACTOR)

    def get_tolerance(self, field_name: str) -> float:
        """获取字段的容忍度"""
        field_type = self.get_field_type(field_name)
        return self.tolerance.get(field_type, 0.01)

    def compare_dataframes(
        self,
        jk2bt_df: pd.DataFrame,
        jq_df: pd.DataFrame,
        compare_columns: Optional[List[str]] = None,
        index_align: bool = True,
        detail_limit: int = 100,
    ) -> Dict[str, DiffResult]:
        """
        比较两个 DataFrame。

        Parameters
        ----------
        jk2bt_df : pd.DataFrame
            jk2bt 数据
        jq_df : pd.DataFrame
            JoinQuant 数据
        compare_columns : list, optional
            要比较的列，默认比较所有共有列
        index_align : bool
            是否对齐索引
        detail_limit : int
            详细差异记录的最大数量

        Returns
        -------
        Dict[str, DiffResult]
            每列的比较结果
        """
        # 确定比较列
        if compare_columns is None:
            compare_columns = list(
                set(jk2bt_df.columns) & set(jq_df.columns)
            )

        if not compare_columns:
            warnings.warn("没有共同的列可以比较")
            return {}

        # 对齐索引
        if index_align:
            common_index = jk2bt_df.index.intersection(jq_df.index)
            if len(common_index) == 0:
                warnings.warn("没有共同的索引")
                return {}
            jk2bt_df = jk2bt_df.loc[common_index]
            jq_df = jq_df.loc[common_index]

        results = {}

        for col in compare_columns:
            if col not in jk2bt_df.columns or col not in jq_df.columns:
                continue

            result = self._compare_series(
                jk2bt_df[col],
                jq_df[col],
                col,
                detail_limit,
            )
            results[col] = result

        return results

    def _compare_series(
        self,
        jk2bt_series: pd.Series,
        jq_series: pd.Series,
        field_name: str,
        detail_limit: int = 100,
    ) -> DiffResult:
        """比较两个 Series"""
        field_type = self.get_field_type(field_name)
        tolerance = self.get_tolerance(field_name)

        # 获取有效数据索引
        jq_valid = jq_series.dropna()
        total_count = len(jq_valid)

        if total_count == 0:
            return DiffResult(
                field=field_name,
                data_type=field_type.value,
                total_count=0,
                match_count=0,
                diff_count=0,
                nan_diff_count=0,
                max_rel_diff=0.0,
                mean_rel_diff=0.0,
                median_rel_diff=0.0,
                pass_rate=1.0,
                tolerance=tolerance,
            )

        match_count = 0
        diff_count = 0
        rel_diffs = []
        diff_details = []

        for idx in jq_valid.index:
            jq_val = jq_series.loc[idx]
            jk2bt_val = jk2bt_series.get(idx, np.nan)

            is_match, diff = self._compare_values(
                jk2bt_val, jq_val, field_type, tolerance
            )

            if is_match:
                match_count += 1
            else:
                diff_count += 1
                if diff is not None and not np.isnan(diff):
                    rel_diffs.append(diff)

                    # 记录详细差异
                    if len(diff_details) < detail_limit:
                        diff_details.append({
                            "index": str(idx),
                            "jq_value": jq_val,
                            "jk2bt_value": jk2bt_val,
                            "rel_diff": diff,
                        })

        # NaN 差异统计
        jq_nan_mask = jq_series.isna()
        jk2bt_nan_mask = jk2bt_series.isna()
        nan_diff_count = (jq_nan_mask != jk2bt_nan_mask).sum()

        # 计算统计量
        max_rel_diff = max(rel_diffs) if rel_diffs else 0.0
        mean_rel_diff = float(np.mean(rel_diffs)) if rel_diffs else 0.0
        median_rel_diff = float(np.median(rel_diffs)) if rel_diffs else 0.0
        pass_rate = match_count / total_count if total_count > 0 else 1.0

        return DiffResult(
            field=field_name,
            data_type=field_type.value,
            total_count=total_count,
            match_count=match_count,
            diff_count=diff_count,
            nan_diff_count=int(nan_diff_count),
            max_rel_diff=float(max_rel_diff),
            mean_rel_diff=float(mean_rel_diff),
            median_rel_diff=float(median_rel_diff),
            pass_rate=float(pass_rate),
            tolerance=tolerance,
            details=pd.DataFrame(diff_details) if diff_details else pd.DataFrame(),
        )

    def _compare_values(
        self,
        jk2bt_val: float,
        jq_val: float,
        field_type: DataType,
        tolerance: float,
    ) -> Tuple[bool, Optional[float]]:
        """
        比较单个值。

        Returns
        -------
        Tuple[bool, Optional[float]]
            (是否一致, 相对误差)
        """
        # 双方都是 NaN
        if pd.isna(jq_val) and pd.isna(jk2bt_val):
            return True, 0.0

        # 一方是 NaN
        if pd.isna(jq_val) or pd.isna(jk2bt_val):
            return False, None

        # 计算差异
        abs_diff = abs(jk2bt_val - jq_val)

        # 对于比例类数据，使用绝对差异
        if field_type == DataType.RATIO:
            return abs_diff < tolerance, abs_diff

        # 对于其他类型，使用相对差异
        if jq_val == 0:
            # 如果基准值为0，使用绝对差异
            rel_diff = abs_diff
        else:
            rel_diff = abs_diff / abs(jq_val)

        return rel_diff < tolerance, rel_diff

    def compare_component_lists(
        self,
        jk2bt_list: List[str],
        jq_list: List[str],
        name: str = "component",
    ) -> Dict:
        """
        比较成分股列表。

        Parameters
        ----------
        jk2bt_list : list
            jk2bt 成分股列表
        jq_list : list
            JQ 成分股列表
        name : str
            列表名称

        Returns
        -------
        Dict
            比较结果
        """
        jk2bt_set = set(jk2bt_list)
        jq_set = set(jq_list)

        common = jk2bt_set & jq_set
        only_jk2bt = jk2bt_set - jq_set
        only_jq = jq_set - jk2bt_set

        match_rate = len(common) / len(jq_set) if jq_set else 0.0

        return {
            "name": name,
            "jk2bt_count": len(jk2bt_list),
            "jq_count": len(jq_list),
            "common_count": len(common),
            "only_jk2bt": list(only_jk2bt),
            "only_jq": list(only_jq),
            "match_rate": match_rate,
            "pass": match_rate > 0.95,
        }

    def generate_summary(self, results: Dict[str, DiffResult]) -> pd.DataFrame:
        """
        生成比较结果摘要。

        Parameters
        ----------
        results : Dict[str, DiffResult]
            比较结果

        Returns
        -------
        pd.DataFrame
            摘要表格
        """
        summary_data = []

        for field, result in results.items():
            summary_data.append({
                "字段": field,
                "类型": result.data_type,
                "总数": result.total_count,
                "匹配数": result.match_count,
                "差异数": result.diff_count,
                "NaN差异": result.nan_diff_count,
                "通过率": f"{result.pass_rate:.2%}",
                "最大误差": f"{result.max_rel_diff:.4f}",
                "平均误差": f"{result.mean_rel_diff:.6f}",
                "容忍度": f"{result.tolerance:.4f}",
                "状态": "✓ 通过" if result.pass_rate > 0.95 else "✗ 失败",
            })

        return pd.DataFrame(summary_data)


def quick_compare(
    jk2bt_df: pd.DataFrame,
    jq_df: pd.DataFrame,
    name: str = "数据",
) -> Tuple[bool, pd.DataFrame]:
    """
    快速比较两个 DataFrame。

    Parameters
    ----------
    jk2bt_df : pd.DataFrame
        jk2bt 数据
    jq_df : pd.DataFrame
        JQ 数据
    name : str
        数据名称

    Returns
    -------
    Tuple[bool, pd.DataFrame]
        (是否通过, 摘要表格)
    """
    comparator = DataComparator()
    results = comparator.compare_dataframes(jk2bt_df, jq_df)
    summary = comparator.generate_summary(results)

    # 判断是否通过
    all_pass = all(r.pass_rate > 0.95 for r in results.values())

    return all_pass, summary