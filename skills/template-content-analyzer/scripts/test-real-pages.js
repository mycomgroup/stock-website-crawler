#!/usr/bin/env node

/**
 * 测试脚本：使用真实网页测试配置驱动的解析
 * 
 * 任务 5.5.4: 测试配置驱动的解析（真实网页版本）
 * 
 * 功能：
 * - 使用真实的网页URL
 * - 测试配置驱动的解析
 * - 验证提取器在真实页面上的效果
 * 
 * 用法：
 *   node scripts/test-real-pages.js [config-file] [url]
 * 
 * 示例：
 *   node scripts/test-real-pages.js examples/template-config.jsonl https://www.lixinger.com/open/api/doc?api-key=cn/company
 */

const { chromium } = require('playwright');
const ConfigLoader = require('../lib/config-loader');
const TemplateParser = require('../lib/template-parser');
const path = require('path');
const fs = require('fs');

/**
 * 主函数
 */
async function main() {
  console.log('='.repeat(70));
  console.log('真实网页解析测试 - 使用Playwright');
  console.log('='.repeat(70));
  console.log();

  // 1. 解析命令行参数
  const args = process.argv.slice(2);
  let configPath = args[0];
  let testUrl = args[1];

  if (!configPath) {
    configPath = path.join(__dirname, '../examples/template-config.jsonl');
    console.log(`使用示例配置: ${configPath}`);
  } else {
    console.log(`使用配置文件: ${configPath}`);
  }

  if (!testUrl) {
    console.log('未指定测试URL，将使用示例URL');
    testUrl = 'https://www.example.com';
  } else {
    console.log(`测试URL: ${testUrl}`);
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

    // 5. 查找匹配的Parser
    console.log('步骤 3: 查找匹配的Parser');
    console.log('-'.repeat(70));
    
    const matchedParsers = parsers
      .filter(p => p.matches(testUrl))
      .sort((a, b) => b.getPriority() - a.getPriority());
    
    if (matchedParsers.length === 0) {
      console.log(`✗ 没有找到匹配URL的Parser: ${testUrl}`);
      console.log();
      console.log('提示: 请检查URL是否正确，或者配置文件中是否有对应的URL模式');
      process.exit(0);
    }
    
    const selectedParser = matchedParsers[0];
    console.log(`✓ 找到 ${matchedParsers.length} 个匹配的Parser`);
    matchedParsers.forEach(p => {
      console.log(`  - ${p.getName()} (优先级: ${p.getPriority()})`);
    });
    console.log(`✓ 选择Parser: ${selectedParser.getName()}`);
    console.log();

    // 6. 启动Playwright浏览器
    console.log('步骤 4: 启动Playwright浏览器');
    console.log('-'.repeat(70));
    
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    console.log('✓ 浏览器启动成功');
    console.log();

    // 7. 访问页面
    console.log('步骤 5: 访问页面');
    console.log('-'.repeat(70));
    console.log(`正在访问: ${testUrl}`);
    
    try {
      await page.goto(testUrl, { waitUntil: 'networkidle', timeout: 30000 });
      console.log('✓ 页面加载成功');
    } catch (error) {
      console.log(`✗ 页面加载失败: ${error.message}`);
      console.log();
      console.log('提示: 请检查URL是否可访问，或者网络连接是否正常');
      process.exit(1);
    }
    console.log();

    // 8. 执行解析
    console.log('步骤 6: 执行配置驱动的解析');
    console.log('-'.repeat(70));
    
    const result = await selectedParser.parse(page, testUrl);
    
    if (result.error) {
      console.log(`✗ 解析失败: ${result.error}`);
    } else {
      console.log('✓ 解析成功');
      console.log();
      
      // 显示解析结果
      console.log('解析结果:');
      console.log('-'.repeat(70));
      console.log(`类型: ${result.type}`);
      console.log(`URL: ${result.url}`);
      console.log(`时间戳: ${result.timestamp}`);
      console.log();
      
      // 显示提取的字段
      const config = selectedParser.getConfig();
      console.log('提取的字段:');
      for (const extractor of config.extractors) {
        const value = result[extractor.field];
        console.log();
        console.log(`${extractor.field} (${extractor.type}):`);
        
        if (value === null || value === undefined) {
          console.log('  (未提取到数据)');
        } else if (typeof value === 'string') {
          const lines = value.split('\n');
          if (lines.length > 5) {
            console.log('  ' + lines.slice(0, 5).join('\n  '));
            console.log(`  ... (共 ${lines.length} 行)`);
          } else {
            console.log('  ' + value);
          }
        } else if (Array.isArray(value)) {
          console.log(`  (共 ${value.length} 项)`);
          value.slice(0, 3).forEach((item, idx) => {
            if (typeof item === 'object') {
              console.log(`  [${idx}]: ${JSON.stringify(item).substring(0, 80)}...`);
            } else {
              console.log(`  [${idx}]: ${item}`);
            }
          });
          if (value.length > 3) {
            console.log(`  ... 还有 ${value.length - 3} 项`);
          }
        } else if (typeof value === 'object') {
          console.log(`  ${JSON.stringify(value, null, 2).split('\n').slice(0, 10).join('\n  ')}`);
          const jsonStr = JSON.stringify(value);
          if (jsonStr.length > 500) {
            console.log('  ...');
          }
        }
      }
    }
    console.log();

    // 9. 保存结果（可选）
    const outputDir = path.join(__dirname, '../output');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const outputFile = path.join(outputDir, `parse-result-${Date.now()}.json`);
    fs.writeFileSync(outputFile, JSON.stringify(result, null, 2), 'utf-8');
    console.log(`✓ 解析结果已保存到: ${outputFile}`);
    console.log();

    // 10. 总结
    console.log('='.repeat(70));
    console.log('测试完成');
    console.log('='.repeat(70));
    console.log(`✓ 使用配置: ${selectedParser.getName()}`);
    console.log(`✓ 解析URL: ${testUrl}`);
    console.log(`✓ 提取字段数: ${config.extractors.length}`);
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
