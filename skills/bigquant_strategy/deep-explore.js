#!/usr/bin/env node
/**
 * BigQuant API 深度探索 - 修复方案验证
 *
 * 发现：
 * 1. PATCH 返回 400（非 405），说明方法被接受，只是格式问题
 * 2. GET /aiflow/v1/taskruns?id=xxx 可用！
 * 3. taskrun 有 msg 字段可能包含输出
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function deepExplore() {
  const client = new BigQuantAPIClient();

  console.log('='.repeat(60));
  console.log('BigQuant API 深度探索');
  console.log('='.repeat(60));

  // ========================================
  // 1. 寻找有成功运行历史的任务
  // ========================================
  console.log('\n[1] 搜索有成功运行历史的任务...');

  const tasks = await client.listTasks({ size: 20 });
  const successTask = tasks.data?.items?.find(t => t.last_run?.state === 'success');

  if (successTask) {
    console.log('找到成功任务:', successTask.name);
    console.log('Task ID:', successTask.id);
    console.log('Run ID:', successTask.last_run?.id);

    // 获取任务详情
    const taskDetail = await client.getTask(successTask.id);
    console.log('\n任务状态:', taskDetail.data?.last_run?.state);

    // 检查 notebook 输出
    if (taskDetail.data?.data?.code) {
      try {
        const notebook = JSON.parse(taskDetail.data.data.code);
        console.log('\nNotebook cells:', notebook.cells?.length);

        for (let i = 0; i < notebook.cells?.length; i++) {
          const cell = notebook.cells[i];
          if (cell.outputs?.length > 0) {
            console.log(`\nCell ${i} outputs:`, JSON.stringify(cell.outputs, null, 2));
          }
        }
      } catch (e) {
        console.log('解析 notebook 失败:', e.message);
      }
    }

    // 获取 taskrun 详情
    const runId = successTask.last_run?.id;
    console.log('\n[2] 获取成功 taskrun 详情...');

    const taskrunsResult = await client.request('GET', `/aiflow/v1/taskruns?task_id=${successTask.id}&size=5`);
    const successRun = taskrunsResult.data?.items?.find(r => r.state === 'success');

    if (successRun) {
      console.log('成功 Run:', successRun.id);
      console.log('Run 字段:', Object.keys(successRun));
      console.log('Run 详情:', JSON.stringify(successRun, null, 2));

      // 检查 msg 是否包含输出
      if (successRun.msg) {
        console.log('\n=== msg 内容 ===');
        console.log(successRun.msg);
      }

      // 检查 data 字段
      if (successRun.data) {
        console.log('\n=== data 内容 ===');
        console.log(JSON.stringify(successRun.data, null, 2));
      }
    }

  } else {
    console.log('没有找到成功运行的任务');

    // 查看失败任务的输出
    const failedTask = tasks.data?.items?.find(t => t.last_run?.state === 'failed');
    if (failedTask) {
      console.log('\n找到失败任务:', failedTask.name);
      console.log('Task ID:', failedTask.id);

      const taskrunsResult = await client.request('GET', `/aiflow/v1/taskruns?task_id=${failedTask.id}&size=5`);
      const failedRun = taskrunsResult.data?.items?.[0];

      if (failedRun) {
        console.log('\n失败 Run 详情:');
        console.log(JSON.stringify(failedRun, null, 2));

        if (failedRun.msg) {
          console.log('\n=== 错误信息 ===');
          console.log(failedRun.msg.substring(0, 500));
        }
      }
    }
  }

  // ========================================
  // 3. 尝试 PATCH 更新任务（正确格式）
  // ========================================
  console.log('\n[3] 尝试 PATCH 更新任务代码...');

  const testTaskId = tasks.data?.items?.[0]?.id;

  // 先获取现有任务数据
  const existingTask = await client.getTask(testTaskId);
  const existingData = existingTask.data;

  // 尝试不同的 PATCH 格式
  const patchFormats = [
    // 格式1: 只更新 data.code
    { data: { code: 'print("test")' } },
    // 格式2: 更新整个 notebook
    { data: { code: JSON.stringify({
      cells: [{
        cell_type: 'code',
        source: ['print("test")'],
        outputs: [],
        execution_count: null,
        metadata: {}
      }],
      metadata: { kernelspec: { name: 'python3' } },
      nbformat: 4
    }) } },
    // 格式3: 只传 code 字段
    { code: 'print("test")' },
    // 格式4: 更新 conf
    { conf: { ...existingData.conf, retries: 1 } },
    // 格式5: 更新 name
    { name: 'test_updated' },
  ];

  for (let i = 0; i < patchFormats.length; i++) {
    try {
      const result = await client.request('PATCH', `/aiflow/v1/tasks/${testTaskId}`, patchFormats[i]);
      console.log(`\n格式${i+1} 成功!`);
      console.log('请求:', JSON.stringify(patchFormats[i]).substring(0, 100));
      console.log('响应:', JSON.stringify(result).substring(0, 300));
    } catch (e) {
      console.log(`\n格式${i+1} 失败: ${e.message.substring(0, 150)}`);
    }
  }

  // ========================================
  // 4. 探索 taskruns 查询参数
  // ========================================
  console.log('\n[4] 探索 taskruns 查询参数...');

  // 尝试通过 id 参数获取特定 taskrun
  const runId = tasks.data?.items?.[0]?.last_run?.id;
  if (runId) {
    const queryFormats = [
      `/aiflow/v1/taskruns?id=${runId}`,
      `/aiflow/v1/taskruns?ids=${runId}`,
      `/aiflow/v1/taskruns?taskrun_id=${runId}`,
      `/aiflow/v1/taskruns?constraints={"id":"${runId}"}`,
    ];

    for (const path of queryFormats) {
      try {
        const result = await client.request('GET', path);
        const items = result.data?.items || [];
        const matchRun = items.find(r => r.id === runId);
        if (matchRun) {
          console.log(`\n✓ ${path}`);
          console.log('找到:', matchRun.id, 'state:', matchRun.state);
          if (matchRun.msg) {
            console.log('msg:', matchRun.msg.substring(0, 100));
          }
        }
      } catch (e) {
        console.log(`✗ ${path}: ${e.message.substring(0, 50)}`);
      }
    }
  }

  // ========================================
  // 5. 查看所有任务类型的结构
  // ========================================
  console.log('\n[5] 分析不同状态任务的结构...');

  const states = ['pending', 'success', 'failed'];
  for (const state of states) {
    const task = tasks.data?.items?.find(t => t.last_run?.state === state);
    if (task) {
      console.log(`\n${state} 任务:`, task.name);

      const runs = await client.request('GET', `/aiflow/v1/taskruns?task_id=${task.id}&size=1`);
      const run = runs.data?.items?.[0];

      if (run) {
        console.log('  data 字段:', Object.keys(run.data || {}));
        console.log('  msg:', run.msg ? run.msg.substring(0, 100) : 'null');
        console.log('  queue:', run.queue);
      }
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('探索完成');
  console.log('='.repeat(60));
}

deepExplore().catch(console.error);