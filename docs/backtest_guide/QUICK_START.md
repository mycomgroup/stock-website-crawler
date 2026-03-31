# Notebook 回测快速入门

## 一分钟开始

### JoinQuant Notebook

```bash
cd skills/joinquant_notebook

# 配置账号（编辑 .env）
echo "JOINQUANT_USERNAME=你的手机号" >> .env
echo "JOINQUANT_PASSWORD=你的密码" >> .env

# 抓取 session
node browser/capture-joinquant-session.js --headed

# 运行策略
node run-strategy.js --strategy examples/test_mini.py
```

### RiceQuant Notebook

```bash
cd skills/ricequant_strategy

# 配置账号（编辑 .env）
echo "RICEQUANT_USERNAME=你的账号" >> .env
echo "RICEQUANT_PASSWORD=你的密码" >> .env

# 运行策略（自动处理 session）
node run-strategy.js --strategy examples/simple_backtest.py
```

## 三种使用方式

### 1. 运行策略文件

```bash
node run-strategy.js --strategy your_strategy.py
```

### 2. 直接执行代码

```bash
node run-strategy.js --cell-source "print('hello')"
```

### 3. 重新执行 Notebook Cell

```bash
node run-strategy.js --cell-index last
node run-strategy.js --mode all
```

## 策略代码格式

### 策略编辑器格式（不推荐）

```python
def initialize(context):
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    stocks = get_all_securities("stock", context.current_dt)
```

### Notebook 格式（推荐）

```python
print("=== 策略测试 ===")

date = "2024-03-20"
stocks = get_all_securities("stock", date)
print(f"股票数: {len(stocks)}")

print("=== 测试完成 ===")
```

## 常见问题快速解决

| 问题 | 解决方案 |
|------|---------|
| Session 过期 | JoinQuant: 重新抓取; RiceQuant: 自动处理 |
| 执行超时 | `--timeout-ms 300000` |
| 无输出 | 使用 Notebook 格式策略，添加 `print()` |
| API 未定义 | 确保在平台环境运行，本地模拟会报错 |

## 查看结果

```bash
# JoinQuant
cat output/joinquant-notebook-result-*.json

# RiceQuant
cat data/ricequant-notebook-result-*.json
```

## 平台选择快速判断

- **首次验证策略** → JoinQuant Notebook
- **因子简单** → RiceQuant Notebook（Session 自动管理）
- **因子复杂** → JoinQuant Notebook（因子库丰富）
- **精确回测** → 策略编辑器

完整文档请查看 [README.md](README.md)