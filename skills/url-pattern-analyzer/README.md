# URL Pattern Analyzer

智能URL模式识别和分类工具，通过三层优化算法自动识别网站的URL结构模式。

## 核心特性

- ✅ **智能聚类**: 自动识别相似URL并分组
- ✅ **三层优化**: 路径严格化 → 半固定段细分 → 大簇严格细分
- ✅ **参数化设计**: 所有关键阈值可配置，无需修改代码
- ✅ **高性能**: 支持8000+ URL快速分析（<200ms）
- ✅ **多格式输出**: JSON + Markdown + 统计报告
- ✅ **业务导向**: 模式数量对应页面模板数量

## 快速开始

### 基本使用

```bash
# 分析项目URL
node run-skill.js lixinger-crawler

# 自定义参数
node run-skill.js lixinger-crawler --min-group-size 10 --strict-top-n 5
```

### 输出文件

- `url-patterns.json`: 完整的模式数据
- `url-patterns.md`: 可读性好的Markdown报告
- `url-patterns-stats.md`: 中文统计报告

## 参数说明

### 基础参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--min-group-size` | 5 | 最小分组大小，过滤小簇 |
| `--sample-count` | 5 | 每个模式的示例URL数量 |
| `--max-patterns` | 无限制 | 最大模式数量（仅统计报告） |

### 细分控制参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--refine-max-values` | 8 | 半固定段最大唯一值数量 |
| `--refine-min-count` | 10 | 每个值最小出现次数 |
| `--refine-min-groups` | 2 | 最少需要几个大组才细分 |

### 严格模式参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--strict-top-n` | 0 | 对前N个最大簇应用严格规则（0=不启用） |
| `--strict-match-ratio` | 0.8 | 严格模式下的匹配比例阈值 |

## 使用场景

### 场景1: 模式太多（>200）

```bash
# 保守模式
node run-skill.js project-name \
  --min-group-size 20 \
  --refine-max-values 5 \
  --refine-min-count 20 \
  --strict-top-n 0
```

### 场景2: 模式太少（<50）

```bash
# 激进模式
node run-skill.js project-name \
  --min-group-size 10 \
  --refine-max-values 12 \
  --refine-min-count 5 \
  --strict-top-n 10
```

### 场景3: 大簇需要细分

```bash
# 大簇优化模式
node run-skill.js project-name \
  --min-group-size 15 \
  --strict-top-n 10 \
  --strict-match-ratio 0.85
```

## 真实案例

### lixinger-crawler 项目

**网站特点**: 8,490个URL，中型金融数据网站

**优化过程**:
1. 初始版本: 14个模式，最大簇3,261个URL
2. 路径严格化: 38个模式，结构分离成功
3. 半固定段细分: 70个模式，市场代码分离
4. 大簇严格细分: 81个模式，最大簇923个URL

**最终配置**:
```bash
node run-skill.js lixinger-crawler --min-group-size 10 --strict-top-n 5
```

**效果**:
- 模式数量: 14 → 81 (+478%)
- 最大簇: 3,261 → 923 (-72%)
- 覆盖率: 99.2%
- 分类精度: 显著提升

## 文档

- [VALUE_FOCUSED_ANALYSIS.md](./VALUE_FOCUSED_ANALYSIS.md) - 价值导向分析（重要！）
- [PRACTICAL_GUIDE.md](./PRACTICAL_GUIDE.md) - 实用调优指南
- [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md) - 优化总结
- [REAL_WORLD_TEST_SUMMARY.md](./REAL_WORLD_TEST_SUMMARY.md) - 真实场景测试
- [ALGORITHM_OPTIMIZATION.md](./ALGORITHM_OPTIMIZATION.md) - 算法优化记录

## 核心原则

1. **模式数 ≈ 模板数**: 一个网站通常有10-200个页面模板
2. **相同模板 = 相同提取**: 同一模式的URL应该用相同方式提取数据
3. **质量 > 数量**: 宁可少而准，不要多而乱
4. **迭代调优**: 先用默认参数，再根据结果调整
5. **价值导向**: 关注大簇（>50 URLs），忽略小簇（<10 URLs）

### 80/20法则

```
前20%的模式 → 覆盖80%的URL → 包含80%的价值数据
```

**实用建议**:
- 重点分析前10-20个最大的模式
- 小簇（<10个URL）通常是低价值页面，可以归为"其他"
- 使用 `--min-group-size 15` 过滤低价值小簇

## 技术亮点

### 三层优化架构

```
基础聚类（路径深度+段匹配）
    ↓
半固定段细分（识别有限唯一值）
    ↓
严格模式细分（对大簇应用严格规则）
    ↓
最终结果
```

### 智能识别机制

- **路径深度**: 必须完全相同
- **段匹配**: 至少50%相同
- **半固定段**: 唯一值≤8且有大组
- **严格细分**: 固定比例<80%时细分

## 性能

- 时间复杂度: O(n log n)
- 实测性能: 8,490个URL，用时<200ms
- 缓存优化: 特征提取和相似度计算

## 适用场景

- ✅ 网站爬虫开发
- ✅ API接口分析
- ✅ 数据提取规划
- ✅ 网站结构分析
- ✅ SEO优化分析

## 版本历史

- **v1.0.0** (2026-02-26): 初始版本
  - 基础URL聚类
  - JSON和Markdown报告生成
  
- **v1.1.0** (2026-02-26): 路径严格化优化
  - 要求路径深度完全相同
  - 要求至少50%段匹配
  
- **v1.2.0** (2026-02-26): 半固定段细分
  - 识别有限唯一值的段
  - 智能细分大组
  - 添加3个可配置参数
  
- **v1.3.0** (2026-02-26): 大簇严格细分
  - 对最大N个簇应用严格规则
  - 计算段固定比例
  - 添加2个可配置参数

## License

MIT
