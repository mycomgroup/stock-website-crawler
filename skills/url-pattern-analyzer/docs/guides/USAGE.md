# URL Pattern Analyzer - 使用指南

## 快速开始

### 最简单的方式：通过项目名运行

```bash
node run-skill.js lixinger-crawler
```

这个命令会：
1. 自动查找 `stock-crawler/output/lixinger-crawler/links.txt`
2. 运行URL模式分析
3. 生成3个报告文件：
   - `url-patterns.json` - JSON格式的详细数据
   - `url-patterns.md` - Markdown格式的可读报告
   - `url-patterns-stats.md` - 统计分析报告

## 参数调优

### 基本参数

```bash
node run-skill.js lixinger-crawler --min-group-size 10 --max-patterns 20
```

### 参数说明

| 参数 | 默认值 | 说明 | 推荐值 |
|------|--------|------|--------|
| `--min-group-size` | 5 | 最小分组大小，过滤掉URL数量少于此值的模式 | 小网站:3-5<br>中网站:5-10<br>大网站:10-20 |
| `--max-patterns` | 无限制 | 最大模式数量，只保留URL数量最多的前N个 | 20-50 |
| `--sample-count` | 5 | 每个模式显示的示例URL数量 | 3-10 |
| `--no-markdown` | false | 不生成Markdown报告 | - |

### 参数调优建议

#### 场景1: 网站URL很多，想要粗粒度分类

```bash
node run-skill.js lixinger-crawler --min-group-size 20 --max-patterns 10
```

效果：
- 只保留URL数量≥20的模式
- 最多显示10个最大的模式
- 适合快速了解网站主要结构

#### 场景2: 想要细粒度分类，发现所有模式

```bash
node run-skill.js lixinger-crawler --min-group-size 3
```

效果：
- 保留URL数量≥3的所有模式
- 可能会有很多模式
- 适合详细分析网站结构

#### 场景3: 平衡模式（推荐）

```bash
node run-skill.js lixinger-crawler --min-group-size 10 --max-patterns 20
```

效果：
- 过滤掉小模式（<10个URL）
- 保留前20个最大的模式
- 覆盖率通常在80-95%之间

## 输出报告说明

### 1. JSON报告 (`url-patterns.json`)

机器可读的完整数据，包含：
- 所有识别的URL模式
- 每个模式的正则表达式
- 示例URL列表
- 统计信息

**用途**: 
- 供程序读取和处理
- 作为下一步（模板内容分析）的输入

### 2. Markdown报告 (`url-patterns.md`)

人类可读的详细报告，包含：
- 总体统计
- 每个模式的详细信息
- 示例URL
- 可视化表格

**用途**:
- 快速浏览分析结果
- 分享给团队成员
- 文档记录

### 3. 统计报告 (`url-patterns-stats.md`)

专注于统计分析的报告，包含：

#### 总体统计
- 总URL数量
- 识别的模式数量
- 覆盖率（被分类的URL占比）
- 平均每个模式的URL数量
- 最大/最小模式的URL数量

#### 配置参数
- 记录使用的参数设置
- 便于复现和调整

#### 模式分布表
- 按URL数量排序的所有模式
- 每个模式的URL数量和占比
- 路径模板

#### Top 10详细信息
- 前10个最大模式的详细信息
- 包含示例URL
- 查询参数列表

#### 质量评估
- 自动评估分析质量
- 基于覆盖率给出评级：
  - ✅ Excellent: 覆盖率 > 90%
  - ⚠️ Good: 覆盖率 70-90%
  - ❌ Poor: 覆盖率 < 70%

#### 优化建议
- 根据分析结果自动给出参数调整建议
- 帮助优化下次分析

## 实际案例

### 案例1: lixinger-crawler项目

```bash
node run-skill.js lixinger-crawler --min-group-size 10 --max-patterns 20
```

**结果**:
- 总URL数: 713
- 识别模式: 7个
- 覆盖率: 100%
- 最大模式: macro-gdp (418个URL, 58.63%)

**分析**:
- 覆盖率100%，说明所有URL都被成功分类
- 7个模式，数量适中，便于管理
- 最大模式占比58%，说明网站有明显的主要功能区

### 案例2: 调整参数提高覆盖率

如果第一次运行覆盖率只有60%：

```bash
# 第一次尝试
node run-skill.js myproject --min-group-size 10
# 结果: 覆盖率60%，很多URL未分类

# 降低最小分组大小
node run-skill.js myproject --min-group-size 5
# 结果: 覆盖率85%，模式数量增加

# 进一步降低
node run-skill.js myproject --min-group-size 3
# 结果: 覆盖率95%，模式数量较多但可接受
```

## 常见问题

### Q1: 覆盖率很低怎么办？

**A**: 降低 `--min-group-size` 参数

```bash
# 从默认的5降低到3
node run-skill.js myproject --min-group-size 3
```

### Q2: 模式太多了怎么办？

**A**: 增加 `--min-group-size` 或设置 `--max-patterns`

```bash
# 方案1: 提高最小分组
node run-skill.js myproject --min-group-size 15

# 方案2: 限制最大模式数
node run-skill.js myproject --min-group-size 10 --max-patterns 15
```

### Q3: 如何找到最佳参数？

**A**: 迭代调整，观察统计报告

```bash
# 步骤1: 使用默认参数
node run-skill.js myproject

# 步骤2: 查看统计报告中的建议
cat stock-crawler/output/myproject/url-patterns-stats.md

# 步骤3: 根据建议调整参数
node run-skill.js myproject --min-group-size 8 --max-patterns 25

# 步骤4: 重复直到满意
```

### Q4: 生成的报告在哪里？

**A**: 在项目的output目录下

```
stock-crawler/output/{projectName}/
├── url-patterns.json        # JSON数据
├── url-patterns.md          # Markdown报告
└── url-patterns-stats.md    # 统计报告
```

### Q5: 如何在Kiro中使用？

**A**: 直接告诉Kiro你的需求

```
"分析 lixinger-crawler 项目的URL模式"
"使用最小分组10，最多20个模式分析URL"
"生成URL模式统计报告"
```

## 下一步

分析完URL模式后，可以使用 `template-content-analyzer` 进行模板内容分析：

```bash
# 在 skills/template-content-analyzer 目录下
node run-skill.js lixinger-crawler
```

这会：
1. 读取 `url-patterns.json`
2. 分析每个模式对应的页面内容
3. 生成模板配置文件 `template-rules.jsonl`

## 技术支持

- 查看详细文档: [SKILL.md](./SKILL.md)
- 查看README: [README.md](./README.md)
- 查看算法实现: [lib/url-clusterer.js](./lib/url-clusterer.js)
