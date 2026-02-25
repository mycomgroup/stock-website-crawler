# 分页抓取功能

## 概述

爬虫现在支持自动检测和抓取分页表格数据，并且采用流式写入方式，边抓取边写入文件，避免内存占用过大。

## 功能特性

### 1. 自动分页检测

爬虫会自动检测页面中的分页控件，支持多种分页样式：

- 标准分页组件（`.pagination`, `.pager`）
- "下一页"按钮（中文/英文）
- 带有`aria-label`的导航按钮
- 自定义分页控件

### 2. 流式数据写入

- **边抓边写**：每抓取一页数据立即写入文件
- **内存友好**：不需要等所有数据下载完才写入
- **实时进度**：可以看到实时的抓取进度

### 3. 表格结构检测

- 自动检测表格结构变化
- 结构一致时追加到同一表格
- 结构变化时创建新表格

## 工作流程

```
1. 访问页面
   ↓
2. 提取第一页表格数据
   ↓
3. 写入文件头和表头
   ↓
4. 写入第一页数据
   ↓
5. 检测是否有"下一页"按钮
   ↓
6. 点击"下一页"
   ↓
7. 等待新数据加载
   ↓
8. 提取当前页数据
   ↓
9. 检查表格结构是否一致
   ├─ 一致：追加数据行到文件
   └─ 不一致：创建新表格
   ↓
10. 重复步骤6-9直到没有下一页
```

## 使用示例

### 基本使用

爬虫会自动处理分页，无需额外配置：

```bash
npm run crawl config/lixinger.json
```

### 测试分页功能

```bash
npm run test:pagination
```

## 输出格式

### 单页表格

```markdown
# 页面标题

## 源URL

https://example.com/data

## 表格 1

| 列1 | 列2 | 列3 |
| --- | --- | --- |
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |
```

### 多页表格

```markdown
# 页面标题

## 源URL

https://example.com/data

## 表格 1

| 列1 | 列2 | 列3 |
| --- | --- | --- |
| 第1页数据1 | 数据2 | 数据3 |
| 第1页数据4 | 数据5 | 数据6 |
| 第2页数据1 | 数据2 | 数据3 |
| 第2页数据4 | 数据5 | 数据6 |
| 第3页数据1 | 数据2 | 数据3 |
...
```

### 结构变化的表格

```markdown
## 表格 1

| 列A | 列B |
| --- | --- |
| 数据1 | 数据2 |
| 数据3 | 数据4 |

## 表格 2 (结构变化)

| 列X | 列Y | 列Z |
| --- | --- | --- |
| 数据1 | 数据2 | 数据3 |
```

## 技术实现

### 分页检测

```javascript
// 查找分页控件
const paginationSelectors = [
  '.pagination',
  '.pager',
  '[class*="pagination"]',
  'nav[aria-label*="pagination"]'
];

// 查找"下一页"按钮
const nextButtonSelectors = [
  'button:has-text("下一页")',
  'a:has-text("下一页")',
  'button:has-text("Next")',
  '.next:not(.disabled)'
];
```

### 流式写入

```javascript
const onDataChunk = async (chunk) => {
  if (chunk.isFirstPage) {
    // 写入表头
    fs.writeFileSync(filepath, header);
  } else {
    // 追加数据行
    fs.appendFileSync(filepath, rows);
  }
};

await parser.parse(page, url, { onDataChunk });
```

### 表格结构比较

```javascript
compareHeaders(headers1, headers2) {
  if (headers1.length !== headers2.length) {
    return false;
  }
  
  for (let i = 0; i < headers1.length; i++) {
    if (headers1[i] !== headers2[i]) {
      return false;
    }
  }
  
  return true;
}
```

## 配置选项

### 最大页数限制

默认最多抓取100页，可以在代码中修改：

```javascript
// generic-parser.js
const maxPages = paginationInfo.totalPages || 100;
```

### 翻页等待时间

```javascript
// 等待新数据加载
await page.waitForTimeout(1000);

// 避免过快翻页
await page.waitForTimeout(500);
```

## 日志输出

抓取过程中会输出详细日志：

```
Table 1 has pagination, extracting all pages...
Extracting page 2...
Appended 20 rows to table 1, page 2
Extracting page 3...
Appended 20 rows to table 1, page 3
...
Reached last page at page 10
```

## 错误处理

### 分页按钮不可点击

- 自动检测按钮是否disabled
- 检测按钮是否有disabled class
- 检测aria-disabled属性

### 页面加载超时

- 使用合理的等待时间
- 捕获并记录错误
- 继续处理下一个表格

### 表格结构变化

- 自动检测结构变化
- 创建新表格而不是追加
- 记录日志说明原因

## 性能优化

### 1. 批量写入

虽然是流式写入，但每页数据作为一个批次写入，减少I/O操作。

### 2. 智能等待

- 使用`waitForTimeout`而不是固定延迟
- 根据页面加载情况调整等待时间

### 3. 内存管理

- 不在内存中保存所有数据
- 每页数据写入后即可释放
- 适合处理大量数据

## 限制和注意事项

### 1. JavaScript渲染的分页

- 支持大多数JavaScript分页
- 需要等待DOM更新
- 可能需要调整等待时间

### 2. 无限滚动

- 当前不支持无限滚动
- 只支持按钮式分页
- 未来可能添加支持

### 3. 动态表格

- 支持动态加载的表格
- 需要等待数据加载完成
- 可能需要增加等待时间

## 故障排除

### 问题：分页没有被检测到

**原因**：分页控件使用了非标准的class或结构

**解决**：在`generic-parser.js`的`findPaginationControls`方法中添加新的选择器

### 问题：数据重复

**原因**：翻页后表格没有更新

**解决**：增加`waitForTimeout`时间，确保数据加载完成

### 问题：表格结构频繁变化

**原因**：表格包含动态内容或广告

**解决**：检查表格选择器，排除干扰元素

## 未来改进

- [ ] 支持无限滚动
- [ ] 支持Ajax分页
- [ ] 可配置的分页选择器
- [ ] 断点续传功能
- [ ] 并行抓取多个表格
- [ ] 自动重试失败的页面

## 示例代码

### 自定义数据处理

```javascript
const onDataChunk = async (chunk) => {
  // 自定义处理逻辑
  if (chunk.type === 'table') {
    console.log(`Processing table ${chunk.tableIndex}, page ${chunk.page}`);
    
    // 可以进行数据清洗、转换等操作
    const cleanedRows = chunk.rows.map(row => 
      row.map(cell => cell.trim())
    );
    
    // 写入数据库、发送到API等
    await saveToDatabase(cleanedRows);
  }
};
```

### 监控抓取进度

```javascript
let totalRows = 0;
const onDataChunk = async (chunk) => {
  if (chunk.rows) {
    totalRows += chunk.rows.length;
    console.log(`Total rows extracted: ${totalRows}`);
  }
};
```

## 总结

分页抓取功能使爬虫能够：
- 自动处理多页数据
- 实时写入避免内存问题
- 智能处理表格结构变化
- 提供详细的抓取日志

这使得爬虫可以处理大规模数据抓取任务，同时保持良好的性能和稳定性。
