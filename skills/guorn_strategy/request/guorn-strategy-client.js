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
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

export class GuornStrategyClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.sessionPayload = options.sessionPayload || loadJson(this.sessionFile);
    this.origin = 'https://guorn.com';
    this.cookieJar = this.sessionPayload.cookies || [];
    this.timestamp = Date.now();
  }

  buildHeaders(url, overrides = {}) {
    const headers = {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'Referer': url,
      'Cookie': this.cookieJar.map(c => `${c.name}=${c.value}`).join('; '),
      ...overrides
    };
    return headers;
  }

  // 果仁网 POST 请求：_xsrf 通过 URL 参数传递，body 是 JSON 字符串（无 contentType）
  buildPostUrl(path) {
    const xsrf = this.cookieJar.find(c => c.name === '_xsrf');
    const sep = path.includes('?') ? '&' : '?';
    return xsrf ? `${path}${sep}_xsrf=${encodeURIComponent(xsrf.value)}` : path;
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

  /**
   * Get user profile
   */
  async getUserProfile() {
    const url = `/user/profile?_=${this.timestamp}`;
    return this.request(url);
  }

  /**
   * Get stock pool list
   */
  async getStockPoolList(category = 'stock') {
    const url = `/stock/pool/all?category=${category}&_=${this.timestamp}`;
    return this.request(url);
  }

  /**
   * Get hot pool list
   */
  async getHotPoolList(category = 'stock') {
    const url = `/stock/hotpool/all?category=${category}&_=${this.timestamp}`;
    return this.request(url);
  }

  /**
   * Get stock meta (indicators, functions)
   */
  async getStockMeta(category = 'stock') {
    const url = `/stock/meta?category=${category}`;
    return this.request(url);
  }

  /**
   * Get strategy list
   */
  async getStrategyList() {
    const url = '/user/home';
    const html = await this.request(url, { method: 'GET' });
    
    // Parse strategy list from HTML
    const matches = [...html.matchAll(/href="\/stock\?id=([^"&]+)[^"]*"[^>]*>([^<]+)<\/a>/g)];
    
    const strategies = matches.map(m => ({
      id: m[1],
      name: m[2].trim()
    }));

    // Filter out duplicates
    const uniqueIds = new Set();
    return strategies.filter(s => {
      if (uniqueIds.has(s.id)) return false;
      uniqueIds.add(s.id);
      return true;
    });
  }

  /**
   * Get strategy detail
   */
  async getStrategy(strategyId) {
    const url = `/stock?id=${strategyId}`;
    const html = await this.request(url, { method: 'GET' });
    
    // Parse strategy config from HTML
    // This is a simplified version, actual parsing would be more complex
    return { id: strategyId, html };
  }

  /**
   * Save strategy (not implemented in API, requires browser interaction)
   */
  async saveStrategy(config) {
    // Note: Guorn.com does not expose a direct save API
    // Strategy saving requires browser interaction
    throw new Error('Strategy save not available via API. Use browser automation instead.');
  }

  /**
   * Run backtest
   */
  async runBacktest(config) {
    const url = '/stock/backtest';
    const body = new URLSearchParams();
    
    body.append('id', config.strategyId || '');
    body.append('start', config.startTime || '2020-01-01');
    body.append('end', config.endTime || '2024-01-01');
    body.append('benchmark', config.benchmark || 'hs300');
    body.append('cost', config.transactionCost || '0.002');

    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
      body: body.toString()
    });
  }

  /**
   * Get backtest result
   */
  async getBacktestResult(backtestId) {
    const url = `/stock/backtest/result?id=${backtestId}`;
    return this.request(url);
  }

  /**
   * Get backtest history
   */
  async getBacktestHistory(strategyId) {
    const url = `/stock/backtest/history?id=${strategyId}`;
    return this.request(url);
  }

  /**
   * Get realtime stock selection
   */
  async getRealtimeSelection(config) {
    const url = '/stock/realtime';
    const body = new URLSearchParams();
    
    body.append('poolid', config.stockPool?.poolId || '');
    body.append('filters', JSON.stringify(config.filters || []));
    body.append('rankings', JSON.stringify(config.rankings || []));

    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
      body: body.toString()
    });
  }

  /**
   * Get historical stock selection
   */
  async getHistoricalSelection(config) {
    const url = '/stock/history';
    const body = new URLSearchParams();
    
    body.append('date', config.date || '');
    body.append('poolid', config.stockPool?.poolId || '');
    body.append('filters', JSON.stringify(config.filters || []));
    body.append('rankings', JSON.stringify(config.rankings || []));

    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
      body: body.toString()
    });
  }

  /**
   * Write artifact to file
   */
  writeArtifact(baseName, data, extension = 'json') {
    const timestamp = Date.now();
    const filePath = path.join(this.outputRoot, `${baseName}-${timestamp}.${extension}`);
    ensureDir(filePath);
    const content = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    fs.writeFileSync(filePath, content, 'utf8');
    return filePath;
  }
}
