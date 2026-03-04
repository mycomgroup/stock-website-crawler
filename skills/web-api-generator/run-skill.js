#!/usr/bin/env node

/**
 * Web API Generator Skill - 快速运行脚本
 * 
 * 使用方法:
 *   node run-skill.js generate-docs
 *   node run-skill.js list
 *   node run-skill.js search 公司详情
 *   node run-skill.js call detail-sh --param4=600519 --param5=600519
 */

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);

if (args.length === 0) {
  console.log(`
Web API Generator Skill - 快速运行

使用方法:
  node run-skill.js <command> [options]

命令:
  generate-docs    生成 API 文档
  list            列出所有 API
  search <关键词>  搜索 API
  call <api> ...  调用 API

示例:
  node run-skill.js generate-docs
  node run-skill.js list
  node run-skill.js search 公司详情
  node run-skill.js call detail-sh --param4=600519 --param5=600519
  `);
  process.exit(0);
}

// 运行 main.js
const mainPath = path.join(__dirname, 'main.js');
const child = spawn('node', [mainPath, ...args], {
  stdio: 'inherit',
  cwd: __dirname
});

child.on('exit', (code) => {
  process.exit(code);
});
