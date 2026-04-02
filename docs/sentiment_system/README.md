# 情绪指标与开关系统

> 统一的情绪指标计算、周期划分、开关判断模块，支持多平台（聚宽/RiceQuant）和实盘监控。

---

## 一、系统概述

### 1.1 什么是情绪系统

情绪系统是一套用于判断市场短线情绪状态的指标体系，核心目标是回答：

> **今天该不该做短线？**

通过量化涨停家数、连板高度、涨跌停比等指标，将模糊的"市场情绪"转化为可执行的"开仓/空仓"信号。

### 1.2 为什么需要情绪系统

| 问题 | 没有情绪系统 | 有情绪系统 |
|------|-------------|-----------|
| 首板低开 | 弱市亏损放大 | 过滤弱市，回撤改善40% |
| 弱转强 | 情绪退潮时高开低走 | 只在上升期做，胜率提升10% |
| 234板 | 几乎无法盈利 | 仅在高潮期做，可盈利 |
| 整体回撤 | 25%-30% | 15%以内 |

### 1.3 系统组成

```
sentiment_system/
├── code/                    # 代码
│   ├── core/                # 核心模块
│   │   ├── sentiment_indicators.py   # 指标计算
│   │   ├── sentiment_switch.py       # 开关判断
│   │   └── sentiment_phase.py        # 周期划分
│   ├── platforms/           # 平台适配
│   │   ├── joinquant_macro_sentiment.py  # 聚宽宏观情绪
│   │   └── ricequant_adapter.py      # RiceQuant适配
│   ├── examples/            # 使用示例
│   └── live/                # 实盘监控
└── docs/                    # 文档（当前目录）
```

---

## 二、快速开始

### 2.1 30秒上手

```python
# 在聚宽环境中
from sentiment_indicators import calc_market_sentiment
from sentiment_switch import sentiment_switch_combo

# 计算情绪指标
sentiment = calc_market_sentiment('2024-01-15', '2024-01-12')

# 判断是否开仓
if sentiment_switch_combo(sentiment):
    print("开仓！")
else:
    print("空仓观望")
```

### 2.2 最简使用

**只需记住一个规则**：

> 涨停家数 >= 30，开仓；否则空仓

```python
zt_count = get_zt_count(date)
if zt_count >= 30:
    # 开仓
    pass
```

### 2.3 推荐配置

| 策略 | 推荐阈值 | 说明 |
|------|----------|------|
| 首板低开 | 30 | 中等严格 |
| 弱转强 | 50 | 较严格 |
| 234板 | 50 | 严格 |
| 小市值防守 | 30 | 中等严格 |

---

## 三、文档索引

| 文档 | 内容 | 适用场景 |
|------|------|----------|
| [01_indicators.md](01_indicators.md) | 情绪指标定义与计算 | 了解指标含义 |
| [02_cycles.md](02_cycles.md) | 情绪周期划分 | 判断市场阶段 |
| [03_switch_rules.md](03_switch_rules.md) | 情绪开关方案 | 决定开仓/空仓 |
| [04_strategy_integration.md](04_strategy_integration.md) | 策略嫁接示例 | 接入自己的策略 |
| [05_backtest_results.md](05_backtest_results.md) | 实测效果汇总 | 验证有效性 |
| [06_usage_guide.md](06_usage_guide.md) | 每日盘前指南 | 实盘使用 |
| [07_ricequant_adapter.md](07_ricequant_adapter.md) | RiceQuant适配 | RiceQuant平台 |
| [08_live_trading_guide.md](08_live_trading_guide.md) | 实盘接口 | 实盘交易 |

---

## 四、代码索引

### 4.1 核心代码

| 文件 | 功能 | 主要函数 |
|------|------|----------|
| `code/core/sentiment_indicators.py` | 指标计算 | `calc_market_sentiment()` |
| `code/core/sentiment_switch.py` | 开关判断 | `sentiment_switch_combo()` |
| `code/core/sentiment_phase.py` | 周期划分 | `classify_sentiment_phase()` |

### 4.2 平台适配

| 文件 | 平台 | 使用方法 |
|------|------|----------|
| `code/platforms/joinquant_macro_sentiment.py` | 聚宽 | 宏观情绪指标 |
| `code/platforms/ricequant_adapter.py` | RiceQuant | API适配代码 |

### 4.3 示例代码

| 文件 | 内容 |
|------|------|
| `code/examples/sentiment_switch_test.py` | 开关测试 |
| `code/examples/threshold_search.py` | 阈值搜索 |
| `code/examples/sentiment_switch_backtest.py` | 回测示例 |
| `code/examples/sentiment_switch_baseline.py` | 基准策略 |
| `code/examples/sentiment_switch_hard.py` | 硬开关策略 |
| `code/examples/sentiment_switch_position.py` | 仓位调节 |

### 4.4 实盘代码

| 文件 | 功能 |
|------|------|
| `code/live/live_sentiment_monitor.py` | 实盘情绪监控 |

---

## 五、核心概念速查

### 5.1 情绪指标

| 指标 | 定义 | 数据来源 | 阈值参考 |
|------|------|----------|----------|
| 涨停家数 | 收盘价=涨停价的股票数 | T-1收盘 | >=30开仓 |
| 跌停家数 | 收盘价=跌停价的股票数 | T-1收盘 | - |
| 涨跌停比 | 涨停/跌停 | 计算 | >=1.5开仓 |
| 最高连板数 | 连续涨停最大天数 | T-1收盘 | >=2开仓 |
| 晋级率 | 前日涨停今日继续涨停比例 | 计算 | >=30% |

### 5.2 情绪周期

| 周期 | 特征 | 仓位建议 |
|------|------|----------|
| 启动期(up) | 连板3-4板，涨停30-60家 | 满仓 |
| 高潮期(high) | 连板5+板，涨停40+家 | 半仓(风险高) |
| 平稳期(normal) | 无明显方向 | 三成仓 |
| 退潮期(down) | 涨停<15，连板<=2 | 空仓 |

### 5.3 开关方案

**推荐方案：组合指标开关**

```python
def sentiment_switch_combo(sentiment):
    return (
        sentiment['max_lianban'] >= 2 and
        sentiment['zt_count'] >= 15 and
        sentiment['zt_dt_ratio'] >= 1.5
    )
```

---

## 六、实测效果

| 策略 | 无开关年化 | 有开关年化 | 回撤改善 | 胜率提升 |
|------|-----------|-----------|----------|----------|
| 首板低开 | ~28% | ~25% | -40% | +3% |
| 弱转强 | 30-60% | 25-50% | -60% | +10% |
| 234板 | 亏损 | 可盈利 | - | - |

详见：[05_backtest_results.md](05_backtest_results.md)

---

## 七、常见问题

**Q: 情绪指标什么时候计算？**

A: 使用T-1日收盘数据，在T日开盘前计算。例如周一开盘前用上周五的数据。

**Q: 涨停买不到怎么办？**

A: 情绪开关只判断环境，不直接选股。选股时避免追涨停。

**Q: 阈值怎么选择？**

A: 保守选50，平衡选30，激进选15。建议从30开始。

**Q: RiceQuant怎么用？**

A: 参考 [07_ricequant_adapter.md](07_ricequant_adapter.md)

---

## 八、更新日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-03-29 | v1.0 | 初始版本，整合所有情绪逻辑 |

---

## 九、参考来源

- 原始策略：`聚宽有价值策略558/07 连板龙头策略.txt`
- 研究报告：`docs/opportunity_strategies_20260329/result_05_consecutive_board_leader_sentiment.md`
- 指标研究：`docs/smallcap_state_router_20260330/result_07_sentiment_threshold_optimization.md`