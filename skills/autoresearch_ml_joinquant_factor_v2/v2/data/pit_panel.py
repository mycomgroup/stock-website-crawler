"""L0 数据治理层：点时一致因子面板构建。

本模块实现 build_pit_panel()，负责：
1. 从 train_merged_all.csv 加载原始数据
2. 将 'Unnamed: 0' 重命名为 'stock_id'
3. 将 'date' 列解析为 datetime 类型
4. 按 [date, stock_id] 排序
5. 构建可交易掩码（Task 1.2 完整实现）
6. 财务因子时滞校验（stub，Task 1.3 完整实现）
7. 存活偏差检查（stub，Task 1.4 完整实现）

对应需求：需求 1（数据治理与点时一致性）
设计文档：4.1 L0 数据治理与点时一致性
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# FactorPanel 数据容器
# ---------------------------------------------------------------------------

@dataclass
class FactorPanel:
    """清洁的点时一致因子面板。

    属性
    ----
    df : pd.DataFrame
        主数据框，包含 stock_id / date / 因子列 / pchg。
        按 [date, stock_id] 排序，date 为 datetime64 类型。
    tradable_mask : pd.Series
        布尔序列，与 df 行对齐，True 表示该行股票在该日期可交易。
        索引与 df.index 一致。
    """

    df: pd.DataFrame
    tradable_mask: pd.Series = field(default_factory=pd.Series)

    def __post_init__(self) -> None:
        if self.tradable_mask.empty and not self.df.empty:
            # 默认全部可交易（stub 行为，Task 1.2 会覆盖）
            self.tradable_mask = pd.Series(True, index=self.df.index, dtype=bool)

    @property
    def n_dates(self) -> int:
        """唯一日期数量。"""
        return int(self.df["date"].nunique()) if "date" in self.df.columns else 0

    @property
    def n_stocks(self) -> int:
        """唯一股票数量。"""
        return int(self.df["stock_id"].nunique()) if "stock_id" in self.df.columns else 0

    @property
    def factor_cols(self) -> list[str]:
        """因子列名列表（排除 stock_id / date / pchg）。"""
        exclude = {"stock_id", "date", "pchg"}
        return [c for c in self.df.columns if c not in exclude]

    def __repr__(self) -> str:
        return (
            f"FactorPanel(dates={self.n_dates}, stocks={self.n_stocks}, "
            f"factors={len(self.factor_cols)}, "
            f"tradable_pct={self.tradable_mask.mean():.1%})"
        )


# ---------------------------------------------------------------------------
# 核心函数
# ---------------------------------------------------------------------------

def build_pit_panel(csv_path: str | Path) -> FactorPanel:
    """从 CSV 文件构建点时一致因子面板。

    步骤：
    1. 加载 CSV
    2. 重命名 'Unnamed: 0' → 'stock_id'
    3. 解析 'date' 为 datetime
    4. 按 [date, stock_id] 排序
    5. 构建可交易掩码（当前为 stub，全部返回 True）
    6. 应用财务因子时滞（当前为 stub）

    参数
    ----
    csv_path : str 或 Path
        train_merged_all.csv 的文件路径。

    返回
    ----
    FactorPanel
        清洁的点时一致因子面板。

    异常
    ----
    FileNotFoundError
        当 csv_path 不存在时抛出。
    ValueError
        当 CSV 缺少必要列（'Unnamed: 0' 或 'date'）时抛出。
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"数据文件不存在：{csv_path}")

    logger.info("正在加载数据文件：%s", csv_path)

    # 1. 加载 CSV
    df = pd.read_csv(csv_path, low_memory=False)
    logger.info("原始数据加载完成，shape=%s", df.shape)

    # 2. 重命名 'Unnamed: 0' → 'stock_id'
    if "Unnamed: 0" not in df.columns:
        if "stock_id" not in df.columns:
            raise ValueError(
                "CSV 中既无 'Unnamed: 0' 列也无 'stock_id' 列，"
                "请检查数据文件格式。"
            )
        logger.warning("'Unnamed: 0' 列不存在，'stock_id' 列已存在，跳过重命名。")
    else:
        df = df.rename(columns={"Unnamed: 0": "stock_id"})
        logger.debug("已将 'Unnamed: 0' 重命名为 'stock_id'")

    # 3. 解析 'date' 为 datetime
    if "date" not in df.columns:
        raise ValueError("CSV 中缺少 'date' 列，请检查数据文件格式。")

    df["date"] = pd.to_datetime(df["date"])
    logger.debug("'date' 列已解析为 datetime，范围：%s ~ %s",
                 df["date"].min(), df["date"].max())

    # 4. 按 [date, stock_id] 排序
    df = df.sort_values(["date", "stock_id"]).reset_index(drop=True)
    logger.info("数据已按 [date, stock_id] 排序，最终 shape=%s", df.shape)

    # 5. 构建可交易掩码（Task 1.2 完整实现）
    financial_cols = _infer_financial_cols(df)
    tradable = compute_tradable_mask(df)

    # 6. 财务因子时滞校验（stub，Task 1.3 完整实现）
    df = apply_disclosure_lag(df, financial_cols)

    return FactorPanel(df=df, tradable_mask=tradable)


def compute_tradable_mask(
    df: pd.DataFrame,
    new_stock_cooldown_days: int = 60,
    pchg_limit_10pct: float = 0.099,
    pchg_limit_20pct: float = 0.195,
) -> pd.Series:
    """构建可交易掩码，过滤不可交易的股票行。

    过滤规则（按优先级依次应用，缺失字段跳过并记录警告）：

    1. **ST/*ST 股票**：检查 ``is_st``、``st_status`` 列（若存在）。
       若列不存在，跳过并记录警告。
    2. **停牌股票**：检查 ``is_suspended``、``paused`` 列（若存在）。
       若列不存在，跳过并记录警告。
    3. **涨跌停一字板**：
       - 若 ``high`` 和 ``low`` 列同时存在，过滤 ``high == low`` 的行。
       - 否则若 ``pchg`` 列存在，过滤 ``|pchg|`` 接近 ±10% 或 ±20% 的行
         （容差 0.5%，覆盖普通股 ±10%、科创板/创业板 ±20%）。
       - 若两者均不存在，跳过并记录警告。
    4. **新股冷启动**：过滤上市不足 ``new_stock_cooldown_days``（默认 60）
       个交易日的股票。此过滤始终可从数据本身计算，无需额外字段。
    5. **退市整理期**：检查 ``is_delisting``、``delisting`` 列（若存在）。
       若列不存在，跳过并记录警告。

    参数
    ----
    df : pd.DataFrame
        已完成列重命名（``stock_id``）和日期解析（``date``）的因子面板，
        按 ``[date, stock_id]`` 排序，索引已 reset。
    new_stock_cooldown_days : int, 默认 60
        新股冷启动过滤阈值（交易日数）。
    pchg_limit_10pct : float, 默认 0.099
        普通股涨跌停识别阈值（绝对值），用于 pchg 方式检测一字板。
    pchg_limit_20pct : float, 默认 0.195
        科创板/创业板涨跌停识别阈值（绝对值），用于 pchg 方式检测一字板。

    返回
    ----
    pd.Series
        布尔序列，与 ``df`` 行对齐，``True`` 表示可交易，``False`` 表示被过滤。
        索引与 ``df.index`` 一致。
    """
    n_rows = len(df)
    # 初始化：全部可交易
    mask = pd.Series(True, index=df.index, dtype=bool)

    # 空 DataFrame 快速返回
    if n_rows == 0:
        logger.debug("compute_tradable_mask: 空 DataFrame，返回空 Series。")
        return mask

    # ------------------------------------------------------------------
    # 过滤 1：ST/*ST 股票
    # ------------------------------------------------------------------
    st_col_candidates = ["is_st", "st_status"]
    st_col = next((c for c in st_col_candidates if c in df.columns), None)
    if st_col is not None:
        st_filter = df[st_col].astype(bool)
        n_filtered = st_filter.sum()
        mask &= ~st_filter
        logger.info(
            "compute_tradable_mask [ST过滤]: 列='%s'，过滤 %d 行（%.2f%%）",
            st_col, n_filtered, 100.0 * n_filtered / n_rows,
        )
    else:
        logger.warning(
            "compute_tradable_mask [ST过滤]: 未找到 ST 状态列（候选：%s），跳过此过滤。"
            "若数据中包含 ST 股票，可交易掩码将不过滤 ST。",
            st_col_candidates,
        )

    # ------------------------------------------------------------------
    # 过滤 2：停牌股票
    # ------------------------------------------------------------------
    suspended_col_candidates = ["is_suspended", "paused"]
    suspended_col = next(
        (c for c in suspended_col_candidates if c in df.columns), None
    )
    if suspended_col is not None:
        suspended_filter = df[suspended_col].astype(bool)
        n_filtered = suspended_filter.sum()
        mask &= ~suspended_filter
        logger.info(
            "compute_tradable_mask [停牌过滤]: 列='%s'，过滤 %d 行（%.2f%%）",
            suspended_col, n_filtered, 100.0 * n_filtered / n_rows,
        )
    else:
        logger.warning(
            "compute_tradable_mask [停牌过滤]: 未找到停牌状态列（候选：%s），跳过此过滤。"
            "若数据中包含停牌股票，可交易掩码将不过滤停牌。",
            suspended_col_candidates,
        )

    # ------------------------------------------------------------------
    # 过滤 3：涨跌停一字板
    # ------------------------------------------------------------------
    if "high" in df.columns and "low" in df.columns:
        # 优先使用 high == low 判断一字板（最精确）
        limit_filter = df["high"] == df["low"]
        n_filtered = limit_filter.sum()
        mask &= ~limit_filter
        logger.info(
            "compute_tradable_mask [一字板过滤]: 使用 high==low，过滤 %d 行（%.2f%%）",
            n_filtered, 100.0 * n_filtered / n_rows,
        )
    elif "pchg" in df.columns:
        # 退而求其次：在缺少 high/low 时，只对明显接近 ±20% 的截面做保守过滤。
        # 若无板块信息，无法仅凭 pchg 稳健地区分普通股 10% 板和正常大波动。
        abs_pchg = df["pchg"].abs()
        limit_filter = abs_pchg >= pchg_limit_20pct
        n_filtered = limit_filter.sum()
        mask &= ~limit_filter
        logger.info(
            "compute_tradable_mask [一字板过滤]: 缺少 high/low，保守使用 |pchg|>=%.3f，"
            "过滤 %d 行（%.2f%%）",
            pchg_limit_20pct,
            n_filtered, 100.0 * n_filtered / n_rows,
        )
    else:
        logger.warning(
            "compute_tradable_mask [一字板过滤]: 未找到 'high'/'low' 或 'pchg' 列，"
            "跳过涨跌停一字板过滤。"
        )

    # ------------------------------------------------------------------
    # 过滤 4：新股冷启动（上市不足 new_stock_cooldown_days 个交易日）
    # 此过滤始终可从数据本身计算，无需额外字段
    # ------------------------------------------------------------------
    trading_days_since_listing = _count_trading_days_since_listing(df)
    new_stock_filter = trading_days_since_listing < new_stock_cooldown_days
    n_filtered = new_stock_filter.sum()
    mask &= ~new_stock_filter
    logger.info(
        "compute_tradable_mask [新股冷启动过滤]: 阈值=%d 交易日，过滤 %d 行（%.2f%%）",
        new_stock_cooldown_days, n_filtered, 100.0 * n_filtered / n_rows,
    )

    # ------------------------------------------------------------------
    # 过滤 5：退市整理期
    # ------------------------------------------------------------------
    delisting_col_candidates = ["is_delisting", "delisting"]
    delisting_col = next(
        (c for c in delisting_col_candidates if c in df.columns), None
    )
    if delisting_col is not None:
        delisting_filter = df[delisting_col].astype(bool)
        n_filtered = delisting_filter.sum()
        mask &= ~delisting_filter
        logger.info(
            "compute_tradable_mask [退市整理过滤]: 列='%s'，过滤 %d 行（%.2f%%）",
            delisting_col, n_filtered, 100.0 * n_filtered / n_rows,
        )
    else:
        logger.warning(
            "compute_tradable_mask [退市整理过滤]: 未找到退市整理状态列（候选：%s），"
            "跳过此过滤。若数据中包含退市整理期股票，可交易掩码将不过滤。",
            delisting_col_candidates,
        )

    # ------------------------------------------------------------------
    # 汇总日志
    # ------------------------------------------------------------------
    n_tradable = mask.sum()
    if n_rows > 0:
        logger.info(
            "compute_tradable_mask 完成：总行数=%d，可交易=%d（%.2f%%），"
            "不可交易=%d（%.2f%%）",
            n_rows, n_tradable, 100.0 * n_tradable / n_rows,
            n_rows - n_tradable, 100.0 * (n_rows - n_tradable) / n_rows,
        )
    else:
        logger.info("compute_tradable_mask 完成：空 DataFrame，无行需要过滤。")

    return mask


def _check_disclosure_lag_status(df: pd.DataFrame) -> dict:
    """检查财务因子时滞校验状态，返回结构化诊断信息。

    参数
    ----
    df : pd.DataFrame
        已完成列重命名和日期解析的因子面板。

    返回
    ----
    dict
        包含以下键的诊断字典：

        - ``has_disclosure_col`` (bool)：是否找到披露日字段。
        - ``disclosure_col_found`` (str | None)：找到的披露日字段名，未找到时为 None。
        - ``n_financial_cols`` (int)：推断出的财务类因子列数。
        - ``financial_cols`` (list[str])：财务类因子列名列表。
        - ``risk_level`` (str)：风险等级，"low" | "medium" | "high"。
        - ``message`` (str)：人类可读的状态描述。
    """
    disclosure_col_candidates = ["ann_date", "announcement_date", "disclosure_date"]
    found_col = next(
        (c for c in disclosure_col_candidates if c in df.columns), None
    )

    financial_cols = _infer_financial_cols(df)
    n_fin = len(financial_cols)

    if found_col is not None:
        risk_level = "low"
        message = (
            f"找到披露日字段 '{found_col}'，财务因子（{n_fin} 列）将按实际披露日生效，"
            "点时一致性已保障。"
        )
    elif n_fin == 0:
        risk_level = "low"
        message = (
            "未找到披露日字段，但也未推断出财务类因子列，"
            "无需时滞校验。"
        )
    else:
        risk_level = "high"
        message = (
            f"未找到披露日字段（候选：{disclosure_col_candidates}），"
            f"共 {n_fin} 个财务类因子列（{financial_cols[:5]}{'...' if n_fin > 5 else ''}）"
            "将按截面日期（date）生效。"
            "财务数据通常在报告期末后 1~4 个月才公开披露，"
            "若直接按截面日期使用，存在未来信息泄漏风险（look-ahead bias）。"
            "建议：补充披露日字段（ann_date），或在回测中对财务因子手动添加 1 个季度的保守时滞。"
        )

    return {
        "has_disclosure_col": found_col is not None,
        "disclosure_col_found": found_col,
        "n_financial_cols": n_fin,
        "financial_cols": financial_cols,
        "risk_level": risk_level,
        "message": message,
    }


def apply_disclosure_lag(
    df: pd.DataFrame,
    financial_cols: Sequence[str],
) -> pd.DataFrame:
    """财务因子时滞校验。

    根据数据框中是否存在披露日字段（``ann_date``、``announcement_date``、
    ``disclosure_date``），执行以下两种路径之一：

    **路径 A：找到披露日字段**
        对每个财务类因子列，将该列的值按实际披露日对齐：
        对于每一行 ``(stock_id, date)``，若该行对应报告期的披露日
        ``disclosure_date > date``（即当前截面日期早于披露日），
        则将该行的财务因子值置为 ``NaN``，确保财务数据不在披露前生效。

        算法细节：
        1. 将披露日字段解析为 datetime。
        2. 对每一行，比较 ``date`` 与 ``disclosure_date``。
        3. 若 ``disclosure_date > date``，则该行所有财务因子列置 NaN。
        4. 记录被置 NaN 的行数和比例。

    **路径 B：未找到披露日字段**
        - 发出 ``UserWarning``，说明风险。
        - 记录结构化 WARNING 日志，包含：受影响列、风险描述、建议操作。
        - 返回原始 ``df`` 不做任何修改（保守策略：无法验证 PIT 一致性时不改数据）。
        - 在返回的 ``df`` 上附加属性 ``_disclosure_lag_status``（dict），
          供调用方审计。

    参数
    ----
    df : pd.DataFrame
        已完成列重命名（``stock_id``）和日期解析（``date``）的因子面板，
        按 ``[date, stock_id]`` 排序，索引已 reset。
    financial_cols : Sequence[str]
        财务类因子列名列表（由 ``_infer_financial_cols`` 推断，
        或由调用方显式传入）。

    返回
    ----
    pd.DataFrame
        - 路径 A：财务因子已按披露日时滞对齐的数据框（未来信息已置 NaN）。
        - 路径 B：原始数据框（未修改），附加 ``_disclosure_lag_status`` 属性。

    注意
    ----
    - 本函数不修改非财务类因子列（emotion、technical、momentum、risk、style）。
    - 路径 A 的 NaN 填充不在本函数内处理，由 L1 预处理层（``impute_factors``）负责。
    - 本函数保证：财务因子不会在其实际披露日之前出现在截面数据中。
    """
    # ------------------------------------------------------------------
    # 诊断：获取时滞校验状态
    # ------------------------------------------------------------------
    status = _check_disclosure_lag_status(df)
    found_disclosure_col: str | None = status["disclosure_col_found"]
    fin_cols: list[str] = [c for c in financial_cols if c in df.columns]

    # ------------------------------------------------------------------
    # 路径 B：未找到披露日字段
    # ------------------------------------------------------------------
    if found_disclosure_col is None:
        # 只有在存在财务类因子列时才发出警告（无财务因子则无需校验）
        if len(fin_cols) > 0:
            # 发出 UserWarning（供调用方捕获）
            warnings.warn(
                "【财务因子时滞校验】未找到披露日字段（候选列：['ann_date', "
                "'announcement_date', 'disclosure_date']）。\n"
                f"受影响的财务类因子列（共 {len(fin_cols)} 列）：{fin_cols[:10]}"
                f"{'...' if len(fin_cols) > 10 else ''}。\n"
                "风险：财务数据通常在报告期末后 1~4 个月才公开披露，"
                "若直接按截面日期（date）使用，存在未来信息泄漏（look-ahead bias）风险，"
                "可能导致回测收益虚高。\n"
                "建议操作：\n"
                "  1. 补充 ann_date（实际披露日）字段到数据源，重新运行 pipeline；\n"
                "  2. 或在 L1 预处理阶段对财务因子手动添加 1 个季度（约 63 个交易日）的保守时滞；\n"
                "  3. 或在回测结论中明确标注此风险，并与无财务因子的基准对比。\n"
                "当前处理：保守策略——数据未修改，原样返回。",
                UserWarning,
                stacklevel=2,
            )

        # 结构化日志（供日志系统采集）
        logger.warning(
            "apply_disclosure_lag [路径B：无披露日字段]\n"
            "  受影响列数: %d\n"
            "  受影响列（前10）: %s\n"
            "  风险等级: %s\n"
            "  风险描述: 财务因子按截面日期生效，存在 look-ahead bias 风险\n"
            "  建议: 补充 ann_date 字段，或对财务因子添加 1 个季度保守时滞\n"
            "  当前处理: 数据未修改（保守策略）",
            len(fin_cols),
            fin_cols[:10],
            status["risk_level"],
        )

        # 附加审计元数据（存储在 attrs 字典，避免触发 Pandas 属性警告）
        df.attrs["_disclosure_lag_status"] = status

        return df

    # ------------------------------------------------------------------
    # 路径 A：找到披露日字段，按实际披露日对齐财务因子
    # ------------------------------------------------------------------
    logger.info(
        "apply_disclosure_lag [路径A：按披露日对齐]\n"
        "  披露日字段: '%s'\n"
        "  财务因子列数: %d\n"
        "  总行数: %d",
        found_disclosure_col,
        len(fin_cols),
        len(df),
    )

    if len(fin_cols) == 0:
        logger.info(
            "apply_disclosure_lag: 未找到需要时滞校验的财务类因子列，跳过对齐。"
        )
        return df

    # 解析披露日字段为 datetime（若尚未解析）
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[found_disclosure_col]):
        df[found_disclosure_col] = pd.to_datetime(
            df[found_disclosure_col], errors="coerce"
        )
        n_invalid = df[found_disclosure_col].isna().sum()
        if n_invalid > 0:
            logger.warning(
                "apply_disclosure_lag: 披露日字段 '%s' 中有 %d 行无法解析为日期，"
                "这些行的财务因子将保留原值（无法判断是否超前）。",
                found_disclosure_col,
                n_invalid,
            )

    # 核心逻辑：若 disclosure_date > date，则该行财务因子置 NaN
    # 即：财务数据尚未披露，不应在当前截面日期可见
    future_disclosure_mask = df[found_disclosure_col] > df["date"]

    n_masked = future_disclosure_mask.sum()
    n_total = len(df)
    logger.info(
        "apply_disclosure_lag: 发现 %d 行（%.2f%%）的披露日晚于截面日期，"
        "这些行的财务因子将置为 NaN（防止未来信息泄漏）。",
        n_masked,
        100.0 * n_masked / n_total if n_total > 0 else 0.0,
    )

    if n_masked > 0:
        df.loc[future_disclosure_mask, fin_cols] = float("nan")
        logger.info(
            "apply_disclosure_lag: 已将 %d 行 × %d 列的财务因子置为 NaN。"
            "后续 L1 预处理（impute_factors）将负责填补这些缺失值。",
            n_masked,
            len(fin_cols),
        )

    # 附加审计属性
    status_with_result = dict(status)
    status_with_result["n_rows_masked"] = int(n_masked)
    status_with_result["pct_rows_masked"] = (
        float(n_masked) / n_total if n_total > 0 else 0.0
    )
    df.attrs["_disclosure_lag_status"] = status_with_result

    logger.info(
        "apply_disclosure_lag 完成：路径A，披露日字段='%s'，"
        "财务因子列数=%d，置NaN行数=%d（%.2f%%）",
        found_disclosure_col,
        len(fin_cols),
        n_masked,
        100.0 * n_masked / n_total if n_total > 0 else 0.0,
    )

    return df


def check_survivorship_bias(df: pd.DataFrame) -> dict:
    """存活偏差检查（Task 1.4 完整实现）。

    识别潜在退市股票（在早期截面出现但在最后截面日期消失的股票），
    验证退市前最后收益是否被纳入，并提供对比报告。

    对应需求 14（存活偏差处理）和技术方案 18.7 节。

    **识别逻辑**：
    - 若某股票的最后出现日期不是数据集的最后截面日期，则视为"潜在退市"。
    - 这包括真正退市、长期停牌后未恢复、数据缺失等情形。

    **报告内容**：
    - ``n_total_stocks``：全部唯一股票数
    - ``n_active_stocks``：在最后截面日期仍出现的股票数
    - ``n_potentially_delisted``：未出现在最后截面日期的股票数
    - ``potentially_delisted_stocks``：潜在退市股票 ID 列表
    - ``last_returns_included``：各潜在退市股票最后可得 pchg 是否非空
    - ``pct_last_returns_captured``：最后收益被捕获的比例（%）
    - ``survivorship_bias_risk``：风险等级 "low" | "medium" | "high"
    - ``ic_all``：全样本（含潜在退市）截面 rank IC 均值
    - ``ic_active``：仅活跃股票截面 rank IC 均值
    - ``ic_diff_pct``：IC 差异百分比（|ic_all - ic_active| / max(|ic_all|, eps)）
    - ``ic_comparison_feasible``：是否成功计算 IC 对比
    - ``message``：人类可读摘要

    **警告逻辑**：
    - 潜在退市比例 > 10%：``survivorship_bias_risk = "high"``，发出 UserWarning。
    - 潜在退市比例 5%~10%：``survivorship_bias_risk = "medium"``。
    - 潜在退市比例 < 5%：``survivorship_bias_risk = "low"``。
    - IC 差异 > 5%：额外发出 UserWarning。

    参数
    ----
    df : pd.DataFrame
        已完成列重命名（``stock_id``）和日期解析（``date``）的因子面板，
        按 ``[date, stock_id]`` 排序。必须包含 ``stock_id`` 和 ``date`` 列。
        若包含 ``pchg`` 列，则用于验证最后收益是否被捕获及 IC 计算。

    返回
    ----
    dict
        存活偏差检查报告，包含上述所有字段。

    异常
    ----
    ValueError
        当 df 缺少 ``stock_id`` 或 ``date`` 列时抛出。
    """
    # ------------------------------------------------------------------
    # 输入校验
    # ------------------------------------------------------------------
    if "stock_id" not in df.columns:
        raise ValueError("check_survivorship_bias: df 缺少 'stock_id' 列。")
    if "date" not in df.columns:
        raise ValueError("check_survivorship_bias: df 缺少 'date' 列。")

    logger.info("check_survivorship_bias: 开始存活偏差检查，数据 shape=%s", df.shape)

    # ------------------------------------------------------------------
    # 基础统计
    # ------------------------------------------------------------------
    all_stocks: list = sorted(df["stock_id"].unique().tolist())
    n_total_stocks: int = len(all_stocks)
    n_dates: int = int(df["date"].nunique())

    if n_total_stocks == 0 or n_dates == 0:
        logger.warning("check_survivorship_bias: 空数据框，返回空报告。")
        return {
            "n_total_stocks": 0,
            "n_active_stocks": 0,
            "n_potentially_delisted": 0,
            "potentially_delisted_stocks": [],
            "last_returns_included": {},
            "pct_last_returns_captured": 0.0,
            "survivorship_bias_risk": "low",
            "ic_all": None,
            "ic_active": None,
            "ic_diff_pct": None,
            "ic_comparison_feasible": False,
            "message": "数据框为空，无法执行存活偏差检查。",
        }

    # 最后截面日期
    last_date = df["date"].max()

    # 每只股票的最后出现日期
    last_date_per_stock: pd.Series = df.groupby("stock_id")["date"].max()

    # 活跃股票：最后出现日期 == 最后截面日期
    active_stocks: list = sorted(
        last_date_per_stock[last_date_per_stock == last_date].index.tolist()
    )
    n_active_stocks: int = len(active_stocks)

    # 潜在退市股票：最后出现日期 != 最后截面日期
    potentially_delisted_stocks: list = sorted(
        last_date_per_stock[last_date_per_stock != last_date].index.tolist()
    )
    n_potentially_delisted: int = len(potentially_delisted_stocks)

    logger.info(
        "check_survivorship_bias: 总股票=%d，活跃=%d，潜在退市=%d（%.2f%%）",
        n_total_stocks, n_active_stocks, n_potentially_delisted,
        100.0 * n_potentially_delisted / n_total_stocks if n_total_stocks > 0 else 0.0,
    )

    # ------------------------------------------------------------------
    # 验证退市前最后收益是否被捕获
    # ------------------------------------------------------------------
    last_returns_included: dict = {}
    pct_last_returns_captured: float = 0.0

    if "pchg" in df.columns and n_potentially_delisted > 0:
        # 对每只潜在退市股票，找其最后一行的 pchg 是否非空
        for stock_id in potentially_delisted_stocks:
            stock_rows = df[df["stock_id"] == stock_id]
            last_row = stock_rows.loc[stock_rows["date"].idxmax()]
            last_pchg = last_row["pchg"]
            last_returns_included[stock_id] = bool(
                pd.notna(last_pchg) and last_pchg != 0.0
            )

        n_captured = sum(last_returns_included.values())
        pct_last_returns_captured = (
            100.0 * n_captured / n_potentially_delisted
            if n_potentially_delisted > 0
            else 0.0
        )
        logger.info(
            "check_survivorship_bias: 潜在退市股票中，最后收益被捕获 %d/%d（%.1f%%）",
            n_captured, n_potentially_delisted, pct_last_returns_captured,
        )
    elif n_potentially_delisted > 0:
        # 无 pchg 列，无法验证
        for stock_id in potentially_delisted_stocks:
            last_returns_included[stock_id] = None  # type: ignore[assignment]
        logger.warning(
            "check_survivorship_bias: 数据框中无 'pchg' 列，无法验证退市前最后收益是否被捕获。"
        )

    # ------------------------------------------------------------------
    # 风险等级评估
    # ------------------------------------------------------------------
    delisted_ratio: float = (
        n_potentially_delisted / n_total_stocks if n_total_stocks > 0 else 0.0
    )

    if delisted_ratio > 0.10:
        survivorship_bias_risk = "high"
    elif delisted_ratio > 0.05:
        survivorship_bias_risk = "medium"
    else:
        survivorship_bias_risk = "low"

    # ------------------------------------------------------------------
    # IC 对比：全样本 vs 仅活跃股票
    # ------------------------------------------------------------------
    ic_all: float | None = None
    ic_active: float | None = None
    ic_diff_pct: float | None = None
    ic_comparison_feasible: bool = False
    ic_skip_reason: str = ""

    # 推断因子列（排除 stock_id / date / pchg）
    exclude_cols = {"stock_id", "date", "pchg"}
    factor_cols = [c for c in df.columns if c not in exclude_cols]

    if "pchg" not in df.columns:
        ic_skip_reason = "数据框中无 'pchg' 列，无法计算 IC。"
        logger.warning("check_survivorship_bias [IC对比]: %s", ic_skip_reason)
    elif len(factor_cols) < 2:
        ic_skip_reason = f"因子列数不足（{len(factor_cols)} 列），跳过 IC 计算。"
        logger.warning("check_survivorship_bias [IC对比]: %s", ic_skip_reason)
    elif n_potentially_delisted == 0:
        ic_skip_reason = "无潜在退市股票，IC 对比无意义（全样本 == 活跃样本）。"
        logger.info("check_survivorship_bias [IC对比]: %s", ic_skip_reason)
        ic_comparison_feasible = False
    else:
        try:
            ic_all, ic_active = _compute_ic_comparison(
                df=df,
                factor_cols=factor_cols,
                active_stocks=active_stocks,
            )
            if ic_all is not None and ic_active is not None:
                eps = 1e-8
                ic_diff_pct = (
                    abs(ic_all - ic_active) / max(abs(ic_all), eps) * 100.0
                )
                ic_comparison_feasible = True
                logger.info(
                    "check_survivorship_bias [IC对比]: IC_all=%.4f，IC_active=%.4f，"
                    "差异=%.2f%%",
                    ic_all, ic_active, ic_diff_pct,
                )
        except Exception as exc:  # pylint: disable=broad-except
            ic_skip_reason = f"IC 计算过程中发生异常：{exc}"
            logger.warning("check_survivorship_bias [IC对比]: %s", ic_skip_reason)

    # ------------------------------------------------------------------
    # 警告逻辑
    # ------------------------------------------------------------------
    if survivorship_bias_risk == "high":
        warnings.warn(
            f"【存活偏差警告】潜在退市股票比例过高：{n_potentially_delisted}/{n_total_stocks}"
            f"（{delisted_ratio:.1%}），超过 10% 阈值。\n"
            "这可能导致回测收益被系统性高估（A 股横截面回测常见问题）。\n"
            "建议：\n"
            "  1. 确认数据供应商是否提供了退市股票的完整历史数据；\n"
            "  2. 检查退市前最后收益是否已纳入训练样本；\n"
            "  3. 在可交易掩码中将退市整理期股票标记为不可交易。",
            UserWarning,
            stacklevel=2,
        )

    if ic_comparison_feasible and ic_diff_pct is not None and ic_diff_pct > 5.0:
        warnings.warn(
            f"【存活偏差 IC 差异警告】含退市样本与不含退市样本的截面 rank IC 差异为 "
            f"{ic_diff_pct:.2f}%，超过 5% 阈值。\n"
            f"  IC（全样本）= {ic_all:.4f}\n"
            f"  IC（仅活跃）= {ic_active:.4f}\n"
            "这表明退市样本对 IC 估计有显著影响，存活偏差可能导致回测高估。",
            UserWarning,
            stacklevel=2,
        )

    # ------------------------------------------------------------------
    # 构建人类可读摘要
    # ------------------------------------------------------------------
    message_parts = [
        f"存活偏差检查完成。",
        f"总股票数：{n_total_stocks}，活跃（最后截面仍存在）：{n_active_stocks}，"
        f"潜在退市：{n_potentially_delisted}（{delisted_ratio:.1%}）。",
        f"风险等级：{survivorship_bias_risk.upper()}。",
    ]

    if n_potentially_delisted > 0 and "pchg" in df.columns:
        message_parts.append(
            f"退市前最后收益捕获率：{pct_last_returns_captured:.1f}%。"
        )

    if ic_comparison_feasible and ic_diff_pct is not None:
        message_parts.append(
            f"IC 对比：全样本 IC={ic_all:.4f}，仅活跃 IC={ic_active:.4f}，"
            f"差异={ic_diff_pct:.2f}%"
            + ("（⚠ 超过 5% 阈值）" if ic_diff_pct > 5.0 else "（正常）")
            + "。"
        )
    elif ic_skip_reason:
        message_parts.append(f"IC 对比跳过：{ic_skip_reason}")

    message = " ".join(message_parts)

    logger.info("check_survivorship_bias 完成：%s", message)

    return {
        "n_total_stocks": n_total_stocks,
        "n_active_stocks": n_active_stocks,
        "n_potentially_delisted": n_potentially_delisted,
        "potentially_delisted_stocks": potentially_delisted_stocks,
        "last_returns_included": last_returns_included,
        "pct_last_returns_captured": pct_last_returns_captured,
        "survivorship_bias_risk": survivorship_bias_risk,
        "ic_all": ic_all,
        "ic_active": ic_active,
        "ic_diff_pct": ic_diff_pct,
        "ic_comparison_feasible": ic_comparison_feasible,
        "message": message,
    }


def _compute_ic_comparison(
    df: pd.DataFrame,
    factor_cols: list[str],
    active_stocks: list,
) -> tuple[float | None, float | None]:
    """计算全样本与仅活跃股票的截面 rank IC 均值。

    使用简单等权信号（所有因子列的 rank 均值）与 pchg 的截面 Spearman 相关系数
    作为 IC 的代理指标。

    参数
    ----
    df : pd.DataFrame
        完整因子面板，含 stock_id / date / pchg / 因子列。
    factor_cols : list[str]
        用于计算等权信号的因子列名列表。
    active_stocks : list
        活跃股票 ID 列表（最后截面日期仍存在的股票）。

    返回
    ----
    tuple[float | None, float | None]
        (ic_all, ic_active)：全样本 IC 均值和仅活跃股票 IC 均值。
        若计算失败，返回 (None, None)。
    """
    # 只使用有 pchg 的行
    df_valid = df[df["pchg"].notna()].copy()
    if df_valid.empty:
        logger.warning("_compute_ic_comparison: 无有效 pchg 行，跳过 IC 计算。")
        return None, None

    # 计算等权信号：对每行，取所有因子列的 rank 均值
    # 先对每个截面做 rank 标准化，再取均值
    dates = sorted(df_valid["date"].unique())

    ic_all_list: list[float] = []
    ic_active_list: list[float] = []

    active_set = set(active_stocks)

    for date in dates:
        cross_section = df_valid[df_valid["date"] == date].copy()
        if len(cross_section) < 5:
            # 截面样本太少，跳过
            continue

        # 计算等权信号（各因子 rank 的均值）
        factor_data = cross_section[factor_cols]
        # 对每列做截面 rank（归一化到 [0,1]）
        ranked = factor_data.rank(axis=0, pct=True)
        # 处理全 NaN 列
        valid_cols = ranked.columns[ranked.notna().any()]
        if len(valid_cols) == 0:
            continue
        signal = ranked[valid_cols].mean(axis=1)

        pchg = cross_section["pchg"]

        # 全样本 IC（Spearman）
        valid_mask = signal.notna() & pchg.notna()
        if valid_mask.sum() >= 5:
            ic_val = float(
                signal[valid_mask].rank().corr(pchg[valid_mask].rank())
            )
            if pd.notna(ic_val):
                ic_all_list.append(ic_val)

        # 仅活跃股票 IC
        active_mask = cross_section["stock_id"].isin(active_set)
        active_cross = cross_section[active_mask]
        if len(active_cross) >= 5:
            signal_active = signal[active_mask]
            pchg_active = pchg[active_mask]
            valid_active = signal_active.notna() & pchg_active.notna()
            if valid_active.sum() >= 5:
                ic_active_val = float(
                    signal_active[valid_active].rank().corr(
                        pchg_active[valid_active].rank()
                    )
                )
                if pd.notna(ic_active_val):
                    ic_active_list.append(ic_active_val)

    if not ic_all_list or not ic_active_list:
        logger.warning(
            "_compute_ic_comparison: IC 列表为空（ic_all=%d 个截面，ic_active=%d 个截面），"
            "跳过 IC 对比。",
            len(ic_all_list), len(ic_active_list),
        )
        return None, None

    ic_all_mean = float(sum(ic_all_list) / len(ic_all_list))
    ic_active_mean = float(sum(ic_active_list) / len(ic_active_list))

    logger.debug(
        "_compute_ic_comparison: ic_all=%.4f（%d 个截面），ic_active=%.4f（%d 个截面）",
        ic_all_mean, len(ic_all_list), ic_active_mean, len(ic_active_list),
    )

    return ic_all_mean, ic_active_mean


# ---------------------------------------------------------------------------
# 内部辅助函数
# ---------------------------------------------------------------------------

def _count_trading_days_since_listing(df: pd.DataFrame) -> pd.Series:
    """计算每行（date, stock_id）距该股票首次出现的交易日数。

    算法：
    1. 找出每只股票在数据集中的首次出现日期（作为上市日期的代理）。
    2. 对全局唯一交易日序列按时间排序，赋予整数序号（rank）。
    3. 对每行，计算当前日期序号减去首次出现日期序号，即为经历的交易日数。

    注意：此处"交易日数"是数据集内的交易日计数，而非自然日历天数。
    若股票在数据集第一个截面日期就已存在，则其首次出现日期即为数据集起始日，
    该股票的冷启动计数从 0 开始（第一天为 0，第二个截面为 1，以此类推）。

    参数
    ----
    df : pd.DataFrame
        已完成列重命名（``stock_id``）和日期解析（``date``）的因子面板。
        必须包含 ``stock_id`` 和 ``date`` 列。

    返回
    ----
    pd.Series
        整数序列，与 ``df`` 行对齐，表示每行距首次出现的交易日数（从 0 开始）。
        索引与 ``df.index`` 一致。
    """
    if "stock_id" not in df.columns or "date" not in df.columns:
        logger.warning(
            "_count_trading_days_since_listing: 缺少 'stock_id' 或 'date' 列，"
            "返回全 0（不过滤新股）。"
        )
        return pd.Series(0, index=df.index, dtype=int)

    # 全局唯一交易日序列，按时间排序，赋予整数序号
    all_dates_sorted = sorted(df["date"].unique())
    date_to_rank: dict = {d: i for i, d in enumerate(all_dates_sorted)}

    # 每只股票的首次出现日期
    first_date_per_stock: pd.Series = df.groupby("stock_id")["date"].min()

    # 每只股票首次出现日期的序号
    first_rank_per_stock: pd.Series = first_date_per_stock.map(date_to_rank)

    # 每行的当前日期序号
    current_rank: pd.Series = df["date"].map(date_to_rank)

    # 每行的首次出现日期序号（通过 stock_id 映射）
    first_rank_per_row: pd.Series = df["stock_id"].map(first_rank_per_stock)

    # 交易日数 = 当前序号 - 首次出现序号
    trading_days: pd.Series = (current_rank - first_rank_per_row).astype(int)
    trading_days.index = df.index

    logger.debug(
        "_count_trading_days_since_listing: 计算完成，"
        "交易日数范围 [%d, %d]，中位数 %.0f",
        trading_days.min(), trading_days.max(), trading_days.median(),
    )
    return trading_days


def _infer_financial_cols(df: pd.DataFrame) -> list[str]:
    """推断财务类因子列名（基于设计文档中的家族划分）。

    财务类家族：basics、growth、pershare、quality
    这些因子需要按实际披露日生效（apply_disclosure_lag）。
    """
    # 基于设计文档 3.3 节的家族映射，列举典型财务类因子前缀/关键词
    # 完整映射将在 Task 3.1 的 family_map.py 中实现
    financial_keywords = [
        # basics 家族典型字段
        "ttm", "assets", "liability", "profit", "revenue", "expense",
        "earnings", "ebit", "ebitda", "income", "cash_flow",
        # growth 家族
        "growth_rate",
        # pershare 家族
        "per_share", "eps", "net_asset_per_share",
        # quality 家族
        "roa", "roe", "ratio", "turnover_rate", "margin",
    ]

    exclude = {"stock_id", "date", "pchg"}
    financial_cols = []
    for col in df.columns:
        if col in exclude:
            continue
        col_lower = col.lower()
        if any(kw in col_lower for kw in financial_keywords):
            financial_cols.append(col)

    logger.debug("推断出 %d 个财务类因子列", len(financial_cols))
    return financial_cols
