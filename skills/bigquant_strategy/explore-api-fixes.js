#!/usr/bin/env node
/**
 * 探索 BigQuant 可能的 API 修复方案
 *
 * 尝试：
 * 1. PATCH 方法更新任务
 * 2. 其他运行端点
 * 3. taskrun 详情获取
 * 4. 结果获取
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function exploreAPIFixes() {
  const client = new BigQuantAPIClient();

  console.log('='.repeat(60));
  console.log('BigQuant API 修复探索');
  console.log('='.repeat(60));

  // 获取测试用的任务
  const tasks = await client.listTasks({ size: 5 });
  const testTask = tasks.data?.items?.[0];
  const taskId = testTask?.id;
  const runId = testTask?.last_run?.id;

  console.log('\n测试任务:', testTask?.name);
  console.log('Task ID:', taskId);
  console.log('Run ID:', runId);

  // ========================================
  // 1. 尝试 PATCH 方法更新任务
  // ========================================
  console.log('\n[1] 尝试 PATCH 更新任务代码...');

  const updateEndpoints = [
    { method: 'PATCH', path: `/aiflow/v1/tasks/${taskId}` },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/update` },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/save` },
    { method: 'PUT', path: `/aiflow/v1/tasks/${taskId}/code` },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/code` },
  ];

  for (const ep of updateEndpoints) {
    try {
      const result = await client.request(ep.method, ep.path, {
        data: { code: 'test' }
      });
      console.log(`✓ ${ep.method} ${ep.path}: 成功!`);
      console.log('  响应:', JSON.stringify(result).substring(0, 300));
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1] || 'error';
      if (status !== '404' && status !== '405') {
        console.log(`? ${ep.method} ${ep.path}: ${status}`);
      }
    }
  }

  // ========================================
  // 2. 尝试运行任务的各种端点
  // ========================================
  console.log('\n[2] 尝试运行任务端点...');

  const runEndpoints = [
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/run` },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/execute` },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/start` },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/trigger` },
    { method: 'POST', path: `/aiflow/v1/taskruns/${runId}/start` },
    { method: 'POST', path: `/aiflow/v1/taskruns/${runId}/execute` },
    { method: 'PUT', path: `/aiflow/v1/taskruns/${runId}`, body: { state: 'running' } },
    { method: 'PATCH', path: `/aiflow/v1/taskruns/${runId}`, body: { state: 'running' } },
  ];

  for (const ep of runEndpoints) {
    try {
      const result = await client.request(ep.method, ep.path, ep.body || {});
      console.log(`✓ ${ep.method} ${ep.path}: 成功!`);
      console.log('  响应:', JSON.stringify(result).substring(0, 300));
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1] || 'error';
      if (status !== '404' && status !== '405') {
        console.log(`? ${ep.method} ${ep.path}: ${status} - ${e.message.substring(0, 100)}`);
      }
    }
  }

  // ========================================
  // 3. 尝试获取 taskrun 详情
  // ========================================
  console.log('\n[3] 尝试获取 taskrun 详情...');

  const taskrunEndpoints = [
    { method: 'GET', path: `/aiflow/v1/taskruns/${runId}` },
    { method: 'GET', path: `/aiflow/v1/taskruns?id=${runId}` },
    { method: 'GET', path: `/aiflow/v1/taskruns?ids=${runId}` },
    { method: 'GET', path: `/aiflow/v1/runs/${runId}` },
    { method: 'GET', path: `/aiflow/v1/task-run/${runId}` },
    { method: 'GET', path: `/aiflow/v1/taskruns/detail?id=${runId}` },
    { method: 'GET', path: `/aiflow/v1/taskruns/${runId}/detail` },
  ];

  for (const ep of taskrunEndpoints) {
    try {
      const result = await client.request(ep.method, ep.path);
      if (result.data && !result.data?.error) {
        console.log(`✓ ${ep.method} ${ep.path}: 成功!`);
        console.log('  响应:', JSON.stringify(result.data).substring(0, 500));
      }
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1] || 'error';
      if (status !== '404') {
        console.log(`? ${ep.method} ${ep.path}: ${status}`);
      }
    }
  }

  // ========================================
  // 4. 尝试获取结果
  // ========================================
  console.log('\n[4] 尝试获取任务结果...');

  const resultEndpoints = [
    { method: 'GET', path: `/aiflow/v1/tasks/${taskId}/result` },
    { method: 'GET', path: `/aiflow/v1/tasks/${taskId}/results` },
    { method: 'GET', path: `/aiflow/v1/tasks/${taskId}/output` },
    { method: 'GET', path: `/aiflow/v1/tasks/${taskId}/report` },
    { method: 'GET', path: `/aiflow/v1/taskruns/${runId}/result` },
    { method: 'GET', path: `/aiflow/v1/taskruns/${runId}/output` },
    { method: 'GET', path: `/aiflow/v1/taskruns/${runId}/report` },
    { method: 'GET', path: `/aiflow/v1/backtests/${taskId}` },
    { method: 'GET', path: `/aiflow/v1/backtest/results/${runId}` },
  ];

  for (const ep of resultEndpoints) {
    try {
      const result = await client.request(ep.method, ep.path);
      if (result.data && !result.data?.error) {
        console.log(`✓ ${ep.method} ${ep.path}: 成功!`);
        console.log('  响应:', JSON.stringify(result).substring(0, 500));
      }
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1] || 'error';
      if (status !== '404') {
        console.log(`? ${ep.method} ${ep.path}: ${status}`);
      }
    }
  }

  // ========================================
  // 5. 查看现有任务的完整数据结构
  // ========================================
  console.log('\n[5] 查看任务完整数据结构...');

  const taskDetail = await client.getTask(taskId);
  console.log('任务字段:', Object.keys(taskDetail.data || {}));
  console.log('last_run 详情:', JSON.stringify(taskDetail.data?.last_run, null, 2));

  // 检查 data.code 中是否有输出
  if (taskDetail.data?.data?.code) {
    try {
      const notebook = JSON.parse(taskDetail.data.data.code);
      console.log('\nNotebook 结构:');
      console.log('- cells 数量:', notebook.cells?.length);
      if (notebook.cells?.[0]?.outputs?.length > 0) {
        console.log('- outputs:', JSON.stringify(notebook.cells[0].outputs, null, 2));
      } else {
        console.log('- outputs: 空 (pending 状态)');
      }
    } catch (e) {
      console.log('解析 notebook 失败:', e.message);
    }
  }

  // ========================================
  // 6. 检查 taskruns 列表是否有更多数据
  // ========================================
  console.log('\n[6] 检查 taskruns 列表数据...');

  const taskrunsList = await client.request('GET', `/aiflow/v1/taskruns?task_id=${taskId}`);
  if (taskrunsList.data?.items?.length > 0) {
    const latestRun = taskrunsList.data.items[0];
    console.log('Taskrun 字段:', Object.keys(latestRun));
    console.log('Taskrun 详情:', JSON.stringify(latestRun, null, 2).substring(0, 1000));
  }

  // ========================================
  // 7. 尝试订阅 API 获取实时更新
  // ========================================
  console.log('\n[7] 检查订阅 API...');

  try {
    const subResult = await client.request('POST', `/aiflow/v1/tasks/data/subscription`, [taskId]);
    console.log('订阅结果:', JSON.stringify(subResult).substring(0, 300));
  } catch (e) {
    console.log('订阅失败:', e.message.substring(0, 100));
  }

  console.log('\n' + '='.repeat(60));
  console.log('探索完成');
  console.log('='.repeat(60));
}

exploreAPIFixes().catch(console.error);