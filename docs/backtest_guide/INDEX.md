# Notebook 回测系统文档索引

## 核心文档

### 1. README.md - 综合使用指南
**主要内容：**
- 系统概述和核心优势
- 平台选择策略
- 快速开始指南
- 策略代码适配方法
- API 差异对比
- 参数说明
- 常见问题和最佳实践

**适用场景：** 首次了解系统、全面了解功能

### 2. QUICK_START.md - 快速入门指南
**主要内容：**
- 一分钟快速开始
- 三种使用方式
- 策略代码格式对比
- 常见问题快速解决

**适用场景：** 快速上手、日常参考

### 3. API_DIFF.md - API 详细差异对比
**主要内容：**
- JoinQuant vs RiceQuant API 对照表
- 基础数据 API 差异
- 财务数据 API 差异
- 实时数据差异
- 因子库差异
- 缺失因子的手动计算方法
- 迁移建议

**适用场景：** 跨平台迁移、API 选择

### 4. MIGRATION.md - 迁移指南
**主要内容：**
- 迁移策略列表和优先级
- 详细迁移步骤
- 迁移示例代码
- 注意事项
- 不适合迁移的策略类型
- 迁移测试计划

**适用场景：** JoinQuant → RiceQuant 迁移

### 5. PROMPT.md - Agent 运行提示词
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
├── README.md                 # 综合指南（必读）
├── QUICK_START.md            # 快速入门（常用）
├── API_DIFF.md               # API 差异（迁移参考）
├── MIGRATION.md              # 迁移指南（迁移必读）
├── PROMPT.md                 # Agent 提示词（自动化必读）
├── ORIGINAL_SUMMARY.md       # 原始总结（参考）
├── MIGRATION_PLAN.md         # 迁移计划（参考）
├── RICEQUANT_API_SUMMARY.md  # RiceQuant API（参考）
├── RICEQUANT_TEST_SUMMARY.md # RiceQuant 测试（参考）
└── INDEX.md                  # 本文档
```

## 使用建议

| 用户场景 | 推荐文档顺序 |
|---------|------------|
| **首次使用** | README.md → QUICK_START.md → 运行示例 |
| **日常使用** | QUICK_START.md |
| **跨平台迁移** | README.md → API_DIFF.md → MIGRATION.md |
| **Agent 自动化** | PROMPT.md → README.md |
| **故障排查** | README.md（常见问题部分） |
| **深入理解** | 所有文档 |

## 快速查找

| 问题 | 查找位置 |
|------|---------|
| 如何开始？ | QUICK_START.md |
| 如何选择平台？ | README.md（平台选择策略） |
| 如何转换策略格式？ | README.md（策略代码适配） + PROMPT.md（策略转换提示词） |
| API 如何替换？ | API_DIFF.md |
| 如何迁移？ | MIGRATION.md |
| Session 过期怎么办？ | README.md（常见问题） |
| 超时怎么办？ | README.md（常见问题） |
| 无输出怎么办？ | README.md（常见问题） |
| Agent 如何运行？ | PROMPT.md |

## 文档更新

- 2026-03-31：创建整合文档
- 来源文档已保留在 `ORIGINAL_*.md` 文件中