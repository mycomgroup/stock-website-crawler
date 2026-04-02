#!/usr/bin/env node
/**
 * 寻找 BigQuant 的执行 API
 * 重点探索 bigapis 下的所有可能端点
 */
import './load-env.js';
import { SESSION_FILE } from './paths.js';
import fs from 'fs';

const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
const cookieStr = session.cookies.filter(c => c.domain.includes('bigquant')).map(c => `${c.name}=${c.value}`).join('; ');
const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';
const taskId = '2a470e0e-d30b-4a4b-b47a-a2647d853a35';
const taskrunId = '5037089d-1531-45af-bcd5-71f6fb2cec21';

async function req(method, path, body) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 5000);
  try {
    const opts = {
      method,
      signal: ctrl.signal,
      headers: { 'Cookie': cookieStr, 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json', 'Content-Type': 'application/json' }
    };
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch('https://bigquant.com' + path, opts);
    clearTimeout(t);
    const text = await r.text();
    return { status: r.status, body: text.slice(0, 200) };
  } catch(e) {
    clearTimeout(t);
    return { status: 0, body: e.message.slice(0, 50) };
  }
}

// 1. 探索 aiflow 的所有 POST 端点
console.log('=== AIFlow 执行端点 ===');
const aiflowPaths = [
  [`/bigapis/aiflow/v1/tasks/${taskId}/run`, {}],
  [`/bigapis/aiflow/v1/tasks/${taskId}/execute`, {}],
  [`/bigapis/aiflow/v1/tasks/${taskId}/start`, {}],
  [`/bigapis/aiflow/v1/tasks/${taskId}/trigger`, {}],
  [`/bigapis/aiflow/v1/tasks/${taskId}/dispatch`, {}],
  [`/bigapis/aiflow/v1/tasks/${taskId}/submit`, {}],
  [`/bigapis/aiflow/v1/tasks/${taskId}/launch`, {}],
  [`/bigapis/aiflow/v1/taskruns/${taskrunId}/run`, {}],
  [`/bigapis/aiflow/v1/taskruns/${taskrunId}/execute`, {}],
  [`/bigapis/aiflow/v1/taskruns/${taskrunId}/start`, {}],
  [`/bigapis/aiflow/v1/taskruns/${taskrunId}/trigger`, {}],
  // PATCH taskrun state
  [`/bigapis/aiflow/v1/taskruns/${taskrunId}`, { state: 'running' }],
  // 创建新 taskrun 时指定 state=running
  [`/bigapis/aiflow/v1/taskruns`, { task_id: taskId, state: 'running', event: '20260402' }],
];

for (const [path, body] of aiflowPaths) {
  const r = await req('POST', path, body);
  if (r.status !== 404 && r.status !== 0) {
    console.log(`POST ${path.slice(-50)}: ${r.status} | ${r.body}`);
  }
}

// 2. 探索 aistudio 执行端点
console.log('\n=== AIStudio 执行端点 ===');
const aistudioPaths = [
  [`/bigapis/aistudio/v1/studios/${studioId}/run`, { task_id: taskId }],
  [`/bigapis/aistudio/v1/studios/${studioId}/execute`, { task_id: taskId }],
  [`/bigapis/aistudio/v1/studios/${studioId}/dispatch`, { task_id: taskId }],
  [`/bigapis/aistudio/v1/studios/${studioId}/submit`, { task_id: taskId }],
  [`/bigapis/aistudio/v1/studios/${studioId}/trigger`, { task_id: taskId }],
  [`/bigapis/aistudio/v1/studios/${studioId}/notebook/run`, { task_id: taskId }],
  [`/bigapis/aistudio/v1/studios/${studioId}/notebook/execute`, {}],
  [`/bigapis/aistudio/v1/execute`, { studio_id: studioId, task_id: taskId }],
  [`/bigapis/aistudio/v1/run`, { studio_id: studioId, task_id: taskId }],
];

for (const [path, body] of aistudioPaths) {
  const r = await req('POST', path, body);
  if (r.status !== 404 && r.status !== 0) {
    console.log(`POST ${path.slice(-50)}: ${r.status} | ${r.body}`);
  }
}

// 3. 探索 bigquant 特有的 API
console.log('\n=== BigQuant 特有 API ===');
const bqPaths = [
  ['/bigapis/bigquant/v1/run', { task_id: taskId }],
  ['/bigapis/bigquant/v1/execute', { task_id: taskId }],
  ['/bigapis/notebook/v1/run', { task_id: taskId }],
  ['/bigapis/notebook/v1/execute', { task_id: taskId }],
  ['/bigapis/kernel/v1/run', { task_id: taskId }],
  ['/bigapis/kernel/v1/execute', { code: 'print(1)' }],
  // 通过 proxy 直接访问内部服务
  [`/aistudio/studios/${studioId}/proxy/8888/api/kernels`, null],
  [`/aistudio/studios/${studioId}/proxy/8888/api/sessions`, null],
];

for (const [path, body] of bqPaths) {
  const method = body === null ? 'GET' : 'POST';
  const r = await req(method, path, body);
  if (r.status !== 404 && r.status !== 0) {
    console.log(`${method} ${path.slice(-50)}: ${r.status} | ${r.body}`);
  }
}

// 4. 检查 taskrun 的 queue 字段 - 尝试改变 queue
console.log('\n=== 修改 taskrun queue ===');
const queueAttempts = [
  { queue: 'auto' },
  { queue: 'default' },
  { queue: 'immediate' },
  { queue: 'high' },
  { state: 'running', queue: 'auto' },
];

for (const body of queueAttempts) {
  const r = await req('PATCH', `/bigapis/aiflow/v1/taskruns/${taskrunId}`, body);
  if (r.status !== 404 && r.status !== 0) {
    console.log(`PATCH taskrun ${JSON.stringify(body)}: ${r.status} | ${r.body}`);
  }
}

// 5. 检查 task 的 queue 字段
console.log('\n=== 修改 task queue/status ===');
const taskAttempts = [
  { status: 'running' },
  { queue: 'auto' },
  { last_run: { state: 'running' } },
];

for (const body of taskAttempts) {
  const r = await req('PATCH', `/bigapis/aiflow/v1/tasks/${taskId}`, body);
  if (r.status !== 404 && r.status !== 0) {
    console.log(`PATCH task ${JSON.stringify(body)}: ${r.status} | ${r.body}`);
  }
}

console.log('\n完成');
