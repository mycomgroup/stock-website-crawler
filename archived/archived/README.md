# Stock Crawler 归档文件

这个文件夹包含了项目开发过程中的历史文件，包括任务总结、迁移脚本和调研文档。

## 📁 目录结构

```
archived/
├── README.md                          # 本文件
├── 调研完成总结.md                    # 数据质量调研总结
├── 两个任务完成总结.md                # 两个任务完成总结
├── QFII_TAB_FIX_SUMMARY.md           # QFII Tab提取修复总结
├── scripts/                           # 历史脚本
│   ├── migrate-links.js              # 链接迁移脚本
│   ├── migrate-output.js             # 输出迁移脚本
│   ├── migrate-status-names.js       # 状态名称迁移脚本
│   ├── reset-cpi-link.js             # 重置CPI链接
│   ├── reset-wiki-link.js            # 重置Wiki链接
│   ├── reset-wiki-list-link.js       # 重置Wiki列表链接
│   ├── add-source-url-to-pages.js    # 添加源URL到页面
│   └── clean-anchors.js              # 清理锚点
└── doc/                               # 历史文档
    ├── TASK1_UNDEFINED_FIX_COMPLETED.md      # 任务1完成文档
    ├── TASK2_FILENAME_STRATEGY_COMPLETED.md  # 任务2完成文档
    ├── DATA_QUALITY_RESEARCH_SUMMARY.md      # 数据质量调研总结
    ├── UNDEFINED_URL_ISSUE.md                # Undefined URL问题
    ├── FILENAME_STRATEGY.md                  # 文件名策略
    ├── STATUS_FIELD_MIGRATION.md             # 状态字段迁移
    ├── README_RESEARCH.md                    # README调研
    └── CHANGELOG.md                          # 变更日志
```

## 📝 文件说明

### 任务总结文档

#### 调研完成总结.md
- **内容**: 数据质量调研的完整总结
- **时间**: 2024年初
- **主要内容**: 
  - 分析了188个markdown文件和3,006张图片
  - 识别了3个问题领域
  - 提出了改进建议

#### 两个任务完成总结.md
- **内容**: 两个重要任务的完成总结
- **任务1**: 修复undefined URL问题（删除230个无效链接）
- **任务2**: 实施新文件名策略（长度减少49%）

#### QFII_TAB_FIX_SUMMARY.md
- **内容**: QFII页面Tab提取问题的修复总结
- **改进**: 实施了三层Tab检测策略
- **效果**: 能够识别自定义Tab实现

### 历史脚本

#### 迁移脚本
- `migrate-links.js` - 链接数据结构迁移
- `migrate-output.js` - 输出目录结构迁移
- `migrate-status-names.js` - 状态字段名称迁移

这些脚本用于项目早期的数据结构调整，现在已经不再需要。

#### 重置脚本
- `reset-cpi-link.js` - 重置CPI相关链接状态
- `reset-wiki-link.js` - 重置Wiki链接状态
- `reset-wiki-list-link.js` - 重置Wiki列表链接状态

这些脚本用于特定链接的状态重置，属于一次性操作。

#### 工具脚本
- `add-source-url-to-pages.js` - 批量添加源URL到已生成的页面
- `clean-anchors.js` - 清理URL中的锚点

这些脚本用于批量处理历史数据，现在功能已集成到主程序中。

### 历史文档

#### 任务完成文档
- `TASK1_UNDEFINED_FIX_COMPLETED.md` - Undefined URL问题修复的详细记录
- `TASK2_FILENAME_STRATEGY_COMPLETED.md` - 文件名策略实施的详细记录

#### 问题分析文档
- `UNDEFINED_URL_ISSUE.md` - Undefined URL问题的分析
- `FILENAME_STRATEGY.md` - 文件名策略的设计
- `DATA_QUALITY_RESEARCH_SUMMARY.md` - 数据质量调研总结

#### 迁移文档
- `STATUS_FIELD_MIGRATION.md` - 状态字段迁移指南
- `README_RESEARCH.md` - README文档调研
- `CHANGELOG.md` - 早期变更日志

## 🔍 为什么归档？

这些文件被归档的原因：

1. **任务已完成**: 相关问题已解决，功能已实现
2. **脚本已过时**: 迁移脚本是一次性的，不再需要
3. **文档已整合**: 重要信息已整合到主文档中
4. **保持整洁**: 减少主目录的文件数量，提高可维护性

## 📚 当前文档

如果你在寻找当前的文档，请查看：

- `../README.md` - 项目主文档
- `../QUICK_START.md` - 快速开始指南
- `../doc/IMPLEMENTATION_SUMMARY.md` - 实现总结
- `../doc/PARSER_ARCHITECTURE.md` - 解析器架构
- `../doc/TAB_EXTRACTION_IMPROVEMENT.md` - Tab提取改进（最新）

## 🗑️ 删除建议

如果你确认不再需要这些历史记录，可以安全删除整个 `archived/` 文件夹。

但建议保留一段时间，以便：
- 回顾项目发展历程
- 参考历史问题的解决方案
- 了解某些设计决策的背景
