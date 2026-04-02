#!/usr/bin/env node
/**
 * BigQuant Task Client
 *
 * 基于 BigQuant aiflow/v1/tasks API 的策略执行客户端。
 * 对齐 JoinQuant/RiceQuant 的接口语义。
 *
 * API 验证结论（2026-04-02 更新）：
 * - POST /tasks: ✓ 可用，创建任务
 * - PATCH /tasks/{id}: ✓ 可用，更新任务代码/配置/名称
 * - GET /taskruns?constraints={"id":"xxx"}: ✓ 可用，获取运行详情
 * - POST /taskruns: ✓ 可用，创建运行记录（但停留在 pending）
 * - POST /tasks/{id}/run: ✗ 不可用(404)，无触发运行 API
 * - GET /tasks/{id}/result: ✗ 不可用(404)，无获取结果 API
 *
 * 使用方式：
 * 1. 创建任务（包含 notebook JSON 代码）
 * 2. 更新任务代码（可选）
 * 3. 通过 Web URL 在浏览器中运行/查看结果
 */

import '../load-env.js';
import { BigQuantAPIClient } from './bigquant-api-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 默认资源规格 ID (D1 免费)
const DEFAULT_RESOURCE_SPEC_ID = 'a059c996-0938-4726-ab6d-97b7e6cb2de5';

// 默认 space ID
const DEFAULT_SPACE_ID = '00000000-0000-0000-0000-000000000000';

export class BigQuantTaskClient extends BigQuantAPIClient {
  constructor(options = {}) {
    super(options);
    this.studioId = options.studioId;
  }

  // ==================== 对齐 JoinQuant/RiceQuant 接口 ====================

  /**
   * 检查登录状态
   */
  async checkLogin() {
    try {
      const user = await this.getCurrentUser();
      return {
        loggedIn: true,
        username: user.data?.username,
        userId: user.data?.id
      };
    } catch (e) {
      return { loggedIn: false, error: e.message };
    }
  }

  /**
   * 获取资源规格
   */
  async getResourceSpecs() {
    return this.request('GET', '/aiflow/v1/resourcespecs');
  }

  /**
   * 获取默认 studio ID
   */
  async ensureStudioId() {
    if (!this.studioId) {
      const studio = await this.getDefaultStudio();
      this.studioId = studio.data?.id;
    }
    return this.studioId;
  }

  /**
   * 创建任务（相当于创建 notebook）
   * @param {string} name - 任务名称
   * @param {string} code - Python 代码
   * @param {Object} options - 配置选项
   */
  async createTask(name, code, options = {}) {
    const userId = this.sessionPayload.userId || (await this.checkLogin()).userId;
    const notebookJson = this.createNotebookJSON(code);

    const taskData = {
      space_id: DEFAULT_SPACE_ID,
      creator: userId,
      name: name,
      task_type: options.taskType || 'run_once',
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
            capital_base: String(options.capital || 100000),
            start_date: options.startDate || '2023-01-01',
            end_date: options.endDate || '2023-12-31',
            benchmark: options.benchmark || '000300.XSHG',
            frequency: options.frequency || 'day'
          }
        },
        retries: 0,
        resource_options: {
          id: options.resourceSpecId || DEFAULT_RESOURCE_SPEC_ID,
          cpu: 1,
          gpu: 0,
          memory: 4
        },
        task_tune_parameters: []
      },
      data: { code: JSON.stringify(notebookJson) },
      priority: 10,
      deployment_id: DEFAULT_SPACE_ID,
      strategy_type: 0
    };

    const result = await this.request('POST', '/aiflow/v1/tasks', taskData);

    if (!result.data?.id) {
      throw new Error('Failed to create task: ' + JSON.stringify(result));
    }

    return {
      taskId: result.data.id,
      task: result.data
    };
  }

  /**
   * 更新任务代码 - 使用 PATCH 方法
   * 发现：PATCH /tasks/{id} 可用，格式为 { "code": xxx }
   */
  async updateTaskCode(taskId, code) {
    // 如果是 Python 代码，转换为 notebook JSON
    const notebookJson = this.createNotebookJSON(code);
    const codeValue = JSON.stringify(notebookJson);

    const result = await this.request('PATCH', `/aiflow/v1/tasks/${taskId}`, {
      code: codeValue
    });

    return result;
  }

  /**
   * 更新任务配置
   */
  async updateTaskConf(taskId, confUpdates) {
    const task = await this.getTask(taskId);
    const currentConf = task.data?.conf || {};

    const newConf = { ...currentConf, ...confUpdates };

    const result = await this.request('PATCH', `/aiflow/v1/tasks/${taskId}`, {
      conf: newConf
    });

    return result;
  }

  /**
   * 更新任务名称
   */
  async updateTaskName(taskId, name) {
    const result = await this.request('PATCH', `/aiflow/v1/tasks/${taskId}`, {
      name: name
    });

    return result;
  }

  /**
   * 运行任务 - 通过创建 taskrun
   */
  async runTask(taskId) {
    const event = new Date().toISOString().split('T')[0].replace(/-/g, '');

    const result = await this.request('POST', '/aiflow/v1/taskruns', {
      task_id: taskId,
      state: 'pending',
      event
    });

    return {
      taskrunId: result.data?.id,
      taskrun: result.data
    };
  }

  /**
   * 获取任务运行状态
   */
  async getTaskRunStatus(taskId) {
    const result = await this.request('GET', `/aiflow/v1/taskruns/update_time?task_id=${taskId}`);
    return result.data;
  }

  /**
   * 获取单个 taskrun 详情
   * 发现：GET /taskruns/{id} 返回 404，但 GET /taskruns?constraints={"id":"xxx"} 可用
   */
  async getTaskRunById(runId) {
    const constraints = JSON.stringify({ id: runId });
    const result = await this.request('GET', `/aiflow/v1/taskruns?constraints=${constraints}&size=1`);
    return result.data?.items?.[0] || null;
  }

  /**
   * 获取任务的所有运行记录
   */
  async getTaskRuns(taskId, options = {}) {
    const constraints = JSON.stringify({ task_id: taskId });
    const params = new URLSearchParams({
      constraints,
      page: options.page || 1,
      size: options.size || 10,
      order_by: '-created_at'
    });
    const result = await this.request('GET', `/aiflow/v1/taskruns?${params}`);
    return result.data;
  }

  /**
   * 等待任务完成
   * 注意：BigQuant 任务可能需要手动在 Web 界面运行
   */
  async waitForCompletion(taskId, timeoutMs = 300000) {
    const startTime = Date.now();
    const pollInterval = 5000;

    while (Date.now() - startTime < timeoutMs) {
      const task = await this.getTask(taskId);
      const state = task.data?.last_run?.state;

      console.log(`Task ${taskId}: state=${state || 'none'}`);

      if (state === 'success') {
        return { success: true, task };
      }

      if (state === 'failed' || state === 'error') {
        return { success: false, task, error: 'Task failed' };
      }

      await new Promise(r => setTimeout(r, pollInterval));
    }

    throw new Error(`Task timeout after ${timeoutMs}ms`);
  }

  // ==================== 辅助方法 ====================

  /**
   * 创建 Jupyter notebook JSON
   */
  createNotebookJSON(code) {
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
      cells: [{
        cell_type: 'code',
        execution_count: null,
        metadata: {},
        outputs: [],
        source: code.split('\n').map((line, i, arr) =>
          i < arr.length - 1 ? line + '\n' : line
        )
      }]
    };
  }

  /**
   * 获取任务的 Web URL
   */
  async getTaskWebUrl(taskId) {
    const studioId = await this.ensureStudioId();
    return `https://bigquant.com/aistudio/studios/${studioId}/?task=${taskId}`;
  }

  /**
   * 完整工作流：创建任务并返回 URL
   */
  async runStrategy(name, code, options = {}) {
    // 1. 确保 studio ID
    const studioId = await this.ensureStudioId();

    // 2. 创建任务
    const { taskId, task } = await this.createTask(name, code, options);

    // 3. 生成 Web URL
    const webUrl = `https://bigquant.com/aistudio/studios/${studioId}/?task=${taskId}`;

    // 3. 尝试创建 taskrun（可能不会自动运行）
    let taskrunId = null;
    try {
      const runResult = await this.runTask(taskId);
      taskrunId = runResult.taskrunId;
      console.log('Created taskrun:', taskrunId);
    } catch (e) {
      console.log('Taskrun creation skipped:', e.message);
    }

    // 4. 保存信息
    const outputPath = this.writeArtifact('bigquant-strategy', {
      taskId,
      taskrunId,
      name,
      options,
      timestamp: new Date().toISOString()
    });

    return {
      taskId,
      taskrunId,
      webUrl,
      outputPath,
      message: '任务已创建，请在浏览器中打开 Web URL 运行'
    };
  }
}

export default BigQuantTaskClient;