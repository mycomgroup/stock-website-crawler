#!/usr/bin/env node
/**
 * 检查所有任务的详细信息和可能的输出
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function checkAllTasks() {
  const client = new BigQuantAPIClient();

  const tasks = await client.listTasks({ size: 20 });

  console.log('=== 所有任务状态 ===\n');

  for (const task of tasks.data?.items || []) {
    console.log('---');
    console.log('名称:', task.name);
    console.log('ID:', task.id);
    console.log('类型:', task.task_type);
    console.log('last_run:', JSON.stringify(task.last_run));

    // 获取详细信息
    const detail = await client.getTask(task.id);

    // 检查 notebook 是否有输出
    if (detail.data?.data?.code) {
      try {
        const notebook = JSON.parse(detail.data.data.code);
        const hasOutputs = notebook.cells?.some(c => c.outputs?.length > 0);
        console.log('Notebook 有输出:', hasOutputs);

        if (hasOutputs) {
          for (const cell of notebook.cells || []) {
            if (cell.outputs?.length > 0) {
              console.log('输出:', JSON.stringify(cell.outputs, null, 2).substring(0, 1000));
            }
          }
        }
      } catch (e) {
        console.log('Notebook 解析失败');
      }
    }

    console.log('');
  }
}

checkAllTasks().catch(console.error);