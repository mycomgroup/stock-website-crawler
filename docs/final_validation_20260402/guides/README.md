# 回测系统使用指南

本文档涵盖两种回测方式：
- **Notebook 回测**：无时间限制，快速验证策略逻辑
- **策略编辑器回测**：精确回测，自动计算风险指标

详细文档：
- `README.md`（本文档）- Notebook 回测系统指南
- `STRATEGY_EDITOR_GUIDE.md` - 策略编辑器回测系统指南 ⭐ 推荐
- `INDEX.md` - 完整文档索引

---

## 一、Notebook 回测系统

### 概述

Notebook 回测的核心优势是**无每日时间限制**，可以快速验证策略逻辑。

### 核心优势

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| **时间限制** | 180分钟/天 | **无限制** |
| 数据 API | 完整 | 完整 |
| 因子 API | 完整 | 完整 |
| 回测框架 | 自动 | 需手动实现 |
| 交互调试 | 不支持 | 支持 |
| 逐步执行 | 不支持 | 支持 |
| 适用场景 | 精确回测 | 快速验证 |

### 推荐流程

```
1. Notebook → 快速验证逻辑（无时间限制）
2. Notebook → 参数调优
3. 策略编辑器 → 最终精确回测
```

## 二、平台选择策略（重要）

### 策略开发完整流程

```
阶段1: 初步调研 → JoinQuant Notebook（探索性验证）
阶段2: 因子简单的新策略 → RiceQuant Notebook（快速开发）
阶段3: 相对完整的策略 → RiceQuant 策略编辑器（完整回测）
阶段4: 成熟策略最终验证 → JoinQuant Strategy（精确回测）
```

### 各阶段选择规则

| 阶段 | 场景特征 | 推荐平台 | Skill 目录 | 优势 |
|------|---------|---------|-----------|------|
| **阶段1：初步调研** | 探索新想法、快速验证概念 | JoinQuant Notebook | `skills/joinquant_notebook` | 无时间限制，可快速试错 |
| **阶段2：新策略开发** | 因子简单（基础财务因子）、新写策略 | **RiceQuant Notebook** | `skills/ricequant_strategy` | Session自动管理，减少迁移成本 |
| **阶段3：完整回测** | 策略逻辑较完整、需要风险指标 | **RiceQuant 策略编辑器** | `skills/ricequant_strategy` | 完整回测框架，自动计算指标 |
| **阶段4：最终验证** | 成熟策略、需要精确结果 | JoinQuant Strategy | `skills/joinquant_strategy` | 最权威平台，验证准确性 |

### 关键决策点

**何时用 RiceQuant？**
- ✅ 因子简单（只用 PE/PB/ROA/ROE/市值等基础因子）
- ✅ 新写的策略，减少迁移成本
- ✅ 策略逻辑相对完整，需要完整回测
- ✅ 希望Session自动管理，无需手动抓取

**何时用 JoinQuant？**
- ✅ 初步调研探索（Notebook）
- ✅ 因子复杂（使用 jqfactor 特殊因子）
- ✅ 成熟策略的最终验证（Strategy编辑器）
- ✅ 需要最权威的平台验证

### RiceQuant vs JoinQuant 对比

| 特性 | JoinQuant Notebook | RiceQuant Notebook | RiceQuant 策略编辑器 | JoinQuant Strategy |
|------|-------------------|-------------------|-------------------|-------------------|
| 时间限制 | 无限制 | 无限制 | 180分钟/天 | 180分钟/天 |
| Session 管理 | 需手动抓取 | **自动管理** | 自动管理 | 需手动抓取 |
| 因子库 | jqfactor（丰富） | fundamentals（有限） | fundamentals（有限） | jqfactor（丰富） |
| 回测框架 | 需手动实现 | 需手动实现 | **自动完整** | **自动完整** |
| 适用阶段 | **初步调研** | **新策略开发** | **完整回测** | **最终验证** |

**📖 更多因子信息**：
- **平台因子使用指南**：`ricequant_factors_guide.md` ⭐ NEW
- **因子列表速查**：`ricequant_factor_list.md`
- **Notebook 运行结果**：`ricequant_notebooks_list.md` ⭐ NEW

### 典型使用案例

**案例1：全新简单因子策略**
```
阶段1: JoinQuant Notebook（快速探索想法）
阶段2: RiceQuant Notebook（开发策略逻辑）
阶段3: RiceQuant 策略编辑器（完整回测看效果）
阶段4: JoinQuant Strategy（最终验证）
```

**案例2：复杂因子策略**
```
阶段1: JoinQuant Notebook（探索验证）
阶段2: JoinQuant Notebook（继续开发）
阶段3: JoinQuant Notebook（参数调优）
阶段4: JoinQuant Strategy（最终验证）
```

**案例3：迁移已有策略**
```
阶段1: RiceQuant Notebook（迁移适配测试）
阶段2: RiceQuant 策略编辑器（完整回测）
阶段3: JoinQuant Strategy（对比验证）
```

## 三、快速开始

### JoinQuant Notebook

```bash
# 目录位置
cd skills/joinquant_notebook

# 1. 首次使用：配置账号并抓取 session
# 编辑 .env 文件：
# JOINQUANT_USERNAME=你的手机号
# JOINQUANT_PASSWORD="你的密码"
# JOINQUANT_NOTEBOOK_URL=你的 notebook URL

node browser/capture-joinquant-session.js --headed

# 2. 运行策略
node run-strategy.js --strategy examples/test_mini.py

# 3. 查看结果
cat output/joinquant-notebook-result-*.json
```

### RiceQuant Notebook

```bash
# 目录位置
cd skills/ricequant_strategy

# 1. 配置账号（编辑 .env）
# RICEQUANT_USERNAME=你的账号
# RICEQUANT_PASSWORD=你的密码
# RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research

# 2. 运行策略（自动处理 session）
node run-strategy.js --strategy examples/simple_backtest.py

# 3. 查看结果
cat data/ricequant-notebook-result-*.json
```

## 四、策略代码适配

### 策略编辑器格式 → Notebook 格式

**策略编辑器格式：**
```python
def initialize(context):
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    date = context.current_dt
    stocks = get_all_securities("stock", date)
```

**Notebook 格式：**
```python
# 直接指定日期
date = "2024-03-20"

# 直接调用函数
stocks = get_all_securities("stock", date)
print(f"股票数: {len(stocks)}")

# 可以逐步执行，查看中间结果
```

### 关键差异

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| 入口函数 | `initialize(context)` | 直接执行 |
| 时间上下文 | `context.current_dt` | 手动指定日期字符串 |
| 定时任务 | `run_daily(func, time)` | 手动调用函数 |
| 回测框架 | 自动循环 | 手动编写循环 |
| 输出查看 | 日志面板 | 直接 print |

### RiceQuant Notebook 格式示例

```python
print("=== 策略测试 ===")

try:
    stocks = get_all_securities(["stock"])
    print(f"股票数: {len(stocks)}")
    
    result = calculate_signals(stocks)
    print(f"结果: {result}")
    
except Exception as e:
    print(f"错误: {e}")

print("=== 测试完成 ===")
```

## 五、API 差异对比

### 基础数据 API

| 功能 | JoinQuant | RiceQuant |
|------|-----------|-----------|
| 所有股票 | `get_all_securities("stock", date)` | `all_instruments("CS")` |
| 指数成分股 | `get_index_stocks("000300.XSHG", date)` | `index_components("000300.XSHG")` |
| 历史K线 | `get_price()` | `history_bars()` |
| 实时数据 | `get_current_data()` | `bar_dict` |
| 财务数据 | `get_fundamentals()` | `get_fundamentals()` |

### 因子 API

| 功能 | JoinQuant | RiceQuant |
|------|-----------|-----------|
| 估值因子 | `get_valuation()` | `get_factor(["pe_ratio", "pb_ratio"])` |
| 市值因子 | `valuation.code` | `fundamentals.eod_derivative_indicator.market_cap` |
| 财务指标 | `indicator.roa` | `fundamentals.financial_indicator.roa` |

### 不支持的功能（RiceQuant）

以下 JoinQuant 因子在 RiceQuant 中**需要手动计算**：
- ❌ `jqfactor.technical_analysis.*` - 技术分析因子
- ❌ `jqfactor.quality.*` - 质量因子
- ❌ `jqfactor.value.*` - 价值因子
- ❌ `jqfactor.momentum.*` - 动量因子
- ❌ `jqfactor.volatility.*` - 波动率因子

**替代方案示例：**
```python
def calc_momentum(stock, period=20):
    bars = history_bars(stock, period, "1d", "close")
    if bars is None or len(bars) < period:
        return None
    return (bars[-1] / bars[0] - 1) * 100

def calc_volatility(stock, period=20):
    bars = history_bars(stock, period, "1d", "close")
    if bars is None or len(bars) < period:
        return None
    returns = np.diff(bars) / bars[:-1]
    return np.std(returns) * np.sqrt(252)
```

## 六、参数说明

### JoinQuant 参数

```bash
node run-strategy.js [参数]

必需参数（二选一）：
  --strategy <path>      策略文件路径
  --cell-source <code>   直接执行的代码

可选参数：
  --notebook-url <url>   Notebook URL（默认从 .env 读取）
  --timeout-ms <ms>      超时时间（默认 60000ms）
  --cell-index <index>   执行指定 cell（0, last）
  --mode <mode>          all: 执行所有 cells
  --cell-marker <text>   替换包含标记的 cell
```

### RiceQuant 参数

```bash
node run-strategy.js [参数]

必需参数（二选一）：
  --strategy <path>             策略文件路径
  --cell-source <code>          直接执行的代码

可选参数：
  --notebook-url <url>          Notebook URL（默认从 .env 读取）
  --timeout-ms <ms>             超时时间（默认 60000ms）
  --cell-index <index>          执行指定 cell（0, last）
  --mode <mode>                 all: 执行所有 cells
  --create-new                  创建新的独立 notebook
  --cleanup                     运行后自动清理 notebook
  --notebook-base-name <name>   Notebook 名称（默认从策略注释提取）
```

## 七、常见问题

### Q1: Session 过期怎么办？

**JoinQuant：**
```bash
node browser/capture-joinquant-session.js --headed
```

**RiceQuant：** 自动处理，无需手动干预。如果需要强制重新登录：
```bash
node browser/capture-ricequant-notebook-session.js --headed
```

### Q2: 执行超时怎么办？

```bash
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000  # 5分钟
node run-strategy.js --strategy your_strategy.py --timeout-ms 600000  # 10分钟
```

### Q3: 如何调试策略？

```python
try:
    result = some_function()
    print(f"结果: {result}")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
```

### Q4: 策略类型区别？

| 策略类型 | 特征 | Notebook支持 | 示例 |
|---------|------|------------|------|
| **策略编辑器格式** | `init()` + `handle_bar()` | 无输出 | simple_test.py |
| **Notebook格式** | 直接执行代码 + `print()` | 完整输出 | mainline_exit_rules_rq.py |

**推荐使用 Notebook 格式策略。**

## 八、最佳实践

### 性能优化

```python
stocks = all_stocks[:500]  # 限制股票数量
df = get_price(stock, end_date=date, count=20)  # 限制天数
```

### 错误处理

```python
try:
    data = get_price(stock, end_date=date)
    if data.empty:
        print(f"{stock} 无数据")
except Exception as e:
    print(f"{stock} 获取失败: {e}")
```

### 参数调优

```python
params = [
    {"pb_threshold": 0.8, "roa_threshold": 0.05},
    {"pb_threshold": 1.0, "roa_threshold": 0.05},
]
for param in params:
    selected = filter_stocks(param)
    return_val = calculate_return(selected)
    print(f"PB < {param['pb_threshold']}: 收益 {return_val:.2f}%")
```

## 九、示例策略

### JoinQuant 示例

| 文件 | 说明 | 运行时间 |
|------|------|---------|
| `examples/test_mini.py` | 最小化测试（涨停统计） | ~30秒 |
| `examples/rfscore_simple_test.py` | 单日选股测试 | ~1分钟 |
| `examples/rfscore_full_comparison.py` | 完整策略对比（51个月） | ~10分钟 |

### RiceQuant 示例

| 文件 | 说明 | 运行时间 |
|------|------|---------|
| `examples/simple_backtest.py` | API 连接测试 | ~30秒 |
| `examples/ma_strategy_notebook.py` | 双均线策略验证 | ~1分钟 |
| `examples/rfscore_simple_notebook.py` | RFScore 选股测试 | ~2分钟 |

## 十、相关文档

### 本目录文档

- `STRATEGY_EDITOR_GUIDE.md` - 策略编辑器回测指南 ⭐ 推荐
- `QUICK_START.md` - 快速入门指南
- `API_DIFF.md` - API 详细差异对比
- `MIGRATION.md` - JoinQuant 到 RiceQuant 迁移指南
- `TEST_SUMMARY.md` - RiceQuant 测试总结报告
- `PROMPT.md` - Agent 运行测试提示词
- `INDEX.md` - 完整文档索引

### 重要迁移文档

- `joinquant_to_ricequant_migration_guide.md` - JoinQuant → RiceQuant 完整迁移指南
- `ricequant_factor_list.md` - RiceQuant 因子列表速查表
- `strategies/Ricequant/README.md` - RiceQuant API 对照表

### Skill 目录文档

**JoinQuant：**
- `skills/joinquant_notebook/README.md` - 详细使用指南
- `skills/joinquant_notebook/QUICK_REFERENCE.md` - 快速参考
- `skills/joinquant_notebook/joinquant_doc/` - API 文档库

**RiceQuant：**
- `skills/ricequant_strategy/README.md` - 详细使用指南
- `skills/ricequant_strategy/QUICK_REFERENCE.md` - 快速参考
- `skills/ricequant_strategy/SESSION_MANAGEMENT.md` - Session 管理

## 十一、总结

### 使用建议

| 场景 | 推荐 |
|------|------|
| **快速验证新策略** | JoinQuant Notebook |
| **因子简单的策略** | RiceQuant Notebook |
| **因子复杂的策略** | JoinQuant Notebook |
| **需要精确回测** | 策略编辑器 |

### 核心改进

- 默认使用无界面模式（headless）
- 每次运行自动创建新 notebook
- Notebook 不会自动删除，保留所有运行结果
- Session 出错自动重试
- 运行出错自动重用同一个 notebook

### 下一步

1. 查看 `examples/` 目录的示例
2. 运行最小测试验证环境
3. 编写自己的策略
4. 享受无时间限制的策略开发！