# Agent 运行 Notebook 回测提示词

以下提示词用于指导 Agent 正确运行 Notebook 回测，请复制使用：

---

## 标准提示词（推荐使用）⭐

```
我需要运行量化策略的回测。请按照以下步骤操作：

**1. 确认策略所处阶段**

请先分析我的策略，判断当前处于哪个开发阶段：

**阶段判断规则（关键）：**

| 阶段 | 场景特征 | 推荐平台 | 优先级 |
|------|---------|---------|--------|
| **阶段1：初步调研** | 探索新想法、验证概念可行性 | JoinQuant Notebook | 低 |
| **阶段2：新策略开发** | 因子简单（基础因子），新写的策略 | **RiceQuant Notebook** | 高 ⭐ |
| **阶段3：完整回测** | 策略逻辑较完整，需要风险指标 | **RiceQuant 策略编辑器** | 高 ⭐ |
| **阶段4：最终验证** | 成熟策略，需要精确结果 | JoinQuant Strategy | 必做 |

**关键判断标准：**
- ✅ 如果因子简单（仅用 PE/PB/ROA/ROE/市值等），**优先 RiceQuant**（减少迁移成本）
- ✅ 如果是新策略且因子简单，**用 RiceQuant Notebook**（Session自动管理）
- ✅ 如果策略逻辑较完整，**用 RiceQuant 策略编辑器**（完整回测）
- ✅ 如果策略已成熟，**最后必须用 JoinQuant Strategy** 验证
- ❌ 如果因子复杂（jqfactor特殊因子），必须用 JoinQuant

**默认优先选择：**
- 新策略 + 简单因子 → **RiceQuant Notebook**（推荐）
- 完整策略 + 简单因子 → **RiceQuant 策略编辑器**（推荐）
- 复杂因子 → JoinQuant Notebook

**2. 进入正确的 Skill 目录**

根据阶段选择，进入对应目录：
- JoinQuant Notebook: `cd skills/joinquant_notebook`
- RiceQuant Notebook 或策略编辑器: `cd skills/ricequant_strategy`

**3. 确认策略格式（根据阶段）**

**Notebook 格式（阶段1-2）：**
```python
print("=== 策略测试开始 ===")

try:
    date = "2024-03-20"
    stocks = get_all_securities("stock", date)  # JoinQuant
    # 或 stocks = all_instruments("CS")  # RiceQuant
    
    result = your_logic(stocks)
    print(f"结果: {result}")
    
except Exception as e:
    print(f"错误: {e}")

print("=== 测试完成 ===")
```

**策略编辑器格式（阶段3-4）：**
```python
# RiceQuant 格式：
def init(context):
    context.month_count = 0
    
def handle_bar(context, bar_dict):
    # 手动判断月份调仓（scheduler可能不触发）
    current_month = context.now.month
    if context.month_count == 0 or current_month != context.last_month:
        rebalance(context, bar_dict)
        context.last_month = current_month
        context.month_count += 1

# JoinQuant 格式：
def initialize(context):
    run_monthly(rebalance, 1)
    
def handle_data(context, data):
    ...
```

**格式选择建议：**
- 阶段1-2：Notebook格式（无时间限制，快速验证）
- 阶段3：RiceQuant策略编辑器格式（完整回测框架）
- 阶段4：JoinQuant策略编辑器格式（最终验证）

**4. 运行策略（根据阶段）**

**JoinQuant Notebook（阶段1）：**
```bash
cd skills/joinquant_notebook
node run-strategy.js --strategy your_strategy.py --timeout-ms 120000
```

**RiceQuant Notebook（阶段2 - 推荐）：**
```bash
cd skills/ricequant_strategy
node run-strategy.js --strategy your_strategy.py --create-new --timeout-ms 120000
```

**RiceQuant 策略编辑器（阶段3 - 推荐）：**
```bash
cd skills/ricequant_strategy
node run-skill.js --id <strategyId> --file ./strategy.py --start 2024-01-01 --end 2024-12-31
node fetch-report.js --id <backtestId> --full  # 获取完整报告
```

**JoinQuant Strategy（阶段4）：**
```bash
# 待完善，目前建议直接在网页平台运行
```

**优先推荐：**
- 新策略验证：**RiceQuant Notebook**（阶段2）
- 完整策略回测：**RiceQuant 策略编辑器**（阶段3）

**5. 增加超时时间**

如果策略涉及大量数据或计算，请增加超时时间：
```bash
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000  # 5分钟
node run-strategy.js --strategy your_strategy.py --timeout-ms 600000  # 10分钟
```

**6. 查看和解读结果（根据阶段）**

- JoinQuant Notebook: `cat output/joinquant-notebook-result-*.json`
- RiceQuant Notebook: `cat data/ricequant-notebook-result-*.json`
- RiceQuant 策略编辑器: `node fetch-report.js --id <backtestId> --full`

**结果解读：**
- Notebook：看 print 输出内容，有输出说明运行成功
- 策略编辑器：看风险指标（年化收益、夏普比率、最大回撤等）
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
- 总体指南: `skills/backtest_guide/SKILL.md`
- 快速入门: `skills/backtest_guide/SKILL.md`
- API差异: `skills/backtest_guide/SKILL.md`
- 迁移指南: `skills/backtest_guide/SKILL.md`
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

参考文档：skills/backtest_guide/SKILL.md
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

参考文档：skills/backtest_guide/SKILL.md, skills/joinquant_notebook/README.md
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

参考文档：skills/backtest_guide/SKILL.md, skills/ricequant_strategy/README.md
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

参考文档：skills/backtest_guide/SKILL.md, skills/backtest_guide/SKILL.md
```

---

## 使用建议

**根据策略开发阶段选择提示词：**

| 阶段 | 场景 | 推荐提示词 |
|------|------|-----------|
| **阶段1** | 初步调研探索 | "标准提示词" 或 "JoinQuant Notebook 提示词" |
| **阶段2** | 新策略开发（简单因子） | **"标准提示词"（重点）** 或 "RiceQuant Notebook 提示词" ⭐ |
| **阶段3** | 完整策略回测 | **"标准提示词"（重点）** 或 "RiceQuant 策略编辑器提示词" ⭐ |
| **阶段4** | 最终验证 | "JoinQuant Strategy 提示词"（待完善） |

**典型使用流程：**
```
新策略（简单因子）：
  1. 用"标准提示词" → RiceQuant Notebook（阶段2）
  2. 效果好 → 用"RiceQuant 策略编辑器提示词"（阶段3）
  3. 成熟后 → JoinQuant Strategy 最终验证（阶段4）

复杂因子策略：
  1. 用"JoinQuant Notebook 提示词"（阶段1）
  2. 继续在 JoinQuant Notebook 开发
  3. 成熟后 → JoinQuant Strategy 最终验证（阶段4）
```

请根据实际需求选择合适的提示词。

---

## 重要提醒

**四阶段策略开发流程（关键）：**

```
阶段1（初步调研）: JoinQuant Notebook → 探索验证
阶段2（新策略开发）: RiceQuant Notebook → 快速开发（推荐）⭐
阶段3（完整回测）: RiceQuant 策略编辑器 → 完整回测（推荐）⭐
阶段4（最终验证）: JoinQuant Strategy → 最终验证
```

**默认优先选择（新策略）：**
- 简单因子新策略 → **RiceQuant Notebook**（阶段2）
- 完整策略 → **RiceQuant 策略编辑器**（阶段3）
- 成熟策略 → **JoinQuant Strategy**（阶段4）

**关键成功因素：**

**阶段1-2（Notebook）：**
1. 策略格式：Notebook格式（直接执行 + print）
2. 平台 API：使用正确的平台 API 格式
3. 超时时间：复杂策略增加 timeout-ms
4. print 输出：必须有 print 才能看到结果
5. Session 管理：JoinQuant 手动抓取，RiceQuant 自动管理

**阶段3（RiceQuant 策略编辑器）：**
1. 策略格式：策略编辑器格式（init + handle_bar）
2. 定时任务：scheduler 可能不触发，建议用 handle_bar 手动判断月份
3. 下单位置：不能在 init() 中下单
4. 全局变量：使用 context.xxx 存储
5. 实时数据：通过 bar_dict 参数获取

**阶段4（JoinQuant Strategy）：**
1. 策略格式：策略编辑器格式（initialize + handle_data）
2. 直接在网页平台运行，最权威验证

**请务必按四阶段流程运行，不要只停留在阶段1。**