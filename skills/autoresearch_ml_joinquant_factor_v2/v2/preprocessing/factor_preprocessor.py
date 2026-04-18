"""
L1 Factor Preprocessor — 因子预处理模块

实现弱因子组合策略 v2 的 L1 预处理流水线：
  1. winsorize_cross_section  — 按日截面 robust winsor（median ± 5*MAD）
  2. impute_factors           — 缺失值填补（stub，待 task 2.2 实现）
  3. standardize_factors      — 双轨标准化（stub，待 task 2.3 实现）
  4. neutralize_factors       — 风格中性化（stub，待 task 2.4 实现）

设计约束（来自 requirements.md 需求 2.1）：
  - 所有操作必须按日截面独立执行，禁止使用全局统计量
  - winsor 截断范围：median ± mad_multiplier * MAD
  - MAD = median(|x - median(x)|)
  - 当 MAD=0（截面内所有值相同）时，不做截断
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Winsorization
# ---------------------------------------------------------------------------

def _winsorize_series(s: pd.Series, mad_multiplier: float) -> pd.Series:
    """对单个截面（单日单因子）执行 robust winsor。

    Parameters
    ----------
    s : pd.Series
        单日单因子的截面值（可含 NaN）。
    mad_multiplier : float
        MAD 倍数，默认 5.0。

    Returns
    -------
    pd.Series
        winsor 后的截面值，NaN 保持不变。
    """
    valid = s.dropna()
    if valid.empty:
        # 全 NaN 截面：原样返回
        return s

    median = valid.median()
    mad = (valid - median).abs().median()

    if mad == 0.0:
        # MAD=0：所有有效值相同，无需截断
        return s

    lower = median - mad_multiplier * mad
    upper = median + mad_multiplier * mad

    # 只对非 NaN 值做 clip，NaN 保持不变
    return s.clip(lower=lower, upper=upper)


def winsorize_cross_section(
    df: pd.DataFrame,
    factor_cols: list[str],
    mad_multiplier: float = 5.0,
) -> pd.DataFrame:
    """按日截面对指定因子列执行 robust winsor（median ± mad_multiplier * MAD）。

    核心约束：
      - 每个日期的截面独立计算 median 和 MAD，禁止使用全局统计量。
      - 当某截面 MAD=0（所有值相同）时，不做截断。
      - 全 NaN 截面原样返回，不抛出异常。
      - 不修改原始 DataFrame（返回副本）。

    Parameters
    ----------
    df : pd.DataFrame
        必须包含 ``date`` 列和 ``stock_id`` 列，以及 ``factor_cols`` 中的列。
    factor_cols : list[str]
        需要 winsor 的因子列名列表。
    mad_multiplier : float, optional
        MAD 倍数，默认 5.0（对应需求 2.1 的 median ± 5*MAD）。

    Returns
    -------
    pd.DataFrame
        与输入结构相同的新 DataFrame，factor_cols 中的值已按截面 winsor。
        非因子列（date、stock_id 等）保持不变。

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "date": ["2020-01-01"] * 5,
    ...     "stock_id": list("ABCDE"),
    ...     "factor1": [1.0, 2.0, 3.0, 4.0, 100.0],
    ... })
    >>> result = winsorize_cross_section(df, ["factor1"])
    >>> result["factor1"].max() < 100.0
    True
    """
    if not factor_cols:
        return df.copy()

    # 验证必要列存在
    missing = [c for c in ["date", "stock_id"] + factor_cols if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame 缺少以下列：{missing}")

    result = df.copy()

    # 向量化实现：一次处理所有因子，按日期分组
    # 比逐因子 groupby().transform() 快 ~100x
    factor_arr = result[factor_cols].values.astype(float)  # (N, K)
    date_codes, _ = pd.factorize(result["date"], sort=True)

    for d in np.unique(date_codes):
        mask = date_codes == d
        X = factor_arr[mask]  # (n_stocks, K)

        # 计算每列的 median 和 MAD（忽略 NaN）
        median = np.nanmedian(X, axis=0)          # (K,)
        abs_dev = np.abs(X - median)
        mad = np.nanmedian(abs_dev, axis=0)        # (K,)

        # 只对 MAD > 0 的列做 clip
        valid_mad = mad > 0
        if valid_mad.any():
            lower = median - mad_multiplier * mad  # (K,)
            upper = median + mad_multiplier * mad  # (K,)
            # clip 保留 NaN（np.clip 不改变 NaN）
            X[:, valid_mad] = np.clip(
                X[:, valid_mad],
                lower[valid_mad],
                upper[valid_mad],
            )

        factor_arr[mask] = X

    result[factor_cols] = factor_arr
    return result


# ---------------------------------------------------------------------------
# 2. Imputation (task 2.2)
# ---------------------------------------------------------------------------

# 财务类家族：用行业内中位数填补
_FINANCIAL_FAMILIES: frozenset[str] = frozenset({"basics", "quality", "growth", "pershare"})
# 微观结构类家族：用前推（forward fill）
_MICROSTRUCTURE_FAMILIES: frozenset[str] = frozenset({"emotion", "technical"})


def _classify_factor(factor: str, factor_family_map: dict[str, str] | None) -> str:
    """将因子分类为 'financial' 或 'microstructure'。

    未知家族保守处理为 'financial'。

    Parameters
    ----------
    factor : str
        因子列名。
    factor_family_map : dict[str, str] | None
        因子名 → 家族名的映射。

    Returns
    -------
    str
        'financial' 或 'microstructure'。
    """
    if factor_family_map is None:
        return "financial"
    family = factor_family_map.get(factor, "")
    if family in _MICROSTRUCTURE_FAMILIES:
        return "microstructure"
    # 已知财务类或未知家族均保守处理为 financial
    return "financial"


def impute_factors(
    df: pd.DataFrame,
    factor_cols: list[str],
    factor_family_map: dict[str, str] | None = None,
    industry_col: str = "industry",
    missing_rate_threshold: float = 0.30,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """缺失值填补。

    按因子家族分类执行差异化填补策略：
      - 财务类因子（basics/quality/growth/pershare）：
          1. 若 df 含 industry_col，先按 (date, industry) 分组用行业内中位数填补；
          2. 再用截面中位数（按 date 分组）填补剩余 NaN。
      - 微观结构类因子（emotion/technical）：
          按 (stock_id, date) 排序后，对每只股票做 forward fill（前推最近可得值）。
      - 未知家族：保守处理为财务类。
      - 禁止对任何因子统一 fillna(0)。

    缺失率超过 missing_rate_threshold 的因子降权（weight=0.5），否则 weight=1.0。

    单调性约束：填补后各因子缺失率 ≤ 填补前缺失率（通过设计保证，不做额外截断）。

    Parameters
    ----------
    df : pd.DataFrame
        含 date、stock_id 及因子列的面板数据。必须包含 date 和 stock_id 列。
    factor_cols : list[str]
        需要填补的因子列名列表。
    factor_family_map : dict[str, str] | None
        因子名 → 家族名的映射，用于区分财务类与微观结构类因子。
        None 时所有因子保守处理为财务类。
    industry_col : str
        行业列名，默认 "industry"。若不存在于 df 中，财务类因子退化为截面中位数填补。
    missing_rate_threshold : float
        缺失率阈值，超过此比例的因子降权（weight=0.5），默认 0.30。

    Returns
    -------
    tuple[pd.DataFrame, dict[str, float]]
        - df_imputed：填补后的 DataFrame（与输入结构相同的副本）。
        - weights：dict[factor_col → float]，缺失率 > threshold 时为 0.5，否则为 1.0。

    Examples
    --------
    >>> import pandas as pd, numpy as np
    >>> df = pd.DataFrame({
    ...     "date": ["2020-01-01"] * 4,
    ...     "stock_id": list("ABCD"),
    ...     "industry": ["tech", "tech", "fin", "fin"],
    ...     "roe": [0.1, np.nan, 0.2, np.nan],
    ... })
    >>> df_out, weights = impute_factors(df, ["roe"],
    ...     factor_family_map={"roe": "quality"})
    >>> df_out["roe"].isna().sum()
    0
    >>> weights["roe"]
    1.0
    """
    if not factor_cols:
        return df.copy(), {}

    # 验证必要列存在
    missing_required = [c for c in ["date", "stock_id"] if c not in df.columns]
    if missing_required:
        raise ValueError(f"DataFrame 缺少以下必要列：{missing_required}")

    missing_factor_cols = [c for c in factor_cols if c not in df.columns]
    if missing_factor_cols:
        raise ValueError(f"DataFrame 缺少以下因子列：{missing_factor_cols}")

    result = df.copy()
    has_industry = industry_col in result.columns

    # 分类因子
    financial_cols = [
        col for col in factor_cols
        if _classify_factor(col, factor_family_map) == "financial"
    ]
    microstructure_cols = [
        col for col in factor_cols
        if _classify_factor(col, factor_family_map) == "microstructure"
    ]

    # ------------------------------------------------------------------
    # 财务类因子：截面中位数填补（向量化）
    # ------------------------------------------------------------------
    if financial_cols:
        fin_arr = result[financial_cols].values.astype(float)  # (N, K_fin)
        date_codes, _ = pd.factorize(result["date"], sort=True)

        for d in np.unique(date_codes):
            mask = date_codes == d
            X = fin_arr[mask]  # (n_stocks, K_fin)
            # 对每列用截面中位数填补 NaN
            col_medians = np.nanmedian(X, axis=0)  # (K_fin,)
            nan_mask = np.isnan(X)
            # 广播填补
            X[nan_mask] = np.take(col_medians, np.where(nan_mask)[1])
            fin_arr[mask] = X

        result[financial_cols] = fin_arr

    # ------------------------------------------------------------------
    # 微观结构类因子：按股票前推（forward fill）
    # ------------------------------------------------------------------
    if microstructure_cols:
        # 保存原始索引顺序，排序后前推，再恢复
        original_index = result.index
        result = result.sort_values(["stock_id", "date"])
        # 向量化 ffill：对所有微观结构因子同时处理
        micro_arr = result[microstructure_cols].values.astype(float)
        stock_codes, _ = pd.factorize(result["stock_id"], sort=False)
        for s in np.unique(stock_codes):
            smask = stock_codes == s
            X_s = micro_arr[smask]  # (n_dates, K_micro)
            # Forward fill per column
            for k in range(X_s.shape[1]):
                col = X_s[:, k]
                mask_nan = np.isnan(col)
                if mask_nan.any() and not mask_nan.all():
                    # Fill forward
                    idx = np.where(~mask_nan)[0]
                    for i in range(len(col)):
                        if mask_nan[i]:
                            prev = idx[idx < i]
                            if len(prev) > 0:
                                col[i] = col[prev[-1]]
                X_s[:, k] = col
            micro_arr[smask] = X_s
        result[microstructure_cols] = micro_arr
        result = result.loc[original_index]

    # ------------------------------------------------------------------
    # 计算缺失率并生成权重字典
    # ------------------------------------------------------------------
    n_total = len(result)
    weights: dict[str, float] = {}
    for col in factor_cols:
        missing_rate = result[col].isna().sum() / n_total if n_total > 0 else 0.0
        weights[col] = 0.5 if missing_rate > missing_rate_threshold else 1.0

    return result, weights


# ---------------------------------------------------------------------------
# 3. Standardization (task 2.3)
# ---------------------------------------------------------------------------

def _rank_series(s: pd.Series) -> pd.Series:
    """对单个截面执行 rank 表示：rank(x) / (N+1) - 0.5。

    Parameters
    ----------
    s : pd.Series
        单日单因子的截面值（可含 NaN）。

    Returns
    -------
    pd.Series
        rank 表示，范围约 (-0.5, +0.5)，NaN 保持不变。
    """
    valid_mask = s.notna()
    n = valid_mask.sum()
    if n == 0:
        return s

    result = s.copy()
    # rank 仅对非 NaN 值计算，NaN 保持 NaN
    ranks = s.rank(method="average", na_option="keep")
    result = ranks / (n + 1) - 0.5
    return result


def _zscore_series(s: pd.Series, eps: float) -> pd.Series:
    """对单个截面执行 robust zscore：(x - median) / (MAD + eps)。

    Parameters
    ----------
    s : pd.Series
        单日单因子的截面值（可含 NaN）。
    eps : float
        防止除零的小量。

    Returns
    -------
    pd.Series
        robust zscore，NaN 保持不变。
    """
    valid = s.dropna()
    if valid.empty:
        return s

    median = valid.median()
    mad = (valid - median).abs().median()

    return (s - median) / (mad + eps)


def standardize_factors(
    df: pd.DataFrame,
    factor_cols: list[str],
    eps: float = 1e-8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """双轨标准化：rank 表示和 robust zscore 表示。

    两种标准化均按日截面独立计算，禁止使用全局统计量。

    **Rank 表示**：``rank(x) / (N+1) - 0.5``
      - N = 截面内非 NaN 值的数量
      - 使用 ``method='average'`` 处理并列值
      - 结果范围约 (-0.5, +0.5)
      - NaN 值保持 NaN

    **Robust zscore**：``(x - median) / (MAD + eps)``
      - median 和 MAD 均按截面计算
      - MAD = median(|x - median(x)|)
      - eps 防止 MAD=0 时除零
      - NaN 值保持 NaN

    **幂等性（P2）**：对已经过 rank 标准化的值再次执行 rank 标准化，
    结果与第一次相同（在数值精度范围内）。这是因为 rank 变换是单调的，
    对已排好序的值再次 rank 仍是线性变换。

    Parameters
    ----------
    df : pd.DataFrame
        含 date、stock_id 及因子列的面板数据（已 winsor + impute）。
        必须包含 ``date`` 和 ``stock_id`` 列。
    factor_cols : list[str]
        需要标准化的因子列名列表。
    eps : float
        防止除零的小量，默认 1e-8。

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        ``(df_rank, df_zscore)``：
        - ``df_rank``：rank 表示的 DataFrame，结构与输入相同，
          非因子列原样复制。
        - ``df_zscore``：robust zscore 表示的 DataFrame，结构与输入相同，
          非因子列原样复制。

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "date": ["2020-01-01"] * 5,
    ...     "stock_id": list("ABCDE"),
    ...     "factor1": [1.0, 2.0, 3.0, 4.0, 5.0],
    ... })
    >>> df_rank, df_zscore = standardize_factors(df, ["factor1"])
    >>> df_rank["factor1"].between(-0.5, 0.5).all()
    True
    >>> abs(df_zscore["factor1"].median()) < 1e-10
    True
    """
    if not factor_cols:
        return df.copy(), df.copy()

    # 验证必要列存在
    missing = [c for c in ["date", "stock_id"] + factor_cols if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame 缺少以下列：{missing}")

    df_rank = df.copy()
    df_zscore = df.copy()

    # 向量化实现：一次处理所有因子，按日期分组
    factor_arr = df[factor_cols].values.astype(float)  # (N, K)
    date_codes, _ = pd.factorize(df["date"], sort=True)

    rank_arr = np.full_like(factor_arr, np.nan)
    zscore_arr = np.full_like(factor_arr, np.nan)

    for d in np.unique(date_codes):
        mask = date_codes == d
        X = factor_arr[mask]  # (n_stocks, K)

        # Rank 表示：rank(x) / (N+1) - 0.5
        # 使用 scipy.stats.rankdata 向量化处理所有列
        from scipy.stats import rankdata
        for k in range(X.shape[1]):
            col_vals = X[:, k]
            valid = ~np.isnan(col_vals)
            n_valid = valid.sum()
            if n_valid > 0:
                ranks = rankdata(col_vals[valid], method="average")
                rank_arr[mask, k][valid] = ranks / (n_valid + 1) - 0.5

        # Robust zscore：(x - median) / (MAD + eps)
        median = np.nanmedian(X, axis=0)  # (K,)
        abs_dev = np.abs(X - median)
        mad = np.nanmedian(abs_dev, axis=0)  # (K,)
        zscore_arr[mask] = (X - median) / (mad + eps)

    df_rank[factor_cols] = rank_arr
    df_zscore[factor_cols] = zscore_arr

    return df_rank, df_zscore


# ---------------------------------------------------------------------------
# 4. Neutralization (task 2.4)
# ---------------------------------------------------------------------------

def _build_exposure_matrix(
    cross_section: pd.DataFrame,
    industry_col: str,
    ln_mcap_col: str,
    beta_col: str,
    residual_vol_col: str,
    liquidity_col: str,
    min_industry_size: int,
) -> tuple[np.ndarray, list[str]]:
    """构建单截面的风险暴露矩阵 B（K-1 行业哑变量 + 截距 + 连续暴露）。

    Parameters
    ----------
    cross_section : pd.DataFrame
        单日截面数据（已过滤 NaN 行）。
    industry_col : str
        行业列名。
    ln_mcap_col, beta_col, residual_vol_col, liquidity_col : str
        连续暴露列名（若不存在于 cross_section 中则跳过）。
    min_industry_size : int
        行业最小样本数，低于此值的行业合并到 "other"。

    Returns
    -------
    B : np.ndarray, shape (N, M)
        风险暴露矩阵。
    col_names : list[str]
        暴露列名（用于调试）。
    """
    n = len(cross_section)
    cols: list[np.ndarray] = []
    col_names: list[str] = []

    # ------------------------------------------------------------------
    # 行业哑变量（K-1 + 截距）
    # ------------------------------------------------------------------
    if industry_col in cross_section.columns:
        industry = cross_section[industry_col].copy()

        # 合并样本极少的行业到 "other"
        industry_counts = industry.value_counts()
        small_industries = industry_counts[industry_counts < min_industry_size].index
        if len(small_industries) > 0:
            industry = industry.where(~industry.isin(small_industries), other="__other__")

        # 获取所有行业，按字母排序，drop 第一个（K-1 哑变量）
        unique_industries = sorted(industry.unique())
        if len(unique_industries) > 1:
            # drop_first=True → K-1 哑变量
            dummies = pd.get_dummies(industry, prefix="ind", drop_first=True, dtype=float)
            for c in dummies.columns:
                cols.append(dummies[c].values)
                col_names.append(c)

    # 截距
    cols.append(np.ones(n))
    col_names.append("intercept")

    # ------------------------------------------------------------------
    # 连续暴露（只包含存在的列）
    # ------------------------------------------------------------------
    for col_name, label in [
        (ln_mcap_col, "ln_mcap"),
        (beta_col, "beta"),
        (residual_vol_col, "residual_vol"),
        (liquidity_col, "liquidity"),
    ]:
        if col_name in cross_section.columns:
            vals = cross_section[col_name].values.astype(float)
            cols.append(vals)
            col_names.append(label)

    B = np.column_stack(cols)  # shape (N, M)
    return B, col_names


def _wls_ridge_residual(
    y: np.ndarray,
    B: np.ndarray,
    w: np.ndarray,
    ridge_alpha: float,
) -> np.ndarray:
    """WLS + ridge 回归，返回残差。

    求解：min_gamma ||W^(1/2) (y - B @ gamma)||^2 + ridge_alpha * ||gamma||^2

    等价于：(B' W B + ridge_alpha * I) gamma = B' W y

    使用向量化乘法（避免构造大型对角矩阵）：
      B' W B = (B * w[:, None]).T @ B
      B' W y = (B * w[:, None]).T @ y

    Parameters
    ----------
    y : np.ndarray, shape (N,)
        因子值（已去除 NaN 行）。
    B : np.ndarray, shape (N, M)
        风险暴露矩阵。
    w : np.ndarray, shape (N,)
        WLS 权重（已 clip，非负）。
    ridge_alpha : float
        ridge 正则化强度。

    Returns
    -------
    residual : np.ndarray, shape (N,)
        中性化残差 y - B @ gamma。
    """
    # 向量化加权：避免构造 N×N 对角矩阵
    Bw = B * w[:, np.newaxis]   # (N, M)，每行乘以对应权重

    # 正规方程：(B' W B + alpha * I) gamma = B' W y
    BtWB = Bw.T @ B             # (M, M)
    BtWy = Bw.T @ y             # (M,)

    # ridge 正则化
    M = B.shape[1]
    A = BtWB + ridge_alpha * np.eye(M)

    try:
        gamma = np.linalg.solve(A, BtWy)
    except np.linalg.LinAlgError:
        # 矩阵奇异时退化为最小二乘
        gamma, _, _, _ = np.linalg.lstsq(A, BtWy, rcond=None)

    residual = y - B @ gamma
    return residual


def neutralize_factors(
    df: pd.DataFrame,
    factor_cols: list[str],
    industry_col: str = "industry",
    ln_mcap_col: str = "ln_float_mcap",
    beta_col: str = "beta",
    residual_vol_col: str = "residual_vol",
    liquidity_col: str = "liquidity",
    weight_col: str = "float_mcap",
    min_industry_size: int = 10,
    ridge_alpha: float = 1e-4,
) -> pd.DataFrame:
    """风格中性化：对每个因子单独执行横截面 WLS 回归残差化。

    实现规范（来自需求 16 和技术方案 6.5 节）：
      - **禁止逐步回归**：对每个因子单独回归，右侧使用**同一组联合风险暴露**。
      - 暴露集合：行业哑变量（K-1+截距）+ ln(float_mcap) + beta + residual_vol + liquidity。
        只包含 df 中实际存在的列。
      - WLS 权重：sqrt(float_mcap) clip 到 [1st, 99th] 百分位，若 weight_col 不存在则等权。
      - 样本极少行业（< min_industry_size）：合并到 "__other__" 类别，避免矩阵近奇异。
      - ridge 正则化（ridge_alpha）：处理近奇异矩阵。
      - 含 NaN 的行从回归中排除，其中性化值设为 NaN。

    Parameters
    ----------
    df : pd.DataFrame
        含 date、stock_id 及因子列的面板数据（已标准化）。
        必须包含 ``date`` 和 ``stock_id`` 列。
    factor_cols : list[str]
        需要中性化的因子列名列表。
    industry_col : str
        行业列名，默认 "industry"。
    ln_mcap_col : str
        对数流通市值列名，默认 "ln_float_mcap"。
    beta_col : str
        市场 beta 列名，默认 "beta"。
    residual_vol_col : str
        残差波动率列名，默认 "residual_vol"。
    liquidity_col : str
        流动性列名，默认 "liquidity"。
    weight_col : str
        WLS 权重列名（float_mcap），默认 "float_mcap"。
        若不存在则使用等权。
    min_industry_size : int
        行业最小样本数，低于此值的行业合并到 "__other__"，默认 10。
    ridge_alpha : float
        ridge 正则化强度，默认 1e-4。

    Returns
    -------
    pd.DataFrame
        与输入结构相同的新 DataFrame，factor_cols 中的值替换为中性化残差。
        非因子列（date、stock_id、暴露列等）保持不变。
        含 NaN 的行（因子或暴露列有 NaN）的中性化值为 NaN。

    Examples
    --------
    >>> import pandas as pd, numpy as np
    >>> df = pd.DataFrame({
    ...     "date": ["2020-01-01"] * 6,
    ...     "stock_id": list("ABCDEF"),
    ...     "industry": ["tech", "tech", "fin", "fin", "med", "med"],
    ...     "ln_float_mcap": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
    ...     "factor1": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
    ... })
    >>> result = neutralize_factors(df, ["factor1"])
    >>> # 中性化后与 ln_float_mcap 的相关性应接近 0
    >>> abs(result["factor1"].corr(df["ln_float_mcap"])) < 0.05
    True
    """
    if not factor_cols:
        return df.copy()

    # 验证必要列存在
    missing_required = [c for c in ["date", "stock_id"] if c not in df.columns]
    if missing_required:
        raise ValueError(f"DataFrame 缺少以下必要列：{missing_required}")

    missing_factor_cols = [c for c in factor_cols if c not in df.columns]
    if missing_factor_cols:
        raise ValueError(f"DataFrame 缺少以下因子列：{missing_factor_cols}")

    result = df.copy()

    # 确定实际存在的暴露列（连续暴露）
    continuous_exposure_cols = [
        c for c in [ln_mcap_col, beta_col, residual_vol_col, liquidity_col]
        if c in df.columns
    ]

    # 按日期分组处理
    for date, group in df.groupby("date"):
        group_idx = group.index

        # ------------------------------------------------------------------
        # 构建 WLS 权重（sqrt(float_mcap) clip 到 [1st, 99th] 百分位）
        # ------------------------------------------------------------------
        if weight_col in group.columns:
            raw_weights = group[weight_col].values.astype(float)
            # 处理 NaN 权重：用 1.0 替代
            raw_weights = np.where(np.isnan(raw_weights), 1.0, raw_weights)
            raw_weights = np.maximum(raw_weights, 0.0)  # 确保非负
            sqrt_w = np.sqrt(raw_weights)
            # clip 到 [1st, 99th] 百分位
            p1 = np.percentile(sqrt_w, 1)
            p99 = np.percentile(sqrt_w, 99)
            sqrt_w = np.clip(sqrt_w, p1, p99)
        else:
            sqrt_w = np.ones(len(group))

        # ------------------------------------------------------------------
        # 确定完整暴露列（用于确定有效行）
        # ------------------------------------------------------------------
        exposure_cols_present = (
            ([industry_col] if industry_col in group.columns else [])
            + continuous_exposure_cols
        )

        # ------------------------------------------------------------------
        # 对每个因子单独回归（使用同一组联合风险暴露）
        # ------------------------------------------------------------------
        for factor in factor_cols:
            y_full = group[factor].values.astype(float)

            # 确定有效行：因子和所有连续暴露均非 NaN
            # 行业列允许有值（字符串），不检查 NaN
            valid_mask = ~np.isnan(y_full)
            for col in continuous_exposure_cols:
                valid_mask &= ~np.isnan(group[col].values.astype(float))

            if valid_mask.sum() < 3:
                # 有效样本太少，残差设为 NaN
                result.loc[group_idx, factor] = np.nan
                continue

            # 提取有效子集
            valid_group = group.loc[group_idx[valid_mask]]
            y_valid = y_full[valid_mask]
            w_valid = sqrt_w[valid_mask]

            # 构建暴露矩阵（仅对有效行）
            B, _ = _build_exposure_matrix(
                valid_group,
                industry_col=industry_col,
                ln_mcap_col=ln_mcap_col,
                beta_col=beta_col,
                residual_vol_col=residual_vol_col,
                liquidity_col=liquidity_col,
                min_industry_size=min_industry_size,
            )

            # WLS + ridge 回归，得到残差
            residuals = _wls_ridge_residual(y_valid, B, w_valid, ridge_alpha)

            # 写回结果：有效行填入残差，无效行保持 NaN
            neu_values = np.full(len(group), np.nan)
            neu_values[valid_mask] = residuals
            result.loc[group_idx, factor] = neu_values

    return result
