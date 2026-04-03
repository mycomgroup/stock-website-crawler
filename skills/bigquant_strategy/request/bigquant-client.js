/**
 * BigQuant Notebook Client
 * 对齐 joinquant_notebook 的接口风格
 *
 * 核心 API（从 aiflow-aistudio-extension 源码逆向）：
 *   POST /bigapis/aistudio/v1/studios/{id}/instances  激活 Studio
 *   GET  /bigapis/aiflow/v1/resourcespecs             查询可用资源（过滤 usable:true）
 *   POST /bigapis/aiflow/v1/tasks                     创建 task
 *   POST /bigapis/aiflow/v1/taskruns {state:"trigger"} 触发执行
 *   GET  /bigapis/aiflow/v1/logs/{runId}              读取日志
 *   GET  /bigapis/aiflow/v1/tasks/{taskId}            读取 notebook outputs
 */

import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { OUTPUT_ROOT } from '../paths.js';
import { extractUserId } from './bigquant-auth.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';
const ORIGIN = 'https://bigquant.com';

function ensureDir(p) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
}

function toOutputText(output) {
  if (!output) return '';
  if (output.output_type === 'stream') {
    return Array.isArray(output.text) ? output.text.join('') : String(output.text || '');
  }
  if (output.output_type === 'error') {
    return `${output.ename || 'Error'}: ${output.evalue || ''}`.trim();
  }
  if (output.output_type === 'execute_result' || output.output_type === 'display_data') {
    if (output.data?.['text/plain']) {
      return Array.isArray(output.data['text/plain'])
        ? output.data['text/plain'].join('')
        : String(output.data['text/plain']);
    }
    return JSON.stringify(output.data || {});
  }
  return '';
}

export class BigQuantClient {
  constructor(session, options = {}) {
    this.session = session;
    this.cookieHeader = session.cookies
      .filter(c => c.domain.includes('bigquant.com'))
      .map(c => `${c.name}=${c.value}`)
      .join('; ');
    this.userId = extractUserId(session);
    this.studioId = options.studioId || process.env.BIGQUANT_STUDIO_ID || this.userId;
    this.outputRoot = options.outputRoot || OUTPUT_ROOT;
    this._resourceSpecId = options.resourceSpecId || process.env.BIGQUANT_RESOURCE_SPEC_ID || null;
  }

  // ── HTTP 基础 ────────────────────────────────────────────────────

  buildHeaders(extra = {}) {
    return {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, */*',
      'Content-Type': 'application/json',
      'Cookie': this.cookieHeader,
      ...extra
    };
  }

  async request(method, url, body = null) {
    const fullUrl = url.startsWith('http') ? url : `${ORIGIN}${url}`;
    const opts = { method, headers: this.buildHeaders() };
    if (body !== null) opts.body = JSON.stringify(body);
    const resp = await fetch(fullUrl, opts);
    const text = await resp.text();
    if (!resp.ok) throw new Error(`HTTP ${resp.status} ${method} ${fullUrl}: ${text.slice(0, 300)}`);
    try { return JSON.parse(text); } catch { return text; }
  }

  // ── 资源规格 ─────────────────────────────────────────────────────

  /**
   * 查询可用资源规格，自动选择 usable:true 的免费资源
   * 对应扩展源码: filter(e => e.usable)
   */
  async getUsableResourceSpec() {
    if (this._resourceSpecId) return this._resourceSpecId;

    const result = await this.request('GET', '/bigapis/aiflow/v1/resourcespecs');
    const specs = result.data || [];

    // 优先选 usable:true 的
    const usable = specs.filter(s => s.usable);
    if (usable.length > 0) {
      const spec = usable[0];
      console.log(`[Resource] 使用资源: ${spec.name} (${spec.id})`);
      this._resourceSpecId = spec.id;
      return spec.id;
    }

    // 没有 usable 的，用 userresourcespecs 的默认值
    const userSpec = await this.request('GET', '/bigapis/aistudio/v1/userresourcespecs');
    const specId = userSpec.data?.id;
    if (specId) {
      console.log(`[Resource] 使用用户默认资源: ${userSpec.data?.name} (${specId})`);
      this._resourceSpecId = specId;
      return specId;
    }

    throw new Error('没有可用的资源规格，请在 BigQuant 页面手动选择一个免费资源后重试');
  }

  // ── Studio ───────────────────────────────────────────────────────

  async activateStudio() {
    try {
      const result = await this.request('POST', `/bigapis/aistudio/v1/studios/${this.studioId}/instances`, {
        aistudio_version: 300
      });
      const status = result?.data?.status;
      console.log(`[Studio] 状态: ${status}`);
      return status;
    } catch (e) {
      console.log('[Studio] 激活失败（可能已激活）:', e.message.slice(0, 80));
    }
  }

  // ── Task ─────────────────────────────────────────────────────────

  async createTask(name, notebookJson, config = {}) {
    const resourceSpecId = await this.getUsableResourceSpec();

    const result = await this.request('POST', '/bigapis/aiflow/v1/tasks', {
      space_id: '00000000-0000-0000-0000-000000000000',
      creator: this.userId,
      name,
      task_type: 'run_once',
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
            start_date: config.startDate || '2023-01-01',
            end_date: config.endDate || '2023-12-31',
            benchmark: config.benchmark || '000300.XSHG',
            frequency: config.frequency || 'day'
          }
        },
        retries: 0,
        resource_options: { id: resourceSpecId, cpu: 1, gpu: 0, memory: 6 },
        task_tune_parameters: []
      },
      data: { code: JSON.stringify(notebookJson) },
      priority: 10,
      deployment_id: '00000000-0000-0000-0000-000000000000',
      strategy_type: 0
    });

    const taskId = result.data?.id;
    if (!taskId) throw new Error('创建 task 失败: ' + JSON.stringify(result));
    return taskId;
  }

  async getTask(taskId) {
    return this.request('GET', `/bigapis/aiflow/v1/tasks/${taskId}`);
  }

  async listTasks(options = {}) {
    const constraints = encodeURIComponent(JSON.stringify({
      space_id: '00000000-0000-0000-0000-000000000000',
      creator: this.userId
    }));
    const size = options.size || 50;
    return this.request('GET', `/bigapis/aiflow/v1/tasks?constraints=${constraints}&page=1&size=${size}&exclude_fields=data&order_by=-created_at`);
  }

  // ── TaskRun ──────────────────────────────────────────────────────

  /**
   * 触发执行 — state:"trigger" 是关键
   */
  async triggerTask(taskId) {
    const result = await this.request('POST', '/bigapis/aiflow/v1/taskruns', {
      task_id: taskId,
      state: 'trigger',
      queue: 'manual'
    });
    const runId = result.data?.id;
    if (!runId) throw new Error('触发失败: ' + JSON.stringify(result));
    return runId;
  }

  // ── 日志 ─────────────────────────────────────────────────────────

  async getLogs(runId, count = 200) {
    const result = await this.request('GET', `/bigapis/aiflow/v1/logs/${runId}?count=${count}`);
    return result.data?.logs || [];
  }

  // ── Notebook Outputs ─────────────────────────────────────────────

  async getNotebookOutputs(taskId) {
    const task = await this.getTask(taskId);
    const codeStr = task.data?.data?.code;
    if (!codeStr) return [];
    try {
      const notebook = JSON.parse(codeStr);
      return (notebook.cells || []).flatMap(cell => cell.outputs || []);
    } catch { return []; }
  }

  // ── 轮询 ─────────────────────────────────────────────────────────

  async waitForCompletion(taskId, timeoutMs = 300000) {
    const start = Date.now();
    let attempts = 0;

    while (Date.now() - start < timeoutMs) {
      await this.sleep(3000);
      attempts++;

      const task = await this.getTask(taskId);
      const state = task.data?.last_run?.state;
      process.stdout.write(`\r    [${attempts}] 状态: ${state || 'unknown'}...`);

      if (state === 'completed' || state === 'success') {
        console.log('\n    ✓ 执行成功!');
        return { success: true, state };
      }
      if (state === 'failed' || state === 'error') {
        console.log(`\n    ✗ 执行失败: ${state}`);
        return { success: false, state };
      }
    }

    console.log('\n    ⚠ 超时');
    return { success: false, state: 'timeout' };
  }

  // ── Notebook 构建 ────────────────────────────────────────────────

  buildNotebook(code) {
    return {
      metadata: {
        kernelspec: { display_name: 'Python 3', language: 'python', name: 'python3' },
        language_info: { name: 'python', version: '3.8.0' }
      },
      nbformat: 4,
      nbformat_minor: 4,
      cells: [{
        cell_type: 'code',
        execution_count: null,
        metadata: {},
        outputs: [],
        source: code.split('\n').map((l, i, a) => i < a.length - 1 ? l + '\n' : l)
      }]
    };
  }

  // ── 工具 ─────────────────────────────────────────────────────────

  writeArtifact(baseName, data, extension = 'json') {
    const filePath = path.join(this.outputRoot, `${baseName}-${Date.now()}.${extension}`);
    ensureDir(filePath);
    const content = extension === 'json' ? JSON.stringify(data, null, 2) : String(data);
    fs.writeFileSync(filePath, content, 'utf8');
    return filePath;
  }

  sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
}
