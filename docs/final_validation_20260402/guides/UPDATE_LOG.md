# 回测系统文档更新日志

## 2026-03-31 更新

### 📝 新增文档

#### 1. **ricequant_factors_guide.md** - 平台因子使用指南 ⭐⭐⭐

**核心问题回答**：
> "因子能不能取平台已有的？还要每个都算一下吗？"

**主要内容**：
- ✅ **平台直接提供的因子**（无需计算）
  - 财务因子：市值、PE、PB、ROE、营收增长...
  - 价格因子：涨停价、开盘价、收盘价...
  - 估值因子：换手率、市盈率、市净率...
  
- ⚠️ **需要简单计算的因子**
  - 动量因子、量比因子、开盘涨幅...
  
- 💡 **最佳实践建议**
  - 优先使用平台财务因子
  - 避免重复造轮子
  - 提高效率和准确性

**关键结论**：
> RiceQuant 提供了丰富的财务和估值因子，无需自己计算！
> 优先使用平台能力，提高效率！

**适用场景**：
- 选择因子来源
- 避免重复计算
- 提高开发效率

---

#### 2. **ricequant_notebooks_list.md** - Notebook 列表汇总 ⭐⭐

**核心问题回答**：
> "能重新提交一下运行？并告诉我在 Ricequant 上面的 notebook 名吗？"

**主要内容**：
- 📊 **最新运行的所有 Notebook 列表**
  - 5个成功运行的 Notebook
  - 每个 Notebook 的详细信息
  - 在线访问链接
  
- 📍 **因子来源说明**
  - RiceQuant API 数据源
  - 本地计算因子
  - 使用示例

- 🔍 **快速访问**
  - RiceQuant Notebook 主页
  - 推荐 Notebook 链接

**关键信息**：
- 最新 Notebook：`策略测试_20260331_155250.ipynb`（最完整回测结果）
- 所有 Notebook 都可以在线查看和运行

**适用场景**：
- 查看运行结果
- 访问在线 Notebook
- 了解因子来源

---

### 🔄 更新的文档

#### INDEX.md - 文档索引

**新增内容**：
- 添加 `ricequant_factors_guide.md` 索引
- 添加 `ricequant_notebooks_list.md` 索引
- 更新快速查找表
- 更新文档关系图

#### README.md - Notebook 回测系统指南

**新增内容**：
- 添加对新文档的引用
- 添加因子信息快捷链接

---

## 📚 文档结构总览

```
skills/backtest_guide/SKILL.md
├── README.md                                    # Notebook 回测指南
├── STRATEGY_EDITOR_GUIDE.md                     # 策略编辑器回测指南 ⭐
├── joinquant_to_ricequant_migration_guide.md    # 完整迁移指南
├── ricequant_factor_list.md                     # 因子列表速查
├── ricequant_factors_guide.md                   # 平台因子使用指南 ⭐ NEW
├── ricequant_notebooks_list.md                  # Notebook 列表汇总 ⭐ NEW
├── QUICK_START.md                               # 快速入门
├── API_DIFF.md                                  # API 差异
├── MIGRATION.md                                 # Notebook 迁移指南
├── PROMPT.md                                    # Agent 提示词
├── ORIGINAL_SUMMARY.md                          # 原始总结
├── MIGRATION_PLAN.md                            # 迁移计划
├── RICEQUANT_API_SUMMARY.md                     # RiceQuant API
├── RICEQUANT_TEST_SUMMARY.md                    # RiceQuant 测试
├── UPDATE_LOG.md                                # 本文档 ⭐ NEW
└── INDEX.md                                     # 文档索引
```

---

## 🎯 快速查找指南

### 新增文档查找

| 问题 | 文档 | 位置 |
|------|------|------|
| **哪些因子平台提供？** | ricequant_factors_guide.md | 第1节 |
| **因子要不要自己算？** | ricequant_factors_guide.md | 第3节 |
| **如何使用平台因子？** | ricequant_factors_guide.md | 第5节 |
| **查看运行的 Notebook？** | ricequant_notebooks_list.md | 第2节 |
| **访问在线 Notebook？** | ricequant_notebooks_list.md | 第2节 |
| **因子从哪里来的？** | ricequant_notebooks_list.md | 第3节 |

### 现有文档查找

| 问题 | 文档 |
|------|------|
| 如何开始？ | QUICK_START.md 或 README.md |
| 如何迁移？ | joinquant_to_ricequant_migration_guide.md |
| 如何选择平台？ | STRATEGY_EDITOR_GUIDE.md |
| API 差异？ | API_DIFF.md |
| Agent 运行？ | PROMPT.md |

---

## 💡 重要发现

### 1. **平台因子能力**

RiceQuant 平台提供了丰富的因子，**大部分无需自己计算**：

**✅ 直接使用**：
- 财务因子：市值、ROE、营收增长...
- 估值因子：PE、PB、换手率...
- 价格因子：涨停价、开盘价...

**⚠️ 简单计算**：
- 动量因子：`(close[-1] / close[0] - 1) * 100`
- 量比因子：`mean(volume[-5:]) / mean(volume)`

### 2. **最佳实践**

**推荐做法**：
```python
# ✅ 使用平台财务因子
market_cap = get_fundamentals(query(fundamentals.eod_market_cap), date)

# ✅ 使用平台涨停价
limit_up = history_bars(stock, 1, "1d", ["limit_up"])

# ⚠️ 简单因子自己算
momentum = (close[-1] / close[0] - 1) * 100
```

**不推荐做法**：
```python
# ❌ 不要自己计算市值
price = get_price(stock)
shares = get_shares(stock)  # 需要额外查询
market_cap = price * shares  # 容易出错
```

### 3. **测试结果**

成功运行的 Notebook：
- 5个 Notebook 全部成功创建
- 3个 Notebook 成功返回输出
- 最完整结果：龙头离场规则测试（卡玛比率 68.34）

---

## 📈 使用建议

### 新用户

**推荐阅读顺序**：
1. `INDEX.md` - 了解文档结构
2. `QUICK_START.md` - 快速上手
3. `ricequant_factors_guide.md` - 了解因子使用 ⭐ NEW
4. `README.md` - 深入学习

### 开发者

**推荐工作流**：
1. **查看因子**：`ricequant_factors_guide.md` ⭐ NEW
2. **开发策略**：使用平台因子
3. **运行回测**：查看 `ricequant_notebooks_list.md` ⭐ NEW
4. **查看结果**：访问在线 Notebook

### 迁移用户

**推荐步骤**：
1. `joinquant_to_ricequant_migration_guide.md` - 了解差异
2. `ricequant_factors_guide.md` - 选择因子 ⭐ NEW
3. `ricequant_factor_list.md` - 查找因子
4. 运行测试

---

## 🔗 相关链接

### RiceQuant 平台

- **Notebook 主页**: https://www.ricequant.com/research/user/user_497381/tree
- **最新 Notebook**: https://www.ricequant.com/research/user/user_497381/notebooks/%E7%AD%96%E7%95%A5%E6%B5%8B%E8%AF%95_20260331_155250.ipynb

### 本地文档

- **因子指南**: `ricequant_factors_guide.md`
- **Notebook 列表**: `ricequant_notebooks_list.md`
- **完整索引**: `INDEX.md`

---

## 📝 后续计划

### 待补充

- [ ] 更多策略示例
- [ ] 因子性能对比
- [ ] 常见错误解决方案
- [ ] 优化建议

### 待更新

- [ ] 根据使用反馈更新
- [ ] 添加更多 Notebook 示例
- [ ] 补充因子计算示例

---

**更新时间**: 2026-03-31  
**更新内容**: 新增因子使用指南和 Notebook 列表  
**状态**: ✅ 完成