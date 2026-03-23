# URL 优先级排序规则

## 概述

爬虫在选择要抓取的 URL 时，会按照以下优先级规则进行排序，确保先抓取最重要的页面。

## 排序规则（从高到低）

### 0. 种子 URL（最高优先级）

配置文件中的 `seedUrls` 总是最先处理，无论其状态如何。

### 1. URL长度

**规则**：URL 字符串越短，优先级越高

**原因**：
- 较短的 URL 通常是更高层级的页面或主要入口
- 作为最直观的优先级判断标准，可以快速筛选出重要页面

**示例**：
```
优先级从高到低：
1. https://example.com/company
2. https://example.com/analytics/macro
3. https://example.com/analytics/macro/cpi
4. https://example.com/company/600519/detail
```

### 2. 路径深度（Path Depth）

**规则**：路径中 `/` 的数量越少，优先级越高

**原因**：
- 路径越浅的页面通常是一级或二级导航页面
- 这些页面是网站的入口，包含大量指向其他页面的链接
- 优先抓取这些页面可以快速发现更多有价值的 URL

**示例**：
```
优先级从高到低：
1. https://example.com/company                    (2 个/)
2. https://example.com/analytics/macro            (3 个/)
3. https://example.com/analytics/macro/cpi        (4 个/)
4. https://example.com/company/600519/detail      (4 个/)
```

### 3. 包含数字路径段的URL

**规则**：路径中包含纯数字段的URL 优先

**匹配模式**：`/数字/` 或 `/数字` 结尾

**原因**：
- 这类 URL 通常是具体的数据页面（如公司详情、产品页面）
- 包含实际的业务数据，而非导航页面

**示例**：
```
✓ /company/600519
✓ /product/123
✓ /2024/report
✗ /company/list
```

### 4. 不含查询参数的URL

**规则**：不包含 `?`, `&`, `=` 的 URL 优先

**原因**：
- 这类 URL 通常是主要页面，而非筛选或过滤后的结果
- 避免重复抓取相似内容（如不同筛选条件的搜索结果）

**示例**：
```
优先：/analytics/macro/cpi
次要：/search?keyword=股票&page=2
```

## 完整排序示例

假设有以下 URL：

```
A. https://example.com/company                           (长度短，2 个/, 无数字，无参数)
B. https://example.com/analytics/macro                   (长度中，3 个/, 无数字，无参数)
C. https://example.com/company/600519                    (长度中，3 个/, 有数字，无参数)
D. https://example.com/analytics/macro/cpi               (长度长，4 个/, 无数字，无参数)
E. https://example.com/company/600519/detail             (长度长，4 个/, 有数字，无参数)
F. https://example.com/search?q=test                     (长度短，2 个/, 无数字，有参数)
G. https://example.com/analytics/macro/cpi?year=2024     (长度长，4 个/, 无数字，有参数)
```

排序后的顺序（**注意**：现在 **URL长度**是第一优先级）：

```
1. A - https://example.com/company                       (长度最短，深度 2, 无数字，无参数)
2. F - https://example.com/search?q=test                 (长度短，深度 2, 无数字，有参数)
3. B - https://example.com/analytics/macro               (长度中等，深度 3, 无数字，无参数)
4. C - https://example.com/company/600519                (长度中等，深度 3, 有数字，无参数)
5. D - https://example.com/analytics/macro/cpi           (长度较长，深度 4, 无数字，无参数)
6. E - https://example.com/company/600519/detail         (长度较长，深度 4, 有数字，无参数)
7. G - https://example.com/analytics/macro/cpi?year=2024 (长度最长，深度 4, 无数字，有参数)
```

## 实现细节

### 路径深度计算

```javascript
const getPathDepth = (url) => {
  try {
    const urlObj = new URL(url);
    // 只计算路径部分的斜杠数量（不包括域名）
    return (urlObj.pathname.match(/\//g) || []).length;
  } catch {
    // 如果URL解析失败，直接计数整个URL的斜杠
    return (url.match(/\//g) || []).length;
  }
};
```

### 数字路径段检测

```javascript
const hasNumericSegment = /\/\d+(?:\/|$)/.test(url);
```

### 查询参数检测

```javascript
const hasParams = url.includes('?') || url.includes('&') || url.includes('=');
```

## 配置

URL优先级排序是自动的，不需要额外配置。排序逻辑在 `crawler-main.js` 的 `start()` 方法中实现。

## 优势

1. **快速发现链接**：优先抓取浅层页面，快速建立网站结构图
2. **高效抓取**：先抓取入口页面，避免深入单一分支
3. **智能排序**：结合多个维度（深度、数字、参数、长度）进行综合判断
4. **避免重复**：降低查询参数页面的优先级，减少重复内容

## 调整建议

如果需要调整排序逻辑，可以修改 `stock-crawler/src/crawler-main.js` 中的排序函数。

例如，如果想提高某类特定URL的优先级，可以在排序函数中添加新的判断条件。
