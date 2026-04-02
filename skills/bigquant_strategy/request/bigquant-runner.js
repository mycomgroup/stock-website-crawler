/**
 * BigQuant 策略运行器 - 纯 HTTP 实现
 *
 * 核心思路：
 * BigQuant AIStudio 是 VS Code Web + Jupyter kernel。
 * 执行路径：创建 task → 激活 studio instance → 通过 Jupyter HTTP API 执行 notebook cell
 *
 * Jupyter REST API (code-server 内置):
 *   POST /aistudio/studios/{id}/api/kernels          创建 kernel
 *   GET  /aistudio/studios/{id}/api/kernels           列出 kernels
 *   POST /aistudio/studios/{id}/api/kernels/{kid}/restart  重启
 *   WS   /aistudio/studios/{id}/api/kernels/{kid}/channels  执行通道
 *   POST /aistudio/studios/{id}/api/sessions          创建 session（绑定 notebook）
 *   GET  /aistudio/studios/{id}/api/contents/{path}   读取文件
 *   PUT  /aistudio/studios/{id}/api/contents/{path}   写入文件
 */

import fs from 'node:fs';
import path from 'node:path';
import { WebSocket } from 'ws';
import '../load-env.js';
import { OUTPUT_ROOT } from '../paths.js';
import { extractUserId } from './bigquant-auth.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';
const ORIGIN = 'https://bigquant.com';

function ensureDir(p) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
}

export class BigQuantRunner {
  constructor(session) {
    this.session = session;
    this.cookieHeader = session.cookies
      .filter(c => c.domain.includes('bigquant.com'))
      .map(c => `${c.name}=${c.value}`)
      .join('; ');
    this.userId = extractUserId(session);
    this.studioId = process.env.BIGQUANT_STUDIO_ID || this.userId || 'e6277718-0f37-11ed-93bb-da75731aa77c';
    this.outputRoot = OUTPUT_ROOT;
  }

  buildHeaders(extra = {}) {
    return {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, */*',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Referer': `${ORIGIN}/aistudio/studios/${this.studioId}/`,
      'Origin': ORIGIN,
      'Cookie': this.cookieHeader,
      ...extra
    };
  }

  async request(method, url, body = null, extraHeaders = {}) {
    const fullUrl = url.startsWith('http') ? url : `${ORIGIN}${url}`;
    const opts = {
      method,
      headers: this.buildHeaders({
        'Content-Type': 'application/json',
        ...extraHeaders
      })
    };
    if (body !== null) opts.body = JSON.stringify(body);

    const resp = await fetch(fullUrl, opts);
    const text = await resp.text();

    if (!resp.ok) {
      throw new Error(`HTTP ${resp.status} ${method} ${fullUrl}: ${text.slice(0, 300)}`);
    }
    try { return JSON.parse(text); } catch { return text; }
  }

  // ── AIFlow Task API ──────────────────────────────────────────────

  async createTask(name, notebookJson, config = {}) {
    const userId = this.userId;
    return this.request('POST', '/bigapis/aiflow/v1/tasks', {
      space_id: '00000000-0000-0000-0000-000000000000',
      creator: userId,
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
        resource_options: {
          id: 'a059c996-0938-4726-ab6d-97b7e6cb2de5',
          cpu: 1, gpu: 0, memory: 4
        },
        task_tune_parameters: []
      },
      data: { code: JSON.stringify(notebookJson) },
      priority: 10,
      deployment_id: '00000000-0000-0000-0000-000000000000',
      strategy_type: 0
    });
  }

  async updateTaskCode(taskId, notebookJson) {
    return this.request('PATCH', `/bigapis/aiflow/v1/tasks/${taskId}`, {
      code: JSON.stringify(notebookJson)
    });
  }

  async getTask(taskId) {
    return this.request('GET', `/bigapis/aiflow/v1/tasks/${taskId}`);
  }

  async listTasks(size = 50) {
    const userId = this.userId;
    const constraints = encodeURIComponent(JSON.stringify({
      space_id: '00000000-0000-0000-0000-000000000000',
      creator: userId
    }));
    return this.request('GET', `/bigapis/aiflow/v1/tasks?constraints=${constraints}&page=1&size=${size}&exclude_fields=data&order_by=-created_at`);
  }

  // ── Studio Instance API ──────────────────────────────────────────

  async activateStudio() {
    console.log('[Runner] 激活 Studio instance...');
    try {
      const result = await this.request('POST', `/bigapis/aistudio/v1/studios/${this.studioId}/instances`, {
        resource_spec_id: 'a059c996-0938-4726-ab6d-97b7e6cb2de5',
        survival_time: 120
      });
      console.log('[Runner] Studio 激活:', result?.data?.status || JSON.stringify(result).slice(0, 100));
      return result;
    } catch (e) {
      console.log('[Runner] Studio 激活失败（可能已激活）:', e.message.slice(0, 100));
    }
  }

  // ── Jupyter REST API (通过 AIStudio 代理) ────────────────────────

  jupyterUrl(path) {
    return `${ORIGIN}/aistudio/studios/${this.studioId}${path}`;
  }

  async jupyterRequest(method, path, body = null) {
    const url = this.jupyterUrl(path);
    const opts = {
      method,
      headers: this.buildHeaders({
        'Content-Type': 'application/json',
        'X-XSRFToken': this._xsrf || ''
      })
    };
    if (body !== null) opts.body = JSON.stringify(body);

    const resp = await fetch(url, opts);
    const text = await resp.text();

    if (!resp.ok) {
      throw new Error(`Jupyter HTTP ${resp.status} ${method} ${path}: ${text.slice(0, 300)}`);
    }
    try { return JSON.parse(text); } catch { return text; }
  }

  async getJupyterXSRF() {
    // 获取 Jupyter XSRF token
    try {
      const resp = await fetch(this.jupyterUrl('/api/kernels'), {
        headers: this.buildHeaders()
      });
      const xsrf = resp.headers.get('set-cookie')?.match(/_xsrf=([^;]+)/)?.[1];
      if (xsrf) this._xsrf = xsrf;
      return xsrf;
    } catch (e) {
      return null;
    }
  }

  async listKernels() {
    return this.jupyterRequest('GET', '/api/kernels');
  }

  async createKernel(kernelName = 'python3') {
    return this.jupyterRequest('POST', '/api/kernels', { name: kernelName });
  }

  async deleteKernel(kernelId) {
    return this.jupyterRequest('DELETE', `/api/kernels/${kernelId}`);
  }

  async listSessions() {
    return this.jupyterRequest('GET', '/api/sessions');
  }

  async createSession(notebookPath, kernelName = 'python3') {
    return this.jupyterRequest('POST', '/api/sessions', {
      path: notebookPath,
      type: 'notebook',
      name: notebookPath,
      kernel: { name: kernelName }
    });
  }

  async readContents(filePath) {
    return this.jupyterRequest('GET', `/api/contents/${encodeURIComponent(filePath)}`);
  }

  async writeContents(filePath, notebookJson) {
    return this.jupyterRequest('PUT', `/api/contents/${encodeURIComponent(filePath)}`, {
      type: 'notebook',
      format: 'json',
      content: notebookJson
    });
  }

  // ── Kernel WebSocket 执行 ────────────────────────────────────────

  /**
   * 通过 WebSocket 向 kernel 发送代码并等待执行完成
   * 使用标准 Jupyter messaging protocol
   */
  async executeViaKernel(kernelId, code, timeoutMs = 300000) {
    const wsUrl = `wss://bigquant.com/aistudio/studios/${this.studioId}/api/kernels/${kernelId}/channels`;
    const msgId = `msg_${Date.now()}_${Math.random().toString(36).slice(2)}`;

    return new Promise((resolve, reject) => {
      const ws = new WebSocket(wsUrl, {
        headers: {
          'Cookie': this.cookieHeader,
          'User-Agent': USER_AGENT,
          'Origin': ORIGIN
        }
      });

      const outputs = [];
      let status = 'idle';
      const timer = setTimeout(() => {
        ws.close();
        reject(new Error(`Kernel 执行超时 (${timeoutMs}ms)`));
      }, timeoutMs);

      ws.on('open', () => {
        console.log('[Kernel] WebSocket 已连接');

        // 发送 execute_request
        const msg = {
          header: {
            msg_id: msgId,
            msg_type: 'execute_request',
            username: this.session.username || 'user',
            session: msgId,
            date: new Date().toISOString(),
            version: '5.3'
          },
          parent_header: {},
          metadata: {},
          content: {
            code,
            silent: false,
            store_history: true,
            user_expressions: {},
            allow_stdin: false,
            stop_on_error: true
          },
          channel: 'shell',
          buffers: []
        };

        ws.send(JSON.stringify(msg));
        console.log('[Kernel] 已发送 execute_request');
      });

      ws.on('message', (data) => {
        let msg;
        try { msg = JSON.parse(data.toString()); } catch { return; }

        const msgType = msg.header?.msg_type;
        const parentId = msg.parent_header?.msg_id;

        if (parentId !== msgId && msgType !== 'status') return;

        switch (msgType) {
          case 'stream':
            outputs.push({ type: 'stream', name: msg.content?.name, text: msg.content?.text });
            process.stdout.write(msg.content?.text || '');
            break;

          case 'display_data':
          case 'execute_result':
            outputs.push({ type: msgType, data: msg.content?.data });
            break;

          case 'error':
            outputs.push({ type: 'error', ename: msg.content?.ename, evalue: msg.content?.evalue, traceback: msg.content?.traceback });
            console.error(`[Kernel] 错误: ${msg.content?.ename}: ${msg.content?.evalue}`);
            break;

          case 'status':
            status = msg.content?.execution_state;
            if (status === 'idle' && parentId === msgId) {
              clearTimeout(timer);
              ws.close();
              resolve({ outputs, status: 'success' });
            }
            break;

          case 'execute_reply':
            if (msg.content?.status === 'error') {
              clearTimeout(timer);
              ws.close();
              resolve({ outputs, status: 'error', error: msg.content });
            }
            break;
        }
      });

      ws.on('error', (err) => {
        clearTimeout(timer);
        reject(new Error(`WebSocket 错误: ${err.message}`));
      });

      ws.on('close', (code, reason) => {
        clearTimeout(timer);
        if (outputs.length > 0 || status === 'idle') {
          resolve({ outputs, status: 'closed' });
        } else {
          reject(new Error(`WebSocket 意外关闭: ${code} ${reason}`));
        }
      });
    });
  }

  // ── 完整工作流 ───────────────────────────────────────────────────

  /**
   * 主工作流：上传代码 → 执行 → 获取结果
   */
  async runStrategy(name, code, config = {}) {
    console.log('\n' + '='.repeat(60));
    console.log('BigQuant 策略运行器 (纯 HTTP)');
    console.log('='.repeat(60));

    const notebookJson = this.buildNotebook(code, config);

    // Step 1: 激活 Studio
    await this.activateStudio();
    await this.sleep(2000);

    // Step 2: 尝试 Jupyter API
    console.log('\n[Step 2] 探测 Jupyter API...');
    const jupyterAvailable = await this.probeJupyterAPI();

    if (jupyterAvailable) {
      return await this.runViaJupyter(name, code, notebookJson, config);
    }

    // Step 3: 回退到 AIFlow task + 轮询
    console.log('\n[Step 3] Jupyter 不可用，使用 AIFlow task 模式...');
    return await this.runViaAIFlow(name, notebookJson, config);
  }

  async probeJupyterAPI() {
    try {
      await this.getJupyterXSRF();
      const kernels = await this.listKernels();
      console.log('[Jupyter] API 可用，当前 kernels:', Array.isArray(kernels) ? kernels.length : 'unknown');
      return true;
    } catch (e) {
      console.log('[Jupyter] API 不可用:', e.message.slice(0, 100));
      return false;
    }
  }

  async runViaJupyter(name, code, notebookJson, config) {
    console.log('\n[Jupyter] 开始执行...');

    // 写入 notebook 文件
    const notebookPath = `work/${name}.ipynb`;
    try {
      await this.writeContents(notebookPath, notebookJson);
      console.log(`[Jupyter] 已写入: ${notebookPath}`);
    } catch (e) {
      console.log('[Jupyter] 写入失败，尝试直接执行:', e.message.slice(0, 100));
    }

    // 获取或创建 kernel
    let kernelId;
    const kernels = await this.listKernels();
    if (Array.isArray(kernels) && kernels.length > 0) {
      kernelId = kernels[0].id;
      console.log('[Jupyter] 复用 kernel:', kernelId);
    } else {
      const kernel = await this.createKernel('python3');
      kernelId = kernel.id;
      console.log('[Jupyter] 创建 kernel:', kernelId);
      await this.sleep(3000); // 等待 kernel 启动
    }

    // 执行代码
    console.log('[Jupyter] 执行代码...');
    const result = await this.executeViaKernel(kernelId, code);

    // 保存结果
    const report = this.extractReport(result.outputs, config);
    const outputPath = this.writeArtifact(`bigquant-result-${name}`, report);

    console.log('\n' + '='.repeat(60));
    console.log('执行完成');
    this.printSummary(report);
    console.log('结果已保存:', outputPath);

    return { success: true, outputs: result.outputs, report, outputPath };
  }

  async runViaAIFlow(name, notebookJson, config) {
    // 创建 task
    console.log('[AIFlow] 创建 task...');
    const createResult = await this.createTask(name, notebookJson, config);
    const taskId = createResult.data?.id;

    if (!taskId) {
      throw new Error('创建 task 失败: ' + JSON.stringify(createResult));
    }
    console.log('[AIFlow] Task ID:', taskId);

    // 创建 taskrun
    const event = new Date().toISOString().split('T')[0].replace(/-/g, '');
    const runResult = await this.request('POST', '/bigapis/aiflow/v1/taskruns', {
      task_id: taskId,
      state: 'pending',
      event
    });
    const taskrunId = runResult.data?.id;
    console.log('[AIFlow] Taskrun ID:', taskrunId);

    // 轮询状态
    console.log('[AIFlow] 等待执行...');
    const studioUrl = `https://bigquant.com/aistudio/studios/${this.studioId}/?task=${taskId}`;
    console.log('[AIFlow] Web URL:', studioUrl);

    const result = await this.pollTaskCompletion(taskId, 300000);

    const outputPath = this.writeArtifact(`bigquant-aiflow-${taskId}`, {
      taskId, taskrunId, result, config,
      webUrl: studioUrl
    });

    return { success: result.success, taskId, taskrunId, result, outputPath, webUrl: studioUrl };
  }

  async pollTaskCompletion(taskId, timeoutMs = 300000) {
    const start = Date.now();
    let attempts = 0;

    while (Date.now() - start < timeoutMs) {
      await this.sleep(5000);
      attempts++;

      const task = await this.getTask(taskId);
      const lastRun = task.data?.last_run;
      const state = lastRun?.state;

      process.stdout.write(`\r[AIFlow] [${attempts}] 状态: ${state || 'pending'}...`);

      if (state === 'success') {
        console.log('\n[AIFlow] 执行成功!');
        // 尝试读取 notebook outputs
        const outputs = await this.readTaskOutputs(taskId);
        return { success: true, state, outputs };
      }

      if (state === 'failed' || state === 'error') {
        console.log('\n[AIFlow] 执行失败:', state);
        return { success: false, state };
      }
    }

    console.log('\n[AIFlow] 超时');
    return { success: false, state: 'timeout' };
  }

  async readTaskOutputs(taskId) {
    try {
      const task = await this.getTask(taskId);
      const codeStr = task.data?.data?.code;
      if (!codeStr) return [];

      const notebook = JSON.parse(codeStr);
      const outputs = [];
      for (const cell of notebook.cells || []) {
        for (const output of cell.outputs || []) {
          outputs.push(output);
        }
      }
      return outputs;
    } catch (e) {
      return [];
    }
  }

  // ── 工具方法 ─────────────────────────────────────────────────────

  buildNotebook(code, config = {}) {
    // 注入回测参数到代码头部
    const paramHeader = config.startDate ? [
      `# BigQuant 回测参数 (自动注入)`,
      `import os`,
      `os.environ.setdefault('BQ_START_DATE', '${config.startDate || '2023-01-01'}')`,
      `os.environ.setdefault('BQ_END_DATE', '${config.endDate || '2023-12-31'}')`,
      `os.environ.setdefault('BQ_CAPITAL', '${config.capital || 100000}')`,
      ``
    ].join('\n') : '';

    const fullCode = paramHeader + code;

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
        source: fullCode.split('\n').map((l, i, a) => i < a.length - 1 ? l + '\n' : l)
      }]
    };
  }

  extractReport(outputs, config) {
    const stdout = outputs
      .filter(o => o.type === 'stream' && o.name === 'stdout')
      .map(o => o.text)
      .join('');

    const errors = outputs
      .filter(o => o.type === 'error')
      .map(o => `${o.ename}: ${o.evalue}`)
      .join('\n');

    // 尝试从输出中提取回测指标
    const metrics = {};
    const patterns = {
      totalReturn: /总收益[率:]?\s*([-\d.]+)%?/,
      annualReturn: /年化收益[率:]?\s*([-\d.]+)%?/,
      maxDrawdown: /最大回撤[率:]?\s*([-\d.]+)%?/,
      sharpe: /夏普[比率:]?\s*([-\d.]+)/,
      alpha: /alpha[:\s]+([-\d.]+)/i,
      beta: /beta[:\s]+([-\d.]+)/i
    };

    for (const [key, pattern] of Object.entries(patterns)) {
      const m = stdout.match(pattern);
      if (m) metrics[key] = parseFloat(m[1]);
    }

    return {
      config,
      stdout,
      errors,
      metrics,
      outputs,
      timestamp: new Date().toISOString()
    };
  }

  printSummary(report) {
    if (report.errors) {
      console.log('错误:', report.errors.slice(0, 200));
    }
    if (Object.keys(report.metrics).length > 0) {
      console.log('回测指标:');
      for (const [k, v] of Object.entries(report.metrics)) {
        console.log(`  ${k}: ${v}`);
      }
    }
    if (report.stdout) {
      console.log('输出 (前500字符):');
      console.log(report.stdout.slice(0, 500));
    }
  }

  writeArtifact(name, data) {
    const filePath = path.join(this.outputRoot, `${name}-${Date.now()}.json`);
    ensureDir(filePath);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    return filePath;
  }

  sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
  }
}
