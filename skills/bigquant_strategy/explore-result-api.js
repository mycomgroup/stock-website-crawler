#!/usr/bin/env node
/**
 * 探索 BigQuant 任务结果获取方式
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function exploreResultAPI() {
  const client = new BigQuantAPIClient();

  // 获取一个有运行结果的任务
  const tasks = await client.listTasks({ size: 10 });

  console.log('=== 查找可用的任务 ===\n');

  for (const task of tasks.data?.items || []) {
    if (task.last_run?.state && task.last_run.state !== 'pending') {
      console.log('任务:', task.name, '-', task.id);
      console.log('类型:', task.task_type);
      console.log('最后运行:', JSON.stringify(task.last_run));

      // 尝试各种可能的端点
      const endpoints = [
        { name: 'GET task', fn: () => client.getTask(task.id) },
        { name: 'GET task/result', fn: () => client.request('GET', `/aiflow/v1/tasks/${task.id}/result`) },
        { name: 'GET task/output', fn: () => client.request('GET', `/aiflow/v1/tasks/${task.id}/output`) },
        { name: 'GET task/logs', fn: () => client.request('GET', `/aiflow/v1/tasks/${task.id}/logs`) },
        { name: 'GET taskruns', fn: () => client.request('GET', `/aiflow/v1/taskruns?task_id=${task.id}`) },
        { name: 'GET taskrun detail', fn: () => client.request('GET', `/aiflow/v1/taskruns/${task.last_run?.id}`) },
        { name: 'GET taskrun result', fn: () => client.request('GET', `/aiflow/v1/taskruns/${task.last_run?.id}/result`) },
        { name: 'GET taskrun output', fn: () => client.request('GET', `/aiflow/v1/taskruns/${task.last_run?.id}/output`) },
        { name: 'GET taskrun logs', fn: () => client.request('GET', `/aiflow/v1/taskruns/${task.last_run?.id}/logs`) },
        { name: 'GET backtest result', fn: () => client.request('GET', `/aiflow/v1/backtests/${task.id}`) },
        { name: 'GET report', fn: () => client.request('GET', `/aiflow/v1/reports/${task.id}`) },
      ];

      console.log('\n尝试获取结果:');
      for (const ep of endpoints) {
        try {
          const result = await ep.fn();
          console.log(`  ✓ ${ep.name}:`, JSON.stringify(result).substring(0, 300));

          // 如果成功，打印更多详情
          if (result.data && typeof result.data === 'object') {
            console.log('    data keys:', Object.keys(result.data));
          }
        } catch (e) {
          const msg = e.message.substring(0, 100);
          if (!msg.includes('404') && !msg.includes('405')) {
            console.log(`  ? ${ep.name}:`, msg);
          }
        }
      }

      console.log('\n' + '-'.repeat(60) + '\n');
      break;  // 只检查第一个有结果的任务
    }
  }
}

exploreResultAPI().catch(console.error);