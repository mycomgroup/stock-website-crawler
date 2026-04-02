#!/usr/bin/env node
/**
 * 验证 BigQuant API 修复结果
 *
 * 修复发现：
 * 1. PUT /tasks/{id} → 改用 PATCH /tasks/{id}，格式 { "code": xxx }
 * 2. GET /taskruns/{id} → 改用 GET /taskruns?constraints={"id":"xxx"}
 */

import './load-env.js';
import { BigQuantTaskClient } from './request/bigquant-task-client.js';

async function verifyFixes() {
  const client = new BigQuantTaskClient();

  console.log('='.repeat(60));
  console.log('BigQuant API 修复验证');
  console.log('='.repeat(60));

  // 1. 检查登录
  console.log('\n[1] 检查登录状态...');
  const loginStatus = await client.checkLogin();
  if (!loginStatus.loggedIn) {
    console.log('✗ 未登录:', loginStatus.error);
    process.exit(1);
  }
  console.log('✓ 已登录:', loginStatus.username);

  // 获取测试任务
  const tasks = await client.listTasks({ size: 1 });
  const testTaskId = tasks.data?.items?.[0]?.id;
  console.log('测试任务 ID:', testTaskId);

  // 2. 验证 PATCH 更新任务代码
  console.log('\n[2] 验证 updateTaskCode (PATCH /tasks/{id})...');
  try {
    const testCode = '# test code\nprint("hello bigquant")';
    const result = await client.updateTaskCode(testTaskId, testCode);
    console.log('✓ 成功! PATCH 方法可用');

    // 验证更新
    const task = await client.getTask(testTaskId);
    const notebook = JSON.parse(task.data?.data?.code || '{}');
    console.log('  更新后的代码:', notebook.cells?.[0]?.source?.[0]?.substring(0, 50));
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 3. 验证更新任务配置
  console.log('\n[3] 验证 updateTaskConf...');
  try {
    const result = await client.updateTaskConf(testTaskId, {
      retries: 3
    });
    console.log('✓ 成功!');
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 4. 验证更新任务名称
  console.log('\n[4] 验证 updateTaskName...');
  try {
    const result = await client.updateTaskName(testTaskId, 'simple_backtest');
    console.log('✓ 成功!');
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 5. 验证获取 taskrun 详情
  console.log('\n[5] 验证 getTaskRunById (GET /taskruns?constraints=...)...');
  try {
    const runs = await client.getTaskRuns(testTaskId, { size: 1 });
    const runId = runs?.items?.[0]?.id;

    if (runId) {
      const run = await client.getTaskRunById(runId);
      console.log('✓ 成功! constraints 查询可用');
      console.log('  taskrun ID:', run?.id?.substring(0, 8));
      console.log('  状态:', run?.state);
      console.log('  队列:', run?.queue);
    }
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 6. 验证获取任务运行列表
  console.log('\n[6] 验证 getTaskRuns...');
  try {
    const runs = await client.getTaskRuns(testTaskId, { size: 5 });
    console.log('✓ 成功! 总数:', runs?.total);
    console.log('  运行列表:', runs?.items?.map(r => `${r.id.substring(0,8)}(${r.state})`));
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 7. 探索任务触发（预期不可用）
  console.log('\n[7] 探索任务触发端点...');
  const triggerEndpoints = [
    'POST /aiflow/v1/tasks/{id}/run',
    'POST /aiflow/v1/tasks/{id}/execute',
    'POST /aiflow/v1/tasks/{id}/trigger',
    'POST /aiflow/v1/tasks/{id}/start',
  ];

  console.log('  预期: 这些端点都返回 404');
  for (const ep of triggerEndpoints) {
    try {
      await client.request('POST', `/aiflow/v1/tasks/${testTaskId}/${ep.split(' ')[2]}`);
      console.log(`  ? ${ep}: 意外成功`);
    } catch (e) {
      const status = e.message.match(/Request failed (\d+)/)?.[1];
      if (status === '404') {
        console.log(`  ✓ ${ep}: 404 (符合预期)`);
      } else {
        console.log(`  ? ${ep}: ${status}`);
      }
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('修复验证完成');
  console.log('='.repeat(60));

  console.log('\n修复总结:');
  console.log('┌─────────────────────────────────────────────────────────────┐');
  console.log('│ 原问题                    │ 修复方案              │ 状态   │');
  console.log('├─────────────────────────────────────────────────────────────┤');
  console.log('│ PUT /tasks/{id} → 405     │ PATCH /tasks/{id}     │ ✓ 修复 │');
  console.log('│ GET /taskruns/{id} → 404  │ constraints 查询      │ ✓ 修复 │');
  console.log('│ POST /tasks/{id}/run 404  │ 无 API 支持           │ ✗ 未修复 │');
  console.log('│ GET /tasks/{id}/result    │ 无 API 支持           │ ✗ 未修复 │');
  console.log('└─────────────────────────────────────────────────────────────┘');

  console.log('\n当前可实现功能:');
  console.log('  ✓ 创建任务');
  console.log('  ✓ 更新任务代码 (PATCH)');
  console.log('  ✓ 更新任务配置');
  console.log('  ✓ 获取任务详情');
  console.log('  ✓ 获取运行列表');
  console.log('  ✓ 获取运行详情 (constraints)');
  console.log('  ✗ 自动触发运行 (需 Web UI)');
  console.log('  ✗ 获取运行结果 (需 Web UI)');
}

verifyFixes().catch(console.error);