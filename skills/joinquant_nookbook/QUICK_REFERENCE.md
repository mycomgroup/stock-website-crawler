# JoinQuant Notebook 策略运行 - 快速参考

## 一键运行

```bash
# 首次使用：抓取 session
node browser/capture-joinquant-session.js --notebook-url "YOUR_NOTEBOOK_URL" --headed

# 运行策略
node run-strategy.js --strategy examples/rfscore_full_comparison.py
```

## 常用命令

```bash
# 运行策略文件
node run-strategy.js --strategy your_strategy.py

# 直接执行代码
node run-strategy.js --cell-source "print('hello')"

# 增加超时时间
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000

# 重新执行 notebook 中的 cell
node run-strategy.js --cell-index last
```

## 策略代码转换

### 策略编辑器格式
```python
def initialize(context):
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    date = context.current_dt
    stocks = get_all_securities("stock", date)
```

### Notebook 格式
```python
# 直接指定日期
date = "2024-03-20"

# 直接调用函数
stocks = get_all_securities("stock", date)
print(f"股票数: {len(stocks)}")
```

## 目录结构

```
skills/joinquant_nookbook/
├── examples/          # 策略示例
├── output/           # 输出文件
├── data/             # Session 数据
├── run-strategy.js   # 运行脚本
└── README.md         # 详细文档
```

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| Session 过期 | `node browser/capture-joinquant-session.js --headed` |
| 执行超时 | 增加 `--timeout-ms 300000` |
| Notebook 缓存 | 使用 `--cell-marker "# REFRESH"` |
| 找不到策略文件 | 使用绝对路径 |

## 示例策略

| 文件 | 说明 | 时间 |
|------|------|------|
| `test_mini.py` | 最小化测试 | 30秒 |
| `rfscore_simple_test.py` | 单日选股测试 | 1分钟 |
| `rfscore_full_comparison.py` | 完整策略对比 | 10分钟 |

## 优势

- ✓ 无时间限制（策略编辑器限制 180分钟/天）
- ✓ 快速验证
- ✓ 交互调试
- ✓ 逐步执行

完整文档请查看 [README.md](README.md)