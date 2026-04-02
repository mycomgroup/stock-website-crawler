#!/usr/bin/env node
/**
 * 搜索 BigQuant 可能的结果获取 API
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function searchResultAPIs() {
  const client = new BigQuantAPIClient();

  // 获取一个有运行历史的任务
  const tasks = await client.listTasks({ size: 10 });
  const taskWithRun = tasks.data?.items?.find(t => t.last_run?.state === 'failed');

  if (!taskWithRun) {
    console.log('没有找到有运行结果的任务');
    return;
  }

  console.log('任务:', taskWithRun.name);
  console.log('Task ID:', taskWithRun.id);
  console.log('Last run:', JSON.stringify(taskWithRun.last_run));

  const taskId = taskWithRun.id;
  const runId = taskWithRun.last_run?.id;

  // 尝试各种可能的端点
  const endpoints = [
    // 回测相关
    `GET /aiflow/v1/backtests?task_id=${taskId}`,
    `GET /aiflow/v1/backtests/${taskId}`,
    `GET /aiflow/v1/backtest/${taskId}`,
    `GET /aiflow/v1/backtest/${runId}`,

    // 结果相关
    `GET /aiflow/v1/results?task_id=${taskId}`,
    `GET /aiflow/v1/results/${runId}`,
    `GET /aiflow/v1/taskruns/${runId}/result`,
    `GET /aiflow/v1/taskruns/${runId}/output`,
    `GET /aiflow/v1/taskruns/${runId}/logs`,

    // 报告相关
    `GET /aiflow/v1/reports?task_id=${taskId}`,
    `GET /aiflow/v1/reports/${taskId}`,
    `GET /aiflow/v1/reports/${runId}`,

    // 交易相关
    `GET /trading/v1/portfolio/strategies/${taskId}`,
    `GET /trading/v1/portfolio/backtests/${taskId}`,
  ];

  console.log('\n=== 测试各种端点 ===\n');

  for (const endpoint of endpoints) {
    const [method, path] = endpoint.split(' ');
    try {
      const result = await client.request(method, path);
      const data = JSON.stringify(result, null, 2);
      if (data.length > 50 && !data.includes('"data":null') && !data.includes('"items":[]')) {
        console.log(`✓ ${endpoint}`);
        console.log('  响应:', data.substring(0, 500));
        console.log('');
      }
    } catch (e) {
      // 忽略 404 和 405
    }
  }
}

searchResultAPIs().catch(console.error);