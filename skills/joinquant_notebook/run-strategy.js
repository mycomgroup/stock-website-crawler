#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { runNotebookTest } from './request/test-joinquant-notebook.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGY_ROOT = path.resolve(__dirname, '../joinquant_strategy');
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

  // 如果是绝对路径，直接使用
  if (path.isAbsolute(strategyPath)) {
    return strategyPath;
  }

  // 如果以 ../joinquant_strategy 开头，解析到策略目录
  if (strategyPath.startsWith('../joinquant_strategy/') || strategyPath.startsWith('joinquant_strategy/')) {
    const relativePath = strategyPath.replace(/^\.\.\/joinquant_strategy\/|^joinquant_strategy\//, '');
    return path.join(STRATEGY_ROOT, relativePath);
  }

  // 如果以 ../ 开头，相对于当前目录
  if (strategyPath.startsWith('../')) {
    return path.resolve(__dirname, strategyPath);
  }

  // 否则先在策略目录查找，然后在示例目录查找
  const strategyFullPath = path.join(STRATEGY_ROOT, strategyPath);
  if (fs.existsSync(strategyFullPath)) {
    return strategyFullPath;
  }

  const exampleFullPath = path.join(EXAMPLES_ROOT, strategyPath);
  if (fs.existsSync(exampleFullPath)) {
    return exampleFullPath;
  }

  // 直接作为相对路径
  return path.resolve(__dirname, strategyPath);
}

function readStrategyFile(filePath) {
  if (!filePath || !fs.existsSync(filePath)) {
    throw new Error(`策略文件不存在: ${filePath}`);
  }
  return fs.readFileSync(filePath, 'utf8');
}

function convertStrategyToNotebook(strategyCode) {
  // 简单的策略代码转换提示
  // 对于复杂的策略，需要手动转换或使用专门的转换器
  return `
# 策略代码（来自 joinquant_strategy）
# 注意：Notebook 中没有回测框架，需要手动模拟

${strategyCode}

# 如果策略包含 initialize/handle_data 函数，需要手动调用
# 示例：手动测试某一天的选股逻辑
`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  let cellSource = args['cell-source'];

  // 如果指定了策略文件，读取文件内容
  if (args.strategy) {
    const strategyPath = resolveStrategyPath(args.strategy);
    console.log(`读取策略文件: ${strategyPath}`);

    const strategyCode = readStrategyFile(strategyPath);

    if (args.convert) {
      cellSource = convertStrategyToNotebook(strategyCode);
    } else {
      cellSource = strategyCode;
    }
  }

  if (!cellSource) {
    console.error('请指定 --strategy 或 --cell-source');
    console.error('\n使用示例:');
    console.error('  node run-strategy.js --strategy weak_to_strong_simple.py');
    console.error('  node run-strategy.js --strategy ../joinquant_strategy/weak_to_strong_simple.py');
    console.error('  node run-strategy.js --cell-source "print(\'hello\')"');
    console.error('  node run-strategy.js --strategy examples/test_mini.py');
    process.exit(1);
  }

  const timeoutMs = Number(args['timeout-ms'] || 60000);

  console.log(`执行策略，超时设置: ${timeoutMs}ms`);
  console.log(`代码长度: ${cellSource.length} 字符`);

  const result = await runNotebookTest({
    sessionFile: args['session-file'],
    notebookUrl: args['notebook-url'] || process.env.JOINQUANT_NOTEBOOK_URL,
    mode: args.mode,
    cellSource,
    cellIndex: args['cell-index'],
    cellMarker: args['cell-marker'],
    timeoutMs,
    kernelName: args['kernel-name'] || 'python3',
    appendCell: args['append-cell'] !== 'false',
    headed: args.headed === true
  });

  // 输出执行结果
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
}

main().catch(error => {
  console.error('执行失败:', error.message);
  process.exit(1);
});