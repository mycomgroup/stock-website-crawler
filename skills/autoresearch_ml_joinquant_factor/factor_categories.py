#!/usr/bin/env python
# coding: utf-8
"""
因子分类定义和分散度计算
"""

# 因子分类
FACTOR_CATEGORIES = {
    "basics": [
        "administration_expense_ttm",
        "asset_impairment_loss_ttm",
        "cash_flow_to_price_ratio",
        "circulating_market_cap",
        "EBIT",
        "EBITDA",
        "financial_assets",
        "financial_expense_ttm",
        "financial_liability",
        "goods_sale_and_service_render_cash_ttm",
        "gross_profit_ttm",
        "interest_carry_current_liability",
        "interest_free_current_liability",
        "market_cap",
        "net_debt",
        "net_finance_cash_flow_ttm",
        "net_interest_expense",
        "net_invest_cash_flow_ttm",
        "net_operate_cash_flow_ttm",
        "net_profit_ttm",
        "net_working_capital",
        "non_operating_net_profit_ttm",
        "non_recurring_gain_loss",
        "np_parent_company_owners_ttm",
        "OperateNetIncome",
        "operating_assets",
        "operating_cost_ttm",
        "operating_liability",
        "operating_profit_ttm",
        "operating_revenue_ttm",
        "retained_earnings",
        "sales_to_price_ratio",
        "sale_expense_ttm",
        "total_operating_cost_ttm",
        "total_operating_revenue_ttm",
        "total_profit_ttm",
        "value_change_profit_ttm",
    ],
    "emotion": [
        "AR",
        "ARBR",
        "ATR14",
        "ATR6",
        "BR",
        "DAVOL10",
        "DAVOL20",
        "DAVOL5",
        "MAWVAD",
        "money_flow_20",
        "PSY",
        "turnover_volatility",
        "TVMA20",
        "TVMA6",
        "TVSTD20",
        "TVSTD6",
        "VDEA",
        "VDIFF",
        "VEMA10",
        "VEMA12",
        "VEMA26",
        "VEMA5",
        "VMACD",
        "VOL10",
        "VOL120",
        "VOL20",
        "VOL240",
        "VOL5",
        "VOL60",
        "VOSC",
        "VR",
        "VROC12",
        "VROC6",
        "VSTD10",
        "VSTD20",
        "WVAD",
    ],
    "growth": [
        "financing_cash_growth_rate",
        "net_asset_growth_rate",
        "net_operate_cashflow_growth_rate",
        "net_profit_growth_rate",
        "np_parent_company_owners_growth_rate",
        "operating_revenue_growth_rate",
        "PEG",
        "total_asset_growth_rate",
        "total_profit_growth_rate",
    ],
    "momentum": [
        "arron_down_25",
        "arron_up_25",
        "BBIC",
        "bear_power",
        "BIAS10",
        "BIAS20",
        "BIAS5",
        "BIAS60",
        "bull_power",
        "CCI10",
        "CCI15",
        "CCI20",
        "CCI88",
        "CR20",
        "fifty_two_week_close_rank",
        "MASS",
        "PLRC12",
        "PLRC24",
        "PLRC6",
        "Price1M",
        "Price1Y",
        "Price3M",
        "Rank1M",
        "ROC12",
        "ROC120",
        "ROC20",
        "ROC6",
        "ROC60",
        "single_day_VPT",
        "single_day_VPT_12",
        "single_day_VPT_6",
        "TRIX10",
        "TRIX5",
        "Volume1M",
    ],
    "pershare": [
        "capital_reserve_fund_per_share",
        "cashflow_per_share_ttm",
        "cash_and_equivalents_per_share",
        "eps_ttm",
        "net_asset_per_share",
        "net_operate_cash_flow_per_share",
        "operating_profit_per_share",
        "operating_profit_per_share_ttm",
        "operating_revenue_per_share",
        "operating_revenue_per_share_ttm",
        "retained_earnings_per_share",
        "retained_profit_per_share",
        "surplus_reserve_fund_per_share",
        "total_operating_revenue_per_share",
        "total_operating_revenue_per_share_ttm",
    ],
    "quality": [
        "ACCA",
        "accounts_payable_turnover_days",
        "accounts_payable_turnover_rate",
        "account_receivable_turnover_days",
        "account_receivable_turnover_rate",
        "adjusted_profit_to_total_profit",
        "admin_expense_rate",
        "asset_turnover_ttm",
        "cash_rate_of_sales",
        "cash_to_current_liability",
        "cfo_to_ev",
        "current_asset_turnover_rate",
        "current_ratio",
        "debt_to_asset_ratio",
        "debt_to_equity_ratio",
        "debt_to_tangible_equity_ratio",
        "DEGM",
        "DEGM_8y",
        "DSRI",
        "equity_to_asset_ratio",
        "equity_to_fixed_asset_ratio",
        "equity_turnover_rate",
        "financial_expense_rate",
        "fixed_assets_turnover_rate",
        "fixed_asset_ratio",
        "GMI",
        "goods_service_cash_to_operating_revenue_ttm",
        "gross_income_ratio",
        "intangible_asset_ratio",
        "inventory_turnover_days",
        "inventory_turnover_rate",
        "invest_income_associates_to_total_profit",
        "long_debt_to_asset_ratio",
        "long_debt_to_working_capital_ratio",
        "long_term_debt_to_asset_ratio",
        "LVGI",
        "margin_stability",
        "maximum_margin",
        "MLEV",
        "net_non_operating_income_to_total_profit",
        "net_operate_cash_flow_to_asset",
        "net_operate_cash_flow_to_net_debt",
        "net_operate_cash_flow_to_operate_income",
        "net_operate_cash_flow_to_total_current_liability",
        "net_operate_cash_flow_to_total_liability",
        "net_operating_cash_flow_coverage",
        "net_profit_ratio",
        "net_profit_to_total_operate_revenue_ttm",
        "non_current_asset_ratio",
        "OperatingCycle",
        "operating_cost_to_operating_revenue_ratio",
        "operating_profit_growth_rate",
        "operating_profit_ratio",
        "operating_profit_to_operating_revenue",
        "operating_profit_to_total_profit",
        "operating_tax_to_operating_revenue_ratio_ttm",
        "profit_margin_ttm",
        "quick_ratio",
        "rnoa_ttm",
        "ROAEBITTTM",
        "roa_ttm",
        "roa_ttm_8y",
        "roe_ttm",
        "roe_ttm_8y",
        "roic_ttm",
        "sale_expense_to_operating_revenue",
        "SGAI",
        "SGI",
        "super_quick_ratio",
        "total_asset_turnover_rate",
        "total_profit_to_cost_ratio",
    ],
    "risk": [
        "Kurtosis120",
        "Kurtosis20",
        "Kurtosis60",
        "sharpe_ratio_120",
        "sharpe_ratio_20",
        "sharpe_ratio_60",
        "Skewness120",
        "Skewness20",
        "Skewness60",
        "Variance120",
        "Variance20",
        "Variance60",
    ],
    "style": [
        "average_share_turnover_annual",
        "average_share_turnover_quarterly",
        "beta",
        "book_leverage",
        "book_to_price_ratio",
        "cash_earnings_to_price_ratio",
        "cube_of_size",
        "cumulative_range",
        "daily_standard_deviation",
        "debt_to_assets",
        "earnings_growth",
        "earnings_to_price_ratio",
        "earnings_yield",
        "growth",
        "historical_sigma",
        "leverage",
        "liquidity",
        "long_term_predicted_earnings_growth",
        "market_leverage",
        "momentum",
        "natural_log_of_market_cap",
        "non_linear_size",
        "predicted_earnings_to_price_ratio",
        "raw_beta",
        "relative_strength",
        "residual_volatility",
        "sales_growth",
        "share_turnover_monthly",
        "short_term_predicted_earnings_growth",
        "size",
    ],
    "technical": [
        "boll_down",
        "boll_up",
        "EMA5",
        "EMAC10",
        "EMAC12",
        "EMAC120",
        "EMAC20",
        "EMAC26",
        "MAC10",
        "MAC120",
        "MAC20",
        "MAC5",
        "MAC60",
        "MACDC",
        "MFI14",
        "price_no_fq",
    ],
}

# 反向映射：因子 -> 类别
FACTOR_TO_CATEGORY = {}
for category, factors in FACTOR_CATEGORIES.items():
    for factor in factors:
        FACTOR_TO_CATEGORY[factor] = category


def get_factor_category(factor: str) -> str:
    """获取因子所属类别"""
    return FACTOR_TO_CATEGORY.get(factor, "unknown")


def calculate_diversity_score(factors: list) -> float:
    """
    计算因子组合的类别分散度得分

    返回 0-1 之间的分数：
    - 1.0: 所有因子来自不同类别（最大分散）
    - 0.0: 所有因子来自同一类别（无分散）

    计算方式：唯一类别数 / 因子数量
    """
    if len(factors) <= 1:
        return 1.0

    categories = [get_factor_category(f) for f in factors]
    unique_categories = len(set(categories))

    return unique_categories / len(factors)


def calculate_diversity_bonus(
    factors: list, base_score: float, weight: float = 0.1
) -> float:
    """
    计算分散度加分

    Args:
        factors: 因子组合
        base_score: 原始分数
        weight: 分散度权重（默认 0.1，即分散度最多贡献 10% 的加分）

    Returns:
        调整后的分数
    """
    diversity = calculate_diversity_score(factors)

    # 分散度加分：基础分数 * 权重 * 分散度
    bonus = base_score * weight * diversity

    return base_score + bonus, diversity
