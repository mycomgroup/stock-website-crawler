import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36';

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

export function loadJson(filePath) {
  if (!fs.existsSync(filePath)) return {};
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch (e) { return {}; }
}

export class JqkaBacktestClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.origin = 'https://backtest.10jqka.com.cn';
    const session = options.sessionPayload || loadJson(this.sessionFile);
    this.cookieJar = options.cookies || session.cookies || [];
  }

  getCookieHeader() {
    return this.cookieJar.map(c => `${c.name}=${c.value}`).join('; ');
  }

  buildHeaders(referer) {
    return {
      'Content-Type': 'application/json', // Using JSON mostly for 10jqka backtest
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Origin': this.origin,
      'Referer': referer || `${this.origin}/backtest/app.html`,
      'Cookie': this.getCookieHeader()
    };
  }

  async request(endpoint, bodyObj = null, method = 'POST', retries = 3) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.origin}${endpoint}`;
    
    const options = {
      method,
      headers: this.buildHeaders(url)
    };

    if (bodyObj) {
      options.body = typeof bodyObj === 'string' ? bodyObj : JSON.stringify(bodyObj);
      if (options.body.includes('=')) {
        options.headers['Content-Type'] = 'application/x-www-form-urlencoded';
      }
    }

    for (let attempt = 0; attempt < retries; attempt++) {
      try {
        const response = await fetch(url, options);
        const text = await response.text();
        
        if (!response.ok) {
          if (response.status >= 500 && attempt < retries - 1) {
            await new Promise(r => setTimeout(r, 2000 * (attempt + 1)));
            continue;
          }
          throw new Error(`HTTP ${response.status} ${url}: ${text.slice(0, 200)}`);
        }

        try {
          return JSON.parse(text);
        } catch (e) {
          return { raw: text.slice(0, 500), parseError: e.message };
        }
      } catch (error) {
        if (error.message.includes('fetch failed') && attempt < retries - 1) {
          await new Promise(r => setTimeout(r, 3000 * (attempt + 1)));
          continue;
        }
        throw error;
      }
    }
    throw new Error(`Request failed after ${retries} retries`);
  }

  /**
   * Run the backtest and return a taskId or immediate errors.
   */
  async runBacktest(config = {}) {
    const defaultData = {
        query: "创业板，非ST",
        period: "2,3",
        start_date: "2025-01-01",
        end_date: "2026-04-10",
        stock_hold: "2",
        upper_income: "25",
        lower_income: "9",
        fall_income: "5",
        day_buy_stock_num: "2",
        engine: "undefined",
        capital: "10000000"
    };
    
    const payload = { ...defaultData, ...config };
    const data = await this.request('/tradebacktest/yieldbacktest', payload);
    
    if (data.errorcode === -401) {
        throw new Error('未授权 (noauth)，请先运行 node browser/manual-login-capture.js 重新登录并捕获 session。');
    }
    
    // Note: If success, we should get back a taskId. Need to adapt once we see the real payload shape.
    return {
        success: data.errorcode !== -401, // Temp condition
        data
    };
  }

  writeArtifact(baseName, data, ext = 'json') {
    const filePath = path.join(this.outputRoot, `${baseName}-${Date.now()}.${ext}`);
    ensureDir(filePath);
    fs.writeFileSync(filePath, typeof data === 'string' ? data : JSON.stringify(data, null, 2), 'utf8');
    return filePath;
  }
}
