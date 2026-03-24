#!/usr/bin/env node
// run-skill.js - CLI entry point for lixinger-screener skill
//
// Usage:
//   node run-skill.js --query "PE小于20，ROE大于15%" [--headless false] [--limit 100]

import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load .env from the skill directory
const require = createRequire(import.meta.url);
const dotenv = require('dotenv');
dotenv.config({ path: join(__dirname, '.env') });

import { main, validateEnv } from './main.js';

// --- Arg parsing ---
const args = process.argv.slice(2);

const get = (flag) => {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] : undefined;
};

const has = (flag) => args.includes(flag);

// --query (required)
const query = get('--query');
if (!query) {
  console.error('错误：缺少必要参数 --query');
  console.error('');
  console.error('用法：');
  console.error('  node run-skill.js --query "PE小于20，ROE大于15%" [--headless false] [--limit 100]');
  process.exit(1);
}

// --headless (default true; --headless false sets it to false)
let headless = true;
if (has('--headless')) {
  const val = get('--headless');
  headless = val !== 'false';
}

// --limit (optional positive integer)
let limit;
const limitRaw = get('--limit');
if (limitRaw !== undefined) {
  const parsed = parseInt(limitRaw, 10);
  if (Number.isInteger(parsed) && parsed > 0) {
    limit = parsed;
  }
}

// --- Validate environment ---
const envResult = validateEnv();
if (!envResult.valid) {
  console.error(`错误：缺少必要的环境变量：${envResult.missing.join('、')}`);
  console.error('请在 .env 文件中配置以上变量，参考 .env.example');
  process.exit(1);
}

// --- Run ---
try {
  await main({ query, headless, limit });
} catch (err) {
  console.error(`错误：${err.message}`);
  process.exit(1);
}
