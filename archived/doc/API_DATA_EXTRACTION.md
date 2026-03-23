# API数据提取功能

## 概述

爬虫现在支持自动拦截和提取页面的API响应数据，特别适用于数据通过JavaScript动态加载并渲染到图表中的页面。

## 问题背景

许多现代网站（特别是数据可视化网站）不使用HTML表格来展示数据，而是：
1. 通过API获取JSON数据
2. 使用JavaScript图表库（ECharts、Highcharts等）渲染图表
3. 数据只存在于JavaScript内存和Canvas/SVG中

传统的HTML解析无法获取这些数据，因此需要拦截API响应。

## 功能特性

### 1. 自动API响应拦截

爬虫会自动拦截页面加载过程中的所有API调用：
- 只拦截包含`/api/`的URL
- 只处理HTTP 200成功响应
- 只解析JSON格式的响应
- 只保存数组类型的数据（通常是数据列表）

### 2. 智能数据转换

将JSON数据自动转换为表格格式：
- **扁平化嵌套对象**：将多层嵌套的JSON展开为平面结构
- **动态列名**：自动识别所有字段作为表头
- **类型处理**：正确处理字符串、数字、日期、对象等类型
- **空值处理**：null和undefined转换为空字符串

### 3. 无缝集成

- 如果页面有HTML表格，优先使用HTML表格
- 如果没有HTML表格但有API数据，自动使用API数据
- API数据以相同格式保存到Markdown文件
- 支持流式写入和数据块回调

## 工作流程

```
1. 页面加载开始
   ↓
2. 设置API响应拦截器
   ↓
3. 页面加载过程中
   ├─ 拦截所有API调用
   ├─ 检查响应类型（JSON）
   ├─ 检查数据类型（数组）
   └─ 保存到apiData列表
   ↓
4. 页面加载完成
   ↓
5. 尝试提取HTML表格
   ├─ 找到表格：使用HTML表格
   └─ 未找到表格：检查apiData
   ↓
6. 如果有apiData
   ├─ 分析JSON结构
   ├─ 扁平化嵌套对象
   ├─ 生成表头和行数据
   └─ 转换为表格格式
   ↓
7. 保存到Markdown文件
```

## 使用场景

### 场景1：宏观数据页面（CPI、GDP等）

```
页面：https://www.lixinger.com/analytics/macro/price-index/cn/cpi
特点：
  - 数据通过API加载：/api/macro
  - 渲染为ECharts图表
  - 没有HTML表格

处理：
  1. 拦截API响应
  2. 提取JSON数据
  3. 转换为表格
  4. 保存到Markdown

结果：
  - 获取完整的历史CPI数据
  - 包含日期、同比、环比等字段
```

### 场景2：股票价格图表

```
页面：股票K线图
特点：
  - 价格数据通过API加载
  - 渲染为Canvas图表
  - 没有数据表格

处理：
  - 拦截价格数据API
  - 提取OHLC数据
  - 转换为表格格式
```

### 场景3：财务指标趋势图

```
页面：公司财务指标趋势
特点：
  - 多年财务数据通过API加载
  - 渲染为折线图
  - 没有数据表格

处理：
  - 拦截财务数据API
  - 提取各年度指标
  - 转换为表格格式
```

## 数据转换示例

### 输入：API JSON数据

```json
[
  {
    "areaCode": "cn",
    "date": "2024-01-30T16:00:00.000Z",
    "type": "pi",
    "m": {
      "cpi": { "t": -0.008 },
      "ccpi": { "t": 0.003 }
    }
  },
  {
    "areaCode": "cn",
    "date": "2023-12-30T16:00:00.000Z",
    "type": "pi",
    "m": {
      "cpi": { "t": -0.003 },
      "ccpi": { "t": 0.005 }
    }
  }
]
```

### 输出：Markdown表格

```markdown
## 表格 1

API数据: macro

| areaCode | date | type | m.cpi.t | m.ccpi.t |
| --- | --- | --- | --- | --- |
| cn | 2024-01-30T16:00:00.000Z | pi | -0.008 | 0.003 |
| cn | 2023-12-30T16:00:00.000Z | pi | -0.003 | 0.005 |
```

## 技术实现

### API响应拦截

```javascript
// 在parse方法开始时设置拦截器
const apiData = [];
page.on('response', async (response) => {
  const responseUrl = response.url();
  
  // 只拦截API调用
  if (responseUrl.includes('/api/') && response.status() === 200) {
    try {
      const contentType = response.headers()['content-type'] || '';
      if (contentType.includes('json')) {
        const data = await response.json();
        
        // 只保存数组数据
        if (Array.isArray(data) && data.length > 0) {
          apiData.push({ url: responseUrl, data: data });
        }
      }
    } catch (e) {
      // Ignore parsing errors
    }
  }
});
```

### 嵌套对象扁平化

```javascript
// 将嵌套对象展开为平面结构
const flattenedData = data.map(item => {
  const flat = {};
  
  for (const key of Object.keys(item)) {
    const value = item[key];
    
    if (value && typeof value === 'object') {
      // 嵌套对象，展开为 key.subKey
      for (const subKey of Object.keys(value)) {
        flat[`${key}.${subKey}`] = value[subKey];
      }
    } else {
      flat[key] = value;
    }
  }
  
  return flat;
});
```

### 表格生成

```javascript
// 获取所有列名
const allKeys = new Set();
flattenedData.forEach(item => {
  Object.keys(item).forEach(key => allKeys.add(key));
});
const headers = Array.from(allKeys);

// 转换为行数据
const rows = flattenedData.map(item => {
  return headers.map(header => {
    const value = item[header];
    return value === null || value === undefined ? '' : String(value);
  });
});
```

## 配置

API数据提取功能是自动的，不需要额外配置。爬虫会：
1. 自动拦截所有API响应
2. 自动识别数据格式
3. 自动转换为表格
4. 自动保存到Markdown

## 优势

1. **自动化**：无需手动分析API或编写提取脚本
2. **通用性**：适用于各种API数据格式
3. **完整性**：获取完整的原始数据，不受图表渲染限制
4. **准确性**：直接从API获取，避免OCR或图表解析错误
5. **高效性**：一次页面加载即可获取所有数据

## 限制

1. **API识别**：只拦截URL包含`/api/`的请求，特殊API路径可能遗漏
2. **数据格式**：只处理JSON数组格式，其他格式需要扩展
3. **嵌套深度**：目前支持2层嵌套，更深的嵌套可能需要调整
4. **数据量**：大量API调用可能产生很多表格

## 未来改进

1. 支持更多API路径模式识别
2. 支持非数组JSON数据（对象、嵌套结构等）
3. 智能合并相关API数据
4. 支持API数据过滤和筛选
5. 支持自定义数据转换规则

## 示例输出

对于CPI页面，现在可以获取：

```markdown
# 居民消费价格指数|大陆|价格指数|宏观 - 理杏仁

## 源URL

https://www.lixinger.com/analytics/macro/price-index/cn/cpi

## 表格 1

API数据: macro

| areaCode | date | type | m.cpi.t | m.ccpi.t |
| --- | --- | --- | --- | --- |
| cn | 2026-01-30T16:00:00.000Z | pi | | |
| cn | 2025-12-30T16:00:00.000Z | pi | 0.008 | 0.012 |
| cn | 2025-11-29T16:00:00.000Z | pi | -0.006 | 0.002 |
...（更多历史数据）
```

这样就成功获取了原本只在图表中显示的数据！
