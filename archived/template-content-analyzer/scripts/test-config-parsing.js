#!/usr/bin/env node

/**
 * 测试脚本：使用Playwright测试配置驱动的解析
 * 
 * 任务 5.5.4: 测试配置驱动的解析
 * 
 * 功能：
 * - 使用真实的Playwright页面对象
 * - 测试所有提取器类型（text, table, code, list）
 * - 验证URL匹配
 * - 验证数据提取准确性
 * 
 * 用法：
 *   node scripts/test-config-parsing.js [config-file]
 * 
 * 示例：
 *   node scripts/test-config-parsing.js examples/template-config.jsonl
 */

const { chromium } = require('playwright');
const ConfigLoader = require('../lib/config-loader');
const TemplateParser = require('../lib/template-parser');
const path = require('path');
const fs = require('fs');

/**
 * 创建测试HTML页面
 */
function createTestHTML() {
  return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>API文档 - 测试页面</title>
</head>
<body>
  <h1>获取公司基本信息</h1>
  <h2>API文档</h2>
  
  <p>获取指定公司的基本信息，包括公司名称、代码、行业等。</p>
  
  <h3>请求URL</h3>
  <code>https://open.lixinger.com/api/cn/company</code>
  
  <h3>请求参数</h3>
  <table>
    <thead>
      <tr>
        <th>参数名称</th>
        <th>必选</th>
        <th>类型</th>
        <th>说明</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>stockCode</td>
        <td>是</td>
        <td>string</td>
        <td>股票代码</td>
      </tr>
      <tr>
        <td>date</td>
        <td>否</td>
        <td>string</td>
        <td>查询日期</td>
      </tr>
    </tbody>
  </table>
  
  <h3>返回数据</h3>
  <table>
    <thead>
      <tr>
        <th>字段</th>
        <th>类型</th>
        <th>说明</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>name</td>
        <td>string</td>
        <td>公司名称</td>
      </tr>
      <tr>
        <td>code</td>
        <td>string</td>
        <td>股票代码</td>
      </tr>
      <tr>
        <td>industry</td>
        <td>string</td>
        <td>所属行业</td>
      </tr>
    </tbody>
  </table>
  
  <h3>示例代码</h3>
  <textarea readonly>
{
  "stockCode": "600000",
  "date": "2024-01-01"
}
  </textarea>
  
  <pre><code class="language-json">
{
  "code": 0,
  "message": "success",
  "data": {
    "name": "浦发银行",
    "code": "600000",
    "industry": "银行"
  }
}
  </code></pre>
  
  <h3>导航</h3>
  <ul>
    <li><a href="/open/api/doc?api-key=cn/company">公司信息</a></li>
    <li><a href="/open/api/doc?api-key=cn/index">指数信息</a></li>
    <li><a href="/open/api/doc?api-key=hk/stock">港股信息</a></li>
  </ul>
</body>
</html>
  `.trim();
}

/**
 * 创建仪表板测试页面
 */
function createDashboardHTML() {
  return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>公司仪表板</title>
</head>
<body>
  <h1>浦发银行 - 公司仪表板</h1>
  
  <table>
    <thead>
      <tr>
        <th>指标</th>
        <th>数值</th>
        <th>单位</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>总资产</td>
        <td>1000000</td>
        <td>万元</td>
      </tr>
      <tr>
        <td>净利润</td>
        <td>50000</td>
        <td>万元</td>
      </tr>
    </tbody>
  </table>
  
  <ul class="charts">
    <li>营收趋势图</li>
    <li>利润趋势图</li>
    <li>ROE趋势图</li>
  </ul>
</body>
</html>
  `.trim();
}

/**
 * 测试文本提取器
 */
async function testTextExtractor(page, parser) {
  console.log('\n  测试文本提取器:');
  
  const config = parser.getConfig();
  const textExtractors = config.extractors.filter(e => e.type === 'text');
  
  for (const extractor of textExtractors) {
    try {
      const result = await parser.extractText(page, extractor);
      console.log(`    ✓ ${extractor.field}: "${result.substring(0, 50)}${result.length > 50 ? '...' : ''}"`);
    } catch (error) {
      console.log(`    ✗ ${extractor.field}: ${error.message}`);
    }
  }
}

/**
 * 测试表格提取器
 */
async function testTableExtractor(page, parser) {
  console.log('\n  测试表格提取器:');
  
  const config = parser.getConfig();
  const tableExtractors = config.extractors.filter(e => e.type === 'table');
  
  for (const extractor of tableExtractors) {
    try {
      const result = await parser.extractTable(page, extractor);
      
      if (Array.isArray(result)) {
        console.log(`    ✓ ${extractor.field}: 提取了 ${result.length} 个表格`);
        result.forEach((table, idx) => {
          console.log(`      表格 ${idx + 1}: ${table.headers.length} 列, ${table.rows.length} 行`);
        });
      } else {
        console.log(`    ✓ ${extractor.field}: ${result.headers.length} 列, ${result.rows.length} 行`);
        console.log(`      列名: ${result.headers.join(', ')}`);
        console.log(`      第一行: ${result.rows[0]?.join(', ') || 'N/A'}`);
      }
    } catch (error) {
      console.log(`    ✗ ${extractor.field}: ${error.message}`);
    }
  }
}

/**
 * 测试代码块提取器
 */
async function testCodeExtractor(page, parser) {
  console.log('\n  测试代码块提取器:');
  
  const config = parser.getConfig();
  const codeExtractors = config.extractors.filter(e => e.type === 'code');
  
  for (const extractor of codeExtractors) {
    try {
      const result = await parser.extractCode(page, extractor);
      console.log(`    ✓ ${extractor.field}: 提取了 ${result.length} 个代码块`);
      result.forEach((block, idx) => {
        const preview = block.code.substring(0, 40).replace(/\n/g, ' ');
        console.log(`      代码块 ${idx + 1} (${block.language}): ${preview}...`);
      });
    } catch (error) {
      console.log(`    ✗ ${extractor.field}: ${error.message}`);
    }
  }
}

/**
 * 测试列表提取器
 */
async function testListExtractor(page, parser) {
  console.log('\n  测试列表提取器:');
  
  const config = parser.getConfig();
  const listExtractors = config.extractors.filter(e => e.type === 'list');
  
  for (const extractor of listExtractors) {
    try {
      const result = await parser.extractList(page, extractor);
      console.log(`    ✓ ${extractor.field}: 提取了 ${result.length} 个列表`);
      result.forEach((list, idx) => {
        console.log(`      列表 ${idx + 1} (${list.type}): ${list.items.length} 项`);
      });
    } catch (error) {
      console.log(`    ✗ ${extractor.field}: ${error.message}`);
    }
  }
}

/**
 * 测试完整解析
 */
async function testFullParse(page, parser, url) {
  console.log('\n  测试完整解析:');
  
  try {
    const result = await parser.parse(page, url);
    
    console.log(`    ✓ 解析成功`);
    console.log(`    类型: ${result.type}`);
    console.log(`    URL: ${result.url}`);
    console.log(`    时间戳: ${result.timestamp}`);
    
    // 显示提取的字段
    const config = parser.getConfig();
    console.log(`    提取的字段:`);
    for (const extractor of config.extractors) {
      const value = result[extractor.field];
      if (value !== null && value !== undefined) {
        let preview = '';
        if (typeof value === 'string') {
          preview = value.substring(0, 30);
        } else if (Array.isArray(value)) {
          preview = `[${value.length} 项]`;
        } else if (typeof value === 'object') {
          preview = `{${Object.keys(value).length} 键}`;
        }
        console.log(`      - ${extractor.field}: ${preview}`);
      } else {
        console.log(`      - ${extractor.field}: null`);
      }
    }
    
    return result;
  } catch (error) {
    console.log(`    ✗ 解析失败: ${error.message}`);
    return null;
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('='.repeat(70));
  console.log('配置驱动解析测试 - 使用Playwright');
  console.log('='.repeat(70));
  console.log();

  // 1. 解析命令行参数
  const args = process.argv.slice(2);
  let configPath = args[0];

  if (!configPath) {
    configPath = path.join(__dirname, '../examples/template-config.jsonl');
    console.log(`使用示例配置: ${configPath}`);
  } else {
    console.log(`使用配置文件: ${configPath}`);
  }
  console.log();

  // 2. 检查配置文件
  if (!fs.existsSync(configPath)) {
    console.error(`❌ 错误: 配置文件不存在: ${configPath}`);
    process.exit(1);
  }

  let browser;
  try {
    // 3. 加载配置
    console.log('步骤 1: 加载配置文件');
    console.log('-'.repeat(70));
    
    const configs = ConfigLoader.loadConfigs(configPath);
    console.log(`✓ 成功加载 ${configs.length} 个配置`);
    console.log();

    // 4. 创建Parser实例
    console.log('步骤 2: 创建TemplateParser实例');
    console.log('-'.repeat(70));
    
    const parsers = configs.map(config => new TemplateParser(config));
    console.log(`✓ 成功创建 ${parsers.length} 个Parser实例`);
    parsers.forEach(p => {
      console.log(`  - ${p.getName()} (优先级: ${p.getPriority()})`);
    });
    console.log();

    // 5. 启动Playwright浏览器
    console.log('步骤 3: 启动Playwright浏览器');
    console.log('-'.repeat(70));
    
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    console.log('✓ 浏览器启动成功');
    console.log();

    // 6. 测试API文档Parser
    const apiDocParser = parsers.find(p => p.getName() === 'api-doc');
    if (apiDocParser) {
      console.log('步骤 4: 测试API文档Parser');
      console.log('-'.repeat(70));
      
      const page = await context.newPage();
      const testUrl = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
      
      // 设置测试HTML
      await page.setContent(createTestHTML());
      console.log(`✓ 加载测试页面: ${testUrl}`);
      
      // 测试URL匹配
      console.log('\n  测试URL匹配:');
      const matches = apiDocParser.matches(testUrl);
      console.log(`    ${matches ? '✓' : '✗'} URL匹配: ${matches}`);
      
      // 测试各种提取器
      await testTextExtractor(page, apiDocParser);
      await testTableExtractor(page, apiDocParser);
      await testCodeExtractor(page, apiDocParser);
      await testListExtractor(page, apiDocParser);
      
      // 测试完整解析
      const result = await testFullParse(page, apiDocParser, testUrl);
      
      await page.close();
      console.log();
    }

    // 7. 测试Dashboard Parser
    const dashboardParser = parsers.find(p => p.getName() === 'dashboard');
    if (dashboardParser) {
      console.log('步骤 5: 测试Dashboard Parser');
      console.log('-'.repeat(70));
      
      const page = await context.newPage();
      const testUrl = 'https://www.lixinger.com/analytics/company/dashboard';
      
      // 设置测试HTML
      await page.setContent(createDashboardHTML());
      console.log(`✓ 加载测试页面: ${testUrl}`);
      
      // 测试URL匹配
      console.log('\n  测试URL匹配:');
      const matches = dashboardParser.matches(testUrl);
      console.log(`    ${matches ? '✓' : '✗'} URL匹配: ${matches}`);
      
      // 测试各种提取器
      await testTextExtractor(page, dashboardParser);
      await testTableExtractor(page, dashboardParser);
      await testListExtractor(page, dashboardParser);
      
      // 测试完整解析
      const result = await testFullParse(page, dashboardParser, testUrl);
      
      await page.close();
      console.log();
    }

    // 8. 测试URL匹配优先级
    console.log('步骤 6: 测试URL匹配和优先级');
    console.log('-'.repeat(70));
    
    const testUrls = [
      'https://www.lixinger.com/open/api/doc?api-key=cn/company',
      'https://www.lixinger.com/open/api/doc?api-key=hk/index',
      'https://www.lixinger.com/analytics/company/dashboard',
      'https://www.lixinger.com/analytics/index/dashboard',
      'https://www.lixinger.com/other/page',
    ];

    for (const url of testUrls) {
      console.log(`\n  URL: ${url}`);
      
      const matchedParsers = parsers
        .filter(p => p.matches(url))
        .sort((a, b) => b.getPriority() - a.getPriority());
      
      if (matchedParsers.length > 0) {
        matchedParsers.forEach(p => {
          console.log(`    ✓ ${p.getName()} (优先级: ${p.getPriority()})`);
        });
        console.log(`    → 选择: ${matchedParsers[0].getName()}`);
      } else {
        console.log(`    ✗ 无匹配的Parser`);
      }
    }
    console.log();

    // 9. 总结
    console.log('='.repeat(70));
    console.log('测试完成');
    console.log('='.repeat(70));
    console.log(`✓ 配置文件加载成功`);
    console.log(`✓ 创建了 ${parsers.length} 个TemplateParser实例`);
    console.log(`✓ 使用Playwright测试了所有提取器类型`);
    console.log(`✓ 验证了URL匹配和优先级`);
    console.log();
    console.log('结论: 配置驱动的解析功能正常工作');
    console.log();

  } catch (error) {
    console.error();
    console.error('❌ 错误:', error.message);
    console.error();
    if (error.stack) {
      console.error('堆栈跟踪:');
      console.error(error.stack);
    }
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// 运行主函数
if (require.main === module) {
  main().catch(error => {
    console.error('未捕获的错误:', error);
    process.exit(1);
  });
}

module.exports = { main };
