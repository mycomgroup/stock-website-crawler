/**
 * 示例：生成模板分析报告
 * 
 * 演示如何使用TemplateContentAnalyzer生成JSON和Markdown格式的报告
 */

const TemplateContentAnalyzer = require('../lib/content-analyzer');
const fs = require('fs').promises;
const path = require('path');

async function main() {
  const analyzer = new TemplateContentAnalyzer();

  // 示例页面数据
  const pages = [
    `# API文档

## 导航
- 首页
- API列表
- 关于

## 获取公司基本信息

**简要描述**：获取指定公司的基本信息

**请求URL**：\`https://open.lixinger.com/api/cn/company\`

**请求方式**：GET

**参数**：

| 参数名称 | 必选 | 类型 | 说明 |
|---------|------|------|------|
| stockCode | 是 | string | 股票代码 |
| date | 否 | string | 日期 |

**返回示例**：

\`\`\`json
{
  "code": 0,
  "message": "success",
  "data": {
    "stockCode": "600000",
    "name": "浦发银行"
  }
}
\`\`\`

© 2024 理杏仁`,

    `# API文档

## 导航
- 首页
- API列表
- 关于

## 获取指数基本信息

**简要描述**：获取指定指数的基本信息

**请求URL**：\`https://open.lixinger.com/api/cn/index\`

**请求方式**：GET

**参数**：

| 参数名称 | 必选 | 类型 | 说明 |
|---------|------|------|------|
| indexCode | 是 | string | 指数代码 |
| date | 否 | string | 日期 |

**返回示例**：

\`\`\`json
{
  "code": 0,
  "message": "success",
  "data": {
    "indexCode": "000001",
    "name": "上证指数"
  }
}
\`\`\`

© 2024 理杏仁`,

    `# API文档

## 导航
- 首页
- API列表
- 关于

## 获取行业基本信息

**简要描述**：获取指定行业的基本信息

**请求URL**：\`https://open.lixinger.com/api/cn/industry\`

**请求方式**：GET

**参数**：

| 参数名称 | 必选 | 类型 | 说明 |
|---------|------|------|------|
| industryCode | 是 | string | 行业代码 |

**返回示例**：

\`\`\`json
{
  "code": 0,
  "message": "success",
  "data": {
    "industryCode": "001",
    "name": "金融"
  }
}
\`\`\`

© 2024 理杏仁`
  ];

  // URL模式信息
  const urlPattern = {
    name: 'api-doc',
    pathTemplate: '/open/api/doc',
    pattern: '^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$',
    queryParams: ['api-key'],
    urlCount: 163
  };

  console.log('开始分析模板...\n');

  // 1. 执行完整的模板分析
  const analysisResult = analyzer.analyzeTemplate(pages, {
    thresholds: { template: 0.8, unique: 0.2 }
  });

  console.log('分析完成！统计信息：');
  console.log(`- 总页面数: ${analysisResult.stats.totalPages}`);
  console.log(`- 总内容块数: ${analysisResult.stats.totalBlocks}`);
  console.log(`- 模板内容块: ${analysisResult.stats.templateBlocks}`);
  console.log(`- 独特内容块: ${analysisResult.stats.uniqueBlocks}`);
  console.log(`- 混合内容块: ${analysisResult.stats.mixedBlocks}`);
  console.log(`- 表格结构类型: ${analysisResult.stats.tableStructures}`);
  console.log(`- 代码块类型: ${analysisResult.stats.codeBlockTypes}\n`);

  // 2. 生成JSON格式报告
  console.log('生成JSON报告...');
  const jsonReport = analyzer.generateAnalysisJSON(analysisResult, urlPattern);
  
  const jsonOutputPath = path.join(__dirname, 'analysis-report.json');
  await fs.writeFile(jsonOutputPath, JSON.stringify(jsonReport, null, 2), 'utf-8');
  console.log(`✓ JSON报告已保存到: ${jsonOutputPath}\n`);

  // 3. 生成Markdown格式报告
  console.log('生成Markdown报告...');
  const markdownReport = analyzer.generateAnalysisMarkdown(analysisResult, urlPattern);
  
  const mdOutputPath = path.join(__dirname, 'analysis-report.md');
  await fs.writeFile(mdOutputPath, markdownReport, 'utf-8');
  console.log(`✓ Markdown报告已保存到: ${mdOutputPath}\n`);

  // 4. 生成清洗前后对比示例
  console.log('生成清洗前后对比示例...');
  const cleaningExamples = analyzer.generateCleaningExamples(
    pages, 
    analysisResult.cleaningRules,
    { maxExamples: 2 }
  );

  console.log(`生成了 ${cleaningExamples.length} 个清洗示例：\n`);
  cleaningExamples.forEach((example, index) => {
    console.log(`示例 ${example.index}:`);
    console.log(`  原始长度: ${example.stats.originalLength} 字符`);
    console.log(`  清洗后长度: ${example.stats.cleanedLength} 字符`);
    console.log(`  减少: ${example.stats.reduction}`);
    console.log(`  移除: ${example.stats.removedLength} 字符\n`);
  });

  // 保存清洗示例
  const examplesOutputPath = path.join(__dirname, 'cleaning-examples.json');
  await fs.writeFile(examplesOutputPath, JSON.stringify(cleaningExamples, null, 2), 'utf-8');
  console.log(`✓ 清洗示例已保存到: ${examplesOutputPath}\n`);

  console.log('所有报告生成完成！');
}

// 运行示例
main().catch(error => {
  console.error('错误:', error);
  process.exit(1);
});
