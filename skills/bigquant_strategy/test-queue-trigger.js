#!/usr/bin/env node
/**
 * 测试修改 task queue 是否能触发执行
 */
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');

async function req(method, path, body) {
  const r = await fetch('https://bigquant.com' + path, {
    method,
    headers: { 'Cookie': cookieStr, 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json', 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined
  });
  return r.json();
}

// 1. 创建新 task（简单测试代码）
console.log('[1] 创建测试 task...');
const userId = 'e6277718-0f37-11ed-93bb-da75731aa77c';
const notebookJson = {
  metadata: { kernelspec: { display_name: 'Python 3', language: 'python', name: 'python3' }, language_info: { name: 'python', version: '3.8.0' } },
  nbformat: 4, nbformat_minor: 4,
  cells: [{ cell_type: 'code', execution_count: null, metadata: {}, outputs: [], source: ['print("hello from bigquant")\n', 'print("test complete")'] }]
};

const createResult = await req('POST', '/bigapis/aiflow/v1/tasks', {
  space_id: '00000000-0000-0000-0000-000000000000',
  creator: userId,
  name: 'queue_test_' + Date.now(),
  task_type: 'run_once',
  labels: { in_labels: [], out_labels: [] },
  conf: {
    file_type: 'ipynb', trade_mode: 0, timezone: 'Asia/Shanghai',
    task_source: 'aistudio', scheduled_time: '', aistudio_version: 300,
    envs: { isBackTest: false },
    retries: 0,
    resource_options: { id: 'a059c996-0938-4726-ab6d-97b7e6cb2de5', cpu: 1, gpu: 0, memory: 4 },
    task_tune_parameters: []
  },
  data: { code: JSON.stringify(notebookJson) },
  priority: 10,
  deployment_id: '00000000-0000-0000-0000-000000000000',
  strategy_type: 0
});

const taskId = createResult.data?.id;
console.log('Task ID:', taskId);

// 2. 尝试不同的 queue 值
console.log('\n[2] 尝试修改 queue...');
const queues = ['auto', 'default', 'immediate', 'high', 'normal', 'low', 'backtest'];
for (const q of queues) {
  const r = await req('PATCH', `/bigapis/aiflow/v1/tasks/${taskId}`, { queue: q });
  if (r.code === 0) {
    console.log(`  queue=${q}: OK, task.queue=${r.data?.queue || 'N/A'}`);
  } else {
    console.log(`  queue=${q}: FAIL ${r.message}`);
  }
}

// 3. 创建 taskrun 并检查状态变化
console.log('\n[3] 创建 taskrun...');
const runResult = await req('POST', '/bigapis/aiflow/v1/taskruns', {
  task_id: taskId,
  state: 'pending',
  event: new Date().toISOString().split('T')[0].replace(/-/g, '')
});
const taskrunId = runResult.data?.id;
console.log('Taskrun ID:', taskrunId, 'state:', runResult.data?.state, 'queue:', runResult.data?.queue);

// 4. 等待 10 秒，检查状态
console.log('\n[4] 等待 10 秒检查状态...');
await new Promise(r => setTimeout(r, 10000));

const taskStatus = await req('GET', `/bigapis/aiflow/v1/tasks/${taskId}`);
console.log('Task last_run:', JSON.stringify(taskStatus.data?.last_run));

const runStatus = await req('GET', `/bigapis/aiflow/v1/taskruns?constraints=${encodeURIComponent(JSON.stringify({id: taskrunId}))}&size=1`);
console.log('Taskrun state:', runStatus.data?.items?.[0]?.state);

// 5. 尝试 PATCH taskrun 的 queue
console.log('\n[5] 尝试 PATCH taskrun queue...');
for (const q of ['auto', 'default', 'immediate']) {
  const r = await req('PATCH', `/bigapis/aiflow/v1/taskruns/${taskrunId}`, { queue: q });
  console.log(`  PATCH taskrun queue=${q}: ${r.code} ${r.message}`);
}

// 6. 再等 10 秒
console.log('\n[6] 再等 10 秒...');
await new Promise(r => setTimeout(r, 10000));

const finalStatus = await req('GET', `/bigapis/aiflow/v1/taskruns?constraints=${encodeURIComponent(JSON.stringify({id: taskrunId}))}&size=1`);
console.log('最终 taskrun state:', finalStatus.data?.items?.[0]?.state);

const finalTask = await req('GET', `/bigapis/aiflow/v1/tasks/${taskId}`);
console.log('最终 task last_run:', JSON.stringify(finalTask.data?.last_run));

console.log('\n完成');
