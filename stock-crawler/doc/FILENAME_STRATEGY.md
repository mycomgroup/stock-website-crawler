# 文件名生成策略详细设计

生成时间: 2026-02-25

## 设计目标

1. **直观性**: 文件名能清晰表达页面内容
2. **唯一性**: 避免文件名冲突
3. **简洁性**: 控制文件名长度在合理范围（30-60字符）
4. **可维护性**: 规则清晰，易于理解和调试

## 核心策略

采用 **"标题 + URL关键部分"** 组合方式：

```
格式: {清理后的标题}_{URL关键部分}.md
示例: 居民消费价格指数_cn.md
     样本信息API_us_index.md
     费用_我的_annually.md
```

## 实现规则

### 1. 标题清理规则

```javascript
function cleanTitle(title) {
  return title
    .replace(/\|/g, '_')              // 管道符转下划线
    .replace(/\s+/g, '_')             // 空格转下划线
    .replace(/_-_理杏仁$/i, '')       // 移除网站名后缀
    .replace(/_-_[^_]+$/i, '')        // 移除其他网站名后缀
    .replace(/[\/\\?*:|"<>]/g, '_')   // 替换文件系统不允许的字符
    .replace(/_{2,}/g, '_')           // 合并多个下划线
    .replace(/^_|_$/g, '');           // 移除首尾下划线
}
```

**示例**:
- `居民消费价格指数|大陆|价格指数|宏观 - 理杏仁` → `居民消费价格指数_大陆_价格指数_宏观`
- `费用|我的 - 理杏仁` → `费用_我的`
- `API文档|开放平台 - 理杏仁` → `API文档_开放平台`

### 2. URL关键部分提取规则

#### 规则优先级

1. **市场代码** (最高优先级)
2. **数据类型/周期**
3. **API Key路径**
4. **查询参数关键字**
5. **路径段关键字**

#### 具体提取规则

```javascript
function extractKeyParts(url) {
  const parts = [];
  const urlObj = new URL(url);
  const pathname = urlObj.pathname;
  const searchParams = urlObj.searchParams;
  
  // 1. 提取市场代码 (cn/hk/us/a/b/h)
  const marketCodes = ['cn', 'hk', 'us', 'a', 'b', 'h'];
  marketCodes.forEach(code => {
    if (pathname.includes(`/${code}/`) || 
        pathname.endsWith(`/${code}`) ||
        searchParams.toString().includes(`=${code}`) ||
        searchParams.toString().includes(`/${code}/`)) {
      if (!parts.includes(code)) {
        parts.push(code);
      }
    }
  });
  
  // 2. 提取数据类型/周期
  const dataTypes = {
    'weekly': 'weekly',
    'monthly': 'monthly',
    'quarterly': 'quarterly',
    'annually': 'annually',
    'daily': 'daily',
    'custom': 'custom',
    'realtime': 'realtime'
  };
  
  Object.entries(dataTypes).forEach(([key, value]) => {
    if (pathname.includes(key) || searchParams.toString().includes(key)) {
      if (!parts.includes(value)) {
        parts.push(value);
      }
    }
  });
  
  // 3. 提取 API Key 的关键部分
  const apiKey = searchParams.get('api-key');
  if (apiKey && apiKey !== 'undefined') {
    // 取最后两段作为关键部分
    const apiParts = apiKey.split('/').filter(p => p && p !== 'undefined');
    const keyParts = apiParts.slice(-2).join('_');
    if (keyParts && !parts.includes(keyParts)) {
      parts.push(keyParts);
    }
  }
  
  // 4. 提取查询参数中的关键字
  const importantParams = [
    'chart-granularity',
    'date-range',
    'period',
    'type',
    'category'
  ];
  
  importantParams.forEach(param => {
    const value = searchParams.get(param);
    if (value && value !== 'undefined') {
      // 简化参数值
      const shortValue = value.substring(0, 10).replace(/[^a-zA-Z0-9]/g, '');
      if (shortValue && !parts.includes(shortValue)) {
        parts.push(shortValue);
      }
    }
  });
  
  // 5. 提取路径中的关键段
  const pathSegments = pathname.split('/').filter(s => s);
  const keywordSegments = [
    'index', 'constituents', 'fundamental', 'financial',
    'non-financial', 'industry', 'company', 'macro',
    'analytics', 'chart-maker', 'shareholders', 'treasury',
    'money-supply', 'cpi', 'ppi', 'gdp'
  ];
  
  pathSegments.forEach(segment => {
    if (keywordSegments.includes(segment) && !parts.includes(segment)) {
      parts.push(segment);
    }
  });
  
  return parts;
}
```

### 3. 文件名组合规则

```javascript
function generateFilename(title, url) {
  // 1. 清理标题
  const cleanedTitle = cleanTitle(title);
  
  // 2. 提取URL关键部分
  const urlParts = extractKeyParts(url);
  
  // 3. 组合文件名
  let filename = cleanedTitle;
  
  if (urlParts.length > 0) {
    // 限制URL部分最多3个关键字
    const limitedParts = urlParts.slice(0, 3);
    filename += '_' + limitedParts.join('_');
  }
  
  // 4. 限制总长度
  if (filename.length > 60) {
    // 优先保留标题，截断URL部分
    const titlePart = cleanedTitle.substring(0, 40);
    const urlPart = urlParts.slice(0, 2).join('_').substring(0, 18);
    filename = titlePart + (urlPart ? '_' + urlPart : '');
  }
  
  // 5. 最终清理
  filename = filename
    .replace(/_{2,}/g, '_')
    .replace(/^_|_$/g, '');
  
  // 6. 如果文件名为空，使用默认值
  if (!filename) {
    filename = 'untitled';
  }
  
  return filename + '.md';
}
```

### 4. 冲突处理规则

如果生成的文件名仍然冲突（极少情况），添加数字后缀：

```javascript
function ensureUniqueFilename(filename, existingFiles) {
  if (!existingFiles.has(filename)) {
    return filename;
  }
  
  const baseName = filename.replace(/\.md$/, '');
  let counter = 2;
  let newFilename = `${baseName}_${counter}.md`;
  
  while (existingFiles.has(newFilename)) {
    counter++;
    newFilename = `${baseName}_${counter}.md`;
  }
  
  return newFilename;
}
```

## 效果对比

### 当前文件名 vs 新文件名

| 当前文件名 | 新文件名 | 改进点 |
|-----------|---------|--------|
| `费用_我的_-_理杏仁_841dc123.md` | `费用_我的_annually.md` | ✓ 去除哈希，更直观 |
| `样本信息API购买_23a63f7e.md` | `样本信息API_us_index_constituents.md` | ✓ 明确市场和类型 |
| `大陆_货币供应_宏观_-_理杏仁_c210a99b.md` | `货币供应_cn.md` | ✓ 更简洁 |
| `居民消费价格指数_大陆_价格指数_宏观_-_理杏仁.md` | `居民消费价格指数_cn_cpi.md` | ✓ 更短，保留关键信息 |
| `国家财政_宏观_-_理杏仁_0ec4011e.md` | `国家财政_y.md` | ✓ 标识年度数据 |
| `自定义_制图_-_理杏仁_89fbaa64.md` | `自定义_制图_custom.md` | ✓ 明确是自定义页面 |

### 长度分布预测

| 长度范围 | 当前数量 | 预计数量 | 变化 |
|---------|---------|---------|------|
| < 30 字符 | ~50 (26%) | ~80 (42%) | ↑ 60% |
| 30-50 字符 | ~100 (53%) | ~90 (48%) | ↓ 10% |
| 50-70 字符 | ~30 (16%) | ~18 (10%) | ↓ 40% |
| > 70 字符 | ~8 (4%) | ~0 (0%) | ↓ 100% |

**平均长度**: 42 字符 → 35 字符 (减少 17%)

## 特殊情况处理

### 1. URL包含undefined

**问题**: `https://www.lixinger.com/open/api/doc?api-key=macro/undefined`

**处理**: 
- 在提取API Key时过滤掉`undefined`
- 如果整个API Key是`undefined`，则忽略该部分
- 记录警告日志，便于后续修复链接提取逻辑

### 2. 标题为空或无效

**处理**:
- 使用URL路径的最后一段作为标题
- 如果路径也无效，使用`untitled`

### 3. 标题过长

**处理**:
- 优先保留标题前40个字符
- URL部分最多保留2个关键字，共18个字符
- 总长度控制在60字符以内

### 4. 标题完全相同但URL不同

**示例**: 多个"费用"页面，但订阅周期不同

**处理**:
- 通过URL关键部分区分（weekly/monthly/annually）
- 如果仍然冲突，添加数字后缀

## 测试用例

### 测试集1: 市场区分

| URL | 标题 | 预期文件名 |
|-----|------|-----------|
| `/open/api/doc?api-key=hk/index/constituents` | `样本信息API购买` | `样本信息API_hk_index_constituents.md` |
| `/open/api/doc?api-key=us/index/constituents` | `样本信息API购买` | `样本信息API_us_index_constituents.md` |
| `/open/api/doc?api-key=cn/index/constituents` | `样本信息API购买` | `样本信息API_cn_index_constituents.md` |

### 测试集2: 周期区分

| URL | 标题 | 预期文件名 |
|-----|------|-----------|
| `/place-order/weekly` | `费用\|我的 - 理杏仁` | `费用_我的_weekly.md` |
| `/place-order/monthly` | `费用\|我的 - 理杏仁` | `费用_我的_monthly.md` |
| `/place-order/annually` | `费用\|我的 - 理杏仁` | `费用_我的_annually.md` |

### 测试集3: 数据粒度区分

| URL | 标题 | 预期文件名 |
|-----|------|-----------|
| `/analytics/macro/treasury` | `国家财政\|宏观 - 理杏仁` | `国家财政_macro_treasury.md` |
| `/analytics/macro/treasury?chart-granularity=y` | `国家财政\|宏观 - 理杏仁` | `国家财政_macro_treasury_y.md` |

### 测试集4: 特殊情况

| URL | 标题 | 预期文件名 |
|-----|------|-----------|
| `/open/api/doc?api-key=macro/undefined` | `API文档\|开放平台 - 理杏仁` | `API文档_开放平台_macro.md` |
| `/analytics/chart-maker/` | `自定义\|制图 - 理杏仁` | `自定义_制图.md` |
| `/analytics/chart-maker/custom` | `自定义\|制图 - 理杏仁` | `自定义_制图_custom.md` |

## 实施计划

### 阶段1: 代码实现 (1天)

1. 在 `markdown-generator.js` 中实现新的文件名生成逻辑
2. 保留旧的 `safeFilename` 方法作为后备
3. 添加详细的注释和文档

**文件修改**:
- `stock-crawler/src/markdown-generator.js`
  - 添加 `cleanTitle()` 方法
  - 添加 `extractKeyParts()` 方法
  - 修改 `safeFilename()` 方法调用新逻辑
  - 添加 `ensureUniqueFilename()` 方法

### 阶段2: 单元测试 (半天)

1. 编写测试用例覆盖所有规则
2. 测试边界情况和特殊字符
3. 验证唯一性保证

**文件创建**:
- `stock-crawler/test/filename-generator.test.js`

### 阶段3: 集成测试 (半天)

1. 对现有188个URL进行模拟文件名生成
2. 检查是否有冲突
3. 验证文件名长度分布
4. 人工审查可读性

**脚本创建**:
- `stock-crawler/scripts/test-filename-generation.js`

### 阶段4: 部署和监控 (半天)

1. 更新配置和文档
2. 在新抓取中启用新策略
3. 监控文件名生成效果
4. 收集反馈并调整

### 阶段5: 迁移 (可选)

如果需要重命名现有文件：

1. 编写迁移脚本
2. 生成新旧文件名映射表
3. 批量重命名文件和文件夹
4. 更新 links.txt 中的记录

**脚本创建**:
- `stock-crawler/scripts/migrate-filenames.js`

## 风险和缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| URL规则不完善导致冲突 | 中 | 中 | 保留数字后缀作为后备方案 |
| 文件名仍然过长 | 低 | 低 | 实施严格的长度限制和截断规则 |
| 特殊字符处理不当 | 低 | 中 | 充分测试各种特殊字符 |
| 迁移脚本出错 | 低 | 高 | 先在测试环境验证，保留备份 |
| 用户不习惯新文件名 | 低 | 低 | 新旧文件名可共存，逐步迁移 |

## 成功指标

1. **唯一性**: 冲突率 < 1%（需要数字后缀的文件）
2. **长度**: 平均文件名长度 < 40字符
3. **可读性**: 人工审查通过率 > 95%
4. **性能**: 文件名生成时间 < 10ms

## 后续优化

1. **机器学习优化**: 根据实际使用情况，自动学习最佳关键字提取规则
2. **用户自定义**: 允许用户配置文件名生成规则
3. **智能缩写**: 对常见长词进行智能缩写（如"居民消费价格指数" → "CPI"）
4. **分类目录**: 考虑引入一级分类目录，进一步简化文件名

## 参考资料

- 文件名调研报告: `FILENAME_RESEARCH.md`
- 数据分析报告: `DATA_ANALYSIS_REPORT.md`
- URL工具函数: `src/url-utils.js`
- Markdown生成器: `src/markdown-generator.js`
