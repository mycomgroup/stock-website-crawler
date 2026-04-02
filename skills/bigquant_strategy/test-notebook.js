#!/usr/bin/env node
/**
 * Test BigQuant Notebook Client
 *
 * Tests the task-based notebook functionality for BigQuant:
 * - Creating backtest tasks
 * - Running tasks
 * - Waiting for results
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';
import { BigQuantNotebookClient } from './request/bigquant-notebook-client.js';

async function testNotebookClient() {
  console.log('='.repeat(60));
  console.log('BigQuant Notebook Client Test');
  console.log('='.repeat(60));

  // First get studio ID from API client
  const apiClient = new BigQuantAPIClient();

  // Get studio info first
  console.log('\n[Step 0] Getting studio info...');
  const studio = await apiClient.getDefaultStudio();
  const studioId = studio.data?.id;

  if (!studioId) {
    console.log('Failed to get studio ID');
    console.log('Studio response:', JSON.stringify(studio, null, 2).substring(0, 500));
    return;
  }

  console.log('Studio ID:', studioId);
  console.log('Studio status:', studio.data?.status);

  // Create notebook client with studio ID
  const client = new BigQuantNotebookClient({ studioId });

  // Test 1: Create notebook JSON
  console.log('\n[Step 1] Testing createNotebookJSON...');
  const notebookJson = client.createNotebookJSON(['print("Hello BigQuant!")']);
  console.log('Notebook JSON:', JSON.stringify(notebookJson, null, 2));

  // Test 2: Create and run a simple backtest
  console.log('\n[Step 2] Testing createAndRunBacktest...');

  // Simple test strategy
  const testCode = `# BigQuant Test Strategy
import bigquant as bq

# Simple print test
print("BigQuant test strategy running")

# Get data
data = bq.DataSource.get('000300.XSHG', start_date='${new Date().toISOString().split('T')[0].replace(/-/g, '').slice(0, 8) - 30}', end_date='${new Date().toISOString().split('T')[0].replace(/-/g, '')}')
print("Data retrieved:", len(data) if hasattr(data, '__len__') else 'N/A')
`;

  try {
    const { taskId, task } = await client.createAndRunBacktest({
      code: testCode,
      name: 'test_strategy',
      startDate: '2023-01-01',
      endDate: '2023-12-31',
      capital: 100000,
      taskType: 'run_once'
    });

    console.log('Task created:', taskId);
    console.log('Task status:', task.status);
    console.log('Task type:', task.task_type);

    // Test 3: Check task status
    console.log('\n[Step 3] Checking task status...');
    const taskDetail = await client.getTask(taskId);
    console.log('Task detail:', JSON.stringify(taskDetail.data, null, 2).substring(0, 1000));

    // Test 4: List existing tasks to verify creation
    console.log('\n[Step 4] Listing tasks...');
    const tasks = await client.listTasks({ size: 5 });
    console.log('Recent tasks:', JSON.stringify(tasks.data?.items?.slice(0, 3), null, 2));

    console.log('\n✓ Task creation successful');
    console.log('Task ID:', taskId);

    // Note: Waiting for completion would take time
    // const result = await client.waitForResult(taskId, 60000);
    // console.log('Result:', JSON.stringify(result, null, 2));

  } catch (e) {
    console.log('Error creating/running task:', e.message);
    console.log('\nTrying alternative approach...');

    // If task creation fails, try executeCode method
    try {
      const result = await client.executeCode('print("test")', {
        name: 'simple_test',
        startDate: '2023-01-01',
        endDate: '2023-01-31'
      });
      console.log('ExecuteCode result:', JSON.stringify(result, null, 2));
    } catch (e2) {
      console.log('ExecuteCode also failed:', e2.message);
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('Test complete');
  console.log('='.repeat(60));
}

testNotebookClient().catch(console.error);