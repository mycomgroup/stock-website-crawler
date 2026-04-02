#!/usr/bin/env node
/**
 * BigQuant Notebook Client
 *
 * BigQuant AIStudio uses a task-based approach for strategy execution.
 * Strategies are executed via the task API:
 * - POST /bigapis/aiflow/v1/tasks - Create a task
 * - POST /bigapis/aiflow/v1/taskruns - Create a taskrun to trigger execution
 * - GET /bigapis/aiflow/v1/tasks/{id} - Check task status
 * - GET /bigapis/aiflow/v1/tasks/{id}/result - Get results
 *
 * The notebook JSON is stored in task.data.code.
 *
 * IMPORTANT: BigQuant tasks may require execution from the web interface.
 * The API allows creating tasks but the scheduler might need manual triggering.
 */

import '../load-env.js';
import { BigQuantAPIClient } from './bigquant-api-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export class BigQuantNotebookClient extends BigQuantAPIClient {
  constructor(options = {}) {
    super(options);
    this.studioId = options.studioId || process.env.BIGQUANT_STUDIO_ID;
    this.baseUrl = `/aistudio/studios/${this.studioId}/`;
  }

  /**
   * Create a Jupyter notebook JSON structure
   */
  createNotebookJSON(cells = []) {
    return {
      metadata: {
        kernelspec: {
          display_name: 'Python 3',
          language: 'python',
          name: 'python3'
        },
        language_info: {
          name: 'python',
          version: '3.8.0'
        }
      },
      nbformat: 4,
      nbformat_minor: 4,
      cells: cells.map(cell => {
        if (typeof cell === 'string') {
          return {
            cell_type: 'code',
            execution_count: null,
            metadata: {},
            outputs: [],
            source: cell.split('\n').map((line, i, arr) => i < arr.length - 1 ? line + '\n' : line)
          };
        }
        return cell;
      })
    };
  }

  /**
   * Create a taskrun to trigger task execution
   */
  async createTaskRun(taskId) {
    const event = new Date().toISOString().split('T')[0].replace(/-/g, '');
    return this.request('POST', '/aiflow/v1/taskruns', {
      task_id: taskId,
      state: 'pending',
      event
    });
  }

  /**
   * Get taskrun details
   */
  async getTaskRun(taskrunId) {
    return this.request('GET', `/aiflow/v1/taskruns/${taskrunId}`);
  }

  /**
   * List taskruns for a task
   */
  async listTaskRuns(taskId) {
    return this.request('GET', `/aiflow/v1/taskruns?task_id=${taskId}`);
  }

  /**
   * Create and run a backtest task with notebook-style code
   */
  async createAndRunBacktest(config) {
    const notebookJson = this.createNotebookJSON([config.code]);
    const userId = this.sessionPayload.userId || 'e6277718-0f37-11ed-93bb-da75731aa77c';

    const taskData = {
      space_id: '00000000-0000-0000-0000-000000000000',
      creator: userId,
      name: config.name || 'strategy',
      task_type: config.taskType || 'run_once',
      labels: { in_labels: [], out_labels: [] },
      conf: {
        file_type: 'ipynb',
        trade_mode: 0,
        timezone: 'Asia/Shanghai',
        task_source: 'aistudio',
        scheduled_time: '',
        aistudio_version: 300,
        envs: {
          isBackTest: true,
          strategy_params: {
            capital_base: String(config.capital || 100000),
            start_date: config.startDate || '2021-01-01',
            end_date: config.endDate || '2025-03-28',
            benchmark: config.benchmark || '000300.XSHG',
            frequency: config.frequency || 'day'
          }
        },
        retries: 0,
        resource_options: {
          id: 'a059c996-0938-4726-ab6d-97b7e6cb2de5',
          cpu: 1,
          gpu: 0,
          memory: 4
        },
        task_tune_parameters: []
      },
      data: { code: JSON.stringify(notebookJson) },
      priority: 10,
      deployment_id: '00000000-0000-0000-0000-000000000000',
      strategy_type: 0
    };

    // Create the task
    const createResult = await this.createTask(taskData);

    if (!createResult.data?.id) {
      throw new Error('Failed to create task: ' + JSON.stringify(createResult));
    }

    const taskId = createResult.data.id;
    console.log('Created task:', taskId);

    // Create a taskrun to trigger execution
    try {
      const taskrunResult = await this.createTaskRun(taskId);
      const taskrunId = taskrunResult.data?.id;
      console.log('Created taskrun:', taskrunId);

      return {
        taskId,
        taskrunId,
        task: createResult.data,
        taskrun: taskrunResult.data
      };
    } catch (e) {
      console.log('Taskrun creation error:', e.message);
      return { taskId, task: createResult.data };
    }
  }

  /**
   * Execute code as a notebook cell
   */
  async executeCode(code, options = {}) {
    return this.createAndRunBacktest({
      code,
      name: options.name || 'notebook_execution',
      startDate: options.startDate,
      endDate: options.endDate,
      capital: options.capital,
      benchmark: options.benchmark,
      frequency: options.frequency,
      taskType: options.taskType || 'run_once'
    });
  }

  /**
   * Wait for task completion
   */
  async waitForResult(taskId, timeoutMs = 300000) {
    const startTime = Date.now();
    const pollInterval = 10000;

    while (Date.now() - startTime < timeoutMs) {
      const task = await this.getTask(taskId);
      const lastRun = task.data?.last_run;

      console.log(`Task ${taskId}: last_run.state=${lastRun?.state || 'none'}`);

      if (lastRun?.state === 'success') {
        try {
          const result = await this.getTaskResult(taskId);
          return { success: true, task, result };
        } catch (e) {
          return { success: true, task, result: null };
        }
      }

      if (lastRun?.state === 'failed') {
        return { success: false, task, error: 'Task failed', details: lastRun };
      }

      await new Promise(r => setTimeout(r, pollInterval));
    }

    throw new Error(`Task timeout after ${timeoutMs}ms`);
  }

  /**
   * Run a complete backtest workflow
   */
  async runBacktest(strategyCode, config = {}) {
    console.log('Creating backtest task...');
    const { taskId, taskrunId } = await this.createAndRunBacktest({
      code: strategyCode,
      name: config.name || 'backtest',
      startDate: config.startDate || '2023-01-01',
      endDate: config.endDate || '2023-12-31',
      capital: config.capital || 100000,
      benchmark: config.benchmark || '000300.XSHG'
    });

    // Save task info
    const outputPath = this.writeArtifact('bigquant-task', {
      taskId,
      taskrunId,
      config,
      timestamp: new Date().toISOString()
    });
    console.log('Task info saved to:', outputPath);

    return {
      taskId,
      taskrunId,
      outputPath,
      webUrl: `https://bigquant.com/aistudio/studios/${this.studioId}/?task=${taskId}`
    };
  }
}

export default BigQuantNotebookClient;