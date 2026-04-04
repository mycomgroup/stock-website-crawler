import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36';

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

export function loadJson(filePath) {
  if (!fs.existsSync(filePath)) return {};
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch (e) { return {}; }
}

/**
 * THSQuant (同花顺 SuperMind) HTTP Client
 *
 * 已验证的 API 端点和参数格式（通过逆向工程确认）:
 *
 * 策略相关 (camelCase 参数):
 *   POST /platform/algorithms/queryinfo/   algoId=
 *   POST /platform/algorithms/update/      algoId= algo_name= code=
 *   POST /platform/algorithms/queryall2/   isajax=1
 *   POST /platform/algorithms/add/         algo_name= code= stock_market=
 *   POST /platform/algorithms/delete/      algo_id=
 *
 * 回测相关 (混合 camelCase):
 *   POST /platform/backtest/run/           algoId= beginDate= endDate= capitalBase= frequency= benchmark=
 *   POST /platform/backtest/queryinfo/     backTestId=   (注意 T 大写)
 *   POST /platform/backtest/backtestdetail/ backTestId=
 *   POST /platform/backtest/backtestperformance  backTestId=
 *   POST /platform/backtest/tradelog       backTestId=
 *   POST /platform/backtest/backtestlog/   backTestId=
 *   POST /platform/backtest/dailypositiongains  backTestId=
 *   POST /platform/backtest/backtestloop/  backTestId=
 *   POST /platform/backtest/backspecificinfo  backTestId= type=profit
 *   POST /platform/backtest/querylatest/   algoId= query=status
 *   POST /platform/backtest/queryall/      algo_id= page= num=
 *   POST /platform/backtest/cancel/        backTestId=
 */
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
    return Math.pow(2, retryCount) * 10000;
  }
  return 0;
}

/** 网络/超时错误的退避：5s / 10s / 20s */
function networkRetryDelay(retryCount) {
  return Math.pow(2, retryCount) * 5000;
}

export class THSQuantClient {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.outputRoot = path.resolve(options.outputRoot || OUTPUT_ROOT);
    this.origin = 'https://quant.10jqka.com.cn';
    const session = options.sessionPayload || loadJson(this.sessionFile);
    this.cookieJar = options.cookies || session.cookies || [];
  }

  getCookieHeader() {
    return this.cookieJar.map(c => `${c.name}=${c.value}`).join('; ');
  }

  buildHeaders(referer) {
    return {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Referer': referer || `${this.origin}/view/study-index.html`,
      'Origin': this.origin,
      'Cookie': this.getCookieHeader()
    };
  }

  async request(endpoint, body = 'isajax=1', retryCount = 0) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.origin}${endpoint}`;
    const maxRetries = 3;
    const timeoutMs = 30000;

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: this.buildHeaders(url),
        body: body.includes('isajax') ? body : body + '&isajax=1',
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
            return this.request(endpoint, body, retryCount + 1);
          }
        }
        throw new Error(`HTTP ${response.status} ${url}: ${text.slice(0, 200)}`);
      }

      // 解析 JSONP 或 JSON
      try {
        const trimmed = text.trim();
        if (trimmed.startsWith('(') && trimmed.endsWith(')')) {
          const m = trimmed.match(/\(\{.+\}\)/s);
          if (m) return JSON.parse(m[1]);
        }
        return JSON.parse(trimmed);
      } catch (e) {
        return { raw: text.slice(0, 500), parseError: e.message };
      }
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
        return this.request(endpoint, body, retryCount + 1);
      }
      throw error;
    }
  }

  // ─── 认证 ───────────────────────────────────────────────

  async checkLogin() {
    const data = await this.request('/platform/user/getauthdata');
    return {
      logged: data.errorcode === 0,
      userId: data.result?.user_id,
      data
    };
  }

  // ─── 策略管理 ────────────────────────────────────────────

  async listStrategies() {
    const data = await this.request('/platform/algorithms/queryall2/', 'isajax=1&datatype=jsonp');
    if (data.errorcode !== 0) throw new Error(data.errormsg || '获取策略列表失败');
    return (data.result?.strategys || []).map(s => ({
      id: s.algo_id,
      name: s.algo_name,
      backtestCount: s.backtest_number,
      latestBacktestId: s.backtest_id,
      modified: s.modified,
      raw: s
    }));
  }

  async getStrategyInfo(algoId) {
    // 注意: queryinfo 用 algoId (camelCase)
    const data = await this.request('/platform/algorithms/queryinfo/', `algoId=${algoId}&isajax=1`);
    if (data.errorcode !== 0) throw new Error(data.errormsg || '获取策略信息失败');
    return data.result;
  }

  /**
   * 获取策略上下文（对标 JoinQuant getStrategyContext）
   * THSQuant 不需要 CSRF token，直接返回策略信息
   */
  async getStrategyContext(algoId) {
    const info = await this.getStrategyInfo(algoId);
    const login = await this.checkLogin();
    return {
      algoId: info._id || algoId,
      name: info.algo_name,
      userId: login.userId,
      language: info.language,
      stockMarket: info.stock_market,
      raw: info
    };
  }

  async saveStrategy(algoId, name, code) {
    // update 用 algoId (camelCase)
    const body = new URLSearchParams({
      algoId,
      algo_name: name,
      code,
      isajax: '1'
    }).toString();
    const data = await this.request('/platform/algorithms/update/', body);
    return { success: data.errorcode === 0, message: data.errormsg, data };
  }

  async createStrategy(name, code = '', stockMarket = 'STOCK') {
    // 真实参数格式（从 JS 源码逆向）：algoName + stock_market + algoCode
    const body = new URLSearchParams({
      algoName: name,
      stock_market: stockMarket,
      algoCode: code,
      isajax: '1'
    }).toString();
    const data = await this.request('/platform/algorithms/add/', body);
    return {
      success: data.errorcode === 0,
      algoId: data.result?._id || data.result?.algo_id,
      message: data.errormsg,
      data
    };
  }

  async deleteStrategy(algoId) {
    const data = await this.request('/platform/algorithms/delete/', `algo_id=${algoId}&isajax=1`);
    return { success: data.errorcode === 0, message: data.errormsg };
  }

  // ─── 回测运行 ────────────────────────────────────────────

  /**
   * 运行回测
   * @param {string} algoId
   * @param {object} config - { beginDate, endDate, capitalBase, frequency, benchmark }
   */
  async runBacktest(algoId, config = {}) {
    const body = new URLSearchParams({
      algoId,
      beginDate: config.beginDate || config.startDate || config.start_date || '2023-01-01',
      endDate: config.endDate || config.end_date || '2024-12-31',
      capitalBase: String(config.capitalBase || config.capital_base || 100000),
      frequency: config.frequency || 'DAILY',
      benchmark: config.benchmark || '000300.SH',
      isajax: '1'
    }).toString();

    const data = await this.request('/platform/backtest/run/', body);
    if (data.errorcode !== 0) throw new Error(data.errormsg || '启动回测失败');

    // result 可能是 {backtest_id, progress} 或 {type:"ERROR", value:"..."}
    const result = data.result || {};
    if (result.type === 'ERROR') {
      throw new Error(`回测启动失败: ${result.value || '策略代码错误'}`);
    }

    return {
      backtestId: result.backtest_id,
      progress: result.progress || 0,
      data
    };
  }

  async cancelBacktest(backtestId) {
    const data = await this.request('/platform/backtest/cancel/', `backTestId=${backtestId}&isajax=1`);
    return { success: data.errorcode === 0, message: data.errormsg };
  }

  // ─── 回测状态轮询 ─────────────────────────────────────────

  /**
   * 轮询回测状态（用 backtestloop，最高效）
   */
  async pollBacktestStatus(backtestId) {
    const data = await this.request('/platform/backtest/backtestloop/', `backTestId=${backtestId}&isajax=1`);
    if (data.errorcode !== 0) return { status: 'ERROR', error: data.errormsg };
    return {
      status: data.result?.status,   // SUCCESS / RUNNING / FAILED / ERROR
      progress: data.result?.progress || 0,
      debug: data.result?.debug,
      raw: data.result
    };
  }

  /**
   * 等待回测完成（轮询直到 SUCCESS 或 FAILED）
   */
  async waitForBacktest(backtestId, { maxWait = 300000, interval = 3000, onProgress } = {}) {
    const start = Date.now();
    while (Date.now() - start < maxWait) {
      await new Promise(r => setTimeout(r, interval));
      const status = await this.pollBacktestStatus(backtestId);

      if (onProgress) onProgress(status);

      if (status.status === 'SUCCESS') return { success: true, status };
      if (status.status === 'FAILED' || status.status === 'ERROR') {
        return { success: false, status, error: status.error || '回测失败' };
      }
    }
    return { success: false, error: '回测超时' };
  }

  // ─── 回测结果 ────────────────────────────────────────────

  async getBacktestInfo(backtestId) {
    // backTestId (T 大写)
    const data = await this.request('/platform/backtest/queryinfo/', `backTestId=${backtestId}&isajax=1`);
    if (data.errorcode !== 0) throw new Error(data.errormsg || '获取回测信息失败');
    return data.result;
  }

  async getBacktestDetail(backtestId) {
    const data = await this.request('/platform/backtest/backtestdetail/', `backTestId=${backtestId}&isajax=1`);
    if (data.errorcode !== 0) throw new Error(data.errormsg || '获取回测详情失败');
    return data.result;
  }

  async getBacktestPerformance(backtestId) {
    const data = await this.request('/platform/backtest/backtestperformance', `backTestId=${backtestId}&isajax=1`);
    if (data.errorcode !== 0) throw new Error(data.errormsg || '获取回测绩效失败');
    return data.result;
  }

  async getTradeLog(backtestId) {
    const data = await this.request('/platform/backtest/tradelog', `backTestId=${backtestId}&isajax=1`);
    if (data.errorcode !== 0) return [];
    return data.result?.data || data.result || [];
  }

  async getBacktestLog(backtestId) {
    const data = await this.request('/platform/backtest/backtestlog/', `backTestId=${backtestId}&isajax=1`);
    if (data.errorcode !== 0) return [];
    return data.result?.list || data.result || [];
  }

  async getDailyPositionGains(backtestId) {
    const data = await this.request('/platform/backtest/dailypositiongains', `backTestId=${backtestId}&isajax=1`);
    if (data.errorcode !== 0) return [];
    return data.result?.data || data.result || [];
  }

  async getBacktestSpecificInfo(backtestId, type = 'profit') {
    const data = await this.request('/platform/backtest/backspecificinfo', `backTestId=${backtestId}&type=${type}&isajax=1`);
    if (data.errorcode !== 0) return null;
    return data.result;
  }

  async getRiskAnalysis(backtestId) {
    const data = await this.request('/platform/backtest/getriskanalysis', `backTestId=${backtestId}&isajax=1`);
    if (data.errorcode !== 0) return null;
    return data.result;
  }

  // ─── 回测历史 ────────────────────────────────────────────

  async getLatestBacktest(algoId) {
    const data = await this.request('/platform/backtest/querylatest/', `algoId=${algoId}&query=status&isajax=1`);
    if (data.errorcode !== 0) return null;
    return data.result;
  }

  async listBacktests(algoId, page = 1, num = 10) {
    // queryall 用 algo_id (snake_case)
    const data = await this.request('/platform/backtest/queryall/', `algo_id=${algoId}&page=${page}&num=${num}&isajax=1`);
    if (data.errorcode !== 0) return [];
    return data.result?.history || [];
  }

  // ─── 完整报告 ────────────────────────────────────────────

  /**
   * 获取完整回测报告（并行拉取所有数据）
   */
  async getFullReport(backtestId) {
    const [detail, performance, tradeLog, backtestLog, dailyGains, specificInfo] = await Promise.allSettled([
      this.getBacktestDetail(backtestId),
      this.getBacktestPerformance(backtestId),
      this.getTradeLog(backtestId),
      this.getBacktestLog(backtestId),
      this.getDailyPositionGains(backtestId),
      this.getBacktestSpecificInfo(backtestId, 'profit')
    ]);

    const get = r => r.status === 'fulfilled' ? r.value : null;

    return {
      backtestId,
      detail: get(detail),
      performance: get(performance),
      tradeLog: get(tradeLog),
      backtestLog: get(backtestLog),
      dailyGains: get(dailyGains),
      specificInfo: get(specificInfo)
    };
  }

  // ─── 工具 ────────────────────────────────────────────────

  writeArtifact(baseName, data, ext = 'json') {
    const filePath = path.join(this.outputRoot, `${baseName}-${Date.now()}.${ext}`);
    ensureDir(filePath);
    fs.writeFileSync(filePath, typeof data === 'string' ? data : JSON.stringify(data, null, 2), 'utf8');
    return filePath;
  }
}
