import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
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

export class JoinQuantStrategyClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.sessionPayload = options.sessionPayload || loadJson(this.sessionFile);
    this.origin = 'https://www.joinquant.com';
    this.cookieJar = this.sessionPayload.cookies || [];
    
    // Extract _xsrf from cookies for general requests
    this.xsrfToken = this.cookieJar.find(item => item.name === '_xsrf')?.value?.split('|')[2] || '';
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
        if (response.status >= 500 && retryCount < maxRetries) {
          const delay = Math.pow(2, retryCount) * 1000;
          console.warn(`      [Retry ${retryCount+1}/${maxRetries}] HTTP ${response.status}, retrying in ${delay}ms...`);
          await new Promise(r => setTimeout(r, delay));
          return this.request(url, options, retryCount + 1);
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
        const delay = Math.pow(2, retryCount) * 1000;
        const reason = error.name === 'AbortError' ? `timeout(${timeoutMs}ms)` : error.message;
        console.warn(`      [Retry ${retryCount+1}/${maxRetries}] ${reason}, retrying in ${delay}ms...`);
        await new Promise(r => setTimeout(r, delay));
        return this.request(url, options, retryCount + 1);
      }
      throw error;
    }
  }

  /**
   * Fetch the strategy edit page to extract the CSRF token and algorithm metadata
   */
  async getStrategyContext(algorithmId) {
    const url = `/algorithm/index/edit?algorithmId=${algorithmId}`;
    console.log(`GET ${url} with cookies:`, this.buildHeaders(`${this.origin}${url}`).Cookie.slice(0, 100) + '...');
    const html = await this.request(url, { method: 'GET' });
    
    if (html.includes('登录') && !html.includes('算法回测')) {
       console.log('Page seems to be a login page instead of the edit page.');
       // console.log(html.slice(0, 1000));
    }
    // Extract token: can be in window.tokenData, var token = "...", or in a hidden input
    const tokenMatch = html.match(/window\.tokenData\s*=\s*{[\s\S]*?value:\s*['"]([^'"]+)['"]/) ||
                       html.match(/var\s+token\s*=\s*['"]([^'"]+)['"]/) || 
                       html.match(/name="token"\s+value="([^"]+)"/) ||
                       html.match(/id="token"\s+value="([^"]+)"/);
    const token = tokenMatch ? tokenMatch[1] : '';
    
    // Extract internal algorithmId (sometimes different from URL ID)
    const internalIdMatch = html.match(/name="algorithm\[algorithmId\]"\s+value="([^"]+)"/);
    const internalId = internalIdMatch ? internalIdMatch[1] : algorithmId;

    // Extract userId
    const userIdMatch = html.match(/name="algorithm\[userId\]"\s+value="([^"]+)"/) ||
                        html.match(/user_id\s*=\s*['"]?(\d+)['"]?/);
    const userId = userIdMatch ? userIdMatch[1] : '';
    
    // Extract strategy name
    const nameMatch = html.match(/id="title-box".*?value="([^"]+)"/) ||
                      html.match(/<title>(.*?)<\/title>/);
    let name = nameMatch ? nameMatch[1] : '';
    name = name.replace(' - 聚宽', '').trim();

    // Extract pyVersion
    const pyVersionMatch = html.match(/name="backtest\[pyVersion\]"\s+value="([^"]+)"/) ||
                           html.match(/pyVersion\s*:\s*(\d+)/);
    const pyVersion = pyVersionMatch ? pyVersionMatch[1] : '3';

    if (!token) {
      const debugFile = this.writeArtifact(`failed-page-${algorithmId}`, html, 'html');
      console.log(`Failed to extract token. HTML saved to ${debugFile}`);
      throw new Error(`Failed to extract CSRF token. Page content might have changed. See ${debugFile}`);
    }

    return { algorithmId: internalId, urlId: algorithmId, token, name, userId, pyVersion };
  }

  /**
   * Save strategy code
   */
  async saveStrategy(algorithmId, name, code, context) {
    const url = '/algorithm/index/save?ajax=1';
    const body = new URLSearchParams();
    body.append('algorithm[algorithmId]', algorithmId);
    body.append('algorithm[name]', name);
    body.append('algorithm[code]', Buffer.from(code).toString('base64'));
    body.append('token', context.token);
    body.append('ajax', '1');

    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
      body: body.toString()
    });
  }

  /**
   * Run backtest
   */
  async runBacktest(algorithmId, code, config, context) {
    const url = '/algorithm/index/build?ajax=1';
    const body = new URLSearchParams();
    
    // Algorithm Metadata
    body.append('algorithm[algorithmId]', algorithmId);
    body.append('algorithm[userId]', context.userId || '');
    body.append('algorithm[name]', context.name || '');
    body.append('algorithm[code]', Buffer.from(code).toString('base64'));
    body.append('encrType', 'base64');
    
    // Backtest Config
    const formatTime = (d) => d.includes(':') ? d : `${d} 00:00:00`;
    body.append('backtest[startTime]', formatTime(config.startTime || '2023-01-01'));
    body.append('backtest[endTime]', formatTime(config.endTime || '2023-12-31'));
    body.append('backtest[baseCapital]', config.baseCapital || '100000');
    body.append('backtest[frequency]', config.frequency || 'day');
    body.append('backtest[pyVersion]', context.pyVersion || '3');
    body.append('backtest[type]', '0'); // 0 for backtest
    
    body.append('ajax', '1');
    body.append('token', context.token);

    const result = await this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
      body: body.toString()
    });

    if (result.status != 0 && result.status != '0') {
      throw new Error(`Failed to start backtest: ${JSON.stringify(result)}`);
    }

    return result.data; // Includes backtestId
  }

  /**
   * Poll backtest results
   */
  async getBacktestResult(backtestId, context, offset = 0) {
    const url = `/algorithm/backtest/result?backtestId=${backtestId}&offset=${offset}&userRecordOffset=0&ajax=1`;
    const body = new URLSearchParams();
    body.append('token', context.token);
    body.append('ajax', '1');

    return this.request(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
      body: body.toString()
    });
  }

  /**
   * Get all transactions (trades) for a backtest
   */
  async getTransactionInfo(backtestId) {
    const url = `/algorithm/backtest/transactionInfo?backtestId=${backtestId}&ajax=1`;
    return this.request(url, { method: 'POST' });
  }

  /**
   * Get all position details for a backtest
   */
  async getPositionInfo(backtestId) {
    const url = `/algorithm/backtest/positionInfo?backtestId=${backtestId}&ajax=1`;
    return this.request(url, { method: 'POST' });
  }

  /**
   * Get backtest logs
   */
  async getLog(backtestId, offset = 0) {
    const url = `/algorithm/backtest/log?backtestId=${backtestId}&offset=${offset}&ajax=1`;
    return this.request(url, { method: 'POST' });
  }

  /**
   * List all strategies
   */
  async listStrategies() {
    const url = '/algorithm/index/list';
    const html = await this.request(url, { method: 'GET' });
    
    // Improved regex based on research
    // <a href='/algorithm/index/edit?algorithmId=...' class='black file_name' ...>NAME</a>
    const matches = [...html.matchAll(/href="\/algorithm\/index\/edit\?algorithmId=([^"&]+)[^"]*"[^>]*>([^<]+)<\/a>/g)];
    
    const strategies = matches.map(m => ({
      id: m[1],
      name: m[2].trim()
    }));

    if (strategies.length === 0) {
      const debugFile = this.writeArtifact('list-page-empty', html, 'html');
      console.log(`No strategies matched regex. HTML saved to ${debugFile}`);
      // Try a broader regex for debugging
      const allLinks = [...html.matchAll(/href="([^"]+)"/g)].map(m => m[1]);
      console.log('Sample links found:', allLinks.slice(0, 10));
    }

    // Filter out duplicates (sometimes links appear twice)
    const uniqueIds = new Set();
    return strategies.filter(s => {
      if (uniqueIds.has(s.id)) return false;
      uniqueIds.add(s.id);
      return true;
    });
  }

  /**
   * List backtests for a strategy
   */
  async getBacktests(algorithmId) {
    const url = `/algorithm/backtest/list?algorithmId=${algorithmId}`;
    const html = await this.request(url, { method: 'GET' });
    
    // Extract backtest info from the table
    // <tr ... data-backtestid="BT_ID"> ... <a ...>NAME</a> ... <td class="time">TIME</td>
    const matches = [...html.matchAll(/data-backtestid="([^"]+)"[\s\S]*?<a[^>]*>([^<]+)<\/a>[\s\S]*?<td class="time">([^<]+)<\/td>/g)];
    
    return matches.map(m => ({
      id: m[1],
      name: m[2].trim(),
      time: m[3].trim()
    }));
  }

  /**
   * Get backtest summary statistics (Alpha, Sharpe, etc.)
   */
  async getBacktestStats(backtestId, context = {}) {
    const url = `/algorithm/backtest/stats?backtestId=${backtestId}&ajax=1`;
    const body = new URLSearchParams();
    if (context.token) body.append('token', context.token);
    body.append('ajax', '1');
    return this.request(url, { method: 'POST', body });
  }

  /**
   * Attribution Analysis: Returns Overview
   */
  async getAttributionReturnOverview(backtestId, context = {}) {
    const url = `/factor/backtest/returnOverview?backtestId=${backtestId}&ajax=1`;
    const body = new URLSearchParams();
    if (context.token) body.append('token', context.token);
    body.append('ajax', '1');
    return this.request(url, { method: 'POST', body });
  }

  /**
   * Attribution Analysis: Benefit Analysis
   */
  async getAttributionBenefit(backtestId, context = {}) {
    const url = `/factor/backtest/benifit?backtestId=${backtestId}&ajax=1`;
    const body = new URLSearchParams();
    if (context.token) body.append('token', context.token);
    body.append('ajax', '1');
    return this.request(url, { method: 'POST', body });
  }

  /**
   * Attribution Analysis: Risk Indicators
   */
  async getAttributionRiskIndicator(backtestId, context = {}) {
    const url = `/factor/backtest/riskIndicator?backtestId=${backtestId}&ajax=1`;
    const body = new URLSearchParams();
    if (context.token) body.append('token', context.token);
    body.append('ajax', '1');
    return this.request(url, { method: 'POST', body });
  }

  /**
   * Attribution Analysis: Position Analysis
   */
  async getAttributionPositionAnaly(backtestId, context = {}) {
    const url = `/factor/backtest/positionAnaly?backtestId=${backtestId}&ajax=1`;
    const body = new URLSearchParams();
    if (context.token) body.append('token', context.token);
    body.append('ajax', '1');
    return this.request(url, { method: 'POST', body });
  }

  /**
   * Attribution Analysis: Brinson Attribution
   */
  async getAttributionBrinson(backtestId, context = {}) {
    const url = `/factor/backtest/Brinson?backtestId=${backtestId}&ajax=1`;
    const body = new URLSearchParams();
    if (context.token) body.append('token', context.token);
    body.append('ajax', '1');
    return this.request(url, { method: 'POST', body });
  }

  /**
   * Attribution Analysis: Attribution Status
   */
  async getAttributionStatus(backtestId) {
    const url = `/factor/backtest/AttributionStatus?backtestId=${backtestId}`;
    return this.request(url, { method: 'POST' });
  }

  /**
   * Get context (token, etc.) from the attribution analysis page
   */
  async getAttributionContext(backtestId) {
    const url = `/algorithm/backtest/attributionAnaly?backtestId=${backtestId}`;
    const html = await this.request(url, { method: 'GET' });
    
    // Extract token: similar regex to edit page
    const tokenMatch = html.match(/window\.tokenData\s*=\s*{[\s\S]*?value:\s*['\"]([^'\"]+)['\"]/) ||
                       html.match(/var\s+token\s*=\s*['\"]([^'\"]+)['\"]/);
    
    return {
      token: tokenMatch ? tokenMatch[1] : null,
      backtestId
    };
  }

  /**
   * Aggregate all available data for a backtest
   */
  async getFullReport(backtestId, context) {
    console.log(`Generating full report for backtest ${backtestId}...`);
    
    // Get attribution context first to get the correct token for factor APIs
    const attrContext = await this.getAttributionContext(backtestId);

    const results = await Promise.allSettled([
      this.getBacktestResult(backtestId, context),
      this.getBacktestStats(backtestId, context),
      this.getTransactionInfo(backtestId),
      this.getPositionInfo(backtestId),
      this.getLog(backtestId),
      this.getAttributionReturnOverview(backtestId, attrContext),
      this.getAttributionBenefit(backtestId, attrContext),
      this.getAttributionRiskIndicator(backtestId, attrContext),
      this.getAttributionPositionAnaly(backtestId, attrContext),
      this.getAttributionBrinson(backtestId, attrContext)
    ]);

    const getValue = (r) => r.status === 'fulfilled' ? r.value : {};
    const [
      result, 
      stats, 
      transactions, 
      positions, 
      log,
      attrReturn,
      attrBenefit,
      attrRisk,
      attrPosition,
      attrBrinson
    ] = results.map(getValue);

    const resultData = result.data?.result || {};
    const statsData = stats.data || {};

    return {
      backtestId,
      summary: statsData,
      backtest: resultData.backtest || {},
      benchmark: resultData.benchmark || {},
      equityCurve: resultData.overallReturn || {},
      transactions: transactions.data || transactions,
      positions: positions.data || positions,
      log: log.data || log,
      attribution: {
        returnOverview: attrReturn.data || attrReturn,
        benefit: attrBenefit.data || attrBenefit,
        riskIndicator: attrRisk.data || attrRisk,
        positionAnaly: attrPosition.data || attrPosition,
        brinson: attrBrinson.data || attrBrinson
      }
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
