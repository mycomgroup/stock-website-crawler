# 数据质量调研总结报告

生成时间: 2026-02-25

## 执行概要

对已抓取的188个页面（3,006张图片）进行了全面的数据质量分析，识别了3个主要问题领域并提供了详细的解决方案。

## 调研范围

- **数据集**: 188个markdown文件，3,006张图片
- **输出目录**: `stock-crawler/output/lixinger-crawler/pages/`
- **分析维度**: 文件重复性、内容完整性、文件命名规范

## 主要发现

### 1. "重复"文件问题 ✅ 已澄清

**初步发现**: 42个文件（22%）使用了哈希后缀，疑似重复

**调研结论**: ❌ 不是重复，是不同页面

**详细分析**:

| 类型 | 示例 | 差异点 |
|------|------|--------|
| 不同订阅周期 | `费用_我的_-_理杏仁.md` vs `费用_我的_-_理杏仁_841dc123.md` | weekly vs annually |
| 不同市场 | `样本信息API购买.md` vs `样本信息API购买_23a63f7e.md` | HK vs US |
| 不同数据粒度 | `大陆_货币供应_宏观_-_理杏仁.md` (37KB) vs `大陆_货币供应_宏观_-_理杏仁_c210a99b.md` (361KB) | 概览 vs 详细历史数据 |
| 不同参数 | `国家财政_宏观_-_理杏仁.md` (12KB) vs `国家财政_宏观_-_理杏仁_0ec4011e.md` (94KB) | 默认 vs 年度粒度 |

**结论**: 哈希后缀是必要的，用于区分相同标题但不同URL参数的页面。

**建议**: ✅ 保持现状，但可以优化文件名策略使其更直观（见问题3）

---

### 2. 空页面问题 ✅ 大部分正常

**初步发现**: 16个小文件（< 1KB），疑似抓取失败

**调研结论**: 
- ✅ 9个是正常的空数据页面（用户无数据）
- ✅ 7个是有效的小文件
- ⚠️ 1个包含`undefined`参数（需要修复）

#### 分类详情

**A. 正常的空数据页面（9个）**

这些页面抓取成功，只是用户账号没有相关数据：

```
我的税务_概况_-_理杏仁.md - "没有相关数据"
我的发票_费用_我的_-_理杏仁.md - "您还没有创建任何发票"
系统奖励_费用_我的_-_理杏仁.md - "您还没有任何系统奖励"
全部_我的资源文件_概况_-_理杏仁.md - "暂无文件"
excel列表_我的资源文件_概况_-_理杏仁.md - "暂无文件"
搜索_天眼_-_理杏仁_0a25602d.md - "没有相关数据"
```

**B. 有效的小文件（7个）**

虽然文件小，但包含有效内容：

```
自定义_制图_-_理杏仁_89fbaa64.md (262 bytes) - 包含表格数据
指数跟踪基金信息API购买.md (948 bytes) - API文档
```

**C. 问题页面（1个）**

```
API文档_开放平台_-_理杏仁.md (111 bytes)
URL: https://www.lixinger.com/open/api/doc?api-key=macro/undefined
问题: URL参数包含 undefined
```

**建议**: 
- ✅ 保留A类和B类文件
- ⚠️ 修复C类问题（见详细方案）

---

### 3. 文件名策略问题 📋 需要优化

**初步发现**: 
- 文件名较长（平均42字符，最长83字符）
- 哈希后缀不直观（无法从文件名看出差异）
- 包含冗余后缀（`_-_理杏仁`）

**调研结论**: 需要改进文件名生成策略

#### 当前策略的问题

```
格式: {页面标题}_{层级}_-_{网站名}.md + 哈希后缀（如有冲突）
示例: 居民消费价格指数_大陆_价格指数_宏观_-_理杏仁.md (42字符)
     非金融_基本面数据_公司接口_大陆_API文档_开放平台_-_理杏仁.md (83字符)
```

**问题**:
1. 文件名过长，不便于浏览
2. 哈希后缀（如`_841dc123`）不直观
3. 包含冗余信息（`_-_理杏仁`）
4. 无法从文件名看出页面的关键差异

#### 推荐的新策略

```
格式: {清理后的标题}_{URL关键部分}.md
示例: 居民消费价格指数_cn_cpi.md (25字符)
     样本信息API_us_index_constituents.md (35字符)
```

**改进点**:
1. ✓ 去除网站名后缀
2. ✓ 用URL关键部分替代哈希
3. ✓ 文件名更短（平均35字符）
4. ✓ 更直观（能看出市场、类型等关键信息）

#### 效果对比

| 当前文件名 | 新文件名 | 长度变化 | 可读性 |
|-----------|---------|---------|--------|
| `费用_我的_-_理杏仁_841dc123.md` (30) | `费用_我的_annually.md` (20) | -33% | ⬆️ |
| `样本信息API购买_23a63f7e.md` (26) | `样本信息API_us_index_constituents.md` (35) | +35% | ⬆️⬆️ |
| `大陆_货币供应_宏观_-_理杏仁_c210a99b.md` (38) | `货币供应_cn.md` (14) | -63% | ⬆️ |
| `居民消费价格指数_大陆_价格指数_宏观_-_理杏仁.md` (42) | `居民消费价格指数_cn_cpi.md` (25) | -40% | ⬆️ |

**建议**: 实施新的文件名生成策略（见详细设计文档）

---

## 详细解决方案

### 问题1: "重复"文件 ✅ 无需处理

**结论**: 这些文件不是重复，是不同的页面，保持现状即可。

**理由**: 
- 哈希后缀有效区分了相同标题但不同URL的页面
- 文件内容确实不同（不同市场、周期、粒度等）
- 删除会导致数据丢失

**后续优化**: 通过改进文件名策略（问题3的方案）使差异更直观。

---

### 问题2: undefined URL参数 ⚠️ 需要修复

**问题**: 2个URL包含`undefined`参数

```
https://www.lixinger.com/open/api/doc?api-key=macro/undefined
https://www.lixinger.com/open/api/detail?api-key=undefined
```

**根本原因**: 链接提取时没有验证参数值的有效性

**解决方案**: 多层防御策略

#### 方案A: 链接提取时过滤（第一道防线）

修改 `link-finder.js`:

```javascript
// 在 extractLinks 方法中添加验证
const apiKey = urlObj.searchParams.get('api-key');
if (!apiKey || apiKey === 'undefined' || apiKey === 'null' || apiKey.trim() === '') {
  continue; // 跳过无效链接
}
```

#### 方案B: URL过滤时排除（第二道防线）

修改 `url-utils.js`:

```javascript
export function isValidUrl(url) {
  try {
    const urlObj = new URL(url);
    for (const [key, value] of urlObj.searchParams.entries()) {
      if (value === 'undefined' || value === 'null' || value.trim() === '') {
        return false;
      }
    }
    return true;
  } catch {
    return false;
  }
}
```

#### 方案C: 保存前验证（最后防线）

修改 `link-manager.js`:

```javascript
addLinks(urls) {
  const validUrls = urls.filter(url => isValidUrl(url));
  // ... 添加有效的URL
}
```

**实施步骤**:
1. 修改3个文件添加验证逻辑
2. 创建清理脚本删除现有的2个无效链接
3. 删除无效的markdown文件
4. 添加监控指标跟踪跳过的无效URL数量

**详细文档**: `UNDEFINED_URL_ISSUE.md`

---

### 问题3: 文件名策略 📋 需要设计和实施

**目标**: 
- 文件名直观（能看出页面内容和关键差异）
- 文件名简洁（平均35字符，最长60字符）
- 避免冲突（唯一性保证）

**核心策略**: "标题 + URL关键部分"

#### 实现规则

**1. 标题清理**

```javascript
function cleanTitle(title) {
  return title
    .replace(/\|/g, '_')              // 管道符转下划线
    .replace(/\s+/g, '_')             // 空格转下划线
    .replace(/_-_理杏仁$/i, '')       // 移除网站名后缀
    .replace(/[\/\\?*:|"<>]/g, '_')   // 替换非法字符
    .replace(/_{2,}/g, '_')           // 合并多个下划线
    .replace(/^_|_$/g, '');           // 移除首尾下划线
}
```

**2. URL关键部分提取**

优先级顺序：
1. 市场代码（cn/hk/us/a/b/h）
2. 数据类型/周期（weekly/monthly/annually/daily/custom）
3. API Key路径（取最后2段）
4. 查询参数关键字（chart-granularity/date-range等）
5. 路径段关键字（index/constituents/fundamental等）

```javascript
function extractKeyParts(url) {
  const parts = [];
  const urlObj = new URL(url);
  
  // 提取市场代码
  if (url.includes('/cn/') || url.includes('=cn')) parts.push('cn');
  if (url.includes('/hk/') || url.includes('=hk')) parts.push('hk');
  if (url.includes('/us/') || url.includes('=us')) parts.push('us');
  
  // 提取数据类型
  if (url.includes('weekly')) parts.push('weekly');
  if (url.includes('annually')) parts.push('annually');
  
  // 提取API Key关键部分
  const apiKey = urlObj.searchParams.get('api-key');
  if (apiKey && apiKey !== 'undefined') {
    const keyParts = apiKey.split('/').slice(-2).join('_');
    parts.push(keyParts);
  }
  
  return parts.slice(0, 3); // 最多3个关键字
}
```

**3. 文件名组合**

```javascript
function generateFilename(title, url) {
  const cleanedTitle = cleanTitle(title);
  const urlParts = extractKeyParts(url);
  
  let filename = cleanedTitle;
  if (urlParts.length > 0) {
    filename += '_' + urlParts.join('_');
  }
  
  // 限制长度
  if (filename.length > 60) {
    filename = cleanedTitle.substring(0, 40) + '_' + 
               urlParts.slice(0, 2).join('_').substring(0, 18);
  }
  
  return filename + '.md';
}
```

**4. 冲突处理**

如果仍有冲突（极少情况），添加数字后缀：

```javascript
function ensureUniqueFilename(filename, existingFiles) {
  if (!existingFiles.has(filename)) {
    return filename;
  }
  
  let counter = 2;
  while (existingFiles.has(`${baseName}_${counter}.md`)) {
    counter++;
  }
  
  return `${baseName}_${counter}.md`;
}
```

#### 实施计划

**阶段1: 代码实现（1天）**
- 修改 `markdown-generator.js`
- 添加新的文件名生成方法
- 保留旧方法作为后备

**阶段2: 单元测试（半天）**
- 编写测试用例
- 测试边界情况
- 验证唯一性

**阶段3: 集成测试（半天）**
- 对现有188个URL模拟生成
- 检查冲突率
- 验证长度分布
- 人工审查可读性

**阶段4: 部署监控（半天）**
- 在新抓取中启用
- 监控效果
- 收集反馈

**阶段5: 迁移（可选）**
- 编写迁移脚本
- 重命名现有文件
- 更新links.txt

**详细文档**: `FILENAME_STRATEGY.md`

---

## 数据质量指标

### 当前状态

| 指标 | 数值 | 状态 |
|------|------|------|
| 总文件数 | 188 | ✅ |
| 总图片数 | 3,006 | ✅ |
| 重复文件 | 0 | ✅ |
| 空数据页面 | 9 (4.8%) | ✅ 正常 |
| 有效小文件 | 7 (3.7%) | ✅ |
| 无效URL | 2 (1.1%) | ⚠️ 需修复 |
| 使用哈希后缀 | 42 (22%) | ⚠️ 可优化 |
| 平均文件名长度 | 42字符 | ⚠️ 可优化 |
| 最长文件名 | 83字符 | ⚠️ 可优化 |

### 目标状态（实施后）

| 指标 | 目标值 | 改进 |
|------|--------|------|
| 无效URL | 0 | ✅ 完全消除 |
| 使用数字后缀 | < 2 (< 1%) | ⬆️ 从22%降至<1% |
| 平均文件名长度 | 35字符 | ⬆️ 减少17% |
| 最长文件名 | 60字符 | ⬆️ 减少28% |
| 文件名可读性 | > 95% | ⬆️ 显著提升 |

---

## 实施优先级

### 高优先级（立即实施）

1. **修复undefined URL问题**
   - 影响: 2个无效页面
   - 工作量: 半天
   - 风险: 低
   - 文档: `UNDEFINED_URL_ISSUE.md`

### 中优先级（1-2周内）

2. **实施新文件名策略**
   - 影响: 所有新抓取的页面
   - 工作量: 2-3天
   - 风险: 中（需充分测试）
   - 文档: `FILENAME_STRATEGY.md`

### 低优先级（可选）

3. **迁移现有文件名**
   - 影响: 188个现有文件
   - 工作量: 1天
   - 风险: 中（需要备份）
   - 前提: 新策略运行稳定后

---

## 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| URL验证过于严格导致漏抓 | 低 | 中 | 详细日志记录，定期审查 |
| 新文件名策略仍有冲突 | 低 | 低 | 保留数字后缀作为后备 |
| 文件名规则不完善 | 中 | 中 | 充分测试，逐步优化 |
| 迁移脚本出错 | 低 | 高 | 先在测试环境验证，保留备份 |

---

## 成功标准

### 短期（1周）

- ✅ 无效URL问题完全修复
- ✅ 不再生成包含`undefined`的链接
- ✅ 添加了URL验证的监控指标

### 中期（2-3周）

- ✅ 新文件名策略实施并稳定运行
- ✅ 新抓取的页面文件名符合新规范
- ✅ 文件名冲突率 < 1%
- ✅ 平均文件名长度 < 40字符

### 长期（1-2月）

- ✅ 现有文件迁移完成（如果需要）
- ✅ 文件名可读性人工审查通过率 > 95%
- ✅ 用户反馈积极

---

## 相关文档

### 详细设计文档

1. **FILENAME_RESEARCH.md** - 文件名问题调研报告
   - 重复文件分析
   - 空页面分析
   - 文件名策略对比

2. **FILENAME_STRATEGY.md** - 文件名生成策略详细设计
   - 实现规则
   - 测试用例
   - 实施计划

3. **UNDEFINED_URL_ISSUE.md** - undefined参数问题分析
   - 问题定位
   - 解决方案
   - 实施步骤

### 数据分析文档

4. **DATA_ANALYSIS_REPORT.md** - 初步数据分析报告
   - 文件统计
   - 初步发现

### 代码文件

5. **src/markdown-generator.js** - 文件名生成逻辑
6. **src/link-finder.js** - 链接提取逻辑
7. **src/url-utils.js** - URL过滤逻辑
8. **src/link-manager.js** - 链接管理逻辑

---

## 下一步行动

### 立即执行

1. ✅ 阅读并确认本调研报告
2. ⏭️ 实施undefined URL修复方案
3. ⏭️ 运行清理脚本删除无效链接

### 本周内

4. ⏭️ 审查文件名策略设计
5. ⏭️ 开始实施新文件名策略
6. ⏭️ 编写单元测试

### 下周

7. ⏭️ 集成测试新文件名策略
8. ⏭️ 在新抓取中启用新策略
9. ⏭️ 监控效果并收集反馈

---

## 总结

经过全面的数据质量分析，我们发现：

1. **"重复"文件不是问题** - 它们是不同的页面，哈希后缀是必要的
2. **空页面大部分正常** - 只有2个URL包含`undefined`需要修复
3. **文件名策略需要优化** - 新策略将使文件名更短、更直观

所有问题都有明确的解决方案和详细的实施计划。优先修复undefined URL问题（半天工作量），然后实施新的文件名策略（2-3天工作量）。

**总体评估**: 数据质量良好，发现的问题都是可以优化的细节，不影响核心功能。
