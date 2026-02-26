# URL Pattern Analyzer - 实用调优指南

## 核心原则

### 业务视角：模板数量有上限

一个网站的URL模式数量应该与其**页面模板数量**相对应：

- 每个URL模式 ≈ 一个页面模板
- 相同模板的页面 = 相同的数据提取逻辑
- 网站不会为每个页面写一个模板

### 合理的模式数量范围

| 网站规模 | URL数量 | 合理模式数 | 说明 |
|---------|---------|-----------|------|
| 小型 | <1,000 | 10-50 | 博客、企业官网、小型电商 |
| 中型 | 1,000-10,000 | 50-100 | 中型电商、新闻网站 |
| 大型 | 10,000-100,000 | 100-200 | 大型电商、门户网站 |
| 超大型 | >100,000 | 150-300 | 综合平台、搜索引擎 |

**警告信号**:
- 模式数 > 300: 很可能过度细分
- 模式数 < 10: 可能细分不足
- 模式数 > URL数 / 50: 过度细分

---

## 快速调优流程

### 第1步：初次分析（使用默认参数）

```bash
node run-skill.js lixinger-crawler
```

查看结果：
- 模式数量
- 最大簇大小
- 覆盖率

### 第2步：判断结果质量

#### 情况A：模式太多（>200）

**症状**:
```
模式数量: 350
最大簇: 50个URL
很多小簇: <20个URL
```

**原因**: 过度细分，把相同模板的页面分开了

**解决方案**:
```bash
# 保守模式
node run-skill.js lixinger-crawler \
  --min-group-size 20 \
  --refine-max-values 5 \
  --refine-min-count 20 \
  --strict-top-n 0
```

**目标**: 减少到100-150个模式

#### 情况B：模式太少（<50）

**症状**:
```
模式数量: 30
最大簇: 2000个URL
样本URL明显不同
```

**原因**: 细分不足，不同模板的页面混在一起

**解决方案**:
```bash
# 激进模式
node run-skill.js lixinger-crawler \
  --min-group-size 10 \
  --refine-max-values 10 \
  --refine-min-count 8 \
  --strict-top-n 10
```

**目标**: 增加到80-120个模式

#### 情况C：数量合理但有大簇混合

**症状**:
```
模式数量: 80
最大簇: 1500个URL
前5个簇的样本URL结构不同
```

**原因**: 大簇内部仍有不同模板

**解决方案**:
```bash
# 针对大簇优化
node run-skill.js lixinger-crawler \
  --min-group-size 15 \
  --strict-top-n 10 \
  --strict-match-ratio 0.85
```

**目标**: 细分大簇，总数控制在150以内

---

## 参数速查表

### 控制总数量的参数

| 参数 | 增大效果 | 减小效果 | 推荐范围 |
|------|---------|---------|---------|
| `min-group-size` | 减少模式 | 增加模式 | 10-25 |
| `refine-max-values` | 增加模式 | 减少模式 | 5-12 |
| `refine-min-count` | 减少模式 | 增加模式 | 8-20 |
| `strict-top-n` | 增加模式 | 减少模式 | 0-15 |

### 常用参数组合

#### 1. 保守组合（减少模式）
```bash
--min-group-size 20 \
--refine-max-values 5 \
--refine-min-count 20 \
--refine-min-groups 3 \
--strict-top-n 0
```
**适用**: 模式数 > 200

#### 2. 平衡组合（默认）
```bash
--min-group-size 10 \
--refine-max-values 8 \
--refine-min-count 10 \
--refine-min-groups 2 \
--strict-top-n 0
```
**适用**: 初次分析

#### 3. 激进组合（增加模式）
```bash
--min-group-size 10 \
--refine-max-values 12 \
--refine-min-count 5 \
--refine-min-groups 2 \
--strict-top-n 10 \
--strict-match-ratio 0.9
```
**适用**: 模式数 < 50

#### 4. 大簇优化组合
```bash
--min-group-size 15 \
--refine-max-values 8 \
--refine-min-count 12 \
--strict-top-n 10 \
--strict-match-ratio 0.85
```
**适用**: 有大簇混合问题

---

## 实战案例：lixinger-crawler

### 网站特点
- URL总数: 8,490
- 预期模板数: 80-150个

### 调优过程

#### 尝试1：默认参数
```bash
node run-skill.js lixinger-crawler
```
**结果**: 70个模式
**评估**: ✅ 数量合理，但最大簇923个URL，需要检查

#### 尝试2：启用严格模式
```bash
node run-skill.js lixinger-crawler --strict-top-n 5
```
**结果**: 81个模式，最大簇923个URL
**评估**: ✅ 数量合理，大簇已细分

#### 尝试3：更激进（测试）
```bash
node run-skill.js lixinger-crawler \
  --min-group-size 8 \
  --refine-max-values 12 \
  --strict-top-n 10
```
**结果**: 120个模式
**评估**: ⚠️ 可能过度细分，需要验证

### 最终选择
```bash
node run-skill.js lixinger-crawler \
  --min-group-size 10 \
  --strict-top-n 5
```
**结果**: 81个模式
**理由**: 
- 数量合理（80-150范围内）
- 大簇已细分
- 覆盖率99%+

---

## 验证模式质量

### 方法1：检查最大簇

```bash
# 查看前10个最大簇
node -e "const data = require('./stock-crawler/output/lixinger-crawler/url-patterns.json'); \
  data.patterns.slice(0, 10).forEach((p, i) => { \
    console.log(\`\${i+1}. \${p.name} (\${p.urlCount} URLs)\`); \
    console.log(\`   Template: \${p.pathTemplate}\`); \
    console.log(\`   Samples:\`); \
    p.samples.slice(0, 3).forEach(s => console.log(\`     \${s}\`)); \
    console.log(); \
  });"
```

**检查点**:
- 样本URL是否结构相同？
- 是否明显属于同一类页面？
- 最大簇是否 < 1000个URL？

### 方法2：检查小簇

```bash
# 查看最小的10个簇
node -e "const data = require('./stock-crawler/output/lixinger-crawler/url-patterns.json'); \
  const sorted = data.patterns.sort((a, b) => a.urlCount - b.urlCount); \
  sorted.slice(0, 10).forEach((p, i) => { \
    console.log(\`\${i+1}. \${p.name} (\${p.urlCount} URLs) - \${p.pathTemplate}\`); \
  });"
```

**检查点**:
- 小簇是否真的是独特的模板？
- 还是应该合并到其他簇？

### 方法3：统计分析

查看统计报告：
```
stock-crawler/output/lixinger-crawler/url-patterns-stats.md
```

**关键指标**:
- 覆盖率: 应该 > 95%
- 平均每模式URL数: 应该 > 30
- 最大/最小比例: 不应该 > 100:1

---

## 常见问题

### Q1: 为什么我的网站有300+个模式？

**可能原因**:
1. 参数太激进（min-group-size太小）
2. 网站确实有很多模板（罕见）
3. URL中包含了不应该作为模式的变化（如时间戳）

**解决方案**:
- 增大 `min-group-size` 到 20-25
- 减小 `refine-max-values` 到 5
- 关闭严格模式 `strict-top-n 0`

### Q2: 如何判断两个模式是否应该合并？

**判断标准**:
1. 路径结构是否相同？
2. 页面内容类型是否相同？
3. 数据提取逻辑是否相同？

如果都是"是"，应该合并。

### Q3: 模式数量的"黄金法则"是什么？

**经验公式**:
```
合理模式数 ≈ √(URL总数) × 2

例如:
- 10,000个URL → 约200个模式
- 1,000个URL → 约60个模式
- 100个URL → 约20个模式
```

但这只是参考，最终要看实际页面模板数量。

---

## 总结

### 记住这些原则

1. **模式数 ≈ 模板数**: 一个网站通常有10-200个页面模板
2. **相同模板 = 相同提取**: 同一模式的URL应该用相同方式提取数据
3. **质量 > 数量**: 宁可少而准，不要多而乱
4. **迭代调优**: 先用默认参数，再根据结果调整

### 推荐工作流

```
1. 运行默认参数
   ↓
2. 查看模式数量
   ↓
3. 如果 > 200: 使用保守组合
   如果 < 50: 使用激进组合
   如果 50-200: 检查大簇质量
   ↓
4. 验证结果质量
   ↓
5. 微调参数
   ↓
6. 确定最终配置
```

### 最后的建议

- 不要追求"完美"的模式数量
- 关注模式的**业务意义**
- 如果不确定，选择**保守**的参数
- 记录你的参数选择和理由

---

**记住**: URL模式分析的目标是为数据提取服务，不是为了分类而分类。
