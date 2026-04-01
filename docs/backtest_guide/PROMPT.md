# Agent 运行 Notebook 回测提示词

以下提示词用于指导 Agent 正确运行 Notebook 回测，请复制使用：

---

## 标准提示词（推荐使用）

```
我需要运行量化策略的 Notebook 回测。请按照以下步骤操作：

**1. 确认策略类型和平台选择**

请先分析我的策略，根据以下规则选择平台：

- 如果策略依赖 jqfactor 特殊因子（technical_analysis/quality/momentum/volatility），使用 **JoinQuant Notebook**
- 如果策略因子简单（仅用 PE/PB/ROA/ROE/市值等基础因子），使用 **RiceQuant Notebook**
- 如果是首次验证策略，优先使用 **JoinQuant Notebook**

**2. 进入正确的 Skill 目录**

根据选择的平台，进入对应目录：
- JoinQuant Notebook: `cd skills/joinquant_notebook`
- RiceQuant Notebook: `cd skills/ricequant_strategy`

**3. 确认策略格式**

请检查策略文件格式是否适合 Notebook 运行：

**适合 Notebook 的格式（推荐）：**
```python
print("=== 策略测试开始 ===")

try:
    # 直接执行代码，不依赖策略框架
    date = "2024-03-20"
    stocks = get_all_securities("stock", date)  # JoinQuant
    # 或 stocks = all_instruments("CS")  # RiceQuant
    
    # 计算逻辑
    result = your_logic(stocks)
    print(f"结果: {result}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("=== 测试完成 ===")
```

**不适合 Notebook 的格式：**
```python
def initialize(context):  # 策略编辑器格式，Notebook 不会调用
    ...
def handle_data(context, data):  # 不会被执行
    ...
```

如果策略是策略编辑器格式，请先转换为 Notebook 格式。

**4. 运行策略**

请根据平台使用正确的命令：

**JoinQuant Notebook：**
```bash
# 确保已配置 .env 文件（JOINQUANT_USERNAME, JOINQUANT_PASSWORD, JOINQUANT_NOTEBOOK_URL）
# 如果 session 过期，先运行：node browser/capture-joinquant-session.js --headed

node run-strategy.js --strategy your_strategy.py --timeout-ms 120000
```

**RiceQuant Notebook：**
```bash
# 确保已配置 .env 文件（RICEQUANT_USERNAME, RICEQUANT_PASSWORD, RICEQUANT_NOTEBOOK_URL）
# Session 会自动管理，无需手动抓取

node run-strategy.js --strategy your_strategy.py --create-new --timeout-ms 120000
```

**5. 增加超时时间**

如果策略涉及大量数据或计算，请增加超时时间：
```bash
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000  # 5分钟
node run-strategy.js --strategy your_strategy.py --timeout-ms 600000  # 10分钟
```

**6. 查看和解读结果**

运行后查看结果文件：
- JoinQuant: `cat output/joinquant-notebook-result-*.json`
- RiceQuant: `cat data/ricequant-notebook-result-*.json`

请解读输出内容：
- 如果看到 "执行成功" 且有 print 输出，说明策略运行正确
- 如果看到 API 未定义错误，说明策略格式不对或需要在平台环境运行
- 如果超时，增加 timeout-ms 参数重新运行

**7. 故障排查**

遇到问题时请按以下步骤排查：

| 问题 | 解决方案 |
|------|---------|
| Session 过期 | JoinQuant: 重新抓取 session<br>RiceQuant: 自动处理 |
| 执行超时 | 增加 --timeout-ms |
| 无输出 | 使用 Notebook 格式，添加 print |
| API 未定义 | 检查平台环境，转换 API |

**8. 参考文档**

请参考以下文档获取详细说明：
- 总体指南: `docs/backtest_guide/README.md`
- 快速入门: `docs/backtest_guide/QUICK_START.md`
- API差异: `docs/backtest_guide/API_DIFF.md`
- 迁移指南: `docs/backtest_guide/MIGRATION.md`
```

---

## 精简提示词（用于快速运行）

```
请帮我运行 Notebook 回测。策略文件路径：[填写路径]

平台选择规则：
- 因子复杂（jqfactor）→ JoinQuant Notebook
- 因子简单 → RiceQuant Notebook

运行命令：
- JoinQuant: `cd skills/joinquant_notebook && node run-strategy.js --strategy [策略路径] --timeout-ms 120000`
- RiceQuant: `cd skills/ricequant_strategy && node run-strategy.js --strategy [策略路径] --create-new --timeout-ms 120000`

注意事项：
1. 策略必须是 Notebook 格式（直接执行 + print），不是策略编辑器格式（initialize/handle_data）
2. 查看结果：JoinQuant 在 output/ 目录，RiceQuant 在 data/ 目录
3. 如超时，增加 --timeout-ms 参数

参考文档：docs/backtest_guide/README.md
```

---

## JoinQuant Notebook 提示词

```
请帮我运行 JoinQuant Notebook 回测。

策略文件：[填写路径]

步骤：
1. 进入目录：`cd skills/joinquant_notebook`
2. 确保 .env 配置正确（JOINQUANT_USERNAME, JOINQUANT_PASSWORD, JOINQUANT_NOTEBOOK_URL）
3. 如果 session 过期：`node browser/capture-joinquant-session.js --headed`
4. 运行策略：`node run-strategy.js --strategy [策略路径] --timeout-ms 120000`
5. 查看结果：`cat output/joinquant-notebook-result-*.json`

策略格式要求：
- 必须是 Notebook 格式（直接执行代码 + print）
- 不能是策略编辑器格式（initialize/handle_data）
- API 使用 JoinQuant 格式：get_all_securities("stock", date)

参考文档：docs/backtest_guide/README.md, skills/joinquant_notebook/README.md
```

---

## RiceQuant Notebook 提示词

```
请帮我运行 RiceQuant Notebook 回测。

策略文件：[填写路径]

步骤：
1. 进入目录：`cd skills/ricequant_strategy`
2. 确保 .env 配置正确（RICEQUANT_USERNAME, RICEQUANT_PASSWORD）
3. 运行策略：`node run-strategy.js --strategy [策略路径] --create-new --timeout-ms 120000`
4. 查看结果：`cat data/ricequant-notebook-result-*.json`

策略格式要求：
- 必须是 Notebook 格式（直接执行代码 + print）
- 不能是策略编辑器格式（init/handle_bar）
- API 使用 RiceQuant 格式：all_instruments("CS"), history_bars()

Session 自动管理，无需手动抓取。

参考文档：docs/backtest_guide/README.md, skills/ricequant_strategy/README.md
```

---

## RiceQuant 策略编辑器提示词 ⭐ 推荐

```
请帮我运行 RiceQuant 策略编辑器回测。

策略文件：[填写路径]
策略ID：[填写策略ID，如果不确定，先运行 list-strategies.js 查看列表]

步骤：
1. 进入目录：`cd skills/ricequant_strategy`
2. 确保 .env 配置正确（RICEQUANT_USERNAME, RICEQUANT_PASSWORD）
3. Session 自动管理，无需手动抓取
4. 运行回测：`node run-skill.js --id [策略ID] --file [策略路径] --start 2024-01-01 --end 2024-12-31`
5. 查看结果：回测完成后查看输出的风险指标

策略格式要求：
- 必须是策略编辑器格式（init + handle_bar）
- 不能在 init() 中下单
- 建议使用 handle_bar 手动判断月份调仓（scheduler.run_monthly 可能不触发）
- 使用 context.xxx 存储全局变量
- 使用 bar_dict[stock] 获取实时数据

常见问题：
1. 策略没有交易：检查 scheduler 是否触发，建议用 handle_bar 手动判断
2. 获取因子：使用 get_factor(stocks, "pe_ratio", start_date, end_date)
3. 涨停价：使用 history_bars(stock, 1, "1d", "limit_up")

参考文档：
- STRATEGY_EDITOR_GUIDE.md
- joinquant_to_ricequant_migration_guide.md
- ricequant_factor_list.md
- skills/ricequant_strategy/README.md
```

---

## 策略转换提示词

```
请帮我将策略编辑器格式的策略转换为 Notebook 格式，以便在 Notebook 中运行。

原始策略：
[粘贴原始策略代码]

转换规则：
1. 移除 initialize/handle_data 等策略框架函数
2. 将 context.current_dt 替换为手动指定的日期字符串（如 "2024-03-20"）
3. 将 run_daily/run_monthly 等定时任务改为手动调用函数
4. 添加 print 输出以便查看中间结果
5. 添加 try-except 捕获错误
6. 使用平台对应的 API 格式

转换后的策略格式：
```python
print("=== 策略测试开始 ===")

try:
    date = "2024-03-20"  # 手动指定日期
    
    # 选股逻辑（直接执行）
    stocks = your_selection_logic(date)
    print(f"选中股票: {len(stocks)}")
    
    # 计算收益（手动实现循环）
    results = []
    for stock in stocks:
        result = calculate_return(stock, date)
        results.append(result)
    
    print(f"平均收益: {np.mean(results):.2f}%")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("=== 测试完成 ===")
```

请生成转换后的代码。
```

---

## 迁移 JoinQuant 策略到 RiceQuant 提示词

```
请帮我将 JoinQuant 策略迁移到 RiceQuant，并生成 Notebook 格式的版本。

原始策略：
[粘贴 JoinQuant 策略代码]

迁移步骤：
1. 替换 API：
   - get_all_securities("stock", date) → all_instruments("CS")
   - get_index_stocks(code, date) → index_components(code)
   - get_price() → history_bars()
   - get_trade_days() → get_trading_dates()
   - valuation.* → fundamentals.eod_derivative_indicator.*

2. 转换为 Notebook 格式：
   - 移除 initialize/handle_data 框架
   - 手动指定日期
   - 添加 print 输出

3. 处理缺失因子：
   - jqfactor.technical_analysis.* → 手动计算技术指标
   - jqfactor.momentum.* → 手动计算动量
   - jqfactor.volatility.* → 手动计算波动率

4. 处理涨停价：
   - get_current_data()[stock].high_limit → history_bars(stock, 1, "1d", "limit_up")

请生成迁移后的代码。

参考文档：docs/backtest_guide/MIGRATION.md, docs/backtest_guide/API_DIFF.md
```

---

## 使用建议

1. **首次运行策略**：使用"标准提示词"
2. **快速运行已知策略**：使用"精简提示词"
3. **运行特定平台策略**：使用对应平台提示词
4. **精确回测（推荐）**：使用"RiceQuant 策略编辑器提示词"
5. **快速验证逻辑**：使用"RiceQuant Notebook 提示词"
6. **转换策略格式**：使用"策略转换提示词"
7. **跨平台迁移**：使用"迁移提示词"

请根据实际需求选择合适的提示词。

---

## 重要提醒

**Notebook 回测成功率关键因素：**

1. **策略格式**：必须是 Notebook 格式，不是策略编辑器格式
2. **平台 API**：使用正确的平台 API 格式
3. **超时时间**：复杂策略需要足够的超时时间
4. **print 输出**：必须有 print 才能看到结果
5. **Session 管理**：JoinQuant 需要手动抓取，RiceQuant 自动管理

**策略编辑器回测成功率关键因素：**

1. **策略格式**：必须是策略编辑器格式（init + handle_bar）
2. **定时任务**：scheduler.run_monthly 可能不触发，建议用 handle_bar 手动判断
3. **下单位置**：不能在 init() 中下单，只能在 handle_bar 或其他函数中下单
4. **全局变量**：使用 context.xxx 存储
5. **实时数据**：通过 bar_dict 参数获取
6. **Session 管理**：RiceQuant 自动管理（有效期 7 天）

**请务必检查以上因素后再运行。**