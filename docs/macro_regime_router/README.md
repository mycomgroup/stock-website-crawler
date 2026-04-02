# 宏观 + 市场状态路由器 (Macro Regime Router)

## 概述

本文件夹包含宏观 + 市场状态路由器的完整研究资料，包括策略代码、验证报告、适用性分析和实测对比。

核心目标：不是做纯宏观研究，而是构建一个能指导"现在该偏哪类策略"的轻量状态机。

## 文件结构

### 策略代码 (可直接在聚宽Notebook运行)

| 文件 | 说明 | 来源 |
|------|------|------|
| `verify_08_regime_router.py` | 市场状态路由器验证代码 | 任务08原始验证 |
| `risk_premium_timing_strategy.py` | 风险溢价择时策略 | 聚宽notebook 33号 |
| `vol_turnover_bear_bull_strategy.py` | 波动率+换手率牛熊指标策略 | 聚宽notebook 63号 |

### 研究报告

| 文件 | 内容 |
|------|------|
| `11_macro_regime_router_validation.md` | 路由器初始验证报告 (2026-03-28实测) |
| `12_risk_premium_timing_analysis.md` | 风险溢价择时策略深度分析 |
| `13_strategy_applicability_summary.md` | 策略适用性总结 (何时有效、收益预期) |
| `14_regime_router_applicability_and_returns.md` | 路由器适用条件与收益潜力深度调研 |
| `15_two_timing_strategies_comparison.md` | 两大择时策略实测对比报告 |

## 核心结论

### 市场状态定义

| 状态 | 宽度 | 估值 | 趋势 | 对应策略 |
|------|------|------|------|---------|
| 底部试错 | <30% | 低估 | 向下/震荡 | RFScore7+PB20 小仓位, 高股息防守 |
| 趋势进攻 | >50% | 中性 | 向上 | ETF动量满仓, RFScore7满仓 |
| 震荡轮动 | 30-50% | 中性 | 震荡 | ETF轮动半仓, 行业增强 |
| 高估防守 | >70% | 高估 | 向上 | 降仓至30%, 债券/货基 |

### 当前市场状态 (2026-03-28)

- **路由器判断**: 底部试错
- **风险溢价策略**: 空仓 (信号趋势向下)
- **牛熊指标策略**: 上升初期，建议80-100%仓位
- **综合建议**: 60-80%仓位，结构性布局

### 策略实测表现

| 策略 | 年化收益 | 夏普比率 | 最大回撤 | 当前信号 |
|------|---------|---------|---------|---------|
| 风险溢价择时 | 4.17% | 0.66 | 25.30% | 空仓 |
| 牛熊指标 | - | -0.97相关性 | - | 强烈看多 |

## 如何使用

### 运行策略

```bash
# 确保 session.json 已配置
cd skills/joinquant_nookbook

# 运行风险溢价择时策略
python run_notebook.py --cell-source "$(cat docs/macro_regime_router/risk_premium_timing_strategy.py)"

# 运行波动率+换手率牛熊指标策略
python run_notebook.py --cell-source "$(cat docs/macro_regime_router/vol_turnover_bear_bull_strategy.py)"
```

### 参考资料

- 聚宽notebook 33号: 基于风险溢价的沪深300择时
- 聚宽notebook 63号: 波动率和换手率构建牛熊指标
- 聚宽notebook 97号: 大周期顶底判断：FED指标+格雷厄姆指数
- 聚宽notebook 45/52号: 市场宽度
- 聚宽notebook 93号: 国信投资者情绪指数择时模型
