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
 * THSQuant (同花顺量化/SuperMind) API Client
 *
 * 实现与 JoinQuant/RiceQuant 相似的接口
 *
 * 已验证的API端点:
 * - /platform/user/getauthdata - 检查登录
 * - /platform/algorithms/queryall2/ - 策略列表
 * - /platform/simupaper/queryall/ - 模拟交易列表
 *
 * 待验证的API端点 (需要浏览器捕获):
 * - /platform/algorithms/add/ - 创建策略
 * - /platform/backtest/run/ - 运行回测
 * - /platform/backtest/result/ - 回测结果
 */
export class THSQuantClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.sessionPayload = options.sessionPayload || loadJson(this.sessionFile);
    this.origin = 'https://quant.10jqka.com.cn';
    this.cookieJar = options.cookies || this.sessionPayload.cookies || [];
  }

  getCookieHeader() {
    return this.cookieJar.map(c => `${c.name}=${c.value}`).join('; ');
  }

  buildHeaders(url, overrides = {}) {
    const headers = {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'X-Requested-With': 'XMLHttpRequest',
      'Referer': url,
      'Origin': this.origin,
      'Cookie': this.getCookieHeader(),
      ...overrides
    };
    return headers;
  }

  /**
   * 发送请求并解析JSONP响应
   */
  async request(url, options = {}) {
    const fullUrl = url.startsWith('http') ? url : `${this.origin}${url}`;

    const response = await fetch(fullUrl, {
      method: options.method || 'POST',
      headers: this.buildHeaders(fullUrl, options.headers),
      body: options.body || 'isajax=1'
    });

    const text = await response.text();

    if (!response.ok) {
      throw new Error(`Request failed ${response.status} ${fullUrl}: ${text.slice(0, 500)}`);
    }

    // 解析JSONP响应: jQuery183...( {...} );
    const jsonpMatch = text.match(/\((.+)\)/s);
    if (jsonpMatch) {
      try {
        return JSON.parse(jsonpMatch[1]);
      } catch (e) {
        // JSONP解析失败，尝试直接解析
      }
    }

    // 直接解析JSON
    try {
      return JSON.parse(text);
    } catch (e) {
      return { raw: text, error: 'parse_failed' };
    }
  }

  /**
   * 检查登录状态 (对应 JoinQuant checkLogin)
   */
  async checkLogin() {
    try {
      const data = await this.request('/platform/user/getauthdata');
      return {
        code: data.errorcode,
        logged: data.errorcode === 0,
        userId: data.result?.user_id,
        vip: data.result?.vip,
        data
      };
    } catch (e) {
      return { code: -1, logged: false, message: e.message };
    }
  }

  /**
   * 获取策略列表 (对应 JoinQuant listStrategies)
   */
  async listStrategies() {
    const data = await this.request('/platform/algorithms/queryall2/', {
      body: 'isajax=1&datatype=jsonp'
    });

    if (data.errorcode !== 0) {
      throw new Error(data.errormsg || '获取策略列表失败');
    }

    const strategies = data.result?.strategys || [];

    return strategies.map(s => ({
      id: s.algo_id,
      name: s.algo_name,
      backtestCount: s.backtest_number,
      modified: s.modified,
      raw: s
    }));
  }

  /**
   * 获取策略上下文 (对应 JoinQuant getStrategyContext)
   * THSQuant没有编辑页面token，直接返回策略基本信息
   */
  async getStrategyContext(strategyId) {
    // THSQuant没有单独的策略详情API，需要从列表中查找
    const strategies = await this.listStrategies();
    const strategy = strategies.find(s => s.id === strategyId);

    if (!strategy) {
      throw new Error(`策略不存在: ${strategyId}`);
    }

    return {
      strategyId: strategy.id,
      name: strategy.name,
      userId: await this.getUserId(),
      raw: strategy.raw
    };
  }

  /**
   * 获取用户ID
   */
  async getUserId() {
    const login = await this.checkLogin();
    return login.userId;
  }

  /**
   * 保存策略代码 (对应 JoinQuant saveStrategy)
   * 注意: 此API端点未完全验证，可能需要浏览器辅助
   */
  async saveStrategy(strategyId, name, code, context) {
    const userId = context?.userId || await this.getUserId();

    const body = new URLSearchParams({
      isajax: '1',
      user_id: userId,
      algo_id: strategyId,
      algo_name: name,
      code: code,
      stock_market: 'STOCK'
    }).toString();

    try {
      const data = await this.request('/platform/algorithms/edit/', { body });
      return {
        success: data.errorcode === 0,
        message: data.errormsg,
        data
      };
    } catch (e) {
      // 如果API失败，返回需要浏览器操作的提示
      return {
        success: false,
        message: e.message,
        requiresBrowser: true
      };
    }
  }

  /**
   * 运行回测 (对应 JoinQuant runBacktest)
   * 注意: 此API端点未完全验证，可能需要浏览器辅助
   */
  async runBacktest(strategyId, code, config, context) {
    const userId = context?.userId || await this.getUserId();

    const body = new URLSearchParams({
      isajax: '1',
      algo_id: strategyId,
      user_id: userId,
      start_date: config.startTime || config.start_date || '2023-01-01',
      end_date: config.endTime || config.end_date || '2024-12-31',
      capital_base: String(config.baseCapital || config.capital_base || 100000),
      frequency: config.frequency || 'DAILY',
      benchmark: config.benchmark || '000300.SH'
    }).toString();

    try {
      const data = await this.request('/platform/backtest/run/', { body });

      if (data.errorcode !== 0) {
        throw new Error(data.errormsg || '启动回测失败');
      }

      return {
        backtestId: data.result?.backtest_id || data.result?.id,
        success: true,
        data
      };
    } catch (e) {
      return {
        success: false,
        message: e.message,
        requiresBrowser: true
      };
    }
  }

  /**
   * 获取回测结果 (对应 JoinQuant getBacktestResult)
   */
  async getBacktestResult(backtestId, context = {}, offset = 0) {
    const body = new URLSearchParams({
      isajax: '1',
      backtest_id: backtestId,
      offset: String(offset)
    }).toString();

    try {
      const data = await this.request('/platform/backtest/result/', { body });
      return data;
    } catch (e) {
      return { error: e.message };
    }
  }

  /**
   * 获取回测列表 (对应 JoinQuant getBacktests)
   */
  async getBacktests(strategyId) {
    // THSQuant可能没有单独的回测列表API
    // 需要从策略详情获取
    const strategies = await this.listStrategies();
    const strategy = strategies.find(s => s.id === strategyId);

    return {
      strategyId,
      backtestCount: strategy?.backtestCount || 0,
      backtests: [] // 需要浏览器捕获真实API
    };
  }

  /**
   * 获取回测统计 (对应 JoinQuant getBacktestStats)
   */
  async getBacktestStats(backtestId, context = {}) {
    const result = await this.getBacktestResult(backtestId, context);

    // THSQuant的统计数据可能直接在result中
    return {
      backtestId,
      stats: result.result?.stats || result.stats || {},
      raw: result
    };
  }

  /**
   * 创建新策略 (对应 JoinQuant createStrategy)
   */
  async createStrategy(name, code = '') {
    const userId = await this.getUserId();

    const body = new URLSearchParams({
      isajax: '1',
      user_id: userId,
      algo_name: name,
      code: code,
      stock_market: 'STOCK'
    }).toString();

    try {
      const data = await this.request('/platform/algorithms/add/', { body });

      return {
        success: data.errorcode === 0,
        strategyId: data.result?.algo_id,
        message: data.errormsg,
        data
      };
    } catch (e) {
      return {
        success: false,
        message: e.message,
        requiresBrowser: true
      };
    }
  }

  /**
   * 删除策略
   */
  async deleteStrategy(strategyId) {
    const body = new URLSearchParams({
      isajax: '1',
      algo_id: strategyId
    }).toString();

    try {
      const data = await this.request('/platform/algorithms/delete/', { body });
      return {
        success: data.errorcode === 0,
        message: data.errormsg
      };
    } catch (e) {
      return { success: false, message: e.message };
    }
  }

  /**
   * 获取模拟交易列表
   */
  async listSimuPapers() {
    const data = await this.request('/platform/simupaper/queryall/', {
      body: 'isajax=1'
    });

    if (data.errorcode !== 0) {
      throw new Error(data.errormsg || '获取模拟交易列表失败');
    }

    return data.result || [];
  }

  /**
   * 获取完整回测报告 (对应 JoinQuant getFullReport)
   */
  async getFullReport(backtestId, context = {}) {
    console.log(`Generating full report for backtest ${backtestId}...`);

    const results = await Promise.allSettled([
      this.getBacktestResult(backtestId, context),
      this.getBacktestStats(backtestId, context)
    ]);

    const getValue = (r) => r.status === 'fulfilled' ? r.value : {};
    const [result, stats] = results.map(getValue);

    const resultData = result.result || result.data?.result || {};
    const statsData = stats.stats || {};

    return {
      backtestId,
      summary: statsData,
      backtest: resultData.backtest || {},
      benchmark: resultData.benchmark || {},
      equityCurve: resultData.overallReturn || resultData.equity_curve || {},
      transactions: resultData.transactions || [],
      positions: resultData.positions || [],
      log: resultData.log || [],
      raw: { result, stats }
    };
  }

  /**
   * 保存文件
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