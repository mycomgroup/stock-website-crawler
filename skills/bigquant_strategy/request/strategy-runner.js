/**
 * BigQuant 策略运行器 — 对齐 joinquant_notebook 接口
 *
 * 用法（对齐 joinquant_notebook/request/test-joinquant-notebook.js）：
 *   runStrategyTest({ cellSource, strategy, startDate, endDate, capital, ... })
 *
 * 接口对齐说明：
 *   - strategy / cellSource  对应 JoinQuant 的 codeFilePath / cellSource
 *   - startDate / endDate    对应 JoinQuant 的 startTime / endTime
 *   - capital                对应 JoinQuant 的 baseCapital
 *   - taskName               对应 JoinQuant 的 algorithmId（策略名称）
 *   - 返回 { resultFile, taskId, runId, taskName, success, executions, textOutput, logs }
 *     对应 JoinQuant 的 { resultPath, backtestId, summary }
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

/**
 * 从策略文件/代码提取有业务含义的任务名称
 * 优先级：文件名 > 第一行注释 > 'strategy'
 * 加时间戳确保每次提交都是新 task，历史不覆盖
 */
function extractTaskName(strategyPath, cellSource) {
  let baseName = '';

  if (strategyPath) {
    baseName = path.basename(strategyPath, '.py');
  } else {
    // 从代码第一行注释提取
    const firstLine = (cellSource || '').split('\n').find(l => l.trim().startsWith('#'));
    if (firstLine) {
      baseName = firstLine.replace(/^#\s*/, '').replace(/[^\u4e00-\u9fa5a-zA-Z0-9_-]/g, '').slice(0, 20);
    }
  }

  if (!baseName) baseName = 'strategy';

  // 加日期时间戳，确保每次提交都是新 task，历史保留
  const now = new Date();
  const ts = now.toISOString().slice(0, 16).replace('T', '_').replace(':', '').replace('-', '').replace('-', '');
  return (baseName + '_' + ts).slice(0, 48);
}

/**
 * 从输出文本中解析回测指标
 * 支持常见的中英文格式
 */
function parseMetrics(text) {
  const metrics = {};
  const patterns = [
    // 中文格式
    { key: 'totalReturn',  re: /总收益[率:]?\s*([-\d.]+)\s*%/ },
    { key: 'annualReturn', re: /年化收益[率:]?\s*([-\d.]+)\s*%/ },
    { key: 'maxDrawdown',  re: /最大回撤[率:]?\s*([-\d.]+)\s*%/ },
    { key: 'sharpe',       re: /夏普[比率:]?\s*([-\d.]+)/ },
    { key: 'winRate',      re: /胜率[:]?\s*([-\d.]+)\s*%/ },
    { key: 'avgReturn',    re: /平均[单笔日]?收益[率:]?\s*([-\d.]+)\s*%/ },
    { key: 'tradeCount',   re: /(?:总)?交易[次数日]?[数:]?\s*(\d+)/ },
    { key: 'stockCount',   re: /选出?股票[数:]?\s*(\d+)/ },
    // 英文格式
    { key: 'totalReturn',  re: /total.?return[:\s]+([-\d.]+)\s*%/i },
    { key: 'annualReturn', re: /annual.?return[:\s]+([-\d.]+)\s*%/i },
    { key: 'maxDrawdown',  re: /max.?drawdown[:\s]+([-\d.]+)\s*%/i },
    { key: 'sharpe',       re: /sharpe[:\s]+([-\d.]+)/i },
  ];

  for (const { key, re } of patterns) {
    if (metrics[key] !== undefined) continue;
    const m = text.match(re);
    if (m) metrics[key] = parseFloat(m[1]);
  }

  return metrics;
}

function summarizeExecution(outputs, logs) {
  // outputs 来自 notebook cell outputs（可能为空）
  const outputText = outputs
    .map(o => {
      if (o.output_type === 'stream') return Array.isArray(o.text) ? o.text.join('') : String(o.text || '');
      if (o.output_type === 'error') return o.ename + ': ' + o.evalue;
      return '';
    })
    .filter(Boolean)
    .join('');

  // 从日志中提取 print 输出（非系统日志行）
  const logOutput = logs
    .filter(l => !l.match(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (?:任务运行|任务运行状态|\[info\s*\]|\[warn\s*\]|\[error\s*\])/))
    .join('\n');

  const textOutput = outputText || logOutput;
  const metrics = parseMetrics(textOutput);

  const hasError = outputs.some(o => o.output_type === 'error') ||
    logs.some(l => l.includes('[error') || l.includes('state=failed'));
  const status = hasError ? 'error' : 'ok';

  return { status, textOutput, metrics, outputs, logs };
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
    resourceSpecId,
    // 允许外部指定 taskName（不加时间戳）
    taskName: explicitTaskName
  } = options;

  const cellSource = normalizeCellSource(rawCellSource, strategyPath);
  const taskName = explicitTaskName || extractTaskName(strategyPath, cellSource);

  // 1. 确保 session
  const session = await ensureSession({ sessionFile });
  const client = new BigQuantClient(session, { studioId, resourceSpecId });

  console.log('[BigQuant] 策略: ' + taskName);
  console.log('[BigQuant] 回测: ' + startDate + ' ~ ' + endDate + ', 资金: ' + capital);

  // 2. 激活 Studio
  await client.activateStudio();
  await client.sleep(1000);

  // 3. 创建 Task（每次新建，历史保留）
  const notebookJson = client.buildNotebook(cellSource);
  const taskId = await client.createTask(taskName, notebookJson, {
    startDate, endDate, capital, benchmark, frequency
  });
  console.log('[BigQuant] Task ID: ' + taskId);

  // 4. 触发执行
  const runId = await client.triggerTask(taskId);
  console.log('[BigQuant] Run ID: ' + runId);

  // 5. 等待完成
  console.log('[BigQuant] 等待执行...');
  const completion = await client.waitForCompletion(taskId, timeoutMs);

  // 6. 读取结果
  const outputs = await client.getNotebookOutputs(taskId);
  const logs = await client.getLogs(runId);
  const execution = summarizeExecution(outputs, logs);

  // 7. 保存结果（丰富的结构化数据）
  const resultPayload = {
    capturedAt: new Date().toISOString(),
    platform: 'bigquant',
    taskId,
    runId,
    taskName,
    config: { startDate, endDate, capital, benchmark, frequency },
    success: completion.success,
    state: completion.state,
    // 解析出的指标（方便快速查看）
    metrics: execution.metrics,
    // 完整执行记录
    executions: [{
      taskId,
      runId,
      strategyFile: strategyPath || null,
      source: cellSource.slice(0, 500),
      status: execution.status,
      textOutput: execution.textOutput,
      metrics: execution.metrics,
      outputs: execution.outputs,
      logs: execution.logs
    }]
  };

  const resultFile = client.writeArtifact('bigquant-result-' + taskName.replace(/[^a-zA-Z0-9\u4e00-\u9fa5_-]/g, '_'), resultPayload);
  console.log('[BigQuant] 结果已保存: ' + resultFile);

  if (Object.keys(execution.metrics).length > 0) {
    console.log('[BigQuant] 解析指标: ' + JSON.stringify(execution.metrics));
  }

  return {
    resultFile,
    taskId,
    runId,
    taskName,
    success: completion.success,
    state: completion.state,
    metrics: execution.metrics,
    executions: resultPayload.executions,
    textOutput: execution.textOutput,
    outputs,
    logs
  };
}
