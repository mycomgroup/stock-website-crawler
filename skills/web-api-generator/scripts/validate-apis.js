#!/usr/bin/env node
/**
 * 验证提取的 API 是否可以直接请求
 */

import { HARParser } from '../lib/har-parser.js';
import { RequestValidator } from '../lib/request-validator.js';
import fs from 'fs';
import path from 'path';

async function validateAPIs(harPath, options = {}) {
  const {
    maxConcurrent = 3,
    delay = 1000,
    outputReport = true
  } = options;

  console.log(`加载 HAR 文件: ${harPath}`);
  
  const parser = new HARParser(harPath);
  if (!parser.load()) {
    throw new Error('加载 HAR 文件失败');
  }

  const apis = parser.extractDataAPIs();
  console.log(`发现 ${apis.length} 个 API\n`);

  // 转换为验证格式
  const apiInfos = apis.map(entry => parser.extractRequestDetails(entry));

  // 验证
  const validator = new RequestValidator();
  const report = await validator.validateAll(apiInfos, {
    maxConcurrent,
    delay
  });

  // 显示结果
  console.log(`\n验证完成！`);
  console.log(`\n=== 概览 ===`);
  console.log(`总计: ${report.summary.total}`);
  console.log(`成功: ${report.summary.success}`);
  console.log(`失败: ${report.summary.failed}`);
  console.log(`可直连: ${report.summary.canBypass}`);
  console.log(`成功率: ${report.summary.successRate}`);
  console.log(`直连率: ${report.summary.bypassRate}`);

  if (Object.keys(report.failureReasons).length > 0) {
    console.log(`\n=== 失败原因 ===`);
    Object.entries(report.failureReasons).forEach(([reason, count]) => {
      console.log(`${reason}: ${count}`);
    });
  }

  // 保存报告
  if (outputReport) {
    const reportDir = path.dirname(harPath);
    const reportPath = path.join(reportDir, 'validation-report.json');
    const mdPath = path.join(reportDir, 'validation-report.md');
    
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    fs.writeFileSync(mdPath, validator.generateMarkdownReport(report));
    
    console.log(`\n报告已保存:`);
    console.log(`- JSON: ${reportPath}`);
    console.log(`- Markdown: ${mdPath}`);
  }

  return report;
}

// 从 JSON 文件验证
async function validateFromJSON(jsonPath, options = {}) {
  console.log(`加载 API 数据: ${jsonPath}`);
  
  const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const apis = data.apis || data;

  console.log(`发现 ${apis.length} 个 API\n`);

  const validator = new RequestValidator();
  const report = await validator.validateAll(apis, options);

  console.log(`\n验证完成！`);
  console.log(`成功率: ${report.summary.successRate}`);
  console.log(`直连率: ${report.summary.bypassRate}`);

  return report;
}

// CLI 使用
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log(`
使用方法:
  node validate-apis.js <har-file|json-file> [options]

示例:
  node validate-apis.js output/example.har
  node validate-apis.js output/apis/apis.json --concurrent 5

选项:
  --concurrent <n>  并发数 (默认: 3)
  --delay <ms>      请求间隔 (默认: 1000)
  --no-report       不保存报告
    `);
    process.exit(1);
  }
  
  const [inputFile] = args;
  
  const options = {
    maxConcurrent: 3,
    delay: 1000,
    outputReport: true
  };
  
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--concurrent' && args[i + 1]) {
      options.maxConcurrent = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--delay' && args[i + 1]) {
      options.delay = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--no-report') {
      options.outputReport = false;
    }
  }
  
  const isJSON = inputFile.endsWith('.json');
  const validateFn = isJSON ? validateFromJSON : validateAPIs;
  
  validateFn(inputFile, options).catch(error => {
    console.error('错误:', error);
    process.exit(1);
  });
}

export { validateAPIs, validateFromJSON };
