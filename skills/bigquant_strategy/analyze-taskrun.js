#!/usr/bin/env node
/**
 * 深入分析 taskrun 数据结构
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function analyzeTaskRun() {
  const client = new BigQuantAPIClient();

  // 获取一个有运行结果的任务
  const tasks = await client.listTasks({ size: 10 });

  for (const task of tasks.data?.items || []) {
    if (task.last_run?.state && task.last_run.state !== 'pending') {
      console.log('任务:', task.name);
      console.log('Task ID:', task.id);
      console.log('Task last_run:', JSON.stringify(task.last_run, null, 2));

      // 获取 taskruns 列表
      const taskruns = await client.request('GET', `/aiflow/v1/taskruns?task_id=${task.id}&size=5`);

      if (taskruns.data?.items?.length > 0) {
        for (const run of taskruns.data.items) {
          console.log('\n--- TaskRun ---');
          console.log('ID:', run.id);
          console.log('State:', run.state);
          console.log('Event:', run.event);
          console.log('Data:', JSON.stringify(run.data, null, 2));
        }
      }

      // 获取完整 task 详情
      const taskDetail = await client.getTask(task.id);
      console.log('\n--- Task Detail ---');
      console.log('data.code 前500字符:', taskDetail.data?.data?.code?.substring(0, 500));

      // 检查是否有输出字段
      console.log('\nTask data 字段:', JSON.stringify(taskDetail.data?.data, null, 2).substring(0, 1000));

      break;
    }
  }
}

analyzeTaskRun().catch(console.error);