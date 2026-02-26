# URL多分类支持说明

## 需求

URL可以属于多个分类/模式。在后续数据抽取时，如果一个URL匹配多个模式，会抽取出多个结果，这是可以接受的（视为重复抓取）。

## 当前实现状态

当前的URL聚类算法（`skills/url-pattern-analyzer/lib/url-clusterer.js`）使用层次聚类方法，每个URL只会被分配到一个簇中。

## 需要的改进

### 方案1: 多标签分类（推荐）

修改聚类算法，允许一个URL同时属于多个模式：

```javascript
/**
 * URL多分类（一个URL可以属于多个模式）
 * @param {string[]} urls - URL列表
 * @param {number} minSimilarity - 最小相似度阈值（默认30）
 * @returns {Array} 模式列表，每个模式包含匹配的URL
 */
multiClassifyURLs(urls, minSimilarity = 30) {
  // 1. 首先进行标准聚类，得到主要模式
  const primaryClusters = this.clusterURLs(urls);
  
  // 2. 为每个簇生成模式
  const patterns = primaryClusters.map(cluster => ({
    urls: cluster,
    representative: this._selectRepresentative(cluster),
    pattern: this.generatePattern(cluster)
  }));
  
  // 3. 检查每个URL是否也匹配其他模式
  const multiClassified = patterns.map(pattern => {
    const matchingUrls = new Set(pattern.urls);
    
    // 检查所有URL是否也匹配这个模式
    urls.forEach(url => {
      if (!matchingUrls.has(url)) {
        const similarity = this.calculateSimilarity(url, pattern.representative);
        if (similarity >= minSimilarity) {
          matchingUrls.add(url);
        }
      }
    });
    
    return {
      ...pattern,
      urls: Array.from(matchingUrls)
    };
  });
  
  return multiClassified;
}
```

### 方案2: 基于规则的多匹配

在配置生成阶段，允许一个URL匹配多个模板配置：

```javascript
// 在TemplateParser中
matchAll(url) {
  // 返回所有匹配的配置，而不是只返回第一个
  return this.configs.filter(config => {
    const pattern = new RegExp(config.urlPattern.pattern);
    return pattern.test(url);
  });
}
```

## 使用场景示例

一个URL可能同时匹配多个模式：

```
URL: https://www.lixinger.com/analytics/company/dashboard

可能匹配的模式：
1. /analytics/{type}/dashboard  (通用dashboard模式)
2. /analytics/company/*          (公司分析模式)
3. /analytics/*                  (所有分析页面)
```

每个模式可能提取不同的数据：
- 模式1: 提取dashboard通用数据（标题、导航等）
- 模式2: 提取公司特定数据（财务指标、股价等）
- 模式3: 提取分析页面通用数据（图表、时间范围等）

## 实现优先级

- **P1**: 在报告生成时标注URL可能的多重分类
- **P2**: 修改聚类算法支持多标签分类
- **P3**: 在配置驱动的解析器中支持多模式匹配

## 注意事项

1. **去重处理**: 如果同一个URL被多个模式提取，需要在后续处理中识别和合并重复数据
2. **优先级**: 可以为每个模式设置优先级，在冲突时选择优先级高的结果
3. **性能**: 多分类会增加计算量，需要考虑性能优化
4. **报告展示**: 在分析报告中需要清楚地展示URL的多重归属关系

## 当前工作方案

在当前实现未修改的情况下，可以通过以下方式处理：

1. **接受重复**: 如用户所说，将多次抓取视为正常情况
2. **手动调整**: 在生成的配置文件中手动添加多个模式
3. **后处理**: 在数据处理阶段合并重复的抓取结果

## 下一步

- [ ] 评估是否需要立即实现多分类支持
- [ ] 如果需要，选择实现方案（方案1或方案2）
- [ ] 更新测试用例以验证多分类功能
- [ ] 更新文档说明多分类的使用方法
