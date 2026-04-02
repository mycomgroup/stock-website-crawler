# 回测提交前检查规则

> 更新时间：2026-03-31
> 用途：提交回测前必读，避免超时、报错、资源浪费

---

## 一、时间区间建议

| 策略类型 | 首次验证 | 完整回测 | 说明 |
|---------|---------|---------|------|
| 简单策略 | 1-3个月 | 1-3年 | 快速验证逻辑 |
| 中等策略 | 1-3个月 | 1-2年 | 逐步扩展 |
| 复杂策略 | 1个月 | 分批运行 | 每次半年，合并结果 |

**规则：**
- ✅ 首次验证用 1-3 个月，确认逻辑正确
- ✅ 1年回测通常几分钟，可以接受
- ✅ 超过2年建议分批运行（如2020-2021, 2021-2022, 2022-2023）
- ❌ 不要首次验证就用5年数据

**示例：**
```bash
# 首次验证
node run-skill.js --id 123 --file strategy.py --start 2024-01-01 --end 2024-03-31

# 验证通过后扩展
node run-skill.js --id 123 --file strategy.py --start 2022-01-01 --end 2024-12-31
```

---

## 二、股票池筛选

**问题：** 全市场4000+只股票循环会超时

**解决方案：**
- ✅ 根据策略逻辑先筛选股票池
  - 例如：沪深300成分股（300只）
  - 例如：市值>50亿的股票（可能500只）
  - 例如：排除ST、停牌、新股
- ❌ 不要简单截断 `stocks[:500]`，这会破坏策略逻辑
- ✅ 在选股阶段就减少候选股票

**正确示例：**
```python
# 正确：先筛选再处理
all_stocks = all_instruments("CS")["order_book_id"].tolist()
stocks = [s for s in all_stocks if not s.startswith("688")]  # 排除科创板
stocks = filter_by_market_cap(stocks, min_cap=5000000000)    # 市值筛选
stocks = filter_by_trading(stocks, bar_dict)                 # 剔除停牌

# 错误：简单截断
stocks = all_stocks[:500]  # 破坏策略逻辑！
```

---

## 三、多因子策略

| 因子数量 | 建议 | 说明 |
|---------|------|------|
| 1-3个因子 | 无限制 | 平台API支持良好 |
| 4-5个因子 | 正常 | 大多数策略范围 |
| 6-10个因子 | 需注意 | 模型复杂度增加 |
| >10个因子 | 建议精简 | 可能过拟合 |

**说明：**
- 平台提供了几百个因子，获取计算不是问题
- 问题在于因子太多会导致：
  - 模型过拟合
  - 解释性变差
  - 维护困难
- ✅ 建议使用核心因子（<10个）

---

## 四、超时时间设置

| 策略类型 | 建议超时 | 最大超时 |
|---------|---------|---------|
| 简单策略 | 60-120秒 | 300秒 |
| 中等策略 | 120-300秒 | 600秒 |
| 复杂策略 | 300-600秒 | 1200秒（20分钟） |
| 超长回测 | 600-1200秒 | 3600秒（1小时） |

**规则：**
- ✅ 首次运行设置较短超时（120秒）
- ✅ 根据实际运行时间调整
- ✅ 超时后可以增加时间重跑

**示例：**
```bash
# 首次运行
node run-skill.js --id 123 --file strategy.py --start 2024-01-01 --end 2024-03-31

# 复杂策略增加超时
node run-strategy.js --strategy complex.py --timeout-ms 600000  # 10分钟
```

---

## 五、平台选择

| 场景 | 推荐平台 | 说明 |
|------|---------|------|
| 快速验证逻辑 | Notebook（任一平台） | 无时间限制 |
| 需要交互调试 | Notebook | 可以逐步执行 |
| JoinQuant特殊因子 | JoinQuant Notebook | jqfactor支持 |
| 简单因子策略 | RiceQuant（Notebook或策略编辑器） | 都可以 |
| 需要风险指标 | 策略编辑器 | 自动计算 |
| 实盘前验证 | 策略编辑器 | 精确回测 |

**说明：**
- 根据实际需求选择，不是"精确回测就用RiceQuant"
- JoinQuant 策略编辑器也可以精确回测
- RiceQuant 策略编辑器也可以精确回测
- Notebook 适合验证逻辑

---

## 六、数据获取优化

| 检查项 | 建议 |
|--------|------|
| 批量获取因子 | ✅ `get_factor(stocks, factors, ...)` |
| 避免循环获取 | ❌ 不要在循环中 `get_factor([stock], ...)` |
| 历史数据长度 | ✅ 合理设置 count（20-60） |
| 缓存结果 | ✅ 存到 `context.xxx` 避免重复获取 |

**正确示例：**
```python
# 正确：批量获取
factors = ["pe_ratio", "pb_ratio", "roa"]
data = get_factor(stocks, factors, start_date, end_date)

# 错误：循环获取
for stock in stocks:
    data = get_factor([stock], "pe_ratio", ...)  # 很慢！
```

---

## 七、策略格式检查

### Notebook 回测

- ✅ 直接执行代码 + print输出
- ✅ try-except 错误处理
- ❌ 不要用 init/handle_bar 格式

**正确格式：**
```python
print("=== 策略测试开始 ===")

try:
    date = "2024-03-20"
    stocks = all_instruments("CS")["order_book_id"].tolist()
    print(f"股票数: {len(stocks)}")
    
    # 策略逻辑
    result = your_logic(stocks)
    print(f"结果: {result}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("=== 测试完成 ===")
```

### 策略编辑器回测

- ✅ `init(context)` 初始化
- ✅ `handle_bar(context, bar_dict)` 主循环
- ❌ 不要在 init 中下单
- ⚠️ `scheduler.run_monthly` 可能不触发，建议手动判断

**正确格式：**
```python
def init(context):
    context.last_rebalance_month = -1
    logger.info("策略初始化")

def handle_bar(context, bar_dict):
    today = context.now
    
    # 手动判断月份
    if context.last_rebalance_month != today.month:
        context.last_rebalance_month = today.month
        rebalance(context, bar_dict)

def rebalance(context, bar_dict):
    logger.info(f"调仓: {today.date()}")
    # 交易逻辑
```

---

## 八、分批运行长区间

**需要超过2年回测时：**

```bash
# 方案1：分批运行
# 第1批
node run-skill.js --id 123 --file strategy.py --start 2020-01-01 --end 2021-12-31

# 第2批
node run-skill.js --id 123 --file strategy.py --start 2022-01-01 --end 2023-12-31

# 第3批
node run-skill.js --id 123 --file strategy.py --start 2024-01-01 --end 2024-12-31

# 然后手动合并结果
```

**策略优化：**
```python
# 原策略：每月调仓，回测3年 = 36次调仓
scheduler.run_monthly(rebalance, monthday=1)

# 改为：每季度调仓，回测3年 = 12次调仓
def handle_bar(context, bar_dict):
    if context.now.day <= 3 and context.now.month in [1, 4, 7, 10]:
        rebalance(context, bar_dict)
```

---

## 九、日志输出

**规则：**
- ✅ 输出关键步骤：选股数量、调仓日期、买卖股票
- ✅ 输出中间结果：因子计算完成、筛选完成
- ❌ 不要在循环中每条都输出（4000只股票 × print = 爆炸）
- ✅ 进度输出：每100只输出一次

**正确示例：**
```python
# 正确
print(f"候选股票: {len(candidates)}")
print(f"筛选后: {len(selected)}")
for i, stock in enumerate(selected):
    if i % 100 == 0:
        logger.info(f"处理进度: {i}/{len(selected)}")

# 错误
for stock in stocks:  # 4000只
    print(f"处理: {stock}")  # 日志爆炸！
```

---

## 十、错误处理

**必须包含：**

```python
try:
    # 主要逻辑
    result = your_logic()
    print(f"结果: {result}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
```

**常见错误及处理：**

| 错误类型 | 原因 | 解决方案 |
|---------|------|---------|
| `NoneType` | 数据获取失败 | 检查返回值是否为 None |
| `KeyError` | 字典键不存在 | 使用 `.get(key, default)` |
| `IndexError` | 数组越界 | 检查长度再访问 |
| `TimeoutError` | 超时 | 增加超时时间或减少数据量 |

---

## 检查清单（提交前确认）

### ⏰ 时间区间
- [ ] 首次验证：1-3个月
- [ ] 完整回测：1-3年
- [ ] 超过2年：考虑分批

### 📊 股票池
- [ ] 已根据策略筛选股票池
- [ ] 没有简单截断 `stocks[:N]`
- [ ] 股票数量合理（<1000）

### 🔢 因子数量
- [ ] 核心因子 < 10个
- [ ] 批量获取，不循环

### ⏱️ 超时设置
- [ ] 已设置合理的超时时间
- [ ] 首次运行：120秒
- [ ] 复杂策略：300-600秒

### 🖥️ 平台选择
- [ ] 根据需求选择了合适的平台
- [ ] Notebook用于验证，策略编辑器用于精确回测

### 💻 代码质量
- [ ] 格式正确（Notebook或策略编辑器）
- [ ] 有错误处理
- [ ] 有日志输出
- [ ] 没有循环中频繁输出

### 📝 数据获取
- [ ] 批量获取因子
- [ ] 不在循环中获取数据
- [ ] 历史数据长度合理

---

## 快速参考

### 最小化验证策略

```bash
# 1个月回测，快速验证
node run-skill.js --id 123 --file strategy.py \
  --start 2024-03-01 --end 2024-03-31 \
  --capital 100000
```

### 标准回测命令

```bash
# 1年回测，标准超时
node run-skill.js --id 123 --file strategy.py \
  --start 2024-01-01 --end 2024-12-31 \
  --capital 100000 --benchmark 000300.XSHG
```

### 复杂策略命令

```bash
# 增加超时时间
node run-strategy.js --strategy complex.py \
  --timeout-ms 600000 \
  --create-new
```

---

## 常见问题

### Q1: 回测超时怎么办？

**解决方案：**
1. 缩短时间区间（1年 → 6个月）
2. 减少股票数量（筛选后再处理）
3. 增加超时时间（120秒 → 300秒）
4. 优化代码（批量获取、缓存结果）

### Q2: 策略没有交易记录？

**检查项：**
1. `scheduler.run_monthly` 是否触发
2. 选股条件是否太严格
3. 股票是否都涨停/停牌
4. 是否在 init 中下单（错误）

### Q3: 内存溢出怎么办？

**解决方案：**
1. 分批处理：`for i in range(0, len(stocks), 100)`
2. 使用生成器替代列表
3. 及时释放不用的变量
4. 避免创建过大的中间结果

### Q4: 日志太多看不清？

**解决方案：**
1. 减少循环中的输出
2. 只输出关键信息
3. 使用进度输出：每100条输出一次
4. 清理不必要的调试信息

---

## 相关文档

- `README.md` - Notebook 回测指南
- `STRATEGY_EDITOR_GUIDE.md` - 策略编辑器回测指南
- `joinquant_to_ricequant_migration_guide.md` - 完整迁移指南
- `ricequant_factor_list.md` - 因子列表速查

---

*最后更新: 2026-03-31*
*用途: 提交回测前必读*