#!/usr/bin/env node
/**
 * 检查已运行任务的结果格式
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function checkTaskResult() {
  const client = new BigQuantAPIClient();

  // 列出所有任务，找到有运行结果的
  const tasks = await client.listTasks({ size: 20 });

  console.log('=== 查找有运行结果的任务 ===\n');

  for (const task of tasks.data?.items || []) {
    if (task.last_run?.state && task.last_run.state !== 'pending') {
      console.log('任务:', task.name);
      console.log('ID:', task.id);
      console.log('类型:', task.task_type);
      console.log('最后运行:', JSON.stringify(task.last_run));

      // 获取详细信息
      const detail = await client.getTask(task.id);
      console.log('data.code 长度:', detail.data?.data?.code?.length);

      // 尝试获取结果
      console.log('\n尝试获取结果...');
      try {
        const result = await client.getTaskResult(task.id);
        console.log('getTaskResult 成功:');
        console.log(JSON.stringify(result, null, 2).substring(0, 2000));
      } catch (e) {
        console.log('getTaskResult 失败:', e.message);
      }

      console.log('\n' + '-'.repeat(60) + '\n');
    }
  }
}

checkTaskResult().catch(console.error);