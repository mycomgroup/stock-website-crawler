# Markdown文件读取器

## 概述

为TemplateContentAnalyzer添加了markdown文件读取功能，支持批量加载、URL模式匹配和流式处理。

## 实现的方法

### 1. loadMarkdownPages(filePaths, options)

批量加载markdown页面，使用异步生成器实现流式处理。

**参数**:
- `filePaths`: markdown文件路径数组
- `options.batchSize`: 批次大小，默认100

**返回**: AsyncGenerator，每次yield一批页面数据

**特性**:
- 流式处理，避免内存溢出
- 自动处理读取错误，不中断整体流程
- 返回包含filePath、fileName、content、size的页面对象

**示例**:
```javascript
for await (const batch of analyzer.loadMarkdownPages(files, { batchSize: 100 })) {
  batch.forEach(page => {
    console.log(`加载: ${page.fileName}, 大小: ${page.size}`);
  });
}
```

### 2. matchPagesToURLs(urlPattern, pagesDir)

根据URL模式匹配markdown文件。

**参数**:
- `urlPattern`: URL模式对象（包含name、pathTemplate、pattern）
- `pagesDir`: pages目录路径

**返回**: Promise<Array<string>> 匹配的文件路径数组

**特性**:
- 递归扫描目录及子目录
- 基于pathTemplate和name进行智能匹配
- 自动处理文件名标准化（忽略下划线、连字符、空格）

**示例**:
```javascript
const urlPattern = {
  name: 'api-doc',
  pathTemplate: '/open/api/doc',
  pattern: '^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$'
};

const matchedFiles = await analyzer.matchPagesToURLs(urlPattern, pagesDir);
console.log(`找到 ${matchedFiles.length} 个匹配文件`);
```

### 3. _getAllMarkdownFiles(dir) [私有方法]

递归获取目录下所有markdown文件。

**特性**:
- 递归扫描子目录
- 只返回.md文件
- 自动处理读取错误

### 4. _fileMatchesPattern(fileName, urlPattern) [私有方法]

检查文件名是否匹配URL模式。

**匹配逻辑**:
1. 从pathTemplate提取关键部分（非参数部分）
2. 如果没有关键部分，使用name
3. 标准化文件名和模式（移除下划线、连字符、空格）
4. 检查文件名是否包含任一关键部分

## 测试

### 单元测试

位置: `test/content-analyzer.test.js`

包含以下测试用例:
- 测试16: 批量加载markdown页面
- 测试17: 匹配URL模式和markdown文件
- 测试18: 处理读取失败的文件
- 测试19: 流式处理避免内存溢出

### 集成测试

位置: `test/test-markdown-reader.js`

使用真实数据测试:
- 匹配URL模式到文件
- 批量加载页面（流式处理）
- 分析页面内容

**测试结果**:
```
测试1: 匹配URL模式到文件...
✓ 找到 34 个匹配的文件

测试2: 批量加载页面（流式处理）...
✓ 找到 34 个基金相关文件
✓ 总共处理 4 个批次，总大小: 2507.68 KB

测试3: 分析页面内容...
✓ 找到 2 个CSV相关文件
✓ 分析结果:
  - 总页面数: 2
  - 总内容块: 40
  - 模板内容: 3
  - 独特内容: 0
  - 混合内容: 37
```

## 性能特性

1. **流式处理**: 使用异步生成器，按批次加载文件，避免一次性加载所有文件导致内存溢出
2. **批次大小可配置**: 默认100个文件一批，可根据实际情况调整
3. **错误容错**: 单个文件读取失败不影响其他文件的处理
4. **递归扫描**: 自动扫描子目录，无需手动遍历

## 使用场景

1. **模板内容分析**: 加载同一URL模式的所有页面，分析模板内容和独特数据
2. **批量数据处理**: 处理大量markdown文件时，使用流式处理避免内存问题
3. **URL模式匹配**: 根据URL模式自动找到对应的markdown文件

## 依赖

- `fs/promises`: 异步文件操作
- `path`: 路径处理

## 下一步

这些方法为后续的模板分析功能提供了基础:
- 2.3 数据结构识别
- 2.4 生成清洗规则
- 2.5 生成模板分析报告
