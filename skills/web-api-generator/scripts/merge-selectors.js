#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * 合并数据选择器到 API 配置
 */
function mergeSelectors() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help') {
    console.log(`
使用方法:
  node merge-selectors.js [options]

选项:
  --configs=<path>     API 配置文件路径
  --selectors=<path>   数据选择器文件路径
  --output=<path>      输出文件路径

示例:
  node merge-selectors.js \\
    --configs=../output/web-api-docs/api-configs.json \\
    --selectors=../output/data-selectors.json \\
    --output=../output/web-api-docs/api-configs-with-selectors.json
    `);
    process.exit(0);
  }

  // 解析参数
  const params = {};
  for (const arg of args) {
    if (arg.startsWith('--')) {
      const [key, value] = arg.substring(2).split('=');
      params[key] = value;
    }
  }

  const configsPath = params.configs || path.join(__dirname, '../output/web-api-docs/api-configs.json');
  const selectorsPath = params.selectors || path.join(__dirname, '../output/data-selectors.json');
  const outputPath = params.output || path.join(__dirname, '../output/web-api-docs/api-configs-with-selectors.json');

  console.log('合并数据选择器...\n');
  console.log(`配置文件: ${configsPath}`);
  console.log(`选择器文件: ${selectorsPath}`);
  console.log(`输出文件: ${outputPath}\n`);

  // 加载文件
  const configs = JSON.parse(fs.readFileSync(configsPath, 'utf-8'));
  const selectors = JSON.parse(fs.readFileSync(selectorsPath, 'utf-8'));

  // 创建选择器映射
  const selectorMap = {};
  for (const selector of selectors) {
    selectorMap[selector.api] = selector.dataSelectors;
  }

  // 合并
  let merged = 0;
  for (const config of configs) {
    if (selectorMap[config.api]) {
      config.dataSelectors = selectorMap[config.api];
      merged++;
    }
  }

  // 保存
  fs.writeFileSync(outputPath, JSON.stringify(configs, null, 2));

  console.log(`✓ 合并完成！`);
  console.log(`  - 总配置数: ${configs.length}`);
  console.log(`  - 已合并: ${merged}`);
  console.log(`  - 未合并: ${configs.length - merged}`);
  console.log(`\n结果已保存到: ${outputPath}`);
}

mergeSelectors();
