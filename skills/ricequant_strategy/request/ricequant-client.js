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

export class RiceQuantClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.sessionPayload = options.sessionPayload || loadJson(this.sessionFile);
    this.origin = 'https://www.ricequant.com';
    this.cookieJar = this.sessionPayload.cookies || [];
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

  async request(url, options = {}) {
    const fullUrl = url.startsWith('http') ? url : `${this.origin}${url}`;
    
    const response = await fetch(fullUrl, {
      method: options.method || 'GET',
      headers: this.buildHeaders(fullUrl, options.headers),
      body: options.body
    });

    const text = await response.text();
    
    if (!response.ok) {
      throw new Error(`Request failed ${response.status} ${fullUrl}: ${text.slice(0, 500)}`);
    }

    try {
      return JSON.parse(text);
    } catch (e) {
      return text;
    }
  }

  async checkLogin() {
    const url = '/api/user/isLogin.do';
    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' }
    });
  }

  async login(username, password) {
    const url = '/api/user/login.do';
    const body = new URLSearchParams();
    body.append('username', username);
    body.append('password', password);
    
    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: body.toString()
    });
  }

  async getWorkspaces() {
    const url = '/api/workspace/list.do';
    return this.request(url, { method: 'POST' });
  }

  async getWorkspaceId() {
    if (this.workspaceId) {
      return this.workspaceId;
    }
    
    const result = await this.getWorkspaces();
    
    if (result.code === 0 || result.code === '0') {
      const workspaces = result.data || result.workspaces || [];
      if (workspaces.length > 0) {
        this.workspaceId = workspaces[0].id || workspaces[0]._id || workspaces[0].workspaceId;
        return this.workspaceId;
      }
    }
    
    // 如果获取失败，返回默认值
    console.log('Warning: Could not get workspace ID, using default');
    return 'default';
  }

  async listStrategies() {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/workspace/strategies.do?workspaceId=${workspaceId}`;
    const result = await this.request(url);
    
    const strategies = result.data || result.strategies || result || [];
    return strategies.map(s => ({
      id: s.strategyId || s.id,
      name: s.strategyName || s.name,
      ...s
    }));
  }

  async getStrategyContext(strategyId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/strategy/detail.do?strategyId=${strategyId}&workspaceId=${workspaceId}`;
    const result = await this.request(url);
    
    const data = result.data || result;
    return {
      strategyId,
      workspaceId,
      name: data.strategyName || data.name || '',
      code: data.code || ''
    };
  }

  async saveStrategy(strategyId, name, code, context) {
    const workspaceId = context?.workspaceId || await this.getWorkspaceId();
    const url = '/api/strategy/save.do';
    
    const body = new URLSearchParams();
    body.append('strategyId', strategyId);
    body.append('workspaceId', workspaceId);
    body.append('name', name);
    body.append('code', code);
    
    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: body.toString()
    });
  }

  async runBacktest(strategyId, code, config, context) {
    const workspaceId = context?.workspaceId || await this.getWorkspaceId();
    const url = '/api/backtest/run.do';
    
    const body = new URLSearchParams();
    body.append('strategyId', strategyId);
    body.append('workspaceId', workspaceId);
    body.append('code', code);
    body.append('startDate', config.startTime || '2021-01-01');
    body.append('endDate', config.endTime || '2025-03-28');
    body.append('initialCash', config.baseCapital || '100000');
    body.append('frequency', config.frequency || 'day');
    body.append('benchmark', config.benchmark || '000300.XSHG');
    
    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: body.toString()
    });
  }

  async getBacktestResult(backtestId) {
    const url = `/api/backtest/result.do?backtestId=${backtestId}`;
    return this.request(url);
  }

  async getBacktestList(strategyId) {
    const workspaceId = await this.getWorkspaceId();
    const url = `/api/backtest/list.do?strategyId=${strategyId}&workspaceId=${workspaceId}`;
    const result = await this.request(url);
    return result.data || result.backtests || [];
  }

  async getBacktestRisk(backtestId) {
    const url = `/api/backtest/risk.do?backtestId=${backtestId}`;
    try {
      return this.request(url);
    } catch {
      return null;
    }
  }

  async getFullReport(backtestId) {
    console.log(`Generating full report for backtest ${backtestId}...`);
    
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