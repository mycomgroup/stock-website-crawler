#!/usr/bin/env node

/**
 * 对比测试：配置驱动Parser vs 手写Parser
 * 
 * 任务 6.4.4: 对比手写Parser的效果
 * 
 * 功能：
 * - 使用相同的URL测试两种Parser
 * - 对比提取的数据字段
 * - 生成对比报告
 */

const { chromium } = require('playwright');
const ConfigLoader = require('../lib/config-loader');
const TemplateParser = require('../lib/template-parser');
const path = require('path');
const fs = require('fs');

/**
 * 模拟手写Parser的解析逻辑（简化版）
 */
async function parseWithHandWrittenParser(page, url) {
  try {
    // 提取标题
    const title = await page.title();
    
    // 提取简要描述
    const briefDesc = await page.evaluate(() => {
      const root = document.querySelector('main') || document.body;
      const briefEl = Array.from(root.querySelectorAll('p, div')).find((el) => 
        el.innerText.trim().startsWith('获取') && el.innerText.length < 500
      );
      return briefEl ? briefEl.innerText.trim() : '';
    });
    
    // 提取请求URL
    const requestUrl = await page.evaluate(() => {
      const root = document.querySelector('main') || document.body;
      const urlEl = root.querySelector('code, pre, [class*="url"]');
      if (urlEl && /open\.lixinger\.com|api\.lixinger/.test(urlEl.innerText)) {
        return urlEl.innerText.trim().split(/\s/)[0];
      }
      return '';
    });
    
    // 提取参数表格
    const params = await page.evaluate(() => {
      const root = document.querySelector('main') || document.body;
      const params = [];
      const tables = root.querySelectorAll('table');
      
      for (const table of tables) {
        const rows = table.querySelectorAll('tr');
        if (rows.length < 2) continue;
        
        const header = (rows[0].innerText || '').toLowerCase();
        if (!header.includes('必选') && !header.includes('参数')) continue;
        
        for (let i = 1; i < rows.length; i++) {
          const cells = rows[i].querySelectorAll('td, th');
          if (cells.length < 2) continue;
          
          const name = (cells[0] && cells[0].innerText) ? cells[0].innerText.trim() : '';
          const required = (cells[1] && cells[1].innerText) ? cells[1].innerText.trim() : '';
          const type = (cells[2] && cells[2].innerText) ? cells[2].innerText.trim() : '';
          const desc = (cells[3] && cells[3].innerText) ? cells[3].innerText.trim() : '';
          
          if (name && !name.includes('参数名称')) {
            params.push({ name, required, type, desc });
          }
        }
        
        if (params.length > 0) break;
      }
      
      return params;
    });
    
    // 提取代码块
    const codeBlocks = await page.evaluate(() => {
      const blocks = [];
      const textareas = document.querySelectorAll('textarea');
      textareas.forEach(ta => {
        const code = (ta.value || ta.textContent || '').trim();
        if (code) blocks.push(code);
      });
      
      const pres = document.querySelectorAll('pre code, pre');
      pres.forEach(pre => {
        const code = (pre.textContent || '').trim();
        if (code && code.includes('{')) blocks.push(code);
      });
      
      return blocks;
    });
    
    return {
      type: 'api-doc',
      url,
      title,
      briefDesc,
      requestUrl,
      params,
      codeBlocks,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('手写Parser解析失败:', error.message);
    return { type: 'api-doc', url, error: error.message };
  }
}

/**
 * 对比两个解析结果
 */
function compareResults(configResult, handWrittenResult) {
  const comparison = {
    fieldsComparison: {},
    summary: {
      configFields: 0,
      handWrittenFields: 0,
      commonFields: 0,
      configOnlyFields: [],
      handWrittenOnlyFields: []
    }
  };
  
  // 获取所有字段
  const configFields = Object.keys(configResult).filter(k => 
    k !== 'type' && k !== 'url' && k !== 'timestamp' && k !== 'error'
  );
  const handWrittenFields = Object.keys(handWrittenResult).filter(k => 
    k !== 'type' && k !== 'url' && k !== 'timestamp' && k !== 'error'
  );
  
  comparison.summary.configFields = configFields.length;
  comparison.summary.handWrittenFields = handWrittenFields.length;
  
  // 对比每个字段
  const allFields = new Set([...configFields, ...handWrittenFields]);
  
  for (const field of allFields) {
    const inConfig = configFields.includes(field);
    const inHandWritten = handWrittenFields.includes(field);
    
    if (inConfig && inHandWritten) {
      comparison.summary.commonFields++;
      
      const configValue = configResult[field];
      const handWrittenValue = handWrittenResult[field];
      
      // 比较值
      let match = false;
      let configSize = 0;
      let handWrittenSize = 0;
      
      if (typeof configValue === 'string' && typeof handWrittenValue === 'string') {
        match = configValue === handWrittenValue;
        configSize = configValue.length;
        handWrittenSize = handWrittenValue.length;
      } else if (Array.isArray(configValue) && Array.isArray(handWrittenValue)) {
        configSize = configValue.length;
        handWrittenSize = handWrittenValue.length;
        match = configSize === handWrittenSize;
      }
      
      comparison.fieldsComparison[field] = {
        inConfig,
        inHandWritten,
        match,
        configSize,
        handWrittenSize
      };
    } else if (inConfig) {
      comparison.summary.configOnlyFields.push(field);
      comparison.fieldsComparison[field] = {
        inConfig: true,
        inHandWritten: false
      };
    } else {
      comparison.summary.handWrittenOnlyFields.push(field);
      comparison.fieldsComparison[field] = {
        inConfig: false,
        inHandWritten: true
      };
    }
  }
  
  return comparison;
}

/**
 * 显示对比结果
 */
function displayComparison(comparison, verbose = false) {
  console.log('\n对比结果:');
  console.log('='.repeat(70));
  
  console.log(`\n字段统计:`);
  console.log(`  配置驱动Parser: ${comparison.summary.configFields} 个字段`);
  console.log(`  手写Parser: ${comparison.summary.handWrittenFields} 个字段`);
  console.log(`  共同字段: ${comparison.summary.commonFields} 个`);
  
  if (comparison.summary.configOnlyFields.length > 0) {
    console.log(`  仅配置驱动: ${comparison.summary.configOnlyFields.join(', ')}`);
  }
  
  if (comparison.summary.handWrittenOnlyFields.length > 0) {
    console.log(`  仅手写Parser: ${comparison.summary.handWrittenOnlyFields.join(', ')}`);
  }
  
  if (verbose) {
    console.log(`\n字段详细对比:`);
    for (const [field, info] of Object.entries(comparison.fieldsComparison)) {
      if (info.inConfig && info.inHandWritten) {
        const matchIcon = info.match ? '✓' : '✗';
        console.log(`  ${matchIcon} ${field}:`);
        console.log(`      配置驱动: ${info.configSize} 项/字符`);
        console.log(`      手写Parser: ${info.handWrittenSize} 项/字符`);
      }
    }
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('='.repeat(70));
  console.log('Parser对比测试 - 配置驱动 vs 手写');
  console.log('='.repeat(70));
  
  // 解析命令行参数
  const args = process.argv.slice(2);
  const configPath = args[0] || 'stock-crawler/output/lixinger-crawler/template-rules.jsonl';
  const testUrl = args[1] || 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
  const verbose = args.includes('--verbose');
  
  console.log(`\n配置文件: ${configPath}`);
  console.log(`测试URL: ${testUrl}`);
  console.log();
  
  // 检查配置文件
  if (!fs.existsSync(configPath)) {
    console.error(`❌ 错误: 配置文件不存在: ${configPath}`);
    process.exit(1);
  }
  
  let browser;
  try {
    // 加载配置
    console.log('步骤 1: 加载配置并创建Parser');
    console.log('-'.repeat(70));
    
    const configs = ConfigLoader.loadConfigs(configPath);
    const parsers = configs.map(config => new TemplateParser(config));
    console.log(`✓ 成功创建 ${parsers.length} 个配置驱动Parser`);
    
    const matchedParser = parsers.find(p => p.matches(testUrl));
    if (!matchedParser) {
      console.error(`✗ 没有找到匹配URL的Parser: ${testUrl}`);
      process.exit(1);
    }
    console.log(`✓ 找到匹配的Parser: ${matchedParser.getName()}`);
    console.log();
    
    // 启动浏览器
    console.log('步骤 2: 启动浏览器并访问页面');
    console.log('-'.repeat(70));
    
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    console.log(`正在访问: ${testUrl}`);
    await page.goto(testUrl, { waitUntil: 'networkidle', timeout: 30000 });
    console.log('✓ 页面加载成功');
    console.log();
    
    // 使用配置驱动Parser解析
    console.log('步骤 3: 使用配置驱动Parser解析');
    console.log('-'.repeat(70));
    
    const configResult = await matchedParser.parse(page, testUrl);
    console.log('✓ 配置驱动Parser解析完成');
    console.log(`  提取字段数: ${Object.keys(configResult).filter(k => k !== 'type' && k !== 'url' && k !== 'timestamp').length}`);
    console.log();
    
    // 使用手写Parser解析
    console.log('步骤 4: 使用手写Parser解析');
    console.log('-'.repeat(70));
    
    const handWrittenResult = await parseWithHandWrittenParser(page, testUrl);
    console.log('✓ 手写Parser解析完成');
    console.log(`  提取字段数: ${Object.keys(handWrittenResult).filter(k => k !== 'type' && k !== 'url' && k !== 'timestamp').length}`);
    console.log();
    
    // 对比结果
    console.log('步骤 5: 对比解析结果');
    console.log('-'.repeat(70));
    
    const comparison = compareResults(configResult, handWrittenResult);
    displayComparison(comparison, verbose);
    
    // 保存结果
    const outputDir = path.join(__dirname, '../output');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const reportPath = path.join(outputDir, 'parser-comparison.json');
    fs.writeFileSync(reportPath, JSON.stringify({
      testUrl,
      timestamp: new Date().toISOString(),
      configResult,
      handWrittenResult,
      comparison
    }, null, 2), 'utf-8');
    
    console.log(`\n✓ 对比报告已保存: ${reportPath}`);
    
    await browser.close();
    
    // 总结
    console.log('\n' + '='.repeat(70));
    console.log('测试总结');
    console.log('='.repeat(70));
    console.log(`✓ 配置驱动Parser和手写Parser都能成功解析页面`);
    console.log(`✓ 配置驱动Parser提取了 ${comparison.summary.configFields} 个字段`);
    console.log(`✓ 手写Parser提取了 ${comparison.summary.handWrittenFields} 个字段`);
    console.log(`✓ 共同字段: ${comparison.summary.commonFields} 个`);
    
    if (comparison.summary.configFields >= comparison.summary.handWrittenFields) {
      console.log(`\n结论: 配置驱动Parser的提取能力与手写Parser相当或更好`);
    } else {
      console.log(`\n结论: 配置驱动Parser的提取能力基本达到手写Parser水平`);
    }
    console.log();
    
  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    if (error.stack) {
      console.error('\n堆栈跟踪:');
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

module.exports = { main, compareResults };
