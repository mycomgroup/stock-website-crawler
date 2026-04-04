#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import './load-env.js';
import { runNotebookTest } from './request/test-joinquant-notebook.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const SOURCE_DIR = path.resolve(REPO_ROOT, '聚宽有价值策略558');

const RUN_DIR = path.resolve(__dirname, 'data', 'jq558_notebook_run');
const STATE_FILE = path.resolve(RUN_DIR, 'state.json');
const LOG_JSONL = path.resolve(RUN_DIR, 'submissions.jsonl');
const LOG_MD = path.resolve(RUN_DIR, 'submissions.md');
const TEMPLATE_FILE = path.resolve(__dirname, 'templates', 'notebook_adapter_template.py');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (!current.startsWith('--')) continue;
    const key = current.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      args[key] = next;
      i++;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function walkStrategyFiles(dir) {
  const files = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkStrategyFiles(fullPath));
    } else if (entry.isFile() && (entry.name.endsWith('.txt') || entry.name.endsWith('.py'))) {
      files.push(fullPath);
    }
  }
  return files.sort((a, b) => a.localeCompare(b, 'zh-Hans-CN'));
}

async function runStrategyTask(workerId, file, options) {
  const strategyCode = fs.readFileSync(file, 'utf8');
  const template = fs.readFileSync(TEMPLATE_FILE, 'utf8');
  
  const base64Code = Buffer.from(strategyCode).toString('base64');
  
  const finalCode = template
    .replace('{STRATEGY_CODE_BASE64}', base64Code)
    .replace('{START_DATE}', options.startDate)
    .replace('{END_DATE}', options.endDate)
    .replace('{CAPITAL}', options.capital)
    .replace('{FREQUENCY}', options.frequency);

  console.log(`[Worker ${workerId}] 执行: ${path.relative(REPO_ROOT, file)}`);
  
  const notebookBaseName = `batch_worker_${workerId}`;
  
  try {
    const result = await runNotebookTest({
      cellSource: finalCode,
      notebookBaseName,
      notebookUrl: process.env.JOINQUANT_NOTEBOOK_URL,
      createNew: true, // 初始时创建，后续 test-joinquant-notebook 会尝试复用错误或现有的
      autoShutdown: false, // 保持 kernel 活跃以复用
      timeoutMs: options.timeoutMs || 300000,
      headed: options.headed,
      mode: 'all'
    });

    // 解析结果
    let summaryData = null;
    let errorData = null;

    for (const exec of result.executions) {
      const output = exec.textOutput || '';
      const match = output.match(/BACKTEST_RESULT_BLOCK_START\n([\s\S]*?)\nBACKTEST_RESULT_BLOCK_END/);
      if (match) {
        try {
          summaryData = JSON.parse(match[1]);
        } catch (e) {
          console.error(`解析结果 JSON 失败: ${e.message}`);
        }
      }
      
      const errMatch = output.match(/BACKTEST_EXCEPTION_START\n([\s\S]*?)\nBACKTEST_EXCEPTION_END/);
      if (errMatch) {
        errorData = errMatch[1];
      }
    }

    if (!summaryData && !errorData) {
      // 检查是否有系统级错误
      for (const exec of result.executions) {
        if (exec.outputs) {
          const errorOutput = exec.outputs.find(o => o.output_type === 'error');
          if (errorOutput) {
            errorData = `${errorOutput.ename}: ${errorOutput.evalue}`;
          }
        }
      }
    }

    return {
      status: summaryData ? 'success' : 'failed',
      summary: summaryData,
      error: errorData,
      notebookUrl: result.notebookUrl,
      resultFile: result.resultFile
    };
  } catch (error) {
    return {
      status: 'error',
      error: error.message
    };
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const startDate = args.start || '2025-04-03';
  const endDate = args.end || '2026-04-03';
  const capital = args.capital || '100000';
  const frequency = args.freq || 'day';
  const maxConcurrent = Number(args.maxConcurrent || 3);
  const limit = args.limit ? Number(args.limit) : null;
  const headed = args.headed === true;

  ensureDir(RUN_DIR);
  if (!fs.existsSync(LOG_JSONL)) fs.writeFileSync(LOG_JSONL, '');
  if (!fs.existsSync(LOG_MD)) {
    fs.writeFileSync(LOG_MD, '# JoinQuant Notebook 批量执行结果\n\n| # | 策略 | 状态 | 收益 | 回撤 | 夏普 | 错误 |\n|---|---|---|---|---|---|---|\n');
  }

  const allFiles = walkStrategyFiles(SOURCE_DIR);
  
  // 加载进度
  const submittedSet = new Set();
  if (fs.existsSync(LOG_JSONL)) {
    const lines = fs.readFileSync(LOG_JSONL, 'utf8').split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const item = JSON.parse(line);
        if (item.status === 'success') {
          submittedSet.add(item.file);
        }
      } catch (e) {}
    }
  }

  const pendingFiles = allFiles.filter(f => !submittedSet.has(f));
  const targetFiles = limit ? pendingFiles.slice(0, limit) : pendingFiles;

  console.log(`总文件: ${allFiles.length}`);
  console.log(`已完成: ${submittedSet.size}`);
  console.log(`本次待处理: ${targetFiles.length}`);
  console.log(`并发数: ${maxConcurrent}`);
  console.log('='.repeat(60));

  let currentIndex = 0;
  const workers = Array.from({ length: maxConcurrent }, (_, i) => i + 1);
  
  const processNext = async (workerId) => {
    while (currentIndex < targetFiles.length) {
      const index = currentIndex++;
      const file = targetFiles[index];
      const relativePath = path.relative(REPO_ROOT, file);
      
      console.log(`[${index + 1}/${targetFiles.length}] Worker ${workerId} 处理: ${relativePath}`);
      
      const result = await runStrategyTask(workerId, file, {
        startDate, endDate, capital, frequency, headed
      });

      const record = {
        file,
        relativePath,
        workerId,
        status: result.status,
        timestamp: new Date().toISOString(),
        summary: result.summary,
        error: result.error,
        notebookUrl: result.notebookUrl
      };

      // 写入日志
      fs.appendFileSync(LOG_JSONL, JSON.stringify(record) + '\n');
      
      const summary = result.summary || {};
      const row = [
        index + 1,
        relativePath,
        result.status,
        summary.total_returns !== undefined ? `${(summary.total_returns * 100).toFixed(2)}%` : '-',
        summary.max_drawdown !== undefined ? `${(summary.max_drawdown * 100).toFixed(2)}%` : '-',
        summary.sharpe !== undefined ? summary.sharpe.toFixed(2) : '-',
        result.error ? result.error.slice(0, 100).replace(/\n/g, ' ') : '-'
      ];
      fs.appendFileSync(LOG_MD, `| ${row.join(' | ')} |\n`);

      console.log(`  结果: ${result.status}${result.status === 'success' ? ` (收益: ${(summary.total_returns * 100).toFixed(2)}%)` : ''}`);
    }
  };

  // 启动并发
  await Promise.all(workers.map(workerId => processNext(workerId)));

  console.log('='.repeat(60));
  console.log('所有任务处理完成');
}

main().catch(console.error);
