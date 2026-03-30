# RiceQuant Notebook 策略运行 - 快速参考

## 一键运行

```bash
# 首次使用：抓取 session
node browser/capture-ricequant-notebook-session.js --notebook-url "YOUR_NOTEBOOK_URL" --headed

# 运行策略
node run-strategy.js --strategy examples/simple_backtest.py
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
def init(context):
    scheduler.run_monthly(rebalance, monthday=1)

def rebalance(context, bar_dict):
    stocks = get_all_securities("stock", context.now)
```

### Notebook 格式
```python
# 直接指定日期
stocks = get_all_securities("stock", "2024-03-20")
print(f"股票数: {len(stocks)}")
```

## 目录结构

```
skills/ricequant_strategy/
├── examples/          # 策略示例
├── data/              # Session 数据和输出
├── run-strategy.js    # 运行脚本
├── README.md          # 详细文档
└── SKILL.md           # Skill 说明
```

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| Session 过期 | `node browser/capture-ricequant-notebook-session.js --headed` |
| 执行超时 | 增加 `--timeout-ms 300000` |
| Notebook 缓存 | 使用 `--cell-marker "# REFRESH"` |
| 找不到策略文件 | 使用绝对路径 |

## 示例策略

| 文件 | 说明 | 时间 |
|------|------|------|
| `simple_backtest.py` | API 连接测试 | 30秒 |
| `ma_strategy_notebook.py` | 双均线策略验证 | 1分钟 |
| `rfscore_simple_notebook.py` | RFScore 选股测试 | 2分钟 |

## 优势

- ✓ 无时间限制（策略编辑器限制 180分钟/天）
- ✓ 快速验证
- ✓ 交互调试
- ✓ 逐步执行

完整文档请查看 [README.md](README.md)