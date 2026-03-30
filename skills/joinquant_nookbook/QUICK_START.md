# 快速使用指南

## 1. 准备 Notebook

在 JoinQuant 网站创建一个 Notebook：
1. 登录 https://www.joinquant.com
2. 进入 "研究" → "Notebook"
3. 创建新 Notebook，命名为 `strategy_runner`
4. 复制 Notebook URL 到 `.env` 文件

```bash
# 更新 .env
JOINQUANT_NOTEBOOK_URL=https://www.joinquant.com/user/notebook?url=/user/13311390323/notebooks/strategy_runner.ipynb
```

## 2. 首次运行（需要抓取 session）

```bash
# 抓取浏览器 session（需要手动登录）
node browser/capture-joinquant-session.js --notebook-url $JOINQUANT_NOTEBOOK_URL

# 或者指定 notebook URL
node browser/capture-joinquant-session.js --notebook-url "https://www.joinquant.com/user/notebook?url=/user/13311390323/notebooks/strategy_runner.ipynb"
```

## 3. 运行策略

```bash
# 运行 joinquant_strategy 中的策略
node run-strategy.js --strategy weak_to_strong_simple.py

# 运行 notebook examples 中的策略
node run-strategy.js --strategy examples/test_mini.py

# 直接执行代码
node run-strategy.js --cell-source "from jqdata import *; print(get_trade_days('2024-01-01', '2024-01-10'))"
```

## 4. 查看结果

执行完成后，查看 `output/` 目录：
- Notebook 快照：`joinquant-notebook-*.ipynb`
- 执行结果：`joinquant-notebook-result-*.json`

## 5. 常见问题

### Session 过期

如果遇到 "缺少 `_xsrf` cookie" 或 401/403 错误：

```bash
node browser/capture-joinquant-session.js --notebook-url $JOINQUANT_NOTEBOOK_URL
```

### 策略文件找不到

检查路径是否正确：
```bash
# 使用绝对路径
node run-strategy.js --strategy /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/weak_to_strong_simple.py

# 或者相对路径
node run-strategy.js --strategy ../joinquant_strategy/weak_to_strong_simple.py
```

### 执行超时

增加超时时间：
```bash
node run-strategy.js --strategy large_strategy.py --timeout-ms 120000
```

## 6. 与策略编辑器对比

| 操作 | 策略编辑器 | Notebook |
|------|-----------|----------|
| 修改代码 | 编辑 → 运行回测 | 编辑 → 运行 cell |
| 调试 | 看日志 | 逐步执行 + print |
| 时间限制 | 180分钟/天 | 无限制 |
| 数据获取 | run_daily 定时 | 手动调用 API |

## 7. 策略代码适配

策略编辑器的代码可以直接运行，但回测需要手动模拟：

### 策略编辑器格式
```python
def initialize(context):
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    # 选股逻辑
    pass
```

### Notebook 格式
```python
# 直接调用选股逻辑
from datetime import datetime
context = MockContext(datetime.now())
select_stocks(context)
print(context.stocks)  # 或 g.stocks
```

使用适配器自动转换：
```bash
node run-strategy.js --strategy weak_to_strong_simple.py --convert
```