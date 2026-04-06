#!/usr/bin/env node
/**
 * 获取 error_exit 回测的错误信息，并并行分析58个"代码正常"文件的问题
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';
import { ensureRiceQuantSession } from '../../skills/ricequant_strategy/browser/session-manager.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MAPPING_FILE = path.join(__dirname, 'rq_strategy_mapping.json');
const RESULTS_FILE = path.join(__dirname, 'NEW_STRATEGY_RESULTS.md');

function loadMapping() {
  try { return JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8')); } catch { return {}; }
}

// Parse error_exit files from results md
function getErrorFiles() {
  const content = fs.readFileSync(RESULTS_FILE, 'utf8');
  const files = [];
  for (const line of content.split('\n')) {
    if (!line.startsWith('| rq_')) continue;
    const parts = line.split('|').map(part => part.trim()).filter(Boolean);
    if (parts.length < 8) continue;
    if (parts[6] === '❌ error_exit') {
      files.push(parts[0]);
    }
  }
  return files;
}

async function main() {
  const errorFiles = getErrorFiles();
  console.log(`共 ${errorFiles.length} 个 error_exit 文件\n`);

  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD,
  };
  const cookies = await ensureRiceQuantSession(credentials);
  const client = new RiceQuantClient({ cookies });
  const mapping = loadMapping();

  const results = {};

  // Fetch in batches of 10 concurrently
  const BATCH = 10;
  for (let i = 0; i < errorFiles.length; i += BATCH) {
    const batch = errorFiles.slice(i, i + BATCH);
    await Promise.all(batch.map(async (fname) => {
      const info = mapping[fname];
      if (!info?.backtestId) {
        results[fname] = { error: 'no backtestId in mapping' };
        return;
      }
      try {
        const data = await client.getBacktestResult(info.backtestId);
        let exception = data?.exception || data?.backtest?.exception || '';
        let logs = null;
        if (!exception) {
          logs = await client.getBacktestLogs(info.backtestId);
          if (typeof logs === 'string') {
            exception = logs.slice(0, 4000);
          } else if (Array.isArray(logs)) {
            exception = logs.map(item => item?.message || item?.content || JSON.stringify(item)).join('\n').slice(0, 4000);
          } else if (logs && typeof logs === 'object') {
            exception = JSON.stringify(logs).slice(0, 4000);
          }
        }
        // Extract error info from result
        const status = data?.status || data?.backtest?.status || 'unknown';
        const errMsg = data?.error_message || data?.backtest?.error_message ||
                       data?.message || data?.detail ||
                       JSON.stringify(data).slice(0, 200);
        results[fname] = {
          backtestId: info.backtestId,
          status,
          errMsg,
          exception
        };
      } catch (e) {
        results[fname] = { backtestId: info.backtestId, error: e.message.slice(0, 100) };
      }
    }));
    process.stdout.write(`  进度: ${Math.min(i + BATCH, errorFiles.length)}/${errorFiles.length}\r`);
  }

  console.log('\n\n=== 错误信息汇总 ===\n');
  
  // Group by error message
  const byError = {};
  for (const [fname, info] of Object.entries(results)) {
    const key = info.errMsg || info.error || 'unknown';
    if (!byError[key]) byError[key] = [];
    byError[key].push(fname);
  }

  for (const [errMsg, files] of Object.entries(byError).sort((a,b) => b[1].length - a[1].length)) {
    console.log(`\n[${files.length}个文件] ${errMsg.slice(0, 150)}`);
    for (const f of files.slice(0, 3)) console.log(`  ${f}`);
    if (files.length > 3) console.log(`  ... 还有 ${files.length - 3} 个`);
  }

  // Save full results
  fs.writeFileSync(path.join(__dirname, 'error_logs.json'), JSON.stringify(results, null, 2));
  fs.writeFileSync(path.join(__dirname, 'error_logs_current.json'), JSON.stringify(results, null, 2));
  console.log('\n完整结果已保存到 error_logs.json / error_logs_current.json');
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
