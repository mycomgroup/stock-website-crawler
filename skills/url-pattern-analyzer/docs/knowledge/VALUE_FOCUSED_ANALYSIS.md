# 价值导向的URL模式分析

## 核心洞察：不是所有模式都有价值

### 业务原则

在网站爬虫和数据提取中，我们需要区分：
- **高价值页面**: 包含结构化数据，值得提取
- **低价值页面**: 独立编写，通常没有数据价值

**关键指标**: URL数量

---

## 模式价值分类

### 🎯 高价值模式（重点关注）

**特征**:
- URL数量多（通常 >50个）
- 使用模板批量生成
- 路径结构规律
- 包含动态参数（ID、代码等）

**价值**:
- ✅ 包含结构化数据
- ✅ 数据格式统一
- ✅ 值得投入时间提取
- ✅ ROI高

**示例**:
```
模式: company-detail (1,599 URLs)
路径: /analytics/company/detail/{market}/{code}/{id}
价值: 公司详情数据（财务、估值、基本面）

模式: fund-detail (1,936 URLs)
路径: /analytics/fund/detail/{type}/{code}/{id}
价值: 基金数据（净值、持仓、费率）
```

### ⚠️ 中价值模式（选择性关注）

**特征**:
- URL数量中等（10-50个）
- 可能是模板生成，也可能是独立页面
- 需要具体分析

**价值**:
- 🤔 需要评估数据价值
- 🤔 可能包含有用信息
- 🤔 ROI不确定

**示例**:
```
模式: help-pages (25 URLs)
路径: /help/{category}/{topic}
价值: 帮助文档（可能有用，但不是核心数据）
```

### ❌ 低价值模式（可以忽略）

**特征**:
- URL数量少（<10个）
- 独立编写的特殊页面
- 路径不规律
- 通常是静态内容

**价值**:
- ❌ 没有结构化数据
- ❌ 数据格式不统一
- ❌ 不值得投入时间
- ❌ ROI低

**示例**:
```
模式: about-us (1 URL)
路径: /about
价值: 公司介绍（静态内容，无数据价值）

模式: contact (1 URL)
路径: /contact
价值: 联系方式（静态内容）

模式: terms (1 URL)
路径: /terms
价值: 服务条款（法律文本）
```

---

## 80/20法则

### 帕累托原则在URL分析中的应用

```
前20%的模式 → 覆盖80%的URL → 包含80%的价值数据
后80%的模式 → 覆盖20%的URL → 包含20%的价值数据
```

### 实际案例：lixinger-crawler

**总URL数**: 8,490  
**总模式数**: 81

#### Top 10 模式（12%的模式）

| 模式 | URL数 | 占比 | 累计占比 |
|------|-------|------|----------|
| 1. analytics-chart-maker | 923 | 11.0% | 11.0% |
| 2. detail-sz | 751 | 9.0% | 20.0% |
| 3. detail-sh | 734 | 8.8% | 28.8% |
| 4. user-companies | 419 | 5.0% | 33.8% |
| 5. detail-nasdaq | 382 | 4.6% | 38.4% |
| 6. detail-sz | 237 | 2.8% | 41.2% |
| 7. detail-sh | 230 | 2.8% | 44.0% |
| 8. detail-jjgs | 219 | 2.6% | 46.6% |
| 9. detail-sz | 215 | 2.6% | 49.2% |
| 10. detail-sh | 191 | 2.3% | 51.5% |

**结论**: 
- 前10个模式（12%）覆盖了51.5%的URL
- 这10个模式应该是数据提取的重点

#### Bottom 20 模式（25%的模式）

大多数URL数量 < 20，很多 < 10

**结论**:
- 这些小簇可能是低价值页面
- 可以归为"其他"类别
- 不值得单独开发提取逻辑

---

## 实用建议

### 1. 使用 min-group-size 过滤小簇

```bash
# 只保留URL数量 >= 15 的模式
node run-skill.js project-name --min-group-size 15
```

**效果**:
- 自动过滤低价值小簇
- 减少噪音
- 聚焦高价值模式

### 2. 关注统计报告的Top 10

查看 `url-patterns-stats.md`:
```markdown
## Top 10 模式详情

### 1. company-detail (1,599 URLs)
- 路径模板: /analytics/company/detail/{market}/{code}/{id}
- 查询参数: from-my-followed
- 示例URL: ...
```

**行动**:
- 优先分析这10个模式
- 为这10个模式开发提取逻辑
- 其他模式可以暂时忽略

### 3. 计算价值覆盖率

```bash
# 查看前N个模式的覆盖率
node -e "
const data = require('./stock-crawler/output/lixinger-crawler/url-patterns.json');
const total = data.summary.totalUrls;
let covered = 0;
data.patterns.slice(0, 10).forEach((p, i) => {
  covered += p.urlCount;
  const ratio = (covered / total * 100).toFixed(1);
  console.log(\`前\${i+1}个模式: \${covered}个URL (\${ratio}%)\`);
});
"
```

**目标**: 找到覆盖80%URL的最小模式集

### 4. 标记低价值模式

在分析结果中，可以手动标记：
```json
{
  "name": "about-us",
  "urlCount": 1,
  "value": "low",  // 手动添加
  "priority": 0    // 手动添加
}
```

---

## 数据提取优先级策略

### 阶段1: 核心数据（必须）

**目标**: 覆盖50%的URL  
**模式数**: 通常5-10个  
**特征**: URL数量最多的模式

**行动**:
1. 分析Top 5模式
2. 开发提取逻辑
3. 验证数据质量
4. 部署到生产

### 阶段2: 重要数据（应该）

**目标**: 覆盖80%的URL  
**模式数**: 通常10-20个  
**特征**: URL数量中等的模式

**行动**:
1. 分析Top 6-20模式
2. 评估数据价值
3. 选择性开发提取逻辑
4. 逐步部署

### 阶段3: 补充数据（可选）

**目标**: 覆盖95%的URL  
**模式数**: 通常20-50个  
**特征**: URL数量较少的模式

**行动**:
1. 评估ROI
2. 只提取高价值数据
3. 低优先级

### 阶段4: 边缘数据（忽略）

**目标**: 剩余5%的URL  
**模式数**: 可能很多  
**特征**: URL数量很少（<10个）

**行动**:
- 归为"其他"类别
- 不开发提取逻辑
- 节省时间和资源

---

## 案例分析：如何识别低价值模式

### 示例1: 单个URL的模式

```json
{
  "name": "privacy-policy",
  "pathTemplate": "/privacy",
  "urlCount": 1,
  "samples": ["https://example.com/privacy"]
}
```

**判断**: ❌ 低价值
- 只有1个URL
- 静态页面
- 法律文本
- 无数据价值

**行动**: 忽略

### 示例2: 少量URL的帮助页面

```json
{
  "name": "help-topics",
  "pathTemplate": "/help/{category}",
  "urlCount": 8,
  "samples": [
    "https://example.com/help/getting-started",
    "https://example.com/help/faq"
  ]
}
```

**判断**: ⚠️ 中价值
- 8个URL
- 可能有用的信息
- 但不是核心数据

**行动**: 低优先级，可选

### 示例3: 大量URL的数据页面

```json
{
  "name": "product-detail",
  "pathTemplate": "/product/{category}/{id}",
  "urlCount": 1250,
  "samples": [
    "https://example.com/product/electronics/12345",
    "https://example.com/product/books/67890"
  ]
}
```

**判断**: ✅ 高价值
- 1250个URL
- 模板生成
- 结构化数据
- 核心业务数据

**行动**: 高优先级，必须提取

---

## 总结

### 核心原则

1. **URL数量 = 价值指标**
   - 多 = 高价值
   - 少 = 低价值

2. **80/20法则**
   - 关注前20%的模式
   - 覆盖80%的URL
   - 获得80%的价值

3. **ROI导向**
   - 评估投入产出比
   - 优先高价值模式
   - 忽略低价值模式

### 实用建议

1. **使用 min-group-size 过滤**: `--min-group-size 15`
2. **关注 Top 10 模式**: 查看统计报告
3. **计算覆盖率**: 找到80%覆盖的最小集
4. **分阶段实施**: 核心 → 重要 → 补充 → 忽略

### 最终目标

**不是提取所有数据，而是提取有价值的数据**

- ✅ 聚焦高价值模式
- ✅ 提高开发效率
- ✅ 降低维护成本
- ✅ 最大化ROI

---

**记住**: 小簇通常是低价值页面，可以归为"其他"类别。重点是找到有共同特性、URL数量多的模式，这些才是数据提取的重点。
