# Notebook 方式回测总结

**核心优势：无每日180分钟时间限制**

---

## 一、概述

### 为什么使用 Notebook？

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| **时间限制** | 180分钟/天 | **无限制** ✓ |
| 数据 API | ✓ | ✓ |
| 因子 API | ✓ | ✓ |
| 回测框架 | 完整 | 需手动实现 |
| 交互调试 | ✗ | ✓ |
| 逐步执行 | ✗ | ✓ |
| 适用场景 | 精确回测 | 快速验证 |

### 适用场景

- ✓ 策略逻辑快速验证
- ✓ 参数调优（多参数组合测试）
- ✓ 交互式调试（分步执行、查看中间结果）
- ✓ 快速原型测试

### 不适用场景

- ✗ 需要精确回测结果（使用策略编辑器）
- ✗ 分钟级数据回测
- ✗ 完整的归因分析

---

## 二、平台对比

目前支持两个平台的 Notebook 运行：

| 平台 | Skill 目录 | Session 管理 | API 差异 |
|------|-----------|-------------|---------|
| **JoinQuant** | `skills/joinquant_nookbook` | 手动抓取 | `get_all_securities("stock", date)` |
| **RiceQuant** | `skills/ricequant_strategy` | **自动管理** ✓ | `get_all_securities(["stock"])` |

**RiceQuant 的 Session 自动管理更便捷**

---

## 三、使用方式

### 3.1 JoinQuant Notebook

#### 快速开始

```bash
# 1. 配置环境变量（.env）
JOINQUANT_USERNAME=your_username
JOINQUANT_PASSWORD=your_password
JOINQUANT_NOTEBOOK_URL=your_notebook_url

# 2. 运行策略（自动处理 session）
node run-strategy.js --strategy examples/test_mini.py

# 3. 查看结果
cat output/joinquant-notebook-result-*.json
```

**首次运行或 session 过期时会自动后台登录（headless模式）**

#### 三种使用方式

**方式1：运行策略文件**

```bash
# 运行已有策略
node run-strategy.js --strategy examples/test_mini.py

# 运行自定义策略
node run-strategy.js --strategy /path/to/your/strategy.py

# 运行策略编辑器目录的策略
node run-strategy.js --strategy ../joinquant_strategy/weak_to_strong_simple.py
```

**方式2：直接执行代码**

```bash
# 单行代码
node run-strategy.js --cell-source "print('hello')"

# 多行代码（使用引号）
node run-strategy.js --cell-source "
from jqdata import *
stocks = get_all_securities('stock', '2024-03-20').index.tolist()[:10]
print(stocks)
"
```

**方式3：重新执行 Notebook Cell**

```bash
# 执行最后一个 cell
node run-strategy.js --cell-index last

# 执行指定位置的 cell
node run-strategy.js --cell-index 0

# 执行所有 cells
node run-strategy.js --mode all
```

#### Session 管理

JoinQuant 会自动管理 session（无需手动干预）：

1. **自动检查**：运行时检查现有 session 是否有效
2. **自动重试**：如果 session 出错（401/403），自动重新获取（headless模式）
3. **自动保存**：登录成功后自动保存 session
4. **自动复用**：后续运行自动复用有效 session（7天有效期）

**默认使用无界面模式（headless），不会弹出浏览器窗口**

---

### 3.2 RiceQuant Notebook

#### 快速开始

```bash
# 1. 配置环境变量（.env）
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research

# 2. 运行策略（自动处理 session）
node run-strategy.js --strategy examples/simple_backtest.py

# 3. 查看结果
cat data/ricequant-notebook-result-*.json
```

#### 三种使用方式

**方式1：运行策略文件**

```bash
node run-strategy.js --strategy examples/simple_backtest.py
node run-strategy.js --strategy /path/to/your/strategy.py
```

**方式2：创建独立 Notebook（默认行为）**

每次运行默认创建新的独立 notebook，命名格式：`中文任务名_YYYYMMDD_HHMMSS.ipynb`

任务名自动从策略文件第一行注释提取：
```python
# 最小化测试 - 2025年12月到2026年3月
```
生成：`最小化测试_2025年12月到2026年3月_20260331_133203.ipynb`

```bash
# 运行策略，自动创建新 notebook（推荐）
node run-strategy.js --strategy examples/simple_backtest.py

# 指定 notebook 基础名称
node run-strategy.js --strategy examples/simple_backtest.py --notebook-base-name 自定义任务名
# 生成：自定义任务名_20240115_103045.ipynb
```

**Notebook 不会自动删除，方便查看每次运行的结果**

如果运行出错，下次运行会自动继续使用同一个 notebook，直到修复成功。

**方式3：直接执行代码**

```bash
node run-strategy.js --cell-source "print('hello from ricequant')"
```

#### Session 自动管理

**系统会自动处理 session，无需手动干预：**

1. **自动检查**：运行时检查现有 session 是否有效
2. **自动重试**：如果 session 出错（401/403），自动重新获取（headless模式）
3. **自动登录**：如果 session 无效，自动后台登录（headless模式）
4. **自动保存**：登录成功后自动保存 session
5. **自动复用**：后续运行自动复用有效 session（7天有效期）

**默认使用无界面模式（headless），不会弹出浏览器窗口**

**首次运行或 session 过期时会自动后台登录，无需手动干预**

---

## 四、策略代码适配

### 4.1 策略编辑器 → Notebook

策略编辑器的代码可以直接运行，但需要注意差异：

#### 策略编辑器格式

```python
# 策略编辑器使用 initialize/handle_data 框架
from jqdata import *

def initialize(context):
    set_option("use_real_price", True)
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    # 选股逻辑
    stocks = get_all_securities("stock", context.current_dt).index
    print(stocks)
```

#### Notebook 格式

```python
# Notebook 直接执行逻辑，无需 initialize
from jqdata import *

# 直接指定日期
date = "2024-03-20"

# 直接调用选股逻辑
stocks = get_all_securities("stock", date).index.tolist()
print(f"可选股票数: {len(stocks)}")

# 可以逐步执行，查看中间结果
print(f"前10只: {stocks[:10]}")
```

### 4.2 关键差异

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| 入口函数 | `initialize(context)` | 直接执行 |
| 时间上下文 | `context.current_dt` | 手动指定日期字符串 |
| 定时任务 | `run_daily(func, time)` | 手动调用函数 |
| 回测框架 | 自动循环 | 手动编写循环 |
| 输出查看 | 日志面板 | 直接 print |

### 4.3 API 差异示例

**JoinQuant**

```python
# 获取股票
stocks = get_all_securities("stock", "2024-03-20")

# 获取指数成分股
hs300 = get_index_stocks("000300.XSHG", date="2024-03-20")
```

**RiceQuant**

```python
# 获取股票
all_stocks = get_all_securities(["stock"])

# 获取指数成分股
hs300 = index_components("000300.XSHG")
```

---

## 五、参数说明

### JoinQuant 参数

```bash
node run-strategy.js [参数]

必需参数（二选一）：
  --strategy <path>      策略文件路径
  --cell-source <code>   直接执行的代码

可选参数：
  --notebook-url <url>   Notebook URL（默认从 .env 读取）
  --timeout-ms <ms>      超时时间（默认 60000ms = 1分钟）
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
  --notebook-base-name <name>   Notebook 名称（默认从策略注释提取中文任务名）
```

**说明：**
- 每次运行自动创建新 notebook，命名：`任务名_YYYYMMDD_HHMMSS.ipynb`
- 任务名优先从策略文件第一行注释提取中文描述
- 可通过 `--notebook-base-name` 手动指定
- Notebook 不会自动删除，保留所有运行结果
- 如果运行出错，下次自动继续使用同一个 notebook，直到修复

---

## 六、示例策略

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

---

## 七、工作流程推荐

### 策略开发流程

```
1. 策略编辑器 → 编写策略框架
2. Notebook → 快速验证逻辑
3. Notebook → 参数调优
4. Notebook → 完整回测（简化版）
5. 策略编辑器 → 最终回测（精确版）
```

### 推荐使用顺序

**JoinQuant 用户**

1. 使用 Notebook 验证策略逻辑（无时间限制）
2. 使用 Notebook 进行参数调优
3. 确定参数后，在策略编辑器进行精确回测

**RiceQuant 用户**

1. 使用 Notebook 快速验证（自动 session 管理）
2. 运行后查看保留的 notebook 结果
3. 在策略编辑器进行最终回测

---

## 八、常见问题

### Q1: Session 过期怎么办？

**自动处理，无需手动干预**

```bash
# JoinQuant 和 RiceQuant 都会自动处理
# 如果 session 过期或出错，运行时会自动重新登录（headless模式）
node run-strategy.js --strategy your_strategy.py
```

### Q2: 执行超时怎么办？

```bash
# 增加超时时间（默认 60000ms）
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000  # 5分钟
node run-strategy.js --strategy your_strategy.py --timeout-ms 600000  # 10分钟
```

### Q3: Notebook 管理机制？

**自动管理，无需手动干预**

- **每次运行自动创建新 notebook**：命名格式 `中文任务名_YYYYMMDD_HHMMSS.ipynb`
- **任务名自动提取**：从策略文件第一行注释提取中文任务名
- **不会自动删除**：保留所有运行过的 notebook，方便查看结果
- **出错自动重用**：如果运行出错，下次会继续使用同一个 notebook，直到修复

**示例**：
```python
# 龙头底分型回测 - 2024年Q1
```
生成 notebook：`龙头底分型回测_2024年Q1_20240115_103045.ipynb`

**RiceQuant 用户**

查看运行过的 notebook：
- Notebook URL 会保存在结果文件中
- 可以通过 RiceQuant 网站查看所有历史 notebook

### Q4: 如何调试策略？

**方法1：逐步执行**

```python
# 分成多个 cell，逐步执行
# Cell 1
from jqdata import *
date = "2024-03-20"

# Cell 2
stocks = get_all_securities("stock", date).index.tolist()
print(f"总数: {len(stocks)}")

# Cell 3
filtered = stocks[:100]
print(f"筛选后: {len(filtered)}")
```

**方法2：使用 print 和 try-except**

```python
try:
    # 可能出错的代码
    result = some_function()
    print(f"结果: {result}")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
```

### Q5: 如何查看执行结果？

**输出文件位置**

```bash
# JoinQuant
cat output/joinquant-notebook-result-*.json

# RiceQuant
cat data/ricequant-notebook-result-*.json
```

**Notebook 快照**

```bash
# JoinQuant
output/joinquant-notebook-TIMESTAMP.ipynb

# RiceQuant
data/ricequant-notebook-TIMESTAMP.ipynb
```

---

## 九、最佳实践

### 1. 性能优化

```python
# ✓ 好：限制股票数量
stocks = all_stocks[:500]  # 只测试 500 只

# ✓ 好：使用 count 参数
df = get_price(stock, end_date=date, count=20)  # 只取 20 天

# ✗ 差：获取所有数据
stocks = get_all_securities("stock", date).index  # 4000+ 只股票
df = get_price(stocks, end_date=date)  # 海量数据
```

### 2. 错误处理

```python
# ✓ 好：捕获异常
try:
    data = get_price(stock, end_date=date)
    if data.empty:
        print(f"{stock} 无数据")
except Exception as e:
    print(f"{stock} 获取失败: {e}")

# ✗ 差：不处理错误
data = get_price(stock, end_date=date)  # 可能崩溃
```

### 3. 参数调优示例

```python
# 测试不同参数组合
params = [
    {"pb_threshold": 0.8, "roa_threshold": 0.05},
    {"pb_threshold": 1.0, "roa_threshold": 0.05},
    {"pb_threshold": 1.2, "roa_threshold": 0.03},
]

results = []
for param in params:
    # 选股逻辑
    selected = filter_stocks(param)
    # 计算收益
    return = calculate_return(selected)
    results.append({"params": param, "return": return})

# 输出对比
for r in results:
    print(f"PB < {r['params']['pb_threshold']}: 收益 {r['return']:.2f}%")
```

---

## 十、相关文档

### JoinQuant

- **详细指南**：`skills/joinquant_nookbook/README.md`
- **快速参考**：`skills/joinquant_nookbook/QUICK_REFERENCE.md`
- **API 文档**：`skills/joinquant_nookbook/joinquant_doc/`

### RiceQuant

- **详细指南**：`skills/ricequant_strategy/README.md`
- **快速参考**：`skills/ricequant_strategy/QUICK_REFERENCE.md`
- **Session 管理**：`skills/ricequant_strategy/SESSION_MANAGEMENT.md`

---

## 总结

**Notebook 运行策略的优势**：
- ✓ 无时间限制
- ✓ 快速验证
- ✓ 交互调试
- ✓ 参数调优
- ✓ 自动 session 管理（headless模式）
- ✓ 自动创建新 notebook（整齐命名）
- ✓ 自动错误重试机制

**推荐流程**：
1. Notebook → 快速验证逻辑
2. Notebook → 参数调优
3. 策略编辑器 → 最终精确回测

**平台选择建议**：
- JoinQuant：适合已有策略代码的用户，自动 session 管理
- RiceQuant：适合新手，Session 自动管理更便捷

**核心改进**：
- 默认使用无界面模式（headless），不会弹出浏览器
- 每次运行自动创建新 notebook：`中文任务名_YYYYMMDD_HHMMSS.ipynb`
- 任务名自动从策略文件注释中提取中文描述
- Notebook 不会自动删除，保留所有运行结果
- Session 出错自动重试（401/403）
- 运行出错自动重用同一个 notebook，直到修复

---

**下一步**：
1. 查看 `examples/` 目录的示例
2. 运行最小测试验证环境
3. 编写自己的策略
4. 享受无时间限制的策略开发！