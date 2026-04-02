# 回测系统文档索引

## 核心文档

### 1. README.md - Notebook 回测系统指南
**主要内容：**
- Notebook 回测系统概述和核心优势
- 平台选择策略
- 快速开始指南
- 策略代码适配方法
- API 差异对比
- 参数说明
- 常见问题和最佳实践

**适用场景：** Notebook 回测、快速验证策略

### 2. STRATEGY_EDITOR_GUIDE.md - 策略编辑器回测指南 ⭐ NEW
**主要内容：**
- 策略编辑器 vs Notebook 对比
- RiceQuant 策略编辑器详细指南
- Session 自动管理
- 策略格式要求
- 运行回测命令
- 常见问题解决方案
- 最佳实践

**适用场景：** 精确回测、实盘前验证、JoinQuant 迁移

### 3. QUICK_START.md - 快速入门指南
**主要内容：**
- 一分钟快速开始
- 三种使用方式
- 策略代码格式对比
- 常见问题快速解决

**适用场景：** 快速上手、日常参考

### 4. API_DIFF.md - API 详细差异对比
**主要内容：**
- JoinQuant vs RiceQuant API 对照表
- 基础数据 API 差异
- 财务数据 API 差异
- 实时数据差异
- 因子库差异
- 缺失因子的手动计算方法
- 迁移建议

**适用场景：** 跨平台迁移、API 选择

### 5. PRE_RUN_CHECKLIST.md - 回测提交前检查规则 ⭐ 必读
**主要内容：**
- 时间区间建议
- 股票池筛选规则
- 多因子策略建议
- 超时时间设置
- 平台选择指南
- 数据获取优化
- 策略格式检查
- 分批运行长区间
- 日志输出规则
- 错误处理要求
- 提交前检查清单

**适用场景：** 提交回测前必读，避免超时、报错、资源浪费

### 6. MIGRATION.md - Notebook 迁移指南
**主要内容：**
- 迁移策略列表和优先级
- 详细迁移步骤
- 迁移示例代码
- 注意事项
- 不适合迁移的策略类型
- 迁移测试计划

**适用场景：** JoinQuant → RiceQuant Notebook 迁移

### 7. PROMPT.md - Agent 运行提示词
**主要内容：**
- 标准提示词（推荐）
- 精简提示词
- 平台专用提示词
- 策略转换提示词
- 迁移提示词
- 使用建议

**适用场景：** Agent 自动化运行测试

## 原始文档（参考）

### 6. ORIGINAL_SUMMARY.md - Notebook 回测总结
**来源：** `docs/notebook_backtest_summary.md`

**主要内容：**
- Notebook 方式回测的核心优势
- 平台对比
- 详细使用方式
- 策略代码适配示例
- 参数说明
- 示例策略

### 7. MIGRATION_PLAN.md - 迁移计划
**来源：** `docs/migration_plan.md`

**主要内容：**
- 5个策略的迁移列表
- 迁移优先级和时间评估
- 数据获取差异
- 注意事项

### 8. RICEQUANT_API_SUMMARY.md - RiceQuant API 能力总结
**来源：** `docs/ricequant_api_summary.md`

**主要内容：**
- RiceQuant 支持的因子列表
- 不支持的 JoinQuant 功能
- 手动计算缺失因子的方法
- Notebook 回测方式

### 9. RICEQUANT_TEST_SUMMARY.md - RiceQuant 测试总结报告
**来源：** `docs/ricequant_backtest_summary.md`

**主要内容：**
- 测试概览和详情
- 关键发现
- 测试结论
- 运行示例

### 10. ricequant_factors_guide.md - 平台因子使用指南 ⭐ NEW
**主要内容：**
- 平台直接提供的因子列表（无需计算）
- 需要自己计算的因子
- 平台因子 vs 自己计算对比
- 最佳实践建议
- 完整使用示例

**适用场景：** 查找因子、避免重复计算、提高效率

### 11. ricequant_notebooks_list.md - Notebook 列表汇总 ⭐ NEW
**主要内容：**
- 最新运行的所有 Notebook 列表
- 每个 Notebook 的详细信息
- 因子来源说明
- 使用提示

**适用场景：** 查看运行结果、访问在线 Notebook

### 12. UPDATE_LOG.md - 文档更新日志 ⭐ NEW
**主要内容：**
- 2026-03-31 更新详情
- 新增文档说明
- 重要发现总结
- 使用建议

**适用场景：** 了解文档更新、快速查找新功能

## 迁移指南（重要）

### JoinQuant → RiceQuant 完整迁移指南
**文件：** `joinquant_to_ricequant_migration_guide.md`

**主要内容：**
- 核心差异总览
- 初始化与配置
- 定时任务机制
- 数据获取 API 对照
- 交易函数 API 对照
- 持仓与账户信息
- 全局变量管理
- 完整迁移案例
- 常见问题与陷阱
- 迁移检查清单
- 实测验证要点
- **因子数据 API 对照** ⭐ 包含完整因子列表

**适用场景：** JoinQuant 策略迁移到 RiceQuant

### RiceQuant 因子列表速查
**文件：** `ricequant_factor_list.md`

**主要内容：**
- 估值类因子（pe_ratio, pb_ratio, market_cap 等）
- 盈利能力因子（roa, roe, gross_profit_margin 等）
- 成长能力因子（or_yoy, net_profit_yoy 等）
- 现金流因子（net_operate_cash_flow, free_cash_flow 等）
- 偿债能力因子（current_ratio, debt_to_asset_ratio 等）
- 每股指标因子（eps, bps, ocfps 等）
- JoinQuant 与 RiceQuant 因子名对照表

**适用场景：** 快速查找 RiceQuant 支持的因子

## Skill 目录文档

### JoinQuant Notebook
**目录：** `skills/joinquant_notebook/`

**关键文档：**
- `README.md` - 详细使用指南
- `QUICK_REFERENCE.md` - 快速参考
- `SKILL.md` - Skill 说明

### RiceQuant Notebook
**目录：** `skills/ricequant_strategy/`

**关键文档：**
- `README.md` - 详细使用指南
- `QUICK_REFERENCE.md` - 快速参考
- `SKILL.md` - Skill 说明
- `SESSION_MANAGEMENT.md` - Session 管理详情

## 文档关系图

```
docs/backtest_guide/
├── README.md                                    # Notebook 回测指南（必读）
├── STRATEGY_EDITOR_GUIDE.md                     # 策略编辑器回测指南（必读）⭐
├── PRE_RUN_CHECKLIST.md                         # 回测提交前检查规则（必读）⭐
├── joinquant_to_ricequant_migration_guide.md    # 完整迁移指南（重要）
├── ricequant_factor_list.md                     # 因子列表速查（重要）
├── QUICK_START.md                               # 快速入门（常用）
├── API_DIFF.md                                  # API 差异（迁移参考）
├── MIGRATION.md                                 # Notebook 迁移指南
├── PROMPT.md                                    # Agent 提示词（自动化必读）
├── ORIGINAL_SUMMARY.md                          # 原始总结（参考）
├── MIGRATION_PLAN.md                            # 迁移计划（参考）
├── RICEQUANT_API_SUMMARY.md                     # RiceQuant API（参考）
├── RICEQUANT_TEST_SUMMARY.md                    # RiceQuant 测试（参考）
└── INDEX.md                                     # 本文档

相关文档：
└── strategies/Ricequant/README.md               # RiceQuant API 对照表
```
docs/backtest_guide/
├── README.md                                    # Notebook 回测指南（必读）
├── STRATEGY_EDITOR_GUIDE.md                     # 策略编辑器回测指南（必读）⭐
├── joinquant_to_ricequant_migration_guide.md    # 完整迁移指南（重要）
├── ricequant_factor_list.md                     # 因子列表速查（重要）
├── ricequant_factors_guide.md                   # 平台因子使用指南 ⭐ NEW
├── ricequant_notebooks_list.md                  # Notebook 列表汇总 ⭐ NEW
├── UPDATE_LOG.md                                # 文档更新日志 ⭐ NEW
├── QUICK_START.md                               # 快速入门（常用）
├── API_DIFF.md                                  # API 差异（迁移参考）
├── MIGRATION.md                                 # Notebook 迁移指南
├── PROMPT.md                                    # Agent 提示词（自动化必读）
├── ORIGINAL_SUMMARY.md                          # 原始总结（参考）
├── MIGRATION_PLAN.md                            # 迁移计划（参考）
├── RICEQUANT_API_SUMMARY.md                     # RiceQuant API（参考）
├── RICEQUANT_TEST_SUMMARY.md                    # RiceQuant 测试（参考）
└── INDEX.md                                     # 本文档

相关文档：
└── strategies/Ricequant/README.md               # RiceQuant API 对照表
```

## 使用建议

| 用户场景 | 推荐文档顺序 |
|---------|------------|
| **首次使用 Notebook** | README.md → QUICK_START.md → 运行示例 |
| **首次使用策略编辑器** | STRATEGY_EDITOR_GUIDE.md → 运行示例 |
| **提交回测前** | PRE_RUN_CHECKLIST.md ⭐ 必读 |
| **日常使用** | QUICK_START.md 或 STRATEGY_EDITOR_GUIDE.md |
| **跨平台迁移** | STRATEGY_EDITOR_GUIDE.md → joinquant_to_ricequant_migration_guide.md |
| **查找因子** | ricequant_factor_list.md |
| **Agent 自动化** | PROMPT.md → README.md |
| **故障排查** | STRATEGY_EDITOR_GUIDE.md（常见问题部分） |
| **深入理解** | 所有文档 |

## 快速查找

| 问题 | 查找位置 |
|------|---------|
| 如何开始 Notebook？ | README.md 或 QUICK_START.md |
| 如何开始策略编辑器？ | STRATEGY_EDITOR_GUIDE.md |
| 提交回测前要检查什么？ | PRE_RUN_CHECKLIST.md ⭐ |
| 如何选择时间区间？ | PRE_RUN_CHECKLIST.md（时间区间建议） |
| 如何设置超时时间？ | PRE_RUN_CHECKLIST.md（超时时间设置） |
| 如何选择平台？ | STRATEGY_EDITOR_GUIDE.md（平台选择） |
| 如何转换策略格式？ | README.md（策略代码适配） + PROMPT.md（策略转换提示词） |
| API 如何替换？ | API_DIFF.md 或 joinquant_to_ricequant_migration_guide.md |
| 如何迁移策略？ | joinquant_to_ricequant_migration_guide.md |
| Session 过期怎么办？ | STRATEGY_EDITOR_GUIDE.md（常见问题） |
| 超时怎么办？ | PRE_RUN_CHECKLIST.md（Q1: 回测超时怎么办） |
| 无输出怎么办？ | README.md（常见问题） |
| 策略没有交易？ | STRATEGY_EDITOR_GUIDE.md（常见问题 Q2） |
| 如何获取因子？ | ricequant_factor_list.md 或 STRATEGY_EDITOR_GUIDE.md（常见问题 Q3） |
| Agent 如何运行？ | PROMPT.md |

## 文档更新

- 2026-03-31：
  - 创建整合文档
  - 新增 `ricequant_factors_guide.md` - 平台因子使用指南
  - 新增 `ricequant_notebooks_list.md` - Notebook 列表汇总
  - 更新 INDEX.md 添加新文档索引
- 来源文档已保留在 `ORIGINAL_*.md` 文件中