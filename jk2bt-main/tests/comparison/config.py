"""
tests/comparison/config.py
数据比较框架配置
"""

from typing import Dict, List

# =============================================================================
# 样本配置
# =============================================================================

# 测试股票样本 (15只代表性股票)
SAMPLE_STOCKS: List[str] = [
    # 大盘蓝筹
    "600519.XSHG",  # 贵州茅台
    "601318.XSHG",  # 中国平安
    "600036.XSHG",  # 招商银行
    # 中盘成长
    "000858.XSHE",  # 五粮液
    "000333.XSHE",  # 美的集团
    "002415.XSHE",  # 海康威视
    # 小盘股
    "300750.XSHE",  # 宁德时代
    "300059.XSHE",  # 东方财富
    "002230.XSHE",  # 科大讯飞
    # 金融
    "601398.XSHG",  # 工商银行
    "600030.XSHG",  # 中信证券
    # 周期
    "601899.XSHG",  # 紫金矿业
    "600028.XSHG",  # 中国石化
    # 科技
    "688981.XSHG",  # 中芯国际
    "688599.XSHG",  # 天合光能
]

# 测试指数样本
SAMPLE_INDEXES: List[str] = [
    "000300.XSHG",  # 沪深300
    "000905.XSHG",  # 中证500
    "000016.XSHG",  # 上证50
]

# =============================================================================
# 时间范围
# =============================================================================

START_DATE = "2023-01-01"
END_DATE = "2024-03-31"

# =============================================================================
# 比较配置
# =============================================================================

COMPARISON_CONFIG: Dict = {
    # 精度容忍度
    "tolerance": {
        "price": 0.01,       # 价格类: 1%
        "volume": 0.05,      # 成交量: 5%
        "ratio": 0.001,      # 比例类: 0.1%
        "factor": 0.01,      # 因子: 1%
        "money": 0.02,       # 金额: 2%
    },

    # 统计检验阈值
    "statistics": {
        "ks_test_pvalue": 0.05,      # KS检验p值阈值
        "correlation_threshold": 0.99, # 相关性阈值
        "missing_diff_threshold": 0.05, # 缺失值差异阈值
    },

    # 比较字段
    "compare_fields": {
        "price": ["open", "high", "low", "close", "volume", "money"],
        "valuation": ["pe_ratio", "pb_ratio", "market_cap", "circulating_market_cap", "turnover_ratio"],
        "balance": ["total_assets", "total_liability", "total_owner_equities"],
        "income": ["revenue", "operating_profit", "net_profit"],
        "cash_flow": ["net_operate_cash_flow", "net_invest_cash_flow", "net_finance_cash_flow"],
    },

    # 报告配置
    "report": {
        "output_dir": "./comparison_results",
        "save_raw_data": True,
        "max_diff_details": 100,  # 最大差异数量显示
    },
}

# =============================================================================
# 字段类型映射
# =============================================================================

FIELD_TYPE_MAP = {
    # 行情数据
    "open": "price",
    "high": "price",
    "low": "price",
    "close": "price",
    "volume": "volume",
    "money": "money",
    "amount": "money",

    # 估值因子
    "pe_ratio": "factor",
    "pb_ratio": "factor",
    "ps_ratio": "factor",
    "pcf_ratio": "factor",
    "market_cap": "factor",
    "circulating_market_cap": "factor",
    "turnover_ratio": "ratio",
    "capitalization": "factor",

    # 财务数据
    "revenue": "money",
    "operating_profit": "money",
    "net_profit": "money",
    "total_assets": "money",
    "total_liability": "money",
    "total_owner_equities": "money",
    "net_operate_cash_flow": "money",
    "net_invest_cash_flow": "money",
    "net_finance_cash_flow": "money",

    # 财务指标
    "roe": "ratio",
    "roa": "ratio",
    "gross_profit_margin": "ratio",
    "net_profit_margin": "ratio",
    "current_ratio": "ratio",
    "debt_to_assets": "ratio",
}

# =============================================================================
# 输出目录
# =============================================================================

import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUTPUT_DIR, exist_ok=True)