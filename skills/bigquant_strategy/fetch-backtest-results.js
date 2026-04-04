#!/usr/bin/env node
/**
 * 查询 BigQuant 策略回测结果
 *
 * BigQuant 是 Task-based 模型，没有"策略ID"概念，每次提交创建新 Task。
 * 查询方式：按 task name 前缀过滤，或直接用 taskId 查。
 *
 * 用法：
 *   # 列出所有 Task（最近 50 条）
 *   node fetch-backtest-results.js --list
 *
 *   # 按名称前缀过滤（对应策略文件名）
 *   node fetch-backtest-results.js --name-prefix rfscore7_pb10 --list
 *
 *   # 查最近一条（可配合 --name-prefix 过滤）
 *   node fetch-backtest-results.js --latest
 *   node fetch-backtest-results.js --name-prefix rfscore7_pb10 --latest
 *
 *   # 指定 taskId 查完整结果
 *   node fetch-backtest-results.js --task-id <id>
 *
 *   # 保存结果到文件
 *   node fetch-backtest-results.js --name-prefix rfscore7 --latest --save
 */
import './load-env.js';
import { ensureSession } from './request/bigquant-auth.js';
import { BigQuantClient } from './request/bigquant-client.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { args[key] = next; i++; }
      else args[key] = true;
    }
  }
  return args;
}

function filterByPrefix(tasks, prefix) {
  if (!prefix) return tasks;
  const p = prefix.toLowerCase();
  return tasks.filter(t => (t.name || '').toLowerCase().includes(p));
}

function printList(tasks) {
  console.log(`\n共 ${tasks.length} 条 Task 记录：\n`);
  tasks.forEach((t, i) => {
    const state = t.last_run?.state || t.state || 'unknown';
    const created = t.created_at || '';
    console.log(`[${i + 1}] ID: ${t.id}`);
    console.log(`    名称: ${t.name}`);
    console.log(`    状态: ${state}  创建: ${created}`);
    console.log('');
  });
}

async function getTaskOutputText(client, taskId) {
  try {
    const outputs = await client.getNotebookOutputs(taskId);
    return outputs
      .map(o => {
        if (o.output_type === 'stream') return Array.isArray(o.text) ? o.text.join('') : String(o.text || '');
        if (o.output_type === 'error') return `${o.ename}: ${o.evalue}`;
        if (o.output_type === 'execute_result') {
          return o.data?.['text/plain'] ? String(o.data['text/plain']) : '';
        }
        return '';
      })
      .filter(Boolean)
      .join('');
  } catch {
    return '';
  }
}

async function printTaskResult(client, task) {
  const taskId = task.id;
  const state = task.last_run?.state || task.state || 'unknown';
  const runId = task.last_run?.id;

  console.log(`\nTask ID: ${taskId}`);
  console.log(`名称: ${task.name}`);
  console.log(`状态: ${state}`);
  console.log(`创建: ${task.created_at || 'N/A'}`);

  const text = await getTaskOutputText(client, taskId);
  if (text) {
    console.log('\n--- 输出内容 ---');
    console.log(text.slice(0, 2000));
    if (text.length > 2000) console.log('... (截断，完整内容请用 --save)');
  }

  // 尝试拉日志
  if (runId) {
    try {
      const logs = await client.getLogs(runId, 50);
      const userLogs = logs.filter(l => !l.match(/^\d{4}-\d{2}-\d{2}.*(?:任务运行|state=)/));
      if (userLogs.length > 0) {
        console.log('\n--- 日志 ---');
        console.log(userLogs.slice(0, 20).join('\n'));
      }
    } catch { /* 日志可选 */ }
  }

  return { taskId, state, text };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const taskId     = args['task-id'];
  const namePrefix = args['name-prefix'];
  const { list, latest, save } = args;

  if (!taskId && !list && !latest) {
    console.error('Error: 需要 --list、--latest 或 --task-id');
    console.log('\n示例:');
    console.log('  node fetch-backtest-results.js --list');
    console.log('  node fetch-backtest-results.js --name-prefix rfscore7 --list');
    console.log('  node fetch-backtest-results.js --name-prefix rfscore7 --latest');
    console.log('  node fetch-backtest-results.js --task-id <id>');
    process.exit(1);
  }

  const session = await ensureSession({});
  const client = new BigQuantClient(session);

  let data;

  if (taskId) {
    // 直接查指定 Task
    const task = await client.getTask(taskId);
    const t = task.data || task;
    data = await printTaskResult(client, t);
  } else {
    // 拉列表
    const result = await client.listTasks({ size: 100 });
    let tasks = (result.data?.items || result.data || []);
    tasks = filterByPrefix(tasks, namePrefix);

    if (list) {
      printList(tasks);
      data = tasks;
    }

    if (latest) {
      if (!tasks.length) { console.log('没有找到匹配的 Task'); return; }
      // 按创建时间倒序取第一条
      tasks.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
      const t = tasks[0];
      data = await printTaskResult(client, t);
    }

    if (!list && !latest) {
      printList(tasks);
      if (tasks.length > 0) {
        tasks.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
        data = await printTaskResult(client, tasks[0]);
      }
    }
  }

  if (save && data) {
    const tag = taskId || (namePrefix ? `prefix-${namePrefix}` : 'all');
    const filePath = client.writeArtifact(`bigquant-query-${tag}`, data);
    console.log('\n结果已保存:', filePath);
  }
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
