#!/usr/bin/env node
/**
 * THSQuant 策略提交工具
 * 通过API创建策略并运行回测
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.resolve(__dirname, '../../strategies/thsquant');

class THSQuantStrategyRunner {
  constructor() {
    this.baseUrl = 'https://quant.10jqka.com.cn';
    this.cookies = [];
    this.cookieHeader = '';
    this.userId = null;
    this._loadSession();
  }

  _loadSession() {
    if (fs.existsSync(SESSION_FILE)) {
      const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
      this.cookies = session.cookies || [];
      this.cookieHeader = this.cookies.map(c => `${c.name}=${c.value}`).join('; ');
    }
  }

  async _request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': this.cookieHeader,
      'User-Agent': 'Mozilla/5.0',
      'X-Requested-With': 'XMLHttpRequest'
    };

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: options.body || 'isajax=1'
    });

    const text = await response.text();

    // 解析JSONP
    const jsonpMatch = text.match(/\((.+)\)/s);
    if (jsonpMatch) {
      try { return JSON.parse(jsonpMatch[1]); } catch (e) {}
    }

    try { return JSON.parse(text); } catch (e) {
      return { raw: text };
    }
  }

  async checkLogin() {
    const data = await this._request('/platform/user/getauthdata');
    if (data.errorcode === 0) {
      this.userId = data.result?.user_id;
      return true;
    }
    return false;
  }

  async listStrategies() {
    const data = await this._request('/platform/algorithms/queryall2/', {
      body: 'isajax=1&datatype=jsonp'
    });
    return data.result?.strategys || [];
  }

  /**
   * 创建新策略
   */
  async createStrategy(name, code) {
    if (!this.userId) {
      const logged = await this.checkLogin();
      if (!logged) throw new Error('未登录');
    }

    const body = new URLSearchParams({
      isajax: '1',
      user_id: this.userId,
      algo_name: name,
      code: code,
      stock_market: 'STOCK'
    }).toString();

    const data = await this._request('/platform/algorithms/add/', { body });

    return {
      success: data.errorcode === 0,
      algoId: data.result?.algo_id,
      error: data.errormsg,
      data
    };
  }

  /**
   * 更新策略代码
   */
  async updateStrategy(algoId, name, code) {
    const body = new URLSearchParams({
      isajax: '1',
      algo_id: algoId,
      algo_name: name,
      code: code,
      stock_market: 'STOCK'
    }).toString();

    const data = await this._request('/platform/algorithms/update/', { body });

    return {
      success: data.errorcode === 0,
      data
    };
  }

  /**
   * 运行回测
   */
  async runBacktest(algoId, config = {}) {
    const defaultConfig = {
      start_date: '2023-01-01',
      end_date: '2024-12-31',
      capital_base: 100000,
      frequency: 'DAILY',
      benchmark: '000300.SH'
    };

    const cfg = { ...defaultConfig, ...config };

    const body = new URLSearchParams({
      isajax: '1',
      algo_id: algoId,
      start_date: cfg.start_date,
      end_date: cfg.end_date,
      capital_base: String(cfg.capital_base),
      frequency: cfg.frequency,
      benchmark: cfg.benchmark
    }).toString();

    const data = await this._request('/platform/backtest/run/', { body });

    return {
      success: data.errorcode === 0,
      backtestId: data.result?.backtest_id,
      error: data.errormsg,
      data
    };
  }

  /**
   * 获取回测结果
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
   * 提交策略文件并运行回测
   */
  async submitAndRun(strategyFile, config = {}) {
    const strategyPath = path.resolve(strategyFile);
    if (!fs.existsSync(strategyPath)) {
      throw new Error(`策略文件不存在: ${strategyPath}`);
    }

    const code = fs.readFileSync(strategyPath, 'utf8');
    const name = path.basename(strategyPath, '.py');

    console.log(`\n策略: ${name}`);
    console.log(`代码: ${code.split('\n').length} 行`);

    // 1. 检查登录
    console.log('\n1. 检查登录状态...');
    const logged = await this.checkLogin();
    if (!logged) {
      throw new Error('未登录，请先运行 node browser/auto-login-v6.js');
    }
    console.log(`   ✓ 已登录 (用户ID: ${this.userId})`);

    // 2. 检查是否已存在同名策略
    console.log('\n2. 检查现有策略...');
    const existingStrategies = await this.listStrategies();
    const existing = existingStrategies.find(s => s.algo_name === name);

    let algoId;
    if (existing) {
      console.log(`   找到现有策略: ${existing.algo_id}`);
      algoId = existing.algo_id;

      // 更新代码
      console.log('\n3. 更新策略代码...');
      const updateResult = await this.updateStrategy(algoId, name, code);
      if (updateResult.success) {
        console.log('   ✓ 代码已更新');
      } else {
        console.log('   ⚠ 更新失败，继续...');
      }
    } else {
      // 创建新策略
      console.log('\n3. 创建新策略...');
      const createResult = await this.createStrategy(name, code);
      if (!createResult.success) {
        throw new Error(`创建失败: ${createResult.error}`);
      }
      algoId = createResult.algoId;
      console.log(`   ✓ 已创建 (ID: ${algoId})`);
    }

    // 3. 运行回测
    console.log('\n4. 运行回测...');
    console.log(`   开始: ${config.start_date || '2023-01-01'}`);
    console.log(`   结束: ${config.end_date || '2024-12-31'}`);
    console.log(`   资金: ${config.capital_base || 100000}`);
    console.log(`   基准: ${config.benchmark || '000300.SH'}`);

    const backtestResult = await this.runBacktest(algoId, config);

    if (backtestResult.success) {
      console.log(`   ✓ 回测已提交 (ID: ${backtestResult.backtestId})`);

      // 保存结果
      const resultPath = path.join(OUTPUT_ROOT, `backtest-${name}-${Date.now()}.json`);
      fs.writeFileSync(resultPath, JSON.stringify(backtestResult.data, null, 2));
      console.log(`   结果: ${resultPath}`);
    } else {
      console.log(`   ✗ 回测失败: ${backtestResult.error}`);
    }

    return {
      algoId,
      backtestId: backtestResult.backtestId,
      success: backtestResult.success
    };
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const strategyArg = args.find(a => !a.startsWith('--'));

  if (!strategyArg) {
    console.log(`
用法:
  node browser/submit-strategy.js <策略文件.py> [选项]

选项:
  --start <date>     开始日期 (默认: 2023-01-01)
  --end <date>       结束日期 (默认: 2024-12-31)
  --capital <num>    初始资金 (默认: 100000)
  --benchmark <id>   基准指数 (默认: 000300.SH)

示例:
  node browser/submit-strategy.js ../../strategies/thsquant/rfscore7_base_800.py
  node browser/submit-strategy.js my_strategy.py --start 2024-01-01 --capital 500000
`);
    process.exit(1);
  }

  const config = {};
  const startIdx = args.indexOf('--start');
  if (startIdx !== -1) config.start_date = args[startIdx + 1];

  const endIdx = args.indexOf('--end');
  if (endIdx !== -1) config.end_date = args[endIdx + 1];

  const capitalIdx = args.indexOf('--capital');
  if (capitalIdx !== -1) config.capital_base = parseInt(args[capitalIdx + 1]);

  const benchmarkIdx = args.indexOf('--benchmark');
  if (benchmarkIdx !== -1) config.benchmark = args[benchmarkIdx + 1];

  const runner = new THSQuantStrategyRunner();

  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 策略提交工具');
  console.log('='.repeat(70));

  const result = await runner.submitAndRun(strategyArg, config);

  console.log('\n' + '='.repeat(70));
  if (result.success) {
    console.log('✓ 提交成功');
  } else {
    console.log('✗ 提交失败');
  }
  console.log('='.repeat(70));
}

main().catch(err => {
  console.error('\n错误:', err.message);
  process.exit(1);
});