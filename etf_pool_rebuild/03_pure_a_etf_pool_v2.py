# 纯 A 股完整 ETF 池定义 (v2.0)
# 包含宽基和行业，删除所有跨市场资产
# 生成时间: 2026-03-28

# ---- 旧池问题分析 ----
# 1. 跨市场资产混合: 纳指、标普、黄金、国债与 A 股标的混合
# 2. 择时信号混乱: 用沪深300宽度/RSRS判断跨市场ETF仓位逻辑不合理
# 3. 风险收益特征不匹配: 不同市场资产的波动特性差异巨大

# ---- 新池设计原则 ----
# 1. 纯 A 股资产: 只包含投资于 A 股市场的 ETF
# 2. 宽基 + 行业: 宽基提供市场暴露，行业提供超额收益机会
# 3. 流动性优先: 日均成交额 > 1亿，确保可交易性
# 4. 历史充足: 成立时间 > 2020年，确保回测可靠性
# 5. 低相关性: 不同 ETF 之间相关性 < 0.8，确保分散效果

# ---- 纯 A 宽基 ETF 池 (v2.0) ----
PURE_A_BROAD_POOL = {
    # 大盘蓝筹代表
    "沪深300ETF": "510300.XSHG",
    # 中盘成长代表
    "中证500ETF": "510500.XSHG",
    # 成长风格代表
    "创业板ETF": "159915.XSHE",
    # 科技创新代表
    "科创50ETF": "588000.XSHG",
    # 小盘代表
    "中证1000ETF": "512100.XSHG",
}

# ---- 纯 A 行业 ETF 池 (v2.0) ----
PURE_A_INDUSTRY_POOL = {
    # 医疗行业
    "医疗ETF": "512170.XSHG",
    # 消费行业
    "消费ETF": "159928.XSHE",
    # 新能源行业
    "新能源ETF": "516160.XSHG",
    # 半导体行业
    "半导体ETF": "512480.XSHG",
    # 军工行业
    "军工ETF": "512660.XSHG",
    # 金融行业 (银行)
    "银行ETF": "512800.XSHG",
    # 科技行业 (计算机)
    "计算机ETF": "512720.XSHG",
}

# ---- 完整池 (宽基 + 行业) ----
PURE_A_ETF_POOL_V2 = {**PURE_A_BROAD_POOL, **PURE_A_INDUSTRY_POOL}

# ---- 与旧池对比 ----
# 旧池 (v1.0) - 12只 ETF:
# 沪深300ETF, 中证500ETF, 创业板ETF, 科创50ETF, 中证1000ETF,
# 纳指ETF, 标普500ETF, 黄金ETF, 国债ETF, 医疗ETF, 消费ETF, 新能源ETF

# 新池 (v2.0) - 12只 ETF:
# 宽基5只: 沪深300ETF, 中证500ETF, 创业板ETF, 科创50ETF, 中证1000ETF
# 行业7只: 医疗ETF, 消费ETF, 新能源ETF, 半导体ETF, 军工ETF, 银行ETF, 计算机ETF

# 删除: 纳指ETF, 标普500ETF, 黄金ETF, 国债ETF (跨市场资产)
# 新增: 半导体ETF, 军工ETF, 银行ETF, 计算机ETF (A股行业)

# ---- 使用方法 ----
# 在聚宽环境中导入此文件
# 示例代码:
# from pure_a_etf_pool_v2 import PURE_A_ETF_POOL_V2, PURE_A_BROAD_POOL, PURE_A_INDUSTRY_POOL
#
# # 使用完整池
# codes = list(PURE_A_ETF_POOL_V2.values())
#
# # 只使用宽基
# broad_codes = list(PURE_A_BROAD_POOL.values())
#
# # 只使用行业
# industry_codes = list(PURE_A_INDUSTRY_POOL.values())
