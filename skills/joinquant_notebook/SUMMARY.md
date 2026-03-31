# JoinQuant Notebook 策略运行系统 - 完成总结

## 已完成的功能

### 1. 核心文件

```
skills/joinquant_notebook/
├── SKILL.md                              # 技能主文档
├── README.md                             # 详细使用指南
├── QUICK_REFERENCE.md                    # 快速参考卡片
├── run-strategy.js                       # 策略运行脚本 ⭐
├── strategy_adapter.py                   # 策略适配器
├── run_examples.sh                       # 示例运行脚本
├── examples/
│   ├── test_mini.py                      # 最小化测试
│   ├── rfscore_simple_test.py            # 单日选股测试
│   ├── rfscore_full_comparison.py        # 完整策略对比 ⭐
│   └── strategy_runner_demo.py           # 使用演示
└── output/                               # 输出目录
```

### 2. 运行方式

#### 方式1：运行策略文件
```bash
node run-strategy.js --strategy examples/rfscore_full_comparison.py
```

#### 方式2：直接执行代码
```bash
node run-strategy.js --cell-source "print('hello')"
```

#### 方式3：重新执行 Cell
```bash
node run-strategy.js --cell-index last
node run-strategy.js --mode all
```

### 3. 实际运行案例

**RFScore PB10 策略对比**：

```bash
node run-strategy.js --strategy examples/rfscore_full_comparison.py --timeout-ms 600000
```

**结果**：
- 测试期间：2021-01-01 至 2025-03-28（51个月）
- 原始策略：累计收益 42.20%，夏普 0.49，胜率 52.9%
- 增强策略：累计收益 39.74%，夏普 0.60，胜率 54.9%
- 结论：增强策略风险调整后收益更好 ✓

### 4. 关键特性

| 特性 | 说明 |
|------|------|
| **无时间限制** | 策略编辑器限制 180分钟/天，Notebook 无限制 |
| **代码复用** | 可以直接复用策略编辑器的代码逻辑 |
| **交互调试** | 可以逐步执行，查看中间结果 |
| **快速验证** | 适合快速验证选股逻辑和参数调优 |

## 使用流程

### 首次使用

```bash
# 1. 进入目录
cd skills/joinquant_notebook

# 2. 安装依赖
npm install

# 3. 抓取 session
node browser/capture-joinquant-session.js \
    --notebook-url "YOUR_NOTEBOOK_URL" \
    --headed
```

### 日常使用

```bash
# 运行策略
node run-strategy.js --strategy your_strategy.py

# 查看结果
cat output/joinquant-notebook-result-*.json
```

## 策略代码转换

### 策略编辑器格式

```python
def initialize(context):
    set_option("use_real_price", True)
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    date = context.current_dt
    stocks = get_all_securities("stock", date)
    g.stocks = stocks.tolist()
```

### Notebook 格式

```python
from jqdata import *

date = "2024-03-20"  # 直接指定日期

# 直接调用选股逻辑
stocks = get_all_securities("stock", date).index.tolist()
print(f"股票数: {len(stocks)}")

# 可以逐步执行，查看中间结果
print(f"前10只: {stocks[:10]}")
```

## 最佳实践

### 1. 开发流程

```
策略编辑器 → 编写策略框架
    ↓
Notebook → 快速验证逻辑（无时间限制）
    ↓
Notebook → 参数调优
    ↓
策略编辑器 → 最终精确回测
```

### 2. 性能优化

```python
# ✓ 好：限制数量
stocks = all_stocks[:500]
df = get_price(stock, end_date=date, count=20)

# ✗ 差：获取所有数据
stocks = get_all_securities("stock", date).index  # 4000+ 只
```

### 3. 错误处理

```python
try:
    data = get_price(stock, end_date=date)
    if data.empty:
        print(f"{stock} 无数据")
except Exception as e:
    print(f"{stock} 失败: {e}")
```

## 文档索引

| 文档 | 用途 | 详细程度 |
|------|------|---------|
| SKILL.md | 技能主文档 | 中 |
| README.md | 详细使用指南 | 高 |
| QUICK_REFERENCE.md | 快速参考 | 低 |
| run_examples.sh | 示例脚本 | 实践 |

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| Session 过期 | `node browser/capture-joinquant-session.js --headed` |
| 执行超时 | 增加 `--timeout-ms 300000` |
| Notebook 缓存 | 使用 `--cell-marker "# REFRESH"` |
| 找不到策略文件 | 使用绝对路径 |

## 对比：Notebook vs 策略编辑器

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| 时间限制 | 180分钟/天 | **无限制** ✓ |
| 回测框架 | 完整 | 需手动实现 |
| 交互调试 | ✗ | ✓ |
| 逐步执行 | ✗ | ✓ |
| 精确回测 | ✓ | ✗ |
| 快速验证 | ✗ | ✓ |

## 下一步

1. **查看示例**：`cat examples/test_mini.py`
2. **运行测试**：`node run-strategy.js --strategy examples/test_mini.py`
3. **编写策略**：创建自己的策略文件
4. **参数调优**：快速测试不同参数组合

## 总结

已建立完整的 Notebook 策略运行系统：

- ✓ 核心运行脚本（run-strategy.js）
- ✓ 详细文档（README.md, QUICK_REFERENCE.md）
- ✓ 示例策略（examples/）
- ✓ 实际案例（RFScore PB10 对比）
- ✓ 故障排查指南

**核心优势**：无时间限制，适合快速验证策略逻辑和参数调优。

**使用建议**：Notebook 用于快速验证，策略编辑器用于精确回测。