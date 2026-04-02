#!/usr/bin/env node
/**
 * 验证 BigQuant API 关键端点
 * 对照技术方案检查实现状态
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function verifyAPIs() {
  const client = new BigQuantAPIClient();

  console.log('='.repeat(60));
  console.log('BigQuant API 验证');
  console.log('='.repeat(60));

  // 1. checkLogin - GET /bigapis/auth/v1/users/me
  console.log('\n[1] checkLogin: GET /bigapis/auth/v1/users/me');
  try {
    const user = await client.getCurrentUser();
    console.log('✓ 成功:', user.data?.username, user.data?.id);
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 2. getResourceSpecs - GET /bigapis/aiflow/v1/resourcespecs
  console.log('\n[2] getResourceSpecs: GET /bigapis/aiflow/v1/resourcespecs');
  try {
    const specs = await client.request('GET', '/aiflow/v1/resourcespecs');
    const freeSpec = specs.data?.find(s => s.price === 0);
    console.log('✓ 成功, 免费规格:', freeSpec?.name, freeSpec?.id);
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 3. listTasks - GET /bigapis/aiflow/v1/tasks
  console.log('\n[3] listTasks: GET /bigapis/aiflow/v1/tasks');
  try {
    const tasks = await client.listTasks({ size: 3 });
    console.log('✓ 成功, 总数:', tasks.data?.total);
    console.log('  最近任务:', tasks.data?.items?.map(t => `${t.name}(${t.task_type})`));
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 4. getTask - GET /bigapis/aiflow/v1/tasks/{id}
  console.log('\n[4] getTask: GET /bigapis/aiflow/v1/tasks/{id}');
  try {
    const tasks = await client.listTasks({ size: 1 });
    const taskId = tasks.data?.items?.[0]?.id;
    if (taskId) {
      const task = await client.getTask(taskId);
      console.log('✓ 成功:', task.data?.name);
      console.log('  last_run:', JSON.stringify(task.data?.last_run));
      // 检查输出在哪里
      console.log('  data 字段:', Object.keys(task.data?.data || {}));
    }
  } catch (e) {
    console.log('✗ 失败:', e.message);
  }

  // 5. 测试 PUT 更新任务代码
  console.log('\n[5] updateTaskCode: PUT /bigapis/aiflow/v1/tasks/{id}');
  try {
    const tasks = await client.listTasks({ size: 1 });
    const taskId = tasks.data?.items?.[0]?.id;
    if (taskId) {
      const result = await client.request('PUT', `/aiflow/v1/tasks/${taskId}`, {
        data: { code: 'test' }
      });
      console.log('✓ 成功:', JSON.stringify(result).substring(0, 200));
    }
  } catch (e) {
    console.log('✗ 失败:', e.message.substring(0, 200));
  }

  // 6. 测试 POST /tasks/{id}/run
  console.log('\n[6] runTask: POST /bigapis/aiflow/v1/tasks/{id}/run');
  try {
    const tasks = await client.listTasks({ size: 1 });
    const taskId = tasks.data?.items?.[0]?.id;
    if (taskId) {
      const result = await client.request('POST', `/aiflow/v1/tasks/${taskId}/run`);
      console.log('✓ 成功:', JSON.stringify(result).substring(0, 200));
    }
  } catch (e) {
    console.log('✗ 失败:', e.message.substring(0, 200));
  }

  // 7. 测试 GET /taskruns/update_time
  console.log('\n[7] getTaskRunStatus: GET /bigapis/aiflow/v1/taskruns/update_time');
  try {
    const tasks = await client.listTasks({ size: 1 });
    const taskId = tasks.data?.items?.[0]?.id;
    if (taskId) {
      const result = await client.request('GET', `/aiflow/v1/taskruns/update_time?task_id=${taskId}`);
      console.log('✓ 成功:', JSON.stringify(result).substring(0, 500));
    }
  } catch (e) {
    console.log('✗ 失败:', e.message.substring(0, 200));
  }

  // 8. 测试 taskruns 列表
  console.log('\n[8] listTaskRuns: GET /bigapis/aiflow/v1/taskruns');
  try {
    const tasks = await client.listTasks({ size: 1 });
    const taskId = tasks.data?.items?.[0]?.id;
    if (taskId) {
      const result = await client.request('GET', `/aiflow/v1/taskruns?task_id=${taskId}`);
      console.log('✓ 成功, 数量:', result.data?.total);
      if (result.data?.items?.length > 0) {
        const run = result.data.items[0];
        console.log('  最新 taskrun:', run.id, 'state:', run.state);
        console.log('  data 字段:', Object.keys(run.data || {}));
      }
    }
  } catch (e) {
    console.log('✗ 失败:', e.message.substring(0, 200));
  }

  // 9. 获取 taskrun 详情
  console.log('\n[9] getTaskRun: GET /bigapis/aiflow/v1/taskruns/{id}');
  try {
    const tasks = await client.listTasks({ size: 1 });
    const taskId = tasks.data?.items?.[0]?.id;
    if (taskId) {
      const runs = await client.request('GET', `/aiflow/v1/taskruns?task_id=${taskId}`);
      const runId = runs.data?.items?.[0]?.id;
      if (runId) {
        const run = await client.request('GET', `/aiflow/v1/taskruns/${runId}`);
        console.log('✓ 成功:', JSON.stringify(run.data, null, 2).substring(0, 1000));
      }
    }
  } catch (e) {
    console.log('✗ 失败:', e.message.substring(0, 200));
  }

  console.log('\n' + '='.repeat(60));
  console.log('验证完成');
  console.log('='.repeat(60));
}

verifyAPIs().catch(console.error);