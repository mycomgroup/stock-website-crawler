#!/usr/bin/env node
/**
 * Test BigQuant Notebook Client - Check Task Status
 */

import './load-env.js';
import { BigQuantNotebookClient } from './request/bigquant-notebook-client.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function checkTaskStatus() {
  const client = new BigQuantAPIClient();

  // Get the most recent task
  const tasks = await client.listTasks({ size: 1 });
  const latestTask = tasks.data?.items?.[0];

  if (latestTask) {
    console.log('Latest task:', latestTask.id);
    console.log('Name:', latestTask.name);
    console.log('Status:', latestTask.status);
    console.log('Type:', latestTask.task_type);
    console.log('Last run:', JSON.stringify(latestTask.last_run, null, 2));

    // Get full task details
    const detail = await client.getTask(latestTask.id);
    console.log('\nFull task details:');
    console.log(JSON.stringify(detail.data, null, 2).substring(0, 3000));
  }
}

checkTaskStatus().catch(console.error);