# URL Pattern Analyzer - 目录结构说明

## 完整目录树

```
url-pattern-analyzer/
│
├── 📄 核心文件
│   ├── README.md                    # 项目主文档
│   ├── SKILL.md                     # Skill配置文档
│   ├── main.js                      # 核心入口
│   ├── run-skill.js                 # 增强运行脚本
│   ├── package.json                 # 项目配置
│   └── skill.json                   # 原始配置
│
├── 💻 代码库
│   ├── lib/                         # 核心代码
│   │   ├── url-clusterer.js        # URL聚类算法
│   │   ├── report-generator.js     # 报告生成器
│   │   └── links-reader.js         # 链接读取器
│   │
│   ├── test/                        # 测试文件
│   │   ├── *.test.js               # 单元测试
│   │   └── test-*.js               # 集成测试
│   │
│   └── scripts/                     # 工具脚本
│       ├── README.md
│       └── analyze-url-patterns.js
│
├── 📚 文档中心 (docs/)
│   ├── README.md                    # 文档导航
│   │
│   ├── 📖 guides/                   # 使用指南
│   │   ├── QUICK_START.md          # 5分钟快速开始
│   │   ├── USAGE.md                # 完整使用说明
│   │   └── PRACTICAL_GUIDE.md      # 实战调优指南
│   │
│   ├── 🧠 knowledge/                # 知识文档
│   │   ├── VALUE_FOCUSED_ANALYSIS.md      # 价值导向分析
│   │   ├── ALGORITHM_OPTIMIZATION.md      # 算法优化原理
│   │   └── PARAMETER_TUNING_GUIDE.md      # 参数调优理论
│   │
│   ├── 📊 reports/                  # 测试报告
│   │   ├── OPTIMIZATION_SUMMARY.md        # 优化总结
│   │   ├── REAL_WORLD_TEST_SUMMARY.md     # 真实场景测试
│   │   └── ENHANCEMENT_SUMMARY.md         # 增强功能总结
│   │
│   └── 📋 reference/                # 参考文档
│       ├── QUICK_REFERENCE.md      # 参数速查表
│       └── PATTERN_VALIDATION_GUIDE.md    # 模式验证指南
│
├── 🗄️ archive/                      # 归档文件
│   ├── debug-cluster.js            # 调试脚本
│   ├── performance-test-report.json # 性能测试报告
│   └── ALGORITHM_OPTIMIZATION_SUMMARY.md  # 旧版总结
│
└── 📁 output/                       # 输出目录
    └── *.json, *.md                # 分析结果
```

## 文件数量统计

| 目录 | 文件数 | 说明 |
|------|--------|------|
| 根目录 | 9个 | 核心文件 + 配置 |
| lib/ | 3个 | 核心代码库 |
| test/ | 11个 | 测试文件 |
| scripts/ | 2个 | 工具脚本 |
| docs/guides/ | 3个 | 使用指南 |
| docs/knowledge/ | 3个 | 知识文档 |
| docs/reports/ | 3个 | 测试报告 |
| docs/reference/ | 2个 | 参考文档 |
| archive/ | 3个 | 归档文件 |

**总计**: 39个文件（不含node_modules）

## 快速导航

### 我想快速开始使用
→ [README.md](../README.md)  
→ [docs/guides/QUICK_START.md](guides/QUICK_START.md)

### 我想深入理解原理
→ [docs/knowledge/VALUE_FOCUSED_ANALYSIS.md](knowledge/VALUE_FOCUSED_ANALYSIS.md)  
→ [docs/knowledge/ALGORITHM_OPTIMIZATION.md](knowledge/ALGORITHM_OPTIMIZATION.md)

### 我想学习调优技巧
→ [docs/guides/PRACTICAL_GUIDE.md](guides/PRACTICAL_GUIDE.md)  
→ [docs/reference/QUICK_REFERENCE.md](reference/QUICK_REFERENCE.md)

### 我想了解优化效果
→ [docs/reports/OPTIMIZATION_SUMMARY.md](reports/OPTIMIZATION_SUMMARY.md)  
→ [docs/reports/REAL_WORLD_TEST_SUMMARY.md](reports/REAL_WORLD_TEST_SUMMARY.md)

### 我想查询参数
→ [docs/reference/QUICK_REFERENCE.md](reference/QUICK_REFERENCE.md)

### 我想验证结果
→ [docs/reference/PATTERN_VALIDATION_GUIDE.md](reference/PATTERN_VALIDATION_GUIDE.md)

## 设计原则

### 1. 分离关注点
- 代码 (lib/, test/, scripts/)
- 文档 (docs/)
- 归档 (archive/)
- 输出 (output/)

### 2. 按用途分类
- guides/ - 如何使用
- knowledge/ - 为什么这样设计
- reports/ - 效果如何
- reference/ - 快速查询

### 3. 保持简洁
- 根目录只保留核心文件
- 文档集中在docs/
- 临时文件归档

### 4. 易于扩展
- 新文档有明确归属
- 目录结构清晰
- 命名规范统一

## 命名规范

### 文档命名
- `QUICK_START.md` - 快速开始
- `USAGE.md` - 使用说明
- `*_GUIDE.md` - 指南类
- `*_SUMMARY.md` - 总结类
- `*_ANALYSIS.md` - 分析类
- `*_OPTIMIZATION.md` - 优化类

### 代码命名
- `main.js` - 主入口
- `run-*.js` - 运行脚本
- `*-clusterer.js` - 聚类器
- `*-generator.js` - 生成器
- `*-reader.js` - 读取器

### 测试命名
- `*.test.js` - 单元测试
- `test-*.js` - 集成测试

## 维护指南

### 添加新文档
1. 确定文档类型（使用/知识/报告/参考）
2. 放入对应的docs/子目录
3. 更新docs/README.md
4. 更新主README.md（如果需要）

### 添加新功能
1. 代码放入lib/
2. 测试放入test/
3. 文档放入docs/guides/
4. 更新README.md

### 归档旧文件
1. 移动到archive/
2. 添加归档说明
3. 更新相关链接

## 最佳实践

### ✅ 推荐
- 文档按用途分类
- 代码和文档分离
- 临时文件及时归档
- 保持根目录简洁

### ❌ 避免
- 在根目录堆积文档
- 混合不同类型的文档
- 保留调试文件在主目录
- 创建过深的目录层级

---

返回 [文档中心](README.md) | [主文档](../README.md)
