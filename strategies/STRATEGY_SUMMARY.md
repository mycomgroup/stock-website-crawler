# 策略调研总结文档

## 概览

本目录包含历史调研的量化策略，主要针对A股市场的进攻与防守组合策略研究。

---

## 一、策略分类

### 1. RFScore 进攻策略 (`rfscore_offensive/`)

基于Piotroski F-Score改进的质量因子策略，核心逻辑：
- **RFScore因子**：7个财务指标信号（ROA、Delta ROA、OCFOA、Accrual、Delta Leveler、Delta Margin、Delta Turn）
- **选股范围**：沪深300 + 中证500，排除科创板
- **估值过滤**：PB分位数最低10%或20%
- **风控机制**：市场广度(Breadth) + 趋势(MA20) 双信号控制仓位

**主要文件**：
| 文件 | 描述 |
|------|------|
| `rfscore7_pb10_final_v2.py` | 最终版本，PB10%，月度调仓，20持仓，支持减仓/止损 |
| `rfscore7_pb10_final.py` | 正式版，PB10%，基础风控 |
| `rfscore7_pb10_release_v1.py` | 发布版v1 |
| `rfscore7_pb10_ths.py` | 同花顺版本 |
| `rfscore7_pb20_final.py` | PB20%版本 |
| `rfscore7_pb10_multi_signal_risk_control.py` | 多信号风控版 |
| `rfscore7_pb10_v1_monthly_15hold.py` | 月度调仓15持仓版 |
| `rfscore7_pb10_v1.1_weekly_10hold.py` | 周度调仓10持仓版 |
| `rfscore7_pb10_v1.2_weekly_12hold.py` | 周度调仓12持仓版 |
| `rfscore7_pb10_v1.3_monthly_10hold.py` | 月度调仓10持仓版 |
| `rfscore7_base_800.py` | 基准800股池版 |
| `rfscore_pure_offensive.py` | 纯进攻版（无防守层，对比基准）|
| `rfscore_defensive_dynamic_hedge.py` | 动态对冲组合版，含ETF防守层 |

---

### 2. 小市值防守策略 (`smallcap_defense/`)

低估值小盘股防守线，核心逻辑：
- **市值范围**：15-60亿（v2），10-100亿（优化后）
- **估值筛选**：PB < 1.5，PE < 20
- **动态仓位**：根据市场广度调整持仓数量（3-10只）
- **基准指数**：中证1000 (000852.XSHG)

**主要文件**：
| 文件 | 描述 |
|------|------|
| `smallcap_low_pb_defense.py` | 基础版本 |
| `smallcap_low_pb_defense_v2.py` | v2版本，优化市值区间 |
| `smallcap_low_pb_defense_v2_5hold.py` | 5持仓版 |
| `smallcap_low_pb_defense_v2_8hold.py` | 8持仓版 |
| `smallcap_low_pb_defense_v2_10hold.py` | 10持仓版 |
| `smallcap_low_pb_defense_v2_12hold.py` | 12持仓版 |
| `smallcap_defense_v2.py` | v2通用版 |
| `smallcap_defense_v3.py` | v3改进版 |
| `smallcap_quality_defense.py` | 质量因子防守版 |
| `smallcap_dividend_defense.py` | 分红防守版 |
| `smallcap_freeze_stop.py` | 冻结止损版 |
| `smallcap_reduce_position.py` | 减仓版 |
| `smallcap_state_filter_test.py` | 状态过滤测试 |
| `smallcap_normal_only.py` | 仅正常状态版 |
| `test_simple_smallcap.py` | 简化测试版 |

---

### 3. 组合策略 (`combo_strategies/`)

进攻层 + 防守层组合配置：

**主要文件**：
| 文件 | 描述 |
|------|------|
| `combo_rfscore_dividend_50_50.py` | RFScore + 分红小盘 50:50配置 |
| `combo_rfscore_dividend_60_40.py` | RFScore + 分红小盘 60:40配置 |
| `combo_rfscore_dividend_70_30.py` | RFScore + 分红小盘 70:30配置 |
| `combo_rfscore_dividend_dynamic.py` | 动态权重配置版 |
| `defense_offense_combo_dynamic.py` | 动态攻防组合版 |
| `defense_offense_combo_static.py` | 静态攻防组合版 |

---

### 4. 防守层研究 (`defense_research/`)

纯防守资产研究：

**主要文件**：
| 文件 | 描述 |
|------|------|
| `pure_cash_defense.py` | 纯现金防守（零风险基准）|
| `pure_treasury_defense.py` | 纯国债防守 |
| `rfscore_defensive_combined.py` | RFScore防守组合版 |

---

### 5. 参数调优研究 (`optimization_research/`)

参数优化与验证研究：

**主要文件**：
| 文件 | 描述 |
|------|------|
| `cap_range_optimization_research.py` | 市值区间优化调研 |
| `cap_range_verification.py` | 市值区间验证 |
| `hold_num_optimization_v2.py` | 持仓数量优化 |
| `research_fixed_income_market_regimes.py` | 固收市场状态研究 |

---

### 6. 情绪/短线策略 (`sentiment_shortline/`)

情绪驱动与短线策略：

**主要目录**：
| 目录 | 描述 |
|------|------|
| `mainline_first_board_sentiment/` | 主线首板情绪策略 |
| `second_board_research_20260402/` | 二板策略研究 |
| `secondboard_oos_system/` | 二板OOS系统 |
| `shadow_strategies_20260330/` | 影子策略 |
| `mainline_sim_trading_20260330/` | 主线模拟交易 |

---

### 7. 其他研究 (`misc_research/`)

其他策略与研究：

**主要文件/目录**：
| 文件/目录 | 描述 |
|------|------|
| `dividend_value_quality_v1/` | 分红价值质量策略v1 |
| `enhanced/` | 增强策略 |
| `enhanced_v2/` | 增强策略v2 |
| `quantsplaybook_validation/` | QuantsPlaybook验证 |
| `task02_state_calibration_verify/` | 状态校准验证 |
| `task08_emotion_timing_integration/` | 情绪时序整合 |
| `run_comparison.js` | 策略对比脚本 |
| `strategy_analyzer/` | 策略分析器 |

---

## 二、核心因子说明

### RFScore 因子（7信号）

| 信号 | 计算方式 | 含义 |
|------|----------|------|
| ROA | 资产收益率 | 盈利能力 |
| Delta ROA | ROA同比变化 | 盈利改善 |
| OCFOA | 经营现金流/总资产 | 现金流质量 |
| Accrual | OCFOA - ROA | 应计项目 |
| Delta Leveler | 杠杆率变化 | 杠杆改善 |
| Delta Margin | 毛利率变化 | 盈利能力改善 |
| Delta Turn | 资产周转率变化 | 运营效率改善 |

**评分规则**：每项信号 > 0 得1分，满分7分。RFScore=7为最高质量。

---

### 市场状态指标

| 指标 | 计算方式 | 用途 |
|------|----------|------|
| Breadth | HS300成分股站上MA20的比例 | 市场广度 |
| Trend | 沪深300收盘价 > MA20 | 趋势状态 |
| Sentiment | 涨跌停数量计算的情绪分数 | 情绪状态 |
| North Flow | 北向资金净流入 | 资金流向 |

---

## 三、风控逻辑

### 仓位控制（基于Breadth + Trend）

| 市场状态 | 条件 | 仓位 |
|----------|------|------|
| 止损 | Breadth < 15% + 趋势OFF | 0%（清仓）|
| 减仓 | Breadth < 25% + 趋势OFF | 50%（减半）|
| 正常 | 其他 | 100%（满仓）|

### 动态防守层配置

| 防守资产 | 配置比例 | 用途 |
|----------|----------|------|
| 国债ETF (511010) | 65-80% | 主防守 |
| 黄金ETF (518880) | 8-15% | 抗通胀 |
| 红利ETF (510880) | 8-10% | 股息防守 |
| 美股ETF (513100) | 4-10% | 分散风险 |

---

## 四、回测周期

大部分策略回测周期：**2022-01-01 至 2025-03-30**（约3年OOS期）

部分长周期策略：**2018-01-01 至今**

---

## 五、关键参数汇总

| 参数 | 常用值 | 说明 |
|------|--------|------|
| 基准持仓数 | 20只 | 正常状态持仓 |
| 减仓持仓数 | 10只 | 风险状态持仓 |
| IPO过滤天数 | 180天 | 新股过滤 |
| PB分位数 | 10%或20% | 估值筛选 |
| 调仓周期 | 月度（每月首日）| 主流配置 |
| 交易成本 | 买入0.03%，卖出0.13%| 含印花税 |

---

## 六、文件迁移说明

策略文件已按上述分类移入对应文件夹，便于管理与查阅。