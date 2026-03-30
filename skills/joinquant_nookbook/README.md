# JoinQuant Notebook 策略运行器

**在 JoinQuant Notebook 中运行策略，无每日时间限制**

## 为什么使用 Notebook？

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| **时间限制** | 180分钟/天 | **无限制** ✓ |
| 数据 API | ✓ | ✓ |
| 因子 API | ✓ | ✓ |
| 交互调试 | ✗ | ✓ |
| 代码复用 | 独立 | **直接复用** ✓ |
| 快速验证 | 需要完整回测 | **可以分步执行** ✓ |

## 快速开始

### 1. 前置条件

```bash
# 确保已安装依赖
cd skills/joinquant_nookbook
npm install
```

### 2. 首次使用：抓取 Session

```bash
# 方法1: 使用环境变量中的账号密码
node browser/capture-joinquant-session.js --notebook-url "https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb"

# 方法2: 手动登录（推荐）
node browser/capture-joinquant-session.js --notebook-url "https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb" --headed
```

### 3. 运行策略

```bash
# 运行策略文件
node run-strategy.js --strategy examples/rfscore_full_comparison.py --notebook-url "https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb"

# 或者直接执行代码
node run-strategy.js --cell-source "print('hello')" --notebook-url "..."
```

## 详细指南

### 一、环境配置

#### 1.1 创建 JoinQuant Notebook

1. 登录 [JoinQuant](https://www.joinquant.com)
2. 进入 "研究" → "Notebook"
3. 创建新 Notebook，命名为 `test` 或其他名称
4. 复制 Notebook URL（格式：`https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb`）

#### 1.2 配置环境变量

编辑 `.env` 文件：

```bash
# JoinQuant 账号
JOINQUANT_USERNAME=你的手机号
JOINQUANT_PASSWORD="你的密码"

# Notebook URL（可选，可以在命令行指定）
JOINQUANT_NOTEBOOK_URL=https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb
```

#### 1.3 抓取浏览器 Session

**首次使用必须执行此步骤**

```bash
# 推荐：有头模式，可以看到浏览器操作
node browser/capture-joinquant-session.js \
  --notebook-url "https://www.joinquant.com/user/notebook?url=/user/YOUR_USER_ID/notebooks/test.ipynb" \
  --headed

# 如果 session 过期，重新执行上述命令
```

Session 文件保存在 `data/session.json`，有效期约 1 天。

### 二、策略运行方式

#### 方式1：运行策略文件

**适用场景：完整的策略逻辑，多行代码**

```bash
# 运行已有策略
node run-strategy.js --strategy examples/rfscore_full_comparison.py

# 运行自定义策略
node run-strategy.js --strategy /path/to/your/strategy.py
```

**策略文件路径解析规则**：

```bash
# 相对路径（自动查找）
node run-strategy.js --strategy weak_to_strong_simple.py
# 查找顺序：joinquant_strategy/ → joinquant_nookbook/examples/

# 绝对路径
node run-strategy.js --strategy /Users/xxx/strategy.py

# 从 joinquant_strategy 目录
node run-strategy.js --strategy ../joinquant_strategy/weak_to_strong_simple.py

# 从 examples 目录
node run-strategy.js --strategy examples/test_mini.py
```

#### 方式2：直接执行代码

**适用场景：快速测试，单行/多行代码**

```bash
# 单行代码
node run-strategy.js --cell-source "print('hello')"

# 多行代码（使用引号）
node run-strategy.js --cell-source "
from jqdata import *
date = '2024-03-20'
stocks = get_all_securities('stock', date).index.tolist()[:10]
print(stocks)
"
```

#### 方式3：运行 Notebook 中已有的 Cell

**适用场景：Notebook 中已有代码，只想重新执行**

```bash
# 执行最后一个 cell
node run-strategy.js --cell-index last

# 执行指定位置的 cell
node run-strategy.js --cell-index 0

# 执行多个 cell
node run-strategy.js --cell-index 0,1,2

# 执行所有 cell
node run-strategy.js --mode all
```

### 三、策略代码适配

策略编辑器的代码可以直接运行，但需要注意以下差异：

#### 3.1 策略编辑器格式

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

#### 3.2 Notebook 格式

```python
# Notebook 直接执行逻辑，无需 initialize
from jqdata import *
from datetime import datetime

# 直接指定日期
date = "2024-03-20"

# 直接调用选股逻辑
stocks = get_all_securities("stock", date).index.tolist()
print(f"可选股票数: {len(stocks)}")

# 可以逐步执行，查看中间结果
print(f"前10只: {stocks[:10]}")
```

#### 3.3 关键差异

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| 入口函数 | `initialize(context)` | 直接执行 |
| 时间上下文 | `context.current_dt` | 手动指定日期字符串 |
| 定时任务 | `run_daily(func, time)` | 手动调用函数 |
| 回测框架 | 自动循环 | 手动编写循环 |
| 输出查看 | 日志面板 | 直接 print |

#### 3.4 使用适配器（可选）

对于需要回测框架的策略，可以使用适配器：

```python
# 导入适配器
import sys
sys.path.append('/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook')
from strategy_adapter import NotebookBacktest

# 导入策略
import your_strategy as strategy

# 运行回测
bt = NotebookBacktest(strategy, '2024-01-01', '2024-12-31', 100000)
bt.run()
bt.summary()
```

### 四、参数说明

```bash
node run-strategy.js [参数]

必需参数（二选一）：
  --strategy <path>      策略文件路径
  --cell-source <code>   直接执行的代码

可选参数：
  --notebook-url <url>   Notebook URL（默认从 .env 读取）
  --session-file <path>  Session 文件路径（默认 data/session.json）
  --cell-index <index>   执行指定 cell（0, last, 或 0,1,2）
  --cell-marker <text>   替换包含标记的 cell
  --mode <mode>          all: 执行所有 cells
  --timeout-ms <ms>      超时时间（默认 60000ms = 1分钟）
  --append-cell <bool>   是否追加新 cell（默认 true）
  --kernel-name <name>   内核名称（默认 python3）
```

### 五、输出文件

执行完成后，查看 `output/` 目录：

```bash
output/
├── joinquant-notebook-TIMESTAMP.ipynb    # Notebook 快照
├── joinquant-notebook-result-TIMESTAMP.json  # 执行结果详情
└── your_custom_file.json                  # 策略保存的结果
```

**Notebook 快照**：包含所有 cell 和执行结果，可以在本地 Jupyter 中打开查看。

**执行结果 JSON**：包含每个 cell 的输出、错误信息等。

### 六、完整示例

#### 示例1：快速验证选股逻辑

```bash
# 1. 创建策略文件 test_selection.py
cat > examples/test_selection.py << 'EOF'
from jqdata import *

# 测试日期
test_date = "2024-03-20"

# 获取股票池
hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
stocks = list(hs300 | zz500)

print(f"初始股票数: {len(stocks)}")

# 过滤 ST
is_st = get_extras("is_st", stocks, end_date=test_date, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()

print(f"过滤 ST 后: {len(stocks)}")

# 获取基本面数据
q = query(
    valuation.code,
    valuation.pb_ratio,
    valuation.pe_ratio,
    indicator.roa
).filter(valuation.code.in_(stocks))

df = get_fundamentals(q, date=test_date)
df = df.dropna()

print(f"有基本面数据: {len(df)}")

# 选股：ROA > 0 + PB < 1
selected = df[(df['roa'] > 0) & (df['pb_ratio'] < 1)]
selected = selected.sort_values('roa', ascending=False)

print(f"\n选中股票: {len(selected)}")
print(selected.head(10))
EOF

# 2. 运行策略
node run-strategy.js --strategy examples/test_selection.py --timeout-ms 120000
```

#### 示例2：参数调优

```bash
# 创建参数调优脚本
cat > examples/param_tuning.py << 'EOF'
from jqdata import *
import pandas as pd
import numpy as np

# 测试日期范围
test_dates = ["2024-01-02", "2024-02-01", "2024-03-01"]

# 参数组合
params = [
    {"pb_threshold": 0.8, "roa_threshold": 0.05},
    {"pb_threshold": 1.0, "roa_threshold": 0.05},
    {"pb_threshold": 1.2, "roa_threshold": 0.03},
]

results = []

for param in params:
    monthly_returns = []
    
    for date in test_dates:
        # 选股逻辑
        hs300 = get_index_stocks("000300.XSHG", date=date)
        
        q = query(
            valuation.code,
            valuation.pb_ratio,
            indicator.roa
        ).filter(valuation.code.in_(hs300))
        
        df = get_fundamentals(q, date=date)
        df = df.dropna()
        
        selected = df[
            (df['pb_ratio'] < param['pb_threshold']) & 
            (df['roa'] > param['roa_threshold'])
        ]
        
        # 计算收益
        if len(selected) > 0:
            returns = []
            for stock in selected['code'].head(10):
                try:
                    p1 = get_price(stock, end_date=date, count=1, fields=['close'], panel=False)
                    next_date = get_trade_days(date, "2024-12-31")[20]
                    p2 = get_price(stock, end_date=next_date, count=1, fields=['close'], panel=False)
                    
                    if not p1.empty and not p2.empty:
                        ret = (float(p2['close'].iloc[-1]) - float(p1['close'].iloc[-1])) / float(p1['close'].iloc[-1])
                        returns.append(ret)
                except:
                    pass
            
            if returns:
                monthly_returns.append(np.mean(returns))
    
    results.append({
        "params": param,
        "avg_return": np.mean(monthly_returns) * 100 if monthly_returns else 0
    })

# 输出结果
print("\n参数调优结果:")
print("-" * 60)
for r in results:
    print(f"PB < {r['params']['pb_threshold']}, ROA > {r['params']['roa_threshold']}: 平均收益 {r['avg_return']:.2f}%")
EOF

# 运行调优
node run-strategy.js --strategy examples/param_tuning.py --timeout-ms 180000
```

#### 示例3：运行完整策略对比

```bash
# 运行已有的策略对比脚本
node run-strategy.js --strategy examples/rfscore_full_comparison.py --timeout-ms 600000

# 查看结果
python strategies/enhanced/backtest_comparison.py
```

### 七、常见问题

#### Q1: Session 过期怎么办？

```bash
# 重新抓取 session
node browser/capture-joinquant-session.js --notebook-url "YOUR_NOTEBOOK_URL" --headed
```

#### Q2: 执行超时怎么办？

```bash
# 增加超时时间（默认 60000ms）
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000  # 5分钟
```

#### Q3: Notebook 缓存了旧代码？

```bash
# 使用 cell-marker 替换特定 cell
node run-strategy.js --strategy your_strategy.py --cell-marker "# FORCE_REFRESH"
```

#### Q4: 如何调试策略？

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

#### Q5: 如何保存结果？

```python
import json

# 保存到 JoinQuant 服务器
with open('result.json', 'w') as f:
    json.dump(your_data, f)

# 或者保存到本地（需要指定绝对路径）
result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/my_result.json"
with open(result_file, 'w') as f:
    json.dump(your_data, f)
```

#### Q6: 策略编辑器和 Notebook 结果不一致？

可能原因：
1. 数据时间点不同（Notebook 使用的是当前时间的数据）
2. 因子库版本不同（jqfactor 在 Notebook 中可能有延迟）
3. 代码逻辑差异（日期类型处理等）

建议：使用相同的数据接口和参数进行对比。

### 八、最佳实践

#### 1. 代码组织

```
skills/joinquant_nookbook/
├── examples/                    # 策略示例
│   ├── test_mini.py            # 最小化测试
│   ├── rfscore_simple_test.py  # 单功能测试
│   ├── rfscore_full_comparison.py  # 完整策略
│   └── param_tuning.py         # 参数调优
├── output/                      # 输出目录
├── data/                        # Session 数据
├── run-strategy.js             # 运行脚本
└── README.md                   # 本文档
```

#### 2. 策略开发流程

```
1. 策略编辑器 → 编写策略框架
2. Notebook → 快速验证逻辑
3. Notebook → 参数调优
4. Notebook → 完整回测（简化版）
5. 策略编辑器 → 最终回测（精确版）
```

#### 3. 性能优化

```python
# ✓ 好：限制股票数量
stocks = all_stocks[:500]  # 只测试 500 只

# ✓ 好：使用 count 参数
df = get_price(stock, end_date=date, count=20)  # 只取 20 天

# ✗ 差：获取所有数据
stocks = get_all_securities("stock", date).index  # 4000+ 只股票
df = get_price(stocks, end_date=date)  # 海量数据
```

#### 4. 错误处理

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

### 九、进阶用法

#### 1. 批量测试多个策略

```bash
# 创建批量测试脚本
cat > batch_test.sh << 'EOF'
#!/bin/bash
strategies=(
    "examples/test_mini.py"
    "examples/rfscore_simple_test.py"
    "examples/param_tuning.py"
)

for strategy in "${strategies[@]}"; do
    echo "Testing $strategy..."
    node run-strategy.js --strategy "$strategy" --timeout-ms 300000
    sleep 5
done
EOF

chmod +x batch_test.sh
./batch_test.sh
```

#### 2. 结果对比分析

```python
# 加载多次运行的结果
import json

results = []
for file in ['result1.json', 'result2.json', 'result3.json']:
    with open(file) as f:
        results.append(json.load(f))

# 对比分析
for i, r in enumerate(results):
    print(f"Run {i+1}: Return={r['total_return']:.2f}%, Sharpe={r['sharpe']:.2f}")
```

#### 3. 与策略编辑器联动

```python
# 在 Notebook 中生成策略代码
def generate_strategy_code(params):
    return f"""
from jqdata import *

def initialize(context):
    set_option("use_real_price", True)
    g.pb_threshold = {params['pb_threshold']}
    g.roa_threshold = {params['roa_threshold']}
    
    run_monthly(rebalance, 1, time="9:35")

def rebalance(context):
    # 选股逻辑
    pass
"""

# 保存到文件
code = generate_strategy_code({"pb_threshold": 1.0, "roa_threshold": 0.05})
print(code)  # 复制到策略编辑器
```

## 总结

**Notebook 运行策略的优势**：
- ✓ 无时间限制
- ✓ 快速验证
- ✓ 交互调试
- ✓ 参数调优

**适用场景**：
- 策略开发和验证
- 快速原型测试
- 参数调优
- 教学和研究

**不适用场景**：
- 需要精确回测结果（使用策略编辑器）
- 需要分钟级数据回测
- 需要完整的归因分析

**下一步**：
1. 查看 `examples/` 目录的示例
2. 运行 `test_mini.py` 验证环境
3. 编写自己的策略
4. 享受无时间限制的策略开发！

---

**问题反馈**：如有问题，请检查 `output/` 目录下的日志文件，或重新抓取 session。