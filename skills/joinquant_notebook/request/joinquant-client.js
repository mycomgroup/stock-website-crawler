import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';
const DEFAULT_ACCEPT = 'application/json, text/javascript, */*; q=0.01';

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

export function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

export function saveJson(filePath, data) {
  ensureDir(filePath);
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

export function resolveDirectNotebookUrl(inputUrl) {
  const parsed = new URL(inputUrl);
  const notebookPath = parsed.searchParams.get('url');
  if (notebookPath?.startsWith('/')) {
    return new URL(notebookPath, parsed.origin).toString();
  }
  return inputUrl;
}

function stripWrappedQuotes(value) {
  if (typeof value !== 'string') return value;
  return value.replace(/^"|"$/g, '');
}

function encodeNotebookPath(notebookPath) {
  return String(notebookPath)
    .split('/')
    .filter(Boolean)
    .map(segment => encodeURIComponent(segment))
    .join('/');
}

function normalizeCookieDomain(domain) {
  return String(domain || '').replace(/^\./, '');
}

function hostMatchesDomain(hostname, domain) {
  const normalizedDomain = normalizeCookieDomain(domain);
  return hostname === normalizedDomain || hostname.endsWith(`.${normalizedDomain}`);
}

function pathMatchesCookie(urlPath, cookiePath = '/') {
  return urlPath.startsWith(cookiePath);
}

function toOutputText(output) {
  if (!output) return '';
  if (output.output_type === 'stream') {
    return typeof output.text === 'string' ? output.text : String(output.text || '');
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
  return JSON.stringify(output);
}

export function createCodeCell(source) {
  return {
    metadata: { trusted: true },
    cell_type: 'code',
    source,
    execution_count: null,
    outputs: []
  };
}

export class JoinQuantClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.sessionPayload = options.sessionPayload || loadJson(this.sessionFile);

    const directNotebookUrl = options.notebookUrl
      ? resolveDirectNotebookUrl(options.notebookUrl)
      : this.sessionPayload.directNotebookUrl || resolveDirectNotebookUrl(this.sessionPayload.notebookUrl);
    this.directNotebookUrl = directNotebookUrl;

    const parsedNotebookUrl = new URL(directNotebookUrl);
    const pathParts = parsedNotebookUrl.pathname.split('/').filter(Boolean);
    if (pathParts.length < 4 || pathParts[0] !== 'user' || pathParts[2] !== 'notebooks') {
      throw new Error(`无法从 notebook URL 解析路径：${directNotebookUrl}`);
    }

    this.origin = parsedNotebookUrl.origin;
    this.userId = pathParts[1];
    this.notebookPath = decodeURIComponent(pathParts.slice(3).join('/'));
    this.baseUrl = this.sessionPayload.pageState?.notebook?.baseUrl || `/user/${this.userId}/`;
    this.cookieJar = this.sessionPayload.cookies || [];
    this.xsrfToken = stripWrappedQuotes(
      options.xsrfToken ||
      this.cookieJar.find(item => item.name === '_xsrf' && hostMatchesDomain('www.joinquant.com', item.domain))?.value
    );

    if (!this.xsrfToken) {
      throw new Error('会话中缺少 `_xsrf` cookie，请重新执行浏览器抓取脚本');
    }
  }

  buildUrl(relativeOrAbsoluteUrl) {
    if (/^https?:\/\//.test(relativeOrAbsoluteUrl)) {
      return relativeOrAbsoluteUrl;
    }
    return new URL(relativeOrAbsoluteUrl, this.origin).toString();
  }

  buildCookieHeader(requestUrl) {
    const parsed = new URL(requestUrl);
    const matched = this.cookieJar.filter(cookie => {
      if (!cookie?.name) return false;
      if (!hostMatchesDomain(parsed.hostname, cookie.domain)) return false;
      if (!pathMatchesCookie(parsed.pathname, cookie.path || '/')) return false;
      return true;
    });

    return matched
      .map(cookie => `${cookie.name}=${stripWrappedQuotes(cookie.value)}`)
      .join('; ');
  }

  buildHeaders(requestUrl, overrides = {}) {
    const headers = {
      accept: DEFAULT_ACCEPT,
      'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'user-agent': USER_AGENT,
      'x-requested-with': 'XMLHttpRequest',
      'x-xsrftoken': this.xsrfToken,
      cookie: this.buildCookieHeader(requestUrl),
      referer: this.directNotebookUrl,
      ...overrides
    };

    Object.keys(headers).forEach(key => {
      if (headers[key] == null || headers[key] === '') {
        delete headers[key];
      }
    });

    return headers;
  }

  async requestJson(requestUrl, options = {}) {
    const url = this.buildUrl(requestUrl);
    const body = options.body == null || typeof options.body === 'string'
      ? options.body
      : JSON.stringify(options.body);

    const response = await fetch(url, {
      method: options.method || 'GET',
      headers: this.buildHeaders(url, {
        ...(body ? { 'content-type': 'application/json' } : {}),
        ...(options.headers || {})
      }),
      body
    });

    const text = await response.text();
    if (!response.ok) {
      throw new Error(`请求失败 ${response.status} ${url}: ${text.slice(0, 500)}`);
    }

    const contentType = response.headers.get('content-type') || '';
    if (!/json/i.test(contentType)) {
      throw new Error(`接口未返回 JSON ${url}: ${text.slice(0, 200)}`);
    }

    return {
      data: text ? JSON.parse(text) : null,
      response,
      text,
      url
    };
  }

  get apiRoot() {
    return `${this.origin}${this.baseUrl}api/`;
  }

  buildApiUrl(resourcePath, query = null) {
    const url = new URL(resourcePath.replace(/^\//, ''), this.apiRoot);
    if (query) {
      Object.entries(query).forEach(([key, value]) => {
        if (value != null) {
          url.searchParams.set(key, String(value));
        }
      });
    }
    return url.toString();
  }

  async getNotebookModel(options = {}) {
    const url = this.buildApiUrl(`contents/${encodeNotebookPath(options.notebookPath || this.notebookPath)}`, {
      type: 'notebook',
      _: Date.now()
    });
    const result = await this.requestJson(url);
    return result.data;
  }

  async getNotebookMetadata(options = {}) {
    const url = this.buildApiUrl(`contents/${encodeNotebookPath(options.notebookPath || this.notebookPath)}`, {
      content: 0,
      _: Date.now()
    });
    const result = await this.requestJson(url, {
      headers: { accept: '*/*' }
    });
    return result.data;
  }

  async saveNotebook(notebookContent, options = {}) {
    const url = this.buildApiUrl(`contents/${encodeNotebookPath(options.notebookPath || this.notebookPath)}`);
    const result = await this.requestJson(url, {
      method: 'PUT',
      body: {
        type: 'notebook',
        content: notebookContent
      }
    });
    return result.data;
  }

  async createNotebook(options = {}) {
    const notebookPath = options.notebookPath || this.notebookPath;
    const url = this.buildApiUrl(`contents/${encodeNotebookPath(notebookPath)}`, { _: Date.now() });
    
    const emptyNotebook = {
      metadata: {
        kernelspec: {
          display_name: 'Python 3',
          language: 'python',
          name: options.kernelName || 'python3'
        },
        language_info: {
          codemirror_mode: {
            name: 'ipython',
            version: 3
          },
          file_extension: '.py',
          mimetype: 'text/x-python',
          name: 'python',
          nbconvert_exporter: 'python',
          pygments_lexer: 'ipython3',
          version: '3.8.0'
        }
      },
      nbformat: 4,
      nbformat_minor: 4,
      cells: []
    };

    const result = await this.requestJson(url, {
      method: 'PUT',
      body: {
        type: 'notebook',
        content: emptyNotebook
      }
    });
    
    return {
      notebookPath,
      notebookUrl: `${this.origin}${this.baseUrl}notebooks/${encodeNotebookPath(notebookPath)}`,
      ...result.data
    };
  }

  async deleteNotebook(options = {}) {
    const notebookPath = options.notebookPath || this.notebookPath;
    const url = this.buildApiUrl(`contents/${encodeNotebookPath(notebookPath)}`, { _: Date.now() });
    
    try {
      const result = await this.requestJson(url, {
        method: 'DELETE'
      });
      return { success: true, notebookPath };
    } catch (error) {
      return { success: false, notebookPath, error: error.message };
    }
  }

  generateUniqueNotebookName(baseName = 'strategy_run') {
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
    const timeStr = now.toTimeString().slice(0, 8).replace(/:/g, '');
    return `${baseName}_${dateStr}_${timeStr}.ipynb`;
  }

  async ensureSession(options = {}) {
    const url = this.buildApiUrl('sessions');
    const kernelName = options.kernelName || 'python3';
    const notebookPath = options.notebookPath || this.notebookPath;
    const result = await this.requestJson(url, {
      method: 'POST',
      body: {
        path: notebookPath,
        type: 'notebook',
        name: '',
        kernel: {
          id: null,
          name: kernelName
        }
      }
    });
    return result.data;
  }

  async listSessions() {
    const url = this.buildApiUrl('sessions', { _: Date.now() });
    const result = await this.requestJson(url);
    return result.data || [];
  }

  async deleteSession(sessionId) {
    const url = this.buildApiUrl(`sessions/${sessionId}`);
    try {
      await this.requestJson(url, {
        method: 'DELETE',
        headers: { accept: '*/*' }
      });
      return { success: true, sessionId };
    } catch (error) {
      return { success: false, sessionId, error: error.message };
    }
  }

  buildChannelsUrl(kernelId, websocketSessionId) {
    return `${this.origin}${this.baseUrl}api/kernels/${kernelId}/channels?session_id=${websocketSessionId}`;
  }

  createExecuteRequest(code, websocketSessionId, msgId) {
    return JSON.stringify({
      header: {
        msg_id: msgId,
        username: 'username',
        session: websocketSessionId,
        msg_type: 'execute_request',
        version: '5.2'
      },
      metadata: {},
      content: {
        code,
        silent: false,
        store_history: true,
        user_expressions: {},
        allow_stdin: true,
        stop_on_error: true
      },
      buffers: [],
      parent_header: {},
      channel: 'shell'
    });
  }

  async executeCode(options) {
    const { kernelId, code, timeoutMs = 30000 } = options;
    if (!kernelId) {
      throw new Error('executeCode 缺少 kernelId');
    }

    const websocketSessionId = crypto.randomUUID().replace(/-/g, '');
    const msgId = crypto.randomUUID().replace(/-/g, '');
    const wsUrl = this.buildChannelsUrl(kernelId, websocketSessionId);
    const outputs = [];

    return new Promise((resolve, reject) => {
      let reply = null;
      let executionCount = null;
      let idleReceived = false;
      let settled = false;
      const rawMessages = [];
      const socket = new WebSocket(wsUrl, {
        headers: this.buildHeaders(wsUrl, {
          origin: this.origin,
          referer: this.directNotebookUrl
        })
      });

      const finalize = result => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        socket.close();
        resolve({
          msgId,
          websocketSessionId,
          kernelId,
          code,
          executionCount,
          outputs,
          reply,
          rawMessages,
          textOutput: outputs.map(toOutputText).filter(Boolean).join('')
        });
      };

      const fail = error => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        socket.close();
        reject(error);
      };

      const maybeFinalize = () => {
        if (idleReceived && reply) {
          finalize(reply);
        }
      };

      const timer = setTimeout(() => {
        fail(new Error(`执行超时：${timeoutMs}ms`));
      }, timeoutMs);

      socket.addEventListener('open', () => {
        socket.send(this.createExecuteRequest(code, websocketSessionId, msgId));
      });

      socket.addEventListener('message', event => {
        const text = typeof event.data === 'string' ? event.data : String(event.data);
        let message;
        try {
          message = JSON.parse(text);
        } catch {
          return;
        }

        if (message?.parent_header?.msg_id !== msgId) {
          return;
        }

        rawMessages.push(message);

        switch (message.msg_type) {
          case 'execute_input':
            executionCount = message.content?.execution_count ?? executionCount;
            break;
          case 'stream':
            outputs.push({
              output_type: 'stream',
              name: message.content?.name || 'stdout',
              text: message.content?.text || ''
            });
            break;
          case 'display_data':
          case 'update_display_data':
            outputs.push({
              output_type: 'display_data',
              data: message.content?.data || {},
              metadata: message.content?.metadata || {}
            });
            break;
          case 'execute_result':
            outputs.push({
              output_type: 'execute_result',
              execution_count: message.content?.execution_count ?? executionCount,
              data: message.content?.data || {},
              metadata: message.content?.metadata || {}
            });
            break;
          case 'error':
            outputs.push({
              output_type: 'error',
              ename: message.content?.ename || 'Error',
              evalue: message.content?.evalue || '',
              traceback: message.content?.traceback || []
            });
            break;
          case 'clear_output':
            outputs.length = 0;
            break;
          case 'execute_reply':
            reply = message.content || { status: 'ok' };
            executionCount = message.content?.execution_count ?? executionCount;
            maybeFinalize();
            break;
          case 'status':
            if (message.content?.execution_state === 'idle') {
              idleReceived = true;
              maybeFinalize();
            }
            break;
          default:
            break;
        }
      });

      socket.addEventListener('error', event => {
        const errMsg = event.message || `WebSocket 执行失败：${wsUrl}`;
        if (!settled) {
          fail(new Error(errMsg));
        } else {
          console.warn(`WebSocket error after settled: ${errMsg}`);
        }
      });

      socket.addEventListener('close', event => {
        if (!settled) {
          fail(new Error(`WebSocket 在执行完成前关闭: code=${event.code}, reason=${event.reason || 'unknown'}`));
        } else if (idleReceived && reply) {
          maybeFinalize();
        }
      });
    });
  }

  writeArtifact(baseName, data, extension = 'json') {
    const timestamp = Date.now();
    const filePath = path.join(this.outputRoot, `${baseName}-${timestamp}.${extension}`);
    ensureDir(filePath);
    const content = (extension === 'json' || extension === 'ipynb')
      ? JSON.stringify(data, null, 2)
      : String(data);
    fs.writeFileSync(filePath, content, 'utf8');
    return filePath;
  }
}
