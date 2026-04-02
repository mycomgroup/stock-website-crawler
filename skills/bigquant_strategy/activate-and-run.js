#!/usr/bin/env node
/**
 * 尝试激活 Studio 实例并执行任务
 *
 * 从浏览器捕获中发现:
 * - POST /aistudio/v1/studios/{id}/instances 激活 studio
 * - POST /aiflow/v1/taskruns 创建运行 (但停留在 pending)
 *
 * 假设: 需要先激活 studio instance，taskrun 才能被执行
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';
import { BigQuantTaskClient } from './request/bigquant-task-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function activateStudioAndRun() {
  const client = new BigQuantAPIClient();
  const taskClient = new BigQuantTaskClient();

  const studioId = 'e6277718-0f37-11ed-93bb-da75731aa77c';

  console.log('=== Step 1: 激活 Studio Instance ===');

  // 从捕获的请求中，激活 studio instance 的参数
  const instanceResult = await client.request('POST', `/aistudio/v1/studios/${studioId}/instances`, {
    aistudio_version: 300
  });

  console.log('Instance result:', JSON.stringify(instanceResult, null, 2));

  console.log('\n=== Step 2: 获取 Studio 状态 ===');

  const studioStatus = await client.request('GET', `/aistudio/v1/studios/${studioId}`);
  console.log('Studio status:', JSON.stringify(studioStatus.data, null, 2));

  console.log('\n=== Step 3: 检查现有任务状态 ===');

  const tasks = await client.listTasks({ size: 5 });
  console.log('Recent tasks:');

  for (const task of tasks.data?.items || []) {
    console.log(`  - ${task.name}: ${task.last_run?.state || 'no run'}`);
  }

  console.log('\n=== Step 4: 尝试执行现有任务 ===');

  // 找一个有 pending run 的任务
  const pendingTask = tasks.data?.items?.find(t => t.last_run?.state === 'pending');

  if (pendingTask) {
    console.log('Found pending task:', pendingTask.name, pendingTask.id);

    // 尝试不同的触发方式
    const triggerEndpoints = [
      // 可能的触发 API
      { method: 'POST', path: `/aiflow/v1/taskruns/${pendingTask.last_run.id}/start` },
      { method: 'POST', path: `/aiflow/v1/taskruns/${pendingTask.last_run.id}/execute` },
      { method: 'POST', path: `/aiflow/v1/taskruns/${pendingTask.last_run.id}/run` },
      { method: 'POST', path: `/aiflow/v1/tasks/${pendingTask.id}/trigger` },
      { method: 'POST', path: `/aiflow/v1/tasks/${pendingTask.id}/execute` },
      { method: 'PUT', path: `/aiflow/v1/taskruns/${pendingTask.last_run.id}`, body: { state: 'running' } },
    ];

    console.log('\n尝试触发 API:');
    for (const endpoint of triggerEndpoints) {
      console.log(`  ${endpoint.method} ${endpoint.path}`);
      try {
        const result = await client.request(endpoint.method, endpoint.path, endpoint.body);
        if (result.code === 0 || !result.code) {
          console.log('    ✓ Success:', JSON.stringify(result, null, 2).substring(0, 200));
        } else {
          console.log('    Response:', result.code, result.reason || result.message);
        }
      } catch (e) {
        console.log('    Error:', e.message.substring(0, 50));
      }
    }
  }

  console.log('\n=== Step 5: 创建新任务并运行 ===');

  // 使用一个简单的测试策略
  const testCode = `
# BigQuant 测试策略
import bigquant as bq

# 获取数据
data = bq.get_data('000001.XSHE', '2023-01-01', '2023-12-31')
print(f"获取到 {len(data)} 条数据")

# 简单输出
print("策略执行完成")
`;

  const result = await taskClient.runStrategy('test_execution', testCode, {
    startDate: '2023-01-01',
    endDate: '2023-12-31',
    capital: 100000
  });

  console.log('创建结果:');
  console.log('  Task ID:', result.taskId);
  console.log('  Taskrun ID:', result.taskrunId);
  console.log('  Web URL:', result.webUrl);

  // 等待并监控状态
  console.log('\n=== Step 6: 监控任务状态 (30秒) ===');

  for (let i = 0; i < 6; i++) {
    await new Promise(r => setTimeout(r, 5000));

    const taskStatus = await client.getTask(result.taskId);
    const state = taskStatus.data?.last_run?.state;

    console.log(`  [${i * 5}s] State: ${state || 'none'}`);

    if (state === 'success' || state === 'failed') {
      console.log('任务执行结束:', state);
      break;
    }
  }

  console.log('\n=== 完成 ===');
  console.log('Web URL:', result.webUrl);
}

activateStudioAndRun().catch(console.error);