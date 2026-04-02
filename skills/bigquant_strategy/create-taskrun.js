#!/usr/bin/env node
/**
 * Create a taskrun to execute a BigQuant task
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function createTaskRun() {
  const client = new BigQuantAPIClient();

  // Get the task we just created
  const tasks = await client.listTasks({ size: 1 });
  const taskId = tasks.data?.items?.[0]?.id;

  if (!taskId) {
    console.log('No task found');
    return;
  }

  console.log('Task ID:', taskId);

  // Try to create a taskrun
  console.log('\nTrying to create taskrun...');

  // Based on the error, we need 'state' field
  const taskrunData = {
    task_id: taskId,
    state: 'pending',  // or 'running', 'submitted'?
    event: new Date().toISOString().split('T')[0].replace(/-/g, '')
  };

  console.log('Request body:', JSON.stringify(taskrunData, null, 2));

  try {
    const result = await client.request('POST', '/aiflow/v1/taskruns', taskrunData);
    console.log('Success:', JSON.stringify(result, null, 2));
  } catch (e) {
    console.log('Error:', e.message);

    // Try with different field combinations
    const alternatives = [
      { task_id: taskId, state: 'submitted' },
      { task_id: taskId, state: 'pending', space_id: '00000000-0000-0000-0000-000000000000' },
      { task_id: taskId, state: 'running' },
      { task_id: taskId, state: 'pending', task_type: 'run_once' },
    ];

    for (const body of alternatives) {
      console.log(`\nTrying with:`, JSON.stringify(body));
      try {
        const result = await client.request('POST', '/aiflow/v1/taskruns', body);
        console.log('Success:', JSON.stringify(result, null, 2));
      } catch (e2) {
        console.log('Error:', e2.message.substring(0, 300));
      }
    }
  }
}

createTaskRun().catch(console.error);