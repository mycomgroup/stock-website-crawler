#!/usr/bin/env node
/**
 * Try different approaches to run a BigQuant task
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function tryRunTask() {
  const client = new BigQuantAPIClient();

  // Get the task we just created
  const tasks = await client.listTasks({ size: 1 });
  const taskId = tasks.data?.items?.[0]?.id;

  if (!taskId) {
    console.log('No task found');
    return;
  }

  console.log('Task ID:', taskId);

  // Try different endpoints to run the task
  const endpoints = [
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/run` },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/execute` },
    { method: 'POST', path: `/aiflow/v1/tasks/${taskId}/start` },
    { method: 'POST', path: `/aiflow/v1/taskruns`, body: { task_id: taskId } },
    { method: 'POST', path: `/aiflow/v1/taskruns/create`, body: { task_id: taskId } },
    { method: 'POST', path: `/aiflow/v1/taskruns/${taskId}/run` },
  ];

  for (const endpoint of endpoints) {
    console.log(`\nTrying: ${endpoint.method} ${endpoint.path}`);
    try {
      const result = await client.request(endpoint.method, endpoint.path, endpoint.body);
      console.log('Success:', JSON.stringify(result, null, 2).substring(0, 500));
    } catch (e) {
      console.log('Error:', e.message.substring(0, 200));
    }
  }

  // Check if there's a taskruns endpoint
  console.log('\n\nTrying to list taskruns...');
  try {
    const taskruns = await client.request('GET', `/aiflow/v1/taskruns?task_id=${taskId}`);
    console.log('Taskruns:', JSON.stringify(taskruns, null, 2).substring(0, 1000));
  } catch (e) {
    console.log('Error listing taskruns:', e.message.substring(0, 200));
  }
}

tryRunTask().catch(console.error);