import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

/**
 * 常用因子 ID（从 /stock/meta 获取）
 * 格式：0.M.股票每日指标_<指标名>.0
 */
export const FACTOR_IDS = {
  ROA: '0.M.股票每日指标_中性ROA.0',
  ROE: '0.M.股票每日指标_中性ROE.0',
  PE: '0.M.股票每日指标_市盈率.0',
  PB: '0.M.股票每日指标_市净率.0',
  MOMENTUM: '0.M.股票每日指标_动量.0',
};

/**
 * 账号限制说明：
 * - level=1 普通账号：回测时间窗口限制在最近约 1 年内
 * - 日期格式：斜杠 "2025/04/02"（内部转换，传入时可用连字符）
 * - 回测通过浏览器 JS (scrat.utility.ajaxDispatch) 执行，不能直接 HTTP POST
 */

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
   * Run backtest via /stock/runtest
   * NOTE: Direct HTTP POST to this endpoint returns "Server Error".
   * Must be called from browser context via scrat.utility.ajaxDispatch.
   * Use browser/run-backtest-via-js.js for actual execution.
   *
   * Correct payload format (from reverse-engineering the page JS):
   * - start/end: slash format "2025/04/02" (not dashes)
   * - calc_id: uid + "." + timestamp
   * - All other fields from getCurrentStrategy().tabs.back_test
   */
  buildRunBacktestPayload(config, uid) {
    const toSlashDate = d => d.replace(/-/g, '/');
    return {
      filters: config.filters || [],
      ranks: config.ranks || [],
      pool: config.pool || '',
      exclude_st: config.exclude_st || '0',
      exclude_STIB: config.exclude_STIB ?? 1,
      filter_suspend: config.filter_suspend || false,
      industry_type: config.industry_type || 0,
      timing: config.timing || { indicators: [], position: '0', threshold: ['-1', '-1'] },
      start: toSlashDate(config.start || config.startTime || '2022/01/01'),
      end: toSlashDate(config.end || config.endTime || '2024/01/01'),
      reference: config.reference || '000300',
      count: String(config.count || '10'),
      period: config.period || 5,
      price: config.price || 'close',
      trade_cost: config.trade_cost ?? 0.002,
      position_limit: config.position_limit ?? 1,
      backup_num: config.backup_num || '0',
      backup_fund: config.backup_fund || '',
      ideal_position: config.ideal_position ?? 0.1,
      min_position: config.min_position ?? 0.01,
      position_bias: config.position_bias ?? 0.3,
      model: config.model || 0,
      weight: config.weight || '',
      trading_strategy: config.trading_strategy || { buy_options: [], sell_options: [], hold_options: [] },
      hedge: config.hedge || false,
      always_tradable: config.always_tradable || 0,
      ideal_count: config.ideal_count || 10,
      max_count: config.max_count || 15,
      calc_id: `${uid}.${Date.now()}`
    };
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
