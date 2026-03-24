#!/usr/bin/env node
// run-skill.js - CLI entry point for lixinger-screener skill
import '../load-env.js';

import { main } from './main.js';

// ── Argument parsing ──────────────────────────────────────────────────────────

const args = process.argv.slice(2);

function getArg(flag) {
  const i = args.indexOf(flag);
  return i !== -1 ? args[i + 1] : undefined;
}

const query = getArg('--query');
const inputFile = getArg('--input-file');
const catalogFile = getArg('--catalog-file');
const url = getArg('--url');
const profileDir = getArg('--profile-dir');
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
    [
      '用法：node run-skill.js [--query "<自然语言筛选条件>"] [--input-file <input.json>] [--catalog-file <condition-catalog.cn.json>] [--headless false] [--limit 100]',
      '',
      '说明：',
      '  --query       自然语言输入',
      '  --input-file  统一参数文件输入',
      '  --catalog-file 条件目录；当参数文件里使用 metric/selectors 时需要',
      '  --url         指定理杏仁筛选页 URL，可切到其他 screener 页面',
      '  --profile-dir 指定浏览器 profile 目录；默认使用 LIXINGER_BROWSER_PROFILE_DIR 或 stock-crawler/chrome_user_data',
      '',
      '示例：',
      '  node run-skill.js --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%"',
      '  node run-skill.js --input-file skills/lixinger-screener/data/simple-input-template.cn.json --headless false',
      '  node run-skill.js --url "https://www.lixinger.com/analytics/screener/company-fundamental/cn?screener-id=587c4d21d6e94ed9d447b29d" --profile-dir /path/to/chrome-profile'
    ].join('\n') + '\n'
  );
  process.exit(0);
}

if (!query && !inputFile) {
  process.stderr.write(
    '缺少输入。请提供 --query 或 --input-file\n'
  );
  process.exit(1);
}

// ── Run ───────────────────────────────────────────────────────────────────────

try {
  await main({
    query,
    inputFile,
    catalogPath: catalogFile,
    url,
    profileDir,
    cwd: process.cwd(),
    headless,
    limit
  });
} catch (err) {
  process.stderr.write(`错误：${err.message}\n`);
  process.exit(1);
}
