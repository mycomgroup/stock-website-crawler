# 目录结构

```
ml_multifactor_validation_20260401/
│
├── README.md                          # 主报告（最终版本）
├── QUICK_START.md                     # 快速开始指南
│
├── docs/                              # 文档目录
│   ├── 07_ML_MultiFactor_Validation_Report_REAL.md  # 详细验证报告
│   ├── 07_ML_Results_Summary.md                      # 结果摘要
│   └── RESULT_ANALYSIS.md                            # 深度分析报告
│
├── scripts/                           # 代码目录
│   ├── ml_ultra_quick.py             # 快速验证脚本
│   ├── ml_walkforward_real.py        # 完整验证脚本
│   └── STRATEGY_CODE.md              # 实盘策略代码说明
│
└── results/                           # 结果目录
    └── joinquant-notebook-result-codingutf-1775029231780.json  # 真实运行结果
```

## 文件说明

### 📄 README.md
- **用途**: 主报告，包含完整结论和建议
- **读者**: 决策者、投资经理
- **内容**: 最终判定、核心数据、实施建议

### 📄 QUICK_START.md
- **用途**: 快速开始指南
- **读者**: 开发者、运维人员
- **内容**: 环境准备、运行命令、常见问题

### 📁 docs/
详细文档目录，包含：
- 详细验证报告（完整数据）
- 结果摘要（快速查看）
- 深度分析（统计、对比、建议）

### 📁 scripts/
代码目录，包含：
- 快速验证脚本（推荐首次运行）
- 完整验证脚本（全面测试）
- 实盘策略代码（可直接使用）

### 📁 results/
运行结果目录，包含：
- JSON格式原始结果
- 可用于后续分析

---

## 快速导航

| 我想... | 查看文件 |
|---------|---------|
| 了解最终结论 | README.md |
| 快速运行测试 | QUICK_START.md |
| 查看详细数据 | docs/07_ML_MultiFactor_Validation_Report_REAL.md |
| 了解分析过程 | docs/RESULT_ANALYSIS.md |
| 获取策略代码 | scripts/STRATEGY_CODE.md |
| 查看原始结果 | results/joinquant-notebook-result-*.json |

---

## 版本信息

- **创建日期**: 2026-04-01
- **版本**: v1.0
- **作者**: Agent 07 - ML验证任务
- **状态**: FINAL ✅

---

## 联系方式

如有问题，请参考：
- 回测指南: `docs/backtest_guide/README.md`
- JoinQuant文档: https://www.joinquant.com/help/api/