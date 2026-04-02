#!/usr/bin/env node
import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function inspectTask() {
  const client = new BigQuantAPIClient();

  console.log('=== Inspecting existing tasks ===\n');

  // List tasks
  const tasks = await client.listTasks({ size: 5 });

  if (tasks.data?.items?.length > 0) {
    for (const task of tasks.data.items) {
      console.log('Task ID:', task.id);
      console.log('Name:', task.name);
      console.log('Type:', task.task_type);
      console.log('Status:', task.status);
      console.log('Created:', task.created_at);
      console.log('Config:', JSON.stringify(task.conf, null, 2));
      console.log('-'.repeat(60));
    }
  } else {
    console.log('No tasks found');
  }

  // Get detailed task info
  if (tasks.data?.items?.length > 0) {
    const taskId = tasks.data.items[0].id;
    console.log('\n=== Getting detailed task info ===');
    console.log('Task ID:', taskId);

    try {
      const detail = await client.getTask(taskId);
      console.log('Detail:', JSON.stringify(detail, null, 2).substring(0, 3000));
    } catch (e) {
      console.log('Error getting task detail:', e.message);
    }
  }
}

inspectTask().catch(console.error);