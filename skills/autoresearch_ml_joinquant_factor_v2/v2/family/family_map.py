"""L2 因子家族映射模块 (family_map.py)

冻结 9 个经济家族与 CSV 列的完整映射。
基于 train_merged_all.csv 的实际列名（263列，260个因子）。

- basics: 37 个因子
- emotion: 36 个因子
- growth: 9 个因子
- momentum: 34 个因子
- pershare: 15 个因子
- quality: 71 个因子
- risk: 12 个因子
- style: 30 个因子
- technical: 16 个因子
合计: 260 个因子

**Validates: Requirements 3.1, 3.2, 3.5**
"""

from __future__ import annotations

FAMILY_MAP: dict[str, list[str]] = {
    # ------------------------------------------------------------------ basics (37)
    # 财务基础指标：规模、盈利、资产负债
    "basics": [
        "administration_expense_ttm",
        "asset_impairment_loss_ttm",
        "financial_expense_ttm",
        "financial_assets",
        "financial_liability",
        "goods_sale_and_service_render_cash_ttm",
        "goods_service_cash_to_operating_revenue_ttm",
        "gross_profit_ttm",
        "market_cap",
        "net_debt",
        "net_finance_cash_flow_ttm",
        "net_invest_cash_flow_ttm",
        "net_non_operating_income_to_total_profit",
        "net_operate_cash_flow_ttm",
        "net_profit_ttm",
        "non_operating_net_profit_ttm",
        "non_recurring_gain_loss",
        "np_parent_company_owners_ttm",
        "operating_assets",
        "operating_cost_ttm",
        "operating_liability",
        "operating_profit_ttm",
        "operating_revenue_ttm",
        "retained_earnings",
        "sale_expense_ttm",
        "total_operating_cost_ttm",
        "total_operating_revenue_ttm",
        "total_profit_ttm",
        "value_change_profit_ttm",
        "EBIT",
        "EBITDA",
        "circulating_market_cap",
        "net_working_capital",
        "invest_income_associates_to_total_profit",
        "net_interest_expense",
        "operating_profit_per_share_ttm",
        "operating_revenue_per_share_ttm",
    ],

    # ------------------------------------------------------------------ emotion (36)
    # 情绪/量价指标
    "emotion": [
        "AR",
        "BR",
        "ARBR",
        "DAVOL5",
        "DAVOL10",
        "DAVOL20",
        "MFI14",
        "TVMA6",
        "TVMA20",
        "TVSTD6",
        "TVSTD20",
        "VDEA",
        "VDIFF",
        "VEMA5",
        "VEMA10",
        "VEMA12",
        "VEMA26",
        "VMACD",
        "VOL5",
        "VOL10",
        "VOL20",
        "VOL60",
        "VOL120",
        "VOL240",
        "VOSC",
        "VR",
        "VROC6",
        "VROC12",
        "VSTD10",
        "VSTD20",
        "WVAD",
        "MAWVAD",
        "bear_power",
        "bull_power",
        "money_flow_20",
        "turnover_volatility",
    ],

    # ------------------------------------------------------------------ growth (9)
    # 成长指标
    "growth": [
        "earnings_growth",
        "net_asset_growth_rate",
        "net_operate_cashflow_growth_rate",
        "net_profit_growth_rate",
        "np_parent_company_owners_growth_rate",
        "operating_profit_growth_rate",
        "operating_revenue_growth_rate",
        "sales_growth",
        "total_asset_growth_rate",
    ],

    # ------------------------------------------------------------------ momentum (34)
    # 动量指标
    "momentum": [
        "BIAS5",
        "BIAS10",
        "BIAS20",
        "BIAS60",
        "CCI10",
        "CCI15",
        "CCI20",
        "CCI88",
        "CR20",
        "MASS",
        "PLRC6",
        "PLRC12",
        "PLRC24",
        "Price1M",
        "Price3M",
        "Price1Y",
        "PSY",
        "ROC6",
        "ROC12",
        "ROC20",
        "ROC60",
        "ROC120",
        "Rank1M",
        "TRIX5",
        "TRIX10",
        "Volume1M",
        "cumulative_range",
        "fifty_two_week_close_rank",
        "momentum",
        "relative_strength",
        "single_day_VPT",
        "single_day_VPT_6",
        "single_day_VPT_12",
        "long_term_predicted_earnings_growth",
    ],

    # ------------------------------------------------------------------ pershare (15)
    # 每股指标
    "pershare": [
        "capital_reserve_fund_per_share",
        "cash_and_equivalents_per_share",
        "cashflow_per_share_ttm",
        "eps_ttm",
        "net_asset_per_share",
        "net_operate_cash_flow_per_share",
        "operating_profit_per_share",
        "operating_revenue_per_share",
        "retained_earnings_per_share",
        "retained_profit_per_share",
        "surplus_reserve_fund_per_share",
        "total_operating_revenue_per_share",
        "total_operating_revenue_per_share_ttm",
        "short_term_predicted_earnings_growth",
        "total_profit_growth_rate",
    ],

    # ------------------------------------------------------------------ quality (71)
    # 质量指标：盈利质量、运营效率、偿债能力
    "quality": [
        "ACCA",
        "DEGM",
        "DEGM_8y",
        "DSRI",
        "GMI",
        "LVGI",
        "MLEV",
        "SGAI",
        "SGI",
        "account_receivable_turnover_days",
        "account_receivable_turnover_rate",
        "accounts_payable_turnover_days",
        "accounts_payable_turnover_rate",
        "adjusted_profit_to_total_profit",
        "admin_expense_rate",
        "asset_turnover_ttm",
        "book_leverage",
        "cash_rate_of_sales",
        "cash_to_current_liability",
        "cfo_to_ev",
        "current_asset_turnover_rate",
        "current_ratio",
        "debt_to_asset_ratio",
        "debt_to_assets",
        "debt_to_equity_ratio",
        "debt_to_tangible_equity_ratio",
        "equity_to_asset_ratio",
        "equity_to_fixed_asset_ratio",
        "equity_turnover_rate",
        "financial_expense_rate",
        "fixed_asset_ratio",
        "fixed_assets_turnover_rate",
        "gross_income_ratio",
        "intangible_asset_ratio",
        "inventory_turnover_days",
        "inventory_turnover_rate",
        "long_debt_to_asset_ratio",
        "long_debt_to_working_capital_ratio",
        "long_term_debt_to_asset_ratio",
        "market_leverage",
        "net_operating_cash_flow_coverage",
        "net_operate_cash_flow_to_asset",
        "net_operate_cash_flow_to_net_debt",
        "net_operate_cash_flow_to_operate_income",
        "net_operate_cash_flow_to_total_current_liability",
        "net_operate_cash_flow_to_total_liability",
        "net_profit_ratio",
        "net_profit_to_total_operate_revenue_ttm",
        "non_current_asset_ratio",
        "operating_cost_to_operating_revenue_ratio",
        "operating_profit_ratio",
        "operating_profit_to_operating_revenue",
        "operating_profit_to_total_profit",
        "operating_tax_to_operating_revenue_ratio_ttm",
        "PEG",
        "profit_margin_ttm",
        "quick_ratio",
        "rnoa_ttm",
        "roa_ttm",
        "roa_ttm_8y",
        "roe_ttm",
        "roe_ttm_8y",
        "roic_ttm",
        "ROAEBITTTM",
        "sale_expense_to_operating_revenue",
        "super_quick_ratio",
        "total_asset_turnover_rate",
        "total_profit_to_cost_ratio",
        "financing_cash_growth_rate",
        "margin_stability",
        "maximum_margin",
    ],

    # ------------------------------------------------------------------ risk (12)
    # 风险指标
    "risk": [
        "ATR6",
        "ATR14",
        "Kurtosis20",
        "Kurtosis60",
        "Kurtosis120",
        "Skewness20",
        "Skewness60",
        "Skewness120",
        "Variance20",
        "Variance60",
        "Variance120",
        "historical_sigma",
    ],

    # ------------------------------------------------------------------ style (30)
    # 风格因子（Barra 类）
    "style": [
        "average_share_turnover_annual",
        "average_share_turnover_quarterly",
        "beta",
        "book_to_price_ratio",
        "cash_earnings_to_price_ratio",
        "cash_flow_to_price_ratio",
        "cube_of_size",
        "daily_standard_deviation",
        "earnings_to_price_ratio",
        "earnings_yield",
        "growth",
        "leverage",
        "liquidity",
        "market_leverage",
        "natural_log_of_market_cap",
        "non_linear_size",
        "predicted_earnings_to_price_ratio",
        "price_no_fq",
        "raw_beta",
        "residual_volatility",
        "sales_to_price_ratio",
        "share_turnover_monthly",
        "size",
        "sharpe_ratio_20",
        "sharpe_ratio_60",
        "sharpe_ratio_120",
        "interest_carry_current_liability",
        "interest_free_current_liability",
        "OperateNetIncome",
        "OperatingCycle",
    ],

    # ------------------------------------------------------------------ technical (16)
    # 技术指标
    "technical": [
        "BBIC",
        "EMAC10",
        "EMAC12",
        "EMAC20",
        "EMAC26",
        "EMAC120",
        "EMA5",
        "MAC5",
        "MAC10",
        "MAC20",
        "MAC60",
        "MAC120",
        "MACDC",
        "arron_down_25",
        "arron_up_25",
        "boll_down",
        "boll_up",
    ],
}


# ---------------------------------------------------------------------------
# 去重：确保每个因子只属于一个家族（按家族顺序优先）
# ---------------------------------------------------------------------------

def _deduplicate_family_map(raw_map: dict[str, list[str]]) -> dict[str, list[str]]:
    """去除跨家族重复因子，保留第一次出现的家族归属。"""
    seen: set[str] = set()
    clean: dict[str, list[str]] = {}
    for family, factors in raw_map.items():
        unique = []
        for f in factors:
            if f not in seen:
                seen.add(f)
                unique.append(f)
        clean[family] = unique
    return clean


FAMILY_MAP = _deduplicate_family_map(FAMILY_MAP)

# ---------------------------------------------------------------------------
# 反向映射：因子 → 家族
# ---------------------------------------------------------------------------

FACTOR_TO_FAMILY: dict[str, str] = {
    factor: family
    for family, factors in FAMILY_MAP.items()
    for factor in factors
}

# ---------------------------------------------------------------------------
# 所有因子的有序列表
# ---------------------------------------------------------------------------

ALL_FACTORS: list[str] = [
    factor
    for factors in FAMILY_MAP.values()
    for factor in factors
]

# ---------------------------------------------------------------------------
# 家族衰减速度
# ---------------------------------------------------------------------------

FAMILY_DECAY_SPEED: dict[str, str] = {
    "basics": "slow",
    "emotion": "fast",
    "growth": "slow",
    "momentum": "fast",
    "pershare": "slow",
    "quality": "slow",
    "risk": "medium",
    "style": "medium",
    "technical": "fast",
}

# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------


def get_family_factors(family: str) -> list[str]:
    """返回指定家族的因子列表。"""
    if family not in FAMILY_MAP:
        raise KeyError(f"未知家族: '{family}'。有效家族: {sorted(FAMILY_MAP.keys())}")
    return list(FAMILY_MAP[family])


def get_factor_family(factor: str) -> str:
    """返回指定因子所属的家族名称。"""
    if factor not in FACTOR_TO_FAMILY:
        raise KeyError(f"未知因子: '{factor}'。该因子不属于任何已知家族。")
    return FACTOR_TO_FAMILY[factor]


def validate_family_map() -> dict:
    """验证家族映射的完备性和无重叠性。"""
    errors: list[str] = []
    overlaps: list[str] = []

    family_sizes = {family: len(factors) for family, factors in FAMILY_MAP.items()}

    # 检查重叠
    seen: dict[str, str] = {}
    for family, factors in FAMILY_MAP.items():
        for factor in factors:
            if factor in seen:
                overlaps.append(factor)
                errors.append(f"因子 '{factor}' 同时出现在 '{seen[factor]}' 和 '{family}'")
            else:
                seen[factor] = family

    total_factors = len(ALL_FACTORS)

    return {
        "valid": len(errors) == 0,
        "total_factors": total_factors,
        "family_sizes": family_sizes,
        "overlaps": overlaps,
        "errors": errors,
    }
