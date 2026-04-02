#!/usr/bin/env node
/**
 * 测试任务数据订阅 API
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function testSubscription() {
  const client = new BigQuantAPIClient();

  // 获取最近的任务 IDs
  const tasks = await client.listTasks({ size: 5 });
  const taskIds = tasks.data?.items?.map(t => t.id) || [];

  console.log('Task IDs:', taskIds);

  // 尝试订阅任务状态
  console.log('\n测试 POST /aiflow/v1/tasks/data/subscription');

  try {
    // 直接传列表
    const result = await client.request('POST', '/aiflow/v1/tasks/data/subscription', taskIds);
    console.log('Success:', JSON.stringify(result, null, 2).substring(0, 2000));
  } catch (e) {
    console.log('Error:', e.message);
  }

  // 尝试其他方式
  console.log('\n测试其他端点...');

  // 获取一个有失败结果的任务
  const failedTask = tasks.data?.items?.find(t => t.last_run?.state === 'failed');
  if (failedTask) {
    console.log('\n检查失败任务:', failedTask.name);

    // 尝试获取详细信息
    const detail = await client.getTask(failedTask.id);
    console.log('Task detail keys:', Object.keys(detail.data || {}));

    // 检查 data 字段
    if (detail.data?.data) {
      console.log('data.data keys:', Object.keys(detail.data.data));

      // 如果有 code 字段，看看是否包含输出
      if (detail.data.data.code) {
        try {
          const notebook = JSON.parse(detail.data.data.code);
          console.log('Notebook cells:', notebook.cells?.length);
          for (let i = 0; i < (notebook.cells?.length || 0); i++) {
            const cell = notebook.cells[i];
            console.log(`Cell ${i}: outputs=${cell.outputs?.length || 0}`);
            if (cell.outputs?.length > 0) {
              console.log(`  Outputs:`, JSON.stringify(cell.outputs, null, 2).substring(0, 500));
            }
          }
        } catch (e) {
          console.log('解析 notebook 失败:', e.message);
        }
      }
    }

    // 检查 last_run 的详细信息
    console.log('\nlast_run:', JSON.stringify(detail.data?.last_run, null, 2));
  }
}

testSubscription().catch(console.error);