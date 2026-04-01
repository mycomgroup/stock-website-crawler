---
name: joinquant-notebook-strategy
description: 在 JoinQuant Notebook 中运行策略代码，无时间限制，可快速验证策略
---

# JoinQuant Notebook 策略运行器

**核心优势：无每日 180 分钟时间限制**

## 快速开始

```bash
# 1. 首次使用：抓取 session
node browser/capture-joinquant-session.js --notebook-url "YOUR_NOTEBOOK_URL" --headed

# 2. 运行策略
node run-strategy.js --strategy examples/rfscore_full_comparison.py

# 3. 查看结果
cat output/joinquant-notebook-result-*.json
```

## 三种使用方式

### 1. 运行策略文件

```bash
node run-strategy.js --strategy examples/test_mini.py
node run-strategy.js --strategy /path/to/your/strategy.py
```

### 2. 直接执行代码

```bash
node run-strategy.js --cell-source "from jqdata import *; print(get_trade_days('2024-01-01', '2024-01-10'))"
```

### 3. 重新执行 Notebook Cell

```bash
node run-strategy.js --cell-index last   # 执行最后一个 cell
node run-strategy.js --mode all          # 执行所有 cells
```

## 示例策略

| 文件 | 说明 | 运行时间 |
|------|------|---------|
| `examples/test_mini.py` | 最小化测试（涨停统计） | ~30秒 |
| `examples/rfscore_simple_test.py` | 单日选股测试 | ~1分钟 |
| `examples/rfscore_full_comparison.py` | 完整策略对比（51个月） | ~10分钟 |
| `examples/param_tuning.py` | 参数调优示例 | ~3分钟 |

## 参数说明

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
  --no-shutdown          禁用自动关闭 session（调试模式）
  --auto-shutdown <bool> 执行后自动关闭 session（默认 true）
```

**自动关闭 Session（新功能）**
- 默认执行完成后自动关闭 session，释放资源
- 使用 `--no-shutdown` 禁用自动关闭，便于调试查看运行状态
- 详情见 [AUTO_SHUTDOWN.md](AUTO_SHUTDOWN.md)

## 策略代码适配

### 策略编辑器 → Notebook

```python
# 策略编辑器格式
def initialize(context):
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    date = context.current_dt
    stocks = get_all_securities("stock", date)
```

```python
# Notebook 格式
date = "2024-03-20"  # 直接指定日期
stocks = get_all_securities("stock", date)
print(f"股票数: {len(stocks)}")  # 可以逐步执行查看结果
```

## 输出文件

```bash
output/
├── joinquant-notebook-TIMESTAMP.ipynb           # Notebook 快照
└── joinquant-notebook-result-TIMESTAMP.json     # 执行结果详情
```

## 常见问题

### Session 过期

```bash
node browser/capture-joinquant-session.js --notebook-url "YOUR_URL" --headed
```

### 执行超时

```bash
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000  # 5分钟
```

### Notebook 缓存旧代码

```bash
node run-strategy.js --strategy your_strategy.py --cell-marker "# REFRESH"
```

## 实际案例：策略对比

已成功运行 RFScore PB10 策略对比：

```bash
node run-strategy.js --strategy examples/rfscore_full_comparison.py --timeout-ms 600000
```

**结果**：
- 原始策略：累计收益 42.20%，夏普 0.49，胜率 52.9%
- 增强策略：累计收益 39.74%，夏普 0.60，胜率 54.9%
- **结论**：增强策略风险调整后收益更好 ✓

## 完整文档

- **详细指南**：[README.md](README.md)
- **快速参考**：[QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **API 文档**：[joinquant_doc/SKILL.md](joinquant_doc/SKILL.md)

## 相关资源

- 策略编辑器策略：`../joinquant_strategy/`
- 更多示例：`examples/`
- Session 管理：`browser/capture-joinquant-session.js`

## 对比：Notebook vs 策略编辑器

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| 时间限制 | **180分钟/天** | **无限制** ✓ |
| 数据 API | ✓ | ✓ |
| 因子 API | ✓ | ✓ |
| 回测框架 | 完整 | 需手动实现 |
| 交互调试 | ✗ | ✓ |
| 逐步执行 | ✗ | ✓ |
| 适用场景 | 精确回测 | 快速验证 |

**推荐流程**：
1. Notebook → 快速验证逻辑
2. Notebook → 参数调优
3. 策略编辑器 → 最终精确回测