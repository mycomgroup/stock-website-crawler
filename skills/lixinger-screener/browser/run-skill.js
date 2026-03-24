#!/usr/bin/env node
// run-skill.js - CLI entry point for lixinger-screener skill
import '../load-env.js';

import { main, validateEnv } from './main.js';

// ── Argument parsing ──────────────────────────────────────────────────────────

const args = process.argv.slice(2);

function getArg(flag) {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] : undefined;
}

const query = getArg('--query');
const headlessRaw = getArg('--headless');
const limitRaw = getArg('--limit');
const wantsHelp = args.includes('--help') || args.includes('-h');

// --headless defaults to true; --headless false disables it
const headless = headlessRaw === 'false' ? false : true;

// --limit must be a positive integer
const limitParsed = limitRaw !== undefined ? parseInt(limitRaw, 10) : undefined;
const limit = limitParsed !== undefined && Number.isInteger(limitParsed) && limitParsed > 0
  ? limitParsed
  : undefined;

// ── Validation ────────────────────────────────────────────────────────────────

if (wantsHelp) {
  process.stdout.write(
    '用法：node run-skill.js --query "<自然语言筛选条件>" [--headless false] [--limit 100]\n'
  );
  process.exit(0);
}

if (!query) {
  process.stderr.write(
    '用法：node run-skill.js --query "<自然语言筛选条件>" [--headless false] [--limit 100]\n'
  );
  process.exit(1);
}

const envResult = validateEnv();
if (!envResult.valid) {
  process.stderr.write(`错误：缺少必要的环境变量：${envResult.missing.join('、')}\n`);
  process.stderr.write('请复制 .env.example 为 .env 并填写相应的值。\n');
  process.exit(1);
}

// ── Run ───────────────────────────────────────────────────────────────────────

try {
  await main({ query, headless, limit });
} catch (err) {
  process.stderr.write(`错误：${err.message}\n`);
  process.exit(1);
}
