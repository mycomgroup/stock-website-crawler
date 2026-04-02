#!/usr/bin/env node
/**
 * BigQuant API 修复验证
 *
 * 已发现：
 * 1. PATCH /tasks/{id} 可用，格式：{ "code": "xxx" } 或 { "name": "xxx" }
 * 2. GET /taskruns?constraints={"id":"xxx"} 可用
 *
 * 待验证：
 * 1. PATCH 更新完整 notebook JSON
 * 2. 触发任务运行的方法
 * 3. 获取运行结果
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function verifyFixes() {
  const client = new BigQuantAPIClient();

  console.log('='.repeat(60));
  console.log('BigQuant API 修复验证');
  console.log('='.repeat(60));

  // ========================================
  // 1. 验证 PATCH 更新完整 notebook
  // ========================================
  console.log('\n[1] 验证 PATCH 更新完整 notebook...');

  // 读取示例策略
  const strategyCode = fs.readFileSync(path.join(__dirname, 'examples/simple_backtest.py'), 'utf8');

  // 创建 notebook JSON
  const notebookJson = {
    cells: [{
      cell_type: 'code',
      execution_count: null,
      metadata: {},
      outputs: [],
      source: strategyCode.split('\n').map((line, i, arr) =>
        i < arr.length - 1 ? line + '\n' : line
      )
    }],
    metadata: {
      kernelspec: {
        display_name: 'Python 3',
        language: 'python',
        name: 'python3'
      },
      language_info: {
        name: 'python',
        version: '3.8.0'
      }
    },
    nbformat: 4,
    nbformat_minor: 4
  };

  // 获取一个测试任务
  const tasks = await client.listTasks({ size: 1 });
  const taskId = tasks.data?.items?.[0]?.id;

  console.log('测试任务 ID:', taskId);

  // 尝试 PATCH 更新完整 notebook（作为字符串）
  try {
    const result = await client.request('PATCH', `/aiflow/v1/tasks/${taskId}`, {
      code: JSON.stringify(notebookJson)
    });
    console.log('✓ PATCH 更新 notebook 成功!');
    console.log('响应:', JSON.stringify(result.data).substring(0, 200));

    // 验证更新后的内容
    const updatedTask = await client.getTask(taskId);
    const updatedCode = updatedTask.data?.data?.code;

    if (updatedCode) {
      try {
        const parsed = JSON.parse(updatedCode);
        console.log('✓ 更新后的代码是有效的 notebook JSON');
        console.log('  cells 数量:', parsed.cells?.length);
        console.log('  第一行代码:', parsed.cells?.[0]?.source?.[0]?.substring(0, 50));
      } catch (e) {
        console.log('? 更新后的代码不是 notebook JSON:', updatedCode.substring(0, 100));
      }
    }
  } catch (e) {
    console.log('✗ PATCH 失败:', e.message);
  }

  // ========================================
  // 2. 探索触发任务运行
  // ========================================
  console.log('\n[2] 探索触发任务运行...');

  // 尝试创建新的 taskrun 并触发
  const triggerMethods = [
    // 方法1: 创建 taskrun 时设置 state
    { method: 'POST', path: `/aiflow/v1/taskruns`, body: {
      task_id: taskId,
      state: 'pending',
      event: new Date().toISOString().split('T')[0].replace(/-/g, '')
    }},
    // 方法2: 创建 taskrun 后 PATCH state
    { method: 'PATCH', path: `/aiflow/v1/taskruns`, body: { state: 'running' } },
    // 方法3: POST 到不同端点
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/taskruns`, body: {} },
  ];

  for (const method of triggerMethods) {
    try {
      const result = await client.request(method.method, method.path, method.body);
      console.log(`✓ ${method.method} ${method.path}: 成功`);
      console.log('  响应:', JSON.stringify(result).substring(0, 200));

      // 如果创建了 taskrun，检查状态
      if (result.data?.id) {
        const runId = result.data.id;
        console.log('  新 taskrun ID:', runId);

        // 检查状态
        const runs = await client.request('GET', `/aiflow/v1/taskruns?constraints={"id":"${runId}"}`);
        const run = runs.data?.items?.[0];
        if (run) {
          console.log('  状态:', run.state, '队列:', run.queue);
        }
      }
    } catch (e) {
      console.log(`? ${method.method} ${method.path}: ${e.message.substring(0, 100)}`);
    }
  }

  // ========================================
  // 3. 探索 aiflow 调度器 API
  // ========================================
  console.log('\n[3] 探索调度器相关 API...');

  const schedulerEndpoints = [
    { method: 'GET', path: '/aiflow/v1/scheduler' },
    { method: 'GET', path: '/aiflow/v1/scheduler/status' },
    { method: 'POST', path: '/aiflow/v1/scheduler/run' },
    { method: 'GET', path: '/aiflow/v1/queues' },
    { method: 'GET', path: '/aiflow/v1/queues/manual' },
    { method: 'POST', path: '/aiflow/v1/queues/manual/trigger' },
    { method: 'GET', path: '/aiflow/v1/workflows' },
    { method: 'POST', path: `/aiflow/v1/workflows/${taskId}/execute` },
  ];

  for (const ep of schedulerEndpoints) {
    try {
      const result = await client.request(ep.method, ep.path, ep.body || {});
      if (result.data || result.code === 0) {
        console.log(`✓ ${ep.method} ${ep.path}:`);
        console.log('  响应:', JSON.stringify(result).substring(0, 300));
      }
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1];
      if (status && status !== '404') {
        console.log(`? ${ep.method} ${ep.path}: ${status}`);
      }
    }
  }

  // ========================================
  // 4. 探索 Studio Instance API（可能触发执行）
  // ========================================
  console.log('\n[4] 探索 Studio Instance API...');

  const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

  const studioEndpoints = [
    { method: 'GET', path: `/aistudio/v1/studios/${studioId}` },
    { method: 'GET', path: `/aistudio/v1/studios/${studioId}/instances` },
    { method: 'POST', path: `/aistudio/v1/studios/${studioId}/instances` },
    { method: 'POST', path: `/aistudio/v1/studios/${studioId}/execute`, body: { task_id: taskId } },
    { method: 'POST', path: `/aistudio/v1/studios/${studioId}/run`, body: { task_id: taskId } },
  ];

  for (const ep of studioEndpoints) {
    try {
      const result = await client.request(ep.method, ep.path, ep.body || {});
      console.log(`✓ ${ep.method} ${ep.path}:`);
      console.log('  响应:', JSON.stringify(result).substring(0, 500));
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1];
      if (status && status !== '404' && status !== '405') {
        console.log(`? ${ep.method} ${ep.path}: ${status} - ${e.message.substring(0, 100)}`);
      }
    }
  }

  // ========================================
  // 5. 检查 pending taskrun 是否有执行时间
  // ========================================
  console.log('\n[5] 检查 pending taskrun 详细信息...');

  const pendingRuns = await client.request('GET', `/aiflow/v1/taskruns?task_id=${taskId}&size=5`);
  for (const run of pendingRuns.data?.items || []) {
    console.log(`\nTaskrun: ${run.id}`);
    console.log('  状态:', run.state);
    console.log('  队列:', run.queue);
    console.log('  优先级:', run.priority);
    console.log('  创建时间:', run.created_at);
    console.log('  更新时间:', run.updated_at);
    console.log('  data:', JSON.stringify(run.data));
    if (run.msg) {
      console.log('  msg:', run.msg.substring(0, 200));
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('验证完成');
  console.log('='.repeat(60));
}

verifyFixes().catch(console.error);