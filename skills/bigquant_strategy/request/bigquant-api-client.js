/**
 * BigQuant HTTP API Client
 *
 * BigQuant uses REST API with the following base path:
 * https://bigquant.com/bigapis/
 *
 * Key endpoints:
 * - /bigapis/auth/v1/users/me - User info
 * - /bigapis/aistudio/v1/studios/{id} - Studio info
 * - /bigapis/aiflow/v1/tasks - Tasks (backtests)
 * - /bigapis/trading/v1/portfolio/strategies - Portfolio strategies
 */

import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X_10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

export function loadJson(filePath) {
  if (!fs.existsSync(filePath)) return {};
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    return {};
  }
}

export function saveJson(filePath, data) {
  ensureDir(filePath);
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

export class BigQuantAPIClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.sessionPayload = options.sessionPayload || loadJson(this.sessionFile);
    this.origin = 'https://bigquant.com';
    this.apiBase = `${this.origin}/bigapis`;
    this.cookieJar = this.sessionPayload.cookies || [];
  }

  buildCookieHeader() {
    return this.cookieJar
      .map(cookie => `${cookie.name}=${cookie.value}`)
      .join('; ');
  }

  buildHeaders(requestUrl, overrides = {}) {
    return {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'content-type': 'application/json',
      'user-agent': USER_AGENT,
      'referer': this.origin,
      'cookie': this.buildCookieHeader(),
      ...overrides
    };
  }

  async request(method, endpoint, body = null) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.apiBase}${endpoint}`;

    const options = {
      method,
      headers: this.buildHeaders(url)
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    const text = await response.text();

    if (!response.ok) {
      throw new Error(`Request failed ${response.status} ${url}: ${text.slice(0, 500)}`);
    }

    try {
      return JSON.parse(text);
    } catch (e) {
      return text;
    }
  }

  // ==================== User API ====================

  async getCurrentUser() {
    return this.request('GET', '/auth/v1/users/me');
  }

  async getUserSettings() {
    return this.request('GET', '/auth/v1/users/setting');
  }

  // ==================== AIStudio API ====================

  async getStudio(studioId) {
    return this.request('GET', `/aistudio/v1/studios/${studioId}`);
  }

  async getDefaultStudio() {
    return this.request('GET', '/aistudio/v1/studios/@default');
  }

  async getResourceSpecs() {
    return this.request('GET', '/aistudio/v1/resourcespecs');
  }

  // ==================== Task API (Backtest) ====================

  /**
   * List tasks (backtests)
   * @param {Object} options - Query options
   * @param {string} options.creator - User ID
   * @param {number} options.page - Page number
   * @param {number} options.size - Page size
   */
  async listTasks(options = {}) {
    const creator = options.creator || this.sessionPayload.userId;
    const constraints = JSON.stringify({
      space_id: "00000000-0000-0000-0000-000000000000",
      creator
    });
    const params = new URLSearchParams({
      constraints,
      page: options.page || 1,
      size: options.size || 50,
      exclude_fields: 'data',
      order_by: '-created_at'
    });
    return this.request('GET', `/aiflow/v1/tasks?${params}`);
  }

  /**
   * Get task details
   * @param {string} taskId - Task ID
   */
  async getTask(taskId) {
    return this.request('GET', `/aiflow/v1/tasks/${taskId}`);
  }

  /**
   * Create a new task (backtest)
   * @param {Object} taskData - Task configuration
   */
  async createTask(taskData) {
    return this.request('POST', '/aiflow/v1/tasks', taskData);
  }

  /**
   * Run a backtest task
   * @param {string} taskId - Task ID
   */
  async runTask(taskId) {
    return this.request('POST', `/aiflow/v1/tasks/${taskId}/run`);
  }

  /**
   * Get task result
   * @param {string} taskId - Task ID
   */
  async getTaskResult(taskId) {
    return this.request('GET', `/aiflow/v1/tasks/${taskId}/result`);
  }

  /**
   * Update task time
   * @param {string} taskId - Task ID
   */
  async updateTaskTime(taskId) {
    return this.request('GET', `/aiflow/v1/taskruns/update_time?task_id=${taskId}`);
  }

  // ==================== Strategy API ====================

  /**
   * List portfolio strategies
   */
  async listStrategies(options = {}) {
    const constraints = JSON.stringify({
      status__not_in: [2]
    });
    const params = new URLSearchParams({
      constraints,
      page: options.page || 1,
      size: options.size || 100
    });
    return this.request('GET', `/trading/v1/portfolio/strategies?${params}`);
  }

  /**
   * Get strategy details
   * @param {string} strategyId - Strategy ID
   */
  async getStrategy(strategyId) {
    return this.request('GET', `/trading/v1/portfolio/strategies/${strategyId}`);
  }

  // ==================== Module API ====================

  /**
   * Get available modules
   */
  async getModules() {
    return this.request('GET', '/module/v1/modules');
  }

  // ==================== Helper Methods ====================

  /**
   * Create and run a backtest
   * @param {Object} config - Backtest configuration
   * @param {string} config.code - Strategy code
   * @param {string} config.startDate - Start date (YYYY-MM-DD)
   * @param {string} config.endDate - End date (YYYY-MM-DD)
   * @param {number} config.capital - Initial capital
   */
  async runBacktest(config) {
    // Create task
    const taskData = {
      task_type: 'backtest',
      space_id: '00000000-0000-0000-0000-000000000000',
      data: {
        code: config.code,
        start_date: config.startDate || '2021-01-01',
        end_date: config.endDate || '2025-03-28',
        capital: config.capital || 100000,
        benchmark: config.benchmark || '000300.XSHG',
        frequency: config.frequency || 'day'
      }
    };

    const createResult = await this.createTask(taskData);

    if (!createResult.data?.id) {
      throw new Error('Failed to create task: ' + JSON.stringify(createResult));
    }

    const taskId = createResult.data.id;
    console.log('Created task:', taskId);

    // Run the task
    const runResult = await this.runTask(taskId);
    console.log('Task started');

    return {
      taskId,
      createResult,
      runResult
    };
  }

  /**
   * Wait for task completion
   * @param {string} taskId - Task ID
   * @param {number} timeoutMs - Timeout in milliseconds
   */
  async waitForTask(taskId, timeoutMs = 300000) {
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
      const task = await this.getTask(taskId);
      const status = task.data?.status;

      console.log(`Task ${taskId}: ${status}`);

      if (status === 'completed' || status === 'success') {
        return await this.getTaskResult(taskId);
      }

      if (status === 'failed' || status === 'error') {
        throw new Error(`Task failed: ${JSON.stringify(task)}`);
      }

      await new Promise(r => setTimeout(r, 5000));
    }

    throw new Error(`Task timeout after ${timeoutMs}ms`);
  }

  writeArtifact(baseName, data, extension = 'json') {
    const timestamp = Date.now();
    const filePath = path.join(this.outputRoot, `${baseName}-${timestamp}.${extension}`);
    ensureDir(filePath);
    const content = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    fs.writeFileSync(filePath, content, 'utf8');
    return filePath;
  }
}