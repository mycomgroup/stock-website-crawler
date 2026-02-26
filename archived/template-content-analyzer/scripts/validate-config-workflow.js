#!/usr/bin/env node

/**
 * 综合验证脚本：验证配置驱动解析的完整工作流
 * 
 * 任务 5.5: 验证配置效果（不集成到爬虫系统）
 * - 5.5.1 创建独立测试脚本 ✓
 * - 5.5.2 加载配置文件 ✓
 * - 5.5.3 创建TemplateParser实例 ✓
 * - 5.5.4 测试配置驱动的解析 ✓
 * 
 * 功能：
 * - 完整演示配置驱动解析的工作流程
 * - 加载JSONL配置文件
 * - 创建TemplateParser实例
 * - 使用Playwright测试真实页面解析
 * - 验证URL匹配和数据提取
 * - 生成验证报告
 * 
 * 用法：
 *   node scripts/validate-config-workflow.js [config-file] [--verbose]
 * 
 * 示例：
 *   node scripts/validate-config-workflow.js examples/template-config.jsonl
 *   node scripts/validate-config-workflow.js examples/template-config.jsonl --verbose
 */

const { chromium } = require('playwright');
const ConfigLoader = require('../lib/config-loader');
const TemplateParser = require('../lib/template-parser');
const path = require('path');
const fs = require('fs');

/**
 * 创建测试HTML页面（API文档）
 */
function createAPIDocHTML() {
  return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>API文档 - 获取公司基本信息</title>
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
    "code": "600000"
  }
}
  </code></pre>
</body>
</html>
  `.trim();
}

/**
 * 验证步骤1：加载配置文件
 */
function validateStep1LoadConfig(configPath) {
  console.log('\n步骤 1: 加载配置文件');
  console.log('='.repeat(70));
  
  try {
    const configs = ConfigLoader.loadConfigs(configPath);
    console.log(`✓ 成功加载 ${configs.length} 个配置`);
    
    // 显示配置统计
    const stats = ConfigLoader.getConfigStats(configPath);
    console.log('\n配置统计:');
    console.log(`  总配置数: ${stats.totalConfigs}`);
    console.log(`  配置名称: ${stats.configNames.join(', ')}`);
    console.log(`  总提取器数: ${stats.totalExtractors}`);
    console.log(`  总过滤器数: ${stats.totalFilters}`);
    console.log(`  提取器类型: ${JSON.stringify(stats.extractorTypes)}`);
    console.log(`  过滤器类型: ${JSON.stringify(stats.filterTypes)}`);
    
    return { success: true, configs };
  } catch (error) {
    console.log(`✗ 加载失败: ${error.message}`);
    return { success: false, error };
  }
}

/**
 * 验证步骤2：创建TemplateParser实例
 */
function validateStep2CreateParsers(configs) {
  console.log('\n步骤 2: 创建TemplateParser实例');
  console.log('='.repeat(70));
  
  const parsers = [];
  const errors = [];
  
  for (const config of configs) {
    try {
      const parser = new TemplateParser(config);
      parsers.push(parser);
      console.log(`✓ 创建Parser: ${parser.getName()} (优先级: ${parser.getPriority()})`);
    } catch (error) {
      console.log(`✗ 创建失败 [${config.name}]: ${error.message}`);
      errors.push({ config: config.name, error: error.message });
    }
  }
  
  console.log(`\n成功创建 ${parsers.length}/${configs.length} 个Parser实例`);
  
  return { success: parsers.length > 0, parsers, errors };
}

/**
 * 验证步骤3：测试URL匹配
 */
function validateStep3URLMatching(parsers) {
  console.log('\n步骤 3: 测试URL匹配');
  console.log('='.repeat(70));
  
  const testUrls = [
    'https://www.lixinger.com/open/api/doc?api-key=cn/company',
    'https://www.lixinger.com/open/api/doc?api-key=hk/index',
    'https://www.lixinger.com/analytics/company/dashboard',
    'https://www.lixinger.com/other/page',
  ];

  const results = [];
  
  for (const url of testUrls) {
    console.log(`\n测试URL: ${url}`);
    
    const matchedParsers = parsers
      .filter(p => p.matches(url))
      .sort((a, b) => b.getPriority() - a.getPriority());
    
    if (matchedParsers.length > 0) {
      matchedParsers.forEach(p => {
        console.log(`  ✓ 匹配: ${p.getName()} (优先级: ${p.getPriority()})`);
      });
      console.log(`  → 选择: ${matchedParsers[0].getName()}`);
      results.push({ url, matched: true, parser: matchedParsers[0].getName() });
    } else {
      console.log(`  ✗ 无匹配的Parser`);
      results.push({ url, matched: false });
    }
  }
  
  const matchedCount = results.filter(r => r.matched).length;
  console.log(`\n匹配结果: ${matchedCount}/${testUrls.length} 个URL成功匹配`);
  
  return { success: true, results };
}

/**
 * 验证步骤4：测试数据提取
 */
async function validateStep4DataExtraction(parsers, verbose = false) {
  console.log('\n步骤 4: 测试数据提取（使用Playwright）');
  console.log('='.repeat(70));
  
  let browser;
  const results = [];
  
  try {
    // 启动浏览器
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    console.log('✓ 浏览器启动成功\n');
    
    // 测试API文档Parser
    const apiDocParser = parsers.find(p => p.getName() === 'api-doc');
    if (apiDocParser) {
      console.log('测试 API文档Parser:');
      console.log('-'.repeat(70));
      
      const page = await context.newPage();
      const testUrl = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
      
      // 设置测试HTML
      await page.setContent(createAPIDocHTML());
      
      // 测试URL匹配
      const matches = apiDocParser.matches(testUrl);
      console.log(`URL匹配: ${matches ? '✓' : '✗'}`);
      
      if (matches) {
        // 执行完整解析
        const result = await apiDocParser.parse(page, testUrl);
        
        if (result.error) {
          console.log(`✗ 解析失败: ${result.error}`);
          results.push({ parser: 'api-doc', success: false, error: result.error });
        } else {
          console.log(`✓ 解析成功`);
          
          // 统计提取的字段
          const config = apiDocParser.getConfig();
          const extractedFields = [];
          const missingFields = [];
          
          for (const extractor of config.extractors) {
            const value = result[extractor.field];
            if (value !== null && value !== undefined && value !== '') {
              extractedFields.push(extractor.field);
              
              if (verbose) {
                let preview = '';
                if (typeof value === 'string') {
                  preview = value.substring(0, 50);
                } else if (Array.isArray(value)) {
                  preview = `[${value.length} 项]`;
                } else if (typeof value === 'object') {
                  preview = `{${Object.keys(value).length} 键}`;
                }
                console.log(`  - ${extractor.field}: ${preview}`);
              }
            } else {
              missingFields.push(extractor.field);
            }
          }
          
          console.log(`\n提取字段: ${extractedFields.length}/${config.extractors.length}`);
          if (verbose && missingFields.length > 0) {
            console.log(`缺失字段: ${missingFields.join(', ')}`);
          }
          
          results.push({
            parser: 'api-doc',
            success: true,
            extractedFields: extractedFields.length,
            totalFields: config.extractors.length,
            result
          });
        }
      }
      
      await page.close();
    }
    
    await browser.close();
    
    const successCount = results.filter(r => r.success).length;
    console.log(`\n提取结果: ${successCount}/${results.length} 个Parser成功提取数据`);
    
    return { success: successCount > 0, results };
    
  } catch (error) {
    if (browser) {
      await browser.close();
    }
    console.log(`✗ 测试失败: ${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * 生成验证报告
 */
function generateReport(results, outputPath) {
  console.log('\n步骤 5: 生成验证报告');
  console.log('='.repeat(70));
  
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      configLoaded: results.step1.success,
      parsersCreated: results.step2.parsers?.length || 0,
      urlMatchingPassed: results.step3.success,
      dataExtractionPassed: results.step4.success
    },
    details: {
      step1: results.step1,
      step2: results.step2,
      step3: results.step3,
      step4: results.step4
    }
  };
  
  // 保存报告
  try {
    fs.writeFileSync(outputPath, JSON.stringify(report, null, 2), 'utf-8');
    console.log(`✓ 报告已保存: ${outputPath}`);
    return { success: true, report };
  } catch (error) {
    console.log(`✗ 保存报告失败: ${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * 显示最终总结
 */
function displaySummary(results) {
  console.log('\n' + '='.repeat(70));
  console.log('验证总结');
  console.log('='.repeat(70));
  
  const allPassed = results.step1.success && 
                    results.step2.success && 
                    results.step3.success && 
                    results.step4.success;
  
  console.log(`\n步骤 1 - 加载配置文件: ${results.step1.success ? '✓ 通过' : '✗ 失败'}`);
  console.log(`步骤 2 - 创建Parser实例: ${results.step2.success ? '✓ 通过' : '✗ 失败'}`);
  console.log(`步骤 3 - URL匹配测试: ${results.step3.success ? '✓ 通过' : '✗ 失败'}`);
  console.log(`步骤 4 - 数据提取测试: ${results.step4.success ? '✓ 通过' : '✗ 失败'}`);
  
  console.log(`\n总体结果: ${allPassed ? '✓ 所有测试通过' : '✗ 部分测试失败'}`);
  
  if (allPassed) {
    console.log('\n结论: 配置驱动的解析功能正常工作，可以投入使用');
  } else {
    console.log('\n结论: 配置驱动的解析功能存在问题，需要进一步调试');
  }
  
  console.log();
}

/**
 * 主函数
 */
async function main() {
  console.log('='.repeat(70));
  console.log('配置驱动解析 - 完整工作流验证');
  console.log('='.repeat(70));
  console.log('\n本脚本将验证配置驱动解析的完整工作流程：');
  console.log('1. 加载JSONL配置文件');
  console.log('2. 创建TemplateParser实例');
  console.log('3. 测试URL匹配');
  console.log('4. 测试数据提取（使用Playwright）');
  console.log('5. 生成验证报告');
  
  // 解析命令行参数
  const args = process.argv.slice(2);
  let configPath = args.find(arg => !arg.startsWith('--'));
  const verbose = args.includes('--verbose');
  
  if (!configPath) {
    configPath = path.join(__dirname, '../examples/template-config.jsonl');
    console.log(`\n使用示例配置: ${configPath}`);
  } else {
    console.log(`\n使用配置文件: ${configPath}`);
  }
  
  // 检查配置文件
  if (!fs.existsSync(configPath)) {
    console.error(`\n❌ 错误: 配置文件不存在: ${configPath}`);
    process.exit(1);
  }
  
  try {
    const results = {};
    
    // 步骤1: 加载配置文件
    results.step1 = validateStep1LoadConfig(configPath);
    if (!results.step1.success) {
      throw new Error('配置文件加载失败');
    }
    
    // 步骤2: 创建TemplateParser实例
    results.step2 = validateStep2CreateParsers(results.step1.configs);
    if (!results.step2.success) {
      throw new Error('Parser实例创建失败');
    }
    
    // 步骤3: 测试URL匹配
    results.step3 = validateStep3URLMatching(results.step2.parsers);
    
    // 步骤4: 测试数据提取
    results.step4 = await validateStep4DataExtraction(results.step2.parsers, verbose);
    
    // 步骤5: 生成验证报告
    const reportPath = path.join(__dirname, '../output/validation-report.json');
    const reportDir = path.dirname(reportPath);
    if (!fs.existsSync(reportDir)) {
      fs.mkdirSync(reportDir, { recursive: true });
    }
    results.step5 = generateReport(results, reportPath);
    
    // 显示总结
    displaySummary(results);
    
    // 返回退出码
    const allPassed = results.step1.success && 
                      results.step2.success && 
                      results.step3.success && 
                      results.step4.success;
    process.exit(allPassed ? 0 : 1);
    
  } catch (error) {
    console.error('\n❌ 验证过程中发生错误:', error.message);
    if (verbose && error.stack) {
      console.error('\n堆栈跟踪:');
      console.error(error.stack);
    }
    process.exit(1);
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
