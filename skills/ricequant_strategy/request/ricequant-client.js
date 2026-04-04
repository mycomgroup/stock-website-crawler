import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

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

/**
 * 根据 HTTP 状态码决定重试等待时间
 * - 429 / 503 并发限制：60s / 120s / 300s
 * - 其他 5xx 服务端错误：10s / 20s / 40s
 * - 其他状态码不重试，返回 0
 */
function retryDelay(status, retryCount) {
  if (status === 429 || status === 503) {
    return [60000, 120000, 300000][retryCount] ?? 300000;
  }
  if (status >= 500) {
    return Math.pow(2, retryCount) * 10000; // 10s / 20s / 40s
  }
  return 0; // 4xx 等不重试
}

/** 网络/超时错误的退避：5s / 10s / 20s */
function networkRetryDelay(retryCount) {
  return Math.pow(2, retryCount) * 5000;
}

export class RiceQuantClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.sessionPayload = options.sessionPayload || loadJson(this.sessionFile);
    this.origin = 'https://www.ricequant.com';
    // 支持直接传入 cookies 数组，或从 sessionPayload 中获取
    this.cookieJar = options.cookies || this.sessionPayload.cookies || [];
    this.workspaceId = null;
  }

  buildHeaders(url, overrides = {}) {
    const headers = {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'X-Requested-With': 'XMLHttpRequest',
      'Referer': url,
      'Origin': this.origin,
      'Cookie': this.cookieJar.map(c => `${c.name}=${c.value}`).join('; '),
      ...overrides
    };
    return headers;
  }

  async request(url, options = {}, retryCount = 0) {
    const fullUrl = url.startsWith('http') ? url : `${this.origin}${url}`;
    const maxRetries = 3;
    const timeoutMs = options.timeoutMs || 30000;

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const response = await fetch(fullUrl, {
        method: options.method || 'GET',
        headers: this.buildHeaders(fullUrl, options.headers),
        body: options.body,
        signal: controller.signal
      });
      clearTimeout(timer);

      const text = await response.text();

      if (!response.ok) {
        if (retryCount < maxRetries) {
          const delay = retryDelay(response.status, retryCount);
          if (delay > 0) {
            console.warn(`      [Retry ${retryCount+1}/${maxRetries}] HTTP ${response.status}, waiting ${delay/1000}s...`);
            await new Promise(r => setTimeout(r, delay));
            return this.request(url, options, retryCount + 1);
          }
        }
        throw new Error(`Request failed ${response.status} ${fullUrl}: ${text.slice(0, 500)}`);
      }

      try { return JSON.parse(text); } catch { return text; }
    } catch (error) {
      clearTimeout(timer);
      const isRetryable = error.name === 'AbortError' ||
        error.message.includes('timeout') ||
        error.message.includes('network') ||
        error.message.includes('ECONN') ||
        error.message.includes('ECONNRESET');
      if (isRetryable && retryCount < maxRetries) {
        const delay = networkRetryDelay(retryCount);
        const reason = error.name === 'AbortError' ? `timeout(${timeoutMs}ms)` : error.message;
        console.warn(`      [Retry ${retryCount+1}/${maxRetries}] ${reason}, waiting ${delay/1000}s...`);
        await new Promise(r => setTimeout(r, delay));
        return this.request(url, options, retryCount + 1);
      }
      throw error;
    }
  }

  async checkLogin() {
    return this.request('/api/user/isLogin.do', { method: 'POST' });
  }

  async getWorkspaceId() {
    if (this.workspaceId) return this.workspaceId;
    
    const result = await this.request('/api/user/v1/workspaces');
    
    if (result.data && result.data.length > 0) {
      this.workspaceId = result.data[0].id;
      return this.workspaceId;
    }
    
    throw new Error('No workspace found');
  }

  async listStrategies() {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies?code=false&own=false&metadata=true`;
    const result = await this.request(url);
    
    if (Array.isArray(result)) {
      return result.map(s => ({
        id: s.strategy_id || s._id || s.id,
        name: s.title || s.name || 'Unnamed',
        ...s
      }));
    }
    
    return [];
  }

  async getStrategyContext(strategyId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies/${strategyId}?code=true`;
    const result = await this.request(url);
    
    return {
      strategyId: result._id || result.strategy_id || strategyId,
      workspaceId,
      name: result.name || result.title || '',
      code: result.code || ''
    };
  }

  async saveStrategy(strategyId, name, code, context) {
    const workspaceId = context?.workspaceId || await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies/${strategyId}`;
    
    const body = JSON.stringify({
      title: name,
      code
    });
    
    try {
      return await this.request(url, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body
      });
    } catch (e) {
      // PATCH 可能返回空，忽略错误
      return { success: true };
    }
  }

  async runBacktest(strategyId, code, config, context) {
    const workspaceId = context?.workspaceId || await this.getWorkspaceId();
    const url = `/api/backtest/v1/workspaces/${workspaceId}/backtests`;
    
    const body = JSON.stringify({
      strategy_id: strategyId,
      code,
      config: {
        start_date: config.startTime || '2021-01-01',
        end_date: config.endTime || '2025-03-28',
        stock_init_cash: parseInt(config.baseCapital || '100000', 10),
        futures_init_cash: 0,
        bond_init_cash: 0,
        frequency: config.frequency || 'day',
        benchmark: config.benchmark || '000300.XSHG'
      }
    });
    
    const result = await this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body
    });
    
    // 返回的可能是字符串 ID
    if (typeof result === 'string') {
      return { backtestId: result };
    }
    return result;
  }

  async getBacktestResult(backtestId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}?extra_fields=summary`;
    return this.request(url);
  }

  async getBacktestList(strategyId) {
    const workspaceId = await this.getWorkspaceId();
    const url = strategyId 
      ? `/api/backtest/v1/workspaces/${workspaceId}/backtests?strategy_id=${strategyId}`
      : `/api/backtest/v1/workspaces/${workspaceId}/backtests`;
    const result = await this.request(url);
    return result.backtests || [];
  }

  /**
   * 查询策略的所有回测记录，按时间倒序排列
   * @param {string} strategyId
   * @returns {Array} 回测列表
   */
  async listStrategyBacktests(strategyId) {
    if (!strategyId) throw new Error('strategyId is required');
    const backtests = await this.getBacktestList(strategyId);
    // 按创建时间倒序
    return backtests.sort((a, b) => {
      const ta = new Date(a.created_at || a.createdAt || 0).getTime();
      const tb = new Date(b.created_at || b.createdAt || 0).getTime();
      return tb - ta;
    });
  }

  /**
   * 获取策略最近一次回测的完整结果
   * @param {string} strategyId
   * @returns {{ backtest, result, risk }}
   */
  async getLatestBacktestResult(strategyId) {
    const list = await this.listStrategyBacktests(strategyId);
    if (!list.length) throw new Error(`No backtests found for strategy ${strategyId}`);
    const latest = list[0];
    const backtestId = latest._id || latest.backtest_id || latest.id;
    const [result, risk] = await Promise.all([
      this.getBacktestResult(backtestId),
      this.getBacktestRisk(backtestId)
    ]);
    return { backtest: latest, backtestId, result, risk };
  }

  /**
   * 获取策略指定回测的完整结果（通过 backtestId）
   * @param {string} backtestId
   * @returns {{ backtestId, result, risk }}
   */
  async getBacktestResultById(backtestId) {
    if (!backtestId) throw new Error('backtestId is required');
    const [result, risk] = await Promise.all([
      this.getBacktestResult(backtestId),
      this.getBacktestRisk(backtestId)
    ]);
    return { backtestId, result, risk };
  }

  async getRunningBacktestCount() {
    const backtests = await this.getBacktestList();
    const running = backtests.filter(b => b.status === 'running');
    return running.length;
  }

  async getBacktestRisk(backtestId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}/risk`;
    try {
      return this.request(url);
    } catch {
      return null;
    }
  }

  async createStrategy(title, code) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies`;
    
    const body = JSON.stringify({
      title,
      code,
      metadata: {
        strategy_type: 'general',
        wizard_option: null
      },
      config: {
        stock_init_cash: 100000,
        futures_init_cash: 0,
        bond_init_cash: 0,
        start_date: '2020-01-01',
        end_date: '2025-03-28',
        frequency: 'day',
        benchmark: '000300.XSHG'
      },
      account_type: 'stock',
      permission: 'write'
    });
    
    const result = await this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body
    });
    
    return result;
  }

  async deleteStrategy(strategyId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/v1/workspaces/${workspaceId}/strategies/${strategyId}`;
    try {
      await this.request(url, { method: 'DELETE' });
      return true;
    } catch (e) {
      console.log(`Warning: Failed to delete strategy ${strategyId}: ${e.message}`);
      return false;
    }
  }

  async getFullReport(backtestId) {
    const [result, risk] = await Promise.all([
      this.getBacktestResult(backtestId),
      this.getBacktestRisk(backtestId)
    ]);
    
    return {
      backtestId,
      result,
      risk,
      summary: result?.summary || risk || {}
    };
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