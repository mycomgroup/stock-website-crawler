/**
 * BigQuant 策略运行器 — 对齐 joinquant_notebook 接口
 *
 * 用法（对齐 joinquant_notebook/request/test-joinquant-notebook.js）：
 *   runStrategyTest({ cellSource, strategy, startDate, endDate, capital, ... })
 */

import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { ensureSession } from './bigquant-auth.js';
import { BigQuantClient } from './bigquant-client.js';

function normalizeCellSource(cellSource, strategyPath) {
  if (cellSource) return String(cellSource);
  if (strategyPath && fs.existsSync(strategyPath)) {
    return fs.readFileSync(strategyPath, 'utf8');
  }
  return 'print("hello from bigquant")';
}

function extractTaskName(strategyPath, cellSource) {
  if (strategyPath) {
    return path.basename(strategyPath, '.py').slice(0, 32);
  }
  // 从代码第一行注释提取
  const firstLine = (cellSource || '').split('\n').find(l => l.trim().startsWith('#'));
  if (firstLine) {
    return firstLine.replace(/^#\s*/, '').replace(/[^\u4e00-\u9fa5a-zA-Z0-9_]/g, '').slice(0, 20) || 'strategy';
  }
  return 'strategy';
}

function summarizeExecution(outputs, logs) {
  // outputs 来自 notebook cell outputs（可能为空）
  const outputText = outputs
    .map(o => {
      if (o.output_type === 'stream') return Array.isArray(o.text) ? o.text.join('') : String(o.text || '');
      if (o.output_type === 'error') return `${o.ename}: ${o.evalue}`;
      return '';
    })
    .filter(Boolean)
    .join('');

  // 从日志中提取 print 输出（非系统日志行）
  const logOutput = logs
    .filter(l => !l.match(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (?:任务运行|任务运行状态|\[info\s*\]|\[warn\s*\]|\[error\s*\])/))
    .join('\n');

  const textOutput = outputText || logOutput;
  const hasError = outputs.some(o => o.output_type === 'error') ||
    logs.some(l => l.includes('[error') || l.includes('state=failed'));
  const status = hasError ? 'error' : 'ok';

  return { status, textOutput, outputs, logs };
}

export async function runStrategyTest(options = {}) {
  const {
    cellSource: rawCellSource,
    strategy: strategyPath,
    startDate = '2023-01-01',
    endDate = '2023-12-31',
    capital = 100000,
    benchmark = '000300.XSHG',
    frequency = 'day',
    timeoutMs = 300000,
    sessionFile,
    studioId,
    resourceSpecId
  } = options;

  const cellSource = normalizeCellSource(rawCellSource, strategyPath);
  const taskName = extractTaskName(strategyPath, cellSource);

  // 1. 确保 session
  const session = await ensureSession({ sessionFile });
  const client = new BigQuantClient(session, { studioId, resourceSpecId });

  console.log(`[BigQuant] 策略: ${taskName}`);
  console.log(`[BigQuant] 回测: ${startDate} ~ ${endDate}, 资金: ${capital}`);

  // 2. 激活 Studio
  await client.activateStudio();
  await client.sleep(1000);

  // 3. 创建 Task
  const notebookJson = client.buildNotebook(cellSource);
  const taskId = await client.createTask(taskName, notebookJson, {
    startDate, endDate, capital, benchmark, frequency
  });
  console.log(`[BigQuant] Task ID: ${taskId}`);

  // 4. 触发执行
  const runId = await client.triggerTask(taskId);
  console.log(`[BigQuant] Run ID: ${runId}`);

  // 5. 等待完成
  console.log('[BigQuant] 等待执行...');
  const completion = await client.waitForCompletion(taskId, timeoutMs);

  // 6. 读取结果
  const outputs = await client.getNotebookOutputs(taskId);
  const logs = await client.getLogs(runId);
  const execution = summarizeExecution(outputs, logs);

  // 7. 保存结果
  const resultPayload = {
    capturedAt: new Date().toISOString(),
    taskId,
    runId,
    taskName,
    startDate,
    endDate,
    capital,
    success: completion.success,
    state: completion.state,
    executions: [{
      taskId,
      runId,
      source: cellSource.slice(0, 200),
      ...execution
    }]
  };

  const resultFile = client.writeArtifact(`bigquant-result-${taskName}`, resultPayload);
  console.log(`[BigQuant] 结果已保存: ${resultFile}`);

  return {
    resultFile,
    taskId,
    runId,
    taskName,
    success: completion.success,
    state: completion.state,
    executions: resultPayload.executions,
    textOutput: execution.textOutput,
    outputs,
    logs
  };
}
