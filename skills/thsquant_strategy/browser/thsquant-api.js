/**
 * THSQuant API 客户端
 * 通过浏览器捕获发现的真实API
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export class THSQuantAPIClient {
  constructor(options = {}) {
    this.baseUrl = 'https://quant.10jqka.com.cn';
    this.sessionFile = options.sessionFile || SESSION_FILE;
    this.outputRoot = options.outputRoot || OUTPUT_ROOT;
    this.cookies = [];
    this.cookieHeader = '';

    this._loadSession();
  }

  _loadSession() {
    if (fs.existsSync(this.sessionFile)) {
      const session = JSON.parse(fs.readFileSync(this.sessionFile, 'utf8'));
      this.cookies = session.cookies || [];
      this.cookieHeader = this.cookies.map(c => `${c.name}=${c.value}`).join('; ');
    }
  }

  async _request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const method = options.method || 'POST';

    const headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': this.cookieHeader,
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
      'X-Requested-With': 'XMLHttpRequest',
      ...options.headers
    };

    const body = options.body || 'isajax=1';

    const response = await fetch(url, { method, headers, body });
    const text = await response.text();

    // 解析JSONP响应
    const jsonpMatch = text.match(/\((.+)\)/s);
    if (jsonpMatch) {
      try {
        return JSON.parse(jsonpMatch[1]);
      } catch (e) {}
    }

    // 尝试直接解析JSON
    try {
      return JSON.parse(text);
    } catch (e) {
      return { raw: text };
    }
  }

  /**
   * 检查登录状态
   */
  async checkLogin() {
    const data = await this._request('/platform/user/getauthdata');
    return {
      logged: data.errorcode === 0,
      userId: data.result?.user_id,
      data
    };
  }

  /**
   * 获取策略列表
   */
  async listStrategies() {
    const data = await this._request('/platform/algorithms/queryall2/', {
      body: 'isajax=1&datatype=jsonp'
    });

    if (data.errorcode !== 0) {
      throw new Error(data.errormsg || '获取策略列表失败');
    }

    return data.result?.strategys || [];
  }

  /**
   * 创建新策略
   * @param {string} name - 策略名称
   * @param {string} code - 策略代码
   */
  async createStrategy(name, code = '') {
    const loginStatus = await this.checkLogin();
    if (!loginStatus.logged) {
      throw new Error('未登录');
    }

    const body = new URLSearchParams({
      isajax: '1',
      user_id: loginStatus.userId,
      algo_name: name,
      code: code,
      stock_market: 'STOCK'
    }).toString();

    const data = await this._request('/platform/algorithms/add/', { body });

    return {
      success: data.errorcode === 0,
      algoId: data.result?.algo_id,
      data
    };
  }

  /**
   * 运行回测
   * @param {string} algoId - 策略ID
   * @param {object} config - 回测配置
   */
  async runBacktest(algoId, config = {}) {
    const defaultConfig = {
      start_date: '2023-01-01',
      end_date: '2024-12-31',
      capital_base: 100000,
      frequency: 'DAILY',
      benchmark: '000300.SH'
    };

    const finalConfig = { ...defaultConfig, ...config };

    const body = new URLSearchParams({
      isajax: '1',
      algo_id: algoId,
      start_date: finalConfig.start_date,
      end_date: finalConfig.end_date,
      capital_base: String(finalConfig.capital_base),
      frequency: finalConfig.frequency,
      benchmark: finalConfig.benchmark
    }).toString();

    const data = await this._request('/platform/backtest/run/', { body });

    return {
      success: data.errorcode === 0,
      backtestId: data.result?.backtest_id,
      data
    };
  }

  /**
   * 获取回测结果
   * @param {string} backtestId - 回测ID
   */
  async getBacktestResult(backtestId) {
    const body = new URLSearchParams({
      isajax: '1',
      backtest_id: backtestId
    }).toString();

    const data = await this._request('/platform/backtest/result/', { body });

    return data;
  }

  /**
   * 获取模拟交易列表
   */
  async listSimuPapers() {
    const data = await this._request('/platform/simupaper/queryall/', {
      body: 'isajax=1'
    });

    if (data.errorcode !== 0) {
      throw new Error(data.errormsg || '获取模拟交易列表失败');
    }

    return data.result || [];
  }

  /**
   * 保存结果
   */
  saveResult(name, data) {
    const filePath = path.join(this.outputRoot, `${name}-${Date.now()}.json`);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    return filePath;
  }
}

// CLI使用
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  const client = new THSQuantAPIClient();

  console.log('\n' + '='.repeat(70));
  console.log('THSQuant API 客户端');
  console.log('='.repeat(70));

  switch (command) {
    case 'check':
      const login = await client.checkLogin();
      console.log('\n登录状态:', login.logged ? '已登录' : '未登录');
      if (login.userId) console.log('用户ID:', login.userId);
      break;

    case 'list':
      console.log('\n获取策略列表...');
      const strategies = await client.listStrategies();
      console.log(`\n找到 ${strategies.length} 个策略:`);
      strategies.forEach((s, i) => {
        console.log(`  ${i + 1}. ${s.algo_name} (${s.algo_id})`);
        console.log(`     回测数: ${s.backtest_number}, 修改: ${s.modified}`);
      });
      break;

    case 'simu':
      console.log('\n获取模拟交易列表...');
      const simuPapers = await client.listSimuPapers();
      console.log(`\n找到 ${simuPapers.length} 个模拟交易:`);
      simuPapers.forEach((p, i) => {
        console.log(`  ${i + 1}. ${p.name} (${p.algo_id})`);
        console.log(`     收益: ${p.annual_yield}, 最大回撤: ${p.max_drawdown}`);
      });
      break;

    default:
      console.log('\n用法:');
      console.log('  node browser/thsquant-api.js check   - 检查登录状态');
      console.log('  node browser/thsquant-api.js list    - 列出策略');
      console.log('  node browser/thsquant-api.js simu    - 列出模拟交易');
  }
}

main().catch(err => {
  console.error('\n错误:', err.message);
  process.exit(1);
});