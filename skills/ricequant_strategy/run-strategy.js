#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { runNotebookTest } from './request/test-ricequant-notebook.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const EXAMPLES_ROOT = path.resolve(__dirname, 'examples');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (!current.startsWith('--')) continue;
    const key = current.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i++;
  }
  return args;
}

function resolveStrategyPath(strategyPath) {
  if (!strategyPath) return null;

  if (path.isAbsolute(strategyPath)) {
    return strategyPath;
  }

  const exampleFullPath = path.join(EXAMPLES_ROOT, strategyPath);
  if (fs.existsSync(exampleFullPath)) {
    return exampleFullPath;
  }

  return path.resolve(__dirname, strategyPath);
}

function readStrategyFile(filePath) {
  if (!filePath || !fs.existsSync(filePath)) {
    throw new Error(`策略文件不存在: ${filePath}`);
  }
  return fs.readFileSync(filePath, 'utf8');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  let cellSource = args['cell-source'];

  if (args.strategy) {
    const strategyPath = resolveStrategyPath(args.strategy);
    console.log(`读取策略文件: ${strategyPath}`);

    const strategyCode = readStrategyFile(strategyPath);
    cellSource = strategyCode;
  }

  if (!cellSource) {
    console.error('请指定 --strategy 或 --cell-source');
    console.error('\n使用示例:');
    console.error('  node run-strategy.js --strategy double-ma-strategy.py');
    console.error('  node run-strategy.js --strategy examples/double-ma-strategy.py');
    console.error('  node run-strategy.js --cell-source "print(\'hello\')"');
    console.error('  node run-strategy.js --strategy examples/simple_backtest.py');
    console.error('\n新建独立notebook并运行:');
    console.error('  node run-strategy.js --strategy your_strategy.py --create-new');
    console.error('  node run-strategy.js --strategy your_strategy.py --create-new --cleanup');
    process.exit(1);
  }

  const timeoutMs = Number(args['timeout-ms'] || 60000);
  const createNew = args['create-new'] === true;
  const cleanup = args.cleanup === true;
  const autoShutdown = args['no-shutdown'] ? false : (args['auto-shutdown'] !== 'false');

  console.log(`执行策略，超时设置: ${timeoutMs}ms`);
  console.log(`代码长度: ${cellSource.length} 字符`);
  if (createNew) {
    console.log(`创建新 notebook: 是`);
    console.log(`自动清理: ${cleanup ? '是' : '否'}`);
  }
  console.log(`自动关闭 session: ${autoShutdown}`);

  const result = await runNotebookTest({
    sessionFile: args['session-file'],
    notebookUrl: args['notebook-url'] || process.env.RICEQUANT_NOTEBOOK_URL,
    mode: args.mode,
    cellSource,
    cellIndex: args['cell-index'],
    cellMarker: args['cell-marker'],
    timeoutMs,
    kernelName: args['kernel-name'] || 'python3',
    appendCell: args['append-cell'] !== 'false',
    createNew,
    cleanup,
    notebookBaseName: args['notebook-base-name'],
    autoShutdown
  });

  console.log('\n执行结果:');
  console.log(`  Notebook URL: ${result.notebookUrl}`);
  console.log(`  执行模式: ${result.mode}`);
  console.log(`  执行 cells: ${result.targetCellIndices.join(', ')}`);

  if (result.executions && result.executions.length > 0) {
    console.log('\n输出:');
    for (const exec of result.executions) {
      if (exec.textOutput) {
        console.log(exec.textOutput);
      }
      if (exec.outputs && exec.outputs.length > 0) {
        for (const output of exec.outputs) {
          if (output.output_type === 'error') {
            console.error(`错误: ${output.ename}: ${output.evalue}`);
          }
        }
      }
    }
  }

  console.log(`\n结果文件: ${result.resultFile}`);
  console.log(`Notebook 快照: ${result.notebookSnapshotPath}`);

  if (result.shutdownResult) {
    if (result.shutdownResult.success) {
      console.log(`Session 已关闭: ${result.shutdownResult.sessionId}`);
    } else {
      console.warn(`Session 关闭失败: ${result.shutdownResult.error || 'unknown error'}`);
    }
  }
}

main().catch(error => {
  console.error('执行失败:', error.message);
  process.exit(1);
});